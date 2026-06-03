"""
Initial Setup: Create a PDF with tabular data for CSV extraction task
Task ID: pdf_cf_045
Domain: libreoffice_calc (PDF source)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_cf_045'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/spreadsheet_export.pdf'


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
    os.makedirs(DOCS_DIR, exist_ok=True)

    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf

    doc = pymupdf.open()
    page = doc.new_page(width=612, height=792)  # Letter size

    # Title
    page.insert_text(
        pymupdf.Point(72, 50),
        "Quarterly Sales Report - Regional Performance",
        fontsize=16,
        fontname="hebo",
        color=(0.1, 0.1, 0.3),
    )

    # Subtitle
    page.insert_text(
        pymupdf.Point(72, 72),
        "FY2025 Q1 Summary  |  Generated: 2025-03-31",
        fontsize=9,
        fontname="heit",
        color=(0.4, 0.4, 0.4),
    )

    # Table data: 5 columns, 1 header + 20 data rows
    headers = ["Region", "Product", "Units Sold", "Revenue", "Margin %"]
    data = [
        ["Northeast",   "Widget A",     "1245",  "62250.00",  "18.5"],
        ["Northeast",   "Widget B",     "873",   "52380.00",  "22.1"],
        ["Southeast",   "Widget A",     "1102",  "55100.00",  "17.8"],
        ["Southeast",   "Widget C",     "654",   "45780.00",  "25.3"],
        ["Midwest",     "Widget A",     "987",   "49350.00",  "19.2"],
        ["Midwest",     "Widget B",     "1320",  "79200.00",  "21.7"],
        ["Midwest",     "Widget D",     "445",   "35600.00",  "28.4"],
        ["West Coast",  "Widget A",     "1578",  "78900.00",  "16.9"],
        ["West Coast",  "Widget B",     "1034",  "62040.00",  "20.5"],
        ["West Coast",  "Widget C",     "762",   "53340.00",  "24.8"],
        ["Southwest",   "Widget D",     "523",   "41840.00",  "27.6"],
        ["Southwest",   "Widget A",     "891",   "44550.00",  "18.1"],
        ["Northwest",   "Widget B",     "1156",  "69360.00",  "22.9"],
        ["Northwest",   "Widget C",     "698",   "48860.00",  "26.1"],
        ["Central",     "Widget A",     "1045",  "52250.00",  "17.4"],
        ["Central",     "Widget D",     "387",   "30960.00",  "29.8"],
        ["Northeast",   "Widget D",     "612",   "48960.00",  "26.7"],
        ["Southeast",   "Widget B",     "945",   "56700.00",  "21.3"],
        ["West Coast",  "Widget D",     "489",   "39120.00",  "28.0"],
        ["Midwest",     "Widget C",     "718",   "50260.00",  "25.0"],
    ]

    # Table layout
    col_x = [72, 155, 260, 355, 450]  # left x for each column
    col_right = [150, 255, 350, 445, 540]  # right boundary (for alignment)
    start_y = 110
    row_height = 22
    table_width = 540 - 72

    # Draw table header background
    header_rect = pymupdf.Rect(72, start_y - 15, 540, start_y + 7)
    shape = page.new_shape()
    shape.draw_rect(header_rect)
    shape.finish(color=(0.2, 0.3, 0.5), fill=(0.2, 0.3, 0.5), width=0.5)
    shape.commit()

    # Header text (white on dark)
    for i, h in enumerate(headers):
        page.insert_text(
            pymupdf.Point(col_x[i] + 3, start_y + 2),
            h,
            fontsize=10,
            fontname="hebo",
            color=(1, 1, 1),
        )

    # Draw horizontal line under header
    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(72, start_y + 9), pymupdf.Point(540, start_y + 9))
    shape2.finish(color=(0.3, 0.3, 0.3), width=1)

    # Data rows
    for r, row_data in enumerate(data):
        y = start_y + (r + 1) * row_height + 2

        # Alternate row background
        if r % 2 == 0:
            row_rect = pymupdf.Rect(72, y - 15, 540, y + 7)
            shape2.draw_rect(row_rect)
            shape2.finish(color=None, fill=(0.94, 0.94, 0.97), width=0)

        for c, val in enumerate(row_data):
            page.insert_text(
                pymupdf.Point(col_x[c] + 3, y + 2),
                val,
                fontsize=9,
                fontname="helv",
                color=(0.1, 0.1, 0.1),
            )

    # Draw table borders
    table_bottom = start_y + 21 * row_height + 7
    # Outer border
    shape2.draw_rect(pymupdf.Rect(72, start_y - 15, 540, table_bottom))
    shape2.finish(color=(0.4, 0.4, 0.4), width=1)

    # Vertical column dividers
    for x in col_x[1:]:
        shape2.draw_line(pymupdf.Point(x, start_y - 15), pymupdf.Point(x, table_bottom))
        shape2.finish(color=(0.7, 0.7, 0.7), width=0.5)

    # Horizontal row dividers
    for r in range(1, 21):
        ry = start_y + r * row_height + 9
        shape2.draw_line(pymupdf.Point(72, ry), pymupdf.Point(540, ry))
        shape2.finish(color=(0.85, 0.85, 0.85), width=0.3)

    shape2.commit()

    # Footer
    page.insert_text(
        pymupdf.Point(72, 760),
        "Confidential - Internal Use Only",
        fontsize=8,
        fontname="heit",
        color=(0.5, 0.5, 0.5),
    )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial PDF created: {OUTPUT}')

    # Open PDF in Evince for the agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
