"""
Initial Setup: Create construction_bid.pdf with 5 pages on ~/Desktop/.
Task ID: pdf_basic_184
Domain: pdf

Creates:
  ~/Desktop/construction_bid.pdf  — 5 pages (construction bid document)

Page 2 contains the text 'estimated completion: 6 months'.

The agent must:
  1. Open ~/Desktop/construction_bid.pdf in Evince.
  2. On page 2, add a strikethrough annotation over 'estimated completion: 6 months'.
  3. Add a sticky note (text annotation) on page 2 saying
     'Revised timeline: 4 months per updated schedule'.
  4. Save the file.

Opens construction_bid.pdf in Evince for the GUI agent to start with.
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

DESKTOP = '/home/user/Desktop'
OUTPUT = f'{DESKTOP}/construction_bid.pdf'

# Letter size dimensions in points (72 pts/inch)
PAGE_W, PAGE_H = 612, 792


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


def make_page(doc, page_num, total_pages, section_title, body_text):
    """Add a single styled construction bid page to doc."""
    page = doc.new_page(width=PAGE_W, height=PAGE_H)

    # Background — light cream
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 0, PAGE_W, PAGE_H))
    shape.finish(color=None, fill=(0.99, 0.98, 0.95), width=0)
    shape.commit()

    # Header band — dark green
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 0, PAGE_W, 58))
    shape.finish(color=None, fill=(0.12, 0.30, 0.18), width=0)
    shape.commit()

    # Header text: document title left, page number right
    page.insert_text(
        pymupdf.Point(36, 22),
        "CONSTRUCTION BID PROPOSAL",
        fontsize=11,
        fontname="hebo",
        color=(1.0, 1.0, 1.0),
    )
    page.insert_text(
        pymupdf.Point(36, 42),
        "Ridgemont Commercial Development — Phase II",
        fontsize=8,
        fontname="helv",
        color=(0.80, 0.92, 0.82),
    )
    page.insert_text(
        pymupdf.Point(530, 32),
        f"{page_num}/{total_pages}",
        fontsize=9,
        fontname="helv",
        color=(0.80, 0.92, 0.82),
    )

    # Thin divider below header
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(36, 72), pymupdf.Point(576, 72))
    shape.finish(color=(0.12, 0.30, 0.18), width=1.5)
    shape.commit()

    # Section title
    page.insert_text(
        pymupdf.Point(36, 100),
        section_title,
        fontsize=13,
        fontname="hebo",
        color=(0.12, 0.30, 0.18),
    )

    # Divider below section title
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(36, 108), pymupdf.Point(576, 108))
    shape.finish(color=(0.60, 0.72, 0.62), width=0.8)
    shape.commit()

    # Body text
    text_rect = pymupdf.Rect(36, 120, 576, 760)
    page.insert_textbox(
        text_rect,
        body_text,
        fontsize=10,
        fontname="helv",
        color=(0.10, 0.10, 0.10),
        align=pymupdf.TEXT_ALIGN_LEFT,
    )

    # Footer line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(36, 772), pymupdf.Point(576, 772))
    shape.finish(color=(0.70, 0.70, 0.70), width=0.5)
    shape.commit()

    page.insert_text(
        pymupdf.Point(36, 785),
        "Ridgemont Construction Group LLC  |  Confidential Bid Document  |  2024",
        fontsize=7.5,
        fontname="helv",
        color=(0.50, 0.50, 0.50),
    )


def create_initial():
    os.makedirs(DESKTOP, exist_ok=True)

    pages_content = [
        (
            "Section 1 — Bid Overview and Executive Summary",
            (
                "Project Name: Ridgemont Commercial Development Phase II\n"
                "Bid Reference: RCG-2024-BID-047\n"
                "Submission Date: October 14, 2024\n"
                "Prepared By: Ridgemont Construction Group LLC\n\n"
                "Executive Summary:\n"
                "Ridgemont Construction Group LLC is pleased to submit this formal\n"
                "bid proposal for the construction of the Ridgemont Commercial\n"
                "Development Phase II project. Our team brings over 25 years of\n"
                "experience in commercial construction, having successfully delivered\n"
                "more than 140 major projects across the Pacific Northwest region.\n\n"
                "This proposal covers all aspects of the construction scope including\n"
                "site preparation, foundation work, structural framing, mechanical\n"
                "and electrical systems, interior finishes, and final commissioning.\n\n"
                "Total Bid Value: $4,850,000 (Four Million Eight Hundred Fifty Thousand)\n"
                "Project Location: 1200 Harbor View Blvd, Portland, OR 97201\n"
                "Owner Representative: Pacific Shore Holdings, Inc.\n\n"
                "BID_PAGE_1_MARKER: Section 1 — Bid Overview"
            ),
        ),
        (
            "Section 2 — Project Schedule and Timeline",
            (
                "Project Commencement: January 6, 2025 (pending permit approval)\n"
                "Substantial Completion: July 7, 2025\n"
                "estimated completion: 6 months\n"
                "Final Acceptance: July 31, 2025\n\n"
                "Milestone Schedule:\n"
                "  Milestone 1 — Site Mobilization & Clearing:    Weeks 1–2\n"
                "  Milestone 2 — Excavation & Foundation:         Weeks 3–6\n"
                "  Milestone 3 — Structural Steel Erection:       Weeks 7–12\n"
                "  Milestone 4 — Exterior Envelope:               Weeks 11–16\n"
                "  Milestone 5 — MEP Rough-in:                    Weeks 13–18\n"
                "  Milestone 6 — Interior Finishes:               Weeks 17–22\n"
                "  Milestone 7 — Final Inspections & Commissioning: Weeks 23–26\n\n"
                "Schedule Assumptions:\n"
                "The above schedule is contingent upon: (a) receipt of all required\n"
                "building permits no later than December 20, 2024; (b) timely delivery\n"
                "of owner-furnished equipment per the schedule in Exhibit B;\n"
                "(c) unobstructed site access during all scheduled working hours;\n"
                "(d) no significant subsurface obstructions beyond those indicated\n"
                "in the provided geotechnical report.\n\n"
                "Weather Contingency: A 5-day weather delay contingency has been\n"
                "included in the schedule per Pacific Northwest climate norms.\n\n"
                "BID_PAGE_2_MARKER: Section 2 — Project Schedule and Timeline"
            ),
        ),
        (
            "Section 3 — Cost Breakdown and Bid Pricing",
            (
                "Division 01 — General Conditions:             $285,000\n"
                "Division 02 — Site Work & Demolition:         $310,000\n"
                "Division 03 — Concrete & Foundations:         $620,000\n"
                "Division 04 — Masonry:                        $155,000\n"
                "Division 05 — Structural Steel:               $730,000\n"
                "Division 06 — Rough Carpentry:                $110,000\n"
                "Division 07 — Thermal & Moisture Protection:  $185,000\n"
                "Division 08 — Doors, Windows & Glazing:       $210,000\n"
                "Division 09 — Finishes:                       $420,000\n"
                "Division 10 — Specialties:                     $65,000\n"
                "Division 15 — Mechanical (HVAC & Plumbing):   $560,000\n"
                "Division 16 — Electrical:                     $475,000\n"
                "Contingency (3%):                             $145,000\n"
                "Contractor Fee & Overhead (8%):               $380,000\n"
                "─────────────────────────────────────────────────────\n"
                "TOTAL BID PRICE:                            $4,850,000\n\n"
                "Unit Prices: Unit prices for changes in scope are listed in\n"
                "Exhibit C. All prices are firm for 60 days from submission.\n\n"
                "BID_PAGE_3_MARKER: Section 3 — Cost Breakdown and Bid Pricing"
            ),
        ),
        (
            "Section 4 — Qualifications and References",
            (
                "Contractor License: Oregon CCB #198445 | Washington RIDGECG123BN\n"
                "Bonding Capacity: $10,000,000 (Travelers Casualty & Surety Co.)\n"
                "Insurance: $5M General Liability | $2M Workers Compensation\n\n"
                "Selected Project References:\n\n"
                "  Reference 1: Cascade Office Park — Salem, OR\n"
                "    Value: $3.2M | Completed: 2023 | On-time delivery\n"
                "    Owner Contact: Mr. T. Brennan, 503-555-0142\n\n"
                "  Reference 2: Harborside Retail Center — Tacoma, WA\n"
                "    Value: $5.8M | Completed: 2022 | 2% under budget\n"
                "    Owner Contact: Ms. L. Chang, 253-555-0298\n\n"
                "  Reference 3: Summit Medical Office Building — Medford, OR\n"
                "    Value: $4.1M | Completed: 2023 | Zero recordable incidents\n"
                "    Owner Contact: Dr. R. Patel, 541-555-0377\n\n"
                "Key Personnel:\n"
                "  Project Manager: Marcus T. Holloway, PE (18 yrs experience)\n"
                "  Site Superintendent: Diane Kowalski (22 yrs experience)\n"
                "  Safety Officer: James R. Finch, CSP (OSHA 30, CHST certified)\n\n"
                "BID_PAGE_4_MARKER: Section 4 — Qualifications and References"
            ),
        ),
        (
            "Section 5 — Terms, Conditions, and Signature",
            (
                "Payment Terms: Progress payments submitted monthly based on\n"
                "percentage of work complete per AIA G702/G703 application.\n"
                "Retainage: 5% retained until substantial completion is achieved.\n\n"
                "Warranty: Ridgemont Construction Group LLC warrants all work\n"
                "against defects in materials and workmanship for a period of\n"
                "one (1) year from the date of substantial completion.\n\n"
                "Dispute Resolution: Any disputes arising from this contract shall\n"
                "be resolved through binding arbitration under the Construction\n"
                "Industry Arbitration Rules of the American Arbitration Association.\n\n"
                "Validity: This bid is valid for sixty (60) calendar days from the\n"
                "date of submission. Ridgemont Construction Group LLC reserves\n"
                "the right to withdraw or revise this bid prior to formal acceptance.\n\n"
                "By submitting this bid, Ridgemont Construction Group LLC confirms\n"
                "that it has reviewed all project documents, visited the site, and\n"
                "is prepared to execute the Work in full compliance with all\n"
                "applicable codes, regulations, and the contract documents.\n\n"
                "Authorized Signature:\n"
                "_________________________________\n"
                "Robert J. Crane, President\n"
                "Ridgemont Construction Group LLC\n"
                "Date: October 14, 2024\n\n"
                "BID_PAGE_5_MARKER: Section 5 — Terms, Conditions, and Signature"
            ),
        ),
    ]

    doc = pymupdf.open()

    section_titles = [
        "Section 1 — Bid Overview and Executive Summary",
        "Section 2 — Project Schedule and Timeline",
        "Section 3 — Cost Breakdown and Bid Pricing",
        "Section 4 — Qualifications and References",
        "Section 5 — Terms, Conditions, and Signature",
    ]

    for i, (section_title, body_text) in enumerate(pages_content):
        make_page(doc, page_num=i + 1, total_pages=5,
                  section_title=section_title, body_text=body_text)

    doc.save(OUTPUT)
    doc.close()
    print(f"Created: {OUTPUT} (5 pages)")

    # Verify
    verify_doc = pymupdf.open(OUTPUT)
    assert verify_doc.page_count == 5, (
        f"Expected 5 pages, got {verify_doc.page_count}"
    )

    # Verify page 2 contains the target text (0-indexed: page index 1)
    page2_text = verify_doc[1].get_text("text")
    assert "estimated completion: 6 months" in page2_text, (
        "Target text 'estimated completion: 6 months' not found on page 2"
    )

    # Spot-check markers
    for page_idx, marker in [
        (0, "BID_PAGE_1_MARKER"),
        (1, "BID_PAGE_2_MARKER"),
        (4, "BID_PAGE_5_MARKER"),
    ]:
        text = verify_doc[page_idx].get_text("text")
        assert marker in text, f"Missing {marker} on page {page_idx + 1}"

    verify_doc.close()
    print("Verified: construction_bid.pdf has 5 pages with correct content")
    print("  - Page 2 contains 'estimated completion: 6 months'")

    # Open in Evince at page 2 for the GUI agent
    launch_gui(f'evince --page-index=1 "{OUTPUT}"', delay_sec=2.0)
    print("GUI_READY: launched Evince at page 2 with DISPLAY=:0")


create_initial()
