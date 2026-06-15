"""
Initial Setup: Create a 3-page financial audit certificate PDF
Task ID: pdf_fin_089
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
TASK_ID = 'pdf_fin_089'
FINANCE_DIR = f'{WORKDIR}/finance'
OUTPUT = f'{FINANCE_DIR}/audit_certificate.pdf'


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
    os.makedirs(FINANCE_DIR, exist_ok=True)

    doc = pymupdf.open()

    # --- Page 1: Cover / Certificate Title ---
    page1 = doc.new_page(width=612, height=792)  # Letter size
    # Title
    page1.insert_text(
        pymupdf.Point(180, 120),
        "INDEPENDENT AUDITOR'S",
        fontsize=22,
        fontname="hebo",
        color=(0.05, 0.1, 0.3),
    )
    page1.insert_text(
        pymupdf.Point(220, 155),
        "CERTIFICATE",
        fontsize=22,
        fontname="hebo",
        color=(0.05, 0.1, 0.3),
    )

    # Firm name
    page1.insert_text(
        pymupdf.Point(170, 220),
        "Meridian & Whitfield LLP",
        fontsize=16,
        fontname="tibo",
        color=(0.2, 0.2, 0.2),
    )
    page1.insert_text(
        pymupdf.Point(180, 245),
        "Certified Public Accountants",
        fontsize=12,
        fontname="tiit",
        color=(0.3, 0.3, 0.3),
    )

    # Decorative line
    shape1 = page1.new_shape()
    shape1.draw_line(pymupdf.Point(150, 270), pymupdf.Point(462, 270))
    shape1.finish(color=(0.05, 0.1, 0.3), width=1.5)
    shape1.commit()

    # Certificate body
    body_text = (
        "We have audited the accompanying consolidated financial statements of "
        "Evergreen Capital Holdings, Inc. and its subsidiaries (the \"Company\"), "
        "which comprise the consolidated balance sheet as of December 31, 2025, "
        "and the related consolidated statements of comprehensive income, "
        "stockholders' equity, and cash flows for the fiscal year then ended, "
        "and the related notes to the consolidated financial statements.\n\n"
        "In our opinion, the consolidated financial statements referred to above "
        "present fairly, in all material respects, the financial position of "
        "Evergreen Capital Holdings, Inc. as of December 31, 2025, and the results "
        "of its operations and its cash flows for the year then ended, in conformity "
        "with accounting principles generally accepted in the United States of America."
    )
    page1.insert_textbox(
        pymupdf.Rect(72, 310, 540, 560),
        body_text,
        fontsize=11,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Signature block
    page1.insert_text(pymupdf.Point(72, 620), "Date: March 15, 2026", fontsize=11, fontname="tiro", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 650), "________________________", fontsize=11, fontname="tiro", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 670), "Robert J. Whitfield, CPA", fontsize=11, fontname="tibo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 690), "Managing Partner", fontsize=10, fontname="tiit", color=(0.3, 0.3, 0.3))
    page1.insert_text(pymupdf.Point(72, 710), "Meridian & Whitfield LLP", fontsize=10, fontname="tiro", color=(0.3, 0.3, 0.3))
    page1.insert_text(pymupdf.Point(72, 730), "New York, NY", fontsize=10, fontname="tiro", color=(0.3, 0.3, 0.3))

    # --- Page 2: Basis for Opinion ---
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(
        pymupdf.Point(72, 72),
        "Basis for Opinion",
        fontsize=16,
        fontname="hebo",
        color=(0.05, 0.1, 0.3),
    )

    basis_text = (
        "We conducted our audit in accordance with auditing standards generally accepted "
        "in the United States of America (GAAS) and in accordance with the standards of the "
        "Public Company Accounting Oversight Board (PCAOB). Our responsibilities under those "
        "standards are further described in the Auditor's Responsibilities for the Audit of "
        "the Financial Statements section of our report.\n\n"
        "We are required to be independent of Evergreen Capital Holdings, Inc. and to meet "
        "our other ethical responsibilities in accordance with the relevant ethical requirements "
        "relating to our audit. We believe that the audit evidence we have obtained is sufficient "
        "and appropriate to provide a basis for our audit opinion.\n\n"
        "Key Audit Matters\n\n"
        "Key audit matters are those matters that, in our professional judgment, were of most "
        "significance in our audit of the financial statements of the current period. These "
        "matters were addressed in the context of our audit of the financial statements as a "
        "whole, and in forming our opinion thereon.\n\n"
        "1. Revenue Recognition (ASC 606)\n"
        "   The Company recognized $2.87 billion in consolidated revenue for the fiscal year "
        "ended December 31, 2025. Due to the complexity of customer arrangements and the "
        "significance of management estimates in determining the timing and amount of revenue, "
        "we identified revenue recognition as a key audit matter.\n\n"
        "2. Goodwill Impairment Assessment\n"
        "   As of December 31, 2025, the Company reported $1.42 billion in goodwill across "
        "four reporting units. We evaluated the methodologies, assumptions, and data used by "
        "management in performing the annual impairment test."
    )
    page2.insert_textbox(
        pymupdf.Rect(72, 100, 540, 720),
        basis_text,
        fontsize=11,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page number
    page2.insert_text(pymupdf.Point(290, 760), "2", fontsize=10, fontname="tiro", color=(0.5, 0.5, 0.5))

    # --- Page 3: Responsibilities ---
    page3 = doc.new_page(width=612, height=792)
    page3.insert_text(
        pymupdf.Point(72, 72),
        "Responsibilities of Management and Auditors",
        fontsize=16,
        fontname="hebo",
        color=(0.05, 0.1, 0.3),
    )

    responsibilities_text = (
        "Management's Responsibilities\n\n"
        "Management is responsible for the preparation and fair presentation of the "
        "consolidated financial statements in accordance with accounting principles generally "
        "accepted in the United States of America, and for the design, implementation, and "
        "maintenance of internal control relevant to the preparation and fair presentation of "
        "consolidated financial statements that are free from material misstatement, whether "
        "due to fraud or error.\n\n"
        "In preparing the consolidated financial statements, management is required to evaluate "
        "whether there are conditions or events, considered in the aggregate, that raise "
        "substantial doubt about the Company's ability to continue as a going concern for one "
        "year after the date the financial statements are available to be issued.\n\n"
        "Auditor's Responsibilities\n\n"
        "Our objectives are to obtain reasonable assurance about whether the consolidated "
        "financial statements as a whole are free from material misstatement, whether due to "
        "fraud or error, and to issue an auditor's report that includes our opinion. Reasonable "
        "assurance is a high level of assurance but is not absolute assurance and therefore is "
        "not a guarantee that an audit conducted in accordance with GAAS and PCAOB standards "
        "will always detect a material misstatement when it exists.\n\n"
        "The risk of not detecting a material misstatement resulting from fraud is higher than "
        "for one resulting from error, as fraud may involve collusion, forgery, intentional "
        "omissions, misrepresentations, or the override of internal control.\n\n"
        "This certificate has been issued in compliance with all applicable regulatory requirements."
    )
    page3.insert_textbox(
        pymupdf.Rect(72, 100, 540, 700),
        responsibilities_text,
        fontsize=11,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page number
    page3.insert_text(pymupdf.Point(290, 760), "3", fontsize=10, fontname="tiro", color=(0.5, 0.5, 0.5))

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready: open the PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
