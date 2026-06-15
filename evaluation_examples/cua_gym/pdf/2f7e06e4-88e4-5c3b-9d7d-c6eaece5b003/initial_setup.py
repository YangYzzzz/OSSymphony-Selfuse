"""
Initial Setup: Create an encrypted classified PDF with owner password restrictions.
Task ID: pdf_mbc_013
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_013'
SECURE_DIR = f'{WORKDIR}/Secure'
OUTPUT = f'{SECURE_DIR}/classified.pdf'


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
    os.makedirs(SECURE_DIR, exist_ok=True)

    import pymupdf

    # ---- Build a realistic multi-page classified document ----
    doc = pymupdf.open()

    # --- Page 1: Cover page ---
    page = doc.new_page(width=612, height=792)  # US Letter
    page.insert_text(
        pymupdf.Point(200, 80),
        "CLASSIFIED",
        fontsize=36,
        fontname="hebo",
        color=(0.7, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(130, 140),
        "Project Meridian - Phase IV",
        fontsize=22,
        fontname="hebo",
        color=(0, 0, 0),
    )
    page.insert_text(
        pymupdf.Point(170, 200),
        "Strategic Operations Brief",
        fontsize=16,
        fontname="heit",
        color=(0.3, 0.3, 0.3),
    )

    # Classification block
    rect = pymupdf.Rect(72, 280, 540, 500)
    page.insert_textbox(
        rect,
        (
            "Document Classification: TOP SECRET / SCI\n"
            "Originating Agency: National Security Directorate\n"
            "Date of Issue: 2025-09-14\n"
            "Control Number: NSD-MER-2025-0473\n\n"
            "Distribution: Eyes Only - Cleared personnel with\n"
            "TS/SCI access and Project Meridian read-in.\n\n"
            "Unauthorized disclosure of this document is subject\n"
            "to penalties under 18 U.S.C. Sections 793 and 798."
        ),
        fontsize=12,
        fontname="helv",
        color=(0, 0, 0),
    )

    # Footer
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 700), pymupdf.Point(540, 700))
    shape.finish(color=(0.5, 0, 0), width=1.5)
    shape.commit()
    page.insert_text(
        pymupdf.Point(72, 720),
        "Prepared by: Dr. Elena Vasquez, Chief Analyst",
        fontsize=10,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )
    page.insert_text(
        pymupdf.Point(72, 740),
        "Reviewed by: Gen. Robert S. Hartley, Operations Director",
        fontsize=10,
        fontname="helv",
        color=(0.3, 0.3, 0.3),
    )

    # --- Page 2: Executive Summary ---
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(
        pymupdf.Point(72, 60),
        "EXECUTIVE SUMMARY",
        fontsize=18,
        fontname="hebo",
        color=(0, 0, 0.5),
    )

    summary_text = (
        "Project Meridian Phase IV represents a significant advancement in "
        "our signals intelligence capabilities across the Indo-Pacific theater. "
        "Over the past 18 months, field teams have successfully deployed 47 "
        "collection nodes across 12 allied partner nations, achieving a 340% "
        "increase in intercept volume compared to Phase III.\n\n"
        "Key achievements during the reporting period include:\n\n"
        "1. Integration of the PRISM-7 analytical framework with existing "
        "SIGINT processing pipelines, reducing analysis latency from 72 hours "
        "to under 6 hours for priority targets.\n\n"
        "2. Establishment of redundant communication channels with Station "
        "Alpha (Singapore), Station Bravo (Darwin), and Station Charlie "
        "(Yokosuka), ensuring 99.7% uptime across the network.\n\n"
        "3. Successful recruitment and vetting of 23 additional analysts with "
        "native-level proficiency in Mandarin, Bahasa, Vietnamese, and Thai.\n\n"
        "4. Completion of the Neptune submarine cable tap at coordinates "
        "redacted per OPSEC requirements, yielding approximately 2.3 TB of "
        "raw intercept data per day.\n\n"
        "Budget expenditure for Phase IV totaled $847.3 million against an "
        "authorized ceiling of $900 million, representing a 5.9% under-spend "
        "attributable to procurement efficiencies negotiated with contractor "
        "Raytheon-Northrop Systems Integration."
    )

    rect2 = pymupdf.Rect(72, 90, 540, 750)
    page2.insert_textbox(
        rect2,
        summary_text,
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 3: Operational Details ---
    page3 = doc.new_page(width=612, height=792)
    page3.insert_text(
        pymupdf.Point(72, 60),
        "OPERATIONAL ASSESSMENT",
        fontsize=18,
        fontname="hebo",
        color=(0, 0, 0.5),
    )

    ops_text = (
        "Threat Environment Analysis\n\n"
        "The current threat posture across the Indo-Pacific region remains "
        "elevated. Adversarial cyber operations attributed to APT-41 and "
        "APT-31 have increased 78% year-over-year, with particular focus on "
        "maritime domain awareness systems and satellite communication "
        "infrastructure.\n\n"
        "Our assessment indicates that foreign intelligence services have "
        "increased counterintelligence operations targeting allied SIGINT "
        "facilities by approximately 45% since January 2025. Two attempted "
        "physical intrusions at Station Bravo were detected and neutralized "
        "in March and June respectively.\n\n"
        "Resource Allocation for Phase V\n\n"
        "Based on current operational tempo and projected threat evolution, "
        "the directorate recommends an authorized budget of $1.12 billion "
        "for Phase V, representing a 24.6% increase over Phase IV. Key "
        "investment areas include:\n\n"
        "- Quantum-resistant encryption deployment: $180M\n"
        "- Next-generation collection platform development: $340M\n"
        "- Analyst workforce expansion (38 positions): $52M\n"
        "- Infrastructure hardening at forward stations: $95M\n"
        "- Contingency and operational reserve: $120M\n\n"
        "Timeline: Phase V is projected to commence Q1 2026 pending "
        "Congressional notification and appropriation confirmation."
    )

    rect3 = pymupdf.Rect(72, 90, 540, 750)
    page3.insert_textbox(
        rect3,
        ops_text,
        fontsize=11,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Set metadata ---
    doc.set_metadata({
        "title": "Project Meridian Phase IV - Strategic Operations Brief",
        "author": "Dr. Elena Vasquez",
        "subject": "Classified Operations Assessment",
        "keywords": "classified, meridian, phase-iv, sigint",
        "creator": "National Security Directorate",
        "producer": "NSD Document Systems",
    })

    # --- Set TOC ---
    toc = [
        [1, "Cover Page", 1],
        [1, "Executive Summary", 2],
        [1, "Operational Assessment", 3],
    ]
    doc.set_toc(toc)

    # Save unencrypted first
    tmp_path = f'{SECURE_DIR}/classified_tmp.pdf'
    doc.save(tmp_path)
    doc.close()

    # Now encrypt with pikepdf
    import pikepdf

    pdf = pikepdf.open(tmp_path)
    pdf.save(
        OUTPUT,
        encryption=pikepdf.Encryption(
            owner="oldpass123",
            user="",              # empty user password - opens freely
            R=6,                  # AES-256
            allow=pikepdf.Permissions(
                extract=False,           # no copying
                modify_annotation=False, # no editing
                print_lowres=True,       # allow printing
                print_highres=True,      # allow printing
                modify_form=False,       # no form editing
                modify_other=False,      # no other modifications
                modify_assembly=False,   # no page assembly
            ),
        ),
    )
    pdf.close()

    # Clean up temp file
    os.remove(tmp_path)

    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
