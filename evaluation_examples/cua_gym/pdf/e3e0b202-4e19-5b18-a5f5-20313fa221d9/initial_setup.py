"""
Initial Setup: Create a 9-page civil complaint PDF with 5 full addresses
Task ID: pdf_legal_012
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_012'
LEGAL_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{LEGAL_DIR}/complaint.pdf'

# Page dimensions (Letter size)
W, H = 612, 792
MARGIN_L = 72
MARGIN_R = 540
MARGIN_T = 72
MARGIN_B = 720
LINE_H = 14

# 5 addresses embedded throughout the complaint
ADDRESSES = [
    "4721 Riverside Drive, Sacramento, CA 95820",
    "1388 Magnolia Boulevard, Burbank, CA 91502",
    "903 West Elm Street, Suite 200, Denver, CO 80204",
    "2650 Peachtree Road NW, Atlanta, GA 30305",
    "517 Harbor View Lane, Annapolis, MD 21401",
]


def launch_gui(command: str, delay_sec: float = 1.0):
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def add_text(page, x, y, text, fontsize=11, fontname="tiro", bold=False):
    """Insert text and return new y position."""
    fn = "tibo" if bold else fontname
    page.insert_text(pymupdf.Point(x, y), text, fontsize=fontsize, fontname=fn, color=(0, 0, 0))
    return y + LINE_H


def add_paragraph(page, x, y, text, fontsize=11, fontname="tiro", line_width=468):
    """Insert wrapped text and return new y position."""
    rect = pymupdf.Rect(x, y - 2, x + line_width, y + 400)
    excess = page.insert_textbox(rect, text, fontsize=fontsize, fontname=fontname,
                                  color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    # Estimate lines used
    approx_chars_per_line = int(line_width / (fontsize * 0.5))
    num_lines = max(1, (len(text) // approx_chars_per_line) + 1)
    return y + num_lines * (fontsize + 3) + 4


def create_complaint():
    os.makedirs(LEGAL_DIR, exist_ok=True)

    doc = pymupdf.open()

    # =========================================================================
    # PAGE 1: Caption / Cover Page
    # =========================================================================
    p = doc.new_page(width=W, height=H)
    y = 72

    y = add_text(p, 200, y, "SUPERIOR COURT OF CALIFORNIA", fontsize=14, bold=True)
    y += 4
    y = add_text(p, 220, y, "COUNTY OF SACRAMENTO", fontsize=12, bold=True)
    y += 20

    # Horizontal line
    shape = p.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_L, y), pymupdf.Point(MARGIN_R, y))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()
    y += 20

    y = add_text(p, MARGIN_L, y, "ELENA VASQUEZ, an individual,", fontsize=11)
    y += 2
    y = add_text(p, MARGIN_L + 40, y, "Plaintiff,", fontsize=11)
    y += 10
    y = add_text(p, MARGIN_L + 20, y, "v.", fontsize=11, bold=True)
    y += 10
    y = add_text(p, MARGIN_L, y, "SUMMIT RIDGE PROPERTIES, LLC,", fontsize=11)
    y = add_text(p, MARGIN_L, y, "a California limited liability company;", fontsize=11)
    y = add_text(p, MARGIN_L, y, "DEREK THORNTON, an individual;", fontsize=11)
    y = add_text(p, MARGIN_L, y, "and DOES 1 through 50, inclusive,", fontsize=11)
    y += 2
    y = add_text(p, MARGIN_L + 40, y, "Defendants.", fontsize=11)
    y += 20

    # Case number box
    y = add_text(p, 350, 160, "Case No. 2025-CV-03847", fontsize=11, bold=True)
    y = add_text(p, 350, 175, "COMPLAINT FOR DAMAGES", fontsize=10, bold=True)
    y = add_text(p, 350, 190, "(1) Breach of Contract", fontsize=10)
    y = add_text(p, 350, 204, "(2) Fraud and Misrepresentation", fontsize=10)
    y = add_text(p, 350, 218, "(3) Negligence", fontsize=10)
    y = add_text(p, 350, 232, "(4) Violation of Bus. & Prof.", fontsize=10)
    y = add_text(p, 350, 246, "    Code Section 17200", fontsize=10)
    y = add_text(p, 350, 260, "DEMAND FOR JURY TRIAL", fontsize=10, bold=True)

    y = 340
    shape = p.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_L, y), pymupdf.Point(MARGIN_R, y))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()
    y += 20

    y = add_text(p, MARGIN_L, y, "COMPLAINT", fontsize=13, bold=True)
    y += 10
    y = add_paragraph(p, MARGIN_L, y,
        "Plaintiff ELENA VASQUEZ (\"Plaintiff\") alleges the following against "
        "Defendants SUMMIT RIDGE PROPERTIES, LLC (\"Summit Ridge\") and DEREK "
        "THORNTON (\"Thornton\") (collectively, \"Defendants\"), and each of them, "
        "and DOES 1 through 50, inclusive, on information and belief as follows:")
    y += 10

    y = add_text(p, MARGIN_L, y, "PARTIES", fontsize=12, bold=True)
    y += 6
    y = add_paragraph(p, MARGIN_L, y,
        f"1. Plaintiff ELENA VASQUEZ is an individual residing at "
        f"{ADDRESSES[0]}. Plaintiff is a licensed real estate appraiser who "
        f"entered into a contractual relationship with Defendants for property "
        f"management services beginning on or about March 15, 2024.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        f"2. Defendant SUMMIT RIDGE PROPERTIES, LLC is a California limited "
        f"liability company with its principal place of business located at "
        f"{ADDRESSES[1]}. Upon information and belief, Summit Ridge is engaged "
        f"in the business of commercial and residential property management and "
        f"development throughout the State of California.")

    # =========================================================================
    # PAGE 2: Parties continued + Jurisdiction
    # =========================================================================
    p = doc.new_page(width=W, height=H)
    y = 72

    y = add_paragraph(p, MARGIN_L, y,
        f"3. Defendant DEREK THORNTON is an individual who, upon information "
        f"and belief, resides at {ADDRESSES[2]}. At all times relevant hereto, "
        f"Thornton served as the Managing Director of Summit Ridge Properties, "
        f"LLC, and was responsible for overseeing all property acquisition "
        f"transactions and client relationships.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "4. The true names and capacities of Defendants sued herein as DOES 1 "
        "through 50, inclusive, are unknown to Plaintiff. Plaintiff is informed "
        "and believes and thereon alleges that each of the fictitiously named "
        "Defendants is in some manner responsible for the acts and omissions "
        "alleged herein. Plaintiff will amend this Complaint to allege their "
        "true names and capacities when ascertained.")
    y += 10

    y = add_text(p, MARGIN_L, y, "JURISDICTION AND VENUE", fontsize=12, bold=True)
    y += 6
    y = add_paragraph(p, MARGIN_L, y,
        "5. This Court has jurisdiction over this action pursuant to California "
        "Code of Civil Procedure Section 410.10. The amount in controversy "
        "exceeds the jurisdictional minimum of the Court.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "6. Venue is proper in this Court pursuant to California Code of Civil "
        "Procedure Section 395(a) because the obligations and transactions that "
        "are the subject of this action occurred in Sacramento County, and "
        "Defendants conduct substantial business in this County.")
    y += 10

    y = add_text(p, MARGIN_L, y, "GENERAL ALLEGATIONS", fontsize=12, bold=True)
    y += 6
    y = add_paragraph(p, MARGIN_L, y,
        "7. On or about March 15, 2024, Plaintiff entered into a Property "
        "Management Agreement (the \"Agreement\") with Summit Ridge for the "
        "management of a commercial office building located at 1580 Capitol "
        "Avenue, Sacramento, California. The Agreement required Summit Ridge "
        "to provide comprehensive property management services including tenant "
        "screening, maintenance coordination, financial reporting, and regulatory "
        "compliance for a monthly fee of $4,750.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "8. Defendant Thornton personally guaranteed the performance of Summit "
        "Ridge under the Agreement and represented to Plaintiff that he would "
        "personally oversee all aspects of the property management operations. "
        "Thornton further represented that Summit Ridge had extensive experience "
        "managing similar commercial properties and maintained a staff of "
        "qualified property management professionals.")

    # =========================================================================
    # PAGE 3: General Allegations continued
    # =========================================================================
    p = doc.new_page(width=W, height=H)
    y = 72

    y = add_paragraph(p, MARGIN_L, y,
        "9. In reliance on Defendants' representations, Plaintiff executed the "
        "Agreement and transferred management authority over the property at "
        "1580 Capitol Avenue to Summit Ridge. Plaintiff also provided Summit "
        "Ridge with access to the property's operating account containing "
        "approximately $127,500 in reserves for maintenance and capital "
        "improvements.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "10. Between April 2024 and September 2024, Defendants failed to "
        "perform their obligations under the Agreement in multiple material "
        "respects, including but not limited to: (a) failing to conduct proper "
        "tenant screening for three new tenants admitted during this period; "
        "(b) failing to perform or arrange scheduled maintenance including "
        "HVAC servicing, elevator inspections, and fire safety system testing; "
        "(c) misappropriating approximately $43,200 from the property's "
        "operating reserves; and (d) failing to provide accurate monthly "
        "financial statements as required by Section 4.2 of the Agreement.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "11. On or about October 3, 2024, Plaintiff discovered that Summit "
        "Ridge had failed to remit property tax payments totaling $18,750 "
        "that were due on September 15, 2024, despite having received funds "
        "from the property operating account specifically designated for "
        "that purpose.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "12. On October 10, 2024, Plaintiff sent a written demand letter to "
        "Defendants via certified mail requesting a full accounting of all "
        "funds received and disbursed from the property operating account. "
        "Defendants failed to respond to this demand within the 15-day period "
        "specified in Section 7.1 of the Agreement.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "13. On November 1, 2024, Plaintiff retained the forensic accounting "
        "firm of Whitfield & Associates to conduct an independent audit of the "
        "property's financial records. The audit revealed that Defendants had "
        "diverted a total of $86,400 from the property operating account to "
        "accounts controlled by Thornton personally.")

    # =========================================================================
    # PAGE 4: First Cause of Action
    # =========================================================================
    p = doc.new_page(width=W, height=H)
    y = 72

    y = add_text(p, MARGIN_L, y, "FIRST CAUSE OF ACTION", fontsize=12, bold=True)
    y = add_text(p, MARGIN_L, y, "(Breach of Contract -- Against All Defendants)", fontsize=11, bold=True)
    y += 6
    y = add_paragraph(p, MARGIN_L, y,
        "14. Plaintiff re-alleges and incorporates by reference each and every "
        "allegation set forth in paragraphs 1 through 13 above as though fully "
        "set forth herein.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "15. As set forth above, a valid and enforceable contract existed "
        "between Plaintiff and Defendants in the form of the Property "
        "Management Agreement dated March 15, 2024.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "16. Plaintiff performed all conditions, covenants, and promises "
        "required of her under the Agreement, or was excused from performance "
        "by Defendants' material breaches.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "17. Defendants breached the Agreement by, among other things: "
        "(a) failing to provide competent property management services as "
        "required by Section 2.1; (b) misappropriating property operating "
        "funds in violation of Section 3.4; (c) failing to maintain adequate "
        "records and provide financial reports as required by Section 4.2; "
        "(d) failing to remit property tax payments as required by Section "
        "5.1; and (e) failing to respond to Plaintiff's demand for accounting "
        "within the contractually required timeframe under Section 7.1.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "18. As a direct and proximate result of Defendants' breaches, "
        "Plaintiff has suffered damages in an amount to be proven at trial, "
        "but estimated to exceed $215,000, including but not limited to: "
        "$86,400 in misappropriated funds; $18,750 in unpaid property taxes "
        "and associated penalties; $32,000 in costs to remediate deferred "
        "maintenance; $45,000 in lost rental income; and $12,500 in "
        "professional fees for forensic accounting.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "19. Defendants' breaches were willful, knowing, and deliberate, "
        "entitling Plaintiff to an award of consequential damages.")

    # =========================================================================
    # PAGE 5: Second Cause of Action
    # =========================================================================
    p = doc.new_page(width=W, height=H)
    y = 72

    y = add_text(p, MARGIN_L, y, "SECOND CAUSE OF ACTION", fontsize=12, bold=True)
    y = add_text(p, MARGIN_L, y, "(Fraud and Intentional Misrepresentation -- Against All Defendants)", fontsize=11, bold=True)
    y += 6
    y = add_paragraph(p, MARGIN_L, y,
        "20. Plaintiff re-alleges and incorporates by reference each and every "
        "allegation set forth in paragraphs 1 through 19 above as though fully "
        "set forth herein.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "21. Prior to and at the time of entering into the Agreement, "
        "Defendants made material representations to Plaintiff, including that: "
        "(a) Summit Ridge had successfully managed over 200 commercial "
        "properties in the greater Sacramento area; (b) Thornton held a "
        "Certified Property Manager (CPM) designation from the Institute of "
        "Real Estate Management; and (c) Summit Ridge maintained professional "
        "liability insurance with coverage of at least $2,000,000.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "22. These representations were false and known by Defendants to be "
        "false at the time they were made. In truth: (a) Summit Ridge had "
        "managed fewer than 15 properties, most of which were residential; "
        "(b) Thornton's CPM designation had been revoked in 2022 for ethical "
        "violations; and (c) Summit Ridge's insurance policy had lapsed "
        "prior to execution of the Agreement.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "23. Defendants made these representations with the intent to induce "
        "Plaintiff to enter into the Agreement and to entrust Defendants with "
        "management of her property and substantial financial resources.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "24. Plaintiff justifiably relied on Defendants' representations in "
        "entering into the Agreement and would not have done so had she known "
        "the true facts.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "25. As a direct and proximate result of Defendants' fraudulent "
        "misrepresentations, Plaintiff has suffered damages as alleged herein. "
        "Defendants' conduct was malicious, oppressive, and fraudulent, "
        "entitling Plaintiff to an award of punitive damages in an amount "
        "sufficient to punish and deter such conduct.")

    # =========================================================================
    # PAGE 6: Third Cause of Action + Witness references
    # =========================================================================
    p = doc.new_page(width=W, height=H)
    y = 72

    y = add_text(p, MARGIN_L, y, "THIRD CAUSE OF ACTION", fontsize=12, bold=True)
    y = add_text(p, MARGIN_L, y, "(Negligence -- Against All Defendants)", fontsize=11, bold=True)
    y += 6
    y = add_paragraph(p, MARGIN_L, y,
        "26. Plaintiff re-alleges and incorporates by reference each and every "
        "allegation set forth in paragraphs 1 through 25 above as though fully "
        "set forth herein.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "27. Defendants owed Plaintiff a duty of care in the management of "
        "Plaintiff's property and financial resources. This duty arose both "
        "from the contractual relationship and from Defendants' professional "
        "obligations as property managers licensed under California Business "
        "and Professions Code Section 10131.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "28. Defendants breached their duty of care by failing to exercise "
        "the degree of skill, care, and diligence that a reasonably prudent "
        "property manager would exercise under similar circumstances.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        f"29. Witness MARGARET CHEN, a former employee of Summit Ridge residing "
        f"at {ADDRESSES[3]}, has confirmed through sworn declaration that "
        f"Thornton directed staff members to divert client funds to his "
        f"personal accounts on multiple occasions between May and August 2024. "
        f"Ms. Chen further stated that she reported these practices to the "
        f"California Department of Real Estate on September 12, 2024.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "30. As a direct and proximate result of Defendants' negligence, "
        "Plaintiff has suffered damages in an amount to be proven at trial, "
        "including property damage, financial losses, and emotional distress.")

    # =========================================================================
    # PAGE 7: Fourth Cause of Action + another witness address
    # =========================================================================
    p = doc.new_page(width=W, height=H)
    y = 72

    y = add_text(p, MARGIN_L, y, "FOURTH CAUSE OF ACTION", fontsize=12, bold=True)
    y = add_text(p, MARGIN_L, y, "(Violation of Business & Professions Code Section 17200 -- Against All Defendants)", fontsize=11, bold=True)
    y += 6
    y = add_paragraph(p, MARGIN_L, y,
        "31. Plaintiff re-alleges and incorporates by reference each and every "
        "allegation set forth in paragraphs 1 through 30 above as though fully "
        "set forth herein.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "32. California Business and Professions Code Section 17200 prohibits "
        "any unlawful, unfair, or fraudulent business act or practice. "
        "Defendants' conduct as alleged herein constitutes unlawful, unfair, "
        "and fraudulent business practices within the meaning of Section 17200.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "33. Defendants' unlawful business practices include, but are not "
        "limited to: (a) operating a property management business without "
        "maintaining required insurance; (b) misrepresenting professional "
        "credentials; (c) commingling and converting client funds in violation "
        "of Business and Professions Code Section 10145; and (d) failing to "
        "maintain records as required by Business and Professions Code "
        "Section 10148.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        f"34. Independent investigator ROBERT HAYES, of {ADDRESSES[4]}, "
        f"retained by Plaintiff's counsel, has documented additional instances "
        f"of Defendants engaging in substantially similar conduct with at least "
        f"four other property owners in the Sacramento and Placer County areas "
        f"during the period from January 2023 to the present.")
    y += 4
    y = add_paragraph(p, MARGIN_L, y,
        "35. As a result of Defendants' unfair business practices, Plaintiff "
        "seeks restitution of all money obtained through such practices, "
        "together with injunctive relief prohibiting Defendants from continuing "
        "to engage in property management activities.")

    # =========================================================================
    # PAGE 8: Damages, Prayer for Relief
    # =========================================================================
    p = doc.new_page(width=W, height=H)
    y = 72

    y = add_text(p, MARGIN_L, y, "DAMAGES", fontsize=12, bold=True)
    y += 6
    y = add_paragraph(p, MARGIN_L, y,
        "36. As a direct and proximate result of Defendants' wrongful conduct, "
        "Plaintiff has suffered the following categories of damages:")
    y += 4
    y = add_paragraph(p, MARGIN_L + 20, y,
        "a. Misappropriated property operating funds: $86,400.00")
    y = add_paragraph(p, MARGIN_L + 20, y,
        "b. Unpaid property taxes and associated penalties: $21,375.00")
    y = add_paragraph(p, MARGIN_L + 20, y,
        "c. Deferred maintenance remediation costs: $32,000.00")
    y = add_paragraph(p, MARGIN_L + 20, y,
        "d. Lost rental income from improperly screened tenants: $45,000.00")
    y = add_paragraph(p, MARGIN_L + 20, y,
        "e. Forensic accounting fees: $12,500.00")
    y = add_paragraph(p, MARGIN_L + 20, y,
        "f. Legal fees and costs incurred: amount to be proven at trial")
    y = add_paragraph(p, MARGIN_L + 20, y,
        "g. General damages for emotional distress: amount to be proven at trial")
    y += 10

    y = add_text(p, MARGIN_L, y, "PRAYER FOR RELIEF", fontsize=12, bold=True)
    y += 6
    y = add_paragraph(p, MARGIN_L, y,
        "WHEREFORE, Plaintiff ELENA VASQUEZ prays for judgment against "
        "Defendants, and each of them, as follows:")
    y += 4
    y = add_paragraph(p, MARGIN_L + 20, y,
        "1. For general and special damages according to proof at trial;")
    y = add_paragraph(p, MARGIN_L + 20, y,
        "2. For punitive and exemplary damages on the Second Cause of Action;")
    y = add_paragraph(p, MARGIN_L + 20, y,
        "3. For restitution of all monies wrongfully obtained;")
    y = add_paragraph(p, MARGIN_L + 20, y,
        "4. For injunctive relief as described herein;")
    y = add_paragraph(p, MARGIN_L + 20, y,
        "5. For prejudgment interest at the maximum rate allowed by law;")
    y = add_paragraph(p, MARGIN_L + 20, y,
        "6. For costs of suit incurred herein;")
    y = add_paragraph(p, MARGIN_L + 20, y,
        "7. For attorneys' fees as allowed by law or contract;")
    y = add_paragraph(p, MARGIN_L + 20, y,
        "8. For such other and further relief as the Court deems just and proper.")

    # =========================================================================
    # PAGE 9: Verification / Signature Page
    # =========================================================================
    p = doc.new_page(width=W, height=H)
    y = 72

    y = add_text(p, MARGIN_L, y, "VERIFICATION", fontsize=12, bold=True)
    y += 10
    y = add_paragraph(p, MARGIN_L, y,
        "I, ELENA VASQUEZ, am the Plaintiff in the above-entitled action. I "
        "have read the foregoing Complaint and know the contents thereof. The "
        "same is true of my own knowledge, except as to those matters which are "
        "therein stated upon information and belief, and as to those matters, "
        "I believe them to be true.")
    y += 20
    y = add_paragraph(p, MARGIN_L, y,
        "I declare under penalty of perjury under the laws of the State of "
        "California that the foregoing is true and correct.")
    y += 20
    y = add_text(p, MARGIN_L, y, "Executed on December 15, 2024, at Sacramento, California.", fontsize=11)
    y += 30
    # Signature line
    shape = p.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_L, y), pymupdf.Point(300, y))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    y += 14
    y = add_text(p, MARGIN_L, y, "ELENA VASQUEZ", fontsize=11, bold=True)
    y = add_text(p, MARGIN_L, y, "Plaintiff, Pro Se", fontsize=11)
    y += 30

    y = add_text(p, MARGIN_L, y, "DEMAND FOR JURY TRIAL", fontsize=12, bold=True)
    y += 10
    y = add_paragraph(p, MARGIN_L, y,
        "Plaintiff hereby demands a trial by jury on all issues so triable "
        "in this action.")
    y += 30
    y = add_text(p, MARGIN_L, y, "Dated: December 15, 2024", fontsize=11)
    y += 30
    shape = p.new_shape()
    shape.draw_line(pymupdf.Point(MARGIN_L, y), pymupdf.Point(300, y))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    y += 14
    y = add_text(p, MARGIN_L, y, "ELENA VASQUEZ", fontsize=11, bold=True)

    # Add page numbers
    for i in range(doc.page_count):
        page = doc[i]
        page.insert_text(
            pymupdf.Point(290, H - 30),
            f"- {i + 1} -",
            fontsize=10, fontname="tiro", color=(0, 0, 0)
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Total pages: 9')

    # Open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_complaint()
