"""
Initial Setup: Create a 12-page legal settlement agreement PDF with dates and dollar amounts
Task ID: pdf_pw_031
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_031'
OUTPUT_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{OUTPUT_DIR}/settlement_agreement.pdf'

# Page dimensions (Letter size)
PAGE_W, PAGE_H = 612, 792

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

def add_text(page, x, y, text, fontsize=11, fontname="tiro", color=(0, 0, 0), bold=False):
    """Insert text at position, return updated y position."""
    fn = "tibo" if bold else fontname
    page.insert_text(pymupdf.Point(x, y), text, fontsize=fontsize, fontname=fn, color=color)
    return y + fontsize + 4

def add_paragraph(page, x, y, text, fontsize=11, fontname="tiro", line_width=468, max_y=740):
    """Insert wrapped paragraph text. Returns updated y position."""
    rect = pymupdf.Rect(x, y, x + line_width, max_y)
    excess = page.insert_textbox(rect, text, fontsize=fontsize, fontname=fontname,
                                  color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    # Estimate lines used
    chars_per_line = int(line_width / (fontsize * 0.5))
    num_lines = max(1, (len(text) + chars_per_line - 1) // chars_per_line)
    return y + num_lines * (fontsize + 3) + 8

def create_initial():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    doc = pymupdf.open()

    # =========================================================================
    # PAGE 1: Title Page
    # =========================================================================
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    y = 200
    page.insert_text(pymupdf.Point(306, y), "SETTLEMENT AGREEMENT", fontsize=22, fontname="tibo",
                     color=(0, 0, 0))
    # Center by using textbox
    rect = pymupdf.Rect(72, y - 10, 540, y + 30)
    page.insert_textbox(rect, "SETTLEMENT AGREEMENT", fontsize=22, fontname="tibo",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_CENTER)
    y += 50
    rect = pymupdf.Rect(72, y, 540, y + 25)
    page.insert_textbox(rect, "AND MUTUAL RELEASE", fontsize=18, fontname="tibo",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_CENTER)
    y += 60
    rect = pymupdf.Rect(72, y, 540, y + 20)
    page.insert_textbox(rect, "Case No. 2024-CV-08923", fontsize=14, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_CENTER)
    y += 40
    rect = pymupdf.Rect(72, y, 540, y + 20)
    page.insert_textbox(rect, "Westbrook Technologies, Inc. v. Meridian Solutions Group, LLC",
                        fontsize=13, fontname="tiit", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_CENTER)
    y += 40
    rect = pymupdf.Rect(72, y, 540, y + 20)
    page.insert_textbox(rect, "Executed on 2024-06-15", fontsize=12, fontname="tiro",
                        color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_CENTER)
    y += 40
    rect = pymupdf.Rect(72, y, 540, y + 20)
    page.insert_textbox(rect, "Superior Court of the State of California, County of Santa Clara",
                        fontsize=11, fontname="tiro", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_CENTER)

    # =========================================================================
    # PAGE 2: Recitals and Definitions
    # =========================================================================
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    y = 72
    y = add_text(page, 72, y, "I. RECITALS", fontsize=14, bold=True)
    y += 8

    y = add_paragraph(page, 72, y,
        "This Settlement Agreement and Mutual Release (\"Agreement\") is entered into as of "
        "2024-06-15 by and between Westbrook Technologies, Inc., a Delaware corporation "
        "(\"Plaintiff\" or \"Westbrook\"), and Meridian Solutions Group, LLC, an Oregon limited "
        "liability company (\"Defendant\" or \"Meridian\"), collectively referred to as the \"Parties.\"")
    y += 4

    y = add_paragraph(page, 72, y,
        "WHEREAS, Westbrook filed a civil complaint against Meridian on 2023-03-22 in the "
        "Superior Court of the State of California, County of Santa Clara, Case No. 2024-CV-08923, "
        "alleging breach of contract, misappropriation of trade secrets, and unfair business "
        "practices arising from the Software Development and Licensing Agreement dated 2022-08-10;")
    y += 4

    y = add_paragraph(page, 72, y,
        "WHEREAS, Meridian filed counterclaims on 2023-05-14 alleging breach of the implied "
        "covenant of good faith and fair dealing, fraudulent inducement, and unjust enrichment;")
    y += 4

    y = add_paragraph(page, 72, y,
        "WHEREAS, the Parties have engaged in extensive discovery, including document production "
        "of over 45,000 pages, depositions of twelve witnesses, and expert reports;")
    y += 4

    y = add_paragraph(page, 72, y,
        "WHEREAS, on 2024-02-28, the Parties participated in a full-day mediation session before "
        "the Honorable Robert K. Tanaka (Ret.) and reached a framework for settlement;")
    y += 4

    y = add_paragraph(page, 72, y,
        "WHEREAS, the Parties wish to resolve all disputes, claims, and counterclaims between "
        "them without further litigation, and each Party has been advised by independent legal "
        "counsel regarding the terms and conditions of this Agreement;")
    y += 8

    y = add_text(page, 72, y, "II. DEFINITIONS", fontsize=14, bold=True)
    y += 8

    y = add_paragraph(page, 72, y,
        "2.1 \"Effective Date\" means the date this Agreement is fully executed by both Parties, "
        "which shall be 2024-06-15.")
    y += 4

    y = add_paragraph(page, 72, y,
        "2.2 \"Settlement Amount\" means the total sum of $1,250,000.00 (One Million Two Hundred "
        "Fifty Thousand Dollars) to be paid by Meridian to Westbrook pursuant to the terms herein.")

    # =========================================================================
    # PAGE 3: Payment Terms
    # =========================================================================
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    y = 72
    y = add_text(page, 72, y, "III. SETTLEMENT PAYMENT", fontsize=14, bold=True)
    y += 8

    y = add_paragraph(page, 72, y,
        "3.1 Total Settlement Amount. In consideration of the mutual covenants and releases "
        "contained herein, Meridian shall pay Westbrook the total sum of $1,250,000.00 "
        "(the \"Settlement Amount\") according to the following schedule:")
    y += 4

    y = add_paragraph(page, 72, y,
        "    (a) First Installment: $500,000.00 due within thirty (30) calendar days of the "
        "Effective Date, payable no later than 2024-07-15;")
    y += 4

    y = add_paragraph(page, 72, y,
        "    (b) Second Installment: $375,000.00 due within ninety (90) calendar days of the "
        "Effective Date, payable no later than 2024-09-13;")
    y += 4

    y = add_paragraph(page, 72, y,
        "    (c) Third Installment: $375,000.00 due within one hundred eighty (180) calendar "
        "days of the Effective Date, payable no later than 2024-12-12.")
    y += 8

    y = add_paragraph(page, 72, y,
        "3.2 Method of Payment. All payments shall be made by wire transfer to the trust account "
        "of Westbrook's counsel, Morrison & Takahashi LLP, at Silicon Valley Bank, Account "
        "No. XXXXX-4892, Routing No. XXXXX-6731.")
    y += 4

    y = add_paragraph(page, 72, y,
        "3.3 Late Payment. In the event any installment is not received within ten (10) business "
        "days of its due date, interest shall accrue at the rate of 8% per annum on the unpaid "
        "balance, and Westbrook shall be entitled to accelerate all remaining payments.")
    y += 4

    y = add_paragraph(page, 72, y,
        "3.4 Tax Obligations. Each Party shall be solely responsible for its own tax obligations "
        "arising from this Agreement. Meridian shall issue an IRS Form 1099 to Westbrook for "
        "the Settlement Amount.")

    # =========================================================================
    # PAGE 4: Intellectual Property Terms
    # =========================================================================
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    y = 72
    y = add_text(page, 72, y, "IV. INTELLECTUAL PROPERTY PROVISIONS", fontsize=14, bold=True)
    y += 8

    y = add_paragraph(page, 72, y,
        "4.1 License Grant. Effective upon receipt of the First Installment, Westbrook hereby "
        "grants Meridian a non-exclusive, non-transferable, royalty-free license to use the "
        "DataSync Platform software (Version 3.2 and earlier) solely for Meridian's internal "
        "business operations. This license does not extend to any derivative works, sublicensing, "
        "or commercial redistribution of the software.")
    y += 4

    y = add_paragraph(page, 72, y,
        "4.2 Ownership. Westbrook retains all right, title, and interest in and to the DataSync "
        "Platform, including all intellectual property rights therein. Nothing in this Agreement "
        "shall be construed as transferring any ownership rights to Meridian.")
    y += 4

    y = add_paragraph(page, 72, y,
        "4.3 Return of Materials. Within fourteen (14) days of the Effective Date, Meridian "
        "shall return or certify the destruction of all proprietary materials, source code, "
        "documentation, and confidential information belonging to Westbrook, except as expressly "
        "permitted under the license granted in Section 4.1.")
    y += 4

    y = add_paragraph(page, 72, y,
        "4.4 Non-Compete. For a period of twenty-four (24) months following the Effective Date, "
        "Meridian shall not develop, market, or distribute any software product that directly "
        "competes with the DataSync Platform in the enterprise data synchronization market. "
        "The Parties acknowledge that $50,000.00 of the Settlement Amount constitutes "
        "consideration for this non-compete obligation.")

    # =========================================================================
    # PAGE 5: Confidentiality
    # =========================================================================
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    y = 72
    y = add_text(page, 72, y, "V. CONFIDENTIALITY", fontsize=14, bold=True)
    y += 8

    y = add_paragraph(page, 72, y,
        "5.1 Confidential Information. The terms and conditions of this Agreement, including "
        "the Settlement Amount and all payment terms, shall be treated as strictly confidential "
        "by both Parties. Neither Party shall disclose any terms of this Agreement to any third "
        "party, except as required by law, regulation, or court order, or to their respective "
        "attorneys, accountants, tax advisors, and insurers on a need-to-know basis.")
    y += 4

    y = add_paragraph(page, 72, y,
        "5.2 Public Statements. In the event either Party is asked about the litigation or its "
        "resolution, the only permitted response shall be: \"The matter has been resolved to the "
        "mutual satisfaction of both parties.\" No further comment or elaboration is permitted.")
    y += 4

    y = add_paragraph(page, 72, y,
        "5.3 Remedies for Breach. In the event of a breach of this confidentiality provision, "
        "the non-breaching Party shall be entitled to injunctive relief and liquidated damages "
        "in the amount of $75,000.00 per occurrence, in addition to any other remedies available "
        "at law or in equity.")
    y += 4

    y = add_paragraph(page, 72, y,
        "5.4 Duration. The confidentiality obligations set forth in this Section V shall survive "
        "the termination or expiration of this Agreement and shall remain in effect for a period "
        "of five (5) years from the Effective Date.")

    # =========================================================================
    # PAGE 6: Mutual Release
    # =========================================================================
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    y = 72
    y = add_text(page, 72, y, "VI. MUTUAL RELEASE OF CLAIMS", fontsize=14, bold=True)
    y += 8

    y = add_paragraph(page, 72, y,
        "6.1 Release by Westbrook. Upon receipt of the full Settlement Amount, Westbrook, on "
        "behalf of itself, its officers, directors, employees, agents, successors, and assigns, "
        "hereby fully and forever releases and discharges Meridian and its officers, directors, "
        "members, managers, employees, agents, successors, and assigns from any and all claims, "
        "demands, causes of action, obligations, damages, and liabilities of any kind or nature "
        "whatsoever, whether known or unknown, suspected or unsuspected, that arose or could have "
        "arisen from the facts alleged in Case No. 2024-CV-08923.")
    y += 4

    y = add_paragraph(page, 72, y,
        "6.2 Release by Meridian. Upon execution of this Agreement, Meridian, on behalf of "
        "itself, its members, managers, officers, employees, agents, successors, and assigns, "
        "hereby fully and forever releases and discharges Westbrook and its officers, directors, "
        "employees, agents, successors, and assigns from any and all claims, demands, causes of "
        "action, obligations, damages, and liabilities of any kind or nature whatsoever, whether "
        "known or unknown, suspected or unsuspected, that arose or could have arisen from the "
        "facts alleged in the counterclaims filed in Case No. 2024-CV-08923.")
    y += 4

    y = add_paragraph(page, 72, y,
        "6.3 California Civil Code Section 1542 Waiver. Each Party expressly waives and "
        "relinquishes all rights and benefits under Section 1542 of the California Civil Code, "
        "which provides: \"A general release does not extend to claims that the creditor or "
        "releasing party does not know or suspect to exist in his or her favor at the time of "
        "executing the release and that, if known by him or her, would have materially affected "
        "his or her settlement with the debtor or released party.\"")

    # =========================================================================
    # PAGE 7: Representations and Warranties
    # =========================================================================
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    y = 72
    y = add_text(page, 72, y, "VII. REPRESENTATIONS AND WARRANTIES", fontsize=14, bold=True)
    y += 8

    y = add_paragraph(page, 72, y,
        "7.1 Authority. Each Party represents and warrants that it has the full legal authority "
        "and capacity to enter into this Agreement and to perform its obligations hereunder. "
        "Each person signing this Agreement represents that he or she is duly authorized to "
        "execute this Agreement on behalf of the respective Party.")
    y += 4

    y = add_paragraph(page, 72, y,
        "7.2 No Assignment. Each Party represents and warrants that it has not assigned, "
        "transferred, or encumbered any of the claims or causes of action released herein, "
        "and that no other person or entity has any interest in such claims.")
    y += 4

    y = add_paragraph(page, 72, y,
        "7.3 Voluntary Agreement. Each Party acknowledges that this Agreement is entered into "
        "voluntarily, without duress or undue influence, and that each Party has had the "
        "opportunity to consult with independent legal counsel of its choosing.")
    y += 4

    y = add_paragraph(page, 72, y,
        "7.4 Financial Capacity. Meridian represents and warrants that it has sufficient "
        "financial resources and liquidity to satisfy all payment obligations under this "
        "Agreement. Meridian's current operating budget allocates $2,100,000.00 for legal "
        "settlements and contingencies for the fiscal year ending 2024-12-31.")

    # =========================================================================
    # PAGE 8: Dispute Resolution
    # =========================================================================
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    y = 72
    y = add_text(page, 72, y, "VIII. DISPUTE RESOLUTION", fontsize=14, bold=True)
    y += 8

    y = add_paragraph(page, 72, y,
        "8.1 Mediation. In the event of any dispute arising out of or relating to this "
        "Agreement, the Parties shall first attempt to resolve such dispute through mediation "
        "conducted by JAMS in San Jose, California. The mediator shall be selected by mutual "
        "agreement or, failing agreement, by JAMS. The cost of mediation shall be shared "
        "equally by the Parties. Mediation fees are estimated at $15,000.00 per session.")
    y += 4

    y = add_paragraph(page, 72, y,
        "8.2 Arbitration. If mediation fails to resolve the dispute within sixty (60) days, "
        "the dispute shall be submitted to binding arbitration under the rules of JAMS. The "
        "arbitration shall be conducted by a single arbitrator in San Jose, California. The "
        "arbitrator's decision shall be final and binding, and judgment thereon may be entered "
        "in any court of competent jurisdiction.")
    y += 4

    y = add_paragraph(page, 72, y,
        "8.3 Attorneys' Fees. In any mediation, arbitration, or litigation to enforce this "
        "Agreement, the prevailing Party shall be entitled to recover its reasonable attorneys' "
        "fees and costs, not to exceed $25,000.00.")

    # =========================================================================
    # PAGE 9: Non-Disparagement and Cooperation
    # =========================================================================
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    y = 72
    y = add_text(page, 72, y, "IX. NON-DISPARAGEMENT AND COOPERATION", fontsize=14, bold=True)
    y += 8

    y = add_paragraph(page, 72, y,
        "9.1 Non-Disparagement. Each Party agrees not to make any disparaging, defamatory, "
        "or derogatory statements about the other Party, its officers, directors, employees, "
        "products, or services, whether orally, in writing, or through electronic media.")
    y += 4

    y = add_paragraph(page, 72, y,
        "9.2 Cooperation. The Parties agree to cooperate fully in the implementation of this "
        "Agreement, including executing any additional documents reasonably necessary to "
        "effectuate the terms hereof. Each Party shall bear its own costs of cooperation.")
    y += 4

    y = add_paragraph(page, 72, y,
        "9.3 Dismissal of Action. Within five (5) business days of receipt of the First "
        "Installment payment of $500,000.00, the Parties shall file a joint stipulation to "
        "dismiss Case No. 2024-CV-08923 with prejudice, with each Party bearing its own costs "
        "and attorneys' fees.")

    # =========================================================================
    # PAGE 10: General Provisions
    # =========================================================================
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    y = 72
    y = add_text(page, 72, y, "X. GENERAL PROVISIONS", fontsize=14, bold=True)
    y += 8

    y = add_paragraph(page, 72, y,
        "10.1 Entire Agreement. This Agreement constitutes the entire agreement between the "
        "Parties with respect to the subject matter hereof and supersedes all prior negotiations, "
        "representations, warranties, commitments, offers, and agreements, whether written or "
        "oral, relating to such subject matter.")
    y += 4

    y = add_paragraph(page, 72, y,
        "10.2 Amendments. This Agreement may not be amended, modified, or supplemented except "
        "by a written instrument executed by both Parties.")
    y += 4

    y = add_paragraph(page, 72, y,
        "10.3 Governing Law. This Agreement shall be governed by and construed in accordance "
        "with the laws of the State of California, without regard to its conflicts of law "
        "principles.")
    y += 4

    y = add_paragraph(page, 72, y,
        "10.4 Severability. If any provision of this Agreement is held to be invalid, illegal, "
        "or unenforceable, the remaining provisions shall continue in full force and effect.")
    y += 4

    y = add_paragraph(page, 72, y,
        "10.5 Counterparts. This Agreement may be executed in counterparts, each of which shall "
        "be deemed an original, and all of which together shall constitute one and the same "
        "instrument. Facsimile and electronic signatures shall be deemed original signatures.")
    y += 4

    y = add_paragraph(page, 72, y,
        "10.6 Notices. All notices required under this Agreement shall be delivered via "
        "certified mail or overnight courier to the addresses set forth below. Notice fees "
        "and costs estimated at $150.00 per delivery shall be borne by the sending Party.")

    # =========================================================================
    # PAGE 11: Additional Terms and Exhibits Reference
    # =========================================================================
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    y = 72
    y = add_text(page, 72, y, "XI. ADDITIONAL TERMS", fontsize=14, bold=True)
    y += 8

    y = add_paragraph(page, 72, y,
        "11.1 Insurance. Meridian represents that it maintains errors and omissions insurance "
        "with coverage of $5,000,000.00 per occurrence through National Indemnity Corporation, "
        "Policy No. EO-2024-88431, effective through 2025-03-31.")
    y += 4

    y = add_paragraph(page, 72, y,
        "11.2 Indemnification. Each Party agrees to indemnify, defend, and hold harmless the "
        "other Party from and against any claims, losses, damages, liabilities, and expenses "
        "(including reasonable attorneys' fees) arising from any breach of this Agreement.")
    y += 4

    y = add_paragraph(page, 72, y,
        "11.3 Force Majeure. Neither Party shall be liable for any delay or failure to perform "
        "its obligations under this Agreement to the extent that such delay or failure is caused "
        "by circumstances beyond its reasonable control, including acts of God, war, terrorism, "
        "pandemic, government action, or natural disaster.")
    y += 4

    y = add_paragraph(page, 72, y,
        "11.4 Exhibits. The following exhibits are attached hereto and incorporated herein by "
        "reference:")
    y += 4

    y = add_paragraph(page, 72, y,
        "    Exhibit A: Software License Agreement dated 2022-08-10")
    y = add_paragraph(page, 72, y,
        "    Exhibit B: Payment Schedule and Wire Transfer Instructions")
    y = add_paragraph(page, 72, y,
        "    Exhibit C: List of Proprietary Materials to be Returned")

    # =========================================================================
    # PAGE 12: Signature Page
    # =========================================================================
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    y = 72
    y = add_text(page, 72, y, "XII. EXECUTION", fontsize=14, bold=True)
    y += 8

    y = add_paragraph(page, 72, y,
        "IN WITNESS WHEREOF, the Parties have executed this Settlement Agreement and Mutual "
        "Release as of the date first written above.")
    y += 20

    y = add_text(page, 72, y, "WESTBROOK TECHNOLOGIES, INC.", fontsize=12, bold=True)
    y += 30
    page.draw_line(pymupdf.Point(72, y), pymupdf.Point(300, y), color=(0, 0, 0), width=0.5)
    y += 4
    y = add_text(page, 72, y, "By: Patricia L. Westbrook", fontsize=11)
    y = add_text(page, 72, y, "Title: Chief Executive Officer", fontsize=11)
    y = add_text(page, 72, y, "Date: 2024-06-15", fontsize=11)
    y += 30

    y = add_text(page, 72, y, "MERIDIAN SOLUTIONS GROUP, LLC", fontsize=12, bold=True)
    y += 30
    page.draw_line(pymupdf.Point(72, y), pymupdf.Point(300, y), color=(0, 0, 0), width=0.5)
    y += 4
    y = add_text(page, 72, y, "By: James R. Nakamura", fontsize=11)
    y = add_text(page, 72, y, "Title: Managing Partner", fontsize=11)
    y = add_text(page, 72, y, "Date: 2024-06-15", fontsize=11)
    y += 30

    y = add_text(page, 72, y, "APPROVED AS TO FORM:", fontsize=12, bold=True)
    y += 20
    page.draw_line(pymupdf.Point(72, y), pymupdf.Point(300, y), color=(0, 0, 0), width=0.5)
    y += 4
    y = add_text(page, 72, y, "Morrison & Takahashi LLP", fontsize=11)
    y = add_text(page, 72, y, "Counsel for Westbrook Technologies, Inc.", fontsize=11)
    y += 20
    page.draw_line(pymupdf.Point(72, y), pymupdf.Point(300, y), color=(0, 0, 0), width=0.5)
    y += 4
    y = add_text(page, 72, y, "Chen, Alvarez & Partners", fontsize=11)
    y = add_text(page, 72, y, "Counsel for Meridian Solutions Group, LLC", fontsize=11)

    # Add page numbers to all pages
    for i, pg in enumerate(doc):
        pg.insert_text(
            pymupdf.Point(306, 780),
            f"- {i + 1} -",
            fontsize=9,
            fontname="tiro",
            color=(0.4, 0.4, 0.4),
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 12')

    # GUI-ready: open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
