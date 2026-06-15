"""
Initial Setup: Create a 24-page PDF presentation with 3 embedded fonts
Task ID: pdf_mbc_033
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
TASK_ID = 'pdf_mbc_033'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/presentation.pdf'

# Page dimensions: Letter size
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


def create_initial():
    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Set metadata to look realistic
    doc.set_metadata({
        "title": "Q4 2025 Strategic Planning Presentation",
        "author": "Elena Vasquez",
        "subject": "Corporate Strategy and Financial Outlook",
        "keywords": "strategy, planning, Q4, 2025, forecast",
        "creator": "Microsoft PowerPoint",
        "producer": "Microsoft PDF Converter",
    })

    # Register three external fonts to ensure they are embedded:
    # Arial (sans-serif), Times New Roman (serif), Courier (monospace)
    # On the VM, these fonts should be available via truetype paths.
    # We'll use DejaVu as fallback mappings but label them accordingly.

    # We'll use the built-in fonts that correspond to the three families
    # and also register actual TrueType fonts to embed them.
    # Built-in: helv (Helvetica/Arial-like), tiro (Times Roman), cour (Courier)

    # For proper embedding, we use Font objects from TrueType files
    font_paths = {
        'arial': [
            '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            '/usr/share/fonts/truetype/freefont/FreeSans.ttf',
        ],
        'times': [
            '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',
            '/usr/share/fonts/truetype/freefont/FreeSerif.ttf',
        ],
        'courier': [
            '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
            '/usr/share/fonts/truetype/freefont/FreeMono.ttf',
        ],
    }

    def find_font(paths):
        for p in paths:
            if os.path.exists(p):
                return p
        return None

    arial_path = find_font(font_paths['arial'])
    times_path = find_font(font_paths['times'])
    courier_path = find_font(font_paths['courier'])

    # Slide content for a realistic 24-page presentation
    slides = [
        {
            "title": "Q4 2025 Strategic Planning",
            "subtitle": "Prepared by Elena Vasquez, VP of Strategy",
            "body": "Meridian Global Solutions Inc.\nConfidential - Internal Use Only",
        },
        {
            "title": "Agenda",
            "body": "1. Executive Summary\n2. Market Analysis\n3. Financial Performance\n4. Product Roadmap\n5. Competitive Landscape\n6. Risk Assessment\n7. Talent Strategy\n8. Technology Infrastructure\n9. Customer Insights\n10. Q1 2026 Objectives",
        },
        {
            "title": "Executive Summary",
            "body": "Revenue grew 18.3% year-over-year reaching $247M in Q3 2025.\nOperating margin improved to 22.7% from 19.4% in Q3 2024.\nCustomer acquisition cost decreased by 14% through optimized digital channels.\nEmployee retention rate stands at 94.2%, above industry benchmark of 88%.",
        },
        {
            "title": "Market Overview",
            "body": "Total addressable market expanded to $12.8B in 2025.\nOur market share increased from 6.2% to 7.8% over the past 12 months.\nKey growth sectors: Healthcare IT (+24%), FinTech (+19%), EdTech (+15%).\nEmerging opportunities in Southeast Asia and Latin America.",
        },
        {
            "title": "Revenue Breakdown by Segment",
            "body": "Enterprise Solutions: $142M (57.5%) - up 21% YoY\nSMB Platform: $58M (23.5%) - up 14% YoY\nProfessional Services: $32M (12.9%) - up 11% YoY\nLicensing & Partnerships: $15M (6.1%) - up 28% YoY\n\nTotal Revenue: $247M",
        },
        {
            "title": "Quarterly Financial Trends",
            "body": "Q1 2025: $218M revenue, 20.1% margin\nQ2 2025: $231M revenue, 21.5% margin\nQ3 2025: $247M revenue, 22.7% margin\nQ4 2025 Forecast: $263M revenue, 23.4% margin\n\nFull Year 2025 Projection: $959M",
        },
        {
            "title": "Cost Structure Analysis",
            "body": "R&D Investment: $48.2M (19.5% of revenue)\nSales & Marketing: $39.5M (16.0% of revenue)\nGeneral & Administrative: $22.2M (9.0% of revenue)\nInfrastructure & Operations: $18.5M (7.5% of revenue)\nCustomer Support: $12.4M (5.0% of revenue)",
        },
        {
            "title": "Product Roadmap - Current Quarter",
            "body": "Atlas Platform v3.2 - Enhanced AI-driven analytics dashboard\nNexus Integration Hub - 15 new third-party connectors\nGuardian Security Suite - Zero-trust architecture implementation\nPulse Customer Intelligence - Real-time sentiment analysis\n\nAll releases scheduled for November 2025.",
        },
        {
            "title": "Product Roadmap - 2026 Vision",
            "body": "Q1: Atlas Platform v4.0 with predictive modeling\nQ2: Mobile-first experience redesign\nQ3: Edge computing capabilities for IoT verticals\nQ4: Autonomous workflow engine powered by LLM integration\n\nTotal R&D budget allocated: $52M for FY2026.",
        },
        {
            "title": "Competitive Landscape",
            "body": "Primary Competitors:\n- Apex Technologies (12.3% market share)\n- Pinnacle Systems (9.1% market share)\n- Meridian Global (7.8% market share)\n- Vertex Solutions (5.4% market share)\n\nOur differentiator: End-to-end integration with 340+ enterprise tools.",
        },
        {
            "title": "Competitive SWOT Analysis",
            "body": "Strengths: Deep vertical expertise, strong customer NPS (72)\nWeaknesses: Limited presence in APAC region\nOpportunities: AI/ML market growing 35% annually\nThreats: Large cloud providers bundling competing features\n\nStrategic response: Accelerate vertical specialization.",
        },
        {
            "title": "Customer Metrics Dashboard",
            "body": "Active Enterprise Clients: 1,247 (up from 1,089)\nMonthly Active Users: 328,000 (up 24% QoQ)\nNet Promoter Score: 72 (industry avg: 54)\nCustomer Churn Rate: 3.8% (down from 5.1%)\nAverage Contract Value: $198,000 (up 12%)",
        },
        {
            "title": "Customer Success Stories",
            "body": "Global Health Corp: Reduced operational costs by 34% using Atlas Platform\nFirst National Bank: Achieved 99.97% uptime with Guardian Suite\nEduBridge Academy: Scaled to 2M students with Nexus Integration\nGreenPath Energy: Automated 78% of compliance reporting\n\nCombined customer ROI: 340% average over 18 months.",
        },
        {
            "title": "Risk Assessment Matrix",
            "body": "High Impact / High Probability:\n- Regulatory changes in data privacy (GDPR expansion)\n- Supply chain disruptions affecting hardware partnerships\n\nHigh Impact / Low Probability:\n- Major security breach\n- Key talent departure in leadership\n\nMitigation budget: $8.5M allocated for FY2026.",
        },
        {
            "title": "Talent Strategy Overview",
            "body": "Current Headcount: 2,847 employees across 14 offices\nOpen Positions: 186 (primarily Engineering and Sales)\nDiversity Metrics: 42% women in leadership (up from 37%)\nAverage Tenure: 4.2 years\n\nKey Initiative: Launch Meridian Technical Academy in Q1 2026.",
        },
        {
            "title": "Engineering Team Expansion",
            "body": "Current: 1,124 engineers (39.5% of company)\nTarget by Q2 2026: 1,350 engineers\nFocus Areas:\n- Machine Learning Engineers: +45 headcount\n- Platform Security: +30 headcount\n- Mobile Development: +25 headcount\n- DevOps/SRE: +20 headcount\n\nRecruiting budget increase: 22% YoY.",
        },
        {
            "title": "Technology Infrastructure",
            "body": "Cloud Spend: $14.2M/quarter (multi-cloud: AWS 60%, Azure 30%, GCP 10%)\nUptime SLA Achievement: 99.95% (target: 99.9%)\nAverage API Response Time: 142ms (down from 198ms)\nData Processed: 4.7 PB/month\nSecurity Incidents: 0 critical, 3 medium in Q3 2025.",
        },
        {
            "title": "Digital Transformation Initiatives",
            "body": "1. AI-Powered Customer Support - 45% ticket deflection achieved\n2. Automated Testing Pipeline - 92% code coverage\n3. Real-Time Data Lake - Processing 15M events/hour\n4. Edge Computing Pilot - 3 enterprise clients onboarded\n5. Blockchain-based Audit Trail - SOC2 compliance accelerated",
        },
        {
            "title": "Marketing & Brand Strategy",
            "body": "Brand Awareness: 67% in target segments (up 12 pts YoY)\nDigital Marketing ROI: 4.2x (up from 3.1x)\nContent Marketing: 450 articles, 28 whitepapers published\nEvent Sponsorships: 12 major conferences in 2025\nSocial Media Following: 285K across platforms (up 38%)",
        },
        {
            "title": "Partnership Ecosystem",
            "body": "Technology Partners: 48 active integrations\nChannel Partners: 127 resellers across 32 countries\nStrategic Alliances: Microsoft, Salesforce, ServiceNow\n\nPartner-Sourced Revenue: $37M (15% of total)\nPartner Satisfaction Score: 8.4/10\n\nNew Partnership Target for 2026: 25 additional partners.",
        },
        {
            "title": "Sustainability & ESG Report",
            "body": "Carbon Footprint: Reduced by 28% vs 2023 baseline\nRenewable Energy: 85% of office operations powered by renewables\nDiversity & Inclusion: Published first annual D&I report\nCommunity Investment: $2.1M in STEM education programs\nGovernance: Independent board audit committee established",
        },
        {
            "title": "Q1 2026 Key Objectives",
            "body": "1. Achieve $270M quarterly revenue target\n2. Launch Atlas Platform v4.0\n3. Expand into Japanese market with local team\n4. Complete SOC2 Type II certification\n5. Hire 120 engineers across all disciplines\n6. Reduce customer onboarding time by 30%\n7. Establish AI Center of Excellence",
        },
        {
            "title": "Budget Allocation - FY2026",
            "body": "Total Budget: $385M\n\nR&D: $52M (13.5%)\nSales & Marketing: $68M (17.7%)\nOperations: $42M (10.9%)\nG&A: $38M (9.9%)\nCapital Expenditure: $28M (7.3%)\nStrategic Reserves: $15M (3.9%)\n\nProjected Revenue: $1.12B (+17% YoY)",
        },
        {
            "title": "Thank You & Next Steps",
            "subtitle": "Questions & Discussion",
            "body": "Elena Vasquez - elena.vasquez@meridianglobal.com\nMarco Delgado - marco.delgado@meridianglobal.com\nSarah Chen - sarah.chen@meridianglobal.com\n\nNext Board Review: January 15, 2026\nStrategy Finalization Deadline: December 20, 2025",
        },
    ]

    for i, slide in enumerate(slides):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)

        # Use different fonts on different sections to ensure all 3 are embedded

        # Title - use Arial (sans-serif) font
        if arial_path:
            font_arial = pymupdf.Font(fontfile=arial_path)
            tw = pymupdf.TextWriter(page.rect)
            tw.append(pymupdf.Point(50, 60), slide["title"], font=font_arial, fontsize=24)
            tw.write_text(page, color=(0.1, 0.1, 0.4))
        else:
            page.insert_text(pymupdf.Point(50, 60), slide["title"],
                             fontsize=24, fontname="helv", color=(0.1, 0.1, 0.4))

        # Subtitle if present - use Times New Roman (serif) font
        if "subtitle" in slide:
            if times_path:
                font_times = pymupdf.Font(fontfile=times_path)
                tw = pymupdf.TextWriter(page.rect)
                tw.append(pymupdf.Point(50, 95), slide["subtitle"], font=font_times, fontsize=14)
                tw.write_text(page, color=(0.3, 0.3, 0.3))
            else:
                page.insert_text(pymupdf.Point(50, 95), slide["subtitle"],
                                 fontsize=14, fontname="tiro", color=(0.3, 0.3, 0.3))

        # Horizontal rule under title
        shape = page.new_shape()
        y_rule = 110 if "subtitle" not in slide else 115
        shape.draw_line(pymupdf.Point(50, y_rule), pymupdf.Point(562, y_rule))
        shape.finish(color=(0.2, 0.3, 0.6), width=1.5)
        shape.commit()

        # Body text - use Courier (monospace) font for data/numbers feel
        body_y = y_rule + 30
        body_lines = slide["body"].split("\n")
        for line in body_lines:
            if body_y > PAGE_H - 80:
                break
            if courier_path:
                font_courier = pymupdf.Font(fontfile=courier_path)
                tw = pymupdf.TextWriter(page.rect)
                tw.append(pymupdf.Point(50, body_y), line, font=font_courier, fontsize=11)
                tw.write_text(page, color=(0.15, 0.15, 0.15))
            else:
                page.insert_text(pymupdf.Point(50, body_y), line,
                                 fontsize=11, fontname="cour", color=(0.15, 0.15, 0.15))
            body_y += 20

        # Page number at bottom - use Arial
        page_num_text = f"Slide {i + 1} of 24"
        if arial_path:
            font_arial = pymupdf.Font(fontfile=arial_path)
            tw = pymupdf.TextWriter(page.rect)
            tw.append(pymupdf.Point(270, PAGE_H - 30), page_num_text, font=font_arial, fontsize=9)
            tw.write_text(page, color=(0.5, 0.5, 0.5))
        else:
            page.insert_text(pymupdf.Point(270, PAGE_H - 30), page_num_text,
                             fontsize=9, fontname="helv", color=(0.5, 0.5, 0.5))

        # Footer line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(50, PAGE_H - 45), pymupdf.Point(562, PAGE_H - 45))
        shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
        shape.commit()

    # Save as PDF 1.6 using pikepdf to set the version explicitly
    temp_path = f'{DOCS_DIR}/presentation_temp.pdf'
    doc.save(temp_path)
    doc.close()

    # Use pikepdf to set PDF version to 1.6
    import pikepdf
    pdf = pikepdf.open(temp_path)
    # pikepdf saves with the version we specify
    pdf.save(OUTPUT, min_version='1.6')
    pdf.close()

    # Clean up temp
    os.remove(temp_path)

    print(f'Initial file created: {OUTPUT}')

    # Verify the file
    doc = pymupdf.open(OUTPUT)
    print(f'Page count: {doc.page_count}')
    fonts_on_page0 = doc[0].get_fonts()
    print(f'Fonts on page 0: {fonts_on_page0}')

    # Check all unique fonts across the document
    all_fonts = set()
    for pg in doc:
        for f in pg.get_fonts():
            all_fonts.add(f[3])  # basefont name
    print(f'All embedded fonts: {all_fonts}')
    doc.close()

    # Make sure okular_props.txt does NOT exist (negative constraint)
    props_file = f'{DOCS_DIR}/okular_props.txt'
    if os.path.exists(props_file):
        os.remove(props_file)

    # GUI-ready startup: open PDF in a viewer
    # Task says Okular but it may not be installed; try okular first, fall back to evince
    import shutil as _shutil
    if _shutil.which('okular'):
        launch_gui(f'okular "{OUTPUT}"', delay_sec=2.0)
        print('GUI_READY: launched Okular with DISPLAY=:0')
    else:
        launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
        print('GUI_READY: launched Evince (okular not found) with DISPLAY=:0')


create_initial()
