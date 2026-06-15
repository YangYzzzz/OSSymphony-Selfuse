"""
Initial Setup: Create market_analysis.pdf with 10 pages of realistic content
Task ID: pdf_basic_168
Domain: pdf

Creates ~/Desktop/market_analysis.pdf with:
- 10 pages of realistic market analysis content
- Page 3 contains exact text 'market share increased by 12%'
- Page 5 contains exact text 'projected growth rate of 8.5%'
- NO highlights (clean document)
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user/Desktop'
TASK_ID = 'market_analysis'
OUTPUT = f'{WORKDIR}/{TASK_ID}.pdf'


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
    # Ensure Desktop directory exists
    os.makedirs(WORKDIR, exist_ok=True)

    doc = pymupdf.open()

    # Page size: Letter (612 x 792 points)
    W, H = 612, 792
    MARGIN = 72  # 1 inch margin

    # ------------------------------------------------
    # Page 1: Executive Summary
    # ------------------------------------------------
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN, MARGIN + 20), "MARKET ANALYSIS REPORT 2024",
                     fontsize=18, fontname="hebo", color=(0, 0, 0))
    page.insert_text(pymupdf.Point(MARGIN, MARGIN + 50), "Executive Summary",
                     fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.5))

    exec_summary = (
        "This comprehensive market analysis examines key trends and developments across\n"
        "the global technology sector for the fiscal year 2024. Our research team has\n"
        "analyzed data from over 500 companies spanning North America, Europe, and Asia-\n"
        "Pacific regions to deliver actionable insights for strategic decision-making.\n\n"
        "The report covers competitive landscape shifts, consumer behavior changes,\n"
        "emerging market opportunities, and risk factors that may impact business\n"
        "performance in the coming quarters. Key findings indicate strong momentum\n"
        "in cloud computing, artificial intelligence, and cybersecurity verticals.\n\n"
        "Overall market conditions remain favorable despite macroeconomic headwinds\n"
        "including inflationary pressures and supply chain normalization challenges.\n"
        "Companies with diversified revenue streams and strong balance sheets are\n"
        "best positioned to capitalize on emerging opportunities.\n\n"
        "Prepared by: Strategic Research Division\n"
        "Date: March 2024\n"
        "Classification: Confidential - Internal Use Only"
    )
    page.insert_textbox(
        pymupdf.Rect(MARGIN, MARGIN + 80, W - MARGIN, H - MARGIN),
        exec_summary,
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT
    )

    # ------------------------------------------------
    # Page 2: Industry Overview
    # ------------------------------------------------
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN, MARGIN + 20), "Chapter 1: Industry Overview",
                     fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.5))

    overview_text = (
        "The global technology industry continues to demonstrate resilience and adaptability\n"
        "in the face of changing economic conditions. Total market capitalization across\n"
        "major technology indices reached $18.7 trillion by year-end 2024, representing\n"
        "a 9.3% increase from the prior year.\n\n"
        "Key Industry Segments:\n\n"
        "Cloud Infrastructure: The cloud services market expanded significantly with\n"
        "enterprise adoption accelerating across all verticals. Hyperscale providers\n"
        "reported combined revenues exceeding $320 billion for the year, driven by\n"
        "increased workload migrations and AI/ML infrastructure demands.\n\n"
        "Software as a Service (SaaS): The SaaS segment demonstrated strong retention\n"
        "metrics with average net revenue retention rates of 115% among top performers.\n"
        "Vertical SaaS solutions gained particular traction in healthcare, fintech,\n"
        "and manufacturing sectors.\n\n"
        "Semiconductor Industry: Supply chain normalization contributed to improved\n"
        "availability and competitive pricing. Advanced packaging technologies and\n"
        "chiplet architectures gained momentum as alternatives to traditional scaling.\n\n"
        "Regional Performance:\n"
        "North America: +11.2% YoY growth\n"
        "Europe: +7.8% YoY growth\n"
        "Asia-Pacific: +14.5% YoY growth\n"
        "Emerging Markets: +19.3% YoY growth"
    )
    page.insert_textbox(
        pymupdf.Rect(MARGIN, MARGIN + 50, W - MARGIN, H - MARGIN),
        overview_text,
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT
    )

    # ------------------------------------------------
    # Page 3: Competitive Landscape (MUST contain 'market share increased by 12%')
    # ------------------------------------------------
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN, MARGIN + 20), "Chapter 2: Competitive Landscape",
                     fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.5))

    competitive_text = (
        "The competitive dynamics within the technology sector shifted considerably during\n"
        "2024, with established players facing new challenges from well-funded startups\n"
        "and regional competitors targeting niche market opportunities.\n\n"
        "Market Share Analysis:\n\n"
        "Enterprise Software Solutions:\n"
        "Analysis of the enterprise software segment reveals significant consolidation.\n"
        "The top three vendors now collectively control 68% of the addressable market,\n"
        "up from 61% in the previous year. Notably, the category leader reported that\n"
        "its market share increased by 12% following a series of strategic acquisitions\n"
        "and product bundle expansions targeting mid-market customers.\n\n"
        "This growth trajectory was supported by aggressive sales expansion into\n"
        "previously underserved geographic territories and vertical-specific solutions\n"
        "tailored to regulated industries including financial services, healthcare,\n"
        "and government sectors.\n\n"
        "Competitive Positioning Factors:\n"
        "- Product differentiation through AI-powered features\n"
        "- Customer success and retention programs\n"
        "- Partnership ecosystem development\n"
        "- Pricing strategy optimization\n"
        "- Geographic expansion into tier-2 markets\n\n"
        "The battle for developer mindshare continued to intensify, with open-source\n"
        "communities increasingly influencing enterprise purchasing decisions. Vendors\n"
        "with strong developer communities outperformed peers by an average of 23%\n"
        "in net new logo acquisition metrics."
    )
    page.insert_textbox(
        pymupdf.Rect(MARGIN, MARGIN + 50, W - MARGIN, H - MARGIN),
        competitive_text,
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT
    )

    # ------------------------------------------------
    # Page 4: Consumer Behavior Trends
    # ------------------------------------------------
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN, MARGIN + 20), "Chapter 3: Consumer Behavior Trends",
                     fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.5))

    consumer_text = (
        "Consumer behavior in the technology sector continues to evolve rapidly, driven\n"
        "by generational shifts, remote work normalization, and increasing mobile-first\n"
        "consumption patterns across all demographic segments.\n\n"
        "Digital Adoption Metrics:\n\n"
        "The accelerated digital transformation initiated during the pandemic has become\n"
        "permanently embedded in consumer habits. Average daily screen time reached\n"
        "7.4 hours globally, with mobile devices accounting for 58% of all digital\n"
        "interactions. Streaming services, social commerce, and cloud-based productivity\n"
        "tools lead in engagement metrics.\n\n"
        "Subscription Economy:\n"
        "Consumers demonstrate strong preference for subscription models over one-time\n"
        "purchases. Average household subscription count reached 12.3 services per\n"
        "year in developed markets. Churn rates have stabilized at approximately 4.8%\n"
        "monthly for non-premium tiers, while premium services maintained churn below\n"
        "2.1% due to superior feature differentiation and bundling strategies.\n\n"
        "Privacy and Security Awareness:\n"
        "Consumer awareness around data privacy increased significantly. Survey data\n"
        "indicates 73% of consumers now consider privacy policies before downloading\n"
        "applications, compared to 41% in 2021. This trend is driving demand for\n"
        "privacy-first products and transparent data practices.\n\n"
        "Purchase Decision Factors (2024 Survey Results):\n"
        "1. Security features and data protection: 78%\n"
        "2. Ease of use and intuitive design: 74%\n"
        "3. Integration with existing tools: 69%\n"
        "4. Customer support quality: 64%\n"
        "5. Pricing transparency: 61%"
    )
    page.insert_textbox(
        pymupdf.Rect(MARGIN, MARGIN + 50, W - MARGIN, H - MARGIN),
        consumer_text,
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT
    )

    # ------------------------------------------------
    # Page 5: Growth Projections (MUST contain 'projected growth rate of 8.5%')
    # ------------------------------------------------
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN, MARGIN + 20), "Chapter 4: Growth Projections",
                     fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.5))

    growth_text = (
        "Forward-looking analysis based on current macroeconomic conditions, technological\n"
        "development trajectories, and competitive dynamics suggests continued expansion\n"
        "across most technology verticals through 2025 and into 2026.\n\n"
        "Five-Year Market Forecast:\n\n"
        "The overall technology sector maintains a positive long-term outlook. Consensus\n"
        "analyst estimates indicate a projected growth rate of 8.5% compound annual\n"
        "growth rate (CAGR) through 2028, driven primarily by enterprise digital\n"
        "transformation initiatives and emerging market expansion.\n\n"
        "Segment-Specific Projections:\n\n"
        "Artificial Intelligence & Machine Learning:\n"
        "The AI/ML market is forecasted to expand at 34.6% CAGR through 2027,\n"
        "reaching an estimated market size of $890 billion. Enterprise AI adoption\n"
        "is expected to reach 75% penetration among Fortune 500 companies by 2026.\n\n"
        "Cybersecurity:\n"
        "Global cybersecurity spending is projected to exceed $300 billion by 2026,\n"
        "representing a CAGR of 12.8%. Increased regulatory requirements and the\n"
        "proliferation of connected devices are primary demand drivers.\n\n"
        "Cloud Services:\n"
        "Public cloud infrastructure spending is expected to grow at 18.4% CAGR\n"
        "through 2026, with multi-cloud strategies becoming the standard approach\n"
        "for enterprises managing complex, distributed workloads.\n\n"
        "Investment Implications:\n"
        "Companies well-positioned in high-growth segments, particularly those\n"
        "combining AI capabilities with established distribution channels, represent\n"
        "the most compelling investment opportunities in the near to medium term."
    )
    page.insert_textbox(
        pymupdf.Rect(MARGIN, MARGIN + 50, W - MARGIN, H - MARGIN),
        growth_text,
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT
    )

    # ------------------------------------------------
    # Page 6: Risk Factors
    # ------------------------------------------------
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN, MARGIN + 20), "Chapter 5: Risk Factors",
                     fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.5))

    risk_text = (
        "A comprehensive risk assessment is essential for balanced strategic planning.\n"
        "The following risk factors have been identified as most material to technology\n"
        "sector performance over the forecast period.\n\n"
        "Macroeconomic Risks:\n\n"
        "Interest Rate Environment: Elevated interest rates continue to pressure growth\n"
        "company valuations and increase the cost of capital for expansion initiatives.\n"
        "Companies with high leverage ratios face particular vulnerability to sustained\n"
        "high-rate environments.\n\n"
        "Currency Volatility: Multinational technology companies generating significant\n"
        "revenue outside their home currencies face ongoing foreign exchange headwinds.\n"
        "The US dollar strength has reduced reported earnings for many international\n"
        "operations by an estimated 3-5% on average.\n\n"
        "Geopolitical Risks:\n\n"
        "Technology Decoupling: Ongoing US-China technology tensions create supply chain\n"
        "complexity and market access restrictions. Companies with significant China\n"
        "exposure face potential revenue disruption from escalating trade controls.\n\n"
        "Regulatory Landscape: Antitrust scrutiny of major technology platforms has\n"
        "intensified globally. The EU Digital Markets Act and US legislative proposals\n"
        "could fundamentally alter business models for platform companies.\n\n"
        "Technology Risks:\n\n"
        "Cybersecurity Threats: The frequency and sophistication of cyberattacks against\n"
        "technology companies continues to increase. Major breaches can result in\n"
        "significant financial liability, reputational damage, and customer attrition.\n\n"
        "Technical Debt: Legacy system modernization remains a significant challenge\n"
        "for enterprise software vendors. Companies with high technical debt face\n"
        "increasing development costs and competitive disadvantages in feature velocity."
    )
    page.insert_textbox(
        pymupdf.Rect(MARGIN, MARGIN + 50, W - MARGIN, H - MARGIN),
        risk_text,
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT
    )

    # ------------------------------------------------
    # Page 7: Regional Analysis
    # ------------------------------------------------
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN, MARGIN + 20), "Chapter 6: Regional Analysis",
                     fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.5))

    regional_text = (
        "Regional market dynamics vary considerably, reflecting different stages of\n"
        "technology adoption, regulatory environments, and economic development.\n\n"
        "North America:\n\n"
        "The North American market remains the largest and most mature technology\n"
        "market globally, accounting for approximately 38% of total global technology\n"
        "spending. The United States continues to lead in venture capital investment,\n"
        "with $187 billion deployed across technology startups in 2024. Canada and\n"
        "Mexico showed strong growth in nearshore development services.\n\n"
        "Europe:\n\n"
        "European technology markets demonstrated steady growth despite challenging\n"
        "macroeconomic conditions. Germany, France, and the UK collectively represent\n"
        "over 60% of European technology spending. GDPR compliance requirements\n"
        "continue to drive significant investment in data governance platforms and\n"
        "privacy-enhancing technologies.\n\n"
        "Asia-Pacific:\n\n"
        "The Asia-Pacific region continues to demonstrate the highest growth rates\n"
        "globally, driven by rapid digitization in emerging economies and continued\n"
        "technology leadership in established markets. India's technology services\n"
        "sector grew 14.8% in 2024, while Southeast Asian markets collectively\n"
        "attracted $45.2 billion in technology investment.\n\n"
        "China maintains its position as a major technology producer and consumer,\n"
        "though access for foreign technology companies remains constrained by\n"
        "regulatory requirements and competitive domestic alternatives.\n\n"
        "Latin America and Middle East & Africa regions showed emerging market\n"
        "dynamics with above-average growth rates from lower base levels."
    )
    page.insert_textbox(
        pymupdf.Rect(MARGIN, MARGIN + 50, W - MARGIN, H - MARGIN),
        regional_text,
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT
    )

    # ------------------------------------------------
    # Page 8: Investment Landscape
    # ------------------------------------------------
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN, MARGIN + 20), "Chapter 7: Investment Landscape",
                     fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.5))

    investment_text = (
        "The technology investment landscape in 2024 reflected a recalibration of\n"
        "market expectations following the exuberant valuations of 2020-2021. Investors\n"
        "showed increased discipline around profitability metrics and sustainable\n"
        "growth trajectories.\n\n"
        "Venture Capital Activity:\n\n"
        "Global venture capital investment in technology totaled $312 billion in 2024,\n"
        "representing a 7% decline from 2023 but a normalization toward pre-pandemic\n"
        "activity levels. Artificial intelligence startups captured an outsized share\n"
        "of investment activity, receiving approximately 28% of all technology venture\n"
        "funding during the year.\n\n"
        "Late-stage valuations showed signs of stabilization after significant\n"
        "markdowns in 2022-2023. Companies demonstrating strong unit economics and\n"
        "clear paths to profitability commanded premium valuations in funding rounds.\n\n"
        "Public Market Performance:\n\n"
        "Technology sector public market performance exceeded broader market indices\n"
        "by an average of 6.3 percentage points, driven by AI enthusiasm and continued\n"
        "strong fundamental performance from established players. The NASDAQ Composite\n"
        "reached all-time highs multiple times throughout the year.\n\n"
        "M&A Activity:\n\n"
        "Merger and acquisition activity increased significantly, with total deal value\n"
        "reaching $425 billion across 2,847 transactions. Large platform companies\n"
        "pursued tuck-in acquisitions to enhance AI capabilities, while private equity\n"
        "firms targeted mature software businesses with recurring revenue profiles."
    )
    page.insert_textbox(
        pymupdf.Rect(MARGIN, MARGIN + 50, W - MARGIN, H - MARGIN),
        investment_text,
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT
    )

    # ------------------------------------------------
    # Page 9: Strategic Recommendations
    # ------------------------------------------------
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN, MARGIN + 20), "Chapter 8: Strategic Recommendations",
                     fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.5))

    strategy_text = (
        "Based on our comprehensive analysis of market conditions, competitive dynamics,\n"
        "and growth projections, we present the following strategic recommendations\n"
        "for technology companies seeking to maximize value creation.\n\n"
        "Priority Recommendations:\n\n"
        "1. Accelerate AI Integration\n"
        "Companies should prioritize embedding AI capabilities into core products and\n"
        "operational workflows. Organizations that delay AI adoption risk competitive\n"
        "disadvantage as early movers establish learning advantages and customer lock-in.\n\n"
        "2. Focus on Profitable Growth\n"
        "The market environment rewards sustainable, profitable growth over revenue\n"
        "maximization at the expense of margins. Companies should target free cash flow\n"
        "conversion rates of at least 25% while maintaining competitive growth rates.\n\n"
        "3. Strengthen Data Governance\n"
        "Regulatory compliance and customer trust require robust data governance\n"
        "frameworks. Proactive investment in privacy-enhancing technologies positions\n"
        "companies favorably ahead of anticipated regulatory changes.\n\n"
        "4. Diversify Revenue Streams\n"
        "Single-product or single-market dependencies create vulnerability. Companies\n"
        "should develop complementary revenue streams through platform expansion,\n"
        "ecosystem partnerships, and geographic diversification.\n\n"
        "5. Invest in Talent Retention\n"
        "Technical talent remains a critical constraint on growth. Competitive\n"
        "compensation, meaningful work, and clear career development paths are\n"
        "essential for retaining high-performing teams in competitive markets.\n\n"
        "6. Build Resilient Supply Chains\n"
        "Hardware-dependent companies should continue diversifying supplier\n"
        "relationships and building strategic inventory buffers to mitigate disruption."
    )
    page.insert_textbox(
        pymupdf.Rect(MARGIN, MARGIN + 50, W - MARGIN, H - MARGIN),
        strategy_text,
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT
    )

    # ------------------------------------------------
    # Page 10: Appendix and Conclusion
    # ------------------------------------------------
    page = doc.new_page(width=W, height=H)
    page.insert_text(pymupdf.Point(MARGIN, MARGIN + 20), "Appendix & Conclusion",
                     fontsize=14, fontname="hebo", color=(0.1, 0.1, 0.5))

    appendix_text = (
        "Conclusion:\n\n"
        "The technology sector enters 2025 with strong fundamentals and several\n"
        "powerful secular growth tailwinds, including AI adoption, continued cloud\n"
        "migration, and digital transformation of traditional industries. While near-\n"
        "term macroeconomic uncertainties and geopolitical risks warrant careful\n"
        "monitoring, the long-term investment thesis for quality technology companies\n"
        "remains compelling.\n\n"
        "Companies that successfully navigate the transition to AI-augmented products\n"
        "and services while maintaining financial discipline will be best positioned\n"
        "to deliver superior returns to stakeholders over the forecast period.\n\n"
        "Appendix A: Data Sources\n\n"
        "Primary data sources for this report include:\n"
        "- IDC Global Technology Market Research Database\n"
        "- Gartner Magic Quadrant and Market Data Reports\n"
        "- Bloomberg Technology Sector Analytics\n"
        "- Company Annual Reports and Earnings Call Transcripts\n"
        "- Federal Reserve Economic Data (FRED)\n"
        "- World Bank Technology Indicators\n"
        "- Internal Survey Data (n=2,847 technology decision-makers)\n\n"
        "Appendix B: Methodology\n\n"
        "Market size estimates are based on bottom-up analysis combining publicly\n"
        "available data with proprietary survey results. Growth projections use\n"
        "consensus analyst estimates weighted by firm coverage and historical accuracy.\n"
        "Regional allocations are derived from trade association data and company\n"
        "geographic revenue disclosures.\n\n"
        "Disclaimer: This report is intended for informational purposes only and\n"
        "does not constitute investment advice. Past performance is not indicative\n"
        "of future results."
    )
    page.insert_textbox(
        pymupdf.Rect(MARGIN, MARGIN + 50, W - MARGIN, H - MARGIN),
        appendix_text,
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_LEFT
    )

    # Save
    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 10')

    # GUI-ready startup: open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
