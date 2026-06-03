"""
Initial Setup: Create five closing documents for a real estate transaction
Task ID: pdf_legal_034
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_034'
CLOSING_DIR = f'{WORKDIR}/legal/closing'


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


def add_legal_text(page, title, paragraphs, start_y=72):
    """Add legal document text to a page with title and body paragraphs."""
    y = start_y
    # Title
    page.insert_text(pymupdf.Point(72, y), title, fontsize=16, fontname="hebo", color=(0, 0, 0))
    y += 30
    # Horizontal rule
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(523, y))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()
    y += 20
    # Body paragraphs
    for para in paragraphs:
        rect = pymupdf.Rect(72, y, 523, y + 200)
        excess = page.insert_textbox(rect, para, fontsize=10, fontname="helv",
                                     color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 200 - max(excess, 0)
        if y > 750:
            break
    return y


def create_deed():
    """Create a 4-page warranty deed document."""
    doc = pymupdf.open()

    # Page 1 - Cover/Header
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(200, 80), "WARRANTY DEED", fontsize=22, fontname="hebo", color=(0, 0, 0.4))
    page.insert_text(pymupdf.Point(72, 130), "State of California", fontsize=12, fontname="helv")
    page.insert_text(pymupdf.Point(72, 150), "County of Santa Clara", fontsize=12, fontname="helv")
    page.insert_text(pymupdf.Point(72, 190), "Recording Requested By:", fontsize=10, fontname="hebo")
    page.insert_text(pymupdf.Point(72, 210), "Pacific Coast Title Company", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 230), "1250 Oakmead Parkway, Suite 100", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 250), "Sunnyvale, CA 94085", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 290), "Document Number: WD-2025-0847291", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 310), "Recording Date: March 15, 2025", fontsize=10, fontname="helv")

    body = ("THIS DEED, made this 15th day of March, 2025, between GRANTOR: Robert James Mitchell "
            "and Catherine Anne Mitchell, husband and wife, of 4872 Redwood Lane, Palo Alto, CA 94301, "
            "and GRANTEE: David Chen and Lisa Marie Chen, husband and wife, as joint tenants, "
            "of 1923 Elm Street, Mountain View, CA 94041.")
    rect = pymupdf.Rect(72, 350, 540, 550)
    page.insert_textbox(rect, body, fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    witnesseth = ("WITNESSETH, that the said Grantor, for and in consideration of the sum of ONE MILLION "
                  "EIGHT HUNDRED FIFTY THOUSAND DOLLARS ($1,850,000.00) lawful money of the United States "
                  "of America, to Grantor in hand paid by the said Grantee, the receipt whereof is hereby "
                  "acknowledged, does by these presents grant, bargain, sell, convey, and confirm unto the "
                  "said Grantee, and to the Grantee's heirs and assigns forever, all that certain lot, piece, "
                  "or parcel of land situate in the County of Santa Clara, State of California, described as follows:")
    rect2 = pymupdf.Rect(72, 560, 540, 760)
    page.insert_textbox(rect2, witnesseth, fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 2 - Legal Description
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(pymupdf.Point(72, 60), "LEGAL DESCRIPTION", fontsize=14, fontname="hebo")
    legal_desc = ("Lot 47 of Tract No. 9823, as per map recorded in Book 342 of Maps, Pages 15 through 18, "
                  "inclusive, in the Office of the County Recorder of Santa Clara County, California. "
                  "APN: 167-42-089. Located at 4872 Redwood Lane, Palo Alto, California 94301. "
                  "TOGETHER WITH all and singular the tenements, hereditaments, and appurtenances thereunto "
                  "belonging or in anywise appertaining, and the reversion and reversions, remainder and "
                  "remainders, rents, issues, and profits thereof.")
    rect = pymupdf.Rect(72, 90, 540, 300)
    page2.insert_textbox(rect, legal_desc, fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    covenants = ("TO HAVE AND TO HOLD the said premises, together with the appurtenances, unto the said "
                 "Grantee, and to the Grantee's heirs and assigns forever. And the said Grantor, for Grantor "
                 "and Grantor's heirs, executors, and administrators, does covenant, promise, and agree to and "
                 "with the said Grantee, and the Grantee's heirs and assigns, that at the time of the ensealing "
                 "and delivery of these presents, Grantor is well seized of the premises above conveyed, as of "
                 "a good, sure, perfect, absolute, and indefeasible estate of inheritance, in the law, in fee simple, "
                 "and has good right, full power, and lawful authority to grant, bargain, sell, and convey the same "
                 "in manner and form aforesaid.")
    rect2 = pymupdf.Rect(72, 320, 540, 550)
    page2.insert_textbox(rect2, covenants, fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 3 - Additional Covenants
    page3 = doc.new_page(width=612, height=792)
    page3.insert_text(pymupdf.Point(72, 60), "ADDITIONAL COVENANTS AND EXCEPTIONS", fontsize=14, fontname="hebo")
    addl = ("This conveyance is subject to: (1) General and special real property taxes and assessments for "
            "the fiscal year 2025-2026, a lien not yet due or payable; (2) Covenants, conditions, restrictions, "
            "reservations, rights, rights of way, and easements of record, if any; (3) Any state of facts which "
            "an accurate survey or physical inspection of the property would disclose; (4) Building and zoning "
            "regulations and ordinances of the City of Palo Alto and Santa Clara County; (5) The lien of any "
            "supplemental taxes assessed pursuant to California Revenue and Taxation Code Section 75 et seq.")
    rect = pymupdf.Rect(72, 90, 540, 350)
    page3.insert_textbox(rect, addl, fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    env_disc = ("ENVIRONMENTAL DISCLOSURE: To the best of Grantor's knowledge, there are no hazardous "
                "substances, pollutants, or contaminants present on, under, or about the property. Grantor has "
                "not received any notice from any governmental authority regarding any environmental condition "
                "affecting the property. The property has not been used for industrial purposes or waste disposal.")
    rect2 = pymupdf.Rect(72, 370, 540, 550)
    page3.insert_textbox(rect2, env_disc, fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 4 - Signatures
    page4 = doc.new_page(width=612, height=792)
    page4.insert_text(pymupdf.Point(72, 60), "IN WITNESS WHEREOF", fontsize=14, fontname="hebo")
    witness = ("IN WITNESS WHEREOF, the said Grantor has hereunto set Grantor's hand and seal the day and "
               "year first above written.")
    rect = pymupdf.Rect(72, 90, 540, 160)
    page4.insert_textbox(rect, witness, fontsize=10, fontname="helv")

    page4.insert_text(pymupdf.Point(72, 200), "____________________________________", fontsize=10, fontname="helv")
    page4.insert_text(pymupdf.Point(72, 220), "Robert James Mitchell, Grantor", fontsize=10, fontname="helv")
    page4.insert_text(pymupdf.Point(72, 270), "____________________________________", fontsize=10, fontname="helv")
    page4.insert_text(pymupdf.Point(72, 290), "Catherine Anne Mitchell, Grantor", fontsize=10, fontname="helv")

    page4.insert_text(pymupdf.Point(72, 350), "STATE OF CALIFORNIA", fontsize=11, fontname="hebo")
    page4.insert_text(pymupdf.Point(72, 370), "COUNTY OF SANTA CLARA", fontsize=11, fontname="hebo")
    notary = ("On March 15, 2025, before me, Jennifer L. Nakamura, a Notary Public in and for said County "
              "and State, personally appeared Robert James Mitchell and Catherine Anne Mitchell, known to me "
              "to be the persons whose names are subscribed to the within instrument and acknowledged to me "
              "that they executed the same in their authorized capacities.")
    rect3 = pymupdf.Rect(72, 400, 540, 550)
    page4.insert_textbox(rect3, notary, fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page4.insert_text(pymupdf.Point(72, 580), "____________________________________", fontsize=10, fontname="helv")
    page4.insert_text(pymupdf.Point(72, 600), "Jennifer L. Nakamura, Notary Public", fontsize=10, fontname="helv")
    page4.insert_text(pymupdf.Point(72, 620), "Commission No. 2347891", fontsize=10, fontname="helv")
    page4.insert_text(pymupdf.Point(72, 640), "My Commission Expires: December 31, 2027", fontsize=10, fontname="helv")

    path = f'{CLOSING_DIR}/deed.pdf'
    doc.save(path)
    doc.close()
    print(f'Created: {path} ({4} pages)')


def create_mortgage():
    """Create a 15-page mortgage agreement document."""
    doc = pymupdf.open()

    sections = [
        ("MORTGAGE AGREEMENT", [
            "This Mortgage Agreement ('Agreement') is entered into as of March 15, 2025, by and between:",
            "BORROWER: David Chen and Lisa Marie Chen, husband and wife, whose principal address is "
            "4872 Redwood Lane, Palo Alto, CA 94301 ('Borrower').",
            "LENDER: First National Savings Bank, a federally chartered savings bank organized under the "
            "laws of the United States of America, having its principal office at 500 Market Street, "
            "San Francisco, CA 94105 ('Lender').",
            "PROPERTY ADDRESS: 4872 Redwood Lane, Palo Alto, California 94301.",
            "LOAN AMOUNT: One Million Four Hundred Eighty Thousand Dollars ($1,480,000.00).",
            "LOAN NUMBER: FNS-2025-7834291.",
        ]),
        ("ARTICLE I: DEFINITIONS", [
            "Section 1.1 - 'Note' means the promissory note executed by Borrower and payable to the order "
            "of Lender in the principal amount of $1,480,000.00, dated March 15, 2025.",
            "Section 1.2 - 'Property' means that certain real property located in Santa Clara County, "
            "California, as more particularly described in Exhibit A attached hereto.",
            "Section 1.3 - 'Hazard Insurance' means insurance against loss by fire, hazards included within "
            "the term 'extended coverage,' and any other hazards for which Lender requires insurance.",
            "Section 1.4 - 'Escrow Items' means those items described in Section 3.3 hereof.",
            "Section 1.5 - 'Applicable Law' means all controlling applicable federal, state, and local "
            "statutes, regulations, ordinances, and administrative rules and orders.",
        ]),
        ("ARTICLE II: GRANTING CLAUSE", [
            "Borrower hereby mortgages, grants, and conveys to Lender the Property described in Exhibit A, "
            "together with all improvements now or hereafter erected on the property, all easements, "
            "appurtenances, and fixtures now or hereafter a part of the property.",
            "This Security Instrument secures to Lender: (a) the repayment of the Loan, and all renewals, "
            "extensions, and modifications of the Note; (b) the payment of all other sums, with interest, "
            "advanced under this Security Instrument; and (c) the performance of Borrower's covenants and "
            "agreements under this Security Instrument and the Note.",
        ]),
        ("ARTICLE III: BORROWER'S COVENANTS", [
            "Section 3.1 - Payment of Principal and Interest. Borrower shall pay when due the principal of, "
            "and interest on, the debt evidenced by the Note. Monthly payments shall be $7,842.36, commencing "
            "on May 1, 2025, and continuing on the first day of each month thereafter for a period of thirty "
            "(30) years, with a final maturity date of April 1, 2055.",
            "Section 3.2 - Funds for Escrow Items. Borrower shall pay to Lender on the day Installments of "
            "principal and interest are payable under the Note, until the Note is paid in full, a sum "
            "('Funds') to provide for payment of amounts due for: (a) taxes and assessments; (b) leasehold "
            "payments or ground rents; (c) premiums for Hazard Insurance; (d) premiums for Mortgage Insurance.",
            "Section 3.3 - Application of Funds. Unless applicable law requires otherwise, Lender shall apply "
            "the Funds to pay the Escrow Items no later than the time specified under RESPA.",
            "Section 3.4 - Charges and Liens. Borrower shall pay all taxes, assessments, charges, fines, and "
            "impositions attributable to the Property which can attain priority over this Security Instrument.",
        ]),
        ("ARTICLE IV: HAZARD AND PROPERTY INSURANCE", [
            "Section 4.1 - Borrower shall keep the improvements now existing or hereafter erected on the "
            "Property insured against loss by fire, hazards included within the term 'extended coverage,' "
            "and any other hazards including floods, for which Lender requires insurance.",
            "Section 4.2 - The insurance carrier providing the insurance shall be chosen by Borrower subject "
            "to Lender's right to disapprove Borrower's choice, which right shall not be exercised unreasonably.",
            "Section 4.3 - All insurance policies required by Lender and renewals of such policies shall be "
            "subject to Lender's right to disapprove such policies, shall include a standard mortgage clause, "
            "and shall name Lender as mortgagee and/or as an additional loss payee.",
        ]),
        ("ARTICLE V: PRESERVATION AND MAINTENANCE OF PROPERTY", [
            "Section 5.1 - Borrower shall not destroy, damage, or impair the Property, allow the Property to "
            "deteriorate, or commit waste on the Property. Borrower shall maintain the Property in good repair.",
            "Section 5.2 - If a condemnation or other proceeding that may significantly affect Lender's interest "
            "in the Property is commenced, Borrower shall give prompt notice to Lender.",
            "Section 5.3 - Borrower shall be in compliance with all governmental health, safety, and environmental "
            "requirements applicable to the Property, and shall not cause or permit the presence, use, disposal, "
            "storage, or release of any Hazardous Substances on, under, or about the Property.",
        ]),
        ("ARTICLE VI: DEFAULT AND REMEDIES", [
            "Section 6.1 - Events of Default. The following events shall constitute events of default: "
            "(a) failure to pay any installment when due; (b) breach of any covenant or condition contained "
            "in this Security Instrument; (c) filing of a petition in bankruptcy by or against Borrower; "
            "(d) appointment of a receiver for Borrower's property.",
            "Section 6.2 - Acceleration. Upon an event of default, Lender may declare the entire unpaid principal "
            "balance of the Note, together with all accrued interest, immediately due and payable.",
            "Section 6.3 - Foreclosure. If the default is not cured within thirty (30) days of written notice, "
            "Lender may invoke the power of sale or any other remedies permitted by Applicable Law.",
            "Section 6.4 - Borrower's Right to Reinstate. Notwithstanding Lender's acceleration of the sums "
            "secured by this Security Instrument, Borrower shall have the right to have enforcement of this "
            "Security Instrument discontinued at any time prior to the earliest of certain conditions.",
        ]),
        ("ARTICLE VII: TRANSFER OF PROPERTY / DUE ON SALE", [
            "Section 7.1 - If all or any part of the Property or any interest in the Property is sold or "
            "transferred without Lender's prior written consent, Lender may require immediate payment in "
            "full of all sums secured by this Security Instrument.",
            "Section 7.2 - Exceptions. The prohibition in Section 7.1 shall not apply to: (a) a transfer "
            "by devise, descent, or operation of law on the death of a joint tenant; (b) a transfer to a "
            "relative resulting from the death of a Borrower; (c) a transfer where the spouse or children "
            "of the Borrower become an owner of the Property.",
        ]),
        ("ARTICLE VIII: MISCELLANEOUS PROVISIONS", [
            "Section 8.1 - Notices. All notices required or permitted under this Agreement shall be in writing "
            "and shall be delivered personally or sent by certified mail, return receipt requested.",
            "Section 8.2 - Governing Law. This Agreement shall be governed by and construed in accordance with "
            "the laws of the State of California, without regard to its conflict of laws provisions.",
            "Section 8.3 - Severability. If any provision of this Agreement is held to be invalid or "
            "unenforceable, the remaining provisions shall continue in full force and effect.",
            "Section 8.4 - Entire Agreement. This Agreement, together with the Note, constitutes the entire "
            "agreement between the parties relating to the subject matter hereof.",
            "Section 8.5 - Amendments. This Agreement may not be modified or amended except by written "
            "instrument signed by both Borrower and Lender.",
        ]),
        ("ARTICLE IX: SIGNATURES AND ACKNOWLEDGMENT", [
            "IN WITNESS WHEREOF, the parties have executed this Mortgage Agreement as of the date first "
            "above written.",
            "BORROWER:                          LENDER:",
            "___________________________       ___________________________",
            "David Chen                        Marcus R. Thompson, SVP",
            "                                  First National Savings Bank",
            "___________________________",
            "Lisa Marie Chen",
            "",
            "Acknowledged before me this 15th day of March, 2025.",
            "___________________________",
            "Notary Public, State of California",
            "Commission Number: 2398471",
        ]),
    ]

    # We need 15 pages total. Distribute sections across pages.
    # Some sections will span multiple pages for realism.
    page_count = 0
    for section_title, paragraphs in sections:
        page = doc.new_page(width=612, height=792)
        page_count += 1
        y = 60
        page.insert_text(pymupdf.Point(72, y), section_title, fontsize=14, fontname="hebo", color=(0, 0, 0.3))
        y += 25
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(540, y))
        shape.finish(color=(0, 0, 0.3), width=0.5)
        shape.commit()
        y += 15

        for para in paragraphs:
            rect = pymupdf.Rect(72, y, 540, y + 120)
            excess = page.insert_textbox(rect, para, fontsize=10, fontname="helv",
                                         color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
            y += 120 - max(excess, 0)
            if y > 730:
                break

        # Footer
        page.insert_text(pymupdf.Point(280, 770), f"Page {page_count}", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    # Add extra pages to reach 15
    while page_count < 15:
        page = doc.new_page(width=612, height=792)
        page_count += 1
        extra_sections = [
            ("EXHIBIT A: LEGAL DESCRIPTION OF PROPERTY",
             "Lot 47 of Tract No. 9823, City of Palo Alto, County of Santa Clara, State of California, "
             "as shown on the map filed in Book 342 of Maps, at Pages 15 through 18, Records of Santa Clara County. "
             "APN: 167-42-089. The property is further bounded and described as: Beginning at the northeast corner "
             "of said Lot 47; thence South 00 degrees 15 minutes 30 seconds East along the easterly line of said "
             "Lot 47, a distance of 125.00 feet; thence South 89 degrees 44 minutes 30 seconds West, a distance "
             "of 60.00 feet; thence North 00 degrees 15 minutes 30 seconds West, a distance of 125.00 feet to "
             "the northerly line of said Lot 47; thence North 89 degrees 44 minutes 30 seconds East along said "
             "northerly line, a distance of 60.00 feet to the Point of Beginning."),
            ("EXHIBIT B: PAYMENT SCHEDULE",
             "Monthly Payment Amount: $7,842.36. Interest Rate: 6.25% per annum, fixed for 30 years. "
             "First Payment Due: May 1, 2025. Last Payment Due: April 1, 2055. "
             "Late Charge: 5% of overdue amount if payment received after the 15th day of the month. "
             "Prepayment: Borrower may prepay the principal balance in whole or in part without penalty "
             "after the first three (3) years of the loan term."),
            ("EXHIBIT C: ESCROW INSTRUCTIONS",
             "Pacific Coast Title Company, acting as escrow agent, is hereby instructed to: "
             "(1) Record the Warranty Deed in favor of Borrower; (2) Record this Mortgage in favor of Lender; "
             "(3) Disburse loan proceeds per the Settlement Statement; (4) Obtain and deliver title insurance "
             "policies to all parties. Escrow Number: PC-2025-48712."),
            ("EXHIBIT D: RIDER TO MORTGAGE",
             "ADJUSTABLE RATE RIDER: Not applicable - this is a fixed rate mortgage. "
             "CONDOMINIUM RIDER: Not applicable. PLANNED UNIT DEVELOPMENT RIDER: Not applicable. "
             "BIWEEKLY PAYMENT RIDER: Not applicable. SECOND HOME RIDER: Not applicable. "
             "1-4 FAMILY RIDER: This rider supplements the Mortgage. The Property includes a single-family "
             "residence that will be occupied by Borrower as Borrower's principal residence."),
            ("EXHIBIT E: CLOSING COST SUMMARY",
             "Appraisal Fee: $750.00. Credit Report: $65.00. Flood Certification: $25.00. "
             "Tax Service Fee: $85.00. Title Insurance (Lender's Policy): $2,340.00. "
             "Title Insurance (Owner's Policy): $1,890.00. Escrow Fee: $2,100.00. "
             "Recording Fees: $175.00. Transfer Tax: $2,035.00. Origination Fee: $14,800.00 (1%). "
             "Total Estimated Closing Costs: $24,265.00."),
        ]
        idx = page_count - 11  # 0-indexed from page 11
        if idx < len(extra_sections):
            title, content = extra_sections[idx]
            page.insert_text(pymupdf.Point(72, 60), title, fontsize=14, fontname="hebo", color=(0, 0, 0.3))
            rect = pymupdf.Rect(72, 90, 540, 700)
            page.insert_textbox(rect, content, fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)
        page.insert_text(pymupdf.Point(280, 770), f"Page {page_count}", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    path = f'{CLOSING_DIR}/mortgage.pdf'
    doc.save(path)
    doc.close()
    print(f'Created: {path} ({page_count} pages)')


def create_title_insurance():
    """Create an 8-page title insurance policy."""
    doc = pymupdf.open()

    sections = [
        ("OWNER'S POLICY OF TITLE INSURANCE", [
            "Policy Number: OTP-2025-893247",
            "Date of Policy: March 15, 2025",
            "Amount of Insurance: $1,850,000.00",
            "Name of Insured: David Chen and Lisa Marie Chen",
            "The estate or interest in the Land that is insured by this policy is: Fee Simple",
            "The Land referred to in this policy is described as follows: Lot 47 of Tract No. 9823, "
            "City of Palo Alto, County of Santa Clara, State of California.",
            "Pacific Title Insurance Company ('Company'), a California corporation, for a valuable "
            "consideration, the receipt of which is hereby acknowledged, and subject to the Exclusions "
            "from Coverage, the Exceptions from Coverage contained in Schedule B, and the Conditions "
            "stated herein, insures, as of the Date of Policy shown above, against loss or damage sustained "
            "by the Insured by reason of any defect in or lien or encumbrance on the Title.",
        ]),
        ("SCHEDULE A: COVERED RISKS", [
            "1. Any defect in or lien or encumbrance on the Title. This Covered Risk includes but is not "
            "limited to insurance against loss from: (a) A defect in the Title caused by forgery, fraud, "
            "undue influence, duress, incompetency, incapacity, or impersonation.",
            "(b) A defect in the Title caused by an instrument that has not been duly executed, delivered, "
            "or recorded. (c) A defect in the Title caused by a failure of any person or entity to have "
            "authorized a transfer or conveyance.",
            "2. The lien of real estate taxes or assessments imposed on the Title by a governmental authority "
            "due or payable, but unpaid.",
            "3. Any encroachment, encumbrance, violation, variation, or adverse circumstance affecting the "
            "Title that would be disclosed by an accurate and complete land survey of the Land.",
            "4. Any statutory or constitutional mechanic's, contractor's, or materialman's lien for labor "
            "or materials having their inception on or before the Date of Policy.",
        ]),
        ("SCHEDULE B: EXCEPTIONS FROM COVERAGE", [
            "This policy does not insure against loss or damage arising from:",
            "Exception 1: Property taxes and assessments for the fiscal year 2025-2026, a lien not yet due "
            "or payable. First installment: $11,562.50 (due November 1, 2025).",
            "Exception 2: Covenants, conditions, and restrictions as set forth in instrument recorded "
            "September 12, 1987, as Document No. 10847329, Official Records of Santa Clara County.",
            "Exception 3: An easement for public utilities and incidental purposes, in favor of Pacific Gas "
            "and Electric Company, recorded March 3, 1965, as Document No. 5847921.",
            "Exception 4: Rights of the public in and to that portion of the Land lying within the boundaries "
            "of Redwood Lane, as established by the recorded subdivision map.",
        ]),
        ("CONDITIONS AND STIPULATIONS", [
            "1. DEFINITION OF TERMS: (a) 'Insured' means the Insured named in Schedule A, and subject to "
            "any rights or defenses the Company would have had against the named Insured, those who succeed "
            "to the interest of the named Insured by operation of law.",
            "(b) 'Knowledge' or 'Known' means actual knowledge, not constructive knowledge or notice that "
            "may be imputed to an Insured by reason of the Public Records.",
            "(c) 'Land' means the land described in Schedule A and affixed improvements that by law constitute "
            "real property. The term does not include any property beyond the lines of the area specifically "
            "described in Schedule A.",
            "2. CONTINUATION OF INSURANCE: The coverage of this policy shall continue in force as of the Date "
            "of Policy in favor of an Insured, but only so long as the Insured retains an estate or interest "
            "in the Land, or holds an obligation secured by a purchase money Mortgage given by a purchaser "
            "from the Insured.",
        ]),
        ("ENDORSEMENTS", [
            "CLTA Form 100 - Restrictions, Encroachments, Minerals Endorsement",
            "This endorsement is issued as part of the policy. Except as it expressly states, it does not "
            "(i) modify any of the terms and provisions of the policy, (ii) modify any prior endorsements, "
            "(iii) extend the Date of Policy, or (iv) increase the Amount of Insurance.",
            "The Company insures the Insured against loss or damage sustained by reason of: "
            "(a) Any future violations of the covenants, conditions, or restrictions referred to in "
            "Exception 2 of Schedule B; (b) Damage to existing improvements located on the Land that "
            "encroach onto the easement referred to in Exception 3 of Schedule B.",
            "CLTA Form 116 - Survey Endorsement: The Company insures that the Land is the same as the "
            "property shown on the survey prepared by Henderson & Associates, dated February 28, 2025.",
        ]),
        ("CLAIMS PROCEDURES", [
            "Any claim under this policy must be submitted in writing to Pacific Title Insurance Company, "
            "Claims Department, 2100 Glendale Galleria, Suite 300, Glendale, CA 91210.",
            "The Company's obligations under this policy shall be limited to the Amount of Insurance stated "
            "in Schedule A, and in no event shall the Company be liable for (a) consequential damages, "
            "(b) damages in excess of the Amount of Insurance, or (c) attorney fees in excess of the "
            "Amount of Insurance.",
            "Notice of claim must be given within sixty (60) days of the Insured's discovery of the matter "
            "giving rise to the claim.",
        ]),
        ("ARBITRATION AND GOVERNING LAW", [
            "Either the Company or the Insured may demand that the claim or controversy shall be submitted "
            "to arbitration pursuant to the Title Insurance Arbitration Rules of the American Land Title "
            "Association. Any arbitration shall take place in the County of Santa Clara, California.",
            "This policy shall be governed by and construed in accordance with the laws of the State of "
            "California.",
        ]),
        ("SIGNATURES AND ATTESTATION", [
            "IN WITNESS WHEREOF, Pacific Title Insurance Company has caused this policy to be signed and "
            "sealed as of March 15, 2025.",
            "",
            "___________________________",
            "Margaret A. Sullivan, President",
            "Pacific Title Insurance Company",
            "",
            "Countersigned:",
            "___________________________",
            "Raymond K. Patel, Authorized Agent",
            "Pacific Coast Title Company (Issuing Agent)",
        ]),
    ]

    for i, (title, paragraphs) in enumerate(sections):
        page = doc.new_page(width=612, height=792)
        y = 60
        page.insert_text(pymupdf.Point(72, y), title, fontsize=14, fontname="hebo", color=(0, 0.2, 0.4))
        y += 25
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(540, y))
        shape.finish(color=(0, 0.2, 0.4), width=0.5)
        shape.commit()
        y += 15
        for para in paragraphs:
            rect = pymupdf.Rect(72, y, 540, y + 100)
            excess = page.insert_textbox(rect, para, fontsize=10, fontname="helv",
                                         color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
            y += 100 - max(excess, 0)
            if y > 740:
                break
        page.insert_text(pymupdf.Point(280, 770), f"Page {i + 1} of 8", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    path = f'{CLOSING_DIR}/title_insurance.pdf'
    doc.save(path)
    doc.close()
    print(f'Created: {path} (8 pages)')


def create_survey():
    """Create a 2-page property survey report."""
    doc = pymupdf.open()

    # Page 1 - Survey details
    page = doc.new_page(width=612, height=792)
    page.insert_text(pymupdf.Point(150, 60), "PROPERTY SURVEY REPORT", fontsize=18, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(72, 100), "Henderson & Associates Land Surveying, Inc.", fontsize=12, fontname="hebo")
    page.insert_text(pymupdf.Point(72, 118), "1845 Hamilton Avenue, Suite 200, San Jose, CA 95125", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 136), "License No. LS-7834 | Phone: (408) 555-0147", fontsize=10, fontname="helv")

    page.insert_text(pymupdf.Point(72, 175), "Survey Number: HS-2025-0294", fontsize=10, fontname="hebo")
    page.insert_text(pymupdf.Point(72, 193), "Date of Survey: February 28, 2025", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 211), "Property: 4872 Redwood Lane, Palo Alto, CA 94301", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 229), "APN: 167-42-089", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 247), "Client: Pacific Coast Title Company", fontsize=10, fontname="helv")
    page.insert_text(pymupdf.Point(72, 265), "Ordered by: First National Savings Bank (Lender)", fontsize=10, fontname="helv")

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 280), pymupdf.Point(540, 280))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()

    page.insert_text(pymupdf.Point(72, 300), "SURVEY FINDINGS:", fontsize=12, fontname="hebo")
    findings = ("The undersigned Professional Land Surveyor hereby certifies that this survey was made "
                "in conformity with the 2021 Minimum Standard Detail Requirements for ALTA/NSPS Land "
                "Title Surveys as adopted by the American Land Title Association and the National Society "
                "of Professional Surveyors. The property is a rectangular lot measuring 60.00 feet along "
                "its north and south boundaries and 125.00 feet along its east and west boundaries, "
                "containing approximately 7,500 square feet (0.172 acres). The property is improved with "
                "a two-story single-family residence with an attached two-car garage.")
    rect = pymupdf.Rect(72, 320, 540, 500)
    page.insert_textbox(rect, findings, fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page.insert_text(pymupdf.Point(72, 520), "BOUNDARY DIMENSIONS:", fontsize=11, fontname="hebo")
    dims = [
        "North boundary: 60.00 feet (along Redwood Lane right-of-way)",
        "South boundary: 60.00 feet (along rear property line)",
        "East boundary: 125.00 feet (along Lot 48)",
        "West boundary: 125.00 feet (along Lot 46)",
    ]
    y = 540
    for dim in dims:
        page.insert_text(pymupdf.Point(90, y), dim, fontsize=10, fontname="helv")
        y += 18

    page.insert_text(pymupdf.Point(72, 630), "IMPROVEMENTS FOUND:", fontsize=11, fontname="hebo")
    improvements = ("Main residence: 2,450 sq ft, two-story wood frame construction, built 1985. "
                    "Attached garage: 440 sq ft. Concrete driveway. Wood fence along south and east "
                    "boundaries. Mature landscaping with oak and redwood trees. No encroachments observed "
                    "by or onto the subject property.")
    rect2 = pymupdf.Rect(72, 650, 540, 760)
    page.insert_textbox(rect2, improvements, fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Page 2 - Certification and plat sketch
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(pymupdf.Point(72, 60), "SURVEYOR'S CERTIFICATION", fontsize=14, fontname="hebo")

    cert = ("I, Thomas R. Henderson, a Professional Land Surveyor licensed in the State of California, "
            "License No. LS-7834, do hereby certify to Pacific Coast Title Company, First National "
            "Savings Bank, David Chen, and Lisa Marie Chen, that this survey was prepared under my "
            "direct supervision and that it correctly represents the boundaries and improvements on "
            "the property described herein as of the date of the field survey, February 28, 2025.")
    rect = pymupdf.Rect(72, 85, 540, 200)
    page2.insert_textbox(rect, cert, fontsize=10, fontname="helv", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page2.insert_text(pymupdf.Point(72, 230), "EASEMENTS AND ENCUMBRANCES NOTED:", fontsize=11, fontname="hebo")
    easements = [
        "1. 10-foot public utility easement along north boundary (PG&E, recorded 1965)",
        "2. 5-foot drainage easement along east boundary (per subdivision map)",
        "3. No encroachments by or onto the subject property were observed",
        "4. All improvements are within property boundary lines",
    ]
    y = 250
    for e in easements:
        page2.insert_text(pymupdf.Point(90, y), e, fontsize=10, fontname="helv")
        y += 18

    # Simple plat sketch representation
    page2.insert_text(pymupdf.Point(200, 350), "PLAT SKETCH (NOT TO SCALE)", fontsize=12, fontname="hebo")
    shape2 = page2.new_shape()
    # Property boundary rectangle
    shape2.draw_rect(pymupdf.Rect(150, 370, 460, 620))
    shape2.finish(color=(0, 0, 0), width=1.5)
    # House outline
    shape2.draw_rect(pymupdf.Rect(200, 420, 410, 570))
    shape2.finish(color=(0.3, 0.3, 0.3), width=1, dashes="[3 3]")
    shape2.commit()

    page2.insert_text(pymupdf.Point(220, 500), "RESIDENCE", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    page2.insert_text(pymupdf.Point(250, 365), "REDWOOD LANE (N)", fontsize=8, fontname="helv")
    page2.insert_text(pymupdf.Point(285, 640), "60.00'", fontsize=9, fontname="helv")
    page2.insert_text(pymupdf.Point(130, 500), "125.00'", fontsize=9, fontname="helv", rotate=90)

    page2.insert_text(pymupdf.Point(72, 680), "____________________________________", fontsize=10, fontname="helv")
    page2.insert_text(pymupdf.Point(72, 700), "Thomas R. Henderson, PLS", fontsize=10, fontname="helv")
    page2.insert_text(pymupdf.Point(72, 718), "California License No. LS-7834", fontsize=10, fontname="helv")
    page2.insert_text(pymupdf.Point(72, 736), "Date: February 28, 2025", fontsize=10, fontname="helv")

    path = f'{CLOSING_DIR}/survey.pdf'
    doc.save(path)
    doc.close()
    print(f'Created: {path} (2 pages)')


def create_disclosure():
    """Create a 6-page seller's disclosure statement."""
    doc = pymupdf.open()

    sections = [
        ("SELLER'S REAL PROPERTY DISCLOSURE STATEMENT", [
            "Property Address: 4872 Redwood Lane, Palo Alto, CA 94301",
            "Seller(s): Robert James Mitchell and Catherine Anne Mitchell",
            "Buyer(s): David Chen and Lisa Marie Chen",
            "Date: March 1, 2025",
            "",
            "This statement is a disclosure of the condition of the above-described property in compliance "
            "with California Civil Code Section 1102. It is not a warranty of any kind by the Seller(s) "
            "or any agent(s) representing any principal(s) in this transaction, and is not a substitute "
            "for any inspections or warranties the principal(s) may wish to obtain.",
        ]),
        ("SECTION I: STRUCTURAL AND SYSTEMS", [
            "A. Foundation: Concrete slab foundation, poured 1985. No known cracks or settling issues. "
            "Last inspected: January 2025 by Bay Area Foundation Specialists.",
            "B. Roof: Composition shingle roof, replaced in 2018 by Premier Roofing Co. Estimated "
            "remaining useful life: 15-20 years. No known leaks.",
            "C. Electrical System: 200-amp service panel, upgraded 2015. All circuits properly grounded. "
            "GFCI outlets in kitchen, bathrooms, garage, and exterior.",
            "D. Plumbing: Copper supply lines, ABS drain lines. Water heater (50 gallon, gas) installed "
            "2020 by Palo Alto Plumbing. No known leaks or drainage issues.",
            "E. HVAC: Central heating and air conditioning, Carrier system installed 2019. Ductwork "
            "inspected and cleaned October 2024. Programmable thermostat (Nest).",
            "F. Fireplace: One wood-burning fireplace in living room. Chimney last inspected and cleaned "
            "September 2024 by Bay Area Chimney Sweep.",
        ]),
        ("SECTION II: ENVIRONMENTAL CONDITIONS", [
            "A. Asbestos: Home built in 1985; no asbestos-containing materials are known to be present. "
            "Previous testing conducted in 2015 during renovation - negative results.",
            "B. Lead-Based Paint: Property was built after 1978. No lead-based paint is known or suspected "
            "to be present on the property.",
            "C. Radon: No radon testing has been conducted on this property. Seller makes no representation "
            "regarding radon levels.",
            "D. Mold: No known mold or mildew issues. Bathroom exhaust fans maintained and operational. "
            "No history of water damage or flooding.",
            "E. Pest Control: Annual termite inspection by Peninsula Pest Control. Last inspection: "
            "November 2024. No active infestations found. Previous treatment for subterranean termites "
            "in 2016; monitoring stations in place.",
            "F. Flood Zone: Property is NOT located in a FEMA-designated Special Flood Hazard Area "
            "(Zone X - minimal flood hazard). Flood insurance is not required by lender but is recommended.",
        ]),
        ("SECTION III: PROPERTY HISTORY AND REPAIRS", [
            "Seller has owned the property since June 2008. During ownership, the following significant "
            "repairs, improvements, and modifications have been made:",
            "2015 - Kitchen remodel ($85,000): New cabinets, countertops, appliances, flooring. "
            "All permits pulled from City of Palo Alto (Permit #BP-2015-4271).",
            "2016 - Termite treatment and repair ($4,200): Subterranean termite treatment, replacement "
            "of damaged wood members in garage.",
            "2018 - Roof replacement ($28,500): Complete tear-off and replacement with 30-year "
            "composition shingles (Permit #BP-2018-1893).",
            "2019 - HVAC replacement ($15,800): New Carrier central heating and air conditioning system.",
            "2020 - Water heater replacement ($2,400): 50-gallon gas water heater.",
            "2021 - Bathroom remodel ($32,000): Master bathroom renovation with new tile, vanity, "
            "and glass shower enclosure (Permit #BP-2021-3847).",
            "2023 - Exterior painting ($12,500): Complete exterior repaint, Dunn-Edwards paint.",
            "All permitted work was inspected and finaled by the City of Palo Alto Building Department.",
        ]),
        ("SECTION IV: NEIGHBORHOOD AND COMMUNITY DISCLOSURES", [
            "A. Homeowners Association: None. Property is not subject to HOA fees or restrictions.",
            "B. Special Assessments: None known at this time.",
            "C. Noise: Property is located in a residential neighborhood. Occasional aircraft noise from "
            "Palo Alto Airport (approximately 2 miles northeast). No known noise ordinance violations.",
            "D. Schools: Property is within the Palo Alto Unified School District. Nearby schools: "
            "Barron Park Elementary (0.5 miles), Terman Middle School (1.2 miles), "
            "Gunn High School (1.8 miles).",
            "E. Neighborhood Issues: No known disputes with neighbors. No pending litigation involving "
            "the property or neighboring properties. No known planned developments that would materially "
            "affect the property value.",
            "F. Insurance Claims: One insurance claim filed in 2017 for a fallen tree branch causing minor "
            "roof damage ($3,200 claim, repaired promptly). No other claims in the past 10 years.",
        ]),
        ("SECTION V: SELLER CERTIFICATION", [
            "The undersigned Seller(s) certify that the information herein is true and correct to the best "
            "of their knowledge as of the date signed. Seller(s) agree to disclose any additional material "
            "facts that become known prior to close of escrow.",
            "",
            "Seller acknowledges that this disclosure is not intended to be part of any contract between "
            "Buyer and Seller. Seller further acknowledges that this disclosure form is not a warranty "
            "or guarantee of any kind.",
            "",
            "___________________________          Date: March 1, 2025",
            "Robert James Mitchell",
            "",
            "___________________________          Date: March 1, 2025",
            "Catherine Anne Mitchell",
            "",
            "BUYER'S ACKNOWLEDGMENT",
            "Buyer acknowledges receipt of this Seller's Disclosure Statement.",
            "",
            "___________________________          Date: _______________",
            "David Chen",
            "",
            "___________________________          Date: _______________",
            "Lisa Marie Chen",
        ]),
    ]

    for i, (title, paragraphs) in enumerate(sections):
        page = doc.new_page(width=612, height=792)
        y = 60
        page.insert_text(pymupdf.Point(72, y), title, fontsize=14, fontname="hebo", color=(0.3, 0, 0))
        y += 25
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(540, y))
        shape.finish(color=(0.3, 0, 0), width=0.5)
        shape.commit()
        y += 15
        for para in paragraphs:
            if para == "":
                y += 10
                continue
            rect = pymupdf.Rect(72, y, 540, y + 100)
            excess = page.insert_textbox(rect, para, fontsize=10, fontname="helv",
                                         color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
            y += 100 - max(excess, 0)
            if y > 740:
                break
        page.insert_text(pymupdf.Point(280, 770), f"Page {i + 1} of 6", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))

    path = f'{CLOSING_DIR}/disclosure.pdf'
    doc.save(path)
    doc.close()
    print(f'Created: {path} (6 pages)')


def create_initial():
    # Create directory structure
    os.makedirs(CLOSING_DIR, exist_ok=True)

    # Create all five documents
    create_deed()
    create_mortgage()
    create_title_insurance()
    create_survey()
    create_disclosure()

    # Verify page counts
    for fname, expected in [('deed.pdf', 4), ('mortgage.pdf', 15),
                            ('title_insurance.pdf', 8), ('survey.pdf', 2),
                            ('disclosure.pdf', 6)]:
        path = f'{CLOSING_DIR}/{fname}'
        doc = pymupdf.open(path)
        actual = doc.page_count
        doc.close()
        status = "OK" if actual == expected else f"MISMATCH (got {actual})"
        print(f'  {fname}: {actual} pages [{status}]')

    # Open the closing directory in file manager for the agent
    launch_gui(f'nautilus "{CLOSING_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched nautilus with closing directory')


create_initial()
