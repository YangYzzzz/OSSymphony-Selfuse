"""
Initial Setup: Create plain_letter.pdf (3 pages) and letterhead.pdf (1 page template)
Task ID: pdf_fm_073
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_073'
DOCS_DIR = f'{WORKDIR}/Documents'
TEMPLATES_DIR = f'{DOCS_DIR}/templates'
PLAIN_LETTER = f'{DOCS_DIR}/plain_letter.pdf'
LETTERHEAD = f'{TEMPLATES_DIR}/letterhead.pdf'


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


def create_letterhead():
    """Create a 1-page letterhead template with company header and footer design."""
    os.makedirs(TEMPLATES_DIR, exist_ok=True)

    doc = pymupdf.open()
    page = doc.new_page(width=612, height=792)  # US Letter

    # --- Company Header ---
    # Header background bar
    shape = page.new_shape()
    header_rect = pymupdf.Rect(0, 0, 612, 85)
    shape.draw_rect(header_rect)
    shape.finish(color=None, fill=(0.12, 0.24, 0.45))  # dark navy fill
    shape.commit()

    # Company name
    page.insert_text(
        pymupdf.Point(50, 42),
        "Meridian Global Solutions",
        fontsize=22,
        fontname="hebo",
        color=(1, 1, 1),
    )

    # Company tagline
    page.insert_text(
        pymupdf.Point(50, 62),
        "Innovative Consulting | Strategic Advisory | Digital Transformation",
        fontsize=9,
        fontname="heit",
        color=(0.8, 0.85, 0.95),
    )

    # Accent line under header
    shape2 = page.new_shape()
    shape2.draw_line(pymupdf.Point(0, 86), pymupdf.Point(612, 86))
    shape2.finish(color=(0.85, 0.55, 0.15), width=3)  # gold accent line
    shape2.commit()

    # --- Footer ---
    # Footer line
    shape3 = page.new_shape()
    shape3.draw_line(pymupdf.Point(50, 740), pymupdf.Point(562, 740))
    shape3.finish(color=(0.12, 0.24, 0.45), width=1)
    shape3.commit()

    # Footer text
    page.insert_text(
        pymupdf.Point(50, 758),
        "1200 Commerce Blvd, Suite 450, San Francisco, CA 94107",
        fontsize=8,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )
    page.insert_text(
        pymupdf.Point(50, 770),
        "Tel: (415) 555-0192  |  info@meridianglobal.com  |  www.meridianglobal.com",
        fontsize=8,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )

    doc.save(LETTERHEAD)
    doc.close()
    print(f"Letterhead template created: {LETTERHEAD}")


def create_plain_letter():
    """Create a 3-page plain text business letter with no background/branding."""
    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # --- Page 1 ---
    page1 = doc.new_page(width=612, height=792)
    y = 100
    # Date
    page1.insert_text(pymupdf.Point(72, y), "March 28, 2026", fontsize=11, fontname="helv", color=(0, 0, 0))
    y += 30

    # Recipient address
    lines_addr = [
        "Ms. Elena Rodriguez",
        "Chief Technology Officer",
        "Vertex Dynamics Inc.",
        "4500 Innovation Parkway",
        "Austin, TX 78759",
    ]
    for line in lines_addr:
        page1.insert_text(pymupdf.Point(72, y), line, fontsize=11, fontname="helv", color=(0, 0, 0))
        y += 16
    y += 14

    page1.insert_text(pymupdf.Point(72, y), "Dear Ms. Rodriguez,", fontsize=11, fontname="helv", color=(0, 0, 0))
    y += 26

    # Subject line
    page1.insert_text(pymupdf.Point(72, y), "Re: Proposal for Enterprise Digital Transformation Initiative", fontsize=11, fontname="hebo", color=(0, 0, 0))
    y += 26

    # Body paragraphs - page 1
    body_p1 = [
        "Thank you for taking the time to meet with our team last Thursday to discuss Vertex Dynamics' "
        "strategic goals for the upcoming fiscal year. We were impressed by the clarity of your vision "
        "for modernizing your technology infrastructure, and we are confident that Meridian Global Solutions "
        "is uniquely positioned to help you achieve these objectives.",

        "Following our discussion, we have prepared a comprehensive proposal that addresses the three "
        "primary areas you identified: legacy system migration, cloud-native application development, "
        "and enterprise data analytics modernization. Each of these workstreams has been carefully scoped "
        "to align with the timeline and budgetary parameters you outlined.",

        "Phase 1: Legacy System Migration (Q2-Q3 2026)",

        "Our analysis of your current SAP ERP environment indicates that a phased migration to the "
        "cloud-hosted solution would minimize disruption to your daily operations. We propose beginning "
        "with the finance and procurement modules, which our assessment shows carry the lowest integration "
        "risk. The estimated timeline for this phase is 14 weeks, with a dedicated team of six consultants "
        "working alongside your internal IT staff.",

        "The migration will follow our proven CloudBridge methodology, which has been successfully deployed "
        "at over 40 enterprise clients. Key milestones include an initial environment provisioning sprint, "
        "followed by iterative data migration cycles with continuous validation checkpoints.",
    ]

    content_rect = pymupdf.Rect(72, y, 540, 740)
    text = "\n\n".join(body_p1)
    page1.insert_textbox(content_rect, text, fontsize=11, fontname="helv", color=(0, 0, 0), align=0)

    # --- Page 2 ---
    page2 = doc.new_page(width=612, height=792)
    body_p2 = [
        "Phase 2: Cloud-Native Application Development (Q3-Q4 2026)",

        "Based on the requirements gathered from your product engineering team, we recommend developing "
        "three customer-facing microservices using a Kubernetes-based architecture hosted on AWS. This "
        "approach provides the scalability and resilience that your growing user base demands, while "
        "maintaining compatibility with your existing API gateway infrastructure.",

        "Our development team will employ an agile sprint model with two-week iterations. Each sprint "
        "will conclude with a demo session for your stakeholders, ensuring continuous alignment with "
        "business requirements. We anticipate delivering a production-ready MVP within 16 weeks.",

        "Phase 3: Enterprise Data Analytics Modernization (Q4 2026 - Q1 2027)",

        "The third workstream focuses on transforming your data analytics capabilities. We propose "
        "implementing a modern data lakehouse architecture that consolidates your currently fragmented "
        "data sources into a unified analytical platform. This will enable the self-service analytics "
        "capabilities your business intelligence team has been requesting.",

        "Key deliverables include a centralized data catalog, automated ETL pipelines for your top "
        "15 data sources, and a suite of executive dashboards built on Tableau. Our data engineering "
        "team has extensive experience with similar transformations in the manufacturing sector, and "
        "we expect this phase to be completed within 18 weeks.",

        "Investment Summary",

        "The total investment for the three-phase program is $2,450,000, broken down as follows:\n"
        "  - Phase 1 (Legacy Migration): $680,000\n"
        "  - Phase 2 (Cloud-Native Dev): $920,000\n"
        "  - Phase 3 (Analytics Modernization): $850,000",

        "This pricing reflects a 12% volume discount from our standard consulting rates, in recognition "
        "of the long-term partnership we hope to build with Vertex Dynamics. Payment terms are net-30, "
        "billed monthly based on actual hours and materials consumed.",
    ]

    content_rect2 = pymupdf.Rect(72, 72, 540, 740)
    text2 = "\n\n".join(body_p2)
    page2.insert_textbox(content_rect2, text2, fontsize=11, fontname="helv", color=(0, 0, 0), align=0)

    # --- Page 3 ---
    page3 = doc.new_page(width=612, height=792)
    body_p3 = [
        "Team Composition and Governance",

        "We will assign a dedicated engagement manager, Dr. James Whitfield, who will serve as your "
        "single point of contact throughout the program. James brings 18 years of experience leading "
        "enterprise transformation projects and has worked with three Fortune 500 companies in your "
        "industry vertical.",

        "In addition, each phase will have a designated technical lead:\n"
        "  - Phase 1: Sarah Nakamura, Senior Cloud Architect (AWS Certified Solutions Architect Professional)\n"
        "  - Phase 2: David Okonkwo, Principal Software Engineer (12 years in microservices architecture)\n"
        "  - Phase 3: Maria Castellano, Head of Data Engineering (former Databricks Solutions Architect)",

        "Governance will follow a tiered model with weekly operational standups, bi-weekly steering "
        "committee meetings, and monthly executive briefings. We will use Jira for project tracking "
        "and Confluence for documentation, integrated with your existing Atlassian suite.",

        "Next Steps",

        "We would welcome the opportunity to present this proposal in detail to your leadership team. "
        "Our suggestion is to schedule a 90-minute working session during the week of April 14th, where "
        "we can walk through the technical architecture, timeline, and risk mitigation strategies.",

        "Please do not hesitate to contact me directly at (415) 555-0192 or via email at "
        "r.martinez@meridianglobal.com if you have any questions or require additional information.",

        "We look forward to the possibility of working together to drive Vertex Dynamics' digital "
        "transformation forward.",
    ]

    content_rect3 = pymupdf.Rect(72, 72, 540, 560)
    text3 = "\n\n".join(body_p3)
    page3.insert_textbox(content_rect3, text3, fontsize=11, fontname="helv", color=(0, 0, 0), align=0)

    # Closing
    y_close = 590
    page3.insert_text(pymupdf.Point(72, y_close), "Sincerely,", fontsize=11, fontname="helv", color=(0, 0, 0))
    y_close += 40
    page3.insert_text(pymupdf.Point(72, y_close), "Ricardo Martinez", fontsize=11, fontname="hebo", color=(0, 0, 0))
    y_close += 16
    page3.insert_text(pymupdf.Point(72, y_close), "Managing Director", fontsize=11, fontname="helv", color=(0, 0, 0))
    y_close += 16
    page3.insert_text(pymupdf.Point(72, y_close), "Meridian Global Solutions", fontsize=11, fontname="helv", color=(0, 0, 0))

    doc.save(PLAIN_LETTER)
    doc.close()
    print(f"Plain letter created: {PLAIN_LETTER}")


def install_pdftk_wrapper():
    """
    Install a pdftk wrapper script that uses pymupdf to handle the 'background' subcommand.
    This makes 'pdftk' available as a command-line tool on the VM.
    """
    wrapper_script = r'''#!/usr/bin/env python3
"""
pdftk-compatible wrapper using PyMuPDF.
Supports: pdftk <input> background <bg_pdf> output <output_pdf>
"""
import sys
import pymupdf

def apply_background(input_pdf, bg_pdf, output_pdf):
    """Apply a background PDF to every page of the input PDF."""
    letter = pymupdf.open(input_pdf)
    bg = pymupdf.open(bg_pdf)

    output = pymupdf.open()
    for i in range(len(letter)):
        # Start with a copy of the background page
        bg_page_idx = min(i, len(bg) - 1)
        output.insert_pdf(bg, from_page=bg_page_idx, to_page=bg_page_idx)
        new_page = output[-1]
        # Overlay the letter content on top
        new_page.show_pdf_page(new_page.rect, letter, pno=i, overlay=True)

    output.save(output_pdf)
    output.close()
    letter.close()
    bg.close()

def main():
    args = sys.argv[1:]
    if len(args) < 5:
        print("Usage: pdftk <input.pdf> background <bg.pdf> output <output.pdf>")
        sys.exit(1)

    input_pdf = args[0]
    if args[1].lower() == 'background' and args[3].lower() == 'output':
        bg_pdf = args[2]
        output_pdf = args[4]
        apply_background(input_pdf, bg_pdf, output_pdf)
        print(f"Background applied: {output_pdf}")
    elif args[1].lower() == 'stamp' and args[3].lower() == 'output':
        # stamp is overlay (foreground), same implementation but reversed
        bg_pdf = args[2]
        output_pdf = args[4]
        # For stamp, the "stamp" goes on top
        letter = pymupdf.open(input_pdf)
        stamp = pymupdf.open(bg_pdf)
        output = pymupdf.open()
        for i in range(len(letter)):
            output.insert_pdf(letter, from_page=i, to_page=i)
            new_page = output[-1]
            stamp_idx = min(i, len(stamp) - 1)
            new_page.show_pdf_page(new_page.rect, stamp, pno=stamp_idx, overlay=True)
        output.save(output_pdf)
        output.close()
        letter.close()
        stamp.close()
        print(f"Stamp applied: {output_pdf}")
    else:
        print(f"Unsupported pdftk operation: {' '.join(args)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
'''
    wrapper_path = '/home/user/.local/bin/pdftk'
    os.makedirs('/home/user/.local/bin', exist_ok=True)
    with open(wrapper_path, 'w') as f:
        f.write(wrapper_script)
    os.chmod(wrapper_path, 0o755)

    # Ensure ~/.local/bin is on PATH by adding to .bashrc if not already
    bashrc = '/home/user/.bashrc'
    path_line = 'export PATH="$HOME/.local/bin:$PATH"'
    try:
        with open(bashrc, 'r') as f:
            content = f.read()
        if '.local/bin' not in content:
            with open(bashrc, 'a') as f:
                f.write(f'\n{path_line}\n')
    except FileNotFoundError:
        with open(bashrc, 'w') as f:
            f.write(f'{path_line}\n')

    # Also create a symlink-style approach: add to /usr/local/bin via a profile.d
    # Since we can't write to /usr/local/bin, the PATH approach is sufficient
    print(f"pdftk wrapper installed: {wrapper_path}")
    # Quick test
    result = subprocess.run([wrapper_path, '--help'], capture_output=True, text=True)
    print(f"pdftk test: returncode={result.returncode}")


def main():
    create_letterhead()
    create_plain_letter()
    install_pdftk_wrapper()

    # Open the plain letter in Evince so the agent can see it
    launch_gui(f'evince "{PLAIN_LETTER}"', delay_sec=2.0)

    # Also open a file manager showing the Documents folder
    launch_gui(f'nautilus "{DOCS_DIR}"', delay_sec=1.0)

    print('GUI_READY: launched Evince and Nautilus with DISPLAY=:0')


main()
