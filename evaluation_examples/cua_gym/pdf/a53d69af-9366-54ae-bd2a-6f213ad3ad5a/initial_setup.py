"""
Initial Setup: Create a 15-page financial quarterly report PDF with ~23 occurrences of 'revenue'
Task ID: pdf_ro_003
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_003'
FINANCE_DIR = f'{WORKDIR}/finance'
OUTPUT = f'{FINANCE_DIR}/quarterly.pdf'


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
    os.makedirs(FINANCE_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page dimensions (Letter size)
    W, H = 612, 792
    LEFT = 72
    RIGHT = W - 72
    TOP = 72
    BOTTOM = H - 72
    TEXT_WIDTH = RIGHT - LEFT

    # Helper to add page number footer
    def add_footer(page, page_num, total):
        page.insert_text(
            pymupdf.Point(W / 2 - 20, H - 36),
            f"Page {page_num} of {total}",
            fontsize=9,
            fontname="helv",
            color=(0.5, 0.5, 0.5),
        )

    # ---- PAGE 1: Cover Page ----
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(LEFT, 200), "Meridian Financial Group", fontsize=28, fontname="hebo", color=(0.0, 0.13, 0.4))
    p.insert_text(pymupdf.Point(LEFT, 250), "Quarterly Financial Report", fontsize=22, fontname="helv", color=(0.2, 0.2, 0.2))
    p.insert_text(pymupdf.Point(LEFT, 285), "Q4 2025 | October - December", fontsize=14, fontname="helv", color=(0.4, 0.4, 0.4))
    p.insert_text(pymupdf.Point(LEFT, 330), "Prepared by the Office of the Chief Financial Officer", fontsize=11, fontname="heit", color=(0.4, 0.4, 0.4))
    p.insert_text(pymupdf.Point(LEFT, 355), "Confidential - For Internal Distribution Only", fontsize=10, fontname="hebo", color=(0.7, 0.0, 0.0))
    # Draw a decorative line
    shape = p.new_shape()
    shape.draw_line(pymupdf.Point(LEFT, 300), pymupdf.Point(RIGHT, 300))
    shape.finish(color=(0.0, 0.13, 0.4), width=2)
    shape.commit()

    # ---- PAGE 2: Table of Contents ----
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(LEFT, TOP + 10), "Table of Contents", fontsize=20, fontname="hebo", color=(0.0, 0.13, 0.4))
    toc_items = [
        ("1. Executive Summary", "3"),
        ("2. Financial Performance Overview", "4"),
        ("3. Segment Breakdown", "5"),
        ("4. Operating Expenses", "7"),
        ("5. Net Income Analysis", "8"),
        ("6. Balance Sheet Highlights", "9"),
        ("7. Cash Flow Statement", "10"),
        ("8. Growth Forecast & Outlook", "11"),
        ("9. Risk Factors", "13"),
        ("10. Appendix: Detailed Financial Tables", "14"),
    ]
    y = TOP + 50
    for title, pg in toc_items:
        p.insert_text(pymupdf.Point(LEFT + 20, y), title, fontsize=12, fontname="helv", color=(0, 0, 0))
        p.insert_text(pymupdf.Point(RIGHT - 30, y), pg, fontsize=12, fontname="helv", color=(0, 0, 0))
        y += 24
    add_footer(p, 2, 15)

    # ---- PAGE 3: Executive Summary ----
    # revenue count target: 3 on this page
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(LEFT, TOP + 10), "1. Executive Summary", fontsize=18, fontname="hebo", color=(0.0, 0.13, 0.4))
    text = (
        "Meridian Financial Group delivered strong results in Q4 2025, driven by robust revenue "
        "growth across all business segments. Total revenue for the quarter reached $487.3 million, "
        "representing a 12.4% increase year-over-year. This growth was primarily fueled by expanded "
        "market share in our Enterprise Solutions division and the successful launch of our new "
        "digital platform in September.\n\n"
        "Operating margins improved to 18.7%, reflecting disciplined cost management and favorable "
        "product mix. Net income rose to $62.1 million, a 15.2% improvement compared to Q4 2024. "
        "The company maintained its strong balance sheet position with $892 million in cash and "
        "short-term investments.\n\n"
        "Key achievements during the quarter included the acquisition of DataVault Technologies "
        "for $145 million, the expansion of our Asia-Pacific operations to three new markets, and "
        "the achievement of a record-high customer satisfaction score of 94.2%. Total sales "
        "for the full year 2025 exceeded $1.8 billion."
    )
    p.insert_textbox(pymupdf.Rect(LEFT, TOP + 30, RIGHT, BOTTOM - 20), text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    add_footer(p, 3, 15)

    # ---- PAGE 4: Revenue Overview ----
    # revenue count target: 4 on this page
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(LEFT, TOP + 10), "2. Financial Performance Overview", fontsize=18, fontname="hebo", color=(0.0, 0.13, 0.4))
    text = (
        "Total consolidated revenue for Q4 2025 was $487.3 million, compared to $433.5 million "
        "in Q4 2024. Growth was broad-based, with all four business segments contributing "
        "positively. The Enterprise Solutions segment accounted for 42% of total earnings, followed "
        "by Consumer Products at 28%, Professional Services at 18%, and Licensing at 12%.\n\n"
        "Sequential income increased by 3.8% from Q3 2025, reflecting typical seasonal strength "
        "in our enterprise and consumer divisions. Foreign currency fluctuations had a modest "
        "negative impact on reported figures of approximately $4.2 million, or 0.9 percentage "
        "points of growth.\n\n"
        "Recurring revenue streams, including software subscriptions and maintenance contracts, "
        "represented 67% of total quarterly income, up from 61% in the prior-year quarter. This "
        "shift toward recurring business models continues to improve visibility and predictability "
        "of our financial performance."
    )
    p.insert_textbox(pymupdf.Rect(LEFT, TOP + 30, RIGHT, BOTTOM - 20), text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    add_footer(p, 4, 15)

    # ---- PAGE 5: Revenue by Segment (part 1) ----
    # revenue count target: 3 on this page
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(LEFT, TOP + 10), "3. Segment Breakdown", fontsize=18, fontname="hebo", color=(0.0, 0.13, 0.4))
    text = (
        "Enterprise Solutions revenue reached $204.6 million in Q4 2025, an increase of 16.3% "
        "year-over-year. Growth was led by strong demand for our cloud-based analytics platform, "
        "which saw a 34% increase in new customer acquisitions. Earnings from existing enterprise "
        "clients expanded by 9.7%, reflecting successful upselling and cross-selling initiatives.\n\n"
        "The Consumer Products division generated revenue of $136.4 million, up 8.2% from the "
        "prior year. The launch of our Smart Home integration suite contributed $18.3 million "
        "in incremental sales during the quarter."
    )
    p.insert_textbox(pymupdf.Rect(LEFT, TOP + 30, RIGHT, BOTTOM - 20), text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    add_footer(p, 5, 15)

    # ---- PAGE 6: Revenue by Segment (part 2) ----
    # revenue count target: 2 on this page
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(LEFT, TOP + 10), "3. Segment Breakdown (continued)", fontsize=16, fontname="hebo", color=(0.0, 0.13, 0.4))
    text = (
        "Professional Services revenue totaled $87.7 million, growing 11.5% year-over-year. "
        "This segment benefited from increased consulting engagements related to digital "
        "transformation projects and expanded managed services contracts. Average project size "
        "increased by 22% compared to the prior year.\n\n"
        "The Licensing segment contributed $58.6 million in revenue, a moderate 4.1% increase "
        "from Q4 2024. While perpetual license sales declined as expected, this was more than "
        "offset by growth in subscription-based licensing models."
    )
    p.insert_textbox(pymupdf.Rect(LEFT, TOP + 30, RIGHT, BOTTOM - 20), text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    add_footer(p, 6, 15)

    # ---- PAGE 7: Operating Expenses ----
    # revenue count target: 1 on this page
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(LEFT, TOP + 10), "4. Operating Expenses", fontsize=18, fontname="hebo", color=(0.0, 0.13, 0.4))
    text = (
        "Total operating expenses for Q4 2025 were $396.2 million, an increase of 10.8% "
        "year-over-year. As a percentage of revenue, operating expenses decreased from 82.4% "
        "to 81.3%, demonstrating improving operating leverage. Cost of goods sold was $241.8 "
        "million, reflecting a gross margin of 50.4%, compared to 49.1% in Q4 2024. Revenue-related "
        "costs grew in line with overall sales performance.\n\n"
        "Research and development expenses were $68.4 million, or 14.0% of total quarterly "
        "sales. Key R&D investments included our next-generation AI platform, enhanced "
        "cybersecurity capabilities, and IoT edge computing solutions.\n\n"
        "Sales and marketing expenses totaled $58.3 million, while general and administrative "
        "costs were $27.7 million. Restructuring charges of $4.8 million were related to the "
        "integration of DataVault Technologies."
    )
    p.insert_textbox(pymupdf.Rect(LEFT, TOP + 30, RIGHT, BOTTOM - 20), text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    add_footer(p, 7, 15)

    # ---- PAGE 8: Net Income Analysis ----
    # revenue count target: 1 on this page
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(LEFT, TOP + 10), "5. Net Income Analysis", fontsize=18, fontname="hebo", color=(0.0, 0.13, 0.4))
    text = (
        "Net income for Q4 2025 was $62.1 million, compared to $53.9 million in Q4 2024. "
        "Earnings per share (diluted) increased to $1.24 from $1.08 in the prior-year quarter. "
        "The effective tax rate was 22.3%, compared to 23.1% in Q4 2024, benefiting from "
        "increased R&D tax credits and the favorable resolution of certain tax matters.\n\n"
        "EBITDA for the quarter was $91.1 million, representing an EBITDA margin of 18.7%. "
        "Excluding one-time items related to the DataVault acquisition, adjusted EBITDA "
        "was $95.9 million, or 19.7% of total revenue. Operating income grew 14.8% "
        "year-over-year to $74.2 million. Revenue per share reached $9.74 for the quarter."
    )
    p.insert_textbox(pymupdf.Rect(LEFT, TOP + 30, RIGHT, BOTTOM - 20), text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    add_footer(p, 8, 15)

    # ---- PAGE 9: Balance Sheet Highlights ----
    # revenue count target: 0 on this page
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(LEFT, TOP + 10), "6. Balance Sheet Highlights", fontsize=18, fontname="hebo", color=(0.0, 0.13, 0.4))
    text = (
        "Total assets as of December 31, 2025 were $4.12 billion, compared to $3.68 billion "
        "at the end of 2024. Cash and short-term investments totaled $892 million, providing "
        "ample liquidity for operations and strategic investments.\n\n"
        "Total debt was $1.05 billion, resulting in a net debt position of $158 million. The "
        "debt-to-equity ratio improved to 0.42 from 0.48 in the prior year. Accounts receivable "
        "increased to $312 million, with days sales outstanding of 58 days, compared to 55 days "
        "in Q4 2024. Deferred revenue stood at $234 million, up 18% from the prior year.\n\n"
        "Shareholders' equity grew to $2.51 billion, reflecting retained earnings growth and "
        "the impact of share repurchases totaling $75 million during the quarter."
    )
    p.insert_textbox(pymupdf.Rect(LEFT, TOP + 30, RIGHT, BOTTOM - 20), text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    add_footer(p, 9, 15)

    # ---- PAGE 10: Cash Flow Statement ----
    # revenue count target: 0 on this page
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(LEFT, TOP + 10), "7. Cash Flow Statement", fontsize=18, fontname="hebo", color=(0.0, 0.13, 0.4))
    text = (
        "Cash generated from operating activities was $98.4 million in Q4 2025, compared to "
        "$84.7 million in Q4 2024. The improvement was driven by higher net income, strong revenue "
        "collections, and favorable changes in working capital, partially offset by increased tax payments.\n\n"
        "Capital expenditures totaled $32.1 million, primarily related to data center expansion, "
        "office renovations at our London facility, and technology infrastructure upgrades. Free "
        "cash flow was $66.3 million, representing a free cash flow margin of 13.6%.\n\n"
        "Investing activities consumed $178.2 million, including $145 million for the DataVault "
        "acquisition. Financing activities included $75 million in share repurchases and $22.4 "
        "million in dividend payments."
    )
    p.insert_textbox(pymupdf.Rect(LEFT, TOP + 30, RIGHT, BOTTOM - 20), text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    add_footer(p, 10, 15)

    # ---- PAGE 11: Revenue Forecast & Outlook (part 1) ----
    # revenue count target: 4 on this page
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(LEFT, TOP + 10), "8. Growth Forecast & Outlook", fontsize=18, fontname="hebo", color=(0.0, 0.13, 0.4))
    text = (
        "Management expects total revenue for Q1 2026 to be in the range of $495 million to "
        "$510 million, representing year-over-year growth of 10% to 13%. For the full "
        "fiscal year 2026, the company is targeting total revenue of $2.05 billion to $2.12 "
        "billion.\n\n"
        "Key growth drivers for 2026 include the continued expansion of cloud-based "
        "enterprise solutions, expected contributions from the DataVault integration "
        "beginning in Q2 2026, and the launch of three new product lines in the Consumer "
        "division. International markets are expected to contribute an increasing share of "
        "total revenue, growing from 31% in 2025 to an estimated 35% in 2026."
    )
    p.insert_textbox(pymupdf.Rect(LEFT, TOP + 30, RIGHT, BOTTOM - 20), text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    add_footer(p, 11, 15)

    # ---- PAGE 12: Revenue Forecast & Outlook (part 2) ----
    # revenue count target: 2 on this page
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(LEFT, TOP + 10), "8. Growth Forecast & Outlook (continued)", fontsize=16, fontname="hebo", color=(0.0, 0.13, 0.4))
    text = (
        "The company expects operating margins to improve to approximately 19.5% to 20.5% "
        "in 2026, benefiting from scale efficiencies and the higher-margin product mix from "
        "cloud services. Capital expenditures are planned at $140 million to $160 million, "
        "focused on infrastructure and capacity expansion.\n\n"
        "Management remains cautiously optimistic about the macroeconomic environment but "
        "acknowledges potential headwinds from foreign currency volatility, evolving trade "
        "policies, and competitive pricing pressure in certain segments. The recurring revenue "
        "base provides a solid foundation for predictable growth."
    )
    p.insert_textbox(pymupdf.Rect(LEFT, TOP + 30, RIGHT, BOTTOM - 20), text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    add_footer(p, 12, 15)

    # ---- PAGE 13: Risk Factors ----
    # revenue count target: 1 on this page
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(LEFT, TOP + 10), "9. Risk Factors", fontsize=18, fontname="hebo", color=(0.0, 0.13, 0.4))
    text = (
        "The following factors could materially affect the company's financial performance:\n\n"
        "1. Macroeconomic Uncertainty: A deterioration in global economic conditions could reduce "
        "enterprise IT spending and negatively impact revenue across all segments.\n\n"
        "2. Competition: Increased competition from both established players and emerging startups "
        "could pressure pricing and market share.\n\n"
        "3. Technology Disruption: Rapid advances in artificial intelligence and automation could "
        "render certain product offerings obsolete.\n\n"
        "4. Regulatory Changes: New data privacy regulations in key markets could increase "
        "compliance costs and limit the scope of certain product features.\n\n"
        "5. Integration Risks: The successful integration of DataVault Technologies is critical "
        "to achieving projected synergies and cost savings."
    )
    p.insert_textbox(pymupdf.Rect(LEFT, TOP + 30, RIGHT, BOTTOM - 20), text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)
    add_footer(p, 13, 15)

    # ---- PAGE 14: Appendix - Detailed Revenue Tables ----
    # revenue count target: 2 on this page
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(LEFT, TOP + 10), "10. Appendix: Detailed Financial Tables", fontsize=18, fontname="hebo", color=(0.0, 0.13, 0.4))
    text = (
        "The following tables present a detailed breakdown of results by segment and geography "
        "for Q4 2025.\n\n"
        "Table A: Quarterly Revenue by Segment ($M)\n"
    )
    p.insert_textbox(pymupdf.Rect(LEFT, TOP + 30, RIGHT, TOP + 100), text, fontsize=11, fontname="helv", color=(0, 0, 0))
    # Draw a simple table
    table_data = [
        ["Segment", "Q4 2025", "Q4 2024", "Change"],
        ["Enterprise Solutions", "$204.6", "$175.9", "+16.3%"],
        ["Consumer Products", "$136.4", "$126.1", "+8.2%"],
        ["Professional Services", "$87.7", "$78.7", "+11.5%"],
        ["Licensing", "$58.6", "$56.3", "+4.1%"],
        ["Total Revenue", "$487.3", "$433.5", "+12.4%"],
    ]
    y_start = TOP + 110
    col_x = [LEFT, LEFT + 170, LEFT + 280, LEFT + 380]
    for r, row in enumerate(table_data):
        y = y_start + r * 22
        for c, cell in enumerate(row):
            fn = "hebo" if r == 0 or r == len(table_data) - 1 else "helv"
            p.insert_text(pymupdf.Point(col_x[c], y), cell, fontsize=10, fontname=fn, color=(0, 0, 0))
    # Horizontal lines
    shape = p.new_shape()
    shape.draw_line(pymupdf.Point(LEFT, y_start - 8), pymupdf.Point(RIGHT - 60, y_start - 8))
    shape.draw_line(pymupdf.Point(LEFT, y_start + 14), pymupdf.Point(RIGHT - 60, y_start + 14))
    shape.draw_line(pymupdf.Point(LEFT, y_start + (len(table_data) - 1) * 22 - 8), pymupdf.Point(RIGHT - 60, y_start + (len(table_data) - 1) * 22 - 8))
    shape.draw_line(pymupdf.Point(LEFT, y_start + (len(table_data) - 1) * 22 + 14), pymupdf.Point(RIGHT - 60, y_start + (len(table_data) - 1) * 22 + 14))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()
    add_footer(p, 14, 15)

    # ---- PAGE 15: Appendix continued ----
    # revenue count target: 1 on this page
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(LEFT, TOP + 10), "10. Appendix (continued)", fontsize=16, fontname="hebo", color=(0.0, 0.13, 0.4))
    text = (
        "Table B: Revenue by Geography ($M)\n"
    )
    p.insert_textbox(pymupdf.Rect(LEFT, TOP + 30, RIGHT, TOP + 55), text, fontsize=11, fontname="hebo", color=(0, 0, 0))
    table_data2 = [
        ["Region", "Q4 2025", "Q4 2024", "% of Total"],
        ["North America", "$335.8", "$303.5", "68.9%"],
        ["Europe", "$82.4", "$73.6", "16.9%"],
        ["Asia-Pacific", "$48.7", "$39.0", "10.0%"],
        ["Rest of World", "$20.4", "$17.4", "4.2%"],
        ["Total", "$487.3", "$433.5", "100.0%"],
    ]
    y_start2 = TOP + 65
    for r, row in enumerate(table_data2):
        y = y_start2 + r * 22
        for c, cell in enumerate(row):
            fn = "hebo" if r == 0 or r == len(table_data2) - 1 else "helv"
            p.insert_text(pymupdf.Point(col_x[c], y), cell, fontsize=10, fontname=fn, color=(0, 0, 0))
    shape = p.new_shape()
    shape.draw_line(pymupdf.Point(LEFT, y_start2 - 8), pymupdf.Point(RIGHT - 60, y_start2 - 8))
    shape.draw_line(pymupdf.Point(LEFT, y_start2 + 14), pymupdf.Point(RIGHT - 60, y_start2 + 14))
    shape.draw_line(pymupdf.Point(LEFT, y_start2 + (len(table_data2) - 1) * 22 - 8), pymupdf.Point(RIGHT - 60, y_start2 + (len(table_data2) - 1) * 22 - 8))
    shape.draw_line(pymupdf.Point(LEFT, y_start2 + (len(table_data2) - 1) * 22 + 14), pymupdf.Point(RIGHT - 60, y_start2 + (len(table_data2) - 1) * 22 + 14))
    shape.finish(color=(0, 0, 0), width=0.5)
    shape.commit()

    # Disclaimer text at bottom
    p.insert_textbox(
        pymupdf.Rect(LEFT, BOTTOM - 80, RIGHT, BOTTOM - 20),
        "This document contains forward-looking statements that involve risks and uncertainties. "
        "Actual results may differ materially from those projected. This report is for internal "
        "use only and should not be distributed outside the organization without prior approval.",
        fontsize=9, fontname="heit", color=(0.5, 0.5, 0.5),
    )
    add_footer(p, 15, 15)

    # Save
    doc.save(OUTPUT)
    doc.close()

    # Count occurrences to verify
    doc = pymupdf.open(OUTPUT)
    total = 0
    for page in doc:
        instances = page.search_for("revenue")
        # Also search capitalized variants
        instances += page.search_for("Revenue")
        # Deduplicate overlapping rects
        seen = set()
        for inst in instances:
            key = (round(inst.x0, 1), round(inst.y0, 1))
            seen.add(key)
        total += len(seen)
    doc.close()
    print(f"Initial file created: {OUTPUT}")
    print(f"Total 'revenue' occurrences found: {total}")

    # Open in Evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
