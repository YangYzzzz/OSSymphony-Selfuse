"""
Initial Setup: Create a 9-page business report draft PDF without page numbers.
Task ID: pdf_gf1_021
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
DOCUMENTS = f'{WORKDIR}/Documents'
TASK_ID = 'pdf_gf1_021'
OUTPUT = f'{DOCUMENTS}/report_draft.pdf'

# Page dimensions: US Letter
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
    os.makedirs(DOCUMENTS, exist_ok=True)

    doc = pymupdf.open()

    # --- Page 1: Title Page ---
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(PAGE_W / 2 - 150, 250), "Meridian Technologies Inc.",
                     fontsize=22, fontname="hebo", color=(0.1, 0.15, 0.35))
    page.insert_text(pymupdf.Point(PAGE_W / 2 - 120, 310), "Annual Business Report",
                     fontsize=20, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text(pymupdf.Point(PAGE_W / 2 - 50, 360), "Fiscal Year 2025",
                     fontsize=14, fontname="helv", color=(0.4, 0.4, 0.4))
    page.insert_text(pymupdf.Point(PAGE_W / 2 - 80, 420), "Prepared by: Strategy Division",
                     fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(PAGE_W / 2 - 65, 445), "Date: March 15, 2025",
                     fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))
    # Decorative line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(100, 280), pymupdf.Point(512, 280))
    shape.finish(color=(0.1, 0.15, 0.35), width=2)
    shape.commit()

    # --- Page 2: Table of Contents ---
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(72, 72), "Table of Contents", fontsize=18, fontname="hebo", color=(0.1, 0.15, 0.35))
    toc_items = [
        ("1. Executive Summary", 3),
        ("2. Financial Performance Overview", 4),
        ("3. Revenue Analysis by Segment", 5),
        ("4. Operational Highlights", 6),
        ("5. Market Expansion Strategy", 7),
        ("6. Human Resources & Talent", 8),
        ("7. Outlook and Recommendations", 9),
    ]
    y = 120
    for title, pg in toc_items:
        page.insert_text(pymupdf.Point(90, y), title, fontsize=12, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(480, y), f"....... {pg}", fontsize=12, fontname="helv", color=(0.4, 0.4, 0.4))
        y += 28

    # --- Page 3: Executive Summary ---
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(72, 72), "1. Executive Summary", fontsize=16, fontname="hebo", color=(0.1, 0.15, 0.35))
    summary_text = (
        "Meridian Technologies delivered strong results in fiscal year 2025, achieving consolidated "
        "revenue of $487.3 million, representing a 12.4% year-over-year increase. Our strategic "
        "investments in cloud infrastructure and artificial intelligence capabilities drove growth "
        "across all major business segments. Operating margin improved to 18.7%, up from 16.2% in "
        "the prior year, reflecting disciplined cost management and operational efficiency gains. "
        "The enterprise solutions division contributed $198.5 million in revenue, while our emerging "
        "data analytics platform exceeded expectations with $89.2 million. Customer retention rates "
        "remained robust at 94.3%, underscoring the strength of our product portfolio and client "
        "relationships. Looking ahead, we are well-positioned to capitalize on accelerating digital "
        "transformation trends and anticipate continued momentum into FY2026."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 400), summary_text,
                        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    page.insert_text(pymupdf.Point(72, 430), "Key Highlights:", fontsize=13, fontname="hebo", color=(0.1, 0.15, 0.35))
    highlights = [
        "Revenue growth of 12.4% to $487.3M",
        "Operating margin expansion to 18.7%",
        "Customer retention rate of 94.3%",
        "Successful launch of DataStream Analytics platform",
        "Expansion into 3 new international markets",
    ]
    y = 460
    for h in highlights:
        page.insert_text(pymupdf.Point(90, y), f"\u2022  {h}", fontsize=11, fontname="helv", color=(0, 0, 0))
        y += 22

    # --- Page 4: Financial Performance ---
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(72, 72), "2. Financial Performance Overview", fontsize=16, fontname="hebo", color=(0.1, 0.15, 0.35))
    fin_text = (
        "Total revenue for FY2025 reached $487.3 million, compared to $433.5 million in FY2024. "
        "Gross profit increased to $312.1 million with a gross margin of 64.1%. Research and "
        "development expenditure totaled $67.4 million (13.8% of revenue), reflecting our continued "
        "commitment to innovation. Selling, general, and administrative expenses were $153.5 million. "
        "Net income attributable to shareholders was $62.8 million, or $3.42 per diluted share."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 300), fin_text,
                        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    # Simple financial table header
    page.insert_text(pymupdf.Point(72, 330), "Condensed Income Statement (in millions USD)", fontsize=12, fontname="hebo", color=(0.1, 0.15, 0.35))
    table_data = [
        ("", "FY2025", "FY2024", "Change"),
        ("Revenue", "$487.3", "$433.5", "+12.4%"),
        ("Cost of Revenue", "$175.2", "$160.4", "+9.2%"),
        ("Gross Profit", "$312.1", "$273.1", "+14.3%"),
        ("R&D Expenses", "$67.4", "$61.8", "+9.1%"),
        ("SG&A Expenses", "$153.5", "$141.2", "+8.7%"),
        ("Operating Income", "$91.2", "$70.1", "+30.1%"),
        ("Net Income", "$62.8", "$48.3", "+30.0%"),
    ]
    y_start = 360
    col_x = [90, 260, 360, 460]
    for i, row in enumerate(table_data):
        fontname = "hebo" if i == 0 else "helv"
        for j, val in enumerate(row):
            page.insert_text(pymupdf.Point(col_x[j], y_start + i * 22), val,
                             fontsize=10, fontname=fontname, color=(0, 0, 0))

    # --- Page 5: Revenue Analysis ---
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(72, 72), "3. Revenue Analysis by Segment", fontsize=16, fontname="hebo", color=(0.1, 0.15, 0.35))
    segments_text = (
        "Our diversified business model across four operating segments provided resilience and "
        "growth opportunities throughout the fiscal year. Enterprise Solutions remained our largest "
        "segment at $198.5 million (40.7% of total revenue), while the Cloud Services segment "
        "showed the strongest growth at 23.1%, reaching $124.6 million."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 240), segments_text,
                        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    segments = [
        ("Enterprise Solutions", "$198.5M", "40.7%", "+8.3%"),
        ("Cloud Services", "$124.6M", "25.6%", "+23.1%"),
        ("Data Analytics Platform", "$89.2M", "18.3%", "+18.7%"),
        ("Professional Services", "$75.0M", "15.4%", "+4.2%"),
    ]
    page.insert_text(pymupdf.Point(72, 270), "Segment Breakdown:", fontsize=13, fontname="hebo", color=(0.1, 0.15, 0.35))
    seg_headers = ["Segment", "Revenue", "% of Total", "YoY Growth"]
    seg_x = [90, 260, 360, 450]
    y = 300
    for j, h in enumerate(seg_headers):
        page.insert_text(pymupdf.Point(seg_x[j], y), h, fontsize=10, fontname="hebo", color=(0, 0, 0))
    y += 22
    for row in segments:
        for j, val in enumerate(row):
            page.insert_text(pymupdf.Point(seg_x[j], y), val, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 22

    # --- Page 6: Operational Highlights ---
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(72, 72), "4. Operational Highlights", fontsize=16, fontname="hebo", color=(0.1, 0.15, 0.35))
    ops_text = (
        "In FY2025, Meridian Technologies achieved several operational milestones that strengthen "
        "our competitive position. We expanded our cloud data center footprint to 14 locations "
        "across North America, Europe, and Asia-Pacific. System uptime across all platforms "
        "averaged 99.97%, exceeding our SLA commitments. Our engineering team delivered 47 major "
        "product releases and 312 feature updates throughout the year."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 280), ops_text,
                        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    ops_items = [
        "Deployed next-generation security framework across all products",
        "Achieved SOC 2 Type II and ISO 27001 certifications",
        "Reduced average incident response time by 34%",
        "Migrated 89% of legacy customers to the unified platform",
        "Launched self-service analytics dashboard for enterprise clients",
        "Opened new engineering hub in Austin, Texas with 120 positions",
    ]
    page.insert_text(pymupdf.Point(72, 310), "Major Achievements:", fontsize=13, fontname="hebo", color=(0.1, 0.15, 0.35))
    y = 340
    for item in ops_items:
        page.insert_text(pymupdf.Point(90, y), f"\u2022  {item}", fontsize=11, fontname="helv", color=(0, 0, 0))
        y += 22

    # --- Page 7: Market Expansion ---
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(72, 72), "5. Market Expansion Strategy", fontsize=16, fontname="hebo", color=(0.1, 0.15, 0.35))
    market_text = (
        "Meridian Technologies expanded its geographic presence significantly in FY2025. We "
        "established regional offices in Singapore, Munich, and Sao Paulo, strengthening our "
        "ability to serve enterprise clients in high-growth markets. International revenue "
        "contributed $143.7 million (29.5% of total), up from $108.4 million (25.0%) in FY2024. "
        "Our partner ecosystem grew to 340 certified resellers and technology partners globally."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 280), market_text,
                        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    geo_data = [
        ("North America", "$343.6M", "70.5%"),
        ("Europe", "$78.9M", "16.2%"),
        ("Asia-Pacific", "$48.7M", "10.0%"),
        ("Latin America", "$16.1M", "3.3%"),
    ]
    page.insert_text(pymupdf.Point(72, 310), "Revenue by Geography:", fontsize=13, fontname="hebo", color=(0.1, 0.15, 0.35))
    geo_x = [90, 280, 400]
    y = 340
    for h in ["Region", "Revenue", "% of Total"]:
        page.insert_text(pymupdf.Point(geo_x[["Region", "Revenue", "% of Total"].index(h)], y), h,
                         fontsize=10, fontname="hebo", color=(0, 0, 0))
    y += 22
    for row in geo_data:
        for j, val in enumerate(row):
            page.insert_text(pymupdf.Point(geo_x[j], y), val, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 22

    # --- Page 8: Human Resources ---
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(72, 72), "6. Human Resources & Talent", fontsize=16, fontname="hebo", color=(0.1, 0.15, 0.35))
    hr_text = (
        "Our workforce grew to 3,247 full-time employees by year-end, a net increase of 418 "
        "positions. Employee engagement scores improved to 82.4%, reflecting investments in "
        "professional development, flexible work arrangements, and competitive compensation. "
        "Voluntary turnover decreased to 11.3% from 14.7% in the prior year. We onboarded "
        "287 engineering professionals and invested $8.2 million in learning and development "
        "programs across the organization."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 300), hr_text,
                        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    hr_stats = [
        ("Total Headcount", "3,247"),
        ("Engineering Staff", "1,456 (44.8%)"),
        ("Sales & Marketing", "842 (25.9%)"),
        ("Operations & Support", "621 (19.1%)"),
        ("Corporate & Admin", "328 (10.1%)"),
        ("Employee Engagement", "82.4%"),
        ("Voluntary Turnover", "11.3%"),
    ]
    page.insert_text(pymupdf.Point(72, 330), "Workforce Statistics:", fontsize=13, fontname="hebo", color=(0.1, 0.15, 0.35))
    y = 360
    for label, value in hr_stats:
        page.insert_text(pymupdf.Point(90, y), f"{label}:", fontsize=11, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(300, y), value, fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))
        y += 22

    # --- Page 9: Outlook and Recommendations ---
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text(pymupdf.Point(72, 72), "7. Outlook and Recommendations", fontsize=16, fontname="hebo", color=(0.1, 0.15, 0.35))
    outlook_text = (
        "Looking ahead to FY2026, Meridian Technologies is well-positioned to sustain growth "
        "momentum. We project consolidated revenue in the range of $545 to $560 million, "
        "representing 12-15% growth. Key strategic priorities include: deepening our AI and "
        "machine learning capabilities, expanding the partner ecosystem in international markets, "
        "and continuing to invest in talent acquisition and retention."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 540, 280), outlook_text,
                        fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    recs = [
        "Increase R&D investment to 15% of revenue to accelerate AI capabilities",
        "Expand cloud infrastructure to 20 data centers by end of FY2026",
        "Target 3 strategic acquisitions in adjacent technology segments",
        "Achieve $600M revenue run-rate by Q4 FY2026",
        "Launch next-generation enterprise platform (Project Horizon)",
    ]
    page.insert_text(pymupdf.Point(72, 310), "Strategic Recommendations:", fontsize=13, fontname="hebo", color=(0.1, 0.15, 0.35))
    y = 340
    for i, rec in enumerate(recs, 1):
        page.insert_text(pymupdf.Point(90, y), f"{i}.  {rec}", fontsize=11, fontname="helv", color=(0, 0, 0))
        y += 24

    page.insert_text(pymupdf.Point(72, 500), "This document is confidential and intended for internal use only.",
                     fontsize=9, fontname="heit", color=(0.5, 0.5, 0.5))

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready: open in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
