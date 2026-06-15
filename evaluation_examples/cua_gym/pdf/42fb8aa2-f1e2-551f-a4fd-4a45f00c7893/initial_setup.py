"""
Initial Setup: Create a 12-page unencrypted mediation brief PDF
Task ID: pdf_legal_063
Domain: pdf
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_063'
BRIEF_DIR = f'{WORKDIR}/legal/mediation'
OUTPUT = f'{BRIEF_DIR}/brief.pdf'

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


def add_header_footer(page, page_num, total_pages):
    """Add header and footer to each page."""
    # Header line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(54, 54), pymupdf.Point(W - 54, 54))
    shape.finish(color=(0.2, 0.2, 0.4), width=1.5)
    shape.commit()

    page.insert_text(
        pymupdf.Point(54, 46),
        "CONFIDENTIAL - MEDIATION BRIEF",
        fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4),
    )
    page.insert_text(
        pymupdf.Point(W - 200, 46),
        "Case No. 2024-MED-08271",
        fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4),
    )

    # Footer line
    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(54, H - 50), pymupdf.Point(W - 54, H - 50))
    shape2.finish(color=(0.2, 0.2, 0.4), width=1.0)
    shape2.commit()

    page.insert_text(
        pymupdf.Point(54, H - 38),
        "Raines & Whitfield LLP | Attorneys at Law",
        fontsize=8, fontname="heit", color=(0.4, 0.4, 0.4),
    )
    page.insert_text(
        pymupdf.Point(W - 100, H - 38),
        f"Page {page_num} of {total_pages}",
        fontsize=8, fontname="helv", color=(0.4, 0.4, 0.4),
    )


def create_initial():
    os.makedirs(BRIEF_DIR, exist_ok=True)

    doc = pymupdf.open()
    total_pages = 12
    content_rect = pymupdf.Rect(54, 72, W - 54, H - 60)

    # ========================
    # PAGE 1 - COVER PAGE
    # ========================
    page = doc.new_page(width=W, height=H)
    # Title block centered
    page.insert_text(pymupdf.Point(W / 2 - 140, 180),
                     "MEDIATION BRIEF", fontsize=28, fontname="hebo",
                     color=(0.1, 0.1, 0.3))
    page.insert_text(pymupdf.Point(W / 2 - 80, 220),
                     "CONFIDENTIAL", fontsize=14, fontname="hebo",
                     color=(0.6, 0.0, 0.0))

    # Case info
    cover_text = [
        ("BEFORE THE AMERICAN ARBITRATION ASSOCIATION", 280),
        ("CASE NO. 2024-MED-08271", 310),
        ("", 330),
        ("GREENFIELD TECHNOLOGIES, INC.", 370),
        ("Claimant,", 390),
        ("v.", 420),
        ("MERIDIAN CONSULTING GROUP, LLC", 450),
        ("Respondent.", 470),
        ("", 500),
        ("Prepared by:", 540),
        ("Raines & Whitfield LLP", 560),
        ("1200 Commerce Tower, Suite 3400", 578),
        ("San Francisco, California 94105", 596),
        ("Tel: (415) 555-0198", 614),
        ("", 640),
        ("Lead Counsel: Katherine A. Raines, Esq.", 660),
        ("Associate: David M. Chen, Esq.", 678),
        ("Date: March 15, 2024", 710),
    ]
    for text, y in cover_text:
        if text:
            fs = 12 if y < 500 else 11
            fn = "hebo" if y in (370, 450, 560) else "helv"
            page.insert_text(pymupdf.Point(W / 2 - 160, y), text,
                             fontsize=fs, fontname=fn, color=(0, 0, 0))
    add_header_footer(page, 1, total_pages)

    # ========================
    # PAGE 2 - TABLE OF CONTENTS
    # ========================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(54, 100), "TABLE OF CONTENTS",
                     fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.3))

    toc_items = [
        ("I.", "Introduction and Summary of Dispute", "3"),
        ("II.", "Background and Factual Summary", "4"),
        ("III.", "Claimant's Position and Key Arguments", "5"),
        ("IV.", "Respondent's Anticipated Position", "6"),
        ("V.", "Disputed Issues of Fact", "7"),
        ("VI.", "Disputed Issues of Law", "8"),
        ("VII.", "Prior Settlement Negotiations", "9"),
        ("VIII.", "Damages Analysis", "10"),
        ("IX.", "Settlement Framework and Proposal", "11"),
        ("X.", "Conclusion", "12"),
    ]
    y = 140
    for num, title, pg in toc_items:
        page.insert_text(pymupdf.Point(72, y), num, fontsize=11,
                         fontname="hebo", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(100, y), title, fontsize=11,
                         fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(W - 90, y), pg, fontsize=11,
                         fontname="helv", color=(0, 0, 0))
        y += 24
    add_header_footer(page, 2, total_pages)

    # ========================
    # PAGE 3 - INTRODUCTION
    # ========================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(54, 100),
                     "I. INTRODUCTION AND SUMMARY OF DISPUTE",
                     fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.3))
    intro_text = (
        "This mediation brief is submitted on behalf of Greenfield Technologies, Inc. "
        "(\"Claimant\" or \"Greenfield\") in connection with the above-captioned dispute "
        "against Meridian Consulting Group, LLC (\"Respondent\" or \"Meridian\"). This "
        "mediation is scheduled for April 22, 2024, before Mediator Hon. Patricia "
        "Watanabe (Ret.).\n\n"
        "The dispute arises from a Master Services Agreement (\"MSA\") dated June 1, 2022, "
        "under which Meridian agreed to provide enterprise software integration services "
        "to Greenfield for a fixed fee of $2,450,000. Greenfield alleges that Meridian "
        "materially breached the MSA by delivering a fundamentally defective integration "
        "platform that failed to meet the agreed-upon specifications, resulting in "
        "significant business losses, remediation costs, and reputational harm.\n\n"
        "Greenfield seeks total damages in the amount of $4,875,000, comprising direct "
        "damages of $2,450,000 (fees paid), consequential damages of $1,825,000 (lost "
        "revenue and additional IT costs), and remediation expenses of $600,000. "
        "Greenfield approaches this mediation in good faith and is prepared to engage "
        "in meaningful settlement discussions within a reasonable range."
    )
    page.insert_textbox(pymupdf.Rect(54, 120, W - 54, H - 70), intro_text,
                        fontsize=11, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)
    add_header_footer(page, 3, total_pages)

    # ========================
    # PAGE 4 - BACKGROUND
    # ========================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(54, 100),
                     "II. BACKGROUND AND FACTUAL SUMMARY",
                     fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.3))
    bg_text = (
        "Greenfield Technologies is a mid-size technology company headquartered in "
        "San Jose, California, specializing in cloud-based supply chain management "
        "solutions for the manufacturing sector. Founded in 2015, Greenfield employs "
        "approximately 340 people and reported annual revenue of $42 million in 2023.\n\n"
        "In early 2022, Greenfield initiated a comprehensive digital transformation "
        "project to modernize its legacy ERP system. After a competitive bidding "
        "process involving four qualified vendors, Greenfield selected Meridian "
        "Consulting Group to provide integration services. Meridian represented itself "
        "as having extensive experience with enterprise software integration, "
        "particularly with the SAP S/4HANA platform that Greenfield intended to deploy.\n\n"
        "The MSA was executed on June 1, 2022, with a project timeline of 14 months "
        "and a completion date of August 1, 2023. Key deliverables included: (1) full "
        "data migration from legacy systems; (2) custom API development for supply "
        "chain modules; (3) user acceptance testing across all business units; and "
        "(4) go-live support for 90 days post-deployment.\n\n"
        "Meridian assigned a project team of 12 consultants led by Senior Engagement "
        "Manager Robert Thornton. Initial project milestones were met through "
        "December 2022. However, beginning in January 2023, significant delays and "
        "technical deficiencies emerged, as described in detail below."
    )
    page.insert_textbox(pymupdf.Rect(54, 120, W - 54, H - 70), bg_text,
                        fontsize=11, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)
    add_header_footer(page, 4, total_pages)

    # ========================
    # PAGE 5 - CLAIMANT'S POSITION
    # ========================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(54, 100),
                     "III. CLAIMANT'S POSITION AND KEY ARGUMENTS",
                     fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.3))
    pos_text = (
        "Greenfield's position rests on three primary grounds:\n\n"
        "A. Material Breach of the MSA\n\n"
        "Meridian failed to deliver a functioning integration platform by the agreed "
        "deadline. The platform delivered on September 15, 2023 (six weeks late) "
        "contained 847 documented defects, of which 23 were classified as critical "
        "severity. The User Acceptance Testing (UAT) report dated October 3, 2023, "
        "documented a pass rate of only 61%, well below the contractual threshold "
        "of 95%.\n\n"
        "B. Failure to Provide Qualified Personnel\n\n"
        "Meridian replaced three key team members during the critical development "
        "phase (March-June 2023) without prior notice or client approval as required "
        "under Section 4.3 of the MSA. The replacement consultants lacked adequate "
        "SAP S/4HANA experience, resulting in fundamental architectural errors in the "
        "custom API layer.\n\n"
        "C. Misrepresentation of Capabilities\n\n"
        "During the pre-contract evaluation, Meridian represented that it had "
        "successfully completed seven comparable SAP integration projects. Greenfield "
        "has since discovered that only two of these projects were completed without "
        "significant disputes or litigation, and one resulted in a $1.2 million "
        "settlement payment by Meridian to the client."
    )
    page.insert_textbox(pymupdf.Rect(54, 120, W - 54, H - 70), pos_text,
                        fontsize=11, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)
    add_header_footer(page, 5, total_pages)

    # ========================
    # PAGE 6 - RESPONDENT'S ANTICIPATED POSITION
    # ========================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(54, 100),
                     "IV. RESPONDENT'S ANTICIPATED POSITION",
                     fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.3))
    resp_text = (
        "Based on correspondence and pre-mediation communications, Greenfield "
        "anticipates that Meridian will advance the following arguments:\n\n"
        "1. Scope Creep: Meridian contends that Greenfield submitted 47 change "
        "requests during the project, expanding the scope well beyond the original "
        "MSA specifications. Meridian claims these changes added an estimated "
        "$380,000 in unreimbursed costs and caused the timeline delays.\n\n"
        "2. Client-Side Delays: Meridian asserts that Greenfield's internal IT "
        "team failed to provide timely access to legacy systems and data, causing "
        "cumulative delays of approximately 8 weeks. Meridian has cited 14 instances "
        "of delayed data provisioning between February and May 2023.\n\n"
        "3. Substantial Performance: Meridian maintains that it substantially "
        "performed under the MSA and that the remaining defects were minor and "
        "correctable through standard warranty support. Meridian claims that 89% of "
        "the platform modules were functioning as of the October 2023 assessment.\n\n"
        "4. Limitation of Liability: Meridian will likely invoke Section 9.2 of the "
        "MSA, which caps consequential damages at the total contract value of "
        "$2,450,000."
    )
    page.insert_textbox(pymupdf.Rect(54, 120, W - 54, H - 70), resp_text,
                        fontsize=11, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)
    add_header_footer(page, 6, total_pages)

    # ========================
    # PAGE 7 - DISPUTED ISSUES OF FACT
    # ========================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(54, 100),
                     "V. DISPUTED ISSUES OF FACT",
                     fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.3))
    fact_text = (
        "The parties disagree on the following material facts:\n\n"
        "1. Root Cause of Defects: Greenfield contends the defects arose from "
        "Meridian's inadequate architecture design and unqualified personnel. "
        "Meridian attributes the defects to specification changes and data quality "
        "issues on Greenfield's side.\n\n"
        "2. Change Request Impact: Greenfield maintains that the 47 change requests "
        "were minor clarifications within the original scope. Meridian characterizes "
        "them as material scope expansions totaling approximately 2,100 additional "
        "development hours.\n\n"
        "3. Timeline Responsibility: The parties dispute whether the 6-week delay "
        "is attributable to Meridian's personnel changes or Greenfield's delayed "
        "data provisioning.\n\n"
        "4. UAT Methodology: Meridian challenges the validity of the UAT results, "
        "claiming that Greenfield's testing team used outdated test scripts and "
        "included 43 test cases outside the agreed scope.\n\n"
        "5. Remediation Feasibility: Greenfield engaged an independent auditor, "
        "TechReview Associates, which estimated 4,200 hours to remediate the "
        "defects. Meridian's internal assessment estimated only 800 hours."
    )
    page.insert_textbox(pymupdf.Rect(54, 120, W - 54, H - 70), fact_text,
                        fontsize=11, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)
    add_header_footer(page, 7, total_pages)

    # ========================
    # PAGE 8 - DISPUTED ISSUES OF LAW
    # ========================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(54, 100),
                     "VI. DISPUTED ISSUES OF LAW",
                     fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.3))
    law_text = (
        "1. Material Breach Standard: Whether Meridian's performance constitutes "
        "a material breach under California law entitling Greenfield to rescission "
        "and full damages, or merely a partial breach subject to offset. See "
        "Sackett v. Spindler (1967) 248 Cal.App.2d 220.\n\n"
        "2. Consequential Damages Cap: Whether the limitation of liability clause "
        "in Section 9.2 is enforceable given Greenfield's allegation of willful "
        "misconduct and misrepresentation. Under California Civil Code Section "
        "1668, contractual provisions exempting a party from liability for willful "
        "injury or fraud are void.\n\n"
        "3. Duty to Mitigate: Whether Greenfield adequately mitigated its damages "
        "by engaging a replacement vendor in November 2023 or whether earlier action "
        "was required.\n\n"
        "4. Pre-Contractual Representations: Whether Meridian's statements during "
        "the bidding process regarding its prior project experience constitute "
        "actionable misrepresentations under California Business & Professions "
        "Code Section 17200.\n\n"
        "5. Implied Warranty of Workmanlike Performance: Whether California's "
        "implied warranty of workmanlike performance applies to software integration "
        "services and, if so, whether Meridian breached this warranty."
    )
    page.insert_textbox(pymupdf.Rect(54, 120, W - 54, H - 70), law_text,
                        fontsize=11, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)
    add_header_footer(page, 8, total_pages)

    # ========================
    # PAGE 9 - PRIOR SETTLEMENT NEGOTIATIONS
    # ========================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(54, 100),
                     "VII. PRIOR SETTLEMENT NEGOTIATIONS",
                     fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.3))
    settle_text = (
        "The parties have engaged in the following settlement discussions prior to "
        "this mediation:\n\n"
        "November 8, 2023: Greenfield's counsel sent a demand letter seeking "
        "$4,875,000 in total damages. Meridian's counsel responded on November 22, "
        "2023, denying liability and offering a $250,000 \"goodwill\" credit toward "
        "future services.\n\n"
        "December 14, 2023: The parties participated in a voluntary settlement "
        "conference facilitated by their respective managing partners. Greenfield "
        "reduced its demand to $3,800,000. Meridian offered $600,000 as a full "
        "and final settlement. No agreement was reached.\n\n"
        "January 30, 2024: Meridian's counsel proposed a structured resolution "
        "involving: (a) $750,000 cash payment; (b) completion of defect "
        "remediation at no charge (estimated value $180,000); and (c) a 12-month "
        "extended warranty. Greenfield rejected this proposal as insufficient.\n\n"
        "February 20, 2024: Greenfield proposed arbitration under the MSA's dispute "
        "resolution clause. Meridian counter-proposed mediation first, which both "
        "parties agreed to on March 1, 2024."
    )
    page.insert_textbox(pymupdf.Rect(54, 120, W - 54, H - 70), settle_text,
                        fontsize=11, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)
    add_header_footer(page, 9, total_pages)

    # ========================
    # PAGE 10 - DAMAGES ANALYSIS
    # ========================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(54, 100),
                     "VIII. DAMAGES ANALYSIS",
                     fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.3))
    dmg_text = (
        "Greenfield's damages are calculated as follows:\n\n"
        "A. Direct Damages (Contract Price): $2,450,000\n"
        "   Fees paid to Meridian for services that failed to meet contractual "
        "specifications. Greenfield has received no usable deliverables and has "
        "been required to engage a replacement vendor.\n\n"
        "B. Consequential Damages: $1,825,000\n"
        "   Lost Revenue (Q4 2023 - Q1 2024):        $1,200,000\n"
        "   Additional IT Staffing Costs:                 $425,000\n"
        "   Third-Party Consulting (TechReview):      $200,000\n\n"
        "C. Remediation Costs: $600,000\n"
        "   Engagement of Pinnacle Systems Inc. as replacement vendor. Contract "
        "signed December 1, 2023, with estimated completion by June 2024.\n\n"
        "TOTAL DAMAGES CLAIMED: $4,875,000\n\n"
        "Supporting documentation includes: quarterly financial statements, vendor "
        "invoices, TechReview audit report (Exhibit A), project management logs "
        "(Exhibit B), and correspondence records (Exhibit C)."
    )
    page.insert_textbox(pymupdf.Rect(54, 120, W - 54, H - 70), dmg_text,
                        fontsize=11, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)
    add_header_footer(page, 10, total_pages)

    # ========================
    # PAGE 11 - SETTLEMENT FRAMEWORK
    # ========================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(54, 100),
                     "IX. SETTLEMENT FRAMEWORK AND PROPOSAL",
                     fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.3))
    frame_text = (
        "Greenfield enters this mediation prepared to negotiate in good faith and "
        "recognizes the inherent uncertainties and costs of protracted litigation. "
        "Accordingly, Greenfield proposes the following settlement framework:\n\n"
        "Preferred Resolution: $3,200,000\n"
        "This amount reflects a significant reduction from Greenfield's full damages "
        "claim of $4,875,000 and accounts for litigation risk, the limitation of "
        "liability clause, and the desire for prompt resolution.\n\n"
        "Settlement Structure Options:\n"
        "Option A - Lump Sum: $3,200,000 payable within 30 days of execution.\n"
        "Option B - Structured: $1,600,000 upon execution; $800,000 at 6 months; "
        "$800,000 at 12 months, with 5% annual interest on unpaid balance.\n"
        "Option C - Hybrid: $2,400,000 cash payment plus Meridian's commitment to "
        "complete specific remediation tasks (valued at $800,000) at no charge.\n\n"
        "Non-Monetary Terms:\n"
        "- Mutual non-disparagement agreement\n"
        "- Confidentiality of settlement terms\n"
        "- Meridian's cooperation in transition to replacement vendor\n"
        "- Release of all claims between the parties"
    )
    page.insert_textbox(pymupdf.Rect(54, 120, W - 54, H - 70), frame_text,
                        fontsize=11, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)
    add_header_footer(page, 11, total_pages)

    # ========================
    # PAGE 12 - CONCLUSION
    # ========================
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(54, 100),
                     "X. CONCLUSION",
                     fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.3))
    conc_text = (
        "Greenfield Technologies respectfully submits this mediation brief and "
        "looks forward to a productive mediation session. Greenfield believes that "
        "a negotiated resolution is in the best interest of both parties, avoiding "
        "the substantial time, expense, and uncertainty of arbitration or litigation.\n\n"
        "Greenfield's counsel is authorized to negotiate within the framework "
        "described above and has full settlement authority up to the amounts "
        "specified. We request that Meridian's representatives attending the "
        "mediation likewise have full authority to negotiate and bind the company "
        "to any agreement reached.\n\n"
        "We are confident that with the assistance of Mediator Watanabe, the "
        "parties can reach a fair resolution that addresses Greenfield's legitimate "
        "damages while providing Meridian with certainty and closure."
    )
    page.insert_textbox(pymupdf.Rect(54, 120, W - 54, 450), conc_text,
                        fontsize=11, fontname="helv", color=(0, 0, 0),
                        align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Signature block
    page.insert_text(pymupdf.Point(54, 500), "Respectfully submitted,",
                     fontsize=11, fontname="heit", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(54, 550), "________________________________",
                     fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(54, 570), "Katherine A. Raines, Esq.",
                     fontsize=11, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(54, 588), "Raines & Whitfield LLP",
                     fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(54, 606),
                     "Counsel for Claimant Greenfield Technologies, Inc.",
                     fontsize=11, fontname="helv", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(54, 640), "Date: March 15, 2024",
                     fontsize=11, fontname="helv", color=(0, 0, 0))

    add_header_footer(page, 12, total_pages)

    # Set TOC / bookmarks
    toc = [
        [1, "I. Introduction and Summary of Dispute", 3],
        [1, "II. Background and Factual Summary", 4],
        [1, "III. Claimant's Position and Key Arguments", 5],
        [1, "IV. Respondent's Anticipated Position", 6],
        [1, "V. Disputed Issues of Fact", 7],
        [1, "VI. Disputed Issues of Law", 8],
        [1, "VII. Prior Settlement Negotiations", 9],
        [1, "VIII. Damages Analysis", 10],
        [1, "IX. Settlement Framework and Proposal", 11],
        [1, "X. Conclusion", 12],
    ]
    doc.set_toc(toc)

    # Set metadata
    doc.set_metadata({
        "title": "Mediation Brief - Greenfield Technologies v. Meridian Consulting",
        "author": "Katherine A. Raines, Esq.",
        "subject": "Mediation Brief - Case No. 2024-MED-08271",
        "keywords": "mediation, brief, legal, dispute, software, integration",
        "creator": "Raines & Whitfield LLP",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open the PDF in Evince for the agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
