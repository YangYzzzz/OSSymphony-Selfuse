"""
Initial Setup: Create a 12-page proposal PDF with no stamps
Task ID: pdf_aw_040
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_aw_040'
DOCS_DIR = f'{WORKDIR}/docs'
TEMPLATES_DIR = f'{WORKDIR}/templates'
OUTPUT = f'{DOCS_DIR}/proposal.pdf'


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
    # Create directories
    os.makedirs(DOCS_DIR, exist_ok=True)
    os.makedirs(TEMPLATES_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page dimensions (Letter size)
    W, H = 612, 792

    # Proposal content for 12 pages
    pages_content = [
        {
            "title": "Strategic Growth Proposal 2026",
            "subtitle": "Meridian Technologies Inc.",
            "body": [
                "Prepared by: Strategic Planning Division",
                "Date: March 15, 2026",
                "Document Reference: MTP-2026-0412",
                "",
                "Classification: Internal - Confidential",
                "",
                "This proposal outlines the strategic growth initiatives",
                "planned for Meridian Technologies over the next fiscal",
                "year, with projected investments across key business",
                "units and emerging market opportunities.",
            ]
        },
        {
            "title": "1. Executive Summary",
            "subtitle": "",
            "body": [
                "Meridian Technologies has experienced sustained growth over the",
                "past three fiscal years, with revenue increasing from $142M in",
                "FY2023 to $198M in FY2025. This proposal requests a capital",
                "allocation of $47.5M to fund four strategic initiatives that are",
                "projected to generate an additional $85M in annual revenue by",
                "FY2028.",
                "",
                "Key highlights:",
                "  - Cloud Infrastructure Expansion: $18.2M investment",
                "  - AI/ML Product Suite Launch: $14.8M investment",
                "  - European Market Entry: $9.5M investment",
                "  - Talent Acquisition & Development: $5.0M investment",
                "",
                "The projected ROI across all four initiatives ranges from 2.3x",
                "to 4.1x over a 36-month horizon, with breakeven expected within",
                "18 months for the cloud and AI initiatives.",
            ]
        },
        {
            "title": "2. Market Analysis",
            "subtitle": "2.1 Industry Landscape",
            "body": [
                "The global enterprise software market reached $297B in 2025,",
                "growing at a CAGR of 11.4%. Cloud-native solutions now account",
                "for 64% of new enterprise deployments, up from 41% in 2022.",
                "",
                "Key market drivers:",
                "  - Digital transformation acceleration post-pandemic",
                "  - Rising demand for AI-integrated business solutions",
                "  - Shift toward consumption-based pricing models",
                "  - Increased regulatory compliance requirements",
                "",
                "Competitive landscape analysis reveals three primary segments:",
                "  1. Hyperscale platforms (AWS, Azure, GCP)",
                "  2. Specialized vertical SaaS providers",
                "  3. Hybrid infrastructure enablers (our target segment)",
                "",
                "Meridian's current market share in the hybrid segment is 8.3%,",
                "ranking fourth behind Nexus Corp (14.1%), Vertex Systems",
                "(12.7%), and Pinnacle Software (9.8%).",
            ]
        },
        {
            "title": "2. Market Analysis (continued)",
            "subtitle": "2.2 Target Customer Segments",
            "body": [
                "Primary Target: Mid-market enterprises ($50M-$500M revenue)",
                "  - 12,400 addressable accounts in North America",
                "  - Average contract value: $185,000/year",
                "  - Current penetration: 3.2% (396 active accounts)",
                "",
                "Secondary Target: Large enterprises ($500M+ revenue)",
                "  - 2,800 addressable accounts globally",
                "  - Average contract value: $740,000/year",
                "  - Current penetration: 1.1% (31 active accounts)",
                "",
                "Growth Opportunity: European mid-market",
                "  - 8,600 addressable accounts",
                "  - Estimated average contract value: EUR 165,000/year",
                "  - Current penetration: 0% (no European presence)",
                "",
                "Customer acquisition cost has decreased 22% YoY due to",
                "improved brand recognition and partner channel expansion.",
            ]
        },
        {
            "title": "3. Cloud Infrastructure Expansion",
            "subtitle": "Initiative 1: $18.2M Investment",
            "body": [
                "Objective: Scale cloud platform capacity by 340% to support",
                "anticipated demand growth and new product launches.",
                "",
                "Investment Breakdown:",
                "  - Data center co-location (3 new regions): $8.4M",
                "  - Network infrastructure upgrades: $3.7M",
                "  - Security & compliance tooling: $2.8M",
                "  - DevOps automation platform: $2.1M",
                "  - Contingency reserve: $1.2M",
                "",
                "Timeline:",
                "  Q1 2026: Architecture design and vendor selection",
                "  Q2 2026: US-West region deployment",
                "  Q3 2026: EU-Central region deployment",
                "  Q4 2026: APAC-Southeast region deployment",
                "",
                "Expected Outcomes:",
                "  - 99.99% uptime SLA capability (up from 99.95%)",
                "  - 40% reduction in latency for European customers",
                "  - Support for 10,000+ concurrent enterprise tenants",
                "  - SOC 2 Type II and ISO 27001 certification",
            ]
        },
        {
            "title": "4. AI/ML Product Suite",
            "subtitle": "Initiative 2: $14.8M Investment",
            "body": [
                "Objective: Launch an integrated AI/ML product suite that",
                "enhances existing platform capabilities and opens new",
                "revenue streams.",
                "",
                "Product Components:",
                "  - Meridian Predict: Predictive analytics engine",
                "  - Meridian Automate: Intelligent workflow automation",
                "  - Meridian Insights: Natural language business intelligence",
                "",
                "Investment Breakdown:",
                "  - R&D team expansion (24 engineers, 6 researchers): $9.2M",
                "  - GPU compute infrastructure: $2.8M",
                "  - Training data acquisition & labeling: $1.5M",
                "  - Product design & UX research: $0.8M",
                "  - Beta program & early adopter support: $0.5M",
                "",
                "Revenue Projections:",
                "  Year 1: $12M (150 customers at avg $80K)",
                "  Year 2: $34M (380 customers at avg $89K)",
                "  Year 3: $58M (580 customers at avg $100K)",
            ]
        },
        {
            "title": "5. European Market Entry",
            "subtitle": "Initiative 3: $9.5M Investment",
            "body": [
                "Objective: Establish Meridian's presence in the European",
                "enterprise software market through a regional office,",
                "localized products, and strategic partnerships.",
                "",
                "Phase 1 - Foundation (Q1-Q2 2026):",
                "  - Open London headquarters: $1.8M",
                "  - Hire regional leadership team (8 positions): $1.2M",
                "  - GDPR compliance & data residency: $0.9M",
                "  - Localization (DE, FR, ES, IT, NL): $0.6M",
                "",
                "Phase 2 - Growth (Q3-Q4 2026):",
                "  - Channel partner recruitment (target: 15 partners): $1.4M",
                "  - Marketing & demand generation: $2.0M",
                "  - Customer success team (6 positions): $0.9M",
                "  - Industry events & thought leadership: $0.7M",
                "",
                "Year 1 Revenue Target: EUR 4.2M",
                "Year 2 Revenue Target: EUR 14.8M",
                "Year 3 Revenue Target: EUR 28.5M",
            ]
        },
        {
            "title": "6. Talent Strategy",
            "subtitle": "Initiative 4: $5.0M Investment",
            "body": [
                "Objective: Attract, develop, and retain top technical talent",
                "to support growth initiatives and maintain competitive edge.",
                "",
                "Current Workforce: 847 employees",
                "Planned Net Additions: 142 roles by end of FY2026",
                "",
                "Key Programs:",
                "  - Engineering Excellence Academy: $1.2M",
                "    Training program for 200+ engineers on cloud-native",
                "    architecture, AI/ML, and modern DevOps practices",
                "",
                "  - Recruitment Marketing & Employer Brand: $1.5M",
                "    Campus partnerships with 12 universities",
                "    Tech conference sponsorships (8 events)",
                "    Engineering blog and open-source contributions",
                "",
                "  - Compensation & Benefits Enhancement: $1.8M",
                "    Market adjustment for 15% of workforce",
                "    Enhanced equity refresh program",
                "    Expanded remote work infrastructure",
                "",
                "  - Diversity & Inclusion Programs: $0.5M",
                "    Targeted outreach and mentorship initiatives",
            ]
        },
        {
            "title": "7. Financial Projections",
            "subtitle": "Consolidated Three-Year Model",
            "body": [
                "Revenue Projections (in millions USD):",
                "",
                "                       FY2026    FY2027    FY2028",
                "  Core Platform         $210.5    $236.8    $261.4",
                "  AI/ML Suite            $12.0     $34.0     $58.0",
                "  European Operations     $4.6     $16.2     $31.2",
                "  Professional Services   $18.2    $21.5     $24.8",
                "  ----------------------------------------",
                "  Total Revenue         $245.3    $308.5    $375.4",
                "",
                "Operating Expenses:",
                "  Cost of Revenue        $73.6     $89.5    $105.2",
                "  R&D                    $61.3     $71.0     $78.8",
                "  Sales & Marketing      $49.1     $55.5     $60.1",
                "  G&A                    $24.5     $27.8     $30.0",
                "  ----------------------------------------",
                "  Total OpEx           $208.5    $243.8    $274.1",
                "",
                "  Operating Income       $36.8     $64.7    $101.3",
                "  Operating Margin       15.0%     21.0%     27.0%",
            ]
        },
        {
            "title": "8. Risk Assessment",
            "subtitle": "Key Risks and Mitigation Strategies",
            "body": [
                "Risk 1: Cloud Infrastructure Delays",
                "  Probability: Medium | Impact: High",
                "  Mitigation: Multi-vendor strategy, phased rollout,",
                "  pre-negotiated SLAs with penalty clauses",
                "",
                "Risk 2: AI/ML Product Market Fit",
                "  Probability: Medium | Impact: High",
                "  Mitigation: Extensive beta program with 25 anchor",
                "  customers, iterative development sprints, pivot criteria",
                "",
                "Risk 3: European Regulatory Complexity",
                "  Probability: High | Impact: Medium",
                "  Mitigation: Dedicated legal counsel, GDPR-by-design",
                "  architecture, local compliance officers",
                "",
                "Risk 4: Talent Competition",
                "  Probability: High | Impact: Medium",
                "  Mitigation: Above-market compensation, strong culture,",
                "  flexible work arrangements, compelling mission",
                "",
                "Risk 5: Currency Fluctuation (EUR/USD)",
                "  Probability: Medium | Impact: Low",
                "  Mitigation: Natural hedging through local cost base,",
                "  forward contracts for large transactions",
            ]
        },
        {
            "title": "9. Implementation Roadmap",
            "subtitle": "Key Milestones FY2026",
            "body": [
                "Q1 2026 (January - March):",
                "  [x] Board approval of strategic plan",
                "  [ ] Cloud architecture finalized",
                "  [ ] AI/ML team leads hired (6 of 6)",
                "  [ ] London office lease signed",
                "  [ ] Recruitment campaign launch",
                "",
                "Q2 2026 (April - June):",
                "  [ ] US-West data center operational",
                "  [ ] Meridian Predict alpha release",
                "  [ ] European partner program launched",
                "  [ ] Engineering Academy cohort 1 complete",
                "",
                "Q3 2026 (July - September):",
                "  [ ] EU-Central data center operational",
                "  [ ] AI/ML suite beta with 25 customers",
                "  [ ] First 10 European customers onboarded",
                "  [ ] Mid-year financial review",
                "",
                "Q4 2026 (October - December):",
                "  [ ] APAC data center operational",
                "  [ ] AI/ML suite general availability",
                "  [ ] European revenue target: EUR 4.2M",
                "  [ ] Annual performance reviews complete",
            ]
        },
        {
            "title": "10. Conclusion & Request for Approval",
            "subtitle": "",
            "body": [
                "This strategic growth proposal represents a carefully designed",
                "investment plan that balances ambitious growth targets with",
                "prudent risk management. The four initiatives are complementary",
                "and mutually reinforcing:",
                "",
                "  - Cloud expansion enables AI/ML product scale",
                "  - AI/ML products differentiate European market entry",
                "  - European presence diversifies revenue geography",
                "  - Talent strategy underpins execution across all initiatives",
                "",
                "Total Investment Requested: $47.5M",
                "Projected 3-Year Revenue Impact: +$177M annually by FY2028",
                "Projected 3-Year ROI: 3.7x",
                "",
                "We respectfully request the Board's approval to proceed with",
                "Phase 1 funding of $22.6M in Q1 2026, with subsequent phases",
                "subject to milestone achievement review.",
                "",
                "Submitted by:",
                "  Dr. Amara Okafor, Chief Strategy Officer",
                "  Elena Vasquez, VP of Corporate Development",
                "  James Chen, Chief Financial Officer",
                "",
                "Meridian Technologies Inc.",
                "March 15, 2026",
            ]
        },
    ]

    for i, content in enumerate(pages_content):
        page = doc.new_page(width=W, height=H)

        if i == 0:
            # Cover page - centered title
            page.insert_text(
                pymupdf.Point(W / 2 - 180, 250),
                content["title"],
                fontsize=24,
                fontname="hebo",
                color=(0.1, 0.1, 0.3),
            )
            page.insert_text(
                pymupdf.Point(W / 2 - 130, 290),
                content["subtitle"],
                fontsize=16,
                fontname="helv",
                color=(0.3, 0.3, 0.5),
            )
            y = 360
            for line in content["body"]:
                page.insert_text(
                    pymupdf.Point(W / 2 - 170, y),
                    line,
                    fontsize=11,
                    fontname="helv",
                    color=(0.2, 0.2, 0.2),
                )
                y += 18

            # Decorative line on cover
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(100, 320), pymupdf.Point(512, 320))
            shape.finish(color=(0.1, 0.1, 0.3), width=2)
            shape.commit()
        else:
            # Regular pages
            # Header line
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(60, 55), pymupdf.Point(552, 55))
            shape.finish(color=(0.6, 0.6, 0.6), width=0.5)
            shape.commit()

            # Page header
            page.insert_text(
                pymupdf.Point(60, 48),
                "Meridian Technologies - Strategic Growth Proposal 2026",
                fontsize=8,
                fontname="heit",
                color=(0.5, 0.5, 0.5),
            )

            # Title
            page.insert_text(
                pymupdf.Point(60, 90),
                content["title"],
                fontsize=18,
                fontname="hebo",
                color=(0.1, 0.1, 0.3),
            )

            y_start = 120
            if content["subtitle"]:
                page.insert_text(
                    pymupdf.Point(60, y_start),
                    content["subtitle"],
                    fontsize=13,
                    fontname="hebo",
                    color=(0.2, 0.2, 0.4),
                )
                y_start += 30

            # Body text
            y = y_start
            for line in content["body"]:
                if line == "":
                    y += 10
                    continue
                page.insert_text(
                    pymupdf.Point(60, y),
                    line,
                    fontsize=10,
                    fontname="helv",
                    color=(0.15, 0.15, 0.15),
                )
                y += 15

            # Footer
            page.insert_text(
                pymupdf.Point(60, H - 40),
                f"Page {i + 1} of 12",
                fontsize=8,
                fontname="helv",
                color=(0.5, 0.5, 0.5),
            )
            page.insert_text(
                pymupdf.Point(400, H - 40),
                "Confidential",
                fontsize=8,
                fontname="heit",
                color=(0.5, 0.5, 0.5),
            )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Templates directory created: {TEMPLATES_DIR}')
    print(f'Page count: 12')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
