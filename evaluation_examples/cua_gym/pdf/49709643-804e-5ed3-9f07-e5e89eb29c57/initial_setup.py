"""
Initial Setup: Create an unencrypted 4-page NDA template PDF
Task ID: pdf_mbc_009
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_009'
LEGAL_DIR = f'{WORKDIR}/Legal'
OUTPUT = f'{LEGAL_DIR}/nda_template.pdf'


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


def add_page_header_footer(page, page_num, total_pages):
    """Add consistent header and footer to each page."""
    w = page.rect.width
    h = page.rect.height
    # Header line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(50, 55), pymupdf.Point(w - 50, 55))
    shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
    shape.commit()
    # Header text
    page.insert_text(pymupdf.Point(50, 48), "CONFIDENTIAL — NON-DISCLOSURE AGREEMENT",
                     fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
    # Footer
    page.insert_text(pymupdf.Point(50, h - 35),
                     f"Page {page_num} of {total_pages}",
                     fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
    page.insert_text(pymupdf.Point(w - 200, h - 35),
                     "Meridian Technologies Inc.",
                     fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))


def create_initial():
    os.makedirs(LEGAL_DIR, exist_ok=True)

    doc = pymupdf.open()
    W, H = 612, 792  # Letter size

    # ==================== PAGE 1: Cover Page ====================
    page1 = doc.new_page(width=W, height=H)

    # Company logo area (rectangle)
    shape = page1.new_shape()
    shape.draw_rect(pymupdf.Rect(206, 80, 406, 130))
    shape.finish(color=(0.1, 0.2, 0.5), fill=(0.1, 0.2, 0.5), width=1)
    shape.commit()
    page1.insert_text(pymupdf.Point(220, 115), "MERIDIAN TECHNOLOGIES",
                      fontsize=13, fontname="hebo", color=(1, 1, 1))

    # Title
    page1.insert_text(pymupdf.Point(130, 220), "NON-DISCLOSURE AGREEMENT",
                      fontsize=28, fontname="hebo", color=(0.1, 0.2, 0.5))

    # Subtitle line
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(130, 235), pymupdf.Point(482, 235))
    shape.finish(color=(0.7, 0.15, 0.15), width=2)
    shape.commit()

    # Agreement details
    details = [
        ("Agreement Number:", "NDA-2025-MT-00347"),
        ("Effective Date:", "March 15, 2025"),
        ("Disclosing Party:", "Meridian Technologies Inc."),
        ("Receiving Party:", "Orion Analytics Group LLC"),
        ("Classification:", "Strictly Confidential"),
        ("Governing Law:", "State of Delaware, United States"),
    ]
    y = 290
    for label, value in details:
        page1.insert_text(pymupdf.Point(130, y), label,
                          fontsize=11, fontname="hebo", color=(0.2, 0.2, 0.2))
        page1.insert_text(pymupdf.Point(290, y), value,
                          fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))
        y += 24

    # Prepared by
    page1.insert_text(pymupdf.Point(130, 520), "Prepared by:",
                      fontsize=10, fontname="heit", color=(0.4, 0.4, 0.4))
    page1.insert_text(pymupdf.Point(130, 536), "Rebecca Thornton, General Counsel",
                      fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))
    page1.insert_text(pymupdf.Point(130, 552), "Meridian Technologies Inc.",
                      fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))
    page1.insert_text(pymupdf.Point(130, 568), "1200 Innovation Boulevard, Suite 400",
                      fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))
    page1.insert_text(pymupdf.Point(130, 584), "Wilmington, DE 19801",
                      fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))

    add_page_header_footer(page1, 1, 4)

    # ==================== PAGE 2: Definitions & Scope ====================
    page2 = doc.new_page(width=W, height=H)
    add_page_header_footer(page2, 2, 4)

    page2.insert_text(pymupdf.Point(50, 90), "1. DEFINITIONS AND SCOPE",
                      fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))

    sections_p2 = [
        ("1.1 Confidential Information",
         "\"Confidential Information\" shall mean any and all non-public, proprietary, or "
         "trade secret information disclosed by the Disclosing Party to the Receiving Party, "
         "whether orally, in writing, electronically, or by any other means. This includes, "
         "but is not limited to: (a) technical data, research findings, algorithms, source code, "
         "software architecture, and product roadmaps; (b) business strategies, financial "
         "projections, customer lists, pricing models, and marketing plans; (c) employee "
         "information, organizational structures, and internal processes; (d) any third-party "
         "information entrusted to the Disclosing Party under separate confidentiality obligations."),

        ("1.2 Exclusions",
         "Confidential Information shall not include information that: (a) is or becomes publicly "
         "available through no fault of the Receiving Party; (b) was already known to the Receiving "
         "Party prior to disclosure, as evidenced by written records; (c) is independently developed "
         "by the Receiving Party without use of or reference to the Confidential Information; "
         "(d) is disclosed to the Receiving Party by a third party who is not bound by any "
         "obligation of confidentiality; (e) is required to be disclosed by law, regulation, or "
         "court order, provided that the Receiving Party gives prompt written notice to the "
         "Disclosing Party to allow the Disclosing Party to seek a protective order."),

        ("1.3 Scope of Agreement",
         "This Agreement covers all Confidential Information exchanged between the parties in "
         "connection with the proposed joint development project known internally as \"Project "
         "Helios\" — a next-generation data analytics platform for financial services institutions. "
         "The scope includes technical specifications, integration protocols, API documentation, "
         "and all related materials shared during the evaluation and development phases."),
    ]

    y = 120
    for title, body in sections_p2:
        page2.insert_text(pymupdf.Point(50, y), title,
                          fontsize=12, fontname="hebo", color=(0.2, 0.2, 0.2))
        y += 18
        rect = pymupdf.Rect(50, y, W - 50, y + 120)
        excess = page2.insert_textbox(rect, body, fontsize=10, fontname="helv",
                                       color=(0.25, 0.25, 0.25),
                                       align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 130

    # ==================== PAGE 3: Obligations & Terms ====================
    page3 = doc.new_page(width=W, height=H)
    add_page_header_footer(page3, 3, 4)

    page3.insert_text(pymupdf.Point(50, 90), "2. OBLIGATIONS AND TERMS",
                      fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))

    sections_p3 = [
        ("2.1 Non-Disclosure Obligations",
         "The Receiving Party agrees to: (a) hold all Confidential Information in strict "
         "confidence and protect it using the same degree of care it uses to protect its own "
         "confidential information, but in no event less than reasonable care; (b) not disclose "
         "any Confidential Information to any third party without prior written consent of the "
         "Disclosing Party; (c) limit access to Confidential Information to those employees, "
         "contractors, and advisors who have a legitimate need to know and who are bound by "
         "obligations of confidentiality at least as protective as those contained herein."),

        ("2.2 Permitted Use",
         "The Receiving Party may use the Confidential Information solely for the purpose of "
         "evaluating, developing, and implementing the proposed collaboration under Project "
         "Helios. Any other use requires the prior written consent of the Disclosing Party. "
         "The Receiving Party shall not reverse engineer, decompile, or disassemble any "
         "Confidential Information comprising software, prototypes, or technical specifications."),

        ("2.3 Term and Duration",
         "This Agreement shall be effective as of the Effective Date and shall continue for a "
         "period of three (3) years, unless earlier terminated by either party upon thirty (30) "
         "days' written notice. The obligations of confidentiality shall survive termination or "
         "expiration of this Agreement for an additional period of five (5) years from the date "
         "of disclosure of each item of Confidential Information."),

        ("2.4 Return of Materials",
         "Upon termination of this Agreement or upon the Disclosing Party's written request, "
         "the Receiving Party shall promptly return or destroy all Confidential Information, "
         "including all copies, summaries, and derivative works, and shall certify in writing "
         "that it has done so. Notwithstanding the foregoing, the Receiving Party may retain "
         "one archival copy solely for compliance and legal audit purposes."),
    ]

    y = 120
    for title, body in sections_p3:
        page3.insert_text(pymupdf.Point(50, y), title,
                          fontsize=12, fontname="hebo", color=(0.2, 0.2, 0.2))
        y += 18
        rect = pymupdf.Rect(50, y, W - 50, y + 105)
        excess = page3.insert_textbox(rect, body, fontsize=10, fontname="helv",
                                       color=(0.25, 0.25, 0.25),
                                       align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 115

    # ==================== PAGE 4: Signatures ====================
    page4 = doc.new_page(width=W, height=H)
    add_page_header_footer(page4, 4, 4)

    page4.insert_text(pymupdf.Point(50, 90), "3. REMEDIES AND SIGNATURES",
                      fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))

    page4.insert_text(pymupdf.Point(50, 120), "3.1 Remedies",
                      fontsize=12, fontname="hebo", color=(0.2, 0.2, 0.2))
    rect = pymupdf.Rect(50, 138, W - 50, 250)
    page4.insert_textbox(rect, (
        "The parties acknowledge that any breach of this Agreement may cause irreparable "
        "harm to the Disclosing Party for which monetary damages would be an inadequate remedy. "
        "Accordingly, the Disclosing Party shall be entitled to seek injunctive or other equitable "
        "relief in addition to any other remedies available at law or in equity. The prevailing "
        "party in any dispute arising under this Agreement shall be entitled to recover its "
        "reasonable attorneys' fees and costs from the non-prevailing party."
    ), fontsize=10, fontname="helv", color=(0.25, 0.25, 0.25),
       align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page4.insert_text(pymupdf.Point(50, 275), "3.2 General Provisions",
                      fontsize=12, fontname="hebo", color=(0.2, 0.2, 0.2))
    rect = pymupdf.Rect(50, 293, W - 50, 400)
    page4.insert_textbox(rect, (
        "This Agreement constitutes the entire understanding between the parties concerning "
        "the subject matter hereof and supersedes all prior agreements, whether written or oral. "
        "This Agreement may not be amended except in writing signed by both parties. If any "
        "provision of this Agreement is found to be unenforceable, the remaining provisions "
        "shall remain in full force and effect. This Agreement shall be governed by and construed "
        "in accordance with the laws of the State of Delaware."
    ), fontsize=10, fontname="helv", color=(0.25, 0.25, 0.25),
       align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Signature blocks
    page4.insert_text(pymupdf.Point(50, 440),
                      "IN WITNESS WHEREOF, the parties have executed this Agreement as of the Effective Date.",
                      fontsize=10, fontname="hebo", color=(0.2, 0.2, 0.2))

    # Disclosing Party signature block
    page4.insert_text(pymupdf.Point(50, 490), "DISCLOSING PARTY:",
                      fontsize=11, fontname="hebo", color=(0.1, 0.2, 0.5))
    page4.insert_text(pymupdf.Point(50, 510), "Meridian Technologies Inc.",
                      fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

    shape = page4.new_shape()
    shape.draw_line(pymupdf.Point(50, 560), pymupdf.Point(260, 560))
    shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
    shape.commit()
    page4.insert_text(pymupdf.Point(50, 575), "Signature",
                      fontsize=9, fontname="heit", color=(0.5, 0.5, 0.5))
    page4.insert_text(pymupdf.Point(50, 600), "Name: Rebecca Thornton",
                      fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    page4.insert_text(pymupdf.Point(50, 616), "Title: General Counsel",
                      fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    page4.insert_text(pymupdf.Point(50, 632), "Date: _______________",
                      fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

    # Receiving Party signature block
    page4.insert_text(pymupdf.Point(330, 490), "RECEIVING PARTY:",
                      fontsize=11, fontname="hebo", color=(0.1, 0.2, 0.5))
    page4.insert_text(pymupdf.Point(330, 510), "Orion Analytics Group LLC",
                      fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

    shape = page4.new_shape()
    shape.draw_line(pymupdf.Point(330, 560), pymupdf.Point(540, 560))
    shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
    shape.commit()
    page4.insert_text(pymupdf.Point(330, 575), "Signature",
                      fontsize=9, fontname="heit", color=(0.5, 0.5, 0.5))
    page4.insert_text(pymupdf.Point(330, 600), "Name: David Nakamura",
                      fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    page4.insert_text(pymupdf.Point(330, 616), "Title: Chief Technology Officer",
                      fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    page4.insert_text(pymupdf.Point(330, 632), "Date: _______________",
                      fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

    # Set metadata
    doc.set_metadata({
        "title": "Non-Disclosure Agreement — NDA-2025-MT-00347",
        "author": "Rebecca Thornton",
        "subject": "Confidentiality Agreement between Meridian Technologies and Orion Analytics",
        "keywords": "NDA, confidentiality, non-disclosure, Project Helios",
        "creator": "Meridian Technologies Legal Department",
        "producer": "Meridian Technologies Inc.",
    })

    # Set TOC/bookmarks
    toc = [
        [1, "Cover Page", 1],
        [1, "Definitions and Scope", 2],
        [2, "Confidential Information", 2],
        [2, "Exclusions", 2],
        [2, "Scope of Agreement", 2],
        [1, "Obligations and Terms", 3],
        [2, "Non-Disclosure Obligations", 3],
        [2, "Permitted Use", 3],
        [2, "Term and Duration", 3],
        [2, "Return of Materials", 3],
        [1, "Remedies and Signatures", 4],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
