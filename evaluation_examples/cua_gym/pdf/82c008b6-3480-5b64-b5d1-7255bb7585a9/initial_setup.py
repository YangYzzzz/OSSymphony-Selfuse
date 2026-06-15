"""
Initial Setup: Create a 10-page A4 PDF document for page size conversion task.
Task ID: pdf_gf2_032
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
DOCS_DIR = f'{WORKDIR}/Documents'
TASK_ID = 'pdf_gf2_032'
OUTPUT = f'{DOCS_DIR}/a4_document.pdf'

A4_WIDTH = 595
A4_HEIGHT = 842


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

    # --- Page 1: Title Page ---
    page = doc.new_page(width=A4_WIDTH, height=A4_HEIGHT)
    page.insert_text(pymupdf.Point(150, 200), "Meridian Analytics", fontsize=28, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_text(pymupdf.Point(130, 260), "Annual Performance Report 2024", fontsize=18, fontname="helv", color=(0.2, 0.2, 0.2))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 290), pymupdf.Point(523, 290))
    shape.finish(color=(0.1, 0.2, 0.5), width=2)
    shape.commit()
    page.insert_text(pymupdf.Point(180, 400), "Prepared by: Finance Division", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(200, 430), "Date: March 15, 2024", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(170, 460), "Classification: Internal Use Only", fontsize=11, fontname="heit", color=(0.5, 0.3, 0.3))

    # --- Page 2: Executive Summary ---
    page = doc.new_page(width=A4_WIDTH, height=A4_HEIGHT)
    page.insert_text(pymupdf.Point(72, 72), "1. Executive Summary", fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(523, 82))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()
    summary_text = (
        "Meridian Analytics delivered strong results in fiscal year 2024, achieving total revenue "
        "of $48.7 million, representing a 12.3% increase over the prior year. Operating margins "
        "improved to 23.5%, driven by efficiency gains across all business units. The Enterprise "
        "Solutions division led growth with a 28% year-over-year increase, while the Analytics "
        "Platform segment maintained steady performance with 8% growth. Key strategic initiatives "
        "including the cloud migration program and the APAC expansion contributed significantly "
        "to the improved financial position. Employee headcount grew to 342, with notable additions "
        "in the engineering and data science teams. Customer retention rate remained above 94%, "
        "reflecting the strength of our product portfolio and client relationships."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 350), summary_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    page.insert_text(pymupdf.Point(72, 380), "Key Highlights:", fontsize=13, fontname="hebo", color=(0.1, 0.2, 0.5))
    highlights = [
        "Revenue: $48.7M (+12.3% YoY)",
        "Operating Margin: 23.5% (up from 21.1%)",
        "Customer Retention: 94.2%",
        "New Enterprise Contracts: 47",
        "Employee Headcount: 342 (+18%)",
    ]
    y = 405
    for h in highlights:
        page.insert_text(pymupdf.Point(90, y), f"•  {h}", fontsize=11, fontname="helv", color=(0, 0, 0))
        y += 20

    # --- Page 3: Revenue Breakdown ---
    page = doc.new_page(width=A4_WIDTH, height=A4_HEIGHT)
    page.insert_text(pymupdf.Point(72, 72), "2. Revenue Breakdown", fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(523, 82))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()
    rev_text = (
        "Total revenue for FY2024 was distributed across three primary business segments. "
        "The Enterprise Solutions division contributed $22.1M (45.4%), the Analytics Platform "
        "segment generated $17.3M (35.5%), and Professional Services accounted for $9.3M (19.1%). "
        "Quarter-over-quarter trends showed acceleration in the second half, with Q3 and Q4 "
        "each exceeding $13M in combined revenue."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 250), rev_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Revenue table header
    table_y = 270
    headers = ["Division", "Q1 ($M)", "Q2 ($M)", "Q3 ($M)", "Q4 ($M)", "Total ($M)"]
    col_x = [72, 180, 255, 330, 405, 480]
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(70, table_y - 5, 535, table_y + 18))
    shape.finish(fill=(0.1, 0.2, 0.5))
    shape.commit()
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(col_x[i], table_y + 12), h, fontsize=9, fontname="hebo", color=(1, 1, 1))
    # Table data
    rows = [
        ["Enterprise Solutions", "4.8", "5.1", "5.9", "6.3", "22.1"],
        ["Analytics Platform", "3.9", "4.1", "4.5", "4.8", "17.3"],
        ["Professional Services", "2.0", "2.2", "2.4", "2.7", "9.3"],
        ["Total", "10.7", "11.4", "12.8", "13.8", "48.7"],
    ]
    row_y = table_y + 35
    for ri, row in enumerate(rows):
        if ri % 2 == 1:
            shape = page.new_shape()
            shape.draw_rect(pymupdf.Rect(70, row_y - 5, 535, row_y + 15))
            shape.finish(fill=(0.93, 0.93, 0.97))
            shape.commit()
        fn = "hebo" if ri == len(rows) - 1 else "helv"
        for ci, val in enumerate(row):
            page.insert_text(pymupdf.Point(col_x[ci], row_y + 10), val, fontsize=9, fontname=fn, color=(0, 0, 0))
        row_y += 22

    # --- Page 4: Operating Expenses ---
    page = doc.new_page(width=A4_WIDTH, height=A4_HEIGHT)
    page.insert_text(pymupdf.Point(72, 72), "3. Operating Expenses", fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(523, 82))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()
    expense_text = (
        "Total operating expenses for FY2024 were $37.3M, representing a 9.8% increase from "
        "the prior year. The largest cost categories were personnel ($21.4M), technology "
        "infrastructure ($7.2M), and sales and marketing ($5.1M). General and administrative "
        "costs were $3.6M, representing a slight decrease as a percentage of revenue due to "
        "improved operational efficiency."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 260), expense_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    # Expense items
    expenses = [
        ("Personnel & Benefits", "$21.4M", "57.4%"),
        ("Technology Infrastructure", "$7.2M", "19.3%"),
        ("Sales & Marketing", "$5.1M", "13.7%"),
        ("General & Administrative", "$3.6M", "9.6%"),
    ]
    y = 290
    for name, amount, pct in expenses:
        page.insert_text(pymupdf.Point(90, y), name, fontsize=11, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(340, y), amount, fontsize=11, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(430, y), pct, fontsize=11, fontname="helv", color=(0.4, 0.4, 0.4))
        y += 25

    # --- Page 5: Client Portfolio ---
    page = doc.new_page(width=A4_WIDTH, height=A4_HEIGHT)
    page.insert_text(pymupdf.Point(72, 72), "4. Client Portfolio Analysis", fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(523, 82))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()
    client_text = (
        "Meridian Analytics serves 218 active enterprise clients across financial services, "
        "healthcare, retail, and technology sectors. The top 20 clients represent 42% of total "
        "revenue, a slight decrease from 45% in 2023, indicating healthy portfolio diversification. "
        "Average contract value increased to $223K from $198K, with the median contract duration "
        "extending to 2.4 years."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 260), client_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    # Client sector table
    sectors = [
        ("Financial Services", "78", "$11.2M", "23.0%"),
        ("Healthcare", "52", "$9.8M", "20.1%"),
        ("Retail & E-Commerce", "41", "$8.4M", "17.2%"),
        ("Technology", "31", "$12.6M", "25.9%"),
        ("Other Industries", "16", "$6.7M", "13.8%"),
    ]
    table_y = 280
    sec_cols = [72, 230, 320, 420]
    sec_headers = ["Sector", "Clients", "Revenue", "% of Total"]
    shape = page.new_shape()
    shape.draw_rect(pymupdf.Rect(70, table_y - 5, 520, table_y + 18))
    shape.finish(fill=(0.1, 0.2, 0.5))
    shape.commit()
    for i, h in enumerate(sec_headers):
        page.insert_text(pymupdf.Point(sec_cols[i], table_y + 12), h, fontsize=10, fontname="hebo", color=(1, 1, 1))
    row_y = table_y + 35
    for ri, (sector, clients, rev, pct) in enumerate(sectors):
        if ri % 2 == 1:
            shape = page.new_shape()
            shape.draw_rect(pymupdf.Rect(70, row_y - 5, 520, row_y + 15))
            shape.finish(fill=(0.93, 0.93, 0.97))
            shape.commit()
        vals = [sector, clients, rev, pct]
        for ci, val in enumerate(vals):
            page.insert_text(pymupdf.Point(sec_cols[ci], row_y + 10), val, fontsize=10, fontname="helv", color=(0, 0, 0))
        row_y += 22

    # --- Page 6: Product Development ---
    page = doc.new_page(width=A4_WIDTH, height=A4_HEIGHT)
    page.insert_text(pymupdf.Point(72, 72), "5. Product Development", fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(523, 82))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()
    prod_text = (
        "The product team shipped 14 major feature releases throughout 2024, including the "
        "launch of Meridian Insight Engine 3.0, which introduced real-time anomaly detection "
        "and natural language querying capabilities. The cloud migration program reached 78% "
        "completion, with full migration expected by Q2 2025. R&D investment totaled $6.8M, "
        "representing 14% of revenue, consistent with our target range of 13-16%."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 280), prod_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    page.insert_text(pymupdf.Point(72, 310), "Major Releases:", fontsize=13, fontname="hebo", color=(0.1, 0.2, 0.5))
    releases = [
        "Insight Engine 3.0 — Real-time anomaly detection (March 2024)",
        "DataSync Pro 2.5 — Multi-cloud data federation (June 2024)",
        "Meridian Dashboard — Self-service analytics portal (August 2024)",
        "API Gateway v4 — Enhanced rate limiting and caching (October 2024)",
        "Mobile Analytics Suite — iOS and Android apps (December 2024)",
    ]
    y = 335
    for r in releases:
        page.insert_text(pymupdf.Point(90, y), f"•  {r}", fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 20

    # --- Page 7: Human Resources ---
    page = doc.new_page(width=A4_WIDTH, height=A4_HEIGHT)
    page.insert_text(pymupdf.Point(72, 72), "6. Human Resources", fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(523, 82))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()
    hr_text = (
        "Headcount grew from 290 to 342 employees during FY2024. The engineering team expanded "
        "most significantly, adding 28 new hires including 12 machine learning engineers. "
        "Employee satisfaction scores averaged 4.2 out of 5.0 across quarterly surveys. "
        "Voluntary turnover decreased to 8.7% from 11.2%, reflecting improvements in "
        "compensation and career development programs. The diversity index improved to 0.71, "
        "with women representing 38% of leadership positions."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 300), hr_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Department breakdown
    depts = [
        ("Engineering", "128", "37.4%"),
        ("Sales & Marketing", "72", "21.1%"),
        ("Data Science", "48", "14.0%"),
        ("Customer Success", "36", "10.5%"),
        ("Finance & Operations", "32", "9.4%"),
        ("Executive & Admin", "26", "7.6%"),
    ]
    table_y = 320
    dept_cols = [90, 280, 400]
    page.insert_text(pymupdf.Point(90, table_y), "Department", fontsize=10, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_text(pymupdf.Point(280, table_y), "Headcount", fontsize=10, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_text(pymupdf.Point(400, table_y), "% of Total", fontsize=10, fontname="hebo", color=(0.1, 0.2, 0.5))
    y = table_y + 22
    for dept, count, pct in depts:
        page.insert_text(pymupdf.Point(90, y), dept, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(300, y), count, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(415, y), pct, fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))
        y += 20

    # --- Page 8: Risk Assessment ---
    page = doc.new_page(width=A4_WIDTH, height=A4_HEIGHT)
    page.insert_text(pymupdf.Point(72, 72), "7. Risk Assessment", fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(523, 82))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()
    risk_text = (
        "The enterprise risk management committee identified several key risk factors for "
        "the coming fiscal year. Cybersecurity threats remain the highest-priority concern, "
        "with investment in security infrastructure increasing by 35% to $2.1M. Market "
        "concentration risk has decreased due to successful diversification efforts, though "
        "the top-3 clients still account for 18% of revenue."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 260), risk_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    risks = [
        ("Cybersecurity Threats", "High", "Enhanced SOC operations, zero-trust architecture"),
        ("Market Competition", "Medium", "Product differentiation, customer lock-in features"),
        ("Regulatory Compliance", "Medium", "Dedicated compliance team, automated auditing"),
        ("Talent Acquisition", "Medium-Low", "Expanded recruitment channels, retention bonuses"),
        ("Technology Obsolescence", "Low", "Continuous R&D investment, agile methodology"),
    ]
    y = 290
    page.insert_text(pymupdf.Point(72, y), "Risk Factor", fontsize=10, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_text(pymupdf.Point(230, y), "Severity", fontsize=10, fontname="hebo", color=(0.1, 0.2, 0.5))
    page.insert_text(pymupdf.Point(320, y), "Mitigation Strategy", fontsize=10, fontname="hebo", color=(0.1, 0.2, 0.5))
    y += 22
    for risk, severity, mitigation in risks:
        page.insert_text(pymupdf.Point(72, y), risk, fontsize=9, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(230, y), severity, fontsize=9, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(320, y), mitigation, fontsize=9, fontname="helv", color=(0, 0, 0))
        y += 22

    # --- Page 9: Strategic Outlook ---
    page = doc.new_page(width=A4_WIDTH, height=A4_HEIGHT)
    page.insert_text(pymupdf.Point(72, 72), "8. Strategic Outlook for FY2025", fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(523, 82))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()
    outlook_text = (
        "Looking ahead, Meridian Analytics projects revenue growth of 15-18% for FY2025, "
        "targeting $56-58M in total revenue. The APAC expansion is expected to contribute "
        "$3-5M in new revenue, with offices planned in Singapore and Sydney. The company "
        "will continue investing heavily in AI and machine learning capabilities, with plans "
        "to launch a generative AI assistant for data analysts in Q2 2025."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 260), outlook_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    page.insert_text(pymupdf.Point(72, 290), "Strategic Priorities:", fontsize=13, fontname="hebo", color=(0.1, 0.2, 0.5))
    priorities = [
        "Complete cloud migration by Q2 2025",
        "Launch APAC regional offices (Singapore, Sydney)",
        "Release Meridian AI Assistant for data analysts",
        "Achieve SOC 2 Type II certification",
        "Expand partnership program to 50+ technology partners",
        "Grow annual recurring revenue to $42M",
    ]
    y = 315
    for p in priorities:
        page.insert_text(pymupdf.Point(90, y), f"•  {p}", fontsize=11, fontname="helv", color=(0, 0, 0))
        y += 22

    # --- Page 10: Appendix ---
    page = doc.new_page(width=A4_WIDTH, height=A4_HEIGHT)
    page.insert_text(pymupdf.Point(72, 72), "Appendix: Financial Summary Tables", fontsize=18, fontname="hebo", color=(0.1, 0.2, 0.5))
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 82), pymupdf.Point(523, 82))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()
    appendix_text = (
        "The following tables provide a condensed view of the company's financial position "
        "as of December 31, 2024. All figures are in USD millions unless otherwise noted. "
        "These statements have been prepared in accordance with generally accepted accounting "
        "principles and have been reviewed by Deloitte & Touche LLP."
    )
    page.insert_textbox(pymupdf.Rect(72, 100, 523, 200), appendix_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Balance sheet summary
    page.insert_text(pymupdf.Point(72, 230), "Condensed Balance Sheet", fontsize=13, fontname="hebo", color=(0.1, 0.2, 0.5))
    bs_items = [
        ("Total Assets", "$62.4M"),
        ("Total Liabilities", "$18.7M"),
        ("Shareholders' Equity", "$43.7M"),
        ("Cash & Equivalents", "$14.2M"),
        ("Accounts Receivable", "$8.9M"),
        ("Long-term Debt", "$5.3M"),
    ]
    y = 255
    for item, val in bs_items:
        page.insert_text(pymupdf.Point(100, y), item, fontsize=10, fontname="helv", color=(0, 0, 0))
        page.insert_text(pymupdf.Point(380, y), val, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 18

    # Footer on all pages
    for i in range(doc.page_count):
        p = doc[i]
        p.insert_text(
            pymupdf.Point(250, A4_HEIGHT - 30),
            f"Page {i + 1} of 10",
            fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5)
        )
        if i > 0:
            p.insert_text(
                pymupdf.Point(72, A4_HEIGHT - 30),
                "Meridian Analytics — Confidential",
                fontsize=7, fontname="heit", color=(0.6, 0.6, 0.6)
            )

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Verify page dimensions
    verify = pymupdf.open(OUTPUT)
    for i in range(verify.page_count):
        p = verify[i]
        print(f'Page {i+1}: {p.rect.width:.0f}x{p.rect.height:.0f} pts')
    verify.close()

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
