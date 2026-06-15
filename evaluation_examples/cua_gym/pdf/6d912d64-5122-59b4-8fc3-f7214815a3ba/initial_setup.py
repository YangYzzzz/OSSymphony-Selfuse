"""
Initial Setup: Create a PDF/A-1b compliant PDF with proper XMP metadata
Task ID: pdf_mbc_032
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_032'
DOCUMENTS = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS}/compliant.pdf'


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
    os.makedirs(DOCUMENTS, exist_ok=True)

    # Remove any leftover pdfa_check.txt (must NOT exist in initial state)
    check_file = f'{DOCUMENTS}/pdfa_check.txt'
    if os.path.exists(check_file):
        os.remove(check_file)

    # Step 1: Create a realistic multi-page PDF using PyMuPDF
    import pymupdf

    doc = pymupdf.open()

    # --- Page 1: Title page ---
    page1 = doc.new_page(width=595, height=842)
    page1.insert_text(
        pymupdf.Point(150, 200),
        "Meridian Consulting Group",
        fontsize=24,
        fontname="hebo",
        color=(0.0, 0.15, 0.45),
    )
    page1.insert_text(
        pymupdf.Point(150, 250),
        "Annual Compliance Report",
        fontsize=18,
        fontname="helv",
        color=(0.2, 0.2, 0.2),
    )
    page1.insert_text(
        pymupdf.Point(150, 290),
        "Fiscal Year 2025 — Prepared for the Board of Directors",
        fontsize=11,
        fontname="tiit",
        color=(0.4, 0.4, 0.4),
    )

    # Horizontal rule
    shape1 = page1.new_shape()
    shape1.draw_line(pymupdf.Point(72, 320), pymupdf.Point(523, 320))
    shape1.finish(color=(0.0, 0.15, 0.45), width=2)
    shape1.commit()

    page1.insert_text(
        pymupdf.Point(150, 360),
        "Document Classification: Internal — Confidential",
        fontsize=10,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )
    page1.insert_text(
        pymupdf.Point(150, 385),
        "Date of Issue: March 15, 2025",
        fontsize=10,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )
    page1.insert_text(
        pymupdf.Point(150, 410),
        "Prepared by: Elena Vasquez, Chief Compliance Officer",
        fontsize=10,
        fontname="helv",
        color=(0.5, 0.5, 0.5),
    )

    # --- Page 2: Executive Summary ---
    page2 = doc.new_page(width=595, height=842)
    page2.insert_text(
        pymupdf.Point(72, 72),
        "1. Executive Summary",
        fontsize=16,
        fontname="hebo",
        color=(0.0, 0.15, 0.45),
    )

    summary_text = (
        "Meridian Consulting Group has maintained full regulatory compliance across all "
        "operational jurisdictions during fiscal year 2025. Our internal audit program "
        "identified zero material findings and three minor observations, all of which "
        "have been remediated as of February 28, 2025.\n\n"
        "Key highlights include:\n"
        "  • Successfully completed SOC 2 Type II recertification\n"
        "  • Achieved 99.7% employee compliance training completion rate\n"
        "  • Implemented enhanced data protection measures across 14 regional offices\n"
        "  • Resolved all prior-year findings with documented corrective actions\n\n"
        "Total compliance expenditure for the period was $1,247,500, representing a 6.2% "
        "increase from the prior year, primarily driven by expanded cybersecurity measures "
        "and additional regulatory requirements in the APAC region."
    )
    rect2 = pymupdf.Rect(72, 100, 523, 500)
    page2.insert_textbox(rect2, summary_text, fontsize=11, fontname="helv",
                         color=(0.1, 0.1, 0.1), align=pymupdf.TEXT_ALIGN_LEFT)

    # --- Page 3: Compliance Metrics ---
    page3 = doc.new_page(width=595, height=842)
    page3.insert_text(
        pymupdf.Point(72, 72),
        "2. Compliance Metrics Overview",
        fontsize=16,
        fontname="hebo",
        color=(0.0, 0.15, 0.45),
    )

    metrics_text = (
        "The following table summarizes key compliance metrics tracked throughout FY2025.\n\n"
        "Metric                               Target    Actual    Status\n"
        "─────────────────────────────────────────────────────────────\n"
        "Training Completion Rate              98.0%     99.7%     PASS\n"
        "Incident Response Time (avg)          < 4 hrs   2.8 hrs   PASS\n"
        "Policy Acknowledgment Rate            100%      100%      PASS\n"
        "Vendor Risk Assessments Completed     100%      97.3%     REVIEW\n"
        "Data Breach Incidents                 0         0         PASS\n"
        "Regulatory Filing Timeliness          100%      100%      PASS\n"
        "Internal Audit Findings (Material)    0         0         PASS\n"
        "Internal Audit Findings (Minor)       ≤ 5       3         PASS\n"
        "─────────────────────────────────────────────────────────────\n\n"
        "Overall compliance posture: STRONG. The vendor risk assessment shortfall is "
        "attributed to delayed responses from two newly onboarded suppliers in Q3. "
        "Corrective actions are underway with expected completion by April 30, 2025."
    )
    rect3 = pymupdf.Rect(72, 100, 523, 600)
    page3.insert_textbox(rect3, metrics_text, fontsize=10, fontname="cour",
                         color=(0.1, 0.1, 0.1), align=pymupdf.TEXT_ALIGN_LEFT)

    # --- Page 4: Regional Breakdown ---
    page4 = doc.new_page(width=595, height=842)
    page4.insert_text(
        pymupdf.Point(72, 72),
        "3. Regional Compliance Breakdown",
        fontsize=16,
        fontname="hebo",
        color=(0.0, 0.15, 0.45),
    )

    regional_text = (
        "North America (7 offices)\n"
        "All offices achieved full compliance. New York and Toronto offices completed "
        "enhanced financial regulatory training ahead of schedule.\n\n"
        "Europe (4 offices)\n"
        "GDPR compliance maintained at 100%. London office led a successful cross-border "
        "data transfer audit under the EU-US Data Privacy Framework.\n\n"
        "Asia-Pacific (3 offices)\n"
        "Singapore and Tokyo offices fully compliant. Sydney office flagged one minor "
        "finding related to local privacy notification requirements, resolved January 2025.\n\n"
        "Recommendations:\n"
        "  1. Expand APAC compliance team by 2 FTEs to support regulatory growth\n"
        "  2. Implement automated vendor risk monitoring platform (Q2 2025)\n"
        "  3. Establish quarterly cross-regional compliance sync meetings\n"
        "  4. Update data retention policies to align with new EU Digital Services Act"
    )
    rect4 = pymupdf.Rect(72, 100, 523, 600)
    page4.insert_textbox(rect4, regional_text, fontsize=11, fontname="helv",
                         color=(0.1, 0.1, 0.1), align=pymupdf.TEXT_ALIGN_LEFT)

    # Set metadata
    doc.set_metadata({
        "title": "Annual Compliance Report FY2025",
        "author": "Elena Vasquez",
        "subject": "Regulatory Compliance",
        "keywords": "compliance, audit, regulatory, FY2025",
        "creator": "Meridian Consulting Group",
        "producer": "PDF/A Generator",
    })

    # Set TOC
    toc = [
        [1, "Executive Summary", 2],
        [1, "Compliance Metrics Overview", 3],
        [1, "Regional Compliance Breakdown", 4],
    ]
    doc.set_toc(toc)

    # Save the base PDF first
    doc.save(OUTPUT)
    doc.close()

    # Step 2: Now inject PDF/A-1b XMP metadata using pikepdf
    import pikepdf

    pdf = pikepdf.open(OUTPUT, allow_overwriting_input=True)

    with pdf.open_metadata() as meta:
        # Set PDF/A identification in XMP
        meta['pdfaid:part'] = '1'
        meta['pdfaid:conformance'] = 'B'
        # Also set standard metadata
        meta['dc:title'] = 'Annual Compliance Report FY2025'
        meta['dc:creator'] = ['Elena Vasquez']
        meta['dc:description'] = 'Meridian Consulting Group Annual Compliance Report for Fiscal Year 2025'
        meta['xmp:CreatorTool'] = 'PDF/A Generator'
        meta['pdf:Producer'] = 'pikepdf PDF/A Generator'

    pdf.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # Verify the XMP metadata was written correctly
    pdf2 = pikepdf.open(OUTPUT, allow_overwriting_input=True)
    with pdf2.open_metadata() as meta2:
        part = meta2.get('pdfaid:part', 'NOT FOUND')
        conf = meta2.get('pdfaid:conformance', 'NOT FOUND')
        print(f'Verification - pdfaid:part={part}, pdfaid:conformance={conf}')
    pdf2.close()

    # GUI-ready: open the PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
