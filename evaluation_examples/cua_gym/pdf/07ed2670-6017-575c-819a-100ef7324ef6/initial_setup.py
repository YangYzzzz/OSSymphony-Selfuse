"""
Initial Setup: Create a 20-page employee payroll report PDF with embedded
bank account numbers and Social Security numbers for redaction task.
Task ID: pdf_fin_004
Domain: pdf
"""

import os
import random
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_004'
FINANCE_DIR = f'{WORKDIR}/finance'
OUTPUT = f'{FINANCE_DIR}/payroll_march2024.pdf'


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


# ── Realistic employee data ──────────────────────────────────────────────

FIRST_NAMES = [
    "Sarah", "Marcus", "Elena", "David", "Priya", "James", "Mei-Lin",
    "Carlos", "Aisha", "Thomas", "Yuki", "Robert", "Fatima", "Andrew",
    "Olivia", "Kwame", "Jessica", "Rajesh", "Hannah", "Dmitri",
    "Lauren", "Wei", "Michelle", "Alejandro", "Grace", "Patrick",
    "Nadia", "Samuel", "Christina", "Haruto", "Rebecca", "Omar",
    "Sophia", "Daniel", "Amara", "Michael", "Keiko", "Benjamin",
    "Valentina", "Jordan",
]

LAST_NAMES = [
    "Chen", "Johnson", "Kowalski", "Okafor", "Patel", "Williams",
    "Rodriguez", "Nakamura", "Thompson", "Al-Rashid", "Kim", "Mueller",
    "Garcia", "Singh", "Anderson", "Mbeki", "Johansson", "Tanaka",
    "DeSilva", "Petrov", "Harper", "Li", "Brooks", "Martinez",
    "Fitzgerald", "Park", "Schmidt", "Morales", "Suzuki", "Campbell",
    "Fernandez", "Nguyen", "O'Brien", "Sato", "Richardson", "Gupta",
    "Morrison", "Costa", "Yamamoto", "Bennett",
]

DEPARTMENTS = [
    "Engineering", "Marketing", "Finance", "Human Resources", "Sales",
    "Operations", "Legal", "Product", "Customer Success", "IT",
]

TITLES = [
    "Software Engineer", "Marketing Manager", "Financial Analyst",
    "HR Coordinator", "Sales Representative", "Operations Lead",
    "Legal Counsel", "Product Manager", "Account Manager", "IT Specialist",
    "Senior Developer", "VP of Marketing", "Controller", "Recruiter",
    "Business Development", "Logistics Manager", "Compliance Officer",
    "UX Designer", "Support Lead", "Systems Administrator",
]

random.seed(42)  # reproducible


def gen_ssn():
    """Generate a realistic-looking SSN in XXX-XX-XXXX format."""
    return f"{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(1000,9999)}"


def gen_bank_account():
    """Generate a bank account number — alternates between two patterns."""
    if random.random() < 0.6:
        # XXXX-XXXX-XXXX pattern
        return f"{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}"
    else:
        # XXXXXXXXXX pattern (10 digits)
        return str(random.randint(1000000000, 9999999999))


def gen_salary():
    base = random.randint(55, 165) * 1000
    return base


def gen_employees(n):
    """Generate n unique employee records."""
    employees = []
    used_names = set()
    for _ in range(n):
        while True:
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            name = f"{first} {last}"
            if name not in used_names:
                used_names.add(name)
                break
        emp = {
            "name": name,
            "emp_id": f"EMP-{random.randint(10000,99999)}",
            "department": random.choice(DEPARTMENTS),
            "title": random.choice(TITLES),
            "ssn": gen_ssn(),
            "bank_account": gen_bank_account(),
            "salary": gen_salary(),
            "fed_tax": 0,
            "state_tax": 0,
            "ss_tax": 0,
            "medicare": 0,
            "health_ins": random.choice([250, 350, 450, 550]),
            "retirement": 0,
        }
        emp["fed_tax"] = round(emp["salary"] * random.uniform(0.18, 0.24) / 12, 2)
        emp["state_tax"] = round(emp["salary"] * random.uniform(0.04, 0.08) / 12, 2)
        emp["ss_tax"] = round(emp["salary"] * 0.062 / 12, 2)
        emp["medicare"] = round(emp["salary"] * 0.0145 / 12, 2)
        emp["retirement"] = round(emp["salary"] * random.uniform(0.03, 0.10) / 12, 2)
        gross_monthly = round(emp["salary"] / 12, 2)
        total_deductions = round(
            emp["fed_tax"] + emp["state_tax"] + emp["ss_tax"]
            + emp["medicare"] + emp["health_ins"] + emp["retirement"], 2
        )
        emp["gross_monthly"] = gross_monthly
        emp["total_deductions"] = total_deductions
        emp["net_pay"] = round(gross_monthly - total_deductions, 2)
        employees.append(emp)
    return employees


