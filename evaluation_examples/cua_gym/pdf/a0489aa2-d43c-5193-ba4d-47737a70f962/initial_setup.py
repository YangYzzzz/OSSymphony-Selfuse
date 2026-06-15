"""
Initial Setup: Add sequential exhibit stamps to financial evidence documents
Task ID: pdf_fin_094
Domain: pdf

Creates 3 source PDFs in /home/user/finance/evidence/ and an empty stamped/ directory.
- doc_a.pdf: 5 pages (invoice records)
- doc_b.pdf: 3 pages (bank statements)
- doc_c.pdf: 7 pages (expense reports)
"""

import os
import shlex
import subprocess
import time
import pymupdf


EVIDENCE_DIR = "/home/user/finance/evidence"
STAMPED_DIR = os.path.join(EVIDENCE_DIR, "stamped")


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


def create_doc_a():
    """Create doc_a.pdf - 5 pages of invoice records."""
    doc = pymupdf.open()

    # Page 1: Invoice cover sheet
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "MERIDIAN CONSULTING GROUP", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(72, 85), "Invoice Summary Report", fontsize=14, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 110), "Prepared for: Westfield Capital Partners LLC", fontsize=11, fontname="helv")
    page.insert_text(pymupdf.Point(72, 130), "Report Period: January 1, 2024 - June 30, 2024", fontsize=11, fontname="helv")
    page.insert_text(pymupdf.Point(72, 150), "Document Reference: MCG-2024-INV-0847", fontsize=11, fontname="helv")

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 170), pymupdf.Point(540, 170))
    shape.finish(color=(0.1, 0.1, 0.4), width=1.5)
    shape.commit()

    y = 200
    invoices = [
        ("INV-2024-001", "2024-01-15", "Strategic Advisory Services - Q1", "$45,000.00"),
        ("INV-2024-002", "2024-02-20", "Due Diligence Review - Acme Corp", "$32,500.00"),
        ("INV-2024-003", "2024-03-10", "Regulatory Compliance Assessment", "$28,750.00"),
        ("INV-2024-004", "2024-04-05", "Market Analysis Report - Tech Sector", "$19,200.00"),
        ("INV-2024-005", "2024-05-18", "Merger Integration Support", "$67,300.00"),
        ("INV-2024-006", "2024-06-22", "Quarterly Financial Review", "$41,800.00"),
    ]

    headers = ["Invoice #", "Date", "Description", "Amount"]
    cols = [72, 170, 260, 470]
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(cols[i], y), h, fontsize=10, fontname="hebo")
    y += 20
    for inv in invoices:
        for i, val in enumerate(inv):
            page.insert_text(pymupdf.Point(cols[i], y), val, fontsize=9, fontname="helv")
        y += 18

    page.insert_text(pymupdf.Point(370, y + 20), "Total: $234,550.00", fontsize=11, fontname="hebo")

    # Page 2: Detailed invoice INV-2024-001
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "INVOICE", fontsize=22, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(72, 90), "Invoice Number: INV-2024-001", fontsize=11, fontname="helv")
    page.insert_text(pymupdf.Point(72, 110), "Date Issued: January 15, 2024", fontsize=11, fontname="helv")
    page.insert_text(pymupdf.Point(72, 130), "Payment Terms: Net 30", fontsize=11, fontname="helv")
    page.insert_text(pymupdf.Point(72, 170), "Bill To:", fontsize=10, fontname="hebo")
    page.insert_text(pymupdf.Point(72, 188), "Westfield Capital Partners LLC", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 204), "1200 Financial Plaza, Suite 400", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 220), "New York, NY 10005", fontsize=10, fontname="helv")

    y = 270
    items = [
        ("Strategic Advisory Services", "120 hours @ $375/hr", "$45,000.00"),
    ]
    page.insert_text(pymupdf.Point(72, y), "Service", fontsize=10, fontname="hebo")
    page.insert_text(pymupdf.Point(300, y), "Rate", fontsize=10, fontname="hebo")
    page.insert_text(pymupdf.Point(470, y), "Amount", fontsize=10, fontname="hebo")
    y += 20
    for item in items:
        page.insert_text(pymupdf.Point(72, y), item[0], fontsize=9, fontname="helv")
        page.insert_text(pymupdf.Point(300, y), item[1], fontsize=9, fontname="helv")
        page.insert_text(pymupdf.Point(470, y), item[2], fontsize=9, fontname="helv")
        y += 18

    page.insert_text(pymupdf.Point(400, y + 30), "Subtotal: $45,000.00", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(400, y + 48), "Tax (0%): $0.00", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(400, y + 66), "Total Due: $45,000.00", fontsize=11, fontname="hebo")

    # Page 3: Invoice INV-2024-003
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "INVOICE", fontsize=22, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(72, 90), "Invoice Number: INV-2024-003", fontsize=11, fontname="helv")
    page.insert_text(pymupdf.Point(72, 110), "Date Issued: March 10, 2024", fontsize=11, fontname="helv")
    page.insert_text(pymupdf.Point(72, 130), "Payment Terms: Net 30", fontsize=11, fontname="helv")
    page.insert_text(pymupdf.Point(72, 170), "Services: Regulatory Compliance Assessment", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 190), "Scope: Full regulatory review for SEC filing requirements", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 210), "Personnel: Jennifer Walsh, Senior Compliance Analyst", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 230), "Hours: 115 hours @ $250/hr", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(400, 280), "Total Due: $28,750.00", fontsize=11, fontname="hebo")

    # Page 4: Invoice INV-2024-005
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "INVOICE", fontsize=22, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(72, 90), "Invoice Number: INV-2024-005", fontsize=11, fontname="helv")
    page.insert_text(pymupdf.Point(72, 110), "Date Issued: May 18, 2024", fontsize=11, fontname="helv")
    page.insert_text(pymupdf.Point(72, 130), "Payment Terms: Net 30", fontsize=11, fontname="helv")
    page.insert_text(pymupdf.Point(72, 170), "Services: Merger Integration Support", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 190), "Client: Westfield Capital Partners LLC / TechVentures Inc.", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 210), "Lead Consultant: David Park, Managing Director", fontsize=10, fontname="helv")

    y = 260
    line_items = [
        ("Integration Planning", "80 hrs", "$30,000.00"),
        ("Systems Migration Assessment", "45 hrs", "$16,875.00"),
        ("Staff Transition Consulting", "35 hrs", "$13,125.00"),
        ("Travel Expenses", "Lump sum", "$7,300.00"),
    ]
    page.insert_text(pymupdf.Point(72, y), "Line Item", fontsize=10, fontname="hebo")
    page.insert_text(pymupdf.Point(300, y), "Hours", fontsize=10, fontname="hebo")
    page.insert_text(pymupdf.Point(470, y), "Amount", fontsize=10, fontname="hebo")
    y += 20
    for item in line_items:
        page.insert_text(pymupdf.Point(72, y), item[0], fontsize=9, fontname="helv")
        page.insert_text(pymupdf.Point(300, y), item[1], fontsize=9, fontname="helv")
        page.insert_text(pymupdf.Point(470, y), item[2], fontsize=9, fontname="helv")
        y += 18

    page.insert_text(pymupdf.Point(400, y + 30), "Total Due: $67,300.00", fontsize=11, fontname="hebo")

    # Page 5: Payment summary
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "Payment Status Summary", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(72, 90), "As of June 30, 2024", fontsize=11, fontname="helv")

    y = 130
    payments = [
        ("INV-2024-001", "$45,000.00", "Paid", "2024-02-12"),
        ("INV-2024-002", "$32,500.00", "Paid", "2024-03-18"),
        ("INV-2024-003", "$28,750.00", "Paid", "2024-04-08"),
        ("INV-2024-004", "$19,200.00", "Paid", "2024-05-02"),
        ("INV-2024-005", "$67,300.00", "Outstanding", "—"),
        ("INV-2024-006", "$41,800.00", "Outstanding", "—"),
    ]
    headers = ["Invoice", "Amount", "Status", "Payment Date"]
    cols = [72, 190, 310, 420]
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(cols[i], y), h, fontsize=10, fontname="hebo")
    y += 20
    for p in payments:
        for i, val in enumerate(p):
            color = (0.8, 0, 0) if val == "Outstanding" else (0, 0, 0)
            page.insert_text(pymupdf.Point(cols[i], y), val, fontsize=9, fontname="helv", color=color)
        y += 18

    page.insert_text(pymupdf.Point(72, y + 30), "Total Outstanding: $109,100.00", fontsize=11, fontname="hebo", color=(0.8, 0, 0))
    page.insert_text(pymupdf.Point(72, y + 50), "Total Paid: $125,450.00", fontsize=11, fontname="hebo", color=(0, 0.5, 0))

    output_path = os.path.join(EVIDENCE_DIR, "doc_a.pdf")
    doc.save(output_path)
    doc.close()
    print(f"Created: {output_path} ({5} pages)")


