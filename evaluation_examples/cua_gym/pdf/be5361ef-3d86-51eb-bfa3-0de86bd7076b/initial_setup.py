"""
Initial Setup: Create a 22-page company report PDF and a logo image.
Task ID: pdf_pw_046
Domain: pdf
"""

import os
import shlex
import subprocess
import time

import pymupdf
from PIL import Image, ImageDraw, ImageFont

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_046'
DOCUMENTS_DIR = f'{WORKDIR}/Documents'
ASSETS_DIR = f'{WORKDIR}/assets'
OUTPUT_PDF = f'{DOCUMENTS_DIR}/company_report.pdf'
LOGO_PATH = f'{ASSETS_DIR}/logo.png'


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


def create_logo():
    """Create a 400x200 company logo PNG with transparent background."""
    os.makedirs(ASSETS_DIR, exist_ok=True)
    img = Image.new('RGBA', (400, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw a stylized logo shape - rounded rectangle with company initials
    # Blue gradient-like rectangle
    draw.rounded_rectangle(
        [(20, 30), (380, 170)],
        radius=20,
        fill=(30, 70, 150, 220),
        outline=(20, 50, 120, 255),
        width=3,
    )

    # Company name text
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except OSError:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    draw.text((60, 55), "NovaTech", fill=(255, 255, 255, 255), font=font_large)
    draw.text((62, 120), "Solutions Inc.", fill=(200, 220, 255, 255), font=font_small)

    # Small accent circle
    draw.ellipse([(320, 50), (360, 90)], fill=(100, 200, 255, 200))

    img.save(LOGO_PATH, 'PNG')
    print(f'Logo created: {LOGO_PATH}')


def create_report():
    """Create a 22-page company report PDF with realistic content."""
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)

    doc = pymupdf.open()
    W, H = 612, 792  # US Letter

    # Report structure: cover + 21 content pages
    sections = [
        ("NovaTech Solutions Inc.\nAnnual Report 2025", True),  # Cover page
        ("Executive Summary", False),
        ("Company Overview", False),
        ("Financial Highlights", False),
        ("Revenue Analysis - Q1", False),
        ("Revenue Analysis - Q2", False),
        ("Revenue Analysis - Q3", False),
        ("Revenue Analysis - Q4", False),
        ("Operating Expenses", False),
        ("Research & Development", False),
        ("Product Portfolio", False),
        ("Market Expansion", False),
        ("Customer Acquisition", False),
        ("Employee Statistics", False),
        ("Talent Development", False),
        ("Sustainability Report", False),
        ("Risk Assessment", False),
        ("Regulatory Compliance", False),
        ("Strategic Outlook 2026", False),
        ("Board of Directors", False),
        ("Auditor's Report", False),
        ("Appendix: Financial Statements", False),
    ]

    paragraphs_pool = [
        "NovaTech Solutions demonstrated exceptional growth throughout fiscal year 2025, "
        "achieving a consolidated revenue of $847.3 million, representing a 23.4% increase "
        "over the prior year. This growth was driven primarily by our cloud infrastructure "
        "services division and the successful launch of our enterprise AI platform.",

        "Operating margins improved to 18.7% from 15.2% in the previous fiscal year, "
        "reflecting our continued focus on operational efficiency and strategic cost management. "
        "The company invested $142.6 million in research and development, representing 16.8% "
        "of total revenue.",

        "Our customer base expanded to over 12,400 enterprise clients across 47 countries, "
        "with a net retention rate of 118%. Key client acquisitions include Fortune 500 companies "
        "in the financial services, healthcare, and manufacturing sectors.",

        "The board approved a quarterly dividend of $0.85 per share, marking the 14th consecutive "
        "quarter of dividend increases. Total shareholder return for the fiscal year was 31.2%, "
        "outperforming the S&P 500 Technology Index by 8.7 percentage points.",

        "Employee headcount grew to 8,450 across 23 global offices. The company maintained "
        "an employee satisfaction score of 4.3 out of 5.0 and was recognized as one of the "
        "Top 50 Best Places to Work in Technology by Workplace Analytics Group.",

        "Our sustainability initiatives reduced carbon emissions by 28% year-over-year. "
        "The company committed to achieving carbon neutrality by 2028 and has invested "
        "$18.5 million in renewable energy infrastructure for our data centers.",

        "Strategic partnerships with leading cloud providers and system integrators expanded "
        "our market reach significantly. The partnership ecosystem contributed $196.4 million "
        "in influenced revenue, a 34% increase from the previous year.",

        "The risk management framework was enhanced with the implementation of an enterprise-wide "
        "cybersecurity platform, reducing critical vulnerability exposure by 67%. The company "
        "maintained zero material data breaches throughout the fiscal year.",

        "Product innovation remained a core focus, with 14 major product releases and 238 "
        "feature updates delivered across our platform portfolio. Customer adoption of our "
        "latest AI-powered analytics suite exceeded projections by 45%.",

        "Regional performance was led by North America ($412.8M, +19%), followed by Europe "
        "($218.5M, +27%), Asia-Pacific ($156.3M, +31%), and Rest of World ($59.7M, +18%). "
        "The Asia-Pacific region showed the strongest growth trajectory.",

        "Capital expenditure totaled $89.4 million, primarily allocated to data center "
        "expansion in Singapore and Frankfurt, as well as the renovation of our headquarters "
        "campus in Austin, Texas. These investments position us well for projected demand growth.",

        "The company's free cash flow reached $198.7 million, enabling accelerated debt "
        "repayment and strategic acquisition activity. We completed two bolt-on acquisitions "
        "valued at $67.2 million combined, enhancing our capabilities in edge computing.",
    ]

    table_data_sets = [
        {
            "headers": ["Quarter", "Revenue ($M)", "Growth (%)", "EBITDA ($M)", "Margin (%)"],
            "rows": [
                ["Q1 2025", "192.4", "21.3", "38.1", "19.8"],
                ["Q2 2025", "208.7", "24.1", "41.2", "19.7"],
                ["Q3 2025", "219.5", "25.8", "42.8", "19.5"],
                ["Q4 2025", "226.7", "22.6", "39.6", "17.5"],
                ["FY 2025", "847.3", "23.4", "161.7", "19.1"],
            ],
        },
        {
            "headers": ["Department", "Headcount", "Budget ($M)", "YoY Change"],
            "rows": [
                ["Engineering", "3,240", "312.5", "+18%"],
                ["Sales & Marketing", "2,150", "178.3", "+22%"],
                ["Operations", "1,680", "134.7", "+12%"],
                ["R&D", "890", "142.6", "+28%"],
                ["G&A", "490", "79.2", "+8%"],
            ],
        },
        {
            "headers": ["Region", "Clients", "Revenue ($M)", "NRR (%)", "Growth"],
            "rows": [
                ["North America", "5,840", "412.8", "121%", "+19%"],
                ["Europe", "3,420", "218.5", "116%", "+27%"],
                ["Asia-Pacific", "2,180", "156.3", "119%", "+31%"],
                ["Rest of World", "960", "59.7", "108%", "+18%"],
            ],
        },
    ]

    for page_idx, (title, is_cover) in enumerate(sections):
        page = doc.new_page(width=W, height=H)

        if is_cover:
            # Cover page - centered title, no content near top-right
            # Company name large centered
            page.insert_text(
                pymupdf.Point(W / 2 - 180, 300),
                "NovaTech Solutions Inc.",
                fontsize=28,
                fontname="hebo",
                color=(0.1, 0.2, 0.5),
            )
            page.insert_text(
                pymupdf.Point(W / 2 - 100, 360),
                "Annual Report 2025",
                fontsize=22,
                fontname="helv",
                color=(0.3, 0.3, 0.3),
            )
            # Decorative line
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(150, 390), pymupdf.Point(462, 390))
            shape.finish(color=(0.1, 0.2, 0.5), width=2)
            shape.commit()

            page.insert_text(
                pymupdf.Point(W / 2 - 80, 440),
                "Fiscal Year Ending",
                fontsize=14,
                fontname="helv",
                color=(0.4, 0.4, 0.4),
            )
            page.insert_text(
                pymupdf.Point(W / 2 - 80, 465),
                "December 31, 2025",
                fontsize=14,
                fontname="hebo",
                color=(0.4, 0.4, 0.4),
            )
            page.insert_text(
                pymupdf.Point(W / 2 - 120, 700),
                "Confidential - For Internal Use Only",
                fontsize=10,
                fontname="heit",
                color=(0.6, 0.6, 0.6),
            )
        else:
            # Content pages - leave top-right area (450,20)-(550,70) clear
            # Page number at bottom center
            page.insert_text(
                pymupdf.Point(W / 2 - 10, H - 30),
                str(page_idx + 1),
                fontsize=10,
                fontname="helv",
                color=(0.5, 0.5, 0.5),
            )

            # Section title at top-left (well away from top-right logo area)
            page.insert_text(
                pymupdf.Point(60, 60),
                title,
                fontsize=20,
                fontname="hebo",
                color=(0.1, 0.2, 0.5),
            )

            # Horizontal rule under title
            shape = page.new_shape()
            shape.draw_line(pymupdf.Point(60, 70), pymupdf.Point(400, 70))
            shape.finish(color=(0.1, 0.2, 0.5), width=1.5)
            shape.commit()

            # Body text - use paragraphs from pool
            y_pos = 100
            para_indices = [(page_idx * 2 + i) % len(paragraphs_pool) for i in range(3)]
            for pi in para_indices:
                rect = pymupdf.Rect(60, y_pos, W - 60, y_pos + 120)
                page.insert_textbox(
                    rect,
                    paragraphs_pool[pi],
                    fontsize=10,
                    fontname="helv",
                    color=(0.15, 0.15, 0.15),
                    align=pymupdf.TEXT_ALIGN_JUSTIFY,
                )
                y_pos += 130

            # Add a table on some pages
            if page_idx % 4 == 1 and (page_idx // 4) < len(table_data_sets):
                tdata = table_data_sets[page_idx // 4]
                table_y = y_pos + 20
                col_width = (W - 120) / len(tdata["headers"])

                # Table header
                shape2 = page.new_shape()
                header_rect = pymupdf.Rect(60, table_y, W - 60, table_y + 22)
                shape2.draw_rect(header_rect)
                shape2.finish(fill=(0.1, 0.2, 0.5), color=(0.1, 0.2, 0.5))
                shape2.commit()

                for ci, h in enumerate(tdata["headers"]):
                    page.insert_text(
                        pymupdf.Point(65 + ci * col_width, table_y + 16),
                        h,
                        fontsize=9,
                        fontname="hebo",
                        color=(1, 1, 1),
                    )

                # Table rows
                for ri, row in enumerate(tdata["rows"]):
                    row_y = table_y + 22 + ri * 20
                    if ri % 2 == 0:
                        shape3 = page.new_shape()
                        row_rect = pymupdf.Rect(60, row_y, W - 60, row_y + 20)
                        shape3.draw_rect(row_rect)
                        shape3.finish(fill=(0.93, 0.93, 0.97), color=(0.93, 0.93, 0.97))
                        shape3.commit()
                    for ci, val in enumerate(row):
                        page.insert_text(
                            pymupdf.Point(65 + ci * col_width, row_y + 14),
                            val,
                            fontsize=9,
                            fontname="helv",
                            color=(0.15, 0.15, 0.15),
                        )

    # Add Table of Contents
    toc = []
    for idx, (title, is_cover) in enumerate(sections):
        if is_cover:
            toc.append([1, "Cover Page", idx + 1])
        else:
            toc.append([1, title, idx + 1])
    doc.set_toc(toc)

    doc.save(OUTPUT_PDF)
    doc.close()
    print(f'Initial report created: {OUTPUT_PDF} (22 pages)')


def main():
    create_logo()
    create_report()

    # Open the report in Evince for the GUI agent
    launch_gui(f'evince "{OUTPUT_PDF}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


main()
