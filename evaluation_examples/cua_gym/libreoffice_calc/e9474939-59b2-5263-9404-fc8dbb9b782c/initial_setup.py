"""
Initial Setup: Create a 5-page PDF with tabular employee data
Task ID: pdf_mbc_078
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_078'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/spreadsheet_data.pdf'

# ---------- realistic employee data (100 rows) ----------

HEADERS = ['ID', 'Name', 'Department', 'Salary', 'Start Date']

NAMES = [
    "Sarah Chen", "Marcus Johnson", "Elena Rodriguez", "David Kim",
    "Priya Patel", "James O'Brien", "Fatima Al-Hassan", "Thomas Mueller",
    "Yuki Tanaka", "Olivia Foster", "Carlos Mendez", "Amara Okafor",
    "Liam Fitzgerald", "Nina Petrova", "Raj Sharma", "Emily Watson",
    "Hassan Youssef", "Maria Gonzalez", "Andre Williams", "Sophie Laurent",
    "Wei Zhang", "Grace Adeyemi", "Michael Torres", "Anna Kowalski",
    "Kwame Mensah", "Isabella Rossi", "Derek Chang", "Lucia Fernandez",
    "Benjamin Park", "Nadia Ivanova", "Robert Singh", "Chloe Moreau",
    "Samuel Osei", "Diana Popescu", "Kevin Li", "Aisha Mohammed",
    "Patrick Sullivan", "Mika Hoshino", "Ricardo Silva", "Freya Larsen",
    "George Papadopoulos", "Zara Hussain", "Vincent Dubois", "Ingrid Svensson",
    "Tomasz Novak", "Julia Santos", "Arthur Campbell", "Leila Khoury",
    "Oscar Rivera", "Hannah Schmidt", "Felix Andersson", "Carmen Reyes",
    "Ivan Petrov", "Melanie Fischer", "Javier Castillo", "Sonia Gupta",
    "Nathan Brooks", "Elise Fontaine", "Ryan O'Connor", "Aaliya Rahman",
    "Peter Hoffmann", "Laura Bianchi", "Simon De Vries", "Vanessa Cruz",
    "Christian Bauer", "Esther Nakamura", "Darius Jackson", "Monika Szabo",
    "Alexandre Martin", "Tanya Volkov", "Brendan Kelly", "Cecilia Morales",
    "Lucas Weber", "Hanna Johansson", "Omar Farooq", "Rebecca Stone",
    "Stefan Gruber", "Valentina Marchetti", "Ian McKenzie", "Noor Abbas",
    "Gabriel Costa", "Katarina Lindqvist", "Zachary Turner", "Lina Al-Rashid",
    "Hugo Berger", "Mei-Lin Wu", "Adrian Stanescu", "Fiona Gallagher",
    "Nikolai Volkov", "Simone Beaumont", "Ethan Reed", "Dina El-Sayed",
    "Maxwell Hart", "Chiara Colombo", "Brandon Lee", "Anya Kuznetsova",
    "Jerome Baptiste", "Heidi Zimmermann", "Rohan Kapoor", "Astrid Nielsen",
]

DEPARTMENTS = [
    "Engineering", "Marketing", "Sales", "Finance", "Human Resources",
    "Operations", "Product", "Design", "Legal", "Customer Support",
    "Research", "IT", "Business Development", "Quality Assurance",
]

SALARIES = [
    62000, 71500, 58000, 95000, 67000, 83000, 74500, 91000, 56000, 78000,
    69500, 88000, 54000, 76000, 103000, 64000, 72000, 85500, 61000, 97000,
    55000, 79500, 68000, 92000, 63000, 81000, 70000, 87500, 59000, 94000,
    66000, 73500, 57000, 89000, 77000, 82000, 60000, 96000, 71000, 65000,
    84000, 58500, 93000, 75000, 86500, 62500, 99000, 68500, 74000, 80000,
    67500, 91500, 55500, 78500, 104000, 63500, 72500, 86000, 60500, 98000,
    56500, 80500, 69000, 93500, 64500, 82500, 71500, 88500, 59500, 95500,
    66500, 74500, 57500, 90000, 77500, 83500, 61500, 97500, 70500, 65500,
    85000, 58000, 94500, 76500, 87000, 63000, 100000, 69000, 75500, 81500,
    68000, 92500, 56000, 79000, 105000, 64000, 73000, 87000, 62000, 99500,
]

START_DATES = [
    "2019-03-15", "2020-07-01", "2018-11-20", "2021-01-10", "2019-05-22",
    "2022-02-14", "2020-09-03", "2018-06-30", "2023-04-17", "2019-08-12",
    "2021-06-25", "2020-01-08", "2022-11-05", "2019-12-01", "2018-03-28",
    "2023-07-14", "2020-04-22", "2021-09-18", "2019-02-07", "2022-05-30",
    "2018-08-15", "2023-01-20", "2020-10-11", "2019-06-03", "2021-03-27",
    "2022-08-19", "2018-12-10", "2020-05-15", "2023-09-01", "2019-11-22",
    "2021-07-08", "2020-02-28", "2022-04-14", "2018-10-05", "2019-04-30",
    "2023-06-12", "2021-01-25", "2020-08-07", "2022-12-18", "2019-09-14",
    "2018-05-20", "2023-02-10", "2021-10-30", "2020-06-05", "2019-01-18",
    "2022-07-22", "2018-09-08", "2023-11-15", "2020-03-12", "2021-05-03",
    "2019-07-28", "2022-01-16", "2018-04-10", "2023-08-25", "2020-11-20",
    "2021-02-14", "2019-10-06", "2022-06-30", "2018-07-18", "2023-03-05",
    "2020-12-22", "2021-08-11", "2019-03-01", "2022-10-15", "2018-01-28",
    "2023-05-20", "2020-07-14", "2021-11-08", "2019-06-22", "2022-03-17",
    "2018-11-02", "2023-10-10", "2020-01-30", "2021-04-25", "2019-08-18",
    "2022-09-05", "2018-02-20", "2023-12-01", "2020-09-15", "2021-06-10",
    "2019-12-28", "2022-02-08", "2018-06-14", "2023-07-22", "2020-04-05",
    "2021-09-30", "2019-05-12", "2022-11-25", "2018-08-08", "2023-04-18",
    "2020-10-28", "2021-01-15", "2019-07-03", "2022-05-20", "2018-10-30",
    "2023-06-08", "2020-03-25", "2021-12-12", "2019-02-18", "2022-08-02",
]

def build_rows():
    """Build 100 rows of employee data."""
    rows = []
    dept_idx = 0
    for i in range(100):
        row = [
            i + 1,                          # ID
            NAMES[i],                       # Name
            DEPARTMENTS[dept_idx % len(DEPARTMENTS)],  # Department
            SALARIES[i],                    # Salary
            START_DATES[i],                 # Start Date
        ]
        rows.append(row)
        dept_idx += 1
    return rows


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

    rows = build_rows()

    # Create the PDF with tabular data across 5 pages
    doc = pymupdf.open()

    # Page dimensions
    PAGE_W, PAGE_H = 595, 842  # A4
    LEFT_MARGIN = 50
    TOP_MARGIN = 60
    ROW_HEIGHT = 18
    COL_WIDTHS = [40, 160, 120, 70, 90]  # ID, Name, Department, Salary, Start Date
    FONT_SIZE = 10
    HEADER_FONT_SIZE = 11

    # Page 1: Headers + rows 1-20
    page = doc.new_page(width=PAGE_W, height=PAGE_H)

    # Title
    page.insert_text(
        pymupdf.Point(PAGE_W / 2 - 80, 35),
        "Employee Directory",
        fontsize=16,
        fontname="hebo",
        color=(0, 0, 0.5),
    )

    y = TOP_MARGIN

    # Draw header row
    x = LEFT_MARGIN
    for col_idx, header in enumerate(HEADERS):
        page.insert_text(
            pymupdf.Point(x + 2, y + 13),
            header,
            fontsize=HEADER_FONT_SIZE,
            fontname="hebo",
            color=(1, 1, 1),
        )
        x += COL_WIDTHS[col_idx]

    # Header background
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(LEFT_MARGIN, y, LEFT_MARGIN + sum(COL_WIDTHS), y + ROW_HEIGHT))
    shape.finish(color=(0, 0, 0.4), fill=(0.15, 0.27, 0.53), width=0.5)
    shape.commit()

    # Re-draw header text on top
    x = LEFT_MARGIN
    for col_idx, header in enumerate(HEADERS):
        page.insert_text(
            pymupdf.Point(x + 2, y + 13),
            header,
            fontsize=HEADER_FONT_SIZE,
            fontname="hebo",
            color=(1, 1, 1),
        )
        x += COL_WIDTHS[col_idx]

    y += ROW_HEIGHT

    # Data rows 1-20
    for row_idx in range(20):
        row = rows[row_idx]
        x = LEFT_MARGIN

        # Alternating row background
        if row_idx % 2 == 1:
            shape = page.new_shape()
            shape.draw_rect(pymupdf.Rect(LEFT_MARGIN, y, LEFT_MARGIN + sum(COL_WIDTHS), y + ROW_HEIGHT))
            shape.finish(fill=(0.93, 0.93, 0.97), width=0)
            shape.commit()

        for col_idx, val in enumerate(row):
            text = str(val)
            page.insert_text(
                pymupdf.Point(x + 2, y + 13),
                text,
                fontsize=FONT_SIZE,
                fontname="helv",
                color=(0, 0, 0),
            )
            x += COL_WIDTHS[col_idx]
        y += ROW_HEIGHT

    # Draw table border
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(LEFT_MARGIN, TOP_MARGIN, LEFT_MARGIN + sum(COL_WIDTHS), y))
    shape.finish(color=(0.4, 0.4, 0.4), width=0.5)
    shape.commit()

    # Footer
    page.insert_text(
        pymupdf.Point(PAGE_W / 2 - 20, PAGE_H - 30),
        "Page 1 of 5",
        fontsize=9,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    # Pages 2-5: 20 rows each
    for page_num in range(2, 6):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        start_row = (page_num - 1) * 20
        end_row = page_num * 20

        # Continuation header
        page.insert_text(
            pymupdf.Point(PAGE_W / 2 - 100, 35),
            "Employee Directory (continued)",
            fontsize=14,
            fontname="hebo",
            color=(0, 0, 0.5),
        )

        y = TOP_MARGIN

        # Column headers on each page for readability
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(LEFT_MARGIN, y, LEFT_MARGIN + sum(COL_WIDTHS), y + ROW_HEIGHT))
        shape.finish(color=(0, 0, 0.4), fill=(0.15, 0.27, 0.53), width=0.5)
        shape.commit()

        x = LEFT_MARGIN
        for col_idx, header in enumerate(HEADERS):
            page.insert_text(
                pymupdf.Point(x + 2, y + 13),
                header,
                fontsize=HEADER_FONT_SIZE,
                fontname="hebo",
                color=(1, 1, 1),
            )
            x += COL_WIDTHS[col_idx]
        y += ROW_HEIGHT

        # Data rows
        for row_idx in range(start_row, end_row):
            row = rows[row_idx]
            x = LEFT_MARGIN

            if (row_idx - start_row) % 2 == 1:
                shape = page.new_shape()
                shape.draw_rect(pymupdf.Rect(LEFT_MARGIN, y, LEFT_MARGIN + sum(COL_WIDTHS), y + ROW_HEIGHT))
                shape.finish(fill=(0.93, 0.93, 0.97), width=0)
                shape.commit()

            for col_idx, val in enumerate(row):
                text = str(val)
                page.insert_text(
                    pymupdf.Point(x + 2, y + 13),
                    text,
                    fontsize=FONT_SIZE,
                    fontname="helv",
                    color=(0, 0, 0),
                )
                x += COL_WIDTHS[col_idx]
            y += ROW_HEIGHT

        # Table border
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(LEFT_MARGIN, TOP_MARGIN, LEFT_MARGIN + sum(COL_WIDTHS), y))
        shape.finish(color=(0.4, 0.4, 0.4), width=0.5)
        shape.commit()

        # Footer
        page.insert_text(
            pymupdf.Point(PAGE_W / 2 - 20, PAGE_H - 30),
            f"Page {page_num} of 5",
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open PDF in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
