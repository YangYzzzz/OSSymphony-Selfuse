"""
Initial Setup: Create a 25-page financial report PDF with section references on page 1.
Task ID: pdf_fin_075
Domain: pdf

The report has text references to Income Statement (page 10), Balance Sheet (page 15),
and Cash Flow (page 20) on page 1, but NO clickable hyperlinks yet.
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_075'
FINANCE_DIR = f'{WORKDIR}/finance'
OUTPUT = f'{FINANCE_DIR}/report_with_refs.pdf'

# Page dimensions (Letter size)
W, H = 612, 792


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


def add_page_header(page, title, page_num):
    """Add a consistent header and footer to each page."""
    # Header line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(50, 55), pymupdf.Point(W - 50, 55))
    shape.finish(color=(0.2, 0.3, 0.5), width=1.5)
    shape.commit()

    # Header text
    page.insert_text(pymupdf.Point(50, 45), "Meridian Global Partners, Inc.",
                     fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text(pymupdf.Point(W - 200, 45), "Annual Financial Report FY2025",
                     fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))

    # Footer
    page.insert_text(pymupdf.Point(50, H - 30), "Confidential",
                     fontsize=8, fontname="heit", color=(0.5, 0.5, 0.5))
    page.insert_text(pymupdf.Point(W - 100, H - 30), f"Page {page_num}",
                     fontsize=8, fontname="helv", color=(0.5, 0.5, 0.5))


def create_cover_page(doc):
    """Page 1: Cover / Table of Contents with section references (NO links)."""
    page = doc.new_page(width=W, height=H)

    # Company title
    page.insert_text(pymupdf.Point(100, 80), "MERIDIAN GLOBAL PARTNERS, INC.",
                     fontsize=22, fontname="hebo", color=(0.1, 0.2, 0.4))

    # Report title
    page.insert_text(pymupdf.Point(100, 115), "Annual Financial Report",
                     fontsize=18, fontname="hebo", color=(0.2, 0.3, 0.5))
    page.insert_text(pymupdf.Point(100, 140), "Fiscal Year Ending December 31, 2025",
                     fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))

    # Decorative line
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(100, 155), pymupdf.Point(500, 155))
    shape.finish(color=(0.2, 0.3, 0.5), width=2)
    shape.commit()

    # Table of Contents heading
    page.insert_text(pymupdf.Point(100, 185), "TABLE OF CONTENTS",
                     fontsize=14, fontname="hebo", color=(0.1, 0.2, 0.4))

    # Section references - these are plain text at the exact rects where links will go
    # Rect (100,200,300,215) - Income Statement reference
    page.insert_text(pymupdf.Point(100, 212), "Income Statement",
                     fontsize=11, fontname="helv", color=(0.0, 0.0, 0.6))
    page.insert_text(pymupdf.Point(310, 212), "............................... Page 10",
                     fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))

    # Rect (100,220,300,235) - Balance Sheet reference
    page.insert_text(pymupdf.Point(100, 232), "Balance Sheet",
                     fontsize=11, fontname="helv", color=(0.0, 0.0, 0.6))
    page.insert_text(pymupdf.Point(310, 232), "............................... Page 15",
                     fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))

    # Rect (100,240,300,255) - Cash Flow reference
    page.insert_text(pymupdf.Point(100, 252), "Cash Flow Statement",
                     fontsize=11, fontname="helv", color=(0.0, 0.0, 0.6))
    page.insert_text(pymupdf.Point(310, 252), "............................... Page 20",
                     fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))

    # Additional TOC entries
    y = 280
    other_sections = [
        ("Executive Summary", "2"),
        ("Company Overview", "3"),
        ("Market Analysis", "5"),
        ("Revenue Breakdown", "7"),
        ("Operating Expenses", "9"),
        ("Shareholder Equity", "22"),
        ("Notes to Financial Statements", "23"),
        ("Auditor's Report", "25"),
    ]
    for section, pg in other_sections:
        page.insert_text(pymupdf.Point(100, y), section,
                         fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
        page.insert_text(pymupdf.Point(310, y), f"............................... Page {pg}",
                         fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
        y += 18

    # Footer note
    page.insert_text(pymupdf.Point(100, H - 80),
                     "This document contains confidential financial information.",
                     fontsize=9, fontname="heit", color=(0.5, 0.5, 0.5))
    page.insert_text(pymupdf.Point(100, H - 65),
                     "Prepared by the Office of the Chief Financial Officer.",
                     fontsize=9, fontname="heit", color=(0.5, 0.5, 0.5))

    return page


def add_text_page(doc, page_num, title, paragraphs):
    """Add a content page with title and paragraphs."""
    page = doc.new_page(width=W, height=H)
    add_page_header(page, title, page_num)

    # Section title
    page.insert_text(pymupdf.Point(50, 90), title,
                     fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.4))

    # Underline
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(50, 98), pymupdf.Point(W - 50, 98))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()

    y = 125
    for para in paragraphs:
        rect = pymupdf.Rect(50, y, W - 50, y + 80)
        excess = page.insert_textbox(rect, para,
                                     fontsize=10, fontname="helv",
                                     color=(0.15, 0.15, 0.15),
                                     align=pymupdf.TEXT_ALIGN_JUSTIFY)
        y += 85
        if y > H - 80:
            break

    return page


def add_financial_table_page(doc, page_num, title, headers, data):
    """Add a page with a financial data table."""
    page = doc.new_page(width=W, height=H)
    add_page_header(page, title, page_num)

    page.insert_text(pymupdf.Point(50, 90), title,
                     fontsize=16, fontname="hebo", color=(0.1, 0.2, 0.4))

    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(50, 98), pymupdf.Point(W - 50, 98))
    shape.finish(color=(0.7, 0.7, 0.7), width=0.5)
    shape.commit()

    # Table header background
    y_start = 115
    col_widths = [180, 100, 100, 100]
    x_positions = [50]
    for cw in col_widths[:-1]:
        x_positions.append(x_positions[-1] + cw)

    shape2 = page.new_shape()
    shape2.draw_rect(pymupdf.Rect(50, y_start, W - 82, y_start + 20))
    shape2.finish(fill=(0.2, 0.3, 0.5), color=(0.2, 0.3, 0.5))
    shape2.commit()

    # Header text
    for i, h in enumerate(headers):
        page.insert_text(pymupdf.Point(x_positions[i] + 5, y_start + 14), h,
                         fontsize=9, fontname="hebo", color=(1, 1, 1))

    # Data rows
    y = y_start + 25
    for row_idx, row in enumerate(data):
        # Alternating row background
        if row_idx % 2 == 0:
            shape3 = page.new_shape()
            shape3.draw_rect(pymupdf.Rect(50, y - 4, W - 82, y + 14))
            shape3.finish(fill=(0.95, 0.95, 0.97), color=(0.95, 0.95, 0.97))
            shape3.commit()

        for i, val in enumerate(row):
            page.insert_text(pymupdf.Point(x_positions[i] + 5, y + 10), str(val),
                             fontsize=9, fontname="helv", color=(0.15, 0.15, 0.15))
        y += 18
        if y > H - 80:
            break

    return page


def create_initial():
    os.makedirs(FINANCE_DIR, exist_ok=True)

    doc = pymupdf.open()

    # === Page 1: Cover / TOC ===
    create_cover_page(doc)

    # === Page 2: Executive Summary ===
    add_text_page(doc, 2, "Executive Summary", [
        "Meridian Global Partners delivered strong financial results in fiscal year 2025, "
        "achieving record revenue of $4.87 billion, representing a 12.3% increase year-over-year. "
        "Net income grew 18.7% to $623 million, driven by operational efficiency improvements "
        "and strategic investments in high-growth markets.",
        "Our diversified portfolio across technology services, financial consulting, and healthcare "
        "solutions continued to provide resilience against market volatility. The technology services "
        "division led growth with a 22% revenue increase, while our consulting practice maintained "
        "steady margins above 28%.",
        "Capital expenditures totaled $312 million, primarily directed toward data center expansion "
        "and AI-driven analytics platforms. We returned $445 million to shareholders through dividends "
        "and share repurchases, reflecting our commitment to sustainable value creation.",
        "Looking ahead, management remains confident in achieving 10-15% revenue growth in FY2026, "
        "supported by a robust pipeline of enterprise contracts and expanding market presence in "
        "Southeast Asia and Latin America.",
    ])

    # === Page 3: Company Overview ===
    add_text_page(doc, 3, "Company Overview", [
        "Founded in 1998, Meridian Global Partners has evolved from a regional consulting firm "
        "into a multinational conglomerate serving Fortune 500 clients across 42 countries. "
        "Headquartered in Chicago, Illinois, the company employs approximately 28,500 professionals.",
        "Our three core business segments are: Technology Services (48% of revenue), Financial "
        "Consulting (32% of revenue), and Healthcare Solutions (20% of revenue). Each segment "
        "operates with dedicated leadership teams and autonomous P&L responsibility.",
        "The company's competitive advantage stems from its proprietary analytics platform, "
        "MeridianIQ, which leverages machine learning to deliver predictive insights for enterprise "
        "clients. The platform processes over 2.3 petabytes of data daily.",
        "Key clients include Northwind Pharmaceuticals, Contoso Manufacturing, Fabrikam Technologies, "
        "and Woodgrove Financial Group, representing approximately 35% of total revenue.",
    ])

    # === Page 4: Company Overview continued ===
    add_text_page(doc, 4, "Company Overview (continued)", [
        "Our global footprint spans offices in 18 major metropolitan areas, including New York, "
        "London, Singapore, Tokyo, Sydney, Frankfurt, and Sao Paulo. Regional hubs coordinate "
        "service delivery and maintain client relationships across time zones.",
        "The Board of Directors comprises 11 members, including 8 independent directors with "
        "diverse expertise spanning finance, technology, law, and international business. "
        "CEO Margaret Thornton has led the company since 2019, driving the digital transformation strategy.",
        "Meridian's corporate culture emphasizes innovation, integrity, and impact. The company "
        "has been recognized as a 'Best Place to Work' by Glassdoor for five consecutive years "
        "and maintains a 94% client retention rate.",
    ])

    # === Page 5: Market Analysis ===
    add_text_page(doc, 5, "Market Analysis", [
        "The global professional services market reached $6.2 trillion in 2025, with technology "
        "consulting and digital transformation services growing at 15% CAGR. Meridian is well-positioned "
        "to capture an increasing share of this expanding market.",
        "Key industry trends driving demand include: enterprise AI adoption (projected $180B market "
        "by 2027), cloud migration services, cybersecurity consulting, and ESG compliance advisory. "
        "Meridian has dedicated practices in each of these high-growth areas.",
        "Competitive landscape analysis indicates consolidation among mid-tier firms, creating "
        "opportunities for Meridian to acquire complementary capabilities. Management has identified "
        "three potential acquisition targets with combined revenue of $420 million.",
        "Emerging market expansion remains a strategic priority, with Southeast Asia projected to "
        "contribute 12% of revenue by FY2027, up from 6% currently. Recent partnerships with "
        "regional firms in Vietnam, Thailand, and Indonesia are accelerating market entry.",
    ])

    # === Page 6: Market Analysis continued ===
    add_text_page(doc, 6, "Market Analysis (continued)", [
        "Regulatory environments across our key markets continue to evolve. The EU's Digital Markets "
        "Act and AI Act create new compliance requirements that drive demand for our consulting services. "
        "Similarly, SEC climate disclosure rules in the US have generated substantial ESG advisory revenue.",
        "Client spending patterns show a shift toward multi-year engagement models, with 67% of new "
        "contracts signed in 2025 spanning 3+ years compared to 52% in 2023. This trend improves "
        "revenue visibility and supports more strategic resource planning.",
        "Technology disruption, particularly generative AI, presents both opportunity and risk. "
        "Our MeridianIQ platform incorporates large language models for automated report generation "
        "and anomaly detection, reducing delivery costs by an estimated 18% in affected service lines.",
    ])

    # === Page 7: Revenue Breakdown ===
    add_financial_table_page(doc, 7, "Revenue Breakdown by Segment", [
        "Segment", "FY2025 ($M)", "FY2024 ($M)", "Growth (%)"
    ], [
        ["Technology Services", "$2,337.6", "$1,916.0", "22.0%"],
        ["Financial Consulting", "$1,558.4", "$1,436.1", "8.5%"],
        ["Healthcare Solutions", "$974.0", "$886.2", "9.9%"],
        ["Total Revenue", "$4,870.0", "$4,238.3", "14.9%"],
        ["", "", "", ""],
        ["North America", "$2,678.5", "$2,415.8", "10.9%"],
        ["Europe", "$1,218.5", "$1,101.0", "10.7%"],
        ["Asia-Pacific", "$730.5", "$593.4", "23.1%"],
        ["Latin America", "$242.5", "$128.1", "89.3%"],
        ["Total Revenue", "$4,870.0", "$4,238.3", "14.9%"],
    ])

    # === Page 8: Revenue Breakdown continued ===
    add_financial_table_page(doc, 8, "Quarterly Revenue Summary", [
        "Quarter", "Revenue ($M)", "Gross Margin", "Operating Margin"
    ], [
        ["Q1 2025", "$1,120.5", "42.3%", "18.7%"],
        ["Q2 2025", "$1,185.2", "43.1%", "19.2%"],
        ["Q3 2025", "$1,243.8", "44.0%", "20.1%"],
        ["Q4 2025", "$1,320.5", "44.8%", "21.3%"],
        ["Full Year", "$4,870.0", "43.6%", "19.8%"],
        ["", "", "", ""],
        ["Q1 2024", "$985.3", "40.2%", "16.8%"],
        ["Q2 2024", "$1,025.7", "40.8%", "17.1%"],
        ["Q3 2024", "$1,078.4", "41.2%", "17.6%"],
        ["Q4 2024", "$1,148.9", "41.9%", "18.2%"],
        ["Full Year", "$4,238.3", "41.0%", "17.4%"],
    ])

    # === Page 9: Operating Expenses ===
    add_financial_table_page(doc, 9, "Operating Expenses Summary", [
        "Category", "FY2025 ($M)", "% of Revenue", "YoY Change"
    ], [
        ["Cost of Revenue", "$2,746.6", "56.4%", "+11.8%"],
        ["Research & Development", "$389.6", "8.0%", "+24.3%"],
        ["Sales & Marketing", "$535.7", "11.0%", "+15.1%"],
        ["General & Administrative", "$233.8", "4.8%", "+6.2%"],
        ["Depreciation & Amort.", "$178.4", "3.7%", "+8.9%"],
        ["Total Operating Expenses", "$4,084.1", "83.9%", "+12.7%"],
        ["Operating Income", "$785.9", "16.1%", "+22.4%"],
        ["", "", "", ""],
        ["Employee Compensation", "$1,898.4", "39.0%", "+13.2%"],
        ["Technology Infrastructure", "$438.3", "9.0%", "+19.8%"],
        ["Facility Costs", "$146.1", "3.0%", "+4.1%"],
        ["Professional Fees", "$97.4", "2.0%", "+7.3%"],
        ["Travel & Entertainment", "$121.8", "2.5%", "+28.6%"],
    ])

    # === Page 10: Income Statement ===
    add_financial_table_page(doc, 10, "Consolidated Income Statement", [
        "Line Item", "FY2025 ($M)", "FY2024 ($M)", "Change (%)"
    ], [
        ["Net Revenue", "$4,870.0", "$4,238.3", "+14.9%"],
        ["Cost of Revenue", "($2,746.6)", "($2,456.2)", "+11.8%"],
        ["Gross Profit", "$2,123.4", "$1,782.1", "+19.2%"],
        ["Operating Expenses", "($1,337.5)", "($1,166.1)", "+14.7%"],
        ["Operating Income", "$785.9", "$616.0", "+27.6%"],
        ["Interest Income", "$23.4", "$18.7", "+25.1%"],
        ["Interest Expense", "($45.2)", "($52.1)", "-13.2%"],
        ["Other Income/(Expense)", "$12.8", "($3.6)", "N/A"],
        ["Income Before Tax", "$776.9", "$579.0", "+34.2%"],
        ["Income Tax Expense", "($153.9)", "($104.2)", "+47.7%"],
        ["Net Income", "$623.0", "$474.8", "+31.2%"],
        ["", "", "", ""],
        ["Earnings Per Share (Basic)", "$8.42", "$6.38", "+32.0%"],
        ["Earnings Per Share (Diluted)", "$8.31", "$6.29", "+32.1%"],
        ["Weighted Avg Shares (M)", "74.0", "74.4", "-0.5%"],
    ])

    # === Pages 11-14: Income Statement supporting detail ===
    add_text_page(doc, 11, "Income Statement Notes", [
        "Revenue recognition follows ASC 606 principles. Technology services revenue is recognized "
        "over time as performance obligations are satisfied. Consulting engagements are billed on "
        "a time-and-materials or fixed-fee basis with revenue recognized proportionally.",
        "Cost of revenue includes direct labor, subcontractor costs, technology platform hosting, "
        "and allocated overhead. Gross margin improvement of 260 basis points reflects productivity "
        "gains from AI-assisted delivery and favorable project mix toward higher-margin engagements.",
        "Research and development expenses increased 24.3% year-over-year, driven by continued "
        "investment in the MeridianIQ platform and development of next-generation analytics tools. "
        "The company capitalized $67.2 million in software development costs during the period.",
    ])

    add_text_page(doc, 12, "Revenue Recognition Details", [
        "Performance obligations are identified at contract inception. Multi-element arrangements "
        "are allocated based on standalone selling prices using the expected cost plus margin approach "
        "for customized deliverables and observable prices for standardized offerings.",
        "Deferred revenue at December 31, 2025 totaled $384.7 million, compared to $312.5 million "
        "at the prior year end. The increase reflects the growing proportion of multi-year contracts "
        "with upfront billing components. Approximately 62% is expected to be recognized within 12 months.",
        "Contract assets (unbilled receivables) decreased to $167.3 million from $189.4 million, "
        "indicating improved billing cycles and reduced exposure to collection risk.",
    ])

    add_text_page(doc, 13, "Tax Provision Analysis", [
        "The effective tax rate for FY2025 was 19.8%, compared to 18.0% in FY2024. The increase "
        "reflects higher pre-tax income and a shift in geographic profit mix toward higher-tax "
        "jurisdictions, partially offset by increased R&D tax credits.",
        "Deferred tax assets totaled $89.3 million, primarily related to stock compensation, "
        "accrued liabilities, and net operating loss carryforwards in certain foreign subsidiaries. "
        "A valuation allowance of $12.1 million is maintained against NOLs with uncertain realizability.",
        "The company's tax position is subject to examination by various authorities. "
        "Management believes adequate reserves are maintained for all open tax years (2022-2025).",
    ])

    add_text_page(doc, 14, "Earnings Per Share Reconciliation", [
        "Basic earnings per share is computed by dividing net income by the weighted-average number "
        "of common shares outstanding. Diluted EPS includes the effect of potentially dilutive "
        "securities, including stock options and restricted stock units.",
        "The weighted-average diluted share count of 74.9 million includes 0.9 million shares from "
        "in-the-money stock options and unvested RSUs. Anti-dilutive securities excluded from the "
        "calculation totaled 0.3 million shares.",
        "The Board approved a $500 million share repurchase program in March 2025. As of December 31, "
        "$245 million remained available under this authorization. During FY2025, the company "
        "repurchased 1.8 million shares at an average price of $141.67 per share.",
    ])

    # === Page 15: Balance Sheet ===
    add_financial_table_page(doc, 15, "Consolidated Balance Sheet", [
        "Line Item", "Dec 31 2025", "Dec 31 2024", "Change"
    ], [
        ["ASSETS", "", "", ""],
        ["Cash & Equivalents", "$1,245.3", "$987.6", "+$257.7"],
        ["Short-term Investments", "$312.8", "$278.4", "+$34.4"],
        ["Accounts Receivable", "$876.5", "$762.3", "+$114.2"],
        ["Prepaid Expenses", "$89.4", "$76.8", "+$12.6"],
        ["Total Current Assets", "$2,524.0", "$2,105.1", "+$418.9"],
        ["Property & Equipment", "$567.2", "$498.3", "+$68.9"],
        ["Goodwill", "$1,834.6", "$1,723.1", "+$111.5"],
        ["Intangible Assets", "$423.7", "$389.2", "+$34.5"],
        ["Other Long-term Assets", "$198.5", "$167.4", "+$31.1"],
        ["Total Assets", "$5,548.0", "$4,883.1", "+$664.9"],
        ["", "", "", ""],
        ["LIABILITIES & EQUITY", "", "", ""],
        ["Accounts Payable", "$234.5", "$198.7", "+$35.8"],
        ["Accrued Liabilities", "$567.8", "$489.3", "+$78.5"],
        ["Total Current Liab.", "$1,287.3", "$1,098.4", "+$188.9"],
        ["Long-term Debt", "$892.0", "$1,023.5", "-$131.5"],
        ["Total Stockholders Eq.", "$2,876.4", "$2,412.8", "+$463.6"],
    ])

    # === Pages 16-19: Balance Sheet supporting detail ===
    add_text_page(doc, 16, "Balance Sheet Notes - Assets", [
        "Cash and cash equivalents include demand deposits and money market funds with original "
        "maturities of three months or less. The increase of $257.7 million reflects strong operating "
        "cash flow partially offset by capital expenditures and shareholder returns.",
        "Accounts receivable are presented net of an allowance for doubtful accounts of $18.9 million "
        "(FY2024: $16.2 million). Days sales outstanding improved to 65 days from 69 days in the "
        "prior year, reflecting enhanced collection processes.",
        "Goodwill of $1,834.6 million relates to acquisitions in the Technology Services ($1,124.3M) "
        "and Healthcare Solutions ($710.3M) segments. Annual impairment testing confirmed no impairment "
        "charges were required in FY2025.",
    ])

    add_text_page(doc, 17, "Balance Sheet Notes - Liabilities", [
        "Long-term debt decreased by $131.5 million to $892.0 million, reflecting scheduled principal "
        "repayments on our senior unsecured notes. The company's debt-to-EBITDA ratio improved to "
        "0.92x from 1.28x, well within our target of less than 2.0x.",
        "The revolving credit facility of $750 million remains undrawn at December 31, 2025. "
        "The facility carries a variable rate of SOFR + 1.25% and matures in June 2028. "
        "All financial covenants were met with substantial headroom.",
        "Lease liabilities totaled $234.8 million, comprising $45.2 million current and "
        "$189.6 million non-current. The company has commitments for new office leases in "
        "Singapore and Frankfurt commencing Q2 2026 with combined annual rent of $18.3 million.",
    ])

    add_text_page(doc, 18, "Stockholders' Equity Analysis", [
        "Total stockholders' equity increased $463.6 million to $2,876.4 million, driven by "
        "net income of $623.0 million, partially offset by dividends paid ($190.3 million) "
        "and share repurchases ($255.0 million).",
        "Accumulated other comprehensive loss decreased by $23.1 million to ($67.8 million), "
        "primarily due to favorable foreign currency translation adjustments as the U.S. dollar "
        "weakened against the Euro and British Pound.",
        "Stock-based compensation expense totaled $112.4 million in FY2025. The company granted "
        "1.2 million restricted stock units with a weighted-average grant date fair value of "
        "$138.50 per share. Approximately 0.8 million RSUs vested during the year.",
    ])

    add_text_page(doc, 19, "Working Capital Management", [
        "Net working capital (current assets minus current liabilities) improved to $1,236.7 million "
        "from $1,006.7 million. The $230.0 million improvement primarily reflects cash generation "
        "and disciplined management of receivables and payables.",
        "Inventory management is not a material factor for our services-based business model. "
        "However, prepaid software licenses and technology equipment purchases are managed through "
        "a centralized procurement function that achieved 6% cost savings in FY2025.",
        "Cash conversion cycle improved to 48 days from 53 days, reflecting the combined effect "
        "of faster collections, optimized billing processes, and strategic extension of payment "
        "terms with key vendors.",
    ])

    # === Page 20: Cash Flow Statement ===
    add_financial_table_page(doc, 20, "Consolidated Statement of Cash Flows", [
        "Line Item", "FY2025 ($M)", "FY2024 ($M)", "Change"
    ], [
        ["OPERATING ACTIVITIES", "", "", ""],
        ["Net Income", "$623.0", "$474.8", "+$148.2"],
        ["Depreciation & Amort.", "$178.4", "$163.8", "+$14.6"],
        ["Stock-based Compensation", "$112.4", "$96.7", "+$15.7"],
        ["Changes in Working Capital", "($45.2)", "($32.1)", "-$13.1"],
        ["Cash from Operations", "$868.6", "$703.2", "+$165.4"],
        ["", "", "", ""],
        ["INVESTING ACTIVITIES", "", "", ""],
        ["Capital Expenditures", "($312.0)", "($267.5)", "-$44.5"],
        ["Acquisitions, net", "($156.3)", "($89.4)", "-$66.9"],
        ["Investments", "($34.4)", "($52.8)", "+$18.4"],
        ["Cash from Investing", "($502.7)", "($409.7)", "-$93.0"],
        ["", "", "", ""],
        ["FINANCING ACTIVITIES", "", "", ""],
        ["Debt Repayments", "($131.5)", "($100.0)", "-$31.5"],
        ["Share Repurchases", "($255.0)", "($190.0)", "-$65.0"],
        ["Dividends Paid", "($190.3)", "($172.4)", "-$17.9"],
        ["Cash from Financing", "($576.8)", "($462.4)", "-$114.4"],
    ])

    # === Pages 21-25: Remaining content ===
    add_text_page(doc, 21, "Cash Flow Analysis", [
        "Operating cash flow of $868.6 million represented a 23.5% increase over the prior year, "
        "driven by higher net income and strong working capital management. Free cash flow "
        "(operating cash flow less CapEx) was $556.6 million, a 27.8% increase.",
        "Capital expenditures of $312.0 million were allocated across data center expansion "
        "($142.3M), technology platform development ($98.7M), and office infrastructure ($71.0M). "
        "We expect FY2026 CapEx to range between $330-360 million.",
        "Acquisition spending of $156.3 million relates to the purchase of DataVault Analytics (Q2) "
        "and HealthBridge Consulting (Q4). Both acquisitions are expected to be accretive to earnings "
        "within 18 months of closing.",
    ])

    add_financial_table_page(doc, 22, "Shareholder Equity Rollforward", [
        "Component", "Opening", "Changes", "Closing"
    ], [
        ["Common Stock", "$74.4M", "($0.4M)", "$74.0M"],
        ["Additional Paid-in Capital", "$1,245.6M", "$112.4M", "$1,358.0M"],
        ["Retained Earnings", "$1,184.1M", "$177.7M", "$1,361.8M"],
        ["Treasury Stock", "($0.0M)", "($255.0M)", "($255.0M)"],
        ["Accum. Other Comp. Income", "($90.9M)", "$23.1M", "($67.8M)"],
        ["Non-controlling Interest", "$79.6M", "($0.2M)", "$79.4M"],
        ["Total Equity", "$2,412.8M", "$463.6M", "$2,876.4M"],
    ])

    add_text_page(doc, 23, "Notes to Financial Statements", [
        "Note 1 - Basis of Presentation: These consolidated financial statements have been "
        "prepared in accordance with U.S. Generally Accepted Accounting Principles (GAAP) and "
        "include the accounts of Meridian Global Partners, Inc. and all majority-owned subsidiaries.",
        "Note 2 - Significant Accounting Policies: Revenue recognition follows ASC 606. "
        "Stock-based compensation is measured at fair value on the grant date using the "
        "Black-Scholes option pricing model for options and closing stock price for RSUs.",
        "Note 3 - Business Combinations: The acquisition of DataVault Analytics was completed "
        "on June 15, 2025 for total consideration of $98.7 million, comprising $82.3 million "
        "in cash and $16.4 million in Meridian common stock.",
        "Note 4 - Segment Information: The company operates in three reportable segments as "
        "described in the Company Overview section. Inter-segment transactions are eliminated "
        "in consolidation and are not material to reported results.",
    ])

    add_text_page(doc, 24, "Risk Factors", [
        "Economic Conditions: A prolonged economic downturn could reduce client spending on "
        "consulting and technology services. Revenue concentration in financial services and "
        "technology sectors creates exposure to sector-specific downturns.",
        "Talent Acquisition and Retention: Our business depends on attracting and retaining "
        "skilled professionals. Intense competition for talent, particularly in AI and data science, "
        "may increase compensation costs or impair our ability to staff engagements.",
        "Technology Disruption: Rapid advances in generative AI could commoditize certain "
        "service offerings, requiring continuous investment in differentiated capabilities. "
        "Failure to adapt could result in market share loss.",
        "Cybersecurity Risks: As a custodian of sensitive client data, a significant security "
        "breach could result in financial losses, regulatory penalties, and reputational damage. "
        "We maintain comprehensive insurance coverage and invest approximately $45M annually "
        "in cybersecurity infrastructure.",
    ])

    add_text_page(doc, 25, "Independent Auditor's Report", [
        "To the Board of Directors and Shareholders of Meridian Global Partners, Inc.:",
        "We have audited the accompanying consolidated financial statements of Meridian Global "
        "Partners, Inc. and subsidiaries, which comprise the consolidated balance sheet as of "
        "December 31, 2025 and 2024, and the related consolidated statements of income, "
        "comprehensive income, stockholders' equity, and cash flows for the years then ended.",
        "In our opinion, the consolidated financial statements present fairly, in all material "
        "respects, the financial position of Meridian Global Partners, Inc. as of December 31, 2025, "
        "and the results of its operations and its cash flows for the year then ended in conformity "
        "with accounting principles generally accepted in the United States of America.",
        "Deloitte & Thornton LLP, Certified Public Accountants. Chicago, Illinois. February 28, 2026.",
    ])

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Page count: 25')

    # GUI-ready startup: open the PDF in Evince
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with DISPLAY=:0')


create_initial()
