"""
Initial Setup: Create survey_results.pdf (10 pages) on the Desktop.
Task ID: pdf_basic_068
Domain: pdf

Creates:
  ~/Desktop/survey_results.pdf  — 10 pages, page 2 contains a data table

The agent must:
  1. Open survey_results.pdf in Evince
  2. Select and copy the text from the table on page 2
  3. Paste it into ~/Desktop/survey_table.txt

Opens survey_results.pdf in Evince for the GUI agent to start with.
"""

import os
import shlex
import subprocess
import time

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

DESKTOP_DIR = os.path.expanduser("~/Desktop")
PDF_PATH = os.path.join(DESKTOP_DIR, "survey_results.pdf")

A4_W, A4_H = 595, 842


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


def add_page_header(page, title, page_num, total_pages):
    """Add a standard header to a page."""
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 0, A4_W, 50))
    shape.finish(fill=(0.15, 0.30, 0.55), color=None)
    shape.commit()

    page.insert_text(
        pymupdf.Point(40, 20),
        "Customer Experience Survey Report 2024",
        fontsize=10,
        fontname="hebo",
        color=(0.95, 0.95, 0.95),
    )
    page.insert_text(
        pymupdf.Point(40, 38),
        f"{title}  |  Page {page_num} of {total_pages}",
        fontsize=8,
        fontname="helv",
        color=(0.80, 0.85, 0.95),
    )

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(40, 60), pymupdf.Point(555, 60))
    shape.finish(color=(0.55, 0.60, 0.75), width=0.5)
    shape.commit()


def add_page_footer(page):
    """Add a standard footer to a page."""
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 825, A4_W, A4_H))
    shape.finish(fill=(0.15, 0.30, 0.55), color=None)
    shape.commit()
    page.insert_text(
        pymupdf.Point(200, 836),
        "Confidential — Internal Use Only",
        fontsize=7,
        fontname="helv",
        color=(0.85, 0.88, 0.95),
    )


def create_page1(doc):
    """Page 1: Executive Summary / Introduction"""
    page = doc.new_page(width=A4_W, height=A4_H)
    add_page_header(page, "Executive Summary", 1, 10)
    add_page_footer(page)

    page.insert_text(
        pymupdf.Point(40, 80),
        "Executive Summary",
        fontsize=15,
        fontname="hebo",
        color=(0.15, 0.30, 0.55),
    )

    body = [
        "This report presents the findings of the 2024 Customer Experience Survey conducted",
        "across all major product lines. A total of 1,247 respondents participated in the",
        "survey between January and March 2024.",
        "",
        "The survey aimed to assess customer satisfaction, product usability, support quality,",
        "and overall brand perception. Results are aggregated across five key dimensions:",
        "Satisfaction, Usability, Support, Value, and Loyalty.",
        "",
        "Key findings:",
        "  • Overall satisfaction score: 4.2 / 5.0 (up from 3.9 in 2023)",
        "  • Net Promoter Score: 48 (industry benchmark: 35)",
        "  • Top strength: Product reliability (rated 4.5 / 5.0)",
        "  • Top improvement area: Onboarding experience (rated 3.6 / 5.0)",
        "",
        "Detailed breakdowns by product line and customer segment are provided in the",
        "following sections. Statistical significance was assessed at the 95% confidence level.",
    ]

    y = 110
    for line in body:
        page.insert_text(
            pymupdf.Point(40, y),
            line,
            fontsize=10,
            fontname="helv",
            color=(0.08, 0.08, 0.08),
        )
        y += 16


