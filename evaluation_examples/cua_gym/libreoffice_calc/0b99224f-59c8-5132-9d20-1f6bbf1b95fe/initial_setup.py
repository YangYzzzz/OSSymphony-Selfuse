"""
Initial Setup: Create a 16-page business strategy document with no watermarks or encryption.
Task ID: pdf_pw_012
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_012'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/strategy_doc.pdf'

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
    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page layout constants
    PAGE_W, PAGE_H = 612, 792  # US Letter
    MARGIN_LEFT = 72
    MARGIN_RIGHT = 540
    MARGIN_TOP = 72
    MARGIN_BOTTOM = 720
    CONTENT_W = MARGIN_RIGHT - MARGIN_LEFT

    # --- Helper to add a page with title and body paragraphs ---
    def add_page(title, paragraphs, include_header=True):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)

        y = MARGIN_TOP

        if include_header:
            # Header line
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(MARGIN_LEFT, 50), pymupdf.Point(MARGIN_RIGHT, 50))
            shape.finish(color=(0.2, 0.2, 0.5), width=1.5)
            shape.commit()
            page.insert_text(pymupdf.Point(MARGIN_LEFT, 45), "Apex Dynamics Inc. — Strategic Plan 2026-2030",
                             fontsize=8, fontname="heit", color=(0.4, 0.4, 0.6))
            y = 72

        # Section title
        page.insert_text(pymupdf.Point(MARGIN_LEFT, y + 20), title,
                         fontsize=18, fontname="hebo", color=(0.1, 0.1, 0.3))
        y += 40

        # Body paragraphs
        for para in paragraphs:
            rect = pymupdf.Rect(MARGIN_LEFT, y, MARGIN_RIGHT, MARGIN_BOTTOM)
            excess = page.insert_textbox(rect, para, fontsize=11, fontname="helv",
                                         color=(0.1, 0.1, 0.1), align=pymupdf.TEXT_ALIGN_JUSTIFY)
            # Estimate how much vertical space was used
            lines_approx = max(1, len(para) / 75)
            y += lines_approx * 14 + 12

            if y > MARGIN_BOTTOM - 40:
                break

        # Footer
        page_num = doc.page_count
        page.insert_text(pymupdf.Point(MARGIN_LEFT, PAGE_H - 30),
                         f"Confidential — Apex Dynamics Inc.    Page {page_num}",
                         fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))
        return page

    # ==================== PAGE 1: Title Page ====================
    p = doc.new_page(width=PAGE_W, height=PAGE_H)
    p.insert_text(pymupdf.Point(150, 250), "APEX DYNAMICS INC.",
                  fontsize=28, fontname="hebo", color=(0.1, 0.1, 0.3))
    p.insert_text(pymupdf.Point(130, 300), "Strategic Business Plan 2026-2030",
                  fontsize=18, fontname="helv", color=(0.2, 0.2, 0.5))
    shape = p.new_shape()
    shape.draw_line(pymupdf.Point(130, 315), pymupdf.Point(480, 315))
    shape.finish(color=(0.2, 0.2, 0.5), width=2)
    shape.commit()
    p.insert_text(pymupdf.Point(180, 380), "Prepared by: Office of the CEO",
                  fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    p.insert_text(pymupdf.Point(180, 400), "Date: March 15, 2026",
                  fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    p.insert_text(pymupdf.Point(180, 420), "Classification: Internal Use Only",
                  fontsize=12, fontname="hebo", color=(0.6, 0.1, 0.1))
    p.insert_text(pymupdf.Point(MARGIN_LEFT, PAGE_H - 30),
                  "Confidential — Apex Dynamics Inc.    Page 1",
                  fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))

    # ==================== PAGE 2: Table of Contents ====================
    add_page("Table of Contents", [
        "1. Executive Summary .................................................. 3",
        "2. Market Analysis & Competitive Landscape .......................... 4",
        "3. Competitive Intelligence Report .................................. 5",
        "4. SWOT Analysis ..................................................... 6",
        "5. Strategic Objectives 2026-2028 ................................... 7",
        "6. Product Roadmap ................................................... 8",
        "7. Financial Projections — Revenue .................................. 9",
        "8. Financial Projections — Cost Structure .......................... 10",
        "9. Go-to-Market Strategy ............................................ 11",
        "10. Talent Acquisition & Organizational Growth ..................... 12",
        "11. Technology Infrastructure Investments .......................... 13",
        "12. Risk Assessment & Mitigation ................................... 14",
        "13. Implementation Timeline ......................................... 15",
        "14. Appendix: Key Assumptions ....................................... 16",
    ])

    # ==================== PAGE 3: Executive Summary ====================
    add_page("1. Executive Summary", [
        "Apex Dynamics Inc. has experienced 34% year-over-year revenue growth in fiscal year 2025, "
        "reaching $187.3 million in total revenue. Our enterprise SaaS platform now serves 2,847 "
        "active customers across 42 countries, with a net revenue retention rate of 128%.",

        "This strategic plan outlines our path to $500 million in annual recurring revenue by 2030. "
        "Key initiatives include expanding into the Asia-Pacific market, launching our AI-powered "
        "analytics module, and deepening our presence in the financial services vertical.",

        "Our competitive advantage rests on three pillars: proprietary machine learning algorithms "
        "that deliver 40% faster data processing than competitors, an industry-leading 99.97% uptime "
        "SLA, and a customer success model that has driven our NPS score to 72.",

        "Capital requirements for the 2026-2030 period total $145 million, primarily allocated to "
        "R&D expansion ($62M), sales and marketing ($48M), and infrastructure ($35M). We project "
        "achieving operating profitability by Q3 2027 with EBITDA margins reaching 22% by 2030.",
    ])

    # ==================== PAGE 4: Market Analysis ====================
    add_page("2. Market Analysis & Competitive Landscape", [
        "The global enterprise analytics market is projected to grow from $68.4 billion in 2025 to "
        "$142.7 billion by 2030, representing a CAGR of 15.8% (Gartner, 2025). Cloud-native solutions "
        "now account for 67% of new deployments, up from 41% in 2022.",

        "Key market segments include: Financial Services ($23.4B, growing at 18.2% CAGR), Healthcare "
        "($15.7B, 16.9% CAGR), Retail & E-commerce ($12.8B, 14.3% CAGR), and Manufacturing ($9.6B, "
        "13.1% CAGR). Our current market share is approximately 2.7% overall, with 8.3% in Financial "
        "Services where we have the strongest positioning.",

        "Regulatory tailwinds are strengthening demand. The EU AI Act, SOC 2 Type II requirements, and "
        "DORA compliance mandates in financial services are driving organizations toward auditable, "
        "enterprise-grade analytics platforms — a core strength of our offering.",

        "Geographic expansion opportunities are significant. Asia-Pacific represents 31% of global "
        "enterprise software spending but only 4% of our current revenue. Japan, Australia, and Singapore "
        "have been identified as priority markets for 2026-2027 entry.",
    ])

    # ==================== PAGE 5: Competitive Intelligence ====================
    add_page("3. Competitive Intelligence Report", [
        "Primary competitors include DataVault Systems (est. revenue $420M, 6.1% market share), "
        "Prism Analytics ($310M, 4.5%), NovaTech Solutions ($265M, 3.9%), and CloudMetrics Inc. "
        "($195M, 2.9%). Our positioning as the fastest-growing platform in the segment gives us "
        "momentum advantage despite smaller absolute scale.",

        "DataVault's recent acquisition of StreamLogic for $890M signals intent to strengthen their "
        "real-time processing capabilities — an area where we currently lead. Their integration "
        "timeline is estimated at 18-24 months, providing a window to extend our advantage.",

        "Prism Analytics announced a $200M Series E at a $3.2B valuation. Their stated focus on "
        "healthcare vertical AI creates moderate competitive pressure in one of our growth segments. "
        "However, their platform reliability (99.91% uptime) remains significantly below our SLA.",

        "NovaTech's open-source strategy has gained developer mindshare but struggles with enterprise "
        "conversion. Their reported enterprise close rate of 3.2% (vs. our 11.7%) validates our "
        "premium positioning approach.",
    ])

    # ==================== PAGE 6: SWOT Analysis ====================
    add_page("4. SWOT Analysis", [
        "STRENGTHS: Proprietary ML pipeline with 23 patents pending. Industry-leading platform "
        "reliability at 99.97% uptime. Strong unit economics with LTV:CAC ratio of 5.8x. Deep "
        "financial services expertise with 340+ banking and insurance clients. World-class engineering "
        "team — 78% hold advanced degrees, median tenure 3.4 years.",

        "WEAKNESSES: Limited brand recognition outside North America and Europe. Sales cycle averaging "
        "127 days for enterprise deals (target: sub-90 days). Technical debt in legacy data connectors "
        "requiring $8.2M remediation investment. Concentration risk with top 10 customers representing "
        "23% of ARR.",

        "OPPORTUNITIES: Asia-Pacific market entry with projected $45M incremental ARR by 2028. "
        "AI-powered predictive analytics module with $30M pipeline already identified. Federal "
        "government vertical through FedRAMP authorization (application submitted Q4 2025). "
        "Strategic partnerships with Salesforce and SAP for integrated analytics workflows.",

        "THREATS: Hyperscaler competition from AWS QuickSight and Google Looker gaining enterprise "
        "traction. Potential economic downturn reducing enterprise IT budgets by estimated 12-15%. "
        "Talent market competition with FAANG compensation packages. Regulatory fragmentation across "
        "markets increasing compliance costs.",
    ])

    # ==================== PAGE 7: Strategic Objectives ====================
    add_page("5. Strategic Objectives 2026-2028", [
        "Objective 1 — Revenue Scale: Achieve $320M ARR by end of FY2028, representing 71% growth "
        "from current $187.3M baseline. This requires maintaining 20%+ net new ARR growth rate while "
        "sustaining 128% net revenue retention.",

        "Objective 2 — Market Expansion: Establish physical presence in Tokyo, Sydney, and Singapore "
        "by Q2 2027. Target 15% of revenue from APAC by 2028, up from current 4%. Hire 45 "
        "region-dedicated sales and customer success professionals.",

        "Objective 3 — Product Innovation: Launch AI Analytics Suite by Q3 2026, targeting $30M in "
        "first-year bookings. Achieve SOC 2 Type II + ISO 27001 dual certification by Q1 2027. "
        "Release real-time collaboration features to reduce customer workflow friction by 40%.",

        "Objective 4 — Operational Excellence: Reduce customer acquisition cost from $42,300 to "
        "$34,000 by optimizing digital marketing funnel and partner channel. Achieve 22% EBITDA "
        "margin by FY2030 through operational leverage and platform efficiency gains.",
    ])

    # ==================== PAGE 8: Product Roadmap ====================
    add_page("6. Product Roadmap", [
        "Q1-Q2 2026: AI Analytics Suite beta release to 50 design partners. Enhanced data connector "
        "library supporting 200+ enterprise data sources. Mobile dashboard application for iOS and "
        "Android with offline capability.",

        "Q3-Q4 2026: General availability of AI Analytics Suite. Natural language query interface "
        "powered by GPT-4 integration. Automated anomaly detection with configurable alert thresholds. "
        "FedRAMP High authorization milestone.",

        "Q1-Q2 2027: Real-time collaboration workspace for team analytics. Embedded analytics SDK "
        "for ISV partners. Multi-region data residency options (EU, APAC, US). Advanced role-based "
        "access control with attribute-based policies.",

        "Q3-Q4 2027: Predictive forecasting engine with 95% confidence intervals. Industry-specific "
        "analytics templates for top 5 verticals. GraphQL API for developer ecosystem. Automated "
        "compliance reporting for SOX, GDPR, and DORA.",
    ])

    # ==================== PAGE 9: Financial Projections — Revenue ====================
    add_page("7. Financial Projections — Revenue", [
        "FY2025 Actual: Total Revenue $187.3M (Subscription: $168.6M, Services: $18.7M). "
        "YoY Growth: 34.2%. Gross Margin: 76.8%. Net Revenue Retention: 128%.",

        "FY2026 Projected: Total Revenue $243.5M (Subscription: $221.6M, Services: $21.9M). "
        "YoY Growth: 30.0%. Gross Margin Target: 78.5%. Key driver: AI Analytics Suite launch "
        "contributing estimated $15M in H2 bookings.",

        "FY2027 Projected: Total Revenue $316.6M (Subscription: $291.3M, Services: $25.3M). "
        "YoY Growth: 30.0%. Gross Margin Target: 80.2%. Key driver: APAC expansion contributing "
        "$28M, AI Suite ramping to $45M annual run rate.",

        "FY2028 Projected: Total Revenue $395.7M (Subscription: $367.0M, Services: $28.7M). "
        "YoY Growth: 25.0%. FY2029: $475M. FY2030: $547M at 22% EBITDA margin. "
        "Cumulative 5-year revenue: $1,978M.",
    ])

    # ==================== PAGE 10: Financial Projections — Costs ====================
    add_page("8. Financial Projections — Cost Structure", [
        "R&D Investment: $38.2M (FY2025) scaling to $62.0M by FY2028. Headcount growth from 187 "
        "to 310 engineers. Key investments: AI/ML team expansion ($12M), platform scalability ($8M), "
        "security and compliance ($5M), developer experience ($4M).",

        "Sales & Marketing: $52.4M (FY2025) scaling to $78.0M by FY2028. Investment in APAC field "
        "sales team ($8.5M), digital marketing automation ($4.2M), partner ecosystem development "
        "($3.8M), and brand awareness campaigns ($6.5M).",

        "General & Administrative: $18.7M (FY2025) scaling to $24.0M by FY2028. Includes new "
        "regional offices ($3.2M), legal and compliance infrastructure ($2.1M), and ERP system "
        "upgrade ($1.8M).",

        "Capital Expenditure: Total 5-year investment of $145M. Breakdown: Cloud infrastructure "
        "$35M, office buildouts $12M, equipment and tooling $8M. Operating lease commitments "
        "total $42M over the period.",
    ])

    # ==================== PAGE 11: Go-to-Market Strategy ====================
    add_page("9. Go-to-Market Strategy", [
        "Enterprise Direct Sales: Maintain 60% of new ARR from direct sales team. Expand enterprise "
        "account executives from 34 to 55 by end of 2027. Target average deal size increase from "
        "$127K to $165K through platform bundling and multi-year commitments.",

        "Partner Channel: Grow partner-sourced revenue from 12% to 25% of new ARR by 2028. "
        "Strategic alliances with Deloitte, Accenture, and PwC for implementation services. "
        "Technology partnerships with Snowflake, Databricks, and AWS for co-selling motions.",

        "Product-Led Growth: Launch self-service tier targeting mid-market companies (500-2000 "
        "employees). Target 5,000 self-service accounts by 2027, with 8% conversion to enterprise. "
        "Freemium data connector marketplace to build developer community.",

        "Digital Marketing: Increase content marketing investment by 150%. Launch industry-specific "
        "podcast series and executive briefing program. Target 40% of qualified pipeline from "
        "inbound channels by 2028, up from current 22%.",
    ])

    # ==================== PAGE 12: Talent & Organization ====================
    add_page("10. Talent Acquisition & Organizational Growth", [
        "Current headcount: 423 employees across 6 offices. Planned growth to 680 by end of 2028. "
        "Key hiring priorities: Engineering (123 new hires), Sales (67), Customer Success (34), "
        "Product Management (18), and G&A (15).",

        "Compensation philosophy: Target 75th percentile for base salary, with equity participation "
        "for all full-time employees. Annual equity refresh grants averaging 15% of initial grant. "
        "Performance bonus pool of 12-20% of base salary for individual contributors.",

        "Diversity and inclusion targets: Achieve 40% underrepresented groups in new hires by 2027. "
        "Establish Employee Resource Groups for Women in Tech, BIPOC, LGBTQ+, and Veterans. "
        "Partner with 12 universities for diverse pipeline development.",

        "Retention strategy: Maintain voluntary attrition below 12% (currently 9.3%). Key levers: "
        "career pathing framework, learning stipend of $3,000/year, sabbatical program at 5-year "
        "tenure, and hybrid work model with 2 office days minimum.",
    ])

    # ==================== PAGE 13: Technology Infrastructure ====================
    add_page("11. Technology Infrastructure Investments", [
        "Cloud architecture migration: Complete transition from hybrid to cloud-native by Q4 2027. "
        "Multi-cloud strategy with AWS as primary (70%) and GCP as secondary (30%). Projected "
        "infrastructure cost savings of 18% through reserved instance optimization.",

        "Data platform modernization: Upgrade to Apache Iceberg table format for data lakehouse "
        "architecture. Implement real-time CDC pipelines using Debezium. Target sub-100ms query "
        "latency for 95th percentile of dashboard loads.",

        "Security posture enhancement: Zero-trust network architecture implementation by Q2 2027. "
        "SOC 2 Type II continuous monitoring. Customer-managed encryption keys (CMEK) for enterprise "
        "tier. Bug bounty program expansion with $500K annual budget.",

        "Developer productivity: Internal developer platform (IDP) reducing deployment cycle time "
        "from 4.2 days to 0.5 days. AI-assisted code review reducing defect escape rate by 35%. "
        "Automated testing coverage target of 92% across all production services.",
    ])

    # ==================== PAGE 14: Risk Assessment ====================
    add_page("12. Risk Assessment & Mitigation", [
        "Economic Risk (HIGH): Global recession probability estimated at 25-30% for 2026-2027. "
        "Mitigation: Maintain 18 months operating runway, diversify customer base across industries, "
        "and offer flexible payment terms to retain at-risk accounts.",

        "Competitive Risk (MEDIUM-HIGH): Hyperscaler analytics offerings gaining enterprise traction. "
        "Mitigation: Accelerate product differentiation through AI capabilities, deepen vertical "
        "expertise, and strengthen switching costs via platform integrations.",

        "Cybersecurity Risk (MEDIUM): Increasing sophistication of supply chain attacks. "
        "Mitigation: SBOM (Software Bill of Materials) for all dependencies, quarterly penetration "
        "testing by third-party firms, $10M cyber insurance policy, and 24/7 SOC operations.",

        "Regulatory Risk (MEDIUM): Evolving data privacy regulations across jurisdictions. "
        "Mitigation: Dedicated compliance team of 8 FTEs, proactive engagement with regulators, "
        "modular data residency architecture, and automated compliance monitoring.",
    ])

    # ==================== PAGE 15: Implementation Timeline ====================
    add_page("13. Implementation Timeline", [
        "Phase 1 — Foundation (Q1-Q2 2026): AI Analytics Suite beta launch. Tokyo office establishment. "
        "FedRAMP application advancement. Hiring wave 1: 45 engineering and 20 sales roles. Partner "
        "program launch with Deloitte and Accenture.",

        "Phase 2 — Acceleration (Q3 2026 - Q2 2027): AI Suite GA release. Sydney and Singapore offices. "
        "Self-service tier launch. SOC 2 + ISO 27001 dual certification. Hiring wave 2: 35 engineering, "
        "25 sales, 15 customer success roles.",

        "Phase 3 — Scale (Q3 2027 - Q4 2028): Predictive analytics engine release. APAC revenue "
        "target of $45M. Partner channel contributing 25% of new ARR. Operating profitability "
        "achievement. Hiring wave 3: 40 engineering, 22 sales roles.",

        "Key Milestones: $250M ARR (Q4 2026), $320M ARR (Q4 2027), APAC breakeven (Q2 2028), "
        "22% EBITDA margin (Q4 2030). Board reviews scheduled quarterly with full strategy "
        "reassessment annually in Q4.",
    ])

    # ==================== PAGE 16: Appendix ====================
    add_page("14. Appendix: Key Assumptions", [
        "Market growth assumptions: Enterprise analytics TAM growing at 15.8% CAGR (Gartner 2025). "
        "Cloud migration rate: 8-10% annual shift from on-premise to cloud. Average enterprise "
        "analytics budget increase: 12% annually.",

        "Financial model assumptions: Gross margin improvement from 76.8% to 82% driven by platform "
        "scale economies. CAC payback period reducing from 14 months to 10 months. Churn rate "
        "stable at 5.2% gross, offset by expansion revenue.",

        "Currency assumptions: USD/JPY at 148, USD/AUD at 0.66, USD/SGD at 1.34. Hedging policy "
        "covers 60% of projected non-USD revenue. Interest rate environment: Federal Funds Rate "
        "projected at 3.75-4.25% through 2027.",

        "Scenario analysis: Base case as presented. Bull case (+15% revenue) assumes faster APAC "
        "adoption and AI Suite exceeding targets. Bear case (-20% revenue) assumes economic downturn "
        "and delayed market expansion. All scenarios maintain positive cash flow by 2028.",
    ])

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: {doc.page_count}')
    doc.close()

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')

create_initial()
