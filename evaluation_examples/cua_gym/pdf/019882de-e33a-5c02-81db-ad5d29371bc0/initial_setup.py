"""
Initial Setup: Multi-app PDF mailing workflow
Task ID: pdf_cross_150
Domain: pdf

Creates ~/Documents/recipients.pdf with 5 recipients listed.
Opens the file in evince and LibreOffice Writer for the agent to start working.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_cross_150'
DOCS_DIR = f'{WORKDIR}/Documents'
RECIPIENTS_PDF = f'{DOCS_DIR}/recipients.pdf'


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


def create_recipients_pdf():
    """Create ~/Documents/recipients.pdf listing 5 recipients."""
    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf

    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()
    page = doc.new_page(width=612, height=792)  # Letter size

    # Title area
    page.insert_text(
        pymupdf.Point(72, 72),
        "Mailing Recipients List",
        fontsize=18,
        fontname="hebo",
        color=(0, 0, 0.5),
    )

    # Subtitle / date
    page.insert_text(
        pymupdf.Point(72, 100),
        "Academic & Industry Outreach - Spring 2025",
        fontsize=11,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

    # Horizontal rule (drawn as a rectangle)
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 115), pymupdf.Point(540, 115))
    shape.finish(color=(0.4, 0.4, 0.4), width=1.5)
    shape.commit()

    # Column headers
    page.insert_text(pymupdf.Point(72, 145), "Name", fontsize=11, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(230, 145), "Organization", fontsize=11, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(390, 145), "Location", fontsize=11, fontname="hebo", color=(0, 0, 0))

    # Header underline
    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(72, 155), pymupdf.Point(540, 155))
    shape2.finish(color=(0.6, 0.6, 0.6), width=0.5)
    shape2.commit()

    # Recipients data
    recipients = [
        ("Dr. Emily Watson",    "Stanford University",   "Palo Alto, CA"),
        ("Prof. Robert Chang",  "MIT",                   "Cambridge, MA"),
        ("Ms. Laura Fisher",    "Google",                "Mountain View, CA"),
        ("Mr. Kevin O'Brien",   "Amazon",                "Seattle, WA"),
        ("Dr. Aisha Patel",     "Johns Hopkins",         "Baltimore, MD"),
    ]

    y_start = 175
    row_height = 30

    for i, (name, org, location) in enumerate(recipients):
        y = y_start + i * row_height

        # Alternate row shading
        if i % 2 == 0:
            shade_shape = page.new_shape()
            shade_shape.draw_rect(pymupdf.Rect(68, y - 14, 544, y + 14))
            shade_shape.finish(fill=(0.95, 0.95, 0.98), color=None, width=0)
            shade_shape.commit()

        page.insert_text(pymupdf.Point(72, y), name, fontsize=11, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(230, y), org, fontsize=11, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(390, y), location, fontsize=11, fontname="helv", color=(0, 0, 0))

        # Row number (small, left margin)
        page.insert_text(pymupdf.Point(50, y), str(i + 1), fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # Bottom separator
    shape3 = page.new_shape()
    shape3.draw_line(pymupdf.Point(72, y_start + len(recipients) * row_height), pymupdf.Point(540, y_start + len(recipients) * row_height))
    shape3.finish(color=(0.6, 0.6, 0.6), width=0.5)
    shape3.commit()

    # Footer note
    footer_y = y_start + len(recipients) * row_height + 30
    page.insert_text(
        pymupdf.Point(72, footer_y),
        f"Total recipients: {len(recipients)}    |    Generated for form letter mailing batch",
        fontsize=9,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )

    # Additional contact info section
    info_y = footer_y + 50
    page.insert_text(
        pymupdf.Point(72, info_y),
        "Instructions:",
        fontsize=11,
        fontname="hebo",
        color=(0, 0, 0),
    )
    instructions = [
        "1. Create personalized form letters using the above recipient data.",
        "2. Each letter should be addressed to the recipient by name and organization.",
        "3. Export each letter as an individual PDF file.",
        "4. Merge all letters into a single mailing batch PDF with sequential page numbers.",
        "5. Save the final merged document as ~/Documents/mailing_batch.pdf",
    ]
    for j, line in enumerate(instructions):
        page.insert_text(
            pymupdf.Point(72, info_y + 20 + j * 18),
            line,
            fontsize=10,
            fontname="helv",
            color=(0.2, 0.2, 0.2),
        )

    doc.save(RECIPIENTS_PDF)
    doc.close()
    print(f"Created: {RECIPIENTS_PDF}")


def create_initial():
    create_recipients_pdf()

    # Launch LibreOffice Writer for the agent to start working
    launch_gui('libreoffice --writer', delay_sec=2.0)
    print("GUI_READY: launched LibreOffice Writer with DISPLAY=:0")


create_initial()
