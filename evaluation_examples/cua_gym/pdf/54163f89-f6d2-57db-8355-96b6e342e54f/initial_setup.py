"""
Initial Setup: Stamp approved_stamp.pdf onto page 1 of final_proposal.pdf using pdftk
Task ID: pdf_fm_087
Domain: pdf
"""

import os
import shlex
import subprocess
import time

subprocess.run(['pip3', 'install', 'PyMuPDF'], capture_output=True)
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_087'
DOCUMENTS = f'{WORKDIR}/Documents'
TEMPLATES = f'{DOCUMENTS}/templates'
PROPOSAL_PATH = f'{DOCUMENTS}/final_proposal.pdf'
STAMP_PATH = f'{TEMPLATES}/approved_stamp.pdf'


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


def create_proposal():
    """Create a 10-page business proposal PDF."""
    doc = pymupdf.open()

    # Page dimensions (Letter)
    W, H = 612, 792

    sections = [
        ("Meridian Dynamics - Strategic Growth Proposal", [
            "Prepared for: Board of Directors",
            "Date: March 28, 2026",
            "Prepared by: Strategic Planning Division",
            "",
            "Classification: Internal - Confidential",
            "",
            "This document outlines a comprehensive strategy for expanding Meridian Dynamics",
            "into emerging markets over the next five fiscal years. The proposal addresses",
            "market analysis, resource allocation, risk assessment, and projected returns.",
        ]),
        ("1. Executive Summary", [
            "Meridian Dynamics has experienced steady growth of 12% year-over-year since 2022.",
            "However, market saturation in our primary regions (North America, Western Europe)",
            "necessitates a pivot toward high-growth emerging markets.",
            "",
            "Key recommendations:",
            "  - Enter Southeast Asian market through strategic partnership with Taiyo Industries",
            "  - Establish regional headquarters in Singapore by Q3 2026",
            "  - Allocate $14.5M in capital expenditure for infrastructure buildout",
            "  - Target 8% market share in APAC renewable energy sector within 36 months",
            "",
            "Expected ROI: 23% over 5 years with breakeven projected at month 28.",
        ]),
        ("2. Market Analysis", [
            "2.1 Current Market Position",
            "Revenue FY2025: $287M | EBITDA Margin: 18.3% | Employee Count: 2,140",
            "",
            "2.2 Target Market Overview",
            "The Southeast Asian renewable energy market is projected to grow at 15.7% CAGR",
            "through 2030 (source: BloombergNEF). Key drivers include:",
            "  - Government mandates for 40% renewable energy by 2030",
            "  - Declining solar panel costs (now $0.20/W, down 34% since 2023)",
            "  - Rising electricity demand from manufacturing sector expansion",
            "",
            "2.3 Competitive Landscape",
            "Major competitors: SolarEdge (12% share), Envision Energy (9%), local players (31%)",
            "Gap analysis reveals underserved mid-market commercial segment.",
        ]),
        ("3. Strategic Approach", [
            "3.1 Phase 1: Market Entry (Q2-Q4 2026)",
            "  - Formalize partnership agreement with Taiyo Industries (MOU signed Jan 2026)",
            "  - Deploy advance team of 15 personnel to Singapore office",
            "  - Begin regulatory compliance process in Singapore, Thailand, Vietnam",
            "",
            "3.2 Phase 2: Scaling Operations (2027)",
            "  - Expand team to 85 FTEs across 3 regional offices",
            "  - Launch localized product lines for commercial rooftop installations",
            "  - Secure initial contracts targeting $18M in first-year revenue",
            "",
            "3.3 Phase 3: Market Consolidation (2028-2030)",
            "  - Achieve 8% regional market share",
            "  - Evaluate acquisition targets for vertical integration",
            "  - Establish R&D center in partnership with NUS Engineering faculty",
        ]),
        ("4. Financial Projections", [
            "Capital Requirements:",
            "  Year 1: $14.5M (infrastructure, staffing, regulatory)",
            "  Year 2: $8.2M  (scaling, marketing, inventory)",
            "  Year 3: $4.1M  (maintenance, R&D)",
            "",
            "Revenue Projections:",
            "  Year 1: $18M  | Year 2: $42M  | Year 3: $67M",
            "  Year 4: $89M  | Year 5: $112M",
            "",
            "Net Present Value (10% discount rate): $47.3M",
            "Internal Rate of Return: 23.1%",
            "Payback Period: 28 months",
        ]),
        ("5. Risk Assessment", [
            "5.1 High-Impact Risks",
            "  - Regulatory changes in target markets (Mitigation: diversified country portfolio)",
            "  - Currency fluctuation exposure (Mitigation: hedging strategy via JPMorgan FX desk)",
            "  - Supply chain disruption (Mitigation: dual-source procurement policy)",
            "",
            "5.2 Medium-Impact Risks",
            "  - Talent acquisition challenges (Mitigation: partnership with 3 regional universities)",
            "  - Technology obsolescence (Mitigation: modular platform architecture)",
            "  - Competitive price war (Mitigation: differentiation through service quality)",
            "",
            "5.3 Risk Matrix Score: 3.2/5.0 (Moderate - Acceptable)",
        ]),
        ("6. Implementation Timeline", [
            "Q2 2026: Partnership formalization, Singapore office lease signed",
            "Q3 2026: Advance team deployed, regulatory filings initiated",
            "Q4 2026: First pilot installations (3 commercial sites)",
            "Q1 2027: Thailand and Vietnam offices opened",
            "Q2 2027: Production scaling, first major contract ($4.2M with PT Sinar Mas)",
            "Q3 2027: 50 FTE milestone, marketing campaign launch",
            "Q4 2027: Year 1 revenue target assessment and course correction",
            "2028: Full-scale operations across 3 countries",
            "2029: R&D center establishment, acquisition pipeline review",
            "2030: Target 8% market share evaluation and Phase 4 planning",
        ]),
        ("7. Team and Governance", [
            "Executive Sponsor: Dr. Elena Vasquez, CEO",
            "Program Director: James Whitfield, SVP Strategic Initiatives",
            "Regional Lead: Ananya Sharma, VP Asia-Pacific Operations",
            "Finance Lead: Robert Chen, Director of FP&A",
            "",
            "Governance Structure:",
            "  - Steering Committee: Monthly review with C-suite",
            "  - Program Board: Bi-weekly operational updates",
            "  - Risk Committee: Quarterly risk assessment reviews",
            "",
            "Reporting: Monthly dashboard to Board, quarterly detailed report",
        ]),
        ("8. Resource Requirements", [
            "8.1 Human Resources",
            "  Year 1: 15 expats + 20 local hires = 35 FTE",
            "  Year 2: 35 carry-forward + 50 new hires = 85 FTE",
            "  Year 3: 85 carry-forward + 40 new hires = 125 FTE",
            "",
            "8.2 Technology Infrastructure",
            "  - Cloud: AWS Asia-Pacific (Singapore) region - $320K/year",
            "  - ERP: SAP S/4HANA extension - $180K implementation",
            "  - CRM: Salesforce APAC instance - $95K/year",
            "",
            "8.3 Facilities",
            "  - Singapore HQ: 8,500 sq ft, Grade A office at Marina Bay - $42K/month",
            "  - Bangkok satellite: 3,200 sq ft - $12K/month",
            "  - Ho Chi Minh City satellite: 2,800 sq ft - $8K/month",
        ]),
        ("9. Conclusion and Recommendation", [
            "The Southeast Asian renewable energy market represents a compelling growth",
            "opportunity for Meridian Dynamics. With a disciplined phased approach, strong",
            "local partnerships, and adequate capital allocation, we project achieving our",
            "target market position within 36 months.",
            "",
            "We recommend the Board approve:",
            "  1. Initial capital allocation of $14.5M for Year 1 operations",
            "  2. Partnership agreement with Taiyo Industries",
            "  3. Establishment of Singapore regional headquarters",
            "  4. Formation of the APAC Expansion Steering Committee",
            "",
            "Respectfully submitted,",
            "James Whitfield",
            "SVP Strategic Initiatives",
            "Meridian Dynamics Inc.",
        ]),
    ]

    for i, (title, lines) in enumerate(sections):
        page = doc.new_page(width=W, height=H)

        # Header line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(54, 54), pymupdf.Point(W - 54, 54))
        shape.finish(color=(0.1, 0.3, 0.6), width=2)
        shape.commit()

        # Title
        if i == 0:
            # Cover page - centered title
            page.insert_text(
                pymupdf.Point(54, 200),
                title,
                fontsize=22,
                fontname="hebo",
                color=(0.1, 0.2, 0.5),
            )
            y = 260
        else:
            page.insert_text(
                pymupdf.Point(54, 82),
                title,
                fontsize=16,
                fontname="hebo",
                color=(0.1, 0.2, 0.5),
            )
            y = 115

        # Content lines
        for line in lines:
            if y > H - 72:
                break
            page.insert_text(
                pymupdf.Point(54, y),
                line,
                fontsize=10.5,
                fontname="helv",
                color=(0.1, 0.1, 0.1),
            )
            y += 16

        # Footer
        page.insert_text(
            pymupdf.Point(54, H - 40),
            f"Meridian Dynamics - Confidential",
            fontsize=8,
            fontname="heit",
            color=(0.5, 0.5, 0.5),
        )
        page.insert_text(
            pymupdf.Point(W - 90, H - 40),
            f"Page {i + 1} of 10",
            fontsize=8,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

        # Footer line
        shape2 = page.new_shape()
        shape2.draw_line(pymupdf.Point(54, H - 50), pymupdf.Point(W - 54, H - 50))
        shape2.finish(color=(0.1, 0.3, 0.6), width=0.5)
        shape2.commit()

    doc.save(PROPOSAL_PATH)
    doc.close()
    print(f"Created proposal: {PROPOSAL_PATH}")


def create_stamp():
    """Create a 1-page PDF with a green 'APPROVED' stamp graphic."""
    doc = pymupdf.open()
    # Same page size as proposal (Letter)
    page = doc.new_page(width=612, height=792)

    # Draw a green stamp graphic in the upper-right area
    # Outer rounded rectangle border
    cx, cy = 450, 140  # center of stamp
    stamp_w, stamp_h = 200, 80

    shape = page.new_shape()

    # Outer border rectangle
    r = pymupdf.Rect(cx - stamp_w/2, cy - stamp_h/2, cx + stamp_w/2, cy + stamp_h/2)
    shape.draw_rect(r)
    shape.finish(color=(0.0, 0.5, 0.0), width=4)

    # Inner border rectangle (double border effect)
    r2 = pymupdf.Rect(cx - stamp_w/2 + 6, cy - stamp_h/2 + 6, cx + stamp_w/2 - 6, cy + stamp_h/2 - 6)
    shape.draw_rect(r2)
    shape.finish(color=(0.0, 0.5, 0.0), width=2)

    shape.commit()

    # "APPROVED" text centered in the stamp area
    page.insert_text(
        pymupdf.Point(cx - 68, cy + 8),
        "APPROVED",
        fontsize=28,
        fontname="hebo",
        color=(0.0, 0.5, 0.0),
    )

    # Small date line below
    page.insert_text(
        pymupdf.Point(cx - 42, cy + 26),
        "2026-03-28",
        fontsize=10,
        fontname="helv",
        color=(0.0, 0.5, 0.0),
    )

    doc.save(STAMP_PATH)
    doc.close()
    print(f"Created stamp: {STAMP_PATH}")


def main():
    # Create directories
    os.makedirs(TEMPLATES, exist_ok=True)

    # Create proposal and stamp
    create_proposal()
    create_stamp()

    # Install pdftk if not already available
    r = subprocess.run(["which", "pdftk"], capture_output=True)
    if r.returncode != 0:
        subprocess.run(["bash", "-c", "echo 'password' | sudo -S apt-get update -qq"], capture_output=True)
        subprocess.run(["bash", "-c", "echo 'password' | sudo -S apt-get install -y pdftk-java"], capture_output=True)
    print(f"pdftk available: {subprocess.run(['which', 'pdftk'], capture_output=True).returncode == 0}")

    # Verify files exist
    for f in [PROPOSAL_PATH, STAMP_PATH]:
        assert os.path.exists(f), f"Missing: {f}"
        print(f"Verified: {f} ({os.path.getsize(f)} bytes)")

    # Open the proposal in evince for the GUI agent
    launch_gui(f'evince "{PROPOSAL_PATH}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


main()
