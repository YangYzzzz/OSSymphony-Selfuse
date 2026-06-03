"""
Initial Setup: Create a 6-page signed contract PDF with 12 filled form fields
Task ID: pdf_ro_007
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_007'
FORMS_DIR = f'{WORKDIR}/forms'
OUTPUT = f'{FORMS_DIR}/signed_contract.pdf'


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


def add_contract_text(page, page_num, page_width, page_height):
    """Add realistic contract text to each page."""

    # Common layout
    margin_left = 72
    margin_right = page_width - 72
    text_width = margin_right - margin_left

    if page_num == 0:
        # Title page / header + opening sections
        page.insert_text(pymupdf.Point(page_width / 2 - 120, 60),
                         "PROFESSIONAL SERVICES AGREEMENT",
                         fontsize=16, fontname="hebo", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(page_width / 2 - 80, 82),
                         "Contract No. PSA-2025-04182",
                         fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

        # Horizontal rule
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(margin_left, 95), pymupdf.Point(margin_right, 95))
        shape.finish(color=(0, 0, 0), width=1)
        shape.commit()

        y = 120
        page.insert_text(pymupdf.Point(margin_left, y),
                         "This Professional Services Agreement (\"Agreement\") is entered into as of the",
                         fontsize=10, fontname="helv")
        y += 16
        page.insert_text(pymupdf.Point(margin_left, y),
                         "date last signed below, by and between:",
                         fontsize=10, fontname="helv")

        y += 30
        page.insert_text(pymupdf.Point(margin_left, y),
                         "SERVICE PROVIDER:", fontsize=10, fontname="hebo")
        y += 16
        page.insert_text(pymupdf.Point(margin_left, y),
                         "Meridian Consulting Group, LLC", fontsize=10, fontname="helv")
        y += 14
        page.insert_text(pymupdf.Point(margin_left, y),
                         "1250 Technology Parkway, Suite 400", fontsize=10, fontname="helv")
        y += 14
        page.insert_text(pymupdf.Point(margin_left, y),
                         "San Francisco, CA 94105", fontsize=10, fontname="helv")

        y += 30
        page.insert_text(pymupdf.Point(margin_left, y),
                         "CLIENT INFORMATION:", fontsize=10, fontname="hebo")

        # Page 0 will have form fields for client info (added separately)

        y += 50
        page.insert_text(pymupdf.Point(margin_left, y), "Client Full Name:", fontsize=10, fontname="hebo")
        y += 30
        page.insert_text(pymupdf.Point(margin_left, y), "Company Name:", fontsize=10, fontname="hebo")
        y += 30
        page.insert_text(pymupdf.Point(margin_left, y), "Street Address:", fontsize=10, fontname="hebo")
        y += 30
        page.insert_text(pymupdf.Point(margin_left, y), "Phone Number:", fontsize=10, fontname="hebo")
        y += 30
        page.insert_text(pymupdf.Point(margin_left, y), "Email Address:", fontsize=10, fontname="hebo")

        y += 40
        page.insert_text(pymupdf.Point(margin_left, y),
                         "1. SCOPE OF SERVICES", fontsize=12, fontname="hebo")
        y += 18
        page.insert_textbox(
            pymupdf.Rect(margin_left, y, margin_right, y + 100),
            "The Service Provider agrees to provide the following professional consulting "
            "services to the Client: strategic business analysis, process optimization, "
            "technology assessment, and implementation support as detailed in Exhibit A "
            "attached hereto and incorporated by reference. The scope of services may be "
            "modified only by written amendment signed by both parties.",
            fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    elif page_num == 1:
        y = 60
        page.insert_text(pymupdf.Point(margin_left, y),
                         "2. TERM AND TERMINATION", fontsize=12, fontname="hebo")
        y += 20
        page.insert_text(pymupdf.Point(margin_left, y), "Effective Date:", fontsize=10, fontname="hebo")
        y += 30
        page.insert_text(pymupdf.Point(margin_left, y), "End Date:", fontsize=10, fontname="hebo")

        y += 40
        page.insert_textbox(
            pymupdf.Rect(margin_left, y, margin_right, y + 80),
            "2.1 This Agreement shall commence on the Effective Date specified above and "
            "shall continue until the End Date, unless earlier terminated in accordance "
            "with the provisions herein. Either party may terminate this Agreement for "
            "cause upon thirty (30) days' written notice to the other party.",
            fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 90

        page.insert_textbox(
            pymupdf.Rect(margin_left, y, margin_right, y + 60),
            "2.2 Upon termination, the Client shall pay the Service Provider for all "
            "services rendered through the date of termination, plus any approved "
            "expenses incurred prior to the termination date.",
            fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

        y += 80
        page.insert_text(pymupdf.Point(margin_left, y),
                         "3. COMPENSATION AND PAYMENT", fontsize=12, fontname="hebo")
        y += 20
        page.insert_text(pymupdf.Point(margin_left, y), "Project Fee (USD):", fontsize=10, fontname="hebo")

        y += 40
        page.insert_textbox(
            pymupdf.Rect(margin_left, y, margin_right, y + 100),
            "3.1 The Client agrees to pay the Service Provider the Project Fee specified "
            "above for the services described in this Agreement. Payment shall be made in "
            "three installments: 40% upon execution of this Agreement, 30% upon completion "
            "of the midpoint deliverables, and 30% upon final delivery and acceptance. "
            "All invoices are due within thirty (30) days of receipt. Late payments shall "
            "accrue interest at a rate of 1.5% per month.",
            fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

        y += 120
        page.insert_textbox(
            pymupdf.Rect(margin_left, y, margin_right, y + 80),
            "3.2 The Service Provider shall submit itemized invoices on a monthly basis. "
            "Each invoice shall include a description of services performed, hours worked "
            "(if applicable), and any pre-approved expenses. The Client reserves the right "
            "to dispute any invoice item within fifteen (15) days of receipt.",
            fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    elif page_num == 2:
        y = 60
        page.insert_text(pymupdf.Point(margin_left, y),
                         "4. CONFIDENTIALITY", fontsize=12, fontname="hebo")
        y += 20
        page.insert_textbox(
            pymupdf.Rect(margin_left, y, margin_right, y + 100),
            "4.1 Each party acknowledges that during the performance of this Agreement, "
            "it may receive or have access to confidential information of the other party. "
            "\"Confidential Information\" means any information that is marked as confidential "
            "or that a reasonable person would understand to be confidential given the nature "
            "of the information and the circumstances of disclosure.",
            fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

        y += 110
        page.insert_textbox(
            pymupdf.Rect(margin_left, y, margin_right, y + 80),
            "4.2 The receiving party shall not disclose any Confidential Information to "
            "third parties without the prior written consent of the disclosing party, "
            "except as required by law. This obligation shall survive the termination "
            "of this Agreement for a period of three (3) years.",
            fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

        y += 100
        page.insert_text(pymupdf.Point(margin_left, y),
                         "5. INTELLECTUAL PROPERTY", fontsize=12, fontname="hebo")
        y += 20
        page.insert_textbox(
            pymupdf.Rect(margin_left, y, margin_right, y + 100),
            "5.1 All deliverables, work product, and materials created by the Service "
            "Provider specifically for the Client under this Agreement shall be considered "
            "\"work made for hire\" and shall be the exclusive property of the Client upon "
            "full payment. The Service Provider retains ownership of any pre-existing "
            "intellectual property, tools, frameworks, and methodologies.",
            fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

        y += 110
        page.insert_textbox(
            pymupdf.Rect(margin_left, y, margin_right, y + 80),
            "5.2 The Service Provider grants the Client a non-exclusive, perpetual, "
            "royalty-free license to use any pre-existing intellectual property "
            "incorporated into the deliverables, solely for the purposes described "
            "in this Agreement.",
            fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

        y += 100
        page.insert_text(pymupdf.Point(margin_left, y),
                         "6. WARRANTIES AND REPRESENTATIONS", fontsize=12, fontname="hebo")
        y += 20
        page.insert_textbox(
            pymupdf.Rect(margin_left, y, margin_right, y + 80),
            "6.1 The Service Provider represents and warrants that: (a) it has the "
            "requisite skills, experience, and qualifications to perform the services; "
            "(b) the services will be performed in a professional and workmanlike manner; "
            "and (c) the deliverables will conform to the specifications set forth in "
            "Exhibit A.",
            fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    elif page_num == 3:
        y = 60
        page.insert_text(pymupdf.Point(margin_left, y),
                         "7. LIMITATION OF LIABILITY", fontsize=12, fontname="hebo")
        y += 20
        page.insert_textbox(
            pymupdf.Rect(margin_left, y, margin_right, y + 100),
            "7.1 IN NO EVENT SHALL EITHER PARTY BE LIABLE TO THE OTHER FOR ANY INDIRECT, "
            "INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING BUT NOT "
            "LIMITED TO LOSS OF PROFITS, DATA, OR BUSINESS OPPORTUNITIES, ARISING OUT OF "
            "OR RELATED TO THIS AGREEMENT, REGARDLESS OF THE FORM OF ACTION OR THEORY "
            "OF LIABILITY.",
            fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

        y += 110
        page.insert_textbox(
            pymupdf.Rect(margin_left, y, margin_right, y + 60),
            "7.2 The total aggregate liability of the Service Provider under this "
            "Agreement shall not exceed the total fees paid or payable by the Client "
            "under this Agreement during the twelve (12) months preceding the claim.",
            fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

        y += 80
        page.insert_text(pymupdf.Point(margin_left, y),
                         "8. INDEMNIFICATION", fontsize=12, fontname="hebo")
        y += 20
        page.insert_textbox(
            pymupdf.Rect(margin_left, y, margin_right, y + 100),
            "8.1 Each party shall indemnify, defend, and hold harmless the other party "
            "from and against any and all claims, damages, losses, liabilities, costs, "
            "and expenses (including reasonable attorneys' fees) arising out of or "
            "relating to: (a) any breach of this Agreement by the indemnifying party; "
            "(b) the negligence or willful misconduct of the indemnifying party; or "
            "(c) any violation of applicable law by the indemnifying party.",
            fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

        y += 120
        page.insert_text(pymupdf.Point(margin_left, y),
                         "9. DISPUTE RESOLUTION", fontsize=12, fontname="hebo")
        y += 20
        page.insert_textbox(
            pymupdf.Rect(margin_left, y, margin_right, y + 100),
            "9.1 Any dispute arising out of or relating to this Agreement shall first "
            "be submitted to good faith mediation. If mediation is unsuccessful within "
            "sixty (60) days, the dispute shall be resolved by binding arbitration under "
            "the rules of the American Arbitration Association. The arbitration shall "
            "take place in San Francisco, California. The prevailing party shall be "
            "entitled to recover reasonable attorneys' fees and costs.",
            fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    elif page_num == 4:
        y = 60
        page.insert_text(pymupdf.Point(margin_left, y),
                         "10. GENERAL PROVISIONS", fontsize=12, fontname="hebo")
        y += 20
        page.insert_textbox(
            pymupdf.Rect(margin_left, y, margin_right, y + 60),
            "10.1 Entire Agreement. This Agreement, together with all exhibits and "
            "amendments, constitutes the entire agreement between the parties and "
            "supersedes all prior negotiations, representations, and agreements.",
            fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

        y += 70
        page.insert_textbox(
            pymupdf.Rect(margin_left, y, margin_right, y + 60),
            "10.2 Amendment. No modification of this Agreement shall be effective "
            "unless made in writing and signed by authorized representatives of "
            "both parties.",
            fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

        y += 70
        page.insert_textbox(
            pymupdf.Rect(margin_left, y, margin_right, y + 60),
            "10.3 Severability. If any provision of this Agreement is held to be "
            "invalid or unenforceable, the remaining provisions shall continue in "
            "full force and effect.",
            fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

        y += 70
        page.insert_textbox(
            pymupdf.Rect(margin_left, y, margin_right, y + 60),
            "10.4 Waiver. The failure of either party to enforce any provision of "
            "this Agreement shall not constitute a waiver of that party's right to "
            "enforce such provision in the future.",
            fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

        y += 70
        page.insert_textbox(
            pymupdf.Rect(margin_left, y, margin_right, y + 60),
            "10.5 Governing Law. This Agreement shall be governed by and construed "
            "in accordance with the laws of the State of California, without regard "
            "to its conflict of laws principles.",
            fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

        y += 70
        page.insert_textbox(
            pymupdf.Rect(margin_left, y, margin_right, y + 80),
            "10.6 Notices. All notices required or permitted under this Agreement "
            "shall be in writing and shall be delivered by certified mail, return "
            "receipt requested, or by nationally recognized overnight courier, to "
            "the addresses set forth on the first page of this Agreement.",
            fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    elif page_num == 5:
        y = 60
        page.insert_text(pymupdf.Point(margin_left, y),
                         "SIGNATURES", fontsize=14, fontname="hebo")

        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(margin_left, y + 10), pymupdf.Point(margin_right, y + 10))
        shape.finish(color=(0, 0, 0), width=1)
        shape.commit()

        y += 35
        page.insert_text(pymupdf.Point(margin_left, y),
                         "IN WITNESS WHEREOF, the parties have executed this Agreement as of",
                         fontsize=10, fontname="helv")
        y += 16
        page.insert_text(pymupdf.Point(margin_left, y),
                         "the date last written below.", fontsize=10, fontname="helv")

        y += 40
        page.insert_text(pymupdf.Point(margin_left, y),
                         "SERVICE PROVIDER: Meridian Consulting Group, LLC",
                         fontsize=10, fontname="hebo")

        y += 25
        page.insert_text(pymupdf.Point(margin_left, y),
                         "Authorized Signature:", fontsize=10, fontname="helv")
        # Signature line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(200, y + 3), pymupdf.Point(400, y + 3))
        shape.finish(color=(0.5, 0.5, 0.5), width=0.5)
        shape.commit()

        y += 25
        page.insert_text(pymupdf.Point(margin_left, y),
                         "Print Name:", fontsize=10, fontname="helv")
        y += 25
        page.insert_text(pymupdf.Point(margin_left, y),
                         "Title:", fontsize=10, fontname="helv")
        y += 25
        page.insert_text(pymupdf.Point(margin_left, y),
                         "Date Signed:", fontsize=10, fontname="helv")

        y += 50
        page.insert_text(pymupdf.Point(margin_left, y),
                         "CLIENT:", fontsize=10, fontname="hebo")

        y += 25
        page.insert_text(pymupdf.Point(margin_left, y),
                         "Client Signature:", fontsize=10, fontname="helv")

        y += 25
        page.insert_text(pymupdf.Point(margin_left, y),
                         "Date Signed:", fontsize=10, fontname="helv")

    # Footer on every page
    page.insert_text(
        pymupdf.Point(margin_left, page_height - 30),
        f"PSA-2025-04182  |  Meridian Consulting Group  |  Page {page_num + 1} of 6",
        fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))


def add_form_fields(doc):
    """Add 12 form fields across the 6-page contract."""
    field_x = 220  # x-position for field start
    field_w = 320  # field width end x

    # --- Page 0: Client Information (5 fields) ---
    page = doc[0]

    fields_p0 = [
        ("client_name", "Alexandra Petrova", 287),
        ("company_name", "Northwind Technologies Inc.", 317),
        ("street_address", "4720 Innovation Boulevard, Austin, TX 78701", 347),
        ("phone_number", "(512) 555-0198", 377),
        ("email_address", "a.petrova@northwindtech.com", 407),
    ]

    for name, value, y_pos in fields_p0:
        widget = pymupdf.Widget()
        widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
        widget.field_name = name
        widget.field_value = value
        widget.rect = pymupdf.Rect(field_x, y_pos - 13, field_w + 100, y_pos + 5)
        widget.text_fontsize = 10
        widget.text_color = (0, 0, 0.5)
        widget.fill_color = (0.97, 0.97, 1.0)
        widget.border_color = (0.6, 0.6, 0.8)
        widget.border_width = 0.5
        page.add_widget(widget)

    # --- Page 1: Dates and Fee (3 fields) ---
    page = doc[1]

    fields_p1 = [
        ("effective_date", "March 15, 2025", 77),
        ("end_date", "September 15, 2025", 107),
        ("project_fee", "$87,500.00", 277),
    ]

    for name, value, y_pos in fields_p1:
        widget = pymupdf.Widget()
        widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
        widget.field_name = name
        widget.field_value = value
        widget.rect = pymupdf.Rect(field_x, y_pos - 13, field_w + 50, y_pos + 5)
        widget.text_fontsize = 10
        widget.text_color = (0, 0, 0.5)
        widget.fill_color = (0.97, 0.97, 1.0)
        widget.border_color = (0.6, 0.6, 0.8)
        widget.border_width = 0.5
        page.add_widget(widget)

    # --- Page 5: Signatures (4 fields) ---
    page = doc[5]

    # Provider signature fields
    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "provider_signature"
    widget.field_value = "Daniel R. Whitmore"
    widget.rect = pymupdf.Rect(200, 147, 400, 165)
    widget.text_fontsize = 12
    widget.text_color = (0, 0, 0.3)
    widget.fill_color = (0.97, 0.97, 1.0)
    widget.border_color = (0.6, 0.6, 0.8)
    widget.border_width = 0.5
    page.add_widget(widget)

    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "provider_date"
    widget.field_value = "March 12, 2025"
    widget.rect = pymupdf.Rect(200, 222, 350, 240)
    widget.text_fontsize = 10
    widget.text_color = (0, 0, 0.5)
    widget.fill_color = (0.97, 0.97, 1.0)
    widget.border_color = (0.6, 0.6, 0.8)
    widget.border_width = 0.5
    page.add_widget(widget)

    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "client_signature"
    widget.field_value = "Alexandra Petrova"
    widget.rect = pymupdf.Rect(200, 287, 400, 305)
    widget.text_fontsize = 12
    widget.text_color = (0, 0, 0.3)
    widget.fill_color = (0.97, 0.97, 1.0)
    widget.border_color = (0.6, 0.6, 0.8)
    widget.border_width = 0.5
    page.add_widget(widget)

    widget = pymupdf.Widget()
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "client_date"
    widget.field_value = "March 15, 2025"
    widget.rect = pymupdf.Rect(200, 312, 350, 330)
    widget.text_fontsize = 10
    widget.text_color = (0, 0, 0.5)
    widget.fill_color = (0.97, 0.97, 1.0)
    widget.border_color = (0.6, 0.6, 0.8)
    widget.border_width = 0.5
    page.add_widget(widget)


def create_initial():
    os.makedirs(FORMS_DIR, exist_ok=True)

    doc = pymupdf.open()
    page_width, page_height = 612, 792  # US Letter

    # Create 6 pages with contract content
    for i in range(6):
        page = doc.new_page(width=page_width, height=page_height)
        add_contract_text(page, i, page_width, page_height)

    # Save first to establish the document, then add form fields
    doc.save(OUTPUT)
    doc.close()

    # Reopen to add form fields (widgets need an existing PDF)
    doc = pymupdf.open(OUTPUT)
    add_form_fields(doc)
    doc.save(OUTPUT, incremental=True, encryption=pymupdf.PDF_ENCRYPT_KEEP)
    doc.close()

    # Verify
    doc = pymupdf.open(OUTPUT)
    widget_count = 0
    for page in doc:
        for w in page.widgets():
            widget_count += 1
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: {doc.page_count}')
    print(f'Form field count: {widget_count}')
    doc.close()

    # Remove any pre-existing flattened file (must not exist in initial)
    final_path = f'{FORMS_DIR}/signed_contract_final.pdf'
    if os.path.exists(final_path):
        os.remove(final_path)

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
