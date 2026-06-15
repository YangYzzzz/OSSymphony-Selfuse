"""
Initial Setup: Expense Dashboard Multi-App Task
Task ID: osworld_multi_apps_code_script_output_009
Domain: libreoffice_calc (multi-app: terminal, python scripts, file management)
Creates: /home/user/data/expenses.ods with 60 rows of realistic expense data
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_script_output_009'
DATA_DIR = f'{WORKDIR}/data'
SCRIPTS_DIR = f'{WORKDIR}/scripts'
ODS_OUTPUT = f'{DATA_DIR}/expenses.ods'


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
    # Create required directories
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)

    # Define 60 rows of realistic expense data across 3 months (Jan-Mar 2025)
    # Columns: date, category, amount, description
    expenses = [
        # January 2025
        ('2025-01-02', 'Housing',       1850.00, 'Monthly rent payment'),
        ('2025-01-03', 'Food',            85.40, 'Weekly grocery run at Whole Foods'),
        ('2025-01-04', 'Transport',        42.50, 'Monthly bus pass'),
        ('2025-01-05', 'Utilities',       120.30, 'Electricity bill - January'),
        ('2025-01-06', 'Food',             32.75, 'Lunch at Noodle House'),
        ('2025-01-07', 'Entertainment',    18.99, 'Netflix monthly subscription'),
        ('2025-01-08', 'Healthcare',       45.00, 'GP consultation copay'),
        ('2025-01-09', 'Food',             67.20, 'Supermarket - weekly groceries'),
        ('2025-01-11', 'Transport',        28.00, 'Uber rides - weekend'),
        ('2025-01-12', 'Entertainment',    55.00, 'Concert tickets - jazz night'),
        ('2025-01-13', 'Food',             24.50, 'Dinner at Italian Bistro'),
        ('2025-01-14', 'Education',        99.00, 'Online Python course - Udemy'),
        ('2025-01-15', 'Food',             78.90, 'Weekly grocery run at Trader Joe\'s'),
        ('2025-01-16', 'Utilities',        65.00, 'Internet and phone bill'),
        ('2025-01-18', 'Transport',        15.00, 'Parking fees - downtown'),
        ('2025-01-20', 'Healthcare',      120.00, 'Dental cleaning appointment'),
        ('2025-01-21', 'Food',             41.30, 'Lunch and coffee - work meetings'),
        ('2025-01-23', 'Entertainment',    22.00, 'Movie tickets - IMAX'),
        ('2025-01-25', 'Food',             92.40, 'Supermarket - bi-weekly stock-up'),
        ('2025-01-28', 'Transport',        35.00, 'Taxi to airport'),
        # February 2025
        ('2025-02-01', 'Housing',       1850.00, 'Monthly rent payment'),
        ('2025-02-02', 'Utilities',       108.50, 'Electricity bill - February'),
        ('2025-02-03', 'Food',             73.60, 'Weekly groceries at Costco'),
        ('2025-02-05', 'Transport',        42.50, 'Monthly bus pass renewal'),
        ('2025-02-06', 'Healthcare',       35.00, 'Prescription refill - allergy meds'),
        ('2025-02-07', 'Food',             29.80, 'Sushi dinner with friend'),
        ('2025-02-08', 'Entertainment',    14.99, 'Spotify Premium monthly'),
        ('2025-02-09', 'Entertainment',    45.00, 'Museum annual membership'),
        ('2025-02-10', 'Food',             58.20, 'Weekly grocery run'),
        ('2025-02-12', 'Transport',        22.00, 'Rideshare - evening out'),
        ('2025-02-14', 'Entertainment',   125.00, 'Valentine\'s Day dinner - The Oak Room'),
        ('2025-02-15', 'Food',             44.70, 'Brunch - weekend farmers market'),
        ('2025-02-17', 'Education',        49.00, 'AWS Cloud Practitioner study guide'),
        ('2025-02-18', 'Healthcare',       80.00, 'Eye exam and new glasses deposit'),
        ('2025-02-19', 'Food',             81.30, 'Supermarket - weekly stock'),
        ('2025-02-20', 'Utilities',        55.00, 'Gas bill - February'),
        ('2025-02-22', 'Transport',        18.50, 'Subway weekly card top-up'),
        ('2025-02-24', 'Food',             36.40, 'Thai restaurant - team lunch'),
        ('2025-02-26', 'Entertainment',    30.00, 'Comedy club tickets'),
        ('2025-02-28', 'Food',             62.10, 'End of month grocery run'),
        # March 2025
        ('2025-03-01', 'Housing',       1850.00, 'Monthly rent payment'),
        ('2025-03-02', 'Food',             88.50, 'Weekly groceries at Whole Foods'),
        ('2025-03-03', 'Transport',        42.50, 'Monthly bus pass'),
        ('2025-03-04', 'Utilities',       115.80, 'Electricity bill - March'),
        ('2025-03-05', 'Healthcare',       60.00, 'Physical therapy session'),
        ('2025-03-06', 'Food',             27.90, 'Coffee shop - remote work day'),
        ('2025-03-07', 'Entertainment',    18.99, 'Netflix monthly subscription'),
        ('2025-03-08', 'Education',        79.00, 'Data Science bootcamp - module 3'),
        ('2025-03-09', 'Food',             69.40, 'Sunday grocery shopping'),
        ('2025-03-11', 'Transport',        32.00, 'Car rental - weekend trip'),
        ('2025-03-12', 'Entertainment',    40.00, 'Theatre tickets - matinee'),
        ('2025-03-13', 'Food',             54.60, 'Dinner - Mexican restaurant'),
        ('2025-03-14', 'Utilities',        62.00, 'Internet and phone bill - March'),
        ('2025-03-15', 'Healthcare',       95.00, 'Specialist referral consultation'),
        ('2025-03-17', 'Food',             76.80, 'Weekly grocery run at Trader Joe\'s'),
        ('2025-03-19', 'Transport',        25.00, 'Parking permit - monthly office lot'),
        ('2025-03-21', 'Entertainment',    65.00, 'Art gallery opening event'),
        ('2025-03-23', 'Food',             48.20, 'Lunch with client - Cafe Central'),
        ('2025-03-26', 'Education',        35.00, 'Technical book - Clean Architecture'),
        ('2025-03-29', 'Food',             83.70, 'End of quarter grocery stock-up'),
    ]

    # Write ODS file using odfpy
    from odf.opendocument import OpenDocumentSpreadsheet
    from odf.table import Table, TableRow, TableCell
    from odf.text import P
    from odf.style import Style, TableCellProperties, TextProperties
    from odf import style

    doc = OpenDocumentSpreadsheet()

    # Create table (sheet)
    table = Table(name="Expenses")

    # Header row
    headers = ['date', 'category', 'amount', 'description']
    header_row = TableRow()
    for h in headers:
        cell = TableCell(valuetype="string")
        cell.addElement(P(text=str(h)))
        header_row.addElement(cell)
    table.addElement(header_row)

    # Data rows
    for (date, category, amount, description) in expenses:
        row = TableRow()

        # date cell (string)
        cell_date = TableCell(valuetype="string")
        cell_date.addElement(P(text=str(date)))
        row.addElement(cell_date)

        # category cell (string)
        cell_cat = TableCell(valuetype="string")
        cell_cat.addElement(P(text=str(category)))
        row.addElement(cell_cat)

        # amount cell (float)
        cell_amt = TableCell(valuetype="float", value=str(amount))
        cell_amt.addElement(P(text=str(amount)))
        row.addElement(cell_amt)

        # description cell (string)
        cell_desc = TableCell(valuetype="string")
        cell_desc.addElement(P(text=str(description)))
        row.addElement(cell_desc)

        table.addElement(row)

    doc.spreadsheet.addElement(table)
    doc.save(ODS_OUTPUT)
    print(f'Initial file created: {ODS_OUTPUT}')
    print(f'  - 60 rows of expense data across 3 months (Jan-Mar 2025)')
    print(f'  - Columns: date, category, amount, description')
    print(f'  - Categories: Housing, Food, Transport, Utilities, Healthcare, Entertainment, Education')
    print(f'  - NO expenses.csv (agent must export it)')
    print(f'  - NO expense_dashboard.py script (agent must write it)')
    print(f'  - NO expense_summary.csv (agent must generate it)')
    print(f'  - NO chart PNGs on Desktop (agent must generate them)')

    # GUI-ready startup: open LibreOffice Calc with the ODS file
    time.sleep(1.0)
    launch_gui(f'libreoffice --calc "{ODS_OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Calc with expenses.ods on DISPLAY=:0')


create_initial()
