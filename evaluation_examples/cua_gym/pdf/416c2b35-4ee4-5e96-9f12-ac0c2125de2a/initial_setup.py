"""
Initial Setup: Create an 85-page legal document production set
Task ID: pdf_legal_071
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_071'
PROD_DIR = f'{WORKDIR}/legal/production'
OUTPUT = f'{PROD_DIR}/set_2.pdf'


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


# --- Legal content templates ---

CASE_CAPTION = """IN THE UNITED STATES DISTRICT COURT
FOR THE SOUTHERN DISTRICT OF NEW YORK

JONES MANUFACTURING, INC.,
    Plaintiff,

v.                                     Case No. 2024-CV-08391

MERIDIAN SUPPLY CHAIN CORP.,
    Defendant.
"""

DEPOSITION_WITNESSES = [
    ("Rebecca Torres", "VP of Operations, Meridian Supply Chain Corp."),
    ("David Whitfield", "Director of Quality Assurance, Jones Manufacturing"),
    ("Priya Nair", "Senior Procurement Manager, Meridian Supply Chain Corp."),
    ("James Kowalski", "Chief Financial Officer, Jones Manufacturing"),
    ("Linda Cheng", "Contract Compliance Officer, Meridian Supply Chain Corp."),
]

EXHIBIT_TITLES = [
    "Purchase Agreement dated March 15, 2023",
    "Amendment No. 1 to Purchase Agreement dated June 22, 2023",
    "Email correspondence: Torres to Whitfield, August 3, 2023",
    "Quality Inspection Report QIR-2023-0472",
    "Invoice No. INV-2023-09871 dated September 14, 2023",
    "Internal Memorandum: Supply Chain Disruption Analysis",
    "Board of Directors Meeting Minutes, October 2, 2023",
    "Accounts Receivable Aging Report, Q3 2023",
    "Shipping and Delivery Log, July-September 2023",
    "Expert Report of Dr. Samuel Okafor, Ph.D.",
    "Supplemental Expert Report of Dr. Okafor",
    "Deposition Errata Sheet - Rebecca Torres",
    "Deposition Errata Sheet - David Whitfield",
    "Third-Party Subpoena to Apex Logistics, Inc.",
    "Response to Interrogatories, Set One",
    "Response to Requests for Admission, Set One",
    "Defendant's Privilege Log",
    "Plaintiff's Supplemental Disclosure",
    "Settlement Demand Letter dated November 20, 2023",
    "Mediation Statement, December 5, 2023",
]

DEPO_QA_BLOCKS = [
    [
        ("Q", "Could you please state your full name and current position for the record?"),
        ("A", "My name is Rebecca Torres. I am the Vice President of Operations at Meridian Supply Chain Corporation, a position I have held since January 2021."),
        ("Q", "Ms. Torres, directing your attention to Exhibit A, the Purchase Agreement dated March 15, 2023, can you identify this document?"),
        ("A", "Yes, this is the master purchase agreement between Meridian and Jones Manufacturing for the supply of precision-machined titanium alloy components."),
        ("Q", "And what was the total contract value?"),
        ("A", "The initial contract was valued at approximately $4.2 million over a 24-month term, with options for renewal."),
        ("Q", "Were there any modifications to the delivery schedule after execution?"),
        ("A", "Yes, Amendment No. 1, which was executed on June 22, 2023, revised the delivery timeline for Phase 2 components from quarterly to monthly shipments."),
        ("Q", "What prompted that amendment?"),
        ("A", "Jones Manufacturing requested accelerated delivery due to increased demand from their aerospace division. We accommodated the request subject to a 7% price adjustment."),
    ],
    [
        ("Q", "Mr. Whitfield, you serve as Director of Quality Assurance at Jones Manufacturing, correct?"),
        ("A", "That is correct. I have been in that role for approximately eight years."),
        ("Q", "Can you describe the inspection process for incoming shipments from Meridian?"),
        ("A", "Every incoming lot undergoes a three-stage inspection protocol. First, a visual and dimensional check against the engineering drawings. Second, material composition verification using X-ray fluorescence spectroscopy. Third, mechanical property testing including tensile strength and hardness."),
        ("Q", "And what was the rejection rate for Meridian's shipments in Q3 2023?"),
        ("A", "The rejection rate spiked to 14.3% in Q3, which was significantly above our contractual threshold of 2%."),
        ("Q", "What specific defects were identified?"),
        ("A", "The primary defect was dimensional non-conformance. Several lots had tolerances exceeding plus or minus 0.005 inches on critical bore diameters, which rendered the parts unsuitable for our aerospace applications."),
    ],
    [
        ("Q", "Ms. Nair, in your role as Senior Procurement Manager, what oversight did you have of the Jones Manufacturing account?"),
        ("A", "I was the primary relationship manager for the Jones account. I handled day-to-day communications, managed purchase orders, and coordinated logistics."),
        ("Q", "Were you aware of the quality issues raised by Jones Manufacturing in August 2023?"),
        ("A", "I became aware of concerns when Mr. Whitfield sent an email to Ms. Torres on August 3, 2023, which was copied to me, detailing rejected lots."),
        ("Q", "What steps did Meridian take in response?"),
        ("A", "We initiated a root cause analysis with our manufacturing engineering team, implemented additional in-process quality controls, and offered to expedite replacement parts at no additional cost."),
        ("Q", "Did those corrective measures resolve the quality issues?"),
        ("A", "Partially. The October shipment showed improvement with a rejection rate of 5.1%, but that was still above the contractual threshold."),
    ],
    [
        ("Q", "Mr. Kowalski, as CFO of Jones Manufacturing, can you describe the financial impact of the supply chain disruption?"),
        ("A", "The impact was substantial. Due to the defective components from Meridian, we experienced production line shutdowns totaling 47 days in Q3 and Q4 of 2023."),
        ("Q", "Can you quantify the losses?"),
        ("A", "Our forensic accounting team has calculated total damages of $3.87 million, which includes $1.2 million in direct costs for rework and scrap, $1.9 million in lost revenue from delayed customer deliveries, and approximately $770,000 in expediting costs from alternative suppliers."),
        ("Q", "Were there any consequential damages to customer relationships?"),
        ("A", "Yes. We lost our preferred supplier status with Aerotech Defense Systems, our largest aerospace client, which represented approximately $12 million in annual revenue."),
    ],
    [
        ("Q", "Ms. Cheng, as Contract Compliance Officer, did you review the dispute resolution provisions of the Purchase Agreement?"),
        ("A", "Yes, I reviewed them in detail after the quality issues became apparent in September 2023."),
        ("Q", "What did those provisions require?"),
        ("A", "Section 14.2 of the agreement required the parties to engage in good faith negotiations for a period of 30 days before initiating formal dispute resolution. If negotiations failed, the agreement called for binding arbitration under ICC rules."),
        ("Q", "Was the 30-day negotiation period observed?"),
        ("A", "Meridian sent its initial demand letter on November 20, 2023. Jones Manufacturing responded on December 1. However, Jones filed this lawsuit on December 18, which was only 28 days after the demand letter, arguably before the negotiation period had expired."),
    ],
]

MEMO_CONTENT = """MEMORANDUM

