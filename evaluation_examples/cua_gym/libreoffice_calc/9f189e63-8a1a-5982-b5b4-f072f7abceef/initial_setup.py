"""
Initial Setup: Import CSV file into LibreOffice Calc spreadsheet
Task ID: calc_adv_import_csv_041
Domain: libreoffice_calc

Creates:
  1. /home/user/Documents/sales_data.csv  — the CSV file to be imported
  2. /home/user/calc_adv_import_csv_041_initial.xlsx — empty spreadsheet (pre-import state)
"""

import os
import csv
import random
import datetime
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_adv_import_csv_041'
OUTPUT_XLSX = f'{WORKDIR}/{TASK_ID}_initial.xlsx'
OUTPUT_CSV = f'{WORKDIR}/Documents/sales_data.csv'

# ── Realistic data pools ────────────────────────────────────────────────────
REGIONS = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East']
PRODUCTS = [
    'Laptop Pro 15', 'Wireless Keyboard', 'USB-C Hub', 'Monitor 27"',
    'Mechanical Mouse', 'Webcam HD', 'Standing Desk', 'Office Chair',
    'Noise-Canceling Headphones', 'Portable SSD 1TB',
    'Graphics Card RTX 4070', 'Network Switch 24-Port', 'Tablet 10"',
    'Smartwatch Series 5', 'Bluetooth Speaker',
]
PRICE_RANGE = {
    'Laptop Pro 15': (899.99, 1299.99),
    'Wireless Keyboard': (49.99, 89.99),
    'USB-C Hub': (29.99, 59.99),
    'Monitor 27"': (299.99, 499.99),
    'Mechanical Mouse': (39.99, 79.99),
    'Webcam HD': (69.99, 119.99),
    'Standing Desk': (349.99, 599.99),
    'Office Chair': (199.99, 399.99),
    'Noise-Canceling Headphones': (149.99, 299.99),
    'Portable SSD 1TB': (89.99, 149.99),
    'Graphics Card RTX 4070': (549.99, 799.99),
    'Network Switch 24-Port': (199.99, 349.99),
    'Tablet 10"': (249.99, 449.99),
    'Smartwatch Series 5': (199.99, 349.99),
    'Bluetooth Speaker': (59.99, 129.99),
}


def random_date(start_year=2023, end_year=2025):
    """Generate a random date string in YYYY-MM-DD format."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    delta = (end - start).days
    return (start + datetime.timedelta(days=random.randint(0, delta))).strftime('%Y-%m-%d')


def generate_csv_data(num_rows=500):
    """Generate 500 rows of realistic sales data."""
    random.seed(42)  # reproducible
    rows = []
    for _ in range(num_rows):
        product = random.choice(PRODUCTS)
        lo, hi = PRICE_RANGE[product]
        price = round(random.uniform(lo, hi), 2)
        quantity = random.randint(1, 50)
        total = round(price * quantity, 2)
        rows.append({
            'Date': random_date(),
            'Region': random.choice(REGIONS),
            'Product': product,
            'Quantity': quantity,
            'Price': price,
            'Total': total,
        })
    return rows


def create_csv():
    """Create the sales_data.csv file in /home/user/Documents/."""
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    rows = generate_csv_data(500)
    fieldnames = ['Date', 'Region', 'Product', 'Quantity', 'Price', 'Total']
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f'CSV file created: {OUTPUT_CSV}  ({len(rows)} data rows + 1 header)')


def create_initial_xlsx():
    """Create an empty LibreOffice Calc spreadsheet (pre-import state)."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Sheet1'
    # Completely empty — the agent's job is to import the CSV data here
    wb.save(OUTPUT_XLSX)
    print(f'Initial spreadsheet created: {OUTPUT_XLSX}  (empty, ready for CSV import)')


# ── Main ─────────────────────────────────────────────────────────────────────
create_csv()
create_initial_xlsx()
print('Done.')
