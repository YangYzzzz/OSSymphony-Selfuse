"""
Initial Setup: Create an unencrypted 8-page confidential business PDF
Task ID: pdf_ro_008
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_008'
OUTPUT = f'{WORKDIR}/Documents/confidential.pdf'


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
    os.makedirs(f'{WORKDIR}/Documents', exist_ok=True)

    doc = pymupdf.open()

    # --- Page 1: Title / Cover Page ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 120), "CONFIDENTIAL", fontsize=36, fontname="hebo", color=(0.7, 0, 0))
    page.insert_text(pymupdf.Point(72, 180), "Meridian Global Partners", fontsize=24, fontname="hebo", color=(0, 0, 0.3))
    page.insert_text(pymupdf.Point(72, 220), "Strategic Growth & Acquisition Report", fontsize=16, fontname="tiro", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(72, 260), "Fiscal Year 2025 - Q4 Analysis", fontsize=14, fontname="tiro", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(72, 310), "Prepared by: Office of the CFO", fontsize=12, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(72, 335), "Distribution: Board of Directors Only", fontsize=12, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(72, 360), "Date: December 15, 2025", fontsize=12, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(72, 400), "Classification: STRICTLY CONFIDENTIAL", fontsize=11, fontname="hebo", color=(0.8, 0, 0))

    # --- Page 2: Executive Summary ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "1. Executive Summary", fontsize=18, fontname="hebo", color=(0, 0, 0.3))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape.finish(color=(0, 0, 0.3), width=1.5)
    shape.commit()
    summary = (
        "Meridian Global Partners achieved record revenue of $847.3 million in Q4 2025, "
        "representing a 23.4% year-over-year increase. Net income reached $142.6 million, "
        "driven by strong performance in our Asia-Pacific division and the successful "
        "integration of the Vertex Analytics acquisition completed in July 2025. "
        "Operating margins expanded to 22.8%, up from 19.1% in the prior year quarter. "
        "The board approved a special dividend of $2.45 per share to be distributed in "
        "January 2026. Our strategic pipeline includes three potential acquisition targets "
        "valued between $200M and $500M each, currently under NDA-protected due diligence."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 350), summary, fontsize=11, fontname="tiro", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 370), "Key Highlights:", fontsize=13, fontname="hebo", color=(0, 0, 0))
    highlights = [
        "Revenue: $847.3M (+23.4% YoY)",
        "Net Income: $142.6M (+31.2% YoY)",
        "Operating Margin: 22.8% (up from 19.1%)",
        "Headcount: 4,872 employees across 14 offices",
        "Cash Position: $1.23B (including credit facilities)",
        "Debt-to-Equity Ratio: 0.42 (down from 0.58)",
    ]
    y = 395
    for h in highlights:
        page.insert_text(pymupdf.Point(90, y), f"  {h}", fontsize=11, fontname="helv", color=(0, 0, 0))
        y += 20

    # --- Page 3: Revenue Breakdown ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "2. Revenue Breakdown by Division", fontsize=18, fontname="hebo", color=(0, 0, 0.3))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape.finish(color=(0, 0, 0.3), width=1.5)
    shape.commit()
    divisions = [
        ("Division", "Q4 2025", "Q4 2024", "Growth"),
        ("North America", "$312.5M", "$268.1M", "+16.6%"),
        ("Europe & UK", "$198.7M", "$172.3M", "+15.3%"),
        ("Asia-Pacific", "$214.8M", "$152.4M", "+40.9%"),
        ("Latin America", "$78.2M", "$62.8M", "+24.5%"),
        ("Middle East & Africa", "$43.1M", "$31.2M", "+38.1%"),
        ("TOTAL", "$847.3M", "$686.8M", "+23.4%"),
    ]
    y = 110
    for i, row in enumerate(divisions):
        x = 72
        font = "hebo" if i == 0 or i == len(divisions) - 1 else "helv"
        for val in row:
            page.insert_text(pymupdf.Point(x, y), val, fontsize=10, fontname=font, color=(0, 0, 0))
            x += 120
        y += 22

    page.insert_textbox(
        pymupdf.Rect(72, y + 20, 540, y + 120),
        "The Asia-Pacific division demonstrated the strongest growth trajectory at 40.9%, "
        "primarily fueled by our expansion into the South Korean and Vietnamese markets. "
        "The Singapore hub, opened in March 2025, has already secured $45M in new contracts "
        "with regional financial institutions.",
        fontsize=11, fontname="tiro", color=(0, 0, 0),
    )

    # --- Page 4: Acquisition Pipeline ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "3. Acquisition Pipeline (HIGHLY SENSITIVE)", fontsize=18, fontname="hebo", color=(0.7, 0, 0))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape.finish(color=(0.7, 0, 0), width=1.5)
    shape.commit()
    targets = [
        ("Target Alpha (Codename: Phoenix)", "$320M", "Cloud Infrastructure", "Due Diligence Phase 2"),
        ("Target Beta (Codename: Orion)", "$485M", "AI/ML Platform", "LOI Signed, Pending Board Approval"),
        ("Target Gamma (Codename: Atlas)", "$210M", "Cybersecurity", "Preliminary Discussions"),
    ]
    y = 110
    for name, val, sector, status in targets:
        page.insert_text(pymupdf.Point(72, y), name, fontsize=12, fontname="hebo", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(90, y + 20), f"Estimated Value: {val}", fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(90, y + 38), f"Sector: {sector}", fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(90, y + 56), f"Status: {status}", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
        y += 85
    page.insert_textbox(
        pymupdf.Rect(72, y + 10, 540, y + 80),
        "NOTICE: The information on this page is subject to non-disclosure agreements. "
        "Any unauthorized distribution may result in legal action and termination of employment.",
        fontsize=10, fontname="hebo", color=(0.7, 0, 0),
    )

    # --- Page 5: Financial Projections ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "4. Financial Projections FY2026", fontsize=18, fontname="hebo", color=(0, 0, 0.3))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape.finish(color=(0, 0, 0.3), width=1.5)
    shape.commit()
    projections = [
        ("Metric", "FY2025 Actual", "FY2026 Conservative", "FY2026 Optimistic"),
        ("Revenue", "$3.12B", "$3.58B", "$3.94B"),
        ("EBITDA", "$782M", "$915M", "$1.02B"),
        ("Net Income", "$498M", "$580M", "$655M"),
        ("EPS", "$8.42", "$9.81", "$11.08"),
        ("Free Cash Flow", "$612M", "$720M", "$810M"),
        ("Capex", "$245M", "$310M", "$340M"),
    ]
    y = 110
    for i, row in enumerate(projections):
        x = 72
        font = "hebo" if i == 0 else "helv"
        for val in row:
            page.insert_text(pymupdf.Point(x, y), val, fontsize=10, fontname=font, color=(0, 0, 0))
            x += 120
        y += 22

    # --- Page 6: Personnel Changes ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "5. Key Personnel & Compensation", fontsize=18, fontname="hebo", color=(0, 0, 0.3))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape.finish(color=(0, 0, 0.3), width=1.5)
    shape.commit()
    personnel = [
        ("Name", "Title", "Base Salary", "Bonus", "Equity"),
        ("Catherine Xu", "CEO", "$1.85M", "$2.4M", "125K RSUs"),
        ("David Nakamura", "CFO", "$1.2M", "$1.5M", "85K RSUs"),
        ("Elena Petrova", "CTO", "$1.15M", "$1.3M", "90K RSUs"),
        ("James Okafor", "COO", "$1.1M", "$1.2M", "75K RSUs"),
        ("Sarah Martinez", "CLO", "$980K", "$800K", "60K RSUs"),
        ("Michael Reeves", "VP Engineering", "$620K", "$450K", "40K RSUs"),
        ("Anita Desai", "VP Sales APAC", "$580K", "$720K", "35K RSUs"),
    ]
    y = 110
    for i, row in enumerate(personnel):
        x = 72
        font = "hebo" if i == 0 else "helv"
        for val in row:
            page.insert_text(pymupdf.Point(x, y), val, fontsize=9, fontname=font, color=(0, 0, 0))
            x += 100
        y += 20

    # --- Page 7: Risk Assessment ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "6. Risk Assessment & Mitigation", fontsize=18, fontname="hebo", color=(0, 0, 0.3))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape.finish(color=(0, 0, 0.3), width=1.5)
    shape.commit()
    risks = [
        ("Regulatory Compliance (HIGH)", "New EU data sovereignty requirements effective March 2026 "
         "may require infrastructure relocation for European client data. Estimated cost: $12-18M."),
        ("Currency Exposure (MEDIUM)", "Approximately 38% of revenue is denominated in non-USD currencies. "
         "Current hedging covers 65% of projected exposure through Q2 2026."),
        ("Talent Retention (MEDIUM)", "Key engineering leads in the AI division have received competing "
         "offers. Retention packages worth $4.2M have been proposed for 12 critical employees."),
        ("Supply Chain (LOW)", "Cloud infrastructure costs have stabilized. Multi-cloud strategy "
         "provides adequate redundancy across AWS, Azure, and GCP."),
    ]
    y = 110
    for title, desc in risks:
        page.insert_text(pymupdf.Point(72, y), title, fontsize=12, fontname="hebo", color=(0, 0, 0))
        page.insert_textbox(pymupdf.Rect(90, y + 8, 540, y + 70), desc, fontsize=10, fontname="tiro", color=(0.2, 0.2, 0.2))
        y += 80

    # --- Page 8: Legal Disclaimer ---
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(72, 72), "7. Legal Disclaimer & Distribution Notice", fontsize=18, fontname="hebo", color=(0, 0, 0.3))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape.finish(color=(0, 0, 0.3), width=1.5)
    shape.commit()
    disclaimer = (
        "This document contains proprietary and confidential information belonging to "
        "Meridian Global Partners, Inc. ('the Company'). It is intended solely for the "
        "use of authorized members of the Board of Directors and designated senior executives.\n\n"
        "Unauthorized reproduction, distribution, or disclosure of this material, in whole "
        "or in part, is strictly prohibited and may result in civil and criminal penalties "
        "under applicable securities regulations, including but not limited to the Securities "
        "Exchange Act of 1934 and Regulation FD.\n\n"
        "Recipients of this document are reminded of their fiduciary duties and obligations "
        "under the Company's Insider Trading Policy (revised September 2025). Trading on "
        "material non-public information contained herein is prohibited.\n\n"
        "For questions regarding this report, contact the Office of the General Counsel at "
        "legal@meridianglobal.com or +1 (212) 555-0199.\n\n"
        "Document ID: MGP-2025-Q4-BOARD-007\n"
        "Version: 3.2 (Final)\n"
        "Last Modified: December 14, 2025 at 11:47 PM EST"
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 600), disclaimer, fontsize=11, fontname="tiro", color=(0, 0, 0))

    # Set metadata
    doc.set_metadata({
        "title": "Strategic Growth & Acquisition Report - Q4 2025",
        "author": "Meridian Global Partners - Office of the CFO",
        "subject": "Confidential Board Report",
        "keywords": "confidential, financial, Q4 2025, acquisition, board",
        "creator": "Meridian Document Management System",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
