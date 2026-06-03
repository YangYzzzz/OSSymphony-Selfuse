"""
Initial Setup: Create an 18-page M&A acquisition agreement PDF with no annotations.
Task ID: pdf_legal_067
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_067'
OUTPUT_DIR = f'{WORKDIR}/legal/ma'
OUTPUT = f'{OUTPUT_DIR}/acquisition_agreement.pdf'

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

def add_section_text(page, y_start, title, paragraphs, fontsize_title=13, fontsize_body=10):
    """Add a section with title and body paragraphs. Returns y position after content."""
    y = y_start

    # Section title
    page.insert_text(
        pymupdf.Point(72, y),
        title,
        fontsize=fontsize_title,
        fontname="tibo",
        color=(0, 0, 0),
    )
    y += fontsize_title + 8

    # Body paragraphs
    for para in paragraphs:
        rect = pymupdf.Rect(72, y, W - 72, H - 72)
        excess = page.insert_textbox(
            rect,
            para,
            fontsize=fontsize_body,
            fontname="tiro",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )
        # Estimate height used
        chars_per_line = 75
        lines = max(1, len(para) // chars_per_line + 1)
        y += lines * (fontsize_body + 3) + 10
        if y > H - 100:
            break

    return y

def create_initial():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    doc = pymupdf.open()

    # =========================================================================
    # PAGE 1: Title Page
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(150, 200), "ACQUISITION AGREEMENT", fontsize=22, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(200, 250), "by and between", fontsize=14, fontname="tiro", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(130, 290), "MERIDIAN TECHNOLOGIES, INC.", fontsize=16, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(250, 320), "and", fontsize=14, fontname="tiro", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(150, 360), "ATLAS GLOBAL SOLUTIONS, LLC", fontsize=16, fontname="tibo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(200, 430), "Dated as of March 15, 2025", fontsize=12, fontname="tiro", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(140, 480), "Harrison & Whitfield LLP, Counsel to Buyer", fontsize=10, fontname="tiro", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(140, 500), "Donovan, Kessler & Park, Counsel to Seller", fontsize=10, fontname="tiro", color=(0.3, 0.3, 0.3))

    # =========================================================================
    # PAGE 2: Table of Contents
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(220, 60), "TABLE OF CONTENTS", fontsize=14, fontname="tibo", color=(0, 0, 0))
    toc_items = [
        ("Article I", "Definitions and Interpretation", "3"),
        ("Article II", "The Acquisition", "4"),
        ("Article III", "Consideration and Payment", "5"),
        ("Article IV", "Representations and Warranties of Seller", "6"),
        ("Article V", "Representations and Warranties of Buyer", "7"),
        ("Article VI", "Covenants and Agreements", "8"),
        ("Article VII", "Conditions to Closing", "9"),
        ("Article VIII", "Indemnification", "10"),
        ("Article IX", "Termination", "12"),
        ("Article X", "Tax Matters", "13"),
        ("Article XI", "Escrow Arrangements", "14"),
        ("Article XII", "Non-Competition and Non-Solicitation", "15"),
        ("Article XIII", "Confidentiality", "16"),
        ("Article XIV", "Miscellaneous Provisions", "17"),
        ("Article XV", "Governing Law and Dispute Resolution", "18"),
    ]
    y = 100
    for art, desc, pg in toc_items:
        page.insert_text(pymupdf.Point(72, y), f"{art}.", fontsize=10, fontname="tibo", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(140, y), desc, fontsize=10, fontname="tiro", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(520, y), pg, fontsize=10, fontname="tiro", color=(0, 0, 0))
        y += 18

    # =========================================================================
    # PAGE 3: Article I - Definitions
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    add_section_text(page, 60, "ARTICLE I - DEFINITIONS AND INTERPRETATION", [
        '1.1 "Affiliate" means, with respect to any Person, any other Person that directly or indirectly, through one or more intermediaries, controls, is controlled by, or is under common control with, such Person. For purposes of this definition, "control" means the possession, directly or indirectly, of the power to direct or cause the direction of the management and policies of a Person.',
        '1.2 "Business Day" means any day that is not a Saturday, Sunday, or other day on which commercial banks in New York, New York are authorized or obligated by Law to close.',
        '1.3 "Company Material Adverse Effect" means any event, circumstance, development, change, or effect that, individually or in the aggregate with all other events, circumstances, developments, changes, or effects, (a) is or would reasonably be expected to be materially adverse to the business, assets, liabilities, financial condition, or results of operations of the Company and its Subsidiaries, taken as a whole.',
        '1.4 "Environmental Law" means all applicable federal, state, local, and foreign Laws relating to pollution, the protection of the environment, or the release, threatened release, or handling of Hazardous Materials.',
        '1.5 "GAAP" means generally accepted accounting principles as applied in the United States of America, consistently applied throughout the periods involved.',
        '1.6 "Governmental Authority" means any federal, state, local, or foreign government, any court, tribunal, administrative or regulatory agency or commission, or other governmental or quasi-governmental authority or instrumentality.',
        '1.7 "Intellectual Property" means all patents, trademarks, service marks, trade names, copyrights, trade secrets, know-how, domain names, and all applications and registrations therefor.',
    ])

    # =========================================================================
    # PAGE 4: Article II - The Acquisition
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    add_section_text(page, 60, "ARTICLE II - THE ACQUISITION", [
        "2.1 Purchase and Sale. Subject to the terms and conditions set forth herein, at the Closing, Seller shall sell, convey, transfer, assign, and deliver to Buyer, and Buyer shall purchase, acquire, and accept from Seller, all of Seller's right, title, and interest in and to one hundred percent (100%) of the issued and outstanding membership interests of Atlas Global Solutions, LLC (the \"Acquired Interests\"), free and clear of all Encumbrances.",
        "2.2 Closing. The closing of the transactions contemplated by this Agreement (the \"Closing\") shall take place remotely via the electronic exchange of documents and signatures, on the date that is five (5) Business Days after the satisfaction or waiver of all conditions precedent set forth in Article VII (other than those conditions that by their nature are to be satisfied at the Closing), or at such other time and place as Buyer and Seller may mutually agree in writing.",
        "2.3 Closing Deliverables of Seller. At the Closing, Seller shall deliver or cause to be delivered to Buyer each of the following: (a) an assignment of the Acquired Interests, duly executed by Seller; (b) a certificate from Seller certifying the satisfaction of the conditions in Section 7.2; (c) a non-foreign affidavit dated as of the Closing Date, sworn under penalty of perjury and in form and substance required under the Treasury Regulations issued pursuant to Section 1445 of the Code.",
        "2.4 Closing Deliverables of Buyer. At the Closing, Buyer shall deliver or cause to be delivered to Seller: (a) the Purchase Price, in accordance with Section 3.1; (b) a certificate from Buyer certifying the satisfaction of the conditions set forth in Section 7.3; (c) evidence reasonably satisfactory to Seller that all required approvals and consents of Governmental Authorities have been obtained.",
    ])

    # =========================================================================
    # PAGE 5: Article III - Consideration
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    add_section_text(page, 60, "ARTICLE III - CONSIDERATION AND PAYMENT", [
        "3.1 Purchase Price. In consideration for the Acquired Interests, Buyer shall pay to Seller an aggregate purchase price equal to Four Hundred Seventy-Five Million Dollars ($475,000,000) (the \"Base Purchase Price\"), subject to adjustment as provided in Section 3.2 (as so adjusted, the \"Purchase Price\").",
        "3.2 Purchase Price Adjustment. (a) Not later than ninety (90) days following the Closing Date, Buyer shall prepare and deliver to Seller a statement (the \"Closing Statement\") setting forth Buyer's calculation of: (i) the Closing Net Working Capital; (ii) the Closing Cash; (iii) the Closing Indebtedness; and (iv) the Closing Transaction Expenses.",
        "3.3 Payment Method. The Purchase Price shall be paid as follows: (a) at the Closing, Buyer shall pay to Seller, by wire transfer of immediately available funds, an amount equal to the Estimated Purchase Price minus the Escrow Amount; and (b) at the Closing, Buyer shall deposit the Escrow Amount with the Escrow Agent in accordance with Section 11.1.",
        "3.4 Withholding. Buyer shall be entitled to deduct and withhold from any amounts payable pursuant to this Agreement such amounts as may be required to be deducted and withheld under applicable Tax Law.",
    ])

    # =========================================================================
    # PAGE 6: Article IV - Seller Representations (Part 1)
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    add_section_text(page, 60, "ARTICLE IV - REPRESENTATIONS AND WARRANTIES OF SELLER", [
        "Seller hereby represents and warrants to Buyer as of the date hereof and as of the Closing Date as follows:",
        "4.1 Organization and Good Standing. The Company is a limited liability company duly organized, validly existing, and in good standing under the Laws of the State of Delaware. The Company has all requisite limited liability company power and authority to own, lease, and operate its properties and assets and to carry on its business as currently conducted.",
        "4.2 Authority; Binding Effect. Seller has the full right, power, and authority to execute and deliver this Agreement and to perform its obligations hereunder. This Agreement has been duly authorized, executed, and delivered by Seller and constitutes the legal, valid, and binding obligation of Seller, enforceable against Seller in accordance with its terms.",
        "4.3 Financial Statements. Seller has delivered to Buyer true, correct, and complete copies of: (a) the audited consolidated balance sheets of the Company as of December 31, 2023, and December 31, 2024, and the related audited consolidated statements of income, shareholders' equity, and cash flows for the fiscal years then ended; and (b) the unaudited consolidated balance sheet of the Company as of September 30, 2025.",
        "4.4 No Undisclosed Liabilities. The Company does not have any liability, indebtedness, obligation, expense, claim, deficiency, guaranty, or endorsement of any kind, whether accrued, absolute, contingent, matured, or unmatured, except for liabilities reflected or reserved against in the Latest Balance Sheet.",
    ])

    # =========================================================================
    # PAGE 7: Article IV - Seller Representations (Part 2)
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    add_section_text(page, 60, "ARTICLE IV - REPRESENTATIONS AND WARRANTIES OF SELLER (CONTINUED)", [
        "4.5 Material Contracts. Section 4.5 of the Disclosure Schedules sets forth a complete and accurate list of all Material Contracts. Each Material Contract is valid, binding, and enforceable in accordance with its terms and is in full force and effect. Neither the Company nor, to Seller's Knowledge, any other party thereto is in material breach of or material default under any Material Contract.",
        "4.6 Intellectual Property. The Company owns or has the valid right to use all Intellectual Property necessary for the conduct of its business as currently conducted. To Seller's Knowledge, the conduct of the Company's business does not infringe, misappropriate, or otherwise violate the Intellectual Property rights of any third party.",
        "4.7 Tax Matters. The Company has timely filed all material Tax Returns required to be filed by it. All such Tax Returns are true, correct, and complete in all material respects. The Company has timely paid all material Taxes due and owing, whether or not shown on any Tax Return.",
        "4.8 Employee Matters. Section 4.8 of the Disclosure Schedules contains a complete and accurate list of all employees of the Company, including each employee's name, title, hire date, annual compensation, and work location. The Company is not a party to any collective bargaining agreement or other labor union contract.",
    ])

    # =========================================================================
    # PAGE 8: Article V - Buyer Representations
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    add_section_text(page, 60, "ARTICLE V - REPRESENTATIONS AND WARRANTIES OF BUYER", [
        "Buyer hereby represents and warrants to Seller as of the date hereof and as of the Closing Date as follows:",
        "5.1 Organization and Good Standing. Buyer is a corporation duly organized, validly existing, and in good standing under the Laws of the State of Delaware. Buyer has all requisite corporate power and authority to own, lease, and operate its properties and to carry on its business as currently conducted.",
        "5.2 Authority; Binding Effect. Buyer has the full corporate right, power, and authority to execute and deliver this Agreement and to consummate the transactions contemplated hereby. The execution, delivery, and performance by Buyer of this Agreement have been duly authorized by all necessary corporate action on the part of Buyer.",
        "5.3 Financial Capability. Buyer has, and at the Closing will have, sufficient funds available to pay the Purchase Price and all fees and expenses related to the transactions contemplated by this Agreement. Buyer's obligations under this Agreement are not contingent upon its ability to obtain financing.",
        "5.4 No Conflicts. The execution, delivery, and performance of this Agreement by Buyer and the consummation of the transactions contemplated hereby do not and will not: (a) violate the certificate of incorporation or bylaws of Buyer; (b) violate any Law applicable to Buyer; or (c) result in a breach of or default under any agreement to which Buyer is a party.",
    ])

    # =========================================================================
    # PAGE 9: Article VI - Covenants
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    add_section_text(page, 60, "ARTICLE VI - COVENANTS AND AGREEMENTS", [
        "6.1 Conduct of Business Pending Closing. From the date hereof until the Closing or the earlier termination of this Agreement, Seller shall cause the Company to: (a) conduct its business only in the Ordinary Course of Business; (b) use commercially reasonable efforts to preserve intact its business relationships with customers, suppliers, and other third parties; and (c) maintain all insurance policies currently in effect.",
        "6.2 Access to Information. From the date hereof until the Closing, Seller shall afford Buyer and its Representatives reasonable access during normal business hours to the properties, books, records, contracts, and personnel of the Company, and shall furnish to Buyer such financial and operating data and other information with respect to the business of the Company as Buyer may reasonably request.",
        "6.3 Exclusivity. From the date hereof until the Closing or the earlier termination of this Agreement, Seller shall not, and shall cause the Company not to, directly or indirectly: (a) solicit, initiate, or encourage any Alternative Transaction Proposal; (b) participate in any discussions or negotiations regarding an Alternative Transaction Proposal; or (c) furnish any information to any Person in connection with an Alternative Transaction Proposal.",
        "6.4 Regulatory Filings. Each party shall use its commercially reasonable efforts to make all filings and obtain all approvals required under applicable Law in connection with the transactions contemplated hereby, including under the Hart-Scott-Rodino Antitrust Improvements Act of 1976.",
    ])

    # =========================================================================
    # PAGE 10: Article VII - Conditions to Closing (Part 1)
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    add_section_text(page, 60, "ARTICLE VII - CONDITIONS TO CLOSING", [
        "7.1 Conditions to Obligations of Both Parties. The obligations of Buyer and Seller to consummate the Closing are subject to the satisfaction or waiver of the following conditions: (a) no Governmental Authority shall have enacted, issued, promulgated, or enforced any Law or Order that has the effect of making the transactions contemplated by this Agreement illegal or otherwise prohibiting the consummation thereof; and (b) all required filings under the HSR Act shall have been made and the applicable waiting period shall have expired or been terminated.",
        "7.2 Conditions to Obligations of Buyer. The obligations of Buyer to consummate the Closing are further subject to the satisfaction or waiver of the following conditions: (a) the representations and warranties of Seller contained in Article IV shall be true and correct in all material respects as of the Closing Date; (b) Seller shall have performed in all material respects all obligations required to be performed by Seller under this Agreement at or prior to the Closing; and (c) since the date of this Agreement, there shall not have occurred a Company Material Adverse Effect.",
        "7.3 Conditions to Obligations of Seller. The obligations of Seller to consummate the Closing are further subject to the satisfaction or waiver of the following conditions: (a) the representations and warranties of Buyer contained in Article V shall be true and correct in all material respects as of the Closing Date; and (b) Buyer shall have performed in all material respects all obligations required to be performed by Buyer under this Agreement at or prior to the Closing.",
    ])

    # =========================================================================
    # PAGE 11: Article VII continued + transition
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    add_section_text(page, 60, "ARTICLE VII - CONDITIONS TO CLOSING (CONTINUED)", [
        "7.4 Frustration of Conditions. No party may rely on the failure of any condition to its own obligation to consummate the Closing set forth in this Article VII if such failure was caused by such party's failure to use commercially reasonable efforts to satisfy such condition or by such party's breach of any provision of this Agreement.",
        "7.5 Waiver of Conditions. Any condition set forth in this Article VII that is for the benefit of a party may be waived by such party in its sole discretion by delivering a written notice of such waiver to the other party. No waiver of any condition shall constitute a waiver of any other condition or of any indemnification right under this Agreement.",
        "7.6 Third Party Consents. Seller shall use commercially reasonable efforts to obtain, prior to the Closing, all consents and approvals from third parties that are required in connection with the consummation of the transactions contemplated by this Agreement. Buyer shall cooperate with Seller in connection with obtaining such consents and approvals.",
        "7.7 Employee Matters. Prior to the Closing, Buyer shall make offers of employment to substantially all employees of the Company on terms and conditions that are substantially comparable to the terms and conditions of their employment with the Company immediately prior to the Closing.",
    ])

    # =========================================================================
    # PAGE 12: Article VIII - Indemnification (Part 1)
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    add_section_text(page, 60, "ARTICLE VIII - INDEMNIFICATION", [
        "8.1 Survival of Representations. The representations and warranties contained in this Agreement shall survive the Closing and continue in full force and effect until the date that is eighteen (18) months following the Closing Date; provided, however, that the Fundamental Representations shall survive until the date that is sixty (60) months following the Closing Date.",
        "8.2 Indemnification by Seller. Subject to the terms and conditions of this Article VIII, from and after the Closing, Seller shall indemnify, defend, and hold harmless Buyer and its Affiliates, officers, directors, employees, agents, and Representatives (collectively, the \"Buyer Indemnified Parties\") from and against any and all losses, damages, liabilities, costs, and expenses (including reasonable attorneys' fees) (\"Losses\") arising out of or resulting from: (a) any breach of any representation or warranty of Seller contained in this Agreement; (b) any breach of any covenant or agreement of Seller contained in this Agreement; or (c) any Pre-Closing Tax liabilities of the Company.",
        "8.3 Indemnification by Buyer. Subject to the terms and conditions of this Article VIII, from and after the Closing, Buyer shall indemnify, defend, and hold harmless Seller and its Affiliates, officers, directors, employees, agents, and Representatives from and against any and all Losses arising out of or resulting from: (a) any breach of any representation or warranty of Buyer contained in this Agreement; or (b) any breach of any covenant or agreement of Buyer contained in this Agreement.",
        "8.4 Limitation on Indemnification. (a) Seller shall not be obligated to indemnify Buyer Indemnified Parties until the aggregate amount of all Losses exceeds Two Million Five Hundred Thousand Dollars ($2,500,000) (the \"Deductible\"), in which event Seller shall be obligated to indemnify for all Losses in excess of the Deductible. (b) The maximum aggregate liability of Seller for indemnification under Section 8.2(a) shall not exceed Forty-Seven Million Five Hundred Thousand Dollars ($47,500,000) (the \"Cap\").",
    ])

    # =========================================================================
    # PAGE 13: Article VIII - Indemnification (Part 2)
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    add_section_text(page, 60, "ARTICLE VIII - INDEMNIFICATION (CONTINUED)", [
        "8.5 Indemnification Procedures. (a) If any Buyer Indemnified Party or Seller Indemnified Party (an \"Indemnified Party\") receives notice of any claim, demand, action, or proceeding by a third party (a \"Third-Party Claim\") for which indemnification is sought, the Indemnified Party shall promptly notify the indemnifying party in writing. (b) The indemnifying party shall have the right to assume the defense of any Third-Party Claim with counsel reasonably satisfactory to the Indemnified Party.",
        "8.6 Direct Claims. Any claim for indemnification that does not involve a Third-Party Claim shall be asserted by written notice from the Indemnified Party to the indemnifying party, which notice shall set forth in reasonable detail the nature of the claim, the specific provision of this Agreement upon which the claim is based, and the amount of Losses (to the extent known).",
        "8.7 Mitigation. The Indemnified Party shall use commercially reasonable efforts to mitigate any Losses for which it is entitled to indemnification under this Article VIII. The indemnifying party shall not be liable for any Losses that the Indemnified Party could have reasonably avoided or mitigated.",
        "8.8 Exclusive Remedy. From and after the Closing, the indemnification provisions of this Article VIII shall be the sole and exclusive remedy of the parties and their respective Affiliates for any Losses arising out of or relating to this Agreement or the transactions contemplated hereby, except in cases of fraud or willful misconduct.",
    ])

    # =========================================================================
    # PAGE 14: Article IX - Termination
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    add_section_text(page, 60, "ARTICLE IX - TERMINATION", [
        "9.1 Termination. This Agreement may be terminated at any time prior to the Closing: (a) by mutual written consent of Buyer and Seller; (b) by either Buyer or Seller, if the Closing shall not have occurred on or before September 30, 2025 (the \"Outside Date\"); (c) by Buyer, if Seller shall have breached any of its representations, warranties, covenants, or agreements contained in this Agreement, which breach would give rise to the failure of a condition set forth in Section 7.2; or (d) by Seller, if Buyer shall have breached any of its representations, warranties, covenants, or agreements contained in this Agreement, which breach would give rise to the failure of a condition set forth in Section 7.3.",
        "9.2 Effect of Termination. In the event of the termination of this Agreement in accordance with Section 9.1, this Agreement shall forthwith become void and have no effect, without any liability on the part of any party, except that: (a) the provisions of Section 13.1 (Confidentiality), this Section 9.2, and Article XIV shall survive any termination of this Agreement; and (b) nothing herein shall relieve any party from liability for any willful breach of this Agreement.",
        "9.3 Termination Fee. In the event this Agreement is terminated by Buyer pursuant to Section 9.1(c) as a result of Seller's willful breach, Seller shall pay to Buyer, within five (5) Business Days of such termination, a termination fee in the amount of Twenty-Three Million Seven Hundred Fifty Thousand Dollars ($23,750,000).",
    ])

    # =========================================================================
    # PAGE 15: Article X - Tax Matters
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    add_section_text(page, 60, "ARTICLE X - TAX MATTERS", [
        "10.1 Tax Returns. (a) Seller shall prepare or cause to be prepared and timely file or cause to be timely filed all Tax Returns required to be filed by the Company for any Pre-Closing Tax Period. All such Tax Returns shall be prepared in a manner consistent with past practice, except as otherwise required by applicable Law.",
        "10.2 Cooperation on Tax Matters. After the Closing, each of Buyer and Seller shall (and shall cause their respective Affiliates to) cooperate fully in connection with the preparation and filing of Tax Returns and any Tax proceeding. Such cooperation shall include providing access to books and records, making employees available for interviews and testimony, and providing other reasonable assistance.",
        "10.3 Transfer Taxes. All transfer, documentary, stamp, sales, use, registration, and other similar Taxes and fees incurred in connection with the transactions contemplated by this Agreement shall be borne equally by Buyer and Seller.",
        "10.4 Tax Contests. Buyer shall promptly notify Seller in writing upon receipt of notice of any pending or threatened Tax audit or assessment relating to the Company for any Pre-Closing Tax Period. Seller shall have the right to control, at its own expense, any such Tax contest; provided, however, that Seller shall not settle any such Tax contest without the prior written consent of Buyer.",
    ])

    # =========================================================================
    # PAGE 16: Article XI - Escrow Arrangements
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    add_section_text(page, 60, "ARTICLE XI - ESCROW ARRANGEMENTS", [
        "11.1 Escrow Deposit. At the Closing, Buyer shall deposit Twenty-Three Million Seven Hundred Fifty Thousand Dollars ($23,750,000) (the \"Escrow Amount\") with JPMorgan Chase Bank, N.A. (the \"Escrow Agent\") in accordance with the terms of the Escrow Agreement, to be held and distributed in accordance with the Escrow Agreement and this Agreement.",
        "11.2 Escrow Agreement. Buyer and Seller shall enter into an Escrow Agreement with the Escrow Agent at the Closing in substantially the form attached hereto as Exhibit C. The Escrow Agreement shall provide for the establishment of an escrow account and the terms and conditions governing the deposit, maintenance, and release of the Escrow Amount.",
        "11.3 Release of Escrow. (a) On the date that is eighteen (18) months following the Closing Date (the \"Escrow Release Date\"), the Escrow Agent shall release to Seller an amount equal to the then-remaining Escrow Amount, less any amounts subject to pending indemnification claims. (b) Any amounts retained in escrow on account of pending indemnification claims shall be released upon resolution of such claims.",
        "11.4 Investment of Escrow Amount. The Escrow Amount shall be invested by the Escrow Agent in short-term, investment-grade instruments as directed by mutual agreement of Buyer and Seller, with all investment income being distributed to Seller upon release of the Escrow Amount.",
    ])

    # =========================================================================
    # PAGE 17: Article XII - Non-Competition
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    add_section_text(page, 60, "ARTICLE XII - NON-COMPETITION AND NON-SOLICITATION", [
        "12.1 Non-Competition. For a period of three (3) years following the Closing Date, Seller shall not, and shall cause its Affiliates not to, directly or indirectly, engage in, own, manage, operate, control, or participate in the ownership, management, operation, or control of, any business that competes with the business of the Company as conducted as of the Closing Date within the United States, Canada, and the European Union.",
        "12.2 Non-Solicitation. For a period of two (2) years following the Closing Date, Seller shall not, and shall cause its Affiliates not to, directly or indirectly: (a) solicit, recruit, or hire any employee of the Company or Buyer; or (b) solicit, divert, or take away, or attempt to solicit, divert, or take away, the business of any customer, supplier, or client of the Company.",
        "12.3 Reasonableness. Seller acknowledges that the covenants contained in this Article XII are reasonable and necessary to protect the legitimate business interests of Buyer and the Company, and that any breach of such covenants would result in irreparable harm to Buyer.",
        "12.4 Remedies. In the event of a breach or threatened breach of this Article XII, Buyer shall be entitled to seek injunctive relief in any court of competent jurisdiction, in addition to any other remedies available at law or in equity, without the requirement to post bond.",
    ])

    # =========================================================================
    # PAGE 18: Article XIII - Confidentiality + Article XIV - Miscellaneous + Article XV - Governing Law
    # =========================================================================
    page = doc.new_page(width=W, height=H)
    add_section_text(page, 60, "ARTICLE XIII - CONFIDENTIALITY", [
        "13.1 Confidentiality Obligations. Each party agrees to hold in strict confidence all Confidential Information received from the other party and shall not disclose such Confidential Information to any third party without the prior written consent of the disclosing party, except as required by applicable Law or as necessary to enforce rights under this Agreement.",
    ])
    add_section_text(page, 180, "ARTICLE XIV - MISCELLANEOUS PROVISIONS", [
        "14.1 Entire Agreement. This Agreement, together with the Exhibits, Schedules, and Disclosure Schedules, constitutes the entire agreement between the parties with respect to the subject matter hereof and supersedes all prior negotiations, representations, warranties, commitments, offers, and agreements.",
        "14.2 Amendment. This Agreement may not be amended, modified, or supplemented except by a written instrument executed by both parties.",
        "14.3 Notices. All notices required or permitted to be given under this Agreement shall be in writing and shall be deemed given when delivered personally, sent by confirmed electronic mail, or one (1) Business Day after deposit with a nationally recognized overnight courier.",
    ])
    add_section_text(page, 440, "ARTICLE XV - GOVERNING LAW AND DISPUTE RESOLUTION", [
        "15.1 Governing Law. This Agreement shall be governed by and construed in accordance with the internal Laws of the State of Delaware, without giving effect to any choice or conflict of law provision.",
        "15.2 Dispute Resolution. Any dispute arising out of or relating to this Agreement shall be submitted to binding arbitration administered by the American Arbitration Association in accordance with its Commercial Arbitration Rules. The arbitration shall be conducted in New York, New York.",
    ])

    # Add page numbers to all pages
    for i in range(doc.page_count):
        p = doc[i]
        p.insert_text(
            pymupdf.Point(W / 2 - 10, H - 30),
            str(i + 1),
            fontsize=9,
            fontname="tiro",
            color=(0.4, 0.4, 0.4),
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