def create_page2_with_table(doc):
    """Page 2: Survey Results by Product Line (data table)"""
    page = doc.new_page(width=A4_W, height=A4_H)
    add_page_header(page, "Survey Results by Product Line", 2, 10)
    add_page_footer(page)

    page.insert_text(
        pymupdf.Point(40, 78),
        "Survey Results by Product Line",
        fontsize=14,
        fontname="hebo",
        color=(0.15, 0.30, 0.55),
    )

    page.insert_text(
        pymupdf.Point(40, 100),
        "Table 1: Mean satisfaction scores by product line (scale 1–5)",
        fontsize=9,
        fontname="tiit",
        color=(0.35, 0.35, 0.45),
    )

    # -----------------------------------------------------------------------
    # Draw the table
    # -----------------------------------------------------------------------
    TABLE_DATA = [
        # (Product Line, Satisfaction, Usability, Support, Value, Loyalty, N)
        ("Product Line",      "Satisfaction", "Usability", "Support", "Value", "Loyalty", "N"),
        ("CRM Pro",           "4.3",          "4.1",       "4.4",     "4.0",   "4.2",     "312"),
        ("Analytics Suite",   "4.1",          "3.9",       "4.2",     "3.8",   "3.9",     "278"),
        ("Mobile App",        "4.5",          "4.4",       "4.3",     "4.3",   "4.6",     "195"),
        ("Enterprise Portal", "3.8",          "3.6",       "4.0",     "3.7",   "3.7",     "214"),
        ("Data Connector",    "4.0",          "3.8",       "4.1",     "3.9",   "3.8",     "148"),
        ("Support Hub",       "4.4",          "4.2",       "4.6",     "4.2",   "4.3",     "100"),
        ("All Products",      "4.2",          "4.0",       "4.3",     "4.0",   "4.1",     "1247"),
    ]

    col_widths = [120, 65, 62, 55, 50, 55, 45]  # total ~452
    col_x = [40]
    for w in col_widths[:-1]:
        col_x.append(col_x[-1] + w)

    row_height = 22
    table_top = 118

    for row_idx, row in enumerate(TABLE_DATA):
        y_top = table_top + row_idx * row_height
        y_bottom = y_top + row_height

        # Row background
        shape = page.new_shape()
        if row_idx == 0:
            bg_color = (0.15, 0.30, 0.55)  # dark header
        elif row_idx == len(TABLE_DATA) - 1:
            bg_color = (0.88, 0.90, 0.95)  # totals row
        elif row_idx % 2 == 0:
            bg_color = (0.96, 0.96, 0.98)  # alternate row
        else:
            bg_color = (1.0, 1.0, 1.0)
        shape.draw_rect(pymupdf.Rect(40, y_top, 40 + sum(col_widths), y_bottom))
        shape.finish(fill=bg_color, color=(0.70, 0.70, 0.80), width=0.4)
        shape.commit()

        text_color = (0.95, 0.95, 0.95) if row_idx == 0 else (0.08, 0.08, 0.08)
        font = "hebo" if row_idx in (0, len(TABLE_DATA) - 1) else "helv"

        for col_idx, (cell_text, cx, cw) in enumerate(zip(row, col_x, col_widths)):
            align_x = cx + 5 if col_idx == 0 else cx + cw // 2 - len(cell_text) * 2.8
            page.insert_text(
                pymupdf.Point(align_x, y_top + 15),
                cell_text,
                fontsize=9,
                fontname=font,
                color=text_color,
            )

    # Vertical column dividers
    table_bottom = table_top + len(TABLE_DATA) * row_height
    shape = page.new_shape()
    for cx in col_x[1:]:
        shape.draw_line(pymupdf.Point(cx, table_top), pymupdf.Point(cx, table_bottom))
    shape.finish(color=(0.70, 0.70, 0.80), width=0.4)
    shape.commit()

    # Caption / note below the table
    caption_y = table_bottom + 12
    page.insert_text(
        pymupdf.Point(40, caption_y),
        "Note: Scores represent arithmetic means. N = number of valid responses per product line.",
        fontsize=8,
        fontname="tiit",
        color=(0.40, 0.40, 0.50),
    )

    # Additional commentary below
    page.insert_text(
        pymupdf.Point(40, caption_y + 20),
        "The Mobile App recorded the highest overall satisfaction (4.5) and loyalty (4.6) scores,",
        fontsize=10,
        fontname="helv",
        color=(0.08, 0.08, 0.08),
    )
    page.insert_text(
        pymupdf.Point(40, caption_y + 36),
        "while the Enterprise Portal received the lowest satisfaction (3.8) and usability (3.6)",
        fontsize=10,
        fontname="helv",
        color=(0.08, 0.08, 0.08),
    )
    page.insert_text(
        pymupdf.Point(40, caption_y + 52),
        "ratings, indicating a priority area for the product team in the coming quarter.",
        fontsize=10,
        fontname="helv",
        color=(0.08, 0.08, 0.08),
    )