def create_doc_b():
    """Create doc_b.pdf - 3 pages of bank statements."""
    doc = pymupdf.open()

    # Page 1: Bank statement - April
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 50), "FIRST NATIONAL BANK", fontsize=18, fontname="hebo", color=(0, 0.2, 0.5))
    page.insert_text(pymupdf.Point(72, 75), "Business Account Statement", fontsize=12, fontname="helv")
    page.insert_text(pymupdf.Point(72, 100), "Account: Westfield Capital Partners LLC", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 118), "Account Number: ****4782", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 136), "Statement Period: April 1-30, 2024", fontsize=10, fontname="helv")

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 155), pymupdf.Point(540, 155))
    shape.finish(color=(0, 0.2, 0.5), width=1)
    shape.commit()

    page.insert_text(pymupdf.Point(72, 175), "Opening Balance: $1,247,832.56", fontsize=10, fontname="hebo")

    y = 210
    txns = [
        ("04/02", "Wire Transfer - MCG Advisory Fee", "-$45,000.00", "$1,202,832.56"),
        ("04/05", "ACH Deposit - Portfolio Return Q1", "+$182,400.00", "$1,385,232.56"),
        ("04/10", "Check #4521 - Office Lease", "-$12,500.00", "$1,372,732.56"),
        ("04/15", "Wire Transfer - MCG Compliance Rev.", "-$28,750.00", "$1,343,982.56"),
        ("04/18", "ACH Deposit - Client Fee - Rivera Est.", "+$75,000.00", "$1,418,982.56"),
        ("04/22", "Wire Transfer - Insurance Premium", "-$8,340.00", "$1,410,642.56"),
        ("04/28", "ACH Deposit - Dividend Income", "+$23,150.00", "$1,433,792.56"),
    ]
    headers = ["Date", "Description", "Amount", "Balance"]
    cols = [72, 130, 380, 480]
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(cols[i], y), h, fontsize=9, fontname="hebo")
    y += 18
    for txn in txns:
        for i, val in enumerate(txn):
            page.insert_text(pymupdf.Point(cols[i], y), val, fontsize=8, fontname="helv")
        y += 16

    page.insert_text(pymupdf.Point(72, y + 20), "Closing Balance: $1,433,792.56", fontsize=10, fontname="hebo")

    # Page 2: Bank statement - May
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 50), "FIRST NATIONAL BANK", fontsize=18, fontname="hebo", color=(0, 0.2, 0.5))
    page.insert_text(pymupdf.Point(72, 75), "Business Account Statement", fontsize=12, fontname="helv")
    page.insert_text(pymupdf.Point(72, 100), "Statement Period: May 1-31, 2024", fontsize=10, fontname="helv")

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 120), pymupdf.Point(540, 120))
    shape.finish(color=(0, 0.2, 0.5), width=1)
    shape.commit()

    page.insert_text(pymupdf.Point(72, 140), "Opening Balance: $1,433,792.56", fontsize=10, fontname="hebo")

    y = 175
    txns = [
        ("05/03", "Wire Transfer - MCG Market Analysis", "-$19,200.00", "$1,414,592.56"),
        ("05/08", "ACH Deposit - Bond Interest", "+$34,200.00", "$1,448,792.56"),
        ("05/12", "Check #4522 - Legal Retainer", "-$15,000.00", "$1,433,792.56"),
        ("05/18", "Wire Transfer - MCG Merger Support", "-$67,300.00", "$1,366,492.56"),
        ("05/25", "ACH Deposit - Client Fee - Park Trust", "+$95,000.00", "$1,461,492.56"),
        ("05/30", "Wire Transfer - IT Services", "-$6,800.00", "$1,454,692.56"),
    ]
    headers = ["Date", "Description", "Amount", "Balance"]
    cols = [72, 130, 380, 480]
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(cols[i], y), h, fontsize=9, fontname="hebo")
    y += 18
    for txn in txns:
        for i, val in enumerate(txn):
            page.insert_text(pymupdf.Point(cols[i], y), val, fontsize=8, fontname="helv")
        y += 16

    page.insert_text(pymupdf.Point(72, y + 20), "Closing Balance: $1,454,692.56", fontsize=10, fontname="hebo")

    # Page 3: Bank statement - June
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 50), "FIRST NATIONAL BANK", fontsize=18, fontname="hebo", color=(0, 0.2, 0.5))
    page.insert_text(pymupdf.Point(72, 75), "Business Account Statement", fontsize=12, fontname="helv")
    page.insert_text(pymupdf.Point(72, 100), "Statement Period: June 1-30, 2024", fontsize=10, fontname="helv")

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 120), pymupdf.Point(540, 120))
    shape.finish(color=(0, 0.2, 0.5), width=1)
    shape.commit()

    page.insert_text(pymupdf.Point(72, 140), "Opening Balance: $1,454,692.56", fontsize=10, fontname="hebo")

    y = 175
    txns = [
        ("06/04", "Wire Transfer - MCG Quarterly Review", "-$41,800.00", "$1,412,892.56"),
        ("06/10", "ACH Deposit - Portfolio Return Q2", "+$198,750.00", "$1,611,642.56"),
        ("06/15", "Check #4523 - Office Lease", "-$12,500.00", "$1,599,142.56"),
        ("06/20", "ACH Deposit - Client Fee - Chen Family", "+$62,000.00", "$1,661,142.56"),
        ("06/25", "Wire Transfer - Professional Insurance", "-$4,200.00", "$1,656,942.56"),
        ("06/28", "ACH Deposit - Dividend Income", "+$27,830.00", "$1,684,772.56"),
    ]
    headers = ["Date", "Description", "Amount", "Balance"]
    cols = [72, 130, 380, 480]
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(cols[i], y), h, fontsize=9, fontname="hebo")
    y += 18
    for txn in txns:
        for i, val in enumerate(txn):
            page.insert_text(pymupdf.Point(cols[i], y), val, fontsize=8, fontname="helv")
        y += 16

    page.insert_text(pymupdf.Point(72, y + 20), "Closing Balance: $1,684,772.56", fontsize=10, fontname="hebo")

    output_path = os.path.join(EVIDENCE_DIR, "doc_b.pdf")
    doc.save(output_path)
    doc.close()
    print(f"Created: {output_path} ({3} pages)")


