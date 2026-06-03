"""
Initial Setup: PDF table extractor task
Task ID: pdf_gf3_021
Domain: pdf / libreoffice_calc
Creates a 15-page financial PDF with 8 tables of varying sizes.
"""

import os
import shlex
import subprocess
import time
import shutil

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_021'
REPORTS_DIR = f'{WORKDIR}/reports'
SCRIPTS_DIR = f'{WORKDIR}/scripts'
TABLES_DIR = f'{REPORTS_DIR}/tables'
OUTPUT_PDF = f'{REPORTS_DIR}/financial_tables.pdf'


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
    # Ensure directories exist
    os.makedirs(REPORTS_DIR, exist_ok=True)
    os.makedirs(SCRIPTS_DIR, exist_ok=True)

    # Ensure tables/ directory does NOT exist (task requires creating it)
    if os.path.exists(TABLES_DIR):
        shutil.rmtree(TABLES_DIR)

    # Ensure extract_tables.py does NOT exist
    script_path = f'{SCRIPTS_DIR}/extract_tables.py'
    if os.path.exists(script_path):
        os.remove(script_path)

    # Install PyMuPDF for PDF creation
    subprocess.run(['pip3', 'install', 'PyMuPDF'], capture_output=True)

    import pymupdf

    doc = pymupdf.open()

    # Define 8 financial tables distributed across 15 pages
    # Table locations: pages 2, 4, 5, 7, 9, 10, 12, 14 (0-indexed: 1, 3, 4, 6, 8, 9, 11, 13)
    table_pages = [1, 3, 4, 6, 8, 9, 11, 13]

    # Table data definitions
    tables_data = [
        {
            "title": "Table 1: Quarterly Revenue Summary (FY2024)",
            "headers": ["Quarter", "Revenue ($M)", "COGS ($M)", "Gross Profit ($M)", "Margin (%)"],
            "rows": [
                ["Q1 2024", "12.45", "7.23", "5.22", "41.9"],
                ["Q2 2024", "14.87", "8.56", "6.31", "42.4"],
                ["Q3 2024", "16.32", "9.12", "7.20", "44.1"],
                ["Q4 2024", "18.91", "10.45", "8.46", "44.7"],
                ["Total", "62.55", "35.36", "27.19", "43.5"],
            ]
        },
        {
            "title": "Table 2: Department Operating Expenses",
            "headers": ["Department", "Salaries", "Marketing", "Travel", "Software", "Total"],
            "rows": [
                ["Engineering", "$2,340,000", "$45,000", "$120,000", "$380,000", "$2,885,000"],
                ["Sales", "$1,890,000", "$560,000", "$340,000", "$95,000", "$2,885,000"],
                ["Marketing", "$980,000", "$1,200,000", "$85,000", "$210,000", "$2,475,000"],
                ["Finance", "$1,120,000", "$12,000", "$45,000", "$180,000", "$1,357,000"],
                ["HR", "$780,000", "$25,000", "$30,000", "$65,000", "$900,000"],
                ["Operations", "$1,560,000", "$35,000", "$95,000", "$290,000", "$1,980,000"],
                ["Legal", "$890,000", "$8,000", "$55,000", "$120,000", "$1,073,000"],
            ]
        },
        {
            "title": "Table 3: Product Line Performance",
            "headers": ["Product", "Units Sold", "Avg Price", "Revenue", "YoY Growth"],
            "rows": [
                ["CloudSync Pro", "3,245", "$149.99", "$486,718", "+23.4%"],
                ["DataVault Enterprise", "892", "$499.00", "$445,108", "+15.7%"],
                ["SecureNet Gateway", "1,567", "$299.50", "$469,317", "+31.2%"],
                ["AnalyticsPro Suite", "2,103", "$199.00", "$418,497", "+8.9%"],
                ["DevOps Pipeline", "734", "$599.00", "$439,666", "+42.1%"],
                ["MobileFirst Platform", "4,521", "$79.99", "$361,635", "+56.3%"],
            ]
        },
        {
            "title": "Table 4: Regional Sales Breakdown",
            "headers": ["Region", "Q1", "Q2", "Q3", "Q4", "Annual Total"],
            "rows": [
                ["North America", "$4.2M", "$4.8M", "$5.3M", "$6.1M", "$20.4M"],
                ["Europe", "$2.8M", "$3.2M", "$3.6M", "$4.1M", "$13.7M"],
                ["Asia Pacific", "$3.1M", "$3.5M", "$4.0M", "$4.7M", "$15.3M"],
                ["Latin America", "$1.2M", "$1.5M", "$1.7M", "$2.0M", "$6.4M"],
                ["Middle East & Africa", "$0.8M", "$0.9M", "$1.1M", "$1.3M", "$4.1M"],
                ["Total", "$12.1M", "$13.9M", "$15.7M", "$18.2M", "$59.9M"],
            ]
        },
        {
            "title": "Table 5: Employee Headcount by Division",
            "headers": ["Division", "Full-Time", "Part-Time", "Contractors", "Total", "Budget"],
            "rows": [
                ["Engineering", "234", "12", "45", "291", "$29.1M"],
                ["Product", "67", "5", "18", "90", "$9.0M"],
                ["Sales", "189", "23", "34", "246", "$19.7M"],
                ["Marketing", "78", "8", "22", "108", "$7.6M"],
                ["Customer Success", "112", "34", "15", "161", "$11.3M"],
                ["G&A", "89", "6", "8", "103", "$8.2M"],
                ["Total", "769", "88", "142", "999", "$84.9M"],
            ]
        },
        {
            "title": "Table 6: Cash Flow Statement Summary",
            "headers": ["Category", "FY2023", "FY2024", "Change"],
            "rows": [
                ["Operating Cash Flow", "$8,450,000", "$11,230,000", "+32.9%"],
                ["Capital Expenditures", "($2,100,000)", "($3,450,000)", "+64.3%"],
                ["Free Cash Flow", "$6,350,000", "$7,780,000", "+22.5%"],
                ["Debt Repayment", "($1,500,000)", "($2,000,000)", "+33.3%"],
                ["Dividends Paid", "($800,000)", "($1,200,000)", "+50.0%"],
                ["Net Cash Change", "$4,050,000", "$4,580,000", "+13.1%"],
                ["Cash Balance (EOY)", "$15,200,000", "$19,780,000", "+30.1%"],
                ["Short-term Investments", "$3,400,000", "$5,100,000", "+50.0%"],
            ]
        },
        {
            "title": "Table 7: Customer Acquisition Metrics",
            "headers": ["Channel", "Leads", "Conversions", "Conv. Rate", "CAC", "LTV"],
            "rows": [
                ["Organic Search", "12,450", "1,245", "10.0%", "$85", "$2,340"],
                ["Paid Search", "8,900", "712", "8.0%", "$145", "$1,890"],
                ["Social Media", "15,670", "940", "6.0%", "$110", "$1,560"],
                ["Email Campaigns", "6,230", "873", "14.0%", "$42", "$2,100"],
                ["Referral Program", "3,890", "623", "16.0%", "$65", "$3,450"],
                ["Partner Channel", "2,100", "378", "18.0%", "$195", "$4,200"],
                ["Direct Sales", "1,560", "312", "20.0%", "$320", "$5,670"],
                ["Events/Trade Shows", "890", "134", "15.1%", "$450", "$3,890"],
                ["Total/Weighted Avg", "51,690", "5,217", "10.1%", "$125", "$2,650"],
            ]
        },
        {
            "title": "Table 8: Balance Sheet Highlights",
            "headers": ["Item", "Dec 2023", "Dec 2024", "Change (%)"],
            "rows": [
                ["Total Assets", "$45,230,000", "$58,450,000", "+29.2%"],
                ["Current Assets", "$22,100,000", "$28,900,000", "+30.8%"],
                ["Fixed Assets", "$18,500,000", "$23,200,000", "+25.4%"],
                ["Intangible Assets", "$4,630,000", "$6,350,000", "+37.1%"],
                ["Total Liabilities", "$18,900,000", "$22,100,000", "+16.9%"],
                ["Current Liabilities", "$8,200,000", "$9,450,000", "+15.2%"],
                ["Long-term Debt", "$10,700,000", "$12,650,000", "+18.2%"],
                ["Shareholders' Equity", "$26,330,000", "$36,350,000", "+38.1%"],
                ["Book Value/Share", "$13.17", "$18.18", "+38.0%"],
            ]
        },
    ]

    # Non-table page content for narrative pages
    narrative_pages = {
        0: {
            "title": "Meridian Technologies Inc.\nAnnual Financial Report FY2024",
            "body": (
                "Prepared by the Office of the Chief Financial Officer\n"
                "Confidential - For Internal Distribution Only\n\n"
                "Report Date: March 15, 2025\n"
                "Fiscal Year: January 1, 2024 - December 31, 2024"
            )
        },
        2: {
            "title": "Executive Summary",
            "body": (
                "Meridian Technologies delivered strong financial performance in FY2024, "
                "with total revenue reaching $62.55 million, representing a 28.3% year-over-year "
                "increase. Our gross margin improved to 43.5%, up from 40.2% in the prior year, "
                "driven by operational efficiencies and favorable product mix shifts. "
                "The company's expansion into the Asia Pacific market contributed significantly "
                "to top-line growth, with the region posting 35.2% revenue growth.\n\n"
                "Key strategic initiatives completed during the fiscal year include the launch "
                "of MobileFirst Platform, which achieved 56.3% growth in unit sales, and the "
                "expansion of our enterprise customer base through the Partner Channel program. "
                "Operating cash flow increased by 32.9% to $11.23 million, providing ample "
                "resources for continued investment in R&D and market expansion."
            )
        },
        5: {
            "title": "Market Analysis and Competitive Positioning",
            "body": (
                "The global enterprise software market grew by 11.2% in 2024, reaching $685 billion "
                "in total addressable market. Meridian Technologies maintained its position as a "
                "leading provider in the cloud security and data management segments. Key market "
                "trends driving growth include the acceleration of cloud adoption among mid-market "
                "enterprises, increasing regulatory requirements for data protection, and the "
                "growing demand for integrated DevOps solutions.\n\n"
                "Competitive dynamics remain favorable with our Net Promoter Score increasing "
                "from 62 to 71, reflecting strong customer satisfaction. Our technology moat "
                "continues to widen with 12 new patents filed during the fiscal year and R&D "
                "spending increasing to 18.5% of revenue."
            )
        },
        7: {
            "title": "Operational Highlights",
            "body": (
                "The operations team achieved significant milestones in FY2024:\n\n"
                "Infrastructure Uptime: 99.97% across all cloud services\n"
                "Customer Support: Average response time reduced to 2.3 hours (from 4.1 hours)\n"
                "Product Releases: 4 major releases and 23 minor updates delivered on schedule\n"
                "Security: Zero critical security incidents; SOC 2 Type II certification renewed\n"
                "Partner Ecosystem: 45 new technology partnerships established\n\n"
                "The engineering team grew from 234 to 291 employees, with strategic hires "
                "in machine learning, cloud infrastructure, and mobile development. Employee "
                "retention rate improved to 92.3%, above the industry average of 85.1%."
            )
        },
        10: {
            "title": "Risk Factors and Outlook",
            "body": (
                "While the company's financial position is strong, several risk factors warrant "
                "attention in the coming fiscal year:\n\n"
                "1. Macroeconomic uncertainty may impact enterprise IT spending budgets\n"
                "2. Increasing competition from well-funded startups in the cloud security space\n"
                "3. Regulatory changes in key markets (GDPR enforcement, US data privacy laws)\n"
                "4. Currency fluctuation risk as international revenue reaches 66% of total\n"
                "5. Talent acquisition challenges in specialized engineering roles\n\n"
                "Despite these risks, the FY2025 outlook remains positive. Management guidance "
                "projects revenue growth of 22-25%, with continued margin expansion as the "
                "company benefits from operating leverage."
            )
        },
        12: {
            "title": "Investment and Capital Allocation",
            "body": (
                "Capital allocation priorities for FY2025 reflect the company's commitment to "
                "balancing growth investments with shareholder returns:\n\n"
                "R&D Investment: $13.5M planned (21% of projected revenue)\n"
                "Sales & Marketing Expansion: $8.2M for new market entry\n"
                "Infrastructure: $4.8M for data center and cloud infrastructure\n"
                "M&A Reserve: $10M allocated for strategic acquisitions\n"
                "Share Buyback Program: $3M authorized by the Board\n"
                "Dividend Increase: 15% increase to $0.48 per share annually\n\n"
                "The Board has approved a $25M credit facility to support potential "
                "acquisition opportunities in the AI/ML and cybersecurity verticals."
            )
        },
        14: {
            "title": "Appendix and Notes",
            "body": (
                "This report contains forward-looking statements within the meaning of Section 27A "
                "of the Securities Act. Actual results may differ materially from those projected. "
                "All financial figures are presented in accordance with GAAP unless otherwise noted.\n\n"
                "Auditor: Deloitte & Touche LLP\n"
                "Audit Opinion: Unqualified\n"
                "Internal Controls Assessment: Effective\n\n"
                "For questions regarding this report, contact:\n"
                "Sarah Chen, Chief Financial Officer\n"
                "Email: s.chen@meridiantech.com\n"
                "Phone: +1 (415) 555-0142"
            )
        },
    }

    def draw_table(page, title, headers, rows, start_y):
        """Draw a table on a PDF page with borders."""
        fontsize = 9
        header_fontsize = 10
        title_fontsize = 12
        col_count = len(headers)
        page_width = page.rect.width
        margin = 50
        table_width = page_width - 2 * margin
        col_width = table_width / col_count
        row_height = 20
        header_height = 22

        # Title
        page.insert_text(
            pymupdf.Point(margin, start_y),
            title,
            fontsize=title_fontsize,
            fontname="hebo",
            color=(0, 0, 0.5),
        )
        start_y += 20

        shape = page.new_shape()

        # Header background
        header_rect = pymupdf.Rect(margin, start_y, margin + table_width, start_y + header_height)
        shape.draw_rect(header_rect)
        shape.finish(color=(0, 0, 0), fill=(0.2, 0.3, 0.5), width=0.5)

        # Header text
        for i, h in enumerate(headers):
            x = margin + i * col_width + 4
            page.insert_text(
                pymupdf.Point(x, start_y + 15),
                h,
                fontsize=header_fontsize,
                fontname="hebo",
                color=(1, 1, 1),
            )

        start_y += header_height

        # Data rows
        for r_idx, row in enumerate(rows):
            # Alternating row background
            if r_idx % 2 == 0:
                row_rect = pymupdf.Rect(margin, start_y, margin + table_width, start_y + row_height)
                shape2 = page.new_shape()
                shape2.draw_rect(row_rect)
                shape2.finish(color=None, fill=(0.93, 0.93, 0.97), width=0)
                shape2.commit()

            for i, val in enumerate(row):
                x = margin + i * col_width + 4
                page.insert_text(
                    pymupdf.Point(x, start_y + 14),
                    str(val),
                    fontsize=fontsize,
                    fontname="helv",
                    color=(0, 0, 0),
                )
            start_y += row_height

        # Draw table border
        border_rect = pymupdf.Rect(margin, start_y - row_height * len(rows) - header_height,
                                    margin + table_width, start_y)
        shape3 = page.new_shape()
        shape3.draw_rect(border_rect)
        shape3.finish(color=(0, 0, 0), fill=None, width=0.5)
        shape3.commit()

        # Draw column lines
        shape4 = page.new_shape()
        for i in range(1, col_count):
            x = margin + i * col_width
            shape4.draw_line(
                pymupdf.Point(x, start_y - row_height * len(rows) - header_height),
                pymupdf.Point(x, start_y),
            )
        shape4.finish(color=(0.5, 0.5, 0.5), width=0.3)
        shape4.commit()

        # Draw row lines
        shape5 = page.new_shape()
        for r_idx in range(len(rows) + 1):
            y = start_y - row_height * (len(rows) - r_idx)
            shape5.draw_line(
                pymupdf.Point(margin, y),
                pymupdf.Point(margin + table_width, y),
            )
        shape5.finish(color=(0.5, 0.5, 0.5), width=0.3)
        shape5.commit()

        shape.commit()
        return start_y + 10

    # Create all 15 pages
    table_idx = 0
    for page_num in range(15):
        page = doc.new_page(width=595, height=842)  # A4

        # Add page header
        page.insert_text(
            pymupdf.Point(50, 30),
            "Meridian Technologies Inc. - Annual Financial Report FY2024",
            fontsize=8,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )
        # Page number
        page.insert_text(
            pymupdf.Point(530, 830),
            f"Page {page_num + 1}",
            fontsize=8,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
        )

        if page_num in narrative_pages:
            info = narrative_pages[page_num]
            # Title
            if page_num == 0:
                # Cover page - centered
                page.insert_text(
                    pymupdf.Point(100, 300),
                    info["title"].split('\n')[0],
                    fontsize=24,
                    fontname="hebo",
                    color=(0.1, 0.2, 0.4),
                )
                page.insert_text(
                    pymupdf.Point(120, 340),
                    info["title"].split('\n')[1],
                    fontsize=18,
                    fontname="hebo",
                    color=(0.1, 0.2, 0.4),
                )
                rect = pymupdf.Rect(100, 400, 495, 550)
                page.insert_textbox(
                    rect,
                    info["body"],
                    fontsize=12,
                    fontname="helv",
                    color=(0.3, 0.3, 0.3),
                    align=pymupdf.TEXT_ALIGN_CENTER,
                )
            else:
                page.insert_text(
                    pymupdf.Point(50, 70),
                    info["title"],
                    fontsize=16,
                    fontname="hebo",
                    color=(0.1, 0.2, 0.4),
                )
                rect = pymupdf.Rect(50, 95, 545, 780)
                page.insert_textbox(
                    rect,
                    info["body"],
                    fontsize=11,
                    fontname="helv",
                    color=(0, 0, 0),
                    align=pymupdf.TEXT_ALIGN_LEFT,
                )

        if page_num in table_pages:
            td = tables_data[table_idx]
            # If page also has narrative, start table lower
            start_y = 400 if page_num in narrative_pages else 80
            draw_table(page, td["title"], td["headers"], td["rows"], start_y)
            table_idx += 1

    doc.save(OUTPUT_PDF)
    doc.close()
    print(f'Initial file created: {OUTPUT_PDF}')
    print(f'PDF has 15 pages with 8 tables')

    # Install camelot/pdfplumber so they are available for the agent
    subprocess.run(['pip3', 'install', 'pdfplumber', 'camelot-py[cv]'], capture_output=True)

    # Open PDF in evince for GUI-ready state
    launch_gui(f'evince "{OUTPUT_PDF}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')


create_initial()
