"""
Initial Setup: Create a 10-page strategy document PDF with no headers.
Task ID: pdf_fm_084
Domain: pdf
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_084'
DOC_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOC_DIR}/strategy_doc.pdf'

# Page dimensions (A4)
A4_W, A4_H = 595, 842


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
    os.makedirs(DOC_DIR, exist_ok=True)

    doc = pymupdf.open()

    # --- Content for a realistic 10-page business strategy document ---
    pages_content = [
        # Page 1: Title page
        {
            "title": "Vertex Technologies\nStrategic Plan 2025-2028",
            "body": (
                "Prepared by the Office of Strategic Planning\n"
                "March 2025\n\n"
                "This document outlines the three-year strategic roadmap for Vertex Technologies, "
                "covering market expansion, product innovation, operational excellence, and talent "
                "development initiatives. The plan has been reviewed and endorsed by the Executive "
                "Leadership Team and the Board of Directors."
            ),
        },
        # Page 2: Executive Summary
        {
            "title": "1. Executive Summary",
            "body": (
                "Vertex Technologies has experienced sustained growth over the past five years, "
                "achieving a compound annual growth rate of 18.3% in revenue and expanding our "
                "customer base to over 12,000 enterprise clients across 34 countries. Our cloud "
                "infrastructure platform now processes over 2.4 billion API requests daily.\n\n"
                "However, the competitive landscape is evolving rapidly. New entrants from Asia-Pacific "
                "markets and consolidation among mid-tier players require us to accelerate our "
                "innovation cycle and deepen customer engagement. This strategic plan addresses "
                "these challenges through four key pillars:\n\n"
                "  - Market Expansion into Southeast Asia and Latin America\n"
                "  - Product Innovation with AI-native capabilities\n"
                "  - Operational Excellence through automation\n"
                "  - Talent Development and retention programs\n\n"
                "We project that successful execution will yield $840M in annual recurring revenue "
                "by FY2028, up from $520M in FY2024."
            ),
        },
        # Page 3: Market Analysis
        {
            "title": "2. Market Analysis",
            "body": (
                "The global cloud infrastructure market is projected to reach $312 billion by 2027, "
                "growing at a CAGR of 22.1%. Key trends shaping our market include:\n\n"
                "Multi-Cloud Adoption: 78% of enterprises now use two or more cloud providers, "
                "creating demand for unified management platforms. Our CloudBridge product is "
                "well-positioned to capture this segment.\n\n"
                "Edge Computing Growth: The edge computing market will reach $61.1 billion by 2028. "
                "Our partnership with NexGen Hardware gives us early-mover advantage in edge "
                "deployment services.\n\n"
                "AI Infrastructure Demand: Enterprise AI workloads are growing 45% year-over-year. "
                "GPU-optimized compute instances represent our fastest-growing product line, with "
                "Q4 2024 revenue of $38.2M, up 67% from the prior year.\n\n"
                "Regulatory Compliance: GDPR, CCPA, and emerging regulations in India and Brazil "
                "are driving demand for region-specific data residency solutions. Our sovereign "
                "cloud offering addresses this need directly."
            ),
        },
        # Page 4: Competitive Landscape
        {
            "title": "3. Competitive Landscape",
            "body": (
                "Our primary competitors fall into three tiers:\n\n"
                "Tier 1 - Hyperscalers: Amazon Web Services, Microsoft Azure, and Google Cloud "
                "Platform dominate with 62% combined market share. We compete by offering superior "
                "developer experience and specialized vertical solutions.\n\n"
                "Tier 2 - Mid-Market Providers: DigitalOcean, Linode (now Akamai), and Vultr "
                "compete on price and simplicity. Recent acquisitions in this tier suggest further "
                "consolidation. Our differentiation lies in enterprise-grade SLAs and compliance "
                "certifications.\n\n"
                "Tier 3 - Regional Players: CloudAsia, SaoPaulo Cloud, and AfriHost are gaining "
                "traction in their respective regions. Our strategy includes selective partnerships "
                "and co-location agreements rather than direct competition.\n\n"
                "SWOT Summary:\n"
                "  Strengths: Developer tools, API reliability (99.997% uptime), vertical expertise\n"
                "  Weaknesses: Limited brand awareness in APAC, higher price point vs Tier 2\n"
                "  Opportunities: AI infrastructure, sovereign cloud, edge computing\n"
                "  Threats: Hyperscaler bundling, price wars, talent competition"
            ),
        },
        # Page 5: Strategic Pillar 1
        {
            "title": "4. Strategic Pillar: Market Expansion",
            "body": (
                "Objective: Increase international revenue from 28% to 45% of total revenue by 2028.\n\n"
                "4.1 Southeast Asia Expansion\n"
                "  - Open regional data centers in Singapore (Q2 2025) and Jakarta (Q4 2025)\n"
                "  - Hire 35 sales and support staff in the region by mid-2026\n"
                "  - Target 200 enterprise customers in the first 18 months\n"
                "  - Investment: $24.5M over three years\n"
                "  - Expected ROI: 3.2x by end of year three\n\n"
                "4.2 Latin America Entry\n"
                "  - Partner with BrazilTech Solutions for local compliance and support\n"
                "  - Launch Spanish and Portuguese language platform by Q3 2025\n"
                "  - Target financial services and healthcare verticals\n"
                "  - Investment: $18.8M over three years\n"
                "  - Expected ROI: 2.8x by end of year three\n\n"
                "4.3 European Deepening\n"
                "  - Expand Frankfurt and Amsterdam facilities by 40%\n"
                "  - Achieve ISO 27701 certification for all EU data centers\n"
                "  - Launch dedicated EU compliance dashboard for DORA regulation"
            ),
        },
        # Page 6: Strategic Pillar 2
        {
            "title": "5. Strategic Pillar: Product Innovation",
            "body": (
                "Objective: Launch 6 new products and 15 major feature releases by 2028.\n\n"
                "5.1 AI-Native Platform (Project Aurora)\n"
                "  - Integrated LLM inference endpoints with auto-scaling\n"
                "  - Fine-tuning-as-a-Service for enterprise models\n"
                "  - AI model marketplace with revenue sharing\n"
                "  - Timeline: Beta Q3 2025, GA Q1 2026\n"
                "  - Investment: $42M (R&D + infrastructure)\n\n"
                "5.2 Edge Computing Platform (Project Meridian)\n"
                "  - Lightweight container runtime for edge nodes\n"
                "  - Centralized management console for 10,000+ edge deployments\n"
                "  - Built-in ML inference at the edge\n"
                "  - Timeline: GA Q2 2026\n\n"
                "5.3 Developer Experience Overhaul\n"
                "  - Redesigned CLI with AI-assisted configuration\n"
                "  - Interactive infrastructure-as-code playground\n"
                "  - Real-time cost estimation for architecture changes\n"
                "  - Timeline: Rolling releases throughout 2025-2026"
            ),
        },
        # Page 7: Strategic Pillar 3
        {
            "title": "6. Strategic Pillar: Operational Excellence",
            "body": (
                "Objective: Reduce operational costs by 20% while improving service reliability.\n\n"
                "6.1 Infrastructure Automation\n"
                "  - Implement self-healing infrastructure with ML-based anomaly detection\n"
                "  - Reduce mean time to recovery (MTTR) from 4.2 minutes to under 90 seconds\n"
                "  - Automate 85% of routine operational tasks by Q4 2026\n"
                "  - Expected annual savings: $12.3M\n\n"
                "6.2 Supply Chain Optimization\n"
                "  - Diversify hardware suppliers (reduce single-vendor dependency from 65% to 35%)\n"
                "  - Implement predictive procurement based on capacity forecasting\n"
                "  - Negotiate multi-year contracts with 3 additional chip manufacturers\n"
                "  - Expected annual savings: $8.7M\n\n"
                "6.3 Energy Efficiency\n"
                "  - Achieve carbon neutrality for all data centers by 2027\n"
                "  - Deploy liquid cooling in high-density GPU clusters\n"
                "  - Target Power Usage Effectiveness (PUE) of 1.15 across all facilities\n"
                "  - Current PUE: 1.38 (industry average: 1.57)"
            ),
        },
        # Page 8: Strategic Pillar 4
        {
            "title": "7. Strategic Pillar: Talent Development",
            "body": (
                "Objective: Reduce voluntary attrition from 14.2% to below 8% and grow headcount to 3,200.\n\n"
                "7.1 Compensation and Benefits\n"
                "  - Benchmark all roles to 75th percentile of market compensation\n"
                "  - Introduce equity refresh grants tied to tenure milestones\n"
                "  - Expand remote work policy to cover 90% of engineering roles\n"
                "  - Launch wellness stipend ($2,500/year per employee)\n\n"
                "7.2 Learning and Development\n"
                "  - Partner with Stanford Online and MIT OpenCourseWare for technical training\n"
                "  - Allocate 10% of work time for skill development (Tech Fridays)\n"
                "  - Launch internal mentorship program pairing senior and junior engineers\n"
                "  - Budget: $4.2M annually\n\n"
                "7.3 Diversity and Inclusion\n"
                "  - Increase underrepresented groups in engineering from 22% to 35%\n"
                "  - Expand university recruiting to 15 additional schools\n"
                "  - Launch returnship program for career-break professionals\n"
                "  - Establish Employee Resource Groups for 6 communities"
            ),
        },
        # Page 9: Financial Projections
        {
            "title": "8. Financial Projections",
            "body": (
                "Revenue Projections (Annual Recurring Revenue):\n"
                "  FY2024 (Actual):  $520.0M\n"
                "  FY2025 (Target):  $614.0M  (+18.1%)\n"
                "  FY2026 (Target):  $718.0M  (+16.9%)\n"
                "  FY2027 (Target):  $798.0M  (+11.1%)\n"
                "  FY2028 (Target):  $840.0M  (+5.3%)\n\n"
                "Investment Requirements:\n"
                "  Market Expansion:      $43.3M\n"
                "  Product Innovation:    $62.0M\n"
                "  Operational Programs:  $28.5M\n"
                "  Talent Initiatives:    $16.8M\n"
                "  Total 3-Year CapEx:   $150.6M\n\n"
                "EBITDA Margin Forecast:\n"
                "  FY2024: 24.1% (Actual)\n"
                "  FY2025: 22.8% (investment year)\n"
                "  FY2026: 25.3%\n"
                "  FY2027: 28.7%\n"
                "  FY2028: 31.2%\n\n"
                "Free Cash Flow is projected to remain positive throughout the plan period, "
                "with cumulative FCF of $285M over three years."
            ),
        },
        # Page 10: Implementation Timeline & Governance
        {
            "title": "9. Implementation Timeline and Governance",
            "body": (
                "Phase 1 (Q2 2025 - Q4 2025): Foundation\n"
                "  - Singapore data center operational\n"
                "  - Project Aurora beta launch\n"
                "  - Compensation benchmarking complete\n"
                "  - Self-healing infrastructure v1 deployed\n\n"
                "Phase 2 (Q1 2026 - Q4 2026): Acceleration\n"
                "  - Jakarta data center operational\n"
                "  - Aurora and Meridian GA releases\n"
                "  - Latin America market entry\n"
                "  - 85% operational automation achieved\n\n"
                "Phase 3 (Q1 2027 - Q4 2028): Scale\n"
                "  - Carbon neutrality across all facilities\n"
                "  - $840M ARR target achievement\n"
                "  - Full international revenue target (45%)\n\n"
                "Governance Structure:\n"
                "  - Quarterly Strategy Review Board (CEO + C-suite)\n"
                "  - Monthly Pillar Owner Updates (VP-level)\n"
                "  - Bi-weekly Program Management Office check-ins\n"
                "  - Annual Board of Directors strategy session\n\n"
                "Risk Mitigation: Each pillar maintains a risk register reviewed monthly. "
                "Escalation path: Pillar Owner -> CTO/COO -> CEO -> Board."
            ),
        },
    ]

    for i, content in enumerate(pages_content):
        page = doc.new_page(width=A4_W, height=A4_H)

        if i == 0:
            # Title page: centered title, larger font
            page.insert_textbox(
                pymupdf.Rect(72, 200, A4_W - 72, 400),
                content["title"],
                fontsize=28,
                fontname="hebo",
                color=(0.0, 0.13, 0.33),
                align=pymupdf.TEXT_ALIGN_CENTER,
            )
            page.insert_textbox(
                pymupdf.Rect(72, 420, A4_W - 72, 650),
                content["body"],
                fontsize=12,
                fontname="helv",
                color=(0.2, 0.2, 0.2),
                align=pymupdf.TEXT_ALIGN_CENTER,
            )
            # Draw a decorative line
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(150, 390), pymupdf.Point(A4_W - 150, 390))
            shape.finish(color=(0.0, 0.13, 0.33), width=2)
            shape.commit()
        else:
            # Regular page: heading + body
            page.insert_text(
                pymupdf.Point(72, 72),
                content["title"],
                fontsize=18,
                fontname="hebo",
                color=(0.0, 0.13, 0.33),
            )
            # Underline for heading
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(72, 80), pymupdf.Point(A4_W - 72, 80))
            shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
            shape.commit()

            page.insert_textbox(
                pymupdf.Rect(72, 100, A4_W - 72, A4_H - 60),
                content["body"],
                fontsize=11,
                fontname="helv",
                color=(0.1, 0.1, 0.1),
                align=pymupdf.TEXT_ALIGN_LEFT,
            )

        # Page number at bottom center
        page.insert_text(
            pymupdf.Point(A4_W / 2 - 10, A4_H - 30),
            str(i + 1),
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
