"""
Initial Setup: Expense tracker project with buggy IndexError crash on empty list deletion
Task ID: osworld_multi_apps_vscode_debug_crash_003
Domain: vscode / python debugging
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = '/home/user/Desktop/expense_tracker'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # --- storage.py ---
    storage_content = '''"""
storage.py — Persistent storage for expense records using a JSON file.
"""

import json
import os

STORAGE_FILE = os.path.join(os.path.dirname(__file__), "expenses.json")


def load_expenses():
    """Load expenses from disk. Returns a list of expense dicts."""
    if not os.path.exists(STORAGE_FILE):
        return []
    try:
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_expenses(expenses):
    """Persist the expenses list to disk."""
    with open(STORAGE_FILE, "w") as f:
        json.dump(expenses, f, indent=2)
'''

    # --- tracker.py — BUGGY version (IndexError when deleting from empty list) ---
    tracker_content = '''"""
tracker.py — Core logic for the expense tracker application.

Manages a list of expense records. Each expense is a dict with:
  - id (int): unique identifier
  - description (str): short description
  - amount (float): expense amount in USD
  - category (str): e.g. "Food", "Travel", "Office"
  - date (str): ISO date string "YYYY-MM-DD"
"""

from storage import load_expenses, save_expenses


class ExpenseTracker:
    def __init__(self):
        self.expenses = load_expenses()
        self._next_id = max((e["id"] for e in self.expenses), default=0) + 1

    # ------------------------------------------------------------------
    # CRUD operations
    # ------------------------------------------------------------------

    def add_expense(self, description, amount, category, date):
        """Add a new expense record."""
        expense = {
            "id": self._next_id,
            "description": description,
            "amount": float(amount),
            "category": category,
            "date": date,
        }
        self.expenses.append(expense)
        self._next_id += 1
        save_expenses(self.expenses)
        return expense

    def list_expenses(self):
        """Return a copy of all expenses."""
        return list(self.expenses)

    def get_expense(self, expense_id):
        """Retrieve a single expense by id, or None if not found."""
        for e in self.expenses:
            if e["id"] == expense_id:
                return e
        return None

    def update_expense(self, expense_id, **kwargs):
        """Update fields of an existing expense. Returns True on success."""
        for e in self.expenses:
            if e["id"] == expense_id:
                for k, v in kwargs.items():
                    if k in ("description", "amount", "category", "date"):
                        e[k] = v
                save_expenses(self.expenses)
                return True
        return False

    def delete_expense(self, expense_id):
        """Remove expense by id.

        BUG: Does not guard against an empty list.
        When self.expenses is empty, the list comprehension still runs but
        the original list index used elsewhere causes IndexError.
        """
        # BUG: Accessing index 0 without checking if list is empty first.
        # This crashes with IndexError when the list has no items.
        _ = self.expenses[0]  # <-- IndexError when list is empty
        original_len = len(self.expenses)
        self.expenses = [e for e in self.expenses if e["id"] != expense_id]
        if len(self.expenses) < original_len:
            save_expenses(self.expenses)
            return True
        return False

    # ------------------------------------------------------------------
    # Summary helpers
    # ------------------------------------------------------------------

    def total_by_category(self):
        """Return a dict mapping category -> total amount."""
        totals = {}
        for e in self.expenses:
            totals[e["category"]] = totals.get(e["category"], 0.0) + e["amount"]
        return totals

    def grand_total(self):
        """Return the sum of all expenses."""
        return sum(e["amount"] for e in self.expenses)
'''

    # --- ui.py ---
    ui_content = '''"""
