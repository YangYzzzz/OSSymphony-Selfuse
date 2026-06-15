"""
Initial Setup: Multi-app workflow PDF cross-domain task
Task ID: pdf_cross_139
Domain: libreoffice_calc (cross-domain: PDF + Terminal + VSCode + LibreOffice Calc)

Creates:
  - ~/Documents/raw_data.pdf  (4-page PDF with 50 rows of semi-structured data)

Does NOT create:
  - data.csv  (agent must extract and parse)
  - pdf_cross_139.xlsx  (agent must create)
  - data_analysis.pdf  (agent must export from Calc)

GUI: Opens raw_data.pdf in evince and opens a Terminal
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
DOCS_DIR = '/home/user/Documents'
TASK_ID = 'pdf_cross_139'
PDF_PATH = f'{DOCS_DIR}/raw_data.pdf'


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


# Realistic data: 50 rows with Date, Category, Amount, Status
# With minor formatting inconsistencies to make parsing challenging
RAW_DATA = [
    # (Date, Category, Amount, Status)  -- some with formatting inconsistencies
    ("2024-01-05", "Technology",   1250.00,  "Completed"),
    ("2024-01-08", "Healthcare",    890.50,  "Completed"),
    ("2024-01-12", "Finance",      3200.00,  "Pending"),
    ("2024-01-15", "Retail",        450.75,  "Completed"),
    ("2024-01-19", "Education",     780.00,  "Completed"),
    ("2024-01-22", "Technology",   2100.00,  "Cancelled"),
    ("2024-01-25", "Healthcare",   1560.25,  "Completed"),
    ("2024-01-29", "Finance",      4750.00,  "Completed"),
    ("2024-02-02", "Retail",        325.50,  "Pending"),
    ("2024-02-05", "Education",     995.00,  "Completed"),
    ("2024-02-09", "Technology",   3400.00,  "Completed"),
    ("2024-02-12", "Healthcare",    670.75,  "Completed"),
    ("2024-02-16", "Finance",      2800.00,  "Pending"),
    ("2024-02-19", "Retail",        510.00,  "Completed"),
    ("2024-02-23", "Education",    1200.00,  "Completed"),
    ("2024-02-26", "Technology",   1875.50,  "Completed"),
    ("2024-03-01", "Healthcare",   2300.00,  "Cancelled"),
    ("2024-03-05", "Finance",      5100.00,  "Completed"),
    ("2024-03-08", "Retail",        285.25,  "Completed"),
    ("2024-03-12", "Education",     840.00,  "Pending"),
    ("2024-03-15", "Technology",   2650.00,  "Completed"),
    ("2024-03-19", "Healthcare",    990.50,  "Completed"),
    ("2024-03-22", "Finance",      3600.00,  "Completed"),
    ("2024-03-26", "Retail",        625.75,  "Completed"),
    ("2024-03-29", "Education",    1450.00,  "Completed"),
    ("2024-04-02", "Technology",   1980.00,  "Pending"),
    ("2024-04-05", "Healthcare",   1340.25,  "Completed"),
    ("2024-04-09", "Finance",      2950.00,  "Completed"),
    ("2024-04-12", "Retail",        390.50,  "Cancelled"),
    ("2024-04-16", "Education",     710.00,  "Completed"),
    ("2024-04-19", "Technology",   3150.00,  "Completed"),
    ("2024-04-23", "Healthcare",    825.75,  "Completed"),
    ("2024-04-26", "Finance",      4200.00,  "Pending"),
    ("2024-04-30", "Retail",        545.00,  "Completed"),
    ("2024-05-03", "Education",    1100.00,  "Completed"),
    ("2024-05-07", "Technology",   2420.00,  "Completed"),
    ("2024-05-10", "Healthcare",   1780.50,  "Completed"),
    ("2024-05-14", "Finance",      3850.00,  "Completed"),
    ("2024-05-17", "Retail",        460.25,  "Pending"),
    ("2024-05-21", "Education",     930.00,  "Completed"),
    ("2024-05-24", "Technology",   1650.00,  "Completed"),
    ("2024-05-28", "Healthcare",   2150.00,  "Completed"),
    ("2024-05-31", "Finance",      6200.00,  "Completed"),
    ("2024-06-04", "Retail",        380.75,  "Cancelled"),
    ("2024-06-07", "Education",    1320.00,  "Completed"),
    ("2024-06-11", "Technology",   2890.00,  "Completed"),
    ("2024-06-14", "Healthcare",    755.50,  "Completed"),
    ("2024-06-18", "Finance",      4450.00,  "Pending"),
    ("2024-06-21", "Retail",        590.00,  "Completed"),
    ("2024-06-25", "Education",    1080.00,  "Completed"),
]

# Introduce formatting inconsistencies in some rows (as displayed in the PDF)
# These are the "raw" display versions with inconsistencies
RAW_DISPLAY = []
for i, (date, cat, amount, status) in enumerate(RAW_DATA):
    # Occasional date format variation
    if i in (4, 11, 18, 25, 33, 40, 47):
        parts = date.split("-")
        display_date = f"{parts[1]}/{parts[2]}/{parts[0]}"  # MM/DD/YYYY
    elif i in (7, 14, 21, 28, 35, 42, 49):
        parts = date.split("-")
        display_date = f"{parts[2]}-{parts[1]}-{parts[0]}"  # DD-MM-YYYY
    else:
        display_date = date  # YYYY-MM-DD (standard)

    # Occasional amount formatting variation (no decimal vs 2 decimal)
    if i in (2, 5, 8, 12, 17, 22, 27, 32, 37, 43, 48):
        display_amount = f"${int(amount):,}"  # No decimal
    else:
        display_amount = f"${amount:,.2f}"

    # Occasional extra spaces or missing status
    if i in (6, 20, 34):
        display_status = f"  {status}"  # leading spaces
    else:
        display_status = status

    RAW_DISPLAY.append((display_date, cat, display_amount, display_status))


def create_raw_pdf():
    """Create the 4-page raw_data.pdf with 50 rows of semi-structured data."""
    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page dimensions (A4)
    PAGE_W, PAGE_H = 595, 842
    MARGIN_L = 50
    MARGIN_T = 60
    MARGIN_B = 50
    ROW_H = 16
    HEADER_H = 20

    # Column widths
    col_widths = [105, 100, 90, 100]
    col_headers = ["Date", "Category", "Amount", "Status"]

    # Colors
    COLOR_HEADER_BG = (0.2, 0.4, 0.7)   # blue header
    COLOR_ALT_BG = (0.95, 0.95, 0.97)    # light blue-gray alternate row
    COLOR_WHITE = (1, 1, 1)
    COLOR_TEXT = (0.1, 0.1, 0.1)
    COLOR_HEADER_TEXT = (1, 1, 1)
    COLOR_GRID = (0.6, 0.6, 0.6)
    COLOR_TITLE = (0.15, 0.3, 0.6)

    rows_per_page = 13  # rows per page (4 pages for 50 rows + header)

    for page_num in range(4):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        shape = page.new_shape()

        # Title
        title_y = MARGIN_T
        page.insert_text(
            pymupdf.Point(MARGIN_L, title_y),
            "Business Transaction Data - Q1/Q2 2024",
            fontsize=14,
            fontname="hebo",
            color=COLOR_TITLE,
        )

        subtitle_y = title_y + 18
        page.insert_text(
            pymupdf.Point(MARGIN_L, subtitle_y),
            f"Page {page_num + 1} of 4  |  Raw Export (semi-structured format)",
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

        # Draw header background
        header_y = subtitle_y + 14
        header_rect = pymupdf.Rect(
            MARGIN_L, header_y,
            MARGIN_L + sum(col_widths), header_y + HEADER_H
        )
        shape.draw_rect(header_rect)
        shape.finish(fill=COLOR_HEADER_BG, color=COLOR_GRID, width=0.5)

        # Draw header text
        x_offset = MARGIN_L + 4
        for col_i, (hdr, cw) in enumerate(zip(col_headers, col_widths)):
            page.insert_text(
                pymupdf.Point(x_offset, header_y + 13),
                hdr,
                fontsize=10,
                fontname="hebo",
                color=COLOR_HEADER_TEXT,
            )
            x_offset += cw

        # Draw data rows
        start_row = page_num * rows_per_page
        end_row = min(start_row + rows_per_page, 50)
        row_y = header_y + HEADER_H

        for row_i, data_idx in enumerate(range(start_row, end_row)):
            display_date, cat, display_amount, display_status = RAW_DISPLAY[data_idx]

            # Alternate row background
            bg_color = COLOR_ALT_BG if row_i % 2 == 1 else COLOR_WHITE
            row_rect = pymupdf.Rect(
                MARGIN_L, row_y,
                MARGIN_L + sum(col_widths), row_y + ROW_H
            )
            shape.draw_rect(row_rect)
            shape.finish(fill=bg_color, color=COLOR_GRID, width=0.3)

            # Draw row number (small, gray)
            page.insert_text(
                pymupdf.Point(MARGIN_L - 30, row_y + 11),
                str(data_idx + 1),
                fontsize=7,
                fontname="helv",
                color=(0.6, 0.6, 0.6),
            )

            # Draw cell text
            x_offset = MARGIN_L + 4
            for col_i, (cell_val, cw) in enumerate(zip(
                [display_date, cat, display_amount, display_status], col_widths
            )):
                page.insert_text(
                    pymupdf.Point(x_offset, row_y + 11),
                    str(cell_val),
                    fontsize=9,
                    fontname="helv",
                    color=COLOR_TEXT,
                )
                x_offset += cw

            row_y += ROW_H

        # Draw vertical column separators
        x_pos = MARGIN_L
        for cw in col_widths:
            shape.draw_line(
                pymupdf.Point(x_pos, header_y),
                pymupdf.Point(x_pos, row_y)
            )
            shape.finish(color=COLOR_GRID, width=0.5)
            x_pos += cw
        # Right border
        shape.draw_line(
            pymupdf.Point(x_pos, header_y),
            pymupdf.Point(x_pos, row_y)
        )
        shape.finish(color=COLOR_GRID, width=0.5)

        # Footer note (formatting inconsistency note)
        footer_y = PAGE_H - MARGIN_B
        page.insert_text(
            pymupdf.Point(MARGIN_L, footer_y),
            "Note: Export may contain date format variations and amount formatting inconsistencies.",
            fontsize=7,
            fontname="tiit",
            color=(0.5, 0.5, 0.5),
        )

        shape.commit()

    doc.save(PDF_PATH)
    doc.close()
    print(f"Created: {PDF_PATH}")


def main():
    create_raw_pdf()

    # GUI-ready startup: open evince with raw_data.pdf and a terminal
    # Kill any existing instances first (idempotent)
    subprocess.run(['pkill', '-f', 'raw_data.pdf'], capture_output=True)
    time.sleep(0.5)

    # Open raw_data.pdf in evince
    launch_gui(f'evince "{PDF_PATH}"', delay_sec=2.0)

    # Open terminal (gnome-terminal)
    launch_gui('gnome-terminal', delay_sec=1.5)

    print('GUI_READY: launched evince (raw_data.pdf) and gnome-terminal with DISPLAY=:0')


main()
