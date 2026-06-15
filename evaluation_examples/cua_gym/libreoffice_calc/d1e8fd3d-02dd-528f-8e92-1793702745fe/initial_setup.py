"""
Initial Setup: Create a PDF containing a spreadsheet table for CSV extraction task
Task ID: pdf_gf1_045
Domain: pdf / libreoffice_calc
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_045'
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

    # Define realistic spreadsheet data: 20 rows of purchase/expense records
    headers = ['Date', 'Item', 'Quantity', 'Unit Price', 'Total']

    data = [
        ['2025-01-03', 'Wireless Mouse',          '12', '24.99',  '299.88'],
        ['2025-01-07', 'USB-C Hub',               '5',  '39.50',  '197.50'],
        ['2025-01-12', 'Mechanical Keyboard',      '8',  '74.95',  '599.60'],
        ['2025-01-18', 'Monitor Stand',            '15', '32.00',  '480.00'],
        ['2025-01-25', 'Webcam HD 1080p',          '10', '49.99',  '499.90'],
        ['2025-02-02', 'Laptop Sleeve 15in',       '20', '18.75',  '375.00'],
        ['2025-02-08', 'HDMI Cable 6ft',           '30', '8.99',   '269.70'],
        ['2025-02-14', 'Desk Lamp LED',            '7',  '42.50',  '297.50'],
        ['2025-02-21', 'Noise Cancelling Headset', '4',  '129.00', '516.00'],
        ['2025-02-28', 'Ergonomic Chair Pad',      '6',  '55.00',  '330.00'],
        ['2025-03-05', 'Portable SSD 1TB',         '3',  '89.99',  '269.97'],
        ['2025-03-11', 'Surge Protector Strip',    '25', '15.49',  '387.25'],
        ['2025-03-17', 'Whiteboard Markers Set',   '40', '6.25',   '250.00'],
        ['2025-03-22', 'Cable Management Kit',     '18', '12.99',  '233.82'],
        ['2025-03-29', 'Bluetooth Speaker',        '9',  '34.75',  '312.75'],
        ['2025-04-03', 'Wireless Charger Pad',     '14', '19.99',  '279.86'],
        ['2025-04-10', 'Screen Privacy Filter',    '11', '28.50',  '313.50'],
        ['2025-04-16', 'USB Flash Drive 64GB',     '50', '7.99',   '399.50'],
        ['2025-04-23', 'Document Scanner',         '2',  '199.00', '398.00'],
        ['2025-04-30', 'Ethernet Patch Cable',     '35', '4.50',   '157.50'],
    ]

    # Build PDF with a nicely formatted table using PyMuPDF
    import pymupdf

    doc = pymupdf.open()
    page = doc.new_page(width=612, height=792)  # Letter size

    # Title
    page.insert_text(
        pymupdf.Point(72, 50),
        "Office Supplies Procurement Log",
        fontsize=18,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    # Subtitle
    page.insert_text(
        pymupdf.Point(72, 72),
        "January - April 2025",
        fontsize=11,
        fontname="heit",
        color=(0.3, 0.3, 0.3),
    )

    # Table parameters
    start_x = 55
    start_y = 100
    col_widths = [90, 170, 65, 75, 75]  # 5 columns
    row_height = 22
    header_height = 26

    # Draw header row background
    header_rect = pymupdf.Rect(
        start_x, start_y,
        start_x + sum(col_widths), start_y + header_height
    )
    shape = page.new_shape()
    shape.draw_rect(header_rect)
    shape.finish(color=(0.2, 0.2, 0.5), fill=(0.2, 0.2, 0.5), width=0.5)
    shape.commit()

    # Draw header text
    x = start_x
    for i, h in enumerate(headers):
        page.insert_text(
            pymupdf.Point(x + 5, start_y + 17),
            h,
            fontsize=10,
            fontname="hebo",
            color=(1, 1, 1),
        )
        x += col_widths[i]

    # Draw data rows
    y = start_y + header_height
    for row_idx, row in enumerate(data):
        # Alternating row background
        if row_idx % 2 == 0:
            row_rect = pymupdf.Rect(start_x, y, start_x + sum(col_widths), y + row_height)
            shape2 = page.new_shape()
            shape2.draw_rect(row_rect)
            shape2.finish(color=None, fill=(0.93, 0.93, 0.97), width=0)
            shape2.commit()

        x = start_x
        for i, val in enumerate(row):
            page.insert_text(
                pymupdf.Point(x + 5, y + 15),
                str(val),
                fontsize=9,
                fontname="helv",
                color=(0.1, 0.1, 0.1),
            )
            x += col_widths[i]
        y += row_height

    # Draw outer table border
    table_rect = pymupdf.Rect(
        start_x, start_y,
        start_x + sum(col_widths), start_y + header_height + len(data) * row_height
    )
    shape3 = page.new_shape()
    shape3.draw_rect(table_rect)
    shape3.finish(color=(0.3, 0.3, 0.3), fill=None, width=0.8)

    # Draw column lines
    x = start_x
    for i in range(len(col_widths) - 1):
        x += col_widths[i]
        shape3.draw_line(
            pymupdf.Point(x, start_y),
            pymupdf.Point(x, start_y + header_height + len(data) * row_height)
        )
        shape3.finish(color=(0.6, 0.6, 0.6), width=0.3)

    # Draw row lines
    y_line = start_y + header_height
    for _ in range(len(data)):
        shape3.draw_line(
            pymupdf.Point(start_x, y_line),
            pymupdf.Point(start_x + sum(col_widths), y_line)
        )
        shape3.finish(color=(0.7, 0.7, 0.7), width=0.2)
        y_line += row_height

    shape3.commit()

    # Footer
    page.insert_text(
        pymupdf.Point(72, 770),
        "Generated from LibreOffice Calc - Procurement Department",
        fontsize=8,
        fontname="heit",
        color=(0.5, 0.5, 0.5),
    )

    doc.set_metadata({
        "title": "Office Supplies Procurement Log",
        "author": "Procurement Department",
        "subject": "Spreadsheet Export",
        "creator": "LibreOffice Calc",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open PDF in Evince for the agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
