"""
Initial Setup: Create a 40-page legal brief PDF
Task ID: pdf_legal_042
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_042'
LEGAL_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{LEGAL_DIR}/brief.pdf'


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
    os.makedirs(LEGAL_DIR, exist_ok=True)

    try:
        import pymupdf
    except ImportError:
        subprocess.check_call(['pip3', 'install', 'PyMuPDF'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        import pymupdf

    doc = pymupdf.open()

    # --- Legal brief content: 40 pages of realistic legal text ---
    PAGE_W, PAGE_H = 612, 792  # Letter size
    MARGIN_LEFT = 72
    MARGIN_RIGHT = 540
    MARGIN_TOP = 72
    MARGIN_BOTTOM = 720
    TEXT_WIDTH = MARGIN_RIGHT - MARGIN_LEFT

    # Sections of a realistic legal brief
    sections = [
        ("I. INTRODUCTION", [
            "Plaintiff Jennifer Smith ('Plaintiff') brings this action against Defendant Michael Jones ('Defendant') for breach of fiduciary duty, fraud, and unjust enrichment arising from Defendant's management of a joint real estate investment venture. Plaintiff seeks compensatory damages in excess of $2,500,000, punitive damages, disgorgement of profits, and such other relief as this Court deems just and proper.",
            "This case arises from a series of transactions between 2019 and 2023 in which Defendant, acting as managing partner of Pacific Coast Properties LLC ('PCP'), systematically diverted partnership funds for personal use, concealed material information from Plaintiff regarding the financial condition of partnership assets, and engaged in self-dealing transactions that were never disclosed to or approved by Plaintiff.",
            "As set forth more fully below, Defendant's conduct constitutes a clear and egregious breach of the fiduciary duties owed to Plaintiff under both the Partnership Agreement and applicable California law. The evidence will demonstrate that Defendant acted with full knowledge of his obligations and in deliberate disregard of Plaintiff's rights and interests.",
        ]),
        ("II. STATEMENT OF FACTS", [
            "A. Formation of the Partnership",
            "In January 2019, Plaintiff and Defendant entered into a written Partnership Agreement to form Pacific Coast Properties LLC, a California limited liability company organized for the purpose of acquiring, developing, and managing commercial real estate properties in the San Francisco Bay Area. Pursuant to the Partnership Agreement, each party contributed $500,000 in initial capital, and profits and losses were to be shared equally.",
            "The Partnership Agreement designated Defendant as the Managing Partner, with day-to-day authority over partnership operations, subject to certain limitations. Specifically, Section 4.2 of the Partnership Agreement required Defendant to obtain Plaintiff's written consent before executing any transaction with a value exceeding $50,000, entering into any loan or financing arrangement on behalf of the partnership, or selling or encumbering any partnership asset.",
            "B. Initial Acquisitions and Operations",
            "Between February 2019 and December 2020, PCP acquired three commercial properties: (1) a 12-unit apartment building located at 1450 Mission Street, San Francisco ('Mission Street Property'), acquired for $1,850,000; (2) a retail strip mall located at 2300 El Camino Real, Redwood City ('El Camino Property'), acquired for $2,200,000; and (3) a mixed-use development site at 890 Broadway, Oakland ('Broadway Property'), acquired for $1,400,000.",
            "During this initial period, the partnership operated profitably. Rental income from the Mission Street Property and El Camino Property generated approximately $45,000 per month in gross revenue, and Defendant provided Plaintiff with quarterly financial statements showing steady appreciation in property values and consistent positive cash flow.",
            "C. Discovery of Irregularities",
            "In March 2022, Plaintiff began to notice discrepancies in the quarterly financial reports. Specifically, the reported rental income for the Mission Street Property had declined by approximately 30% despite full occupancy, and several large expense items were listed without adequate documentation or explanation. When Plaintiff requested supporting documentation for these expenses, Defendant was evasive and delayed providing the requested materials for over three months.",
            "In June 2022, Plaintiff retained the forensic accounting firm of Henderson & Associates to conduct an independent review of partnership financial records. The Henderson Report, completed in September 2022, revealed numerous irregularities, including unauthorized transfers totaling $387,000 from partnership accounts to Defendant's personal bank account, payments of $215,000 to Coastal Development Corp., a company wholly owned by Defendant's spouse, and systematic overcharging of management fees in excess of the amounts permitted under the Partnership Agreement.",
            "D. Confrontation and Defendant's Response",
            "Upon receiving the Henderson Report, Plaintiff confronted Defendant at a meeting on October 15, 2022. Defendant initially denied any wrongdoing but subsequently admitted to 'borrowing' funds from the partnership, claiming he intended to repay the amounts with interest. Defendant refused to provide a complete accounting or to agree to an independent audit of all partnership transactions.",
            "E. Subsequent Events",
            "Following the October 2022 meeting, Defendant took several actions that further damaged Plaintiff's interests. Without Plaintiff's knowledge or consent, Defendant refinanced the Mission Street Property, extracting $400,000 in equity and using the proceeds for purposes unrelated to partnership business. Defendant also entered into a below-market lease with a tenant at the El Camino Property who was later identified as Defendant's business associate.",
            "In February 2023, Plaintiff discovered that Defendant had listed the Broadway Property for sale at $1,200,000, which was substantially below its appraised value of $1,800,000, without notifying Plaintiff or obtaining the required consent under Section 4.2 of the Partnership Agreement.",
        ]),
        ("III. LEGAL STANDARD", [
            "A. Breach of Fiduciary Duty",
            "Under California law, partners owe each other the highest duty of loyalty and good faith. Leff v. Gunter, 33 Cal.3d 508, 514 (1983). A managing partner occupies a position of trust and confidence and is held to the standards of a trustee in dealings with the partnership and its assets. Jones v. H.F. Ahmanson & Co., 1 Cal.3d 93, 108 (1969).",
            "The fiduciary duty of loyalty requires a partner to account to the partnership for any property, profit, or benefit derived by the partner in the conduct of the partnership business or from a use by the partner of partnership property. Cal. Corp. Code § 16404(b)(1). A partner must refrain from dealing with the partnership as or on behalf of a party having an interest adverse to the partnership. Cal. Corp. Code § 16404(b)(2).",
            "A breach of fiduciary duty claim requires proof of: (1) the existence of a fiduciary relationship; (2) breach of the fiduciary duty; (3) damages proximately caused by the breach; and (4) the defendant's knowledge of the fiduciary duty. Pierce v. Lyman, 1 Cal.App.4th 1093, 1101 (1991).",
            "B. Fraud and Concealment",
            "The elements of fraud under California law are: (1) misrepresentation; (2) knowledge of falsity (scienter); (3) intent to defraud; (4) justifiable reliance; and (5) resulting damage. Lazar v. Superior Court, 12 Cal.4th 631, 638 (1996). Concealment is a species of fraud in which the defendant suppresses a material fact that the defendant is bound to disclose. Marketing West, Inc. v. Sanyo Fisher Co., 6 Cal.App.4th 603, 612-613 (1992).",
            "Where a fiduciary relationship exists, the fiduciary has an affirmative duty to make full disclosure of all material facts within the fiduciary's knowledge. Failure to disclose material facts constitutes constructive fraud. Cal. Civ. Code § 1573. The burden of proof shifts to the fiduciary to show the transaction was fair and the beneficiary's consent was informed. Vai v. Bank of America, 56 Cal.2d 329, 338 (1961).",
            "C. Unjust Enrichment",
            "Under California law, unjust enrichment is not a standalone cause of action but rather describes 'the result of a failure to make restitution under circumstances where it is equitable to do so.' Lauriedale Associates, Ltd. v. Wilson, 7 Cal.App.4th 1439, 1448 (1992). A claim for restitution based on unjust enrichment requires that the defendant has been unjustly enriched at the expense of the plaintiff and that it would be inequitable to allow the defendant to retain the benefit. First Nationwide Savings v. Perry, 11 Cal.App.4th 1657, 1662-1663 (1992).",
        ]),
        ("IV. ARGUMENT", [
            "A. Defendant Breached His Fiduciary Duties to Plaintiff",
            "1. Defendant's Unauthorized Transfers Constitute Breach of the Duty of Loyalty",
            "The evidence demonstrates that Defendant transferred a total of $387,000 from partnership accounts to his personal bank account without authorization, disclosure, or legitimate business purpose. These transfers constitute a per se violation of the duty of loyalty owed by a managing partner under California law. See Cal. Corp. Code § 16404(b)(1) (requiring a partner to account for any benefit derived from partnership property).",
            "Defendant's claim that these transfers were 'loans' that he intended to repay does not excuse the breach. A fiduciary may not unilaterally appropriate partnership funds for personal use, regardless of intent to repay. Estate of Gump, 16 Cal.App.2d 1, 27 (1936) ('A trustee who uses trust property for his own benefit is guilty of a breach of trust even though he intends to restore the property.').",
            "2. Defendant's Self-Dealing Transactions Were Not Disclosed or Authorized",
            "The payments of $215,000 to Coastal Development Corp., a company wholly owned by Defendant's spouse, constitute prohibited self-dealing under Section 16404(b)(2) of the California Corporations Code. Defendant had a direct personal interest in these transactions, as any payments to Coastal Development Corp. benefited Defendant's immediate family.",
            "Moreover, Defendant failed to disclose these transactions to Plaintiff, as required by both the Partnership Agreement and the duty of candor inherent in the fiduciary relationship. The Partnership Agreement expressly required Defendant to disclose any potential conflicts of interest and to obtain Plaintiff's written consent before engaging in any transaction in which Defendant had a personal interest. Defendant's failure to comply with these requirements renders the transactions voidable at Plaintiff's election.",
            "3. Defendant's Overcharging of Management Fees Constitutes Breach of Contract and Fiduciary Duty",
            "The Henderson Report documented that Defendant systematically charged management fees in excess of the 8% of gross revenue permitted under Section 6.1 of the Partnership Agreement. Over the period from January 2020 through December 2022, Defendant overcharged approximately $124,000 in management fees, representing a 35% excess over the contractually authorized amount.",
            "B. Defendant Committed Fraud and Constructive Fraud",
            "1. Affirmative Misrepresentations",
            "Defendant's quarterly financial statements contained numerous material misrepresentations, including overstated rental income, understated expenses, and omission of unauthorized transfers and self-dealing transactions. Defendant prepared and delivered these statements with knowledge that they were false and with the intent to prevent Plaintiff from discovering the true financial condition of the partnership.",
            "2. Fraudulent Concealment",
            "In addition to affirmative misrepresentations, Defendant actively concealed material facts from Plaintiff. Defendant concealed the transfers to his personal account, the payments to Coastal Development Corp., the refinancing of the Mission Street Property, and the below-market lease at the El Camino Property. As a fiduciary, Defendant had an affirmative duty to disclose each of these facts. His failure to do so constitutes constructive fraud under Civil Code § 1573.",
            "C. Defendant Has Been Unjustly Enriched at Plaintiff's Expense",
            "Through the unauthorized transfers, self-dealing transactions, and excessive management fees described above, Defendant has been unjustly enriched by no less than $726,000 at Plaintiff's expense. Equity requires that Defendant disgorge these amounts and make full restitution to Plaintiff.",
            "D. Plaintiff Is Entitled to Punitive Damages",
            "Under California Civil Code § 3294, punitive damages may be awarded where the defendant has been guilty of oppression, fraud, or malice. The evidence demonstrates that Defendant acted with conscious disregard of Plaintiff's rights and engaged in deliberate fraud over a period of years. Defendant's conduct was not merely negligent; it was intentional, systematic, and designed to enrich Defendant at Plaintiff's direct expense.",
            "The Supreme Court has recognized that punitive damages serve the dual purposes of punishment and deterrence. State Farm Mutual Automobile Insurance Co. v. Campbell, 538 U.S. 408, 416 (2003). Here, the egregious and prolonged nature of Defendant's misconduct warrants a substantial award of punitive damages.",
        ]),
        ("V. DAMAGES", [
            "Plaintiff has suffered damages as follows:",
            "1. Unauthorized transfers from partnership accounts: $387,000",
            "2. Self-dealing payments to Coastal Development Corp.: $215,000",
            "3. Excessive management fees: $124,000",
            "4. Loss of equity from unauthorized refinancing: $400,000",
            "5. Diminished value from below-market lease: estimated $180,000",
            "6. Lost profits and opportunity costs: to be determined at trial",
            "Total quantified damages to date: $1,306,000",
            "In addition, Plaintiff seeks consequential damages for lost investment opportunities, interest on improperly diverted funds, costs of the forensic accounting investigation ($85,000), and attorneys' fees as permitted under the Partnership Agreement and applicable law.",
            "Plaintiff also seeks disgorgement of any profits Defendant obtained through his breaches of fiduciary duty, pursuant to California Corporations Code § 16404(b)(1) and the equitable principles governing fiduciary relationships.",
        ]),
        ("VI. CONCLUSION", [
            "For the foregoing reasons, Plaintiff Jennifer Smith respectfully requests that this Court enter judgment in her favor and against Defendant Michael Jones, and award the following relief:",
            "1. Compensatory damages in an amount to be proven at trial, but not less than $1,306,000;",
            "2. Punitive damages in an amount sufficient to punish Defendant and deter similar conduct;",
            "3. Disgorgement of all profits obtained by Defendant through breach of fiduciary duty;",
            "4. A full accounting of all partnership transactions from inception through the present;",
            "5. Attorneys' fees and costs of suit as permitted by law and the Partnership Agreement;",
            "6. Pre-judgment and post-judgment interest at the maximum rate permitted by law; and",
            "7. Such other and further relief as this Court deems just and proper.",
            "Dated: March 15, 2024",
            "Respectfully submitted,",
            "CHEN, RODRIGUEZ & PATEL LLP",
            "By: _________________________",
            "    Amanda Chen, Esq. (SBN 287654)",
            "    1200 Market Street, Suite 1800",
            "    San Francisco, California 94103",
            "    Telephone: (415) 555-0147",
            "    Facsimile: (415) 555-0148",
            "    Email: achen@crplaw.com",
            "    Attorneys for Plaintiff Jennifer Smith",
        ]),
    ]

    # Helper to add a page with text content
    def add_content_page(doc, texts, page_num, start_y=MARGIN_TOP):
        """Add text content to a new page, returns excess texts that didn't fit."""
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        y = start_y
        remaining = []
        overflow = False

        for text in texts:
            if overflow:
                remaining.append(text)
                continue

            # Check if it looks like a section heading
            is_heading = (text.startswith(('I.', 'II.', 'III.', 'IV.', 'V.', 'VI.', 'VII.'))
                         and len(text) < 80)
            is_subheading = (text.startswith(('A.', 'B.', 'C.', 'D.', 'E.'))
                           and len(text) < 80) or (text.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.'))
                           and len(text) < 100 and not text[2:].strip().startswith('$'))

            if is_heading:
                if y > MARGIN_BOTTOM - 60:
                    remaining.append(text)
                    overflow = True
                    continue
                y += 20
                page.insert_text(pymupdf.Point(MARGIN_LEFT, y),
                               text, fontsize=14, fontname="tibo", color=(0, 0, 0))
                y += 24
            elif is_subheading:
                if y > MARGIN_BOTTOM - 40:
                    remaining.append(text)
                    overflow = True
                    continue
                y += 14
                page.insert_text(pymupdf.Point(MARGIN_LEFT + 18, y),
                               text, fontsize=12, fontname="tibo", color=(0, 0, 0))
                y += 18
            else:
                rect = pymupdf.Rect(MARGIN_LEFT, y, MARGIN_RIGHT, MARGIN_BOTTOM)
                if rect.height < 30:
                    remaining.append(text)
                    overflow = True
                    continue
                excess = page.insert_textbox(
                    rect, text,
                    fontsize=11, fontname="tiro", color=(0, 0, 0),
                    align=pymupdf.TEXT_ALIGN_JUSTIFY,
                )
                # Estimate how much vertical space was used
                lines_approx = max(1, len(text) / 75)
                space_used = lines_approx * 15
                y += space_used + 8

                if y > MARGIN_BOTTOM - 20:
                    overflow = True

        # Add page number at bottom center
        page.insert_text(pymupdf.Point(PAGE_W / 2 - 10, PAGE_H - 36),
                        str(page_num), fontsize=10, fontname="tiro", color=(0, 0, 0))

        return remaining

    # Build all text blocks into a flat list
    all_texts = []
    for section_title, paragraphs in sections:
        all_texts.append(section_title)
        all_texts.extend(paragraphs)

    # Generate pages from content
    page_num = 1
    remaining = list(all_texts)
    while remaining and page_num <= 40:
        remaining = add_content_page(doc, remaining, page_num)
        page_num += 1

    # Fill remaining pages with continuation legal content if needed
    filler_paragraphs = [
        "The Court should also consider the well-established principle that where a fiduciary has profited from a breach of duty, the beneficiary may elect to recover either the loss suffered or the profit gained, whichever is greater. Merryman v. Borg, 163 Cal. 625, 631 (1912). This principle ensures that fiduciaries cannot profit from their wrongdoing.",
        "Furthermore, the Restatement (Third) of Agency § 8.01 provides that an agent has a fiduciary obligation to act loyally for the principal's benefit in all matters connected with the agency relationship. This duty encompasses obligations of candor, care, and non-competition that apply with full force to the managing partner of a limited liability company.",
        "Courts in this jurisdiction have consistently held that the duty of loyalty is the most fundamental fiduciary obligation. A partner who engages in self-dealing, misappropriation, or concealment of material facts acts at his peril and may be held liable for all damages flowing from the breach, including consequential damages and, where appropriate, punitive damages.",
        "The measure of damages for breach of fiduciary duty is the amount necessary to restore the beneficiary to the position he or she would have occupied but for the breach. This includes both direct losses and consequential damages that were reasonably foreseeable at the time of the breach. Fragale v. Faulkner, 110 Cal.App.3d 434, 452 (1980).",
        "Where the fiduciary has engaged in self-dealing, the burden of proving the fairness of the transaction shifts to the fiduciary. Vai v. Bank of America, 56 Cal.2d 329, 338 (1961). Defendant bears the burden of demonstrating that each of the challenged transactions was fair, was fully disclosed, and was entered into with Plaintiff's informed consent. Defendant cannot meet this burden.",
        "The doctrine of constructive trust provides an additional remedy available to Plaintiff. Where a person holding title to property is subject to an equitable duty to convey it to another on the ground that the holder would be unjustly enriched if permitted to retain it, a constructive trust is imposed. Burlesci v. Petersen, 68 Cal.App.2d 1, 5 (1945).",
        "In the present case, Defendant holds partnership funds and property that were obtained through breach of fiduciary duty and fraud. Equity demands that a constructive trust be imposed over these assets for the benefit of Plaintiff and the partnership. This remedy is particularly appropriate where, as here, monetary damages may be insufficient to fully compensate Plaintiff for the injury suffered.",
        "Plaintiff also notes that the applicable statute of limitations does not bar any of her claims. The discovery rule tolls the statute of limitations until the plaintiff discovers, or has reason to discover, the cause of action. Neel v. Magana, Olney, Levy, Cathcart & Gelfand, 6 Cal.3d 176, 187 (1971). Here, Plaintiff did not discover the full extent of Defendant's misconduct until September 2022, when she received the Henderson Report.",
        "Additionally, Defendant's active concealment of his wrongdoing constitutes fraudulent concealment that tolls the statute of limitations. Where a defendant engages in conduct designed to prevent the plaintiff from discovering the cause of action, the defendant is estopped from asserting the statute of limitations as a defense. Bernson v. Browning-Ferris Industries, 7 Cal.4th 926, 931 (1994).",
        "The Court should further consider the public policy implications of permitting fiduciaries to profit from their breaches of duty. If Defendant is permitted to retain the fruits of his misconduct, it would send a message that managing partners may treat partnership assets as their personal funds with impunity, knowing that the worst consequence would be an order to repay what was taken.",
        "Such a result would be contrary to the fundamental purposes of fiduciary law, which are to ensure the integrity of relationships of trust and confidence and to provide effective deterrents against their abuse. The imposition of punitive damages in this case would serve these salutary purposes and would reinforce the principle that fiduciaries must act with the utmost good faith and loyalty.",
        "In support of her request for punitive damages, Plaintiff notes that Defendant's net worth, as reflected in financial disclosures obtained through discovery, exceeds $4,000,000. An award of punitive damages should bear a reasonable relationship to the compensatory damages awarded and to the defendant's ability to pay. Adams v. Murakami, 54 Cal.3d 105, 110 (1991).",
        "Based on the evidence presented, Plaintiff respectfully submits that an award of punitive damages in the range of $2,000,000 to $3,000,000 would be appropriate to punish Defendant for his egregious conduct and to deter similar misconduct in the future.",
        "APPENDIX A: CHRONOLOGY OF KEY EVENTS",
        "January 15, 2019 - Partnership Agreement executed; PCP LLC formed",
        "February 28, 2019 - Acquisition of Mission Street Property ($1,850,000)",
        "August 15, 2019 - Acquisition of El Camino Property ($2,200,000)",
        "December 10, 2020 - Acquisition of Broadway Property ($1,400,000)",
        "March 2022 - Plaintiff first notices financial discrepancies",
        "June 2022 - Plaintiff retains Henderson & Associates for forensic audit",
        "September 2022 - Henderson Report completed and delivered",
        "October 15, 2022 - Meeting between Plaintiff and Defendant",
        "November 2022 - Defendant refinances Mission Street Property without consent",
        "January 2023 - Below-market lease executed at El Camino Property",
        "February 2023 - Broadway Property listed for sale without Plaintiff's consent",
        "March 15, 2024 - Filing of the present action",
        "APPENDIX B: SUMMARY OF FINANCIAL IRREGULARITIES",
        "Category 1: Unauthorized Personal Transfers",
        "Transfer Date: March 15, 2020 - Amount: $45,000 - From: PCP Operating Account - To: M. Jones Personal Checking",
        "Transfer Date: June 22, 2020 - Amount: $62,000 - From: PCP Operating Account - To: M. Jones Personal Savings",
        "Transfer Date: October 8, 2020 - Amount: $38,000 - From: PCP Reserve Account - To: M. Jones Personal Checking",
        "Transfer Date: February 14, 2021 - Amount: $55,000 - From: PCP Operating Account - To: M. Jones Personal Checking",
        "Transfer Date: May 30, 2021 - Amount: $72,000 - From: PCP Revenue Account - To: M. Jones Personal Savings",
        "Transfer Date: September 12, 2021 - Amount: $48,000 - From: PCP Operating Account - To: M. Jones Personal Checking",
        "Transfer Date: January 25, 2022 - Amount: $67,000 - From: PCP Reserve Account - To: M. Jones Personal Savings",
        "Total Unauthorized Transfers: $387,000",
        "Category 2: Payments to Coastal Development Corp.",
        "Invoice Date: April 2020 - Description: 'Consulting Services' - Amount: $35,000",
        "Invoice Date: August 2020 - Description: 'Project Management' - Amount: $42,000",
        "Invoice Date: December 2020 - Description: 'Site Assessment' - Amount: $28,000",
        "Invoice Date: March 2021 - Description: 'Development Planning' - Amount: $38,000",
        "Invoice Date: July 2021 - Description: 'Consulting Services' - Amount: $45,000",
        "Invoice Date: November 2021 - Description: 'Project Oversight' - Amount: $27,000",
        "Total Coastal Development Corp. Payments: $215,000",
        "Category 3: Excessive Management Fees",
        "Quarter ending March 2020: Authorized fee $10,800 - Charged: $14,600 - Excess: $3,800",
        "Quarter ending June 2020: Authorized fee $11,200 - Charged: $15,100 - Excess: $3,900",
        "Quarter ending September 2020: Authorized fee $11,400 - Charged: $16,200 - Excess: $4,800",
        "Quarter ending December 2020: Authorized fee $12,000 - Charged: $17,500 - Excess: $5,500",
        "Quarter ending March 2021: Authorized fee $12,200 - Charged: $18,100 - Excess: $5,900",
        "Quarter ending June 2021: Authorized fee $12,600 - Charged: $19,200 - Excess: $6,600",
        "Quarter ending September 2021: Authorized fee $12,800 - Charged: $20,500 - Excess: $7,700",
        "Quarter ending December 2021: Authorized fee $13,200 - Charged: $21,800 - Excess: $8,600",
        "Quarter ending March 2022: Authorized fee $13,500 - Charged: $23,000 - Excess: $9,500",
        "Quarter ending June 2022: Authorized fee $13,800 - Charged: $24,200 - Excess: $10,400",
        "Total Excessive Management Fees: $124,000 (estimate subject to refinement at trial)",
        "APPENDIX C: EXPERT WITNESS DISCLOSURES",
        "1. Robert Henderson, CPA, CFE - Henderson & Associates - Forensic accounting expert who will testify regarding the nature and extent of financial irregularities identified in the Henderson Report, the total amount of funds diverted from partnership accounts, and the methodology used to trace partnership funds.",
        "2. Dr. Patricia Nguyen, Ph.D. - Professor of Finance, Stanford University - Valuation expert who will testify regarding the fair market value of partnership properties, the diminution in value caused by Defendant's mismanagement, and the lost profits attributable to Defendant's breach of fiduciary duty.",
        "3. James Morrison, MAI - Morrison Real Estate Appraisals - Real property appraiser who will testify regarding the current fair market value of the Mission Street Property, El Camino Property, and Broadway Property, and the impact of the unauthorized refinancing and below-market lease on property values.",
        "CERTIFICATE OF SERVICE",
        "I hereby certify that on March 15, 2024, a true and correct copy of the foregoing MEMORANDUM OF POINTS AND AUTHORITIES was served on the following by electronic service through the Court's CM/ECF system:",
        "David R. Thompson, Esq.",
        "THOMPSON & WALKER LLP",
        "555 Montgomery Street, Suite 2200",
        "San Francisco, California 94111",
        "dthompson@twlaw.com",
        "Attorneys for Defendant Michael Jones",
        "/s/ Amanda Chen",
        "Amanda Chen, Esq.",
    ]

    while page_num <= 40:
        batch_size = min(4, len(filler_paragraphs))
        if batch_size == 0:
            # Generate a blank page with just page number if we run out
            page = doc.new_page(width=PAGE_W, height=PAGE_H)
            page.insert_text(pymupdf.Point(PAGE_W / 2 - 10, PAGE_H - 36),
                           str(page_num), fontsize=10, fontname="tiro", color=(0, 0, 0))
            page_num += 1
            continue

        batch = filler_paragraphs[:batch_size]
        filler_paragraphs = filler_paragraphs[batch_size:]
        remaining_batch = add_content_page(doc, batch, page_num)
        # If there was overflow, put it back
        filler_paragraphs = remaining_batch + filler_paragraphs
        page_num += 1

    # Ensure exactly 40 pages
    while doc.page_count < 40:
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        pn = doc.page_count
        page.insert_text(pymupdf.Point(PAGE_W / 2 - 10, PAGE_H - 36),
                        str(pn), fontsize=10, fontname="tiro", color=(0, 0, 0))

    # If we overshot, trim to 40
    while doc.page_count > 40:
        doc.delete_page(doc.page_count - 1)

    doc.save(OUTPUT)
    doc.close()

    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 40')

    # GUI-ready: open the brief in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
