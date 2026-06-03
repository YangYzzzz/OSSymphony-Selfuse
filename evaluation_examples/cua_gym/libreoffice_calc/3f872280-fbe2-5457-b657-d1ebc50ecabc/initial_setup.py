"""
Initial Setup: Create a 10-page budget PDF with a table on page 4.
Task ID: pdf_ro_019
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_019'
FINANCE_DIR = f'{WORKDIR}/finance'
OUTPUT = f'{FINANCE_DIR}/budget.pdf'

# Department budget data for the table on page 4
DEPARTMENTS = [
    ("Engineering", 185000, 192000, 198500, 205000),
    ("Marketing", 95000, 102000, 98000, 110000),
    ("Sales", 120000, 135000, 128000, 142000),
    ("Human Resources", 68000, 70500, 72000, 74000),
    ("Operations", 145000, 148000, 152000, 156000),
    ("Finance", 82000, 84500, 86000, 88500),
    ("Research & Development", 210000, 225000, 238000, 245000),
    ("Customer Support", 76000, 78500, 81000, 83000),
]

HEADERS = ["Department", "Q1", "Q2", "Q3", "Q4"]


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


def add_text_page(doc, title, paragraphs):
    """Add a page with a title and body paragraphs."""
    page = doc.new_page(width=595, height=842)
    # Title
    page.insert_text(
        pymupdf.Point(72, 60),
        title,
        fontsize=20,
        fontname="hebo",
        color=(0.1, 0.15, 0.35),
    )
    # Divider line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, 70), pymupdf.Point(523, 70))
    shape.finish(color=(0.3, 0.3, 0.3), width=1)
    shape.commit()
    # Body text
    y = 100
    for para in paragraphs:
        rect = pymupdf.Rect(72, y, 523, y + 80)
        excess = page.insert_textbox(
            rect, para, fontsize=11, fontname="helv", color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_LEFT,
        )
        y += 85
        if y > 780:
            break
    return page


def add_table_page(doc):
    """Add page 4 with the department budget table at y=200 to y=500."""
    page = doc.new_page(width=595, height=842)

    # Page title
    page.insert_text(
        pymupdf.Point(72, 60),
        "FY2025 Departmental Budget Allocation",
        fontsize=20,
        fontname="hebo",
        color=(0.1, 0.15, 0.35),
    )

    # Intro paragraph before the table
    rect = pymupdf.Rect(72, 85, 523, 180)
    page.insert_textbox(
        rect,
        "The following table summarizes the quarterly budget allocations for each "
        "department during fiscal year 2025. All figures are in USD. These allocations "
        "were approved by the executive committee in the December 2024 planning session "
        "and reflect the organization's strategic priorities for the upcoming year.",
        fontsize=11, fontname="helv", color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # Table area: y=200 to y=500
    table_top = 200
    row_height = 30
    col_widths = [140, 75, 75, 75, 75]  # total ~440
    col_starts = [72]
    for w in col_widths[:-1]:
        col_starts.append(col_starts[-1] + w)
    table_right = col_starts[-1] + col_widths[-1]

    shape = page.new_shape()

    # Draw header row background
    shape.draw_rect(pymupdf.Rect(72, table_top, table_right, table_top + row_height))
    shape.finish(color=(0.2, 0.25, 0.45), fill=(0.2, 0.25, 0.45), width=0.5)

    # Header text (white on dark)
    for i, header in enumerate(HEADERS):
        x = col_starts[i] + 5
        page.insert_text(
            pymupdf.Point(x, table_top + 20),
            header,
            fontsize=11,
            fontname="hebo",
            color=(1, 1, 1),
        )

    # Data rows
    for row_idx, dept_data in enumerate(DEPARTMENTS):
        y_top = table_top + row_height * (row_idx + 1)
        # Alternate row background
        if row_idx % 2 == 0:
            shape.draw_rect(pymupdf.Rect(72, y_top, table_right, y_top + row_height))
            shape.finish(color=(0.92, 0.93, 0.96), fill=(0.92, 0.93, 0.96), width=0)

        # Department name
        page.insert_text(
            pymupdf.Point(col_starts[0] + 5, y_top + 20),
            dept_data[0],
            fontsize=10,
            fontname="helv",
            color=(0, 0, 0),
        )
        # Quarterly values
        for col_idx in range(1, 5):
            val = dept_data[col_idx]
            page.insert_text(
                pymupdf.Point(col_starts[col_idx] + 5, y_top + 20),
                f"{val:,}",
                fontsize=10,
                fontname="helv",
                color=(0, 0, 0),
            )

    # Draw grid lines
    total_rows = len(DEPARTMENTS) + 1  # header + data
    table_bottom = table_top + row_height * total_rows
    # Horizontal lines
    for r in range(total_rows + 1):
        y = table_top + r * row_height
        shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(table_right, y))
        shape.finish(color=(0.4, 0.4, 0.4), width=0.5)
    # Vertical lines
    for i, x in enumerate(col_starts):
        shape.draw_line(pymupdf.Point(x, table_top), pymupdf.Point(x, table_bottom))
        shape.finish(color=(0.4, 0.4, 0.4), width=0.5)
    # Right edge
    shape.draw_line(pymupdf.Point(table_right, table_top), pymupdf.Point(table_right, table_bottom))
    shape.finish(color=(0.4, 0.4, 0.4), width=0.5)

    shape.commit()

    # Note below table
    page.insert_text(
        pymupdf.Point(72, table_bottom + 25),
        "Note: All amounts are in USD. Q1=Jan-Mar, Q2=Apr-Jun, Q3=Jul-Sep, Q4=Oct-Dec.",
        fontsize=9,
        fontname="heit",
        color=(0.4, 0.4, 0.4),
    )

    return page


def create_initial():
    os.makedirs(FINANCE_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page 1: Cover page
    p1 = doc.new_page(width=595, height=842)
    p1.insert_text(pymupdf.Point(120, 300), "Meridian Technologies Inc.", fontsize=28, fontname="hebo", color=(0.1, 0.15, 0.35))
    p1.insert_text(pymupdf.Point(160, 350), "Annual Budget Report FY2025", fontsize=20, fontname="helv", color=(0.3, 0.3, 0.3))
    p1.insert_text(pymupdf.Point(200, 400), "Prepared by the Finance Department", fontsize=14, fontname="heit", color=(0.4, 0.4, 0.4))
    p1.insert_text(pymupdf.Point(230, 430), "January 2025 | Confidential", fontsize=12, fontname="helv", color=(0.5, 0.5, 0.5))

    # Page 2: Executive Summary
    add_text_page(doc, "Executive Summary", [
        "This report provides a comprehensive overview of the budget allocations for "
        "Meridian Technologies Inc. for fiscal year 2025. The total organizational budget "
        "has been set at $12.4 million, representing a 7.2% increase over FY2024.",
        "Key strategic investments include expansion of the engineering and R&D departments, "
        "reflecting our commitment to product innovation. Marketing spend is projected to "
        "increase by 8% to support the launch of three new product lines.",
        "Operational efficiencies gained through automation initiatives in FY2024 have "
        "allowed us to reallocate approximately $340,000 toward growth-oriented departments "
        "without increasing the overall cost structure proportionally.",
        "The Finance Committee has approved contingency reserves of $620,000 for unplanned "
        "expenditures, which represents 5% of the total budget.",
    ])

    # Page 3: Budget Overview
    add_text_page(doc, "Budget Methodology & Assumptions", [
        "The FY2025 budget was developed using a zero-based budgeting approach for "
        "discretionary spending categories, combined with incremental budgeting for "
        "fixed operational costs. Each department submitted proposals in October 2024.",
        "Revenue projections assume 12% year-over-year growth based on current pipeline "
        "analysis and market forecasts from McKinsey Global Institute. Conservative "
        "estimates were used for new product revenue streams.",
        "Headcount assumptions: Total FTEs are projected at 342, up from 318 in FY2024. "
        "New hires are concentrated in Engineering (+12), R&D (+8), and Customer Support (+4).",
        "Currency assumptions: All figures are in USD. International operations budget "
        "uses exchange rates as of December 15, 2024.",
    ])

    # Page 4: THE TABLE PAGE (y=200 to y=500)
    add_table_page(doc)

    # Page 5: Capital Expenditure
    add_text_page(doc, "Capital Expenditure Plan", [
        "Capital expenditures for FY2025 are projected at $2.1 million, allocated across "
        "technology infrastructure upgrades ($890,000), office expansion at the Austin "
        "campus ($650,000), and laboratory equipment for the R&D division ($560,000).",
        "The technology infrastructure budget covers migration of legacy systems to cloud "
        "architecture, with estimated completion by Q3. This investment is expected to "
        "reduce annual hosting costs by $180,000 starting in FY2026.",
        "Office expansion in Austin will add 12,000 square feet of workspace to accommodate "
        "projected headcount growth through FY2027. Construction is scheduled to begin in "
        "March 2025 with occupancy expected by September 2025.",
    ])

    # Page 6: Revenue Projections
    add_text_page(doc, "Revenue Projections & Growth Targets", [
        "Total revenue for FY2025 is projected at $48.6 million, compared to $43.4 million "
        "in FY2024. The Enterprise Solutions segment is expected to contribute $28.2 million, "
        "while Cloud Services should reach $15.8 million.",
        "The new AI Analytics product line, launching in Q2, is forecast to generate $4.6 "
        "million in its first partial year. Early customer trials have shown strong adoption "
        "metrics with a 92% satisfaction rate among pilot participants.",
        "Geographic revenue breakdown: North America 62%, Europe 24%, Asia-Pacific 14%. "
        "We anticipate stronger growth in APAC due to new partnership agreements with "
        "distributors in Japan and Australia.",
    ])

    # Page 7: Risk Assessment
    add_text_page(doc, "Risk Assessment & Mitigation", [
        "The primary financial risk for FY2025 is the potential for delayed product launches "
        "which could impact revenue recognition. Mitigation includes maintaining a 60-day "
        "buffer in project timelines and earmarking contingency funds.",
        "Supply chain risks remain moderate following the disruptions experienced in "
        "FY2023-2024. We have diversified our vendor base from 3 to 7 primary suppliers "
        "and maintain 90-day inventory reserves for critical components.",
        "Regulatory compliance costs may increase due to pending legislation in the EU "
        "and California. The legal team estimates potential additional costs of $150,000 "
        "to $280,000 which are covered by the contingency reserve.",
    ])

    # Page 8: Staffing Plan
    add_text_page(doc, "Staffing & Compensation Plan", [
        "Total compensation expense for FY2025 is budgeted at $7.8 million, representing "
        "63% of the total budget. This includes base salaries, performance bonuses, "
        "benefits, and equity compensation for eligible employees.",
        "A 4.2% average salary increase has been approved effective April 2025, in line "
        "with industry benchmarks provided by Radford and Mercer surveys. Top performers "
        "may receive increases up to 7.5%.",
        "Benefits costs are projected to increase 6.8% due to rising healthcare premiums. "
        "The company will absorb 80% of the increase, with employee contribution adjustments "
        "communicated in the Q1 benefits enrollment period.",
    ])

    # Page 9: Technology Roadmap
    add_text_page(doc, "Technology Investment Roadmap", [
        "FY2025 technology investments focus on three pillars: cloud migration, data "
        "analytics platform modernization, and cybersecurity enhancement. Total IT spend "
        "is budgeted at $3.2 million across operating and capital budgets.",
        "The cloud migration initiative will transition 85% of on-premises workloads to "
        "AWS by end of Q3. Expected benefits include improved scalability, 99.99% uptime "
        "SLA, and estimated annual savings of $180,000 starting FY2026.",
        "Cybersecurity investments include deployment of zero-trust architecture, enhanced "
        "endpoint detection and response (EDR), and mandatory security awareness training "
        "for all employees. Budget allocation: $420,000.",
    ])

    # Page 10: Appendix
    add_text_page(doc, "Appendix: Budget Approval History", [
        "This budget was developed through a collaborative process spanning October through "
        "December 2024. Initial department proposals were submitted October 15, 2024.",
        "The Finance Committee reviewed all proposals in three sessions held on November 5, "
        "November 19, and December 3, 2024. Adjustments were made based on strategic "
        "priority alignment and return-on-investment analysis.",
        "Final approval was granted by the Board of Directors on December 18, 2024, with "
        "a unanimous vote. The CFO, Sarah Martinez, is responsible for budget oversight "
        "and quarterly variance reporting to the Board.",
        "Document version: 3.1 | Last updated: January 8, 2025 | Classification: Confidential",
    ])

    # Set document metadata
    doc.set_metadata({
        "title": "Annual Budget Report FY2025 - Meridian Technologies Inc.",
        "author": "Finance Department",
        "subject": "Fiscal Year 2025 Budget Allocations",
        "keywords": "budget, finance, FY2025, Meridian Technologies",
        "creator": "Meridian Finance System",
    })

    # Set table of contents
    toc = [
        [1, "Cover", 1],
        [1, "Executive Summary", 2],
        [1, "Budget Methodology & Assumptions", 3],
        [1, "Departmental Budget Allocation", 4],
        [1, "Capital Expenditure Plan", 5],
        [1, "Revenue Projections & Growth Targets", 6],
        [1, "Risk Assessment & Mitigation", 7],
        [1, "Staffing & Compensation Plan", 8],
        [1, "Technology Investment Roadmap", 9],
        [1, "Appendix: Budget Approval History", 10],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')

    # Open in Evince for GUI readiness
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
