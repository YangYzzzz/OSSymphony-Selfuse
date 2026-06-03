"""
Initial Setup: Create a PDF with sensitive metadata for metadata stripping task
Task ID: pdf_gf2_015
Domain: pdf
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
TASK_ID = 'pdf_gf2_015'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/sensitive_doc.pdf'


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

    doc = pymupdf.open()

    # --- Page 1: Cover Page ---
    page1 = doc.new_page(width=612, height=792)  # Letter size
    page1.insert_text(
        pymupdf.Point(180, 200),
        "Q3 Compensation Analysis",
        fontsize=24,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )
    page1.insert_text(
        pymupdf.Point(200, 260),
        "Confidential - HR Use Only",
        fontsize=14,
        fontname="tiit",
        color=(0.6, 0.0, 0.0),
    )
    page1.insert_text(
        pymupdf.Point(220, 320),
        "Prepared by: Jane Smith",
        fontsize=12,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
    )
    page1.insert_text(
        pymupdf.Point(215, 345),
        "Director of Human Resources",
        fontsize=11,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page1.insert_text(
        pymupdf.Point(240, 390),
        "Date: September 30, 2025",
        fontsize=11,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

    # Horizontal rule
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(72, 420), pymupdf.Point(540, 420))
    shape.finish(color=(0.5, 0.5, 0.5), width=1)
    shape.commit()

    page1.insert_text(
        pymupdf.Point(72, 480),
        "This document contains compensation data for all departments.",
        fontsize=11,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
    )
    page1.insert_text(
        pymupdf.Point(72, 500),
        "Distribution is restricted to authorized HR personnel only.",
        fontsize=11,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
    )

    # --- Page 2: Engineering Department ---
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(
        pymupdf.Point(72, 60),
        "Engineering Department - Compensation Summary",
        fontsize=16,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    # Table header
    y = 100
    headers = ["Employee", "Title", "Base Salary", "Bonus", "Total"]
    x_positions = [72, 180, 310, 410, 500]
    for i, h in enumerate(headers):
        page2.insert_text(pymupdf.Point(x_positions[i], y), h, fontsize=10, fontname="hebo", color=(0, 0, 0))

    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, y + 5), pymupdf.Point(560, y + 5))
    shape2.finish(color=(0, 0, 0), width=0.5)
    shape2.commit()

    eng_data = [
        ["Sarah Chen", "Sr. Engineer", "$142,000", "$21,300", "$163,300"],
        ["Marcus Johnson", "Staff Engineer", "$168,500", "$33,700", "$202,200"],
        ["Priya Patel", "Engineering Mgr", "$175,000", "$35,000", "$210,000"],
        ["David Kim", "Jr. Engineer", "$95,000", "$9,500", "$104,500"],
        ["Emily Torres", "Sr. Engineer", "$138,000", "$20,700", "$158,700"],
        ["Ryan O'Brien", "Principal Eng.", "$195,000", "$48,750", "$243,750"],
        ["Lisa Wang", "Engineer II", "$118,000", "$14,160", "$132,160"],
        ["James Anderson", "Engineer III", "$130,000", "$16,900", "$146,900"],
    ]

    for row_idx, row in enumerate(eng_data):
        ry = y + 20 + row_idx * 18
        for col_idx, val in enumerate(row):
            page2.insert_text(
                pymupdf.Point(x_positions[col_idx], ry),
                val, fontsize=9, fontname="helv", color=(0.1, 0.1, 0.1),
            )

    page2.insert_text(
        pymupdf.Point(72, y + 20 + len(eng_data) * 18 + 25),
        "Department Average Total Compensation: $170,189",
        fontsize=10,
        fontname="hebo",
        color=(0.2, 0.2, 0.2),
    )

    # --- Page 3: Marketing & Sales ---
    page3 = doc.new_page(width=612, height=792)
    page3.insert_text(
        pymupdf.Point(72, 60),
        "Marketing & Sales - Compensation Summary",
        fontsize=16,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    y3 = 100
    for i, h in enumerate(headers):
        page3.insert_text(pymupdf.Point(x_positions[i], y3), h, fontsize=10, fontname="hebo", color=(0, 0, 0))

    shape3 = page3.new_shape()
    shape3.draw_line(pymupdf.Point(72, y3 + 5), pymupdf.Point(560, y3 + 5))
    shape3.finish(color=(0, 0, 0), width=0.5)
    shape3.commit()

    mktg_data = [
        ["Alex Rivera", "VP Marketing", "$185,000", "$46,250", "$231,250"],
        ["Nicole Foster", "Content Mgr", "$92,000", "$9,200", "$101,200"],
        ["Tom Bradley", "Sales Director", "$155,000", "$62,000", "$217,000"],
        ["Mia Zhang", "Digital Mktg Spec", "$78,000", "$7,800", "$85,800"],
        ["Chris Nakamura", "Account Exec", "$85,000", "$34,000", "$119,000"],
        ["Sofia Hernandez", "Brand Manager", "$105,000", "$15,750", "$120,750"],
    ]

    for row_idx, row in enumerate(mktg_data):
        ry = y3 + 20 + row_idx * 18
        for col_idx, val in enumerate(row):
            page3.insert_text(
                pymupdf.Point(x_positions[col_idx], ry),
                val, fontsize=9, fontname="helv", color=(0.1, 0.1, 0.1),
            )

    page3.insert_text(
        pymupdf.Point(72, y3 + 20 + len(mktg_data) * 18 + 25),
        "Department Average Total Compensation: $145,833",
        fontsize=10,
        fontname="hebo",
        color=(0.2, 0.2, 0.2),
    )

    # --- Page 4: Summary and Recommendations ---
    page4 = doc.new_page(width=612, height=792)
    page4.insert_text(
        pymupdf.Point(72, 60),
        "Executive Summary & Recommendations",
        fontsize=16,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    summary_text = (
        "Based on the Q3 2025 compensation review, several key findings have emerged. "
        "The Engineering department has maintained competitive salary levels with an average "
        "total compensation of $170,189, which aligns with the 75th percentile of industry benchmarks. "
        "Marketing and Sales compensation averages $145,833, slightly below the 60th percentile target."
    )
    rect = pymupdf.Rect(72, 90, 540, 220)
    page4.insert_textbox(rect, summary_text, fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))

    page4.insert_text(
        pymupdf.Point(72, 240),
        "Recommendations:",
        fontsize=13,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    recommendations = [
        "1. Adjust Marketing & Sales base salaries by 5-8% to reach 65th percentile.",
        "2. Implement retention bonuses for Senior and Principal Engineers.",
        "3. Review commission structures for Account Executives in Q4.",
        "4. Conduct external benchmarking study for Engineering Manager roles.",
        "5. Propose equity refresh grants for top performers in all departments.",
    ]

    for i, rec in enumerate(recommendations):
        page4.insert_text(
            pymupdf.Point(90, 270 + i * 22),
            rec, fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2),
        )

    page4.insert_text(
        pymupdf.Point(72, 400),
        "Prepared by the Human Resources Department - Q3 FY2025",
        fontsize=9,
        fontname="tiit",
        color=(0.4, 0.4, 0.4),
    )

    # Set metadata with identifying information
    doc.set_metadata({
        "title": "Q3 Compensation Analysis",
        "author": "HR Director Jane Smith",
        "subject": "Employee Salaries",
        "keywords": "salaries, compensation, HR",
        "creator": "Microsoft Word 2021",
        "producer": "Acme Corp HR Suite v3.2",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
