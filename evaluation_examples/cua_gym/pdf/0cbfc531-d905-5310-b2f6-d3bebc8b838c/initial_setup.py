"""
Initial Setup: Create two exhibit PDF sets for Bates numbering task
Task ID: pdf_legal_078
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_078'
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


def create_exhibit_page(doc, page_num, exhibit_set, title, body_text):
    """Create a single exhibit page with realistic legal content."""
    page = doc.new_page(width=612, height=792)  # Letter size

    # Header line
    page.insert_text(
        pymupdf.Point(72, 50),
        f"EXHIBIT SET {exhibit_set}",
        fontsize=10,
        fontname="hebo",
        color=(0.3, 0.3, 0.3),
    )

    # Horizontal rule
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 58), pymupdf.Point(540, 58))
    shape.finish(color=(0.5, 0.5, 0.5), width=0.5)
    shape.commit()

    # Title
    page.insert_text(
        pymupdf.Point(72, 90),
        title,
        fontsize=14,
        fontname="hebo",
        color=(0, 0, 0),
    )

    # Body text in a textbox
    rect = pymupdf.Rect(72, 110, 540, 720)
    page.insert_textbox(
        rect,
        body_text,
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # Footer
    page.insert_text(
        pymupdf.Point(72, 755),
        f"Page {page_num}",
        fontsize=9,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    return page


def create_set_a():
    """Create Exhibit Set A - 20 pages of patent litigation documents."""
    doc = pymupdf.open()

    exhibits_a = [
        ("Exhibit A-1: Patent Assignment Agreement",
         "PATENT ASSIGNMENT AGREEMENT\n\nThis Patent Assignment Agreement (the 'Agreement') is entered into as of "
         "March 15, 2024, by and between Nextera Innovations, Inc., a Delaware corporation ('Assignor'), "
         "and Plex Technologies Corporation, a California corporation ('Assignee').\n\n"
         "WHEREAS, Assignor is the owner of certain patents and patent applications relating to advanced "
         "semiconductor fabrication processes;\n\n"
         "WHEREAS, Assignee desires to acquire all right, title, and interest in and to said patents;\n\n"
         "NOW, THEREFORE, in consideration of the mutual covenants contained herein, and for good and "
         "valuable consideration, the receipt and sufficiency of which are hereby acknowledged, the parties "
         "agree as follows:\n\n"
         "1. ASSIGNMENT. Assignor hereby irrevocably assigns, transfers, and conveys to Assignee all of "
         "Assignor's right, title, and interest in and to the patents listed in Schedule A attached hereto "
         "(the 'Assigned Patents'), including all divisions, continuations, continuations-in-part, reissues, "
         "reexaminations, and extensions thereof.\n\n"
         "2. CONSIDERATION. In consideration for the assignment, Assignee shall pay to Assignor the sum of "
         "Forty-Seven Million Five Hundred Thousand Dollars ($47,500,000.00), payable as follows:\n"
         "   (a) Twenty Million Dollars ($20,000,000.00) upon execution of this Agreement;\n"
         "   (b) The remaining balance in four equal quarterly installments."),

        ("Exhibit A-2: Prior Art Search Report",
         "PRIOR ART SEARCH REPORT\n\nPrepared by: Morrison & Keller IP Associates\n"
         "Date: January 22, 2024\nClient Reference: PLX-2024-0087\n\n"
         "1. SCOPE OF SEARCH\n\n"
         "This report summarizes the results of a comprehensive prior art search conducted in connection "
         "with U.S. Patent No. 11,234,567 ('the '567 Patent') entitled 'Method and System for Multi-Layer "
         "Semiconductor Deposition Using Plasma-Enhanced Chemical Vapor Deposition.'\n\n"
         "The search covered the following databases:\n"
         "- USPTO patent database (1976-present)\n"
         "- European Patent Office (EPO) database\n"
         "- World Intellectual Property Organization (WIPO) database\n"
         "- IEEE Xplore Digital Library\n"
         "- Journal of Applied Physics archives\n\n"
         "2. SEARCH RESULTS\n\n"
         "A total of 47 prior art references were identified. Of these, 12 references are considered "
         "highly relevant to the claims of the '567 Patent. The most pertinent references are:\n\n"
         "Reference 1: U.S. Patent No. 9,876,543 (filed 2018, issued 2020)\n"
         "Inventor: Dr. Haruki Tanaka\n"
         "Title: 'Plasma Deposition Apparatus with Rotating Substrate Holder'\n"
         "Relevance: Discloses substrate rotation mechanism similar to Claim 3 of the '567 Patent."),

        ("Exhibit A-3: Licensing Revenue Summary",
         "LICENSING REVENUE SUMMARY\nFiscal Years 2020-2024\n\n"
         "Prepared by: Financial Analysis Division\nPlex Technologies Corporation\n\n"
         "The following table summarizes licensing revenue generated by the Assigned Patents "
         "during the relevant period:\n\n"
         "Fiscal Year 2020:\n"
         "  Total Licensing Revenue: $8,234,500\n"
         "  Number of Active Licenses: 14\n"
         "  Largest Licensee: Samsung Electronics ($2,100,000)\n\n"
         "Fiscal Year 2021:\n"
         "  Total Licensing Revenue: $11,567,800\n"
         "  Number of Active Licenses: 19\n"
         "  Largest Licensee: Taiwan Semiconductor ($3,450,000)\n\n"
         "Fiscal Year 2022:\n"
         "  Total Licensing Revenue: $15,890,200\n"
         "  Number of Active Licenses: 23\n"
         "  Largest Licensee: Intel Corporation ($4,200,000)\n\n"
         "Fiscal Year 2023:\n"
         "  Total Licensing Revenue: $18,345,600\n"
         "  Number of Active Licenses: 27\n"
         "  Largest Licensee: Taiwan Semiconductor ($5,100,000)\n\n"
         "Fiscal Year 2024 (Projected):\n"
         "  Projected Licensing Revenue: $22,100,000\n"
         "  Projected Active Licenses: 31"),

        ("Exhibit A-4: Expert Witness Declaration - Dr. Rebecca Thornton",
         "DECLARATION OF DR. REBECCA THORNTON\n\n"
         "I, Dr. Rebecca Thornton, declare as follows:\n\n"
         "1. I am a Professor of Electrical Engineering and Materials Science at Stanford University, "
         "where I have been a faculty member since 2008. I received my Ph.D. in Materials Science from "
         "MIT in 2005 and my B.S. in Physics from Caltech in 2000.\n\n"
         "2. I have been retained by counsel for Plex Technologies Corporation to provide expert opinions "
         "regarding the validity and infringement of U.S. Patent No. 11,234,567.\n\n"
         "3. My qualifications include over 120 peer-reviewed publications in the field of semiconductor "
         "fabrication, 15 U.S. patents, and service as a technical consultant to multiple semiconductor "
         "manufacturers including TSMC, GlobalFoundries, and Applied Materials.\n\n"
         "4. OPINION ON CLAIM CONSTRUCTION\n\n"
         "In my professional opinion, the term 'multi-layer deposition sequence' as used in Claim 1 of "
         "the '567 Patent would be understood by a person of ordinary skill in the art to mean a process "
         "involving the sequential deposition of at least three distinct material layers using plasma-"
         "enhanced chemical vapor deposition (PECVD) technology.\n\n"
         "5. I have reviewed the accused products manufactured by Respondent Vertex Semiconductor, Inc., "
         "and in my opinion, the fabrication process used in their 5nm chip line infringes at least "
         "Claims 1, 3, 7, and 12 of the '567 Patent."),

        ("Exhibit A-5: Claim Chart - Infringement Analysis",
         "CLAIM CHART: INFRINGEMENT ANALYSIS\n\n"
         "U.S. Patent No. 11,234,567 vs. Vertex Semiconductor 5nm Process\n\n"
         "CLAIM 1:\n"
         "'A method for semiconductor fabrication comprising: providing a substrate in a vacuum chamber; "
         "initiating a multi-layer deposition sequence using PECVD; controlling plasma density via "
         "real-time spectroscopic feedback; and forming at least three dielectric layers with graded "
         "composition profiles.'\n\n"
         "Vertex 5nm Process:\n"
         "- Uses PECVD chamber (Vertex Model VX-5000) with in-situ substrate loading\n"
         "- Performs sequential deposition of SiO2/SiN/SiON layers\n"
         "- Employs optical emission spectroscopy (OES) for real-time plasma monitoring\n"
         "- Produces graded dielectric stacks with composition varying from pure SiO2 to SiN\n\n"
         "CLAIM 3:\n"
         "'The method of Claim 1, further comprising rotating the substrate at a rate between 5 and "
         "50 RPM during deposition.'\n\n"
         "Vertex 5nm Process:\n"
         "- Substrate rotation at 15 RPM (confirmed by Vertex technical documentation, VX-5000 "
         "Operations Manual, Section 4.3.2)"),

        ("Exhibit A-6: Correspondence - Cease and Desist Letter",
         "MORRISON & KELLER LLP\nAttorneys at Law\n"
         "1200 Park Avenue, Suite 4500\nNew York, NY 10166\n\n"
         "April 3, 2024\n\n"
         "VIA CERTIFIED MAIL AND EMAIL\n\n"
         "Mr. David Chen, General Counsel\nVertex Semiconductor, Inc.\n"
         "4800 Technology Drive\nSan Jose, CA 95134\n\n"
         "Re: Patent Infringement - U.S. Patent No. 11,234,567\n\n"
         "Dear Mr. Chen:\n\n"
         "We represent Plex Technologies Corporation ('Plex') in connection with the above-referenced "
         "patent. We write to notify you that Vertex Semiconductor, Inc. ('Vertex') is infringing one "
         "or more claims of U.S. Patent No. 11,234,567 through its manufacture, use, and sale of "
         "semiconductor devices produced using the Vertex 5nm fabrication process.\n\n"
         "Our client has conducted a thorough investigation and has determined that Vertex's 5nm process "
         "practices at least Claims 1, 3, 7, and 12 of the '567 Patent. We demand that Vertex:\n\n"
         "1. Immediately cease and desist all infringing activities;\n"
         "2. Provide a full accounting of all revenues derived from the infringing process;\n"
         "3. Enter into good-faith licensing negotiations with Plex.\n\n"
         "Please respond within thirty (30) days of receipt of this letter."),

        ("Exhibit A-7: Vertex Response Letter",
         "VERTEX SEMICONDUCTOR, INC.\nLegal Department\n"
         "4800 Technology Drive\nSan Jose, CA 95134\n\n"
         "May 2, 2024\n\n"
         "VIA EMAIL\n\n"
         "Ms. Patricia Morrison, Esq.\nMorrison & Keller LLP\n"
         "1200 Park Avenue, Suite 4500\nNew York, NY 10166\n\n"
         "Re: Response to Patent Infringement Allegations - U.S. Patent No. 11,234,567\n\n"
         "Dear Ms. Morrison:\n\n"
         "We are in receipt of your letter dated April 3, 2024, on behalf of Plex Technologies "
         "Corporation. After careful review by our technical and legal teams, we respectfully disagree "
         "with your allegations of patent infringement.\n\n"
         "Our position is as follows:\n\n"
         "1. NON-INFRINGEMENT: Vertex's 5nm fabrication process does not practice any valid claim of "
         "the '567 Patent. The specific plasma control mechanism employed by Vertex differs fundamentally "
         "from the claimed 'real-time spectroscopic feedback' system.\n\n"
         "2. INVALIDITY: We have identified substantial prior art that anticipates and/or renders "
         "obvious the claims of the '567 Patent, including publications by Dr. Tanaka (2017) and "
         "Dr. Weiss (2018).\n\n"
         "We are prepared to defend our position vigorously in any forum."),

        ("Exhibit A-8: Technical Specification - VX-5000 PECVD System",
         "VERTEX SEMICONDUCTOR, INC.\nTECHNICAL SPECIFICATION DOCUMENT\n\n"
         "Product: VX-5000 Plasma-Enhanced Chemical Vapor Deposition System\n"
         "Document Number: VX-TS-2023-0456\nRevision: 3.2\nDate: September 15, 2023\n\n"
         "1. SYSTEM OVERVIEW\n\n"
         "The VX-5000 is a high-throughput PECVD system designed for advanced node semiconductor "
         "fabrication (7nm and below). Key features include:\n\n"
         "- Multi-zone plasma generation with independent RF power control\n"
         "- Substrate temperature range: 200C to 500C (+/- 1C uniformity)\n"
         "- Chamber base pressure: < 1 x 10^-7 Torr\n"
         "- Substrate rotation: 5-50 RPM (programmable)\n"
         "- In-situ optical emission spectroscopy (OES) monitoring\n\n"
         "2. DEPOSITION CAPABILITIES\n\n"
         "Material          | Rate (nm/min) | Uniformity\n"
         "SiO2              | 50-200        | < 1.5%\n"
         "SiN               | 30-150        | < 2.0%\n"
         "SiON (graded)     | 40-180        | < 1.8%\n"
         "Low-k dielectric  | 20-100        | < 2.5%\n\n"
         "3. PROCESS MONITORING\n\n"
         "The integrated OES system monitors plasma emission lines in real-time, including:\n"
         "- SiH4 emission at 414.2 nm\n"
         "- N2 emission at 337.1 nm\n"
         "- O2 emission at 777.4 nm"),

        ("Exhibit A-9: Deposition Record of Related Patents",
         "UNITED STATES PATENT AND TRADEMARK OFFICE\n\n"
         "CERTIFICATE OF PATENT\n\n"
         "This is to certify that the annexed is a true copy from the records of the United States "
         "Patent and Trademark Office of:\n\n"
         "Patent Number: 11,234,567\n"
         "Issue Date: February 14, 2023\n"
         "Title: Method and System for Multi-Layer Semiconductor Deposition Using Plasma-Enhanced "
         "Chemical Vapor Deposition\n"
         "Inventors: Dr. James R. Whitfield, Dr. Ananya Patel, Dr. Michael Torres\n"
         "Assignee: Plex Technologies Corporation\n"
         "Filing Date: June 8, 2020\n"
         "Priority Date: June 8, 2020\n\n"
         "Number of Claims: 24 (14 independent, 10 dependent)\n\n"
         "Related Patents:\n"
         "- U.S. Patent No. 10,987,654 (parent, issued 2021)\n"
         "- U.S. Patent No. 10,555,321 (continuation, issued 2022)\n"
         "- PCT Application PCT/US2020/036789"),

        ("Exhibit A-10: Damages Report - Dr. Alan Prescott",
         "EXPERT REPORT ON DAMAGES\n\n"
         "Prepared by: Dr. Alan Prescott, CFA, CPA\n"
         "Economic Analysis Group, LLC\nDate: August 10, 2024\n\n"
         "I. QUALIFICATIONS\n\n"
         "I hold a Ph.D. in Economics from the University of Chicago and have over 25 years of "
         "experience in patent damages analysis. I have been qualified as an expert witness in over "
         "80 patent cases in federal courts.\n\n"
         "II. SCOPE OF ANALYSIS\n\n"
         "I have been retained to calculate the reasonable royalty damages owed by Vertex Semiconductor "
         "for its infringement of U.S. Patent No. 11,234,567.\n\n"
         "III. DAMAGES CALCULATION\n\n"
         "Based on my analysis of comparable license agreements, the Georgia-Pacific factors, and "
         "the parties' economic circumstances, I have determined that:\n\n"
         "A. Royalty Base: Total revenue from Vertex's 5nm chip products\n"
         "   FY2023: $2,340,000,000\n"
         "   FY2024 (est.): $3,120,000,000\n\n"
         "B. Royalty Rate: 3.25% (based on comparable licenses in the semiconductor industry)\n\n"
         "C. Total Damages (through 2024): $177,450,000"),

        ("Exhibit A-11: License Agreement Template",
         "PATENT LICENSE AGREEMENT\n\n"
         "This Patent License Agreement ('License') is made effective as of [DATE], by and between "
         "Plex Technologies Corporation ('Licensor') and [LICENSEE] ('Licensee').\n\n"
         "1. DEFINITIONS\n\n"
         "'Licensed Patents' means U.S. Patent Nos. 11,234,567; 10,987,654; and 10,555,321, and any "
         "continuations, divisionals, reissues, or foreign counterparts thereof.\n\n"
         "'Licensed Products' means any product or process that, but for this License, would infringe "
         "one or more claims of the Licensed Patents.\n\n"
         "2. GRANT OF LICENSE\n\n"
         "Subject to the terms and conditions of this License, Licensor grants to Licensee a non-exclusive, "
         "non-transferable, worldwide license under the Licensed Patents to make, use, sell, offer to sell, "
         "and import Licensed Products.\n\n"
         "3. ROYALTIES\n\n"
         "Licensee shall pay to Licensor a running royalty of [X]% of Net Sales of Licensed Products.\n\n"
         "4. TERM\n\n"
         "This License shall remain in effect until the last of the Licensed Patents expires, unless "
         "earlier terminated pursuant to Section 8."),

        ("Exhibit A-12: Prosecution History Summary",
         "PROSECUTION HISTORY SUMMARY\nU.S. Patent Application No. 16/895,234\n"
         "(Issued as U.S. Patent No. 11,234,567)\n\n"
         "June 8, 2020: Application filed (24 claims)\n"
         "October 15, 2020: Filing receipt and preliminary examination\n"
         "March 22, 2021: Non-final Office Action (Claims 1-8 rejected under 35 U.S.C. 102(a)(1); "
         "Claims 9-24 rejected under 35 U.S.C. 103)\n"
         "September 22, 2021: Response to Office Action (Claims 1-8 amended; Claims 9-24 argued)\n"
         "January 10, 2022: Final Office Action (Claims 1-5 allowed; Claims 6-8 rejected under "
         "35 U.S.C. 112(b); Claims 9-24 maintained rejection)\n"
         "April 10, 2022: Request for Continued Examination (RCE) filed\n"
         "July 18, 2022: Non-final Office Action after RCE (Claims 6-8 amended and allowed; "
         "Claims 9-18 allowed; Claims 19-24 rejected under 35 U.S.C. 103)\n"
         "October 18, 2022: Response (Claims 19-24 amended)\n"
         "November 30, 2022: Notice of Allowance (all 24 claims)\n"
         "February 14, 2023: Patent issued"),

        ("Exhibit A-13: ITC Complaint Filing",
         "BEFORE THE UNITED STATES INTERNATIONAL TRADE COMMISSION\n"
         "Washington, D.C.\n\n"
         "In the Matter of:\nCERTAIN SEMICONDUCTOR DEVICES AND\n"
         "PRODUCTS CONTAINING SAME\n\n"
         "Investigation No. 337-TA-[XXXX]\n\n"
         "COMPLAINT UNDER SECTION 337\nOF THE TARIFF ACT OF 1930, AS AMENDED\n\n"
         "Complainant: Plex Technologies Corporation\n"
         "Proposed Respondent: Vertex Semiconductor, Inc.\n\n"
         "I. INTRODUCTION\n\n"
         "Complainant Plex Technologies Corporation ('Plex') files this Complaint pursuant to "
         "Section 337 of the Tariff Act of 1930, as amended, 19 U.S.C. 1337, requesting that the "
         "Commission institute an investigation into the unlawful importation into the United States "
         "of certain semiconductor devices and products containing same that infringe one or more "
         "claims of U.S. Patent No. 11,234,567.\n\n"
         "II. THE PARTIES\n\n"
         "A. Complainant Plex Technologies Corporation is a California corporation with its principal "
         "place of business at 2500 Innovation Parkway, Menlo Park, CA 94025."),

        ("Exhibit A-14: Supply Chain Analysis",
         "SUPPLY CHAIN ANALYSIS REPORT\n"
         "Vertex Semiconductor 5nm Product Line\n\n"
         "Prepared by: Industrial Intelligence Partners, LLC\nDate: July 2024\n\n"
         "1. MANUFACTURING LOCATIONS\n\n"
         "Vertex's 5nm chips are fabricated at the following facilities:\n"
         "- Vertex Fab 3 (Hsinchu, Taiwan) - Primary production\n"
         "- Vertex Fab 5 (Dresden, Germany) - Secondary production\n"
         "- Contract fabrication at TSMC (Tainan, Taiwan) - Overflow capacity\n\n"
         "2. PRODUCT DISTRIBUTION\n\n"
         "Finished semiconductor devices are imported into the United States through:\n"
         "- Port of Long Beach, CA (estimated 45% of volume)\n"
         "- Port of Newark, NJ (estimated 30% of volume)\n"
         "- Memphis, TN air freight hub (estimated 25% of volume)\n\n"
         "3. KEY CUSTOMERS IN THE U.S.\n\n"
         "- Apple Inc. (Cupertino, CA) - Mobile processor SoCs\n"
         "- NVIDIA Corporation (Santa Clara, CA) - AI accelerator chips\n"
         "- Amazon Web Services (Seattle, WA) - Custom cloud processors\n"
         "- Tesla, Inc. (Austin, TX) - Autonomous driving controllers"),

        ("Exhibit A-15: Inventor Deposition Transcript Excerpts",
         "DEPOSITION OF DR. JAMES R. WHITFIELD\nJune 15, 2024\n\n"
         "EXAMINATION BY MS. MORRISON:\n\n"
         "Q: Dr. Whitfield, can you describe the key innovation of the '567 Patent?\n\n"
         "A: Yes. The fundamental advance is the integration of real-time spectroscopic feedback "
         "into the PECVD deposition control loop. Prior systems used pre-set recipes, but our system "
         "monitors plasma composition in real-time and adjusts parameters on-the-fly to achieve precise "
         "graded composition profiles.\n\n"
         "Q: How does this differ from the prior art cited by the Examiner during prosecution?\n\n"
         "A: The Tanaka reference, for example, describes a rotating substrate holder but uses a "
         "fixed-recipe approach. There is no feedback mechanism. Our invention combines rotation with "
         "active plasma monitoring to achieve uniformity levels that were previously unattainable.\n\n"
         "Q: When did you first conceive of this invention?\n\n"
         "A: I first had the idea in late 2019, around November. Dr. Patel and I were working on "
         "improving deposition uniformity in our lab at Plex, and we realized that OES data could "
         "be fed back into the control system in real-time."),

        ("Exhibit A-16: Financial Projections - Patent Portfolio",
         "PATENT PORTFOLIO VALUATION\nPlex Technologies Corporation\n\n"
         "Prepared by: Meridian Valuation Services\nDate: March 2024\n\n"
         "1. PORTFOLIO OVERVIEW\n\n"
         "The Plex semiconductor patent portfolio consists of:\n"
         "- 12 issued U.S. patents\n"
         "- 5 pending U.S. applications\n"
         "- 8 international filings (PCT, EP, JP, KR, CN)\n"
         "- Total estimated remaining life: 14.5 years (weighted average)\n\n"
         "2. VALUATION METHODOLOGY\n\n"
         "We employed three approaches:\n"
         "- Income Approach (DCF): $285,000,000\n"
         "- Market Approach (comparable transactions): $310,000,000\n"
         "- Cost Approach (replacement cost): $175,000,000\n\n"
         "3. CONCLUDED VALUE\n\n"
         "Based on a weighted average of the three approaches (50% income, 35% market, 15% cost), "
         "the fair market value of the Plex semiconductor patent portfolio is:\n\n"
         "  CONCLUDED FAIR MARKET VALUE: $278,250,000\n\n"
         "This valuation assumes continued enforcement and active licensing programs."),

        ("Exhibit A-17: Technical Tutorial - PECVD Fundamentals",
         "PLASMA-ENHANCED CVD: TECHNICAL PRIMER\n\n"
         "Prepared for litigation counsel by Dr. Rebecca Thornton\n\n"
         "1. WHAT IS PECVD?\n\n"
         "Plasma-Enhanced Chemical Vapor Deposition (PECVD) is a thin film deposition process "
         "used extensively in semiconductor manufacturing. Unlike thermal CVD, which requires "
         "substrate temperatures above 600C, PECVD uses plasma energy to enable chemical reactions "
         "at temperatures as low as 200C.\n\n"
         "2. BASIC PROCESS\n\n"
         "Step 1: Precursor gases (e.g., SiH4, N2O, NH3) are introduced into a vacuum chamber.\n"
         "Step 2: Radio frequency (RF) power (typically 13.56 MHz) generates a plasma.\n"
         "Step 3: Plasma dissociates precursor molecules into reactive species.\n"
         "Step 4: Reactive species deposit on the substrate surface, forming a thin film.\n"
         "Step 5: Byproduct gases are pumped away.\n\n"
         "3. KEY PARAMETERS\n\n"
         "- RF Power: Controls plasma density and deposition rate\n"
         "- Pressure: Typically 0.1-10 Torr; affects film quality\n"
         "- Temperature: 200-400C for most applications\n"
         "- Gas flow ratios: Determine film composition\n"
         "- Substrate rotation: Improves thickness uniformity"),

        ("Exhibit A-18: Market Analysis - Semiconductor Industry",
         "SEMICONDUCTOR INDUSTRY MARKET ANALYSIS\n\n"
         "Prepared by: Pacific Rim Technology Research\nDate: Q2 2024\n\n"
         "1. GLOBAL MARKET SIZE\n\n"
         "The global semiconductor market reached $574.1 billion in 2023, with projected growth "
         "to $680 billion by 2025 (CAGR: 8.8%).\n\n"
         "2. ADVANCED NODE (7nm AND BELOW) SEGMENT\n\n"
         "Revenue by manufacturer:\n"
         "- TSMC: $42.3 billion (62% market share)\n"
         "- Samsung: $14.2 billion (21%)\n"
         "- Intel: $6.8 billion (10%)\n"
         "- Vertex Semiconductor: $3.4 billion (5%)\n"
         "- Others: $1.4 billion (2%)\n\n"
         "3. VERTEX SEMICONDUCTOR PROFILE\n\n"
         "Founded: 2015\nHeadquarters: San Jose, California\n"
         "2023 Revenue: $8.7 billion (total), $3.4 billion (5nm segment)\n"
         "Employees: 12,400\n"
         "R&D Spending: $1.9 billion (21.8% of revenue)\n\n"
         "Vertex has grown rapidly in the advanced node segment, increasing 5nm revenue by "
         "340% from 2021 to 2023."),

        ("Exhibit A-19: Settlement Demand Letter",
         "MORRISON & KELLER LLP\nAttorneys at Law\n"
         "1200 Park Avenue, Suite 4500\nNew York, NY 10166\n\n"
         "CONFIDENTIAL - FOR SETTLEMENT PURPOSES ONLY\n"
         "SUBJECT TO FRE 408\n\n"
         "September 5, 2024\n\n"
         "Mr. David Chen, General Counsel\nVertex Semiconductor, Inc.\n\n"
         "Re: Settlement Proposal - U.S. Patent No. 11,234,567\n\n"
         "Dear Mr. Chen:\n\n"
         "Following the filing of our ITC complaint and the institution of Investigation "
         "No. 337-TA-1298, our client Plex Technologies Corporation proposes the following "
         "settlement terms:\n\n"
         "1. LUMP SUM PAYMENT: Vertex shall pay Plex $95,000,000 as past damages for the period "
         "2022-2024.\n\n"
         "2. ONGOING LICENSE: Vertex shall enter into a non-exclusive license agreement at a royalty "
         "rate of 2.75% of net sales of Licensed Products.\n\n"
         "3. CROSS-LICENSE: Plex shall grant Vertex a non-exclusive license to its full semiconductor "
         "patent portfolio, and Vertex shall grant reciprocal rights.\n\n"
         "This offer remains open for sixty (60) days from the date of this letter."),

        ("Exhibit A-20: Case Timeline Summary",
         "CASE TIMELINE\nPlex Technologies Corp. v. Vertex Semiconductor, Inc.\n\n"
         "2019-11: Invention conceived by Drs. Whitfield, Patel, and Torres\n"
         "2020-06-08: U.S. Patent Application No. 16/895,234 filed\n"
         "2023-02-14: U.S. Patent No. 11,234,567 issued\n"
         "2023-09: Plex identifies potential infringement by Vertex\n"
         "2024-01-22: Prior art search report completed\n"
         "2024-03-15: Patent assignment from Nextera to Plex finalized\n"
         "2024-04-03: Cease and desist letter sent to Vertex\n"
         "2024-05-02: Vertex response received - denies infringement\n"
         "2024-06-15: Dr. Whitfield deposition conducted\n"
         "2024-07: Supply chain analysis completed\n"
         "2024-08-10: Dr. Prescott damages report completed\n"
         "2024-08-15: ITC complaint filed\n"
         "2024-09-05: Settlement demand sent to Vertex\n"
         "2024-09-20: ITC Investigation No. 337-TA-1298 instituted\n"
         "2024-10: Discovery phase begins\n"
         "2024-12: Markman hearing scheduled\n"
         "2025-03: Target trial date at ITC\n\n"
         "TOTAL ESTIMATED DAMAGES THROUGH 2024: $177,450,000\n"
         "SETTLEMENT DEMAND: $95,000,000 + 2.75% ongoing royalty"),
    ]

    for i, (title, body) in enumerate(exhibits_a):
        create_exhibit_page(doc, i + 1, "A", title, body)

    output_path = f'{EXHIBITS_DIR}/set_a.pdf'
    doc.save(output_path)
    doc.close()
    print(f'Created: {output_path} ({len(exhibits_a)} pages)')


def create_set_b():
    """Create Exhibit Set B - 15 pages of trade secret / employment documents."""
    doc = pymupdf.open()

    exhibits_b = [
        ("Exhibit B-1: Employment Agreement - Dr. Michael Torres",
         "EMPLOYMENT AGREEMENT\n\n"
         "This Employment Agreement ('Agreement') is made as of January 15, 2018, by and between "
         "Nextera Innovations, Inc. ('Company') and Dr. Michael Torres ('Employee').\n\n"
         "1. POSITION AND DUTIES\n\n"
         "Employee shall serve as Director of Process Engineering, reporting to the VP of R&D. "
         "Employee's responsibilities shall include overseeing all PECVD process development "
         "activities and managing a team of 15 engineers.\n\n"
         "2. COMPENSATION\n\n"
         "Base Salary: $245,000 per annum\n"
         "Signing Bonus: $50,000\n"
         "Annual Bonus Target: 25% of base salary\n"
         "Stock Options: 50,000 shares (4-year vest, 1-year cliff)\n\n"
         "3. CONFIDENTIALITY\n\n"
         "Employee agrees to maintain strict confidentiality of all proprietary information, "
         "trade secrets, and inventions developed during the course of employment."),

        ("Exhibit B-2: Non-Compete Agreement",
         "NON-COMPETITION AND NON-SOLICITATION AGREEMENT\n\n"
         "This Agreement is entered into as of January 15, 2018, by Dr. Michael Torres ('Employee') "
         "in connection with his employment by Nextera Innovations, Inc. ('Company').\n\n"
         "1. NON-COMPETE COVENANT\n\n"
         "For a period of twelve (12) months following termination, Employee shall not:\n"
         "(a) Engage in semiconductor process development for any Competing Business;\n"
         "(b) Accept employment with any entity that manufactures PECVD equipment;\n"
         "(c) Provide consulting services related to thin film deposition.\n\n"
         "2. NON-SOLICITATION\n\n"
         "For a period of eighteen (18) months following termination, Employee shall not:\n"
         "(a) Solicit any customer or client of the Company;\n"
         "(b) Recruit or hire any employee of the Company.\n\n"
         "3. GEOGRAPHIC SCOPE\n\n"
         "The restrictions in Section 1 apply within the United States, Taiwan, South Korea, "
         "Japan, and the European Union."),

        ("Exhibit B-3: Resignation Letter - Dr. Torres",
         "Dr. Michael Torres\n1847 Willow Creek Drive\nPalo Alto, CA 94301\n\n"
         "March 1, 2022\n\n"
         "Dr. Sandra Kim, VP of R&D\nNextera Innovations, Inc.\n"
         "3300 Semiconductor Way\nSanta Clara, CA 95054\n\n"
         "Dear Dr. Kim:\n\n"
         "I am writing to inform you of my resignation from Nextera Innovations, effective "
         "March 31, 2022. This was not an easy decision, as I have greatly valued my four years "
         "with the company and the opportunity to lead the PECVD process development team.\n\n"
         "I have accepted a position at Vertex Semiconductor, Inc., where I will be serving as "
         "VP of Advanced Manufacturing. I believe this represents an exciting opportunity for "
         "career growth.\n\n"
         "I am committed to ensuring a smooth transition and will complete all ongoing projects "
         "during my remaining time. I will also fully comply with my confidentiality obligations "
         "and return all company property.\n\n"
         "Thank you for the mentorship and support.\n\n"
         "Sincerely,\nDr. Michael Torres"),

        ("Exhibit B-4: Exit Interview Notes",
         "EXIT INTERVIEW RECORD\n\n"
         "Employee: Dr. Michael Torres\n"
         "Date: March 28, 2022\n"
         "Interviewer: Jennifer Walsh, Director of Human Resources\n\n"
         "SUMMARY:\n\n"
         "Dr. Torres stated that his primary reason for departure was a desire for broader "
         "leadership responsibilities. He mentioned that the VP of Advanced Manufacturing role "
         "at Vertex would allow him to oversee both PECVD and PVD operations.\n\n"
         "KEY POINTS:\n\n"
         "1. Dr. Torres confirmed he understands his confidentiality obligations and signed the "
         "exit certification form.\n\n"
         "2. He returned his laptop (Asset ID: NX-L-4523), badge, and all physical documents.\n\n"
         "3. IT confirmed remote access has been revoked as of 5:00 PM today.\n\n"
         "4. Dr. Torres was reminded of his non-compete agreement and stated he had consulted "
         "with personal counsel regarding its enforceability.\n\n"
         "INTERVIEWER NOTES:\n"
         "Dr. Torres appeared cooperative throughout the interview. However, his move to Vertex "
         "is concerning given his deep knowledge of our proprietary PECVD processes."),

        ("Exhibit B-5: IT Forensics Report",
         "DIGITAL FORENSICS INVESTIGATION REPORT\n\n"
         "Case: Torres Data Access Review\n"
         "Investigator: Marcus Rodriguez, CISSP, GCFE\n"
         "Date: April 15, 2022\n\n"
         "1. SCOPE\n\n"
         "At the request of Legal, Digital Security conducted a forensic review of Dr. Michael "
         "Torres's digital activity during his final 90 days of employment (January 1 - March 31, 2022).\n\n"
         "2. FINDINGS\n\n"
         "2.1 FILE ACCESS ANOMALIES\n\n"
         "Between February 15-28, 2022, Dr. Torres accessed 247 files on the restricted R&D server "
         "(server: NX-RD-PROD-03) that were outside his normal work scope:\n\n"
         "- 89 files related to next-generation 3nm PECVD process recipes\n"
         "- 43 files containing substrate rotation optimization algorithms\n"
         "- 62 files with proprietary plasma modeling simulation data\n"
         "- 53 files documenting OES calibration procedures\n\n"
         "2.2 USB DEVICE ACTIVITY\n\n"
         "On February 22, 2022, a USB storage device (SanDisk Ultra 128GB, S/N: 4CE0014D) was "
         "connected to Dr. Torres's workstation. Approximately 3.2 GB of data was transferred "
         "to the device over a 45-minute period.\n\n"
         "2.3 EMAIL ANALYSIS\n\n"
         "Dr. Torres forwarded 17 emails containing technical attachments to his personal Gmail "
         "account (m.torres.eng@gmail.com) between February 20-27, 2022."),

        ("Exhibit B-6: USB Device Contents Reconstruction",
         "USB DEVICE CONTENTS RECONSTRUCTION\n\n"
         "Based on forensic analysis of Dr. Torres's workstation and file server access logs, "
         "the following files are believed to have been copied to the USB device on February 22, 2022:\n\n"
         "Directory: /Process_Recipes/\n"
         "  - PECVD_5nm_SiO2_v4.2.rcp (Last Modified: 2022-01-10)\n"
         "  - PECVD_5nm_SiN_v3.8.rcp (Last Modified: 2022-01-15)\n"
         "  - PECVD_5nm_SiON_graded_v2.1.rcp (Last Modified: 2022-02-01)\n"
         "  - PECVD_3nm_experimental_v0.9.rcp (Last Modified: 2022-02-12)\n\n"
         "Directory: /Simulation_Data/\n"
         "  - plasma_model_5nm_calibrated.dat (1.2 GB)\n"
         "  - substrate_rotation_optimization.m (MATLAB, 450 KB)\n"
         "  - OES_spectral_library_v6.db (800 MB)\n\n"
         "Directory: /Documentation/\n"
         "  - VX_competitor_analysis_Q4_2021.pptx\n"
         "  - Patent_strategy_2022_2025.docx\n"
         "  - Customer_licensing_terms_master.xlsx\n\n"
         "TOTAL ESTIMATED SIZE: 3.18 GB\n"
         "CLASSIFICATION: All files marked CONFIDENTIAL or RESTRICTED"),

        ("Exhibit B-7: Temporary Restraining Order",
         "UNITED STATES DISTRICT COURT\n"
         "NORTHERN DISTRICT OF CALIFORNIA\nSAN JOSE DIVISION\n\n"
         "NEXTERA INNOVATIONS, INC.,\n  Plaintiff,\n\nv.\n\n"
         "DR. MICHAEL TORRES and\nVERTEX SEMICONDUCTOR, INC.,\n  Defendants.\n\n"
         "Case No. 5:22-cv-02847-LHK\n\n"
         "ORDER GRANTING TEMPORARY RESTRAINING ORDER\n\n"
         "Upon consideration of Plaintiff's emergency motion for a temporary restraining order, "
         "and good cause appearing therefor, IT IS HEREBY ORDERED:\n\n"
         "1. Defendant Dr. Michael Torres is RESTRAINED from:\n"
         "   (a) Using, disclosing, or disseminating any trade secrets or confidential information "
         "of Nextera Innovations;\n"
         "   (b) Destroying, altering, or concealing any documents or electronic media obtained "
         "from Nextera Innovations;\n\n"
         "2. Defendant Vertex Semiconductor, Inc. is RESTRAINED from:\n"
         "   (a) Using any Nextera trade secrets in its manufacturing processes;\n"
         "   (b) Deploying any process recipes or simulation data originating from Nextera;\n\n"
         "3. Defendants shall preserve all documents and electronic media.\n\n"
         "SO ORDERED this 20th day of April, 2022.\n"
         "Hon. Lucy H. Koh, United States District Judge"),

        ("Exhibit B-8: Torres Deposition Transcript",
         "DEPOSITION OF DR. MICHAEL TORRES\nMay 10, 2022\n\n"
         "EXAMINATION BY MR. GRAHAM (Counsel for Nextera):\n\n"
         "Q: Dr. Torres, did you copy any Nextera files to a USB device in February 2022?\n\n"
         "A: I copied some of my own work product - personal notes and presentations I had created.\n\n"
         "Q: The forensic report indicates 3.2 gigabytes of data were copied. Were those all "
         "personal notes?\n\n"
         "A: I may have inadvertently copied some additional files. The USB drive had auto-sync "
         "software that may have pulled files from shared directories.\n\n"
         "Q: Did you forward emails with technical attachments to your personal Gmail account?\n\n"
         "A: I forwarded some emails for reference purposes. I regularly work from home and "
         "sometimes need access to my work on personal devices.\n\n"
         "Q: Were you aware that forwarding confidential technical documents to personal email "
         "violated company policy?\n\n"
         "A: I was aware of the policy but believed my actions were within the scope of my normal "
         "work practices. Many engineers at Nextera access work materials remotely.\n\n"
         "Q: When did you first have discussions with Vertex about employment?\n\n"
         "A: I was first contacted by a Vertex recruiter in December 2021."),

        ("Exhibit B-9: Vertex Internal Email Chain",
         "FROM: David Chen <d.chen@vertex-semi.com>\n"
         "TO: Sarah Park <s.park@vertex-semi.com>\n"
         "CC: Robert Liu <r.liu@vertex-semi.com>\n"
         "DATE: April 2, 2022\n"
         "SUBJECT: RE: Torres Onboarding - Process Integration\n\n"
         "Sarah,\n\n"
         "I want to make sure we handle Mike Torres's onboarding carefully. Given the sensitivity "
         "around his departure from Nextera, please ensure:\n\n"
         "1. All work he does is documented as independently developed.\n"
         "2. He should NOT bring any materials from his previous employer.\n"
         "3. Set up an ethical wall between his team and the 5nm PECVD group for the first 6 months.\n\n"
         "We need to protect Vertex while still leveraging Mike's expertise.\n\n"
         "David\n\n"
         "---\n"
         "FROM: Sarah Park <s.park@vertex-semi.com>\n"
         "TO: David Chen <d.chen@vertex-semi.com>\n"
         "DATE: April 1, 2022\n"
         "SUBJECT: Torres Onboarding - Process Integration\n\n"
         "David,\n\n"
         "Mike Torres starts Monday. He's eager to dive into our 5nm process optimization. "
         "Should we have him review our current PECVD recipes first, or start fresh with his "
         "own approach? His experience could accelerate our roadmap by 6-12 months.\n\n"
         "Sarah"),

        ("Exhibit B-10: Comparison Analysis - Before and After Torres",
         "TECHNICAL COMPARISON ANALYSIS\n\n"
         "Vertex 5nm PECVD Process: Pre-Torres vs. Post-Torres\n"
         "Prepared by: Nextera Expert Consulting Team\nDate: August 2022\n\n"
         "PARAMETER           | PRE-TORRES      | POST-TORRES     | NEXTERA PROCESS\n"
         "                    | (Before Apr '22) | (After Apr '22) | (Confidential)\n"
         "--------------------+-----------------+-----------------+------------------\n"
         "SiO2 dep rate       | 80 nm/min       | 145 nm/min      | 150 nm/min\n"
         "SiN dep rate        | 55 nm/min       | 120 nm/min      | 125 nm/min\n"
         "Uniformity (SiO2)   | 3.2%            | 1.4%            | 1.3%\n"
         "Uniformity (SiN)    | 4.1%            | 1.9%            | 1.8%\n"
         "Substrate rotation  | Not used        | 15 RPM          | 12 RPM\n"
         "OES feedback        | Post-run only   | Real-time       | Real-time\n"
         "Graded SiON         | Not available   | Available       | Available\n"
         "Plasma recipe steps | 3               | 7               | 8\n\n"
         "CONCLUSION: The dramatic improvement in Vertex's process parameters after Dr. Torres "
         "joined, combined with the striking similarity to Nextera's proprietary process, "
         "strongly suggests misappropriation of Nextera trade secrets."),

        ("Exhibit B-11: Expert Report on Trade Secret Identification",
         "EXPERT REPORT ON TRADE SECRET IDENTIFICATION\n\n"
         "Prepared by: Dr. Karen Washburn, Ph.D.\n"
         "Semiconductor Process Consulting, Inc.\nDate: September 2022\n\n"
         "1. TRADE SECRETS AT ISSUE\n\n"
         "I have identified the following categories of Nextera trade secrets:\n\n"
         "Trade Secret 1: Graded SiON PECVD Recipe\n"
         "- Multi-step process with precisely controlled gas flow ratios\n"
         "- Novel use of NH3/N2O gas switching for composition grading\n"
         "- Protected since: 2019\n"
         "- Economic value: Estimated $15M+ in licensing revenue annually\n\n"
         "Trade Secret 2: OES Feedback Algorithm\n"
         "- Proprietary spectral analysis for real-time plasma monitoring\n"
         "- Uses machine learning model trained on 50,000+ process runs\n"
         "- Protected since: 2020\n"
         "- Economic value: Key differentiator for process control\n\n"
         "Trade Secret 3: Substrate Rotation Optimization\n"
         "- Empirically derived RPM profiles for different film compositions\n"
         "- Enables sub-2% uniformity across 300mm wafers\n"
         "- Protected since: 2019\n"
         "- Economic value: Reduces wafer rejection rate by 40%"),

        ("Exhibit B-12: Privilege Log (Partial)",
         "PRIVILEGE LOG\nNextera Innovations, Inc. v. Torres & Vertex Semiconductor, Inc.\n"
         "Case No. 5:22-cv-02847-LHK\n\n"
         "Entry | Date       | From           | To                | Subject                          | Privilege\n"
         "------+------------+----------------+-------------------+----------------------------------+-----------\n"
         "001   | 2022-03-15 | S. Kim         | Legal Dept.       | Torres Departure Concerns        | A/C\n"
         "002   | 2022-03-18 | Legal Dept.    | CEO               | Potential Trade Secret Theft     | A/C, WP\n"
         "003   | 2022-04-01 | M. Rodriguez   | Legal Dept.       | Forensic Investigation Update    | A/C, WP\n"
         "004   | 2022-04-05 | Outside Counsel| Board of Directors| Litigation Strategy              | A/C, WP\n"
         "005   | 2022-04-10 | Legal Dept.    | HR Dept.          | Torres NDA Obligations           | A/C\n"
         "006   | 2022-04-12 | Outside Counsel| Legal Dept.       | TRO Motion Draft                 | A/C, WP\n"
         "007   | 2022-04-18 | Expert Counsel | Legal Dept.       | Trade Secret Identification      | A/C, WP\n"
         "008   | 2022-05-01 | Legal Dept.    | Outside Counsel   | Torres Depo Preparation          | A/C, WP\n"
         "009   | 2022-06-15 | Outside Counsel| Legal Dept.       | Settlement Considerations        | A/C, WP\n"
         "010   | 2022-07-22 | Legal Dept.    | Board of Directors| Case Status Update               | A/C\n\n"
         "A/C = Attorney-Client Privilege\n"
         "WP = Work Product Doctrine"),

        ("Exhibit B-13: Nextera Security Policy Excerpts",
         "NEXTERA INNOVATIONS, INC.\nINFORMATION SECURITY POLICY\nVersion 4.1 - Effective January 1, 2021\n\n"
         "Section 5: DATA CLASSIFICATION AND HANDLING\n\n"
         "5.1 Classification Levels:\n"
         "  - PUBLIC: Information approved for external distribution\n"
         "  - INTERNAL: For employee use only\n"
         "  - CONFIDENTIAL: Restricted to authorized personnel\n"
         "  - RESTRICTED: Highest sensitivity; access requires VP+ approval\n\n"
         "5.2 Prohibited Activities:\n"
         "  (a) Copying CONFIDENTIAL or RESTRICTED data to personal devices or accounts\n"
         "  (b) Using unauthorized USB storage devices on company systems\n"
         "  (c) Forwarding company emails with technical attachments to personal accounts\n"
         "  (d) Storing company data on non-approved cloud services\n\n"
         "Section 7: EMPLOYEE DEPARTURE PROCEDURES\n\n"
         "7.1 Upon notice of resignation or termination:\n"
         "  (a) Immediate review of file access patterns (past 90 days)\n"
         "  (b) Preservation of all electronic communications\n"
         "  (c) Exit interview with IT Security representative\n"
         "  (d) Return and verification of all company assets\n"
         "  (e) Revocation of all system access within 4 hours of final departure"),

        ("Exhibit B-14: Court Order - Discovery Sanctions",
         "UNITED STATES DISTRICT COURT\n"
         "NORTHERN DISTRICT OF CALIFORNIA\nSAN JOSE DIVISION\n\n"
         "NEXTERA INNOVATIONS, INC.,\n  Plaintiff,\n\nv.\n\n"
         "DR. MICHAEL TORRES and\nVERTEX SEMICONDUCTOR, INC.,\n  Defendants.\n\n"
         "Case No. 5:22-cv-02847-LHK\n\n"
         "ORDER RE: PLAINTIFF'S MOTION FOR DISCOVERY SANCTIONS\n\n"
         "Plaintiff's motion for sanctions based on Defendant Vertex's failure to produce "
         "documents responsive to Requests for Production Nos. 15-22 came before the Court "
         "on October 5, 2022.\n\n"
         "The Court finds that:\n\n"
         "1. Vertex failed to produce internal communications regarding Dr. Torres's onboarding "
         "and integration into the 5nm PECVD team, despite their clear relevance.\n\n"
         "2. Vertex's claim that such documents are protected by attorney-client privilege is "
         "largely without merit, as the communications were primarily between business personnel.\n\n"
         "IT IS HEREBY ORDERED:\n\n"
         "1. Vertex shall produce all responsive documents within 14 days.\n"
         "2. Vertex shall pay Plaintiff's reasonable attorneys' fees in bringing this motion.\n"
         "3. The Court reserves the right to impose additional sanctions.\n\n"
         "SO ORDERED this 12th day of October, 2022."),

        ("Exhibit B-15: Joint Status Report",
         "UNITED STATES DISTRICT COURT\n"
         "NORTHERN DISTRICT OF CALIFORNIA\nSAN JOSE DIVISION\n\n"
         "Case No. 5:22-cv-02847-LHK\n\n"
         "JOINT STATUS REPORT\n\n"
         "Pursuant to the Court's scheduling order, the parties submit this joint status report:\n\n"
         "1. CURRENT STATUS\n\n"
         "Fact discovery is ongoing. To date, the parties have exchanged over 450,000 documents "
         "and conducted 12 depositions.\n\n"
         "2. PLAINTIFF'S POSITION\n\n"
         "Nextera maintains that evidence obtained through discovery confirms trade secret "
         "misappropriation by Dr. Torres and knowing participation by Vertex. The forensic "
         "evidence, combined with the dramatic improvement in Vertex's process parameters, "
         "establishes a compelling case for preliminary injunctive relief.\n\n"
         "3. DEFENDANTS' POSITION\n\n"
         "Defendants maintain that all process improvements at Vertex were independently developed. "
         "Dr. Torres's expertise in PECVD technology is the result of his education and two decades "
         "of industry experience, not trade secret misappropriation.\n\n"
         "4. UPCOMING MILESTONES\n\n"
         "Expert discovery deadline: December 15, 2022\n"
         "Summary judgment motions: January 31, 2023\n"
         "Pretrial conference: March 1, 2023\n"
         "Trial date: March 20, 2023\n\n"
         "Respectfully submitted,\n\n"
         "Morrison & Keller LLP (for Plaintiff)\n"
         "Wilson, Park & Associates (for Defendants)"),
    ]

    for i, (title, body) in enumerate(exhibits_b):
        create_exhibit_page(doc, i + 1, "B", title, body)

    output_path = f'{EXHIBITS_DIR}/set_b.pdf'
    doc.save(output_path)
    doc.close()
    print(f'Created: {output_path} ({len(exhibits_b)} pages)')


def create_initial():
    # Create directory structure
    os.makedirs(EXHIBITS_DIR, exist_ok=True)

    # Create both exhibit sets
    create_set_a()
    create_set_b()

    # Open Set A in Evince for the agent
    launch_gui(f'evince "{EXHIBITS_DIR}/set_a.pdf"', delay_sec=2.0)
    print('GUI_READY: launched Evince with set_a.pdf on DISPLAY=:0')


create_initial()
