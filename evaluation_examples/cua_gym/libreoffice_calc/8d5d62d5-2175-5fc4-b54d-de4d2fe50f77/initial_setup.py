"""
Initial Setup: Create a 6-page image report PDF with 11 embedded images.
Task ID: pdf_gf2_045
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_045'
DOC_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOC_DIR}/image_report.pdf'


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


def create_sample_image(path, width, height, color, label):
    """Create a simple labeled image using PIL."""
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new('RGB', (width, height), color)
    draw = ImageDraw.Draw(img)
    # Draw a simple pattern
    for i in range(0, width, 40):
        draw.line([(i, 0), (i, height)], fill=(200, 200, 200), width=1)
    for i in range(0, height, 40):
        draw.line([(0, i), (width, i)], fill=(200, 200, 200), width=1)
    # Add label text
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except Exception:
        font = ImageFont.load_default()
    draw.text((10, 10), label, fill=(0, 0, 0), font=font)
    img.save(path)


def create_initial():
    import pymupdf

    os.makedirs(DOC_DIR, exist_ok=True)

    # Create 11 sample images with varied sizes and colors
    img_dir = '/tmp/report_images'
    os.makedirs(img_dir, exist_ok=True)

    image_specs = [
        # (filename, width, height, bg_color, label)
        ('chart_revenue.png', 480, 320, (230, 240, 255), 'Revenue Chart Q1-Q4'),
        ('chart_expenses.png', 480, 320, (255, 240, 230), 'Expense Breakdown'),
        ('photo_office.png', 400, 280, (220, 235, 220), 'Corporate Headquarters'),
        ('diagram_workflow.png', 520, 300, (245, 245, 220), 'Workflow Process Diagram'),
        ('chart_growth.png', 460, 300, (235, 230, 250), 'Year-over-Year Growth'),
        ('photo_team.png', 440, 310, (225, 240, 240), 'Executive Leadership Team'),
        ('chart_market.png', 500, 340, (250, 240, 235), 'Market Share Analysis'),
        ('diagram_org.png', 480, 350, (240, 250, 240), 'Organization Structure'),
        ('photo_product.png', 420, 280, (245, 235, 225), 'Product Line Showcase'),
        ('chart_satisfaction.png', 460, 300, (230, 245, 250), 'Customer Satisfaction Scores'),
        ('chart_forecast.png', 500, 320, (250, 245, 235), 'Financial Forecast 2026'),
    ]

    for fname, w, h, color, label in image_specs:
        create_sample_image(os.path.join(img_dir, fname), w, h, color, label)

    # Create the PDF document
    doc = pymupdf.open()

    # Helper: add text at position
    def add_text(page, x, y, text, fontsize=11, fontname="helv", color=(0, 0, 0), bold=False):
        fn = "hebo" if bold else fontname
        page.insert_text(pymupdf.Point(x, y), text, fontsize=fontsize, fontname=fn, color=color)

    def add_paragraph(page, rect, text, fontsize=10, fontname="helv"):
        page.insert_textbox(rect, text, fontsize=fontsize, fontname=fontname,
                            color=(0.15, 0.15, 0.15), align=pymupdf.TEXT_ALIGN_LEFT)

    # ==================== PAGE 1: Title & Executive Summary ====================
    page = doc.new_page(width=595, height=842)
    add_text(page, 72, 60, "Meridian Technologies Annual Report 2025", fontsize=22, bold=True, color=(0.1, 0.15, 0.4))
    add_text(page, 72, 85, "Prepared by the Strategy & Analytics Division", fontsize=11, color=(0.4, 0.4, 0.4))

    # Horizontal rule
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 95), pymupdf.Point(523, 95))
    shape.finish(color=(0.7, 0.7, 0.7), width=1)
    shape.commit()

    add_text(page, 72, 120, "Executive Summary", fontsize=14, bold=True, color=(0.1, 0.15, 0.4))
    add_paragraph(page, pymupdf.Rect(72, 135, 523, 210),
        "Meridian Technologies achieved record performance in fiscal year 2025, with consolidated "
        "revenue reaching $4.2 billion, representing a 17% year-over-year increase. Operating margins "
        "expanded to 23.4%, driven by efficiency gains in our cloud infrastructure and enterprise "
        "software divisions. This report provides a comprehensive overview of financial results, "
        "strategic initiatives, and the outlook for the year ahead.")

    # Image 1: Revenue chart
    img_rect1 = pymupdf.Rect(72, 225, 523, 505)
    page.insert_image(img_rect1, filename=os.path.join(img_dir, 'chart_revenue.png'))

    add_text(page, 72, 525, "Figure 1: Quarterly Revenue Performance (in millions USD)", fontsize=9, color=(0.3, 0.3, 0.3))

    add_paragraph(page, pymupdf.Rect(72, 545, 523, 640),
        "Revenue growth was primarily driven by three factors: expansion of our SaaS platform "
        "subscriber base (up 34%), increased average contract values in the enterprise segment, "
        "and strong adoption of our AI-powered analytics suite launched in Q2. International "
        "markets contributed 38% of total revenue, with particularly strong growth in APAC (+26%).")

    # Image 2: Expenses chart
    img_rect2 = pymupdf.Rect(72, 655, 360, 810)
    page.insert_image(img_rect2, filename=os.path.join(img_dir, 'chart_expenses.png'))

    add_text(page, 72, 825, "Figure 2: Expense Distribution by Category", fontsize=9, color=(0.3, 0.3, 0.3))

    # ==================== PAGE 2: Operations ====================
    page = doc.new_page(width=595, height=842)
    add_text(page, 72, 55, "Operational Highlights", fontsize=16, bold=True, color=(0.1, 0.15, 0.4))

    add_paragraph(page, pymupdf.Rect(72, 75, 523, 170),
        "Our operational footprint expanded significantly in 2025. We opened three new data centers "
        "in Frankfurt, Singapore, and Sao Paulo, bringing our global infrastructure to 14 facilities "
        "across 9 countries. Total compute capacity increased by 42%, while maintaining a 99.997% "
        "uptime SLA across all regions. Employee headcount grew from 8,200 to 9,450, with key hires "
        "in engineering, product design, and customer success functions.")

    # Image 3: Office photo
    img_rect3 = pymupdf.Rect(72, 185, 340, 400)
    page.insert_image(img_rect3, filename=os.path.join(img_dir, 'photo_office.png'))

    add_text(page, 72, 415, "Figure 3: Meridian Technologies Global HQ, Austin TX", fontsize=9, color=(0.3, 0.3, 0.3))

    add_paragraph(page, pymupdf.Rect(72, 435, 523, 510),
        "The company completed a $180 million campus expansion project at our Austin headquarters, "
        "adding 240,000 square feet of office and laboratory space. The new facilities include a "
        "dedicated AI research lab, an expanded customer briefing center, and sustainability-focused "
        "infrastructure achieving LEED Platinum certification.")

    # Image 4: Workflow diagram
    img_rect4 = pymupdf.Rect(100, 525, 500, 780)
    page.insert_image(img_rect4, filename=os.path.join(img_dir, 'diagram_workflow.png'))

    add_text(page, 100, 795, "Figure 4: Integrated Product Development Workflow", fontsize=9, color=(0.3, 0.3, 0.3))

    # ==================== PAGE 3: Growth & Team ====================
    page = doc.new_page(width=595, height=842)
    add_text(page, 72, 55, "Growth Metrics & Leadership", fontsize=16, bold=True, color=(0.1, 0.15, 0.4))

    add_paragraph(page, pymupdf.Rect(72, 75, 523, 150),
        "Meridian's growth trajectory accelerated in H2 2025, fueled by the launch of MeridianAI "
        "and strategic partnerships with three Fortune 100 companies. Customer retention remained "
        "strong at 94.3%, while net revenue retention reached 118%, indicating significant expansion "
        "within existing accounts.")

    # Image 5: Growth chart
    img_rect5 = pymupdf.Rect(72, 165, 523, 430)
    page.insert_image(img_rect5, filename=os.path.join(img_dir, 'chart_growth.png'))

    add_text(page, 72, 445, "Figure 5: Year-over-Year Growth Rates by Division", fontsize=9, color=(0.3, 0.3, 0.3))

    add_text(page, 72, 475, "Leadership Team", fontsize=14, bold=True, color=(0.1, 0.15, 0.4))

    add_paragraph(page, pymupdf.Rect(72, 495, 523, 555),
        "In 2025, the executive team was strengthened with the appointments of Dr. Priya Sharma "
        "as Chief Technology Officer and David Kim as Chief Revenue Officer. Both bring extensive "
        "experience from leading technology companies and have already made significant contributions "
        "to our product and go-to-market strategies.")

    # Image 6: Team photo
    img_rect6 = pymupdf.Rect(90, 570, 505, 810)
    page.insert_image(img_rect6, filename=os.path.join(img_dir, 'photo_team.png'))

    add_text(page, 90, 825, "Figure 6: Executive Leadership Team at Annual Strategy Summit", fontsize=9, color=(0.3, 0.3, 0.3))

    # ==================== PAGE 4: Market Analysis ====================
    page = doc.new_page(width=595, height=842)
    add_text(page, 72, 55, "Market Analysis", fontsize=16, bold=True, color=(0.1, 0.15, 0.4))

    add_paragraph(page, pymupdf.Rect(72, 75, 523, 155),
        "The enterprise software market continued its robust growth in 2025, expanding to $685 billion "
        "globally. Meridian maintained its position as a top-5 vendor in the cloud infrastructure "
        "management segment, with an estimated 8.2% market share. The competitive landscape saw "
        "increased consolidation, with three major acquisitions reshaping the industry.")

    # Image 7: Market chart
    img_rect7 = pymupdf.Rect(72, 170, 523, 460)
    page.insert_image(img_rect7, filename=os.path.join(img_dir, 'chart_market.png'))

    add_text(page, 72, 475, "Figure 7: Market Share by Major Vendor (Cloud Infrastructure)", fontsize=9, color=(0.3, 0.3, 0.3))

    add_text(page, 72, 505, "Organizational Development", fontsize=14, bold=True, color=(0.1, 0.15, 0.4))

    add_paragraph(page, pymupdf.Rect(72, 525, 523, 580),
        "Our organization underwent a strategic restructuring to better align with customer needs "
        "and market opportunities. Four business units were consolidated into three focused divisions.")

    # Image 8: Org diagram
    img_rect8 = pymupdf.Rect(80, 595, 515, 810)
    page.insert_image(img_rect8, filename=os.path.join(img_dir, 'diagram_org.png'))

    add_text(page, 80, 825, "Figure 8: Revised Organizational Structure (effective Q3 2025)", fontsize=9, color=(0.3, 0.3, 0.3))

    # ==================== PAGE 5: Products & Customer Satisfaction ====================
    page = doc.new_page(width=595, height=842)
    add_text(page, 72, 55, "Product Portfolio & Customer Insights", fontsize=16, bold=True, color=(0.1, 0.15, 0.4))

    add_paragraph(page, pymupdf.Rect(72, 75, 523, 140),
        "Meridian's product portfolio expanded with the introduction of five new products and "
        "significant upgrades to twelve existing offerings. The MeridianAI platform emerged as "
        "the fastest-growing product in company history, reaching $180 million ARR within nine "
        "months of launch.")

    # Image 9: Product photo
    img_rect9 = pymupdf.Rect(72, 155, 380, 380)
    page.insert_image(img_rect9, filename=os.path.join(img_dir, 'photo_product.png'))

    add_text(page, 72, 395, "Figure 9: Meridian Product Line at TechExpo 2025", fontsize=9, color=(0.3, 0.3, 0.3))

    add_text(page, 72, 425, "Customer Satisfaction", fontsize=14, bold=True, color=(0.1, 0.15, 0.4))

    add_paragraph(page, pymupdf.Rect(72, 445, 523, 510),
        "Customer satisfaction scores reached their highest levels in company history, with an "
        "overall NPS of 72 (up from 65 in 2024). Enterprise customers reported the highest "
        "satisfaction, with 91% rating Meridian as 'excellent' or 'very good' in the annual survey.")

    # Image 10: Satisfaction chart
    img_rect10 = pymupdf.Rect(100, 525, 500, 810)
    page.insert_image(img_rect10, filename=os.path.join(img_dir, 'chart_satisfaction.png'))

    add_text(page, 100, 825, "Figure 10: Customer Satisfaction Trends (2021-2025)", fontsize=9, color=(0.3, 0.3, 0.3))

    # ==================== PAGE 6: Outlook ====================
    page = doc.new_page(width=595, height=842)
    add_text(page, 72, 55, "Forward-Looking Outlook", fontsize=16, bold=True, color=(0.1, 0.15, 0.4))

    add_paragraph(page, pymupdf.Rect(72, 75, 523, 200),
        "Looking ahead to fiscal year 2026, Meridian Technologies is positioned for continued "
        "strong growth. Management has set a revenue target of $4.8-5.0 billion, representing "
        "14-19% growth. Key strategic priorities include: expanding the AI product portfolio, "
        "deepening partnerships in the healthcare and financial services verticals, and achieving "
        "carbon neutrality across all global operations by Q4 2026. Capital expenditure is "
        "projected at $320 million, primarily for data center expansion in North America and Europe.")

    # Image 11: Forecast chart
    img_rect11 = pymupdf.Rect(72, 215, 523, 500)
    page.insert_image(img_rect11, filename=os.path.join(img_dir, 'chart_forecast.png'))

    add_text(page, 72, 515, "Figure 11: Three-Year Financial Forecast (Revenue & EBITDA)", fontsize=9, color=(0.3, 0.3, 0.3))

    add_paragraph(page, pymupdf.Rect(72, 540, 523, 650),
        "The board of directors has approved a $500 million share repurchase program and a 15% "
        "increase in the quarterly dividend, reflecting confidence in the company's cash flow "
        "generation and long-term growth prospects. Total shareholder return for 2025 was 41%, "
        "significantly outperforming the S&P 500 Information Technology index.")

    add_text(page, 72, 680, "Disclaimer", fontsize=10, bold=True, color=(0.4, 0.4, 0.4))
    add_paragraph(page, pymupdf.Rect(72, 695, 523, 780),
        "This report contains forward-looking statements that involve risks and uncertainties. "
        "Actual results may differ materially from those projected. Meridian Technologies "
        "undertakes no obligation to update any forward-looking statements. This document is "
        "intended for informational purposes only and does not constitute investment advice.",
        fontsize=8)

    # Save
    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify
    verify_doc = pymupdf.open(OUTPUT)
    total_images = sum(len(p.get_images()) for p in verify_doc)
    print(f'Pages: {verify_doc.page_count}, Total images: {total_images}')
    verify_doc.close()

    # GUI-ready: open PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
