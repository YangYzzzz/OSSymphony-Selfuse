"""
Initial Setup: Create encrypted archived records PDF
Task ID: pdf_mbc_029
Domain: pdf
Creates ~/Secure/archived_records.pdf encrypted with RC4, user password 'arch1ve2020', 30 pages.
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_029'
SECURE_DIR = f'{WORKDIR}/Secure'
OUTPUT_UNENC = f'/tmp/{TASK_ID}_plain.pdf'
OUTPUT = f'{SECURE_DIR}/archived_records.pdf'

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
    os.makedirs(SECURE_DIR, exist_ok=True)

    # Create a 30-page PDF with realistic archived records content
    doc = pymupdf.open()

    # Document metadata
    doc.set_metadata({
        "title": "Archived Records 2018-2020",
        "author": "Central Records Office",
        "subject": "Archived Personnel and Financial Records",
        "keywords": "archive, records, personnel, finance, 2018, 2019, 2020",
        "creator": "Records Management System v3.2",
    })

    departments = [
        "Engineering", "Marketing", "Finance", "Human Resources",
        "Operations", "Sales", "Legal", "Research & Development",
        "Customer Support", "Information Technology"
    ]

    employees = [
        ("Sarah Chen", "EMP-2018-0042", "Senior Engineer", "$92,400"),
        ("Marcus Johnson", "EMP-2018-0078", "Marketing Director", "$105,800"),
        ("Priya Patel", "EMP-2018-0103", "Financial Analyst", "$78,500"),
        ("James O'Brien", "EMP-2018-0156", "HR Coordinator", "$65,200"),
        ("Lisa Nakamura", "EMP-2019-0012", "Operations Manager", "$88,700"),
        ("David Kowalski", "EMP-2019-0034", "Sales Representative", "$62,100"),
        ("Amara Osei", "EMP-2019-0067", "Legal Counsel", "$115,300"),
        ("Robert Fernandez", "EMP-2019-0089", "Research Scientist", "$97,600"),
        ("Emma Johansson", "EMP-2020-0005", "Support Lead", "$71,400"),
        ("Wei Zhang", "EMP-2020-0023", "IT Administrator", "$83,900"),
        ("Catherine Dubois", "EMP-2018-0198", "Project Manager", "$94,100"),
        ("Tomasz Nowak", "EMP-2019-0112", "Data Analyst", "$76,800"),
        ("Aisha Rahman", "EMP-2020-0045", "UX Designer", "$82,300"),
        ("Michael Torres", "EMP-2018-0221", "Quality Assurance Lead", "$79,500"),
        ("Yuki Tanaka", "EMP-2019-0145", "Software Developer", "$91,200"),
    ]

    quarters = ["Q1", "Q2", "Q3", "Q4"]
    years = ["2018", "2019", "2020"]

    revenue_data = {
        "2018": {"Q1": "$2,345,000", "Q2": "$2,567,000", "Q3": "$2,890,000", "Q4": "$3,120,000"},
        "2019": {"Q1": "$3,210,000", "Q2": "$3,450,000", "Q3": "$3,678,000", "Q4": "$3,890,000"},
        "2020": {"Q1": "$3,150,000", "Q2": "$2,890,000", "Q3": "$3,450,000", "Q4": "$3,780,000"},
    }

    expense_categories = [
        "Salaries & Benefits", "Office Lease", "Equipment & Supplies",
        "Software Licenses", "Travel & Entertainment", "Professional Services",
        "Insurance", "Utilities", "Marketing & Advertising", "Miscellaneous"
    ]

    # Page 1: Cover Page
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(180, 250), "ARCHIVED RECORDS", fontsize=28, fontname="hebo", color=(0.1, 0.1, 0.4))
    page.insert_text(pymupdf.Point(210, 290), "2018 - 2020", fontsize=22, fontname="helv", color=(0.2, 0.2, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(150, 310), pymupdf.Point(462, 310))
    shape.finish(color=(0.1, 0.1, 0.4), width=2)
    shape.commit()
    page.insert_text(pymupdf.Point(175, 360), "Central Records Office", fontsize=16, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(195, 385), "Classification: Internal", fontsize=12, fontname="heit", color=(0.5, 0.5, 0.5))
    page.insert_text(pymupdf.Point(175, 420), "Document ID: ARC-2020-FINAL-001", fontsize=11, fontname="cour", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(175, 445), "Date Archived: December 31, 2020", fontsize=11, fontname="cour", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(175, 470), "Retention Period: 7 Years", fontsize=11, fontname="cour", color=(0.4, 0.4, 0.4))

    # Page 2: Table of Contents
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "TABLE OF CONTENTS", fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.4))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(540, 82))
    shape.finish(color=(0.1, 0.1, 0.4), width=1)
    shape.commit()
    toc_items = [
        ("1. Executive Summary", "3"),
        ("2. Personnel Records - 2018", "4"),
        ("3. Personnel Records - 2019", "7"),
        ("4. Personnel Records - 2020", "10"),
        ("5. Financial Summary - 2018", "13"),
        ("6. Financial Summary - 2019", "16"),
        ("7. Financial Summary - 2020", "19"),
        ("8. Departmental Reports", "22"),
        ("9. Compliance & Audit Trail", "25"),
        ("10. Appendices", "28"),
    ]
    y = 120
    for title, pg in toc_items:
        page.insert_text(pymupdf.Point(90, y), title, fontsize=12, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(490, y), pg, fontsize=12, fontname="helv", color=(0, 0, 0))
        y += 28

    # Page 3: Executive Summary
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "1. EXECUTIVE SUMMARY", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
    summary_text = (
        "This document consolidates all archived records from the Central Records Office for the "
        "fiscal years 2018 through 2020. The archive includes personnel records for all active and "
        "separated employees, quarterly financial summaries, departmental performance reports, and "
        "compliance documentation as required under corporate retention policy CRP-2015-007.\n\n"
        "During the three-year period covered by this archive, the organization experienced steady "
        "growth in revenue from $10.92 million in 2018 to $14.27 million in 2020, representing a "
        "compound annual growth rate of approximately 14.3%. Total headcount grew from 142 employees "
        "at the start of 2018 to 198 by year-end 2020.\n\n"
        "Key highlights of the archived period include the successful completion of the ERP migration "
        "project in Q2 2019, the opening of the Portland regional office in Q4 2018, and the transition "
        "to remote operations beginning March 2020. All records contained herein have been verified for "
        "accuracy by the internal audit team and conform to regulatory requirements."
    )
    rect = pymupdf.Rect(72, 100, 540, 700)
    page.insert_textbox(rect, summary_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Pages 4-6: Personnel Records 2018
    for pg_idx in range(3):
        page = doc.new_page(width=612, height=792)
        if pg_idx == 0:
            page.insert_text(pymupdf.Point(72, 72), "2. PERSONNEL RECORDS - 2018", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
            start_y = 110
        else:
            page.insert_text(pymupdf.Point(72, 72), f"2. Personnel Records - 2018 (continued)", fontsize=12, fontname="heit", color=(0.3, 0.3, 0.3))
            start_y = 100
        y = start_y
        subset = employees[pg_idx*5:(pg_idx+1)*5] if pg_idx < 3 else employees[:2]
        for emp in subset:
            page.insert_text(pymupdf.Point(90, y), f"Name: {emp[0]}", fontsize=11, fontname="hebo", color=(0, 0, 0))
            page.insert_text(pymupdf.Point(90, y+18), f"Employee ID: {emp[1]}    Position: {emp[2]}", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
            page.insert_text(pymupdf.Point(90, y+34), f"Annual Compensation: {emp[3]}    Status: Active", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
            page.insert_text(pymupdf.Point(90, y+50), f"Department: {departments[employees.index(emp) % len(departments)]}", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(85, y+60), pymupdf.Point(530, y+60))
            shape.finish(color=(0.8, 0.8, 0.8), width=0.5)
            shape.commit()
            y += 80

    # Pages 7-9: Personnel Records 2019
    for pg_idx in range(3):
        page = doc.new_page(width=612, height=792)
        if pg_idx == 0:
            page.insert_text(pymupdf.Point(72, 72), "3. PERSONNEL RECORDS - 2019", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
            start_y = 110
        else:
            page.insert_text(pymupdf.Point(72, 72), f"3. Personnel Records - 2019 (continued)", fontsize=12, fontname="heit", color=(0.3, 0.3, 0.3))
            start_y = 100
        y = start_y
        subset = employees[pg_idx*5:(pg_idx+1)*5]
        for emp in subset:
            page.insert_text(pymupdf.Point(90, y), f"Name: {emp[0]}", fontsize=11, fontname="hebo", color=(0, 0, 0))
            page.insert_text(pymupdf.Point(90, y+18), f"Employee ID: {emp[1]}    Position: {emp[2]}", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
            page.insert_text(pymupdf.Point(90, y+34), f"Annual Compensation: {emp[3]}    Status: Active", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
            page.insert_text(pymupdf.Point(90, y+50), f"Review Rating: Meets Expectations", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(85, y+60), pymupdf.Point(530, y+60))
            shape.finish(color=(0.8, 0.8, 0.8), width=0.5)
            shape.commit()
            y += 80

    # Pages 10-12: Personnel Records 2020
    for pg_idx in range(3):
        page = doc.new_page(width=612, height=792)
        if pg_idx == 0:
            page.insert_text(pymupdf.Point(72, 72), "4. PERSONNEL RECORDS - 2020", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
            start_y = 110
        else:
            page.insert_text(pymupdf.Point(72, 72), f"4. Personnel Records - 2020 (continued)", fontsize=12, fontname="heit", color=(0.3, 0.3, 0.3))
            start_y = 100
        y = start_y
        subset = employees[pg_idx*5:(pg_idx+1)*5]
        for emp in subset:
            page.insert_text(pymupdf.Point(90, y), f"Name: {emp[0]}", fontsize=11, fontname="hebo", color=(0, 0, 0))
            page.insert_text(pymupdf.Point(90, y+18), f"Employee ID: {emp[1]}    Position: {emp[2]}", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
            page.insert_text(pymupdf.Point(90, y+34), f"Annual Compensation: {emp[3]}    Remote: Yes (COVID-19)", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(85, y+60), pymupdf.Point(530, y+60))
            shape.finish(color=(0.8, 0.8, 0.8), width=0.5)
            shape.commit()
            y += 80

    # Pages 13-15: Financial Summary 2018
    for pg_idx in range(3):
        page = doc.new_page(width=612, height=792)
        if pg_idx == 0:
            page.insert_text(pymupdf.Point(72, 72), "5. FINANCIAL SUMMARY - 2018", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
            y = 110
            page.insert_text(pymupdf.Point(90, y), "Quarterly Revenue:", fontsize=12, fontname="hebo", color=(0, 0, 0))
            y += 25
            for q in quarters:
                page.insert_text(pymupdf.Point(110, y), f"{q}: {revenue_data['2018'][q]}", fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))
                y += 20
            page.insert_text(pymupdf.Point(90, y+10), "Total Revenue: $10,922,000", fontsize=12, fontname="hebo", color=(0, 0, 0))
        elif pg_idx == 1:
            page.insert_text(pymupdf.Point(72, 72), "5. Financial Summary - 2018 (Expenses)", fontsize=12, fontname="heit", color=(0.3, 0.3, 0.3))
            y = 100
            for i, cat in enumerate(expense_categories):
                amt = 150000 + i * 45000
                page.insert_text(pymupdf.Point(110, y), f"{cat}: ${amt:,}", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
                y += 22
        else:
            page.insert_text(pymupdf.Point(72, 72), "5. Financial Summary - 2018 (Analysis)", fontsize=12, fontname="heit", color=(0.3, 0.3, 0.3))
            analysis = (
                "The 2018 fiscal year demonstrated strong fundamentals with consistent quarter-over-quarter "
                "revenue growth. The opening of the Portland regional office in Q4 contributed an additional "
                "$230,000 in revenue during its first quarter of operations. Operating margins remained stable "
                "at 18.2%, slightly above the industry average of 16.8%. Key cost drivers included the "
                "one-time ERP system procurement cost of $340,000 and increased hiring expenses related to "
                "the 23 new positions filled during the year."
            )
            rect = pymupdf.Rect(72, 100, 540, 600)
            page.insert_textbox(rect, analysis, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Pages 16-18: Financial Summary 2019
    for pg_idx in range(3):
        page = doc.new_page(width=612, height=792)
        if pg_idx == 0:
            page.insert_text(pymupdf.Point(72, 72), "6. FINANCIAL SUMMARY - 2019", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
            y = 110
            page.insert_text(pymupdf.Point(90, y), "Quarterly Revenue:", fontsize=12, fontname="hebo", color=(0, 0, 0))
            y += 25
            for q in quarters:
                page.insert_text(pymupdf.Point(110, y), f"{q}: {revenue_data['2019'][q]}", fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))
                y += 20
            page.insert_text(pymupdf.Point(90, y+10), "Total Revenue: $14,228,000", fontsize=12, fontname="hebo", color=(0, 0, 0))
        elif pg_idx == 1:
            page.insert_text(pymupdf.Point(72, 72), "6. Financial Summary - 2019 (Expenses)", fontsize=12, fontname="heit", color=(0.3, 0.3, 0.3))
            y = 100
            for i, cat in enumerate(expense_categories):
                amt = 175000 + i * 52000
                page.insert_text(pymupdf.Point(110, y), f"{cat}: ${amt:,}", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
                y += 22
        else:
            page.insert_text(pymupdf.Point(72, 72), "6. Financial Summary - 2019 (Analysis)", fontsize=12, fontname="heit", color=(0.3, 0.3, 0.3))
            analysis = (
                "Fiscal year 2019 marked a significant milestone with the successful completion of the "
                "ERP migration project in Q2, which streamlined operations and reduced manual processing "
                "time by approximately 35%. Revenue grew 30.3% year-over-year to $14.23 million. The "
                "Portland office reached full operational capacity in Q3, contributing $890,000 to annual "
                "revenue. Employee satisfaction scores averaged 4.2 out of 5.0, the highest in company history."
            )
            rect = pymupdf.Rect(72, 100, 540, 600)
            page.insert_textbox(rect, analysis, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Pages 19-21: Financial Summary 2020
    for pg_idx in range(3):
        page = doc.new_page(width=612, height=792)
        if pg_idx == 0:
            page.insert_text(pymupdf.Point(72, 72), "7. FINANCIAL SUMMARY - 2020", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
            y = 110
            page.insert_text(pymupdf.Point(90, y), "Quarterly Revenue:", fontsize=12, fontname="hebo", color=(0, 0, 0))
            y += 25
            for q in quarters:
                page.insert_text(pymupdf.Point(110, y), f"{q}: {revenue_data['2020'][q]}", fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))
                y += 20
            page.insert_text(pymupdf.Point(90, y+10), "Total Revenue: $13,270,000", fontsize=12, fontname="hebo", color=(0, 0, 0))
        elif pg_idx == 1:
            page.insert_text(pymupdf.Point(72, 72), "7. Financial Summary - 2020 (Expenses)", fontsize=12, fontname="heit", color=(0.3, 0.3, 0.3))
            y = 100
            for i, cat in enumerate(expense_categories):
                amt = 160000 + i * 48000
                page.insert_text(pymupdf.Point(110, y), f"{cat}: ${amt:,}", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
                y += 22
        else:
            page.insert_text(pymupdf.Point(72, 72), "7. Financial Summary - 2020 (Analysis)", fontsize=12, fontname="heit", color=(0.3, 0.3, 0.3))
            analysis = (
                "The 2020 fiscal year was significantly impacted by the global pandemic. Q2 revenue "
                "declined 8.3% compared to Q1 as the company transitioned to fully remote operations. "
                "However, the organization demonstrated resilience, recovering in Q3 and achieving "
                "near-record Q4 results. Total revenue of $13.27 million represented a 6.7% decline "
                "from 2019, but profitability was maintained through cost optimization measures including "
                "reduced travel expenses ($420,000 savings) and renegotiated vendor contracts."
            )
            rect = pymupdf.Rect(72, 100, 540, 600)
            page.insert_textbox(rect, analysis, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Pages 22-24: Departmental Reports
    for pg_idx in range(3):
        page = doc.new_page(width=612, height=792)
        if pg_idx == 0:
            page.insert_text(pymupdf.Point(72, 72), "8. DEPARTMENTAL REPORTS", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
            y = 110
        else:
            page.insert_text(pymupdf.Point(72, 72), "8. Departmental Reports (continued)", fontsize=12, fontname="heit", color=(0.3, 0.3, 0.3))
            y = 100
        dept_subset = departments[pg_idx*3:(pg_idx+1)*3 + (1 if pg_idx == 2 else 0)]
        for dept in dept_subset:
            page.insert_text(pymupdf.Point(90, y), dept, fontsize=13, fontname="hebo", color=(0.1, 0.1, 0.4))
            y += 20
            page.insert_text(pymupdf.Point(110, y), f"Headcount: {15 + hash(dept) % 20}  |  Budget Utilization: {85 + hash(dept) % 14}%", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
            y += 18
            page.insert_text(pymupdf.Point(110, y), f"Performance Rating: {3.5 + (hash(dept) % 15) / 10:.1f}/5.0  |  Attrition Rate: {4 + hash(dept) % 8}%", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
            y += 18
            page.insert_text(pymupdf.Point(110, y), f"Key Achievement: Completed annual targets within budget allocation.", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(85, y+15), pymupdf.Point(530, y+15))
            shape.finish(color=(0.8, 0.8, 0.8), width=0.5)
            shape.commit()
            y += 40

    # Pages 25-27: Compliance & Audit Trail
    for pg_idx in range(3):
        page = doc.new_page(width=612, height=792)
        if pg_idx == 0:
            page.insert_text(pymupdf.Point(72, 72), "9. COMPLIANCE & AUDIT TRAIL", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
            compliance_text = (
                "All records contained in this archive have been subject to the following compliance checks:\n\n"
                "1. SOX Compliance Review (completed March 2021)\n"
                "   - Financial records verified by external auditor Deloitte & Touche LLP\n"
                "   - No material misstatements identified\n"
                "   - Internal controls rated as 'Effective'\n\n"
                "2. GDPR Data Protection Audit (completed January 2021)\n"
                "   - Personnel data handling procedures reviewed\n"
                "   - All data subject consent forms verified\n"
                "   - Retention schedules confirmed compliant\n\n"
                "3. Internal Audit Report IA-2021-003 (completed February 2021)\n"
                "   - Record completeness: 99.7%\n"
                "   - Cross-referencing accuracy: 99.2%\n"
                "   - Recommendations: 2 minor, 0 major findings"
            )
            rect = pymupdf.Rect(72, 100, 540, 700)
            page.insert_textbox(rect, compliance_text, fontsize=10, fontname="helv", color=(0, 0, 0))
        elif pg_idx == 1:
            page.insert_text(pymupdf.Point(72, 72), "9. Compliance & Audit Trail (continued)", fontsize=12, fontname="heit", color=(0.3, 0.3, 0.3))
            audit_entries = [
                ("2021-01-15", "Archive created from source systems", "System"),
                ("2021-01-16", "Data integrity checksums generated", "System"),
                ("2021-01-20", "Initial compliance review completed", "J. Martinez"),
                ("2021-02-05", "Internal audit commenced", "Audit Team"),
                ("2021-02-28", "Internal audit completed - no issues", "K. Williams"),
                ("2021-03-10", "SOX review commenced", "Deloitte LLP"),
                ("2021-03-31", "SOX review completed - compliant", "Deloitte LLP"),
                ("2021-04-15", "Final archive certification", "Records Office"),
            ]
            y = 100
            page.insert_text(pymupdf.Point(90, y), "Date", fontsize=10, fontname="hebo", color=(0, 0, 0))
            page.insert_text(pymupdf.Point(190, y), "Action", fontsize=10, fontname="hebo", color=(0, 0, 0))
            page.insert_text(pymupdf.Point(460, y), "By", fontsize=10, fontname="hebo", color=(0, 0, 0))
            y += 20
            for date, action, by in audit_entries:
                page.insert_text(pymupdf.Point(90, y), date, fontsize=9, fontname="cour", color=(0.2, 0.2, 0.2))
                page.insert_text(pymupdf.Point(190, y), action, fontsize=9, fontname="helv", color=(0.2, 0.2, 0.2))
                page.insert_text(pymupdf.Point(460, y), by, fontsize=9, fontname="helv", color=(0.2, 0.2, 0.2))
                y += 18
        else:
            page.insert_text(pymupdf.Point(72, 72), "9. Compliance - Certification", fontsize=12, fontname="heit", color=(0.3, 0.3, 0.3))
            cert_text = (
                "CERTIFICATION OF ARCHIVE INTEGRITY\n\n"
                "I hereby certify that the records contained in this archived document are true and "
                "accurate copies of the original records maintained by the Central Records Office for "
                "fiscal years 2018, 2019, and 2020.\n\n"
                "All records have been reviewed for completeness and accuracy in accordance with "
                "corporate retention policy CRP-2015-007 and applicable regulatory requirements.\n\n"
                "Certified by: Maria Santiago, Director of Records Management\n"
                "Date: April 30, 2021\n"
                "Digital Signature ID: DS-2021-04-30-MS-7829"
            )
            rect = pymupdf.Rect(72, 100, 540, 500)
            page.insert_textbox(rect, cert_text, fontsize=11, fontname="helv", color=(0, 0, 0))

    # Pages 28-30: Appendices
    for pg_idx in range(3):
        page = doc.new_page(width=612, height=792)
        if pg_idx == 0:
            page.insert_text(pymupdf.Point(72, 72), "10. APPENDICES", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.4))
            page.insert_text(pymupdf.Point(90, 110), "Appendix A: Abbreviations and Definitions", fontsize=13, fontname="hebo", color=(0, 0, 0))
            abbrevs = [
                ("CRP", "Corporate Retention Policy"),
                ("ERP", "Enterprise Resource Planning"),
                ("GDPR", "General Data Protection Regulation"),
                ("SOX", "Sarbanes-Oxley Act"),
                ("IA", "Internal Audit"),
                ("FY", "Fiscal Year"),
                ("YoY", "Year-over-Year"),
                ("CAGR", "Compound Annual Growth Rate"),
                ("KPI", "Key Performance Indicator"),
                ("SLA", "Service Level Agreement"),
            ]
            y = 140
            for abbr, defn in abbrevs:
                page.insert_text(pymupdf.Point(110, y), f"{abbr}", fontsize=10, fontname="hebo", color=(0, 0, 0))
                page.insert_text(pymupdf.Point(180, y), f"- {defn}", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
                y += 18
        elif pg_idx == 1:
            page.insert_text(pymupdf.Point(72, 72), "Appendix B: Contact Information", fontsize=13, fontname="hebo", color=(0, 0, 0))
            contacts = [
                ("Records Management", "records@company.com", "ext. 4501"),
                ("Internal Audit", "audit@company.com", "ext. 4520"),
                ("Legal Department", "legal@company.com", "ext. 4530"),
                ("Human Resources", "hr@company.com", "ext. 4540"),
                ("Finance Department", "finance@company.com", "ext. 4550"),
                ("IT Support", "itsupport@company.com", "ext. 4560"),
            ]
            y = 110
            for dept, email, ext in contacts:
                page.insert_text(pymupdf.Point(90, y), dept, fontsize=10, fontname="hebo", color=(0, 0, 0))
                page.insert_text(pymupdf.Point(90, y+16), f"Email: {email}    Phone: {ext}", fontsize=9, fontname="helv", color=(0.2, 0.2, 0.2))
                y += 40
        else:
            page.insert_text(pymupdf.Point(72, 72), "Appendix C: Revision History", fontsize=13, fontname="hebo", color=(0, 0, 0))
            revisions = [
                ("1.0", "2021-01-15", "Initial archive creation", "System Auto"),
                ("1.1", "2021-02-28", "Added audit trail section", "K. Williams"),
                ("1.2", "2021-03-31", "Added SOX compliance certification", "M. Santiago"),
                ("2.0", "2021-04-30", "Final certified version", "M. Santiago"),
            ]
            y = 110
            page.insert_text(pymupdf.Point(90, y), "Version", fontsize=10, fontname="hebo", color=(0, 0, 0))
            page.insert_text(pymupdf.Point(160, y), "Date", fontsize=10, fontname="hebo", color=(0, 0, 0))
            page.insert_text(pymupdf.Point(260, y), "Description", fontsize=10, fontname="hebo", color=(0, 0, 0))
            page.insert_text(pymupdf.Point(460, y), "Author", fontsize=10, fontname="hebo", color=(0, 0, 0))
            y += 22
            for ver, date, desc, author in revisions:
                page.insert_text(pymupdf.Point(90, y), ver, fontsize=9, fontname="cour", color=(0.2, 0.2, 0.2))
                page.insert_text(pymupdf.Point(160, y), date, fontsize=9, fontname="cour", color=(0.2, 0.2, 0.2))
                page.insert_text(pymupdf.Point(260, y), desc, fontsize=9, fontname="helv", color=(0.2, 0.2, 0.2))
                page.insert_text(pymupdf.Point(460, y), author, fontsize=9, fontname="helv", color=(0.2, 0.2, 0.2))
                y += 18

    # Save unencrypted first
    doc.save(OUTPUT_UNENC)
    doc.close()
    print(f"Plain PDF created with {30} pages: {OUTPUT_UNENC}")

    # Now encrypt with RC4 and user password 'arch1ve2020' using pikepdf
    import pikepdf
    pdf = pikepdf.open(OUTPUT_UNENC)
    pdf.save(
        OUTPUT,
        encryption=pikepdf.Encryption(
            owner="owner_arch2020",
            user="arch1ve2020",
            R=4,  # R=4 = RC4 128-bit (PDF 1.5 compatible)
        ),
    )
    pdf.close()
    print(f"Encrypted PDF (RC4) saved: {OUTPUT}")

    # Clean up temp
    os.remove(OUTPUT_UNENC)

    # Open in Evince for GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