TO:     Executive Leadership Team
FROM:   Operations Division
DATE:   September 28, 2023
RE:     Supply Chain Disruption - Jones Manufacturing Account

SUMMARY

This memorandum provides an overview of the ongoing supply chain disruption affecting
our relationship with Jones Manufacturing, Inc. and recommends corrective actions to
mitigate further impact.

BACKGROUND

Since July 2023, Jones Manufacturing has reported quality non-conformances in three
consecutive shipments of precision titanium alloy components under Purchase Agreement
No. PA-2023-0315. The defects primarily involve dimensional tolerances on critical
bore diameters exceeding the specified +/- 0.003 inch threshold.

ROOT CAUSE ANALYSIS

Our manufacturing engineering team has identified two primary contributing factors:

1. Tooling Wear: The CNC milling centers used for the Jones components were operating
   beyond their recommended tool change intervals. The maintenance schedule has since
   been revised from 500 to 350 operating hours between tool replacements.

2. Raw Material Variability: Lot-to-lot variation in the Ti-6Al-4V titanium alloy
   from our primary material supplier (Apex Metals Corp.) contributed to inconsistent
   machining behavior. We have implemented incoming material inspection protocols and
   are qualifying an alternative supplier.

FINANCIAL EXPOSURE

Based on contract terms, our potential liability exposure includes:
- Direct replacement costs:                  $342,000
- Contractual penalty for late delivery:     $185,000
- Potential consequential damage claims:     $1,500,000 - $3,000,000

RECOMMENDED ACTIONS

1. Immediately expedite replacement parts for Lots #47, #48, and #49
2. Engage outside counsel to review liability exposure
3. Propose a meeting with Jones Manufacturing to discuss corrective action plan
4. Evaluate business continuity insurance coverage applicability

