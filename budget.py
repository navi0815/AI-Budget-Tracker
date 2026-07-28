"""
budget.py - Simple Daily Expense Tracker

Lets you enter daily expenses through the terminal, saves them to a CSV
file using pandas, and shows a pie chart of spending by category using
matplotlib every time the script runs.

Usage:
    python budget.py
"""

import os
from datetime import date

import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE = "expenses.csv"
COLUMNS = ["Date", "Category", "Description", "Amount"]


def load_data():
    """Load existing expense data from CSV, or create an empty DataFrame."""
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=COLUMNS)


def save_data(df):
    """Save the DataFrame back to the CSV file."""
    df.to_csv(CSV_FILE, index=False)


def get_expense_input():
    """Ask the user for one expense entry via the terminal."""
    print("\n--- Add a new expense ---")

    category = input("Category (e.g. Food, Travel, Rent, Fun): ").strip().title()
    description = input("Description (e.g. Lunch, Bus ticket): ").strip()

    while True:
        amount_str = input("Amount spent: ").strip()
        try:
            amount = float(amount_str)
            if amount < 0:
                print("Amount can't be negative. Try again.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    entry_date = date.today().isoformat()

    return {
        "Date": entry_date,
        "Category": category if category else "Uncategorized",
        "Description": description if description else "-",
        "Amount": amount,
    }


def add_expenses(df):
    """Loop letting the user add multiple expenses in one run."""
    while True:
        new_entry = get_expense_input()
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)

        again = input("Add another expense? (y/n): ").strip().lower()
        if again != "y":
            break

    return df


def show_summary(df):
    """Print a quick text summary of spending by category."""
    if df.empty:
        print("\nNo expenses recorded yet.")
        return

    print("\n--- Spending Summary ---")
    summary = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    for category, total in summary.items():
        print(f"{category:<15} ₹{total:,.2f}")
    print(f"{'Total':<15} ₹{df['Amount'].sum():,.2f}")


def show_pie_chart(df):
    """Generate and display a pie chart of spending by category."""
    if df.empty:
        print("No data to plot yet. Add some expenses first!")
        return

    summary = df.groupby("Category")["Amount"].sum()

    plt.figure(figsize=(7, 7))
    plt.pie(
        summary.values,
        labels=summary.index,
        autopct="%1.1f%%",
        startangle=90,
    )
    plt.title("Expenses by Category")
    plt.axis("equal")  # keeps the pie chart circular
    plt.tight_layout()

    chart_file = "expense_pie_chart.png"
    plt.savefig(chart_file)
    print(f"\nPie chart saved as '{chart_file}'.")

    plt.show()


def main():
    print("=== Daily Expense Tracker ===")
    df = load_data()

    choice = input(
        "\nWhat do you want to do?\n"
        "  1. Add expense(s)\n"
        "  2. Just view chart/summary from saved data\n"
        "Enter choice (1/2): "
    ).strip()

    if choice == "1":
        df = add_expenses(df)
        save_data(df)
        print(f"\nSaved to '{CSV_FILE}'.")

    show_summary(df)
    show_pie_chart(df)


if __name__ == "__main__":
    main()