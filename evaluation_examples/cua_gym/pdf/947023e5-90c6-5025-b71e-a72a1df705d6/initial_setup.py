"""
Initial Setup: Create a 10-page expense report PDF with 18 credit card numbers
Task ID: pdf_fin_019
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_019'
FINANCE_DIR = f'{WORKDIR}/finance'
OUTPUT = f'{FINANCE_DIR}/expense_report_q1.pdf'

# Page dimensions (Letter)
W, H = 612, 792

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

# Credit card numbers to embed (18 total)
# Mix of XXXX-XXXX-XXXX-XXXX and XXXXXXXXXXXXXXXX formats
CC_NUMBERS = [
    # Dashed format (10)
    "4532-8891-2045-6673",
    "5214-7730-4489-1126",
    "3782-0641-5598-3347",
    "6011-4922-8836-7715",
    "4916-3378-5502-9941",
    "5105-2244-6633-8807",
    "4024-0071-8845-2293",
    "3714-4963-5398-4310",
    "6221-2612-0000-5877",
    "4485-7920-1134-6658",
    # Continuous format (8)
    "5287334410926643",
    "4539281074563921",
    "6011553498726140",
    "3787344936710005",
    "4916028754213680",
    "5432109876543210",
    "4111222233334444",
    "6504321098765432",
]

# Expense data per page - each page covers different expense categories
PAGES_DATA = [
    {
        "title": "Q1 2025 Expense Report - Meridian Consulting Group",
        "subtitle": "Corporate Travel Expenses - January 2025",
        "employee": "Sarah Chen - Senior Consultant",
        "dept": "Strategic Advisory Division",
        "entries": [
            ("Jan 05", "Delta Airlines - SFO to JFK", "$1,247.80", CC_NUMBERS[0]),
            ("Jan 06", "Marriott Times Square - 3 nights", "$1,892.45", CC_NUMBERS[1]),
        ],
    },
    {
        "title": "Q1 2025 Expense Report - Meridian Consulting Group",
        "subtitle": "Client Entertainment - January 2025",
        "employee": "Marcus Johnson - Managing Director",
        "dept": "Business Development",
        "entries": [
            ("Jan 10", "Eleven Madison Park - Client dinner (6 pax)", "$2,340.00", CC_NUMBERS[2]),
            ("Jan 18", "Club Suite - Barclays Center event tickets", "$1,580.00", CC_NUMBERS[3]),
        ],
    },
    {
        "title": "Q1 2025 Expense Report - Meridian Consulting Group",
        "subtitle": "Office Supplies & Equipment - January 2025",
        "employee": "Priya Ramirez - Operations Manager",
        "dept": "Operations",
        "entries": [
            ("Jan 12", "Apple Store - MacBook Pro M3 Max", "$3,499.00", CC_NUMBERS[4]),
            ("Jan 15", "Staples - Printer cartridges & paper (bulk)", "$487.25", CC_NUMBERS[5]),
        ],
    },
    {
        "title": "Q1 2025 Expense Report - Meridian Consulting Group",
        "subtitle": "Corporate Travel Expenses - February 2025",
        "employee": "James O'Brien - VP of Sales",
        "dept": "Revenue Operations",
        "entries": [
            ("Feb 02", "United Airlines - ORD to LAX first class", "$2,815.00", CC_NUMBERS[6]),
            ("Feb 03", "Four Seasons Beverly Hills - 4 nights", "$4,120.00", CC_NUMBERS[7]),
        ],
    },
    {
        "title": "Q1 2025 Expense Report - Meridian Consulting Group",
        "subtitle": "Software & Subscriptions - February 2025",
        "employee": "Elena Vasquez - CTO",
        "dept": "Technology",
        "entries": [
            ("Feb 08", "Salesforce Enterprise License renewal (annual)", "$18,500.00", CC_NUMBERS[8]),
            ("Feb 14", "AWS monthly infrastructure charges", "$7,234.67", CC_NUMBERS[9]),
        ],
    },
    {
        "title": "Q1 2025 Expense Report - Meridian Consulting Group",
        "subtitle": "Training & Development - February 2025",
        "employee": "David Kim - HR Director",
        "dept": "Human Resources",
        "entries": [
            ("Feb 10", "Coursera Business subscription (50 seats)", "$4,750.00", CC_NUMBERS[10]),
            ("Feb 20", "Conference registration - HR Tech Summit", "$2,195.00", CC_NUMBERS[11]),
        ],
    },
    {
        "title": "Q1 2025 Expense Report - Meridian Consulting Group",
        "subtitle": "Client Engagement - March 2025",
        "employee": "Sarah Chen - Senior Consultant",
        "dept": "Strategic Advisory Division",
        "entries": [
            ("Mar 03", "Ritz Carlton - Client workshop venue rental", "$5,800.00", CC_NUMBERS[12]),
            ("Mar 05", "FedEx - Overnight shipping of proposal docs", "$342.50", CC_NUMBERS[13]),
        ],
    },
    {
        "title": "Q1 2025 Expense Report - Meridian Consulting Group",
        "subtitle": "Vehicle & Transportation - March 2025",
        "employee": "Marcus Johnson - Managing Director",
        "dept": "Business Development",
        "entries": [
            ("Mar 10", "Hertz - Weekly car rental (premium sedan)", "$1,245.00", CC_NUMBERS[14]),
            ("Mar 12", "Shell - Fuel charges (client site visits)", "$287.35", CC_NUMBERS[15]),
        ],
    },
    {
        "title": "Q1 2025 Expense Report - Meridian Consulting Group",
        "subtitle": "Telecommunications - March 2025",
        "employee": "Elena Vasquez - CTO",
        "dept": "Technology",
        "entries": [
            ("Mar 15", "Verizon Business - Monthly corporate plan (25 lines)", "$3,875.00", CC_NUMBERS[16]),
            ("Mar 22", "Zoom Enterprise - Annual subscription renewal", "$6,400.00", CC_NUMBERS[17]),
        ],
    },
    {
        "title": "Q1 2025 Expense Report - Meridian Consulting Group",
        "subtitle": "Quarter Summary & Approvals",
        "employee": "CFO Review - Alexandra Petrov",
        "dept": "Finance & Accounting",
        "entries": [],
        "summary": True,
    },
]


def add_page(doc, page_data, page_num):
    """Add one expense report page to the document."""
    page = doc.new_page(width=W, height=H)

    # Header area - company logo placeholder and title
    # Blue header bar
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 0, W, 60))
    shape.finish(fill=(0.1, 0.2, 0.45), color=(0.1, 0.2, 0.45))
    shape.commit()

    page.insert_text(pymupdf.Point(40, 38), page_data["title"],
                     fontsize=14, fontname="hebo", color=(1, 1, 1))

    # Subtitle
    page.insert_text(pymupdf.Point(40, 85), page_data["subtitle"],
                     fontsize=12, fontname="hebo", color=(0.1, 0.2, 0.45))

    # Employee and department info
    page.insert_text(pymupdf.Point(40, 110), f"Employee: {page_data['employee']}",
                     fontsize=10, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(40, 125), f"Department: {page_data['dept']}",
                     fontsize=10, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(400, 110), f"Report Date: March 31, 2025",
                     fontsize=10, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(400, 125), f"Page {page_num} of 10",
                     fontsize=10, fontname="helv", color=(0, 0, 0))

    # Horizontal line
    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(40, 140), pymupdf.Point(W - 40, 140))
    shape2.finish(color=(0.7, 0.7, 0.7), width=1)
    shape2.commit()

    if page_data.get("summary"):
        # Summary page
        y = 170
        page.insert_text(pymupdf.Point(40, y), "QUARTERLY EXPENSE SUMMARY",
                         fontsize=14, fontname="hebo", color=(0.1, 0.2, 0.45))
        y += 30

        summaries = [
            ("Corporate Travel", "$10,075.25"),
            ("Client Entertainment", "$3,920.00"),
            ("Office Supplies & Equipment", "$3,986.25"),
            ("Software & Subscriptions", "$25,734.67"),
            ("Training & Development", "$6,945.00"),
            ("Client Engagement", "$6,142.50"),
            ("Vehicle & Transportation", "$1,532.35"),
            ("Telecommunications", "$10,275.00"),
        ]

        # Table header
        page.insert_text(pymupdf.Point(60, y), "Category", fontsize=10, fontname="hebo", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(350, y), "Total Amount", fontsize=10, fontname="hebo", color=(0, 0, 0))
        y += 5

        shape3 = page.new_shape()
        shape3.draw_line(pymupdf.Point(40, y), pymupdf.Point(W - 40, y))
        shape3.finish(color=(0.5, 0.5, 0.5), width=0.5)
        shape3.commit()
        y += 18

        grand_total = 0
        for cat, amount in summaries:
            page.insert_text(pymupdf.Point(60, y), cat, fontsize=10, fontname="helv", color=(0, 0, 0))
            page.insert_text(pymupdf.Point(350, y), amount, fontsize=10, fontname="helv", color=(0, 0, 0))
            val = float(amount.replace("$", "").replace(",", ""))
            grand_total += val
            y += 20

        y += 5
        shape4 = page.new_shape()
        shape4.draw_line(pymupdf.Point(40, y), pymupdf.Point(W - 40, y))
        shape4.finish(color=(0.1, 0.2, 0.45), width=1.5)
        shape4.commit()
        y += 18

        page.insert_text(pymupdf.Point(60, y), "GRAND TOTAL",
                         fontsize=11, fontname="hebo", color=(0.1, 0.2, 0.45))
        page.insert_text(pymupdf.Point(350, y), f"${grand_total:,.2f}",
                         fontsize=11, fontname="hebo", color=(0.1, 0.2, 0.45))

        y += 50
        page.insert_text(pymupdf.Point(40, y), "Approval Status: PENDING REVIEW",
                         fontsize=11, fontname="hebo", color=(0.8, 0.1, 0.1))
        y += 25
        page.insert_text(pymupdf.Point(40, y), "Authorized Approver: Alexandra Petrov, CFO",
                         fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 18
        page.insert_text(pymupdf.Point(40, y), "Approval Deadline: April 15, 2025",
                         fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 30
        page.insert_text(pymupdf.Point(40, y),
                         "Note: All expenses require original receipts. Credit card statements must be attached.",
                         fontsize=9, fontname="heit", color=(0.4, 0.4, 0.4))

    else:
        # Expense entries page with table
        y = 165

        # Table headers
        headers = [("Date", 40), ("Description", 110), ("Amount", 390), ("Card Number", 470)]
        for hdr, x in headers:
            page.insert_text(pymupdf.Point(x, y), hdr,
                             fontsize=10, fontname="hebo", color=(1, 1, 1))

        # Header background
        shape_hdr = page.new_shape()
        shape_hdr.draw_rect(pymupdf.Rect(35, y - 12, W - 35, y + 5))
        shape_hdr.finish(fill=(0.2, 0.35, 0.6), color=(0.2, 0.35, 0.6))
        shape_hdr.commit()

        # Re-draw headers on top
        for hdr, x in headers:
            page.insert_text(pymupdf.Point(x, y), hdr,
                             fontsize=10, fontname="hebo", color=(1, 1, 1))

        y += 22

        for i, (date, desc, amount, cc) in enumerate(page_data["entries"]):
            # Alternating row background
            if i % 2 == 0:
                shape_row = page.new_shape()
                shape_row.draw_rect(pymupdf.Rect(35, y - 12, W - 35, y + 5))
                shape_row.finish(fill=(0.95, 0.95, 0.97), color=(0.95, 0.95, 0.97))
                shape_row.commit()

            page.insert_text(pymupdf.Point(40, y), date,
                             fontsize=9, fontname="helv", color=(0, 0, 0))
            # Description might be long, truncate if needed
            page.insert_text(pymupdf.Point(110, y), desc[:45],
                             fontsize=9, fontname="helv", color=(0, 0, 0))
            page.insert_text(pymupdf.Point(390, y), amount,
                             fontsize=9, fontname="helv", color=(0, 0, 0))
            page.insert_text(pymupdf.Point(470, y), cc,
                             fontsize=8, fontname="cour", color=(0.2, 0.2, 0.2))
            y += 22

        # Additional detail section
        y += 20
        page.insert_text(pymupdf.Point(40, y), "Transaction Details:",
                         fontsize=10, fontname="hebo", color=(0.1, 0.2, 0.45))
        y += 18

        for date, desc, amount, cc in page_data["entries"]:
            page.insert_text(pymupdf.Point(50, y),
                             f"Payment processed on {date} via card ending in ...{cc[-4:]}",
                             fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
            y += 15
            page.insert_text(pymupdf.Point(50, y),
                             f"Authorization code: {hash(cc) % 900000 + 100000}  |  Status: Approved",
                             fontsize=9, fontname="cour", color=(0.3, 0.3, 0.3))
            y += 15
            page.insert_text(pymupdf.Point(50, y),
                             f"Vendor: {desc.split(' - ')[0] if ' - ' in desc else desc[:30]}  |  Amount: {amount}",
                             fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
            y += 22

        # Policy reminder at bottom
        y = H - 80
        shape_bottom = page.new_shape()
        shape_bottom.draw_line(pymupdf.Point(40, y), pymupdf.Point(W - 40, y))
        shape_bottom.finish(color=(0.8, 0.8, 0.8), width=0.5)
        shape_bottom.commit()
        y += 15
        page.insert_text(pymupdf.Point(40, y),
                         "CONFIDENTIAL - This document contains sensitive financial information including credit card numbers.",
                         fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))
        y += 12
        page.insert_text(pymupdf.Point(40, y),
                         "Handle according to Meridian Consulting Group Data Protection Policy (DPP-2024-Rev3).",
                         fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))


def create_initial():
    os.makedirs(FINANCE_DIR, exist_ok=True)

    doc = pymupdf.open()

    for i, page_data in enumerate(PAGES_DATA):
        add_page(doc, page_data, i + 1)

    # Set metadata
    doc.set_metadata({
        "title": "Q1 2025 Expense Report - Meridian Consulting Group",
        "author": "Finance Department",
        "subject": "Quarterly Expense Report",
        "keywords": "expense, report, Q1, 2025, finance",
        "creator": "Meridian ERP System v4.2",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f"Initial file created: {OUTPUT}")

    # Verify CC count
    doc2 = pymupdf.open(OUTPUT)
    all_text = ""
    for page in doc2:
        all_text += page.get_text("text")
    page_count = doc2.page_count
    doc2.close()

    cc_count = 0
    for cc in CC_NUMBERS:
        cc_count += all_text.count(cc)
    print(f"Credit card numbers found in document: {cc_count}")
    print(f"Page count: {page_count}")

    # Open in evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print("GUI_READY: launched evince with DISPLAY=:0")


create_initial()
