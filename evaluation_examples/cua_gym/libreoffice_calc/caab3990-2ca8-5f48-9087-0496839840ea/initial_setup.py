"""
Initial Setup: Extract teaching grant stats from PDFs and create LibreOffice Calc table
Task ID: osworld_multi_apps_pdf_stats_table_009
Domain: libreoffice_calc (multi-app: PDF files + Calc)

Creates:
  - /home/user/Documents/Teaching_Grants/ with 6 PDF annual reports (2017-2022)
  - Opens Nautilus at Teaching_Grants folder so the agent can see the PDFs
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_stats_table_009'
GRANTS_DIR = f'{WORKDIR}/Documents/Teaching_Grants'


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


def create_pdf_report(filepath, year, applications, awards):
    """Create a realistic annual report PDF for a teaching grant program."""
    from fpdf import FPDF

    award_rate = (awards / applications) * 100
    total_funding = awards * 8500

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title block
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(31, 73, 125)
    pdf.cell(0, 12, "Westbrook University", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 9, "Office of Teaching Excellence", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(0, 9, "Annual Teaching Grant Program", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Annual Report {year}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(4)

    # Divider
    pdf.set_draw_color(31, 73, 125)
    pdf.set_line_width(0.8)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    # Executive Summary
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(31, 73, 125)
    pdf.cell(0, 8, "Executive Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 0, 0)

    summaries = {
        2017: (
            "In fiscal year 2017, the Teaching Grant Program received 342 applications "
            "from faculty across all schools and departments. Following rigorous peer "
            "review, 89 grants were awarded, supporting innovative curriculum development, "
            "technology integration, and student engagement initiatives. The program fosters "
            "a culture of teaching excellence and evidence-based pedagogical practice."
        ),
        2018: (
            "The 2018 grant cycle saw a notable increase in applications over the prior year. "
            "A total of 401 proposals were submitted, of which 98 were selected for funding "
            "after review by interdisciplinary panels. Funded projects spanned active learning "
            "redesigns, inclusive assessment strategies, and digital tool adoptions."
        ),
        2019: (
            "Fiscal year 2019 maintained strong faculty participation with 387 applications "
            "submitted to the Teaching Grant Program. The review panels selected 103 projects "
            "for funding, the highest award count in program history at that time. Notable "
            "themes included interdisciplinary course redesign and universal design for learning."
        ),
        2020: (
            "The 2020 grant cycle was impacted by the global public health emergency, "
            "requiring rapid pivots to remote and hybrid instruction. Despite challenges, "
            "312 faculty members submitted applications. The committee awarded 74 grants, "
            "prioritizing projects addressing remote learning and equitable access to resources."
        ),
        2021: (
            "Academic year 2021 marked a strong recovery with 428 applications submitted, "
            "the highest in program history. As instruction transitioned back to in-person "
            "and hybrid modalities, faculty focused on integrating remote teaching lessons "
            "into permanent curricular improvements. The program awarded 115 grants."
        ),
        2022: (
            "In 2022, the Teaching Grant Program reached a record 456 applications, reflecting "
            "sustained growth in faculty commitment to teaching excellence. The review committee "
            "awarded 128 grants, the highest since program inception, supporting active learning, "
            "equity-centered pedagogy, and experiential education initiatives."
        ),
    }

    pdf.multi_cell(0, 7, summaries[year])
    pdf.ln(4)

    # Key Statistics
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(31, 73, 125)
    pdf.cell(0, 8, f"Grant Statistics - Academic Year {year}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # Table header
    pdf.set_fill_color(220, 230, 242)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(100, 9, "Metric", border=1, fill=True)
    pdf.cell(90, 9, "Value", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")

    # Table rows
    pdf.set_font("Helvetica", "", 11)
    rows = [
        ("Total Applications Received", f"{applications}"),
        ("Applications Awarded", f"{awards}"),
        ("Applications Not Funded", f"{applications - awards}"),
        ("Award Rate (%)", f"{award_rate:.2f}%"),
        ("Total Funding Disbursed", f"${total_funding:,}"),
        ("Average Grant Amount", "$8,500"),
    ]
    for i, (label, value) in enumerate(rows):
        if i % 2 == 0:
            pdf.set_fill_color(245, 248, 252)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.cell(100, 8, label, border=1, fill=True)
        pdf.cell(90, 8, value, border=1, fill=True, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(5)

    # Review Timeline
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(31, 73, 125)
    pdf.cell(0, 8, "Application and Review Timeline", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 0, 0)

    timeline = [
        (f"{year}-01-15", "Call for Proposals Opens"),
        (f"{year}-03-31", f"Application Deadline ({applications} total submissions)"),
        (f"{year}-05-15", "Peer Review Panel Convenes"),
        (f"{year}-06-30", f"Funding Decisions Announced ({awards} grants awarded)"),
        (f"{year}-07-15", "Grant Agreements Executed"),
        (f"{year}-09-01", "Project Activities Begin"),
        (f"{year}-12-31", "Year-End Progress Reports Due"),
    ]
    for date, event in timeline:
        pdf.cell(35, 7, date, border="B")
        pdf.cell(0, 7, event, border="B", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(5)

    # Footer
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(
        0, 6,
        f"Office of Academic Development | {year} Annual Report | Confidential",
        new_x="LMARGIN", new_y="NEXT", align="C"
    )

    pdf.output(filepath)


def create_pdfs():
    """Create 6 realistic annual report PDFs for 2017-2022."""
    os.makedirs(GRANTS_DIR, exist_ok=True)

    yearly_data = [
        {"year": 2017, "applications": 342, "awards": 89},
        {"year": 2018, "applications": 401, "awards": 98},
        {"year": 2019, "applications": 387, "awards": 103},
        {"year": 2020, "applications": 312, "awards": 74},
        {"year": 2021, "applications": 428, "awards": 115},
        {"year": 2022, "applications": 456, "awards": 128},
    ]

    for entry in yearly_data:
        year = entry["year"]
        filepath = os.path.join(GRANTS_DIR, f"annual_report_{year}.pdf")
        create_pdf_report(
            filepath=filepath,
            year=year,
            applications=entry["applications"],
            awards=entry["awards"],
        )
        size = os.path.getsize(filepath)
        print(f"Created: {filepath} ({size} bytes)")


def create_initial():
    # 1. Create PDF files
    create_pdfs()

    # 2. List files created
    files = sorted(os.listdir(GRANTS_DIR))
    print(f"\nFiles in {GRANTS_DIR}:")
    for f in files:
        size = os.path.getsize(os.path.join(GRANTS_DIR, f))
        print(f"  {f}  ({size} bytes)")

    # 3. GUI-ready startup: open Nautilus at the Teaching_Grants folder
    launch_gui(f'nautilus "{GRANTS_DIR}"', delay_sec=2.0)
    print(f'\nGUI_READY: Nautilus opened at {GRANTS_DIR} with DISPLAY=:0')


create_initial()
