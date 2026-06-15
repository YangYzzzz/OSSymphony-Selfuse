"""
Initial Setup: Create an 8-page proposed settlement PDF with sensitive financial terms
Task ID: pdf_legal_060
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_060'
LEGAL_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{LEGAL_DIR}/proposed_settlement.pdf'


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


def add_page_header_footer(page, page_num, total_pages):
    """Add consistent header and footer to each page."""
    w = page.rect.width
    h = page.rect.height
    # Header line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 60), pymupdf.Point(w - 72, 60))
    shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
    shape.commit()
    # Header text
    page.insert_text(pymupdf.Point(72, 52), "PROPOSED SETTLEMENT AGREEMENT",
                     fontsize=8, fontname="hebo", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(w - 200, 52), "CONFIDENTIAL",
                     fontsize=8, fontname="hebo", color=(0.8, 0, 0))
    # Footer
    page.insert_text(pymupdf.Point(72, h - 30),
                     f"Page {page_num} of {total_pages}",
                     fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(w - 250, h - 30),
                     "Case No. 2025-CV-04821 | Strictly Confidential",
                     fontsize=7, fontname="helv", color=(0.4, 0.4, 0.4))


def create_initial():
    os.makedirs(LEGAL_DIR, exist_ok=True)

    doc = pymupdf.open()
    W, H = 612, 792  # US Letter

    total_pages = 8

    # ============================================================
    # PAGE 1: Title / Cover Page
    # ============================================================
    p1 = doc.new_page(width=W, height=H)
    add_page_header_footer(p1, 1, total_pages)

    p1.insert_text(pymupdf.Point(170, 140), "PROPOSED SETTLEMENT AGREEMENT",
                   fontsize=18, fontname="hebo", color=(0, 0, 0))
    p1.insert_text(pymupdf.Point(230, 170), "AND MUTUAL RELEASE",
                   fontsize=14, fontname="hebo", color=(0, 0, 0))

    cover_text = [
        ("Case No.", "2025-CV-04821"),
        ("Court", "Superior Court of the State of California"),
        ("County", "Los Angeles County"),
        ("Filed", "January 14, 2025"),
        ("", ""),
        ("Plaintiff Name", "v."),
        ("", "Meridian Healthcare Systems, Inc."),
        ("", "(Defendant)"),
    ]
    y = 230
    for label, value in cover_text:
        if label:
            p1.insert_text(pymupdf.Point(150, y), f"{label}:", fontsize=11, fontname="hebo", color=(0, 0, 0))
            p1.insert_text(pymupdf.Point(300, y), value, fontsize=11, fontname="helv", color=(0, 0, 0))
        else:
            p1.insert_text(pymupdf.Point(200, y), value, fontsize=11, fontname="helv", color=(0, 0, 0))
        y += 22

    p1.insert_text(pymupdf.Point(72, 500),
                   "This Settlement Agreement and Mutual Release (\"Agreement\") is entered into",
                   fontsize=10, fontname="helv", color=(0, 0, 0))
    p1.insert_text(pymupdf.Point(72, 515),
                   "by and between Plaintiff Name (\"Plaintiff\") and Meridian Healthcare",
                   fontsize=10, fontname="helv", color=(0, 0, 0))
    p1.insert_text(pymupdf.Point(72, 530),
                   "Systems, Inc. (\"Defendant\"), collectively referred to as the \"Parties.\"",
                   fontsize=10, fontname="helv", color=(0, 0, 0))

    p1.insert_text(pymupdf.Point(72, 570),
                   "WHEREAS, Plaintiff Name filed a complaint alleging wrongful termination,",
                   fontsize=10, fontname="helv", color=(0, 0, 0))
    p1.insert_text(pymupdf.Point(72, 585),
                   "discrimination, and retaliation in violation of state and federal employment laws;",
                   fontsize=10, fontname="helv", color=(0, 0, 0))

    p1.insert_text(pymupdf.Point(72, 620),
                   "WHEREAS, Defendant denies all allegations and liability but wishes to avoid",
                   fontsize=10, fontname="helv", color=(0, 0, 0))
    p1.insert_text(pymupdf.Point(72, 635),
                   "the expense and uncertainty of prolonged litigation;",
                   fontsize=10, fontname="helv", color=(0, 0, 0))

    p1.insert_text(pymupdf.Point(72, 670),
                   "NOW, THEREFORE, in consideration of the mutual promises and covenants",
                   fontsize=10, fontname="helv", color=(0, 0, 0))
    p1.insert_text(pymupdf.Point(72, 685),
                   "contained herein, and for other good and valuable consideration, the receipt",
                   fontsize=10, fontname="helv", color=(0, 0, 0))
    p1.insert_text(pymupdf.Point(72, 700),
                   "and sufficiency of which are hereby acknowledged, the Parties agree as follows:",
                   fontsize=10, fontname="helv", color=(0, 0, 0))

    # ============================================================
    # PAGE 2: Financial Terms (contains dollar amounts to redact)
    # ============================================================
    p2 = doc.new_page(width=W, height=H)
    add_page_header_footer(p2, 2, total_pages)

    p2.insert_text(pymupdf.Point(72, 90), "ARTICLE I: SETTLEMENT PAYMENT AND FINANCIAL TERMS",
                   fontsize=13, fontname="hebo", color=(0, 0, 0))

    financial_lines = [
        "1.1  Settlement Amount. Defendant shall pay to Plaintiff Name a total",
        "settlement amount of $2,750,000.00 (Two Million Seven Hundred Fifty",
        "Thousand Dollars) (the \"Settlement Amount\"), allocated as follows:",
        "",
        "     (a) Compensatory Damages: $1,500,000.00 for alleged emotional",
        "         distress and lost wages sustained by Plaintiff Name;",
        "",
        "     (b) Back Pay: $475,000.00 representing estimated lost wages and",
        "         benefits from the date of termination through the date of",
        "         this Agreement;",
        "",
        "     (c) Front Pay: $325,000.00 representing estimated future lost",
        "         wages and diminished earning capacity;",
        "",
        "     (d) Attorney Fees and Costs: $450,000.00 payable directly to",
        "         the law firm of Chen & Associates, LLP, representing",
        "         Plaintiff Name in this matter.",
        "",
        "1.2  Payment Schedule. The Settlement Amount shall be paid as follows:",
        "",
        "     (a) Initial Payment: $1,375,000.00 within thirty (30) calendar",
        "         days of the Effective Date;",
        "",
        "     (b) Second Installment: $825,000.00 within ninety (90) calendar",
        "         days of the Effective Date;",
        "",
        "     (c) Final Installment: $550,000.00 within one hundred eighty",
        "         (180) calendar days of the Effective Date.",
        "",
        "1.3  Tax Obligations. Plaintiff Name acknowledges and agrees that",
        "Plaintiff Name shall be solely responsible for payment of any and all",
        "federal, state, and local taxes arising from receipt of the Settlement",
        "Amount. Defendant shall issue a Form 1099 for the sum of $1,250,000.00",
        "and a Form W-2 for the sum of $1,500,000.00.",
        "",
        "1.4  Late Payment Penalty. In the event any installment is not paid",
        "within the time specified, a late penalty of $15,000.00 per business",
        "day shall accrue until payment is made in full.",
    ]

    y = 120
    for line in financial_lines:
        if line:
            p2.insert_text(pymupdf.Point(72, y), line, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 15

    # ============================================================
    # PAGE 3: Settlement Terms (paragraph at (72,300)-(540,400) to redact)
    # ============================================================
    p3 = doc.new_page(width=W, height=H)
    add_page_header_footer(p3, 3, total_pages)

    p3.insert_text(pymupdf.Point(72, 90), "ARTICLE II: RELEASE AND DISCHARGE",
                   fontsize=13, fontname="hebo", color=(0, 0, 0))

    pre_para = [
        "2.1  General Release by Plaintiff. In consideration of the Settlement",
        "Amount and other good and valuable consideration set forth herein,",
        "Plaintiff Name, on behalf of Plaintiff Name and Plaintiff Name's heirs,",
        "executors, administrators, successors, and assigns, hereby fully and",
        "forever releases and discharges Defendant, its officers, directors,",
        "employees, agents, affiliates, subsidiaries, parent companies,",
        "predecessors, successors, and assigns from any and all claims, demands,",
        "damages, debts, liabilities, accounts, reckonings, obligations, costs,",
        "expenses, liens, actions, and causes of action of every kind and nature.",
        "",
        "2.2  Scope of Release. The release set forth in Section 2.1 includes",
        "but is not limited to the following:",
    ]

    y = 120
    for line in pre_para:
        if line:
            p3.insert_text(pymupdf.Point(72, y), line, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 15

    # The paragraph that should be at approx (72, 300) to (540, 400) on page 3
    # containing settlement terms to be redacted
    settlement_terms_lines = [
        "     The specific terms negotiated between Plaintiff Name and Defendant",
        "     include: (i) a non-compete restriction of twenty-four (24) months",
        "     within the Greater Los Angeles metropolitan area; (ii) mutual",
        "     non-disparagement obligations extending for a period of five (5)",
        "     years from the Effective Date; (iii) a structured payout contingent",
        "     upon Plaintiff Name's compliance with the confidentiality provisions",
        "     set forth in Article IV; and (iv) Defendant's agreement to provide",
    ]

    y = 305
    for line in settlement_terms_lines:
        p3.insert_text(pymupdf.Point(72, y), line, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 14

    post_para = [
        "",
        "     a neutral employment reference for Plaintiff Name confirming dates",
        "     of employment and final job title only.",
        "",
        "2.3  Release by Defendant. Defendant, on behalf of itself, its officers,",
        "directors, employees, agents, and successors, hereby fully and forever",
        "releases Plaintiff Name from any and all claims arising from or related",
        "to Plaintiff Name's employment with Defendant.",
    ]

    y = 410
    for line in post_para:
        if line:
            p3.insert_text(pymupdf.Point(72, y), line, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 15

    # ============================================================
    # PAGE 4: Confidentiality Provisions
    # ============================================================
    p4 = doc.new_page(width=W, height=H)
    add_page_header_footer(p4, 4, total_pages)

    p4.insert_text(pymupdf.Point(72, 90), "ARTICLE III: CONFIDENTIALITY",
                   fontsize=13, fontname="hebo", color=(0, 0, 0))

    conf_lines = [
        "3.1  Confidentiality Obligations. The Parties agree that the terms",
        "and conditions of this Agreement, including the Settlement Amount,",
        "shall be kept strictly confidential. Neither Plaintiff Name nor",
        "Defendant shall disclose any terms of this Agreement to any third",
        "party, except as follows:",
        "",
        "     (a) to their respective attorneys, accountants, tax advisors,",
        "         and financial advisors who have a need to know;",
        "",
        "     (b) to immediate family members of Plaintiff Name, provided such",
        "         family members agree to maintain confidentiality;",
        "",
        "     (c) as required by law, regulation, or valid court order;",
        "",
        "     (d) to any government agency to which disclosure is required.",
        "",
        "3.2  Breach of Confidentiality. In the event of a breach of this",
        "confidentiality provision by Plaintiff Name, Defendant shall be",
        "entitled to recover liquidated damages in the amount of $100,000.00",
        "per occurrence, in addition to any other remedies available at law",
        "or in equity.",
        "",
        "3.3  Public Statements. Neither Party shall make any public statement",
        "regarding this Agreement or the underlying dispute. If asked about",
        "the matter, each Party shall state only that \"the matter has been",
        "resolved to the mutual satisfaction of the Parties.\"",
        "",
        "3.4  Social Media. Plaintiff Name agrees not to post, share, or",
        "otherwise disseminate on any social media platform any information",
        "regarding the terms of this Agreement, the litigation, or any",
        "negative statements about Defendant, its employees, or its products.",
    ]

    y = 120
    for line in conf_lines:
        if line:
            p4.insert_text(pymupdf.Point(72, y), line, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 15

    # ============================================================
    # PAGE 5: Non-Disparagement and Cooperation
    # ============================================================
    p5 = doc.new_page(width=W, height=H)
    add_page_header_footer(p5, 5, total_pages)

    p5.insert_text(pymupdf.Point(72, 90), "ARTICLE IV: NON-DISPARAGEMENT AND COOPERATION",
                   fontsize=13, fontname="hebo", color=(0, 0, 0))

    nd_lines = [
        "4.1  Non-Disparagement by Plaintiff. Plaintiff Name agrees not to",
        "make any disparaging, defamatory, or negative statements, whether",
        "oral, written, or electronic, about Defendant, its officers,",
        "directors, employees, products, services, or business practices.",
        "",
        "4.2  Non-Disparagement by Defendant. Defendant agrees not to make",
        "any disparaging statements about Plaintiff Name, Plaintiff Name's",
        "work performance, or the circumstances of Plaintiff Name's departure",
        "from Defendant's employ.",
        "",
        "4.3  Cooperation. Plaintiff Name agrees to cooperate with Defendant",
        "in any ongoing or future litigation, regulatory proceedings, or",
        "investigations related to matters within Plaintiff Name's knowledge",
        "during the course of employment. Defendant shall reimburse Plaintiff",
        "Name for reasonable out-of-pocket expenses incurred in connection",
        "with such cooperation.",
        "",
        "4.4  Return of Property. Plaintiff Name represents and warrants that",
        "Plaintiff Name has returned all property belonging to Defendant,",
        "including but not limited to laptops, mobile devices, access badges,",
        "documents, and any copies thereof, whether in physical or electronic",
        "form.",
        "",
        "4.5  Non-Solicitation. For a period of twelve (12) months following",
        "the Effective Date, Plaintiff Name shall not directly or indirectly",
        "solicit, recruit, or attempt to hire any employee or contractor of",
        "Defendant.",
    ]

    y = 120
    for line in nd_lines:
        if line:
            p5.insert_text(pymupdf.Point(72, y), line, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 15

    # ============================================================
    # PAGE 6: Representations and Warranties
    # ============================================================
    p6 = doc.new_page(width=W, height=H)
    add_page_header_footer(p6, 6, total_pages)

    p6.insert_text(pymupdf.Point(72, 90), "ARTICLE V: REPRESENTATIONS AND WARRANTIES",
                   fontsize=13, fontname="hebo", color=(0, 0, 0))

    rw_lines = [
        "5.1  Authority. Each Party represents and warrants that it has full",
        "power and authority to enter into this Agreement and to perform its",
        "obligations hereunder.",
        "",
        "5.2  Voluntary Execution. Plaintiff Name represents and warrants",
        "that Plaintiff Name has read this Agreement in its entirety, has",
        "had the opportunity to consult with legal counsel of Plaintiff Name's",
        "choosing, and enters into this Agreement voluntarily and without",
        "coercion or duress.",
        "",
        "5.3  No Assignment. Plaintiff Name represents and warrants that",
        "Plaintiff Name has not assigned, transferred, or conveyed any claims",
        "or causes of action released herein to any other person or entity.",
        "",
        "5.4  No Pending Claims. Plaintiff Name represents and warrants that",
        "there are no pending complaints, charges, or claims filed by or on",
        "behalf of Plaintiff Name against Defendant with any court, agency,",
        "or other tribunal, other than the action identified herein.",
        "",
        "5.5  Medicare Disclaimer. Plaintiff Name represents and warrants that",
        "Plaintiff Name is not a Medicare beneficiary as of the date of this",
        "Agreement and has no reasonable expectation of becoming a Medicare",
        "beneficiary within the next thirty (30) months.",
    ]

    y = 120
    for line in rw_lines:
        if line:
            p6.insert_text(pymupdf.Point(72, y), line, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 15

    # ============================================================
    # PAGE 7: General Provisions
    # ============================================================
    p7 = doc.new_page(width=W, height=H)
    add_page_header_footer(p7, 7, total_pages)

    p7.insert_text(pymupdf.Point(72, 90), "ARTICLE VI: GENERAL PROVISIONS",
                   fontsize=13, fontname="hebo", color=(0, 0, 0))

    gp_lines = [
        "6.1  Governing Law. This Agreement shall be governed by and construed",
        "in accordance with the laws of the State of California, without regard",
        "to its conflict of laws provisions.",
        "",
        "6.2  Entire Agreement. This Agreement constitutes the entire agreement",
        "between the Parties with respect to the subject matter hereof and",
        "supersedes all prior negotiations, representations, warranties,",
        "commitments, offers, and agreements, whether written or oral.",
        "",
        "6.3  Amendments. This Agreement may not be modified, amended, or",
        "supplemented except by a written instrument signed by both Parties.",
        "",
        "6.4  Severability. If any provision of this Agreement is held to be",
        "invalid, illegal, or unenforceable, the remaining provisions shall",
        "continue in full force and effect.",
        "",
        "6.5  Counterparts. This Agreement may be executed in counterparts,",
        "each of which shall be deemed an original, and all of which together",
        "shall constitute one and the same instrument.",
        "",
        "6.6  Notices. All notices under this Agreement shall be in writing",
        "and delivered to the addresses set forth in the signature blocks below,",
        "or to such other address as a Party may designate in writing.",
        "",
        "6.7  Waiver. The failure of either Party to enforce any provision of",
        "this Agreement shall not be deemed a waiver of that Party's right to",
        "enforce that or any other provision in the future.",
        "",
        "6.8  Dispute Resolution. Any dispute arising under this Agreement",
        "shall be resolved through binding arbitration administered by JAMS",
        "in Los Angeles, California, in accordance with its Comprehensive",
        "Arbitration Rules and Procedures.",
    ]

    y = 120
    for line in gp_lines:
        if line:
            p7.insert_text(pymupdf.Point(72, y), line, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 15

    # ============================================================
    # PAGE 8: Signature Page
    # ============================================================
    p8 = doc.new_page(width=W, height=H)
    add_page_header_footer(p8, 8, total_pages)

    p8.insert_text(pymupdf.Point(72, 90), "ARTICLE VII: EXECUTION",
                   fontsize=13, fontname="hebo", color=(0, 0, 0))

    p8.insert_text(pymupdf.Point(72, 130),
                   "IN WITNESS WHEREOF, the Parties have executed this Agreement as of",
                   fontsize=10, fontname="helv", color=(0, 0, 0))
    p8.insert_text(pymupdf.Point(72, 145),
                   "the date last signed below (the \"Effective Date\").",
                   fontsize=10, fontname="helv", color=(0, 0, 0))

    # Plaintiff signature block
    p8.insert_text(pymupdf.Point(72, 200), "PLAINTIFF:", fontsize=11, fontname="hebo", color=(0, 0, 0))
    shape8 = p8.new_shape()
    shape8.draw_line(pymupdf.Point(72, 270), pymupdf.Point(300, 270))
    shape8.finish(color=(0, 0, 0), width=0.5)
    shape8.commit()
    p8.insert_text(pymupdf.Point(72, 285), "Plaintiff Name", fontsize=10, fontname="helv", color=(0, 0, 0))
    p8.insert_text(pymupdf.Point(72, 300), "Date: _______________", fontsize=10, fontname="helv", color=(0, 0, 0))

    # Defendant signature block
    p8.insert_text(pymupdf.Point(72, 370), "DEFENDANT:", fontsize=11, fontname="hebo", color=(0, 0, 0))
    p8.insert_text(pymupdf.Point(72, 390), "MERIDIAN HEALTHCARE SYSTEMS, INC.", fontsize=10, fontname="hebo", color=(0, 0, 0))
    shape8b = p8.new_shape()
    shape8b.draw_line(pymupdf.Point(72, 440), pymupdf.Point(300, 440))
    shape8b.finish(color=(0, 0, 0), width=0.5)
    shape8b.commit()
    p8.insert_text(pymupdf.Point(72, 455), "By: Victoria Harrington, Chief Legal Officer",
                   fontsize=10, fontname="helv", color=(0, 0, 0))
    p8.insert_text(pymupdf.Point(72, 470), "Date: _______________", fontsize=10, fontname="helv", color=(0, 0, 0))

    # Approved as to form
    p8.insert_text(pymupdf.Point(72, 530), "APPROVED AS TO FORM:", fontsize=11, fontname="hebo", color=(0, 0, 0))

    shape8c = p8.new_shape()
    shape8c.draw_line(pymupdf.Point(72, 590), pymupdf.Point(300, 590))
    shape8c.finish(color=(0, 0, 0), width=0.5)
    shape8c.commit()
    p8.insert_text(pymupdf.Point(72, 605), "Rachel Chen, Esq.", fontsize=10, fontname="helv", color=(0, 0, 0))
    p8.insert_text(pymupdf.Point(72, 620), "Chen & Associates, LLP", fontsize=10, fontname="helv", color=(0, 0, 0))
    p8.insert_text(pymupdf.Point(72, 635), "Attorneys for Plaintiff Name", fontsize=10, fontname="helv", color=(0, 0, 0))

    shape8d = p8.new_shape()
    shape8d.draw_line(pymupdf.Point(320, 590), pymupdf.Point(540, 590))
    shape8d.finish(color=(0, 0, 0), width=0.5)
    shape8d.commit()
    p8.insert_text(pymupdf.Point(320, 605), "David Morrison, Esq.", fontsize=10, fontname="helv", color=(0, 0, 0))
    p8.insert_text(pymupdf.Point(320, 620), "Morrison & Whitfield, PLLC", fontsize=10, fontname="helv", color=(0, 0, 0))
    p8.insert_text(pymupdf.Point(320, 635), "Attorneys for Defendant", fontsize=10, fontname="helv", color=(0, 0, 0))

    # Set metadata
    doc.set_metadata({
        "title": "Proposed Settlement Agreement - Case No. 2025-CV-04821",
        "author": "Chen & Associates, LLP",
        "subject": "Settlement Agreement and Mutual Release",
        "keywords": "settlement, employment, confidential",
        "creator": "Legal Document System",
    })

    # Set table of contents
    toc = [
        [1, "Article I: Settlement Payment and Financial Terms", 2],
        [1, "Article II: Release and Discharge", 3],
        [1, "Article III: Confidentiality", 4],
        [1, "Article IV: Non-Disparagement and Cooperation", 5],
        [1, "Article V: Representations and Warranties", 6],
        [1, "Article VI: General Provisions", 7],
        [1, "Article VII: Execution", 8],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
