"""
Initial Setup: Create a 22-page quarterly report PDF without headers/footers
Task ID: pdf_fm_091
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_091'
DOCUMENTS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS_DIR}/quarterly_q3.pdf'


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
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page dimensions (Letter size)
    W, H = 612, 792
    LEFT_MARGIN = 72
    RIGHT_MARGIN = 540
    CONTENT_WIDTH = RIGHT_MARGIN - LEFT_MARGIN

    # ----- Content for 22 pages of a quarterly report -----

    pages_content = [
        # Page 1: Title Page
        {
            "title": None,
            "body": None,
            "custom": "title_page",
        },
        # Page 2: Table of Contents
        {
            "title": "Table of Contents",
            "body": (
                "1. Executive Summary ........................... 3\n"
                "2. Financial Highlights ........................ 4\n"
                "3. Revenue Breakdown ........................... 6\n"
                "4. Operating Expenses .......................... 8\n"
                "5. Regional Performance ........................ 10\n"
                "6. Product Line Analysis ....................... 12\n"
                "7. Customer Metrics ............................ 14\n"
                "8. Strategic Initiatives ....................... 16\n"
                "9. Risk Assessment ............................. 18\n"
                "10. Outlook & Guidance ......................... 20\n"
                "11. Appendix ................................... 22"
            ),
        },
        # Page 3: Executive Summary
        {
            "title": "1. Executive Summary",
            "body": (
                "Company XYZ delivered a strong third quarter, achieving total revenues of $127.4 million, "
                "representing a 14.2% increase over the same period last year. Operating income reached $31.8 million, "
                "reflecting improved operational efficiency across all business segments.\n\n"
                "Key highlights for Q3 2025 include:\n\n"
                "- Revenue growth of 14.2% year-over-year, driven primarily by our Enterprise Solutions division\n"
                "- Gross margin improvement of 180 basis points to 62.3%\n"
                "- Net income of $24.6 million, up from $19.1 million in Q3 2024\n"
                "- Customer retention rate of 94.7%, the highest in the company's history\n"
                "- Successful launch of the Aurora platform, contributing $8.3 million in new revenue\n"
                "- Free cash flow of $28.9 million, enabling continued investment in R&D\n\n"
                "The leadership team remains confident in our ability to meet full-year guidance of $490-510 million "
                "in total revenue, supported by a robust pipeline and strong customer engagement metrics."
            ),
        },
        # Page 4-5: Financial Highlights
        {
            "title": "2. Financial Highlights",
            "body": (
                "Consolidated Financial Summary (in millions USD)\n\n"
                "                          Q3 2025    Q3 2024    Change\n"
                "Total Revenue             $127.4     $111.6     +14.2%\n"
                "Cost of Revenue            $48.1      $43.8     +9.8%\n"
                "Gross Profit               $79.3      $67.8     +17.0%\n"
                "Gross Margin               62.3%      60.5%     +180bps\n"
                "Operating Expenses         $47.5      $42.1     +12.8%\n"
                "Operating Income           $31.8      $25.7     +23.7%\n"
                "Operating Margin           25.0%      23.0%     +200bps\n"
                "Net Income                 $24.6      $19.1     +28.8%\n"
                "Diluted EPS                $1.23      $0.96     +28.1%\n\n"
                "Balance Sheet Highlights:\n"
                "- Cash and equivalents: $189.7 million (up from $162.3 million at end of Q2)\n"
                "- Total debt: $45.0 million (long-term credit facility)\n"
                "- Accounts receivable: $38.4 million (DSO of 27 days)\n"
                "- Deferred revenue: $54.2 million, indicating strong future revenue visibility"
            ),
        },
        {
            "title": "2. Financial Highlights (continued)",
            "body": (
                "Cash Flow Statement Summary (in millions USD)\n\n"
                "                                  Q3 2025    Q3 2024\n"
                "Cash from Operations               $33.2      $26.8\n"
                "Capital Expenditures                ($4.3)     ($3.9)\n"
                "Free Cash Flow                      $28.9      $22.9\n"
                "Acquisitions                        ($0.0)     ($12.5)\n"
                "Stock Repurchases                   ($5.0)     ($3.0)\n"
                "Dividends Paid                      ($4.8)     ($4.2)\n\n"
                "The company generated record free cash flow of $28.9 million during Q3, reflecting "
                "strong working capital management and improved collections. Capital expenditures remained "
                "moderate at $4.3 million, primarily invested in data center infrastructure and security "
                "enhancements. The Board approved a quarterly dividend of $0.24 per share, payable on "
                "November 15, 2025, to shareholders of record as of October 31, 2025."
            ),
        },
        # Page 6-7: Revenue Breakdown
        {
            "title": "3. Revenue Breakdown by Segment",
            "body": (
                "Enterprise Solutions Division - $68.2 million (+18.4% YoY)\n\n"
                "The Enterprise Solutions segment continued to be the primary growth engine, benefiting from "
                "expanded adoption of the Aurora platform and increased deal sizes among Fortune 500 clients. "
                "Average contract value grew 22% to $1.4 million, while new logo acquisition remained healthy "
                "with 14 new enterprise clients onboarded during the quarter.\n\n"
                "Key enterprise wins in Q3:\n"
                "- Meridian Healthcare Systems: $4.8M three-year agreement\n"
                "- Pinnacle Financial Group: $3.2M platform migration\n"
                "- Horizon Manufacturing Corp: $2.7M expansion deal\n"
                "- Atlas Logistics International: $2.1M new deployment\n\n"
                "Small and Medium Business (SMB) Division - $38.6 million (+9.1% YoY)\n\n"
                "The SMB segment delivered steady growth, driven by self-service platform adoption and "
                "improved channel partner performance. Monthly recurring revenue (MRR) from SMB customers "
                "reached $12.9 million, up from $11.8 million in Q2 2025."
            ),
        },
        {
            "title": "3. Revenue Breakdown (continued)",
            "body": (
                "Professional Services Division - $20.6 million (+8.4% YoY)\n\n"
                "Professional Services revenue grew modestly as the company continues to shift toward "
                "higher-margin subscription offerings. Implementation services accounted for $12.3 million, "
                "while consulting and training services contributed $8.3 million.\n\n"
                "Revenue by Geography:\n\n"
                "                     Q3 2025    % of Total    YoY Growth\n"
                "North America        $82.8M       65.0%        +12.8%\n"
                "Europe               $28.0M       22.0%        +16.1%\n"
                "Asia Pacific         $12.7M       10.0%        +19.5%\n"
                "Rest of World         $3.8M        3.0%        +11.8%\n\n"
                "International revenue represented 35% of total revenue, up from 33% in Q3 2024, reflecting "
                "the company's successful expansion into key European and Asia Pacific markets."
            ),
        },
        # Page 8-9: Operating Expenses
        {
            "title": "4. Operating Expenses",
            "body": (
                "Total operating expenses were $47.5 million in Q3 2025, compared to $42.1 million in Q3 2024, "
                "representing a 12.8% increase. As a percentage of revenue, operating expenses declined from "
                "37.7% to 37.3%, demonstrating operating leverage.\n\n"
                "Research & Development - $18.9 million (14.8% of revenue)\n"
                "R&D spending increased 15.8% year-over-year, reflecting investments in:\n"
                "- Aurora platform enhancements and AI-powered features\n"
                "- Next-generation data analytics engine\n"
                "- Security infrastructure improvements (SOC 2 Type II compliance)\n"
                "- Mobile application development\n\n"
                "The R&D team expanded to 342 engineers, including 28 new hires focused on machine learning "
                "and natural language processing capabilities."
            ),
        },
        {
            "title": "4. Operating Expenses (continued)",
            "body": (
                "Sales & Marketing - $21.4 million (16.8% of revenue)\n"
                "Sales and marketing expenses increased 11.5% year-over-year but declined as a percentage of "
                "revenue from 17.2% to 16.8%. The efficiency improvement was driven by:\n"
                "- Higher marketing-qualified lead conversion rates (up to 18.3% from 15.7%)\n"
                "- Reduced customer acquisition cost ($4,200 vs $4,800 in Q3 2024)\n"
                "- Expanded partner channel contributing 23% of new bookings\n\n"
                "General & Administrative - $7.2 million (5.7% of revenue)\n"
                "G&A expenses were relatively flat year-over-year, benefiting from process automation "
                "initiatives and shared services optimization. Key investments included:\n"
                "- ERP system modernization (Phase 2 complete)\n"
                "- Compliance infrastructure for GDPR and CCPA\n"
                "- Talent acquisition platform implementation\n\n"
                "Headcount Summary:\n"
                "                     Q3 2025    Q2 2025    Q3 2024\n"
                "Total Employees        1,247      1,198      1,089\n"
                "Engineering              342        314        287\n"
                "Sales & Marketing        489        472        421\n"
                "G&A                      186        182        172\n"
                "Professional Services    230        230        209"
            ),
        },
        # Page 10-11: Regional Performance
        {
            "title": "5. Regional Performance",
            "body": (
                "North America ($82.8M, +12.8% YoY)\n\n"
                "The North American market remained our strongest region, contributing 65% of total revenue. "
                "Growth was driven by enterprise upsells and cross-sells within our existing customer base. "
                "Notable achievements include:\n"
                "- 97% renewal rate among top 50 accounts\n"
                "- 31% increase in average deal size for new enterprise contracts\n"
                "- Expansion into Canadian public sector with $6.2M in new contracts\n\n"
                "The US federal business pipeline grew to $45 million, supported by FedRAMP authorization "
                "achieved in July 2025.\n\n"
                "Europe ($28.0M, +16.1% YoY)\n\n"
                "European operations delivered exceptional growth, led by strong performance in the UK, "
                "Germany, and the Nordics. The London office expanded to 85 employees, and we established "
                "a new presence in Amsterdam to serve Benelux customers.\n\n"
                "Key European milestones:\n"
                "- Deutsche Telekom partnership generating $3.8M in Q3\n"
                "- UK Government Digital Service framework approval\n"
                "- DACH region revenue up 24% to $9.1 million"
            ),
        },
        {
            "title": "5. Regional Performance (continued)",
            "body": (
                "Asia Pacific ($12.7M, +19.5% YoY)\n\n"
                "Asia Pacific continued to be our fastest-growing region, with particular strength in "
                "Australia, Japan, and Singapore. The Q3 performance was bolstered by:\n"
                "- Three new enterprise wins in Japan totaling $4.1 million\n"
                "- Australian government contract expansion worth $2.3 million\n"
                "- Singapore regional hub fully operational, serving Southeast Asian clients\n\n"
                "The APAC team grew to 78 employees across four offices (Tokyo, Sydney, Singapore, Mumbai). "
                "We expect continued strong growth in this region as we invest in local language support "
                "and data residency solutions.\n\n"
                "Rest of World ($3.8M, +11.8% YoY)\n\n"
                "Rest of World revenue, primarily from Latin America and the Middle East, grew steadily. "
                "We signed our first major contract in Brazil ($1.2 million with Banco Nacional) and "
                "expanded our UAE presence through a partnership with Emirates Technology Group. "
                "The company plans to establish a dedicated Latin American office in Sao Paulo in Q1 2026."
            ),
        },
        # Page 12-13: Product Line Analysis
        {
            "title": "6. Product Line Analysis",
            "body": (
                "Aurora Platform\n"
                "Revenue: $8.3M | Growth: N/A (launched Q2 2025) | ARR Run Rate: $34M\n\n"
                "The Aurora platform, our next-generation cloud-native solution, exceeded initial expectations "
                "in its second quarter of availability. Key metrics:\n"
                "- 47 enterprise customers adopted Aurora in Q3\n"
                "- Average deployment time reduced to 6 weeks from 12 weeks (legacy platform)\n"
                "- Customer satisfaction score of 4.6/5.0\n"
                "- 99.97% uptime since launch\n\n"
                "Core Platform\n"
                "Revenue: $89.5M | Growth: +8.2% YoY | ARR: $362M\n\n"
                "The Core Platform continues to generate the majority of revenue and remains the foundation "
                "for our installed base. Migration incentives have encouraged 15% of Core customers to begin "
                "evaluating Aurora. We expect the migration cycle to take 18-24 months for the majority of "
                "customers, with full support for Core continuing through 2028."
            ),
        },
        {
            "title": "6. Product Line Analysis (continued)",
            "body": (
                "Data Analytics Suite\n"
                "Revenue: $18.4M | Growth: +21.3% YoY | ARR: $74M\n\n"
                "The Data Analytics Suite continued its strong growth trajectory, driven by increasing demand "
                "for real-time business intelligence. The Q3 release introduced:\n"
                "- AI-powered anomaly detection across all data sources\n"
                "- Natural language query interface (beta, 200+ users enrolled)\n"
                "- Enhanced visualization library with 45 new chart types\n"
                "- Direct integration with 12 new third-party data connectors\n\n"
                "Integration Services\n"
                "Revenue: $11.2M | Growth: +5.8% YoY | ARR: $45M\n\n"
                "Integration Services revenue grew moderately as customers consolidated their technology "
                "stacks. The pre-built connector library expanded to 280+ integrations, reducing "
                "implementation time by an average of 35%. Strategic API partnerships were established with "
                "Salesforce, ServiceNow, and Workday during the quarter."
            ),
        },
        # Page 14-15: Customer Metrics
        {
            "title": "7. Customer Metrics",
            "body": (
                "Customer Base Overview\n\n"
                "                        Q3 2025    Q2 2025    Q3 2024\n"
                "Total Customers          3,847      3,712      3,298\n"
                "Enterprise (>$100K ARR)    412        389        341\n"
                "Mid-Market ($25K-$100K)    987        952        876\n"
                "SMB (<$25K)              2,448      2,371      2,081\n\n"
                "Net Revenue Retention Rate: 118%\n"
                "This metric reflects the combined impact of upsells, cross-sells, and churn within our "
                "existing customer base. The 118% rate indicates that revenue expansion from existing "
                "customers more than offsets any losses from downgrades or churn.\n\n"
                "Customer Retention Rate: 94.7%\n"
                "Our highest retention rate on record, driven by improved customer success programs and "
                "proactive account management. The Customer Success team expanded to 45 dedicated CSMs, "
                "each managing an average of 9 enterprise accounts."
            ),
        },
        {
            "title": "7. Customer Metrics (continued)",
            "body": (
                "Net Promoter Score: 67\n"
                "NPS improved from 61 in Q2 to 67 in Q3, placing Company XYZ in the top quartile of "
                "enterprise software providers. Key satisfaction drivers included:\n"
                "- Product reliability and uptime\n"
                "- Quality of customer support (average response time: 2.1 hours)\n"
                "- Pace of feature innovation\n\n"
                "Customer Lifetime Value (CLV) Analysis:\n"
                "- Enterprise: $4.2 million (up from $3.6 million)\n"
                "- Mid-Market: $890,000 (up from $780,000)\n"
                "- SMB: $145,000 (up from $128,000)\n\n"
                "Churn Analysis:\n"
                "Gross revenue churn remained low at 3.2% on an annualized basis. The primary reasons "
                "for churn were:\n"
                "- Customer M&A activity (38% of churned revenue)\n"
                "- Budget constraints / downsizing (29%)\n"
                "- Competitive displacement (18%)\n"
                "- Product fit issues (15%)\n\n"
                "The competitive displacement rate declined from 24% in Q3 2024 to 18%, reflecting "
                "improved product competitiveness and customer engagement."
            ),
        },
        # Page 16-17: Strategic Initiatives
        {
            "title": "8. Strategic Initiatives",
            "body": (
                "Initiative 1: AI-First Strategy\n\n"
                "Company XYZ is embedding artificial intelligence across all product lines. In Q3, we:\n"
                "- Launched AI Copilot for the Aurora platform, assisting users with workflow automation\n"
                "- Deployed machine learning models for predictive analytics in the Data Suite\n"
                "- Filed 8 new patents related to AI-driven process optimization\n"
                "- Established AI Ethics Board to ensure responsible AI development\n\n"
                "Investment to date: $14.2 million in AI R&D during 2025\n"
                "Expected revenue impact: $25-30 million incremental revenue by end of 2026\n\n"
                "Initiative 2: Platform Ecosystem Expansion\n\n"
                "The Company XYZ Marketplace launched in August 2025 with 85 third-party applications "
                "and integrations. Key metrics:\n"
                "- 850+ developers registered in the partner program\n"
                "- 23 certified solution partners\n"
                "- Average of 12 new apps published per month\n"
                "- Marketplace-influenced revenue of $3.4 million in Q3"
            ),
        },
        {
            "title": "8. Strategic Initiatives (continued)",
            "body": (
                "Initiative 3: Global Expansion\n\n"
                "Our international growth strategy continues to deliver results:\n"
                "- Opened Amsterdam office (Q3 2025)\n"
                "- Planning Sao Paulo office (Q1 2026)\n"
                "- Data center established in Frankfurt for EU data residency\n"
                "- Achieved ISO 27001 certification for all international operations\n"
                "- Localization completed for Japanese, German, French, and Portuguese\n\n"
                "Initiative 4: Sustainability & ESG\n\n"
                "Company XYZ is committed to environmental and social responsibility:\n"
                "- Achieved carbon neutrality for all Scope 1 and Scope 2 emissions\n"
                "- Renewable energy powers 92% of data center operations\n"
                "- Diversity hiring: 47% of new hires in Q3 from underrepresented groups\n"
                "- Community investment: $1.2 million donated through XYZ Foundation\n"
                "- Published inaugural ESG report in September 2025\n\n"
                "We received a B+ rating from MSCI ESG Research, up from B in the prior year assessment."
            ),
        },
        # Page 18-19: Risk Assessment
        {
            "title": "9. Risk Assessment",
            "body": (
                "Key Risk Factors\n\n"
                "1. Macroeconomic Uncertainty\n"
                "Elevated interest rates and potential economic slowdown could impact enterprise IT spending. "
                "Mitigation: Diversified customer base across industries and geographies; essential nature "
                "of our platform for customer operations.\n\n"
                "2. Competitive Landscape\n"
                "Increased competition from both established players and well-funded startups. "
                "Mitigation: Continuous innovation, strong customer relationships, and high switching costs. "
                "Competitive win rates improved to 58% in Q3 (from 52% in Q3 2024).\n\n"
                "3. Talent Acquisition and Retention\n"
                "Tight labor market for specialized technology roles. "
                "Mitigation: Competitive compensation packages, remote work flexibility, equity incentive "
                "programs, and focus on employee development. Voluntary turnover rate: 8.2% annualized.\n\n"
                "4. Cybersecurity\n"
                "Evolving threat landscape requires continuous investment. "
                "Mitigation: Zero-trust architecture, regular third-party penetration testing, "
                "24/7 Security Operations Center, and cybersecurity insurance coverage."
            ),
        },
        {
            "title": "9. Risk Assessment (continued)",
            "body": (
                "5. Regulatory Compliance\n"
                "Increasing data privacy regulations globally (GDPR, CCPA, PIPEDA, LGPD). "
                "Mitigation: Dedicated compliance team, regional data residency options, "
                "and privacy-by-design product development methodology.\n\n"
                "6. Technology Platform Risk\n"
                "Risk of technology disruption or migration challenges between Core and Aurora platforms. "
                "Mitigation: Phased migration approach, backward compatibility guarantees, and dedicated "
                "migration support team of 35 specialists.\n\n"
                "7. Foreign Currency Exposure\n"
                "35% of revenue denominated in non-USD currencies. "
                "Mitigation: Natural hedging through local cost structures, forward contracts covering "
                "80% of anticipated non-USD revenue for the next two quarters.\n\n"
                "Risk Heat Map Summary:\n"
                "                     Impact    Likelihood    Trend\n"
                "Macroeconomic        High      Medium        Stable\n"
                "Competition          Medium    High          Increasing\n"
                "Talent               Medium    Medium        Improving\n"
                "Cybersecurity        High      Medium        Stable\n"
                "Regulatory           Medium    Medium        Increasing\n"
                "Platform             Medium    Low           Improving\n"
                "Currency             Low       High          Stable"
            ),
        },
        # Page 20-21: Outlook & Guidance
        {
            "title": "10. Outlook & Guidance",
            "body": (
                "Q4 2025 Guidance\n\n"
                "- Revenue: $132-136 million\n"
                "- Operating margin: 24-26%\n"
                "- Diluted EPS: $1.28-$1.35\n"
                "- Free cash flow: $30-34 million\n\n"
                "Full Year 2025 Guidance (Updated)\n\n"
                "- Revenue: $490-510 million (raised from $475-495 million)\n"
                "- Operating margin: 23-25% (raised from 22-24%)\n"
                "- Diluted EPS: $4.70-$4.95 (raised from $4.45-$4.70)\n"
                "- Free cash flow: $105-115 million (raised from $95-105 million)\n\n"
                "The guidance increase reflects strong Q3 performance and improved visibility into Q4 "
                "pipeline. Approximately 78% of Q4 projected revenue is already under contract or highly "
                "committed, providing confidence in the updated range."
            ),
        },
        {
            "title": "10. Outlook & Guidance (continued)",
            "body": (
                "Strategic Priorities for Q4 2025 and Beyond\n\n"
                "1. Accelerate Aurora Adoption\n"
                "Target: 100+ enterprise Aurora customers by year-end. Current: 62. "
                "Focus on migration tooling and customer success-led adoption programs.\n\n"
                "2. Expand AI Capabilities\n"
                "Launch AI Copilot for Data Analytics Suite in November 2025. "
                "Begin beta testing of AI-driven predictive workflow automation.\n\n"
                "3. International Expansion\n"
                "Target: International revenue to reach 38% of total by Q4 2025. "
                "Focus on DACH region, Japan, and Brazil.\n\n"
                "4. Operational Efficiency\n"
                "Continue driving operating leverage through automation and process optimization. "
                "Target: 25% operating margin for full year 2026.\n\n"
                "5. Talent Development\n"
                "Launch Company XYZ Academy for employee skill development. "
                "Target 1,400 employees by year-end 2025.\n\n"
                "The management team is confident in the company's trajectory and remains committed "
                "to delivering sustainable, profitable growth while investing in long-term value creation."
            ),
        },
        # Page 22: Appendix
        {
            "title": "11. Appendix - Supplementary Financial Data",
            "body": (
                "Quarterly Revenue Trend (in millions USD)\n\n"
                "Quarter    Revenue    YoY Growth    Sequential Growth\n"
                "Q1 2024    $103.2     +11.8%        -2.1%\n"
                "Q2 2024    $107.8     +12.4%        +4.5%\n"
                "Q3 2024    $111.6     +13.1%        +3.5%\n"
                "Q4 2024    $118.4     +13.8%        +6.1%\n"
                "Q1 2025    $115.6     +12.0%        -2.4%\n"
                "Q2 2025    $121.8     +13.0%        +5.4%\n"
                "Q3 2025    $127.4     +14.2%        +4.6%\n\n"
                "Top 10 Customers (% of Revenue)\n"
                "1. Meridian Healthcare       4.2%\n"
                "2. Pinnacle Financial        3.8%\n"
                "3. Horizon Manufacturing     3.1%\n"
                "4. Atlas Logistics           2.7%\n"
                "5. Vertex Telecommunications 2.4%\n"
                "6. Cascade Energy Corp       2.1%\n"
                "7. Summit Retail Group       1.9%\n"
                "8. Nexus Technology          1.7%\n"
                "9. Pacific Aerospace         1.5%\n"
                "10. Evergreen Insurance      1.4%\n\n"
                "Top 10 customers represent 24.8% of total revenue (down from 27.1% in Q3 2024), "
                "reflecting improving customer diversification.\n\n"
                "For investor inquiries, contact: ir@companyxyz.com | +1 (415) 555-0142"
            ),
        },
    ]

    for i, page_info in enumerate(pages_content):
        page = doc.new_page(width=W, height=H)

        if page_info.get("custom") == "title_page":
            # Title page layout
            page.insert_text(
                pymupdf.Point(W / 2 - 120, 250),
                "COMPANY XYZ",
                fontsize=36,
                fontname="hebo",
                color=(0.0, 0.15, 0.45),
            )
            page.insert_text(
                pymupdf.Point(W / 2 - 100, 310),
                "Quarterly Report",
                fontsize=24,
                fontname="helv",
                color=(0.2, 0.2, 0.2),
            )
            page.insert_text(
                pymupdf.Point(W / 2 - 55, 360),
                "Q3 2025",
                fontsize=20,
                fontname="helv",
                color=(0.3, 0.3, 0.3),
            )

            # Horizontal rule
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(150, 390), pymupdf.Point(462, 390))
            shape.finish(color=(0.0, 0.15, 0.45), width=2)
            shape.commit()

            page.insert_text(
                pymupdf.Point(W / 2 - 80, 440),
                "July - September 2025",
                fontsize=14,
                fontname="helv",
                color=(0.4, 0.4, 0.4),
            )
            page.insert_text(
                pymupdf.Point(W / 2 - 55, 480),
                "Prepared for Stakeholders",
                fontsize=11,
                fontname="tiit",
                color=(0.5, 0.5, 0.5),
            )
        else:
            # Section title
            if page_info["title"]:
                page.insert_text(
                    pymupdf.Point(LEFT_MARGIN, 60),
                    page_info["title"],
                    fontsize=16,
                    fontname="hebo",
                    color=(0.0, 0.15, 0.45),
                )
                # Underline
                shape = page.new_shape()
                shape.draw_line(
                    pymupdf.Point(LEFT_MARGIN, 66),
                    pymupdf.Point(RIGHT_MARGIN, 66),
                )
                shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
                shape.commit()

            # Body text in textbox
            if page_info["body"]:
                rect = pymupdf.Rect(LEFT_MARGIN, 90, RIGHT_MARGIN, H - 72)
                page.insert_textbox(
                    rect,
                    page_info["body"],
                    fontsize=10,
                    fontname="helv",
                    color=(0.1, 0.1, 0.1),
                    align=pymupdf.TEXT_ALIGN_LEFT,
                )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 22')

    # Open the PDF in evince for the GUI agent
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
