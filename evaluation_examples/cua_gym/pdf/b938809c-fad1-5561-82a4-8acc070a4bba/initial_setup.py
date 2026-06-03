"""
Initial Setup: Create a 15-page financial report PDF
Task ID: pdf_gf2_023
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_023'
DOCS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCS_DIR}/financial_report.pdf'


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
    """Add consistent header and footer to each page."""
    w = page.rect.width
    h = page.rect.height
    # Header line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(50, 55), pymupdf.Point(w - 50, 55))
    shape.finish(color=(0.2, 0.3, 0.5), width=1.5)
    shape.commit()
    # Header text
    page.insert_text(pymupdf.Point(50, 45), "Meridian Capital Group", fontsize=9, fontname="hebo", color=(0.2, 0.3, 0.5))
    page.insert_text(pymupdf.Point(w - 200, 45), "Annual Financial Report 2024", fontsize=8, fontname="heit", color=(0.4, 0.4, 0.4))
    # Footer
    page.insert_text(pymupdf.Point(50, h - 30), f"Page {page_num} of {total_pages}", fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))
    page.insert_text(pymupdf.Point(w - 200, h - 30), "Confidential", fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))


def create_financial_report():
    os.makedirs(DOCS_DIR, exist_ok=True)
    doc = pymupdf.open()
    W, H = 612, 792  # Letter size

    # ========== PAGE 1: Title Page ==========
    p = doc.new_page(width=W, height=H)
    p.insert_text(pymupdf.Point(150, 200), "Meridian Capital Group", fontsize=28, fontname="hebo", color=(0.15, 0.25, 0.45))
    p.insert_text(pymupdf.Point(130, 260), "Annual Financial Report", fontsize=24, fontname="tibo", color=(0.3, 0.3, 0.3))
    p.insert_text(pymupdf.Point(220, 310), "Fiscal Year 2024", fontsize=18, fontname="tiit", color=(0.4, 0.4, 0.4))
    shape = p.new_shape()
    shape.draw_line(pymupdf.Point(100, 340), pymupdf.Point(512, 340))
    shape.finish(color=(0.15, 0.25, 0.45), width=2)
    shape.commit()
    p.insert_text(pymupdf.Point(160, 400), "Prepared by the Office of the Chief Financial Officer", fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))
    p.insert_text(pymupdf.Point(210, 430), "Date of Publication: March 15, 2025", fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))
    p.insert_text(pymupdf.Point(180, 470), "Robert A. Harrington, CFA - Chief Financial Officer", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    p.insert_text(pymupdf.Point(195, 490), "Elena V. Kuznetsova, CPA - VP of Finance", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    p.insert_text(pymupdf.Point(210, 510), "James T. Whitfield - Director of Accounting", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    add_page_header(p, "", 1, 15)

    # ========== PAGE 2: Table of Contents ==========
    p = doc.new_page(width=W, height=H)
    add_page_header(p, "Table of Contents", 2, 15)
    p.insert_text(pymupdf.Point(50, 90), "Table of Contents", fontsize=20, fontname="hebo", color=(0.15, 0.25, 0.45))
    toc_items = [
        ("1. Executive Summary", 3),
        ("2. Revenue Analysis", 4),
        ("3. Expense Breakdown", 5),
        ("4. Quarterly Performance", 6),
        ("5. Balance Sheet Overview", 7),
        ("6. Cash Flow Statement", 8),
        ("7. Regional Performance", 9),
        ("8. Product Line Analysis", 10),
        ("9. Employee Compensation and Benefits", 11),
        ("10. Capital Expenditures", 12),
        ("11. Risk Assessment and Mitigation", 13),
        ("12. Forward-Looking Projections", 14),
        ("13. Auditor's Notes and Disclosures", 15),
    ]
    y = 130
    for title, pg in toc_items:
        p.insert_text(pymupdf.Point(70, y), title, fontsize=12, fontname="helv", color=(0, 0, 0))
        p.insert_text(pymupdf.Point(480, y), f"...... {pg}", fontsize=12, fontname="helv", color=(0.4, 0.4, 0.4))
        y += 28

    # ========== PAGE 3: Executive Summary ==========
    p = doc.new_page(width=W, height=H)
    add_page_header(p, "Executive Summary", 3, 15)
    p.insert_text(pymupdf.Point(50, 90), "1. Executive Summary", fontsize=18, fontname="hebo", color=(0.15, 0.25, 0.45))
    exec_text = (
        "Meridian Capital Group delivered strong financial results in fiscal year 2024, "
        "achieving total revenue of $847.3 million, representing a 12.4% increase over the "
        "prior year. Operating income grew to $198.6 million, driven by improved margins in "
        "our Technology Solutions and Healthcare Services divisions. Net income reached "
        "$142.8 million, or $4.23 per diluted share, compared to $118.5 million in fiscal 2023.\n\n"
        "Key strategic initiatives completed during the year included the acquisition of Nexus "
        "Analytics for $65 million, which strengthened our data analytics capabilities, and the "
        "successful launch of our CloudBridge platform, generating $38.2 million in first-year "
        "revenue. Our international expansion into Southeast Asian markets contributed an "
        "additional $52.7 million to top-line growth.\n\n"
        "Total assets increased to $2.14 billion, while maintaining a debt-to-equity ratio of "
        "0.42, reflecting our commitment to conservative financial management. The board approved "
        "a 15% increase in the quarterly dividend to $0.92 per share and authorized a $200 million "
        "share repurchase program for fiscal 2025.\n\n"
        "Looking ahead, management projects revenue growth of 8-10% in fiscal 2025, supported by "
        "continued momentum in recurring subscription revenue and the full-year contribution from "
        "the Nexus Analytics integration. We remain focused on disciplined capital allocation and "
        "operational efficiency improvements across all business segments."
    )
    rect = pymupdf.Rect(50, 120, 562, 700)
    p.insert_textbox(rect, exec_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGE 4: Revenue Analysis ==========
    p = doc.new_page(width=W, height=H)
    add_page_header(p, "Revenue Analysis", 4, 15)
    p.insert_text(pymupdf.Point(50, 90), "2. Revenue Analysis", fontsize=18, fontname="hebo", color=(0.15, 0.25, 0.45))
    p.insert_text(pymupdf.Point(50, 125), "Revenue by Business Segment (in millions USD)", fontsize=12, fontname="hebo", color=(0, 0, 0))

    # Revenue table
    y_start = 150
    headers = ["Segment", "FY 2024", "FY 2023", "Change", "% Growth"]
    col_x = [55, 180, 280, 380, 470]
    for i, h in enumerate(headers):
        p.insert_text(pymupdf.Point(col_x[i], y_start), h, fontsize=10, fontname="hebo", color=(1, 1, 1))
    # Header background
    shape = p.new_shape()
    shape.draw_rect(pymupdf.Rect(50, y_start - 14, 560, y_start + 4))
    shape.finish(fill=(0.15, 0.25, 0.45))
    shape.commit()
    # Re-draw header text on top
    for i, h in enumerate(headers):
        p.insert_text(pymupdf.Point(col_x[i], y_start), h, fontsize=10, fontname="hebo", color=(1, 1, 1))

    rev_data = [
        ["Technology Solutions", "$312.5", "$271.8", "+$40.7", "15.0%"],
        ["Healthcare Services", "$198.4", "$178.2", "+$20.2", "11.3%"],
        ["Financial Advisory", "$156.3", "$142.6", "+$13.7", "9.6%"],
        ["Data Analytics", "$89.7", "$52.4", "+$37.3", "71.2%"],
        ["Other Services", "$90.4", "$108.4", "-$18.0", "-16.6%"],
        ["Total Revenue", "$847.3", "$753.4", "+$93.9", "12.4%"],
    ]
    for r, row in enumerate(rev_data):
        y = y_start + 24 + r * 22
        fn = "hebo" if r == len(rev_data) - 1 else "helv"
        for c, val in enumerate(row):
            p.insert_text(pymupdf.Point(col_x[c], y), val, fontsize=10, fontname=fn, color=(0, 0, 0))

    # Narrative
    rev_narrative = (
        "Revenue growth was led by the Technology Solutions segment, which benefited from "
        "strong demand for enterprise software licenses and a 23% increase in recurring "
        "subscription revenue. The Data Analytics segment saw the highest percentage growth, "
        "largely attributable to the Nexus Analytics acquisition completed in Q2 2024. The "
        "decline in Other Services reflects the strategic wind-down of legacy consulting "
        "engagements as the company reallocates resources to higher-margin activities."
    )
    rect = pymupdf.Rect(50, y_start + 180, 562, 550)
    p.insert_textbox(rect, rev_narrative, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGE 5: Expense Breakdown ==========
    p = doc.new_page(width=W, height=H)
    add_page_header(p, "Expense Breakdown", 5, 15)
    p.insert_text(pymupdf.Point(50, 90), "3. Expense Breakdown", fontsize=18, fontname="hebo", color=(0.15, 0.25, 0.45))
    p.insert_text(pymupdf.Point(50, 125), "Operating Expenses Summary (in millions USD)", fontsize=12, fontname="hebo", color=(0, 0, 0))

    expense_items = [
        ("Cost of Revenue", "$423.7", "50.0%"),
        ("Research and Development", "$101.7", "12.0%"),
        ("Sales and Marketing", "$76.3", "9.0%"),
        ("General and Administrative", "$47.0", "5.5%"),
        ("Depreciation and Amortization", "$33.9", "4.0%"),
        ("Restructuring Charges", "$8.5", "1.0%"),
    ]
    y = 155
    for name, amount, pct in expense_items:
        p.insert_text(pymupdf.Point(70, y), name, fontsize=11, fontname="helv", color=(0, 0, 0))
        p.insert_text(pymupdf.Point(350, y), amount, fontsize=11, fontname="helv", color=(0, 0, 0))
        p.insert_text(pymupdf.Point(470, y), pct, fontsize=11, fontname="helv", color=(0.4, 0.4, 0.4))
        y += 24

    expense_text = (
        "Total operating expenses for fiscal year 2024 were $691.1 million, representing "
        "81.6% of total revenue. Cost of revenue increased by $38.2 million year-over-year, "
        "primarily due to higher personnel costs associated with scaling the Technology Solutions "
        "and Healthcare Services divisions. Research and development spending increased by 18.3%, "
        "reflecting investments in the CloudBridge platform and artificial intelligence capabilities. "
        "Restructuring charges of $8.5 million relate to the consolidation of three regional offices "
        "and the integration of Nexus Analytics operations."
    )
    rect = pymupdf.Rect(50, y + 30, 562, 600)
    p.insert_textbox(rect, expense_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGE 6: Quarterly Performance ==========
    p = doc.new_page(width=W, height=H)
    add_page_header(p, "Quarterly Performance", 6, 15)
    p.insert_text(pymupdf.Point(50, 90), "4. Quarterly Performance", fontsize=18, fontname="hebo", color=(0.15, 0.25, 0.45))
    p.insert_text(pymupdf.Point(50, 125), "Quarterly Revenue and Income (in millions USD)", fontsize=12, fontname="hebo", color=(0, 0, 0))

    q_data = [
        ["Metric", "Q1", "Q2", "Q3", "Q4", "Full Year"],
        ["Revenue", "$192.4", "$204.8", "$218.6", "$231.5", "$847.3"],
        ["Gross Profit", "$89.2", "$98.7", "$110.3", "$125.4", "$423.6"],
        ["Operating Income", "$38.5", "$45.2", "$52.8", "$62.1", "$198.6"],
        ["Net Income", "$27.8", "$32.4", "$38.1", "$44.5", "$142.8"],
        ["EPS (Diluted)", "$0.82", "$0.96", "$1.13", "$1.32", "$4.23"],
    ]
    y = 155
    for r, row in enumerate(q_data):
        fn = "hebo" if r == 0 else "helv"
        clr = (1, 1, 1) if r == 0 else (0, 0, 0)
        x_positions = [55, 170, 250, 330, 410, 490]
        for c, val in enumerate(row):
            p.insert_text(pymupdf.Point(x_positions[c], y), val, fontsize=10, fontname=fn, color=clr)
        if r == 0:
            shape = p.new_shape()
            shape.draw_rect(pymupdf.Rect(50, y - 14, 560, y + 4))
            shape.finish(fill=(0.15, 0.25, 0.45))
            shape.commit()
            for c, val in enumerate(row):
                p.insert_text(pymupdf.Point(x_positions[c], y), val, fontsize=10, fontname=fn, color=clr)
        y += 22

    q_text = (
        "The company demonstrated consistent sequential improvement across all quarters, with "
        "Q4 delivering the strongest performance. Revenue growth accelerated from 8.2% in Q1 to "
        "16.8% in Q4, driven by seasonal enterprise software purchasing and the full-quarter impact "
        "of the Nexus Analytics acquisition. Gross margin expanded from 46.4% in Q1 to 54.2% in Q4, "
        "reflecting improved operational leverage and higher-margin subscription revenue mix. "
        "Management expects this upward trajectory to continue into fiscal 2025 Q1."
    )
    rect = pymupdf.Rect(50, y + 30, 562, 550)
    p.insert_textbox(rect, q_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGE 7: Balance Sheet ==========
    p = doc.new_page(width=W, height=H)
    add_page_header(p, "Balance Sheet", 7, 15)
    p.insert_text(pymupdf.Point(50, 90), "5. Balance Sheet Overview", fontsize=18, fontname="hebo", color=(0.15, 0.25, 0.45))
    p.insert_text(pymupdf.Point(50, 125), "Consolidated Balance Sheet as of December 31, 2024 (in millions USD)", fontsize=11, fontname="hebo", color=(0, 0, 0))

    bs_items = [
        ("ASSETS", "", True),
        ("Cash and Cash Equivalents", "$284.3"),
        ("Short-term Investments", "$156.8"),
        ("Accounts Receivable", "$198.5"),
        ("Inventory", "$42.1"),
        ("Prepaid Expenses", "$23.7"),
        ("Total Current Assets", "$705.4"),
        ("Property, Plant & Equipment", "$412.6"),
        ("Goodwill and Intangibles", "$687.2"),
        ("Long-term Investments", "$214.8"),
        ("Other Non-Current Assets", "$120.0"),
        ("Total Assets", "$2,140.0"),
        ("", ""),
        ("LIABILITIES AND EQUITY", "", True),
        ("Accounts Payable", "$87.3"),
        ("Accrued Expenses", "$124.6"),
        ("Short-term Debt", "$45.0"),
        ("Total Current Liabilities", "$256.9"),
        ("Long-term Debt", "$385.0"),
        ("Deferred Tax Liabilities", "$67.4"),
        ("Other Long-term Liabilities", "$42.7"),
        ("Total Liabilities", "$752.0"),
        ("Total Shareholders' Equity", "$1,388.0"),
        ("Total Liabilities and Equity", "$2,140.0"),
    ]
    y = 155
    for item in bs_items:
        if len(item) == 3:  # section header
            p.insert_text(pymupdf.Point(55, y), item[0], fontsize=11, fontname="hebo", color=(0.15, 0.25, 0.45))
        elif item[0] == "":
            pass
        elif item[0].startswith("Total"):
            p.insert_text(pymupdf.Point(70, y), item[0], fontsize=10, fontname="hebo", color=(0, 0, 0))
            p.insert_text(pymupdf.Point(420, y), item[1], fontsize=10, fontname="hebo", color=(0, 0, 0))
        else:
            p.insert_text(pymupdf.Point(80, y), item[0], fontsize=10, fontname="helv", color=(0, 0, 0))
            p.insert_text(pymupdf.Point(420, y), item[1], fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 20

    # ========== PAGE 8: Cash Flow Statement ==========
    p = doc.new_page(width=W, height=H)
    add_page_header(p, "Cash Flow", 8, 15)
    p.insert_text(pymupdf.Point(50, 90), "6. Cash Flow Statement", fontsize=18, fontname="hebo", color=(0.15, 0.25, 0.45))

    cf_text = (
        "Cash Flow from Operating Activities\n\n"
        "Net income for fiscal year 2024 totaled $142.8 million. After adjustments for "
        "depreciation and amortization of $33.9 million, stock-based compensation of $28.4 million, "
        "and changes in working capital of negative $15.2 million, net cash provided by operating "
        "activities was $189.9 million.\n\n"
        "Cash Flow from Investing Activities\n\n"
        "Capital expenditures totaled $78.3 million, primarily for technology infrastructure "
        "upgrades and new office facilities. The acquisition of Nexus Analytics utilized $65.0 million "
        "in cash, net of cash acquired. Purchases of short-term investments amounted to $42.5 million, "
        "partially offset by maturities of $38.7 million. Net cash used in investing activities was "
        "$147.1 million.\n\n"
        "Cash Flow from Financing Activities\n\n"
        "The company repaid $25.0 million of long-term debt and paid dividends of $108.7 million. "
        "Proceeds from employee stock option exercises contributed $18.3 million. Share repurchases "
        "under the existing authorization totaled $75.0 million. Net cash used in financing activities "
        "was $190.4 million.\n\n"
        "Net decrease in cash and cash equivalents was $147.6 million, resulting in an ending cash "
        "balance of $284.3 million as of December 31, 2024."
    )
    rect = pymupdf.Rect(50, 120, 562, 720)
    p.insert_textbox(rect, cf_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGE 9: Regional Performance ==========
    p = doc.new_page(width=W, height=H)
    add_page_header(p, "Regional Performance", 9, 15)
    p.insert_text(pymupdf.Point(50, 90), "7. Regional Performance", fontsize=18, fontname="hebo", color=(0.15, 0.25, 0.45))
    p.insert_text(pymupdf.Point(50, 125), "Revenue by Geographic Region (in millions USD)", fontsize=12, fontname="hebo", color=(0, 0, 0))

    regions = [
        ("North America", "$524.6", "61.9%", "+9.8%"),
        ("Europe", "$168.3", "19.9%", "+7.2%"),
        ("Asia Pacific", "$98.5", "11.6%", "+34.6%"),
        ("Latin America", "$33.2", "3.9%", "+18.5%"),
        ("Middle East & Africa", "$22.7", "2.7%", "+11.3%"),
    ]
    y = 160
    # Headers
    for i, h in enumerate(["Region", "Revenue", "% of Total", "YoY Growth"]):
        p.insert_text(pymupdf.Point([60, 260, 370, 470][i], y), h, fontsize=10, fontname="hebo", color=(0, 0, 0))
    y += 24
    for name, rev, pct, growth in regions:
        p.insert_text(pymupdf.Point(60, y), name, fontsize=10, fontname="helv", color=(0, 0, 0))
        p.insert_text(pymupdf.Point(260, y), rev, fontsize=10, fontname="helv", color=(0, 0, 0))
        p.insert_text(pymupdf.Point(370, y), pct, fontsize=10, fontname="helv", color=(0, 0, 0))
        p.insert_text(pymupdf.Point(470, y), growth, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 22

    region_text = (
        "North America remains the largest revenue contributor, anchored by strong enterprise "
        "demand in the United States and Canada. Asia Pacific demonstrated the highest growth rate, "
        "driven by the expansion into Singapore, Vietnam, and the Philippines during Q2 2024. The "
        "newly established regional headquarters in Singapore is expected to support continued "
        "momentum in fiscal 2025. European revenues grew modestly, impacted by currency headwinds "
        "of approximately $8.4 million. Latin American growth was fueled by new partnerships with "
        "major financial institutions in Brazil and Mexico."
    )
    rect = pymupdf.Rect(50, y + 30, 562, 600)
    p.insert_textbox(rect, region_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGE 10: Product Line Analysis ==========
    p = doc.new_page(width=W, height=H)
    add_page_header(p, "Product Line Analysis", 10, 15)
    p.insert_text(pymupdf.Point(50, 90), "8. Product Line Analysis", fontsize=18, fontname="hebo", color=(0.15, 0.25, 0.45))

    product_text = (
        "CloudBridge Platform\n\n"
        "Launched in Q1 2024, CloudBridge is our flagship cloud-native enterprise integration "
        "platform. First-year revenue reached $38.2 million with 847 enterprise customers onboarded. "
        "Annual recurring revenue (ARR) at year-end stood at $52.4 million, reflecting strong "
        "month-over-month subscription growth. Customer retention rate exceeded 94%, and net dollar "
        "retention was 118%, indicating significant expansion within existing accounts.\n\n"
        "MedConnect Suite\n\n"
        "Our healthcare data management platform generated $124.6 million in revenue, a 14.2% "
        "increase year-over-year. Key wins included contracts with three major hospital systems "
        "covering over 1,200 facilities. The platform now processes over 2.3 million patient "
        "transactions daily. Integration with electronic health record systems expanded to support "
        "15 major EHR vendors.\n\n"
        "Nexus Analytics Engine\n\n"
        "Following the acquisition in Q2 2024, the Nexus Analytics Engine contributed $52.1 million "
        "in revenue for the period. The platform serves 423 enterprise clients with advanced "
        "predictive analytics and machine learning capabilities. Post-acquisition integration is "
        "proceeding ahead of schedule, with $12.3 million in annualized cost synergies identified.\n\n"
        "FinGuard Compliance Suite\n\n"
        "Revenue from our regulatory compliance platform grew 8.7% to $87.4 million. New regulatory "
        "requirements in the EU and Asia Pacific drove demand for enhanced monitoring and reporting "
        "capabilities. The platform now covers regulatory frameworks across 38 jurisdictions."
    )
    rect = pymupdf.Rect(50, 120, 562, 740)
    p.insert_textbox(rect, product_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGE 11: Employee Compensation ==========
    p = doc.new_page(width=W, height=H)
    add_page_header(p, "Compensation", 11, 15)
    p.insert_text(pymupdf.Point(50, 90), "9. Employee Compensation and Benefits", fontsize=18, fontname="hebo", color=(0.15, 0.25, 0.45))

    emp_text = (
        "As of December 31, 2024, Meridian Capital Group employed 8,472 full-time employees "
        "across 24 global offices, representing a net increase of 1,126 positions from the prior "
        "year. The increase includes 634 employees from the Nexus Analytics acquisition.\n\n"
        "Total compensation expense for fiscal 2024 was $487.3 million, comprising:\n\n"
        "Base salaries and wages: $312.8 million\n"
        "Performance bonuses: $67.4 million\n"
        "Stock-based compensation: $28.4 million\n"
        "Health and welfare benefits: $48.2 million\n"
        "Retirement plan contributions: $19.8 million\n"
        "Other compensation: $10.7 million\n\n"
        "The average compensation per employee was approximately $57,500 in base salary. "
        "Senior management compensation included both cash and equity components, with long-term "
        "incentive awards vesting over four-year periods tied to cumulative revenue growth and "
        "total shareholder return targets.\n\n"
        "Employee satisfaction scores improved to 4.2 out of 5.0, up from 3.9 in fiscal 2023. "
        "Voluntary turnover decreased to 11.3% from 14.7%, reflecting investments in professional "
        "development programs, flexible work arrangements, and enhanced parental leave policies. "
        "The company invested $14.2 million in employee training and development initiatives."
    )
    rect = pymupdf.Rect(50, 120, 562, 720)
    p.insert_textbox(rect, emp_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGE 12: Capital Expenditures ==========
    p = doc.new_page(width=W, height=H)
    add_page_header(p, "Capital Expenditures", 12, 15)
    p.insert_text(pymupdf.Point(50, 90), "10. Capital Expenditures", fontsize=18, fontname="hebo", color=(0.15, 0.25, 0.45))

    capex_text = (
        "Total capital expenditures for fiscal 2024 amounted to $78.3 million, allocated across "
        "the following categories:\n\n"
        "Technology Infrastructure: $34.7 million\n"
        "Investments in cloud computing capacity, data center expansion, and cybersecurity "
        "infrastructure. This includes the build-out of two new Tier IV data centers in Dallas and "
        "Frankfurt to support CloudBridge platform scaling requirements.\n\n"
        "Office Facilities: $18.9 million\n"
        "Lease improvements and equipment for the new Singapore regional headquarters, expansion "
        "of the Austin innovation campus, and renovation of the New York headquarters building.\n\n"
        "Research and Development Equipment: $14.2 million\n"
        "Specialized hardware for AI model training, quantum computing research infrastructure, "
        "and laboratory equipment for the healthcare technology division.\n\n"
        "Other Capital Projects: $10.5 million\n"
        "Vehicle fleet upgrades for the field services team, furniture and fixtures for newly "
        "acquired office spaces, and enterprise resource planning system modernization.\n\n"
        "Capital expenditures as a percentage of revenue was 9.2%, compared to 8.5% in fiscal 2023. "
        "Management anticipates a similar level of investment in fiscal 2025 as the company continues "
        "to scale its cloud infrastructure and expand internationally."
    )
    rect = pymupdf.Rect(50, 120, 562, 740)
    p.insert_textbox(rect, capex_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGE 13: Risk Assessment ==========
    p = doc.new_page(width=W, height=H)
    add_page_header(p, "Risk Assessment", 13, 15)
    p.insert_text(pymupdf.Point(50, 90), "11. Risk Assessment and Mitigation", fontsize=18, fontname="hebo", color=(0.15, 0.25, 0.45))

    risk_text = (
        "Cybersecurity Risk\n"
        "As a technology company handling sensitive enterprise and healthcare data, cybersecurity "
        "remains our highest priority risk area. During fiscal 2024, we invested $22.8 million in "
        "security operations, achieved SOC 2 Type II certification for all platforms, and "
        "implemented zero-trust architecture across the organization. No material data breaches "
        "occurred during the reporting period.\n\n"
        "Regulatory and Compliance Risk\n"
        "The evolving regulatory landscape, particularly the EU AI Act and updated HIPAA requirements, "
        "requires ongoing adaptation. Our FinGuard platform team proactively updated compliance "
        "modules, and we expanded the legal and compliance team by 23 professionals.\n\n"
        "Market and Competition Risk\n"
        "The enterprise software market remains highly competitive, with major technology firms "
        "and well-funded startups competing for market share. We mitigate this through continuous "
        "product innovation, deep customer relationships, and strategic acquisitions.\n\n"
        "Foreign Currency Risk\n"
        "With 38.1% of revenue generated outside North America, currency fluctuations represent "
        "a material risk. We utilize forward contracts and natural hedging strategies. Currency "
        "headwinds reduced fiscal 2024 revenue by approximately $14.2 million.\n\n"
        "Integration Risk\n"
        "The successful integration of Nexus Analytics remains a key execution risk. Dedicated "
        "integration teams and milestone-based tracking ensure alignment with projected synergies."
    )
    rect = pymupdf.Rect(50, 120, 562, 740)
    p.insert_textbox(rect, risk_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGE 14: Forward-Looking Projections ==========
    p = doc.new_page(width=W, height=H)
    add_page_header(p, "Projections", 14, 15)
    p.insert_text(pymupdf.Point(50, 90), "12. Forward-Looking Projections", fontsize=18, fontname="hebo", color=(0.15, 0.25, 0.45))

    proj_text = (
        "Revenue Guidance\n"
        "Management projects total revenue of $915 million to $935 million for fiscal 2025, "
        "representing year-over-year growth of 8% to 10%. This guidance assumes continued organic "
        "growth momentum in Technology Solutions and Healthcare Services, a full year of Nexus "
        "Analytics contribution, and stable macroeconomic conditions.\n\n"
        "Margin Targets\n"
        "Operating margin is expected to expand to 24.5% to 25.5%, up from 23.4% in fiscal 2024, "
        "driven by operating leverage, Nexus Analytics integration synergies, and an increasing mix "
        "of recurring subscription revenue.\n\n"
        "Strategic Initiatives for Fiscal 2025\n\n"
        "1. Launch of CloudBridge 2.0 with enhanced AI capabilities in Q2 2025\n"
        "2. Expansion into three additional Southeast Asian markets\n"
        "3. Completion of Nexus Analytics integration by end of Q3 2025\n"
        "4. Establishment of dedicated AI research laboratory in Boston\n"
        "5. Launch of FinGuard 4.0 covering new EU regulatory frameworks\n\n"
        "Capital Allocation\n"
        "The Board has authorized a $200 million share repurchase program and approved a 15% "
        "dividend increase to $0.92 per share quarterly. Capital expenditures are projected at "
        "$80 million to $90 million, focused on cloud infrastructure and international expansion. "
        "Management remains open to value-accretive acquisition opportunities in adjacent markets."
    )
    rect = pymupdf.Rect(50, 120, 562, 740)
    p.insert_textbox(rect, proj_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGE 15: Auditor's Notes ==========
    p = doc.new_page(width=W, height=H)
    add_page_header(p, "Auditor's Notes", 15, 15)
    p.insert_text(pymupdf.Point(50, 90), "13. Auditor's Notes and Disclosures", fontsize=18, fontname="hebo", color=(0.15, 0.25, 0.45))

    audit_text = (
        "Independent Auditor's Report\n\n"
        "To the Board of Directors and Shareholders of Meridian Capital Group:\n\n"
        "We have audited the accompanying consolidated financial statements of Meridian Capital "
        "Group and its subsidiaries as of and for the fiscal year ended December 31, 2024. These "
        "financial statements are the responsibility of the Company's management. Our responsibility "
        "is to express an opinion on these financial statements based on our audit.\n\n"
        "We conducted our audit in accordance with the standards of the Public Company Accounting "
        "Oversight Board (United States). Those standards require that we plan and perform the audit "
        "to obtain reasonable assurance about whether the financial statements are free of material "
        "misstatement.\n\n"
        "In our opinion, the consolidated financial statements referred to above present fairly, in "
        "all material respects, the financial position of Meridian Capital Group and its subsidiaries "
        "as of December 31, 2024, and the results of their operations and their cash flows for the "
        "year then ended, in conformity with accounting principles generally accepted in the United "
        "States of America.\n\n"
        "Basis for Opinion\n\n"
        "We identified no material weaknesses in internal control over financial reporting. Revenue "
        "recognition policies were reviewed and found to be in compliance with ASC 606. The goodwill "
        "impairment assessment for the Nexus Analytics reporting unit was evaluated and deemed "
        "appropriate given current market conditions and projected cash flows.\n\n"
        "Signed: Whitmore & Associates LLP\n"
        "Certified Public Accountants\n"
        "March 1, 2025"
    )
    rect = pymupdf.Rect(50, 120, 562, 740)
    p.insert_textbox(rect, audit_text, fontsize=11, fontname="helv", color=(0, 0, 0), align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # Save the document
    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 15')

    # Ensure no JSON file exists (negative constraint)
    json_path = f'{DOCS_DIR}/financial_report_text.json'
    if os.path.exists(json_path):
        os.remove(json_path)
        print(f'Removed pre-existing JSON file: {json_path}')

    # GUI-ready: open PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_financial_report()
