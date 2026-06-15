"""
Initial Setup: Create two contract PDF versions for comparison task
Task ID: pdf_legal_023
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_023'
LEGAL_DIR = f'{WORKDIR}/legal'
V1_PATH = f'{LEGAL_DIR}/contract_v1.pdf'
V2_PATH = f'{LEGAL_DIR}/contract_v2.pdf'

# Page dimensions
PAGE_W, PAGE_H = 612, 792  # Letter size

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

# --- Contract content definition ---
# We define sections that will populate both contracts.
# V2 has specific differences from V1.

HEADER_TITLE = "PROFESSIONAL SERVICES AGREEMENT"
HEADER_SUBTITLE = "Between Meridian Technologies Inc. and Apex Solutions Group LLC"

# Each section: (heading, body_text)
# We'll have enough sections to fill 18 pages for V1 and 19 pages for V2

SECTIONS_COMMON = [
    # Page 1: Title page content
    ("1. DEFINITIONS AND INTERPRETATION",
     """1.1 In this Agreement, unless the context otherwise requires, the following terms shall have the meanings set forth below:\n\n"Affiliate" means any entity that directly or indirectly controls, is controlled by, or is under common control with a party to this Agreement, where "control" means the ownership of more than fifty percent (50%) of the voting securities or equivalent ownership interest.\n\n"Business Day" means any day other than a Saturday, Sunday, or federal holiday recognized in the State of Delaware.\n\n"Change Order" means a written document signed by both parties that modifies the scope, timeline, or compensation of any Statement of Work.\n\n"Confidential Information" means all non-public information disclosed by either party to the other, whether orally, in writing, or by inspection, that is designated as confidential or that reasonably should be understood to be confidential given the nature of the information and the circumstances of disclosure.\n\n"Deliverables" means the tangible and intangible work products to be delivered by Service Provider as specified in each Statement of Work.\n\n"Effective Date" means March 15, 2025, the date upon which this Agreement becomes binding upon the parties.\n\n"Intellectual Property Rights" means all patents, copyrights, trademarks, trade secrets, and other proprietary rights recognized under applicable law."""),

    ("2. SCOPE OF SERVICES",
     """2.1 Service Provider shall provide the professional services described in each Statement of Work ("SOW") executed by both parties pursuant to this Agreement. Each SOW shall be incorporated into and governed by the terms and conditions of this Agreement.\n\n2.2 Service Provider shall perform all Services in a professional and workmanlike manner, consistent with generally accepted industry standards and practices. Service Provider shall assign qualified personnel with appropriate skills and experience to perform the Services.\n\n2.3 Service Provider shall designate a project manager who shall serve as the primary point of contact for all communications related to the Services. The project manager shall be available during normal business hours and shall respond to Client inquiries within one (1) Business Day.\n\n2.4 Any changes to the scope of Services must be documented in a Change Order signed by authorized representatives of both parties. No additional compensation shall be due for work performed outside an approved SOW unless authorized by a Change Order.\n\n2.5 Service Provider acknowledges that time is of the essence with respect to the performance of Services and delivery of Deliverables as specified in each SOW. Service Provider shall promptly notify Client of any anticipated delays."""),

    ("3. COMPENSATION AND PAYMENT TERMS",
     """3.1 Client shall pay Service Provider the fees specified in each Statement of Work. Unless otherwise stated in the applicable SOW, fees shall be calculated on a time-and-materials basis at the rates set forth in Exhibit A attached hereto.\n\n3.2 Service Provider shall submit detailed invoices on a monthly basis, no later than the fifteenth (15th) day of the month following the month in which Services were performed. Each invoice shall include a description of Services rendered, the number of hours worked by each assigned resource, and the applicable hourly rate.\n\n3.3 Client shall pay undisputed invoices within thirty (30) days of receipt. Late payments shall accrue interest at the rate of one and one-half percent (1.5%) per month, or the maximum rate permitted by applicable law, whichever is less.\n\n3.4 Client may dispute any invoice or portion thereof in good faith by providing written notice to Service Provider within fifteen (15) days of receipt, specifying the basis for the dispute. The parties shall work in good faith to resolve any billing disputes within thirty (30) days.\n\n3.5 Service Provider shall be responsible for all taxes arising from the compensation paid under this Agreement, except for taxes based on Client's income. Service Provider shall indemnify Client against any claims related to Service Provider's tax obligations."""),

    ("4. TERM AND TERMINATION",
     """4.1 This Agreement shall commence on the Effective Date and continue for a period of three (3) years, unless earlier terminated in accordance with this Section 4 (the "Initial Term"). Thereafter, this Agreement shall automatically renew for successive one (1) year periods (each a "Renewal Term"), unless either party provides written notice of non-renewal at least ninety (90) days prior to the expiration of the then-current term.\n\n4.2 Either party may terminate this Agreement for cause upon thirty (30) days written notice if the other party materially breaches any provision of this Agreement and fails to cure such breach within the notice period.\n\n4.3 Client may terminate any Statement of Work for convenience upon sixty (60) days prior written notice to Service Provider. In such event, Client shall pay Service Provider for all Services performed through the effective date of termination, plus any non-cancelable costs incurred by Service Provider in reliance on the SOW.\n\n4.4 Either party may terminate this Agreement immediately upon written notice if the other party becomes insolvent, files a petition in bankruptcy, makes an assignment for the benefit of creditors, or has a receiver appointed for a substantial portion of its assets.\n\n4.5 Upon termination or expiration, Service Provider shall promptly deliver to Client all Deliverables completed or in progress, together with all Client Confidential Information and materials."""),

    ("5. INTELLECTUAL PROPERTY",
     """5.1 All Deliverables created by Service Provider in the performance of Services under this Agreement shall be considered "works made for hire" as defined under the United States Copyright Act. To the extent any Deliverable does not qualify as a work made for hire, Service Provider hereby irrevocably assigns to Client all right, title, and interest in and to such Deliverable, including all Intellectual Property Rights therein.\n\n5.2 Service Provider retains all right, title, and interest in any pre-existing intellectual property owned by Service Provider prior to the Effective Date or developed independently outside the scope of this Agreement ("Service Provider IP"). To the extent any Service Provider IP is incorporated into a Deliverable, Service Provider hereby grants Client a non-exclusive, perpetual, irrevocable, worldwide, royalty-free license to use, modify, and distribute such Service Provider IP solely as part of the Deliverable.\n\n5.3 Client retains all right, title, and interest in its pre-existing intellectual property ("Client IP"). Client grants Service Provider a limited, non-exclusive license to use Client IP solely to the extent necessary for the performance of Services under this Agreement.\n\n5.4 Neither party shall use the other party's trademarks, trade names, or logos without prior written consent, except that either party may identify the other as a client or service provider in marketing materials, subject to the other party's branding guidelines."""),

    ("6. CONFIDENTIALITY",
     """6.1 Each party agrees to hold the other party's Confidential Information in strict confidence and not to disclose such information to any third party without the prior written consent of the disclosing party, except to employees, contractors, and advisors who have a need to know and are bound by confidentiality obligations no less restrictive than those contained herein.\n\n6.2 The obligations of confidentiality shall not apply to information that: (a) is or becomes publicly available through no fault of the receiving party; (b) was already known to the receiving party prior to disclosure; (c) is independently developed by the receiving party without use of or reference to the disclosing party's Confidential Information; or (d) is lawfully received from a third party without restriction on disclosure.\n\n6.3 If the receiving party is required by law, regulation, or court order to disclose Confidential Information, the receiving party shall provide the disclosing party with prompt written notice of such requirement and shall cooperate with the disclosing party's efforts to obtain a protective order or other appropriate remedy.\n\n6.4 Upon termination of this Agreement, each party shall return or destroy all Confidential Information of the other party in its possession, except for copies retained in accordance with the receiving party's standard backup procedures or as required by applicable law.\n\n6.5 The obligations of confidentiality shall survive termination of this Agreement for a period of five (5) years from the date of disclosure of the applicable Confidential Information."""),

    ("7. REPRESENTATIONS AND WARRANTIES",
     """7.1 Service Provider represents and warrants that: (a) it has the legal right and authority to enter into this Agreement and perform its obligations hereunder; (b) the Services will be performed in a professional and workmanlike manner by qualified personnel; (c) the Deliverables will conform to the specifications set forth in the applicable SOW; (d) the Deliverables will not infringe upon any third party's Intellectual Property Rights; and (e) Service Provider will comply with all applicable laws and regulations in the performance of Services.\n\n7.2 Client represents and warrants that: (a) it has the legal right and authority to enter into this Agreement; (b) it will provide Service Provider with reasonable access to information, systems, and personnel necessary for the performance of Services; and (c) all Client IP provided to Service Provider is owned by or properly licensed to Client.\n\n7.3 EXCEPT AS EXPRESSLY SET FORTH IN THIS AGREEMENT, NEITHER PARTY MAKES ANY WARRANTIES, EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.\n\n7.4 Service Provider warrants that all Deliverables shall be free from material defects for a period of ninety (90) days following acceptance by Client. During this warranty period, Service Provider shall correct any material defects at no additional charge to Client."""),

    ("8. INDEMNIFICATION",
     """8.1 Service Provider shall indemnify, defend, and hold harmless Client and its officers, directors, employees, and agents from and against any and all third-party claims, damages, losses, costs, and expenses (including reasonable attorneys' fees) arising from or related to: (a) any breach by Service Provider of its representations, warranties, or obligations under this Agreement; (b) any negligent or willful act or omission of Service Provider or its personnel in the performance of Services; or (c) any claim that any Deliverable infringes a third party's Intellectual Property Rights.\n\n8.2 Client shall indemnify, defend, and hold harmless Service Provider and its officers, directors, employees, and agents from and against any and all third-party claims, damages, losses, costs, and expenses (including reasonable attorneys' fees) arising from or related to: (a) any breach by Client of its representations, warranties, or obligations under this Agreement; (b) any negligent or willful act or omission of Client in connection with this Agreement; or (c) any claim arising from Client's use of Deliverables in a manner not authorized under this Agreement.\n\n8.3 The indemnifying party's obligations under this Section 8 are conditioned upon the indemnified party: (a) providing prompt written notice of any claim; (b) granting the indemnifying party sole control of the defense and settlement of such claim; and (c) providing reasonable cooperation at the indemnifying party's expense.\n\n8.4 The indemnifying party shall not settle any claim that imposes any obligation on the indemnified party without the indemnified party's prior written consent, which shall not be unreasonably withheld."""),

    ("9. LIMITATION OF LIABILITY",
     """9.1 IN NO EVENT SHALL EITHER PARTY BE LIABLE TO THE OTHER FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING WITHOUT LIMITATION LOST PROFITS, LOST REVENUE, LOST DATA, OR BUSINESS INTERRUPTION, REGARDLESS OF THE THEORY OF LIABILITY AND EVEN IF SUCH PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.\n\n9.2 EXCEPT FOR OBLIGATIONS ARISING UNDER SECTIONS 6 (CONFIDENTIALITY), 8 (INDEMNIFICATION), AND EITHER PARTY'S WILLFUL MISCONDUCT OR GROSS NEGLIGENCE, THE TOTAL AGGREGATE LIABILITY OF EITHER PARTY UNDER THIS AGREEMENT SHALL NOT EXCEED THE TOTAL FEES PAID OR PAYABLE BY CLIENT TO SERVICE PROVIDER DURING THE TWELVE (12) MONTH PERIOD IMMEDIATELY PRECEDING THE EVENT GIVING RISE TO THE CLAIM.\n\n9.3 The limitations of liability set forth in this Section 9 shall apply to the fullest extent permitted by applicable law and shall survive the termination or expiration of this Agreement.\n\n9.4 Each party acknowledges that the limitations of liability set forth in this Section 9 reflect the allocation of risk between the parties and form an essential basis of the bargain between them."""),

    ("10. INSURANCE",
     """10.1 Service Provider shall maintain, at its own expense, the following insurance coverage throughout the term of this Agreement:\n\n(a) Commercial General Liability insurance with limits of not less than Two Million Dollars ($2,000,000) per occurrence and Four Million Dollars ($4,000,000) in the aggregate;\n\n(b) Professional Liability (Errors and Omissions) insurance with limits of not less than Five Million Dollars ($5,000,000) per claim and Five Million Dollars ($5,000,000) in the aggregate;\n\n(c) Workers' Compensation insurance as required by applicable law, with Employer's Liability limits of not less than One Million Dollars ($1,000,000) per accident;\n\n(d) Cyber Liability insurance with limits of not less than Three Million Dollars ($3,000,000) per claim, covering data breaches, network security failures, and technology errors and omissions.\n\n10.2 All insurance policies shall be issued by carriers with an AM Best rating of A- VII or better. Service Provider shall name Client as an additional insured on its Commercial General Liability policy.\n\n10.3 Service Provider shall provide Client with certificates of insurance evidencing the required coverage upon execution of this Agreement and annually thereafter. Service Provider shall provide at least thirty (30) days prior written notice of any material change or cancellation of coverage."""),

    ("11. DATA PROTECTION AND SECURITY",
     """11.1 Service Provider shall implement and maintain appropriate technical and organizational measures to protect Client data against unauthorized access, disclosure, alteration, or destruction. Such measures shall be consistent with industry best practices and shall comply with all applicable data protection laws and regulations.\n\n11.2 Service Provider shall not process, transfer, or store Client data outside the United States without Client's prior written consent. Where international data transfers are authorized, Service Provider shall ensure appropriate safeguards are in place as required by applicable law.\n\n11.3 In the event of a data breach affecting Client data, Service Provider shall notify Client in writing within seventy-two (72) hours of becoming aware of the breach. The notification shall include a description of the nature of the breach, the categories and approximate number of data records affected, and the measures taken or proposed to address the breach.\n\n11.4 Service Provider shall cooperate fully with Client in the investigation and remediation of any data breach and shall bear all costs associated with notification requirements and credit monitoring services if the breach resulted from Service Provider's negligence or failure to comply with its obligations under this Agreement.\n\n11.5 Upon termination of this Agreement, Service Provider shall securely delete or return all Client data within thirty (30) days and provide written certification of such deletion upon request."""),

    ("12. DISPUTE RESOLUTION",
     """12.1 The parties shall attempt to resolve any dispute arising out of or relating to this Agreement through good faith negotiation. If the dispute cannot be resolved within thirty (30) days, either party may escalate the matter to senior management of both parties for resolution.\n\n12.2 If the dispute remains unresolved after an additional thirty (30) days of senior management discussions, the parties agree to submit the dispute to binding arbitration administered by the American Arbitration Association in accordance with its Commercial Arbitration Rules. The arbitration shall be conducted in Wilmington, Delaware by a single arbitrator selected in accordance with the AAA rules.\n\n12.3 The arbitrator shall have the authority to award any remedy that would be available in a court of competent jurisdiction, including injunctive relief and specific performance. The arbitrator's decision shall be final and binding, and judgment on the award may be entered in any court of competent jurisdiction.\n\n12.4 Notwithstanding the foregoing, either party may seek injunctive or other equitable relief from any court of competent jurisdiction to prevent irreparable harm pending the outcome of arbitration proceedings.\n\n12.5 Each party shall bear its own costs and expenses in connection with any dispute resolution proceedings, provided that the prevailing party shall be entitled to recover its reasonable attorneys' fees and costs from the non-prevailing party."""),

    ("13. FORCE MAJEURE",
     """13.1 Neither party shall be liable for any failure or delay in the performance of its obligations under this Agreement to the extent such failure or delay is caused by circumstances beyond its reasonable control, including but not limited to acts of God, natural disasters, epidemics, pandemics, government actions, war, terrorism, civil unrest, fire, flood, earthquake, power outages, telecommunications failures, or labor disputes ("Force Majeure Event").\n\n13.2 The affected party shall provide written notice to the other party within five (5) Business Days of becoming aware of a Force Majeure Event, describing the nature and expected duration of the event and its impact on the affected party's obligations.\n\n13.3 The affected party shall use commercially reasonable efforts to mitigate the effects of the Force Majeure Event and resume performance of its obligations as soon as practicable.\n\n13.4 If a Force Majeure Event continues for more than ninety (90) consecutive days, either party may terminate the affected Statement of Work upon written notice to the other party. In such event, Client shall pay Service Provider for all Services performed through the date of termination."""),

    ("14. NON-SOLICITATION",
     """14.1 During the term of this Agreement and for a period of twelve (12) months following its termination or expiration, neither party shall, directly or indirectly, solicit or recruit for employment any employee of the other party who was involved in the performance or management of Services under this Agreement, without the prior written consent of the employing party.\n\n14.2 This restriction shall not apply to: (a) general solicitations of employment through advertisements or other public postings not specifically targeted at the other party's employees; or (b) hiring an individual who contacts the hiring party on his or her own initiative without any direct or indirect solicitation.\n\n14.3 In the event of a breach of this Section 14, the breaching party shall pay the non-breaching party liquidated damages equal to fifty percent (50%) of the hired employee's first-year annual compensation, which the parties agree represents a reasonable estimate of the damages that would be incurred."""),

    ("15. NOTICES",
     """15.1 All notices required or permitted under this Agreement shall be in writing and shall be deemed duly given when: (a) delivered personally; (b) sent by confirmed electronic mail; (c) sent by registered or certified mail, return receipt requested, postage prepaid; or (d) sent by nationally recognized overnight courier, in each case addressed as follows:\n\nIf to Client:\nMeridian Technologies Inc.\nAttn: General Counsel\n2400 Innovation Drive, Suite 800\nWilmington, Delaware 19801\nEmail: legal@meridiantech.com\n\nIf to Service Provider:\nApex Solutions Group LLC\nAttn: Contract Administration\n1750 K Street NW, Suite 1200\nWashington, DC 20006\nEmail: contracts@apexsolutions.com\n\n15.2 Either party may change its notice address by providing written notice to the other party in accordance with this Section 15.\n\n15.3 Notices sent by electronic mail shall be effective upon confirmed receipt by the intended recipient. Notices sent by mail shall be effective three (3) Business Days after deposit. Notices sent by overnight courier shall be effective on the next Business Day after deposit."""),

    ("16. GENERAL PROVISIONS",
     """16.1 Entire Agreement. This Agreement, together with all SOWs and exhibits attached hereto, constitutes the entire agreement between the parties with respect to the subject matter hereof and supersedes all prior and contemporaneous agreements, understandings, negotiations, and discussions, whether oral or written.\n\n16.2 Amendments. This Agreement may not be amended or modified except by a written instrument signed by authorized representatives of both parties.\n\n16.3 Waiver. No waiver of any provision of this Agreement shall be effective unless in writing and signed by the party against whom the waiver is sought to be enforced. No failure or delay in exercising any right shall constitute a waiver thereof.\n\n16.4 Severability. If any provision of this Agreement is held to be invalid, illegal, or unenforceable, the remaining provisions shall continue in full force and effect, and the invalid provision shall be reformed to the minimum extent necessary to make it valid and enforceable.\n\n16.5 Assignment. Neither party may assign this Agreement or any of its rights or obligations hereunder without the prior written consent of the other party, except that either party may assign this Agreement to a successor in connection with a merger, acquisition, or sale of all or substantially all of its assets.\n\n16.6 Governing Law. This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without regard to its conflict of laws principles.\n\n16.7 Counterparts. This Agreement may be executed in counterparts, each of which shall be deemed an original, and all of which together shall constitute one and the same instrument.\n\n16.8 Survival. The provisions of Sections 5, 6, 7, 8, 9, and 14 shall survive the termination or expiration of this Agreement."""),
]

