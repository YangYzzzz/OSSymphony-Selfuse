"""
Initial Setup: Create market_analysis.pdf (10-page market analysis report)
Task ID: pdf_cross_079
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_cross_079'
OUTPUT_PDF = f'{WORKDIR}/Documents/market_analysis.pdf'

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
    import pymupdf
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.colors import HexColor, black, white, grey
    from reportlab.lib.units import inch
    from reportlab.graphics.shapes import Drawing, Rect, String, Line, Group
    from reportlab.graphics import renderPDF
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.graphics.widgets.markers import makeMarker
    import io

    # Ensure Documents directory exists
    os.makedirs(f'{WORKDIR}/Documents', exist_ok=True)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=22,
                                  textColor=HexColor('#003366'), spaceAfter=12)
    heading1_style = ParagraphStyle('Heading1', parent=styles['Heading1'], fontSize=16,
                                    textColor=HexColor('#003366'), spaceAfter=8)
    heading2_style = ParagraphStyle('Heading2', parent=styles['Heading2'], fontSize=13,
                                    textColor=HexColor('#005599'), spaceAfter=6)
    normal_style = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=11,
                                   spaceAfter=6, leading=15)
    caption_style = ParagraphStyle('Caption', parent=styles['Normal'], fontSize=9,
                                    textColor=HexColor('#555555'), alignment=1, spaceAfter=10)

    story = []

    # ---- PAGE 1: Title / Executive Summary ----
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("Global Technology Market Analysis Report 2025", title_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Prepared by: Strategic Intelligence Division", normal_style))
    story.append(Paragraph("Date: January 2025 | Confidential", normal_style))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("Executive Summary", heading1_style))
    story.append(Paragraph(
        "This report presents a comprehensive analysis of the global technology market "
        "landscape for the fiscal year 2025. The analysis covers market share distribution, "
        "revenue growth trends, regional performance, and competitive positioning among "
        "major industry players. Key findings indicate a significant shift in market "
        "dynamics, with emerging players disrupting traditional market leaders.",
        normal_style))
    story.append(Paragraph(
        "Total addressable market (TAM) has grown to an estimated $3.7 trillion, "
        "representing a 14.2% year-over-year increase. Cloud infrastructure and AI-driven "
        "services continue to be the primary growth drivers, while hardware margins face "
        "compression due to supply chain normalization.",
        normal_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Key Highlights", heading2_style))
    highlights = [
        ["Metric", "2024", "2025", "YoY Change"],
        ["Total Market Size", "$3.24T", "$3.70T", "+14.2%"],
        ["Cloud Revenue", "$680B", "$812B", "+19.4%"],
        ["AI Services Revenue", "$210B", "$340B", "+61.9%"],
        ["Hardware Revenue", "$1.12T", "$1.18T", "+5.4%"],
        ["Software Licenses", "$890B", "$960B", "+7.9%"],
    ]
    t = Table(highlights, colWidths=[160, 80, 80, 90])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#EEF2FF')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(PageBreak())

    # ---- PAGE 2: Market Overview ----
    story.append(Paragraph("Chapter 1: Market Overview", heading1_style))
    story.append(Paragraph(
        "The global technology sector in 2025 is characterized by accelerating digital "
        "transformation across all major industries. Enterprise spending on technology "
        "solutions reached an all-time high, driven by competitive pressures to adopt "
        "AI, automation, and cloud-native architectures.",
        normal_style))
    story.append(Paragraph(
        "North America remains the largest regional market, accounting for 38% of global "
        "technology spending. Asia-Pacific continues its rapid expansion, now representing "
        "31% of the market — up from 27% in 2022. Europe holds 22%, while Latin America, "
        "the Middle East, and Africa collectively account for the remaining 9%.",
        normal_style))
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("1.1 Sector Breakdown", heading2_style))
    sector_data = [
        ["Sector", "Revenue ($B)", "Growth Rate", "Market Share"],
        ["Cloud Infrastructure", "$812", "+19.4%", "22.0%"],
        ["Enterprise Software", "$680", "+11.2%", "18.4%"],
        ["Hardware & Devices", "$1,180", "+5.4%", "31.9%"],
        ["IT Services", "$520", "+8.7%", "14.1%"],
        ["AI & Analytics", "$340", "+61.9%", "9.2%"],
        ["Cybersecurity", "$168", "+18.3%", "4.5%"],
    ]
    st = Table(sector_data, colWidths=[160, 90, 90, 80])
    st.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#005599')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#EEF5FF')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(st)
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(
        "Cloud infrastructure growth is primarily fueled by enterprise migration from "
        "legacy on-premise systems. The hyperscaler segment — dominated by three major "
        "providers — continues to capture over 65% of new enterprise workloads. "
        "Meanwhile, specialized vertical cloud providers are gaining traction in regulated "
        "industries such as healthcare, finance, and government.",
        normal_style))
    story.append(PageBreak())

    # ---- PAGE 3: Competitive Landscape ----
    story.append(Paragraph("Chapter 2: Competitive Landscape", heading1_style))
    story.append(Paragraph(
        "The competitive dynamics of the global technology market are evolving rapidly. "
        "Traditional incumbents face pressure from agile startups and platform companies "
        "expanding into adjacent markets. Strategic acquisitions, partnerships, and "
        "organic R&D investment are the primary tools for maintaining competitive positioning.",
        normal_style))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("2.1 Competitor Profiles", heading2_style))
    profiles = [
        ("TechCorp", "32%",
         "TechCorp leads the enterprise software and cloud infrastructure segment. "
         "Recent acquisitions in AI tooling have strengthened their competitive moat. "
         "2025 revenue projected at $1.18T with expanding margins due to SaaS mix shift."),
        ("DataSystems Inc", "24%",
         "DataSystems holds strong positioning in data management and analytics. "
         "Their recent pivot to AI-augmented BI tools has driven a 31% increase in "
         "net new customer acquisition. Primary competition comes from TechCorp."),
        ("CloudWave", "18%",
         "CloudWave's pure-play cloud model has attracted mid-market enterprises "
         "seeking cloud-native alternatives. Their developer ecosystem and marketplace "
         "strategy is proving effective in reducing churn and increasing ARPU."),
        ("NetVision", "12%",
         "NetVision specializes in networking infrastructure and edge computing. "
         "The rise of IoT and 5G deployment has created favorable tailwinds for "
         "their product portfolio. Margin improvement is a key focus for 2025."),
        ("AppForge", "9%",
         "AppForge targets the SMB segment with affordable, integrated business "
         "software suites. Their low-code/no-code platform is the fastest growing "
         "product line, attracting developers and business users alike."),
        ("InnoBase", "5%",
         "InnoBase is a challenger player focused on open-source enterprise solutions. "
         "While market share remains modest, their community-driven development model "
         "is gaining recognition among technically sophisticated buyers."),
    ]
    for company, share, desc in profiles:
        story.append(Paragraph(f"<b>{company}</b> — Market Share: {share}", normal_style))
        story.append(Paragraph(desc, normal_style))
        story.append(Spacer(1, 0.05 * inch))
    story.append(PageBreak())

    # ---- PAGE 4: Market Share Chart (Bar Chart) ----
    story.append(Paragraph("Chapter 3: Market Share Analysis", heading1_style))
    story.append(Paragraph(
        "Figure 3 below illustrates the market share distribution among the six major "
        "technology companies as of Q4 2025. TechCorp maintains a commanding lead with "
        "32% market share, well ahead of nearest competitor DataSystems Inc at 24%.",
        normal_style))
    story.append(Spacer(1, 0.15 * inch))

    # Build a proper bar chart using reportlab graphics
    drawing = Drawing(400, 220)

    # Background rectangle
    bg = Rect(40, 30, 340, 170, fillColor=HexColor('#F8FAFF'), strokeColor=HexColor('#CCCCCC'), strokeWidth=0.5)
    drawing.add(bg)

    # Bar chart data
    companies = ['TechCorp', 'DataSys', 'CloudWave', 'NetVision', 'AppForge', 'InnoBase']
    shares = [32, 24, 18, 12, 9, 5]
    bar_colors = [
        HexColor('#1A56DB'),  # TechCorp — blue (tallest, 32%)
        HexColor('#3B82F6'),
        HexColor('#60A5FA'),
        HexColor('#93C5FD'),
        HexColor('#BFDBFE'),
        HexColor('#DBEAFE'),
    ]

    # Draw y-axis gridlines and labels
    max_val = 35
    y_ticks = [0, 5, 10, 15, 20, 25, 30, 35]
    chart_left = 55
    chart_bottom = 45
    chart_width = 305
    chart_height = 140

    for tick in y_ticks:
        y = chart_bottom + (tick / max_val) * chart_height
        # Gridline
        gl = Line(chart_left, y, chart_left + chart_width, y,
                  strokeColor=HexColor('#DDDDDD') if tick > 0 else HexColor('#888888'),
                  strokeWidth=0.5 if tick > 0 else 1)
        drawing.add(gl)
        # Label
        lbl = String(chart_left - 5, y - 4, f'{tick}%',
                     fontSize=7, fillColor=HexColor('#555555'),
                     textAnchor='end')
        drawing.add(lbl)

    # Draw y-axis line
    yaxis = Line(chart_left, chart_bottom, chart_left, chart_bottom + chart_height,
                 strokeColor=HexColor('#888888'), strokeWidth=1)
    drawing.add(yaxis)

    # Draw bars
    bar_width = chart_width / len(companies)
    bar_inner_width = bar_width * 0.6

    for i, (company, share) in enumerate(zip(companies, shares)):
        bar_h = (share / max_val) * chart_height
        bar_x = chart_left + i * bar_width + (bar_width - bar_inner_width) / 2
        bar_y = chart_bottom

        bar_rect = Rect(bar_x, bar_y, bar_inner_width, bar_h,
                        fillColor=bar_colors[i],
                        strokeColor=HexColor('#0A3A8A') if i == 0 else bar_colors[i],
                        strokeWidth=0.5)
        drawing.add(bar_rect)

        # Value label on top of bar
        val_lbl = String(bar_x + bar_inner_width / 2, bar_y + bar_h + 3,
                         f'{share}%',
                         fontSize=7.5,
                         fillColor=HexColor('#1A1A1A'),
                         textAnchor='middle')
        drawing.add(val_lbl)

        # X-axis company label
        x_lbl = String(bar_x + bar_inner_width / 2, chart_bottom - 12,
                       company,
                       fontSize=7,
                       fillColor=HexColor('#333333'),
                       textAnchor='middle')
        drawing.add(x_lbl)

    # X-axis line
    xaxis = Line(chart_left, chart_bottom, chart_left + chart_width, chart_bottom,
                 strokeColor=HexColor('#888888'), strokeWidth=1)
    drawing.add(xaxis)

    # Chart title
    chart_title = String(200, 210, 'Market Share by Company (%) — Q4 2025',
                         fontSize=10,
                         fillColor=HexColor('#003366'),
                         textAnchor='middle')
    drawing.add(chart_title)

    # Y-axis title (rotated simulation with label)
    yaxis_title = String(8, chart_bottom + chart_height / 2, 'Market Share (%)',
                         fontSize=8,
                         fillColor=HexColor('#555555'),
                         textAnchor='middle')
    drawing.add(yaxis_title)

    story.append(drawing)
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(
        "Figure 3: Market Share Distribution Among Major Technology Companies, Q4 2025. "
        "TechCorp leads with 32%, followed by DataSystems Inc (24%) and CloudWave (18%).",
        caption_style))
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph(
        "TechCorp's market dominance is reinforced by their enterprise software lock-in, "
        "extensive partner ecosystem, and continued investment in platform capabilities. "
        "DataSystems Inc has shown the most significant improvement, gaining 3 percentage "
        "points year-over-year through successful upsell motion and new product launches.",
        normal_style))
    story.append(PageBreak())

    # ---- PAGE 5: Revenue Trends ----
    story.append(Paragraph("Chapter 4: Revenue Growth Trends", heading1_style))
    story.append(Paragraph(
        "Revenue growth across the technology sector has been uneven, with AI-driven "
        "product lines outperforming traditional software and hardware categories by a "
        "significant margin. Companies that have successfully integrated generative AI "
        "into their core products report an average 45% uplift in new deal value.",
        normal_style))
    rev_trend = [
        ["Company", "Q1 2025 ($B)", "Q2 2025 ($B)", "Q3 2025 ($B)", "Q4 2025 ($B)"],
        ["TechCorp", "287", "301", "294", "298"],
        ["DataSystems Inc", "201", "218", "224", "231"],
        ["CloudWave", "145", "159", "163", "170"],
        ["NetVision", "98", "103", "107", "112"],
        ["AppForge", "72", "79", "84", "89"],
        ["InnoBase", "38", "43", "46", "49"],
    ]
    rt = Table(rev_trend, colWidths=[130, 80, 80, 80, 80])
    rt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#EEF2FF')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(rt)
    story.append(PageBreak())

    # ---- PAGE 6: Regional Analysis ----
    story.append(Paragraph("Chapter 5: Regional Market Analysis", heading1_style))
    story.append(Paragraph(
        "Regional dynamics play an increasingly critical role in technology market strategy. "
        "The shift toward data sovereignty requirements and regional cloud regulations has "
        "created opportunities for localized service providers while adding compliance "
        "complexity for global enterprises.",
        normal_style))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("5.1 North America", heading2_style))
    story.append(Paragraph(
        "North America generated $1.41 trillion in technology spending in 2025, representing "
        "38% of the global market. The U.S. enterprise sector continues to be the primary "
        "driver, with federal government modernization initiatives adding approximately "
        "$85 billion in incremental demand. Canadian technology adoption is accelerating "
        "particularly in fintech and cleantech sectors.",
        normal_style))
    story.append(Paragraph("5.2 Asia-Pacific", heading2_style))
    story.append(Paragraph(
        "Asia-Pacific reached $1.15 trillion in 2025, growing at 21% year-over-year — "
        "the fastest regional growth rate globally. China's domestic technology ecosystem "
        "is increasingly self-sufficient, with domestic players now capturing 78% of local "
        "spending. India is emerging as a major technology services exporter and a "
        "significant consumer market for SaaS applications.",
        normal_style))
    story.append(Paragraph("5.3 Europe", heading2_style))
    story.append(Paragraph(
        "European technology spending totaled $814 billion in 2025. GDPR compliance and "
        "the EU AI Act have created significant demand for privacy-preserving and "
        "auditable AI solutions. Germany and France lead enterprise AI adoption, while "
        "the Nordic countries maintain their position as leaders in sustainable technology.",
        normal_style))
    story.append(PageBreak())

    # ---- PAGE 7: AI Trends ----
    story.append(Paragraph("Chapter 6: Artificial Intelligence Trends", heading1_style))
    story.append(Paragraph(
        "Artificial intelligence has transitioned from experimental to mission-critical "
        "in enterprise technology stacks. The AI services market reached $340 billion in "
        "2025, growing 62% year-over-year. Generative AI applications — including code "
        "generation, document processing, and customer interaction — account for 41% of "
        "total AI investment.",
        normal_style))
    ai_data = [
        ["AI Application", "2024 Revenue", "2025 Revenue", "Growth"],
        ["Generative AI", "$84B", "$139B", "+65.5%"],
        ["Computer Vision", "$52B", "$68B", "+30.8%"],
        ["NLP & Conversational AI", "$48B", "$72B", "+50.0%"],
        ["Predictive Analytics", "$36B", "$44B", "+22.2%"],
        ["Autonomous Systems", "$22B", "$34B", "+54.5%"],
        ["Recommendation Engines", "$18B", "$23B", "+27.8%"],
    ]
    ait = Table(ai_data, colWidths=[160, 90, 90, 80])
    ait.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#4A148C')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#F3E5F5')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(ait)
    story.append(PageBreak())

    # ---- PAGE 8: Investment and M&A ----
    story.append(Paragraph("Chapter 7: Investment and M&A Activity", heading1_style))
    story.append(Paragraph(
        "Mergers and acquisitions in the technology sector reached a record $680 billion "
        "in 2025, driven by strategic consolidation in AI capabilities, cybersecurity, "
        "and cloud-native software. Private equity continues to play an outsized role, "
        "with technology-focused PE funds deploying $230 billion during the year.",
        normal_style))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Notable Transactions 2025", heading2_style))
    ma_data = [
        ["Acquirer", "Target", "Value ($B)", "Segment"],
        ["TechCorp", "AIMatrix Labs", "$34.2", "AI Infrastructure"],
        ["DataSystems Inc", "CloudAnalytics Co", "$18.7", "Analytics SaaS"],
        ["CloudWave", "SecureEdge Inc", "$12.1", "Cybersecurity"],
        ["NetVision", "EdgeCompute Pro", "$8.9", "Edge Computing"],
        ["AppForge", "WorkflowAI", "$5.4", "Process Automation"],
    ]
    mat = Table(ma_data, colWidths=[120, 130, 80, 120])
    mat.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#EEF2FF')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(mat)
    story.append(PageBreak())

    # ---- PAGE 9: Risks and Challenges ----
    story.append(Paragraph("Chapter 8: Risks and Challenges", heading1_style))
    story.append(Paragraph(
        "Despite strong overall growth, the technology sector faces a number of material "
        "risks that could impact performance and market dynamics in 2025 and beyond.",
        normal_style))
    risks = [
        ("Regulatory Risk",
         "Increasing government scrutiny of large technology platforms, AI regulations, "
         "and data privacy laws across multiple jurisdictions create compliance overhead "
         "and potential market access restrictions for global companies."),
        ("Geopolitical Risk",
         "Technology supply chain dependencies and export control restrictions continue "
         "to affect semiconductor availability and cross-border data flows. Companies "
         "with significant China exposure face particular uncertainty."),
        ("Talent Risk",
         "Demand for AI, cloud, and cybersecurity talent significantly exceeds supply. "
         "Wage inflation and retention challenges are increasing operating costs, "
         "particularly for smaller technology companies."),
        ("Cybersecurity Risk",
         "As digital attack surfaces expand, the frequency and sophistication of "
         "cyberattacks are increasing. State-sponsored threats and ransomware attacks "
         "represent material operational and reputational risks."),
        ("Valuation Risk",
         "High valuations in the AI segment may not be sustainable if revenue growth "
         "fails to meet market expectations. A correction in AI valuations could "
         "reduce access to capital for early-stage companies."),
    ]
    for risk_name, risk_desc in risks:
        story.append(Paragraph(f"<b>{risk_name}</b>", normal_style))
        story.append(Paragraph(risk_desc, normal_style))
        story.append(Spacer(1, 0.05 * inch))
    story.append(PageBreak())

    # ---- PAGE 10: Conclusion and Outlook ----
    story.append(Paragraph("Chapter 9: Conclusion and 2026 Outlook", heading1_style))
    story.append(Paragraph(
        "The global technology market in 2025 has demonstrated remarkable resilience "
        "and adaptability. While macroeconomic headwinds have moderated growth in some "
        "segments, structural tailwinds from AI adoption, cloud migration, and digital "
        "transformation remain powerful drivers of long-term demand.",
        normal_style))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("2026 Projections", heading2_style))
    proj_data = [
        ["Category", "2025 Actual", "2026 Projected", "Growth"],
        ["Total Market", "$3.70T", "$4.18T", "+13.0%"],
        ["Cloud Infrastructure", "$812B", "$980B", "+20.7%"],
        ["AI Services", "$340B", "$520B", "+52.9%"],
        ["Hardware", "$1.18T", "$1.22T", "+3.4%"],
        ["Cybersecurity", "$168B", "$204B", "+21.4%"],
    ]
    pt = Table(proj_data, colWidths=[150, 100, 100, 100])
    pt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#EEF2FF')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(pt)
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(
        "AI services growth is expected to decelerate slightly as the market matures, "
        "but will remain the highest-growth segment through 2026. Cloud infrastructure "
        "spending will benefit from ongoing enterprise migrations and the infrastructure "
        "demands of AI workloads. Cybersecurity investment will be driven by regulatory "
        "mandates and the expanding threat landscape.",
        normal_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(
        "Strategic Recommendation: Organizations should prioritize AI-ready infrastructure "
        "investments, develop clear AI governance frameworks, and build internal capability "
        "for continuous adaptation to rapidly evolving technology landscapes. Vendors who "
        "demonstrate clear ROI and strong security postures will be best positioned for "
        "sustained growth.",
        normal_style))

    # Build the PDF
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=0.9 * inch,
        rightMargin=0.9 * inch,
        topMargin=0.9 * inch,
        bottomMargin=0.9 * inch,
    )
    doc.build(story)
    print(f'Initial file created: {OUTPUT_PDF}')

    # Open in evince at page 4 (0-indexed = 3)
    launch_gui(f'evince --page-index=3 "{OUTPUT_PDF}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0 at page 4')


create_initial()
