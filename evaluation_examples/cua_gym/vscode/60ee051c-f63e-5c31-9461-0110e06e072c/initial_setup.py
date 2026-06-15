"""
Initial Setup: Create a Python project with app.py open in VSCode, no launch.json
Task ID: vscode_td_046
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_046'
PROJECT_DIR = f'{WORKDIR}/projects/python-basics'
APP_FILE = f'{PROJECT_DIR}/app.py'


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
    # Create the project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create a realistic app.py file
    app_content = '''"""
Simple inventory management system for a small bookstore.
"""

from datetime import datetime


class Book:
    def __init__(self, title, author, isbn, price, quantity):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.price = price
        self.quantity = quantity
        self.added_date = datetime.now()

    def __repr__(self):
        return f"Book('{self.title}' by {self.author}, ${self.price:.2f})"


class Inventory:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        for existing in self.books:
            if existing.isbn == book.isbn:
                existing.quantity += book.quantity
                return
        self.books.append(book)

    def remove_book(self, isbn):
        self.books = [b for b in self.books if b.isbn != isbn]

    def find_by_title(self, keyword):
        return [b for b in self.books if keyword.lower() in b.title.lower()]

    def find_by_author(self, author):
        return [b for b in self.books if author.lower() in b.author.lower()]

    def total_value(self):
        return sum(b.price * b.quantity for b in self.books)

    def low_stock(self, threshold=3):
        return [b for b in self.books if b.quantity <= threshold]

    def display_inventory(self):
        print(f"{'Title':<35} {'Author':<25} {'Price':>8} {'Qty':>5}")
        print("-" * 75)
        for b in self.books:
            print(f"{b.title:<35} {b.author:<25} ${b.price:>7.2f} {b.quantity:>5}")
        print(f"\\nTotal inventory value: ${self.total_value():,.2f}")


def main():
    inventory = Inventory()

    sample_books = [
        Book("The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565", 14.99, 8),
        Book("To Kill a Mockingbird", "Harper Lee", "978-0061120084", 12.99, 12),
        Book("1984", "George Orwell", "978-0451524935", 11.99, 5),
        Book("Pride and Prejudice", "Jane Austen", "978-0141439518", 9.99, 15),
        Book("The Catcher in the Rye", "J.D. Salinger", "978-0316769488", 13.99, 2),
        Book("Brave New World", "Aldous Huxley", "978-0060850524", 15.99, 1),
    ]

    for book in sample_books:
        inventory.add_book(book)

    print("=== Bookstore Inventory ===\\n")
    inventory.display_inventory()

    print("\\n=== Low Stock Alert ===")
    for book in inventory.low_stock():
        print(f"  WARNING: '{book.title}' only has {book.quantity} copies left")

    print("\\n=== Search Results for 'the' ===")
    results = inventory.find_by_title("the")
    for book in results:
        print(f"  Found: {book}")


if __name__ == "__main__":
    main()
'''
    with open(APP_FILE, 'w') as f:
        f.write(app_content)

    # Create a simple requirements.txt for realism
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write('# Bookstore inventory dependencies\nrequests>=2.28.0\npytest>=7.0.0\n')

    # Ensure NO .vscode/launch.json exists
    vscode_dir = f'{PROJECT_DIR}/.vscode'
    launch_json = f'{vscode_dir}/launch.json'
    if os.path.exists(launch_json):
        os.remove(launch_json)

    print(f'Project created at: {PROJECT_DIR}')
    print(f'App file created: {APP_FILE}')
    print(f'launch.json exists: {os.path.exists(launch_json)}')

    # Open VSCode with the project folder and app.py
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    launch_gui(f'code "{APP_FILE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