def create_initial():
    import pymupdf

    os.makedirs(FINANCE_DIR, exist_ok=True)

    employees = gen_employees(40)

    # We need 15 bank accounts and 25 SSNs across 20 pages.
    # We'll create exactly 40 employees spread over pages 2-19 (2 per page on 18 pages, + extras).
    # Page 0: cover page
    # Page 1: summary / table of contents
    # Pages 2-19: employee payroll detail (roughly 2-3 employees per page)

    doc = pymupdf.open()

    PAGE_W, PAGE_H = 612, 792  # Letter size

    # ── Helper: draw page header/footer ──
    def draw_header_footer(page, page_num, total_pages):
        # Header
        page.insert_text(
            pymupdf.Point(72, 40),
            "CONFIDENTIAL — Meridian Technologies Inc.",
            fontsize=8, fontname="heit", color=(0.4, 0.4, 0.4),
        )
        page.draw_line(
            pymupdf.Point(72, 48), pymupdf.Point(540, 48),
            color=(0.7, 0.7, 0.7), width=0.5,
        )
        # Footer
        page.draw_line(
            pymupdf.Point(72, 752), pymupdf.Point(540, 752),
            color=(0.7, 0.7, 0.7), width=0.5,
        )
        page.insert_text(
            pymupdf.Point(72, 768),
            f"Payroll Report — March 2024",
            fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4),
        )
        page.insert_text(
            pymupdf.Point(480, 768),
            f"Page {page_num} of {total_pages}",
            fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4),
        )

    total_pages = 20

    # ── Page 0: Cover Page ──
    cover = doc.new_page(width=PAGE_W, height=PAGE_H)
    # Company logo area (just a colored rect)
    shape = cover.new_shape()
    shape.draw_rect(pymupdf.Rect(72, 100, 540, 160))
    shape.finish(fill=(0.12, 0.25, 0.50), color=(0.12, 0.25, 0.50))
    shape.commit()
    cover.insert_text(
        pymupdf.Point(85, 142),
        "MERIDIAN TECHNOLOGIES INC.",
        fontsize=22, fontname="hebo", color=(1, 1, 1),
    )
    cover.insert_text(
        pymupdf.Point(200, 240),
        "Employee Payroll Report",
        fontsize=24, fontname="hebo", color=(0.12, 0.25, 0.50),
    )
    cover.insert_text(
        pymupdf.Point(230, 280),
        "Pay Period: March 1–31, 2024",
        fontsize=14, fontname="helv", color=(0.3, 0.3, 0.3),
    )
    cover.insert_text(
        pymupdf.Point(220, 310),
        "Prepared by: Payroll Department",
        fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3),
    )
    cover.insert_text(
        pymupdf.Point(200, 340),
        "Classification: STRICTLY CONFIDENTIAL",
        fontsize=12, fontname="hebo", color=(0.8, 0.0, 0.0),
    )
    cover.insert_text(
        pymupdf.Point(130, 420),
        "This document contains sensitive employee information including",
        fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3),
    )
    cover.insert_text(
        pymupdf.Point(130, 435),
        "Social Security numbers and bank account details for direct deposit.",
        fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3),
    )
    cover.insert_text(
        pymupdf.Point(130, 450),
        "Unauthorized disclosure is prohibited under company policy CP-2024-07.",
        fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3),
    )
    draw_header_footer(cover, 1, total_pages)

    # ── Page 1: Table of Contents / Summary ──
    toc_page = doc.new_page(width=PAGE_W, height=PAGE_H)
    draw_header_footer(toc_page, 2, total_pages)
    toc_page.insert_text(
        pymupdf.Point(72, 80),
        "Payroll Summary — March 2024",
        fontsize=18, fontname="hebo", color=(0.12, 0.25, 0.50),
    )

    total_gross = sum(e["gross_monthly"] for e in employees)
    total_net = sum(e["net_pay"] for e in employees)
    total_deductions = sum(e["total_deductions"] for e in employees)

    summary_lines = [
        f"Total Employees:          {len(employees)}",
        f"Total Gross Payroll:      ${total_gross:,.2f}",
        f"Total Deductions:         ${total_deductions:,.2f}",
        f"Total Net Disbursement:   ${total_net:,.2f}",
        "",
        "Department Breakdown:",
    ]
    y = 120
    for line in summary_lines:
        toc_page.insert_text(
            pymupdf.Point(90, y), line,
            fontsize=11, fontname="helv", color=(0, 0, 0),
        )
        y += 18

    # Department breakdown
    dept_totals = {}
    for e in employees:
        dept_totals.setdefault(e["department"], {"count": 0, "gross": 0})
        dept_totals[e["department"]]["count"] += 1
        dept_totals[e["department"]]["gross"] += e["gross_monthly"]

    y += 5
    # Table header
    toc_page.insert_text(pymupdf.Point(90, y), "Department", fontsize=10, fontname="hebo", color=(0, 0, 0))
    toc_page.insert_text(pymupdf.Point(250, y), "Headcount", fontsize=10, fontname="hebo", color=(0, 0, 0))
    toc_page.insert_text(pymupdf.Point(370, y), "Gross Payroll", fontsize=10, fontname="hebo", color=(0, 0, 0))
    y += 4
    toc_page.draw_line(pymupdf.Point(90, y), pymupdf.Point(500, y), color=(0, 0, 0), width=0.5)
    y += 14
    for dept in sorted(dept_totals.keys()):
        info = dept_totals[dept]
        toc_page.insert_text(pymupdf.Point(90, y), dept, fontsize=10, fontname="helv", color=(0, 0, 0))
        toc_page.insert_text(pymupdf.Point(270, y), str(info["count"]), fontsize=10, fontname="helv", color=(0, 0, 0))
        toc_page.insert_text(pymupdf.Point(370, y), f"${info['gross']:,.2f}", fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 16

    y += 20
    toc_page.insert_text(
        pymupdf.Point(90, y),
        "Detailed employee records follow on pages 3–20.",
        fontsize=10, fontname="heit", color=(0.3, 0.3, 0.3),
    )

    # ── Pages 2-19: Employee Detail Pages (18 pages, ~2-3 employees each) ──
    # Distribute 40 employees: first 4 pages get 3 each (=12), remaining 14 pages get 2 each (=28), total=40
    # But we need exactly 15 bank accounts and 25 SSNs shown.
    # Actually, every employee has both an SSN and a bank account.
    # The task says "15 bank account numbers and 25 SSNs across various pages".
    # We'll show SSN for 25 employees and bank account for 15 employees.
    # Some employees show both, some show only SSN in a "tax info" section,
    # some show bank account in a "direct deposit" section.

    # Decide which employees show SSN and which show bank account
    # 25 show SSN, 15 show bank account.
    # Let's have employees 0-14 show both SSN and bank account (15 bank + 15 SSN)
    # Employees 15-24 show only SSN (10 more SSN = 25 total)
    # Employees 25-39 show neither sensitive data (just regular payroll info)

    ssn_shown = set(range(25))       # employees 0-24 show SSN (25 total)
    bank_shown = set(range(15))      # employees 0-14 show bank account (15 total)

    # Distribute employees across 18 detail pages
    emp_per_page = []
    idx = 0
    for p in range(18):
        if p < 4:
            count = 3
        else:
            count = 2
        emp_per_page.append(employees[idx:idx+count])
        idx += count
    # Remaining employees go on last page
    if idx < len(employees):
        emp_per_page[-1].extend(employees[idx:])

    emp_global_idx = 0
    for page_idx, page_employees in enumerate(emp_per_page):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        page_num = page_idx + 3  # pages 3-20
        draw_header_footer(page, page_num, total_pages)

        page.insert_text(
            pymupdf.Point(72, 78),
            f"Employee Payroll Detail — Page {page_idx + 1} of 18",
            fontsize=13, fontname="hebo", color=(0.12, 0.25, 0.50),
        )

        y = 105
        for emp in page_employees:
            gi = emp_global_idx  # global employee index

            # Employee header bar
            shape = page.new_shape()
            shape.draw_rect(pymupdf.Rect(72, y - 5, 540, y + 14))
            shape.finish(fill=(0.90, 0.93, 0.97), color=(0.70, 0.75, 0.82))
            shape.commit()

            page.insert_text(
                pymupdf.Point(78, y + 10),
                f"{emp['name']}  |  {emp['emp_id']}  |  {emp['department']}  |  {emp['title']}",
                fontsize=9, fontname="hebo", color=(0.1, 0.1, 0.1),
            )
            y += 26

            # Personal / Tax info section
            if gi in ssn_shown:
                page.insert_text(
                    pymupdf.Point(90, y),
                    f"Social Security Number: {emp['ssn']}",
                    fontsize=9, fontname="helv", color=(0, 0, 0),
                )
                y += 14

            # Direct Deposit info
            if gi in bank_shown:
                page.insert_text(
                    pymupdf.Point(90, y),
                    f"Direct Deposit Account: {emp['bank_account']}",
                    fontsize=9, fontname="helv", color=(0, 0, 0),
                )
                y += 14

            # Earnings
            page.insert_text(pymupdf.Point(90, y), "Earnings:", fontsize=9, fontname="hebo", color=(0, 0, 0))
            y += 13
            page.insert_text(
                pymupdf.Point(110, y),
                f"Annual Salary: ${emp['salary']:,.2f}     Monthly Gross: ${emp['gross_monthly']:,.2f}",
                fontsize=8, fontname="helv", color=(0, 0, 0),
            )
            y += 13

            # Deductions
            page.insert_text(pymupdf.Point(90, y), "Deductions:", fontsize=9, fontname="hebo", color=(0, 0, 0))
            y += 13
            page.insert_text(
                pymupdf.Point(110, y),
                f"Federal Tax: ${emp['fed_tax']:,.2f}    State Tax: ${emp['state_tax']:,.2f}    "
                f"SS Tax: ${emp['ss_tax']:,.2f}    Medicare: ${emp['medicare']:,.2f}",
                fontsize=8, fontname="helv", color=(0, 0, 0),
            )
            y += 12
            page.insert_text(
                pymupdf.Point(110, y),
                f"Health Insurance: ${emp['health_ins']:,.2f}    401(k): ${emp['retirement']:,.2f}    "
                f"Total Deductions: ${emp['total_deductions']:,.2f}",
                fontsize=8, fontname="helv", color=(0, 0, 0),
            )
            y += 14

            # Net Pay
            page.insert_text(
                pymupdf.Point(90, y),
                f"Net Pay: ${emp['net_pay']:,.2f}",
                fontsize=9, fontname="hebo", color=(0.0, 0.4, 0.0),
            )
            y += 12

            # Separator
            page.draw_line(
                pymupdf.Point(80, y), pymupdf.Point(530, y),
                color=(0.8, 0.8, 0.8), width=0.3,
            )
            y += 18

            emp_global_idx += 1

    # Set metadata
    doc.set_metadata({
        "title": "Employee Payroll Report - March 2024",
        "author": "Meridian Technologies Inc. - Payroll Department",
        "subject": "Monthly Payroll",
        "keywords": "payroll, march, 2024, confidential",
        "creator": "Meridian Payroll System v4.2",
        "producer": "PyMuPDF",
    })

    # Add Table of Contents bookmarks
    toc = [
        [1, "Cover Page", 1],
        [1, "Payroll Summary", 2],
        [1, "Employee Details", 3],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()

    print(f"Initial file created: {OUTPUT}")
    print(f"Total pages: {total_pages}")
    print(f"SSNs embedded: {len(ssn_shown)}")
    print(f"Bank accounts embedded: {len(bank_shown)}")

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print("GUI_READY: launched Evince with DISPLAY=:0")


create_initial()