ui.py — Simple text-based user interface for the expense tracker.
"""

from tracker import ExpenseTracker
from datetime import date


def print_menu():
    print("\\n========== Expense Tracker ==========")
    print("  1. List all expenses")
    print("  2. Add expense")
    print("  3. Delete expense")
    print("  4. Show totals by category")
    print("  5. Quit")
    print("======================================")


def list_expenses(tracker):
    expenses = tracker.list_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return
    print(f"\\n{'ID':<5} {'Date':<12} {'Category':<12} {'Amount':>10}  Description")
    print("-" * 60)
    for e in expenses:
        print(f"{e[\'id\']:<5} {e[\'date\']:<12} {e[\'category\']:<12} ${e[\'amount\']:>9.2f}  {e[\'description\']}")
    print(f"\\nGrand total: ${tracker.grand_total():.2f}")


def add_expense(tracker):
    print("\\n-- Add Expense --")
    description = input("Description: ").strip()
    if not description:
        print("Description cannot be empty.")
        return
    try:
        amount = float(input("Amount ($): ").strip())
    except ValueError:
        print("Invalid amount.")
        return
    category = input("Category (Food/Travel/Office/Other): ").strip() or "Other"
    date_str = input(f"Date (YYYY-MM-DD) [default: {date.today()}]: ").strip()
    if not date_str:
        date_str = str(date.today())
    expense = tracker.add_expense(description, amount, category, date_str)
    print(f"Added expense #{expense[\'id\']}: {expense[\'description\']} — ${expense[\'amount\']:.2f}")


def delete_expense(tracker):
    print("\\n-- Delete Expense --")
    try:
        expense_id = int(input("Enter expense ID to delete: ").strip())
    except ValueError:
        print("Invalid ID.")
        return
    success = tracker.delete_expense(expense_id)
    if success:
        print(f"Expense #{expense_id} deleted.")
    else:
        print(f"No expense found with ID {expense_id}.")


def show_totals(tracker):
    totals = tracker.total_by_category()
    if not totals:
        print("No expenses to summarize.")
        return
    print("\\n-- Totals by Category --")
    for category, total in sorted(totals.items()):
        print(f"  {category:<15} ${total:.2f}")
    print(f"  {\'TOTAL\':<15} ${tracker.grand_total():.2f}")


def run_ui():
    tracker = ExpenseTracker()
    while True:
        print_menu()
        choice = input("Select option: ").strip()
        if choice == "1":
            list_expenses(tracker)
        elif choice == "2":
            add_expense(tracker)
        elif choice == "3":
            delete_expense(tracker)
        elif choice == "4":
            show_totals(tracker)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-5.")
'''

    # --- main.py ---
    main_content = '''"""
main.py — Entry point for the expense tracker application.
"""

from ui import run_ui

if __name__ == "__main__":
    run_ui()
'''

    # Write all project files
    with open(os.path.join(PROJECT_DIR, 'storage.py'), 'w') as f:
        f.write(storage_content)
    print(f'Created: {PROJECT_DIR}/storage.py')

    with open(os.path.join(PROJECT_DIR, 'tracker.py'), 'w') as f:
        f.write(tracker_content)
    print(f'Created: {PROJECT_DIR}/tracker.py')

    with open(os.path.join(PROJECT_DIR, 'ui.py'), 'w') as f:
        f.write(ui_content)
    print(f'Created: {PROJECT_DIR}/ui.py')

    with open(os.path.join(PROJECT_DIR, 'main.py'), 'w') as f:
        f.write(main_content)
    print(f'Created: {PROJECT_DIR}/main.py')

    # Create a pre-populated expenses.json with some initial data
    import json
    sample_expenses = [
        {"id": 1, "description": "Team lunch at Sakura Bistro", "amount": 87.50, "category": "Food", "date": "2025-03-10"},
        {"id": 2, "description": "Flight to client site (SFO-LAX)", "amount": 214.00, "category": "Travel", "date": "2025-03-12"},
        {"id": 3, "description": "Printer ink cartridges", "amount": 34.99, "category": "Office", "date": "2025-03-14"},
        {"id": 4, "description": "Conference registration fee", "amount": 450.00, "category": "Travel", "date": "2025-03-15"},
        {"id": 5, "description": "Client dinner at The Grillhouse", "amount": 163.75, "category": "Food", "date": "2025-03-18"},
    ]
    with open(os.path.join(PROJECT_DIR, 'expenses.json'), 'w') as f:
        json.dump(sample_expenses, f, indent=2)
    print(f'Created: {PROJECT_DIR}/expenses.json')

    # GUI-ready startup: open VSCode with the expense_tracker folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with expense_tracker folder (DISPLAY=:0)')


create_initial()
