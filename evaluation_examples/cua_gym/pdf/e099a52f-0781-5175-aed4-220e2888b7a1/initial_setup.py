"""
Initial Setup: Create payment records PDF with credit card numbers for redaction task
Task ID: pdf_gf2_028
Domain: pdf
"""

import os
import shlex
import subprocess
import time

import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_028'
FINANCE_DIR = f'{WORKDIR}/finance'
OUTPUT = f'{FINANCE_DIR}/payment_records.pdf'


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


# Credit card numbers to embed (18 total, spread across pages 1-6)
CARD_NUMBERS = [
    "4539-1234-5678-9012",
    "5412-7890-1234-5678",
    "3782-0012-3456-7890",
    "6011-4567-8901-2345",
    "4916-3344-5566-7788",
    "5500-1122-3344-5566",
    "3714-9256-0012-3456",
    "4024-0071-8923-4567",
    "5105-1051-0510-5100",
    "6011-0009-9013-9424",
    "4556-7375-8689-9855",
    "5425-2334-1102-9876",
    "3787-3449-3671-0005",
    "4929-5831-6047-1234",
    "5218-6100-7445-3890",
    "6011-1111-1111-1117",
    "4485-3922-6157-0014",
    "5390-2168-7412-9003",
]

# Payment records data - 3 records per page for pages 1-6
RECORDS = [
    # Page 1
    [
        {"name": "Sarah Chen", "date": "2025-11-02", "amount": "$1,245.99", "method": "Visa", "card": CARD_NUMBERS[0], "invoice": "INV-2025-0417"},
        {"name": "Marcus Johnson", "date": "2025-11-05", "amount": "$832.50", "method": "MasterCard", "card": CARD_NUMBERS[1], "invoice": "INV-2025-0423"},
        {"name": "Priya Patel", "date": "2025-11-08", "amount": "$2,100.00", "method": "Amex", "card": CARD_NUMBERS[2], "invoice": "INV-2025-0431"},
    ],
    # Page 2
    [
        {"name": "James O'Brien", "date": "2025-11-10", "amount": "$567.25", "method": "Discover", "card": CARD_NUMBERS[3], "invoice": "INV-2025-0445"},
        {"name": "Lin Wei", "date": "2025-11-12", "amount": "$3,450.00", "method": "Visa", "card": CARD_NUMBERS[4], "invoice": "INV-2025-0452"},
        {"name": "Elena Rodriguez", "date": "2025-11-14", "amount": "$189.99", "method": "MasterCard", "card": CARD_NUMBERS[5], "invoice": "INV-2025-0460"},
    ],
    # Page 3
    [
        {"name": "David Kim", "date": "2025-11-17", "amount": "$4,820.00", "method": "Amex", "card": CARD_NUMBERS[6], "invoice": "INV-2025-0471"},
        {"name": "Rachel Foster", "date": "2025-11-19", "amount": "$725.50", "method": "Visa", "card": CARD_NUMBERS[7], "invoice": "INV-2025-0478"},
        {"name": "Ahmed Hassan", "date": "2025-11-21", "amount": "$1,980.00", "method": "MasterCard", "card": CARD_NUMBERS[8], "invoice": "INV-2025-0485"},
    ],
    # Page 4
    [
        {"name": "Jessica Thompson", "date": "2025-11-23", "amount": "$342.75", "method": "Discover", "card": CARD_NUMBERS[9], "invoice": "INV-2025-0493"},
        {"name": "Robert Nakamura", "date": "2025-11-25", "amount": "$6,150.00", "method": "Visa", "card": CARD_NUMBERS[10], "invoice": "INV-2025-0501"},
        {"name": "Sofia Martinez", "date": "2025-12-01", "amount": "$1,475.25", "method": "MasterCard", "card": CARD_NUMBERS[11], "invoice": "INV-2025-0512"},
    ],
    # Page 5
    [
        {"name": "Thomas Wright", "date": "2025-12-03", "amount": "$890.00", "method": "Amex", "card": CARD_NUMBERS[12], "invoice": "INV-2025-0520"},
        {"name": "Maria Gonzalez", "date": "2025-12-05", "amount": "$2,340.50", "method": "Visa", "card": CARD_NUMBERS[13], "invoice": "INV-2025-0528"},
        {"name": "Yuki Tanaka", "date": "2025-12-08", "amount": "$1,100.00", "method": "MasterCard", "card": CARD_NUMBERS[14], "invoice": "INV-2025-0535"},
    ],
    # Page 6
    [
        {"name": "Christopher Lee", "date": "2025-12-10", "amount": "$4,200.00", "method": "Discover", "card": CARD_NUMBERS[15], "invoice": "INV-2025-0543"},
        {"name": "Anna Petrov", "date": "2025-12-12", "amount": "$615.75", "method": "Visa", "card": CARD_NUMBERS[16], "invoice": "INV-2025-0551"},
        {"name": "Daniel Okafor", "date": "2025-12-15", "amount": "$3,890.00", "method": "MasterCard", "card": CARD_NUMBERS[17], "invoice": "INV-2025-0558"},
    ],
]


