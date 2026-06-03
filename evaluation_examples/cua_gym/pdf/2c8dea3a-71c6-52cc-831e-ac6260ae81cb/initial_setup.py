"""
Initial Setup: Create an unsigned agreement PDF with 2 pages and no signature fields.
Task ID: pdf_gf1_043
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
DOCUMENTS = f'{WORKDIR}/Documents'
TASK_ID = 'pdf_gf1_043'
OUTPUT = f'{DOCUMENTS}/agreement.pdf'


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
    os.makedirs(DOCUMENTS, exist_ok=True)

    doc = pymupdf.open()

    # ---- Page 1: Agreement header, preamble, and first clauses ----
    page1 = doc.new_page(width=612, height=792)  # US Letter

    # Title
    page1.insert_text(
        pymupdf.Point(180, 60),
        "SERVICE AGREEMENT",
        fontsize=22,
        fontname="hebo",
        color=(0, 0, 0),
    )

    # Subtitle / Date
    page1.insert_text(
        pymupdf.Point(200, 85),
        "Effective Date: March 15, 2025",
        fontsize=11,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

    # Horizontal rule
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(72, 100), pymupdf.Point(540, 100))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()

    # Preamble
    preamble = (
        "This Service Agreement (\"Agreement\") is entered into as of March 15, 2025, "
        "by and between Meridian Technology Solutions, Inc., a Delaware corporation with "
        "principal offices at 4500 Innovation Drive, Suite 300, San Jose, CA 95134 "
        "(\"Provider\"), and Cascade Financial Group, LLC, a New York limited liability "
        "company with principal offices at 275 Park Avenue, 18th Floor, New York, NY 10172 "
        "(\"Client\")."
    )
    page1.insert_textbox(
        pymupdf.Rect(72, 120, 540, 220),
        preamble,
        fontsize=10,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Section 1
    page1.insert_text(
        pymupdf.Point(72, 240),
        "1. SCOPE OF SERVICES",
        fontsize=12,
        fontname="hebo",
        color=(0, 0, 0),
    )
    scope_text = (
        "Provider agrees to deliver the following managed IT services to Client: "
        "(a) 24/7 network monitoring and incident response; (b) cloud infrastructure "
        "management across AWS and Azure environments; (c) quarterly security audits "
        "and penetration testing; (d) help desk support with a guaranteed 4-hour "
        "response SLA for critical issues; and (e) monthly performance reporting "
        "with executive summaries."
    )
    page1.insert_textbox(
        pymupdf.Rect(72, 255, 540, 355),
        scope_text,
        fontsize=10,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Section 2
    page1.insert_text(
        pymupdf.Point(72, 370),
        "2. TERM AND RENEWAL",
        fontsize=12,
        fontname="hebo",
        color=(0, 0, 0),
    )
    term_text = (
        "This Agreement shall commence on April 1, 2025 and continue for an initial "
        "term of twenty-four (24) months. Upon expiration, the Agreement shall "
        "automatically renew for successive twelve (12) month periods unless either "
        "party provides written notice of non-renewal at least ninety (90) days prior "
        "to the end of the then-current term."
    )
    page1.insert_textbox(
        pymupdf.Rect(72, 385, 540, 465),
        term_text,
        fontsize=10,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Section 3
    page1.insert_text(
        pymupdf.Point(72, 480),
        "3. COMPENSATION",
        fontsize=12,
        fontname="hebo",
        color=(0, 0, 0),
    )
    comp_text = (
        "Client shall pay Provider a monthly service fee of $18,750.00 (Eighteen Thousand "
        "Seven Hundred Fifty Dollars), due within thirty (30) days of invoice date. "
        "Provider reserves the right to adjust fees annually by no more than 5% upon "
        "sixty (60) days written notice. Late payments shall accrue interest at a rate "
        "of 1.5% per month."
    )
    page1.insert_textbox(
        pymupdf.Rect(72, 495, 540, 585),
        comp_text,
        fontsize=10,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Section 4
    page1.insert_text(
        pymupdf.Point(72, 600),
        "4. CONFIDENTIALITY",
        fontsize=12,
        fontname="hebo",
        color=(0, 0, 0),
    )
    conf_text = (
        "Each party acknowledges that in the course of performing under this Agreement, "
        "it may receive confidential and proprietary information of the other party. "
        "Both parties agree to maintain strict confidentiality of such information and "
        "not to disclose it to any third party without prior written consent, except as "
        "required by law."
    )
    page1.insert_textbox(
        pymupdf.Rect(72, 615, 540, 700),
        conf_text,
        fontsize=10,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Page number
    page1.insert_text(
        pymupdf.Point(290, 770),
        "Page 1 of 2",
        fontsize=9,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    # ---- Page 2: Remaining clauses, signature block ----
    page2 = doc.new_page(width=612, height=792)

    # Section 5
    page2.insert_text(
        pymupdf.Point(72, 60),
        "5. LIABILITY AND INDEMNIFICATION",
        fontsize=12,
        fontname="hebo",
        color=(0, 0, 0),
    )
    liab_text = (
        "Provider's total aggregate liability under this Agreement shall not exceed "
        "the total fees paid by Client during the twelve (12) months preceding the "
        "claim. Neither party shall be liable for indirect, incidental, consequential, "
        "or punitive damages, regardless of the form of action."
    )
    page2.insert_textbox(
        pymupdf.Rect(72, 75, 540, 150),
        liab_text,
        fontsize=10,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Section 6
    page2.insert_text(
        pymupdf.Point(72, 170),
        "6. TERMINATION",
        fontsize=12,
        fontname="hebo",
        color=(0, 0, 0),
    )
    term2_text = (
        "Either party may terminate this Agreement for cause upon thirty (30) days "
        "written notice if the other party materially breaches any provision of this "
        "Agreement and fails to cure such breach within the notice period. Client may "
        "terminate for convenience upon sixty (60) days written notice, subject to "
        "payment of a termination fee equal to three (3) months of service fees."
    )
    page2.insert_textbox(
        pymupdf.Rect(72, 185, 540, 280),
        term2_text,
        fontsize=10,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Section 7
    page2.insert_text(
        pymupdf.Point(72, 300),
        "7. GOVERNING LAW",
        fontsize=12,
        fontname="hebo",
        color=(0, 0, 0),
    )
    gov_text = (
        "This Agreement shall be governed by and construed in accordance with the laws "
        "of the State of New York, without regard to conflict of law principles. Any "
        "disputes arising hereunder shall be subject to the exclusive jurisdiction of "
        "the state and federal courts located in Manhattan, New York."
    )
    page2.insert_textbox(
        pymupdf.Rect(72, 315, 540, 395),
        gov_text,
        fontsize=10,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Section 8 - Entire Agreement
    page2.insert_text(
        pymupdf.Point(72, 415),
        "8. ENTIRE AGREEMENT",
        fontsize=12,
        fontname="hebo",
        color=(0, 0, 0),
    )
    entire_text = (
        "This Agreement constitutes the entire agreement between the parties with respect "
        "to the subject matter hereof and supersedes all prior negotiations, representations, "
        "warranties, commitments, offers, and agreements, whether written or oral."
    )
    page2.insert_textbox(
        pymupdf.Rect(72, 430, 540, 500),
        entire_text,
        fontsize=10,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Signature block heading
    page2.insert_text(
        pymupdf.Point(72, 530),
        "IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.",
        fontsize=10,
        fontname="tibo",
        color=(0, 0, 0),
    )

    # Provider signature block
    page2.insert_text(pymupdf.Point(72, 570), "PROVIDER:", fontsize=10, fontname="hebo")
    page2.insert_text(pymupdf.Point(72, 590), "Meridian Technology Solutions, Inc.", fontsize=10, fontname="tiro")
    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, 630), pymupdf.Point(280, 630))
    shape2.finish(color=(0, 0, 0), width=0.5)
    shape2.commit()
    page2.insert_text(pymupdf.Point(72, 645), "Name: _________________________", fontsize=10, fontname="tiro")
    page2.insert_text(pymupdf.Point(72, 665), "Title: _________________________", fontsize=10, fontname="tiro")
    page2.insert_text(pymupdf.Point(72, 685), "Date: _________________________", fontsize=10, fontname="tiro")

    # Client signature block
    page2.insert_text(pymupdf.Point(350, 570), "CLIENT:", fontsize=10, fontname="hebo")
    page2.insert_text(pymupdf.Point(350, 590), "Cascade Financial Group, LLC", fontsize=10, fontname="tiro")
    shape3 = page2.new_shape()
    shape3.draw_line(pymupdf.Point(350, 630), pymupdf.Point(540, 630))
    shape3.finish(color=(0, 0, 0), width=0.5)
    shape3.commit()
    page2.insert_text(pymupdf.Point(350, 645), "Name: _________________________", fontsize=10, fontname="tiro")
    page2.insert_text(pymupdf.Point(350, 665), "Title: _________________________", fontsize=10, fontname="tiro")
    page2.insert_text(pymupdf.Point(350, 685), "Date: _________________________", fontsize=10, fontname="tiro")

    # Page number
    page2.insert_text(
        pymupdf.Point(290, 770),
        "Page 2 of 2",
        fontsize=9,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for the agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
