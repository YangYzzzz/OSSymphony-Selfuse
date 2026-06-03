"""
Initial Setup: Create a digitally signed contract PDF with signature fields
Task ID: pdf_gf2_041
Domain: pdf (libreoffice_calc mapped)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_041'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/signed_contract.pdf'


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
    os.makedirs(DOCS_DIR, exist_ok=True)

    # Remove any pre-existing verification report (negative constraint)
    report_path = f'{DOCS_DIR}/signature_verification.txt'
    if os.path.exists(report_path):
        os.remove(report_path)

    # --- Step 1: Create a rich 8-page contract PDF using PyMuPDF ---
    import pymupdf

    doc = pymupdf.open()

    W, H = 612, 792  # Letter size

    # Contract content for 8 pages
    contract_sections = [
        {
            "title": "PROFESSIONAL SERVICES AGREEMENT",
            "subtitle": "Contract No. PSA-2025-0847",
            "body": (
                "This Professional Services Agreement (the \"Agreement\") is entered into as of "
                "March 15, 2025, by and between:\n\n"
                "PARTY A: Meridian Technologies, Inc., a Delaware corporation with its principal "
                "office at 2400 Bayshore Boulevard, Suite 1200, San Francisco, CA 94134 "
                "(\"Client\")\n\n"
                "PARTY B: Apex Consulting Group, LLC, a New York limited liability company with "
                "its principal office at 590 Madison Avenue, 21st Floor, New York, NY 10022 "
                "(\"Consultant\")\n\n"
                "WHEREAS, Client desires to engage Consultant to provide certain professional "
                "consulting services as described herein; and\n\n"
                "WHEREAS, Consultant represents that it has the expertise, qualifications, and "
                "capacity to perform such services;\n\n"
                "NOW, THEREFORE, in consideration of the mutual covenants and agreements set forth "
                "herein, and for other good and valuable consideration, the receipt and sufficiency "
                "of which are hereby acknowledged, the parties agree as follows:"
            ),
        },
        {
            "title": "ARTICLE 1: SCOPE OF SERVICES",
            "body": (
                "1.1 Engagement. Client hereby engages Consultant, and Consultant hereby accepts "
                "such engagement, to provide the professional services described in Exhibit A "
                "attached hereto (the \"Services\").\n\n"
                "1.2 Standard of Performance. Consultant shall perform the Services in a "
                "professional and workmanlike manner, consistent with industry standards and "
                "practices. Consultant shall assign qualified personnel with appropriate expertise "
                "to perform the Services.\n\n"
                "1.3 Project Timeline. The Services shall commence on April 1, 2025, and shall "
                "continue through September 30, 2025, unless earlier terminated in accordance "
                "with Article 6 of this Agreement (the \"Term\").\n\n"
                "1.4 Deliverables. Consultant shall provide the following deliverables:\n"
                "  (a) Initial Assessment Report - Due April 30, 2025\n"
                "  (b) System Architecture Design - Due May 31, 2025\n"
                "  (c) Implementation Plan - Due June 30, 2025\n"
                "  (d) Progress Reports - Monthly, beginning May 2025\n"
                "  (e) Final Implementation and Documentation - Due September 15, 2025\n\n"
                "1.5 Acceptance. Client shall have fifteen (15) business days following receipt "
                "of each deliverable to review and either accept or provide written notice of "
                "rejection with specific reasons. Failure to provide notice within such period "
                "shall constitute acceptance."
            ),
        },
        {
            "title": "ARTICLE 2: COMPENSATION AND PAYMENT",
            "body": (
                "2.1 Fees. In consideration for the Services, Client shall pay Consultant a "
                "total fee of Four Hundred Seventy-Five Thousand United States Dollars "
                "(US$475,000.00) (the \"Fee\"), payable as follows:\n\n"
                "  (a) Initial payment of $95,000.00 upon execution of this Agreement\n"
                "  (b) Monthly installments of $63,333.33 for months 2 through 6\n"
                "  (c) Final payment of $63,333.35 upon completion and acceptance of all "
                "deliverables\n\n"
                "2.2 Expenses. Client shall reimburse Consultant for all reasonable and "
                "pre-approved out-of-pocket expenses incurred in connection with the performance "
                "of the Services, including but not limited to travel, lodging, and materials. "
                "Expenses exceeding $2,500 per item require prior written approval from Client.\n\n"
                "2.3 Invoicing. Consultant shall submit invoices on a monthly basis. Each invoice "
                "shall include a detailed description of Services performed and expenses incurred "
                "during the applicable period.\n\n"
                "2.4 Payment Terms. Client shall pay each invoice within thirty (30) days of "
                "receipt. Late payments shall bear interest at the rate of 1.5% per month or "
                "the maximum rate permitted by applicable law, whichever is less.\n\n"
                "2.5 Taxes. Consultant shall be responsible for all taxes arising from the "
                "compensation received under this Agreement, including income taxes, "
                "self-employment taxes, and any applicable sales or use taxes."
            ),
        },
        {
            "title": "ARTICLE 3: INTELLECTUAL PROPERTY",
            "body": (
                "3.1 Work Product. All work product, deliverables, inventions, discoveries, "
                "designs, developments, improvements, and other results of the Services "
                "(collectively, \"Work Product\") shall be the sole and exclusive property of "
                "Client.\n\n"
                "3.2 Assignment. Consultant hereby irrevocably assigns to Client all right, "
                "title, and interest in and to the Work Product, including all intellectual "
                "property rights therein. Consultant shall execute any documents and take any "
                "actions reasonably requested by Client to perfect Client's ownership rights.\n\n"
                "3.3 Pre-Existing Materials. Consultant retains ownership of all tools, "
                "methodologies, frameworks, and materials developed by Consultant prior to or "
                "independent of this Agreement (\"Pre-Existing Materials\"). To the extent "
                "Pre-Existing Materials are incorporated into any Work Product, Consultant hereby "
                "grants Client a non-exclusive, perpetual, irrevocable, worldwide, royalty-free "
                "license to use, modify, and distribute such Pre-Existing Materials as part of "
                "the Work Product.\n\n"
                "3.4 Third-Party Materials. Consultant shall not incorporate any third-party "
                "materials into the Work Product without Client's prior written consent and "
                "shall ensure that any such materials are properly licensed."
            ),
        },
        {
            "title": "ARTICLE 4: CONFIDENTIALITY",
            "body": (
                "4.1 Confidential Information. \"Confidential Information\" means any non-public "
                "information disclosed by either party to the other in connection with this "
                "Agreement, including but not limited to business plans, financial data, customer "
                "lists, technical specifications, trade secrets, and proprietary methodologies.\n\n"
                "4.2 Obligations. Each party shall: (a) maintain the confidentiality of the other "
                "party's Confidential Information using at least the same degree of care it uses "
                "to protect its own confidential information, but no less than reasonable care; "
                "(b) not disclose Confidential Information to any third party without the prior "
                "written consent of the disclosing party; and (c) use Confidential Information "
                "solely for the purposes of this Agreement.\n\n"
                "4.3 Exceptions. The obligations of Section 4.2 shall not apply to information "
                "that: (a) is or becomes publicly available through no fault of the receiving "
                "party; (b) was known to the receiving party prior to disclosure; (c) is "
                "independently developed by the receiving party; or (d) is disclosed pursuant "
                "to a legal requirement, provided that the receiving party gives prompt notice "
                "to the disclosing party.\n\n"
                "4.4 Duration. The obligations under this Article 4 shall survive the termination "
                "or expiration of this Agreement for a period of five (5) years."
            ),
        },
        {
            "title": "ARTICLE 5: REPRESENTATIONS AND WARRANTIES",
            "body": (
                "5.1 Mutual Representations. Each party represents and warrants that: (a) it has "
                "the legal power and authority to enter into this Agreement; (b) this Agreement "
                "constitutes a valid and binding obligation enforceable against it; and (c) the "
                "execution and performance of this Agreement does not conflict with any other "
                "agreement to which it is a party.\n\n"
                "5.2 Consultant Representations. Consultant additionally represents and warrants "
                "that: (a) it has the necessary skills, experience, and qualifications to perform "
                "the Services; (b) the Services will be performed in a professional manner "
                "consistent with industry standards; (c) the Work Product will not infringe upon "
                "the intellectual property rights of any third party; and (d) it will comply with "
                "all applicable laws and regulations in performing the Services.\n\n"
                "5.3 Limitation of Warranties. EXCEPT AS EXPRESSLY SET FORTH IN THIS AGREEMENT, "
                "NEITHER PARTY MAKES ANY WARRANTIES, EXPRESS OR IMPLIED, INCLUDING WARRANTIES OF "
                "MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.\n\n"
                "5.4 Indemnification. Each party shall indemnify, defend, and hold harmless the "
                "other party from any claims, damages, losses, or expenses arising from the "
                "indemnifying party's breach of its representations and warranties hereunder."
            ),
        },
        {
            "title": "ARTICLE 6: TERMINATION",
            "body": (
                "6.1 Termination for Convenience. Either party may terminate this Agreement upon "
                "sixty (60) days' prior written notice to the other party.\n\n"
                "6.2 Termination for Cause. Either party may terminate this Agreement immediately "
                "upon written notice if the other party: (a) materially breaches this Agreement "
                "and fails to cure such breach within thirty (30) days of written notice; or "
                "(b) becomes insolvent, files for bankruptcy, or has a receiver appointed.\n\n"
                "6.3 Effect of Termination. Upon termination: (a) Consultant shall deliver all "
                "completed and in-progress Work Product to Client; (b) Client shall pay Consultant "
                "for all Services satisfactorily performed through the date of termination; and "
                "(c) all provisions that by their nature should survive termination shall survive.\n\n"
                "ARTICLE 7: GENERAL PROVISIONS\n\n"
                "7.1 Governing Law. This Agreement shall be governed by the laws of the State of "
                "California, without regard to conflict of laws principles.\n\n"
                "7.2 Dispute Resolution. Any disputes arising under this Agreement shall be "
                "resolved through binding arbitration in San Francisco, California, under the "
                "rules of the American Arbitration Association.\n\n"
                "7.3 Entire Agreement. This Agreement constitutes the entire agreement between "
                "the parties and supersedes all prior negotiations, representations, and "
                "agreements.\n\n"
                "7.4 Amendment. This Agreement may be amended only by a written instrument signed "
                "by both parties.\n\n"
                "7.5 Severability. If any provision is found unenforceable, the remaining "
                "provisions shall continue in full force and effect.\n\n"
                "7.6 Notices. All notices shall be in writing and sent to the addresses first "
                "set forth above, or to such other address as a party may designate in writing."
            ),
        },
        {
            "title": "EXECUTION AND SIGNATURES",
            "body": (
                "IN WITNESS WHEREOF, the parties have executed this Professional Services "
                "Agreement as of the date first written above.\n\n"
                "MERIDIAN TECHNOLOGIES, INC.\n\n\n"
                "By: ________________________________\n"
                "Name: Victoria R. Harrington\n"
                "Title: Chief Technology Officer\n"
                "Date: March 15, 2025\n\n\n"
                "APEX CONSULTING GROUP, LLC\n\n\n"
                "By: ________________________________\n"
                "Name: David M. Nakamura\n"
                "Title: Managing Partner\n"
                "Date: March 15, 2025\n\n\n"
                "WITNESS:\n\n\n"
                "By: ________________________________\n"
                "Name: Rachel T. Okonkwo\n"
                "Title: General Counsel, Meridian Technologies\n"
                "Date: March 15, 2025"
            ),
        },
    ]

    for i, section in enumerate(contract_sections):
        page = doc.new_page(width=W, height=H)

        # Header line
        if i == 0:
            # Title page header
            page.insert_text(
                pymupdf.Point(72, 60),
                section["title"],
                fontsize=18,
                fontname="hebo",
                color=(0.1, 0.1, 0.3),
            )
            page.insert_text(
                pymupdf.Point(72, 85),
                section["subtitle"],
                fontsize=12,
                fontname="helv",
                color=(0.3, 0.3, 0.3),
            )
            # Horizontal line
            page.draw_line(pymupdf.Point(72, 95), pymupdf.Point(540, 95),
                           color=(0.1, 0.1, 0.3), width=1.5)
            body_top = 115
        else:
            page.insert_text(
                pymupdf.Point(72, 55),
                section["title"],
                fontsize=14,
                fontname="hebo",
                color=(0.1, 0.1, 0.3),
            )
            page.draw_line(pymupdf.Point(72, 65), pymupdf.Point(540, 65),
                           color=(0.7, 0.7, 0.7), width=0.5)
            body_top = 80

        # Body text
        rect = pymupdf.Rect(72, body_top, 540, 740)
        page.insert_textbox(
            rect,
            section["body"],
            fontsize=10.5,
            fontname="tiro",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

        # Footer
        page.insert_text(
            pymupdf.Point(72, 760),
            f"PSA-2025-0847 | Confidential",
            fontsize=8,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )
        page.insert_text(
            pymupdf.Point(500, 760),
            f"Page {i + 1} of 8",
            fontsize=8,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    # Save intermediate version
    doc.save(OUTPUT)
    doc.close()

    # --- Step 2: Add digital signature fields using pikepdf ---
    import pikepdf

    pdf = pikepdf.open(OUTPUT, allow_overwriting_input=True)

    # Get page object (use .obj to avoid ObjectHelper issues)
    last_page_obj = pdf.pages[-1].obj

    # Helper to create a sig value dict
    def make_sig_value(name, date_str, reason, location, contact):
        sv = pikepdf.Dictionary()
        sv['/Type'] = pikepdf.Name.Sig
        sv['/Filter'] = pikepdf.Name("/Adobe.PPKLite")
        sv['/SubFilter'] = pikepdf.Name("/adbe.pkcs7.detached")
        sv['/Name'] = pikepdf.String(name)
        sv['/M'] = pikepdf.String(date_str)
        sv['/Reason'] = pikepdf.String(reason)
        sv['/Location'] = pikepdf.String(location)
        sv['/ContactInfo'] = pikepdf.String(contact)
        return pdf.make_indirect(sv)

    def make_sig_field(field_name, rect, sig_value_ref=None):
        sf = pikepdf.Dictionary()
        sf['/Type'] = pikepdf.Name.Annot
        sf['/Subtype'] = pikepdf.Name.Widget
        sf['/FT'] = pikepdf.Name.Sig
        sf['/T'] = pikepdf.String(field_name)
        sf['/Rect'] = pikepdf.Array(rect)
        sf['/F'] = 4
        sf['/P'] = last_page_obj
        if sig_value_ref is not None:
            sf['/V'] = sig_value_ref
        return pdf.make_indirect(sf)

    # Signature 1: Client (signed)
    sv1 = make_sig_value("Victoria R. Harrington", "D:20250315143022+00'00'",
                         "Contract Execution - Client Signatory",
                         "San Francisco, CA", "v.harrington@meridiantech.com")
    sf1 = make_sig_field("Signature_Client", [150, 520, 350, 560], sv1)

    # Signature 2: Consultant (signed)
    sv2 = make_sig_value("David M. Nakamura", "D:20250315151530+00'00'",
                         "Contract Execution - Consultant Signatory",
                         "New York, NY", "d.nakamura@apexconsulting.com")
    sf2 = make_sig_field("Signature_Consultant", [150, 360, 350, 400], sv2)

    # Signature 3: Witness (unsigned/empty)
    sf3 = make_sig_field("Signature_Witness", [150, 200, 350, 240])

    # Add annotations to last page
    annots = pikepdf.Array([sf1, sf2, sf3])
    last_page_obj['/Annots'] = annots

    # Create AcroForm
    acroform = pikepdf.Dictionary()
    acroform['/Fields'] = pikepdf.Array([sf1, sf2, sf3])
    acroform['/SigFlags'] = 3  # SignaturesExist | AppendOnly
    pdf.Root['/AcroForm'] = acroform

    pdf.save(OUTPUT)
    pdf.close()

    print(f'Initial file created: {OUTPUT}')
    print(f'  - 8-page contract PDF with 3 signature fields')
    print(f'  - 2 signed (Harrington, Nakamura), 1 empty (Okonkwo)')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