This matter requires urgent attention given the December 15, 2023 deadline for
Jones Manufacturing's response to our proposed corrective action plan.
"""

INVOICE_LINES = [
    ("TI-6AL4V-CYL-25", "Titanium Alloy Cylinder, 25mm", 450, 87.50),
    ("TI-6AL4V-BRG-10", "Titanium Alloy Bearing Housing, 10mm", 200, 142.00),
    ("TI-6AL4V-SHF-50", "Titanium Alloy Shaft, 50mm", 120, 215.75),
    ("SS-316L-FLG-DN50", "Stainless Steel Flange, DN50", 300, 63.25),
    ("TI-6AL4V-PLT-3MM", "Titanium Alloy Plate, 3mm", 75, 328.00),
    ("IN-718-DSC-15", "Inconel 718 Disc, 15mm", 180, 195.50),
    ("TI-6AL4V-RNG-20", "Titanium Ring Blank, 20mm", 240, 112.00),
]


def create_initial():
    os.makedirs(PROD_DIR, exist_ok=True)

    doc = pymupdf.open()
    page_width, page_height = 612, 792  # US Letter

    # --- Helper functions ---
    def new_page():
        return doc.new_page(width=page_width, height=page_height)

    def add_header_footer(page, page_label=""):
        """Add simple header/footer to production pages (no Bates, no confidentiality)."""
        # Header line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(54, 54), pymupdf.Point(558, 54))
        shape.finish(color=(0, 0, 0), width=0.5)
        shape.commit()
        # Case reference in header
        page.insert_text(pymupdf.Point(54, 48), "Jones Mfg. v. Meridian Supply - Case No. 2024-CV-08391",
                         fontsize=7, fontname="helv", color=(0.4, 0.4, 0.4))
        # Footer line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(54, 738), pymupdf.Point(558, 738))
        shape.finish(color=(0, 0, 0), width=0.5)
        shape.commit()
        if page_label:
            page.insert_text(pymupdf.Point(280, 755), page_label,
                             fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))

    # ===== PAGE 1: Cover Sheet =====
    pg = new_page()
    pg.insert_text(pymupdf.Point(180, 200), "DOCUMENT PRODUCTION SET 2",
                   fontsize=20, fontname="hebo", color=(0, 0, 0))
    pg.insert_textbox(pymupdf.Rect(100, 260, 512, 450), CASE_CAPTION,
                      fontsize=11, fontname="cour", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_LEFT)
    pg.insert_text(pymupdf.Point(180, 500), "Produced by: Meridian Supply Chain Corp.",
                   fontsize=11, fontname="helv", color=(0, 0, 0))
    pg.insert_text(pymupdf.Point(180, 520), "Date of Production: December 28, 2023",
                   fontsize=11, fontname="helv", color=(0, 0, 0))
    pg.insert_text(pymupdf.Point(180, 540), "Documents: 85 Pages",
                   fontsize=11, fontname="helv", color=(0, 0, 0))
    add_header_footer(pg)

    # ===== PAGE 2: Table of Contents =====
    pg = new_page()
    pg.insert_text(pymupdf.Point(54, 90), "TABLE OF CONTENTS", fontsize=14, fontname="hebo")
    y = 120
    toc_entries = [
        ("Cover Sheet", "1"),
        ("Table of Contents", "2"),
        ("Deposition Transcript - Rebecca Torres (Excerpt)", "3-10"),
        ("Deposition Transcript - David Whitfield (Excerpt)", "11-18"),
        ("Deposition Transcript - Priya Nair (Excerpt)", "19-26"),
        ("Deposition Transcript - James Kowalski (Excerpt)", "27-34"),
        ("Deposition Transcript - Linda Cheng (Excerpt)", "35-42"),
        ("Exhibit A - Purchase Agreement", "43-50"),
        ("Exhibit B - Amendment No. 1", "51-55"),
        ("Exhibit C - Email Correspondence", "56-60"),
        ("Exhibit D - Quality Inspection Report", "61-65"),
        ("Exhibit E - Invoice No. INV-2023-09871", "66-68"),
        ("Exhibit F - Internal Memorandum", "69-72"),
        ("Exhibit G - Shipping and Delivery Log", "73-77"),
        ("Exhibit H - Expert Report (Excerpt)", "78-82"),
        ("Exhibit I - Privilege Log", "83-85"),
    ]
    for title, pages in toc_entries:
        pg.insert_text(pymupdf.Point(72, y), title, fontsize=10, fontname="helv")
        pg.insert_text(pymupdf.Point(500, y), pages, fontsize=10, fontname="helv")
        y += 18
    add_header_footer(pg, "Page 2")

    # ===== PAGES 3-42: Deposition Transcripts (5 witnesses x 8 pages each) =====
    for w_idx, (witness_name, witness_title) in enumerate(DEPOSITION_WITNESSES):
        qa_block = DEPO_QA_BLOCKS[w_idx]
        start_page = 3 + w_idx * 8

        for sub_page in range(8):
            pg = new_page()
            page_num = start_page + sub_page

            # Deposition header
            pg.insert_text(pymupdf.Point(54, 80), f"DEPOSITION OF {witness_name.upper()}",
                           fontsize=12, fontname="hebo")
            pg.insert_text(pymupdf.Point(54, 96), f"{witness_title}",
                           fontsize=9, fontname="heit", color=(0.3, 0.3, 0.3))
            pg.insert_text(pymupdf.Point(54, 112),
                           f"Taken on behalf of the Plaintiff, Jones Manufacturing, Inc.",
                           fontsize=9, fontname="helv")

            # Line numbers and Q&A content
            y = 145
            line_num = sub_page * 25 + 1

            if sub_page == 0:
                # First page of this witness: use actual Q&A
                for role, text in qa_block:
                    if y > 700:
                        break
                    pg.insert_text(pymupdf.Point(36, y), str(line_num), fontsize=8, fontname="cour",
                                   color=(0.5, 0.5, 0.5))
                    prefix = f"    {role}." if role == "Q" else f"    {role}."
                    # Insert wrapped text
                    rect = pymupdf.Rect(72, y - 10, 540, y + 40)
                    pg.insert_textbox(rect, f"{prefix}  {text}", fontsize=9, fontname="helv",
                                      align=pymupdf.TEXT_ALIGN_LEFT)
                    y += 52
                    line_num += 3
            else:
                # Continuation pages: generate realistic Q&A filler
                continuation_qa = [
                    ("Q", f"Continuing with your testimony regarding the events of {['July', 'August', 'September', 'October', 'November', 'December', 'January'][sub_page % 7]} 2023, do you recall any additional communications?"),
                    ("A", f"Yes, there were several email exchanges and at least two telephone conferences during that period regarding the status of outstanding deliveries and corrective actions."),
                    ("Q", "Can you describe the substance of those communications?"),
                    ("A", f"The communications primarily focused on the inspection results for Lots {45 + sub_page * 3} through {48 + sub_page * 3} and the proposed remediation timeline. There were also discussions about potential credits against future purchase orders."),
                    ("Q", "Were any of those communications documented?"),
                    ("A", "Yes, I believe copies of the relevant emails were produced as part of the discovery process. I also maintained personal notes from the telephone conferences."),
                    ("Q", f"Directing your attention to Exhibit {chr(65 + sub_page)}, do you recognize this document?"),
                    ("A", f"Yes, this appears to be a copy of the {'internal report' if sub_page % 2 == 0 else 'correspondence'} I referenced in my earlier testimony."),
                ]
                for role, text in continuation_qa:
                    if y > 700:
                        break
                    pg.insert_text(pymupdf.Point(36, y), str(line_num), fontsize=8, fontname="cour",
                                   color=(0.5, 0.5, 0.5))
                    rect = pymupdf.Rect(72, y - 10, 540, y + 40)
                    pg.insert_textbox(rect, f"    {role}.  {text}", fontsize=9, fontname="helv",
                                      align=pymupdf.TEXT_ALIGN_LEFT)
                    y += 52
                    line_num += 3

            add_header_footer(pg, f"Page {page_num}")

    # ===== PAGES 43-50: Exhibit A - Purchase Agreement =====
    for sub_page in range(8):
        pg = new_page()
        page_num = 43 + sub_page
        if sub_page == 0:
            pg.insert_text(pymupdf.Point(200, 100), "EXHIBIT A", fontsize=16, fontname="hebo")
            pg.insert_text(pymupdf.Point(150, 140), "PURCHASE AGREEMENT", fontsize=14, fontname="hebo")
            pg.insert_textbox(pymupdf.Rect(72, 180, 540, 350), CASE_CAPTION,
                              fontsize=10, fontname="cour")
            sections = [
                "1. DEFINITIONS AND INTERPRETATION",
                "   1.1 In this Agreement, unless the context otherwise requires:",
                "   'Buyer' means Jones Manufacturing, Inc.",
                "   'Seller' means Meridian Supply Chain Corporation.",
                "   'Products' means precision-machined titanium alloy components as specified in Schedule A.",
                "   'Contract Price' means $4,200,000.00 USD for the Initial Term.",
                "",
                "2. SCOPE OF SUPPLY",
                "   2.1 The Seller agrees to manufacture and deliver the Products in accordance with",
                "       the specifications set forth in Schedule A attached hereto.",
                "   2.2 All Products shall conform to ASTM B348 and AMS 4928 standards.",
            ]
            y = 380
            for line in sections:
                pg.insert_text(pymupdf.Point(72, y), line, fontsize=9, fontname="helv")
                y += 14
        else:
            section_num = sub_page + 2
            sections = {
                1: ("3. DELIVERY AND ACCEPTANCE",
                    ["3.1 Delivery shall be FOB Seller's facility in Newark, NJ.",
                     "3.2 Buyer shall inspect all deliveries within 10 business days.",
                     "3.3 Acceptance shall be deemed to have occurred unless Buyer provides",
                     "    written notice of rejection within the inspection period.",
                     "3.4 Risk of loss transfers to Buyer upon delivery to the carrier.",
                     "",
                     "4. PRICE AND PAYMENT",
                     "4.1 Prices are as set forth in Schedule B attached hereto.",
                     "4.2 Payment terms: Net 45 days from date of invoice.",
                     "4.3 Late payments shall accrue interest at 1.5% per month."]),
                2: ("5. QUALITY REQUIREMENTS",
                    ["5.1 All Products shall meet the quality standards specified in Schedule C.",
                     "5.2 Seller shall maintain ISO 9001:2015 certification throughout the Term.",
                     "5.3 Buyer reserves the right to conduct quality audits at Seller's facility",
                     "    upon 5 business days' prior written notice.",
                     "5.4 Defective Products shall be replaced at Seller's cost within 15 business days.",
                     "5.5 The maximum acceptable defect rate is 2.0% per lot delivered.",
                     "",
                     "6. TERM AND TERMINATION",
                     "6.1 The Initial Term is 24 months from the Effective Date.",
                     "6.2 Either party may terminate for material breach upon 30 days' written notice."]),
                3: ("7. WARRANTIES",
                    ["7.1 Seller warrants that all Products shall be free from defects in material",
                     "    and workmanship for a period of 12 months from delivery.",
                     "7.2 Seller warrants compliance with all applicable laws and regulations.",
                     "7.3 THE WARRANTIES SET FORTH HEREIN ARE EXCLUSIVE AND IN LIEU OF ALL",
                     "    OTHER WARRANTIES, EXPRESS OR IMPLIED.",
                     "",
                     "8. LIMITATION OF LIABILITY",
                     "8.1 Neither party's total liability shall exceed the Contract Price.",
                     "8.2 Neither party shall be liable for indirect, consequential, or punitive damages,",
                     "    except in cases of willful misconduct or gross negligence."]),
                4: ("9. INTELLECTUAL PROPERTY",
                    ["9.1 All designs and specifications provided by Buyer remain Buyer's property.",
                     "9.2 Seller shall not use Buyer's intellectual property except as necessary",
                     "    to perform under this Agreement.",
                     "",
                     "10. CONFIDENTIALITY",
                     "10.1 Each party agrees to maintain the confidentiality of the other party's",
                     "     proprietary information for a period of 5 years.",
                     "10.2 This obligation shall survive termination of this Agreement."]),
                5: ("11. FORCE MAJEURE",
                    ["11.1 Neither party shall be liable for failure to perform due to events beyond",
                     "     its reasonable control, including natural disasters, war, pandemic, or",
                     "     government actions.",
                     "11.2 The affected party must provide notice within 48 hours of such event.",
                     "",
                     "12. INSURANCE",
                     "12.1 Seller shall maintain commercial general liability insurance with",
                     "     minimum coverage of $5,000,000 per occurrence.",
                     "12.2 Seller shall provide certificates of insurance upon request."]),
                6: ("13. GOVERNING LAW",
                    ["13.1 This Agreement shall be governed by the laws of the State of New York.",
                     "13.2 The parties submit to the exclusive jurisdiction of the federal and",
                     "     state courts located in the Southern District of New York.",
                     "",
                     "14. DISPUTE RESOLUTION",
                     "14.1 The parties agree to attempt to resolve any dispute through good faith",
                     "     negotiation for a period of 30 days.",
                     "14.2 If negotiation fails, disputes shall be resolved by binding arbitration",
                     "     under the rules of the International Chamber of Commerce (ICC).",
                     "14.3 The seat of arbitration shall be New York, New York."]),
                7: ("SIGNATURES",
                    ["IN WITNESS WHEREOF, the parties have executed this Agreement as of",
                     "March 15, 2023.",
                     "",
                     "JONES MANUFACTURING, INC.",
                     "",
                     "By: ___________________________",
                     "Name: Thomas R. Jones III",
                     "Title: Chief Executive Officer",
                     "",
                     "MERIDIAN SUPPLY CHAIN CORPORATION",
                     "",
                     "By: ___________________________",
                     "Name: Angela M. Vasquez",
                     "Title: President and CEO"]),
            }
            if sub_page in sections:
                title, lines = sections[sub_page]
                pg.insert_text(pymupdf.Point(72, 90), title, fontsize=11, fontname="hebo")
                y = 120
                for line in lines:
                    pg.insert_text(pymupdf.Point(72, y), line, fontsize=9, fontname="helv")
                    y += 14
        add_header_footer(pg, f"Page {page_num}")

    # ===== PAGES 51-55: Exhibit B - Amendment No. 1 =====
    for sub_page in range(5):
        pg = new_page()
        page_num = 51 + sub_page
        if sub_page == 0:
            pg.insert_text(pymupdf.Point(200, 100), "EXHIBIT B", fontsize=16, fontname="hebo")
            pg.insert_text(pymupdf.Point(100, 140), "AMENDMENT NO. 1 TO PURCHASE AGREEMENT",
                           fontsize=13, fontname="hebo")
            pg.insert_text(pymupdf.Point(72, 200), "This Amendment No. 1 ('Amendment') is entered into as of June 22, 2023,",
                           fontsize=10, fontname="helv")
            pg.insert_text(pymupdf.Point(72, 218), "by and between Jones Manufacturing, Inc. ('Buyer') and Meridian Supply",
                           fontsize=10, fontname="helv")
            pg.insert_text(pymupdf.Point(72, 236), "Chain Corporation ('Seller').",
                           fontsize=10, fontname="helv")
            amend_text = """WHEREAS, the parties entered into that certain Purchase Agreement dated March 15, 2023 (the 'Agreement'); and