# Define the 12 differences between V1 and V2
# Format: (section_index, description, v1_text_fragment, v2_text_fragment)
DIFFERENCES = [
    # Diff 1: Section 1 - Definition of Effective Date
    (0, "Effective Date changed",
     'Effective Date" means March 15, 2025',
     'Effective Date" means April 1, 2025'),

    # Diff 2: Section 2 - Response time
    (1, "Response time changed",
     "respond to Client inquiries within one (1) Business Day",
     "respond to Client inquiries within two (2) Business Days"),

    # Diff 3: Section 3 - Payment terms
    (2, "Payment terms extended",
     "pay undisputed invoices within thirty (30) days of receipt",
     "pay undisputed invoices within forty-five (45) days of receipt"),

    # Diff 4: Section 3 - Late payment interest rate
    (2, "Late payment interest rate changed",
     "one and one-half percent (1.5%) per month",
     "one percent (1.0%) per month"),

    # Diff 5: Section 4 - Initial term duration
    (3, "Initial term duration changed",
     "continue for a period of three (3) years",
     "continue for a period of two (2) years"),

    # Diff 6: Section 4 - Termination notice period
    (3, "Termination notice changed",
     "terminate any Statement of Work for convenience upon sixty (60) days",
     "terminate any Statement of Work for convenience upon forty-five (45) days"),

    # Diff 7: Section 7 - Warranty period
    (6, "Warranty period changed",
     "free from material defects for a period of ninety (90) days",
     "free from material defects for a period of one hundred twenty (120) days"),

    # Diff 8: Section 10 - General liability limits
    (9, "General liability limit changed",
     "Two Million Dollars ($2,000,000) per occurrence and Four Million Dollars ($4,000,000)",
     "Three Million Dollars ($3,000,000) per occurrence and Six Million Dollars ($6,000,000)"),

    # Diff 9: Section 10 - Cyber liability limits
    (9, "Cyber liability limit changed",
     "Three Million Dollars ($3,000,000) per claim",
     "Five Million Dollars ($5,000,000) per claim"),

    # Diff 10: Section 11 - Breach notification timeline
    (10, "Data breach notification timeline changed",
     "notify Client in writing within seventy-two (72) hours",
     "notify Client in writing within forty-eight (48) hours"),

    # Diff 11: Section 13 - Force majeure termination period
    (12, "Force majeure termination period changed",
     "continues for more than ninety (90) consecutive days",
     "continues for more than sixty (60) consecutive days"),

    # Diff 12: Section 14 - Non-solicitation period
    (13, "Non-solicitation period changed",
     "for a period of twelve (12) months",
     "for a period of eighteen (18) months"),
]

