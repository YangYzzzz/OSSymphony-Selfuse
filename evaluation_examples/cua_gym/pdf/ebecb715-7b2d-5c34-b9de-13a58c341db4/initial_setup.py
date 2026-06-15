"""
Initial Setup: Create a court submission PDF with metadata for a legal case.
Task ID: pdf_legal_059
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf


WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_059'
LEGAL_DIR = f'{WORKDIR}/legal'
OUTPUT = f'{LEGAL_DIR}/court_submission.pdf'


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

    doc = pymupdf.open()

    # --- Page 1: Title / Cover page ---
    page1 = doc.new_page(width=612, height=792)  # Letter size
    # Court header
    page1.insert_text(pymupdf.Point(180, 72), "UNITED STATES DISTRICT COURT", fontsize=13, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(170, 92), "NORTHERN DISTRICT OF CALIFORNIA", fontsize=13, fontname="hebo", color=(0, 0, 0))
    # Horizontal rule
    shape = page1.new_shape()
    shape.draw_line(pymupdf.Point(72, 110), pymupdf.Point(540, 110))
    shape.finish(color=(0, 0, 0), width=1.5)
    shape.commit()

    page1.insert_text(pymupdf.Point(72, 140), "GREENFIELD TECHNOLOGIES, INC.,", fontsize=11, fontname="tibo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(300, 140), "Plaintiff,", fontsize=11, fontname="tiit", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(250, 165), "v.", fontsize=11, fontname="tiro", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 190), "HARTWELL DYNAMICS, LLC,", fontsize=11, fontname="tibo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(300, 190), "Defendant.", fontsize=11, fontname="tiit", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(380, 140), "Case No. 2024-CV-5678", fontsize=10, fontname="tiro", color=(0, 0, 0))

    # Title
    page1.insert_text(pymupdf.Point(150, 260), "OPPOSITION BRIEF", fontsize=18, fontname="hebo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(100, 290), "In Opposition to Defendant's Motion for Summary Judgment", fontsize=12, fontname="tiro", color=(0, 0, 0))

    # Attorney info
    page1.insert_text(pymupdf.Point(72, 600), "Respectfully submitted,", fontsize=11, fontname="tiro", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 630), "Jennifer Adams, Esq.", fontsize=11, fontname="tibo", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 650), "Bar No. 284571", fontsize=10, fontname="tiro", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 670), "Adams & Whitfield LLP", fontsize=10, fontname="tiro", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 690), "555 Market Street, Suite 1200", fontsize=10, fontname="tiro", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 710), "San Francisco, CA 94105", fontsize=10, fontname="tiro", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 730), "Tel: (415) 555-0192 | jadams@adamslegal.com", fontsize=10, fontname="tiro", color=(0, 0, 0))
    page1.insert_text(pymupdf.Point(72, 755), "Dated: March 28, 2024", fontsize=10, fontname="tiro", color=(0, 0, 0))

    # --- Page 2: Introduction & Factual Background ---
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(pymupdf.Point(72, 72), "I. INTRODUCTION", fontsize=13, fontname="hebo", color=(0, 0, 0))
    intro_text = (
        "Plaintiff Greenfield Technologies, Inc. respectfully submits this opposition "
        "to Defendant Hartwell Dynamics, LLC's Motion for Summary Judgment. As set forth "
        "below, genuine disputes of material fact preclude summary disposition of this "
        "action. The evidence, viewed in the light most favorable to Plaintiff as the "
        "non-moving party, demonstrates that Defendant misappropriated Plaintiff's "
        "proprietary signal-processing algorithms and incorporated them into the DynaCore "
        "3000 product line without authorization or compensation."
    )
    page2.insert_textbox(pymupdf.Rect(72, 95, 540, 250), intro_text, fontsize=11, fontname="tiro", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page2.insert_text(pymupdf.Point(72, 270), "II. FACTUAL BACKGROUND", fontsize=13, fontname="hebo", color=(0, 0, 0))
    facts_text = (
        "On or about June 15, 2021, Plaintiff and Defendant entered into a Non-Disclosure "
        "Agreement (the \"NDA\") in connection with a proposed joint development venture. "
        "Under the NDA, Plaintiff disclosed detailed technical specifications for its "
        "GreenWave proprietary algorithm suite, including source code excerpts, performance "
        "benchmarks, and integration protocols. The NDA expressly prohibited Defendant from "
        "using the Confidential Information for any purpose other than evaluating the proposed "
        "joint venture.\n\n"
        "Despite these contractual restrictions, forensic analysis conducted by Dr. Raymond "
        "Cho of Stanford University's Computer Science Department confirms that the DynaCore "
        "3000 firmware contains code segments with a 94.7% structural similarity to GreenWave "
        "algorithm modules. The joint venture discussions terminated in October 2021, yet "
        "Defendant launched the DynaCore 3000 product in February 2023, incorporating "
        "Plaintiff's proprietary technology without consent."
    )
    page2.insert_textbox(pymupdf.Rect(72, 293, 540, 570), facts_text, fontsize=11, fontname="tiro", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page2.insert_text(pymupdf.Point(72, 590), "III. LEGAL STANDARD", fontsize=13, fontname="hebo", color=(0, 0, 0))
    standard_text = (
        "Summary judgment is appropriate only when there is no genuine dispute as to any "
        "material fact and the movant is entitled to judgment as a matter of law. Fed. R. Civ. "
        "P. 56(a). The court must view the evidence in the light most favorable to the "
        "nonmoving party and draw all reasonable inferences in that party's favor. Anderson v. "
        "Liberty Lobby, Inc., 477 U.S. 242, 255 (1986)."
    )
    page2.insert_textbox(pymupdf.Rect(72, 613, 540, 760), standard_text, fontsize=11, fontname="tiro", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # --- Page 3: Argument ---
    page3 = doc.new_page(width=612, height=792)
    page3.insert_text(pymupdf.Point(72, 72), "IV. ARGUMENT", fontsize=13, fontname="hebo", color=(0, 0, 0))
    page3.insert_text(pymupdf.Point(72, 100), "A. Genuine Disputes of Material Fact Exist", fontsize=12, fontname="tibo", color=(0, 0, 0))
    arg_text = (
        "Defendant argues that its DynaCore 3000 firmware was independently developed. However, "
        "the record evidence creates, at minimum, a triable issue of fact on this question. "
        "Specifically:\n\n"
        "1. Dr. Cho's expert report identifies 47 distinct code modules in DynaCore 3000 that "
        "mirror GreenWave algorithms in structure, variable naming conventions, and computational "
        "logic, including identical optimization constants that have no independent derivation.\n\n"
        "2. Former Hartwell engineer Lisa Park testified in her deposition that she was instructed "
        "by her supervisor, David Reeves, to \"review the Greenfield materials\" during the "
        "DynaCore development cycle. (Park Dep. at 87:14-88:3.)\n\n"
        "3. Digital forensics show that eight Hartwell employees accessed the shared repository "
        "containing Plaintiff's confidential materials 214 times between November 2021 and "
        "January 2023 -- well after the joint venture discussions ended."
    )
    page3.insert_textbox(pymupdf.Rect(72, 120, 540, 460), arg_text, fontsize=11, fontname="tiro", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    page3.insert_text(pymupdf.Point(72, 480), "B. Defendant's Independent Development Claim Fails", fontsize=12, fontname="tibo", color=(0, 0, 0))
    arg2_text = (
        "Defendant's assertion of independent development is contradicted by the timeline of "
        "events. Defendant had no comparable signal-processing capability prior to receiving "
        "Plaintiff's confidential disclosures. Defendant's own internal project documents, "
        "produced in discovery, describe the DynaCore algorithms as \"building on the framework "
        "shared during the Greenfield collaboration.\" (Ex. 14 at HART000892.)\n\n"
        "The Ninth Circuit has held that even partial reliance on misappropriated trade secrets "
        "defeats a defense of independent development. Silvaco Data Sys. v. Intel Corp., "
        "184 Cal. App. 4th 210, 239 (2010)."
    )
    page3.insert_textbox(pymupdf.Rect(72, 500, 540, 740), arg2_text, fontsize=11, fontname="tiro", align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Set metadata
    doc.set_metadata({
        "title": "Opposition Brief",
        "author": "Jennifer Adams",
        "subject": "Case 2024-CV-5678",
        "keywords": "",
        "creator": "Adobe Acrobat",
        "producer": "Adobe Acrobat Pro DC",
    })

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