WHEREAS, the parties desire to amend the Agreement to modify the delivery schedule and pricing terms for Phase 2 components;

NOW, THEREFORE, in consideration of the mutual covenants herein, the parties agree as follows:

1. Section 3.1 of the Agreement is hereby amended to provide for monthly delivery of Phase 2 components, in lieu of the original quarterly delivery schedule.

2. Schedule B (Pricing) is amended to reflect a 7% increase in unit prices for Phase 2 components, effective July 1, 2023, to account for the accelerated production and delivery requirements.

3. All other terms and conditions of the Agreement remain in full force and effect."""
            pg.insert_textbox(pymupdf.Rect(72, 270, 540, 650), amend_text,
                              fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_LEFT)
        else:
            pg.insert_text(pymupdf.Point(72, 90),
                           f"Amendment No. 1 - Schedule {'ABCDE'[sub_page - 1]} (Revised)",
                           fontsize=11, fontname="hebo")
            schedule_items = [
                f"  Item {i+1}: Component {['TI-CYL-25', 'TI-BRG-10', 'TI-SHF-50', 'SS-FLG-DN50', 'TI-PLT-3MM'][i % 5]} - "
                f"Revised unit price: ${[93.63, 151.94, 230.85, 67.68, 350.96][i % 5]:.2f} - "
                f"Monthly quantity: {[38, 17, 10, 25, 7][i % 5]}"
                for i in range(10)
            ]
            y = 120
            for item in schedule_items:
                pg.insert_text(pymupdf.Point(72, y), item, fontsize=9, fontname="helv")
                y += 16
        add_header_footer(pg, f"Page {page_num}")

    # ===== PAGES 56-60: Exhibit C - Email Correspondence =====
    emails = [
        {
            "from": "Rebecca Torres <rtorres@meridiansupply.com>",
            "to": "David Whitfield <dwhitfield@jonesmfg.com>",
            "cc": "Priya Nair <pnair@meridiansupply.com>",
            "date": "August 3, 2023 2:47 PM EST",
            "subject": "RE: Quality Concerns - Lots #47-49",
            "body": """David,

Thank you for your detailed report regarding the dimensional non-conformances identified in Lots #47 through #49. We take these findings very seriously and have already initiated a root cause analysis with our manufacturing engineering team.

Our preliminary assessment indicates that tooling wear on CNC Mill #7 may be a contributing factor. We have taken the machine offline for inspection and recalibration.

I would like to schedule a call for next week to discuss our corrective action plan. Would Tuesday or Wednesday work for your team?

Best regards,
Rebecca Torres
VP of Operations
Meridian Supply Chain Corporation"""
        },
        {
            "from": "David Whitfield <dwhitfield@jonesmfg.com>",
            "to": "Rebecca Torres <rtorres@meridiansupply.com>",
            "cc": "James Kowalski <jkowalski@jonesmfg.com>",
            "date": "August 4, 2023 9:15 AM EST",
            "subject": "RE: RE: Quality Concerns - Lots #47-49",
            "body": """Rebecca,

Thank you for your prompt response. However, I must convey the severity of this situation. The 14.3% rejection rate is unacceptable and has already caused significant disruption to our production schedule.

We have had to source emergency replacement parts from Titanium Precision Works at a premium, and our Aerotech Defense delivery timeline is now at risk.

