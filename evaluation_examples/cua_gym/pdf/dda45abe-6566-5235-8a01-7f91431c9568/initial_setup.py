"""
Initial Setup: Create password-protected legal case PDF
Task ID: pdf_legal_050
Domain: pdf
"""

import os
import shlex
import subprocess
import time

import pymupdf
import pikepdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_050'
ARCHIVE_DIR = f'{WORKDIR}/legal/archived'
OUTPUT = f'{ARCHIVE_DIR}/case_2020.pdf'


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
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    # Create a realistic multi-page legal case document
    doc = pymupdf.open()

    # --- Page 1: Cover Page ---
    page = doc.new_page(width=612, height=792)  # US Letter
    page.insert_text(
        pymupdf.Point(72, 120),
        "SUPERIOR COURT OF THE STATE OF CALIFORNIA",
        fontsize=14,
        fontname="hebo",
        color=(0, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(72, 145),
        "COUNTY OF LOS ANGELES",
        fontsize=12,
        fontname="hebo",
        color=(0, 0, 0),
    )

    # Horizontal rule
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 170), pymupdf.Point(540, 170))
    shape.finish(color=(0, 0, 0), width=1.5)
    shape.commit()

    page.insert_text(
        pymupdf.Point(72, 210),
        "GREENFIELD PROPERTIES, LLC,",
        fontsize=12,
        fontname="hebo",
        color=(0, 0, 0),
    )
    page.insert_text(pymupdf.Point(300, 210), "Plaintiff,", fontsize=12, fontname="tiit")
    page.insert_text(pymupdf.Point(72, 240), "vs.", fontsize=12, fontname="tiro")
    page.insert_text(
        pymupdf.Point(72, 270),
        "PACIFIC RIM DEVELOPMENT CORP.,",
        fontsize=12,
        fontname="hebo",
        color=(0, 0, 0),
    )
    page.insert_text(pymupdf.Point(300, 270), "Defendant.", fontsize=12, fontname="tiit")

    page.insert_text(
        pymupdf.Point(350, 210),
        "Case No. BC-2020-04587",
        fontsize=11,
        fontname="tiro",
        color=(0, 0, 0),
    )

    page.insert_textbox(
        pymupdf.Rect(72, 340, 540, 400),
        "ORDER GRANTING PARTIAL SUMMARY JUDGMENT\nFiled: September 14, 2020",
        fontsize=14,
        fontname="hebo",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_CENTER,
    )

    page.insert_textbox(
        pymupdf.Rect(72, 440, 540, 520),
        "CONFIDENTIAL - ATTORNEY-CLIENT PRIVILEGED\n"
        "This document contains confidential legal materials protected under "
        "attorney-client privilege and work product doctrine. Unauthorized "
        "disclosure is strictly prohibited.",
        fontsize=10,
        fontname="tiit",
        color=(0.5, 0, 0),
        align=pymupdf.TEXT_ALIGN_CENTER,
    )

    # --- Page 2: Background ---
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(
        pymupdf.Point(72, 72),
        "I. BACKGROUND",
        fontsize=14,
        fontname="hebo",
        color=(0, 0, 0),
    )
    background_text = (
        "This matter arises from a commercial real estate transaction between "
        "Greenfield Properties, LLC (\"Plaintiff\") and Pacific Rim Development Corp. "
        "(\"Defendant\") involving the purchase and development of a 12.5-acre parcel "
        "located at 4500 Westchester Boulevard, Los Angeles, CA 90045.\n\n"
        "On March 15, 2019, the parties entered into a Purchase and Sale Agreement "
        "(\"PSA\") for the property at an agreed price of $18,750,000. The PSA included "
        "standard contingencies for environmental review, title clearance, and zoning "
        "approval. The closing date was set for June 30, 2019.\n\n"
        "During the due diligence period, Plaintiff retained Apex Environmental "
        "Consulting to conduct a Phase II Environmental Site Assessment. The assessment "
        "revealed the presence of petroleum hydrocarbons in soil samples at "
        "concentrations exceeding California Regional Water Quality Control Board "
        "action levels (TPH-d at 1,200 mg/kg vs. the 100 mg/kg threshold).\n\n"
        "Defendant was notified of the contamination findings on April 22, 2019. "
        "Defendant represented that remediation would be completed prior to closing. "
        "However, as of the scheduled closing date, remediation was incomplete, with "
        "an estimated additional cost of $2,350,000."
    )
    page2.insert_textbox(
        pymupdf.Rect(72, 100, 540, 720),
        background_text,
        fontsize=11,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 3: Legal Analysis ---
    page3 = doc.new_page(width=612, height=792)
    page3.insert_text(
        pymupdf.Point(72, 72),
        "II. LEGAL ANALYSIS",
        fontsize=14,
        fontname="hebo",
        color=(0, 0, 0),
    )
    analysis_text = (
        "A. Breach of Contract\n\n"
        "Under California Civil Code Section 1549, a contract is defined as an "
        "agreement to do or not to do a certain thing. The PSA constitutes a valid "
        "and enforceable contract between the parties.\n\n"
        "Defendant's failure to complete remediation as represented constitutes a "
        "material breach under the Restatement (Second) of Contracts Section 241. "
        "The five factors for materiality are met:\n\n"
        "  (a) Plaintiff was deprived of the benefit it reasonably expected;\n"
        "  (b) Plaintiff cannot be adequately compensated through damages alone;\n"
        "  (c) Defendant will not suffer undue forfeiture;\n"
        "  (d) Defendant's conduct was not in good faith; and\n"
        "  (e) The behavior is unlikely to be cured.\n\n"
        "B. Fraudulent Concealment\n\n"
        "Evidence obtained during discovery indicates that Defendant's principals, "
        "Robert K. Tanaka and Michelle S. Watanabe, were aware of prior contamination "
        "reports from 2016 that documented elevated benzene levels (47 ppb vs. the "
        "1 ppb MCL) in groundwater monitoring wells MW-3 and MW-7. These reports were "
        "not disclosed to Plaintiff during negotiations.\n\n"
        "Under California Civil Code Section 1710, Defendant's suppression of known "
        "material facts with the intent to induce Plaintiff to enter the PSA "
        "constitutes actual fraud."
    )
    page3.insert_textbox(
        pymupdf.Rect(72, 100, 540, 720),
        analysis_text,
        fontsize=11,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 4: Findings and Order ---
    page4 = doc.new_page(width=612, height=792)
    page4.insert_text(
        pymupdf.Point(72, 72),
        "III. FINDINGS OF FACT AND CONCLUSIONS OF LAW",
        fontsize=14,
        fontname="hebo",
        color=(0, 0, 0),
    )
    findings_text = (
        "Based on the foregoing analysis, the Court finds:\n\n"
        "1. The Purchase and Sale Agreement dated March 15, 2019, is a valid and "
        "enforceable contract between the parties.\n\n"
        "2. Defendant materially breached the PSA by failing to complete environmental "
        "remediation as represented.\n\n"
        "3. Defendant's principals had actual knowledge of prior contamination at the "
        "subject property and failed to disclose this information.\n\n"
        "4. Plaintiff has established the elements of fraudulent concealment under "
        "California Civil Code Section 1710.\n\n"
        "5. Damages in the amount of $2,350,000 for remediation costs, plus "
        "$875,000 in consequential damages for project delays, are awarded to Plaintiff.\n\n"
        "IV. ORDER\n\n"
        "IT IS HEREBY ORDERED that Plaintiff's Motion for Partial Summary Judgment "
        "on the breach of contract claim is GRANTED. Defendant Pacific Rim Development "
        "Corp. shall pay to Plaintiff Greenfield Properties, LLC the sum of "
        "$3,225,000 within sixty (60) days of this order.\n\n"
        "The fraudulent concealment claim shall proceed to trial, currently scheduled "
        "for January 11, 2021.\n\n"
        "SO ORDERED this 14th day of September, 2020.\n\n\n"
        "___________________________\n"
        "Hon. Margaret L. Chen\n"
        "Judge of the Superior Court"
    )
    page4.insert_textbox(
        pymupdf.Rect(72, 100, 540, 720),
        findings_text,
        fontsize=11,
        fontname="tiro",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Set metadata
    doc.set_metadata({
        "title": "Greenfield Properties v. Pacific Rim Development - Order",
        "author": "Superior Court of California, County of Los Angeles",
        "subject": "Partial Summary Judgment - Case No. BC-2020-04587",
        "keywords": "breach of contract, fraudulent concealment, environmental remediation",
        "creator": "Court Filing System",
    })

    # Set TOC
    toc = [
        [1, "Cover Page", 1],
        [1, "I. Background", 2],
        [1, "II. Legal Analysis", 3],
        [2, "A. Breach of Contract", 3],
        [2, "B. Fraudulent Concealment", 3],
        [1, "III. Findings of Fact and Conclusions of Law", 4],
        [1, "IV. Order", 4],
    ]
    doc.set_toc(toc)

    # Save unencrypted first
    tmp_path = f'{ARCHIVE_DIR}/case_2020_tmp.pdf'
    doc.save(tmp_path)
    doc.close()

    # Encrypt with pikepdf using user password 'oldpass123'
    pdf = pikepdf.open(tmp_path)
    pdf.save(
        OUTPUT,
        encryption=pikepdf.Encryption(
            owner="ownerold",
            user="oldpass123",
            R=6,
        ),
    )
    pdf.close()

    # Remove temp file
    os.remove(tmp_path)

    print(f'Initial file created: {OUTPUT}')

    # Open PDF in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
