"""
Initial Setup: Create a 25-page appellate brief PDF
Task ID: pdf_legal_084
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_084'
OUTPUT_DIR = f'{WORKDIR}/legal/appellate'
OUTPUT = f'{OUTPUT_DIR}/brief.pdf'

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

def create_initial():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    doc = pymupdf.open()

    # --- Page dimensions ---
    W, H = 612, 792  # US Letter

    # Margins
    LEFT = 72
    RIGHT = W - 72
    TOP = 72
    BOT = H - 72
    TEXT_W = RIGHT - LEFT

    # Helper: add centered title text
    def add_centered(page, y, text, fontsize=14, fontname="tibo"):
        page.insert_text(
            pymupdf.Point((W - len(text) * fontsize * 0.35) / 2, y),
            text, fontsize=fontsize, fontname=fontname, color=(0, 0, 0)
        )

    def add_text(page, x, y, text, fontsize=12, fontname="tiro"):
        page.insert_text(
            pymupdf.Point(x, y), text,
            fontsize=fontsize, fontname=fontname, color=(0, 0, 0)
        )

    def add_paragraph(page, rect, text, fontsize=12, fontname="tiro"):
        return page.insert_textbox(
            rect, text, fontsize=fontsize, fontname=fontname,
            color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY
        )

    # ==================== PAGE 1: COVER PAGE ====================
    p = doc.new_page(width=W, height=H)
    add_centered(p, 120, "IN THE UNITED STATES COURT OF APPEALS", fontsize=14, fontname="tibo")
    add_centered(p, 145, "FOR THE NINTH CIRCUIT", fontsize=14, fontname="tibo")
    add_centered(p, 200, "No. 23-56789", fontsize=13, fontname="tiro")
    add_centered(p, 250, "PACIFIC COAST ENVIRONMENTAL COALITION,", fontsize=13, fontname="tibo")
    add_centered(p, 270, "Plaintiff-Appellant,", fontsize=12, fontname="tiit")
    add_centered(p, 310, "v.", fontsize=12, fontname="tiro")
    add_centered(p, 350, "WESTERN ENERGY CORPORATION and", fontsize=13, fontname="tibo")
    add_centered(p, 370, "UNITED STATES ENVIRONMENTAL PROTECTION AGENCY,", fontsize=12, fontname="tibo")
    add_centered(p, 395, "Defendants-Appellees.", fontsize=12, fontname="tiit")
    add_centered(p, 460, "OPENING BRIEF OF APPELLANT", fontsize=15, fontname="tibo")
    add_centered(p, 500, "PACIFIC COAST ENVIRONMENTAL COALITION", fontsize=13, fontname="tibo")
    add_text(p, LEFT, 580, "Rebecca L. Thornton", fontsize=12, fontname="tibo")
    add_text(p, LEFT, 598, "Thornton & Associates LLP", fontsize=11, fontname="tiro")
    add_text(p, LEFT, 614, "1200 Third Avenue, Suite 1850", fontsize=11, fontname="tiro")
    add_text(p, LEFT, 630, "Seattle, Washington 98101", fontsize=11, fontname="tiro")
    add_text(p, LEFT, 646, "Tel: (206) 555-3400", fontsize=11, fontname="tiro")
    add_text(p, LEFT, 666, "Attorney for Plaintiff-Appellant", fontsize=11, fontname="tiit")

    # ==================== PAGE 2: TABLE OF CONTENTS ====================
    p = doc.new_page(width=W, height=H)
    add_centered(p, 80, "TABLE OF CONTENTS", fontsize=14, fontname="tibo")
    toc_entries = [
        ("JURISDICTIONAL STATEMENT", "1"),
        ("STATEMENT OF THE ISSUES PRESENTED FOR REVIEW", "2"),
        ("STATEMENT OF THE CASE", "3"),
        ("     A. Factual Background", "3"),
        ("     B. Regulatory History", "5"),
        ("     C. Proceedings Below", "7"),
        ("SUMMARY OF ARGUMENT", "8"),
        ("ARGUMENT", "10"),
        ("     I. THE DISTRICT COURT ERRED IN GRANTING SUMMARY JUDGMENT", "10"),
        ("          A. Standard of Review", "10"),
        ("          B. The Clean Water Act Requires Strict Compliance", "11"),
        ("     II. THE EPA'S INTERPRETATION IS NOT ENTITLED TO DEFERENCE", "14"),
        ("          A. Chevron Deference Does Not Apply", "14"),
        ("          B. The Statutory Text Is Unambiguous", "16"),
        ("     III. THE REMEDY SHOULD INCLUDE INJUNCTIVE RELIEF", "18"),
        ("CONCLUSION", "20"),
        ("CERTIFICATE OF COMPLIANCE", "21"),
        ("CERTIFICATE OF SERVICE", "22"),
        ("ADDENDUM: PERTINENT STATUTES AND REGULATIONS", "23"),
    ]
    y = 120
    for entry, pg in toc_entries:
        add_text(p, LEFT, y, entry, fontsize=11, fontname="tiro")
        add_text(p, RIGHT - 20, y, pg, fontsize=11, fontname="tiro")
        y += 20
        if y > BOT - 30:
            break

    # ==================== PAGES 3-4: JURISDICTIONAL STATEMENT / ISSUES ====================
    p = doc.new_page(width=W, height=H)
    add_centered(p, 80, "JURISDICTIONAL STATEMENT", fontsize=13, fontname="tibo")
    text = (
        "The United States District Court for the Western District of Washington had "
        "jurisdiction over this action pursuant to 28 U.S.C. \u00a7 1331 (federal question) and "
        "33 U.S.C. \u00a7 1365 (citizen suit provision of the Clean Water Act). The district court "
        "entered final judgment on March 15, 2023, granting Defendants' motion for summary "
        "judgment and dismissing all claims with prejudice. Plaintiff-Appellant Pacific Coast "
        "Environmental Coalition ('PCEC') filed a timely notice of appeal on April 12, 2023, "
        "within the 30-day period prescribed by Federal Rule of Appellate Procedure 4(a)(1)(A). "
        "This Court has jurisdiction under 28 U.S.C. \u00a7 1291 as an appeal from a final decision "
        "of a district court."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, 110, RIGHT, 350), text, fontsize=12)

    # Page 4: Issues
    p = doc.new_page(width=W, height=H)
    add_centered(p, 80, "STATEMENT OF THE ISSUES PRESENTED FOR REVIEW", fontsize=13, fontname="tibo")
    issues = [
        "1. Whether the district court erred in holding that Western Energy Corporation's "
        "discharge of industrial wastewater containing elevated levels of selenium and mercury "
        "into the Clearwater River system did not violate Section 301(a) of the Clean Water Act, "
        "33 U.S.C. \u00a7 1311(a).",
        "2. Whether the EPA's 2019 interpretive guidance permitting 'compliance flexibility' "
        "for thermal discharge limits under NPDES permits is entitled to Chevron deference, "
        "particularly where the statutory text imposes mandatory effluent limitations.",
        "3. Whether Plaintiff-Appellant is entitled to injunctive relief under Section 505 of "
        "the Clean Water Act, 33 U.S.C. \u00a7 1365, requiring cessation of unpermitted discharges "
        "and implementation of best available technology."
    ]
    y = 110
    for issue in issues:
        excess = add_paragraph(p, pymupdf.Rect(LEFT, y, RIGHT, y + 100), issue, fontsize=12)
        y += 110

    # ==================== PAGES 5-7: STATEMENT OF THE CASE ====================
    # Page 5 - Factual Background (references Smith v. Jones here)
    p = doc.new_page(width=W, height=H)
    add_centered(p, 80, "STATEMENT OF THE CASE", fontsize=13, fontname="tibo")
    add_text(p, LEFT, 110, "A. Factual Background", fontsize=12, fontname="tibo")
    factual = (
        "Western Energy Corporation ('WEC') operates the Cascade Generating Station, a "
        "1,200-megawatt coal-fired power plant located along the banks of the Clearwater River "
        "in Lewis County, Washington. Since commencing operations in 1987, the plant has "
        "discharged cooling water and industrial wastewater into the river pursuant to National "
        "Pollutant Discharge Elimination System ('NPDES') Permit No. WA-0023561. As this "
        "Court recognized in Smith v. Jones, 123 F.3d 456, 462 (9th Cir. 2020), facilities "
        "operating under NPDES permits must strictly comply with discharge limitations. "
        "Between January 2019 and December 2021, monitoring data submitted by WEC to the "
        "Washington Department of Ecology revealed 47 separate exceedances of permitted "
        "discharge limits for selenium, mercury, and total suspended solids. The selenium "
        "concentrations ranged from 12.3 to 28.7 micrograms per liter (\u03bcg/L), compared to the "
        "permitted limit of 5.0 \u03bcg/L. Mercury levels consistently exceeded the 0.012 \u03bcg/L "
        "criterion, with measurements as high as 0.089 \u03bcg/L during peak discharge events."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, 130, RIGHT, BOT), factual, fontsize=12)

    # Page 6 - More factual background
    p = doc.new_page(width=W, height=H)
    text6 = (
        "The Clearwater River supports populations of ESA-listed steelhead trout "
        "(Oncorhynchus mykiss) and Chinook salmon (Oncorhynchus tshawytscha). A 2020 study "
        "conducted by the U.S. Fish and Wildlife Service documented elevated selenium "
        "concentrations in fish tissue samples collected downstream of the Cascade plant's "
        "outfall, with levels exceeding the EPA's recommended tissue-based criterion of "
        "15.1 mg/kg dry weight. Dr. Katherine Marsh, a fisheries biologist retained by PCEC, "
        "found statistically significant reproductive impairment in steelhead populations "
        "within the affected reach, including a 34% increase in larval deformity rates compared "
        "to upstream reference sites. These findings are consistent with documented selenium "
        "toxicity pathways in salmonids.\n\n"
        "Furthermore, sediment sampling conducted by the Washington Department of Ecology in "
        "2021 revealed mercury concentrations of 1.8 mg/kg in depositional areas near the "
        "outfall, exceeding the Sediment Quality Standard of 0.41 mg/kg established under "
        "WAC 173-204-320. The contaminated sediments extend approximately 3.2 river miles "
        "downstream, affecting critical spawning habitat identified in the 2018 Clearwater "
        "River Basin Salmonid Recovery Plan."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, TOP, RIGHT, BOT), text6, fontsize=12)

    # Page 7 - Regulatory History (references Brown v. Board)
    p = doc.new_page(width=W, height=H)
    add_text(p, LEFT, 80, "B. Regulatory History", fontsize=12, fontname="tibo")
    text7 = (
        "The Clean Water Act establishes a comprehensive regulatory framework for controlling "
        "the discharge of pollutants into navigable waters. Section 301(a), 33 U.S.C. \u00a7 1311(a), "
        "broadly prohibits the discharge of any pollutant by any person except in compliance "
        "with specifically enumerated sections of the Act, including Section 402, which "
        "authorizes NPDES permits. WEC's current NPDES permit, issued in 2015 and most "
        "recently modified in 2018, contains technology-based effluent limitations derived from "
        "EPA's Steam Electric Power Generating Point Source Category regulations, 40 C.F.R. "
        "Part 423, as well as water quality-based effluent limitations necessary to ensure "
        "compliance with Washington's surface water quality standards. Just as the Supreme "
        "Court's landmark decision in Brown v. Board, 347 U.S. 483 (1954), established that "
        "constitutional protections require affirmative compliance rather than mere procedural "
        "observance, this Court should recognize that environmental statutes demand substantive "
        "adherence to their protective mandates.\n\n"
        "In September 2019, the EPA issued Interpretive Guidance Memorandum No. 2019-OW-0043, "
        "which purported to establish a framework for 'compliance flexibility' allowing "
        "permit holders to exceed numerical effluent limitations during 'transitional periods' "
        "when implementing upgraded pollution control technologies."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, 100, RIGHT, BOT), text7, fontsize=12)

    # Page 8 - Proceedings Below
    p = doc.new_page(width=W, height=H)
    add_text(p, LEFT, 80, "C. Proceedings Below", fontsize=12, fontname="tibo")
    text8 = (
        "PCEC filed its citizen suit complaint on June 3, 2021, alleging violations of the "
        "Clean Water Act. After extensive discovery, including the deposition of 14 witnesses "
        "and production of over 200,000 pages of documents, the defendants moved for summary "
        "judgment. The district court granted the motion in a 42-page opinion, holding that "
        "the EPA's 2019 guidance memorandum shielded WEC from liability during the transitional "
        "period and that PCEC failed to demonstrate an ongoing violation for purposes of "
        "injunctive relief. The court declined to address the merits of PCEC's argument that "
        "the guidance exceeded the EPA's statutory authority."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, 100, RIGHT, BOT), text8, fontsize=12)

    # ==================== PAGE 9: SUMMARY OF ARGUMENT (references Miranda v. Arizona) ====================
    p = doc.new_page(width=W, height=H)
    add_centered(p, 80, "SUMMARY OF ARGUMENT", fontsize=13, fontname="tibo")
    summary = (
        "The district court's grant of summary judgment should be reversed for three "
        "independent reasons. First, the undisputed record establishes that WEC discharged "
        "pollutants in excess of its NPDES permit limits on at least 47 occasions over a "
        "three-year period. The Clean Water Act's prohibition on unpermitted discharges is "
        "absolute, and no administrative guidance can override a statutory mandate. Just as "
        "Miranda v. Arizona, 384 U.S. 436, 467 (1966), established that procedural safeguards "
        "are non-negotiable constitutional requirements, so too are the substantive discharge "
        "limitations imposed by the Clean Water Act non-waivable by executive fiat.\n\n"
        "Second, the EPA's 2019 guidance memorandum is not entitled to Chevron deference "
        "because the statutory text unambiguously prohibits discharges exceeding permit limits. "
        "Even if ambiguity existed, the guidance fails at Chevron Step Two because it is an "
        "unreasonable construction that would effectively nullify the Act's enforcement "
        "mechanism during self-defined transitional periods of indefinite duration.\n\n"
        "Third, PCEC has demonstrated entitlement to injunctive relief. The ongoing violations "
        "continue to cause irreparable harm to the Clearwater River ecosystem, and WEC has "
        "shown no credible plan for achieving full compliance."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, 110, RIGHT, BOT), summary, fontsize=12)

    # ==================== PAGES 10-19: ARGUMENT SECTION ====================
    # Page 10
    p = doc.new_page(width=W, height=H)
    add_centered(p, 80, "ARGUMENT", fontsize=13, fontname="tibo")
    add_text(p, LEFT, 115, "I. THE DISTRICT COURT ERRED IN GRANTING SUMMARY JUDGMENT", fontsize=12, fontname="tibo")
    add_text(p, LEFT, 140, "A. Standard of Review", fontsize=12, fontname="tibo")
    std_review = (
        "This Court reviews a district court's grant of summary judgment de novo, applying "
        "the same standard as the district court under Federal Rule of Civil Procedure 56. "
        "Suzuki v. State of Haw., 861 F.3d 1082, 1085 (9th Cir. 2017). Summary judgment is "
        "appropriate only if there is no genuine dispute as to any material fact and the "
        "movant is entitled to judgment as a matter of law. Celotex Corp. v. Catrett, 477 U.S. "
        "317, 322 (1986). All reasonable inferences must be drawn in favor of the nonmoving "
        "party. Anderson v. Liberty Lobby, Inc., 477 U.S. 242, 255 (1986)."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, 160, RIGHT, BOT), std_review, fontsize=12)

    # Page 11
    p = doc.new_page(width=W, height=H)
    add_text(p, LEFT, 80, "B. The Clean Water Act Requires Strict Compliance", fontsize=12, fontname="tibo")
    strict = (
        "Section 301(a) of the Clean Water Act declares that 'the discharge of any pollutant "
        "by any person shall be unlawful' except in compliance with enumerated provisions of "
        "the Act. 33 U.S.C. \u00a7 1311(a). This prohibition is unqualified and admits of no "
        "exceptions beyond those specifically enumerated by Congress. The referenced case of "
        "Miranda v. Arizona, 384 U.S. 436, 444 (1966), illustrates the principle that when "
        "a statute establishes mandatory protections, administrative agencies cannot create "
        "ad hoc exceptions. Similarly, this Court has consistently held that NPDES permit "
        "limits are not mere guidelines but enforceable limitations. Nw. Envtl. Advocates v. "
        "City of Portland, 56 F.3d 979, 986 (9th Cir. 1995).\n\n"
        "The undisputed monitoring data demonstrates that WEC exceeded its permitted discharge "
        "limits for selenium on 31 occasions, for mercury on 12 occasions, and for total "
        "suspended solids on 4 occasions between January 2019 and December 2021. Each such "
        "exceedance constitutes a separate violation of Section 301(a)."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, 100, RIGHT, BOT), strict, fontsize=12)

    # Page 12 - continuation referencing Smith v. Jones again
    p = doc.new_page(width=W, height=H)
    text12 = (
        "The district court's reliance on the EPA's compliance flexibility guidance to excuse "
        "these violations was legal error. No provision of the Clean Water Act authorizes the "
        "EPA to prospectively excuse permit violations through interpretive guidance. As this "
        "Court held in Smith v. Jones, 123 F.3d 456, 465 (9th Cir. 2020), administrative "
        "convenience cannot override express statutory mandates. The guidance memorandum at "
        "issue here attempts to do precisely what this Court's precedent forbids: create a "
        "de facto exemption from liability through informal agency action.\n\n"
        "Moreover, the district court's holding creates a perverse incentive structure. If "
        "permit holders can avoid liability simply by announcing an intention to upgrade their "
        "pollution control equipment at some indefinite future date, the Act's deterrent effect "
        "is fundamentally undermined. WEC has been 'transitioning' to new cooling technology "
        "since 2017, yet as of the date of the district court's order, no concrete timeline "
        "for completion had been established."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, TOP, RIGHT, BOT), text12, fontsize=12)

    # Pages 13-14
    p = doc.new_page(width=W, height=H)
    text13 = (
        "The legislative history reinforces the statute's plain meaning. The Conference Report "
        "accompanying the 1972 amendments emphasized that the Act was designed to 'restore and "
        "maintain the chemical, physical, and biological integrity of the Nation's waters.' "
        "S. Conf. Rep. No. 92-1236 (1972). Senator Muskie, the Act's principal sponsor, "
        "stated on the floor that the legislation's 'no discharge' goal was intended to "
        "establish 'an aggressive program for eliminating all discharges of pollutants.' "
        "118 Cong. Rec. 33,693 (1972). This unequivocal legislative intent cannot be "
        "reconciled with an administrative framework that tolerates indefinite exceedances.\n\n"
        "The environmental harm caused by WEC's violations further supports reversal. Dr. "
        "Marsh's unrebutted expert testimony documented elevated selenium levels in steelhead "
        "tissue (mean: 22.4 mg/kg dry weight) and statistically significant increases in "
        "larval deformity rates. These findings establish ongoing ecological injury that the "
        "Clean Water Act was specifically enacted to prevent."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, TOP, RIGHT, BOT), text13, fontsize=12)

    # Page 14 - Chevron
    p = doc.new_page(width=W, height=H)
    add_text(p, LEFT, 80, "II. THE EPA'S INTERPRETATION IS NOT ENTITLED TO DEFERENCE", fontsize=12, fontname="tibo")
    add_text(p, LEFT, 105, "A. Chevron Deference Does Not Apply", fontsize=12, fontname="tibo")
    chevron = (
        "Under Chevron U.S.A., Inc. v. Natural Resources Defense Council, Inc., 467 U.S. 837 "
        "(1984), courts apply a two-step framework when reviewing an agency's interpretation "
        "of a statute it administers. At Step One, the court asks whether Congress has directly "
        "spoken to the precise question at issue. If so, the court must give effect to the "
        "unambiguously expressed intent of Congress. Id. at 842-43.\n\n"
        "Here, Congress has spoken with unmistakable clarity. Section 301(a) flatly prohibits "
        "the discharge of any pollutant except in compliance with the Act's permitting "
        "provisions. The word 'any' is among the broadest in the English language, and its "
        "ordinary meaning extends to 'each' and 'every' discharge. United States v. Gonzales, "
        "520 U.S. 1, 5 (1997). There is simply no textual basis for reading an implied "
        "transitional exemption into this categorical prohibition."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, 125, RIGHT, BOT), chevron, fontsize=12)

    # Page 15 - Brown v. Board reference again
    p = doc.new_page(width=W, height=H)
    text15 = (
        "Even if some ambiguity existed in the statutory text, the EPA's interpretation would "
        "fail at Chevron Step Two. An agency interpretation is unreasonable when it would "
        "effectively nullify a core provision of the statute it administers. The compliance "
        "flexibility framework contains no meaningful temporal limitation, no performance "
        "benchmarks, and no mechanism for ensuring that the transitional period does not become "
        "permanent. As the principles underlying Brown v. Board, 347 U.S. 483, 495 (1954), "
        "illustrate, mandates for compliance cannot be deferred indefinitely through "
        "administrative discretion; 'deliberate speed' is not an acceptable substitute for "
        "immediate compliance with clear legal obligations.\n\n"
        "The guidance also fails the procedural requirements for Chevron deference. As an "
        "interpretive guidance memorandum, it was not promulgated through notice-and-comment "
        "rulemaking. While interpretive rules can sometimes receive Chevron deference, the "
        "Supreme Court has emphasized that the degree of deference depends on the 'thoroughness "
        "evident in its consideration, the validity of its reasoning, its consistency with "
        "earlier and later pronouncements, and all those factors which give it power to "
        "persuade.' Skidmore v. Swift & Co., 323 U.S. 134, 140 (1944)."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, TOP, RIGHT, BOT), text15, fontsize=12)

    # Page 16
    p = doc.new_page(width=W, height=H)
    add_text(p, LEFT, 80, "B. The Statutory Text Is Unambiguous", fontsize=12, fontname="tibo")
    text16 = (
        "The structure and purpose of the Clean Water Act confirm the unambiguous meaning of "
        "Section 301(a). Congress established a carefully calibrated system in which "
        "increasingly stringent technology-based and water quality-based limitations would "
        "progressively eliminate the discharge of pollutants. The Act contemplates specific "
        "mechanisms for achieving compliance over time, including compliance schedules "
        "incorporated into individual permits under Section 402(a)(1), 33 U.S.C. \u00a7 1342(a)(1), "
        "and enforcement orders issued under Section 309(a), 33 U.S.C. \u00a7 1319(a). These "
        "specific provisions for transitional compliance demonstrate that Congress did not "
        "intend to grant the EPA a freestanding authority to excuse violations through "
        "informal guidance.\n\n"
        "The interpretive guidance at issue here is particularly problematic because it was "
        "issued without any of the procedural safeguards that attend formal rulemaking. The "
        "guidance was developed internally by the Office of Water, without public notice, "
        "comment period, or response to comments. No environmental impact analysis was "
        "conducted, and no consultation with affected states occurred."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, 100, RIGHT, BOT), text16, fontsize=12)

    # Page 17
    p = doc.new_page(width=W, height=H)
    text17 = (
        "The district court's reasoning would create an unworkable precedent. If the EPA can "
        "excuse compliance with explicit permit conditions through informal guidance, the "
        "entire NPDES permitting system would be rendered advisory rather than mandatory. "
        "Permit holders would have no incentive to invest in pollution control technologies "
        "when they can simply declare an intention to upgrade and receive indefinite immunity "
        "from enforcement. This result is antithetical to the Clean Water Act's structure, "
        "which depends on enforceable permit conditions to achieve its water quality objectives.\n\n"
        "Other circuits have recognized the importance of maintaining the integrity of NPDES "
        "permit limits. The Fourth Circuit held in Piney Run Preservation Ass'n v. County "
        "Comm'rs, 268 F.3d 255, 269 (4th Cir. 2001), that permit conditions must be "
        "interpreted and enforced according to their plain terms. The Sixth Circuit similarly "
        "observed that the 'NPDES permit is the cornerstone of the Clean Water Act's pollution "
        "control scheme.' Sierra Club v. ICG Hazard, LLC, 781 F.3d 281, 284 (6th Cir. 2015)."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, TOP, RIGHT, BOT), text17, fontsize=12)

    # Page 18 - Injunctive Relief (Miranda reference)
    p = doc.new_page(width=W, height=H)
    add_text(p, LEFT, 80, "III. THE REMEDY SHOULD INCLUDE INJUNCTIVE RELIEF", fontsize=12, fontname="tibo")
    text18 = (
        "Section 505(d) of the Clean Water Act authorizes district courts to 'enforce any "
        "effluent standard or limitation ... and to apply any appropriate civil penalties.' "
        "33 U.S.C. \u00a7 1365(d). This Court has held that injunctive relief is the presumptive "
        "remedy for ongoing violations of the Act. Weinberger v. Romero-Barcelo, 456 U.S. "
        "305, 313 (1982). The principle echoed in Miranda v. Arizona, 384 U.S. 436, 479 "
        "(1966), that remedies must be commensurate with the violation, applies with equal "
        "force in the environmental context.\n\n"
        "The record establishes that WEC's violations are ongoing and likely to continue. "
        "As of the date the district court entered summary judgment, WEC had not installed "
        "upgraded selenium treatment technology, had not submitted a revised compliance plan "
        "to the Washington Department of Ecology, and had not achieved consistent compliance "
        "with its permitted discharge limits for any pollutant parameter. The most recent "
        "monthly discharge monitoring report in the record, dated February 2023, showed "
        "selenium concentrations of 8.7 \u03bcg/L, nearly double the permitted 5.0 \u03bcg/L limit."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, 100, RIGHT, BOT), text18, fontsize=12)

    # Page 19
    p = doc.new_page(width=W, height=H)
    text19 = (
        "The traditional equitable factors overwhelmingly favor injunctive relief. PCEC has "
        "demonstrated irreparable harm to the Clearwater River ecosystem, including documented "
        "impacts to ESA-listed salmonid populations. The balance of hardships tips sharply in "
        "PCEC's favor: the costs of compliance pale in comparison to the ecological damage "
        "caused by continued unpermitted discharges. WEC reported net revenues of $2.3 billion "
        "in fiscal year 2022 and estimated the cost of upgraded selenium treatment technology "
        "at approximately $45 million. This represents less than 2% of annual revenue.\n\n"
        "Finally, injunctive relief would serve the public interest by vindicating the Clean "
        "Water Act's protective purpose and deterring future violations. The Clearwater River "
        "provides drinking water to approximately 85,000 residents, recreational fishing and "
        "boating opportunities, and critical habitat for imperiled fish species. The public's "
        "interest in clean water is both tangible and compelling."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, TOP, RIGHT, BOT), text19, fontsize=12)

    # ==================== PAGE 20: CONCLUSION ====================
    p = doc.new_page(width=W, height=H)
    add_centered(p, 80, "CONCLUSION", fontsize=13, fontname="tibo")
    conclusion = (
        "For the foregoing reasons, Plaintiff-Appellant Pacific Coast Environmental Coalition "
        "respectfully requests that this Court reverse the district court's grant of summary "
        "judgment in favor of Defendants-Appellees, hold that Western Energy Corporation's "
        "discharges violated Section 301(a) of the Clean Water Act, hold that the EPA's 2019 "
        "compliance flexibility guidance is not entitled to Chevron deference, and remand this "
        "matter with instructions to enter appropriate injunctive relief and civil penalties."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, 110, RIGHT, 350), conclusion, fontsize=12)

    add_text(p, LEFT, 400, "Respectfully submitted,", fontsize=12, fontname="tiit")
    add_text(p, LEFT, 440, "___________________________", fontsize=12, fontname="tiro")
    add_text(p, LEFT, 460, "Rebecca L. Thornton", fontsize=12, fontname="tibo")
    add_text(p, LEFT, 478, "Thornton & Associates LLP", fontsize=12, fontname="tiro")
    add_text(p, LEFT, 496, "Attorney for Plaintiff-Appellant", fontsize=12, fontname="tiit")
    add_text(p, LEFT, 530, "Dated: November 15, 2023", fontsize=12, fontname="tiro")

    # ==================== PAGE 21: CERTIFICATE OF COMPLIANCE ====================
    p = doc.new_page(width=W, height=H)
    add_centered(p, 80, "CERTIFICATE OF COMPLIANCE", fontsize=13, fontname="tibo")
    cert = (
        "Pursuant to Federal Rule of Appellate Procedure 32(g) and Ninth Circuit Rule 32-1, "
        "I certify that this brief complies with the type-volume limitation of Rule 32(a)(7)(B). "
        "This brief contains 11,842 words, excluding the parts of the brief exempted by "
        "Rule 32(f). This brief complies with the typeface requirements of Rule 32(a)(5) "
        "and the type-style requirements of Rule 32(a)(6) because it was prepared using "
        "proportionally spaced type in 14-point Times New Roman font."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, 110, RIGHT, 350), cert, fontsize=12)
    add_text(p, LEFT, 380, "___________________________", fontsize=12, fontname="tiro")
    add_text(p, LEFT, 400, "Rebecca L. Thornton", fontsize=12, fontname="tibo")

    # ==================== PAGE 22: CERTIFICATE OF SERVICE ====================
    p = doc.new_page(width=W, height=H)
    add_centered(p, 80, "CERTIFICATE OF SERVICE", fontsize=13, fontname="tibo")
    service = (
        "I hereby certify that on November 15, 2023, I electronically filed the foregoing "
        "Opening Brief of Appellant with the Clerk of the Court for the United States Court "
        "of Appeals for the Ninth Circuit using the CM/ECF system, which will send notification "
        "of such filing to all counsel of record.\n\n"
        "Counsel for Western Energy Corporation:\n"
        "James R. Blackwell, Esq.\n"
        "Morrison & Sterling LLP\n"
        "701 Fifth Avenue, Suite 3200\n"
        "Seattle, WA 98104\n\n"
        "Counsel for United States EPA:\n"
        "Sarah M. Whitfield\n"
        "United States Department of Justice\n"
        "Environment and Natural Resources Division\n"
        "P.O. Box 7611\n"
        "Washington, DC 20044"
    )
    add_paragraph(p, pymupdf.Rect(LEFT, 110, RIGHT, BOT), service, fontsize=12)

    # ==================== PAGES 23-25: ADDENDUM ====================
    p = doc.new_page(width=W, height=H)
    add_centered(p, 80, "ADDENDUM: PERTINENT STATUTES AND REGULATIONS", fontsize=13, fontname="tibo")
    add_text(p, LEFT, 120, "33 U.S.C. \u00a7 1311(a) - Effluent Limitations", fontsize=12, fontname="tibo")
    statute1 = (
        "(a) Except as in compliance with this section and sections 1312, 1316, 1317, 1328, "
        "1342, and 1344 of this title, the discharge of any pollutant by any person shall be "
        "unlawful."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, 140, RIGHT, 250), statute1, fontsize=11)
    add_text(p, LEFT, 270, "33 U.S.C. \u00a7 1342(a)(1) - NPDES Permits", fontsize=12, fontname="tibo")
    statute2 = (
        "(a)(1) Except as provided in sections 1328 and 1344 of this title, the Administrator "
        "may, after opportunity for public hearing, issue a permit for the discharge of any "
        "pollutant, or combination of pollutants, notwithstanding section 1311(a) of this "
        "title, upon condition that such discharge will meet all applicable requirements under "
        "sections 1311, 1312, 1316, 1317, 1318, and 1343 of this title..."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, 290, RIGHT, 450), statute2, fontsize=11)

    # Page 24
    p = doc.new_page(width=W, height=H)
    add_text(p, LEFT, 80, "33 U.S.C. \u00a7 1365 - Citizen Suits", fontsize=12, fontname="tibo")
    statute3 = (
        "(a) Except as provided in subsection (b) of this section and section 1319(g)(6) of "
        "this title, any citizen may commence a civil action on his own behalf -- (1) against "
        "any person (including (i) the United States, and (ii) any other governmental "
        "instrumentality or agency to the extent permitted by the eleventh amendment to the "
        "Constitution) who is alleged to be in violation of (A) an effluent standard or "
        "limitation under this chapter or (B) an order issued by the Administrator or a State "
        "with respect to such a standard or limitation...\n\n"
        "(d) The court, in issuing any final order in any action brought pursuant to this "
        "section, may award costs of litigation (including reasonable attorney and expert "
        "witness fees) to any prevailing or substantially prevailing party, whenever the "
        "court determines such award is appropriate."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, 100, RIGHT, 400), statute3, fontsize=11)
    add_text(p, LEFT, 420, "40 C.F.R. Part 423 - Steam Electric Power Generating", fontsize=12, fontname="tibo")
    statute4 = (
        "The regulations at 40 C.F.R. Part 423 establish effluent limitations guidelines and "
        "standards of performance for the steam electric power generating point source category. "
        "These regulations prescribe both Best Practicable Control Technology Currently "
        "Available (BPT) and Best Available Technology Economically Achievable (BAT) "
        "limitations for various pollutant parameters including total suspended solids, oil "
        "and grease, and priority pollutants such as selenium and mercury."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, 440, RIGHT, BOT), statute4, fontsize=11)

    # Page 25
    p = doc.new_page(width=W, height=H)
    add_text(p, LEFT, 80, "Washington Administrative Code (WAC) 173-204-320", fontsize=12, fontname="tibo")
    statute5 = (
        "Sediment Quality Standards. The sediment quality standards establish the maximum "
        "concentration levels of contaminants in marine and freshwater sediments that protect "
        "biological resources and human health. For mercury, the sediment quality standard is "
        "0.41 mg/kg (dry weight) for freshwater sediments. Exceedances of these standards "
        "trigger requirements for sediment characterization, cleanup, and source control under "
        "the Sediment Management Standards program."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, 100, RIGHT, 280), statute5, fontsize=11)
    add_text(p, LEFT, 300, "EPA Interpretive Guidance Memorandum No. 2019-OW-0043", fontsize=12, fontname="tibo")
    guidance = (
        "This memorandum establishes a framework for compliance flexibility under NPDES permits "
        "for facilities implementing upgraded pollution control technologies. Under the guidance, "
        "permit holders may request a compliance schedule extension of up to 36 months when "
        "transitioning to best available technology, provided they demonstrate: (1) a good "
        "faith commitment to achieving compliance; (2) a reasonable timeline for technology "
        "installation; (3) interim measures to minimize discharge exceedances; and (4) periodic "
        "progress reporting. The guidance applies to technology-based effluent limitations and "
        "does not address water quality-based limitations.\n\n"
        "NOTE: This guidance has been challenged in multiple jurisdictions and its legal "
        "authority remains contested. Several environmental organizations and state attorneys "
        "general have filed petitions seeking its withdrawal."
    )
    add_paragraph(p, pymupdf.Rect(LEFT, 320, RIGHT, BOT), guidance, fontsize=11)

    # Add page numbers to all pages (bottom center)
    for i in range(doc.page_count):
        page = doc[i]
        page.insert_text(
            pymupdf.Point(W / 2 - 10, H - 36),
            str(i + 1),
            fontsize=10, fontname="tiro", color=(0, 0, 0)
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 25')

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')

create_initial()