def create_doc_c():
    """Create doc_c.pdf - 7 pages of expense reports."""
    doc = pymupdf.open()

    # Page 1: Expense report cover
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "EXPENSE REPORT", fontsize=20, fontname="hebo", color=(0.5, 0.1, 0.1))
    page.insert_text(pymupdf.Point(72, 90), "Westfield Capital Partners LLC", fontsize=14, fontname="helv")
    page.insert_text(pymupdf.Point(72, 115), "Employee: David Park, Managing Director", fontsize=11, fontname="helv")
    page.insert_text(pymupdf.Point(72, 135), "Department: Mergers & Acquisitions", fontsize=11, fontname="helv")
    page.insert_text(pymupdf.Point(72, 155), "Period: Q2 2024 (April - June)", fontsize=11, fontname="helv")
    page.insert_text(pymupdf.Point(72, 175), "Submission Date: July 5, 2024", fontsize=11, fontname="helv")
    page.insert_text(pymupdf.Point(72, 195), "Approval Status: Pending Review", fontsize=11, fontname="helv", color=(0.8, 0.5, 0))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 220), pymupdf.Point(540, 220))
    shape.finish(color=(0.5, 0.1, 0.1), width=1.5)
    shape.commit()

    page.insert_text(pymupdf.Point(72, 250), "Summary by Category:", fontsize=12, fontname="hebo")
    y = 275
    categories = [
        ("Travel - Airfare", "$8,432.00"),
        ("Travel - Hotels", "$6,180.00"),
        ("Travel - Ground Transportation", "$1,845.00"),
        ("Meals & Entertainment", "$3,267.50"),
        ("Office Supplies", "$892.30"),
        ("Professional Development", "$2,500.00"),
        ("Miscellaneous", "$445.20"),
    ]
    for cat, amt in categories:
        page.insert_text(pymupdf.Point(90, y), cat, fontsize=10, fontname="helv")
        page.insert_text(pymupdf.Point(420, y), amt, fontsize=10, fontname="helv")
        y += 18

    page.insert_text(pymupdf.Point(350, y + 15), "Grand Total: $23,562.00", fontsize=12, fontname="hebo", color=(0.5, 0.1, 0.1))

    # Page 2: April expenses
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 50), "April 2024 - Detailed Expenses", fontsize=14, fontname="hebo")

    y = 85
    expenses = [
        ("04/02", "Delta Airlines - JFK to SFO", "Airfare", "$687.00", "Client Meeting - TechVentures"),
        ("04/02", "Hilton San Francisco", "Hotel", "$289.00", "2 nights"),
        ("04/03", "Uber - Airport to Hotel", "Transport", "$45.00", "SFO to downtown"),
        ("04/03", "Morton's Steakhouse", "Meals", "$342.50", "Client dinner - 4 people"),
        ("04/08", "United Airlines - SFO to JFK", "Airfare", "$612.00", "Return flight"),
        ("04/15", "Office Depot", "Supplies", "$156.30", "Presentation materials"),
        ("04/18", "Amtrak - NYC to Boston", "Transport", "$189.00", "Due diligence trip"),
        ("04/18", "Marriott Boston", "Hotel", "$245.00", "1 night"),
        ("04/19", "Legal Seafood", "Meals", "$187.00", "Working lunch - 3 people"),
        ("04/22", "Lyft - Boston trips", "Transport", "$78.00", "Multiple rides"),
    ]
    headers = ["Date", "Description", "Category", "Amount", "Notes"]
    cols = [72, 120, 310, 385, 450]
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(cols[i], y), h, fontsize=8, fontname="hebo")
    y += 16
    for exp in expenses:
        for i, val in enumerate(exp):
            page.insert_text(pymupdf.Point(cols[i], y), val, fontsize=7, fontname="helv")
        y += 14

    page.insert_text(pymupdf.Point(350, y + 15), "April Total: $2,830.80", fontsize=10, fontname="hebo")

    # Page 3: May expenses
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 50), "May 2024 - Detailed Expenses", fontsize=14, fontname="hebo")

    y = 85
    expenses = [
        ("05/01", "American Airlines - JFK to ORD", "Airfare", "$534.00", "Chicago conference"),
        ("05/01", "Palmer House Hilton", "Hotel", "$312.00", "3 nights"),
        ("05/02", "Taxi - O'Hare to hotel", "Transport", "$62.00", ""),
        ("05/03", "Conference Registration", "Prof. Dev.", "$2,500.00", "M&A Summit 2024"),
        ("05/04", "Gibsons Bar & Steakhouse", "Meals", "$425.00", "Team dinner - 5 people"),
        ("05/06", "United Airlines - ORD to JFK", "Airfare", "$498.00", "Return flight"),
        ("05/15", "Delta Airlines - JFK to LAX", "Airfare", "$723.00", "Client visit"),
        ("05/15", "Ritz-Carlton Los Angeles", "Hotel", "$445.00", "2 nights"),
        ("05/16", "Uber - LAX to Beverly Hills", "Transport", "$67.00", ""),
        ("05/17", "Nobu Malibu", "Meals", "$512.00", "Client entertainment"),
        ("05/20", "Southwest - LAX to JFK", "Airfare", "$389.00", "Return flight"),
    ]
    headers = ["Date", "Description", "Category", "Amount", "Notes"]
    cols = [72, 120, 310, 385, 450]
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(cols[i], y), h, fontsize=8, fontname="hebo")
    y += 16
    for exp in expenses:
        for i, val in enumerate(exp):
            page.insert_text(pymupdf.Point(cols[i], y), val, fontsize=7, fontname="helv")
        y += 14

    page.insert_text(pymupdf.Point(350, y + 15), "May Total: $6,467.00", fontsize=10, fontname="hebo")

    # Page 4: June expenses
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 50), "June 2024 - Detailed Expenses", fontsize=14, fontname="hebo")

    y = 85
    expenses = [
        ("06/03", "JetBlue - JFK to MIA", "Airfare", "$412.00", "Due diligence - SunCoast"),
        ("06/03", "Four Seasons Miami", "Hotel", "$389.00", "2 nights"),
        ("06/04", "Uber - Miami trips", "Transport", "$134.00", "Multiple rides"),
        ("06/05", "Joe's Stone Crab", "Meals", "$278.00", "Client dinner"),
        ("06/05", "American Airlines - MIA to JFK", "Airfare", "$445.00", "Return"),
        ("06/12", "Staples", "Supplies", "$234.00", "Office equipment"),
        ("06/18", "Delta Airlines - JFK to DCA", "Airfare", "$312.00", "DC meetings"),
        ("06/18", "Willard InterContinental", "Hotel", "$356.00", "1 night"),
        ("06/19", "Capital Grille", "Meals", "$345.00", "Regulatory meeting dinner"),
        ("06/19", "Uber - DC trips", "Transport", "$89.00", ""),
        ("06/20", "Amtrak - DCA to NYC", "Airfare", "$178.00", "Return"),
        ("06/25", "Staples - print services", "Supplies", "$502.00", "Quarterly reports"),
    ]
    headers = ["Date", "Description", "Category", "Amount", "Notes"]
    cols = [72, 120, 310, 385, 450]
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(cols[i], y), h, fontsize=8, fontname="hebo")
    y += 16
    for exp in expenses:
        for i, val in enumerate(exp):
            page.insert_text(pymupdf.Point(cols[i], y), val, fontsize=7, fontname="helv")
        y += 14

    page.insert_text(pymupdf.Point(350, y + 15), "June Total: $3,674.00", fontsize=10, fontname="hebo")

    # Page 5: Receipt images placeholder page
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "Supporting Receipts - Section 1", fontsize=14, fontname="hebo")
    page.insert_text(pymupdf.Point(72, 85), "Receipts for travel expenses (April-May 2024)", fontsize=10, fontname="helv")

    y = 120
    receipts = [
        "Receipt #R-001: Delta Airlines confirmation - $687.00 (04/02)",
        "Receipt #R-002: Hilton SF folio #847291 - $289.00 (04/02)",
        "Receipt #R-003: Morton's check #1247 - $342.50 (04/03)",
        "Receipt #R-004: United Airlines confirmation - $612.00 (04/08)",
        "Receipt #R-005: Amtrak ticket #AM78234 - $189.00 (04/18)",
        "Receipt #R-006: American Airlines confirmation - $534.00 (05/01)",
        "Receipt #R-007: Palmer House folio #293847 - $312.00 (05/01)",
        "Receipt #R-008: Gibsons receipt #8834 - $425.00 (05/04)",
        "Receipt #R-009: Delta Airlines confirmation - $723.00 (05/15)",
        "Receipt #R-010: Ritz-Carlton folio #102938 - $445.00 (05/15)",
    ]
    for r in receipts:
        page.insert_text(pymupdf.Point(90, y), r, fontsize=9, fontname="helv")
        y += 16

    page.insert_text(pymupdf.Point(72, y + 20), "[Original receipt images attached separately]", fontsize=9, fontname="heit", color=(0.4, 0.4, 0.4))

    # Page 6: More receipts
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "Supporting Receipts - Section 2", fontsize=14, fontname="hebo")
    page.insert_text(pymupdf.Point(72, 85), "Receipts for travel expenses (June 2024) and miscellaneous", fontsize=10, fontname="helv")

    y = 120
    receipts = [
        "Receipt #R-011: JetBlue confirmation - $412.00 (06/03)",
        "Receipt #R-012: Four Seasons folio #554821 - $389.00 (06/03)",
        "Receipt #R-013: Joe's Stone Crab check #2847 - $278.00 (06/05)",
        "Receipt #R-014: Delta Airlines confirmation - $312.00 (06/18)",
        "Receipt #R-015: Willard IC folio #887234 - $356.00 (06/18)",
        "Receipt #R-016: Capital Grille receipt #4421 - $345.00 (06/19)",
        "Receipt #R-017: Staples order #ST-992847 - $234.00 (06/12)",
        "Receipt #R-018: Staples print order #ST-994102 - $502.00 (06/25)",
        "Receipt #R-019: Various Uber/Lyft receipts - $475.00 (Q2 total)",
        "Receipt #R-020: Miscellaneous expenses - $445.20 (Q2 total)",
    ]
    for r in receipts:
        page.insert_text(pymupdf.Point(90, y), r, fontsize=9, fontname="helv")
        y += 16

    page.insert_text(pymupdf.Point(72, y + 20), "[Original receipt images attached separately]", fontsize=9, fontname="heit", color=(0.4, 0.4, 0.4))

    # Page 7: Approval signatures
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "Expense Report Approval", fontsize=16, fontname="hebo", color=(0.5, 0.1, 0.1))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape.finish(color=(0.5, 0.1, 0.1), width=1)
    shape.commit()

    page.insert_text(pymupdf.Point(72, 110), "I certify that the above expenses were incurred in the course of", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 126), "legitimate business activities for Westfield Capital Partners LLC.", fontsize=10, fontname="helv")

    page.insert_text(pymupdf.Point(72, 175), "Employee Signature:", fontsize=10, fontname="hebo")
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(210, 178), pymupdf.Point(400, 178))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    page.insert_text(pymupdf.Point(72, 195), "Date: _______________", fontsize=10, fontname="helv")

    page.insert_text(pymupdf.Point(72, 245), "Manager Approval:", fontsize=10, fontname="hebo")
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(210, 248), pymupdf.Point(400, 248))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    page.insert_text(pymupdf.Point(72, 265), "Name: Sarah Mitchell, CFO", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 283), "Date: _______________", fontsize=10, fontname="helv")

    page.insert_text(pymupdf.Point(72, 340), "Finance Department Review:", fontsize=10, fontname="hebo")
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(240, 343), pymupdf.Point(400, 343))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    page.insert_text(pymupdf.Point(72, 358), "Reviewer: _______________", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 376), "Date: _______________", fontsize=10, fontname="helv")

    page.insert_text(pymupdf.Point(72, 430), "Notes:", fontsize=10, fontname="hebo")
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(72, 445, 540, 580))
    shape.finish(color=(0.5, 0.5, 0.5), width=0.5)
    shape.commit()

    output_path = os.path.join(EVIDENCE_DIR, "doc_c.pdf")
    doc.save(output_path)
    doc.close()
    print(f"Created: {output_path} ({7} pages)")


def main():
    # Create directory structure
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    os.makedirs(STAMPED_DIR, exist_ok=True)
    print(f"Created directories: {EVIDENCE_DIR}, {STAMPED_DIR}")

    # Create all three documents
    create_doc_a()
    create_doc_b()
    create_doc_c()

    # Open the evidence directory and the first PDF for the agent
    launch_gui(f'nautilus "{EVIDENCE_DIR}"', delay_sec=1.5)
    launch_gui(f'evince "{os.path.join(EVIDENCE_DIR, "doc_a.pdf")}"', delay_sec=2.0)
    print("GUI_READY: launched Nautilus and Evince with DISPLAY=:0")


main()
