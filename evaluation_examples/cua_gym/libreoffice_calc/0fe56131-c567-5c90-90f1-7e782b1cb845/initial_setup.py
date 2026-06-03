"""
Initial Setup: Create unencrypted salary data PDF for password protection task
Task ID: pdf_fm_064
Domain: pdf (OS task using qpdf)
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_064'
DOC_DIR = f'{WORKDIR}/Documents/confidential'
OUTPUT = f'{DOC_DIR}/salary_data.pdf'


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
    # Ensure qpdf is installed (task states it should be available)
    subprocess.run(
        "echo 'password' | sudo -S apt-get install -y qpdf",
        shell=True, capture_output=True,
    )

    os.makedirs(DOC_DIR, exist_ok=True)

    doc = pymupdf.open()

    # ---- Page 1: Cover Page ----
    page = doc.new_page(width=612, height=792)
    page.insert_text(
        pymupdf.Point(72, 200),
        "CONFIDENTIAL",
        fontsize=36,
        fontname="hebo",
        color=(0.8, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(72, 260),
        "Employee Salary Data Report",
        fontsize=24,
        fontname="hebo",
        color=(0, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(72, 310),
        "Fiscal Year 2024-2025",
        fontsize=16,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(72, 350),
        "Prepared by: Human Resources Department",
        fontsize=12,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(72, 375),
        "Date: March 15, 2025",
        fontsize=12,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(72, 420),
        "Distribution: VP Finance, CFO, HR Director only",
        fontsize=11,
        fontname="heit",
        color=(0.5, 0, 0),
    )

    # ---- Page 2: Engineering Department ----
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(pymupdf.Point(72, 60), "Engineering Department - Salary Summary", fontsize=16, fontname="hebo", color=(0, 0, 0.5))

    # Draw table header
    y_start = 90
    headers = ["Employee Name", "Title", "Base Salary", "Bonus", "Total Comp"]
    col_x = [72, 190, 330, 420, 500]
    for i, h in enumerate(headers):
        page2.insert_text(pymupdf.Point(col_x[i], y_start), h, fontsize=9, fontname="hebo", color=(0, 0, 0))

    # Draw separator line
    shape = page2.new_shape()
    shape.draw_line(pymupdf.Point(72, y_start + 5), pymupdf.Point(560, y_start + 5))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()

    eng_data = [
        ["Sarah Chen", "Sr. Software Engineer", "$142,000", "$21,300", "$163,300"],
        ["Marcus Johnson", "Staff Engineer", "$168,500", "$33,700", "$202,200"],
        ["Priya Patel", "Engineering Manager", "$185,000", "$46,250", "$231,250"],
        ["David Kim", "Software Engineer II", "$118,000", "$11,800", "$129,800"],
        ["Emma Rodriguez", "DevOps Lead", "$155,000", "$23,250", "$178,250"],
        ["James O'Brien", "QA Engineer", "$105,000", "$10,500", "$115,500"],
        ["Lisa Wang", "Principal Engineer", "$195,000", "$48,750", "$243,750"],
        ["Carlos Mendez", "Jr. Developer", "$85,000", "$6,375", "$91,375"],
        ["Aisha Okafor", "Data Engineer", "$132,000", "$19,800", "$151,800"],
        ["Ryan Thompson", "Security Engineer", "$148,000", "$22,200", "$170,200"],
    ]

    y = y_start + 20
    for row in eng_data:
        for i, val in enumerate(row):
            page2.insert_text(pymupdf.Point(col_x[i], y), val, fontsize=8, fontname="helv", color=(0, 0, 0))
        y += 16

    page2.insert_text(pymupdf.Point(72, y + 20), "Department Total: $1,677,425", fontsize=10, fontname="hebo", color=(0, 0, 0))
    page2.insert_text(pymupdf.Point(72, y + 40), "Average Compensation: $167,742.50", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

    # ---- Page 3: Sales & Marketing ----
    page3 = doc.new_page(width=612, height=792)
    page3.insert_text(pymupdf.Point(72, 60), "Sales & Marketing - Salary Summary", fontsize=16, fontname="hebo", color=(0, 0, 0.5))

    y_start = 90
    for i, h in enumerate(headers):
        page3.insert_text(pymupdf.Point(col_x[i], y_start), h, fontsize=9, fontname="hebo", color=(0, 0, 0))

    shape3 = page3.new_shape()
    shape3.draw_line(pymupdf.Point(72, y_start + 5), pymupdf.Point(560, y_start + 5))
    shape3.finish(color=(0, 0, 0), width=0.5)
    shape3.commit()

    sales_data = [
        ["Jennifer Adams", "VP of Sales", "$210,000", "$63,000", "$273,000"],
        ["Michael Torres", "Account Executive", "$95,000", "$47,500", "$142,500"],
        ["Samantha Lee", "Marketing Director", "$165,000", "$33,000", "$198,000"],
        ["Robert Blake", "Sales Manager", "$125,000", "$37,500", "$162,500"],
        ["Hannah Fischer", "Content Strategist", "$88,000", "$8,800", "$96,800"],
        ["Kevin Nguyen", "SDR Team Lead", "$92,000", "$18,400", "$110,400"],
        ["Olivia Martin", "Brand Manager", "$110,000", "$16,500", "$126,500"],
        ["Daniel Wright", "Sales Engineer", "$135,000", "$27,000", "$162,000"],
    ]

    y = y_start + 20
    for row in sales_data:
        for i, val in enumerate(row):
            page3.insert_text(pymupdf.Point(col_x[i], y), val, fontsize=8, fontname="helv", color=(0, 0, 0))
        y += 16

    page3.insert_text(pymupdf.Point(72, y + 20), "Department Total: $1,271,700", fontsize=10, fontname="hebo", color=(0, 0, 0))
    page3.insert_text(pymupdf.Point(72, y + 40), "Average Compensation: $158,962.50", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

    # ---- Page 4: Operations & Finance ----
    page4 = doc.new_page(width=612, height=792)
    page4.insert_text(pymupdf.Point(72, 60), "Operations & Finance - Salary Summary", fontsize=16, fontname="hebo", color=(0, 0, 0.5))

    y_start = 90
    for i, h in enumerate(headers):
        page4.insert_text(pymupdf.Point(col_x[i], y_start), h, fontsize=9, fontname="hebo", color=(0, 0, 0))

    shape4 = page4.new_shape()
    shape4.draw_line(pymupdf.Point(72, y_start + 5), pymupdf.Point(560, y_start + 5))
    shape4.finish(color=(0, 0, 0), width=0.5)
    shape4.commit()

    ops_data = [
        ["Patricia Holmes", "CFO", "$245,000", "$73,500", "$318,500"],
        ["Andrew Sullivan", "Controller", "$155,000", "$23,250", "$178,250"],
        ["Maria Garcia", "Financial Analyst", "$98,000", "$9,800", "$107,800"],
        ["Thomas Baker", "Operations Manager", "$120,000", "$18,000", "$138,000"],
        ["Stephanie Price", "Procurement Lead", "$105,000", "$10,500", "$115,500"],
        ["Nathan Cooper", "Payroll Specialist", "$78,000", "$5,850", "$83,850"],
        ["Jessica Liu", "Budget Analyst", "$92,000", "$9,200", "$101,200"],
    ]

    y = y_start + 20
    for row in ops_data:
        for i, val in enumerate(row):
            page4.insert_text(pymupdf.Point(col_x[i], y), val, fontsize=8, fontname="helv", color=(0, 0, 0))
        y += 16

    page4.insert_text(pymupdf.Point(72, y + 20), "Department Total: $1,043,100", fontsize=10, fontname="hebo", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(72, y + 40), "Average Compensation: $149,014.29", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

    # ---- Page 5: Executive Summary & Benefits ----
    page5 = doc.new_page(width=612, height=792)
    page5.insert_text(pymupdf.Point(72, 60), "Executive Compensation Summary", fontsize=16, fontname="hebo", color=(0, 0, 0.5))

    rect = pymupdf.Rect(72, 85, 540, 250)
    page5.insert_textbox(
        rect,
        "This document contains highly sensitive compensation data for all employees across "
        "three departments: Engineering, Sales & Marketing, and Operations & Finance. "
        "Total annual compensation expenditure across all departments is $3,992,225. "
        "The average compensation per employee is $159,689.\n\n"
        "Key observations:\n"
        "- Engineering has the highest average compensation at $167,742.50\n"
        "- Sales & Marketing shows significant bonus variability (8-50% of base)\n"
        "- Operations & Finance maintains the most conservative bonus structure\n"
        "- Executive roles (CFO, VP Sales) account for 14.8% of total spend\n\n"
        "Recommendations for FY2025-2026:\n"
        "1. Adjust Engineering base salaries by 4-6% to remain competitive\n"
        "2. Restructure Sales commission tiers for better retention\n"
        "3. Implement equity compensation for senior Operations roles",
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
    )

    page5.insert_text(
        pymupdf.Point(72, 300),
        "NOTICE: Unauthorized distribution of this document is grounds for termination.",
        fontsize=10,
        fontname="hebo",
        color=(0.8, 0, 0),
    )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
