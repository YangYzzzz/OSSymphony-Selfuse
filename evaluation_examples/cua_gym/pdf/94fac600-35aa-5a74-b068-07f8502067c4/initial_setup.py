"""
Initial Setup: Create a legal settlement agreement PDF with extensive metadata
Task ID: pdf_mbc_020
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_020'
LEGAL_DIR = f'{WORKDIR}/Legal'
OUTPUT = f'{LEGAL_DIR}/settlement_agreement.pdf'


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
    os.makedirs(LEGAL_DIR, exist_ok=True)

    doc = pymupdf.open()

    # ── Page 1: Title Page ──
    page1 = doc.new_page(width=612, height=792)  # Letter size
    page1.insert_text(
        pymupdf.Point(72, 120),
        "SETTLEMENT AGREEMENT AND MUTUAL RELEASE",
        fontsize=18,
        fontname="hebo",
        color=(0, 0, 0),
    )
    page1.insert_text(
        pymupdf.Point(72, 160),
        "Case No. 2024-CV-08173",
        fontsize=14,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
    )

    # Draw a horizontal line
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(72, 180), pymupdf.Point(540, 180))
    shape.finish(color=(0, 0, 0), width=1.5)
    shape.commit()

    page1.insert_text(
        pymupdf.Point(72, 220),
        "Between:",
        fontsize=12,
        fontname="hebo",
        color=(0, 0, 0),
    )

    parties_text = (
        "GREENLEAF TECHNOLOGIES, INC., a Delaware corporation, with its principal "
        "place of business at 4500 Innovation Drive, Suite 800, San Jose, CA 95134 "
        '(hereinafter referred to as "Plaintiff" or "Greenleaf"),\n\n'
        "and\n\n"
        "APEX DIGITAL SOLUTIONS, LLC, a California limited liability company, with "
        "its principal place of business at 1200 Market Street, Floor 15, "
        'San Francisco, CA 94103 (hereinafter referred to as "Defendant" or "Apex").'
    )
    rect1 = pymupdf.Rect(72, 240, 540, 450)
    page1.insert_textbox(rect1, parties_text, fontsize=11, fontname="helv",
                         color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page1.insert_text(
        pymupdf.Point(72, 480),
        "Effective Date: March 15, 2025",
        fontsize=11,
        fontname="tiit",
        color=(0.3, 0.3, 0.3),
    )
    page1.insert_text(
        pymupdf.Point(72, 510),
        "Filed Under Seal — Confidential",
        fontsize=11,
        fontname="hebo",
        color=(0.6, 0, 0),
    )

    # ── Page 2: Recitals and Section 1 ──
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(pymupdf.Point(72, 72), "RECITALS", fontsize=14,
                      fontname="hebo", color=(0, 0, 0))

    recitals = (
        "WHEREAS, Greenleaf Technologies, Inc. filed a complaint against Apex "
        "Digital Solutions, LLC in the Superior Court of California, County of "
        "Santa Clara, on August 12, 2024, alleging trade secret misappropriation, "
        "breach of non-disclosure agreement, and unfair business practices "
        "(collectively, the \"Litigation\");\n\n"
        "WHEREAS, Apex has denied all allegations and asserts that its products "
        "were developed independently through its own research and development "
        "efforts;\n\n"
        "WHEREAS, both parties desire to resolve the Litigation and all related "
        "disputes without further expense, delay, and uncertainty of continued "
        "litigation;\n\n"
        "NOW, THEREFORE, in consideration of the mutual covenants, promises, and "
        "agreements set forth herein, and for other good and valuable consideration, "
        "the receipt and sufficiency of which are hereby acknowledged, the Parties "
        "agree as follows:"
    )
    rect2 = pymupdf.Rect(72, 100, 540, 380)
    page2.insert_textbox(rect2, recitals, fontsize=11, fontname="helv",
                         color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page2.insert_text(pymupdf.Point(72, 400), "SECTION 1: DEFINITIONS",
                      fontsize=13, fontname="hebo", color=(0, 0, 0))

    definitions = (
        '1.1 "Confidential Information" means any trade secrets, proprietary data, '
        "financial records, customer lists, business strategies, source code, "
        "algorithms, or other non-public information disclosed by either Party.\n\n"
        '1.2 "Settlement Amount" means the total sum of Two Million Seven Hundred '
        "Fifty Thousand Dollars ($2,750,000.00), payable as described in Section 3.\n\n"
        '1.3 "Released Claims" means any and all claims, demands, actions, causes '
        "of action, suits, debts, obligations, damages, losses, costs, expenses, "
        "and liabilities of any kind."
    )
    rect3 = pymupdf.Rect(72, 425, 540, 700)
    page2.insert_textbox(rect3, definitions, fontsize=11, fontname="helv",
                         color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ── Page 3: Sections 2-3 ──
    page3 = doc.new_page(width=612, height=792)
    page3.insert_text(pymupdf.Point(72, 72), "SECTION 2: MUTUAL RELEASE",
                      fontsize=13, fontname="hebo", color=(0, 0, 0))

    release_text = (
        "2.1 Release by Greenleaf. Greenleaf hereby releases and forever "
        "discharges Apex, its officers, directors, employees, agents, successors, "
        "and assigns from any and all Released Claims arising from or related to "
        "the Litigation.\n\n"
        "2.2 Release by Apex. Apex hereby releases and forever discharges "
        "Greenleaf, its officers, directors, employees, agents, successors, and "
        "assigns from any and all Released Claims arising from or related to "
        "the Litigation, including any counterclaims or cross-claims.\n\n"
        "2.3 Unknown Claims. Each Party expressly waives any rights under "
        "California Civil Code Section 1542, which provides: \"A general release "
        "does not extend to claims that the creditor or releasing party does not "
        "know or suspect to exist.\""
    )
    rect4 = pymupdf.Rect(72, 97, 540, 360)
    page3.insert_textbox(rect4, release_text, fontsize=11, fontname="helv",
                         color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page3.insert_text(pymupdf.Point(72, 380), "SECTION 3: PAYMENT TERMS",
                      fontsize=13, fontname="hebo", color=(0, 0, 0))

    payment_text = (
        "3.1 Settlement Payment. Apex shall pay to Greenleaf the Settlement "
        "Amount of $2,750,000.00 according to the following schedule:\n\n"
        "  (a) First installment of $1,000,000.00 within thirty (30) days;\n"
        "  (b) Second installment of $875,000.00 within ninety (90) days;\n"
        "  (c) Third installment of $875,000.00 within one hundred eighty (180) days.\n\n"
        "3.2 Wire Transfer. All payments shall be made by wire transfer to "
        "the account designated by Greenleaf's counsel.\n\n"
        "3.3 Late Payment. Any payment not received within five (5) business "
        "days of the due date shall accrue interest at a rate of 1.5% per month."
    )
    rect5 = pymupdf.Rect(72, 405, 540, 700)
    page3.insert_textbox(rect5, payment_text, fontsize=11, fontname="helv",
                         color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ── Page 4: Sections 4-5 and Signatures ──
    page4 = doc.new_page(width=612, height=792)
    page4.insert_text(pymupdf.Point(72, 72), "SECTION 4: CONFIDENTIALITY",
                      fontsize=13, fontname="hebo", color=(0, 0, 0))

    conf_text = (
        "4.1 Confidentiality of Agreement. The Parties agree that the terms "
        "and conditions of this Agreement, including the Settlement Amount, shall "
        "remain strictly confidential and shall not be disclosed to any third "
        "party except as required by law.\n\n"
        "4.2 Non-Disparagement. Neither Party shall make any public statements "
        "or communications that are intended to disparage, defame, or damage the "
        "reputation of the other Party."
    )
    rect6 = pymupdf.Rect(72, 97, 540, 280)
    page4.insert_textbox(rect6, conf_text, fontsize=11, fontname="helv",
                         color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page4.insert_text(pymupdf.Point(72, 300), "SECTION 5: GOVERNING LAW",
                      fontsize=13, fontname="hebo", color=(0, 0, 0))

    gov_text = (
        "5.1 This Agreement shall be governed by and construed in accordance "
        "with the laws of the State of California, without regard to conflicts "
        "of law principles.\n\n"
        "5.2 Any disputes arising under this Agreement shall be resolved through "
        "binding arbitration in Santa Clara County, California, under the rules "
        "of the American Arbitration Association."
    )
    rect7 = pymupdf.Rect(72, 325, 540, 470)
    page4.insert_textbox(rect7, gov_text, fontsize=11, fontname="helv",
                         color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Signature block
    page4.insert_text(pymupdf.Point(72, 510), "IN WITNESS WHEREOF,",
                      fontsize=12, fontname="hebo", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(72, 535),
                      "the Parties have executed this Agreement as of the date first written above.",
                      fontsize=11, fontname="helv", color=(0, 0, 0))

    # Signature lines
    shape4 = page4.new_shape()
    shape4.draw_line(pymupdf.Point(72, 600), pymupdf.Point(280, 600))
    shape4.finish(color=(0, 0, 0), width=0.75)
    shape4.draw_line(pymupdf.Point(332, 600), pymupdf.Point(540, 600))
    shape4.finish(color=(0, 0, 0), width=0.75)
    shape4.commit()

    page4.insert_text(pymupdf.Point(72, 615), "For Greenleaf Technologies, Inc.",
                      fontsize=10, fontname="helv", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(72, 630), "Robert A. Harrington, CEO",
                      fontsize=10, fontname="tiit", color=(0.3, 0.3, 0.3))

    page4.insert_text(pymupdf.Point(332, 615), "For Apex Digital Solutions, LLC",
                      fontsize=10, fontname="helv", color=(0, 0, 0))
    page4.insert_text(pymupdf.Point(332, 630), "Diana L. Castellano, Managing Partner",
                      fontsize=10, fontname="tiit", color=(0.3, 0.3, 0.3))

    # ── Set extensive metadata ──
    doc.set_metadata({
        "title": "Settlement Agreement - Greenleaf v. Apex",
        "author": "Harrington & Associates LLP",
        "subject": "Confidential Settlement Agreement and Mutual Release - Case No. 2024-CV-08173",
        "keywords": "settlement, litigation, trade secret, NDA, confidential, mutual release, Greenleaf, Apex",
        "creator": "Adobe Acrobat Pro DC 2024.001",
        "producer": "Adobe PDF Library 15.0",
        "creationDate": "D:20250315143022-07'00'",
        "modDate": "D:20250320091544-07'00'",
    })

    doc.save(OUTPUT)
    doc.close()

    # Now add XMP metadata using pikepdf for richer metadata
    import pikepdf
    pdf = pikepdf.open(OUTPUT, allow_overwriting_input=True)
    with pdf.open_metadata() as meta:
        meta["dc:title"] = "Settlement Agreement - Greenleaf v. Apex"
        meta["dc:creator"] = ["Harrington & Associates LLP"]
        meta["dc:description"] = "Confidential Settlement Agreement and Mutual Release between Greenleaf Technologies Inc. and Apex Digital Solutions LLC"
        meta["dc:subject"] = ["settlement", "litigation", "trade secret", "NDA", "confidential"]
        meta["xmp:CreatorTool"] = "Adobe Acrobat Pro DC 2024.001"
        meta["xmp:CreateDate"] = "2025-03-15T14:30:22-07:00"
        meta["xmp:ModifyDate"] = "2025-03-20T09:15:44-07:00"
        meta["pdf:Producer"] = "Adobe PDF Library 15.0"
        meta["pdf:Keywords"] = "settlement, litigation, trade secret, NDA, confidential, mutual release"
        meta["xmpMM:DocumentID"] = "uuid:a3f8c2d1-4e6b-4a9f-b3c7-9d2e1f5a8b4c"
        meta["xmpMM:InstanceID"] = "uuid:e7b2a1c5-3d8f-4f2e-a6d9-1c4b7e3f5a2d"
    pdf.save(OUTPUT)
    pdf.close()

    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