# V2 also has an additional section (17. AUDIT RIGHTS) that adds an extra page
V2_EXTRA_SECTION = ("17. AUDIT RIGHTS",
    """17.1 Client shall have the right, upon thirty (30) days prior written notice, to audit Service Provider's records and systems to verify compliance with the terms of this Agreement, including but not limited to invoicing accuracy, data security measures, and intellectual property ownership.\n\n17.2 Audits shall be conducted during normal business hours and shall not unreasonably interfere with Service Provider's operations. Client may engage a qualified independent third-party auditor to conduct such audits, provided that the auditor executes a confidentiality agreement acceptable to Service Provider.\n\n17.3 Service Provider shall cooperate fully with any audit and shall provide reasonable access to relevant records, personnel, and systems. If an audit reveals any material discrepancy or non-compliance, Service Provider shall promptly remedy the issue and bear the reasonable costs of the audit.\n\n17.4 Client's audit rights shall survive the termination or expiration of this Agreement for a period of three (3) years.\n\n17.5 Nothing in this Section 17 shall limit any other rights or remedies available to Client under this Agreement or applicable law.""")


def build_contract_text(version='v1'):
    """Build full section list for the given version."""
    sections = []
    for i, (heading, body) in enumerate(SECTIONS_COMMON):
        if version == 'v2':
            # Apply differences
            modified_body = body
            for diff_idx, desc, v1_frag, v2_frag in DIFFERENCES:
                if diff_idx == i:
                    modified_body = modified_body.replace(v1_frag, v2_frag)
            sections.append((heading, modified_body))
        else:
            sections.append((heading, body))

    if version == 'v2':
        sections.append(V2_EXTRA_SECTION)

    return sections


