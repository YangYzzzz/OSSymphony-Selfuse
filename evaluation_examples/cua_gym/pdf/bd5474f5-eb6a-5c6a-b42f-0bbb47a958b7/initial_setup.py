"""
Initial Setup: Create a static petty cash log PDF template
Task ID: pdf_fin_069
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_069'
FINANCE_DIR = f'{WORKDIR}/finance'
OUTPUT = f'{FINANCE_DIR}/petty_cash_log.pdf'

# Page layout constants
PAGE_W, PAGE_H = 612, 792  # Letter size
MARGIN_LEFT = 50
MARGIN_RIGHT = 562
TABLE_TOP = 200
ROW_HEIGHT = 22
HEADER_ROW_Y = TABLE_TOP
NUM_ROWS = 20

# Column positions (x coordinates)
COL_DATE_X = 50
COL_DESC_X = 150
COL_IN_X = 350
COL_OUT_X = 450
COL_END_X = 562

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
    page = doc.new_page(width=PAGE_W, height=PAGE_H)

    # ---- Title ----
    page.insert_text(
        pymupdf.Point(PAGE_W / 2 - 100, 40),
        "PETTY CASH LOG",
        fontsize=20,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    # ---- Company info line ----
    page.insert_text(
        pymupdf.Point(PAGE_W / 2 - 80, 58),
        "Meridian Consulting Group",
        fontsize=10,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

    # ---- Fund Custodian label ----
    page.insert_text(
        pymupdf.Point(50, 90),
        "Fund Custodian:",
        fontsize=11,
        fontname="hebo",
        color=(0, 0, 0),
    )
    # Draw an underline / blank area for custodian name (static, no form field)
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(150, 92), pymupdf.Point(350, 92))
    shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
    shape.commit()

    # ---- Date range label ----
    page.insert_text(
        pymupdf.Point(400, 90),
        "Period: Q1 2026",
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
    )

    # ---- Starting Balance label ----
    page.insert_text(
        pymupdf.Point(50, 120),
        "Starting Balance: $500.00",
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
    )

    # ---- Instructions ----
    page.insert_text(
        pymupdf.Point(50, 145),
        "Record all petty cash transactions below. Attach receipts for each entry.",
        fontsize=8,
        fontname="heit",
        color=(0.4, 0.4, 0.4),
    )

    # ---- Horizontal separator ----
    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(MARGIN_LEFT, 160), pymupdf.Point(MARGIN_RIGHT, 160))
    shape2.finish(color=(0.1, 0.1, 0.4), width=1.5)
    shape2.commit()

    # ---- Table Header ----
    header_y = 185
    headers = [
        (COL_DATE_X + 5, "Date"),
        (COL_DESC_X + 5, "Description"),
        (COL_IN_X + 5, "Amount In"),
        (COL_OUT_X + 5, "Amount Out"),
    ]
    for hx, htxt in headers:
        page.insert_text(
            pymupdf.Point(hx, header_y),
            htxt,
            fontsize=10,
            fontname="hebo",
            color=(1, 1, 1),
        )

    # Header background
    shape3 = page.new_shape()
    shape3.draw_rect(pymupdf.Rect(MARGIN_LEFT, 170, MARGIN_RIGHT, 192))
    shape3.finish(color=None, fill=(0.15, 0.15, 0.45))
    shape3.commit()

    # Re-draw header text on top of background
    # Since shapes are behind text in draw order, re-insert text
    for hx, htxt in headers:
        page.insert_text(
            pymupdf.Point(hx, header_y),
            htxt,
            fontsize=10,
            fontname="hebo",
            color=(1, 1, 1),
        )

    # ---- Table Grid Lines ----
    shape4 = page.new_shape()

    # Horizontal lines for each row
    for i in range(NUM_ROWS + 1):
        y = TABLE_TOP + i * ROW_HEIGHT
        shape4.draw_line(pymupdf.Point(MARGIN_LEFT, y), pymupdf.Point(MARGIN_RIGHT, y))

    # Vertical column dividers
    for x in [MARGIN_LEFT, COL_DESC_X, COL_IN_X, COL_OUT_X, MARGIN_RIGHT]:
        shape4.draw_line(
            pymupdf.Point(x, TABLE_TOP),
            pymupdf.Point(x, TABLE_TOP + NUM_ROWS * ROW_HEIGHT),
        )

    shape4.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape4.commit()

    # ---- Alternating row shading ----
    shape5 = page.new_shape()
    for i in range(NUM_ROWS):
        if i % 2 == 1:
            y = TABLE_TOP + i * ROW_HEIGHT
            shape5.draw_rect(pymupdf.Rect(MARGIN_LEFT, y, MARGIN_RIGHT, y + ROW_HEIGHT))
    shape5.finish(color=None, fill=(0.94, 0.94, 0.97))
    shape5.commit()

    # ---- Bottom Balance Section ----
    bottom_y = TABLE_TOP + NUM_ROWS * ROW_HEIGHT + 25
    page.insert_text(
        pymupdf.Point(350, bottom_y),
        "Current Balance:",
        fontsize=11,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )
    # Underline for balance value (static)
    shape6 = page.new_shape()
    shape6.draw_line(pymupdf.Point(450, bottom_y + 3), pymupdf.Point(560, bottom_y + 3))
    shape6.finish(color=(0.6, 0.6, 0.6), width=0.5)
    shape6.commit()

    # ---- Footer ----
    page.insert_text(
        pymupdf.Point(50, 740),
        "Authorized Signature: ________________________    Date: ______________",
        fontsize=9,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(50, 760),
        "Meridian Consulting Group  |  Finance Department  |  Petty Cash Management",
        fontsize=7,
        fontname="heit",
        color=(0.5, 0.5, 0.5),
    )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for agent GUI
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
