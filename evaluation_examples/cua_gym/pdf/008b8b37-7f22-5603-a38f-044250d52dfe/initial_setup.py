"""
Initial Setup: Create 6 sensitive financial PDF files for batch encryption task
Task ID: pdf_fin_086
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_086'
SENSITIVE_DIR = f'{WORKDIR}/finance/sensitive'
PROTECTED_DIR = f'{SENSITIVE_DIR}/protected'


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
    import pymupdf

    # Create directory structure
    os.makedirs(SENSITIVE_DIR, exist_ok=True)
    os.makedirs(PROTECTED_DIR, exist_ok=True)

    # --- 1. payroll.pdf ---
    doc = pymupdf.open()
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "CONFIDENTIAL — Employee Payroll Report", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(72, 85), "Meridian Technology Solutions — Q1 2024", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 95), pymupdf.Point(540, 95))
    shape.finish(color=(0.1, 0.1, 0.4), width=1.5)
    shape.commit()

    headers = ["Employee ID", "Name", "Department", "Base Salary", "Bonus", "Net Pay"]
    col_x = [72, 140, 250, 360, 440, 510]
    y = 120
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(col_x[i], y), h, fontsize=9, fontname="hebo", color=(0, 0, 0))

    employees = [
        ("EMP-1001", "Sarah Chen", "Engineering", "$112,500", "$15,000", "$127,500"),
        ("EMP-1002", "Marcus Johnson", "Marketing", "$89,200", "$8,500", "$97,700"),
        ("EMP-1003", "Priya Patel", "Finance", "$95,800", "$12,000", "$107,800"),
        ("EMP-1004", "James O'Brien", "Engineering", "$105,000", "$14,200", "$119,200"),
        ("EMP-1005", "Ana Rodriguez", "Sales", "$78,500", "$22,300", "$100,800"),
        ("EMP-1006", "David Kim", "Operations", "$82,000", "$7,800", "$89,800"),
        ("EMP-1007", "Rachel Foster", "HR", "$91,400", "$9,100", "$100,500"),
        ("EMP-1008", "Thomas Wright", "Engineering", "$118,000", "$16,500", "$134,500"),
        ("EMP-1009", "Lisa Nakamura", "Product", "$103,200", "$13,800", "$117,000"),
        ("EMP-1010", "Robert Okafor", "Finance", "$97,600", "$11,500", "$109,100"),
        ("EMP-1011", "Emily Sanders", "Marketing", "$84,300", "$9,600", "$93,900"),
        ("EMP-1012", "Kevin Zhang", "Engineering", "$110,800", "$15,200", "$126,000"),
    ]
    y = 140
    for emp in employees:
        for i, val in enumerate(emp):
            page.insert_text(pymupdf.Point(col_x[i], y), val, fontsize=8, fontname="helv", color=(0, 0, 0))
        y += 16

    page.insert_text(pymupdf.Point(72, y + 20), "Total Payroll: $1,323,800", fontsize=11, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(72, y + 40), "Report generated: March 31, 2024 | Classification: CONFIDENTIAL", fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))
    doc.save(f'{SENSITIVE_DIR}/payroll.pdf')
    doc.close()
    print("Created payroll.pdf")

    # --- 2. tax_ids.pdf ---
    doc = pymupdf.open()
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "Employee Tax Identification Records", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(72, 85), "For Internal Payroll Processing Only", fontsize=11, fontname="heit", color=(0.6, 0.2, 0.2))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 95), pymupdf.Point(540, 95))
    shape.finish(color=(0.1, 0.1, 0.4), width=1.5)
    shape.commit()

    tax_headers = ["Employee", "Federal TIN", "State Tax ID", "Filing Status", "W-4 Date"]
    tx = [72, 180, 290, 380, 480]
    y = 120
    for i, h in enumerate(tax_headers):
        page.insert_text(pymupdf.Point(tx[i], y), h, fontsize=9, fontname="hebo")

    tax_data = [
        ("Sarah Chen", "***-**-4521", "CA-8834521", "Single", "01/10/2024"),
        ("Marcus Johnson", "***-**-7832", "CA-7127832", "Married-Joint", "01/15/2024"),
        ("Priya Patel", "***-**-6190", "CA-9016190", "Single", "02/01/2024"),
        ("James O'Brien", "***-**-3847", "CA-6553847", "Head of HH", "01/08/2024"),
        ("Ana Rodriguez", "***-**-2956", "CA-4422956", "Married-Joint", "01/22/2024"),
        ("David Kim", "***-**-8104", "CA-3318104", "Single", "01/12/2024"),
        ("Rachel Foster", "***-**-5673", "CA-7785673", "Married-Sep", "02/05/2024"),
        ("Thomas Wright", "***-**-1248", "CA-5561248", "Single", "01/18/2024"),
        ("Lisa Nakamura", "***-**-9035", "CA-2249035", "Married-Joint", "01/30/2024"),
        ("Robert Okafor", "***-**-4762", "CA-8894762", "Single", "02/10/2024"),
    ]
    y = 140
    for row in tax_data:
        for i, val in enumerate(row):
            page.insert_text(pymupdf.Point(tx[i], y), val, fontsize=8, fontname="helv")
        y += 16

    page.insert_text(pymupdf.Point(72, y + 25), "WARNING: This document contains Personally Identifiable Information (PII).", fontsize=9, fontname="hebo", color=(0.7, 0, 0))
    page.insert_text(pymupdf.Point(72, y + 40), "Unauthorized disclosure may result in civil and criminal penalties under IRC Section 7431.", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
    doc.save(f'{SENSITIVE_DIR}/tax_ids.pdf')
    doc.close()
    print("Created tax_ids.pdf")

    # --- 3. bank_details.pdf ---
    doc = pymupdf.open()
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "Direct Deposit — Banking Information", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(72, 85), "Meridian Technology Solutions — Updated March 2024", fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 95), pymupdf.Point(540, 95))
    shape.finish(color=(0.1, 0.1, 0.4), width=1.5)
    shape.commit()

    bk_headers = ["Employee", "Bank Name", "Routing #", "Account #", "Type"]
    bx = [72, 175, 300, 395, 510]
    y = 120
    for i, h in enumerate(bk_headers):
        page.insert_text(pymupdf.Point(bx[i], y), h, fontsize=9, fontname="hebo")

    bank_data = [
        ("Sarah Chen", "Chase Bank", "021000021", "****8834", "Checking"),
        ("Marcus Johnson", "Bank of America", "026009593", "****2917", "Checking"),
        ("Priya Patel", "Wells Fargo", "121000248", "****6450", "Savings"),
        ("James O'Brien", "Citibank", "021000089", "****1273", "Checking"),
        ("Ana Rodriguez", "US Bank", "091000019", "****5098", "Checking"),
        ("David Kim", "PNC Bank", "043000096", "****7741", "Checking"),
        ("Rachel Foster", "Capital One", "051405515", "****3826", "Savings"),
        ("Thomas Wright", "TD Bank", "031101266", "****9154", "Checking"),
        ("Lisa Nakamura", "Chase Bank", "021000021", "****4602", "Checking"),
        ("Robert Okafor", "Ally Bank", "124003116", "****8367", "Savings"),
    ]
    y = 140
    for row in bank_data:
        for i, val in enumerate(row):
            page.insert_text(pymupdf.Point(bx[i], y), val, fontsize=8, fontname="helv")
        y += 16

    page.insert_text(pymupdf.Point(72, y + 25), "RESTRICTED — Do not distribute. For HR & Payroll department use only.", fontsize=9, fontname="hebo", color=(0.7, 0, 0))
    doc.save(f'{SENSITIVE_DIR}/bank_details.pdf')
    doc.close()
    print("Created bank_details.pdf")

    # --- 4. ssn_list.pdf ---
    doc = pymupdf.open()
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "Social Security Number Registry", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(72, 85), "Strictly Confidential — Authorized Personnel Only", fontsize=11, fontname="heit", color=(0.7, 0, 0))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 95), pymupdf.Point(540, 95))
    shape.finish(color=(0.1, 0.1, 0.4), width=1.5)
    shape.commit()

    ssn_headers = ["Employee ID", "Full Name", "Date of Birth", "SSN (Masked)", "Hire Date"]
    sx = [72, 150, 270, 370, 480]
    y = 120
    for i, h in enumerate(ssn_headers):
        page.insert_text(pymupdf.Point(sx[i], y), h, fontsize=9, fontname="hebo")

    ssn_data = [
        ("EMP-1001", "Sarah Chen", "08/14/1990", "XXX-XX-4521", "01/15/2023"),
        ("EMP-1002", "Marcus Johnson", "03/22/1988", "XXX-XX-7832", "06/01/2022"),
        ("EMP-1003", "Priya Patel", "11/05/1992", "XXX-XX-6190", "09/15/2023"),
        ("EMP-1004", "James O'Brien", "07/30/1985", "XXX-XX-3847", "03/01/2021"),
        ("EMP-1005", "Ana Rodriguez", "01/17/1991", "XXX-XX-2956", "11/01/2022"),
        ("EMP-1006", "David Kim", "05/09/1993", "XXX-XX-8104", "07/15/2023"),
        ("EMP-1007", "Rachel Foster", "12/28/1987", "XXX-XX-5673", "04/01/2022"),
        ("EMP-1008", "Thomas Wright", "06/11/1989", "XXX-XX-1248", "08/01/2021"),
        ("EMP-1009", "Lisa Nakamura", "09/03/1994", "XXX-XX-9035", "02/01/2024"),
        ("EMP-1010", "Robert Okafor", "04/19/1986", "XXX-XX-4762", "10/15/2022"),
    ]
    y = 140
    for row in ssn_data:
        for i, val in enumerate(row):
            page.insert_text(pymupdf.Point(sx[i], y), val, fontsize=8, fontname="helv")
        y += 16

    page.insert_text(pymupdf.Point(72, y + 25), "This document is subject to HIPAA and state privacy regulations.", fontsize=9, fontname="hebo", color=(0.7, 0, 0))
    page.insert_text(pymupdf.Point(72, y + 40), "Unauthorized access or disclosure is a federal offense.", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
    doc.save(f'{SENSITIVE_DIR}/ssn_list.pdf')
    doc.close()
    print("Created ssn_list.pdf")

    # --- 5. salary_schedule.pdf ---
    doc = pymupdf.open()
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "2024 Salary Schedule & Pay Bands", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(72, 85), "Meridian Technology Solutions — Human Resources", fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 95), pymupdf.Point(540, 95))
    shape.finish(color=(0.1, 0.1, 0.4), width=1.5)
    shape.commit()

    sal_headers = ["Grade", "Title Range", "Min Salary", "Mid Salary", "Max Salary"]
    slx = [72, 130, 310, 390, 480]
    y = 120
    for i, h in enumerate(sal_headers):
        page.insert_text(pymupdf.Point(slx[i], y), h, fontsize=9, fontname="hebo")

    salary_data = [
        ("L1", "Associate / Junior", "$55,000", "$67,500", "$80,000"),
        ("L2", "Specialist / Analyst", "$70,000", "$85,000", "$100,000"),
        ("L3", "Senior / Lead", "$90,000", "$110,000", "$130,000"),
        ("L4", "Manager / Sr. Lead", "$110,000", "$135,000", "$160,000"),
        ("L5", "Director", "$140,000", "$170,000", "$200,000"),
        ("L6", "VP / Sr. Director", "$175,000", "$215,000", "$255,000"),
        ("L7", "SVP / C-Suite", "$220,000", "$280,000", "$340,000"),
    ]
    y = 140
    for row in salary_data:
        for i, val in enumerate(row):
            page.insert_text(pymupdf.Point(slx[i], y), val, fontsize=8, fontname="helv")
        y += 16

    page.insert_text(pymupdf.Point(72, y + 25), "Effective Date: January 1, 2024", fontsize=9, fontname="hebo")
    page.insert_text(pymupdf.Point(72, y + 40), "Approved by: VP of Human Resources, December 15, 2023", fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(72, y + 55), "INTERNAL USE ONLY — Not for distribution outside HR and Finance.", fontsize=9, fontname="hebo", color=(0.7, 0, 0))
    doc.save(f'{SENSITIVE_DIR}/salary_schedule.pdf')
    doc.close()
    print("Created salary_schedule.pdf")

    # --- 6. bonus_plan.pdf ---
    doc = pymupdf.open()
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 60), "Executive Bonus Plan — FY2024", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(72, 85), "Board-Approved Incentive Compensation Structure", fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 95), pymupdf.Point(540, 95))
    shape.finish(color=(0.1, 0.1, 0.4), width=1.5)
    shape.commit()

    bp_headers = ["Executive", "Base Comp", "Target Bonus %", "Max Bonus %", "Trigger Metric"]
    bpx = [72, 185, 290, 385, 470]
    y = 120
    for i, h in enumerate(bp_headers):
        page.insert_text(pymupdf.Point(bpx[i], y), h, fontsize=9, fontname="hebo")

    bonus_data = [
        ("CEO — J. Mitchell", "$340,000", "50%", "100%", "Revenue Growth"),
        ("CFO — L. Brennan", "$255,000", "40%", "80%", "EBITDA Margin"),
        ("CTO — R. Vasquez", "$260,000", "40%", "80%", "Product Delivery"),
        ("COO — M. Tanaka", "$245,000", "35%", "70%", "Ops Efficiency"),
        ("VP Sales — K. Adams", "$200,000", "45%", "90%", "Bookings Target"),
        ("VP Eng — S. Gupta", "$195,000", "30%", "60%", "Sprint Velocity"),
    ]
    y = 140
    for row in bonus_data:
        for i, val in enumerate(row):
            page.insert_text(pymupdf.Point(bpx[i], y), val, fontsize=8, fontname="helv")
        y += 16

    y += 15
    page.insert_text(pymupdf.Point(72, y), "Vesting Schedule:", fontsize=10, fontname="hebo")
    page.insert_text(pymupdf.Point(72, y + 16), "- 50% paid at fiscal year-end upon board approval", fontsize=9, fontname="helv")
    page.insert_text(pymupdf.Point(72, y + 30), "- 25% deferred to Q1 of following year (retention clause)", fontsize=9, fontname="helv")
    page.insert_text(pymupdf.Point(72, y + 44), "- 25% tied to individual KPI achievement (HR review)", fontsize=9, fontname="helv")

    page.insert_text(pymupdf.Point(72, y + 70), "STRICTLY CONFIDENTIAL — Board of Directors and C-Suite Only", fontsize=9, fontname="hebo", color=(0.7, 0, 0))
    doc.save(f'{SENSITIVE_DIR}/bonus_plan.pdf')
    doc.close()
    print("Created bonus_plan.pdf")

    # GUI-ready: open file manager to the sensitive directory
    launch_gui(f'nautilus "{SENSITIVE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')


create_initial()
