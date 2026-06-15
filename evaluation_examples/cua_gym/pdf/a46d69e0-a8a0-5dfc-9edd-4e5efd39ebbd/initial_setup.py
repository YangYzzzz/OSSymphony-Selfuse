"""
Initial Setup: Create a 10-page legal terms document with realistic content.
Task ID: pdf_gf2_007
Domain: pdf

The document contains the word 'liability' approximately 14 times and
the phrase 'without limitation' 3 times. No annotations exist.
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_007'
LEGAL_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{LEGAL_DIR}/terms.pdf'


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


# Legal document content across 10 pages
PAGES = [
    # Page 1 - Title and Introduction (liability: 0, without limitation: 0)
    {
        "title": "MASTER SERVICES AGREEMENT",
        "subtitle": "Effective Date: January 15, 2025",
        "body": (
            "This Master Services Agreement (the 'Agreement') is entered into by and between "
            "Meridian Technology Solutions, Inc., a Delaware corporation with principal offices "
            "at 1200 Innovation Drive, Suite 800, San Francisco, California 94107 ('Provider'), "
            "and the entity identified on the applicable Order Form ('Client').\n\n"
            "WHEREAS, Provider develops and licenses enterprise software solutions and related "
            "professional services; and\n\n"
            "WHEREAS, Client desires to engage Provider to deliver certain technology services "
            "and software solutions as described in one or more Order Forms executed pursuant "
            "to this Agreement;\n\n"
            "NOW, THEREFORE, in consideration of the mutual covenants and agreements set forth "
            "herein, and for other good and valuable consideration, the receipt and sufficiency "
            "of which are hereby acknowledged, the parties agree as follows:"
        ),
    },
    # Page 2 - Definitions (liability: 0, without limitation: 0)
    {
        "title": "ARTICLE 1: DEFINITIONS",
        "body": (
            "1.1 'Affiliate' means any entity that directly or indirectly controls, is "
            "controlled by, or is under common control with a party, where 'control' means "
            "ownership of more than fifty percent (50%) of the voting securities.\n\n"
            "1.2 'Confidential Information' means all non-public information disclosed by "
            "either party to the other, whether orally or in writing, that is designated as "
            "confidential or that reasonably should be understood to be confidential given "
            "the nature of the information and circumstances of disclosure.\n\n"
            "1.3 'Deliverables' means the work product, reports, data, documentation, and "
            "other materials to be delivered by Provider under an Order Form.\n\n"
            "1.4 'Intellectual Property Rights' means all patent rights, copyrights, trademark "
            "rights, trade secret rights, and any other intellectual property rights recognized "
            "in any jurisdiction worldwide.\n\n"
            "1.5 'Order Form' means a document executed by both parties that references this "
            "Agreement and specifies the Services, fees, and other terms applicable to a "
            "particular engagement.\n\n"
            "1.6 'Services' means the professional services, software development, consulting, "
            "and support services described in an Order Form."
        ),
    },
    # Page 3 - Scope of Services (liability: 1, without limitation: 1)
    {
        "title": "ARTICLE 2: SCOPE OF SERVICES",
        "body": (
            "2.1 Service Delivery. Provider shall perform the Services described in each "
            "Order Form in a professional and workmanlike manner, consistent with generally "
            "accepted industry standards. Provider shall assign qualified personnel to perform "
            "the Services and shall be responsible for their supervision and performance.\n\n"
            "2.2 Change Orders. Either party may request changes to the scope of Services "
            "under an Order Form by submitting a written change request. No change shall be "
            "effective unless agreed to in writing by both parties. Any liability arising "
            "from unauthorized scope changes shall rest with the requesting party.\n\n"
            "2.3 Client Obligations. Client shall provide Provider with timely access to "
            "Client's facilities, systems, data, and personnel as reasonably necessary for "
            "Provider to perform the Services. Client acknowledges that any failure to meet "
            "these obligations may result in delays and additional costs, including but "
            "without limitation additional consulting fees and resource allocation charges.\n\n"
            "2.4 Acceptance Testing. Upon delivery of each Deliverable, Client shall have "
            "fifteen (15) business days to review and test the Deliverable against the "
            "acceptance criteria specified in the applicable Order Form."
        ),
    },
    # Page 4 - Fees and Payment (liability: 2, without limitation: 0)
    {
        "title": "ARTICLE 3: FEES AND PAYMENT",
        "body": (
            "3.1 Fees. Client shall pay Provider the fees specified in each Order Form. "
            "Unless otherwise stated, fees are quoted in United States Dollars and are "
            "exclusive of all taxes, duties, and government levies.\n\n"
            "3.2 Payment Terms. All invoices are due and payable within thirty (30) days "
            "of the invoice date. Late payments shall bear interest at the lesser of one "
            "and one-half percent (1.5%) per month or the maximum rate permitted by applicable "
            "law. The liability for interest charges accrues from the original due date.\n\n"
            "3.3 Expenses. Client shall reimburse Provider for all reasonable travel, "
            "lodging, and out-of-pocket expenses incurred in connection with the performance "
            "of Services, provided that expenses exceeding Five Thousand Dollars ($5,000) "
            "per month require prior written approval from Client.\n\n"
            "3.4 Taxes. Client is responsible for all sales, use, and withholding taxes "
            "imposed on the Services or Deliverables provided under this Agreement. If "
            "Provider is required to collect or remit any such taxes, Client shall indemnify "
            "Provider against any resulting liability, including penalties and interest.\n\n"
            "3.5 Audit Rights. Provider shall maintain accurate records of all fees, expenses, "
            "and time incurred under this Agreement for a period of three (3) years."
        ),
    },
    # Page 5 - Intellectual Property (liability: 2, without limitation: 0)
    {
        "title": "ARTICLE 4: INTELLECTUAL PROPERTY RIGHTS",
        "body": (
            "4.1 Pre-Existing IP. Each party retains all rights, title, and interest in its "
            "pre-existing intellectual property. Nothing in this Agreement shall be construed "
            "as transferring ownership of either party's pre-existing intellectual property "
            "to the other party.\n\n"
            "4.2 Work Product Ownership. Subject to Section 4.1, all Deliverables and work "
            "product created by Provider specifically for Client under an Order Form shall be "
            "owned by Client upon full payment of all applicable fees. Provider hereby assigns "
            "to Client all right, title, and interest in such work product.\n\n"
            "4.3 Provider Tools. Notwithstanding Section 4.2, Provider retains ownership of "
            "all tools, methodologies, frameworks, and reusable components developed by Provider "
            "independently or prior to this Agreement ('Provider Tools'). Provider grants Client "
            "a non-exclusive, perpetual, royalty-free license to use any Provider Tools "
            "incorporated into the Deliverables. Any liability for intellectual property "
            "infringement claims related to Provider Tools shall be borne solely by Provider.\n\n"
            "4.4 Third-Party Components. Provider shall notify Client of any third-party "
            "components incorporated into the Deliverables and ensure appropriate licenses "
            "are obtained. Provider's liability for third-party component defects is limited "
            "to the extent Provider had knowledge of such defects at the time of delivery."
        ),
    },
    # Page 6 - Confidentiality (liability: 1, without limitation: 1)
    {
        "title": "ARTICLE 5: CONFIDENTIALITY",
        "body": (
            "5.1 Obligations. Each party agrees to: (a) hold the other party's Confidential "
            "Information in strict confidence; (b) not disclose such Confidential Information "
            "to any third party except as expressly permitted herein; and (c) use such "
            "Confidential Information only for the purposes of this Agreement.\n\n"
            "5.2 Permitted Disclosures. A receiving party may disclose Confidential Information "
            "to its employees, contractors, and advisors who have a need to know and who are "
            "bound by confidentiality obligations no less restrictive than those set forth herein.\n\n"
            "5.3 Exclusions. Confidential Information does not include information that: "
            "(a) is or becomes publicly available through no fault of the receiving party; "
            "(b) was rightfully in the receiving party's possession prior to disclosure; "
            "(c) is independently developed by the receiving party; or (d) is rightfully "
            "obtained from a third party without restriction.\n\n"
            "5.4 Remedies. The parties acknowledge that a breach of this Article may cause "
            "irreparable harm for which monetary damages may be inadequate. The non-breaching "
            "party shall be entitled to seek equitable relief, including injunctive relief, "
            "without limitation to any other remedies available at law or in equity. The "
            "liability for unauthorized disclosure extends to all direct and consequential "
            "damages suffered by the disclosing party."
        ),
    },
    # Page 7 - Warranties (liability: 2, without limitation: 0)
    {
        "title": "ARTICLE 6: REPRESENTATIONS AND WARRANTIES",
        "body": (
            "6.1 Mutual Representations. Each party represents and warrants that: (a) it is "
            "duly organized, validly existing, and in good standing under the laws of its "
            "jurisdiction of incorporation; (b) it has all necessary power and authority to "
            "enter into and perform this Agreement; and (c) the execution and performance "
            "of this Agreement does not conflict with any other agreement to which it is a party.\n\n"
            "6.2 Provider Warranties. Provider warrants that: (a) the Services will be "
            "performed in a professional manner consistent with industry standards; (b) the "
            "Deliverables will materially conform to the specifications set forth in the "
            "applicable Order Form for a period of ninety (90) days following acceptance; "
            "and (c) to Provider's knowledge, the Deliverables will not infringe any third-party "
            "intellectual property rights. Provider's sole liability for breach of warranty "
            "shall be, at Provider's option, to re-perform the non-conforming Services or "
            "refund the fees paid for such Services.\n\n"
            "6.3 Disclaimer. EXCEPT AS EXPRESSLY SET FORTH IN THIS AGREEMENT, NEITHER PARTY "
            "MAKES ANY WARRANTIES, EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF "
            "MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. This disclaimer does not "
            "affect any liability that cannot be excluded under applicable law."
        ),
    },
    # Page 8 - Limitation of Liability (liability: 3, without limitation: 1)
    {
        "title": "ARTICLE 7: LIMITATION OF LIABILITY",
        "body": (
            "7.1 Exclusion of Consequential Damages. In no event shall either party be "
            "liable to the other party for any indirect, incidental, special, consequential, "
            "or punitive damages arising out of or related to this Agreement, including "
            "without limitation damages for lost profits, lost revenue, loss of data, "
            "business interruption, or cost of substitute services, regardless of the theory "
            "of liability (whether in contract, tort, or otherwise) and even "
            "if such party has been advised of the possibility of such damages.\n\n"
            "7.2 Cap on Liability. Except for obligations under Article 5 (Confidentiality) "
            "and Article 8 (Indemnification), the total aggregate liability of either party "
            "under this Agreement shall not exceed the total fees paid or payable by Client "
            "to Provider during the twelve (12) month period immediately preceding the event "
            "giving rise to such claim.\n\n"
            "7.3 Essential Basis. The parties acknowledge that the limitations of liability "
            "set forth in this Article are an essential element of the bargain between the "
            "parties, and that in the absence of such limitations, the economic terms of this "
            "Agreement would be substantially different."
        ),
    },
    # Page 9 - Indemnification (liability: 1, without limitation: 0)
    {
        "title": "ARTICLE 8: INDEMNIFICATION",
        "body": (
            "8.1 Provider Indemnification. Provider shall defend, indemnify, and hold harmless "
            "Client and its officers, directors, employees, and agents from and against any "
            "third-party claims, damages, losses, and expenses (including reasonable attorneys' "
            "fees) arising out of: (a) Provider's breach of this Agreement; (b) Provider's "
            "negligence or willful misconduct; or (c) any claim that the Deliverables infringe "
            "a third-party's intellectual property rights.\n\n"
            "8.2 Client Indemnification. Client shall defend, indemnify, and hold harmless "
            "Provider and its officers, directors, employees, and agents from and against any "
            "third-party claims, damages, losses, and expenses (including reasonable attorneys' "
            "fees) arising out of: (a) Client's breach of this Agreement; (b) Client's "
            "negligence or willful misconduct; or (c) Client's use of the Deliverables in a "
            "manner not authorized under this Agreement.\n\n"
            "8.3 Indemnification Procedures. The indemnified party shall: (a) promptly notify "
            "the indemnifying party of any claim; (b) grant the indemnifying party sole control "
            "of the defense and settlement; and (c) provide reasonable cooperation at the "
            "indemnifying party's expense. The indemnifying party's total liability under this "
            "Article is subject to the limitations set forth in Article 7.\n\n"
            "8.4 Sole Remedy. This Article states the indemnifying party's sole and exclusive "
            "obligations with respect to third-party claims."
        ),
    },
    # Page 10 - General Provisions (liability: 2, without limitation: 0)
    {
        "title": "ARTICLE 9: GENERAL PROVISIONS",
        "body": (
            "9.1 Term and Termination. This Agreement shall commence on the Effective Date "
            "and continue for an initial term of three (3) years, unless earlier terminated. "
            "Either party may terminate this Agreement for cause upon thirty (30) days' written "
            "notice if the other party materially breaches this Agreement and fails to cure "
            "such breach within the notice period.\n\n"
            "9.2 Effect of Termination. Upon termination, Client shall pay all fees for "
            "Services performed through the termination date. Sections regarding Confidentiality, "
            "Intellectual Property, Limitation of Liability, Indemnification, and General "
            "Provisions shall survive termination.\n\n"
            "9.3 Governing Law. This Agreement shall be governed by and construed in accordance "
            "with the laws of the State of California, without regard to its conflict of "
            "laws principles.\n\n"
            "9.4 Dispute Resolution. Any dispute arising under this Agreement shall first be "
            "submitted to mediation. If mediation fails to resolve the dispute within sixty "
            "(60) days, either party may pursue resolution through binding arbitration in "
            "San Francisco, California, under the Commercial Arbitration Rules of the American "
            "Arbitration Association.\n\n"
            "9.5 Entire Agreement. This Agreement, together with all Order Forms and exhibits, "
            "constitutes the entire agreement between the parties with respect to its subject "
            "matter and supersedes all prior negotiations, representations, and agreements. "
            "No liability shall arise from any prior oral or written communications not "
            "incorporated into this Agreement.\n\n"
            "9.6 Severability. If any provision of this Agreement is held to be invalid or "
            "unenforceable, the remaining provisions shall continue in full force and effect."
        ),
    },
]


def build_pdf(output_path):
    """Build the legal document PDF."""
    doc = pymupdf.open()

    for i, page_content in enumerate(PAGES):
        page = doc.new_page(width=612, height=792)  # US Letter

        y = 72  # top margin

        # Title
        title = page_content["title"]
        page.insert_text(
            pymupdf.Point(72, y),
            title,
            fontsize=14,
            fontname="hebo",
            color=(0, 0, 0),
        )
        y += 30

        # Subtitle (only page 1)
        if "subtitle" in page_content:
            page.insert_text(
                pymupdf.Point(72, y),
                page_content["subtitle"],
                fontsize=11,
                fontname="heit",
                color=(0.3, 0.3, 0.3),
            )
            y += 25

        # Body text in a textbox
        body_rect = pymupdf.Rect(72, y, 540, 750)
        page.insert_textbox(
            body_rect,
            page_content["body"],
            fontsize=10,
            fontname="tiro",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

    doc.save(output_path)
    doc.close()


def create_initial():
    os.makedirs(LEGAL_DIR, exist_ok=True)

    build_pdf(OUTPUT)

    # Verify content
    doc = pymupdf.open(OUTPUT)
    full_text = ""
    liability_search_count = 0
    wl_search_count = 0
    for page in doc:
        full_text += page.get_text("text")
        liability_search_count += len(page.search_for("liability"))
        wl_search_count += len(page.search_for("without limitation"))
    doc.close()

    liability_count = full_text.lower().count("liability")
    wl_count = full_text.lower().count("without limitation")
    print(f"Initial file created: {OUTPUT}")
    print(f"Pages: 10")
    print(f"'liability' text count: {liability_count}")
    print(f"'liability' search_for count: {liability_search_count}")
    print(f"'without limitation' text count: {wl_count}")
    print(f"'without limitation' search_for count: {wl_search_count}")
    print(f"No annotations present.")

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
