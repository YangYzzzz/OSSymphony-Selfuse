"""
Initial Setup: Inventory Analysis - Partial Script with Stubs
Task ID: osworld_multi_apps_code_script_output_007
Domain: libreoffice_calc + os (multi-app)

Creates:
  - /home/user/data/inventory.csv (25 items, 4 categories)
  - /home/user/scripts/inventory.py (function stubs, NOT implemented)
  - /home/user/data/inventory.ods (Sheet1 with raw data, Sheet2 blank)

Then opens:
  - inventory.ods in LibreOffice Calc
  - inventory.py in gedit (text editor)
"""

import os
import shlex
import subprocess
import time

# Install odfpy if needed
try:
    from odf.opendocument import OpenDocumentSpreadsheet
except ImportError:
    subprocess.run(["pip3", "install", "odfpy"], check=True)
    from odf.opendocument import OpenDocumentSpreadsheet

from odf.opendocument import OpenDocumentSpreadsheet
from odf.table import Table, TableRow, TableCell
from odf.text import P

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_script_output_007'
DATA_DIR = f'{WORKDIR}/data'
SCRIPTS_DIR = f'{WORKDIR}/scripts'
CSV_PATH = f'{DATA_DIR}/inventory.csv'
SCRIPT_PATH = f'{SCRIPTS_DIR}/inventory.py'
ODS_PATH = f'{DATA_DIR}/inventory.ods'


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


def make_cell(value):
    """Create an ODS table cell with the given value."""
    if isinstance(value, (int, float)):
        tc = TableCell(valuetype='float', value=str(value))
        tc.addElement(P(text=str(value)))
    else:
        tc = TableCell(valuetype='string')
        tc.addElement(P(text=str(value)))
    return tc