Wednesday at 10 AM works for our team. I will send a calendar invite.

David Whitfield
Director of Quality Assurance
Jones Manufacturing, Inc."""
        },
        {
            "from": "Priya Nair <pnair@meridiansupply.com>",
            "to": "David Whitfield <dwhitfield@jonesmfg.com>",
            "date": "August 7, 2023 4:30 PM EST",
            "subject": "Corrective Action Plan - Lots #47-49",
            "body": """David,

Following our call last Wednesday, please find attached our formal Corrective Action Plan (CAP) for the quality issues identified in Lots #47-49.

Key measures include:
- Immediate retooling of CNC Mill #7 (completed August 5)
- Reduction of tool change interval from 500 to 350 operating hours
- Implementation of additional in-process SPC monitoring
- 100% dimensional inspection on next three lots
- Expedited replacement of rejected parts (ETA: August 25)

We are committed to restoring the quality performance you expect from Meridian.

Best regards,
Priya Nair
Senior Procurement Manager"""
        },
    ]
    for e_idx, email in enumerate(emails):
        pg = new_page()
        page_num = 56 + e_idx
        if e_idx == 0:
            pg.insert_text(pymupdf.Point(200, 80), "EXHIBIT C", fontsize=16, fontname="hebo")
            pg.insert_text(pymupdf.Point(130, 110), "EMAIL CORRESPONDENCE", fontsize=13, fontname="hebo")
            start_y = 150
        else:
            start_y = 80
        pg.insert_text(pymupdf.Point(72, start_y), f"From: {email['from']}", fontsize=9, fontname="hebo")
        pg.insert_text(pymupdf.Point(72, start_y + 14), f"To: {email['to']}", fontsize=9, fontname="helv")
        pg.insert_text(pymupdf.Point(72, start_y + 28), f"CC: {email.get('cc', '')}", fontsize=9, fontname="helv")
        pg.insert_text(pymupdf.Point(72, start_y + 42), f"Date: {email['date']}", fontsize=9, fontname="helv")
        pg.insert_text(pymupdf.Point(72, start_y + 56), f"Subject: {email['subject']}", fontsize=9, fontname="hebo")
        # Separator
        shape = pg.new_shape()
        shape.draw_line(pymupdf.Point(72, start_y + 68), pymupdf.Point(540, start_y + 68))
        shape.finish(color=(0.5, 0.5, 0.5), width=0.5)
        shape.commit()
        pg.insert_textbox(pymupdf.Rect(72, start_y + 78, 540, 720), email['body'],
                          fontsize=9, fontname="helv", align=pymupdf.TEXT_ALIGN_LEFT)
        add_header_footer(pg, f"Page {page_num}")

    # Pages 59-60: additional email threads
    for extra in range(2):
        pg = new_page()
        page_num = 59 + extra
        pg.insert_text(pymupdf.Point(72, 80), f"From: {'rtorres@meridiansupply.com' if extra == 0 else 'jkowalski@jonesmfg.com'}",
                       fontsize=9, fontname="hebo")
        pg.insert_text(pymupdf.Point(72, 94), f"Date: {'September 15' if extra == 0 else 'October 2'}, 2023",
                       fontsize=9, fontname="helv")
        pg.insert_text(pymupdf.Point(72, 108), f"Subject: {'Follow-up: Corrective Action Status' if extra == 0 else 'Formal Notice of Breach'}",
                       fontsize=9, fontname="hebo")
        filler = f"{'This email provides an update on the corrective actions implemented since August. The October shipment showed a rejection rate of 5.1%, which represents significant improvement but remains above the contractual threshold of 2.0%.' if extra == 0 else 'This email constitutes formal notice of material breach of Section 5.5 of the Purchase Agreement. Jones Manufacturing reserves all rights and remedies available under the Agreement and applicable law.'}"
        pg.insert_textbox(pymupdf.Rect(72, 130, 540, 500), filler,
                          fontsize=9, fontname="helv", align=pymupdf.TEXT_ALIGN_LEFT)
        add_header_footer(pg, f"Page {page_num}")

    # ===== PAGES 61-65: Exhibit D - Quality Inspection Report =====
    for sub_page in range(5):
        pg = new_page()
        page_num = 61 + sub_page
        if sub_page == 0:
            pg.insert_text(pymupdf.Point(200, 80), "EXHIBIT D", fontsize=16, fontname="hebo")
            pg.insert_text(pymupdf.Point(100, 110), "QUALITY INSPECTION REPORT QIR-2023-0472",
                           fontsize=12, fontname="hebo")
            details = [
                "Report Number: QIR-2023-0472",
                "Date of Inspection: August 1, 2023",
                "Inspector: David Whitfield, Director of Quality Assurance",
                "Lot Numbers: #47, #48, #49",
                "Supplier: Meridian Supply Chain Corporation",
                "Product: Precision Titanium Alloy Components (Ti-6Al-4V)",
                "",
                "INSPECTION RESULTS SUMMARY:",
                "",
                "Lot #47 (450 units): 58 units rejected (12.9% rejection rate)",
                "  - 42 units: Bore diameter exceeding +0.005 inch tolerance",
                "  - 16 units: Surface finish Ra > 32 microinches (spec: Ra < 16)",
                "",
                "Lot #48 (200 units): 31 units rejected (15.5% rejection rate)",
                "  - 28 units: Bore diameter non-conformance",
                "  - 3 units: Material hardness below specification (HRC 34 vs. min HRC 36)",
                "",
                "Lot #49 (120 units): 17 units rejected (14.2% rejection rate)",
                "  - 14 units: Bore diameter exceeding tolerance",
                "  - 3 units: Thread gauge failure (Class 3A)",
            ]
            y = 150
            for line in details:
                pg.insert_text(pymupdf.Point(72, y), line, fontsize=9, fontname="helv" if not line.startswith("INSP") else "hebo")
                y += 14
        else:
            pg.insert_text(pymupdf.Point(72, 80), f"QIR-2023-0472 - Detailed Measurements (Page {sub_page + 1})",
                           fontsize=11, fontname="hebo")
            # Measurement table simulation
            y = 110
            headers = ["Part ID", "Bore Dia (in)", "Spec Min", "Spec Max", "Result", "Status"]
            x_positions = [72, 160, 260, 340, 420, 500]
            for i, h in enumerate(headers):
                pg.insert_text(pymupdf.Point(x_positions[i], y), h, fontsize=8, fontname="hebo")
            y += 16
            for row in range(25):
                part_num = (sub_page - 1) * 25 + row + 1
                bore = 1.0000 + (0.001 * ((part_num * 7 + 3) % 13) - 0.005)
                status = "FAIL" if abs(bore - 1.0000) > 0.003 else "PASS"
                vals = [
                    f"MC-{47 + part_num // 40}-{part_num:04d}",
                    f"{bore:.4f}",
                    "0.9970",
                    "1.0030",
                    f"{bore:.4f}",
                    status,
                ]
                color = (1, 0, 0) if status == "FAIL" else (0, 0.5, 0)
                for i, v in enumerate(vals):
                    pg.insert_text(pymupdf.Point(x_positions[i], y), v,
                                   fontsize=7, fontname="cour", color=color if i == 5 else (0, 0, 0))
                y += 12
        add_header_footer(pg, f"Page {page_num}")

    # ===== PAGES 66-68: Exhibit E - Invoice =====
    for sub_page in range(3):
        pg = new_page()
        page_num = 66 + sub_page
        if sub_page == 0:
            pg.insert_text(pymupdf.Point(200, 80), "EXHIBIT E", fontsize=16, fontname="hebo")
            pg.insert_text(pymupdf.Point(100, 120), "INVOICE", fontsize=18, fontname="hebo")
            pg.insert_text(pymupdf.Point(72, 160), "Invoice No: INV-2023-09871", fontsize=10, fontname="hebo")
            pg.insert_text(pymupdf.Point(72, 178), "Date: September 14, 2023", fontsize=10, fontname="helv")
            pg.insert_text(pymupdf.Point(72, 196), "Terms: Net 45", fontsize=10, fontname="helv")
            pg.insert_text(pymupdf.Point(72, 214), "Due Date: October 29, 2023", fontsize=10, fontname="helv")
            pg.insert_text(pymupdf.Point(72, 250), "Bill To:", fontsize=10, fontname="hebo")
            pg.insert_text(pymupdf.Point(72, 266), "Jones Manufacturing, Inc.", fontsize=10, fontname="helv")
            pg.insert_text(pymupdf.Point(72, 280), "1847 Industrial Parkway", fontsize=10, fontname="helv")
            pg.insert_text(pymupdf.Point(72, 294), "Rochester, NY 14624", fontsize=10, fontname="helv")

            # Table header
            y = 340
            cols = [72, 180, 360, 420, 490]
            hdrs = ["Part Number", "Description", "Qty", "Unit Price", "Total"]
            for i, h in enumerate(hdrs):
                pg.insert_text(pymupdf.Point(cols[i], y), h, fontsize=9, fontname="hebo")
            shape = pg.new_shape()
            shape.draw_line(pymupdf.Point(72, y + 4), pymupdf.Point(558, y + 4))
            shape.finish(color=(0, 0, 0), width=0.5)
            shape.commit()
            y += 18
            grand_total = 0
            for part_no, desc, qty, price in INVOICE_LINES:
                total = qty * price
                grand_total += total
                pg.insert_text(pymupdf.Point(cols[0], y), part_no, fontsize=8, fontname="cour")
                pg.insert_text(pymupdf.Point(cols[1], y), desc[:30], fontsize=8, fontname="helv")
                pg.insert_text(pymupdf.Point(cols[2], y), str(qty), fontsize=8, fontname="helv")
                pg.insert_text(pymupdf.Point(cols[3], y), f"${price:,.2f}", fontsize=8, fontname="helv")
                pg.insert_text(pymupdf.Point(cols[4], y), f"${total:,.2f}", fontsize=8, fontname="helv")
                y += 14
            shape = pg.new_shape()
            shape.draw_line(pymupdf.Point(420, y + 2), pymupdf.Point(558, y + 2))
            shape.finish(color=(0, 0, 0), width=1)
            shape.commit()
            y += 18
            pg.insert_text(pymupdf.Point(420, y), "TOTAL:", fontsize=10, fontname="hebo")
            pg.insert_text(pymupdf.Point(490, y), f"${grand_total:,.2f}", fontsize=10, fontname="hebo")
        else:
            pg.insert_text(pymupdf.Point(72, 80), f"Invoice INV-2023-09871 - {'Payment History' if sub_page == 1 else 'Terms and Conditions'}",
                           fontsize=11, fontname="hebo")
            if sub_page == 1:
                text = "Payment Status: OVERDUE\nOriginal Due Date: October 29, 2023\nDays Past Due: 60 (as of December 28, 2023)\nAccrued Interest: $4,218.75 (1.5% per month per Section 4.3)\n\nPayment History:\n- No payments received as of the date of this production."
            else:
                text = "Standard Terms and Conditions apply per the Purchase Agreement dated March 15, 2023.\n\nAll amounts are in United States Dollars (USD).\nSeller retains a security interest in all Products until payment in full.\nDisputes regarding this invoice must be raised within 15 business days of receipt."
            pg.insert_textbox(pymupdf.Rect(72, 110, 540, 500), text,
                              fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_LEFT)
        add_header_footer(pg, f"Page {page_num}")

    # ===== PAGES 69-72: Exhibit F - Internal Memorandum =====
    for sub_page in range(4):
        pg = new_page()
        page_num = 69 + sub_page
        if sub_page == 0:
            pg.insert_text(pymupdf.Point(200, 80), "EXHIBIT F", fontsize=16, fontname="hebo")
            pg.insert_textbox(pymupdf.Rect(72, 120, 540, 720), MEMO_CONTENT,
                              fontsize=9.5, fontname="helv", align=pymupdf.TEXT_ALIGN_LEFT)
        else:
            pg.insert_text(pymupdf.Point(72, 80), f"Memorandum - Appendix {sub_page}",
                           fontsize=11, fontname="hebo")
            appendix_text = {
                1: "APPENDIX 1: TIMELINE OF EVENTS\n\nMarch 15, 2023 - Purchase Agreement executed\nJune 22, 2023 - Amendment No. 1 executed\nJuly 15, 2023 - Lot #47 delivered; inspection reveals defects\nJuly 28, 2023 - Lots #48 and #49 delivered\nAugust 1, 2023 - QIR-2023-0472 issued\nAugust 3, 2023 - Torres-Whitfield email exchange\nAugust 7, 2023 - Corrective Action Plan submitted\nSeptember 14, 2023 - Invoice INV-2023-09871 issued\nSeptember 28, 2023 - This memorandum issued\nOctober 2, 2023 - Formal notice of breach sent\nNovember 20, 2023 - Settlement demand letter\nDecember 18, 2023 - Lawsuit filed",
                2: "APPENDIX 2: COST BREAKDOWN\n\nDirect Replacement Costs:\n  Emergency sourcing from Titanium Precision Works: $218,000\n  Expedited shipping (air freight): $47,000\n  Quality re-inspection costs: $28,000\n  Scrap disposal of rejected parts: $49,000\n  Subtotal: $342,000\n\nContractual Penalties:\n  Late delivery penalty (Section 3.3): $185,000\n\nConsequential Exposure (estimated):\n  Production line downtime (47 days x $40,000/day): $1,880,000\n  Lost Aerotech preferred status: $800,000 - $2,000,000\n  Subtotal: $2,680,000 - $3,880,000",
                3: "APPENDIX 3: CORRECTIVE ACTION TRACKING\n\nAction Item 1: Retooling CNC Mill #7\n  Status: COMPLETED (August 5, 2023)\n  Responsible: Manufacturing Engineering\n\nAction Item 2: Reduce tool change interval\n  Status: IMPLEMENTED (August 10, 2023)\n  New interval: 350 operating hours (from 500)\n\nAction Item 3: SPC monitoring implementation\n  Status: IN PROGRESS\n  Target completion: September 30, 2023\n\nAction Item 4: 100% dimensional inspection\n  Status: ACTIVE for Lots #50-52\n\nAction Item 5: Qualify alternative Ti-6Al-4V supplier\n  Status: PENDING (RFQ issued to 3 suppliers)",
            }
            pg.insert_textbox(pymupdf.Rect(72, 110, 540, 720),
                              appendix_text.get(sub_page, ""),
                              fontsize=9, fontname="helv", align=pymupdf.TEXT_ALIGN_LEFT)
        add_header_footer(pg, f"Page {page_num}")

    # ===== PAGES 73-77: Exhibit G - Shipping Log =====
    for sub_page in range(5):
        pg = new_page()
        page_num = 73 + sub_page
        if sub_page == 0:
            pg.insert_text(pymupdf.Point(200, 80), "EXHIBIT G", fontsize=16, fontname="hebo")
            pg.insert_text(pymupdf.Point(100, 110), "SHIPPING AND DELIVERY LOG",
                           fontsize=13, fontname="hebo")
            pg.insert_text(pymupdf.Point(72, 140), "Period: July 1 - September 30, 2023",
                           fontsize=10, fontname="helv")
            start_y = 170
        else:
            start_y = 80

        # Shipping log table
        hdrs = ["Date", "Lot #", "Carrier", "Tracking", "Units", "Status"]
        x_pos = [72, 145, 195, 275, 420, 470]
        pg.insert_text(pymupdf.Point(x_pos[0], start_y), hdrs[0], fontsize=8, fontname="hebo")
        for i in range(1, len(hdrs)):
            pg.insert_text(pymupdf.Point(x_pos[i], start_y), hdrs[i], fontsize=8, fontname="hebo")
        y = start_y + 16

        shipments_per_page = 20
        for row in range(shipments_per_page):
            lot_base = 40 + sub_page * shipments_per_page + row
            day = (row * 3 + sub_page * 7) % 28 + 1
            month = 7 + (lot_base - 40) // 30
            if month > 9:
                month = 9
            date_str = f"2023-{month:02d}-{day:02d}"
            carrier = ["FedEx Freight", "UPS Freight", "XPO Logistics", "Old Dominion"][row % 4]
            tracking = f"{'FX' if row % 4 == 0 else 'UP' if row % 4 == 1 else 'XP' if row % 4 == 2 else 'OD'}{770000000 + lot_base * 1000 + row}"
            units = [450, 200, 120, 300, 75, 180, 240][row % 7]
            status = "Delivered" if row % 5 != 3 else "Partial"
            vals = [date_str, f"#{lot_base}", carrier, tracking, str(units), status]
            for i, v in enumerate(vals):
                pg.insert_text(pymupdf.Point(x_pos[i], y), v, fontsize=7, fontname="cour" if i == 3 else "helv")
            y += 12
            if y > 720:
                break
        add_header_footer(pg, f"Page {page_num}")

    # ===== PAGES 78-82: Exhibit H - Expert Report =====
    for sub_page in range(5):
        pg = new_page()
        page_num = 78 + sub_page
        if sub_page == 0:
            pg.insert_text(pymupdf.Point(200, 80), "EXHIBIT H", fontsize=16, fontname="hebo")
            pg.insert_text(pymupdf.Point(100, 120), "EXPERT REPORT OF DR. SAMUEL OKAFOR, Ph.D.",
                           fontsize=12, fontname="hebo")
            expert_intro = """I, Dr. Samuel Okafor, Ph.D., P.E., have been retained by counsel for Jones Manufacturing, Inc. to provide an expert opinion regarding the manufacturing defects in precision titanium alloy components supplied by Meridian Supply Chain Corporation.