def create_contract_pdf(output_path, version, target_pages):
    """Create a contract PDF with the given version."""
    doc = pymupdf.open()

    sections = build_contract_text(version)

    # Title page
    page = doc.new_page(width=PAGE_W, height=PAGE_H)

    # Title
    y = 200
    page.insert_text(pymupdf.Point(PAGE_W/2 - 180, y), HEADER_TITLE,
                     fontsize=18, fontname="hebo", color=(0, 0, 0.4))
    y += 50
    page.insert_text(pymupdf.Point(PAGE_W/2 - 190, y), HEADER_SUBTITLE,
                     fontsize=11, fontname="helv", color=(0, 0, 0))

    y += 80
    if version == 'v1':
        page.insert_text(pymupdf.Point(PAGE_W/2 - 60, y), "Version 1.0",
                         fontsize=14, fontname="hebo", color=(0, 0, 0))
        y += 30
        page.insert_text(pymupdf.Point(PAGE_W/2 - 70, y), "Date: March 15, 2025",
                         fontsize=11, fontname="helv", color=(0, 0, 0))
    else:
        page.insert_text(pymupdf.Point(PAGE_W/2 - 60, y), "Version 2.0",
                         fontsize=14, fontname="hebo", color=(0, 0, 0))
        y += 30
        page.insert_text(pymupdf.Point(PAGE_W/2 - 70, y), "Date: April 1, 2025",
                         fontsize=11, fontname="helv", color=(0, 0, 0))

    y += 60
    page.insert_text(pymupdf.Point(PAGE_W/2 - 130, y), "CONFIDENTIAL AND PROPRIETARY",
                     fontsize=10, fontname="hebo", color=(0.5, 0, 0))

    # Footer on title page
    page.insert_text(pymupdf.Point(72, PAGE_H - 50),
                     "Meridian Technologies Inc. | Apex Solutions Group LLC",
                     fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))

    # Content pages
    margin_left = 72
    margin_right = PAGE_W - 72
    margin_top = 72
    margin_bottom = PAGE_H - 72
    text_width = margin_right - margin_left

    current_page = None
    y_pos = 0
    page_num = 1  # title page is page 0

    def new_content_page():
        nonlocal current_page, y_pos, page_num
        current_page = doc.new_page(width=PAGE_W, height=PAGE_H)
        y_pos = margin_top
        page_num += 1
        # Header line
        shape = current_page.new_shape()
        shape.draw_line(pymupdf.Point(margin_left, margin_top - 10),
                       pymupdf.Point(margin_right, margin_top - 10))
        shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
        shape.commit()
        # Footer
        current_page.insert_text(
            pymupdf.Point(margin_left, PAGE_H - 40),
            f"Professional Services Agreement - Page {page_num}",
            fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))
        current_page.insert_text(
            pymupdf.Point(margin_right - 80, PAGE_H - 40),
            "Confidential",
            fontsize=8, fontname="heit", color=(0.4, 0.4, 0.4))
        return current_page

    new_content_page()

    for heading, body in sections:
        # Check if we need a new page for the heading
        if y_pos > margin_bottom - 100:
            new_content_page()

        # Section heading
        current_page.insert_text(
            pymupdf.Point(margin_left, y_pos + 14),
            heading, fontsize=13, fontname="hebo", color=(0, 0, 0.3))
        y_pos += 30

        # Underline for heading
        shape = current_page.new_shape()
        shape.draw_line(pymupdf.Point(margin_left, y_pos - 8),
                       pymupdf.Point(margin_left + 250, y_pos - 8))
        shape.finish(color=(0, 0, 0.3), width=0.8)
        shape.commit()
        y_pos += 8

        # Body text - split into paragraphs
        paragraphs = body.split('\n\n')
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # Use textbox for auto-wrapping
            rect = pymupdf.Rect(margin_left, y_pos, margin_right, y_pos + 600)
            # Estimate height needed
            # Rough estimate: ~80 chars per line at fontsize 10, ~14 pts per line
            chars_per_line = int(text_width / 5.5)
            num_lines = max(1, len(para) // chars_per_line + 1)
            estimated_height = num_lines * 14 + 10

            if y_pos + estimated_height > margin_bottom:
                new_content_page()
                rect = pymupdf.Rect(margin_left, y_pos, margin_right, y_pos + 600)

            excess = current_page.insert_textbox(
                rect, para, fontsize=10, fontname="helv",
                color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

            # Calculate actual height used
            actual_height = estimated_height
            if excess > 0:
                # Text overflow - need to continue on next page
                actual_height = 600

            y_pos += actual_height

            # If excess text, create new page and continue
            while excess > 0:
                new_content_page()
                remaining = para[-(int(excess)):]  # approximate
                rect = pymupdf.Rect(margin_left, y_pos, margin_right, y_pos + 600)
                excess = current_page.insert_textbox(
                    rect, remaining, fontsize=10, fontname="helv",
                    color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
                y_pos += 200
                break  # avoid infinite loop

            y_pos += 6  # paragraph spacing

        y_pos += 15  # section spacing

    # Add signature page
    if y_pos > margin_bottom - 200:
        new_content_page()
    else:
        y_pos += 30

    current_page.insert_text(
        pymupdf.Point(margin_left, y_pos + 14),
        "SIGNATURES", fontsize=13, fontname="hebo", color=(0, 0, 0.3))
    y_pos += 40

    current_page.insert_text(
        pymupdf.Point(margin_left, y_pos),
        "IN WITNESS WHEREOF, the parties have executed this Agreement as of the Effective Date.",
        fontsize=10, fontname="helv", color=(0, 0, 0))
    y_pos += 40

    # Client signature block
    current_page.insert_text(pymupdf.Point(margin_left, y_pos),
        "MERIDIAN TECHNOLOGIES INC.", fontsize=11, fontname="hebo", color=(0, 0, 0))
    y_pos += 30
    shape = current_page.new_shape()
    shape.draw_line(pymupdf.Point(margin_left, y_pos), pymupdf.Point(margin_left + 200, y_pos))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    y_pos += 15
    current_page.insert_text(pymupdf.Point(margin_left, y_pos),
        "Name: Victoria Harrington", fontsize=10, fontname="helv", color=(0, 0, 0))
    y_pos += 15
    current_page.insert_text(pymupdf.Point(margin_left, y_pos),
        "Title: Chief Executive Officer", fontsize=10, fontname="helv", color=(0, 0, 0))
    y_pos += 15
    current_page.insert_text(pymupdf.Point(margin_left, y_pos),
        "Date: ______________________", fontsize=10, fontname="helv", color=(0, 0, 0))
    y_pos += 40

    # Service Provider signature block
    current_page.insert_text(pymupdf.Point(margin_left, y_pos),
        "APEX SOLUTIONS GROUP LLC", fontsize=11, fontname="hebo", color=(0, 0, 0))
    y_pos += 30
    shape = current_page.new_shape()
    shape.draw_line(pymupdf.Point(margin_left, y_pos), pymupdf.Point(margin_left + 200, y_pos))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    y_pos += 15
    current_page.insert_text(pymupdf.Point(margin_left, y_pos),
        "Name: Robert Castellano", fontsize=10, fontname="helv", color=(0, 0, 0))
    y_pos += 15
    current_page.insert_text(pymupdf.Point(margin_left, y_pos),
        "Title: Managing Partner", fontsize=10, fontname="helv", color=(0, 0, 0))
    y_pos += 15
    current_page.insert_text(pymupdf.Point(margin_left, y_pos),
        "Date: ______________________", fontsize=10, fontname="helv", color=(0, 0, 0))

    # Pad to reach target page count if needed
    while doc.page_count < target_pages:
        p = doc.new_page(width=PAGE_W, height=PAGE_H)
        page_idx = doc.page_count
        p.insert_text(pymupdf.Point(margin_left, margin_top + 14),
            f"EXHIBIT {'ABCDEFGH'[page_idx % 8]} - RESERVED",
            fontsize=13, fontname="hebo", color=(0, 0, 0.3))
        p.insert_text(pymupdf.Point(margin_left, margin_top + 50),
            "This page is intentionally reserved for future use in connection with "
            "additional exhibits, schedules, or amendments to this Agreement.",
            fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
        p.insert_text(pymupdf.Point(margin_left, PAGE_H - 40),
            f"Professional Services Agreement - Page {page_idx + 1}",
            fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))

    # If too many pages, trim
    while doc.page_count > target_pages:
        doc.delete_page(doc.page_count - 1)

    doc.save(output_path)
    print(f"Created {version} contract: {output_path} ({doc.page_count} pages)")
    doc.close()


def create_initial():
    os.makedirs(LEGAL_DIR, exist_ok=True)

    # Create V1 (18 pages) and V2 (19 pages)
    create_contract_pdf(V1_PATH, 'v1', 18)
    create_contract_pdf(V2_PATH, 'v2', 19)

    # Do NOT create the comparison report - that's the task

    # Open V1 in Evince for the agent
    launch_gui(f'evince "{V1_PATH}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with contract_v1.pdf')


create_initial()
