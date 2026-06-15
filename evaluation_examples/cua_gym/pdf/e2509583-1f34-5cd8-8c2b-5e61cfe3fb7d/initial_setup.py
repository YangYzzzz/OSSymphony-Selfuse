"""
Initial Setup: Replace logo in financial report PDF
Task ID: pdf_fin_091
Domain: pdf

Creates:
  /home/user/finance/report_old_logo.pdf  - multi-page financial report with old company logo
  /home/user/finance/assets/new_logo.png  - replacement logo image (400x200px)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_091'
FINANCE_DIR = f'{WORKDIR}/finance'
ASSETS_DIR = f'{FINANCE_DIR}/assets'
OUTPUT_PDF = f'{FINANCE_DIR}/report_old_logo.pdf'
NEW_LOGO_PATH = f'{ASSETS_DIR}/new_logo.png'


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


def create_old_logo():
    """Create an 'old' company logo as a PNG image (blue square with text)."""
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new('RGB', (400, 200), color=(30, 60, 120))
    draw = ImageDraw.Draw(img)
    # Draw a border
    draw.rectangle([5, 5, 394, 194], outline=(200, 200, 200), width=3)
    # Draw company name text
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except Exception:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    draw.text((50, 55), "OldCorp", fill=(255, 255, 255), font=font_large)
    draw.text((50, 110), "Financial Services", fill=(180, 200, 240), font=font_small)
    # Draw a small icon element
    draw.ellipse([300, 40, 370, 110], fill=(200, 160, 50), outline=(255, 255, 255))
    old_logo_path = f'{ASSETS_DIR}/old_logo.png'
    img.save(old_logo_path)
    return old_logo_path


def create_new_logo():
    """Create a 'new' company logo as a PNG image (green modern design, 400x200px)."""
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new('RGB', (400, 200), color=(15, 100, 70))
    draw = ImageDraw.Draw(img)
    # Modern rounded-look border
    draw.rectangle([4, 4, 395, 195], outline=(100, 220, 160), width=3)
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 38)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except Exception:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    draw.text((45, 50), "NovaCorp", fill=(255, 255, 255), font=font_large)
    draw.text((45, 110), "Financial Solutions", fill=(180, 240, 200), font=font_small)
    # Modern triangle icon
    draw.polygon([(320, 40), (380, 110), (260, 110)], fill=(100, 220, 160))
    img.save(NEW_LOGO_PATH)


def create_report():
    """Create a multi-page financial report PDF with old logo on page 1."""
    import pymupdf

    doc = pymupdf.open()

    # ---- PAGE 1: Cover / Summary ----
    page1 = doc.new_page(width=612, height=792)  # Letter size

    # Insert old logo at top-left (rect approximately 50,50,200,120)
    old_logo_path = create_old_logo()
    logo_rect = pymupdf.Rect(50, 50, 200, 120)
    page1.insert_image(logo_rect, filename=old_logo_path)

    # Title
    page1.insert_text(
        pymupdf.Point(220, 80),
        "Annual Financial Report 2025",
        fontsize=20, fontname="hebo", color=(0.1, 0.1, 0.3)
    )
    page1.insert_text(
        pymupdf.Point(220, 100),
        "Fiscal Year Ending December 31, 2025",
        fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3)
    )

    # Separator line
    shape1 = page1.new_shape()
    shape1.draw_line(pymupdf.Point(50, 140), pymupdf.Point(562, 140))
    shape1.finish(color=(0.1, 0.2, 0.5), width=1.5)
    shape1.commit()

    # Executive Summary
    page1.insert_text(pymupdf.Point(50, 175), "Executive Summary", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))

    summary_text = (
        "This annual report presents the consolidated financial results for OldCorp Financial Services "
        "for the fiscal year ended December 31, 2025. Total revenue reached $487.3 million, representing "
        "a 12.4% year-over-year increase driven by strong performance across all business segments. "
        "Operating income grew to $98.6 million with an operating margin of 20.2%, up from 18.7% in the "
        "prior year. Net income attributable to shareholders was $72.1 million, or $3.42 per diluted share."
    )
    page1.insert_textbox(
        pymupdf.Rect(50, 195, 562, 340),
        summary_text,
        fontsize=11, fontname="helv", color=(0.15, 0.15, 0.15),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Key metrics table header
    page1.insert_text(pymupdf.Point(50, 370), "Key Financial Highlights", fontsize=14, fontname="hebo", color=(0.1, 0.2, 0.5))

    metrics = [
        ("Metric", "FY 2025", "FY 2024", "Change"),
        ("Total Revenue", "$487.3M", "$433.5M", "+12.4%"),
        ("Operating Income", "$98.6M", "$81.1M", "+21.6%"),
        ("Net Income", "$72.1M", "$59.8M", "+20.6%"),
        ("Earnings Per Share", "$3.42", "$2.84", "+20.4%"),
        ("Total Assets", "$2.14B", "$1.89B", "+13.2%"),
        ("Return on Equity", "16.8%", "15.2%", "+1.6pp"),
        ("Dividend Per Share", "$1.20", "$1.05", "+14.3%"),
    ]

    y_start = 390
    col_x = [50, 200, 320, 430]
    for i, row in enumerate(metrics):
        y = y_start + i * 22
        is_header = (i == 0)
        font = "hebo" if is_header else "helv"
        color = (1, 1, 1) if is_header else (0.15, 0.15, 0.15)
        if is_header:
            shape_h = page1.new_shape()
            shape_h.draw_rect(pymupdf.Rect(48, y - 14, 564, y + 8))
            shape_h.finish(fill=(0.1, 0.2, 0.5), color=(0.1, 0.2, 0.5))
            shape_h.commit()
        elif i % 2 == 0:
            shape_alt = page1.new_shape()
            shape_alt.draw_rect(pymupdf.Rect(48, y - 14, 564, y + 8))
            shape_alt.finish(fill=(0.93, 0.95, 0.98), color=(0.93, 0.95, 0.98))
            shape_alt.commit()
        for j, val in enumerate(row):
            page1.insert_text(pymupdf.Point(col_x[j], y), val, fontsize=10, fontname=font, color=color)

    # Footer
    page1.insert_text(
        pymupdf.Point(50, 750),
        "OldCorp Financial Services  |  Confidential  |  Page 1",
        fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5)
    )

    # ---- PAGE 2: Revenue Breakdown ----
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text(pymupdf.Point(50, 60), "Revenue Breakdown by Segment", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))

    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(50, 75), pymupdf.Point(562, 75))
    shape2.finish(color=(0.1, 0.2, 0.5), width=1)
    shape2.commit()

    segments = [
        ("Business Segment", "Revenue", "% of Total", "YoY Growth"),
        ("Wealth Management", "$168.2M", "34.5%", "+15.1%"),
        ("Corporate Banking", "$132.4M", "27.2%", "+9.8%"),
        ("Retail Banking", "$89.7M", "18.4%", "+11.2%"),
        ("Insurance Services", "$54.3M", "11.1%", "+14.6%"),
        ("Capital Markets", "$42.7M", "8.8%", "+8.3%"),
    ]

    y_start2 = 100
    col_x2 = [50, 220, 340, 460]
    for i, row in enumerate(segments):
        y = y_start2 + i * 24
        is_header = (i == 0)
        font = "hebo" if is_header else "helv"
        color = (1, 1, 1) if is_header else (0.15, 0.15, 0.15)
        if is_header:
            sh = page2.new_shape()
            sh.draw_rect(pymupdf.Rect(48, y - 14, 564, y + 10))
            sh.finish(fill=(0.1, 0.2, 0.5), color=(0.1, 0.2, 0.5))
            sh.commit()
        elif i % 2 == 0:
            sh = page2.new_shape()
            sh.draw_rect(pymupdf.Rect(48, y - 14, 564, y + 10))
            sh.finish(fill=(0.93, 0.95, 0.98), color=(0.93, 0.95, 0.98))
            sh.commit()
        for j, val in enumerate(row):
            page2.insert_text(pymupdf.Point(col_x2[j], y), val, fontsize=10, fontname=font, color=color)

    # Narrative
    narrative = (
        "Wealth Management continued to be the largest revenue contributor at 34.5% of total revenue, "
        "driven by increased assets under management and higher advisory fees. The segment benefited from "
        "strong equity market performance and net new client acquisitions of 2,340 high-net-worth individuals.\n\n"
        "Corporate Banking saw steady growth of 9.8%, supported by increased lending activity in the "
        "mid-market segment and higher transaction banking volumes. The loan portfolio grew to $4.2 billion "
        "with non-performing loans remaining below 0.8%.\n\n"
        "Retail Banking achieved 11.2% growth through digital channel expansion, with mobile banking "
        "transactions increasing 28% year-over-year. The branch optimization program reduced operating "
        "costs by $12.3 million while maintaining customer satisfaction scores above 87%."
    )
    page2.insert_textbox(
        pymupdf.Rect(50, 270, 562, 550),
        narrative,
        fontsize=10.5, fontname="helv", color=(0.15, 0.15, 0.15),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    page2.insert_text(
        pymupdf.Point(50, 750),
        "OldCorp Financial Services  |  Confidential  |  Page 2",
        fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5)
    )

    # ---- PAGE 3: Balance Sheet Summary ----
    page3 = doc.new_page(width=612, height=792)
    page3.insert_text(pymupdf.Point(50, 60), "Consolidated Balance Sheet Summary", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))

    shape3 = page3.new_shape()
    shape3.draw_line(pymupdf.Point(50, 75), pymupdf.Point(562, 75))
    shape3.finish(color=(0.1, 0.2, 0.5), width=1)
    shape3.commit()

    balance_data = [
        ("Assets", "Dec 2025", "Dec 2024"),
        ("Cash & Equivalents", "$312.5M", "$278.9M"),
        ("Investment Securities", "$489.1M", "$421.3M"),
        ("Loans & Advances", "$876.4M", "$784.2M"),
        ("Property & Equipment", "$145.8M", "$138.6M"),
        ("Goodwill & Intangibles", "$198.3M", "$172.4M"),
        ("Other Assets", "$118.2M", "$94.8M"),
        ("Total Assets", "$2,140.3M", "$1,890.2M"),
        ("", "", ""),
        ("Liabilities & Equity", "Dec 2025", "Dec 2024"),
        ("Customer Deposits", "$1,245.6M", "$1,098.7M"),
        ("Borrowings", "$387.2M", "$356.1M"),
        ("Other Liabilities", "$78.4M", "$64.3M"),
        ("Total Equity", "$429.1M", "$371.1M"),
        ("Total Liabilities & Equity", "$2,140.3M", "$1,890.2M"),
    ]

    y_start3 = 100
    col_x3 = [50, 300, 440]
    for i, row in enumerate(balance_data):
        y = y_start3 + i * 22
        if row[0] == "":
            continue
        is_header = row[0] in ("Assets", "Liabilities & Equity")
        is_total = "Total" in row[0]
        if is_header:
            sh = page3.new_shape()
            sh.draw_rect(pymupdf.Rect(48, y - 14, 564, y + 8))
            sh.finish(fill=(0.1, 0.2, 0.5), color=(0.1, 0.2, 0.5))
            sh.commit()
            color = (1, 1, 1)
            font = "hebo"
        elif is_total:
            font = "hebo"
            color = (0.1, 0.1, 0.1)
        else:
            font = "helv"
            color = (0.15, 0.15, 0.15)
        for j, val in enumerate(row):
            page3.insert_text(pymupdf.Point(col_x3[j], y), val, fontsize=10, fontname=font, color=color)

    page3.insert_text(
        pymupdf.Point(50, 750),
        "OldCorp Financial Services  |  Confidential  |  Page 3",
        fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5)
    )

    # ---- PAGE 4: Notes and Outlook ----
    page4 = doc.new_page(width=612, height=792)
    page4.insert_text(pymupdf.Point(50, 60), "Forward-Looking Outlook", fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.5))

    shape4 = page4.new_shape()
    shape4.draw_line(pymupdf.Point(50, 75), pymupdf.Point(562, 75))
    shape4.finish(color=(0.1, 0.2, 0.5), width=1)
    shape4.commit()

    outlook = (
        "Management expects continued growth momentum into fiscal year 2026, with revenue projected "
        "to reach $530-545 million, representing approximately 9-12% year-over-year growth. Key strategic "
        "initiatives include:\n\n"
        "1. Digital Transformation: Investment of $45 million in technology modernization, including "
        "AI-powered advisory tools and enhanced cybersecurity infrastructure.\n\n"
        "2. Geographic Expansion: Planned entry into three new markets in the Asia-Pacific region, "
        "with estimated setup costs of $28 million and expected break-even within 18 months.\n\n"
        "3. Talent Acquisition: Recruitment of approximately 850 new employees across technology, "
        "compliance, and client-facing roles to support growth targets.\n\n"
        "4. ESG Integration: Launch of sustainable finance products targeting $500 million in green "
        "bond issuance and ESG-focused investment portfolios.\n\n"
        "Risk factors include potential interest rate volatility, regulatory changes in key markets, "
        "and macroeconomic uncertainty. The company maintains strong capital adequacy ratios (CET1 at "
        "14.2%) and liquidity coverage ratios (128%) well above regulatory minimums."
    )
    page4.insert_textbox(
        pymupdf.Rect(50, 95, 562, 550),
        outlook,
        fontsize=10.5, fontname="helv", color=(0.15, 0.15, 0.15),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    page4.insert_text(
        pymupdf.Point(50, 750),
        "OldCorp Financial Services  |  Confidential  |  Page 4",
        fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5)
    )

    # Set metadata
    doc.set_metadata({
        "title": "OldCorp Financial Services - Annual Report 2025",
        "author": "OldCorp Finance Department",
        "subject": "Annual Financial Report",
        "keywords": "finance, annual report, 2025, OldCorp",
    })

    # Set TOC
    doc.set_toc([
        [1, "Executive Summary", 1],
        [1, "Revenue Breakdown by Segment", 2],
        [1, "Consolidated Balance Sheet Summary", 3],
        [1, "Forward-Looking Outlook", 4],
    ])

    doc.save(OUTPUT_PDF)
    doc.close()
    print(f'Initial PDF created: {OUTPUT_PDF}')


def create_initial():
    os.makedirs(FINANCE_DIR, exist_ok=True)
    os.makedirs(ASSETS_DIR, exist_ok=True)

    # Create the new logo that the agent will use for replacement
    create_new_logo()
    print(f'New logo created: {NEW_LOGO_PATH}')

    # Create the report with the old logo
    create_report()

    # Launch PDF viewer
    launch_gui(f'evince "{OUTPUT_PDF}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
