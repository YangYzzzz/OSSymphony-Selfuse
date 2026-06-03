"""
Initial Setup: Create a 25-page legal brief with 35 statute references
Task ID: pdf_legal_064
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_064'
LEGAL_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{LEGAL_DIR}/statutory_brief.pdf'

# Page dimensions
PW, PH = 612, 792  # US Letter

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

def add_page_text(doc, page, text_blocks, page_num):
    """Add text blocks to a page with proper formatting."""
    y = 72  # top margin
    for block in text_blocks:
        style = block.get("style", "body")
        text = block["text"]

        if style == "title":
            fontname, fontsize = "hebo", 18
            y += 10
        elif style == "heading":
            fontname, fontsize = "hebo", 14
            y += 8
        elif style == "subheading":
            fontname, fontsize = "hebo", 12
            y += 4
        elif style == "citation":
            fontname, fontsize = "tiit", 10
        else:  # body
            fontname, fontsize = "tiro", 11

        # Use textbox for wrapping
        rect = pymupdf.Rect(72, y, PW - 72, PH - 72)
        excess = page.insert_textbox(
            rect, text, fontsize=fontsize, fontname=fontname, color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT if style != "title" else pymupdf.TEXT_ALIGN_CENTER
        )

        # Estimate lines used
        chars_per_line = int((PW - 144) / (fontsize * 0.5))
        if chars_per_line > 0:
            lines = max(1, (len(text) // chars_per_line) + 1)
        else:
            lines = 1
        y += lines * (fontsize + 3) + 6

    # Page number at bottom
    page.insert_text(
        pymupdf.Point(PW / 2 - 10, PH - 36),
        str(page_num),
        fontsize=10, fontname="tiro", color=(0, 0, 0)
    )


def create_initial():
    os.makedirs(LEGAL_DIR, exist_ok=True)
    doc = pymupdf.open()

    # ===== Define the complete legal brief content =====
    # We need 25 pages with 35 statute references distributed throughout.
    # Patterns: "Section XXX.XX" and "ss XXX.XX" (the section sign)

    pages_content = []

    # --- Page 1: Title Page ---
    pages_content.append([
        {"text": "IN THE UNITED STATES DISTRICT COURT\nFOR THE NORTHERN DISTRICT OF CALIFORNIA", "style": "title"},
        {"text": "\n\nMERIDIAN TECHNOLOGIES, INC.,\nPlaintiff,\n\nv.\n\nPACIFIC DIGITAL SOLUTIONS, LLC,\nDefendant.", "style": "heading"},
        {"text": "\nCase No. 3:2025-cv-04817-JKL\n\nPLAINTIFF'S MEMORANDUM OF LAW\nIN SUPPORT OF MOTION FOR SUMMARY JUDGMENT", "style": "heading"},
        {"text": "\nCounsel for Plaintiff:\nElizabeth A. Thornton, Esq.\nRachel M. Vasquez, Esq.\nThornton & Associates LLP\n555 Market Street, Suite 3200\nSan Francisco, CA 94105", "style": "body"},
    ])

    # --- Page 2: Table of Contents ---
    pages_content.append([
        {"text": "TABLE OF CONTENTS", "style": "title"},
        {"text": "\nI. INTRODUCTION.............................................1\nII. STATEMENT OF FACTS......................................3\nIII. LEGAL STANDARD.........................................6\nIV. ARGUMENT................................................8\n    A. Breach of Contract Claim.............................8\n    B. Misappropriation of Trade Secrets...................12\n    C. Unfair Business Practices...........................16\n    D. Damages Analysis....................................20\nV. CONCLUSION..............................................23", "style": "body"},
    ])

    # --- Page 3: Table of Authorities ---
    pages_content.append([
        {"text": "TABLE OF AUTHORITIES", "style": "title"},
        {"text": "\nStatutes:\nCal. Civ. Code Section 1550.05 .......................... 9\nCal. Civ. Code Section 3426.01 .......................... 12\nCal. Bus. & Prof. Code \u00a7 17200.00 ....................... 16\n15 U.S.C. \u00a7 1125.01 ..................................... 18\n18 U.S.C. Section 1836.02 ............................... 13\nCal. Civ. Code Section 3426.03 .......................... 14\nCal. Civ. Proc. Code \u00a7 437c.01 .......................... 7", "style": "body"},
        {"text": "\nCases:\nCelotex Corp. v. Catrett, 477 U.S. 317 (1986)\nMatsushita Elec. Indus. Co. v. Zenith Radio Corp., 475 U.S. 574 (1986)\nAnderson v. Liberty Lobby, Inc., 477 U.S. 242 (1986)\nSilvaco Data Sys. v. Intel Corp., 184 Cal.App.4th 210 (2010)\nCadence Design Sys. v. Avant! Corp., 29 Cal.4th 215 (2002)", "style": "body"},
    ])

    # --- Page 4: Introduction ---
    pages_content.append([
        {"text": "I. INTRODUCTION", "style": "heading"},
        {"text": "\nPlaintiff Meridian Technologies, Inc. (\"Meridian\") respectfully submits this memorandum of law in support of its motion for summary judgment against Defendant Pacific Digital Solutions, LLC (\"Pacific Digital\"). The undisputed material facts establish that Pacific Digital breached its contractual obligations under the Master Services Agreement dated March 15, 2023 (\"MSA\"), and misappropriated Meridian's proprietary trade secrets in violation of both state and federal law.", "style": "body"},
        {"text": "\nThe evidence demonstrates beyond any genuine dispute that Pacific Digital systematically extracted Meridian's confidential source code, client databases, and algorithmic methodologies, then incorporated these materials into competing products. This conduct violates the express terms of the MSA, the California Uniform Trade Secrets Act codified at Section 3426.01 of the Civil Code, and the Defend Trade Secrets Act, 18 U.S.C. Section 1836.02.", "style": "body"},
    ])

    # --- Page 5: Introduction (cont'd) ---
    pages_content.append([
        {"text": "Meridian seeks summary judgment on all three of its claims: (1) breach of contract; (2) misappropriation of trade secrets under Cal. Civ. Code \u00a7 3426.03; and (3) unfair business practices under Cal. Bus. & Prof. Code \u00a7 17200.00. The record before this Court leaves no room for genuine dispute on any material fact.", "style": "body"},
        {"text": "\nAs set forth below, Pacific Digital's own internal communications, deposition testimony of its former Chief Technology Officer, and the forensic analysis of its codebase all confirm Meridian's entitlement to judgment as a matter of law.", "style": "body"},
    ])

    # --- Page 6-7: Statement of Facts ---
    pages_content.append([
        {"text": "II. STATEMENT OF FACTS", "style": "heading"},
        {"text": "\nMeridian is a Delaware corporation headquartered in San Francisco, California, specializing in enterprise software solutions for financial institutions. Since its founding in 2015, Meridian has invested over $47 million in research and development of its proprietary DataStream Analytics Platform (\"DSAP\"), which processes real-time financial transaction data for over 200 banking institutions nationwide.", "style": "body"},
        {"text": "\nOn March 15, 2023, Meridian entered into the MSA with Pacific Digital pursuant to which Pacific Digital would provide supplemental software development services. The MSA contained explicit confidentiality provisions under Section 7.2, non-compete restrictions under Section 8.1, and intellectual property assignment clauses under Section 9.4. These provisions were negotiated at arm's length over a period of six weeks, with both parties represented by experienced legal counsel.", "style": "body"},
    ])

    pages_content.append([
        {"text": "Between April 2023 and September 2024, Pacific Digital's development team was granted limited access to Meridian's proprietary codebase through a secured virtual development environment. Access logs maintained by Meridian's IT Security department (Exhibit A) demonstrate that on 47 separate occasions, Pacific Digital employees downloaded files beyond the scope of their authorized access, including core algorithmic modules and client relationship management databases.", "style": "body"},
        {"text": "\nOn October 3, 2024, Meridian's Chief Information Security Officer, Dr. James Whitfield, detected unauthorized bulk data transfers originating from Pacific Digital's IP addresses. Forensic analysis conducted by CyberTrace Solutions, Inc. (Exhibit B) confirmed that approximately 2.3 terabytes of proprietary data had been exfiltrated to servers controlled by Pacific Digital. The transferred data included source code for the DSAP core processing engine, client financial profiles, and Meridian's proprietary machine learning models.", "style": "body"},
    ])

    # --- Page 8: Statement of Facts (cont'd) ---
    pages_content.append([
        {"text": "On November 12, 2024, Pacific Digital launched its competing product, \"FinanceFlow Pro,\" which Meridian's expert, Dr. Amelia Rodriguez (a professor of Computer Science at Stanford University), has determined contains substantial portions of code derived from Meridian's DSAP platform. Dr. Rodriguez's analysis (Exhibit C) identified 847 instances of functionally identical code segments, 23 shared proprietary algorithm implementations, and identical database schema architectures across both platforms.", "style": "body"},
        {"text": "\nPacific Digital's former CTO, Daniel Kowalski, testified in his deposition that he was \"aware that certain team members had accessed Meridian materials beyond the scope of the MSA\" but characterized the conduct as \"inadvertent.\" (Kowalski Dep. at 142:7-15.) However, internal Slack messages produced in discovery (Exhibit D) reveal that Kowalski specifically directed team members to \"pull everything useful from the Meridian repo before they cut off our access.\" (Ex. D at PDSL-00847.)", "style": "body"},
    ])

    # --- Page 9: Legal Standard ---
    pages_content.append([
        {"text": "III. LEGAL STANDARD", "style": "heading"},
        {"text": "\nSummary judgment is appropriate when \"the movant shows that there is no genuine dispute as to any material fact and the movant is entitled to judgment as a matter of law.\" Cal. Civ. Proc. Code \u00a7 437c.01; see also Fed. R. Civ. P. 56(a). The moving party bears the initial burden of demonstrating the absence of a genuine issue of material fact. Celotex Corp. v. Catrett, 477 U.S. 317, 323 (1986).", "style": "body"},
        {"text": "\nOnce the moving party has met its burden, the nonmoving party must \"set forth specific facts showing that there is a genuine issue for trial.\" Anderson v. Liberty Lobby, Inc., 477 U.S. 242, 248 (1986). The court must view the evidence in the light most favorable to the nonmoving party, but \"the mere existence of a scintilla of evidence\" is insufficient to create a genuine dispute. Id. at 252.", "style": "body"},
    ])

    # --- Page 10-11: Breach of Contract Argument ---
    pages_content.append([
        {"text": "IV. ARGUMENT", "style": "heading"},
        {"text": "\nA. Pacific Digital Breached the Master Services Agreement", "style": "subheading"},
        {"text": "\nTo prevail on a breach of contract claim under California law, a plaintiff must establish: (1) the existence of a valid contract; (2) the plaintiff's performance or excuse for nonperformance; (3) the defendant's breach; and (4) resulting damages. See Cal. Civ. Code Section 1550.05 (elements of a valid contract). Each element is established here as a matter of undisputed fact.", "style": "body"},
        {"text": "\n1. Existence of a Valid Contract\n\nThe MSA constitutes an enforceable contract under California law. It was executed by authorized representatives of both parties, supported by adequate consideration, and contains all material terms necessary for enforcement. Pacific Digital does not dispute the validity of the MSA.", "style": "body"},
    ])

    pages_content.append([
        {"text": "2. Meridian's Performance\n\nMeridian fully performed its obligations under the MSA. It provided Pacific Digital with the agreed-upon access to development resources, made all contractually required payments totaling $3.2 million, and maintained the collaborative infrastructure necessary for Pacific Digital to fulfill its duties.", "style": "body"},
        {"text": "\n3. Pacific Digital's Breach\n\nPacific Digital breached at least three provisions of the MSA: (a) Section 7.2, which prohibited disclosure or use of confidential information outside the scope of the engagement; (b) Section 8.1, which restricted Pacific Digital from developing competing products using Meridian's proprietary technology for a period of 24 months; and (c) Section 9.4, which assigned all intellectual property developed using Meridian's confidential information exclusively to Meridian.", "style": "body"},
    ])

    # --- Page 12-13: Breach continued ---
    pages_content.append([
        {"text": "The evidence of breach is overwhelming. Pacific Digital's own CTO admitted knowledge of unauthorized data access. The forensic analysis confirms the systematic exfiltration of 2.3 terabytes of proprietary data. And Pacific Digital launched a competing product incorporating Meridian's trade secrets within weeks of the data theft. Under Section 1550.05 of the California Civil Code, these acts constitute material breaches entitling Meridian to full contractual remedies.", "style": "body"},
        {"text": "\n4. Damages\n\nMeridian has suffered substantial damages as a direct and proximate result of Pacific Digital's breaches. Meridian's damages expert, Dr. Kenneth Park, has calculated Meridian's lost profits at $18.7 million, based on market analysis of client accounts diverted to Pacific Digital's competing product. Additionally, Meridian seeks recovery of its $47 million R&D investment that Pacific Digital misappropriated.", "style": "body"},
    ])

    pages_content.append([
        {"text": "B. Pacific Digital Misappropriated Meridian's Trade Secrets", "style": "subheading"},
        {"text": "\nThe California Uniform Trade Secrets Act (\"CUTSA\"), codified at Cal. Civ. Code Section 3426.01 through Section 3426.11, provides robust protection against trade secret misappropriation. Under Section 3426.01, a \"trade secret\" is defined as information that (1) derives independent economic value from not being generally known and (2) is the subject of efforts that are reasonable under the circumstances to maintain its secrecy.", "style": "body"},
        {"text": "\nMeridian's DSAP source code, algorithmic models, and client databases clearly qualify as trade secrets. These materials represent nine years of proprietary development and provide Meridian with significant competitive advantages in the financial technology market. Meridian maintained reasonable secrecy measures including encrypted repositories, role-based access controls, multi-factor authentication, and comprehensive non-disclosure agreements with all personnel.", "style": "body"},
    ])

    # --- Page 14-15: Trade Secrets continued ---
    pages_content.append([
        {"text": "\"Misappropriation\" under Section 3426.01 includes both the acquisition of a trade secret by improper means and the disclosure or use of a trade secret obtained through improper means. Pacific Digital's conduct satisfies both definitions. The unauthorized bulk downloads constitute acquisition by improper means, and the incorporation of Meridian's code into FinanceFlow Pro constitutes use of improperly obtained trade secrets.", "style": "body"},
        {"text": "\nUnder the federal Defend Trade Secrets Act, 18 U.S.C. Section 1836.02, Meridian is entitled to injunctive relief, compensatory damages, and exemplary damages. The DTSA applies because Pacific Digital's misappropriation affected products used in interstate and foreign commerce. Section 1836.02 authorizes courts to grant injunctions to prevent further misappropriation and to award damages adequate to compensate the trade secret owner.", "style": "body"},
    ])

    pages_content.append([
        {"text": "Meridian is entitled to remedies under Cal. Civ. Code \u00a7 3426.03, which provides for both injunctive relief and monetary damages. The statute permits recovery of actual loss and unjust enrichment not addressed by actual loss. Additionally, under \u00a7 3426.03, if willful and malicious misappropriation is established, the court may award exemplary damages up to twice the amount of actual damages.", "style": "body"},
        {"text": "\nThe willfulness of Pacific Digital's conduct is evident from the internal communications directing employees to extract Meridian's proprietary materials. CTO Kowalski's directive to \"pull everything useful\" demonstrates a deliberate intent to misappropriate, rather than mere negligence or inadvertent access.", "style": "body"},
        {"text": "\nFurthermore, the scale of the misappropriation, involving 2.3 terabytes of data and 847 instances of code replication, negates any suggestion that the conduct was accidental. These facts establish willful and malicious misappropriation as a matter of law, entitling Meridian to exemplary damages under Section 3426.04 of the Civil Code.", "style": "body"},
    ])

    # --- Page 16-17: Unfair Business Practices ---
    pages_content.append([
        {"text": "C. Pacific Digital Engaged in Unfair Business Practices", "style": "subheading"},
        {"text": "\nCalifornia's Unfair Competition Law (\"UCL\"), codified at Cal. Bus. & Prof. Code \u00a7 17200.00 et seq., prohibits \"any unlawful, unfair or fraudulent business act or practice.\" The UCL's coverage is \"sweeping, embracing anything that can properly be called a business practice and that at the same time is forbidden by law.\" Cel-Tech Communications, Inc. v. Los Angeles Cellular Telephone Co., 20 Cal.4th 163, 180 (1999).", "style": "body"},
        {"text": "\nPacific Digital's conduct is actionable under all three prongs of the UCL. Under the \"unlawful\" prong, Pacific Digital's trade secret misappropriation violates Cal. Civ. Code Section 3426.01 and 18 U.S.C. \u00a7 1125.01, thereby constituting an unlawful business practice under \u00a7 17200.00.", "style": "body"},
    ])

    pages_content.append([
        {"text": "Under the \"unfair\" prong of \u00a7 17200.00, Pacific Digital's systematic theft of a business partner's proprietary technology and use of that technology to directly compete against the partner represents conduct that is \"immoral, unethical, oppressive, [or] unscrupulous\" and causes \"substantial injury to consumers or competitors.\" Smith v. State Farm Mutual Auto. Ins. Co., 93 Cal.App.4th 700, 718 (2001).", "style": "body"},
        {"text": "\nUnder the \"fraudulent\" prong, Pacific Digital represented through the MSA that it would maintain confidentiality and refrain from competitive use of Meridian's proprietary materials. These representations were false when made, as evidenced by the fact that Pacific Digital began unauthorized data extraction within weeks of contract execution. Meridian reasonably relied on these representations to its detriment, satisfying the fraud element under \u00a7 17200.00.", "style": "body"},
        {"text": "\nThe UCL authorizes broad equitable remedies, including restitution and injunctive relief. Under Bus. & Prof. Code Section 17203.01, the court may \"make such orders or judgments as may be necessary to prevent the use or employment\" of the unfair practice and to \"restore to any person in interest any money or property\" obtained through the unfair practice.", "style": "body"},
    ])

    # --- Page 18-19: Additional statutory references ---
    pages_content.append([
        {"text": "Pacific Digital's conduct also implicates federal unfair competition law. The Lanham Act, 15 U.S.C. \u00a7 1125.01, provides a federal cause of action for false designation of origin and unfair competition. By marketing FinanceFlow Pro as an independently developed product when it was substantially derived from Meridian's proprietary DSAP platform, Pacific Digital has engaged in conduct actionable under Section 1125.01.", "style": "body"},
        {"text": "\nCourts have consistently recognized that the misrepresentation of a product's origin, including the concealment of misappropriated source material, constitutes actionable false designation of origin. See Dastar Corp. v. Twentieth Century Fox Film Corp., 539 U.S. 23, 31 (2003); Baden Sports, Inc. v. Molten USA, Inc., 556 F.3d 1300 (Fed. Cir. 2009).", "style": "body"},
        {"text": "\nAdditionally, the Computer Fraud and Abuse Act (\"CFAA\"), 18 U.S.C. Section 1030.05, may provide an independent basis for liability. Pacific Digital's employees exceeded their authorized access to Meridian's systems when they downloaded files beyond the scope of their engagement. Under \u00a7 1030.05, any person who \"intentionally accesses a computer without authorization or exceeds authorized access\" and obtains information is subject to civil liability.", "style": "body"},
    ])

    pages_content.append([
        {"text": "The intersection of state and federal statutory protections ensures that Meridian has multiple avenues for obtaining complete relief. The CUTSA's preemption provision, Cal. Civ. Code Section 3426.07, preempts common law claims based on the same nucleus of facts, but does not preempt statutory causes of action such as the UCL claim or federal claims under the DTSA and Lanham Act.", "style": "body"},
        {"text": "\nMeridian's damages expert, Dr. Park, has calculated the total economic harm at $65.7 million, comprising: (a) $18.7 million in lost profits from diverted client accounts; (b) $47 million representing the misappropriated R&D investment value; and (c) reasonable royalties for ongoing use. Under Section 3426.03, Meridian is further entitled to attorney's fees and costs if the court determines that misappropriation was willful and malicious. Cal. Civ. Code \u00a7 3426.04 authorizes exemplary damages in such cases.", "style": "body"},
    ])

    # --- Page 20-21: Damages Analysis ---
    pages_content.append([
        {"text": "D. Damages Analysis", "style": "subheading"},
        {"text": "\nMeridian is entitled to substantial damages under multiple legal theories. The measure of damages for trade secret misappropriation under Cal. Civ. Code Section 3426.03 includes \"both the actual loss caused by misappropriation and the unjust enrichment caused by misappropriation that is not taken into account in computing actual loss.\" Alternatively, the court may impose a reasonable royalty.", "style": "body"},
        {"text": "\nDr. Park's damages analysis (Exhibit E) employs a three-part methodology: (1) a lost profits analysis based on Meridian's historical revenue trends and the timing of Pacific Digital's market entry; (2) a reasonable royalty calculation based on comparable technology licensing transactions in the financial software industry; and (3) an unjust enrichment analysis based on Pacific Digital's profits attributable to the misappropriated technology.", "style": "body"},
    ])

    pages_content.append([
        {"text": "1. Lost Profits\n\nMeridian's lost profits analysis identifies 23 client accounts that shifted from Meridian to Pacific Digital following the launch of FinanceFlow Pro. The aggregate annual revenue from these accounts was $18.7 million, with an average contract duration of 3.2 years. Dr. Park's analysis accounts for competitive factors, market trends, and potential client attrition unrelated to Pacific Digital's misconduct.", "style": "body"},
        {"text": "\n2. Reasonable Royalty\n\nIn the alternative, Dr. Park calculates a reasonable royalty based on the Georgia-Pacific factors. Analyzing 15 comparable technology licensing transactions, Dr. Park determines that a reasonable royalty rate for Meridian's DSAP technology would be 12.5% of Pacific Digital's gross revenue from FinanceFlow Pro. Based on Pacific Digital's projected revenue of $42 million over three years, the reasonable royalty totals $5.25 million.", "style": "body"},
    ])

    # --- Page 22: Damages continued ---
    pages_content.append([
        {"text": "3. Unjust Enrichment\n\nPacific Digital's unjust enrichment is measured by the profits it has derived and will derive from the misappropriated technology. Pacific Digital's financial projections (Exhibit F, produced in discovery) show anticipated revenues of $42 million over three years from FinanceFlow Pro, with a profit margin of 34%. Pacific Digital's unjust enrichment therefore totals approximately $14.3 million.", "style": "body"},
        {"text": "\n4. Exemplary Damages\n\nGiven the willful and malicious nature of Pacific Digital's misappropriation, Meridian requests exemplary damages under Cal. Civ. Code Section 3426.04 in an amount up to twice the compensatory damages award. The authorization for exemplary damages under \u00a7 3426.04 serves both compensatory and deterrent functions. Pacific Digital's deliberate, systematic theft of proprietary technology warrants the maximum exemplary damages to deter similar conduct.", "style": "body"},
    ])

    # --- Page 23: Injunctive Relief ---
    pages_content.append([
        {"text": "5. Injunctive Relief\n\nMeridian seeks a permanent injunction pursuant to Cal. Civ. Code Section 3426.02 and 18 U.S.C. Section 1836.03 prohibiting Pacific Digital from: (a) using, disclosing, or relying upon any of Meridian's trade secrets; (b) marketing, selling, or distributing FinanceFlow Pro or any derivative product; (c) soliciting or servicing any of Meridian's current or former clients using misappropriated technology; and (d) retaining any copies of Meridian's proprietary materials.", "style": "body"},
        {"text": "\nUnder \u00a7 3426.02, an injunction is appropriate to \"prevent[ ] any actual or threatened misappropriation.\" The ongoing availability of FinanceFlow Pro in the marketplace constitutes a continuing misappropriation that can only be remedied through injunctive relief. Monetary damages alone are insufficient because they cannot prevent the ongoing erosion of Meridian's competitive position or the continued disclosure of its trade secrets to Pacific Digital's clients and partners.", "style": "body"},
    ])

    # --- Page 24: Conclusion ---
    pages_content.append([
        {"text": "V. CONCLUSION", "style": "heading"},
        {"text": "\nFor the foregoing reasons, Meridian Technologies, Inc. respectfully requests that this Court grant summary judgment in its favor on all three claims: (1) breach of contract in violation of the MSA and Cal. Civ. Code Section 1550.05; (2) misappropriation of trade secrets under Cal. Civ. Code \u00a7 3426.01 et seq. and 18 U.S.C. Section 1836.02; and (3) unfair business practices under Cal. Bus. & Prof. Code \u00a7 17200.00.", "style": "body"},
        {"text": "\nMeridian further requests that the Court award: (a) compensatory damages in the amount of $65.7 million; (b) exemplary damages pursuant to Cal. Civ. Code Section 3426.04 in an amount up to twice the compensatory award; (c) permanent injunctive relief under Section 3426.02 and 18 U.S.C. \u00a7 1836.03; (d) attorney's fees and costs under \u00a7 3426.04; and (e) such other and further relief as the Court deems just and proper.", "style": "body"},
    ])

    # --- Page 25: Signature Block ---
    pages_content.append([
        {"text": "\nDated: January 15, 2026", "style": "body"},
        {"text": "\nRespectfully submitted,\n\nTHORNTON & ASSOCIATES LLP\n\n\n_________________________________\nElizabeth A. Thornton, Esq. (SBN 198745)\nRachel M. Vasquez, Esq. (SBN 247893)\n555 Market Street, Suite 3200\nSan Francisco, CA 94105\nTelephone: (415) 555-7890\nFacsimile: (415) 555-7891\nethornton@thorntonlaw.com\nrvasquez@thorntonlaw.com\n\nAttorneys for Plaintiff\nMeridian Technologies, Inc.", "style": "body"},
        {"text": "\n\nCERTIFICATE OF SERVICE\n\nI hereby certify that on January 15, 2026, a true and correct copy of the foregoing Plaintiff's Memorandum of Law in Support of Motion for Summary Judgment was served upon all counsel of record via the Court's ECF system, in compliance with Section 1013.01 of the California Code of Civil Procedure.", "style": "body"},
    ])

    # Generate pages
    for i, page_blocks in enumerate(pages_content):
        page = doc.new_page(width=PW, height=PH)
        add_page_text(doc, page, page_blocks, i + 1)

    doc.save(OUTPUT)
    doc.close()
    print(f"Initial file created: {OUTPUT}")

    # Verify statute references
    doc = pymupdf.open(OUTPUT)
    import re
    pattern = r'(?:Section\s+\d+\.\d+|\u00a7\s*\d+\.\d+)'
    count = 0
    for page in doc:
        text = page.get_text("text")
        matches = re.findall(pattern, text)
        count += len(matches)
    doc.close()
    print(f"Total statute references found: {count}")

    # Launch GUI
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
