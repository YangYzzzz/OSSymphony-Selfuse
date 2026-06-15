"""
Initial Setup: Create a quarterly report PDF with non-embedded fonts, JavaScript actions, and form fields.
Task ID: pdf_aw_038
Domain: pdf
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'pdf_aw_038'
ARCHIVE_DIR = f'{WORKDIR}/archive'
OUTPUT = f'{ARCHIVE_DIR}/quarterly_report.pdf'


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
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    import pymupdf

    doc = pymupdf.open()

    # ---- Page content generation helpers ----
    def add_header_footer(page, page_num, total_pages):
        """Add consistent header and footer to each page."""
        w = page.rect.width
        h = page.rect.height
        # Header line
        shape = page.new_shape()
        shape.draw_line(pymupdf.Point(50, 55), pymupdf.Point(w - 50, 55))
        shape.finish(color=(0.2, 0.3, 0.5), width=1.5)
        shape.commit()
        # Header text
        page.insert_text(pymupdf.Point(50, 48), "Meridian Technologies Inc.",
                         fontsize=9, fontname="helv", color=(0.2, 0.3, 0.5))
        page.insert_text(pymupdf.Point(w - 200, 48), "Q3 2025 Quarterly Report",
                         fontsize=9, fontname="heit", color=(0.4, 0.4, 0.4))
        # Footer
        page.insert_text(pymupdf.Point(50, h - 30),
                         "Confidential - For Internal Distribution Only",
                         fontsize=7, fontname="cour", color=(0.5, 0.5, 0.5))
        page.insert_text(pymupdf.Point(w - 100, h - 30),
                         f"Page {page_num} of {total_pages}",
                         fontsize=8, fontname="helv", color=(0.3, 0.3, 0.3))

    total_pages = 20

    # ========== PAGE 1: Title Page ==========
    p = doc.new_page(width=612, height=792)
    # Title block
    shape = p.new_shape()
    shape.draw_rect(pymupdf.Rect(0, 200, 612, 420))
    shape.finish(fill=(0.15, 0.25, 0.45), color=(0.15, 0.25, 0.45))
    shape.commit()
    p.insert_text(pymupdf.Point(80, 290), "QUARTERLY REPORT",
                  fontsize=36, fontname="hebo", color=(1, 1, 1))
    p.insert_text(pymupdf.Point(80, 330), "Third Quarter  |  Fiscal Year 2025",
                  fontsize=18, fontname="helv", color=(0.8, 0.85, 0.95))
    p.insert_text(pymupdf.Point(80, 370), "Meridian Technologies Inc.",
                  fontsize=14, fontname="heit", color=(0.7, 0.78, 0.9))
    p.insert_text(pymupdf.Point(80, 480), "Prepared by: Office of the CFO",
                  fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))
    p.insert_text(pymupdf.Point(80, 500), "Date: October 15, 2025",
                  fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))
    p.insert_text(pymupdf.Point(80, 520), "Distribution: Board of Directors, Senior Leadership",
                  fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))

    # ========== PAGE 2: Table of Contents ==========
    p = doc.new_page(width=612, height=792)
    add_header_footer(p, 2, total_pages)
    p.insert_text(pymupdf.Point(50, 100), "Table of Contents",
                  fontsize=22, fontname="hebo", color=(0.15, 0.25, 0.45))
    toc_items = [
        ("1. Executive Summary", "3"),
        ("2. Financial Highlights", "4"),
        ("3. Revenue Analysis by Segment", "6"),
        ("4. Operating Expenses Breakdown", "8"),
        ("5. Balance Sheet Overview", "9"),
        ("6. Cash Flow Statement", "10"),
        ("7. Product Development Update", "11"),
        ("8. Market Analysis & Competitive Landscape", "13"),
        ("9. Human Resources & Talent Metrics", "15"),
        ("10. Risk Assessment & Mitigation", "16"),
        ("11. Strategic Initiatives Progress", "17"),
        ("12. Outlook & Guidance for Q4 2025", "18"),
        ("13. Appendix: Detailed Financial Tables", "19"),
        ("14. Approval & Sign-off", "20"),
    ]
    y = 140
    for title, pg in toc_items:
        p.insert_text(pymupdf.Point(70, y), title,
                      fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))
        p.insert_text(pymupdf.Point(500, y), pg,
                      fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))
        y += 22

    # ========== PAGE 3: Executive Summary ==========
    p = doc.new_page(width=612, height=792)
    add_header_footer(p, 3, total_pages)
    p.insert_text(pymupdf.Point(50, 100), "1. Executive Summary",
                  fontsize=20, fontname="hebo", color=(0.15, 0.25, 0.45))
    exec_summary = (
        "Meridian Technologies delivered strong performance in Q3 2025, achieving total revenue of "
        "$487.3 million, representing a 14.2% year-over-year increase. This growth was driven primarily "
        "by our Cloud Services division, which saw a 28.6% surge in subscription revenue. Operating "
        "income reached $73.1 million with an operating margin of 15.0%, up from 13.2% in Q3 2024. "
        "Net income attributable to shareholders was $58.4 million, or $2.17 per diluted share, compared "
        "to $47.9 million ($1.78 per diluted share) in the prior-year period.\n\n"
        "Key achievements during the quarter include the successful launch of our Meridian Cloud Platform "
        "v4.0, which has already attracted 340 enterprise customers. Our strategic acquisition of DataVault "
        "Solutions was completed on August 12, adding $18.2 million in recurring revenue to our portfolio. "
        "Additionally, we expanded our Asia-Pacific operations with new offices in Singapore and Seoul, "
        "positioning the company for continued international growth.\n\n"
        "Looking ahead, management reaffirms full-year revenue guidance of $1.90 to $1.95 billion and "
        "raises the adjusted EBITDA margin target from 22.0% to 23.5%, reflecting operational efficiencies "
        "and the positive contribution of recently integrated acquisitions."
    )
    p.insert_textbox(pymupdf.Rect(50, 125, 562, 550), exec_summary,
                     fontsize=10.5, fontname="tiro", color=(0.1, 0.1, 0.1),
                     align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGE 4-5: Financial Highlights ==========
    for sub_page in range(2):
        p = doc.new_page(width=612, height=792)
        add_header_footer(p, 4 + sub_page, total_pages)
        if sub_page == 0:
            p.insert_text(pymupdf.Point(50, 100), "2. Financial Highlights",
                          fontsize=20, fontname="hebo", color=(0.15, 0.25, 0.45))
            fin_text = (
                "The following table summarizes key financial metrics for Q3 2025 compared to prior periods:"
            )
            p.insert_textbox(pymupdf.Rect(50, 130, 562, 170), fin_text,
                             fontsize=10.5, fontname="tiro", color=(0.1, 0.1, 0.1))

            # Draw a financial summary table
            headers = ["Metric", "Q3 2025", "Q2 2025", "Q3 2024", "YoY Change"]
            data_rows = [
                ["Total Revenue", "$487.3M", "$462.1M", "$426.8M", "+14.2%"],
                ["Gross Profit", "$312.7M", "$294.5M", "$268.3M", "+16.6%"],
                ["Operating Income", "$73.1M", "$67.8M", "$56.3M", "+29.8%"],
                ["Net Income", "$58.4M", "$54.1M", "$47.9M", "+21.9%"],
                ["EPS (Diluted)", "$2.17", "$2.01", "$1.78", "+21.9%"],
                ["Free Cash Flow", "$89.6M", "$82.3M", "$71.4M", "+25.5%"],
                ["Gross Margin", "64.2%", "63.7%", "62.9%", "+1.3pp"],
                ["Operating Margin", "15.0%", "14.7%", "13.2%", "+1.8pp"],
                ["R&D Spend", "$68.4M", "$65.2M", "$58.9M", "+16.1%"],
                ["Headcount", "4,872", "4,651", "4,218", "+15.5%"],
            ]
            y_start = 190
            col_widths = [150, 85, 85, 85, 85]
            col_x = [55]
            for w in col_widths[:-1]:
                col_x.append(col_x[-1] + w)

            shape = p.new_shape()
            # Header row background
            shape.draw_rect(pymupdf.Rect(50, y_start - 15, 555, y_start + 5))
            shape.finish(fill=(0.15, 0.25, 0.45))
            shape.commit()
            for i, h in enumerate(headers):
                p.insert_text(pymupdf.Point(col_x[i], y_start),
                              h, fontsize=9, fontname="hebo", color=(1, 1, 1))
            y = y_start + 25
            for row_idx, row in enumerate(data_rows):
                if row_idx % 2 == 0:
                    shape2 = p.new_shape()
                    shape2.draw_rect(pymupdf.Rect(50, y - 13, 555, y + 7))
                    shape2.finish(fill=(0.93, 0.95, 0.98))
                    shape2.commit()
                for i, val in enumerate(row):
                    fn = "hebo" if i == 0 else "helv"
                    p.insert_text(pymupdf.Point(col_x[i], y), val,
                                  fontsize=9, fontname=fn, color=(0.1, 0.1, 0.1))
                y += 20

        else:
            p.insert_text(pymupdf.Point(50, 100), "2. Financial Highlights (continued)",
                          fontsize=16, fontname="hebo", color=(0.15, 0.25, 0.45))
            cont_text = (
                "Revenue growth was balanced across geographies. North America contributed $298.4 million "
                "(61.2% of total), up 12.1% year-over-year. Europe, Middle East and Africa (EMEA) delivered "
                "$112.3 million (23.0%), growing 15.8%. Asia-Pacific revenue reached $76.6 million (15.7%), "
                "a remarkable 22.4% increase driven by expansion in Japan, South Korea, and Southeast Asia.\n\n"
                "The company repurchased 1.2 million shares during Q3 at an average price of $142.50 per share, "
                "totaling $171.0 million. The remaining buyback authorization stands at $428.0 million. "
                "A quarterly dividend of $0.35 per share was declared on September 15, payable October 31."
            )
            p.insert_textbox(pymupdf.Rect(50, 130, 562, 400), cont_text,
                             fontsize=10.5, fontname="tiro", color=(0.1, 0.1, 0.1),
                             align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGES 6-7: Revenue Analysis ==========
    for sub_page in range(2):
        p = doc.new_page(width=612, height=792)
        add_header_footer(p, 6 + sub_page, total_pages)
        if sub_page == 0:
            p.insert_text(pymupdf.Point(50, 100), "3. Revenue Analysis by Segment",
                          fontsize=20, fontname="hebo", color=(0.15, 0.25, 0.45))
            segments = [
                ("Cloud Services", "$198.7M", "40.8%", "+28.6%"),
                ("Enterprise Software", "$142.1M", "29.2%", "+8.3%"),
                ("Professional Services", "$87.4M", "17.9%", "+5.1%"),
                ("Hardware & Infrastructure", "$59.1M", "12.1%", "-2.4%"),
            ]
            y = 150
            for name, rev, pct, growth in segments:
                p.insert_text(pymupdf.Point(60, y), name,
                              fontsize=12, fontname="hebo", color=(0.15, 0.25, 0.45))
                p.insert_text(pymupdf.Point(250, y), f"Revenue: {rev}",
                              fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
                p.insert_text(pymupdf.Point(400, y), f"Share: {pct}",
                              fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
                growth_color = (0, 0.5, 0) if growth.startswith("+") else (0.7, 0, 0)
                p.insert_text(pymupdf.Point(490, y), growth,
                              fontsize=10, fontname="hebo", color=growth_color)
                y += 35
                desc_map = {
                    "Cloud Services": "Cloud Services remains our fastest-growing segment, driven by enterprise adoption of Meridian Cloud Platform v4.0. Annual recurring revenue (ARR) reached $780M, with net revenue retention at 118%. The segment added 340 new enterprise logos and expanded usage among existing customers.",
                    "Enterprise Software": "Enterprise Software grew steadily with the release of Meridian Suite 12.0. Perpetual license revenue declined 15% as customers migrate to subscription models, but total segment revenue increased 8.3% on the strength of term license and maintenance revenue.",
                    "Professional Services": "Professional Services benefited from implementation projects related to new enterprise wins and the DataVault integration initiative. Utilization rates improved to 78% from 74% in the prior quarter. Average billing rates increased 4.2%.",
                    "Hardware & Infrastructure": "Hardware & Infrastructure experienced a modest decline due to customer transitions to cloud-hosted deployments. Management is evaluating strategic alternatives for this segment, including a potential partnership or joint venture."
                }
                p.insert_textbox(pymupdf.Rect(60, y, 555, y + 70), desc_map[name],
                                 fontsize=9.5, fontname="tiro", color=(0.2, 0.2, 0.2),
                                 align=pymupdf.TEXT_ALIGN_JUSTIFY)
                y += 80
        else:
            p.insert_text(pymupdf.Point(50, 100), "3. Revenue Analysis (continued)",
                          fontsize=16, fontname="hebo", color=(0.15, 0.25, 0.45))
            rev_detail = (
                "Subscription revenue as a percentage of total revenue reached 52.3% in Q3 2025, up from "
                "45.8% in Q3 2024, reflecting the company's successful transition to a recurring revenue model. "
                "The blended customer acquisition cost (CAC) payback period improved to 14.2 months from 16.8 months, "
                "indicating more efficient go-to-market execution.\n\n"
                "Customer concentration risk remains low: no single customer accounts for more than 3.1% of revenue. "
                "The top 20 customers collectively represent 18.4% of total revenue. Dollar-based net retention for "
                "enterprise accounts (>$100K ARR) stands at 124%, while mid-market accounts show 108% retention.\n\n"
                "Bookings for the quarter totaled $523.8 million, yielding a book-to-bill ratio of 1.07x. "
                "Remaining performance obligations (RPO) grew to $1.84 billion, representing approximately "
                "3.8 quarters of forward revenue visibility at current run rates."
            )
            p.insert_textbox(pymupdf.Rect(50, 130, 562, 500), rev_detail,
                             fontsize=10.5, fontname="tiro", color=(0.1, 0.1, 0.1),
                             align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGE 8: Operating Expenses ==========
    p = doc.new_page(width=612, height=792)
    add_header_footer(p, 8, total_pages)
    p.insert_text(pymupdf.Point(50, 100), "4. Operating Expenses Breakdown",
                  fontsize=20, fontname="hebo", color=(0.15, 0.25, 0.45))
    opex_text = (
        "Total operating expenses for Q3 2025 were $414.2 million, representing 85.0% of revenue, "
        "compared to $370.5 million (86.8% of revenue) in Q3 2024. The improvement in operating leverage "
        "reflects the scalability of our platform-based business model.\n\n"
        "Cost of Revenue: $174.6 million (35.8% of revenue) vs. $158.5 million (37.1%) in Q3 2024. "
        "The improvement reflects migration of hosting infrastructure to more cost-effective providers "
        "and automation of support workflows.\n\n"
        "Research & Development: $68.4 million (14.0% of revenue) vs. $58.9 million (13.8%). "
        "Increased investment reflects hiring of 124 engineers and data scientists, and accelerated "
        "development of AI-powered analytics features.\n\n"
        "Sales & Marketing: $121.3 million (24.9% of revenue) vs. $108.7 million (25.5%). "
        "Efficiency gains from digital marketing channels partially offset increased headcount.\n\n"
        "General & Administrative: $49.9 million (10.2% of revenue) vs. $44.4 million (10.4%). "
        "Includes $4.2 million in acquisition-related costs for the DataVault transaction."
    )
    p.insert_textbox(pymupdf.Rect(50, 130, 562, 650), opex_text,
                     fontsize=10.5, fontname="tiro", color=(0.1, 0.1, 0.1),
                     align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGE 9: Balance Sheet ==========
    p = doc.new_page(width=612, height=792)
    add_header_footer(p, 9, total_pages)
    p.insert_text(pymupdf.Point(50, 100), "5. Balance Sheet Overview",
                  fontsize=20, fontname="hebo", color=(0.15, 0.25, 0.45))
    bs_text = (
        "Total assets as of September 30, 2025 were $3.42 billion, up from $2.98 billion at year-end 2024. "
        "Cash and short-term investments totaled $612.4 million. Total debt stands at $485.0 million, "
        "with a net debt-to-EBITDA ratio of 0.8x.\n\n"
        "Current assets: $1.14 billion (Cash: $612.4M, Receivables: $342.1M, Prepaid: $48.7M, Other: $138.2M)\n"
        "Non-current assets: $2.28 billion (Goodwill: $891.2M, Intangibles: $412.3M, PP&E: $298.4M, "
        "Operating lease ROU: $342.8M, Deferred tax: $89.1M, Other: $246.2M)\n\n"
        "Current liabilities: $687.3 million (Payables: $142.8M, Accrued: $198.4M, Deferred revenue: $246.1M, "
        "Current debt: $45.0M, Lease obligations: $55.0M)\n"
        "Non-current liabilities: $892.4 million (Long-term debt: $440.0M, Deferred revenue: $124.3M, "
        "Lease obligations: $287.6M, Other: $40.5M)\n\n"
        "Total stockholders' equity: $1.84 billion, including retained earnings of $1.12 billion."
    )
    p.insert_textbox(pymupdf.Rect(50, 130, 562, 600), bs_text,
                     fontsize=10.5, fontname="tiro", color=(0.1, 0.1, 0.1),
                     align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGE 10: Cash Flow ==========
    p = doc.new_page(width=612, height=792)
    add_header_footer(p, 10, total_pages)
    p.insert_text(pymupdf.Point(50, 100), "6. Cash Flow Statement",
                  fontsize=20, fontname="hebo", color=(0.15, 0.25, 0.45))
    cf_text = (
        "Operating cash flow for Q3 2025 was $112.8 million, up 19.3% from $94.5 million in Q3 2024. "
        "The increase was driven by higher net income and improved working capital management, partially "
        "offset by increased tax payments.\n\n"
        "Capital expenditures totaled $23.2 million, consisting of $14.8 million in data center "
        "infrastructure and $8.4 million in office expansion and equipment. Free cash flow was $89.6 million, "
        "representing an 18.4% FCF margin.\n\n"
        "Investing activities consumed $198.4 million, including $172.0 million for the DataVault acquisition "
        "(net of cash acquired) and $26.4 million in capital expenditures and other investments.\n\n"
        "Financing activities used $195.2 million, primarily consisting of $171.0 million in share repurchases "
        "and $24.2 million in dividend payments, partially offset by $12.0 million in proceeds from employee "
        "stock option exercises."
    )
    p.insert_textbox(pymupdf.Rect(50, 130, 562, 550), cf_text,
                     fontsize=10.5, fontname="tiro", color=(0.1, 0.1, 0.1),
                     align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGES 11-12: Product Development ==========
    for sub_page in range(2):
        p = doc.new_page(width=612, height=792)
        add_header_footer(p, 11 + sub_page, total_pages)
        if sub_page == 0:
            p.insert_text(pymupdf.Point(50, 100), "7. Product Development Update",
                          fontsize=20, fontname="hebo", color=(0.15, 0.25, 0.45))
            prod_text = (
                "Meridian Cloud Platform v4.0\n"
                "Released August 1, 2025. Key features include AI-powered predictive analytics, "
                "real-time collaboration workspace, and enhanced security with zero-trust architecture. "
                "Adoption exceeded expectations with 340 enterprise logos onboarded within 60 days. "
                "Customer NPS for v4.0 stands at 72, compared to 65 for v3.x.\n\n"
                "Meridian Suite 12.0\n"
                "The latest on-premise offering shipped September 15, 2025. Major enhancements include "
                "a modernized UI built on React, native integration with Meridian Cloud for hybrid deployments, "
                "and automated compliance reporting for SOX and GDPR requirements. Early adopter feedback "
                "indicates a 30% reduction in report generation time.\n\n"
                "DataVault Integration\n"
                "Post-acquisition integration is proceeding ahead of schedule. The DataVault data governance "
                "capabilities have been integrated into the Meridian Cloud Platform as the Data Trust Module. "
                "Cross-sell opportunities have been identified for 180+ existing Meridian enterprise accounts.\n\n"
                "AI & Machine Learning Initiatives\n"
                "The newly established Meridian AI Lab has 42 researchers and engineers. Key projects include "
                "natural language query generation for analytics, automated anomaly detection for IT operations, "
                "and intelligent document processing for accounts payable workflows."
            )
            p.insert_textbox(pymupdf.Rect(50, 130, 562, 680), prod_text,
                             fontsize=10.5, fontname="tiro", color=(0.1, 0.1, 0.1),
                             align=pymupdf.TEXT_ALIGN_JUSTIFY)
        else:
            p.insert_text(pymupdf.Point(50, 100), "7. Product Development (continued)",
                          fontsize=16, fontname="hebo", color=(0.15, 0.25, 0.45))
            prod2 = (
                "Product Roadmap Highlights (Q4 2025 - Q2 2026)\n\n"
                "- Meridian Cloud Platform v4.1 (December 2025): Enhanced data visualization library, "
                "support for Apache Iceberg data lakehouse format, and SOC 2 Type II certification.\n\n"
                "- Meridian Mobile App v3.0 (January 2026): Complete redesign for iOS and Android, "
                "offline mode support, and biometric authentication.\n\n"
                "- Meridian AI Copilot (March 2026): Natural language interface for all platform functions, "
                "powered by fine-tuned large language models.\n\n"
                "- Meridian Edge Computing Module (Q2 2026): Extends cloud capabilities to edge devices "
                "for manufacturing, retail, and healthcare verticals.\n\n"
                "Patent portfolio expanded by 12 filings in Q3, bringing the total to 287 active patents "
                "and pending applications. R&D headcount grew 18% year-over-year to 1,284 employees, "
                "representing 26.4% of total workforce."
            )
            p.insert_textbox(pymupdf.Rect(50, 130, 562, 580), prod2,
                             fontsize=10.5, fontname="tiro", color=(0.1, 0.1, 0.1),
                             align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGES 13-14: Market Analysis ==========
    for sub_page in range(2):
        p = doc.new_page(width=612, height=792)
        add_header_footer(p, 13 + sub_page, total_pages)
        if sub_page == 0:
            p.insert_text(pymupdf.Point(50, 100), "8. Market Analysis & Competitive Landscape",
                          fontsize=20, fontname="hebo", color=(0.15, 0.25, 0.45))
            mkt_text = (
                "The global enterprise software market is projected to reach $380 billion by 2027, growing "
                "at a CAGR of 11.2%. Cloud infrastructure and platform services continue to be the fastest-growing "
                "sub-segments, expanding at 19.4% annually.\n\n"
                "Meridian's primary competitors include established players such as Salesforce, ServiceNow, and "
                "Workday in the cloud platform space, as well as legacy vendors like SAP and Oracle in the enterprise "
                "software market. Emerging competition from specialized AI-native startups is increasing in specific "
                "verticals, though their lack of enterprise sales infrastructure limits near-term market impact.\n\n"
                "Market share analysis indicates Meridian holds approximately 4.2% of the addressable market, up "
                "from 3.6% in 2024. The company's competitive advantages include: (1) integrated end-to-end platform "
                "reducing customer vendor sprawl, (2) industry-specific modules for healthcare, financial services, "
                "and manufacturing, (3) hybrid deployment flexibility, and (4) strong customer success organization "
                "with 94% renewal rates.\n\n"
                "Geographic expansion remains a priority, with APAC and Latin America identified as high-growth "
                "opportunity regions. The Singapore and Seoul office openings in Q3 add local presence to complement "
                "existing partner channel coverage."
            )
            p.insert_textbox(pymupdf.Rect(50, 130, 562, 650), mkt_text,
                             fontsize=10.5, fontname="tiro", color=(0.1, 0.1, 0.1),
                             align=pymupdf.TEXT_ALIGN_JUSTIFY)
        else:
            p.insert_text(pymupdf.Point(50, 100), "8. Market Analysis (continued)",
                          fontsize=16, fontname="hebo", color=(0.15, 0.25, 0.45))
            mkt2 = (
                "Analyst Coverage & Recognition\n\n"
                "Meridian was named a Leader in the Gartner Magic Quadrant for Enterprise Integration Platform "
                "as a Service (iPaaS) for the third consecutive year. The company was also positioned in the "
                "Leaders quadrant of the Forrester Wave for Cloud Business Intelligence, Q3 2025.\n\n"
                "Wall Street consensus estimates project FY2026 revenue of $2.15 billion (+12%) and adjusted "
                "EPS of $9.20 (+18%). The stock is trading at approximately 35x forward earnings, a premium to "
                "the SaaS peer group average of 28x, reflecting investor confidence in the company's growth trajectory.\n\n"
                "Twelve analysts cover MERD stock: 8 Buy/Overweight, 3 Hold, 1 Sell. The median 12-month price "
                "target is $168, representing approximately 17% upside from current levels."
            )
            p.insert_textbox(pymupdf.Rect(50, 130, 562, 500), mkt2,
                             fontsize=10.5, fontname="tiro", color=(0.1, 0.1, 0.1),
                             align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGE 15: HR & Talent ==========
    p = doc.new_page(width=612, height=792)
    add_header_footer(p, 15, total_pages)
    p.insert_text(pymupdf.Point(50, 100), "9. Human Resources & Talent Metrics",
                  fontsize=20, fontname="hebo", color=(0.15, 0.25, 0.45))
    hr_text = (
        "Total headcount as of September 30, 2025 was 4,872 employees across 24 offices in 12 countries. "
        "Net hiring in Q3 was 221 positions, primarily in engineering (124), sales (52), and customer success (45).\n\n"
        "Employee engagement score (measured by Gallup Q12): 4.21 out of 5.0, placing Meridian in the "
        "75th percentile of technology companies. Voluntary turnover for the trailing twelve months was "
        "11.8%, down from 14.2% in the prior year, reflecting improved retention programs.\n\n"
        "Diversity metrics: Women represent 38.4% of total workforce (up from 36.1%) and 29.2% of "
        "leadership positions (Director+). Underrepresented minorities comprise 24.8% of U.S. workforce.\n\n"
        "Compensation: Average total compensation (base + bonus + equity) increased 6.8% year-over-year. "
        "The company granted $42.3 million in equity-based compensation during Q3, including RSUs and "
        "performance-based stock units (PSUs) tied to revenue and operating margin targets.\n\n"
        "Learning & Development: Employees completed an average of 32 hours of training in Q3. The Meridian "
        "Leadership Academy graduated its fifth cohort of 24 high-potential managers."
    )
    p.insert_textbox(pymupdf.Rect(50, 130, 562, 650), hr_text,
                     fontsize=10.5, fontname="tiro", color=(0.1, 0.1, 0.1),
                     align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGE 16: Risk Assessment ==========
    p = doc.new_page(width=612, height=792)
    add_header_footer(p, 16, total_pages)
    p.insert_text(pymupdf.Point(50, 100), "10. Risk Assessment & Mitigation",
                  fontsize=20, fontname="hebo", color=(0.15, 0.25, 0.45))
    risk_text = (
        "Cybersecurity: The company completed its annual penetration testing and SOC 2 Type II audit "
        "with no material findings. A new Security Operations Center (SOC) was established in Dublin, "
        "providing 24/7 monitoring coverage. Zero data breaches occurred during Q3.\n\n"
        "Regulatory: GDPR compliance was enhanced with the appointment of a Deputy Data Protection Officer "
        "for APAC operations. The company is actively preparing for the EU AI Act requirements, expected "
        "to take effect in early 2026.\n\n"
        "Supply Chain: Semiconductor shortages have minimal impact on operations due to our cloud-first "
        "strategy. Hardware segment procurement lead times have normalized to 8-10 weeks from peak delays "
        "of 20+ weeks in 2023.\n\n"
        "Macroeconomic: Enterprise IT spending remains resilient despite broader economic uncertainty. "
        "However, elongated sales cycles were observed in certain European markets. Pipeline coverage "
        "remains healthy at 3.8x next quarter forecast.\n\n"
        "Integration Risk: The DataVault acquisition integration carries inherent risk related to "
        "technology platform harmonization and employee retention. A dedicated integration team of 28 "
        "employees is managing this process with bi-weekly executive checkpoint reviews."
    )
    p.insert_textbox(pymupdf.Rect(50, 130, 562, 680), risk_text,
                     fontsize=10.5, fontname="tiro", color=(0.1, 0.1, 0.1),
                     align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGE 17: Strategic Initiatives ==========
    p = doc.new_page(width=612, height=792)
    add_header_footer(p, 17, total_pages)
    p.insert_text(pymupdf.Point(50, 100), "11. Strategic Initiatives Progress",
                  fontsize=20, fontname="hebo", color=(0.15, 0.25, 0.45))
    strat_text = (
        "Initiative 1: Cloud Transition Acceleration (Status: On Track)\n"
        "Target: 65% subscription revenue by FY2026 end. Current: 52.3%. Migration tools and incentive "
        "programs are driving on-premise-to-cloud conversions at 15% per quarter.\n\n"
        "Initiative 2: International Expansion (Status: Ahead of Plan)\n"
        "Target: 45% international revenue by FY2027. Current: 38.8%. APAC growth at 22.4% exceeds plan. "
        "Latin America pilot with partner network launched in September.\n\n"
        "Initiative 3: AI-First Product Strategy (Status: On Track)\n"
        "All product lines now include at least one AI-powered feature. Meridian AI Lab established with "
        "42 specialists. Three AI patents filed in Q3.\n\n"
        "Initiative 4: Customer Success Transformation (Status: On Track)\n"
        "Proactive health scoring deployed for all enterprise accounts. Customer Success-qualified leads "
        "contributed $28.4 million in expansion revenue in Q3.\n\n"
        "Initiative 5: Operational Excellence (Status: Ahead of Plan)\n"
        "Target: 25% adjusted EBITDA margin by FY2026. Current quarter adjusted EBITDA margin: 23.8%. "
        "Automation of internal processes reduced G&A as percentage of revenue from 10.4% to 10.2%."
    )
    p.insert_textbox(pymupdf.Rect(50, 130, 562, 680), strat_text,
                     fontsize=10.5, fontname="tiro", color=(0.1, 0.1, 0.1),
                     align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGE 18: Outlook ==========
    p = doc.new_page(width=612, height=792)
    add_header_footer(p, 18, total_pages)
    p.insert_text(pymupdf.Point(50, 100), "12. Outlook & Guidance for Q4 2025",
                  fontsize=20, fontname="hebo", color=(0.15, 0.25, 0.45))
    outlook_text = (
        "Management reaffirms and narrows full-year fiscal 2025 guidance:\n\n"
        "Revenue: $1.90 to $1.95 billion (previously $1.88 to $1.95 billion)\n"
        "This implies Q4 revenue of $495 to $545 million, reflecting seasonal strength in enterprise "
        "budget flush and continued subscription growth.\n\n"
        "Adjusted EBITDA Margin: 23.0% to 23.5% (raised from 22.0% to 23.0%)\n"
        "The improvement reflects operating leverage from the subscription model and disciplined expense "
        "management. Q4 will include approximately $6 million in one-time integration costs.\n\n"
        "Adjusted EPS: $8.45 to $8.65 (raised from $8.20 to $8.55)\n"
        "Assumes a diluted share count of approximately 27.0 million and an effective tax rate of 20.5%.\n\n"
        "Free Cash Flow: $320 to $340 million for the full year\n"
        "Capital expenditures expected at $90 to $100 million for the year, with Q4 weighted toward "
        "data center expansion in Frankfurt and the new Singapore facility.\n\n"
        "Key assumptions: No material change in macroeconomic conditions, successful Q4 enterprise "
        "renewals (95%+ target), and continued DataVault integration milestones."
    )
    p.insert_textbox(pymupdf.Rect(50, 130, 562, 650), outlook_text,
                     fontsize=10.5, fontname="tiro", color=(0.1, 0.1, 0.1),
                     align=pymupdf.TEXT_ALIGN_JUSTIFY)

    # ========== PAGE 19: Appendix ==========
    p = doc.new_page(width=612, height=792)
    add_header_footer(p, 19, total_pages)
    p.insert_text(pymupdf.Point(50, 100), "13. Appendix: Detailed Financial Tables",
                  fontsize=20, fontname="hebo", color=(0.15, 0.25, 0.45))
    appendix_text = (
        "CONDENSED CONSOLIDATED STATEMENTS OF INCOME (Unaudited)\n"
        "(In millions, except per share amounts)\n\n"
        "                              Q3 2025    Q2 2025    Q3 2024\n"
        "Revenue                       $487.3     $462.1     $426.8\n"
        "Cost of revenue               (174.6)    (167.6)    (158.5)\n"
        "Gross profit                   312.7      294.5      268.3\n\n"
        "Operating expenses:\n"
        "  Research & development       (68.4)     (65.2)     (58.9)\n"
        "  Sales & marketing           (121.3)    (115.8)    (108.7)\n"
        "  General & administrative     (49.9)     (47.1)     (44.4)\n"
        "Total operating expenses      (239.6)    (228.1)    (212.0)\n\n"
        "Operating income                73.1       66.4       56.3\n"
        "Interest expense                (5.8)      (5.9)      (6.1)\n"
        "Other income, net                2.1        1.8        1.5\n"
        "Income before taxes             69.4       62.3       51.7\n"
        "Income tax provision           (11.0)      (8.2)      (3.8)\n"
        "Net income                     $58.4      $54.1      $47.9\n\n"
        "EPS - Basic                    $2.20      $2.05      $1.82\n"
        "EPS - Diluted                  $2.17      $2.01      $1.78\n"
        "Shares - Basic                  26.5       26.4       26.3\n"
        "Shares - Diluted                26.9       26.9       26.9"
    )
    p.insert_textbox(pymupdf.Rect(50, 130, 562, 700), appendix_text,
                     fontsize=9, fontname="cour", color=(0.1, 0.1, 0.1))

    # ========== PAGE 20: Approval & Sign-off ==========
    p = doc.new_page(width=612, height=792)
    add_header_footer(p, 20, total_pages)
    p.insert_text(pymupdf.Point(50, 100), "14. Approval & Sign-off",
                  fontsize=20, fontname="hebo", color=(0.15, 0.25, 0.45))
    signoff_text = (
        "This Quarterly Report for Q3 2025 has been reviewed and approved by the following officers "
        "of Meridian Technologies Inc.:\n\n"
    )
    p.insert_textbox(pymupdf.Rect(50, 130, 562, 190), signoff_text,
                     fontsize=10.5, fontname="tiro", color=(0.1, 0.1, 0.1))

    signatories = [
        ("Katherine A. Morrison", "Chief Executive Officer"),
        ("James D. Hartwell", "Chief Financial Officer"),
        ("Dr. Priya Raghavan", "Chief Technology Officer"),
        ("Robert S. Nakamura", "General Counsel & Corporate Secretary"),
    ]
    y = 210
    for name, title in signatories:
        shape = p.new_shape()
        shape.draw_line(pymupdf.Point(70, y + 30), pymupdf.Point(280, y + 30))
        shape.finish(color=(0.3, 0.3, 0.3), width=0.5)
        shape.commit()
        p.insert_text(pymupdf.Point(70, y + 48), name,
                      fontsize=11, fontname="hebo", color=(0.1, 0.1, 0.1))
        p.insert_text(pymupdf.Point(70, y + 62), title,
                      fontsize=10, fontname="heit", color=(0.3, 0.3, 0.3))
        p.insert_text(pymupdf.Point(350, y + 48), "Date: October 15, 2025",
                      fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))
        y += 90

    # ---- Add Table of Contents bookmarks ----
    toc = [
        [1, "Executive Summary", 3],
        [1, "Financial Highlights", 4],
        [1, "Revenue Analysis by Segment", 6],
        [1, "Operating Expenses Breakdown", 8],
        [1, "Balance Sheet Overview", 9],
        [1, "Cash Flow Statement", 10],
        [1, "Product Development Update", 11],
        [1, "Market Analysis & Competitive Landscape", 13],
        [1, "Human Resources & Talent Metrics", 15],
        [1, "Risk Assessment & Mitigation", 16],
        [1, "Strategic Initiatives Progress", 17],
        [1, "Outlook & Guidance for Q4 2025", 18],
        [1, "Appendix: Detailed Financial Tables", 19],
        [1, "Approval & Sign-off", 20],
    ]
    doc.set_toc(toc)

    # ---- Set document metadata ----
    doc.set_metadata({
        "title": "Meridian Technologies Q3 2025 Quarterly Report",
        "author": "Office of the CFO",
        "subject": "Q3 2025 Financial and Operational Performance",
        "keywords": "quarterly report, Q3 2025, Meridian Technologies, financial results",
        "creator": "Meridian Report Generator",
        "producer": "PyMuPDF",
    })

    # Save the basic document first
    doc.save(OUTPUT)
    doc.close()

    # ---- Now add JavaScript actions and form fields using pikepdf ----
    import pikepdf
    from decimal import Decimal

    pdf = pikepdf.open(OUTPUT, allow_overwriting_input=True)

    # Add 2 JavaScript actions to the document catalog
    js_code_1 = pikepdf.String("app.alert('Welcome to the Meridian Technologies Q3 2025 Quarterly Report. Please review all sections before signing off.');")
    js_action_1 = pikepdf.Dictionary({
        "/Type": pikepdf.Name("/Action"),
        "/S": pikepdf.Name("/JavaScript"),
        "/JS": js_code_1,
    })

    js_code_2 = pikepdf.String("var today = new Date(); this.getField('review_date').value = util.printd('yyyy-mm-dd', today);")
    js_action_2 = pikepdf.Dictionary({
        "/Type": pikepdf.Name("/Action"),
        "/S": pikepdf.Name("/JavaScript"),
        "/JS": js_code_2,
    })

    # Set the first JS as an OpenAction on the document
    pdf.Root["/OpenAction"] = pdf.make_indirect(js_action_1)

    # Add second JS to document-level JavaScript names
    js_name_tree = pikepdf.Dictionary({
        "/Names": pikepdf.Array([
            pikepdf.String("AutoFillDate"),
            pdf.make_indirect(js_action_2),
        ]),
    })
    if "/Names" not in pdf.Root:
        pdf.Root["/Names"] = pdf.make_indirect(pikepdf.Dictionary())
    pdf.Root["/Names"]["/JavaScript"] = pdf.make_indirect(js_name_tree)

    # ---- Add 4 form fields (AcroForm) on page 20 (index 19) ----
    page20 = pdf.pages[19]
    page_ref = pdf.pages[19].obj

    # Helper to create form fields
    def make_text_field(name, value, rect):
        field = pdf.make_indirect(pikepdf.Dictionary({
            "/Type": pikepdf.Name("/Annot"),
            "/Subtype": pikepdf.Name("/Widget"),
            "/FT": pikepdf.Name("/Tx"),
            "/T": pikepdf.String(name),
            "/V": pikepdf.String(value),
            "/Rect": pikepdf.Array([Decimal(str(r)) for r in rect]),
            "/P": page_ref,
            "/F": 4,  # Print flag
            "/DA": pikepdf.String("/Helv 10 Tf 0 g"),
        }))
        return field

    def make_checkbox(name, checked, rect):
        val = pikepdf.Name("/Yes") if checked else pikepdf.Name("/Off")
        field = pdf.make_indirect(pikepdf.Dictionary({
            "/Type": pikepdf.Name("/Annot"),
            "/Subtype": pikepdf.Name("/Widget"),
            "/FT": pikepdf.Name("/Btn"),
            "/T": pikepdf.String(name),
            "/V": val,
            "/Rect": pikepdf.Array([Decimal(str(r)) for r in rect]),
            "/P": page_ref,
            "/F": 4,
        }))
        return field

    # Create the 4 form fields
    field1 = make_text_field("reviewer_name", "", [350, 250, 550, 270])
    field2 = make_text_field("review_date", "", [350, 280, 550, 300])
    field3 = make_text_field("review_comments", "", [350, 310, 550, 360])
    field4 = make_checkbox("review_approved", False, [350, 370, 370, 390])

    fields = [field1, field2, field3, field4]

    # Create AcroForm
    pdf.Root["/AcroForm"] = pdf.make_indirect(pikepdf.Dictionary({
        "/Fields": pikepdf.Array(fields),
        "/DA": pikepdf.String("/Helv 10 Tf 0 g"),
    }))

    # Add annotations to page 20
    if "/Annots" not in page_ref:
        page_ref["/Annots"] = pikepdf.Array()
    for f in fields:
        page_ref["/Annots"].append(f)

    pdf.save(OUTPUT)
    pdf.close()

    print(f'Initial file created: {OUTPUT}')
    print(f'Features: 20 pages, JavaScript actions, form fields, non-embedded base14 fonts')

    # Make sure the golden output does NOT exist
    golden_path = f'{ARCHIVE_DIR}/quarterly_report_pdfa.pdf'
    if os.path.exists(golden_path):
        os.remove(golden_path)

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
