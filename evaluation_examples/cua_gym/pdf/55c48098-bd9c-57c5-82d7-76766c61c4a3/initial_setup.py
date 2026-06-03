"""
Initial Setup: Create a 10-page financial data report PDF with tables on pages 3-4
Task ID: pdf_gf2_038
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_038'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/data_report.pdf'

# Table data: 5 columns, header + 15 data rows (split across pages 3 and 4)
TABLE_HEADERS = ["Department", "Q1 Revenue ($)", "Q2 Revenue ($)", "Q3 Revenue ($)", "Q4 Revenue ($)"]
TABLE_DATA = [
    ["Engineering",       "245,800",  "261,300",  "278,950",  "295,100"],
    ["Marketing",         "182,400",  "195,600",  "201,850",  "218,300"],
    ["Sales",             "534,200",  "567,800",  "589,100",  "612,450"],
    ["Human Resources",   "98,500",   "101,200",  "103,800",  "106,400"],
    ["Finance",           "127,300",  "131,600",  "135,900",  "140,200"],
    ["Operations",        "312,600",  "328,400",  "341,700",  "355,200"],
    ["Research & Dev",    "189,400",  "197,800",  "206,300",  "215,100"],
    ["Customer Support",  "145,700",  "152,300",  "158,900",  "165,800"],
    ["Legal",             "76,200",   "78,400",   "80,700",   "83,100"],
    ["IT Infrastructure", "167,800",  "174,500",  "181,300",  "188,600"],
    ["Product Design",    "112,500",  "118,700",  "125,100",  "131,800"],
    ["Quality Assurance", "89,300",   "93,100",   "97,200",   "101,400"],
    ["Supply Chain",      "203,400",  "215,600",  "228,100",  "241,300"],
    ["Business Dev",      "156,700",  "164,800",  "173,200",  "182,100"],
    ["Data Analytics",    "134,900",  "142,300",  "150,100",  "158,400"],
]


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


def draw_table_on_page(page, headers, rows, start_y, left_margin=50, font_size=9):
    """Draw table rows on a page. Returns the y position after the last row."""
    col_widths = [120, 100, 100, 100, 100]  # 5 columns
    row_height = 20
    right_margin = left_margin + sum(col_widths)
    y = start_y

    # Draw header if provided
    if headers:
        # Header background
        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(left_margin, y, right_margin, y + row_height))
        shape.finish(color=(0, 0, 0), fill=(0.2, 0.3, 0.5), width=0.5)
        shape.commit()

        x = left_margin
        for i, h in enumerate(headers):
            page.insert_text(
                pymupdf.Point(x + 4, y + 14),
                h,
                fontsize=font_size,
                fontname="hebo",
                color=(1, 1, 1),
            )
            x += col_widths[i]
        y += row_height

    # Draw data rows
    for row_idx, row in enumerate(rows):
        # Alternating row background
        if row_idx % 2 == 0:
            fill_color = (0.95, 0.95, 0.97)
        else:
            fill_color = (1, 1, 1)

        shape = page.new_shape()
        shape.draw_rect(pymupdf.Rect(left_margin, y, right_margin, y + row_height))
        shape.finish(color=(0.7, 0.7, 0.7), fill=fill_color, width=0.3)
        shape.commit()

        x = left_margin
        for i, cell in enumerate(row):
            page.insert_text(
                pymupdf.Point(x + 4, y + 14),
                str(cell),
                fontsize=font_size,
                fontname="helv",
                color=(0, 0, 0),
            )
            x += col_widths[i]
        y += row_height

    return y


def create_initial():
    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()
    page_width, page_height = 612, 792  # Letter size

    # ==================== PAGE 1: Title Page ====================
    p1 = doc.new_page(width=page_width, height=page_height)
    p1.insert_text(pymupdf.Point(120, 200), "Meridian Global Holdings", fontsize=28, fontname="hebo", color=(0.1, 0.2, 0.4))
    p1.insert_text(pymupdf.Point(150, 260), "Annual Revenue Report 2025", fontsize=20, fontname="helv", color=(0.3, 0.3, 0.3))
    p1.insert_text(pymupdf.Point(200, 320), "Prepared by: Financial Analytics Division", fontsize=12, fontname="tiit", color=(0.4, 0.4, 0.4))
    p1.insert_text(pymupdf.Point(220, 350), "Report Date: March 15, 2026", fontsize=12, fontname="helv", color=(0.4, 0.4, 0.4))
    p1.insert_text(pymupdf.Point(180, 380), "Classification: Internal - Confidential", fontsize=11, fontname="hebo", color=(0.6, 0.1, 0.1))

    # Decorative line
    shape = p1.new_shape()
    shape.draw_line(pymupdf.Point(100, 270), pymupdf.Point(512, 270))
    shape.finish(color=(0.1, 0.2, 0.4), width=2)
    shape.commit()

    # ==================== PAGE 2: Executive Summary ====================
    p2 = doc.new_page(width=page_width, height=page_height)
    p2.insert_text(pymupdf.Point(50, 60), "Executive Summary", fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.4))

    shape = p2.new_shape()
    shape.draw_line(pymupdf.Point(50, 68), pymupdf.Point(250, 68))
    shape.finish(color=(0.1, 0.2, 0.4), width=1)
    shape.commit()

    summary_text = (
        "Meridian Global Holdings delivered strong financial performance across all fifteen "
        "departments during fiscal year 2025. Total consolidated revenue reached $12.47 billion, "
        "representing a year-over-year increase of 8.3%. The Engineering and Sales divisions "
        "continued to be the primary revenue drivers, collectively contributing 42% of total "
        "company revenue. Notably, the Data Analytics department showed the highest growth "
        "trajectory at 17.4% year-over-year improvement."
    )
    rect = pymupdf.Rect(50, 85, 562, 220)
    p2.insert_textbox(rect, summary_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    overview_text = (
        "This report presents a detailed breakdown of quarterly revenue figures for each of "
        "the company's fifteen operational departments. The data presented in the following "
        "pages covers the period from January 1, 2025 through December 31, 2025. All figures "
        "are reported in US dollars and have been audited by Thornton & Associates LLP."
    )
    p2.insert_text(pymupdf.Point(50, 250), "Report Overview", fontsize=14, fontname="hebo", color=(0.1, 0.2, 0.4))
    rect2 = pymupdf.Rect(50, 268, 562, 380)
    p2.insert_textbox(rect2, overview_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    methodology_text = (
        "Revenue figures are compiled from departmental P&L statements submitted monthly to "
        "the Office of the CFO. Interdepartmental transfers have been eliminated to avoid "
        "double-counting. Foreign currency denominated revenues have been converted at the "
        "average quarterly exchange rate as published by the Federal Reserve."
    )
    p2.insert_text(pymupdf.Point(50, 410), "Methodology", fontsize=14, fontname="hebo", color=(0.1, 0.2, 0.4))
    rect3 = pymupdf.Rect(50, 428, 562, 540)
    p2.insert_textbox(rect3, methodology_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ==================== PAGE 3: Table Part 1 (Header + rows 1-9) ====================
    p3 = doc.new_page(width=page_width, height=page_height)
    p3.insert_text(pymupdf.Point(50, 50), "Departmental Revenue Breakdown", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.4))
    p3.insert_text(pymupdf.Point(50, 70), "Table 1: Quarterly Revenue by Department (FY 2025)", fontsize=11, fontname="tiit", color=(0.3, 0.3, 0.3))

    # Draw table header + first 9 rows on page 3
    draw_table_on_page(p3, TABLE_HEADERS, TABLE_DATA[:9], start_y=90)

    p3.insert_text(pymupdf.Point(50, 400), "(continued on next page)", fontsize=9, fontname="tiit", color=(0.5, 0.5, 0.5))

    # ==================== PAGE 4: Table Part 2 (rows 10-15) ====================
    p4 = doc.new_page(width=page_width, height=page_height)
    p4.insert_text(pymupdf.Point(50, 50), "Departmental Revenue Breakdown (continued)", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.4))

    # Draw remaining 6 rows without header repeat on page 4
    draw_table_on_page(p4, None, TABLE_DATA[9:], start_y=75)

    p4.insert_text(pymupdf.Point(50, 230), "Source: Departmental P&L Statements, FY 2025 (Audited)", fontsize=9, fontname="tiit", color=(0.4, 0.4, 0.4))

    # ==================== PAGE 5: Analysis ====================
    p5 = doc.new_page(width=page_width, height=page_height)
    p5.insert_text(pymupdf.Point(50, 60), "Revenue Analysis", fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.4))

    analysis_text = (
        "The Sales department maintained its position as the highest revenue-generating unit, "
        "with total annual revenue of $2.30 billion. This represents consistent quarter-over-quarter "
        "growth averaging 4.7%. The Engineering department ranked second with $1.08 billion in "
        "total revenue, driven primarily by increased enterprise licensing fees and consulting "
        "engagements in the Asia-Pacific region."
    )
    rect5 = pymupdf.Rect(50, 80, 562, 200)
    p5.insert_textbox(rect5, analysis_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    growth_text = (
        "From a growth perspective, the Data Analytics division led all departments with a "
        "17.4% improvement from Q1 to Q4. The Supply Chain division also showed strong momentum "
        "at 18.6% growth, reflecting the company's investment in logistics optimization technology. "
        "The Legal department exhibited the most stable pattern with modest 9.1% annualized growth."
    )
    p5.insert_text(pymupdf.Point(50, 230), "Growth Highlights", fontsize=14, fontname="hebo", color=(0.1, 0.2, 0.4))
    rect5b = pymupdf.Rect(50, 248, 562, 370)
    p5.insert_textbox(rect5b, growth_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ==================== PAGE 6: Regional Breakdown ====================
    p6 = doc.new_page(width=page_width, height=page_height)
    p6.insert_text(pymupdf.Point(50, 60), "Regional Revenue Distribution", fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.4))

    regional_text = (
        "North America continued to be the largest revenue region at 52% of total revenue, "
        "followed by Europe (28%), Asia-Pacific (14%), and Latin America (6%). The Asia-Pacific "
        "region showed the highest growth rate at 12.8%, driven by expanding operations in "
        "Singapore, Japan, and Australia. European revenue was impacted by currency headwinds "
        "but grew 5.2% in constant currency terms."
    )
    rect6 = pymupdf.Rect(50, 80, 562, 220)
    p6.insert_textbox(rect6, regional_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ==================== PAGE 7: Cost Analysis ====================
    p7 = doc.new_page(width=page_width, height=page_height)
    p7.insert_text(pymupdf.Point(50, 60), "Cost Structure and Margins", fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.4))

    cost_text = (
        "Consolidated gross margins improved by 1.4 percentage points to 62.3%, reflecting "
        "the company's ongoing efficiency initiatives and favorable product mix shift toward "
        "higher-margin software and services revenue. Operating expenses as a percentage of "
        "revenue declined from 43.1% to 41.7%, with the most significant improvements in "
        "general and administrative costs."
    )
    rect7 = pymupdf.Rect(50, 80, 562, 220)
    p7.insert_textbox(rect7, cost_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ==================== PAGE 8: Strategic Initiatives ====================
    p8 = doc.new_page(width=page_width, height=page_height)
    p8.insert_text(pymupdf.Point(50, 60), "Strategic Initiatives for FY 2026", fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.4))

    strategy_text = (
        "Management has identified several key strategic priorities for the coming fiscal year: "
        "expansion of the Data Analytics service portfolio, investment in AI-driven automation "
        "tools for the Operations and Supply Chain divisions, and geographic expansion into "
        "Southeast Asian markets. Capital expenditure for FY 2026 is projected at $840 million, "
        "representing a 12% increase over FY 2025 levels."
    )
    rect8 = pymupdf.Rect(50, 80, 562, 220)
    p8.insert_textbox(rect8, strategy_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ==================== PAGE 9: Risk Factors ====================
    p9 = doc.new_page(width=page_width, height=page_height)
    p9.insert_text(pymupdf.Point(50, 60), "Risk Factors", fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.4))

    risk_text = (
        "Key risk factors include macroeconomic uncertainty, potential regulatory changes in "
        "data privacy legislation across multiple jurisdictions, competitive pressures in the "
        "enterprise software market, and foreign exchange volatility. The company maintains a "
        "comprehensive risk management framework overseen by the Board's Audit and Risk Committee. "
        "Currency hedging positions cover approximately 75% of projected non-USD denominated revenue."
    )
    rect9 = pymupdf.Rect(50, 80, 562, 220)
    p9.insert_textbox(rect9, risk_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ==================== PAGE 10: Appendix / Disclaimer ====================
    p10 = doc.new_page(width=page_width, height=page_height)
    p10.insert_text(pymupdf.Point(50, 60), "Appendix and Disclaimer", fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.4))

    disclaimer_text = (
        "This report has been prepared for internal use by Meridian Global Holdings management "
        "and authorized personnel only. The information contained herein is confidential and "
        "proprietary. Reproduction, distribution, or disclosure without prior written authorization "
        "from the Office of the CFO is strictly prohibited. Financial data has been audited by "
        "Thornton & Associates LLP in accordance with GAAP standards."
    )
    rect10 = pymupdf.Rect(50, 80, 562, 220)
    p10.insert_textbox(rect10, disclaimer_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    p10.insert_text(pymupdf.Point(50, 260), "Contact Information", fontsize=14, fontname="hebo", color=(0.1, 0.2, 0.4))
    p10.insert_text(pymupdf.Point(50, 285), "Financial Analytics Division", fontsize=11, fontname="helv", color=(0, 0, 0))
    p10.insert_text(pymupdf.Point(50, 300), "Meridian Global Holdings", fontsize=11, fontname="helv", color=(0, 0, 0))
    p10.insert_text(pymupdf.Point(50, 315), "1200 Corporate Boulevard, Suite 4500", fontsize=11, fontname="helv", color=(0, 0, 0))
    p10.insert_text(pymupdf.Point(50, 330), "New York, NY 10017", fontsize=11, fontname="helv", color=(0, 0, 0))
    p10.insert_text(pymupdf.Point(50, 345), "Email: analytics@meridianglobal.com", fontsize=11, fontname="helv", color=(0, 0, 0))

    # Save PDF
    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 10')

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
