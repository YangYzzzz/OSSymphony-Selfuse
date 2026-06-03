"""
Initial Setup: Add image watermark to PDF
Task ID: pdf_fm_071
Domain: pdf

Creates:
  - /home/user/Documents/official_doc.pdf (12-page business document)
  - /home/user/Documents/assets/company_logo.png (200x200 company logo)
  - Opens the PDF in Evince for the agent
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_071'
DOCS_DIR = f'{WORKDIR}/Documents'
ASSETS_DIR = f'{DOCS_DIR}/assets'
PDF_PATH = f'{DOCS_DIR}/official_doc.pdf'
LOGO_PATH = f'{ASSETS_DIR}/company_logo.png'


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


def create_company_logo():
    """Create a 200x200 company logo PNG."""
    from PIL import Image, ImageDraw, ImageFont

    os.makedirs(ASSETS_DIR, exist_ok=True)

    img = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Blue circle background
    draw.ellipse([10, 10, 190, 190], fill=(41, 98, 164, 255), outline=(30, 70, 120, 255), width=3)

    # White "A" letter in the center (for "Apex Corp")
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 90)
    except (IOError, OSError):
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), "A", font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (200 - tw) / 2
    ty = (200 - th) / 2 - 10
    draw.text((tx, ty), "A", fill=(255, 255, 255, 255), font=font)

    # Small "APEX" text below the letter
    try:
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    except (IOError, OSError):
        small_font = ImageFont.load_default()

    bbox2 = draw.textbbox((0, 0), "APEX", font=small_font)
    tw2 = bbox2[2] - bbox2[0]
    tx2 = (200 - tw2) / 2
    draw.text((tx2, 148), "APEX", fill=(255, 255, 255, 255), font=small_font)

    img.save(LOGO_PATH)
    print(f'Company logo created: {LOGO_PATH}')


def create_official_document():
    """Create a 12-page business PDF document."""
    import pymupdf

    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()
    W, H = 612, 792  # Letter size

    # Page content definitions - realistic corporate document
    pages_content = [
        {
            "title": "Apex Corporation",
            "subtitle": "Annual Strategic Plan 2025-2026",
            "body": [
                "Prepared by the Office of Strategic Planning",
                "Document Classification: Internal Use Only",
                "Version 3.2 — Final Draft",
                "Approved: March 15, 2025",
            ],
            "is_cover": True,
        },
        {
            "title": "Table of Contents",
            "body": [
                "1. Executive Summary .......................... 3",
                "2. Market Analysis ............................. 4",
                "3. Revenue Projections ........................ 5",
                "4. Operational Goals .......................... 6",
                "5. Workforce Development ...................... 7",
                "6. Technology Roadmap ......................... 8",
                "7. Risk Assessment ............................ 9",
                "8. Budget Allocation .......................... 10",
                "9. Sustainability Initiatives ................. 11",
                "10. Appendix .................................. 12",
            ],
        },
        {
            "title": "1. Executive Summary",
            "body": [
                "Apex Corporation has experienced 18% year-over-year revenue growth,",
                "reaching $247.3 million in FY2024. Our customer base expanded to",
                "over 14,200 enterprise clients across 32 countries.",
                "",
                "Key achievements in the past fiscal year include the successful",
                "launch of the CloudSync Platform, which now serves 6,800 active",
                "subscribers, and the acquisition of DataPulse Analytics for $42M.",
                "",
                "Looking ahead, we project consolidated revenue of $291M for FY2025,",
                "driven by expansion into the Asia-Pacific region and new product",
                "lines in cybersecurity and AI-powered analytics.",
            ],
        },
        {
            "title": "2. Market Analysis",
            "body": [
                "The global enterprise SaaS market is projected to reach $307B by",
                "2026, growing at a CAGR of 13.7% (source: Gartner, 2024).",
                "",
                "Apex holds approximately 2.1% market share in the mid-enterprise",
                "segment (500-5,000 employees), ranking 7th globally.",
                "",
                "Primary competitors include NovaTech Solutions ($312M revenue),",
                "Meridian Systems ($289M), and CloudFirst Inc. ($264M). Our",
                "differentiation lies in vertical-specific integrations for",
                "healthcare, financial services, and manufacturing.",
                "",
                "Emerging opportunities: AI/ML integration, edge computing,",
                "zero-trust security frameworks, and regulatory compliance tools.",
            ],
        },
        {
            "title": "3. Revenue Projections",
            "body": [
                "FY2025 Revenue Forecast by Segment:",
                "",
                "  Segment                  FY2024 Actual    FY2025 Target",
                "  --------------------------------------------------------",
                "  CloudSync Platform        $98.4M           $124.7M",
                "  Professional Services     $62.1M           $68.3M",
                "  Legacy On-Premise         $45.2M           $38.6M",
                "  DataPulse Analytics       $18.7M           $31.2M",
                "  Cybersecurity Suite       $12.4M           $19.8M",
                "  Training & Certification  $10.5M           $8.9M",
                "  --------------------------------------------------------",
                "  TOTAL                     $247.3M          $291.5M",
                "",
                "Projected gross margin: 68.4% (up from 65.1% in FY2024).",
            ],
        },
        {
            "title": "4. Operational Goals",
            "body": [
                "Q1 2025:",
                "  - Complete Singapore data center buildout ($8.2M capex)",
                "  - Onboard 15 new enterprise clients in APAC region",
                "  - Release CloudSync v4.2 with multi-tenant architecture",
                "",
                "Q2 2025:",
                "  - Launch Apex Cybersecurity Suite 2.0",
                "  - Achieve SOC 2 Type II re-certification",
                "  - Reduce customer onboarding time from 14 to 9 days",
                "",
                "Q3-Q4 2025:",
                "  - Expand Berlin office to 120 employees",
                "  - Pilot AI-driven customer success platform",
                "  - Achieve 99.97% platform uptime SLA",
            ],
        },
        {
            "title": "5. Workforce Development",
            "body": [
                "Current headcount: 1,842 full-time employees across 8 offices.",
                "",
                "Hiring targets for FY2025: 310 new positions",
                "  - Engineering: 145 (cloud, security, ML)",
                "  - Sales & Marketing: 78",
                "  - Customer Success: 52",
                "  - Corporate Functions: 35",
                "",
                "Employee engagement score: 4.2/5.0 (industry avg: 3.8)",
                "Voluntary turnover rate: 11.3% (target: <10%)",
                "",
                "Key initiatives: leadership academy expansion, equity refresh",
                "program, remote-first policy for 40% of roles, mental health",
                "stipend increase to $2,500/year per employee.",
            ],
        },
        {
            "title": "6. Technology Roadmap",
            "body": [
                "Platform Architecture Evolution:",
                "",
                "Phase 1 (H1 2025): Microservices migration for core billing",
                "  and provisioning modules. Estimated reduction in deployment",
                "  cycle from 2 weeks to 3 days.",
                "",
                "Phase 2 (H2 2025): ML pipeline integration for predictive",
                "  analytics. Real-time anomaly detection across client tenants.",
                "",
                "Phase 3 (H1 2026): Federated learning framework for privacy-",
                "  preserving cross-client insights. Patent filing in progress.",
                "",
                "R&D investment: $38.6M (15.7% of projected revenue)",
                "Patent applications filed YTD: 12 (granted: 4)",
            ],
        },
        {
            "title": "7. Risk Assessment",
            "body": [
                "Risk Matrix (Likelihood x Impact):",
                "",
                "  HIGH: Cybersecurity breach (L:Med, I:Critical)",
                "    Mitigation: $4.2M security audit + pen testing budget",
                "",
                "  HIGH: Key talent attrition in engineering (L:High, I:High)",
                "    Mitigation: Retention bonuses, equity refresh, career paths",
                "",
                "  MEDIUM: Regulatory changes in EU data sovereignty (L:Med, I:Med)",
                "    Mitigation: EU-only data residency option in CloudSync v4.3",
                "",
                "  MEDIUM: Currency fluctuation impact on APAC expansion (L:High, I:Low)",
                "    Mitigation: Forward contracts for SGD, JPY, AUD",
                "",
                "  LOW: Supply chain disruption for hardware procurement",
                "    Mitigation: Multi-vendor strategy, 6-month inventory buffer",
            ],
        },
        {
            "title": "8. Budget Allocation",
            "body": [
                "FY2025 Operating Budget: $198.4M",
                "",
                "  Category                  Amount      % of Total",
                "  ------------------------------------------------",
                "  Personnel & Benefits       $112.6M     56.8%",
                "  Cloud Infrastructure       $28.3M      14.3%",
                "  R&D Programs               $22.1M      11.1%",
                "  Sales & Marketing          $18.7M       9.4%",
                "  Facilities & Operations    $9.4M        4.7%",
                "  Legal & Compliance         $4.1M        2.1%",
                "  Training & Development     $3.2M        1.6%",
                "  ------------------------------------------------",
                "  TOTAL                      $198.4M     100.0%",
                "",
                "Capital expenditures (separate): $14.8M",
            ],
        },
        {
            "title": "9. Sustainability Initiatives",
            "body": [
                "Apex Corporation ESG Commitments for 2025-2026:",
                "",
                "Environmental:",
                "  - Carbon neutral operations by Q4 2025 (currently 78% offset)",
                "  - 100% renewable energy for all data centers by mid-2026",
                "  - Electronic waste recycling program: target 95% diversion rate",
                "",
                "Social:",
                "  - STEM scholarship program: $500K annual commitment",
                "  - Supplier diversity: 25% procurement from minority-owned businesses",
                "  - Community volunteer program: 16 hours/employee/year",
                "",
                "Governance:",
                "  - Board diversity target: 40% women, 30% underrepresented minorities",
                "  - Annual third-party ethics audit",
                "  - Whistleblower protection enhancement",
            ],
        },
        {
            "title": "Appendix",
            "body": [
                "A. Financial Statements (detailed) — see attached supplement",
                "B. Organization Chart — updated January 2025",
                "C. Patent Portfolio Summary",
                "D. Customer Satisfaction Survey Results (NPS: 62)",
                "E. Competitive Benchmarking Data",
                "F. IT Infrastructure Topology Diagram",
                "",
                "For questions regarding this document, contact:",
                "  Rebecca Torres, VP of Strategic Planning",
                "  rebecca.torres@apexcorp.com",
                "  +1 (415) 555-0187",
                "",
                "  David Nakamura, CFO",
                "  david.nakamura@apexcorp.com",
                "  +1 (415) 555-0234",
                "",
                "Document ID: APEX-SP-2025-003",
                "Last Modified: March 12, 2025",
            ],
        },
    ]

    for i, pg in enumerate(pages_content):
        page = doc.new_page(width=W, height=H)

        if pg.get("is_cover"):
            # Cover page - centered title and subtitle
            page.insert_text(
                pymupdf.Point(W / 2 - 120, 250),
                pg["title"],
                fontsize=28,
                fontname="hebo",
                color=(0.16, 0.24, 0.41),
            )
            page.insert_text(
                pymupdf.Point(W / 2 - 150, 300),
                pg["subtitle"],
                fontsize=16,
                fontname="helv",
                color=(0.3, 0.3, 0.3),
            )
            y = 380
            for line in pg["body"]:
                page.insert_text(
                    pymupdf.Point(W / 2 - 140, y),
                    line,
                    fontsize=11,
                    fontname="helv",
                    color=(0.4, 0.4, 0.4),
                )
                y += 20
        else:
            # Regular page - title at top, body text below
            # Header line
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(54, 65), pymupdf.Point(W - 54, 65))
            shape.finish(color=(0.16, 0.24, 0.41), width=1.5)
            shape.commit()

            page.insert_text(
                pymupdf.Point(54, 55),
                pg["title"],
                fontsize=18,
                fontname="hebo",
                color=(0.16, 0.24, 0.41),
            )

            y = 100
            for line in pg["body"]:
                if line == "":
                    y += 12
                    continue
                page.insert_text(
                    pymupdf.Point(54, y),
                    line,
                    fontsize=10.5,
                    fontname="helv",
                    color=(0.1, 0.1, 0.1),
                )
                y += 16

            # Footer - page number
            page.insert_text(
                pymupdf.Point(W / 2 - 10, H - 36),
                str(i + 1),
                fontsize=9,
                fontname="helv",
                color=(0.5, 0.5, 0.5),
            )

            # Footer line
            shape2 = page.new_shape()
            shape2.draw_line(pymupdf.Point(54, H - 50), pymupdf.Point(W - 54, H - 50))
            shape2.finish(color=(0.7, 0.7, 0.7), width=0.5)
            shape2.commit()

    doc.save(PDF_PATH)
    doc.close()
    print(f'Official document created: {PDF_PATH} ({len(pages_content)} pages)')


def main():
    create_company_logo()
    create_official_document()

    # Open the PDF in Evince for the agent
    launch_gui(f'evince "{PDF_PATH}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


main()
