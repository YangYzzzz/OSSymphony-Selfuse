"""
Initial Setup: Extract Executive Summary from PDF and create Google Doc
Task ID: osworld_multi_apps_pdf_to_gdocs_002
Domain: multi_apps (PDF + Chrome/Google Drive)

Creates:
  - /home/user/Desktop/annual_report_2023.pdf  (PDF with Executive Summary, Financial Highlights, Operations Review)
  - Opens Chrome with Google Drive (board_materials folder visible)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_to_gdocs_002'
DESKTOP = f'{WORKDIR}/Desktop'
PDF_PATH = f'{DESKTOP}/annual_report_2023.pdf'


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


def create_pdf():
    """Create annual_report_2023.pdf with realistic annual report content."""
    try:
        from fpdf import FPDF
    except ImportError:
        subprocess.run(['pip3', 'install', 'fpdf2'], check=True)
        from fpdf import FPDF

    os.makedirs(DESKTOP, exist_ok=True)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # ---- Cover Page ----
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 28)
    pdf.ln(40)
    pdf.cell(0, 15, 'Meridian Capital Group', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 20)
    pdf.cell(0, 12, 'Annual Report 2023', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(6)
    pdf.set_font('Helvetica', 'I', 14)
    pdf.cell(0, 10, 'Building Tomorrow\'s Prosperity Today', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(20)
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 8, 'Fiscal Year Ended December 31, 2023', align='C', new_x='LMARGIN', new_y='NEXT')

    # ---- Table of Contents ----
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 18)
    pdf.ln(10)
    pdf.cell(0, 12, 'Table of Contents', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(4)
    pdf.set_font('Helvetica', '', 12)
    toc_items = [
        ('Executive Summary', '3'),
        ('Financial Highlights', '5'),
        ('Operations Review', '7'),
        ('Risk Management', '9'),
        ('Corporate Governance', '11'),
        ('Auditor\'s Report', '13'),
    ]
    for section, page in toc_items:
        pdf.cell(140, 9, section)
        pdf.cell(0, 9, page, align='R', new_x='LMARGIN', new_y='NEXT')
        pdf.set_draw_color(200, 200, 200)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
        pdf.ln(1)

    # ---- Executive Summary ----
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 20)
    pdf.ln(8)
    pdf.cell(0, 14, 'Executive Summary', new_x='LMARGIN', new_y='NEXT')
    pdf.set_draw_color(0, 82, 165)
    pdf.set_line_width(0.8)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(6)

    pdf.set_font('Helvetica', '', 11)
    exec_summary_paragraphs = [
        "Meridian Capital Group concluded fiscal year 2023 with exceptional performance across all business units, "
        "demonstrating the strength and resilience of our diversified investment strategy. Total revenues reached "
        "$4.72 billion, representing a 14.3% increase compared to the prior year, driven by strong performance in "
        "our asset management and private equity divisions.",

        "Net income attributable to shareholders grew 18.7% year-over-year to $892 million, or $6.41 per diluted "
        "share. Our return on equity improved to 17.2%, up from 14.9% in 2022, reflecting the successful execution "
        "of our capital allocation strategy and disciplined cost management initiatives.",

        "Assets under management (AUM) reached a record $148.6 billion as of December 31, 2023, an increase of "
        "$21.3 billion or 16.7% from year-end 2022. Net inflows of $14.8 billion were driven by strong institutional "
        "client demand across our fixed income, equities, and alternative investment platforms.",

        "During 2023, we completed three strategic acquisitions totaling $1.2 billion in aggregate consideration, "
        "expanding our capabilities in sustainable infrastructure and emerging market credit. These transactions "
        "are expected to contribute approximately $340 million in incremental AUM fees on an annualized basis.",

        "Our digital transformation program delivered $87 million in operational savings during the year, ahead "
        "of our initial target of $65 million. We invested $234 million in technology modernization, including "
        "the rollout of our proprietary AI-driven risk analytics platform, which is now deployed across 92% of "
        "our active portfolio companies.",

        "The Board of Directors approved a 22% increase in the annual dividend to $2.20 per share, reflecting "
        "confidence in our sustained earnings growth and robust cash generation. We also repurchased 6.8 million "
        "shares for $412 million during 2023 under our ongoing share buyback program.",

        "Looking ahead to 2024, management is cautiously optimistic. We anticipate revenue growth of 8-12% and "
        "expect AUM to reach $165-170 billion by year-end, supported by favorable market conditions and continued "
        "momentum in our client acquisition pipeline. Key priorities include the full integration of our 2023 "
        "acquisitions, further expansion of our sustainable investment offerings, and continued investment in "
        "technology and talent.",

        "We remain committed to our Environmental, Social, and Governance (ESG) principles. In 2023, we launched "
        "the Meridian Sustainable Growth Fund with $3.8 billion in initial commitments, and we achieved carbon "
        "neutrality across our corporate operations, two years ahead of our original 2025 target.",

        "On behalf of the Board and senior management, we express deep gratitude to our clients, shareholders, "
        "and employees for their continued trust and dedication. The foundation we have built positions Meridian "
        "Capital Group for sustained success in the years ahead.",
    ]

    for para in exec_summary_paragraphs:
        pdf.multi_cell(0, 6, para, new_x='LMARGIN', new_y='NEXT')
        pdf.ln(4)

    # Key metrics box
    pdf.ln(4)
    pdf.set_fill_color(240, 246, 255)
    pdf.set_draw_color(0, 82, 165)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, '  Key 2023 Metrics', fill=True, new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 10)
    metrics = [
        ('Total Revenue', '$4.72 billion', '+14.3% YoY'),
        ('Net Income', '$892 million', '+18.7% YoY'),
        ('EPS (diluted)', '$6.41', '+20.1% YoY'),
        ('Return on Equity', '17.2%', '+2.3 pp YoY'),
        ('Assets Under Management', '$148.6 billion', '+16.7% YoY'),
        ('Dividend per Share', '$2.20', '+22.2% YoY'),
    ]
    for label, value, change in metrics:
        pdf.cell(80, 7, f'  {label}', fill=True)
        pdf.cell(50, 7, value, fill=True)
        pdf.cell(0, 7, change, fill=True, new_x='LMARGIN', new_y='NEXT')
    pdf.ln(4)

    # ---- Financial Highlights ----
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 20)
    pdf.ln(8)
    pdf.cell(0, 14, 'Financial Highlights', new_x='LMARGIN', new_y='NEXT')
    pdf.set_draw_color(0, 140, 100)
    pdf.set_line_width(0.8)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(6)
    pdf.set_font('Helvetica', '', 11)

    fin_paragraphs = [
        "Revenue for fiscal year 2023 totaled $4.72 billion, with asset management fees contributing 61% ($2.88 billion), "
        "private equity carried interest and management fees at 24% ($1.13 billion), and other financial services "
        "comprising the remaining 15% ($710 million).",

        "Operating expenses increased 9.1% to $3.22 billion, primarily driven by higher compensation and benefits "
        "expenses (+11.4%) reflecting performance-based bonuses tied to exceptional fund returns, partially offset by "
        "technology-enabled efficiency gains (-$87 million in operational cost savings).",

        "EBITDA reached $1.62 billion with an EBITDA margin of 34.3%, expanding from 32.1% in the prior year. "
        "Interest expense declined 8.3% to $156 million following the refinancing of $2.1 billion in long-term debt "
        "at more favorable rates in Q2 2023.",

        "The balance sheet remains strong with total assets of $18.4 billion, including $3.2 billion in cash and "
        "liquid investments, providing ample flexibility to pursue strategic opportunities. Total debt stands at "
        "$4.8 billion with a debt-to-equity ratio of 0.89x, well within our target range of 0.75-1.00x.",

        "Cash flow from operations was $1.14 billion for the year, with free cash flow of $876 million after "
        "deducting $264 million in capital expenditures, primarily related to our technology modernization program.",
    ]
    for para in fin_paragraphs:
        pdf.multi_cell(0, 6, para, new_x='LMARGIN', new_y='NEXT')
        pdf.ln(4)

    # Financial table
    pdf.ln(4)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_fill_color(0, 82, 165)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(80, 8, 'Financial Metric', fill=True)
    pdf.cell(40, 8, 'FY 2023', fill=True, align='R')
    pdf.cell(40, 8, 'FY 2022', fill=True, align='R')
    pdf.cell(0, 8, 'Change', fill=True, align='R', new_x='LMARGIN', new_y='NEXT')
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', '', 10)
    fin_data = [
        ('Total Revenue ($B)', '$4.72', '$4.13', '+14.3%'),
        ('Operating Income ($B)', '$1.50', '$1.27', '+18.1%'),
        ('Net Income ($M)', '$892', '$751', '+18.7%'),
        ('EPS - Diluted', '$6.41', '$5.34', '+20.1%'),
        ('EBITDA Margin', '34.3%', '32.1%', '+2.2 pp'),
        ('Free Cash Flow ($M)', '$876', '$734', '+19.3%'),
        ('Dividends per Share', '$2.20', '$1.80', '+22.2%'),
    ]
    for i, (label, v2023, v2022, chg) in enumerate(fin_data):
        fill = i % 2 == 0
        pdf.set_fill_color(245, 248, 255) if fill else pdf.set_fill_color(255, 255, 255)
        pdf.cell(80, 7, label, fill=True)
        pdf.cell(40, 7, v2023, fill=True, align='R')
        pdf.cell(40, 7, v2022, fill=True, align='R')
        pdf.cell(0, 7, chg, fill=True, align='R', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(4)

    # ---- Operations Review ----
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 20)
    pdf.ln(8)
    pdf.cell(0, 14, 'Operations Review', new_x='LMARGIN', new_y='NEXT')
    pdf.set_draw_color(180, 60, 0)
    pdf.set_line_width(0.8)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(6)
    pdf.set_font('Helvetica', '', 11)

    ops_paragraphs = [
        "Our Asset Management division delivered outstanding results in 2023, with AUM growing 16.7% to $148.6 billion. "
        "The Fixed Income platform benefited from rising interest rates, generating net inflows of $8.2 billion. "
        "Our Global Equities funds outperformed their respective benchmarks by an average of 3.4 percentage points.",

        "The Private Equity segment completed 11 new platform investments and 24 add-on acquisitions during 2023, "
        "deploying $6.8 billion in capital. The portfolio generated a gross IRR of 24.7% on realized investments "
        "during the year, including the successful IPO of TechForge Solutions at a 4.2x return on invested capital.",

        "Our Real Assets division, which manages infrastructure and real estate investments, expanded AUM by 28% to "
        "$24.8 billion. The infrastructure portfolio benefited from inflation-linked revenue contracts, with portfolio "
        "companies generating average EBITDA growth of 19.3% during the year.",

        "Technology and Operations executed on three major initiatives: (1) migration of core portfolio analytics to a "
        "cloud-native infrastructure, reducing processing time by 67%; (2) deployment of our proprietary AI risk "
        "engine across all investment teams; and (3) implementation of a unified client reporting portal "
        "serving 2,340 institutional clients.",

        "Human Capital: We grew our headcount from 4,280 to 4,710 professionals during 2023, adding key talent in "
        "technology, ESG research, and emerging markets. Our voluntary turnover rate declined to 7.2%, below the "
        "industry average of 11.4%, reflecting strong employee engagement and our continued investment in "
        "professional development programs.",

        "Risk Management maintained our strong credit quality profile throughout the year. Non-performing assets "
        "declined to 0.42% of total AUM from 0.61% in 2022. Our Value-at-Risk (VaR) models indicated a "
        "maximum one-day loss at 99% confidence of $124 million, consistent with our risk appetite framework.",
    ]
    for para in ops_paragraphs:
        pdf.multi_cell(0, 6, para, new_x='LMARGIN', new_y='NEXT')
        pdf.ln(4)

    # ---- Risk Management ----
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 20)
    pdf.ln(8)
    pdf.cell(0, 14, 'Risk Management', new_x='LMARGIN', new_y='NEXT')
    pdf.set_draw_color(120, 0, 120)
    pdf.set_line_width(0.8)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(6)
    pdf.set_font('Helvetica', '', 11)

    risk_paragraphs = [
        "Meridian Capital Group maintains a comprehensive enterprise risk management framework designed to identify, "
        "assess, monitor, and mitigate risks across all dimensions of our business. The Risk Committee of the Board "
        "provides oversight of our risk appetite, policies, and controls.",

        "Market risk remains well-controlled with diversified exposure across geographies, asset classes, and "
        "economic sectors. Our stress testing program, which incorporates 48 macroeconomic scenarios, demonstrates "
        "portfolio resilience across a range of adverse conditions.",

        "Operational risk management was strengthened in 2023 through investments in cybersecurity infrastructure "
        "($48 million), business continuity planning, and the expansion of our internal audit function. We "
        "maintained zero material cybersecurity incidents and zero regulatory enforcement actions during the year.",
    ]
    for para in risk_paragraphs:
        pdf.multi_cell(0, 6, para, new_x='LMARGIN', new_y='NEXT')
        pdf.ln(4)

    # ---- Corporate Governance ----
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 20)
    pdf.ln(8)
    pdf.cell(0, 14, 'Corporate Governance', new_x='LMARGIN', new_y='NEXT')
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.8)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(6)
    pdf.set_font('Helvetica', '', 11)
    pdf.multi_cell(0, 6,
        "Meridian Capital Group is committed to the highest standards of corporate governance. Our Board of "
        "Directors consists of 11 members, with 9 independent directors. Board committees include Audit, "
        "Risk, Compensation, Nominations & Governance, and Sustainability. In 2023, we enhanced our ESG "
        "disclosure practices in alignment with TCFD and SASB reporting frameworks.",
        new_x='LMARGIN', new_y='NEXT')

    pdf.output(PDF_PATH)
    print(f'PDF created: {PDF_PATH}')


def setup_initial():
    """Set up the initial environment state."""
    # 1. Create the PDF
    create_pdf()

    # 2. Launch Chrome with Google Drive open (with Google Drive board_materials folder)
    #    The task context says Chrome is open with Google Drive signed in
    launch_gui(
        'google-chrome --new-window "https://drive.google.com/drive/folders/"',
        delay_sec=3.0
    )
    print('GUI_READY: Chrome opened with Google Drive')


setup_initial()
