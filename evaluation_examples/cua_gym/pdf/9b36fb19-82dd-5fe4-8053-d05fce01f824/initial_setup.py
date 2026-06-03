"""
Initial Setup: Create letterhead template and financial memo draft.
Task ID: pdf_fin_056
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf


WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_056'
FINANCE_DIR = f'{WORKDIR}/finance'
TEMPLATES_DIR = f'{FINANCE_DIR}/templates'
LETTERHEAD_PATH = f'{TEMPLATES_DIR}/letterhead.pdf'
MEMO_DRAFT_PATH = f'{FINANCE_DIR}/memo_draft.pdf'

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


def create_letterhead():
    """Create a single-page letterhead PDF with company logo area and border."""
    doc = pymupdf.open()
    page = doc.new_page(width=W, height=H)
    shape = page.new_shape()

    # Outer border (double-line effect)
    outer = pymupdf.Rect(24, 24, W - 24, H - 24)
    shape.draw_rect(outer)
    shape.finish(color=(0.0, 0.22, 0.48), width=2.5)  # dark navy border

    inner = pymupdf.Rect(30, 30, W - 30, H - 30)
    shape.draw_rect(inner)
    shape.finish(color=(0.0, 0.22, 0.48), width=0.5)

    # Top decorative band
    band = pymupdf.Rect(30, 30, W - 30, 90)
    shape.draw_rect(band)
    shape.finish(color=(0.0, 0.22, 0.48), fill=(0.0, 0.22, 0.48), width=0)

    # Bottom decorative line
    shape.draw_line(pymupdf.Point(30, H - 60), pymupdf.Point(W - 30, H - 60))
    shape.finish(color=(0.0, 0.22, 0.48), width=1.5)

    shape.commit()

    # Company name in the top band (white text on dark background)
    page.insert_text(
        pymupdf.Point(50, 70),
        "MERIDIAN CAPITAL PARTNERS",
        fontsize=18,
        fontname="hebo",
        color=(1, 1, 1),
    )

    # Tagline below company name
    page.insert_text(
        pymupdf.Point(50, 105),
        "Investment Advisory & Wealth Management",
        fontsize=9,
        fontname="heit",
        color=(0.3, 0.3, 0.3),
    )

    # Contact info in footer
    page.insert_text(
        pymupdf.Point(50, H - 45),
        "1200 Financial Plaza, Suite 800  |  New York, NY 10005  |  (212) 555-0147  |  info@meridiancap.com",
        fontsize=7,
        fontname="helv",
        color=(0.4, 0.4, 0.4),
    )

    doc.save(LETTERHEAD_PATH)
    doc.close()
    print(f'Letterhead created: {LETTERHEAD_PATH}')


def create_memo_draft():
    """Create a 4-page financial memo PDF."""
    doc = pymupdf.open()

    # --- Page 1: Memo Header & Executive Summary ---
    page = doc.new_page(width=W, height=H)
    y = 130  # Start below where letterhead header would be

    page.insert_text(pymupdf.Point(72, y), "CONFIDENTIAL FINANCIAL MEMO", fontsize=16, fontname="hebo", color=(0, 0, 0))
    y += 30
    page.insert_text(pymupdf.Point(72, y), "Date: March 28, 2025", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    y += 16
    page.insert_text(pymupdf.Point(72, y), "To: Board of Directors, Meridian Capital Partners", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    y += 16
    page.insert_text(pymupdf.Point(72, y), "From: Victoria Chang, Chief Financial Officer", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    y += 16
    page.insert_text(pymupdf.Point(72, y), "Re: Q1 2025 Financial Performance & Capital Allocation Review", fontsize=10, fontname="hebo", color=(0.2, 0.2, 0.2))

    y += 35
    # Horizontal rule
    shape = page.new_shape()
    shape.draw_line(pymupdf.Point(72, y), pymupdf.Point(W - 72, y))
    shape.finish(color=(0, 0, 0), width=0.8)
    shape.commit()

    y += 25
    page.insert_text(pymupdf.Point(72, y), "EXECUTIVE SUMMARY", fontsize=13, fontname="hebo", color=(0.0, 0.22, 0.48))

    y += 22
    exec_summary = (
        "The first quarter of 2025 has demonstrated strong momentum across our core business lines. "
        "Total assets under management (AUM) grew to $4.87 billion, representing a 6.3% increase "
        "from Q4 2024. Net revenue reached $38.2 million, driven primarily by robust performance in "
        "our equity strategies and expanding institutional mandates. Operating margin improved to "
        "34.1%, up from 31.8% in the prior quarter, reflecting ongoing cost optimization initiatives "
        "and favorable market conditions."
    )
    page.insert_textbox(
        pymupdf.Rect(72, y, W - 72, y + 120),
        exec_summary,
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    y += 135
    key_highlights = (
        "Key performance highlights include: (1) the Global Equity Fund returned 8.7% net of fees, "
        "outperforming its benchmark by 215 basis points; (2) client retention rate remained above "
        "97.2%; (3) three new institutional mandates totaling $340 million were secured; and "
        "(4) technology infrastructure modernization reduced trade settlement errors by 42%."
    )
    page.insert_textbox(
        pymupdf.Rect(72, y, W - 72, y + 100),
        key_highlights,
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    y += 120
    page.insert_text(pymupdf.Point(72, y), "REVENUE BREAKDOWN", fontsize=13, fontname="hebo", color=(0.0, 0.22, 0.48))
    y += 22
    revenue_text = (
        "Management fees accounted for $28.4 million (74.3% of total revenue), while performance-based "
        "fees contributed $6.1 million (16.0%). Advisory and consulting revenues totaled $3.7 million "
        "(9.7%), reflecting continued demand for our strategic advisory services. Compared to Q1 2024, "
        "total revenue increased by 11.8%, with the most significant growth occurring in performance fees "
        "which rose 28.3% year-over-year."
    )
    page.insert_textbox(
        pymupdf.Rect(72, y, W - 72, y + 110),
        revenue_text,
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 2: Detailed Financial Data ---
    page2 = doc.new_page(width=W, height=H)
    y = 130

    page2.insert_text(pymupdf.Point(72, y), "PORTFOLIO PERFORMANCE SUMMARY", fontsize=13, fontname="hebo", color=(0.0, 0.22, 0.48))
    y += 25

    # Table header
    headers = ["Fund Name", "AUM ($M)", "Q1 Return", "Benchmark", "Alpha"]
    col_x = [72, 210, 320, 410, 500]
    for i, h in enumerate(headers):
        page2.insert_text(pymupdf.Point(col_x[i], y), h, fontsize=9, fontname="hebo", color=(0, 0, 0))
    y += 4
    shape2 = page2.new_shape()
    shape2.draw_line(pymupdf.Point(72, y), pymupdf.Point(W - 72, y))
    shape2.finish(color=(0, 0, 0), width=0.5)

    fund_data = [
        ["Global Equity Fund", "$1,420", "+8.7%", "+6.5%", "+2.2%"],
        ["Fixed Income Plus", "$980", "+2.1%", "+1.8%", "+0.3%"],
        ["Emerging Markets", "$645", "+11.3%", "+9.1%", "+2.2%"],
        ["Real Assets Fund", "$510", "+4.5%", "+3.9%", "+0.6%"],
        ["Multi-Strategy", "$780", "+6.8%", "+5.4%", "+1.4%"],
        ["Private Credit", "$340", "+3.2%", "+2.6%", "+0.6%"],
        ["Tech Growth Fund", "$195", "+14.2%", "+12.8%", "+1.4%"],
    ]
    for row in fund_data:
        y += 18
        for i, val in enumerate(row):
            page2.insert_text(pymupdf.Point(col_x[i], y), val, fontsize=9, fontname="helv", color=(0, 0, 0))

    y += 8
    shape2.draw_line(pymupdf.Point(72, y), pymupdf.Point(W - 72, y))
    shape2.finish(color=(0, 0, 0), width=0.5)
    shape2.commit()

    y += 18
    page2.insert_text(pymupdf.Point(72, y), "Total AUM: $4,870M", fontsize=10, fontname="hebo", color=(0, 0, 0))
    y += 16
    page2.insert_text(pymupdf.Point(72, y), "Weighted Average Return: +6.9%", fontsize=10, fontname="helv", color=(0, 0, 0))

    y += 40
    page2.insert_text(pymupdf.Point(72, y), "EXPENSE ANALYSIS", fontsize=13, fontname="hebo", color=(0.0, 0.22, 0.48))
    y += 22
    expense_text = (
        "Total operating expenses for Q1 2025 were $25.2 million, an increase of 4.7% from the prior "
        "quarter. Compensation and benefits, our largest expense category at $16.8 million, reflected "
        "annual merit adjustments effective January 2025. Technology and infrastructure costs of $3.9 "
        "million included scheduled investments in our proprietary risk analytics platform. Professional "
        "services fees of $2.1 million and occupancy costs of $1.6 million remained stable. "
        "Marketing and client acquisition expenses decreased to $0.8 million from $1.1 million in Q4 "
        "2024, as several major campaigns concluded."
    )
    page2.insert_textbox(
        pymupdf.Rect(72, y, W - 72, y + 140),
        expense_text,
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    y += 155
    page2.insert_text(pymupdf.Point(72, y), "CAPITAL ALLOCATION RECOMMENDATIONS", fontsize=13, fontname="hebo", color=(0.0, 0.22, 0.48))
    y += 22
    capital_text = (
        "Based on current market conditions and our forward-looking analysis, we recommend the "
        "following capital allocation adjustments for Q2 2025: (1) Increase allocation to the "
        "Emerging Markets fund by $75 million, leveraging favorable valuation spreads; (2) Reduce "
        "Fixed Income Plus exposure by $50 million given the inverted yield curve outlook; "
        "(3) Allocate $120 million to the new infrastructure debt opportunity identified by the "
        "Private Credit team; (4) Maintain current allocation levels for remaining strategies."
    )
    page2.insert_textbox(
        pymupdf.Rect(72, y, W - 72, y + 130),
        capital_text,
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 3: Risk Analysis ---
    page3 = doc.new_page(width=W, height=H)
    y = 130

    page3.insert_text(pymupdf.Point(72, y), "RISK MANAGEMENT UPDATE", fontsize=13, fontname="hebo", color=(0.0, 0.22, 0.48))
    y += 25
    risk_text = (
        "Our firm-wide Value at Risk (VaR) at the 99% confidence level stood at $47.3 million "
        "as of March 31, 2025, compared to $44.1 million at the end of Q4 2024. The increase is "
        "attributable to higher equity allocations and elevated implied volatility in international "
        "markets. Stress testing under our standard adverse scenarios indicates maximum portfolio "
        "drawdown of 12.4%, well within our 15% risk tolerance threshold."
    )
    page3.insert_textbox(
        pymupdf.Rect(72, y, W - 72, y + 110),
        risk_text,
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    y += 125
    page3.insert_text(pymupdf.Point(72, y), "Key Risk Metrics:", fontsize=11, fontname="hebo", color=(0, 0, 0))
    y += 20
    metrics = [
        "Portfolio Beta (vs. MSCI World): 0.94",
        "Sharpe Ratio (annualized): 1.82",
        "Maximum Drawdown (trailing 12 months): -4.7%",
        "Tracking Error (vs. composite benchmark): 2.31%",
        "Concentration Risk (top 10 holdings): 18.6% of total AUM",
        "Liquidity Coverage Ratio: 142% (minimum required: 100%)",
        "Counterparty Exposure (largest single): 3.8% of NAV",
    ]
    for m in metrics:
        page3.insert_text(pymupdf.Point(90, y), f"- {m}", fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 16

    y += 20
    page3.insert_text(pymupdf.Point(72, y), "REGULATORY & COMPLIANCE", fontsize=13, fontname="hebo", color=(0.0, 0.22, 0.48))
    y += 22
    reg_text = (
        "All regulatory filings for Q1 2025 have been submitted on schedule. The SEC examination "
        "initiated in February 2025 has progressed without material findings. Our compliance team "
        "has completed the annual review of personal trading policies and updated the firm's code "
        "of ethics in accordance with the revised Investment Advisers Act requirements effective "
        "January 1, 2025. Anti-money laundering (AML) monitoring systems flagged 14 transactions "
        "for review during the quarter; all were cleared after investigation with no Suspicious "
        "Activity Reports (SARs) filed."
    )
    page3.insert_textbox(
        pymupdf.Rect(72, y, W - 72, y + 130),
        reg_text,
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    y += 145
    page3.insert_text(pymupdf.Point(72, y), "CLIENT RELATIONSHIP MANAGEMENT", fontsize=13, fontname="hebo", color=(0.0, 0.22, 0.48))
    y += 22
    client_text = (
        "Total client count increased to 847 from 831 at the end of Q4 2024. Net new asset flows "
        "reached $412 million, primarily driven by institutional mandates from two sovereign wealth "
        "funds and a major university endowment. Client satisfaction surveys conducted in March "
        "indicated an NPS score of 72, representing a 4-point improvement from the prior survey. "
        "The client services team has implemented a new digital reporting portal, reducing quarterly "
        "report delivery time by 60%."
    )
    page3.insert_textbox(
        pymupdf.Rect(72, y, W - 72, y + 120),
        client_text,
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    # --- Page 4: Outlook & Action Items ---
    page4 = doc.new_page(width=W, height=H)
    y = 130

    page4.insert_text(pymupdf.Point(72, y), "Q2 2025 OUTLOOK & STRATEGIC PRIORITIES", fontsize=13, fontname="hebo", color=(0.0, 0.22, 0.48))
    y += 25
    outlook_text = (
        "Looking ahead to Q2 2025, we anticipate continued but moderating growth in global equity "
        "markets, with potential headwinds from tightening monetary policy in Europe and geopolitical "
        "uncertainties in the Asia-Pacific region. Our base case scenario projects AUM growth of "
        "3-5% for the quarter, supported by strong pipeline activity and existing client commitments. "
        "We expect operating margins to remain in the 33-35% range as seasonal compensation "
        "adjustments normalize."
    )
    page4.insert_textbox(
        pymupdf.Rect(72, y, W - 72, y + 110),
        outlook_text,
        fontsize=10,
        fontname="helv",
        color=(0, 0, 0),
        align=pymupdf.TEXT_ALIGN_JUSTIFY,
    )

    y += 125
    page4.insert_text(pymupdf.Point(72, y), "ACTION ITEMS FOR BOARD APPROVAL:", fontsize=11, fontname="hebo", color=(0, 0, 0))
    y += 22
    actions = [
        "1.  Approve the capital reallocation of $245 million as outlined in the Capital Allocation section.",
        "2.  Authorize the expansion of the Private Credit team with 3 senior hires (est. annual cost: $2.4M).",
        "3.  Ratify the technology infrastructure investment of $5.8 million for the risk analytics upgrade.",
        "4.  Approve the proposed fee restructuring for the Global Equity Fund (reduce mgmt fee from",
        "     1.25% to 1.15% for accounts > $50M to improve competitiveness).",
        "5.  Review and approve the updated Business Continuity Plan incorporating lessons from the",
        "     February 2025 data center incident.",
        "6.  Authorize preliminary due diligence for a potential strategic acquisition of Pinnacle",
        "     Analytics Group (est. valuation: $45-55 million).",
    ]
    for action in actions:
        page4.insert_text(pymupdf.Point(90, y), action, fontsize=10, fontname="helv", color=(0, 0, 0))
        y += 16

    y += 25
    page4.insert_text(pymupdf.Point(72, y), "NEXT MEETING", fontsize=11, fontname="hebo", color=(0.0, 0.22, 0.48))
    y += 20
    page4.insert_text(pymupdf.Point(72, y), "The next Board meeting is scheduled for June 24, 2025, at 9:00 AM EST.", fontsize=10, fontname="helv", color=(0, 0, 0))
    y += 16
    page4.insert_text(pymupdf.Point(72, y), "Agenda materials will be distributed no later than June 17, 2025.", fontsize=10, fontname="helv", color=(0, 0, 0))

    y += 40
    page4.insert_text(pymupdf.Point(72, y), "Respectfully submitted,", fontsize=10, fontname="heit", color=(0, 0, 0))
    y += 25
    page4.insert_text(pymupdf.Point(72, y), "Victoria Chang", fontsize=11, fontname="hebo", color=(0, 0, 0))
    y += 16
    page4.insert_text(pymupdf.Point(72, y), "Chief Financial Officer", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
    y += 14
    page4.insert_text(pymupdf.Point(72, y), "Meridian Capital Partners", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

    doc.save(MEMO_DRAFT_PATH)
    doc.close()
    print(f'Memo draft created: {MEMO_DRAFT_PATH}')


def main():
    # Create directories
    os.makedirs(TEMPLATES_DIR, exist_ok=True)

    # Create the letterhead template
    create_letterhead()

    # Create the 4-page memo draft
    create_memo_draft()

    # Open memo_draft.pdf in Evince for the agent
    launch_gui(f'evince "{MEMO_DRAFT_PATH}"', delay_sec=2.0)
    print('GUI_READY: launched Evince with memo_draft.pdf on DISPLAY=:0')


main()
