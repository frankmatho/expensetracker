import csv
import os
from datetime import date

FILE_NAME = "expenses.csv"

CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Entertainment",
    "Health",
    "Utilities",
    "Other"
]


def initialize_file():
    """Create the CSV file with headers if it doesn't exist."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "category", "amount", "description"])
        print(f"Created new file: {FILE_NAME}")


def add_expense():
    """Add a new expense entry."""
    print("\n--- Add New Expense ---")

    # Get the date
    today = str(date.today())
    date_input = input(f"Date (press Enter for today [{today}]): ").strip()
    if date_input == "":
        date_input = today

    # Get the category
    print("\nCategories:")
    for i, category in enumerate(CATEGORIES, 1):
        print(f"  {i}. {category}")
    while True:
        choice = input("Choose category number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            category = CATEGORIES[int(choice) - 1]
            break
        print("Invalid choice. Please enter a number from the list.")

    # Get the amount
    while True:
        amount_input = input("Amount (KSh): ").strip()
        try:
            amount = float(amount_input)
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a number.")

    # Get the description
    description = input("Description (optional): ").strip()

    # Save to CSV
    with open(FILE_NAME, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date_input, category, amount, description])

    print(f"\n✅ Expense added: {category} - KSh {amount:.2f} on {date_input}")


def view_all_expenses():
    """Display all expenses in a formatted table."""
    print("\n--- All Expenses ---")
    expenses = load_expenses()

    if not expenses:
        print("No expenses recorded yet.")
        return

    print(f"\n{'Date':<12} {'Category':<15} {'Amount (KSh)':<15} {'Description'}")
    print("-" * 60)

    total = 0.0
    for row in expenses:
        date_val = row["date"]
        category = row["category"]
        amount = float(row["amount"])
        description = row["description"]
        total += amount
        print(f"{date_val:<12} {category:<15} {amount:<15.2f} {description}")

    print("-" * 60)
    print(f"{'TOTAL':<12} {'':<15} KSh {total:.2f}")


def view_summary():
    """Show total spent per category."""
    print("\n--- Spending Summary by Category ---")
    expenses = load_expenses()

    if not expenses:
        print("No expenses recorded yet.")
        return

    totals = {}
    grand_total = 0.0

    for row in expenses:
        category = row["category"]
        amount = float(row["amount"])
        totals[category] = totals.get(category, 0.0) + amount
        grand_total += amount

    print(f"\n{'Category':<20} {'Total (KSh)':<15} {'% of Spending'}")
    print("-" * 50)

    for category, total in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        percentage = (total / grand_total) * 100
        print(f"{category:<20} {total:<15.2f} {percentage:.1f}%")

    print("-" * 50)
    print(f"{'GRAND TOTAL':<20} KSh {grand_total:.2f}")


def load_expenses():
    """Load all expenses from the CSV file and return as list of dicts."""
    expenses = []
    if not os.path.exists(FILE_NAME):
        return expenses

    with open(FILE_NAME, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            expenses.append(row)

    return expenses


def main():
    """Main program loop."""
    initialize_file()

    print("============================")
    print("  Personal Expense Tracker  ")
    print("============================")

    while True:
        print("\nWhat would you like to do?")
        print("  1. Add an expense")
        print("  2. View all expenses")
        print("  3. View summary by category")
        print("  4. Exit")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_all_expenses()
        elif choice == "3":
            view_summary()
        elif choice == "4":
            print("\nGoodbye! Keep tracking those expenses ")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()