def create_page3(doc):
    """Page 3: Satisfaction Trends"""
    page = doc.new_page(width=A4_W, height=A4_H)
    add_page_header(page, "Satisfaction Trends", 3, 10)
    add_page_footer(page)

    page.insert_text(
        pymupdf.Point(40, 80),
        "Year-on-Year Satisfaction Trends",
        fontsize=14,
        fontname="hebo",
        color=(0.15, 0.30, 0.55),
    )

    body = [
        "Overall satisfaction scores have improved consistently over the past three years.",
        "The table below shows mean satisfaction scores from 2022 to 2024:",
        "",
        "  Year      Score     Respondents",
        "  2022      3.7       892",
        "  2023      3.9       1,041",
        "  2024      4.2       1,247",
        "",
        "The 0.3-point improvement from 2023 to 2024 is statistically significant (p < 0.01)",
        "and reflects the impact of the product improvements shipped in H2 2023.",
        "",
        "Segment-level trends show that Enterprise customers (+0.4) and SMB customers (+0.3)",
        "both improved substantially, while the Mid-Market segment showed modest improvement (+0.1).",
        "",
        "Areas with the strongest year-on-year improvement:",
        "  • Product reliability: +0.4 (3.9 → 4.3 → 4.5) [significant]",
        "  • Support responsiveness: +0.3 (3.8 → 4.0 → 4.3) [significant]",
        "  • Documentation quality: +0.2 (3.4 → 3.6 → 3.8) [moderate]",
    ]

    y = 110
    for line in body:
        page.insert_text(pymupdf.Point(40, y), line, fontsize=10, fontname="helv",
                         color=(0.08, 0.08, 0.08))
        y += 16


def create_page4(doc):
    """Page 4: NPS Analysis"""
    page = doc.new_page(width=A4_W, height=A4_H)
    add_page_header(page, "Net Promoter Score Analysis", 4, 10)
    add_page_footer(page)

    page.insert_text(pymupdf.Point(40, 80), "Net Promoter Score Analysis",
                     fontsize=14, fontname="hebo", color=(0.15, 0.30, 0.55))

    body = [
        "The 2024 NPS stands at 48, up from 38 in 2023. This places ACME Corp in the",
        "'Excellent' tier for B2B software (benchmark: 35).",
        "",
        "NPS distribution:",
        "  Promoters (9–10):  42%  (524 respondents)",
        "  Passives  (7–8):   34%  (424 respondents)",
        "  Detractors (0–6):  24%  (299 respondents)",
        "",
        "Primary reasons cited by promoters: product reliability, customer support quality,",
        "and the breadth of integrations available.",
        "",
        "Primary reasons cited by detractors: onboarding complexity, pricing transparency,",
        "and speed of new feature delivery.",
        "",
        "NPS by tenure:",
        "  < 1 year:   32  (newest customers — onboarding friction visible)",
        "  1–3 years:  51  (established customers — highest satisfaction)",
        "  3+ years:   58  (long-term customers — strong advocates)",
    ]

    y = 110
    for line in body:
        page.insert_text(pymupdf.Point(40, y), line, fontsize=10, fontname="helv",
                         color=(0.08, 0.08, 0.08))
        y += 16


def create_page5(doc):
    """Page 5: Usability Findings"""
    page = doc.new_page(width=A4_W, height=A4_H)
    add_page_header(page, "Usability Findings", 5, 10)
    add_page_footer(page)

    page.insert_text(pymupdf.Point(40, 80), "Usability Findings",
                     fontsize=14, fontname="hebo", color=(0.15, 0.30, 0.55))

    body = [
        "Usability was assessed across five dimensions: navigation, learnability,",
        "efficiency, error recovery, and satisfaction.",
        "",
        "Mean usability score: 4.0 / 5.0 (up from 3.8 in 2023)",
        "",
        "Top usability strengths:",
        "  • Navigation clarity: 4.3 / 5.0",
        "  • Search functionality: 4.2 / 5.0",
        "  • Dashboard customisation: 4.1 / 5.0",
        "",
        "Top usability improvement areas:",
        "  • Onboarding wizard: 3.4 / 5.0",
        "  • Bulk operation support: 3.5 / 5.0",
        "  • Mobile responsiveness: 3.7 / 5.0",
        "",
        "Open-ended feedback (common themes in usability comments):",
        "  'The dashboard is clean and easy to navigate once set up.'",
        "  'Onboarding took longer than expected. More guided tutorials would help.'",
        "  'The bulk import tool is powerful but not intuitive.'",
    ]

    y = 110
    for line in body:
        page.insert_text(pymupdf.Point(40, y), line, fontsize=10, fontname="helv",
                         color=(0.08, 0.08, 0.08))
        y += 16


