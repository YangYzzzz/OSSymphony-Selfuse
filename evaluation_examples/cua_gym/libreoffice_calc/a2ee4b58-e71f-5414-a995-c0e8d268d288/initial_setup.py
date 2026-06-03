"""
Initial Setup: Create a 22-page legal contract PDF for annotation task
Task ID: pdf_fm_017
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_017'
DOC_DIR = f'{WORKDIR}/Documents/legal'
OUTPUT = f'{DOC_DIR}/contract_draft.pdf'

A4_W, A4_H = 595, 842
ML = 72       # margin left
MR = 523      # margin right
MT = 72       # margin top
MB = 770      # usable bottom


def launch_gui(command: str, delay_sec: float = 1.0):
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def pn(page, num, total):
    """Page number footer."""
    page.insert_text(pymupdf.Point(A4_W/2 - 30, A4_H - 30),
                     f"Page {num} of {total}", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))


def heading(page, y, text):
    page.insert_text(pymupdf.Point(ML, y), text, fontsize=16, fontname="hebo", color=(0.08, 0.08, 0.25))
    return y + 24


def subheading(page, y, text):
    page.insert_text(pymupdf.Point(ML, y), text, fontsize=13, fontname="hebo", color=(0.1, 0.1, 0.1))
    return y + 19


def body(page, y, text, indent=10):
    rect = pymupdf.Rect(ML + indent, y, MR, y + 500)
    page.insert_textbox(rect, text, fontsize=10.5, fontname="helv",
                        color=(0.15, 0.15, 0.15), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    lines = max(1, len(text) // 75 + 1)
    return y + lines * 13.5 + 4


def sep(page, y):
    s = page.new_shape()
    s.draw_line(pymupdf.Point(ML, y), pymupdf.Point(MR, y))
    s.finish(color=(0.7, 0.7, 0.7), width=0.5)
    s.commit()
    return y + 10


def create_initial():
    os.makedirs(DOC_DIR, exist_ok=True)
    doc = pymupdf.open()

    # ========== PAGE 1: Title ==========
    p = doc.new_page(width=A4_W, height=A4_H)
    y = 200
    p.insert_text(pymupdf.Point(A4_W/2 - 140, y), "MASTER SERVICES AGREEMENT", fontsize=20, fontname="hebo", color=(0.08, 0.08, 0.25))
    y += 50
    p.insert_text(pymupdf.Point(A4_W/2 - 50, y), "between", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    y += 40
    p.insert_text(pymupdf.Point(A4_W/2 - 100, y), "Meridian Technologies Inc.", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.1))
    p.insert_text(pymupdf.Point(A4_W/2 - 35, y+22), '("Client")', fontsize=11, fontname="heit", color=(0.3, 0.3, 0.3))
    y += 70
    p.insert_text(pymupdf.Point(A4_W/2 - 20, y), "and", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    y += 40
    p.insert_text(pymupdf.Point(A4_W/2 - 110, y), "Apex Consulting Partners LLC", fontsize=16, fontname="hebo", color=(0.1, 0.1, 0.1))
    p.insert_text(pymupdf.Point(A4_W/2 - 55, y+22), '("Service Provider")', fontsize=11, fontname="heit", color=(0.3, 0.3, 0.3))
    y += 80
    p.insert_text(pymupdf.Point(A4_W/2 - 60, y), "Effective Date: March 1, 2025", fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))
    p.insert_text(pymupdf.Point(A4_W/2 - 65, y+22), "Agreement No.: MSA-2025-0472", fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))
    y += 70
    s = p.new_shape()
    s.draw_line(pymupdf.Point(ML+100, y), pymupdf.Point(MR-100, y))
    s.finish(color=(0.3, 0.3, 0.5), width=1.0)
    s.commit()
    p.insert_text(pymupdf.Point(A4_W/2 - 40, y+20), "CONFIDENTIAL", fontsize=10, fontname="hebo", color=(0.6, 0.1, 0.1))

    # ========== PAGE 2: TOC ==========
    p = doc.new_page(width=A4_W, height=A4_H)
    y = MT
    y = heading(p, y, "TABLE OF CONTENTS")
    y += 10
    toc_entries = [
        ("1.", "Definitions and Interpretation", "3"),
        ("2.", "Scope of Services", "4"),
        ("3.", "Fees and Payment", "5"),
        ("4.", "Intellectual Property", "6"),
        ("5.", "Confidentiality", "7"),
        ("6.", "Representations and Warranties", "8"),
        ("7.", "Representations and Warranties (continued)", "9"),
        ("8.", "Indemnification", "10"),
        ("9.", "Limitation of Liability", "11"),
        ("10.", "Term", "12"),
        ("11.", "Termination for Cause", "13"),
        ("12.", "Termination for Convenience and Effects", "14"),
        ("13.", "Dispute Resolution", "15"),
        ("14.", "General Provisions", "16"),
        ("15.", "Data Protection", "17"),
        ("16.", "Insurance and Compliance", "18"),
        ("", "Signature Page", "19"),
        ("", "Schedule A - Service Description", "20"),
        ("", "Schedule B - Service Levels", "21"),
        ("", "Schedule C - Fee Schedule", "22"),
    ]
    for num, title, pg in toc_entries:
        txt = f"{num} {title}" if num else title
        p.insert_text(pymupdf.Point(ML+10, y), txt, fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))
        p.insert_text(pymupdf.Point(MR-15, y), pg, fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))
        s = p.new_shape()
        s.draw_line(pymupdf.Point(ML+10+len(txt)*5.5, y+2), pymupdf.Point(MR-25, y+2))
        s.finish(color=(0.7, 0.7, 0.7), width=0.3, dashes="[2 2]")
        s.commit()
        y += 22

    # ========== PAGE 3: Definitions ==========
    p = doc.new_page(width=A4_W, height=A4_H)
    y = MT
    y = heading(p, y, "1. DEFINITIONS AND INTERPRETATION")
    y = sep(p, y); y += 5
    y = subheading(p, y, "1.1 Definitions")
    y = body(p, y, 'In this Agreement, unless the context otherwise requires, the following terms shall have the meanings ascribed to them: "Agreement" means this Master Services Agreement, including all Exhibits, Schedules, and Amendments attached hereto. "Affiliate" means any entity that directly or indirectly controls, is controlled by, or is under common control with a Party. "Confidential Information" means all non-public information disclosed by one Party to the other in connection with this Agreement, including but not limited to trade secrets, financial data, customer lists, pricing information, and proprietary technology. "Effective Date" means March 1, 2025. "Party" means either the Client or the Service Provider, and "Parties" means both.')
    y += 8
    y = subheading(p, y, "1.2 Interpretation")
    y = body(p, y, 'In this Agreement: (a) headings are for convenience only and shall not affect interpretation; (b) words importing the singular include the plural and vice versa; (c) a reference to a statute or statutory provision includes any subordinate legislation; (d) references to "including" or "includes" shall mean including or includes without limitation; (e) references to Clauses and Schedules are to Clauses of and Schedules to this Agreement; (f) a reference to a person includes a natural person, corporate body, and unincorporated body.')

    # ========== PAGE 4: Scope of Services ==========
    p = doc.new_page(width=A4_W, height=A4_H)
    y = MT
    y = heading(p, y, "2. SCOPE OF SERVICES")
    y = sep(p, y); y += 5
    y = subheading(p, y, "2.1 Service Description")
    y = body(p, y, 'The Service Provider shall provide to the Client the services described in Schedule A (the "Services"), in accordance with the terms and conditions of this Agreement. The Services shall be performed with reasonable skill and care, consistent with generally accepted industry standards and practices applicable to similar services. The Service Provider shall allocate sufficient qualified personnel and resources to perform the Services in a timely and professional manner.')
    y += 8
    y = subheading(p, y, "2.2 Service Levels")
    y = body(p, y, 'The Service Provider shall perform the Services in accordance with the service levels set out in Schedule B (the "Service Levels"). In the event that the Service Provider fails to meet any Service Level, the Client shall be entitled to the service credits specified in Schedule B. The Service Provider shall promptly notify the Client of any event or circumstance likely to result in a failure to meet any Service Level, and shall take all reasonable steps to mitigate the impact.')
    y += 8
    y = subheading(p, y, "2.3 Change Orders")
    y = body(p, y, 'Either Party may propose changes to the scope of Services by submitting a written change order request ("Change Order"). Each Change Order shall describe the proposed change in reasonable detail, including the estimated impact on fees, timelines, and resources. No Change Order shall be effective unless agreed in writing by both Parties.')

    # ========== PAGE 5: Fees and Payment ==========
    p = doc.new_page(width=A4_W, height=A4_H)
    y = MT
    y = heading(p, y, "3. FEES AND PAYMENT")
    y = sep(p, y); y += 5
    y = subheading(p, y, "3.1 Fees")
    y = body(p, y, 'In consideration for the performance of the Services, the Client shall pay to the Service Provider the fees set out in Schedule C (the "Fees"). The Fees shall be invoiced monthly in arrears, based on actual time and materials expended, unless otherwise specified in Schedule C. All Fees are exclusive of applicable taxes, which shall be added to invoices at the prevailing rate.')
    y += 8
    y = subheading(p, y, "3.2 Payment Terms")
    y = body(p, y, 'All invoices shall be payable within thirty (30) calendar days of receipt by the Client. Late payments shall accrue interest at a rate of 1.5% per month, or the maximum rate permitted by applicable law, whichever is lower. The Client may dispute any invoice in good faith by providing written notice within fifteen (15) days of receipt.')
    y += 8
    y = subheading(p, y, "3.3 Expenses")
    y = body(p, y, 'The Service Provider shall be entitled to reimbursement for reasonable out-of-pocket expenses incurred in the performance of the Services, provided that: (a) such expenses are pre-approved in writing by the Client; (b) the Service Provider provides receipts or other reasonable documentation; and (c) travel expenses comply with the Client travel policy attached as Exhibit D. Total reimbursable expenses shall not exceed $25,000 per calendar quarter without prior written approval.')

    # ========== PAGE 6: Intellectual Property ==========
    p = doc.new_page(width=A4_W, height=A4_H)
    y = MT
    y = heading(p, y, "4. INTELLECTUAL PROPERTY")
    y = sep(p, y); y += 5
    y = subheading(p, y, "4.1 Pre-Existing IP")
    y = body(p, y, 'Each Party shall retain all right, title, and interest in and to its pre-existing intellectual property ("Background IP"). Neither Party shall acquire any right, title, or interest in the other Party\'s Background IP by virtue of this Agreement, except for the limited license rights expressly granted herein.')
    y += 8
    y = subheading(p, y, "4.2 Work Product")
    y = body(p, y, 'All deliverables, reports, documentation, and other materials created by the Service Provider in the course of performing the Services ("Work Product") shall be the exclusive property of the Client. The Service Provider hereby assigns to the Client all right, title, and interest in and to the Work Product, including all intellectual property rights therein. The Service Provider shall execute such documents as reasonably necessary to effect such assignment.')
    y += 8
    y = subheading(p, y, "4.3 License Grant")
    y = body(p, y, 'The Service Provider grants to the Client a non-exclusive, worldwide, perpetual, irrevocable, royalty-free license to use any Background IP of the Service Provider that is incorporated in or necessary for the use of the Work Product. The Client grants to the Service Provider a limited, non-exclusive license to use the Client\'s Background IP solely for the performance of the Services during the term of this Agreement.')

    # ========== PAGE 7: Confidentiality ==========
    p = doc.new_page(width=A4_W, height=A4_H)
    y = MT
    y = heading(p, y, "5. CONFIDENTIALITY")
    y = sep(p, y); y += 5
    y = subheading(p, y, "5.1 Obligations")
    y = body(p, y, 'Each Party (the "Receiving Party") shall: (a) hold in strict confidence all Confidential Information of the other Party (the "Disclosing Party"); (b) not disclose such Confidential Information to any third party without the prior written consent of the Disclosing Party; (c) use such Confidential Information solely for the purposes of this Agreement; and (d) protect such Confidential Information using at least the same degree of care it uses to protect its own confidential information, but in no event less than reasonable care.')
    y += 8
    y = subheading(p, y, "5.2 Exceptions")
    y = body(p, y, 'The obligations of confidentiality shall not apply to information that: (a) is or becomes publicly available through no fault of the Receiving Party; (b) was already known to the Receiving Party prior to disclosure; (c) is independently developed by the Receiving Party without reference to the Confidential Information; (d) is disclosed to the Receiving Party by a third party not under a duty of confidentiality; or (e) is required to be disclosed by law, regulation, or court order.')
    y += 8
    y = subheading(p, y, "5.3 Duration")
    y = body(p, y, 'The obligations of confidentiality shall survive the termination or expiration of this Agreement for a period of five (5) years, except with respect to trade secrets, which shall be protected indefinitely or for so long as they remain trade secrets under applicable law, whichever is longer.')

    # ========== PAGE 8: Representations & Warranties (part 1) ==========
    p = doc.new_page(width=A4_W, height=A4_H)
    y = MT
    y = heading(p, y, "6. REPRESENTATIONS AND WARRANTIES")
    y = sep(p, y); y += 5
    y = subheading(p, y, "6.1 Mutual Representations")
    y = body(p, y, 'Each Party represents and warrants to the other that: (a) it has the legal right and authority to enter into this Agreement; (b) the execution and performance of this Agreement will not conflict with any other agreement to which it is a party; (c) it shall comply with all applicable laws, rules, and regulations in the performance of its obligations under this Agreement; and (d) it has obtained all necessary approvals and authorizations to perform its obligations hereunder.')
    y += 8
    y = subheading(p, y, "6.2 Service Provider Warranties")
    y = body(p, y, 'The Service Provider additionally represents and warrants that: (a) the Services will be performed in a professional and workmanlike manner; (b) all personnel assigned to perform the Services are qualified and experienced; (c) the Work Product will not infringe or misappropriate any intellectual property rights of any third party; and (d) the Services and Work Product will conform to the specifications set forth in Schedule A. The Service Provider further warrants that it maintains appropriate security measures and certifications for handling sensitive client data.')

    # ========== PAGE 9: Representations & Warranties (part 2) ==========
    p = doc.new_page(width=A4_W, height=A4_H)
    y = MT
    y = heading(p, y, "6. REPRESENTATIONS AND WARRANTIES (Continued)")
    y = sep(p, y); y += 5
    y = subheading(p, y, "6.3 Disclaimer")
    y = body(p, y, 'EXCEPT AS EXPRESSLY SET FORTH IN THIS AGREEMENT, NEITHER PARTY MAKES ANY WARRANTIES, EXPRESS OR IMPLIED, INCLUDING ANY IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT. THE SERVICE PROVIDER DOES NOT WARRANT THAT THE SERVICES OR WORK PRODUCT WILL BE ERROR-FREE OR UNINTERRUPTED.')
    y += 8
    y = subheading(p, y, "6.4 Remedies for Breach of Warranty")
    y = body(p, y, 'In the event of a breach of any warranty set forth in this Section 6, the non-breaching Party shall provide written notice specifying the nature of the breach. The breaching Party shall have thirty (30) days from receipt of such notice to cure the breach. If the breach is not cured within such period, the non-breaching Party may: (a) terminate this Agreement in accordance with Section 10.1; (b) seek damages; or (c) pursue specific performance. These remedies are in addition to any other remedies available at law or in equity.')
    y += 8
    y = subheading(p, y, "6.5 Compliance Certifications")
    y = body(p, y, 'The Service Provider shall maintain and provide upon request evidence of the following compliance certifications: SOC 2 Type II, ISO 27001, and any industry-specific certifications required for the performance of the Services. The Service Provider shall promptly notify the Client of any changes to its certification status or any findings of material non-compliance during audit or assessment processes. Failure to maintain required certifications shall constitute a material breach of this Agreement.')

    # ========== PAGE 10: Indemnification ==========
    p = doc.new_page(width=A4_W, height=A4_H)
    y = MT
    y = heading(p, y, "7. INDEMNIFICATION")
    y = sep(p, y); y += 5
    y = subheading(p, y, "7.1 Service Provider Indemnification")
    y = body(p, y, 'The Service Provider shall indemnify, defend, and hold harmless the Client and its Affiliates, officers, directors, employees, and agents from and against any and all claims, damages, losses, costs, and expenses (including reasonable attorneys\' fees) arising out of or relating to: (a) any breach by the Service Provider of its representations, warranties, or obligations; (b) any infringement or misappropriation of intellectual property rights by the Services or Work Product; (c) any negligent or willful act or omission of the Service Provider or its personnel; or (d) any violation of applicable law by the Service Provider.')
    y += 8
    y = subheading(p, y, "7.2 Client Indemnification")
    y = body(p, y, 'The Client shall indemnify, defend, and hold harmless the Service Provider and its Affiliates, officers, directors, employees, and agents from and against any and all claims, damages, losses, costs, and expenses (including reasonable attorneys\' fees) arising out of or relating to: (a) any breach by the Client of its representations, warranties, or obligations; (b) any use of the Work Product in a manner not contemplated by this Agreement; or (c) any materials provided by the Client that infringe third-party intellectual property rights.')
    y += 8
    y = subheading(p, y, "7.3 Indemnification Procedure")
    y = body(p, y, 'A Party seeking indemnification shall: (a) promptly notify the indemnifying Party of any claim; (b) give the indemnifying Party sole control of the defense and settlement; and (c) provide reasonable cooperation and assistance. The indemnifying Party shall not settle any claim without the indemnified Party\'s prior written consent if settlement would impose obligations on or admit fault for the indemnified Party.')

    # ========== PAGE 11: Limitation of Liability ==========
    p = doc.new_page(width=A4_W, height=A4_H)
    y = MT
    y = heading(p, y, "8. LIMITATION OF LIABILITY")
    y = sep(p, y); y += 5
    y = subheading(p, y, "8.1 Cap on Liability")
    y = body(p, y, 'EXCEPT FOR CLAIMS ARISING UNDER SECTIONS 5 (CONFIDENTIALITY) AND 7 (INDEMNIFICATION), NEITHER PARTY\'S TOTAL AGGREGATE LIABILITY UNDER THIS AGREEMENT SHALL EXCEED THE TOTAL FEES PAID OR PAYABLE BY THE CLIENT DURING THE TWELVE (12) MONTH PERIOD IMMEDIATELY PRECEDING THE EVENT GIVING RISE TO THE CLAIM.')
    y += 8
    y = subheading(p, y, "8.2 Exclusion of Consequential Damages")
    y = body(p, y, 'IN NO EVENT SHALL EITHER PARTY BE LIABLE TO THE OTHER FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, PUNITIVE, OR EXEMPLARY DAMAGES, INCLUDING DAMAGES FOR LOSS OF PROFITS, REVENUE, GOODWILL, DATA, OR BUSINESS OPPORTUNITY, ARISING OUT OF OR RELATING TO THIS AGREEMENT, REGARDLESS OF WHETHER SUCH DAMAGES WERE FORESEEABLE OR WHETHER SUCH PARTY WAS ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.')
    y += 8
    y = subheading(p, y, "8.3 Essential Basis")
    y = body(p, y, 'The Parties acknowledge that the limitations of liability set forth in this Section 8 reflect the allocation of risk between the Parties, form an essential basis of the bargain between the Parties, and shall apply notwithstanding the failure of essential purpose of any limited remedy provided herein. Without such limitations, the pricing and other terms of this Agreement would be substantially different.')

    # ========== PAGE 12: Term ==========
    p = doc.new_page(width=A4_W, height=A4_H)
    y = MT
    y = heading(p, y, "9. TERM")
    y = sep(p, y); y += 5
    y = subheading(p, y, "9.1 Initial Term")
    y = body(p, y, 'This Agreement shall commence on the Effective Date and shall continue for an initial term of three (3) years (the "Initial Term"), unless earlier terminated in accordance with Section 10. The Initial Term shall expire on February 28, 2028.')
    y += 8
    y = subheading(p, y, "9.2 Renewal")
    y = body(p, y, 'Upon expiration of the Initial Term, this Agreement shall automatically renew for successive one (1) year periods (each a "Renewal Term"), unless either Party provides written notice of non-renewal at least ninety (90) days prior to the end of the then-current term. The Initial Term and any Renewal Terms are collectively referred to as the "Term." Each Renewal Term shall be subject to the same terms and conditions, except that Fees may be adjusted in accordance with Schedule C.')
    y += 8
    y = subheading(p, y, "9.3 Transition Assistance")
    y = body(p, y, 'During the last ninety (90) days of the Term (whether by expiration or termination), the Service Provider shall provide transition assistance services to the Client to facilitate the orderly transition of the Services to the Client or to a successor service provider designated by the Client. Transition assistance shall include knowledge transfer, documentation, data migration, and reasonable cooperation with the successor service provider. Transition assistance services shall be provided at the rates specified in Schedule C.')

    # ========== PAGE 13: Termination for Cause ==========
    p = doc.new_page(width=A4_W, height=A4_H)
    y = MT
    y = heading(p, y, "10. TERMINATION")
    y = sep(p, y); y += 5
    y = subheading(p, y, "10.1 Termination for Cause")
    y = body(p, y, 'Either Party may terminate this Agreement immediately upon written notice if the other Party: (a) commits a material breach of any provision of this Agreement and fails to cure such breach within thirty (30) days after receipt of written notice thereof; (b) becomes insolvent, files or has filed against it a petition in bankruptcy, or makes an assignment for the benefit of creditors; or (c) ceases to conduct business in the normal course. A termination for cause shall be effective immediately upon delivery of the notice of termination, or on such later date as specified in the notice.')
    y += 8
    y = subheading(p, y, "10.1.1 Cure Period")
    y = body(p, y, 'The thirty (30) day cure period referenced in Section 10.1(a) shall commence upon receipt of written notice from the non-breaching Party. The notice shall specify the nature of the breach with reasonable particularity. If the breach is not fully cured within the cure period, the non-breaching Party may terminate this Agreement by providing written notice of termination. For the avoidance of doubt, certain breaches (including breaches of confidentiality obligations and intellectual property provisions) may be incurable, in which case the non-breaching Party may terminate immediately upon notice.')
    y += 8
    y = subheading(p, y, "10.1.2 Repeated Breaches")
    y = body(p, y, 'Notwithstanding the foregoing cure provisions, if a Party commits the same or substantially similar breach on three (3) or more occasions within any twelve (12) month period, the other Party may terminate this Agreement immediately upon written notice without providing a further opportunity to cure, regardless of whether the prior breaches were cured within the applicable cure period. This provision reflects the Parties\' agreement that repeated breaches demonstrate a pattern of non-compliance that undermines the fundamental basis of this Agreement.')

    # ========== PAGE 14: Termination for Convenience ========== (THIS IS THE KEY PAGE)
    p = doc.new_page(width=A4_W, height=A4_H)
    y = MT
    y = heading(p, y, "10. TERMINATION (Continued)")
    y = sep(p, y); y += 5
    y = subheading(p, y, "Termination for Convenience")
    y = body(p, y, 'Either Party may terminate this Agreement without cause upon ninety (90) days prior written notice to the other Party. In the event of termination for convenience by the Client, the Client shall pay the Service Provider for all Services performed and expenses incurred through the effective date of termination, plus any reasonable wind-down costs approved in writing by the Client. In the event of termination for convenience by the Service Provider, the Service Provider shall continue to perform the Services during the notice period and shall cooperate with the Client to ensure an orderly transition of the Services to the Client or to a successor service provider designated by the Client.')
    y += 8
    y = subheading(p, y, "10.3 Effect of Termination")
    y = body(p, y, 'Upon termination or expiration of this Agreement: (a) the Service Provider shall promptly deliver to the Client all Work Product, whether completed or in progress; (b) each Party shall return or destroy all Confidential Information of the other Party and certify in writing that it has done so; (c) the Client shall pay all outstanding Fees and approved expenses within thirty (30) days of the effective date of termination; (d) all licenses granted hereunder shall terminate, except as expressly stated to survive; and (e) Sections 1, 4, 5, 6.3, 7, 8, 10.3, 11, and 12 shall survive termination or expiration of this Agreement.')
    y += 8
    y = subheading(p, y, "10.4 Return of Materials")
    y = body(p, y, 'Within thirty (30) days of the effective date of termination, each Party shall return to the other Party all documents, materials, and property belonging to such other Party, including all copies, extracts, and summaries thereof. The Service Provider shall also provide the Client with a complete and usable copy of all Work Product, source code, documentation, and related materials in formats reasonably specified by the Client.')

    # ========== PAGE 15: Dispute Resolution ==========
    p = doc.new_page(width=A4_W, height=A4_H)
    y = MT
    y = heading(p, y, "11. DISPUTE RESOLUTION")
    y = sep(p, y); y += 5
    y = subheading(p, y, "11.1 Negotiation")
    y = body(p, y, 'In the event of any dispute arising out of or relating to this Agreement, the Parties shall first attempt to resolve the dispute through good faith negotiations between senior representatives of each Party. Such negotiations shall commence within ten (10) business days of written notice from one Party to the other identifying the dispute, and shall continue for a period of at least thirty (30) days before either Party may escalate the dispute.')
    y += 8
    y = subheading(p, y, "11.2 Mediation")
    y = body(p, y, 'If the dispute cannot be resolved through negotiation within thirty (30) days, the Parties agree to submit the dispute to non-binding mediation administered by JAMS in accordance with its mediation rules. The mediation shall be conducted in San Francisco, California, and each Party shall bear its own costs of mediation, with the mediator\'s fees shared equally between the Parties.')
    y += 8
    y = subheading(p, y, "11.3 Arbitration")
    y = body(p, y, 'If the dispute is not resolved through mediation within sixty (60) days, the dispute shall be finally resolved by binding arbitration administered by JAMS under its Comprehensive Arbitration Rules. The arbitration shall be conducted by a single arbitrator in San Francisco, California. The arbitrator\'s award shall be final and binding, and judgment may be entered in any court of competent jurisdiction. Each Party shall bear its own costs, except that the arbitrator\'s fees shall be shared equally.')

    # ========== PAGE 16: General Provisions ==========
    p = doc.new_page(width=A4_W, height=A4_H)
    y = MT
    y = heading(p, y, "12. GENERAL PROVISIONS")
    y = sep(p, y); y += 5
    y = subheading(p, y, "12.1 Governing Law")
    y = body(p, y, 'This Agreement shall be governed by and construed in accordance with the laws of the State of California, without regard to its conflict of laws principles. The Parties consent to the exclusive jurisdiction of the federal and state courts located in San Francisco County, California.')
    y += 8
    y = subheading(p, y, "12.2 Force Majeure")
    y = body(p, y, 'Neither Party shall be liable for any failure or delay in performing its obligations to the extent caused by circumstances beyond its reasonable control, including acts of God, natural disasters, pandemics, war, terrorism, strikes, government actions, power failures, or internet disruptions.')
    y += 8
    y = subheading(p, y, "12.3 Assignment")
    y = body(p, y, 'Neither Party may assign this Agreement without the prior written consent of the other Party, except that either Party may assign this Agreement to a successor in connection with a merger, acquisition, or sale of all or substantially all of its assets.')
    y += 8
    y = subheading(p, y, "12.4 Entire Agreement")
    y = body(p, y, 'This Agreement, including all Exhibits and Schedules, constitutes the entire agreement between the Parties with respect to the subject matter hereof and supersedes all prior agreements, understandings, negotiations, and discussions, whether oral or written. No modification shall be effective unless in writing and signed by both Parties.')

    # ========== PAGE 17: Data Protection ==========
    p = doc.new_page(width=A4_W, height=A4_H)
    y = MT
    y = heading(p, y, "13. DATA PROTECTION")
    y = sep(p, y); y += 5
    y = subheading(p, y, "13.1 Compliance")
    y = body(p, y, 'Each Party shall comply with all applicable data protection and privacy laws, including the General Data Protection Regulation (GDPR), the California Consumer Privacy Act (CCPA), and any other applicable data protection legislation. The Service Provider shall process personal data only in accordance with the Client\'s documented instructions and shall implement appropriate technical and organizational measures to protect personal data.')
    y += 8
    y = subheading(p, y, "13.2 Data Processing Agreement")
    y = body(p, y, 'The Parties shall enter into a Data Processing Agreement substantially in the form attached as Exhibit E, which sets forth the terms governing the processing of personal data by the Service Provider on behalf of the Client. The Data Processing Agreement is incorporated into and forms part of this Agreement.')
    y += 8
    y = subheading(p, y, "13.3 Data Breach Notification")
    y = body(p, y, 'The Service Provider shall notify the Client of any actual or suspected data breach involving the Client\'s personal data without undue delay and in any event within seventy-two (72) hours of becoming aware of such breach. The notification shall include a description of the nature of the breach, the categories and approximate number of data subjects affected, and the measures taken or proposed to address the breach.')

    # ========== PAGE 18: Insurance and Compliance ==========
    p = doc.new_page(width=A4_W, height=A4_H)
    y = MT
    y = heading(p, y, "14. INSURANCE AND COMPLIANCE")
    y = sep(p, y); y += 5
    y = subheading(p, y, "14.1 Insurance Requirements")
    y = body(p, y, 'The Service Provider shall maintain, at its own expense, the following insurance coverage throughout the Term: (a) Commercial General Liability with limits of not less than $2,000,000 per occurrence and $5,000,000 in the aggregate; (b) Professional Liability (Errors and Omissions) with limits of not less than $3,000,000 per claim; (c) Workers\' Compensation as required by applicable law; and (d) Cyber Liability with limits of not less than $5,000,000 per occurrence.')
    y += 8
    y = subheading(p, y, "14.2 Compliance Audit")
    y = body(p, y, 'During the Term and for a period of two (2) years thereafter, the Client shall have the right, upon reasonable notice and during normal business hours, to audit the Service Provider\'s records, systems, and facilities to verify compliance. The Service Provider shall cooperate fully with any such audit. If any audit reveals a material non-compliance, the Service Provider shall promptly remediate such non-compliance at its own expense.')

    # ========== PAGE 19: Signature ==========
    p = doc.new_page(width=A4_W, height=A4_H)
    y = MT
    y = heading(p, y, "SIGNATURE PAGE")
    y = sep(p, y); y += 10
    p.insert_text(pymupdf.Point(ML, y), "IN WITNESS WHEREOF, the Parties have executed this Agreement as of the Effective Date.", fontsize=10.5, fontname="helv", color=(0.15, 0.15, 0.15))
    y += 50
    p.insert_text(pymupdf.Point(ML, y), "MERIDIAN TECHNOLOGIES INC.", fontsize=12, fontname="hebo")
    y += 40
    s = p.new_shape(); s.draw_line(pymupdf.Point(ML, y), pymupdf.Point(ML+200, y)); s.finish(color=(0,0,0), width=0.5); s.commit()
    y += 15
    p.insert_text(pymupdf.Point(ML, y), "Name: Victoria Hargrove", fontsize=10.5, fontname="helv")
    y += 18
    p.insert_text(pymupdf.Point(ML, y), "Title: Chief Operating Officer", fontsize=10.5, fontname="helv")
    y += 18
    p.insert_text(pymupdf.Point(ML, y), "Date: _________________", fontsize=10.5, fontname="helv")
    y += 60
    p.insert_text(pymupdf.Point(ML, y), "APEX CONSULTING PARTNERS LLC", fontsize=12, fontname="hebo")
    y += 40
    s = p.new_shape(); s.draw_line(pymupdf.Point(ML, y), pymupdf.Point(ML+200, y)); s.finish(color=(0,0,0), width=0.5); s.commit()
    y += 15
    p.insert_text(pymupdf.Point(ML, y), "Name: Robert Nakamura", fontsize=10.5, fontname="helv")
    y += 18
    p.insert_text(pymupdf.Point(ML, y), "Title: Managing Partner", fontsize=10.5, fontname="helv")
    y += 18
    p.insert_text(pymupdf.Point(ML, y), "Date: _________________", fontsize=10.5, fontname="helv")

    # ========== PAGE 20: Schedule A ==========
    p = doc.new_page(width=A4_W, height=A4_H)
    y = MT
    y = heading(p, y, "SCHEDULE A - SERVICE DESCRIPTION")
    y = sep(p, y); y += 5
    y = subheading(p, y, "A.1 Overview of Services")
    y = body(p, y, 'The Service Provider shall provide: (i) Enterprise software development and integration services, including custom application development, API integration, and system architecture design; (ii) Cloud infrastructure management, including deployment, monitoring, scaling, and security; (iii) Data analytics and business intelligence services, including data pipeline development, dashboards, and predictive modeling; (iv) Technical consulting and advisory services.')
    y += 8
    y = subheading(p, y, "A.2 Deliverables")
    y = body(p, y, 'Deliverables include: (a) Comprehensive system architecture documentation; (b) Custom enterprise applications per Statements of Work; (c) Monthly performance reports and dashboards; (d) Quarterly strategic technology reviews; (e) Annual security assessment reports; (f) Training materials and knowledge transfer documentation.')
    y += 8
    y = subheading(p, y, "A.3 Personnel")
    y = body(p, y, 'The Service Provider shall assign: one (1) Senior Project Manager, two (2) Lead Software Engineers, four (4) Software Developers, one (1) DevOps Engineer, one (1) QA Lead, two (2) QA Engineers, and one (1) Business Analyst. Key personnel may not be reassigned without thirty (30) days prior written notice and Client approval.')

    # ========== PAGE 21: Schedule B ==========
    p = doc.new_page(width=A4_W, height=A4_H)
    y = MT
    y = heading(p, y, "SCHEDULE B - SERVICE LEVELS")
    y = sep(p, y); y += 5
    y = subheading(p, y, "B.1 Availability")
    y = body(p, y, 'Minimum uptime of 99.9% per calendar month, measured 24/7, excluding planned maintenance. Planned maintenance during off-peak hours (2:00 AM - 6:00 AM PT), not exceeding four (4) hours per month, with seventy-two (72) hours advance notice.')
    y += 8
    y = subheading(p, y, "B.2 Response Times")
    y = body(p, y, 'Incident response targets: Critical (P1) - Response within 15 minutes, resolution within 4 hours; High (P2) - Response within 1 hour, resolution within 8 hours; Medium (P3) - Response within 4 hours, resolution within 24 hours; Low (P4) - Response within 8 hours, resolution within 5 business days.')
    y += 8
    y = subheading(p, y, "B.3 Service Credits")
    y = body(p, y, 'Service credits for uptime failures: 99.0%-99.9% uptime = 5% credit; 98.0%-98.9% = 10% credit; 97.0%-97.9% = 20% credit; Below 97.0% = 30% credit plus right to terminate. Service credits are the Client\'s sole remedy for SLA failures.')

    # ========== PAGE 22: Schedule C ==========
    p = doc.new_page(width=A4_W, height=A4_H)
    y = MT
    y = heading(p, y, "SCHEDULE C - FEE SCHEDULE")
    y = sep(p, y); y += 5
    y = subheading(p, y, "C.1 Rate Card")
    y = body(p, y, 'Hourly rates: Senior Project Manager - $275/hr; Lead Software Engineer - $250/hr; Software Developer - $200/hr; DevOps Engineer - $225/hr; QA Lead - $210/hr; QA Engineer - $175/hr; Business Analyst - $195/hr. Annual adjustment of up to 3% with ninety (90) days notice.')
    y += 8
    y = subheading(p, y, "C.2 Estimated Monthly Fees")
    y = body(p, y, 'Estimated monthly fees approximately $385,000, subject to variation based on actual utilization. The Service Provider shall notify the Client if monthly fees are expected to exceed estimate by more than 10%. Not-to-exceed cap of $5,000,000 for the Initial Term.')
    y += 8
    y = subheading(p, y, "C.3 Invoicing")
    y = body(p, y, 'Invoices submitted electronically on the first business day of each month for the preceding month. Each invoice shall include: (a) detailed hours by resource category; (b) work descriptions; (c) reimbursable expenses with documentation; (d) applicable tax amounts.')

    # Add page numbers
    total = doc.page_count
    for i in range(total):
        pn(doc[i], i+1, total)

    # Add TOC bookmarks
    toc = [
        [1, "Title Page", 1],
        [1, "Table of Contents", 2],
        [1, "1. Definitions and Interpretation", 3],
        [1, "2. Scope of Services", 4],
        [1, "3. Fees and Payment", 5],
        [1, "4. Intellectual Property", 6],
        [1, "5. Confidentiality", 7],
        [1, "6. Representations and Warranties", 8],
        [1, "7. Indemnification", 10],
        [1, "8. Limitation of Liability", 11],
        [1, "9. Term", 12],
        [1, "10. Termination", 13],
        [2, "Termination for Convenience", 14],
        [1, "11. Dispute Resolution", 15],
        [1, "12. General Provisions", 16],
        [1, "13. Data Protection", 17],
        [1, "14. Insurance and Compliance", 18],
        [1, "Signature Page", 19],
        [1, "Schedule A", 20],
        [1, "Schedule B", 21],
        [1, "Schedule C", 22],
    ]
    doc.set_toc(toc)

    doc.set_metadata({
        "title": "Master Services Agreement - MSA-2025-0472",
        "author": "Meridian Technologies Inc. / Apex Consulting Partners LLC",
        "subject": "Master Services Agreement",
        "keywords": "contract, services, agreement, MSA",
        "creator": "Legal Department",
        "producer": "Meridian Technologies",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f"Initial file created: {OUTPUT}")

    # Verify
    v = pymupdf.open(OUTPUT)
    print(f"Total pages: {v.page_count}")
    p13_text = v[13].get_text("text")
    v.close()
    if "Termination for Convenience" in p13_text:
        print("VERIFIED: Page 14 (index 13) contains 'Termination for Convenience'")
    else:
        print("WARNING: 'Termination for Convenience' NOT found on page 14!")
        v = pymupdf.open(OUTPUT)
        for i in range(v.page_count):
            if "Termination for Convenience" in v[i].get_text("text"):
                print(f"  Found on page {i+1}")
        v.close()

    # Open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print("GUI_READY: launched Evince with DISPLAY=:0")


create_initial()
