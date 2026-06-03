"""
Initial Setup: Create 6 legal PDF files with distinct metadata for court filing batch
Task ID: pdf_legal_094
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_094'
BATCH_DIR = f'{WORKDIR}/legal/filing_batch'


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


# Define the 6 legal PDF files with distinct metadata
PDF_SPECS = [
    {
        "filename": "motion_to_dismiss_henderson.pdf",
        "title": "Motion to Dismiss - Henderson v. Pacific Northwest Industries",
        "author": "Attorney Rachel Whitfield",
        "creationDate": "D:20250812093000",
        "pages": 3,
        "content": [
            "SUPERIOR COURT OF THE STATE OF WASHINGTON\nCOUNTY OF KING\n\nCase No. 25-2-14832-KNT",
            "MOTION TO DISMISS\n\nCOMES NOW Defendant, Pacific Northwest Industries, Inc., by and through undersigned counsel, and respectfully moves this Court to dismiss Plaintiff's Complaint pursuant to CR 12(b)(6) for failure to state a claim upon which relief can be granted.\n\nI. STATEMENT OF FACTS\n\nPlaintiff James Henderson filed this action on June 15, 2025, alleging breach of contract related to a commercial lease agreement at 4500 Rainier Avenue South, Seattle, WA 98118. Defendant contends that the lease was properly terminated per Section 14.2 of the Agreement dated March 3, 2023.",
            "II. ARGUMENT\n\nThe Complaint fails to allege facts sufficient to establish the essential elements of a breach of contract claim. Specifically, Plaintiff has not demonstrated that Defendant failed to perform any obligation under the terms of the lease.\n\nIII. CONCLUSION\n\nFor the foregoing reasons, Defendant respectfully requests that this Court grant the Motion to Dismiss with prejudice.\n\nRespectfully submitted,\nRachel Whitfield, WSBA #38291\nCaldwell & Whitfield LLP\n1201 Third Avenue, Suite 2800\nSeattle, WA 98101"
        ]
    },
    {
        "filename": "settlement_agreement_garcia.pdf",
        "title": "Settlement Agreement - Garcia v. Meridian Health Systems",
        "author": "Mediator Douglas Tanaka",
        "creationDate": "D:20250723141500",
        "pages": 5,
        "content": [
            "CONFIDENTIAL SETTLEMENT AGREEMENT AND MUTUAL RELEASE\n\nThis Settlement Agreement is entered into as of July 23, 2025, by and between Maria Garcia (\"Plaintiff\") and Meridian Health Systems, Inc. (\"Defendant\").",
            "RECITALS\n\nWHEREAS, Plaintiff filed a complaint in the United States District Court for the Central District of California, Case No. 2:24-cv-09173-SVW, alleging employment discrimination and wrongful termination;\n\nWHEREAS, Defendant denies all allegations of wrongdoing but desires to resolve this matter to avoid the expense and uncertainty of litigation;\n\nNOW, THEREFORE, in consideration of the mutual promises contained herein, the parties agree as follows:",
            "1. SETTLEMENT PAYMENT\n\nDefendant shall pay Plaintiff the total sum of Three Hundred Seventy-Five Thousand Dollars ($375,000.00), allocated as follows:\n  a) $250,000.00 as compensatory damages (W-2 wages)\n  b) $75,000.00 as emotional distress damages (1099)\n  c) $50,000.00 for attorney's fees and costs\n\n2. MUTUAL RELEASE\n\nPlaintiff releases Defendant from all claims, known and unknown, arising from or related to Plaintiff's employment with Defendant.",
            "3. CONFIDENTIALITY\n\nThe parties agree to keep the terms of this Agreement strictly confidential. Neither party shall disclose the existence or terms of this Agreement to any third party except as required by law or to their respective attorneys, accountants, or tax advisors.\n\n4. NON-DISPARAGEMENT\n\nNeither party shall make any disparaging statements about the other party, whether oral or written, to any third party.",
            "5. GOVERNING LAW\n\nThis Agreement shall be governed by and construed in accordance with the laws of the State of California.\n\nIN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.\n\n_________________________\nMaria Garcia, Plaintiff\n\n_________________________\nDr. Steven Blackwell, CEO\nMeridian Health Systems, Inc.\n\nApproved as to form:\nDouglas Tanaka, Esq., Mediator\nTanaka Dispute Resolution, Los Angeles, CA"
        ]
    },
    {
        "filename": "appellate_brief_chen_v_state.pdf",
        "title": "Appellant's Opening Brief - Chen v. State of New York",
        "author": "Attorney Priya Narasimhan",
        "creationDate": "D:20250905101200",
        "pages": 4,
        "content": [
            "STATE OF NEW YORK\nAPPELLATE DIVISION, SECOND DEPARTMENT\n\nCase No. 2025-07841\n\nDavid Chen,\n  Appellant,\n\nv.\n\nState of New York,\n  Respondent.\n\nAPPELLANT'S OPENING BRIEF",
            "TABLE OF CONTENTS\n\nTable of Authorities ........................ ii\nStatement of the Case ...................... 1\nStatement of Facts ......................... 2\nArgument ................................... 5\n  I. The Trial Court Erred in Excluding Key Expert Testimony\n  II. The Jury Instructions Were Prejudicially Defective\n  III. Cumulative Error Denied Appellant a Fair Trial\nConclusion ................................. 12",
            "STATEMENT OF THE CASE\n\nAppellant David Chen was convicted on March 18, 2025, of two counts of securities fraud in violation of N.Y. Gen. Bus. Law Section 352-c. He was sentenced to a term of 3 to 9 years' imprisonment. This appeal challenges the conviction on grounds of evidentiary error and improper jury instructions.\n\nSTATEMENT OF FACTS\n\nBetween January 2022 and August 2024, Appellant served as Chief Financial Officer of Eastbridge Capital Partners, a registered investment advisory firm headquartered at 450 Park Avenue, New York, NY 10022. The prosecution alleged that Appellant misrepresented fund performance data to institutional investors, resulting in approximately $12.4 million in investor losses.",
            "ARGUMENT\n\nI. THE TRIAL COURT ERRED IN EXCLUDING KEY EXPERT TESTIMONY\n\nThe trial court's exclusion of Dr. Sandra Okafor's testimony regarding industry-standard accounting practices was an abuse of discretion that substantially prejudiced Appellant's defense. Dr. Okafor, a forensic accountant with 22 years of experience, would have testified that the reporting methodologies used by Appellant were consistent with GAAP and common industry practice.\n\nCONCLUSION\n\nFor the reasons stated herein, Appellant respectfully requests that this Court reverse the judgment of conviction and remand for a new trial.\n\nRespectfully submitted,\nPriya Narasimhan, Esq.\nNarasimhan & Cole LLP\n28 Liberty Street, 39th Floor\nNew York, NY 10005\nAttorney for Appellant"
        ]
    },
    {
        "filename": "subpoena_duces_tecum_morrison.pdf",
        "title": "Subpoena Duces Tecum - In re Morrison Financial Group Investigation",
        "author": "Assistant U.S. Attorney Katherine Voss",
        "creationDate": "D:20250618160000",
        "pages": 2,
        "content": [
            "UNITED STATES DISTRICT COURT\nSOUTHERN DISTRICT OF TEXAS\nHOUSTON DIVISION\n\nIN RE: INVESTIGATION OF\nMORRISON FINANCIAL GROUP, LLC\n\nMisc. No. 4:25-mc-01247\n\nSUBPOENA DUCES TECUM\n\nTO: First National Bank of Houston\n    Attn: Compliance Department\n    2300 Main Street, Houston, TX 77002\n\nYOU ARE COMMANDED to produce the following documents and records to the Office of the United States Attorney, Southern District of Texas, on or before July 18, 2025:",
            "DOCUMENTS REQUESTED:\n\n1. All account statements for Morrison Financial Group, LLC (EIN: 76-4928301) for the period January 1, 2023 through June 1, 2025.\n\n2. All wire transfer records, both incoming and outgoing, for the above-referenced account(s).\n\n3. All Suspicious Activity Reports (SARs) filed in connection with the above-referenced account(s).\n\n4. All correspondence between bank personnel and any representative of Morrison Financial Group, LLC.\n\n5. All records of authorized signatories and beneficial owners for the above-referenced account(s).\n\nFAILURE TO COMPLY with this subpoena may result in contempt of court proceedings.\n\nIssued this 18th day of June, 2025.\n\nKatherine Voss\nAssistant United States Attorney\nSouthern District of Texas\n1000 Louisiana Street, Suite 2300\nHouston, TX 77002"
        ]
    },
    {
        "filename": "expert_witness_declaration_patel.pdf",
        "title": "Declaration of Expert Witness Dr. Rajan Patel",
        "author": "Dr. Rajan Patel",
        "creationDate": "D:20250301080000",
        "pages": 4,
        "content": [
            "UNITED STATES DISTRICT COURT\nNORTHERN DISTRICT OF ILLINOIS\nEASTERN DIVISION\n\nWilliams Industrial Corp.,\n  Plaintiff,\n\nv.\n\nGreenTech Environmental Solutions, Inc.,\n  Defendant.\n\nCase No. 1:24-cv-06317\n\nDECLARATION OF DR. RAJAN PATEL\n\nI, Dr. Rajan Patel, declare under penalty of perjury as follows:",
            "1. I am a licensed Professional Engineer in the State of Illinois (License No. PE-062-047891) and hold a Ph.D. in Environmental Engineering from the Massachusetts Institute of Technology (2008).\n\n2. I have been retained by Plaintiff's counsel to provide expert opinions regarding the environmental remediation standards applicable to the property located at 8750 South Chicago Avenue, Chicago, IL 60617.\n\n3. I have over 17 years of experience in environmental site assessment and remediation, having served as lead consultant on more than 140 Superfund and brownfield projects across the Midwest.",
            "4. OPINIONS\n\nBased on my review of the site investigation reports, laboratory analytical data, and applicable regulatory standards, I hold the following opinions to a reasonable degree of scientific certainty:\n\n  a) The soil contamination levels at the Subject Property exceed Illinois TACO Tier 1 residential remediation objectives for lead (580 mg/kg vs. 400 mg/kg), arsenic (34 mg/kg vs. 13 mg/kg), and benzo(a)pyrene (2.8 mg/kg vs. 0.2 mg/kg).\n\n  b) The groundwater plume has migrated approximately 1,200 feet southeast of the original source area, affecting at least three adjacent properties.\n\n  c) The estimated cost of remediation using the most appropriate technology (in-situ chemical oxidation combined with monitored natural attenuation) ranges from $2.8 million to $4.2 million.",
            "5. I have not been compensated for forming these opinions beyond my standard consulting rate of $475 per hour. My compensation is not contingent on the outcome of this litigation.\n\n6. I am prepared to testify at trial and be subject to cross-examination regarding the opinions expressed herein.\n\nI declare under penalty of perjury under the laws of the United States that the foregoing is true and correct.\n\nExecuted on March 1, 2025, in Evanston, Illinois.\n\n_________________________\nDr. Rajan Patel, Ph.D., P.E.\nSenior Environmental Consultant\nGreat Lakes Environmental Associates\n1800 Sherman Avenue, Suite 400\nEvanston, IL 60201"
        ]
    },
    {
        "filename": "court_order_injunction_biosynth.pdf",
        "title": "Preliminary Injunction Order - FTC v. BioSynth Laboratories",
        "author": "Hon. Judge Margaret Liu",
        "creationDate": "D:20251029143000",
        "pages": 3,
        "content": [
            "UNITED STATES DISTRICT COURT\nDISTRICT OF MASSACHUSETTS\n\nFEDERAL TRADE COMMISSION,\n  Plaintiff,\n\nv.\n\nBIOSYNTH LABORATORIES, INC.,\n  Defendant.\n\nCivil Action No. 1:25-cv-11482-ML\n\nPRELIMINARY INJUNCTION ORDER",
            "THIS MATTER comes before the Court on the Federal Trade Commission's Motion for Preliminary Injunction. Having reviewed the parties' submissions, heard oral argument on October 22, 2025, and considered the applicable legal standards, the Court finds as follows:\n\nFINDINGS OF FACT\n\n1. Defendant BioSynth Laboratories, Inc. has marketed and sold dietary supplements under the brand name \"NeuroBoost Pro\" since September 2023.\n\n2. The FTC has presented substantial evidence that Defendant's advertising claims -- including that NeuroBoost Pro can \"reverse cognitive decline\" and \"restore memory function to youthful levels\" -- are unsubstantiated and likely to mislead consumers.\n\n3. Defendant's gross revenue from NeuroBoost Pro sales exceeds $18.7 million as of the filing date.",
            "ORDER\n\nIT IS HEREBY ORDERED that:\n\n1. Defendant BioSynth Laboratories, Inc., its officers, agents, employees, and all persons in active concert with them, are ENJOINED from:\n  a) Making any representation that NeuroBoost Pro can treat, cure, or mitigate any disease or medical condition unless supported by competent and reliable scientific evidence;\n  b) Disseminating any advertisement for NeuroBoost Pro that contains unsubstantiated health claims;\n  c) Destroying, concealing, or altering any business records related to the marketing and sale of NeuroBoost Pro.\n\n2. Defendant shall, within fourteen (14) days of this Order, place the sum of $5,000,000.00 in an escrow account for potential consumer redress.\n\n3. This Order shall remain in effect pending final disposition of this matter or further order of this Court.\n\nSO ORDERED this 29th day of October, 2025.\n\nHon. Margaret Liu\nUnited States District Judge\nDistrict of Massachusetts"
        ]
    },
]


def create_pdf(spec, output_path):
    """Create a PDF file with the given spec."""
    doc = pymupdf.open()

    for i, page_text in enumerate(spec["content"]):
        # Determine page count; if more pages needed than content, add blank pages
        page = doc.new_page(width=612, height=792)  # Letter size
        # Insert text into a textbox with margins
        rect = pymupdf.Rect(72, 72, 540, 720)
        page.insert_textbox(
            rect,
            page_text,
            fontsize=11,
            fontname="tiro",  # Times-Roman for legal docs
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )

    # Add any extra blank pages to reach target page count
    while doc.page_count < spec["pages"]:
        doc.new_page(width=612, height=792)

    # Set metadata
    doc.set_metadata({
        "title": spec["title"],
        "author": spec["author"],
        "creationDate": spec["creationDate"],
        "creator": "Legal Filing System",
        "producer": "PyMuPDF",
    })

    doc.save(output_path)
    doc.close()
    print(f"Created: {output_path}")


def create_initial():
    os.makedirs(BATCH_DIR, exist_ok=True)

    for spec in PDF_SPECS:
        output_path = os.path.join(BATCH_DIR, spec["filename"])
        create_pdf(spec, output_path)

    # Verify no metadata_report.txt exists (that's what the agent must create)
    report_path = os.path.join(BATCH_DIR, "metadata_report.txt")
    if os.path.exists(report_path):
        os.remove(report_path)

    print(f"\nCreated {len(PDF_SPECS)} PDF files in {BATCH_DIR}")
    print("Files:")
    for spec in PDF_SPECS:
        print(f"  - {spec['filename']} ({spec['pages']} pages)")

    # Open file manager to the directory
    launch_gui(f'nautilus "{BATCH_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus file manager with DISPLAY=:0')


create_initial()