def create_page6(doc):
    """Page 6: Support Quality"""
    page = doc.new_page(width=A4_W, height=A4_H)
    add_page_header(page, "Support Quality", 6, 10)
    add_page_footer(page)

    page.insert_text(pymupdf.Point(40, 80), "Support Quality Assessment",
                     fontsize=14, fontname="hebo", color=(0.15, 0.30, 0.55))

    body = [
        "Support quality received the highest mean score of all dimensions at 4.3 / 5.0.",
        "Customers consistently praised the responsiveness and technical depth of the team.",
        "",
        "Support satisfaction by channel:",
        "  Live chat:    4.6 / 5.0  (most preferred by SMB customers)",
        "  Phone:        4.4 / 5.0  (preferred by Enterprise customers)",
        "  Email:        4.1 / 5.0  (slowest; opportunities for improvement)",
        "  Help centre:  3.9 / 5.0  (documentation completeness flagged)",
        "",
        "Key support metrics from operational data (Q1 2024):",
        "  Median first response time (live chat): 42 seconds",
        "  Median first response time (email): 3.2 hours",
        "  First contact resolution rate: 74%",
        "  CSAT after resolved ticket: 4.5 / 5.0",
        "",
        "Recommendation: Expand help centre content and add video tutorials to raise",
        "the self-service satisfaction score towards 4.3 by Q4 2024.",
    ]

    y = 110
    for line in body:
        page.insert_text(pymupdf.Point(40, y), line, fontsize=10, fontname="helv",
                         color=(0.08, 0.08, 0.08))
        y += 16


def create_page7(doc):
    """Page 7: Value for Money"""
    page = doc.new_page(width=A4_W, height=A4_H)
    add_page_header(page, "Value for Money", 7, 10)
    add_page_footer(page)

    page.insert_text(pymupdf.Point(40, 80), "Value for Money Perception",
                     fontsize=14, fontname="hebo", color=(0.15, 0.30, 0.55))

    body = [
        "Value perception averaged 4.0 / 5.0 across all respondents.",
        "This dimension showed the widest variance across customer segments:",
        "",
        "Value score by segment:",
        "  Enterprise (500+ employees):   4.2 / 5.0",
        "  Mid-Market (50–499 employees): 3.9 / 5.0",
        "  SMB (< 50 employees):          3.7 / 5.0",
        "",
        "SMB customers most often cited pricing as a concern. Key verbatim themes:",
        "  'Great product but the price point is challenging for a small team.'",
        "  'The value is there if you use all features, but we only use half.'",
        "",
        "Improvement opportunities:",
        "  • Introduce a starter tier with limited features at lower price point",
        "  • Provide clearer ROI calculators on the pricing page",
        "  • Create case studies demonstrating ROI for SMB customers",
        "",
        "Customers with 3+ integrations active rated value 0.4 points higher than",
        "those with 0–1 integrations, suggesting integration depth drives perceived value.",
    ]

    y = 110
    for line in body:
        page.insert_text(pymupdf.Point(40, y), line, fontsize=10, fontname="helv",
                         color=(0.08, 0.08, 0.08))
        y += 16


def create_page8(doc):
    """Page 8: Loyalty and Retention"""
    page = doc.new_page(width=A4_W, height=A4_H)
    add_page_header(page, "Loyalty and Retention", 8, 10)
    add_page_footer(page)

    page.insert_text(pymupdf.Point(40, 80), "Loyalty and Retention Indicators",
                     fontsize=14, fontname="hebo", color=(0.15, 0.30, 0.55))

    body = [
        "Loyalty score averaged 4.1 / 5.0. Survey data correlates strongly with",
        "operational retention metrics (Pearson r = 0.82).",
        "",
        "Renewal intent by loyalty score:",
        "  Loyalty 4.5–5.0:  94% renewal intent",
        "  Loyalty 3.5–4.4:  78% renewal intent",
        "  Loyalty 2.5–3.4:  52% renewal intent",
        "  Loyalty < 2.5:    21% renewal intent",
        "",
        "Key drivers of loyalty (regression analysis):",
        "  1. Support quality (β = 0.41) — strongest predictor",
        "  2. Product reliability (β = 0.38)",
        "  3. Onboarding experience (β = 0.29)",
        "  4. Value perception (β = 0.24)",
        "",
        "Customers who completed the onboarding programme had 18% higher loyalty",
        "scores than those who self-configured. This reinforces investment in onboarding.",
    ]

    y = 110
    for line in body:
        page.insert_text(pymupdf.Point(40, y), line, fontsize=10, fontname="helv",
                         color=(0.08, 0.08, 0.08))
        y += 16