def create_initial():
    # Create directories
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(SCRIPTS_DIR, exist_ok=True)

    # ---------------------------------------------------------------
    # 1. Create inventory.csv (25 items, 4 categories)
    # ---------------------------------------------------------------
    inventory_data = [
        # (item, category, quantity, unit_price)
        ('Laptop Pro 15', 'Electronics', 12, 899.99),
        ('Wireless Mouse', 'Electronics', 45, 29.99),
        ('USB Hub 7-Port', 'Electronics', 30, 24.99),
        ('Monitor 27 inch', 'Electronics', 8, 349.99),
        ('Keyboard Mechanical', 'Electronics', 20, 89.99),
        ('Webcam HD 1080p', 'Electronics', 15, 59.99),
        ('Headset Noise Cancel', 'Electronics', 10, 129.99),
        ('Printer Laser Color', 'Office', 5, 299.99),
        ('Scanner Flatbed A4', 'Office', 7, 149.99),
        ('Shredder 10-Sheet', 'Office', 9, 79.99),
        ('Label Maker Pro', 'Office', 18, 44.99),
        ('Stapler Heavy Duty', 'Office', 40, 12.99),
        ('Paper Ream A4', 'Office', 200, 4.99),
        ('Ergonomic Chair', 'Furniture', 6, 399.99),
        ('Standing Desk Adj', 'Furniture', 4, 549.99),
        ('Bookshelf 5-Tier', 'Furniture', 11, 89.99),
        ('Filing Cabinet 3D', 'Furniture', 8, 159.99),
        ('Monitor Stand Dual', 'Furniture', 22, 49.99),
        ('Desk Mat Large', 'Furniture', 35, 19.99),
        ('Sticky Notes Pack', 'Supplies', 150, 1.49),
        ('Pen Set Blue 12pk', 'Supplies', 80, 7.99),
        ('Highlighter Set 8c', 'Supplies', 60, 5.99),
        ('Notebook Spiral A5', 'Supplies', 90, 3.99),
        ('Tape Dispenser', 'Supplies', 25, 8.99),
        ('Scissors Professional', 'Supplies', 35, 11.99),
    ]

    csv_lines = ['item,category,quantity,unit_price']
    for item, cat, qty, price in inventory_data:
        csv_lines.append(f'{item},{cat},{qty},{price}')

    with open(CSV_PATH, 'w') as f:
        f.write('\n'.join(csv_lines) + '\n')
    print(f'Created: {CSV_PATH} ({len(inventory_data)} items)')

    # ---------------------------------------------------------------
    # 2. Create inventory.py with function STUBS (NOT implemented)
    # ---------------------------------------------------------------
    script_content = '''#!/usr/bin/env python3
"""
Inventory Analysis Script
Reads inventory.csv and generates a report.
"""

import csv


def load_data(filepath):
    """Load inventory data from CSV file."""
    data = []
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['quantity'] = int(row['quantity'])
            row['unit_price'] = float(row['unit_price'])
            data.append(row)
    return data


def low_stock_items(data, threshold):
    """
    Return a list of items where quantity is below the threshold.

    Args:
        data: list of dicts with inventory rows
        threshold: integer, items with quantity < threshold are low stock

    Returns:
        list of dicts for low-stock items
    """
    # TODO: implement this function
    pass


def category_totals(data):
    """
    Return a dict mapping each category to the total quantity of items in it.

    Args:
        data: list of dicts with inventory rows

    Returns:
        dict {category: total_quantity}
    """
    # TODO: implement this function
    pass


def reorder_cost(low_stock, unit_price_col):
    """
    Calculate total reorder cost for low-stock items.
    Reorder quantity = 50 - current quantity (to bring stock to 50).

    Args:
        low_stock: list of low-stock item dicts
        unit_price_col: string, name of the unit price column

    Returns:
        float, total reorder cost
    """
    # TODO: implement this function
    pass


def main():
    data_path = '/home/user/data/inventory.csv'
    data = load_data(data_path)

    print("=== Inventory Report ===")
    print(f"Total items loaded: {len(data)}")
    print()

    # Low stock analysis (threshold=10)
    low = low_stock_items(data, 10)
    print(f"Low stock items (qty < 10): {len(low)}")
    for item in low:
        print(f"  - {item['item']}: {item['quantity']} units @ ${item['unit_price']:.2f}")
    print()

    # Category totals
    totals = category_totals(data)
    print("Category totals (by quantity):")
    for cat, total in sorted(totals.items()):
        print(f"  {cat}: {total} units")
    print()

    # Reorder cost
    cost = reorder_cost(low, 'unit_price')
    print(f"Total reorder cost (to bring low-stock to 50 units): ${cost:.2f}")
    print()

    # Total inventory value
    total_value = sum(row['quantity'] * row['unit_price'] for row in data)
    print(f"Total inventory value: ${total_value:.2f}")


if __name__ == '__main__':
    main()
'''

    with open(SCRIPT_PATH, 'w') as f:
        f.write(script_content)
    os.chmod(SCRIPT_PATH, 0o755)
    print(f'Created: {SCRIPT_PATH} (with function stubs)')

    # ---------------------------------------------------------------
    # 3. Create inventory.ods (Sheet1 with raw data, Sheet2 blank)
    # ---------------------------------------------------------------
    doc = OpenDocumentSpreadsheet()

    # Sheet1: Raw inventory data
    sheet1 = Table(name="Sheet1")
    doc.spreadsheet.addElement(sheet1)

    # Header row
    header_row = TableRow()
    sheet1.addElement(header_row)
    for h in ['item', 'category', 'quantity', 'unit_price']:
        header_row.addElement(make_cell(h))

    # Data rows
    for item, cat, qty, price in inventory_data:
        row = TableRow()
        sheet1.addElement(row)
        row.addElement(make_cell(item))
        row.addElement(make_cell(cat))
        row.addElement(make_cell(qty))
        row.addElement(make_cell(price))

    # Sheet2: Blank (agent will enter total inventory value in A1)
    sheet2 = Table(name="Sheet2")
    doc.spreadsheet.addElement(sheet2)
    # Sheet2 is intentionally left blank

    doc.save(ODS_PATH)
    print(f'Created: {ODS_PATH} (Sheet1 with {len(inventory_data)} rows, Sheet2 blank)')

    # ---------------------------------------------------------------
    # 4. GUI-ready startup
    # ---------------------------------------------------------------
    # Open inventory.ods in LibreOffice Calc
    launch_gui(f'libreoffice --calc "{ODS_PATH}"', delay_sec=3.0)

    # Open inventory.py in gedit so agent can edit the script
    launch_gui(f'gedit "{SCRIPT_PATH}"', delay_sec=2.0)

    print('GUI_READY: launched LibreOffice Calc and gedit with DISPLAY=:0')


create_initial()
