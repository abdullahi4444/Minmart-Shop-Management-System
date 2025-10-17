import time
from rich.console import Console
from rich.table import Table
from rich import box
from rich.progress import track

def display_menu():
    print(r"""
            --- Available Products ---
                   Product Menu                   
┌────┬───────────────────────────────┬───────────┐
│ No │ Product                       │ Price ($) │
├────┼───────────────────────────────┼───────────┤
│ 1  │ 🍞 Bread                      │      2.00 │
│ 2  │ 🥛 Milk                       │      1.00 │
│ 3  │ 🥚 Eggs                       │      3.00 │
│ 4  │ ☕ Coffee                     │      5.00 │
│ 5  │ 🍎 Apple                      │      1.00 │
│ 6  │ 🍌 Banana                     │      1.00 │
│ 7  │ 🍊 Orange Juice               │      3.00 │
│ 8  │ 🥣 Cereal                     │      4.00 │
│ 9  │ 🧀 Cheese                     │      3.00 │
│ 10 │ 🍦 Yogurt                     │      1.00 │
│ 11 │ 🍗 Chicken Breast             │      7.00 │
│ 12 │ 🍚 Rice (1 lb)                │      1.00 │
│ 13 │ 🍝 Pasta                      │      2.00 │
│ 14 │ ✅ Done - Finish and Checkout │         - │
└────┴───────────────────────────────┴───────────┘""")

def get_price(item_number):
    prices = {
        1: 2.00,   # Bread
        2: 1.05,   # Milk
        3: 3.00,   # Eggs
        4: 5.00,   # Coffee
        5: 1.00,   # Apple
        6: 1.00,   # Banana
        7: 3.00,   # Orange Juice
        8: 4.00,   # Cereal
        9: 3.00,   # Cheese
        10: 1.00,  # Yogurt
        11: 7.00,  # Chicken Breast
        12: 1.00,  # Rice (1 lb)
        13: 2.00   # Pasta
    }
    return prices.get(item_number, 0)

def animate_checkout():
    for step in track(range(10), description="[green]Processing checkout..."):
        time.sleep(0.1)

def main():
    console = Console()
    cart = []
    display_menu()

    while True:
        try:
            choice = int(console.input("\n[bold cyan]Select an item by number (1-14): [/bold cyan]"))
            if choice == 14:
                break
            elif 1 <= choice <= 13:
                if choice in [8, 11, 12, 13]:
                    quantity = float(console.input(f"[cyan]Enter weight in kilograms for item {choice}: [/cyan]"))
                else: 
                    quantity = int(console.input(f"[cyan]Enter quantity for item {choice}: [/cyan]"))
                cart.append((choice, quantity))

            else:
                console.print("[bold red]Invalid selection, please choose a number between 1 and 14.[/bold red]")
        except ValueError:
            console.print("[bold red]Invalid input, please enter a number.[/bold red]")

    if not cart:
        console.print("[bold yellow]No items selected. Exiting.[/bold yellow]")
        return

    total = 0
    console.print("\n[bold green]--- Receipt ---[/bold green]")
    table = Table(title="Receipt", box=box.MINIMAL_DOUBLE_HEAD)
    table.add_column("Item", justify="left")
    table.add_column("Price ($)", justify="right")
    table.add_column("Quantity", justify="center")
    table.add_column("Total ($)", justify="right")

    for item, quantity in cart:
        item_price = get_price(item)
        item_name = [name for key, (name, price) in {
            1: ("🍞 Bread", 2.00),
            2: ("🥛 Milk", 1.00),
            3: ("🥚 Eggs", 3.00),
            4: ("☕ Coffee", 5.00),
            5: ("🍎 Apple", 1.00),
            6: ("🍌 Banana", 1.00),
            7: ("🍊 Orange Juice", 3.00),
            8: ("🥣 Cereal", 4.00),
            9: ("🧀 Cheese", 3.00),
            10: ("🍦 Yogurt", 1.00),
            11: ("🍗 Chicken Breast", 7.00),
            12: ("🍚 Rice (1 lb)", 1.00),
            13: ("🍝 Pasta", 2.00)
        }.items() if key == item][0]
        item_total = item_price * quantity
        total += item_total
        table.add_row(item_name, f"{item_price:.2f}", str(quantity), f"{item_total:.2f}")

    # Check for discount
    DISCOUNT_THRESHOLD = 150.00
    DISCOUNT_PERCENTAGE = 10  # 10% discount
    discount = 0
    if total >= DISCOUNT_THRESHOLD:
        discount = total * (DISCOUNT_PERCENTAGE / 100)
        console.print(f"\n[bold blue]Discount Applied: {DISCOUNT_PERCENTAGE}%[/bold blue] (${discount:.2f})")

    final_total = total - discount
    console.print(table)
    console.print(f"\n[bold green]Total Amount Before Discount: ${total:.2f}[/bold green]")

    if total >= DISCOUNT_THRESHOLD:
        console.print(f"[bold green]Total Amount After Discount: ${final_total:.2f}[/bold green]")

    # Payment process
    amount_due = final_total
    while amount_due > 0:
        try:
            # Prompt the user to enter the payment amount
            payment_input = console.input(f"[cyan]Enter payment amount (${amount_due:.2f} remaining): $[/cyan]")

            # Check if input is empty
            if payment_input == "":
                console.print("[bold red]Invalid input, please enter a valid amount.[/bold red]")
                continue

            # Convert input to a float
            payment = float(payment_input)
            
            # Check if the payment is valid (greater than 0)
            if payment <= 0:
                console.print("[bold red]Payment must be greater than 0.[/bold red]")
                continue

            # Round values to 2 decimal places to avoid floating-point issues
            payment = round(payment, 2)
            amount_due = round(amount_due, 2)

            # If the payment is less than or equal to the amount due, accept it
            if payment < amount_due:
                amount_due -= payment
                console.print(f"[bold yellow]Partial payment received. You still owe ${amount_due:.2f}[/bold yellow]")
                console.print(f"[bold green]Amount Paid: ${payment:.2f}, Remaining Amount: ${amount_due:.2f}[/bold green]")

            # If the payment is equal to the amount due, complete the payment
            elif payment == amount_due:
                amount_due = 0
                console.print(f"[bold green]Amount Paid: ${payment:.2f}, Remaining Amount: $0.00[/bold green]")

            # Reject overpayment
            else:
                console.print(f"[bold red]Payment exceeds the required amount of ${amount_due:.2f}. Please try again.[/bold red]")
                continue

        except ValueError:
            console.print("[bold red]Invalid input, please enter a valid numeric amount.[/bold red]")

    if amount_due == 0:
        console.print("[bold green]Thank you for your payment. Your transaction is complete![/bold green]")


while True:
    main()
