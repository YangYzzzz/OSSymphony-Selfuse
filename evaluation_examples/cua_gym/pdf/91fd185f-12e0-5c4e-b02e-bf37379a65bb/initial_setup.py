"""
Initial Setup: Create a mixed-size PDF with Letter, Legal, and A3 pages
Task ID: pdf_ro_037
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_037'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/mixed_sizes.pdf'

# Page size constants (points)
LETTER_W, LETTER_H = 612, 792
LEGAL_W, LEGAL_H = 612, 1008
A3_W, A3_H = 842, 1190


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


def add_page_content(page, page_num, size_label, width, height):
    """Add realistic content to a page based on its size and number."""

    # Page title
    page.insert_text(
        pymupdf.Point(50, 50),
        f"Meridian Consulting Group - {size_label} Format",
        fontsize=18,
        fontname="hebo",
        color=(0.1, 0.1, 0.4),
    )

    # Subtitle with page number
    page.insert_text(
        pymupdf.Point(50, 80),
        f"Document Section {page_num} of 15",
        fontsize=12,
        fontname="heit",
        color=(0.4, 0.4, 0.4),
    )

    # Horizontal line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(50, 95), pymupdf.Point(width - 50, 95))
    shape.finish(color=(0.2, 0.2, 0.6), width=1.5)
    shape.commit()

    # Content varies by page number to make each page unique
    content_sets = [
        {
            "heading": "Executive Summary - Q4 Financial Review",
            "body": (
                "The fourth quarter of fiscal year 2025 demonstrated robust growth across all "
                "business segments. Total revenue reached $4.82 million, representing a 12.3% "
                "increase over Q3 figures. The consulting division led performance with $2.1M "
                "in billings, followed by technology services at $1.6M and strategic advisory "
                "at $1.12M. Operating margins improved to 23.4% from 21.7% in the prior quarter, "
                "driven primarily by efficiency gains in project delivery and reduced overhead costs."
            ),
            "table_data": [
                ["Department", "Revenue", "Growth", "Headcount"],
                ["Consulting", "$2,100,000", "+14.2%", "45"],
                ["Technology", "$1,600,000", "+11.8%", "38"],
                ["Advisory", "$1,120,000", "+9.5%", "22"],
            ],
        },
        {
            "heading": "Client Portfolio Analysis",
            "body": (
                "Our client retention rate for the period stood at 94.7%, exceeding the industry "
                "benchmark of 88%. Key accounts including Blackrock Industries, Vertex Healthcare, "
                "and Pinnacle Financial Services renewed multi-year engagements totaling $3.2M in "
                "committed revenue. New client acquisitions included Horizon Aerospace (projected "
                "$450K annual), BlueCrest Manufacturing ($320K annual), and Evergreen Logistics "
                "($280K annual). The pipeline contains 23 qualified opportunities valued at $6.1M."
            ),
            "table_data": [
                ["Client", "Contract Value", "Start Date", "Status"],
                ["Blackrock Industries", "$1,200,000", "2024-01-15", "Active"],
                ["Vertex Healthcare", "$980,000", "2024-03-01", "Active"],
                ["Pinnacle Financial", "$850,000", "2024-06-10", "Active"],
                ["Horizon Aerospace", "$450,000", "2025-01-20", "New"],
            ],
        },
        {
            "heading": "Human Resources & Talent Metrics",
            "body": (
                "Total headcount reached 105 full-time employees, with 12 new hires during Q4. "
                "Employee satisfaction scores averaged 4.3 out of 5.0, with the highest ratings "
                "in professional development (4.6) and team collaboration (4.5). Voluntary turnover "
                "declined to 6.2% annualized, well below the consulting industry average of 15%. "
                "The learning and development budget was utilized at 87% capacity, with 340 training "
                "hours logged across the organization."
            ),
            "table_data": [
                ["Metric", "Q3 2025", "Q4 2025", "Target"],
                ["Headcount", "98", "105", "110"],
                ["Satisfaction", "4.1", "4.3", "4.5"],
                ["Turnover Rate", "7.8%", "6.2%", "<8%"],
                ["Training Hours", "285", "340", "300"],
            ],
        },
        {
            "heading": "Technology Infrastructure Report",
            "body": (
                "System uptime averaged 99.94% across all production environments during Q4. "
                "The cloud migration project completed Phase 2, moving 78% of workloads to AWS. "
                "Cybersecurity assessments identified zero critical vulnerabilities. The new CRM "
                "platform (Salesforce Enterprise) deployment reached 92% user adoption within "
                "six weeks of launch. IT support ticket resolution time improved to 4.2 hours "
                "average, down from 6.8 hours in Q3."
            ),
            "table_data": [
                ["System", "Uptime", "Incidents", "Response Time"],
                ["Production Servers", "99.97%", "2", "12 min"],
                ["Database Cluster", "99.99%", "0", "N/A"],
                ["Email Services", "99.91%", "4", "23 min"],
                ["CRM Platform", "99.88%", "3", "18 min"],
            ],
        },
        {
            "heading": "Project Delivery Performance",
            "body": (
                "Thirty-seven projects were completed during Q4, with 89% delivered on time and "
                "92% within budget. Average project profitability was 31.2%, exceeding the 28% "
                "target. Client satisfaction surveys returned a mean score of 4.4 out of 5.0. "
                "Notable completions included the Vertex Healthcare digital transformation "
                "($420K, 6 months), Blackrock risk assessment framework ($280K, 4 months), "
                "and Pinnacle regulatory compliance overhaul ($195K, 3 months)."
            ),
            "table_data": [
                ["Project", "Budget", "Duration", "Satisfaction"],
                ["Vertex Digital Transform", "$420,000", "6 months", "4.6"],
                ["Blackrock Risk Framework", "$280,000", "4 months", "4.3"],
                ["Pinnacle Compliance", "$195,000", "3 months", "4.5"],
                ["BlueCrest ERP Integration", "$310,000", "5 months", "4.2"],
            ],
        },
    ]

    # Select content set based on page number (cycle through 5 sets for 15 pages)
    content = content_sets[(page_num - 1) % 5]

    # Section heading
    page.insert_text(
        pymupdf.Point(50, 130),
        content["heading"],
        fontsize=15,
        fontname="hebo",
        color=(0.15, 0.15, 0.15),
    )

    # Body text in a textbox
    text_rect = pymupdf.Rect(50, 155, width - 50, 350)
    page.insert_textbox(
        text_rect,
        content["body"],
        fontsize=10.5,
        fontname="helv",
        color=(0.1, 0.1, 0.1),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Draw a simple table
    table_top = 370
    col_widths = [(width - 100) / len(content["table_data"][0])] * len(content["table_data"][0])
    row_height = 24

    shape2 = page.new_shape()
    for r, row in enumerate(content["table_data"]):
        y = table_top + r * row_height
        for c, cell in enumerate(row):
            x = 50 + sum(col_widths[:c])
            cell_rect = pymupdf.Rect(x, y, x + col_widths[c], y + row_height)

            # Header row background
            if r == 0:
                shape2.draw_rect(cell_rect)
                shape2.finish(color=(0.2, 0.2, 0.5), fill=(0.2, 0.2, 0.5), width=0.5)
            else:
                shape2.draw_rect(cell_rect)
                bg = (0.95, 0.95, 0.98) if r % 2 == 0 else (1, 1, 1)
                shape2.finish(color=(0.7, 0.7, 0.7), fill=bg, width=0.5)

    shape2.commit()

    # Table text
    for r, row in enumerate(content["table_data"]):
        y = table_top + r * row_height
        for c, cell in enumerate(row):
            x = 50 + sum(col_widths[:c])
            text_color = (1, 1, 1) if r == 0 else (0.1, 0.1, 0.1)
            font = "hebo" if r == 0 else "helv"
            page.insert_text(
                pymupdf.Point(x + 5, y + 16),
                str(cell),
                fontsize=9,
                fontname=font,
                color=text_color,
            )

    # Footer
    page.insert_text(
        pymupdf.Point(50, height - 40),
        f"Meridian Consulting Group  |  Confidential  |  Page {page_num}",
        fontsize=8,
        fontname="heit",
        color=(0.5, 0.5, 0.5),
    )

    # Additional content for larger pages (Legal and A3)
    if height > 800:
        extra_y = 500
        page.insert_text(
            pymupdf.Point(50, extra_y),
            "Additional Analysis Notes",
            fontsize=13,
            fontname="hebo",
            color=(0.15, 0.15, 0.15),
        )
        extra_text = (
            "This section provides supplementary analysis and contextual information relevant "
            "to the data presented above. Market conditions during Q4 2025 were characterized by "
            "moderate economic growth (GDP +2.4%), stable interest rates, and increasing demand for "
            "digital transformation services across all industry verticals. Our competitive position "
            "strengthened with the expansion of AI-driven analytics capabilities and the launch of "
            "our sustainability consulting practice. Regional performance varied, with the Northeast "
            "corridor accounting for 42% of revenue, followed by the West Coast at 28%, Midwest "
            "at 18%, and Southeast at 12%."
        )
        text_rect2 = pymupdf.Rect(50, extra_y + 25, width - 50, extra_y + 200)
        page.insert_textbox(
            text_rect2,
            extra_text,
            fontsize=10,
            fontname="helv",
            color=(0.1, 0.1, 0.1),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

    # Even more content for A3 pages
    if height > 1000:
        a3_y = 720
        page.insert_text(
            pymupdf.Point(50, a3_y),
            "Extended Regional Breakdown",
            fontsize=13,
            fontname="hebo",
            color=(0.15, 0.15, 0.15),
        )
        regional_text = (
            "The Northeast corridor, anchored by our Boston and New York offices, continued to "
            "generate the largest share of consulting revenue at $2.02M. Key drivers included "
            "financial services modernization projects and healthcare system integrations. The "
            "West Coast operations, centered in San Francisco and Seattle, contributed $1.35M "
            "with strong growth in technology sector engagements. Our Chicago-based Midwest team "
            "delivered $868K in revenue, while the Atlanta-led Southeast practice generated $578K "
            "with promising growth in manufacturing and logistics verticals."
        )
        text_rect3 = pymupdf.Rect(50, a3_y + 25, width - 50, a3_y + 250)
        page.insert_textbox(
            text_rect3,
            regional_text,
            fontsize=10,
            fontname="helv",
            color=(0.1, 0.1, 0.1),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

        # Draw a colored box with summary stats for A3 pages
        shape3 = page.new_shape()
        summary_rect = pymupdf.Rect(50, a3_y + 270, width - 50, a3_y + 370)
        shape3.draw_rect(summary_rect)
        shape3.finish(color=(0.2, 0.2, 0.5), fill=(0.92, 0.93, 0.98), width=1)
        shape3.commit()

        page.insert_text(
            pymupdf.Point(70, a3_y + 300),
            "Key Takeaways: Revenue up 12.3% QoQ  |  Margins at 23.4%  |  Retention at 94.7%  |  105 FTEs",
            fontsize=11,
            fontname="hebo",
            color=(0.15, 0.15, 0.4),
        )


def create_initial():
    os.makedirs(DOCS_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Pages 1-5: Letter (612x792)
    for i in range(1, 6):
        page = doc.new_page(width=LETTER_W, height=LETTER_H)
        add_page_content(page, i, "Letter (8.5 x 11 in)", LETTER_W, LETTER_H)

    # Pages 6-10: Legal (612x1008)
    for i in range(6, 11):
        page = doc.new_page(width=LEGAL_W, height=LEGAL_H)
        add_page_content(page, i, "Legal (8.5 x 14 in)", LEGAL_W, LEGAL_H)

    # Pages 11-15: A3 (842x1190)
    for i in range(11, 16):
        page = doc.new_page(width=A3_W, height=A3_H)
        add_page_content(page, i, "A3 (297 x 420 mm)", A3_W, A3_H)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify
    doc = pymupdf.open(OUTPUT)
    print(f'Page count: {doc.page_count}')
    for i in range(doc.page_count):
        p = doc[i]
        print(f'  Page {i+1}: {p.rect.width:.0f} x {p.rect.height:.0f}')
    doc.close()

    # GUI-ready: open PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