def create_initial():
    os.makedirs(FINANCE_DIR, exist_ok=True)

    doc = pymupdf.open()
    page_width, page_height = 612, 792  # Letter size

    # --- Pages 1-6: Payment records ---
    for page_idx, page_records in enumerate(RECORDS):
        page = doc.new_page(width=page_width, height=page_height)

        # Header
        page.insert_text(
            pymupdf.Point(72, 50),
            "ACME Financial Services — Payment Records",
            fontsize=14,
            fontname="hebo",
            color=(0, 0, 0.4),
        )
        page.insert_text(
            pymupdf.Point(72, 68),
            f"Page {page_idx + 1} of 7   |   Report Generated: 2025-12-20   |   CONFIDENTIAL",
            fontsize=8,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

        # Horizontal rule
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, 75), pymupdf.Point(540, 75))
        shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
        shape.commit()

        y = 100
        for rec_idx, rec in enumerate(page_records):
            # Record header
            page.insert_text(
                pymupdf.Point(72, y),
                f"Transaction #{(page_idx * 3) + rec_idx + 1}",
                fontsize=11,
                fontname="hebo",
                color=(0, 0, 0),
            )
            y += 20

            # Record details in a table-like layout
            fields = [
                ("Customer:", rec["name"]),
                ("Date:", rec["date"]),
                ("Amount:", rec["amount"]),
                ("Payment Method:", rec["method"]),
                ("Card Number:", rec["card"]),
                ("Invoice:", rec["invoice"]),
            ]
            for label, value in fields:
                page.insert_text(
                    pymupdf.Point(90, y),
                    label,
                    fontsize=10,
                    fontname="hebo",
                    color=(0.2, 0.2, 0.2),
                )
                page.insert_text(
                    pymupdf.Point(200, y),
                    value,
                    fontsize=10,
                    fontname="helv",
                    color=(0, 0, 0),
                )
                y += 16

            # Separator between records
            y += 10
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(540, y))
            shape.finish(color=(0.85, 0.85, 0.85), width=0.3)
            shape.commit()
            y += 20

        # Footer
        page.insert_text(
            pymupdf.Point(72, 755),
            "ACME Financial Services  |  123 Commerce Blvd, Suite 400, New York, NY 10001",
            fontsize=7,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    # --- Page 7: Summary ---
    page = doc.new_page(width=page_width, height=page_height)
    page.insert_text(
        pymupdf.Point(72, 50),
        "ACME Financial Services — Payment Records",
        fontsize=14,
        fontname="hebo",
        color=(0, 0, 0.4),
    )
    page.insert_text(
        pymupdf.Point(72, 68),
        "Page 7 of 7   |   Report Generated: 2025-12-20   |   CONFIDENTIAL",
        fontsize=8,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 75), pymupdf.Point(540, 75))
    shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
    shape.commit()

    page.insert_text(
        pymupdf.Point(72, 100),
        "Summary of Payment Transactions",
        fontsize=13,
        fontname="hebo",
        color=(0, 0, 0),
    )

    summary_text = (
        "This report contains 18 payment transactions processed between "
        "November 2, 2025 and December 15, 2025. Total amount processed: $36,925.49. "
        "All transactions were authorized and settled successfully.\n\n"
        "Payment Method Breakdown:\n"
        "  Visa:        7 transactions ($19,447.49)\n"
        "  MasterCard:  6 transactions ($9,468.24)\n"
        "  Amex:        3 transactions ($7,810.00)\n"
        "  Discover:    2 transactions ($4,542.75)\n\n"
        "Note: This document contains sensitive cardholder data subject to "
        "PCI DSS compliance requirements. Handle according to company data "
        "protection policy DP-2024-07. Unauthorized distribution is prohibited.\n\n"
        "For questions regarding this report, contact the Finance Department "
        "at finance@acme-financial.com or ext. 4521."
    )
    page.insert_textbox(
        pymupdf.Rect(72, 120, 540, 500),
        summary_text,
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # Footer
    page.insert_text(
        pymupdf.Point(72, 755),
        "ACME Financial Services  |  123 Commerce Blvd, Suite 400, New York, NY 10001",
        fontsize=7,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Total pages: 7, Total credit card numbers: 18')

    # GUI-ready: open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