QUALIFICATIONS

I hold a Ph.D. in Materials Science and Engineering from MIT (2004) and am a licensed Professional Engineer in the State of New York. I have over 20 years of experience in metallurgy, quality engineering, and failure analysis. I have published 47 peer-reviewed articles and served as an expert witness in 12 prior cases involving manufacturing defects.

SCOPE OF ENGAGEMENT

I was asked to:
1. Analyze the root cause of dimensional non-conformances in Lots #47-49
2. Assess whether Meridian's manufacturing processes met industry standards
3. Evaluate the adequacy of Meridian's corrective actions
4. Quantify the impact of the defects on Jones Manufacturing's operations

METHODOLOGY

I reviewed the following materials:
- Purchase Agreement and Amendment No. 1
- Quality Inspection Report QIR-2023-0472
- Meridian's Corrective Action Plan
- Manufacturing process documentation from Meridian (produced in discovery)
- Technical specifications for Ti-6Al-4V per ASTM B348 and AMS 4928
- Relevant industry standards (AS9100D, ISO 9001:2015)"""
            pg.insert_textbox(pymupdf.Rect(72, 155, 540, 720), expert_intro,
                              fontsize=9, fontname="helv", align=pymupdf.TEXT_ALIGN_LEFT)
        else:
            sections = {
                1: "FINDINGS\n\n1. Root Cause Analysis\n\nBased on my analysis of the manufacturing process documentation and inspection data, the primary root cause of the dimensional non-conformances was excessive tooling wear on Meridian's Haas VF-5 CNC milling center (Machine #7). The tool change interval of 500 operating hours was approximately 43% longer than the manufacturer's recommendation of 350 hours for titanium alloy machining.\n\nAdditionally, lot-to-lot variation in the Ti-6Al-4V raw material from Apex Metals Corp. contributed to inconsistent machining behavior. Incoming material inspection records show that several lots had elevated oxygen content (0.18-0.20%) near the upper specification limit, which increases material hardness and accelerates tool wear.\n\n2. Industry Standards Compliance\n\nMeridian's failure to maintain tooling within manufacturer-recommended intervals represents a departure from industry best practices as codified in AS9100D Section 8.5.1 (Control of Production). A reasonably competent manufacturer would have recognized the need for more frequent tool changes when machining aerospace-grade titanium alloys.",
                2: "3. Corrective Action Assessment\n\nMeridian's corrective actions, while ultimately moving in the right direction, were implemented too slowly. The reduction in tool change interval from 500 to 350 hours should have been the standard practice from the outset of the contract. The implementation of SPC monitoring was not completed until September 30, 2023, nearly two months after the defects were first reported.\n\nFurthermore, Meridian's decision not to halt production pending completion of the root cause analysis exposed Jones Manufacturing to continued risk of receiving non-conforming parts.\n\n4. Impact Quantification\n\nBased on my analysis, the defective components caused:\n- 47 days of production downtime at Jones Manufacturing\n- 106 units of scrap (parts that were installed before defects were detected)\n- Rework of 23 sub-assemblies that had incorporated out-of-spec components\n- Delayed delivery of 8 completed units to Aerotech Defense Systems",
                3: "OPINIONS\n\nBased on the foregoing analysis, it is my opinion, to a reasonable degree of engineering certainty, that:\n\n1. Meridian Supply Chain Corporation failed to exercise reasonable care in maintaining its manufacturing equipment and processes, specifically by operating CNC tooling beyond recommended intervals for titanium alloy machining.\n\n2. Meridian's quality management system failed to detect and prevent the systematic dimensional non-conformances that affected Lots #47-49, in violation of the quality requirements specified in Section 5 of the Purchase Agreement.\n\n3. The defects were foreseeable and preventable through adherence to manufacturer-recommended maintenance schedules and implementation of standard statistical process control techniques.\n\n4. The corrective actions taken by Meridian were insufficient in timeliness and scope, and the continued non-conformance in the October shipment (5.1% rejection rate) demonstrates that the underlying process issues were not fully resolved.\n\n5. The damages claimed by Jones Manufacturing, totaling $3.87 million, are reasonable and supported by the production records and financial data I reviewed.\n\nRespectfully submitted,\n\nDr. Samuel Okafor, Ph.D., P.E.\nDecember 10, 2023",
                4: "APPENDIX: CURRICULUM VITAE\n\nDr. Samuel Okafor, Ph.D., P.E.\n\nEDUCATION\nPh.D., Materials Science and Engineering, MIT, 2004\nM.S., Mechanical Engineering, University of Michigan, 2000\nB.S., Metallurgical Engineering, University of Lagos, 1997\n\nPROFESSIONAL EXPERIENCE\n2015-Present  Principal Consultant, Okafor Engineering Associates\n2008-2015     Director of Materials Engineering, Pratt & Whitney\n2004-2008     Senior Engineer, General Electric Aviation\n\nSELECTED PUBLICATIONS\n1. 'Fatigue Life Prediction in Ti-6Al-4V Aerospace Components' (2022)\n2. 'Statistical Process Control in Precision Machining' (2020)\n3. 'Root Cause Analysis Framework for CNC Manufacturing Defects' (2019)\n4. 'Effect of Oxygen Content on Machinability of Titanium Alloys' (2017)\n\nEXPERT WITNESS EXPERIENCE\n12 prior engagements in federal and state courts\nTopics: manufacturing defects, product liability, quality engineering",
            }
            pg.insert_textbox(pymupdf.Rect(72, 80, 540, 720),
                              sections.get(sub_page, ""),
                              fontsize=9, fontname="helv", align=pymupdf.TEXT_ALIGN_LEFT)
        add_header_footer(pg, f"Page {page_num}")

    # ===== PAGES 83-85: Exhibit I - Privilege Log =====
    for sub_page in range(3):
        pg = new_page()
        page_num = 83 + sub_page
        if sub_page == 0:
            pg.insert_text(pymupdf.Point(200, 80), "EXHIBIT I", fontsize=16, fontname="hebo")
            pg.insert_text(pymupdf.Point(130, 110), "DEFENDANT'S PRIVILEGE LOG",
                           fontsize=13, fontname="hebo")
            pg.insert_text(pymupdf.Point(72, 145),
                           "Produced pursuant to Federal Rule of Civil Procedure 26(b)(5)(A)",
                           fontsize=9, fontname="heit")
            start_y = 175
        else:
            start_y = 80

        # Privilege log entries
        hdrs = ["Doc ID", "Date", "From/To", "Subject", "Privilege"]
        x_pos = [54, 110, 175, 310, 490]
        for i, h in enumerate(hdrs):
            pg.insert_text(pymupdf.Point(x_pos[i], start_y), h, fontsize=7, fontname="hebo")
        y = start_y + 14

        priv_entries = [
            ("PRIV-001", "08/05/23", "Torres to R. Kim, Esq.", "Legal advice re: Jones claims", "Attorney-Client"),
            ("PRIV-002", "08/10/23", "R. Kim, Esq. to Torres", "Litigation risk assessment", "Attorney-Client"),
            ("PRIV-003", "08/12/23", "R. Kim, Esq. memo", "Work product: damage analysis", "Work Product"),
            ("PRIV-004", "09/01/23", "Vasquez to R. Kim, Esq.", "Settlement strategy discussion", "Attorney-Client"),
            ("PRIV-005", "09/15/23", "R. Kim, Esq. to Vasquez", "Privileged legal memorandum", "Attorney-Client"),
            ("PRIV-006", "09/20/23", "R. Kim, Esq. memo", "Work product: deposition prep", "Work Product"),
            ("PRIV-007", "10/05/23", "Cheng to R. Kim, Esq.", "Contract interpretation query", "Attorney-Client"),
            ("PRIV-008", "10/10/23", "R. Kim, Esq. to Cheng", "Analysis of Section 14.2", "Attorney-Client"),
            ("PRIV-009", "10/25/23", "R. Kim, Esq. memo", "Work product: expert retention", "Work Product"),
            ("PRIV-010", "11/01/23", "Vasquez to R. Kim, Esq.", "Insurance coverage inquiry", "Attorney-Client"),
            ("PRIV-011", "11/08/23", "R. Kim, Esq. to Vasquez", "Coverage opinion letter", "Attorney-Client"),
            ("PRIV-012", "11/15/23", "R. Kim, Esq. memo", "Work product: mediation prep", "Work Product"),
            ("PRIV-013", "11/22/23", "Torres to R. Kim, Esq.", "Response to demand letter", "Attorney-Client"),
            ("PRIV-014", "12/01/23", "R. Kim, Esq. to all", "Litigation hold notice", "Attorney-Client"),
            ("PRIV-015", "12/10/23", "R. Kim, Esq. memo", "Work product: trial strategy", "Work Product"),
        ]
        entries_per_page = 15 if sub_page == 0 else 20
        start_idx = 0 if sub_page == 0 else 15
        for idx in range(start_idx, min(start_idx + entries_per_page, len(priv_entries) + 10)):
            if idx < len(priv_entries):
                entry = priv_entries[idx]
            else:
                # Generate additional entries
                e_num = idx + 1
                entry = (f"PRIV-{e_num:03d}", f"12/{5 + (idx - 15):02d}/23",
                         "R. Kim, Esq. to Torres", f"Privileged communication #{e_num}",
                         "Attorney-Client" if idx % 3 != 0 else "Work Product")
            for i, v in enumerate(entry):
                pg.insert_text(pymupdf.Point(x_pos[i], y), v, fontsize=7, fontname="cour" if i == 0 else "helv")
            y += 12
            if y > 720:
                break
        add_header_footer(pg, f"Page {page_num}")

    # Verify page count
    assert doc.page_count == 85, f"Expected 85 pages, got {doc.page_count}"

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT} ({85} pages)')

    # GUI-ready: open the PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
