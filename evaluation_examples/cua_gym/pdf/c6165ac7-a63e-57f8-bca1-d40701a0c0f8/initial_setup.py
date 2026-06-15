"""
Initial Setup: Create a 3-page retainer agreement PDF with no form fields.
Task ID: pdf_legal_020
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_020'
LEGAL_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{LEGAL_DIR}/retainer_agreement.pdf'

# Page dimensions (Letter size)
W, H = 612, 792


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

    # ---- PAGE 1: Title and Introduction ----
    page1 = doc.new_page(width=W, height=H)

    # Header
    page1.insert_text(pymupdf.Point(200, 60), "LEGAL RETAINER AGREEMENT",
                      fontsize=16, fontname="hebo", color=(0, 0, 0))

    page1.insert_text(pymupdf.Point(72, 100), "Agreement Number: RA-2025-0473",
                      fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

    page1.insert_text(pymupdf.Point(72, 115), "Effective Date: March 15, 2025",
                      fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

    # Horizontal rule
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(72, 130), pymupdf.Point(540, 130))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()

    # Parties section
    page1.insert_text(pymupdf.Point(72, 160), "PARTIES", fontsize=13, fontname="hebo")

    parties_text = (
        "This Retainer Agreement (\"Agreement\") is entered into as of March 15, 2025, "
        "by and between:\n\n"
        "CLIENT: Westbrook Holdings, LLC, a Delaware limited liability company, with its "
        "principal office located at 1450 Market Street, Suite 2200, San Francisco, CA 94102 "
        "(hereinafter referred to as \"Client\");\n\n"
        "and\n\n"
        "ATTORNEY: Harrison & Clarke LLP, a California limited liability partnership, with "
        "offices at 555 Montgomery Street, Suite 1800, San Francisco, CA 94111 "
        "(hereinafter referred to as \"Firm\" or \"Attorney\")."
    )
    page1.insert_textbox(pymupdf.Rect(72, 180, 540, 370), parties_text,
                         fontsize=11, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Recitals section
    page1.insert_text(pymupdf.Point(72, 390), "RECITALS", fontsize=13, fontname="hebo")

    recitals_text = (
        "WHEREAS, Client desires to retain the services of Attorney for legal representation "
        "and counsel in connection with general corporate matters, mergers and acquisitions "
        "advisory, and regulatory compliance;\n\n"
        "WHEREAS, Attorney is willing to provide such legal services upon the terms and "
        "conditions set forth herein;\n\n"
        "NOW, THEREFORE, in consideration of the mutual covenants and agreements contained "
        "herein, and for other good and valuable consideration, the receipt and sufficiency "
        "of which are hereby acknowledged, the parties agree as follows:"
    )
    page1.insert_textbox(pymupdf.Rect(72, 410, 540, 580), recitals_text,
                         fontsize=11, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Section 1: Scope of Services
    page1.insert_text(pymupdf.Point(72, 600), "1. SCOPE OF SERVICES", fontsize=12, fontname="hebo")

    scope_text = (
        "Attorney agrees to provide the following legal services to Client:\n\n"
        "  (a) General corporate counseling, including entity formation, governance, "
        "and compliance matters;\n"
        "  (b) Review, drafting, and negotiation of commercial contracts, including but not "
        "limited to vendor agreements, licensing arrangements, and partnership agreements;\n"
        "  (c) Mergers and acquisitions due diligence, structuring, and transaction support;\n"
        "  (d) Regulatory compliance review and filings with applicable federal and state agencies."
    )
    page1.insert_textbox(pymupdf.Rect(72, 618, 540, 770), scope_text,
                         fontsize=11, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- PAGE 2: Terms and Conditions ----
    page2 = doc.new_page(width=W, height=H)

    page2.insert_text(pymupdf.Point(72, 60), "2. RETAINER FEE AND BILLING", fontsize=12, fontname="hebo")

    fee_text = (
        "  (a) Client shall pay Attorney a monthly retainer fee of $12,500 (Twelve Thousand "
        "Five Hundred Dollars), due on the first business day of each calendar month.\n\n"
        "  (b) The retainer fee shall cover up to forty (40) hours of legal services per month. "
        "Any hours exceeding the monthly allotment shall be billed at the rate of $475 per hour "
        "for partners and $325 per hour for associates.\n\n"
        "  (c) Attorney shall submit detailed monthly invoices itemizing all services rendered, "
        "time expended, and any disbursements incurred. Payment of invoices is due within "
        "thirty (30) days of receipt.\n\n"
        "  (d) All out-of-pocket expenses, including filing fees, courier charges, travel "
        "expenses, and expert consultant fees, shall be billed separately and are not included "
        "in the retainer fee."
    )
    page2.insert_textbox(pymupdf.Rect(72, 78, 540, 290), fee_text,
                         fontsize=11, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page2.insert_text(pymupdf.Point(72, 310), "3. TERM AND TERMINATION", fontsize=12, fontname="hebo")

    term_text = (
        "  (a) This Agreement shall commence on the Effective Date and continue for an initial "
        "term of twelve (12) months, unless earlier terminated in accordance with this section.\n\n"
        "  (b) Either party may terminate this Agreement upon sixty (60) days' written notice "
        "to the other party. In the event of termination, Client shall be responsible for payment "
        "of all fees and expenses incurred through the effective date of termination.\n\n"
        "  (c) Attorney may withdraw from representation if Client fails to pay fees when due, "
        "if continued representation would result in a violation of professional conduct rules, "
        "or for other good cause as permitted by applicable law."
    )
    page2.insert_textbox(pymupdf.Rect(72, 328, 540, 510), term_text,
                         fontsize=11, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page2.insert_text(pymupdf.Point(72, 530), "4. CONFIDENTIALITY", fontsize=12, fontname="hebo")

    conf_text = (
        "  (a) Attorney shall maintain in strict confidence all information, documents, and "
        "communications provided by Client in connection with this engagement, subject to the "
        "attorney-client privilege and applicable rules of professional conduct.\n\n"
        "  (b) This obligation of confidentiality shall survive the termination of this Agreement "
        "and shall continue indefinitely."
    )
    page2.insert_textbox(pymupdf.Rect(72, 548, 540, 680), conf_text,
                         fontsize=11, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page2.insert_text(pymupdf.Point(72, 700), "5. GOVERNING LAW AND DISPUTE RESOLUTION", fontsize=12, fontname="hebo")

    gov_text = (
        "This Agreement shall be governed by and construed in accordance with the laws of the "
        "State of California. Any disputes arising out of or related to this Agreement shall be "
        "resolved through binding arbitration administered by JAMS in San Francisco, California."
    )
    page2.insert_textbox(pymupdf.Rect(72, 718, 540, 775), gov_text,
                         fontsize=11, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ---- PAGE 3: Signatures ----
    page3 = doc.new_page(width=W, height=H)

    page3.insert_text(pymupdf.Point(72, 60), "6. ENTIRE AGREEMENT", fontsize=12, fontname="hebo")

    entire_text = (
        "This Agreement constitutes the entire agreement between the parties with respect to "
        "the subject matter hereof and supersedes all prior negotiations, representations, "
        "warranties, commitments, offers, contracts, and writings, whether written or oral, "
        "with respect to such subject matter. No amendment or modification of this Agreement "
        "shall be effective unless made in writing and signed by both parties."
    )
    page3.insert_textbox(pymupdf.Rect(72, 78, 540, 200), entire_text,
                         fontsize=11, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page3.insert_text(pymupdf.Point(72, 220), "7. NOTICES", fontsize=12, fontname="hebo")

    notices_text = (
        "All notices required or permitted under this Agreement shall be in writing and shall "
        "be deemed given when delivered personally, sent by certified mail (return receipt "
        "requested), or sent by overnight courier to the addresses set forth above or to such "
        "other address as either party may designate in writing."
    )
    page3.insert_textbox(pymupdf.Rect(72, 238, 540, 340), notices_text,
                         fontsize=11, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page3.insert_text(pymupdf.Point(72, 360), "8. SEVERABILITY", fontsize=12, fontname="hebo")

    sev_text = (
        "If any provision of this Agreement is held to be invalid, illegal, or unenforceable, "
        "the remaining provisions shall continue in full force and effect."
    )
    page3.insert_textbox(pymupdf.Rect(72, 378, 540, 440), sev_text,
                         fontsize=11, fontname="helv", color=(0, 0, 0),
                         align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Signature block header
    page3.insert_text(pymupdf.Point(72, 470),
                      "IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.",
                      fontsize=11, fontname="helv")

    # Signature lines and labels
    page3.insert_text(pymupdf.Point(72, 530), "CLIENT:", fontsize=11, fontname="hebo")
    page3.insert_text(pymupdf.Point(72, 550), "Westbrook Holdings, LLC", fontsize=10, fontname="helv")
    page3.insert_text(pymupdf.Point(72, 570), "By: _______________________________", fontsize=10, fontname="helv")
    page3.insert_text(pymupdf.Point(72, 585), "Name: David R. Westbrook", fontsize=10, fontname="helv")
    page3.insert_text(pymupdf.Point(72, 598), "Title: Managing Member", fontsize=10, fontname="helv")

    page3.insert_text(pymupdf.Point(350, 530), "ATTORNEY:", fontsize=11, fontname="hebo")
    page3.insert_text(pymupdf.Point(350, 550), "Harrison & Clarke LLP", fontsize=10, fontname="helv")
    page3.insert_text(pymupdf.Point(350, 570), "By: _______________________________", fontsize=10, fontname="helv")
    page3.insert_text(pymupdf.Point(350, 585), "Name: Elizabeth A. Harrison", fontsize=10, fontname="helv")
    page3.insert_text(pymupdf.Point(350, 598), "Title: Managing Partner", fontsize=10, fontname="helv")

    # Date lines
    page3.insert_text(pymupdf.Point(72, 680), "Date: _______________________________", fontsize=10, fontname="helv")
    page3.insert_text(pymupdf.Point(350, 680), "Date: _______________________________", fontsize=10, fontname="helv")

    # Footer
    shape3 = page3.new_shape()
    shape3.draw_line(pymupdf.Point(72, 740), pymupdf.Point(540, 740))
    shape3.finish(color=(0.5, 0.5, 0.5), width=0.5)
    shape3.commit()

    page3.insert_text(pymupdf.Point(200, 755),
                      "Retainer Agreement - RA-2025-0473 - Page 3 of 3",
                      fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
