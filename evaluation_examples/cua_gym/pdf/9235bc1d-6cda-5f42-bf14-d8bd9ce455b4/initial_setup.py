"""
Initial Setup: Create a 40-page journal entries PDF for 2024.
The word 'adjustment' appears on pages 5, 12, 13, 21, 28, and 35 (1-indexed).
Task ID: pdf_fin_062
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import random

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_062'
FINANCE_DIR = f'{WORKDIR}/finance'
OUTPUT = f'{FINANCE_DIR}/journal_entries_2024.pdf'

# Pages that must contain the word 'adjustment' (1-indexed)
ADJUSTMENT_PAGES = {5, 12, 13, 21, 28, 35}

# Realistic account names for journal entries
ACCOUNTS = [
    "Cash", "Accounts Receivable", "Inventory", "Prepaid Insurance",
    "Equipment", "Accumulated Depreciation", "Accounts Payable",
    "Salaries Payable", "Unearned Revenue", "Common Stock",
    "Retained Earnings", "Service Revenue", "Sales Revenue",
    "Cost of Goods Sold", "Salaries Expense", "Rent Expense",
    "Utilities Expense", "Insurance Expense", "Depreciation Expense",
    "Office Supplies", "Notes Payable", "Interest Expense",
    "Interest Payable", "Dividends", "Advertising Expense",
    "Maintenance Expense", "Travel Expense", "Consulting Revenue",
    "Tax Expense", "Accrued Liabilities"
]

DESCRIPTIONS_NORMAL = [
    "Record monthly payroll for {dept} department",
    "Payment received from client {client}",
    "Purchase of office supplies from vendor",
    "Monthly rent payment for {location} office",
    "Invoice #{inv} for consulting services rendered",
    "Utility bill payment for {month} 2024",
    "Equipment purchase - {item}",
    "Revenue recognition for project #{proj}",
    "Vendor payment to {vendor} for materials",
    "Transfer between operating accounts",
    "Record {month} sales commission payments",
    "Insurance premium payment - quarterly",
    "Customer refund processed - order #{order}",
    "Monthly subscription revenue - SaaS platform",
    "Reimbursement for employee travel expenses",
]

DESCRIPTIONS_ADJUSTMENT = [
    "Year-end adjustment for accrued interest",
    "Adjustment entry - correct inventory valuation",
    "Period-end adjustment for prepaid insurance allocation",
    "Adjustment to depreciation schedule for Q{q} assets",
    "Revenue recognition adjustment per ASC 606 review",
    "Adjustment entry for unrealized foreign exchange gains",
    "Accrual adjustment for unbilled consulting services",
    "Adjustment to allowance for doubtful accounts",
    "Reclassification adjustment between expense categories",
    "Prior period adjustment for understated liabilities",
]

DEPARTMENTS = ["Engineering", "Marketing", "Sales", "Finance", "Operations", "HR"]
CLIENTS = ["Nextera Solutions", "Pinnacle Corp", "Meridian Holdings", "Cascade Industries",
           "Vertex Analytics", "Luminance Tech", "Frontier Systems", "Summit Partners"]
VENDORS = ["OfficeMax Pro", "TechDirect", "Global Supply Co", "Metro Logistics"]
LOCATIONS = ["downtown", "midtown", "westside", "corporate HQ"]
ITEMS = ["Dell Latitude 5540 laptop", "standing desk converters (x5)",
         "HP LaserJet Pro printer", "conference room AV system"]
MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


def rand_amount():
    return round(random.uniform(500, 85000), 2)


def format_amount(val):
    return f"${val:,.2f}"


def get_description(is_adjustment, page_idx):
    """Generate a realistic journal entry description."""
    random.seed(page_idx * 100 + 42)
    if is_adjustment:
        desc = random.choice(DESCRIPTIONS_ADJUSTMENT)
    else:
        desc = random.choice(DESCRIPTIONS_NORMAL)

    desc = desc.format(
        dept=random.choice(DEPARTMENTS),
        client=random.choice(CLIENTS),
        location=random.choice(LOCATIONS),
        inv=random.randint(10000, 99999),
        month=random.choice(MONTHS),
        item=random.choice(ITEMS),
        proj=random.randint(2000, 9999),
        vendor=random.choice(VENDORS),
        order=random.randint(50000, 99999),
        q=random.randint(1, 4),
    )
    return desc


def create_journal_page(doc, page_num):
    """Create a single journal entry page. page_num is 1-indexed."""
    random.seed(page_num * 37 + 7)
    is_adjustment = page_num in ADJUSTMENT_PAGES

    page = doc.new_page(width=612, height=792)  # Letter size
    shape = page.new_shape()

    # Header area
    page.insert_text(
        pymupdf.Point(72, 50),
        "GREENFIELD INDUSTRIES, INC.",
        fontsize=14, fontname="hebo", color=(0.1, 0.15, 0.35)
    )
    page.insert_text(
        pymupdf.Point(72, 68),
        "General Journal - Fiscal Year 2024",
        fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3)
    )

    # Page number
    page.insert_text(
        pymupdf.Point(540, 50),
        f"Page {page_num}",
        fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4)
    )

    # Horizontal rule under header
    shape.draw_line(pymupdf.Point(72, 78), pymupdf.Point(540, 78))
    shape.finish(color=(0.6, 0.6, 0.6), width=0.8)

    # Month/period label
    month_idx = ((page_num - 1) * 12) // 40
    month_name = MONTHS[month_idx]
    day_base = ((page_num - 1) % 28) + 1
    entry_date = f"{month_name} {day_base}, 2024"

    page.insert_text(
        pymupdf.Point(72, 100),
        f"Date: {entry_date}",
        fontsize=10, fontname="hebo", color=(0, 0, 0)
    )

    # Journal entry number
    je_num = f"JE-2024-{page_num:04d}"
    page.insert_text(
        pymupdf.Point(400, 100),
        f"Entry: {je_num}",
        fontsize=10, fontname="helv", color=(0, 0, 0)
    )

    # Description
    desc = get_description(is_adjustment, page_num)
    page.insert_text(
        pymupdf.Point(72, 125),
        f"Description: {desc}",
        fontsize=9, fontname="helv", color=(0.15, 0.15, 0.15)
    )

    # If this is an adjustment page, add a visible label
    if is_adjustment:
        page.insert_text(
            pymupdf.Point(72, 145),
            "Type: ADJUSTMENT ENTRY",
            fontsize=9, fontname="hebo", color=(0.6, 0.1, 0.1)
        )
        y_start = 170
    else:
        entry_type = random.choice(["STANDARD", "RECURRING", "CLOSING"])
        page.insert_text(
            pymupdf.Point(72, 145),
            f"Type: {entry_type} ENTRY",
            fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3)
        )
        y_start = 170

    # Table header
    headers = ["Account", "Description", "Debit", "Credit"]
    col_x = [72, 220, 400, 490]
    y = y_start

    # Draw header background
    shape.draw_rect(pymupdf.Rect(70, y - 12, 542, y + 5))
    shape.finish(color=(0.7, 0.75, 0.85), fill=(0.85, 0.88, 0.95), width=0.5)

    for i, h in enumerate(headers):
        page.insert_text(
            pymupdf.Point(col_x[i], y),
            h, fontsize=9, fontname="hebo", color=(0.1, 0.1, 0.3)
        )
    y += 20

    # Generate 4-8 line items per entry
    num_lines = random.randint(4, 8)
    total_debit = 0.0
    total_credit = 0.0
    lines = []

    for i in range(num_lines):
        acct = random.choice(ACCOUNTS)
        amt = rand_amount()
        if i < num_lines // 2:
            # Debit entry
            lines.append((acct, "Dr.", format_amount(amt), ""))
            total_debit += amt
        else:
            lines.append((acct, "Cr.", "", ""))
            total_credit += 0  # Will be balanced below

    # Balance the entry
    total_credit = total_debit
    credit_lines = [l for l in lines if l[2] == ""]
    per_credit = total_credit / max(len(credit_lines), 1)
    balanced_lines = []
    for l in lines:
        if l[2] == "":
            balanced_lines.append((l[0], "Cr.", "", format_amount(per_credit)))
        else:
            balanced_lines.append(l)

    # Draw line items
    for acct, direction, debit, credit in balanced_lines:
        indent = "    " if direction == "Cr." else ""
        page.insert_text(pymupdf.Point(col_x[0], y), f"{indent}{acct}", fontsize=8, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(col_x[1], y), direction, fontsize=8, fontname="helv", color=(0.3, 0.3, 0.3))
        if debit:
            page.insert_text(pymupdf.Point(col_x[2], y), debit, fontsize=8, fontname="helv", color=(0, 0, 0))
        if credit:
            page.insert_text(pymupdf.Point(col_x[3], y), credit, fontsize=8, fontname="helv", color=(0, 0, 0))
        y += 16

    # Totals line
    y += 8
    shape.draw_line(pymupdf.Point(390, y - 8), pymupdf.Point(542, y - 8))
    shape.finish(color=(0, 0, 0), width=0.5)

    page.insert_text(pymupdf.Point(col_x[0], y), "TOTALS", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(col_x[2], y), format_amount(total_debit), fontsize=9, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(col_x[3], y), format_amount(total_debit), fontsize=9, fontname="hebo", color=(0, 0, 0))

    y += 25

    # Additional notes section
    if is_adjustment:
        notes = [
            f"Adjustment reference: ADJ-{random.randint(100,999)}",
            f"Reviewed by: {random.choice(['Sarah Chen, CPA', 'David Park, Controller', 'Lisa Morales, CFO'])}",
            f"Approval date: {entry_date}",
            "This adjustment entry has been reviewed and approved per company policy.",
        ]
    else:
        notes = [
            f"Reference: REF-{random.randint(1000,9999)}",
            f"Posted by: {random.choice(['J. Williams', 'M. Thompson', 'K. Rodriguez', 'A. Patel'])}",
            f"Posting date: {entry_date}",
        ]

    page.insert_text(pymupdf.Point(72, y), "Notes:", fontsize=9, fontname="hebo", color=(0.2, 0.2, 0.2))
    y += 15
    for note in notes:
        page.insert_text(pymupdf.Point(82, y), note, fontsize=8, fontname="helv", color=(0.3, 0.3, 0.3))
        y += 13

    # Footer
    shape.draw_line(pymupdf.Point(72, 745), pymupdf.Point(540, 745))
    shape.finish(color=(0.8, 0.8, 0.8), width=0.5)

    page.insert_text(
        pymupdf.Point(72, 760),
        "Greenfield Industries, Inc. | Confidential | Generated from ERP System v4.2",
        fontsize=7, fontname="helv", color=(0.5, 0.5, 0.5)
    )
    page.insert_text(
        pymupdf.Point(480, 760),
        f"Page {page_num} of 40",
        fontsize=7, fontname="helv", color=(0.5, 0.5, 0.5)
    )

    shape.commit()


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
    os.makedirs(FINANCE_DIR, exist_ok=True)

    doc = pymupdf.open()

    for page_num in range(1, 41):
        create_journal_page(doc, page_num)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Total pages: 40')
    print(f'Pages with "adjustment": {sorted(ADJUSTMENT_PAGES)}')

    # Verify adjustment pages
    doc = pymupdf.open(OUTPUT)
    found_pages = []
    for i in range(doc.page_count):
        text = doc[i].get_text("text")
        if "adjustment" in text.lower():
            found_pages.append(i + 1)  # 1-indexed
    doc.close()
    print(f'Verified pages containing "adjustment": {found_pages}')

    # Open in Evince for the agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
