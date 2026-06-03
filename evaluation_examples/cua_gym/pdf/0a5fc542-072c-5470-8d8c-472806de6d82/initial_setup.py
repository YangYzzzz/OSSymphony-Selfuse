"""
Initial Setup: Create a 200-page discovery production PDF for legal case
Task ID: pdf_legal_021
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import random

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_021'
OUTPUT_DIR = f'{WORKDIR}/legal/discovery'
OUTPUT = f'{OUTPUT_DIR}/production_001.pdf'

LETTER_W, LETTER_H = 612, 792  # US Letter in points

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


# --- Realistic legal discovery content ---

CASE_CAPTION = "UNITED STATES DISTRICT COURT\nSOUTHERN DISTRICT OF NEW YORK\n\nMERIDIAN TECHNOLOGIES, INC.,\n    Plaintiff,\n        v.\n\nATLAS GLOBAL SOLUTIONS, LLC,\n    Defendant.\n\nCase No. 24-CV-03847-RWS"

LAW_FIRM = "KIRKLAND & ASSOCIATES LLP\n555 Madison Avenue, 30th Floor\nNew York, NY 10022\nTel: (212) 555-0147"

EXHIBIT_CATEGORIES = [
    "Email Correspondence",
    "Board Meeting Minutes",
    "Financial Statements",
    "Employment Contracts",
    "Internal Memoranda",
    "Audit Reports",
    "Vendor Agreements",
    "Patent Applications",
    "Compliance Reviews",
    "Strategic Planning Documents",
]

PEOPLE = [
    ("David Chen", "Chief Executive Officer"),
    ("Sarah Mitchell", "General Counsel"),
    ("Robert Vasquez", "Chief Financial Officer"),
    ("Priya Patel", "VP of Engineering"),
    ("James O'Brien", "Director of Operations"),
    ("Lena Kowalski", "Head of Compliance"),
    ("Marcus Thompson", "Senior Vice President"),
    ("Catherine Wu", "Board Member"),
    ("Anthony DiNapoli", "External Auditor"),
    ("Rebecca Hartman", "Chief Technology Officer"),
    ("William Tran", "Controller"),
    ("Aisha Rahman", "VP of Human Resources"),
    ("Derek Sullivan", "Senior Counsel"),
    ("Natasha Volkov", "Director of Strategy"),
    ("Gregory Park", "Chief Information Officer"),
]

EMAIL_SUBJECTS = [
    "Re: Q3 Revenue Projections - CONFIDENTIAL",
    "FW: Merger Discussion Timeline Update",
    "Follow-up: Due Diligence Materials Request",
    "Re: Re: Atlas Partnership Framework",
    "PRIVILEGED: Board Resolution Draft",
    "Re: IP License Agreement Revisions",
    "Quarterly Compliance Report - Action Required",
    "Re: Budget Reallocation for FY2024",
    "FW: Vendor Performance Evaluation Results",
    "Re: Strategic Initiative - Project Phoenix",
    "CONFIDENTIAL: Executive Compensation Review",
    "Re: Data Migration Timeline Concerns",
    "Follow-up: Regulatory Filing Deadline",
    "Re: FW: Client Presentation Materials",
    "DRAFT: Press Release for Board Approval",
]

LOREM_LEGAL = [
    "Pursuant to the terms and conditions set forth in the Master Services Agreement dated March 15, 2023, the parties hereby acknowledge and agree that all intellectual property rights created during the engagement period shall remain the exclusive property of the commissioning party, subject to the limited license granted herein.",
    "The undersigned hereby certifies that, to the best of their knowledge, information, and belief, formed after reasonable inquiry, the representations contained in this document are truthful and accurate in all material respects as of the date of execution.",
    "Notwithstanding anything to the contrary contained herein, neither party shall be liable to the other party for any indirect, incidental, consequential, special, or exemplary damages arising out of or in connection with this Agreement, including but not limited to loss of revenue, loss of profits, loss of business, or loss of data.",
    "In consideration of the mutual covenants and agreements hereinafter set forth and for other good and valuable consideration, the receipt and sufficiency of which are hereby acknowledged, the parties agree to be bound by the following terms and conditions.",
    "The Board of Directors, having duly considered the matter presented at the special meeting convened on September 12, 2023, and having reviewed the supporting documentation provided by management and external advisors, hereby resolves to authorize the proposed transaction.",
    "This document is produced subject to and without waiver of any applicable privileges, including but not limited to the attorney-client privilege, work product doctrine, and any other applicable protections under federal and state law.",
    "All financial projections and forward-looking statements contained herein are based on management's current expectations and assumptions regarding future events and are subject to significant risks and uncertainties that could cause actual results to differ materially.",
    "The compliance audit conducted for the period ending December 31, 2023, identified several areas requiring remediation, as detailed in Appendix B. Management has committed to implementing corrective measures within the timeframes specified herein.",
    "Respondent's counsel is hereby notified that the depositions of the individuals listed in Exhibit A shall commence on the dates and at the locations specified therein, subject to any mutually agreed modifications to the schedule.",
    "The intellectual property portfolio review conducted by the Technology Assessment Team identified 47 active patents, 12 pending applications, and 8 registered trademarks directly relevant to the subject matter of this litigation.",
]

FINANCIAL_LINE_ITEMS = [
    "Revenue", "Cost of Goods Sold", "Gross Profit", "Research & Development",
    "Sales & Marketing", "General & Administrative", "Depreciation & Amortization",
    "Operating Income", "Interest Expense", "Income Tax Provision",
    "Net Income", "Earnings Per Share (Basic)", "Earnings Per Share (Diluted)",
    "Total Assets", "Total Liabilities", "Shareholders' Equity",
]


def add_bates_stamp(page, page_num, total_pages):
    """Add Bates number stamp to bottom of page."""
    bates = f"MERIDIAN-{page_num:06d}"
    page.insert_text(
        pymupdf.Point(LETTER_W - 180, LETTER_H - 25),
        bates,
        fontsize=8,
        fontname="cour",
        color=(0.4, 0.4, 0.4),
    )
    page.insert_text(
        pymupdf.Point(72, LETTER_H - 25),
        "CONFIDENTIAL — SUBJECT TO PROTECTIVE ORDER",
        fontsize=7,
        fontname="helv",
        color=(0.5, 0.0, 0.0),
    )


def add_cover_page(doc):
    """Add production cover sheet."""
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    y = 120
    page.insert_text(pymupdf.Point(72, y), "DOCUMENT PRODUCTION", fontsize=22, fontname="hebo", color=(0, 0, 0))
    y += 40
    page.insert_text(pymupdf.Point(72, y), "Production No. 001", fontsize=14, fontname="helv", color=(0.2, 0.2, 0.2))
    y += 50

    for line in CASE_CAPTION.split('\n'):
        page.insert_text(pymupdf.Point(72, y), line, fontsize=11, fontname="tiro", color=(0, 0, 0))
        y += 16
    y += 30

    page.insert_text(pymupdf.Point(72, y), "PRODUCED BY:", fontsize=10, fontname="hebo", color=(0, 0, 0))
    y += 18
    for line in LAW_FIRM.split('\n'):
        page.insert_text(pymupdf.Point(72, y), line, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 14
    y += 30

    page.insert_text(pymupdf.Point(72, y), "Date of Production: January 15, 2024", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 16
    page.insert_text(pymupdf.Point(72, y), "Bates Range: MERIDIAN-000001 through MERIDIAN-000200", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 16
    page.insert_text(pymupdf.Point(72, y), "Total Documents: 200 pages", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 40

    page.insert_text(pymupdf.Point(72, y), "CONFIDENTIALITY NOTICE", fontsize=12, fontname="hebo", color=(0.6, 0, 0))
    y += 20
    rect = pymupdf.Rect(72, y, LETTER_W - 72, y + 80)
    page.insert_textbox(
        rect,
        "This production contains documents designated as CONFIDENTIAL pursuant to the "
        "Stipulated Protective Order entered by the Court on October 3, 2023. Unauthorized "
        "disclosure, reproduction, or distribution of these materials is strictly prohibited "
        "and may result in sanctions.",
        fontsize=9,
        fontname="helv",
        color=(0, 0, 0),
    )
    add_bates_stamp(page, 1, 200)
    return page


def add_toc_page(doc, page_num_start):
    """Add table of contents / exhibit index."""
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    y = 72
    page.insert_text(pymupdf.Point(72, y), "EXHIBIT INDEX", fontsize=16, fontname="hebo", color=(0, 0, 0))
    y += 30

    # Draw table header
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(LETTER_W - 72, y))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()
    y += 5

    page.insert_text(pymupdf.Point(72, y + 12), "Exhibit", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(160, y + 12), "Description", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(420, y + 12), "Bates Range", fontsize=9, fontname="hebo", color=(0, 0, 0))
    y += 20

    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(72, y), pymupdf.Point(LETTER_W - 72, y))
    shape2.finish(color=(0, 0, 0), width=0.5)
    shape2.commit()
    y += 8

    current_bates = 3
    for i, cat in enumerate(EXHIBIT_CATEGORIES):
        exhibit_label = chr(65 + i)
        end_bates = current_bates + random.randint(10, 25)
        page.insert_text(pymupdf.Point(85, y), f"Exhibit {exhibit_label}", fontsize=9, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(160, y), cat, fontsize=9, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(420, y), f"MERIDIAN-{current_bates:06d} - {end_bates:06d}", fontsize=9, fontname="cour", color=(0.3, 0.3, 0.3))
        y += 18
        current_bates = end_bates + 1

    add_bates_stamp(page, page_num_start, 200)
    return page


def add_email_page(doc, page_num, email_idx):
    """Generate a realistic email exhibit page."""
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    y = 72

    sender = PEOPLE[email_idx % len(PEOPLE)]
    recipient = PEOPLE[(email_idx + 3) % len(PEOPLE)]
    cc = PEOPLE[(email_idx + 7) % len(PEOPLE)]
    subject = EMAIL_SUBJECTS[email_idx % len(EMAIL_SUBJECTS)]

    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    date_str = f"{months[email_idx % 12]} {(email_idx % 28) + 1}, 2023"

    page.insert_text(pymupdf.Point(72, y), f"EXHIBIT {chr(65 + (email_idx % 10))}-{email_idx + 1}", fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 25

    # Draw separator
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(LETTER_W - 72, y))
    shape.finish(color=(0.5, 0.5, 0.5), width=0.5)
    shape.commit()
    y += 15

    fields = [
        ("From:", f"{sender[0]} <{sender[0].lower().replace(' ', '.')}@meridiantech.com>"),
        ("To:", f"{recipient[0]} <{recipient[0].lower().replace(' ', '.')}@meridiantech.com>"),
        ("Cc:", f"{cc[0]} <{cc[0].lower().replace(' ', '.')}@meridiantech.com>"),
        ("Date:", f"{date_str} at {9 + email_idx % 8}:{email_idx % 60:02d} AM EST"),
        ("Subject:", subject),
    ]

    for label, value in fields:
        page.insert_text(pymupdf.Point(72, y), label, fontsize=9, fontname="hebo", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(130, y), value, fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 14

    y += 15
    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(72, y), pymupdf.Point(LETTER_W - 72, y))
    shape2.finish(color=(0.5, 0.5, 0.5), width=0.5)
    shape2.commit()
    y += 20

    # Email body — 2-3 paragraphs
    paragraphs_to_use = [LOREM_LEGAL[email_idx % len(LOREM_LEGAL)],
                         LOREM_LEGAL[(email_idx + 4) % len(LOREM_LEGAL)]]
    if email_idx % 3 == 0:
        paragraphs_to_use.append(LOREM_LEGAL[(email_idx + 7) % len(LOREM_LEGAL)])

    for para in paragraphs_to_use:
        rect = pymupdf.Rect(72, y, LETTER_W - 72, y + 120)
        excess = page.insert_textbox(rect, para, fontsize=10, fontname="helv", color=(0, 0, 0), align=0)
        y += 120 - max(excess, 0) + 15

    # Signature block
    if y < LETTER_H - 120:
        page.insert_text(pymupdf.Point(72, y + 10), "Best regards,", fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(72, y + 28), sender[0], fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(72, y + 42), sender[1], fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))
        page.insert_text(pymupdf.Point(72, y + 55), "Meridian Technologies, Inc.", fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))

    add_bates_stamp(page, page_num, 200)
    return page


def add_minutes_page(doc, page_num, meeting_idx):
    """Generate board meeting minutes page."""
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    y = 72

    quarter = (meeting_idx % 4) + 1
    year = 2023 if meeting_idx < 4 else 2024

    page.insert_text(pymupdf.Point(72, y), "MERIDIAN TECHNOLOGIES, INC.", fontsize=14, fontname="hebo", color=(0, 0, 0))
    y += 22
    page.insert_text(pymupdf.Point(72, y), f"MINUTES OF THE BOARD OF DIRECTORS MEETING", fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 20
    page.insert_text(pymupdf.Point(72, y), f"Q{quarter} {year} — Regular Session", fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))
    y += 30

    page.insert_text(pymupdf.Point(72, y), "ATTENDEES:", fontsize=10, fontname="hebo", color=(0, 0, 0))
    y += 16
    attendees = random.sample(PEOPLE, min(8, len(PEOPLE)))
    for person in attendees:
        page.insert_text(pymupdf.Point(90, y), f"• {person[0]}, {person[1]}", fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 13
    y += 15

    agenda_items = [
        f"Review and Approval of Q{quarter} {year} Financial Results",
        "Report from the Audit Committee",
        "Strategic Initiatives Update — Project Phoenix",
        "Compliance and Regulatory Matters",
        "Executive Compensation Discussion",
        "New Business and Adjournment",
    ]

    page.insert_text(pymupdf.Point(72, y), "AGENDA:", fontsize=10, fontname="hebo", color=(0, 0, 0))
    y += 16
    for i, item in enumerate(agenda_items[:4 + meeting_idx % 3], 1):
        page.insert_text(pymupdf.Point(90, y), f"{i}. {item}", fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 13
    y += 15

    page.insert_text(pymupdf.Point(72, y), "DISCUSSION:", fontsize=10, fontname="hebo", color=(0, 0, 0))
    y += 16

    discussion_text = LOREM_LEGAL[(meeting_idx + 2) % len(LOREM_LEGAL)]
    rect = pymupdf.Rect(72, y, LETTER_W - 72, y + 100)
    page.insert_textbox(rect, discussion_text, fontsize=9, fontname="helv", color=(0, 0, 0))
    y += 115

    if y < LETTER_H - 80:
        page.insert_text(pymupdf.Point(72, y), "RESOLVED:", fontsize=10, fontname="hebo", color=(0, 0, 0))
        y += 16
        rect2 = pymupdf.Rect(72, y, LETTER_W - 72, y + 60)
        page.insert_textbox(rect2, LOREM_LEGAL[(meeting_idx + 5) % len(LOREM_LEGAL)], fontsize=9, fontname="helv", color=(0, 0, 0))

    add_bates_stamp(page, page_num, 200)
    return page


def add_financial_page(doc, page_num, fin_idx):
    """Generate a financial statement page."""
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    y = 72

    quarter = (fin_idx % 4) + 1
    year = 2023

    page.insert_text(pymupdf.Point(72, y), "MERIDIAN TECHNOLOGIES, INC.", fontsize=13, fontname="hebo", color=(0, 0, 0))
    y += 20
    statements = ["Consolidated Income Statement", "Consolidated Balance Sheet",
                  "Cash Flow Statement", "Statement of Shareholders' Equity"]
    page.insert_text(pymupdf.Point(72, y), statements[fin_idx % 4], fontsize=11, fontname="hebo", color=(0, 0, 0))
    y += 18
    page.insert_text(pymupdf.Point(72, y), f"For the Quarter Ended {'March 31' if quarter == 1 else 'June 30' if quarter == 2 else 'September 30' if quarter == 3 else 'December 31'}, {year}", fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))
    y += 14
    page.insert_text(pymupdf.Point(72, y), "(In thousands, except per share data)", fontsize=8, fontname="heit", color=(0.4, 0.4, 0.4))
    y += 25

    # Table header
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(LETTER_W - 72, y))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()
    y += 5

    page.insert_text(pymupdf.Point(72, y + 12), "Line Item", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(350, y + 12), f"Q{quarter} {year}", fontsize=9, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(440, y + 12), f"Q{quarter} {year - 1}", fontsize=9, fontname="hebo", color=(0, 0, 0))
    y += 18

    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(72, y), pymupdf.Point(LETTER_W - 72, y))
    shape2.finish(color=(0, 0, 0), width=0.5)
    shape2.commit()
    y += 10

    random.seed(fin_idx * 42)
    for item in FINANCIAL_LINE_ITEMS:
        val1 = random.randint(1000, 99999)
        val2 = int(val1 * random.uniform(0.85, 1.15))
        is_negative = "Expense" in item or "Cost" in item or "Tax" in item or "Interest" in item
        prefix1 = "(" if is_negative else "$"
        suffix1 = ")" if is_negative else ""
        prefix2 = "(" if is_negative else "$"
        suffix2 = ")" if is_negative else ""

        page.insert_text(pymupdf.Point(90, y), item, fontsize=9, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(350, y), f"{prefix1}{val1:,}{suffix1}", fontsize=9, fontname="cour", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(440, y), f"{prefix2}{val2:,}{suffix2}", fontsize=9, fontname="cour", color=(0, 0, 0))
        y += 14
        if y > LETTER_H - 60:
            break

    add_bates_stamp(page, page_num, 200)
    return page


def add_contract_page(doc, page_num, contract_idx):
    """Generate an employment contract or vendor agreement page."""
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    y = 72

    person = PEOPLE[contract_idx % len(PEOPLE)]
    page.insert_text(pymupdf.Point(72, y), "EMPLOYMENT AGREEMENT", fontsize=14, fontname="hebo", color=(0, 0, 0))
    y += 25

    page.insert_text(pymupdf.Point(72, y), f"This Employment Agreement (\"Agreement\") is entered into as of", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 16
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    page.insert_text(pymupdf.Point(72, y), f"{months[contract_idx % 12]} {(contract_idx % 28) + 1}, 2023, by and between:", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 25

    page.insert_text(pymupdf.Point(90, y), "Meridian Technologies, Inc. (\"Company\")", fontsize=10, fontname="hebo", color=(0, 0, 0))
    y += 16
    page.insert_text(pymupdf.Point(130, y), "and", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 16
    page.insert_text(pymupdf.Point(90, y), f"{person[0]} (\"Employee\")", fontsize=10, fontname="hebo", color=(0, 0, 0))
    y += 30

    sections = [
        ("1. POSITION AND DUTIES", f"Employee shall serve as {person[1]} and shall perform such duties as are customarily associated with such position, together with such other duties as may be assigned from time to time by the Board of Directors."),
        ("2. COMPENSATION", f"Employee shall receive an annual base salary of ${random.randint(120, 450)},{random.randint(0,9)}00, payable in accordance with the Company's standard payroll practices, subject to applicable withholdings and deductions."),
        ("3. BENEFITS", "Employee shall be entitled to participate in all benefit plans and programs maintained by the Company for similarly situated employees, including health insurance, retirement plans, and paid time off."),
        ("4. CONFIDENTIALITY", "Employee acknowledges that during the course of employment, Employee will have access to and become acquainted with trade secrets, proprietary information, and confidential information belonging to the Company."),
        ("5. NON-COMPETE", "For a period of twelve (12) months following termination of employment, Employee shall not directly or indirectly engage in any business that competes with the Company within the geographic areas in which the Company conducts business."),
    ]

    for heading, body in sections:
        if y > LETTER_H - 100:
            break
        page.insert_text(pymupdf.Point(72, y), heading, fontsize=10, fontname="hebo", color=(0, 0, 0))
        y += 16
        rect = pymupdf.Rect(72, y, LETTER_W - 72, y + 65)
        page.insert_textbox(rect, body, fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 75

    add_bates_stamp(page, page_num, 200)
    return page


def add_memo_page(doc, page_num, memo_idx):
    """Generate internal memorandum page."""
    page = doc.new_page(width=LETTER_W, height=LETTER_H)
    y = 72

    sender = PEOPLE[memo_idx % len(PEOPLE)]
    recipient = PEOPLE[(memo_idx + 5) % len(PEOPLE)]

    page.insert_text(pymupdf.Point(72, y), "MERIDIAN TECHNOLOGIES — INTERNAL MEMORANDUM", fontsize=12, fontname="hebo", color=(0, 0, 0))
    y += 25

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(LETTER_W - 72, y))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()
    y += 18

    fields = [
        ("TO:", f"{recipient[0]}, {recipient[1]}"),
        ("FROM:", f"{sender[0]}, {sender[1]}"),
        ("DATE:", f"{'March' if memo_idx % 2 == 0 else 'August'} {10 + memo_idx}, 2023"),
        ("RE:", f"{'Project Phoenix Update' if memo_idx % 3 == 0 else 'Compliance Review Findings' if memo_idx % 3 == 1 else 'Budget Amendment Request'}"),
        ("CLASSIFICATION:", "CONFIDENTIAL — ATTORNEY-CLIENT PRIVILEGED"),
    ]

    for label, value in fields:
        page.insert_text(pymupdf.Point(72, y), label, fontsize=10, fontname="hebo", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(200, y), value, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 16
    y += 15

    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(72, y), pymupdf.Point(LETTER_W - 72, y))
    shape2.finish(color=(0, 0, 0), width=0.5)
    shape2.commit()
    y += 20

    # Body paragraphs
    for pidx in range(3):
        para = LOREM_LEGAL[(memo_idx + pidx) % len(LOREM_LEGAL)]
        rect = pymupdf.Rect(72, y, LETTER_W - 72, y + 90)
        page.insert_textbox(rect, para, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 100
        if y > LETTER_H - 80:
            break

    add_bates_stamp(page, page_num, 200)
    return page


def create_initial():
    """Create a 200-page discovery production PDF."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    random.seed(2024)
    doc = pymupdf.open()

    # Page 1: Cover page
    add_cover_page(doc)

    # Page 2: Table of Contents / Exhibit Index
    add_toc_page(doc, 2)

    page_num = 3
    target_pages = 200

    # Generate content pages in a rotating pattern
    email_idx = 0
    minutes_idx = 0
    financial_idx = 0
    contract_idx = 0
    memo_idx = 0

    while page_num <= target_pages:
        doc_type = page_num % 5
        if doc_type == 0:
            add_email_page(doc, page_num, email_idx)
            email_idx += 1
        elif doc_type == 1:
            add_minutes_page(doc, page_num, minutes_idx)
            minutes_idx += 1
        elif doc_type == 2:
            add_financial_page(doc, page_num, financial_idx)
            financial_idx += 1
        elif doc_type == 3:
            add_contract_page(doc, page_num, contract_idx)
            contract_idx += 1
        else:
            add_memo_page(doc, page_num, memo_idx)
            memo_idx += 1
        page_num += 1

    # Set metadata
    doc.set_metadata({
        "title": "Meridian Technologies v. Atlas Global Solutions — Production No. 001",
        "author": "Kirkland & Associates LLP",
        "subject": "Discovery Production — Case No. 24-CV-03847-RWS",
        "keywords": "discovery, production, litigation, confidential",
        "creator": "Document Production System",
        "producer": "Meridian Legal Department",
    })

    # Set TOC / bookmarks
    toc = [
        [1, "Cover Page", 1],
        [1, "Exhibit Index", 2],
        [1, "Exhibit A — Email Correspondence", 3],
        [1, "Exhibit B — Board Meeting Minutes", 20],
        [1, "Exhibit C — Financial Statements", 50],
        [1, "Exhibit D — Employment Contracts", 80],
        [1, "Exhibit E — Internal Memoranda", 110],
        [1, "Exhibit F — Audit Reports", 140],
        [1, "Exhibit G — Vendor Agreements", 160],
        [1, "Exhibit H — Patent Applications", 175],
        [1, "Exhibit I — Compliance Reviews", 185],
        [1, "Exhibit J — Strategic Planning Documents", 195],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()

    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 200')
    print(f'No encryption applied (initial state)')

    # Open the PDF in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
