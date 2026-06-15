"""
Initial Setup: Create a multi-page PDF with mixed page sizes for dimension verification task.
Task ID: pdf_cr_048
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
TASK_ID = 'pdf_cr_048'
OUTPUT = f'{WORKDIR}/Desktop/mixed_sizes.pdf'


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
    os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)

    doc = pymupdf.open()

    # --- Page 1: A4 (595 x 842) ---
    page1 = doc.new_page(width=595, height=842)
    page1.insert_text(
        pymupdf.Point(72, 60),
        "Meridian Consulting Group",
        fontsize=22,
        fontname="hebo",
        color=(0.1, 0.15, 0.4),
    )
    page1.insert_text(
        pymupdf.Point(72, 90),
        "Strategic Planning Document - Q1 2025",
        fontsize=14,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    rect1 = pymupdf.Rect(72, 120, 523, 400)
    page1.insert_textbox(
        rect1,
        (
            "This document outlines the strategic initiatives planned for the first quarter "
            "of 2025. Our team has identified several key growth areas including market "
            "expansion into Southeast Asia, product diversification within the enterprise "
            "software segment, and strengthening our consulting partnerships with Fortune 500 "
            "companies.\n\n"
            "Key performance indicators for this quarter include a 15% increase in client "
            "retention, a target revenue of $4.2 million from new accounts, and the launch "
            "of three new service offerings in cloud migration, data analytics, and "
            "cybersecurity assessment."
        ),
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 2: Letter (612 x 792) ---
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(
        pymupdf.Point(72, 60),
        "Financial Summary - North America Division",
        fontsize=18,
        fontname="hebo",
        color=(0.0, 0.3, 0.15),
    )
    y = 100
    rows = [
        ("Region", "Revenue ($K)", "Expenses ($K)", "Margin (%)"),
        ("Northeast", "1,245", "892", "28.4"),
        ("Southeast", "987", "710", "28.1"),
        ("Midwest", "1,102", "834", "24.3"),
        ("Southwest", "876", "645", "26.4"),
        ("Pacific West", "1,534", "1,087", "29.1"),
    ]
    for i, row in enumerate(rows):
        x = 72
        fontname = "hebo" if i == 0 else "helv"
        for cell in row:
            page2.insert_text(pymupdf.Point(x, y), cell, fontsize=10, fontname=fontname, color=(0, 0, 0))
            x += 130
        y += 20

    page2.insert_text(
        pymupdf.Point(72, y + 30),
        "Note: All figures are preliminary and subject to final audit review.",
        fontsize=9,
        fontname="tiit",
        color=(0.4, 0.4, 0.4),
    )

    # --- Page 3: Legal (612 x 1008) ---
    page3 = doc.new_page(width=612, height=1008)
    page3.insert_text(
        pymupdf.Point(72, 60),
        "Terms and Conditions of Service Agreement",
        fontsize=18,
        fontname="hebo",
        color=(0.2, 0.0, 0.0),
    )
    sections = [
        ("1. Scope of Services",
         "The Consultant agrees to provide strategic advisory services as described in "
         "Exhibit A attached hereto. Services shall commence on the Effective Date and "
         "continue for a period of twelve (12) months unless terminated earlier in "
         "accordance with Section 7 below."),
        ("2. Compensation",
         "Client shall pay Consultant a monthly retainer of $18,500, payable within "
         "thirty (30) days of receipt of invoice. Additional project-based fees shall "
         "be billed at the rates specified in Exhibit B."),
        ("3. Confidentiality",
         "Each party agrees to hold in strict confidence all Confidential Information "
         "received from the other party. Confidential Information includes, but is not "
         "limited to, trade secrets, client lists, financial data, business strategies, "
         "and proprietary methodologies."),
        ("4. Intellectual Property",
         "All work product created by Consultant in the performance of Services shall "
         "be considered work made for hire and shall be the exclusive property of Client. "
         "Consultant retains the right to use general knowledge, skills, and experience "
         "gained during the engagement."),
        ("5. Limitation of Liability",
         "In no event shall either party be liable for indirect, incidental, special, "
         "consequential, or punitive damages arising out of or related to this Agreement, "
         "regardless of the cause of action or theory of liability."),
    ]
    y = 100
    for title, body in sections:
        page3.insert_text(pymupdf.Point(72, y), title, fontsize=12, fontname="hebo", color=(0, 0, 0))
        y += 20
        rect = pymupdf.Rect(72, y, 540, y + 80)
        page3.insert_textbox(rect, body, fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 90

    # --- Page 4: A3 (842 x 1191) ---
    page4 = doc.new_page(width=842, height=1191)
    page4.insert_text(
        pymupdf.Point(72, 60),
        "Project Timeline - Enterprise Migration Program",
        fontsize=24,
        fontname="hebo",
        color=(0.0, 0.2, 0.5),
    )
    page4.insert_text(
        pymupdf.Point(72, 100),
        "Program Duration: January 2025 - December 2025",
        fontsize=14,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    milestones = [
        ("Phase 1: Discovery & Assessment", "Jan - Mar 2025", "Infrastructure audit, stakeholder interviews, risk assessment"),
        ("Phase 2: Architecture Design", "Apr - Jun 2025", "Cloud architecture blueprint, security framework, migration roadmap"),
        ("Phase 3: Pilot Migration", "Jul - Aug 2025", "Migrate 3 non-critical workloads, performance benchmarking"),
        ("Phase 4: Full Migration", "Sep - Nov 2025", "Batch migration of 47 remaining workloads, parallel testing"),
        ("Phase 5: Optimization & Handoff", "Dec 2025", "Cost optimization, knowledge transfer, documentation"),
    ]
    y = 150
    for phase, period, desc in milestones:
        page4.insert_text(pymupdf.Point(72, y), phase, fontsize=13, fontname="hebo", color=(0.0, 0.2, 0.5))
        page4.insert_text(pymupdf.Point(72, y + 20), f"Timeline: {period}", fontsize=11, fontname="helv", color=(0.4, 0.4, 0.4))
        page4.insert_text(pymupdf.Point(72, y + 38), desc, fontsize=11, fontname="helv", color=(0, 0, 0))
        y += 70

    # --- Page 5: Custom (500 x 700) ---
    page5 = doc.new_page(width=500, height=700)
    page5.insert_text(
        pymupdf.Point(50, 50),
        "Quick Reference Card",
        fontsize=16,
        fontname="hebo",
        color=(0.5, 0.0, 0.3),
    )
    page5.insert_text(
        pymupdf.Point(50, 80),
        "Emergency Contacts & Key Resources",
        fontsize=11,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    contacts = [
        ("IT Help Desk", "ext. 4500", "support@meridian.com"),
        ("Facilities", "ext. 4200", "facilities@meridian.com"),
        ("HR Department", "ext. 4100", "hr@meridian.com"),
        ("Security Office", "ext. 4800", "security@meridian.com"),
        ("Project Manager", "ext. 4350", "pm-office@meridian.com"),
    ]
    y = 120
    for dept, phone, email in contacts:
        page5.insert_text(pymupdf.Point(50, y), dept, fontsize=10, fontname="hebo", color=(0, 0, 0))
        page5.insert_text(pymupdf.Point(200, y), phone, fontsize=10, fontname="helv", color=(0, 0, 0))
        page5.insert_text(pymupdf.Point(300, y), email, fontsize=10, fontname="helv", color=(0, 0, 0.6))
        y += 22

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
