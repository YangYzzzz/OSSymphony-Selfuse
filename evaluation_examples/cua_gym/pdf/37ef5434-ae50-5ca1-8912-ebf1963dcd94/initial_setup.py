"""
Initial Setup: Create a 6-page NDA draft PDF with no watermarks
Task ID: pdf_gf2_004
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_004'
LEGAL_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{LEGAL_DIR}/nda_draft.pdf'


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
    import pymupdf

    os.makedirs(LEGAL_DIR, exist_ok=True)

    doc = pymupdf.open()
    W, H = 612, 792  # Letter size in points

    # --- NDA content for 6 pages ---

    # Page 1: Title page
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(200, 120), "NON-DISCLOSURE AGREEMENT", fontsize=18, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 200), "Agreement Number: NDA-2025-0472", fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 230), "Effective Date: March 15, 2025", fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_textbox(
        pymupdf.Rect(72, 280, 540, 450),
        "This Non-Disclosure Agreement (the \"Agreement\") is entered into as of the Effective Date "
        "by and between Meridian Technologies, Inc., a Delaware corporation with its principal offices "
        "at 1450 Innovation Drive, Suite 300, San Jose, CA 95134 (\"Disclosing Party\"), and Clearwater "
        "Analytics Group, LLC, a California limited liability company with its principal offices at "
        "2800 Pacific Avenue, Suite 1200, Los Angeles, CA 90071 (\"Receiving Party\").\n\n"
        "WHEREAS, the Disclosing Party possesses certain confidential and proprietary information "
        "relating to its business operations, technology, products, and strategic plans; and\n\n"
        "WHEREAS, the Receiving Party desires to receive certain confidential information for the "
        "purpose of evaluating a potential business relationship between the parties;",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )
    page.insert_text(pymupdf.Point(72, 480), "NOW, THEREFORE, in consideration of the mutual covenants herein, the parties agree as follows:",
                     fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(250, 750), "Page 1 of 6", fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # Page 2: Definitions
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "1. DEFINITIONS", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page.insert_textbox(
        pymupdf.Rect(72, 100, 540, 700),
        "1.1 \"Confidential Information\" means any and all non-public information, whether in oral, "
        "written, electronic, or visual form, disclosed by the Disclosing Party to the Receiving Party, "
        "including but not limited to:\n\n"
        "(a) Trade secrets, inventions, patent applications, and technology roadmaps;\n\n"
        "(b) Business strategies, financial projections, revenue models, and customer acquisition data;\n\n"
        "(c) Product specifications, engineering designs, source code, algorithms, and technical architectures;\n\n"
        "(d) Customer lists, vendor agreements, pricing structures, and partnership terms;\n\n"
        "(e) Marketing plans, competitive analyses, and market research findings;\n\n"
        "(f) Employee compensation data, organizational structures, and hiring plans.\n\n"
        "1.2 \"Authorized Representatives\" means those employees, officers, directors, agents, or "
        "professional advisors of the Receiving Party who (a) have a need to know the Confidential "
        "Information for the Purpose, and (b) have been informed of and agreed to be bound by "
        "confidentiality obligations no less restrictive than those in this Agreement.\n\n"
        "1.3 \"Purpose\" means the evaluation, negotiation, and potential consummation of a strategic "
        "partnership between the parties relating to cloud infrastructure optimization and enterprise "
        "data analytics services.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )
    page.insert_text(pymupdf.Point(250, 750), "Page 2 of 6", fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # Page 3: Obligations
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "2. OBLIGATIONS OF RECEIVING PARTY", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page.insert_textbox(
        pymupdf.Rect(72, 100, 540, 700),
        "2.1 The Receiving Party shall hold all Confidential Information in strict confidence and shall "
        "not disclose any Confidential Information to any third party without the prior written consent "
        "of the Disclosing Party.\n\n"
        "2.2 The Receiving Party shall protect the Confidential Information using the same degree of care "
        "it uses to protect its own confidential information, but in no event less than a reasonable "
        "degree of care.\n\n"
        "2.3 The Receiving Party shall use the Confidential Information solely for the Purpose and shall "
        "not use the Confidential Information for any other purpose, including but not limited to "
        "competitive analysis, reverse engineering, or development of competing products.\n\n"
        "2.4 The Receiving Party shall limit access to the Confidential Information to its Authorized "
        "Representatives and shall ensure that each Authorized Representative is aware of and complies "
        "with the terms of this Agreement.\n\n"
        "2.5 The Receiving Party shall promptly notify the Disclosing Party in writing of any unauthorized "
        "use or disclosure of the Confidential Information of which it becomes aware, and shall cooperate "
        "fully with the Disclosing Party to prevent further unauthorized disclosure.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )
    page.insert_text(pymupdf.Point(250, 750), "Page 3 of 6", fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # Page 4: Exclusions
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "3. EXCLUSIONS FROM CONFIDENTIAL INFORMATION", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page.insert_textbox(
        pymupdf.Rect(72, 100, 540, 500),
        "The obligations under this Agreement shall not apply to information that:\n\n"
        "(a) Was already known to the Receiving Party at the time of disclosure, as evidenced by "
        "written records predating the disclosure;\n\n"
        "(b) Is or becomes publicly available through no fault or action of the Receiving Party;\n\n"
        "(c) Is independently developed by the Receiving Party without reference to or use of the "
        "Confidential Information, as demonstrated by contemporaneous documentation;\n\n"
        "(d) Is rightfully received from a third party without restriction on disclosure and without "
        "breach of any obligation of confidentiality;\n\n"
        "(e) Is required to be disclosed by applicable law, regulation, or court order, provided that "
        "the Receiving Party gives the Disclosing Party prompt written notice of such requirement and "
        "reasonable opportunity to seek a protective order or other appropriate remedy.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )
    page.insert_text(pymupdf.Point(72, 530), "4. TERM AND TERMINATION", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page.insert_textbox(
        pymupdf.Rect(72, 558, 540, 720),
        "4.1 This Agreement shall remain in effect for a period of three (3) years from the Effective Date, "
        "unless earlier terminated by either party upon thirty (30) days' written notice.\n\n"
        "4.2 The obligations of confidentiality under this Agreement shall survive termination for a period "
        "of five (5) years following the date of termination.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )
    page.insert_text(pymupdf.Point(250, 750), "Page 4 of 6", fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # Page 5: Return of materials, remedies
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "5. RETURN OF CONFIDENTIAL INFORMATION", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page.insert_textbox(
        pymupdf.Rect(72, 100, 540, 350),
        "5.1 Upon termination of this Agreement or upon written request by the Disclosing Party, the "
        "Receiving Party shall promptly return or destroy all copies of the Confidential Information "
        "in its possession or control, including all documents, files, electronic data, and any other "
        "media containing Confidential Information.\n\n"
        "5.2 The Receiving Party shall certify in writing to the Disclosing Party that it has complied "
        "with the foregoing requirement within fifteen (15) business days of receiving such request.\n\n"
        "5.3 Notwithstanding the foregoing, the Receiving Party may retain one archival copy of the "
        "Confidential Information solely for legal compliance and audit purposes, subject to the "
        "continuing obligations of this Agreement.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )
    page.insert_text(pymupdf.Point(72, 380), "6. REMEDIES", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page.insert_textbox(
        pymupdf.Rect(72, 408, 540, 600),
        "6.1 The parties acknowledge that any breach of this Agreement may cause irreparable harm to "
        "the Disclosing Party for which monetary damages may be inadequate. Accordingly, the Disclosing "
        "Party shall be entitled to seek equitable relief, including injunction and specific performance, "
        "in addition to any other remedies available at law or in equity.\n\n"
        "6.2 The prevailing party in any action to enforce this Agreement shall be entitled to recover "
        "its reasonable attorneys' fees and costs.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )
    page.insert_text(pymupdf.Point(250, 750), "Page 5 of 6", fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

    # Page 6: General provisions and signature block
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(72, 72), "7. GENERAL PROVISIONS", fontsize=14, fontname="hebo", color=(0, 0, 0))
    page.insert_textbox(
        pymupdf.Rect(72, 100, 540, 420),
        "7.1 Governing Law. This Agreement shall be governed by and construed in accordance with the "
        "laws of the State of California, without regard to its conflict of laws principles.\n\n"
        "7.2 Entire Agreement. This Agreement constitutes the entire agreement between the parties with "
        "respect to the subject matter hereof and supersedes all prior and contemporaneous agreements, "
        "understandings, and communications.\n\n"
        "7.3 Amendment. This Agreement may not be amended or modified except by a written instrument "
        "signed by both parties.\n\n"
        "7.4 Severability. If any provision of this Agreement is held to be invalid or unenforceable, "
        "the remaining provisions shall continue in full force and effect.\n\n"
        "7.5 Waiver. The failure of either party to enforce any provision of this Agreement shall not "
        "constitute a waiver of that party's right to subsequently enforce the provision.",
        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )
    page.insert_text(pymupdf.Point(72, 460), "IN WITNESS WHEREOF, the parties have executed this Agreement as of the Effective Date.", fontsize=11, fontname="helv", color=(0, 0, 0))

    # Signature blocks
    page.insert_text(pymupdf.Point(72, 520), "DISCLOSING PARTY:", fontsize=11, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 545), "Meridian Technologies, Inc.", fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 575), "By: _______________________________", fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 595), "Name: Dr. Elena Vasquez, Chief Executive Officer", fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 615), "Date: _______________________________", fontsize=11, fontname="helv", color=(0, 0, 0))

    page.insert_text(pymupdf.Point(72, 660), "RECEIVING PARTY:", fontsize=11, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 685), "Clearwater Analytics Group, LLC", fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 715), "By: _______________________________", fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 735), "Name: Michael R. Thornton, Managing Partner", fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 755), "Date: _______________________________", fontsize=11, fontname="helv", color=(0, 0, 0))

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
