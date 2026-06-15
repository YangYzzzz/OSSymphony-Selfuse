"""
Initial Setup: Create a multi-page financial PDF with a table on page 3
Task ID: pdf_mbc_071
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_071'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/financial_data.pdf'


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

    # Remove any pre-existing CSV to ensure clean initial state
    csv_path = f'{DOCS_DIR}/table_page3.csv'
    if os.path.exists(csv_path):
        os.remove(csv_path)

    import pymupdf

    doc = pymupdf.open()

    # --- Page 1: Title Page ---
    page1 = doc.new_page(width=595, height=842)
    # Title
    page1.insert_text(
        pymupdf.Point(150, 200),
        "Nextera Financial Group",
        fontsize=24,
        fontname="hebo",
        color=(0.0, 0.15, 0.45),
    )
    page1.insert_text(
        pymupdf.Point(165, 250),
        "Annual Financial Report",
        fontsize=18,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
    )
    page1.insert_text(
        pymupdf.Point(220, 290),
        "Fiscal Year 2025",
        fontsize=14,
        fontname="heit",
        color=(0.4, 0.4, 0.4),
    )
    # Decorative line
    shape1 = page1.new_shape()
    shape1.draw_line(pymupdf.Point(120, 310), pymupdf.Point(475, 310))
    shape1.finish(color=(0.0, 0.15, 0.45), width=2)
    shape1.commit()

    page1.insert_text(
        pymupdf.Point(130, 380),
        "Prepared by: Office of the Chief Financial Officer",
        fontsize=11,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page1.insert_text(
        pymupdf.Point(200, 410),
        "Date: March 28, 2026",
        fontsize=11,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page1.insert_text(
        pymupdf.Point(150, 440),
        "Classification: Internal — Confidential",
        fontsize=10,
        fontname="heit",
        color=(0.5, 0.0, 0.0),
    )

    # --- Page 2: Executive Summary ---
    page2 = doc.new_page(width=595, height=842)
    page2.insert_text(
        pymupdf.Point(72, 72),
        "Executive Summary",
        fontsize=18,
        fontname="hebo",
        color=(0.0, 0.15, 0.45),
    )
    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, 80), pymupdf.Point(523, 80))
    shape2.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape2.commit()

    summary_text = (
        "Nextera Financial Group delivered strong results in fiscal year 2025, "
        "achieving total annual revenue of $3,250,000 across all business units. "
        "Despite rising operational costs driven by expansion into new markets and "
        "increased headcount, the company maintained healthy profit margins throughout "
        "the year.\n\n"
        "Key highlights include a 12% year-over-year revenue increase in Q4, driven "
        "primarily by our enterprise solutions division. Expense management initiatives "
        "launched in Q2 helped contain cost growth to 8%, well below the industry "
        "average of 14%.\n\n"
        "The following pages contain detailed quarterly breakdowns of revenue, "
        "expenses, and profit figures. Management recommends reviewing the Q3 "
        "performance closely, as it reflects the impact of the restructuring program "
        "announced in July 2025.\n\n"
        "Looking ahead to FY2026, the leadership team is cautiously optimistic. "
        "New product launches scheduled for Q1 and Q2 are expected to drive "
        "incremental revenue growth of 15-18%. The board has approved a capital "
        "expenditure budget of $450,000 for technology upgrades and facility expansion."
    )
    rect2 = pymupdf.Rect(72, 100, 523, 750)
    page2.insert_textbox(
        rect2,
        summary_text,
        fontsize=11,
        fontname="helv",
        color=(0.1, 0.1, 0.1),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 3: Quarterly Financial Data Table ---
    page3 = doc.new_page(width=595, height=842)
    page3.insert_text(
        pymupdf.Point(72, 72),
        "Quarterly Financial Breakdown",
        fontsize=18,
        fontname="hebo",
        color=(0.0, 0.15, 0.45),
    )
    shape3 = page3.new_shape()
    shape3.draw_line(pymupdf.Point(72, 80), pymupdf.Point(523, 80))
    shape3.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape3.commit()

    page3.insert_text(
        pymupdf.Point(72, 110),
        "The table below summarizes quarterly revenue, expenses, and profit for FY2025.",
        fontsize=11,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
    )

    # Table data
    headers = ["Quarter", "Revenue", "Expenses", "Profit"]
    data_rows = [
        ["Q1", "$780,000", "$540,000", "$240,000"],
        ["Q2", "$820,000", "$575,000", "$245,000"],
        ["Q3", "$790,000", "$560,000", "$230,000"],
        ["Q4", "$860,000", "$590,000", "$270,000"],
    ]

    # Table layout
    table_x = 90
    table_y_start = 140
    col_widths = [100, 110, 110, 110]
    row_height = 30
    total_width = sum(col_widths)

    # Draw header background
    shape_t = page3.new_shape()
    header_rect = pymupdf.Rect(
        table_x, table_y_start,
        table_x + total_width, table_y_start + row_height,
    )
    shape_t.draw_rect(header_rect)
    shape_t.finish(color=(0.0, 0.15, 0.45), fill=(0.0, 0.15, 0.45), width=0.5)

    # Draw alternating row backgrounds
    for i in range(len(data_rows)):
        row_y = table_y_start + (i + 1) * row_height
        row_rect = pymupdf.Rect(
            table_x, row_y,
            table_x + total_width, row_y + row_height,
        )
        fill_color = (0.95, 0.95, 0.97) if i % 2 == 0 else (1.0, 1.0, 1.0)
        shape_t.draw_rect(row_rect)
        shape_t.finish(color=(0.7, 0.7, 0.7), fill=fill_color, width=0.5)

    # Draw grid lines
    total_rows = 1 + len(data_rows)
    # Horizontal lines
    for i in range(total_rows + 1):
        y = table_y_start + i * row_height
        shape_t.draw_line(
            pymupdf.Point(table_x, y),
            pymupdf.Point(table_x + total_width, y),
        )
        shape_t.finish(color=(0.5, 0.5, 0.5), width=0.5)

    # Vertical lines
    x_pos = table_x
    for w in [0] + col_widths:
        x_pos_line = table_x + sum(col_widths[:col_widths.index(w)]) if w in col_widths else table_x
    # Re-do vertical lines properly
    x_acc = table_x
    for i in range(len(col_widths) + 1):
        shape_t.draw_line(
            pymupdf.Point(x_acc, table_y_start),
            pymupdf.Point(x_acc, table_y_start + total_rows * row_height),
        )
        shape_t.finish(color=(0.5, 0.5, 0.5), width=0.5)
        if i < len(col_widths):
            x_acc += col_widths[i]

    shape_t.commit()

    # Insert header text
    x_acc = table_x
    for j, header in enumerate(headers):
        text_x = x_acc + 10
        text_y = table_y_start + 20
        page3.insert_text(
            pymupdf.Point(text_x, text_y),
            header,
            fontsize=11,
            fontname="hebo",
            color=(1.0, 1.0, 1.0),
        )
        x_acc += col_widths[j]

    # Insert data rows
    for i, row in enumerate(data_rows):
        x_acc = table_x
        for j, cell in enumerate(row):
            text_x = x_acc + 10
            text_y = table_y_start + (i + 1) * row_height + 20
            page3.insert_text(
                pymupdf.Point(text_x, text_y),
                cell,
                fontsize=10,
                fontname="helv",
                color=(0.1, 0.1, 0.1),
            )
            x_acc += col_widths[j]

    # Additional note below table
    note_y = table_y_start + total_rows * row_height + 30
    page3.insert_text(
        pymupdf.Point(72, note_y),
        "Note: All figures are in USD. Revenue includes both product and service income.",
        fontsize=9,
        fontname="heit",
        color=(0.4, 0.4, 0.4),
    )

    # --- Page 4: Additional Notes ---
    page4 = doc.new_page(width=595, height=842)
    page4.insert_text(
        pymupdf.Point(72, 72),
        "Notes and Methodology",
        fontsize=18,
        fontname="hebo",
        color=(0.0, 0.15, 0.45),
    )
    shape4 = page4.new_shape()
    shape4.draw_line(pymupdf.Point(72, 80), pymupdf.Point(523, 80))
    shape4.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape4.commit()

    notes_text = (
        "1. Revenue Recognition: Revenue is recognized at the point of delivery for "
        "product sales and on a straight-line basis over the contract period for "
        "service agreements.\n\n"
        "2. Expense Classification: Operating expenses include salaries, benefits, "
        "rent, utilities, marketing, and depreciation. Capital expenditures are "
        "excluded from the quarterly expense figures.\n\n"
        "3. Profit Calculation: Profit is calculated as Revenue minus Expenses for "
        "each quarter. This represents operating profit before tax and interest.\n\n"
        "4. Data Sources: All financial data is sourced from the company's internal "
        "ERP system (SAP S/4HANA) and has been reviewed by the internal audit team.\n\n"
        "5. Rounding: Figures are rounded to the nearest thousand dollars. Minor "
        "discrepancies due to rounding may appear in totals."
    )
    rect4 = pymupdf.Rect(72, 100, 523, 700)
    page4.insert_textbox(
        rect4,
        notes_text,
        fontsize=11,
        fontname="helv",
        color=(0.1, 0.1, 0.1),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Launch PDF viewer
    launch_gui(f'evince --page-index=3 "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
