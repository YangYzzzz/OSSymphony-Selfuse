"""
Initial Setup: Create four separate exhibit PDFs for court filing merge task
Task ID: pdf_legal_004
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf


WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_004'
EXHIBITS_DIR = f'{WORKDIR}/legal/exhibits'


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


def create_exhibit_page(doc, page_num, exhibit_label, title, body_lines):
    """Add a single page with header, footer, and body text to a document."""
    page = doc.new_page(width=612, height=792)  # US Letter

    # Header line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 80), pymupdf.Point(540, 80))
    shape.finish(color=(0, 0, 0), width=1.5)
    shape.commit()

    # Exhibit label top-right
    page.insert_text(
        pymupdf.Point(420, 40),
        exhibit_label,
        fontsize=10,
        fontname="hebo",
        color=(0.2, 0.2, 0.2),
    )

    # Title
    page.insert_text(
        pymupdf.Point(72, 60),
        title,
        fontsize=14,
        fontname="hebo",
        color=(0, 0, 0),
    )

    # Body text
    y = 110
    for line in body_lines:
        if y > 740:
            break
        page.insert_text(
            pymupdf.Point(72, y),
            line,
            fontsize=10,
            fontname="tiro",
            color=(0, 0, 0),
        )
        y += 16

    # Footer
    page.insert_text(
        pymupdf.Point(280, 770),
        f"Page {page_num}",
        fontsize=8,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    return page


def create_exhibit_a():
    """Exhibit A: Purchase Agreement - 5 pages"""
    doc = pymupdf.open()

    pages_content = [
        {
            "title": "ASSET PURCHASE AGREEMENT",
            "lines": [
                "This Asset Purchase Agreement ('Agreement') is entered into as of March 15, 2025,",
                "by and between Meridian Technologies, Inc., a Delaware corporation ('Seller'),",
                "and Apex Ventures Holdings LLC, a California limited liability company ('Buyer').",
                "",
                "RECITALS",
                "",
                "WHEREAS, the Seller is engaged in the business of developing and licensing",
                "enterprise software solutions for supply chain management (the 'Business');",
                "",
                "WHEREAS, the Buyer desires to purchase from the Seller, and the Seller desires",
                "to sell to the Buyer, substantially all of the assets used in or relating to",
                "the Business, upon the terms and subject to the conditions set forth herein;",
                "",
                "NOW, THEREFORE, in consideration of the mutual covenants and agreements herein",
                "contained, and for other good and valuable consideration, the receipt and",
                "sufficiency of which are hereby acknowledged, the parties agree as follows:",
                "",
                "ARTICLE I - DEFINITIONS",
                "",
                "1.1 'Acquired Assets' shall mean all right, title and interest in the following:",
                "    (a) All intellectual property related to the SupplyTrack Platform;",
                "    (b) All customer contracts listed in Schedule 1.1(b);",
                "    (c) All equipment, furniture, and fixtures at 1200 Innovation Drive;",
                "    (d) All accounts receivable as of the Closing Date;",
                "    (e) All prepaid expenses and deposits related to the Business.",
                "",
                "1.2 'Closing Date' means April 30, 2025, or such other date as may be",
                "    mutually agreed upon by the parties in writing.",
                "",
                "1.3 'Purchase Price' means the aggregate sum of Forty-Seven Million Five",
                "    Hundred Thousand Dollars ($47,500,000.00), subject to adjustments as",
                "    provided in Article III of this Agreement.",
            ],
        },
        {
            "title": "ARTICLE II - PURCHASE AND SALE",
            "lines": [
                "2.1 Agreement to Sell and Purchase. Subject to the terms and conditions of",
                "this Agreement, at the Closing, the Seller shall sell, assign, transfer,",
                "convey and deliver to the Buyer, and the Buyer shall purchase, acquire and",
                "accept from the Seller, all of the Acquired Assets, free and clear of all",
                "Encumbrances other than Permitted Encumbrances.",
                "",
                "2.2 Excluded Assets. Notwithstanding anything herein to the contrary, the",
                "following assets shall be excluded from the Acquired Assets:",
                "    (a) Cash and cash equivalents of the Seller;",
                "    (b) The corporate charter, qualifications to do business, taxpayer",
                "        and other identification numbers, seal, minute books, stock",
                "        transfer books and similar corporate records of the Seller;",
                "    (c) Personnel records of the Seller to the extent transfer is",
                "        restricted by applicable law;",
                "    (d) All rights of the Seller under this Agreement.",
                "",
                "2.3 Assumed Liabilities. At the Closing, the Buyer shall assume and agree",
                "to pay, perform and discharge when due the following liabilities:",
                "    (a) All obligations under the Assigned Contracts arising after Closing;",
                "    (b) All accounts payable of the Business as of the Closing Date;",
                "    (c) All liabilities arising from the operation of the Business after",
                "        the Closing Date.",
                "",
                "2.4 Excluded Liabilities. The Buyer shall not assume, and the Seller shall",
                "remain solely responsible for, the following liabilities:",
                "    (a) Any liability for taxes of the Seller for any period;",
                "    (b) Any product liability claims arising prior to the Closing Date;",
                "    (c) Any obligations under contracts not included in Assigned Contracts;",
                "    (d) Any environmental liabilities relating to the Seller's properties.",
            ],
        },
        {
            "title": "ARTICLE III - PURCHASE PRICE AND PAYMENT",
            "lines": [
                "3.1 Purchase Price. The aggregate purchase price for the Acquired Assets",
                "shall be Forty-Seven Million Five Hundred Thousand Dollars ($47,500,000.00)",
                "(the 'Purchase Price'), allocated as follows:",
                "",
                "    Intellectual Property:          $28,000,000.00",
                "    Customer Contracts:             $12,500,000.00",
                "    Equipment and Fixtures:          $3,200,000.00",
                "    Accounts Receivable:             $2,800,000.00",
                "    Goodwill:                        $1,000,000.00",
                "    Total:                          $47,500,000.00",
                "",
                "3.2 Payment Terms. The Purchase Price shall be payable as follows:",
                "    (a) At Closing: $35,000,000.00 in immediately available funds;",
                "    (b) Escrow Deposit: $7,500,000.00 to be held in escrow pursuant to",
                "        the Escrow Agreement attached as Exhibit E;",
                "    (c) Deferred Payment: $5,000,000.00 payable in equal quarterly",
                "        installments over twenty-four (24) months following Closing.",
                "",
                "3.3 Working Capital Adjustment. Within ninety (90) days after the Closing",
                "Date, the Buyer shall prepare and deliver to the Seller a statement of",
                "the actual Net Working Capital as of the Closing Date. If the actual Net",
                "Working Capital exceeds the Target Working Capital of $4,200,000.00 by",
                "more than $100,000.00, the Buyer shall pay the excess to the Seller.",
                "",
                "3.4 Allocation of Purchase Price. The parties agree to allocate the Purchase",
                "Price among the Acquired Assets in accordance with Section 1060 of the",
                "Internal Revenue Code and the regulations thereunder.",
            ],
        },
        {
            "title": "ARTICLE IV - REPRESENTATIONS AND WARRANTIES OF SELLER",
            "lines": [
                "The Seller hereby represents and warrants to the Buyer as follows:",
                "",
                "4.1 Organization. The Seller is a corporation duly organized, validly",
                "existing and in good standing under the laws of the State of Delaware.",
                "",
                "4.2 Authorization. The execution, delivery and performance of this Agreement",
                "have been duly authorized by all requisite corporate action on the part",
                "of the Seller, including approval by the Board of Directors.",
                "",
                "4.3 No Conflicts. The execution and performance of this Agreement will not",
                "conflict with or result in a breach of any agreement, instrument or",
                "obligation to which the Seller is a party or by which it is bound.",
                "",
                "4.4 Title to Assets. The Seller has good and marketable title to all of",
                "the Acquired Assets, free and clear of all Encumbrances.",
                "",
                "4.5 Intellectual Property. Schedule 4.5 sets forth a complete list of all",
                "Intellectual Property owned or licensed by the Seller in connection with",
                "the Business. The Seller has not received any written notice alleging that",
                "the Business infringes upon the intellectual property rights of any person.",
                "",
                "4.6 Contracts. Schedule 4.6 lists all material contracts related to the",
                "Business. Each such contract is valid, binding and in full force and effect.",
                "The Seller is not in material breach of any such contract.",
                "",
                "4.7 Financial Statements. The Seller has delivered to the Buyer audited",
                "financial statements for the fiscal years ended December 31, 2023 and",
                "December 31, 2024, which present fairly the financial condition of the",
                "Business in accordance with generally accepted accounting principles.",
                "",
                "4.8 Compliance with Laws. The Seller has conducted the Business in compliance",
                "with all applicable laws, regulations and ordinances.",
            ],
        },
        {
            "title": "ARTICLE V - CLOSING CONDITIONS AND SIGNATURES",
            "lines": [
                "5.1 Conditions to Buyer's Obligations. The Buyer's obligation to consummate",
                "the transactions contemplated hereby is subject to the satisfaction of:",
                "    (a) Accuracy of Seller's representations and warranties;",
                "    (b) Performance by the Seller of all covenants required at or before Closing;",
                "    (c) Delivery of all required certificates, documents and instruments;",
                "    (d) Receipt of all required third-party consents;",
                "    (e) No Material Adverse Effect shall have occurred since the date hereof.",
                "",
                "5.2 Conditions to Seller's Obligations. The Seller's obligation to consummate",
                "the transactions contemplated hereby is subject to the satisfaction of:",
                "    (a) Accuracy of Buyer's representations and warranties;",
                "    (b) Payment of the Purchase Price in accordance with Section 3.2;",
                "    (c) Delivery of all required certificates and instruments.",
                "",
                "",
                "IN WITNESS WHEREOF, the parties have executed this Agreement as of the date",
                "first written above.",
                "",
                "",
                "MERIDIAN TECHNOLOGIES, INC.",
                "",
                "By: _______________________________",
                "Name: Victoria R. Ashford",
                "Title: Chief Executive Officer",
                "Date: March 15, 2025",
                "",
                "",
                "APEX VENTURES HOLDINGS LLC",
                "",
                "By: _______________________________",
                "Name: David K. Thornton",
                "Title: Managing Partner",
                "Date: March 15, 2025",
            ],
        },
    ]

    for i, content in enumerate(pages_content):
        create_exhibit_page(doc, i + 1, "EXHIBIT A", content["title"], content["lines"])

    doc.save(f'{EXHIBITS_DIR}/exhibit_A.pdf')
    doc.close()
    print(f'Created exhibit_A.pdf (5 pages)')


def create_exhibit_b():
    """Exhibit B: Financial Summary - 3 pages"""
    doc = pymupdf.open()

    pages_content = [
        {
            "title": "FINANCIAL SUMMARY - MERIDIAN TECHNOLOGIES",
            "lines": [
                "Prepared by: Harrington & Associates, CPA",
                "Report Date: February 28, 2025",
                "Fiscal Year Ending: December 31, 2024",
                "",
                "CONSOLIDATED INCOME STATEMENT",
                "",
                "Revenue:",
                "  Software Licensing Revenue          $32,450,000",
                "  Professional Services Revenue         $8,720,000",
                "  Maintenance & Support Revenue         $6,340,000",
                "  Training Revenue                      $1,890,000",
                "                                    ---------------",
                "  Total Revenue                        $49,400,000",
                "",
                "Cost of Revenue:",
                "  Cost of Software Development          $8,200,000",
                "  Cost of Professional Services         $4,100,000",
                "  Infrastructure & Hosting Costs        $3,650,000",
                "                                    ---------------",
                "  Total Cost of Revenue                $15,950,000",
                "",
                "Gross Profit                           $33,450,000",
                "Gross Margin                               67.7%",
                "",
                "Operating Expenses:",
                "  Research & Development                $9,800,000",
                "  Sales & Marketing                     $7,200,000",
                "  General & Administrative              $4,500,000",
                "  Depreciation & Amortization           $2,100,000",
                "                                    ---------------",
                "  Total Operating Expenses             $23,600,000",
                "",
                "Operating Income (EBITDA)               $9,850,000",
            ],
        },
        {
            "title": "BALANCE SHEET SUMMARY",
            "lines": [
                "As of December 31, 2024",
                "",
                "ASSETS",
                "",
                "Current Assets:",
                "  Cash and Cash Equivalents             $5,230,000",
                "  Accounts Receivable (net)             $4,870,000",
                "  Prepaid Expenses                        $820,000",
                "  Other Current Assets                    $340,000",
                "                                    ---------------",
                "  Total Current Assets                 $11,260,000",
                "",
                "Non-Current Assets:",
                "  Property and Equipment (net)          $3,200,000",
                "  Intangible Assets (net)              $18,400,000",
                "  Goodwill                              $5,600,000",
                "  Other Non-Current Assets                $940,000",
                "                                    ---------------",
                "  Total Non-Current Assets             $28,140,000",
                "",
                "TOTAL ASSETS                           $39,400,000",
                "",
                "LIABILITIES AND STOCKHOLDERS' EQUITY",
                "",
                "Current Liabilities:",
                "  Accounts Payable                      $2,100,000",
                "  Accrued Expenses                      $1,850,000",
                "  Deferred Revenue                      $3,400,000",
                "  Current Portion of Long-Term Debt     $1,200,000",
                "                                    ---------------",
                "  Total Current Liabilities             $8,550,000",
                "",
                "Non-Current Liabilities:",
                "  Long-Term Debt                        $4,800,000",
                "  Deferred Tax Liabilities              $1,250,000",
                "                                    ---------------",
                "  Total Non-Current Liabilities         $6,050,000",
            ],
        },
        {
            "title": "KEY FINANCIAL METRICS AND NOTES",
            "lines": [
                "KEY PERFORMANCE METRICS (FY2024)",
                "",
                "  Annual Recurring Revenue (ARR):      $39,590,000",
                "  Net Revenue Retention Rate:               118%",
                "  Customer Acquisition Cost (CAC):         $42,000",
                "  Lifetime Value (LTV):                   $380,000",
                "  LTV/CAC Ratio:                             9.0x",
                "  Monthly Churn Rate:                        0.8%",
                "  Number of Enterprise Clients:                347",
                "  Average Contract Value:                 $114,000",
                "",
                "YEAR-OVER-YEAR COMPARISON",
                "",
                "                         FY2024       FY2023     Change",
                "  Total Revenue       $49,400,000  $41,200,000   +19.9%",
                "  Gross Profit        $33,450,000  $27,100,000   +23.4%",
                "  Operating Income     $9,850,000   $7,600,000   +29.6%",
                "  Total Assets        $39,400,000  $33,200,000   +18.7%",
                "  Headcount                   248          212   +17.0%",
                "",
                "NOTES TO FINANCIAL STATEMENTS",
                "",
                "Note 1: Revenue Recognition",
                "Software licensing revenue is recognized ratably over the contract period.",
                "Professional services revenue is recognized as services are performed.",
                "",
                "Note 2: Material Contracts",
                "The company's top 5 clients represent approximately 34% of total revenue.",
                "No single client exceeds 10% of revenue.",
                "",
                "Note 3: Pending Matters",
                "There are no material legal proceedings pending against the company.",
                "",
                "Certified by: Margaret L. Harrington, CPA",
                "Harrington & Associates",
                "License No. CPA-2847193",
            ],
        },
    ]

    for i, content in enumerate(pages_content):
        create_exhibit_page(doc, i + 1, "EXHIBIT B", content["title"], content["lines"])

    doc.save(f'{EXHIBITS_DIR}/exhibit_B.pdf')
    doc.close()
    print(f'Created exhibit_B.pdf (3 pages)')


def create_exhibit_c():
    """Exhibit C: Email Correspondence - 8 pages"""
    doc = pymupdf.open()

    pages_content = [
        {
            "title": "EMAIL CORRESPONDENCE LOG",
            "lines": [
                "Case No.: 2025-CV-04821",
                "Re: Meridian Technologies, Inc. v. Apex Ventures Holdings LLC",
                "Period: January 8, 2025 through March 12, 2025",
                "",
                "This exhibit contains authenticated copies of email correspondence",
                "between the parties relevant to the disputed transaction.",
                "",
                "---",
                "",
                "Email #1",
                "From: david.thornton@apexventures.com",
                "To: v.ashford@meridiantech.com",
                "Date: January 8, 2025, 9:14 AM PST",
                "Subject: Follow-up from Board Presentation",
                "",
                "Victoria,",
                "",
                "Thank you for the thorough presentation to our investment committee",
                "last Thursday. The team was impressed with the SupplyTrack platform",
                "demo and the growth trajectory. We are prepared to move forward with",
                "a formal offer, subject to satisfactory due diligence.",
                "",
                "Can we schedule a call this week to discuss timeline and key terms?",
                "",
                "Best regards,",
                "David K. Thornton",
                "Managing Partner, Apex Ventures Holdings LLC",
            ],
        },
        {
            "title": "EMAIL CORRESPONDENCE (CONTINUED)",
            "lines": [
                "Email #2",
                "From: v.ashford@meridiantech.com",
                "To: david.thornton@apexventures.com",
                "Cc: legal@meridiantech.com",
                "Date: January 10, 2025, 2:47 PM PST",
                "Subject: RE: Follow-up from Board Presentation",
                "",
                "David,",
                "",
                "Thank you for the prompt follow-up. Our board is aligned on exploring",
                "this opportunity further. I've copied our general counsel, Sandra",
                "Whitfield, to begin coordinating the due diligence process.",
                "",
                "We are available for a call on January 14 at 10:00 AM or January 15",
                "at 2:00 PM. Please let us know your preference.",
                "",
                "Looking forward to productive discussions.",
                "",
                "Victoria R. Ashford",
                "CEO, Meridian Technologies, Inc.",
                "",
                "---",
                "",
                "Email #3",
                "From: david.thornton@apexventures.com",
                "To: v.ashford@meridiantech.com; legal@meridiantech.com",
                "Cc: j.ramirez@apexventures.com",
                "Date: January 13, 2025, 8:32 AM PST",
                "Subject: RE: Follow-up from Board Presentation",
                "",
                "Victoria, Sandra,",
                "",
                "January 14 at 10:00 AM works well. I've included our deal counsel,",
                "Javier Ramirez, on this thread. He will coordinate with Sandra on",
                "the diligence data room setup.",
            ],
        },
        {
            "title": "EMAIL CORRESPONDENCE (CONTINUED)",
            "lines": [
                "Email #4",
                "From: j.ramirez@apexventures.com",
                "To: legal@meridiantech.com",
                "Cc: david.thornton@apexventures.com; v.ashford@meridiantech.com",
                "Date: January 22, 2025, 11:05 AM PST",
                "Subject: Due Diligence Request List",
                "",
                "Sandra,",
                "",
                "Following our kickoff call, attached is the comprehensive due diligence",
                "request list covering the following categories:",
                "",
                "  1. Corporate governance documents (charter, bylaws, minutes)",
                "  2. Financial statements (audited FY2022, FY2023, FY2024 interim)",
                "  3. Material contracts (customer, vendor, employment)",
                "  4. Intellectual property portfolio (patents, trademarks, copyrights)",
                "  5. Litigation and regulatory matters",
                "  6. Tax returns and assessments (last 3 years)",
                "  7. Employee benefit plans and HR records",
                "  8. Insurance policies",
                "  9. Environmental and compliance certifications",
                "",
                "Please upload to the Meridian Data Room (link below) by February 5, 2025.",
                "https://dataroom.meridiantech.com/deal-2025-apex",
                "",
                "Let me know if you have questions.",
                "",
                "Javier Ramirez, Esq.",
                "Apex Ventures Holdings LLC",
            ],
        },
        {
            "title": "EMAIL CORRESPONDENCE (CONTINUED)",
            "lines": [
                "Email #5",
                "From: legal@meridiantech.com",
                "To: j.ramirez@apexventures.com",
                "Cc: v.ashford@meridiantech.com",
                "Date: February 3, 2025, 4:18 PM PST",
                "Subject: RE: Due Diligence Request List",
                "",
                "Javier,",
                "",
                "We have uploaded the majority of the requested documents to the data room.",
                "Items 1-6 and 8-9 are complete. Item 7 (employee records) will require",
                "additional time due to privacy review requirements under applicable",
                "employment laws. We anticipate completing this upload by February 12.",
                "",
                "Please note the following regarding intellectual property (Item 4):",
                "  - 12 registered patents (see Patent Schedule in Folder 4A)",
                "  - 3 pending patent applications (Folder 4B)",
                "  - 47 registered software copyrights (Folder 4C)",
                "  - 8 registered trademarks (Folder 4D)",
                "  - Open source audit report from BlackDuck (Folder 4E)",
                "",
                "Sandra Whitfield",
                "General Counsel, Meridian Technologies, Inc.",
                "",
                "---",
                "",
                "Email #6",
                "From: david.thornton@apexventures.com",
                "To: v.ashford@meridiantech.com",
                "Date: February 14, 2025, 3:22 PM PST",
                "Subject: Initial Due Diligence Findings",
                "",
                "Victoria,",
                "",
                "Our team has substantially completed the initial review. Overall findings",
                "are positive. However, we have identified three areas requiring discussion:",
            ],
        },
        {
            "title": "EMAIL CORRESPONDENCE (CONTINUED)",
            "lines": [
                "  1. The OptiFlow integration contract with Zenith Logistics (valued at",
                "     $3.2M annually) contains a change-of-control clause that requires",
                "     written consent for assignment. We need to discuss the consent",
                "     process and timeline.",
                "",
                "  2. The Q3 2024 revenue recognition for the GlobalPort Systems deal",
                "     appears to have recognized $1.4M upon contract signing rather than",
                "     ratably. Our auditors would like to discuss the accounting treatment.",
                "",
                "  3. Two of the pending patent applications (US App No. 17/892,341 and",
                "     17/923,018) have received initial rejections from the USPTO. While",
                "     this is common, we need clarity on the prosecution strategy.",
                "",
                "Can we schedule a management meeting to address these items? We want",
                "to resolve them efficiently to maintain our target closing timeline.",
                "",
                "David",
                "",
                "---",
                "",
                "Email #7",
                "From: v.ashford@meridiantech.com",
                "To: david.thornton@apexventures.com",
                "Date: February 17, 2025, 10:45 AM PST",
                "Subject: RE: Initial Due Diligence Findings",
                "",
                "David,",
                "",
                "I appreciate the thorough review. Let me address each point briefly:",
                "",
                "  1. Zenith Logistics: We have a strong 7-year relationship with their CTO.",
                "     I am confident we can obtain consent within 2-3 weeks.",
            ],
        },
        {
            "title": "EMAIL CORRESPONDENCE (CONTINUED)",
            "lines": [
                "  2. Revenue recognition: Our controller, James Park, can walk your team",
                "     through the GlobalPort arrangement. The contract included a distinct",
                "     perpetual license component that warranted upfront recognition. We",
                "     have the relevant ASC 606 analysis documented.",
                "",
                "  3. Patent applications: Our IP counsel at Morrison Foerster is preparing",
                "     responses to both office actions. They advise that the rejections are",
                "     based on prior art that can be distinguished. Prosecution budget is",
                "     within normal parameters.",
                "",
                "I propose a management meeting on February 24 at our offices in San Jose.",
                "We can cover all three items and tour the development facility.",
                "",
                "Victoria",
                "",
                "---",
                "",
                "Email #8",
                "From: j.ramirez@apexventures.com",
                "To: legal@meridiantech.com",
                "Cc: david.thornton@apexventures.com; v.ashford@meridiantech.com",
                "Date: February 26, 2025, 5:55 PM PST",
                "Subject: Draft Purchase Agreement",
                "",
                "Sandra,",
                "",
                "Attached please find the initial draft of the Asset Purchase Agreement",
                "for your review. Key terms are as follows:",
                "  - Purchase Price: $47,500,000",
                "  - Structure: Asset purchase (not stock)",
                "  - Closing target: April 30, 2025",
                "  - Escrow: 15% of purchase price held for 18 months",
                "  - Representations & Warranties Insurance: $10M policy",
            ],
        },
        {
            "title": "EMAIL CORRESPONDENCE (CONTINUED)",
            "lines": [
                "Email #9",
                "From: legal@meridiantech.com",
                "To: j.ramirez@apexventures.com",
                "Cc: v.ashford@meridiantech.com; david.thornton@apexventures.com",
                "Date: March 4, 2025, 11:30 AM PST",
                "Subject: RE: Draft Purchase Agreement - Comments",
                "",
                "Javier,",
                "",
                "We have completed our initial review of the draft APA. Our principal",
                "comments are summarized in the attached markup. Key negotiation points:",
                "",
                "  1. Escrow Amount: We propose reducing to 10% ($4,750,000). The 15%",
                "     proposed is above market for a transaction of this size and nature.",
                "",
                "  2. Non-Compete Period: The proposed 5-year non-compete for Victoria",
                "     Ashford and the founding team is excessive. We counter with 2 years,",
                "     which is standard in California and more likely enforceable.",
                "",
                "  3. Working Capital Target: We believe the $4,200,000 target should be",
                "     adjusted to $4,500,000 based on the trailing 12-month average.",
                "",
                "  4. Indemnification Cap: We request a cap of 15% of the Purchase Price",
                "     rather than the proposed 25%.",
                "",
                "  5. Material Adverse Effect Definition: We request exclusion of general",
                "     economic conditions and industry-wide changes.",
                "",
                "We look forward to discussing these points.",
                "",
                "Sandra Whitfield",
                "General Counsel, Meridian Technologies, Inc.",
            ],
        },
        {
            "title": "EMAIL CORRESPONDENCE (CONTINUED)",
            "lines": [
                "Email #10",
                "From: david.thornton@apexventures.com",
                "To: v.ashford@meridiantech.com",
                "Cc: j.ramirez@apexventures.com; legal@meridiantech.com",
                "Date: March 12, 2025, 2:15 PM PST",
                "Subject: RE: Draft Purchase Agreement - Resolution Proposal",
                "",
                "Victoria,",
                "",
                "After internal discussion with our investment committee, we are",
                "prepared to make the following concessions to move toward signing:",
                "",
                "  1. Escrow: We accept 10% ($4,750,000) with a 12-month hold period.",
                "  2. Non-Compete: We accept 3 years as a compromise (from our 5 and",
                "     your proposed 2).",
                "  3. Working Capital: We accept the $4,500,000 target.",
                "  4. Indemnification Cap: We propose 20% as a middle ground.",
                "  5. MAE Definition: Agreed to exclude general economic conditions.",
                "",
                "If these terms are acceptable, I suggest we instruct counsel to prepare",
                "the final agreement for execution by March 15, 2025.",
                "",
                "Please confirm at your earliest convenience.",
                "",
                "Best regards,",
                "David K. Thornton",
                "Managing Partner",
                "Apex Ventures Holdings LLC",
                "",
                "",
                "    [END OF EMAIL CORRESPONDENCE LOG]",
                "",
                "Authenticated by: Court Reporting Services, Inc.",
                "Certificate No.: CRS-2025-04821-EC",
                "Date: March 20, 2025",
            ],
        },
    ]

    for i, content in enumerate(pages_content):
        create_exhibit_page(doc, i + 1, "EXHIBIT C", content["title"], content["lines"])

    doc.save(f'{EXHIBITS_DIR}/exhibit_C.pdf')
    doc.close()
    print(f'Created exhibit_C.pdf (8 pages)')


def create_exhibit_d():
    """Exhibit D: Declaration/Attestation - 2 pages"""
    doc = pymupdf.open()

    pages_content = [
        {
            "title": "DECLARATION OF VICTORIA R. ASHFORD",
            "lines": [
                "IN THE SUPERIOR COURT OF THE STATE OF CALIFORNIA",
                "COUNTY OF SANTA CLARA",
                "",
                "MERIDIAN TECHNOLOGIES, INC.,",
                "                Plaintiff,              Case No.: 2025-CV-04821",
                "        v.",
                "APEX VENTURES HOLDINGS LLC,",
                "                Defendant.",
                "",
                "DECLARATION OF VICTORIA R. ASHFORD IN SUPPORT OF",
                "PLAINTIFF'S MOTION FOR PRELIMINARY INJUNCTION",
                "",
                "I, Victoria R. Ashford, declare as follows:",
                "",
                "1. I am the Chief Executive Officer and co-founder of Meridian",
                "Technologies, Inc. ('Meridian'). I have personal knowledge of the",
                "facts stated herein and could competently testify thereto if called",
                "as a witness.",
                "",
                "2. I co-founded Meridian in 2016 with Dr. Robert Chen, who serves as",
                "Chief Technology Officer. Over the past nine years, we have built the",
                "SupplyTrack platform into a leading enterprise solution serving 347",
                "active clients across 28 countries.",
                "",
                "3. In late 2024, I was approached by David Thornton of Apex Ventures",
                "regarding a potential acquisition. After extensive negotiations, we",
                "executed an Asset Purchase Agreement on March 15, 2025, for a total",
                "consideration of $47,500,000.",
                "",
                "4. As of the date of this declaration, the Closing Date of April 30,",
                "2025 has passed, and Apex Ventures has failed to tender the closing",
                "payment of $35,000,000 as required by Section 3.2(a) of the Agreement.",
            ],
        },
        {
            "title": "DECLARATION (CONTINUED)",
            "lines": [
                "5. On April 28, 2025, two days before the scheduled closing, Mr. Thornton",
                "informed me by telephone that Apex Ventures would not proceed with the",
                "transaction. He stated that their investment committee had 'reconsidered'",
                "the transaction in light of 'market conditions.' This was the first",
                "indication that Apex intended to breach the Agreement.",
                "",
                "6. In reliance on the Agreement, Meridian has:",
                "   (a) Declined two competing acquisition offers, including an offer from",
                "       Pinnacle Software Group valued at approximately $43,000,000;",
                "   (b) Expended approximately $850,000 in legal, accounting and advisory",
                "       fees in connection with the transaction;",
                "   (c) Begun the employee notification and transition planning process,",
                "       resulting in the departure of six key employees who accepted",
                "       positions elsewhere;",
                "   (d) Delayed the planned Series C fundraising round pending completion",
                "       of the acquisition.",
                "",
                "7. The failure of Apex Ventures to close has caused immediate and",
                "irreparable harm to Meridian, including loss of key personnel, client",
                "uncertainty, and competitive disadvantage. If the Court does not grant",
                "injunctive relief, Meridian will suffer further irreparable injury.",
                "",
                "I declare under penalty of perjury under the laws of the State of",
                "California that the foregoing is true and correct.",
                "",
                "Executed on May 5, 2025, at San Jose, California.",
                "",
                "",
                "______________________________",
                "Victoria R. Ashford",
                "Chief Executive Officer",
                "Meridian Technologies, Inc.",
            ],
        },
    ]

    for i, content in enumerate(pages_content):
        create_exhibit_page(doc, i + 1, "EXHIBIT D", content["title"], content["lines"])

    doc.save(f'{EXHIBITS_DIR}/exhibit_D.pdf')
    doc.close()
    print(f'Created exhibit_D.pdf (2 pages)')


def create_initial():
    # Create directory structure
    os.makedirs(EXHIBITS_DIR, exist_ok=True)

    # Create all four exhibits
    create_exhibit_a()
    create_exhibit_b()
    create_exhibit_c()
    create_exhibit_d()

    # Verify page counts
    for name, expected in [('exhibit_A.pdf', 5), ('exhibit_B.pdf', 3),
                           ('exhibit_C.pdf', 8), ('exhibit_D.pdf', 2)]:
        doc = pymupdf.open(f'{EXHIBITS_DIR}/{name}')
        actual = doc.page_count
        doc.close()
        assert actual == expected, f'{name}: expected {expected} pages, got {actual}'

    print(f'All exhibit files created in {EXHIBITS_DIR}')

    # Open file manager to show the exhibits directory
    launch_gui(f'nautilus "{EXHIBITS_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with DISPLAY=:0')


create_initial()