def create_page9(doc):
    """Page 9: Competitive Positioning"""
    page = doc.new_page(width=A4_W, height=A4_H)
    add_page_header(page, "Competitive Positioning", 9, 10)
    add_page_footer(page)

    page.insert_text(pymupdf.Point(40, 80), "Competitive Positioning",
                     fontsize=14, fontname="hebo", color=(0.15, 0.30, 0.55))

    body = [
        "Survey respondents who had evaluated or used competing products were asked",
        "to compare ACME Corp's offerings. 34% of respondents (n = 424) qualified.",
        "",
        "Competitive win/loss drivers cited by respondents:",
        "",
        "Why customers chose ACME over competitors:",
        "  • Integration ecosystem (cited by 58%)",
        "  • Customer support quality (cited by 51%)",
        "  • Ease of onboarding compared to alternatives (cited by 39%)",
        "  • API flexibility (cited by 37%)",
        "",
        "Why customers considered switching to a competitor:",
        "  • Price/feature ratio of alternatives (cited by 44%)",
        "  • Specific missing feature in ACME product (cited by 38%)",
        "  • Competitor brand perception (cited by 22%)",
        "",
        "ACME's competitive differentiation remains strongest in support and integrations.",
        "The product team should prioritise closing the feature gap to reduce churn risk.",
    ]

    y = 110
    for line in body:
        page.insert_text(pymupdf.Point(40, y), line, fontsize=10, fontname="helv",
                         color=(0.08, 0.08, 0.08))
        y += 16


def create_page10(doc):
    """Page 10: Recommendations and Next Steps"""
    page = doc.new_page(width=A4_W, height=A4_H)
    add_page_header(page, "Recommendations", 10, 10)
    add_page_footer(page)

    page.insert_text(pymupdf.Point(40, 80), "Recommendations and Next Steps",
                     fontsize=14, fontname="hebo", color=(0.15, 0.30, 0.55))

    body = [
        "Based on survey findings, the following actions are recommended:",
        "",
        "Priority 1 — Onboarding Improvement (Impact: High, Effort: Medium)",
        "  • Build an interactive guided setup wizard for new accounts",
        "  • Create a library of product tour videos (target: 20 videos by Q3)",
        "  • Assign a dedicated customer success manager for first 90 days",
        "",
        "Priority 2 — Enterprise Portal Usability (Impact: High, Effort: High)",
        "  • Commission user research study with 10 Enterprise Portal customers",
        "  • Redesign the main navigation based on user research findings",
        "  • Target: raise usability score from 3.6 to 4.0 by Q4 2024",
        "",
        "Priority 3 — SMB Value Perception (Impact: Medium, Effort: Low)",
        "  • Launch a Starter tier at a competitive price point",
        "  • Publish 5 SMB-focused ROI case studies by end of Q2",
        "",
        "Priority 4 — Help Centre Enhancement (Impact: Medium, Effort: Low)",
        "  • Audit existing help articles for accuracy and completeness",
        "  • Add contextual help links from within the product interface",
        "",
        "Success metrics: re-survey cohort in Q4 2024; target overall score of 4.4.",
    ]

    y = 110
    for line in body:
        page.insert_text(pymupdf.Point(40, y), line, fontsize=10, fontname="helv",
                         color=(0.08, 0.08, 0.08))
        y += 15


def create_initial():
    os.makedirs(DESKTOP_DIR, exist_ok=True)

    doc = pymupdf.open()

    create_page1(doc)
    create_page2_with_table(doc)
    create_page3(doc)
    create_page4(doc)
    create_page5(doc)
    create_page6(doc)
    create_page7(doc)
    create_page8(doc)
    create_page9(doc)
    create_page10(doc)

    assert doc.page_count == 10, f"Expected 10 pages, got {doc.page_count}"
    doc.save(PDF_PATH)
    doc.close()
    print(f"Created: {PDF_PATH}  (10 pages)")

    # Open in Evince for the GUI agent
    launch_gui(f'evince "{PDF_PATH}"', delay_sec=2.0)
    print("GUI_READY: opened survey_results.pdf in Evince with DISPLAY=:0")


create_initial()
