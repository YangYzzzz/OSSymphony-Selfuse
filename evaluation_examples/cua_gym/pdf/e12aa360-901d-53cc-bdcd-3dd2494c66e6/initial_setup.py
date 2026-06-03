"""
Initial Setup: Create three contract section PDFs for merging task
Task ID: pdf_pw_001
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_001'
LEGAL_DIR = f'{WORKDIR}/legal'

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


def add_text_page(doc, title, paragraphs):
    """Add a page with a title and body paragraphs."""
    page = doc.new_page(width=W, height=H)
    y = 72

    # Title
    page.insert_text(pymupdf.Point(72, y), title, fontsize=16, fontname="hebo", color=(0, 0, 0))
    y += 30

    # Separator line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(W - 72, y))
    shape.finish(color=(0.3, 0.3, 0.3), width=1)
    shape.commit()
    y += 20

    # Body paragraphs
    for para in paragraphs:
        rect = pymupdf.Rect(72, y, W - 72, y + 80)
        excess = page.insert_textbox(rect, para, fontsize=10, fontname="helv",
                                     color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 85
        if y > H - 72:
            break

    return page


def create_scope_of_work():
    """Create scope_of_work.pdf with 4 pages."""
    doc = pymupdf.open()

    # Page 1 - Overview
    add_text_page(doc, "SCOPE OF WORK", [
        "This Scope of Work (\"SOW\") is entered into as of March 15, 2025, by and between "
        "Meridian Technology Solutions, Inc. (\"Provider\") and Cascade Financial Group, LLC "
        "(\"Client\"), collectively referred to as the \"Parties.\"",
        "1. PROJECT OVERVIEW: Provider shall deliver a comprehensive enterprise resource "
        "planning (ERP) system migration, transitioning Client's existing legacy infrastructure "
        "to a modern cloud-based platform. The engagement encompasses discovery, design, "
        "development, testing, deployment, and post-launch support phases.",
        "2. BACKGROUND: Cascade Financial Group currently operates on a legacy ERP system "
        "deployed in 2014. The system has reached end-of-life status and presents significant "
        "operational risks including security vulnerabilities, lack of vendor support, and "
        "inability to integrate with modern financial compliance frameworks.",
        "3. OBJECTIVES: The primary objectives of this engagement are to: (a) migrate all "
        "financial data to the new cloud platform with zero data loss, (b) achieve a 99.9% "
        "uptime SLA within the first 90 days post-launch, (c) reduce monthly operational "
        "costs by a minimum of 25%, and (d) ensure full SOC 2 Type II compliance.",
    ])

    # Page 2 - Deliverables
    add_text_page(doc, "DELIVERABLES AND MILESTONES", [
        "4. PHASE 1 - DISCOVERY (Weeks 1-4): Provider shall conduct a thorough assessment "
        "of Client's current infrastructure, including: inventory of all data assets and schemas, "
        "mapping of 847 active business processes, identification of 23 critical integration "
        "endpoints, and documentation of compliance requirements across 6 regulatory frameworks.",
        "5. PHASE 2 - DESIGN (Weeks 5-10): Provider shall deliver comprehensive architecture "
        "documents including system topology diagrams, data migration strategy with rollback "
        "procedures, API gateway specifications for all integration points, and user access "
        "control matrices aligned with Client's organizational hierarchy of 1,200 employees.",
        "6. PHASE 3 - DEVELOPMENT (Weeks 11-24): Custom module development shall include: "
        "accounts receivable automation module, multi-currency settlement engine supporting "
        "14 currencies, real-time compliance monitoring dashboard, and executive reporting "
        "suite with predictive analytics capabilities.",
        "7. PHASE 4 - TESTING (Weeks 25-30): Testing protocols shall encompass unit testing "
        "with minimum 95% code coverage, integration testing across all 23 endpoints, "
        "performance testing under simulated peak loads of 10,000 concurrent users, "
        "and user acceptance testing with designated Client stakeholders.",
    ])

    # Page 3 - Resources and Timeline
    add_text_page(doc, "RESOURCE ALLOCATION AND TIMELINE", [
        "8. TEAM COMPOSITION: Provider shall assign the following dedicated resources: "
        "1 Senior Project Manager (Elena Rodriguez, PMP), 2 Solution Architects (Raj Patel, "
        "David Kim), 4 Senior Developers, 2 QA Engineers, 1 Database Administrator, "
        "1 Security Specialist, and 1 DevOps Engineer. Total team size: 12 FTE.",
        "9. CLIENT RESPONSIBILITIES: Client shall provide: (a) dedicated project liaison "
        "(Sarah Mitchell, VP of Operations), (b) access to all legacy systems within 5 "
        "business days of contract execution, (c) timely feedback on deliverables within "
        "the review windows specified in Section 7, (d) executive sponsorship for change "
        "management activities, and (e) a testing environment mirroring production.",
        "10. TIMELINE: The total project duration is estimated at 38 weeks from the "
        "effective date. Key milestones include: Discovery Complete (Week 4), Design "
        "Approval (Week 10), Development Complete (Week 24), UAT Sign-off (Week 30), "
        "Go-Live (Week 34), and Hypercare Period End (Week 38).",
        "11. CHANGE MANAGEMENT: Any modifications to this SOW must be documented via "
        "a formal Change Request form, approved by both Parties' authorized representatives, "
        "and may result in adjustments to timeline, budget, and resource allocation.",
    ])

    # Page 4 - Budget Summary
    add_text_page(doc, "BUDGET SUMMARY", [
        "12. FIXED-PRICE COMPONENTS: Discovery Phase: $125,000. Design Phase: $185,000. "
        "Development Phase: $620,000. Testing Phase: $145,000. Deployment and Go-Live: "
        "$95,000. Total Fixed Price: $1,170,000.",
        "13. TIME AND MATERIALS: Post-launch hypercare support shall be billed at the "
        "following rates: Senior Consultant $275/hour, Technical Consultant $225/hour, "
        "Junior Consultant $165/hour. Estimated hypercare budget: $80,000 - $120,000 "
        "based on projected 400-550 support hours.",
        "14. PAYMENT SCHEDULE: 20% upon contract execution ($234,000), 15% upon Design "
        "Approval ($175,500), 30% upon Development Complete ($351,000), 20% upon UAT "
        "Sign-off ($234,000), 15% upon Go-Live ($175,500). All invoices net 30.",
        "15. EXPENSES: Travel expenses for on-site workshops (estimated 6 trips) shall be "
        "reimbursed at actual cost, not to exceed $35,000 total. All travel requires "
        "prior written approval from Client's project liaison.",
    ])

    doc.save(f'{LEGAL_DIR}/scope_of_work.pdf')
    doc.close()
    print(f'Created: {LEGAL_DIR}/scope_of_work.pdf (4 pages)')


def create_terms_conditions():
    """Create terms_conditions.pdf with 6 pages."""
    doc = pymupdf.open()

    # Page 1 - General Terms
    add_text_page(doc, "TERMS AND CONDITIONS", [
        "GENERAL TERMS AND CONDITIONS governing the Master Services Agreement between "
        "Meridian Technology Solutions, Inc. (\"Provider\") and Cascade Financial Group, LLC "
        "(\"Client\"), effective as of March 15, 2025.",
        "ARTICLE I - DEFINITIONS: \"Confidential Information\" means any proprietary data, "
        "trade secrets, business strategies, customer lists, financial records, source code, "
        "algorithms, and any information marked as confidential or that a reasonable person "
        "would understand to be confidential given the nature of the information.",
        "\"Deliverables\" means all work products, documentation, software code, configurations, "
        "reports, and materials produced by Provider in the performance of the Services as "
        "described in the applicable Statement of Work.",
        "\"Intellectual Property Rights\" means all patents, copyrights, trademarks, trade "
        "secrets, moral rights, rights of publicity, and any other intellectual or industrial "
        "property rights, whether registered or unregistered, throughout the world.",
    ])

    # Page 2 - Confidentiality
    add_text_page(doc, "ARTICLE II - CONFIDENTIALITY", [
        "2.1 OBLIGATIONS: Each Party agrees to: (a) maintain the confidentiality of the "
        "other Party's Confidential Information using the same degree of care it uses for "
        "its own confidential information, but no less than reasonable care; (b) not disclose "
        "Confidential Information to any third party without prior written consent; (c) limit "
        "access to Confidential Information to employees and contractors with a legitimate "
        "need to know; and (d) promptly notify the disclosing Party of any unauthorized "
        "disclosure or use.",
        "2.2 EXCEPTIONS: Confidential Information does not include information that: (a) is "
        "or becomes publicly available through no fault of the receiving Party; (b) was "
        "rightfully in the receiving Party's possession before disclosure; (c) is independently "
        "developed without use of or reference to Confidential Information; or (d) is "
        "required to be disclosed by law, regulation, or court order, provided the receiving "
        "Party gives prompt written notice to allow the disclosing Party to seek a protective order.",
        "2.3 DURATION: Confidentiality obligations shall survive termination of this Agreement "
        "for a period of five (5) years, except with respect to trade secrets, which shall be "
        "protected for as long as they remain trade secrets under applicable law.",
        "2.4 RETURN OF MATERIALS: Upon termination or expiration, each Party shall return or "
        "destroy all Confidential Information in its possession within thirty (30) days and "
        "provide written certification of such return or destruction.",
    ])

    # Page 3 - Warranties
    add_text_page(doc, "ARTICLE III - WARRANTIES AND REPRESENTATIONS", [
        "3.1 PROVIDER WARRANTIES: Provider represents and warrants that: (a) all Services "
        "shall be performed in a professional and workmanlike manner consistent with generally "
        "accepted industry standards; (b) all Deliverables shall conform to the specifications "
        "set forth in the applicable SOW; (c) Provider has full power and authority to enter "
        "into this Agreement; (d) the Services and Deliverables will not infringe upon any "
        "third party's intellectual property rights.",
        "3.2 WARRANTY PERIOD: Provider shall correct any Deliverable that fails to conform "
        "to specifications during the warranty period of ninety (90) days following acceptance. "
        "Corrections shall be provided at no additional cost to Client.",
        "3.3 CLIENT WARRANTIES: Client represents and warrants that: (a) it has the authority "
        "to enter into this Agreement; (b) it will provide accurate and complete information "
        "as reasonably requested by Provider; (c) it has obtained all necessary internal "
        "approvals for the engagement.",
        "3.4 DISCLAIMER: EXCEPT AS EXPRESSLY SET FORTH HEREIN, PROVIDER MAKES NO WARRANTIES, "
        "EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO IMPLIED WARRANTIES OF MERCHANTABILITY, "
        "FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. PROVIDER DOES NOT WARRANT "
        "THAT SERVICES WILL BE UNINTERRUPTED OR ERROR-FREE.",
    ])

    # Page 4 - Liability
    add_text_page(doc, "ARTICLE IV - LIMITATION OF LIABILITY", [
        "4.1 CAP ON LIABILITY: EXCEPT FOR BREACHES OF CONFIDENTIALITY OBLIGATIONS, "
        "INDEMNIFICATION OBLIGATIONS, AND WILLFUL MISCONDUCT, NEITHER PARTY'S AGGREGATE "
        "LIABILITY UNDER THIS AGREEMENT SHALL EXCEED THE TOTAL FEES PAID OR PAYABLE TO "
        "PROVIDER UNDER THE APPLICABLE SOW DURING THE TWELVE (12) MONTH PERIOD IMMEDIATELY "
        "PRECEDING THE EVENT GIVING RISE TO THE CLAIM.",
        "4.2 EXCLUSION OF DAMAGES: IN NO EVENT SHALL EITHER PARTY BE LIABLE FOR ANY "
        "INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING BUT "
        "NOT LIMITED TO LOSS OF PROFITS, LOSS OF DATA, LOSS OF BUSINESS OPPORTUNITY, OR "
        "COST OF PROCUREMENT OF SUBSTITUTE SERVICES, REGARDLESS OF THE CAUSE OF ACTION OR "
        "THE THEORY OF LIABILITY, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.",
        "4.3 EXCEPTIONS: The limitations set forth in Sections 4.1 and 4.2 shall not apply "
        "to: (a) either Party's indemnification obligations; (b) breaches of confidentiality "
        "obligations exceeding $2,000,000; (c) Provider's obligation to pay damages for "
        "willful infringement of Client's intellectual property rights; or (d) damages arising "
        "from either Party's gross negligence or willful misconduct.",
        "4.4 ESSENTIAL BASIS: The Parties acknowledge that the limitations of liability set "
        "forth in this Article reflect the allocation of risk between the Parties and form "
        "an essential basis of the bargain between them.",
    ])

    # Page 5 - Indemnification
    add_text_page(doc, "ARTICLE V - INDEMNIFICATION", [
        "5.1 PROVIDER INDEMNIFICATION: Provider shall defend, indemnify, and hold harmless "
        "Client and its officers, directors, employees, and agents from and against any "
        "third-party claims, actions, demands, losses, damages, liabilities, costs, and "
        "expenses (including reasonable attorneys' fees) arising out of or relating to: "
        "(a) any alleged infringement of intellectual property rights by the Deliverables; "
        "(b) Provider's breach of its confidentiality obligations; (c) personal injury or "
        "property damage caused by Provider's employees or contractors while on Client premises.",
        "5.2 CLIENT INDEMNIFICATION: Client shall defend, indemnify, and hold harmless "
        "Provider and its officers, directors, employees, and agents from and against any "
        "third-party claims arising out of or relating to: (a) Client's use of the "
        "Deliverables in a manner not contemplated by this Agreement; (b) Client's breach "
        "of its confidentiality obligations; (c) any content, data, or materials provided "
        "by Client that infringe upon third-party rights.",
        "5.3 INDEMNIFICATION PROCEDURES: The indemnified Party shall: (a) promptly notify "
        "the indemnifying Party in writing of any claim; (b) grant the indemnifying Party "
        "sole control of the defense and settlement; (c) provide reasonable cooperation at "
        "the indemnifying Party's expense. Failure to provide timely notice shall not relieve "
        "the indemnifying Party except to the extent prejudiced by such failure.",
        "5.4 MITIGATION: Upon notice of an infringement claim, Provider may at its option: "
        "(a) modify the Deliverables to be non-infringing while maintaining material "
        "functionality; (b) obtain a license for continued use; or (c) if neither option is "
        "commercially reasonable, terminate the affected SOW and refund fees paid for the "
        "infringing Deliverables pro rata.",
    ])

    # Page 6 - Termination
    add_text_page(doc, "ARTICLE VI - TERMINATION AND DISPUTE RESOLUTION", [
        "6.1 TERMINATION FOR CONVENIENCE: Either Party may terminate this Agreement upon "
        "sixty (60) days' prior written notice. Upon termination for convenience, Client "
        "shall pay Provider for all Services rendered and expenses incurred through the "
        "effective date of termination, plus any non-cancelable commitments made by Provider "
        "on Client's behalf.",
        "6.2 TERMINATION FOR CAUSE: Either Party may terminate this Agreement immediately "
        "upon written notice if the other Party: (a) materially breaches this Agreement and "
        "fails to cure such breach within thirty (30) days of written notice; (b) becomes "
        "insolvent, files for bankruptcy, or has a receiver appointed for a substantial "
        "portion of its assets; or (c) ceases to conduct business in the normal course.",
        "6.3 DISPUTE RESOLUTION: Any dispute arising under this Agreement shall be resolved "
        "as follows: (a) the Parties shall first attempt to resolve the dispute through good "
        "faith negotiation between senior executives for a period of thirty (30) days; "
        "(b) if negotiation fails, the Parties shall submit to binding mediation administered "
        "by the American Arbitration Association; (c) if mediation fails within sixty (60) "
        "days, either Party may pursue litigation in the state or federal courts located in "
        "King County, Washington.",
        "6.4 GOVERNING LAW: This Agreement shall be governed by and construed in accordance "
        "with the laws of the State of Washington, without regard to its conflict of laws "
        "principles. The United Nations Convention on Contracts for the International Sale "
        "of Goods shall not apply to this Agreement.",
    ])

    doc.save(f'{LEGAL_DIR}/terms_conditions.pdf')
    doc.close()
    print(f'Created: {LEGAL_DIR}/terms_conditions.pdf (6 pages)')


def create_signature_page():
    """Create signature_page.pdf with 1 page."""
    doc = pymupdf.open()
    page = doc.new_page(width=W, height=H)

    # Title
    page.insert_text(pymupdf.Point(72, 72), "SIGNATURE PAGE", fontsize=16, fontname="hebo",
                     color=(0, 0, 0))

    # Separator
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 95), pymupdf.Point(W - 72, 95))
    shape.finish(color=(0.3, 0.3, 0.3), width=1)
    shape.commit()

    # Agreement statement
    rect = pymupdf.Rect(72, 115, W - 72, 195)
    page.insert_textbox(rect,
        "IN WITNESS WHEREOF, the Parties hereto have caused this Agreement to be executed "
        "by their duly authorized representatives as of the date first written above. Each "
        "signatory represents and warrants that they have the authority to bind their "
        "respective organization to the terms and conditions set forth herein.",
        fontsize=10, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Provider signature block
    y_block = 240
    page.insert_text(pymupdf.Point(72, y_block), "MERIDIAN TECHNOLOGY SOLUTIONS, INC.",
                     fontsize=11, fontname="hebo", color=(0, 0, 0))
    y_block += 50
    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(72, y_block), pymupdf.Point(300, y_block))
    shape2.finish(color=(0, 0, 0), width=0.5)
    shape2.commit()
    page.insert_text(pymupdf.Point(72, y_block + 15), "Signature", fontsize=9, fontname="helv",
                     color=(0.4, 0.4, 0.4))
    y_block += 40
    page.insert_text(pymupdf.Point(72, y_block), "Name: James Thornton",
                     fontsize=10, fontname="helv", color=(0, 0, 0))
    y_block += 18
    page.insert_text(pymupdf.Point(72, y_block), "Title: Chief Executive Officer",
                     fontsize=10, fontname="helv", color=(0, 0, 0))
    y_block += 18
    page.insert_text(pymupdf.Point(72, y_block), "Date: _______________",
                     fontsize=10, fontname="helv", color=(0, 0, 0))

    # Client signature block
    y_block = 440
    page.insert_text(pymupdf.Point(72, y_block), "CASCADE FINANCIAL GROUP, LLC",
                     fontsize=11, fontname="hebo", color=(0, 0, 0))
    y_block += 50
    shape3 = page.new_shape()
    shape3.draw_line(pymupdf.Point(72, y_block), pymupdf.Point(300, y_block))
    shape3.finish(color=(0, 0, 0), width=0.5)
    shape3.commit()
    page.insert_text(pymupdf.Point(72, y_block + 15), "Signature", fontsize=9, fontname="helv",
                     color=(0.4, 0.4, 0.4))
    y_block += 40
    page.insert_text(pymupdf.Point(72, y_block), "Name: Victoria Ashford",
                     fontsize=10, fontname="helv", color=(0, 0, 0))
    y_block += 18
    page.insert_text(pymupdf.Point(72, y_block), "Title: Managing Partner",
                     fontsize=10, fontname="helv", color=(0, 0, 0))
    y_block += 18
    page.insert_text(pymupdf.Point(72, y_block), "Date: _______________",
                     fontsize=10, fontname="helv", color=(0, 0, 0))

    doc.save(f'{LEGAL_DIR}/signature_page.pdf')
    doc.close()
    print(f'Created: {LEGAL_DIR}/signature_page.pdf (1 page)')


def create_initial():
    os.makedirs(LEGAL_DIR, exist_ok=True)

    create_scope_of_work()
    create_terms_conditions()
    create_signature_page()

    # Open the first source PDF in Evince for the agent
    launch_gui(f'evince "{LEGAL_DIR}/scope_of_work.pdf"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
