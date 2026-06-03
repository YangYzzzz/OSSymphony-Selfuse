"""
Initial Setup: Create an 8-page transaction log PDF with ~20 credit card numbers
Task ID: pdf_ro_016
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import random

random.seed(42)  # Fixed seed for reproducible AUTH codes

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_016'
FINANCE_DIR = f'{WORKDIR}/finance'
OUTPUT = f'{FINANCE_DIR}/transactions.pdf'


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
    import pymupdf

    os.makedirs(FINANCE_DIR, exist_ok=True)

    # Credit card numbers to scatter (20 total)
    cc_numbers = [
        "4532-8891-2245-6677",
        "5124-7783-0012-3498",
        "3782-1029-5567-4401",
        "4916-3342-7788-1120",
        "5501-2293-4456-7789",
        "4024-0071-8834-5562",
        "5312-6601-9923-4478",
        "3714-9200-5567-8832",
        "4556-1122-3344-5566",
        "5234-8877-6655-4433",
        "4716-0293-8847-1156",
        "5421-3378-9912-6640",
        "3852-7741-0023-8896",
        "4929-5510-6678-2234",
        "5103-8824-7756-9901",
        "4485-2267-3398-0045",
        "5290-1143-5572-8807",
        "3601-9988-4423-6651",
        "4832-7765-1109-3342",
        "5047-6639-2281-4478",
    ]

    # Transaction data for realistic content
    merchants = [
        "Amazon Web Services", "Whole Foods Market", "Delta Air Lines",
        "Hilton Hotels & Resorts", "Uber Technologies", "Netflix Inc.",
        "Starbucks Coffee", "Apple Store", "Chevron Gas Station",
        "Target Corporation", "Costco Wholesale", "Southwest Airlines",
        "Marriott International", "Spotify Premium", "Home Depot",
        "Walgreens Pharmacy", "Shell Gas Station", "Best Buy Electronics",
        "Trader Joe's", "United Airlines", "FedEx Shipping",
        "Adobe Systems", "Microsoft 365", "Google Cloud Platform",
        "Airbnb Inc.", "Lyft Rideshare", "Panera Bread", "Chipotle Mexican Grill",
        "CVS Pharmacy", "Walmart Supercenter", "Kroger Grocery",
        "T-Mobile Wireless", "AT&T Services", "Verizon Communications",
    ]

    categories = [
        "Cloud Services", "Groceries", "Travel - Airfare", "Travel - Lodging",
        "Transportation", "Entertainment", "Food & Beverage", "Electronics",
        "Fuel", "Retail", "Subscription", "Home Improvement", "Health",
        "Shipping", "Software", "Telecommunications",
    ]

    dates_2025 = [
        "2025-01-03", "2025-01-07", "2025-01-12", "2025-01-15", "2025-01-18",
        "2025-01-22", "2025-01-25", "2025-01-28", "2025-02-01", "2025-02-05",
        "2025-02-09", "2025-02-14", "2025-02-17", "2025-02-21", "2025-02-24",
        "2025-02-28", "2025-03-02", "2025-03-06", "2025-03-10", "2025-03-14",
        "2025-03-17", "2025-03-20", "2025-03-23", "2025-03-27", "2025-03-30",
        "2025-04-02", "2025-04-05", "2025-04-09", "2025-04-12", "2025-04-16",
        "2025-04-19", "2025-04-22", "2025-04-25", "2025-04-28", "2025-05-01",
        "2025-05-05", "2025-05-08", "2025-05-12", "2025-05-15", "2025-05-18",
    ]

    amounts = [
        "$2,450.00", "$87.34", "$312.50", "$189.99", "$24.67",
        "$15.99", "$6.45", "$1,299.00", "$52.18", "$143.76",
        "$234.50", "$478.00", "$12.99", "$9.99", "$167.82",
        "$35.40", "$48.92", "$899.99", "$72.15", "$456.30",
        "$19.99", "$125.00", "$1,850.00", "$3,200.00", "$67.89",
        "$43.21", "$28.50", "$14.75", "$98.60", "$210.00",
        "$55.00", "$79.99", "$112.00", "$156.78", "$345.60",
        "$22.50", "$88.00", "$1,100.00", "$63.42", "$291.15",
    ]

    ref_ids = [f"TXN-2025-{str(i).zfill(5)}" for i in range(10001, 10041)]

    doc = pymupdf.open()

    # Page layout constants
    PAGE_W, PAGE_H = 612, 792  # Letter size
    LEFT_MARGIN = 50
    RIGHT_MARGIN = 562
    TOP_START = 80
    LINE_HEIGHT = 14
    SECTION_GAP = 8

    # Distribute 20 credit card numbers across 8 pages (~2-3 per page)
    # We'll create transaction entries, some with CC numbers, some without
    cc_index = 0
    txn_index = 0

    # Plan: ~5 transactions per page, 8 pages = 40 transactions
    # 20 of them have CC numbers shown
    cc_assignments = [False] * 40
    # Place CC numbers at specific positions to get ~20
    cc_positions = [0, 1, 3, 5, 7, 8, 10, 12, 14, 16,
                    18, 20, 22, 24, 26, 28, 31, 33, 36, 39]
    for pos in cc_positions:
        cc_assignments[pos] = True

    txn_global = 0

    for page_num in range(8):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)

        y = TOP_START

        # Header
        page.insert_text(
            pymupdf.Point(LEFT_MARGIN, y - 20),
            "ACME Financial Services - Transaction Ledger",
            fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.4)
        )
        y += 5

        # Subheader
        page.insert_text(
            pymupdf.Point(LEFT_MARGIN, y),
            f"Confidential - Internal Use Only | Report Date: 2025-05-20 | Page {page_num + 1} of 8",
            fontsize=8, fontname="heit", color=(0.4, 0.4, 0.4)
        )
        y += 15

        # Separator line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(LEFT_MARGIN, y), pymupdf.Point(RIGHT_MARGIN, y))
        shape.finish(color=(0.2, 0.2, 0.5), width=1.5)
        shape.commit()
        y += 15

        # Transactions for this page (5 per page)
        txns_this_page = 5
        for t in range(txns_this_page):
            if txn_global >= 40:
                break

            txn_date = dates_2025[txn_global % len(dates_2025)]
            merchant = merchants[txn_global % len(merchants)]
            category = categories[txn_global % len(categories)]
            amount = amounts[txn_global % len(amounts)]
            ref_id = ref_ids[txn_global % len(ref_ids)]
            has_cc = cc_assignments[txn_global]

            # Transaction block
            # Reference and date line
            page.insert_text(
                pymupdf.Point(LEFT_MARGIN, y),
                f"{ref_id}",
                fontsize=10, fontname="hebo", color=(0, 0, 0)
            )
            page.insert_text(
                pymupdf.Point(LEFT_MARGIN + 150, y),
                f"Date: {txn_date}",
                fontsize=9, fontname="helv", color=(0.2, 0.2, 0.2)
            )
            page.insert_text(
                pymupdf.Point(RIGHT_MARGIN - 80, y),
                f"{amount}",
                fontsize=10, fontname="hebo", color=(0.0, 0.3, 0.0)
            )
            y += LINE_HEIGHT

            # Merchant and category
            page.insert_text(
                pymupdf.Point(LEFT_MARGIN + 10, y),
                f"Merchant: {merchant}",
                fontsize=9, fontname="helv", color=(0.1, 0.1, 0.1)
            )
            page.insert_text(
                pymupdf.Point(LEFT_MARGIN + 300, y),
                f"Category: {category}",
                fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3)
            )
            y += LINE_HEIGHT

            # Card number line (if applicable)
            if has_cc:
                cc_num = cc_numbers[cc_index % len(cc_numbers)]
                page.insert_text(
                    pymupdf.Point(LEFT_MARGIN + 10, y),
                    f"Card: {cc_num}",
                    fontsize=9, fontname="cour", color=(0.1, 0.1, 0.1)
                )
                page.insert_text(
                    pymupdf.Point(LEFT_MARGIN + 250, y),
                    f"Authorization: AUTH-{random.randint(100000, 999999)}",
                    fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3)
                )
                cc_index += 1
                y += LINE_HEIGHT
            else:
                page.insert_text(
                    pymupdf.Point(LEFT_MARGIN + 10, y),
                    f"Payment Method: ACH Transfer",
                    fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3)
                )
                page.insert_text(
                    pymupdf.Point(LEFT_MARGIN + 250, y),
                    f"Authorization: AUTH-{random.randint(100000, 999999)}",
                    fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3)
                )
                y += LINE_HEIGHT

            # Status line
            statuses = ["Completed", "Settled", "Processed", "Cleared"]
            status = statuses[txn_global % len(statuses)]
            page.insert_text(
                pymupdf.Point(LEFT_MARGIN + 10, y),
                f"Status: {status}",
                fontsize=8, fontname="helv", color=(0.0, 0.5, 0.0)
            )
            y += LINE_HEIGHT

            # Separator between transactions
            shape2 = page.new_shape()
            shape2.draw_line(
                pymupdf.Point(LEFT_MARGIN + 5, y),
                pymupdf.Point(RIGHT_MARGIN - 5, y)
            )
            shape2.finish(color=(0.8, 0.8, 0.8), width=0.5, dashes="[2 2]")
            shape2.commit()
            y += SECTION_GAP + LINE_HEIGHT

            txn_global += 1

        # Footer
        page.insert_text(
            pymupdf.Point(LEFT_MARGIN, PAGE_H - 40),
            "ACME Financial Services | 1200 Commerce Blvd, Suite 400, San Francisco, CA 94105",
            fontsize=7, fontname="helv", color=(0.5, 0.5, 0.5)
        )
        page.insert_text(
            pymupdf.Point(LEFT_MARGIN, PAGE_H - 30),
            "This document contains sensitive financial information. Unauthorized distribution is prohibited.",
            fontsize=7, fontname="heit", color=(0.6, 0.3, 0.3)
        )

    # Set metadata
    doc.set_metadata({
        "title": "ACME Financial Services - Transaction Ledger",
        "author": "ACME Finance Department",
        "subject": "Transaction Log Q1-Q2 2025",
        "keywords": "transactions, finance, ledger, confidential",
        "creator": "ACME ERP System",
        "producer": "PyMuPDF",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
