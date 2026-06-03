"""
Initial Setup: JSPS Kakenhi Kiban-A grant statistics PDF files in ~/Documents/JSPS/
Task ID: osworld_multi_apps_pdf_stats_table_013
Domain: multi_apps (PDF + libreoffice_calc)

Creates 5 PDF files (2019-2023) containing JSPS Kakenhi Kiban-A grant statistics.
Opens Nautilus to show ~/Documents/JSPS directory.
The agent must read the PDFs and create JSPS_KakenA_rates.xlsx manually.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_stats_table_013'
JSPS_DIR = f'{WORKDIR}/Documents/JSPS'

# Realistic JSPS Kakenhi Kiban-A (Scientific Research (A)) grant statistics
# These are plausible figures based on JSPS annual reports
GRANT_DATA = [
    {'year': 2019, 'applications': 2850, 'grants': 572},
    {'year': 2020, 'applications': 2780, 'grants': 548},
    {'year': 2021, 'applications': 2690, 'grants': 524},
    {'year': 2022, 'applications': 2730, 'grants': 539},
    {'year': 2023, 'applications': 2810, 'grants': 563},
]


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


def create_pdf_for_year(year: int, applications: int, grants: int):
    """Create a realistic JSPS Kakenhi Kiban-A statistics PDF for a given year."""
    from fpdf import FPDF

    pass_rate = round(grants / applications * 100, 2)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 12, f"JSPS Grants-in-Aid for Scientific Research", ln=True, align="C")
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"Kiban-A (Scientific Research (A)) Category", ln=True, align="C")
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"Fiscal Year {year} - Annual Statistics Report", ln=True, align="C")
    pdf.ln(8)

    # Horizontal rule
    pdf.set_draw_color(80, 80, 80)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(6)

    # Introduction
    pdf.set_font("Helvetica", "", 11)
    intro = (
        f"This report presents the official statistics for JSPS Grants-in-Aid "
        f"for Scientific Research (Kakenhi) under the Kiban-A category for fiscal year {year}. "
        f"The Kiban-A category supports large-scale research projects led by experienced researchers. "
        f"The following data reflects the results of the competitive review process conducted by the Japan Society "
        f"for the Promotion of Science."
    )
    pdf.multi_cell(0, 6, intro)
    pdf.ln(6)

    # Statistics Table Header
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, f"FY{year} Kiban-A Grant Application Results", ln=True)
    pdf.ln(3)

    # Table
    col_w = [80, 55, 55]
    pdf.set_fill_color(220, 230, 242)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(col_w[0], 9, "Category", border=1, fill=True)
    pdf.cell(col_w[1], 9, "Value", border=1, fill=True)
    pdf.cell(col_w[2], 9, "Notes", border=1, fill=True, ln=True)

    pdf.set_font("Helvetica", "", 11)
    rows = [
        ("Fiscal Year", str(year), "Japanese academic year"),
        ("Total Applications", f"{applications:,}", "Including new and continuation"),
        ("Total Grants Awarded", f"{grants:,}", "Funded projects"),
        ("Pass Rate (%)", f"{pass_rate:.2f}%", "Awards / Applications x 100"),
        ("Grant Category", "Kiban-A", "Scientific Research (A)"),
        ("Funding Agency", "JSPS", "Japan Society for the Promotion of Science"),
        ("Review Method", "Expert Panel", "Multi-stage peer review"),
        ("Max Grant Period", "3-5 years", "Per award"),
    ]
    fill = False
    for row in rows:
        pdf.set_fill_color(245, 248, 253) if fill else pdf.set_fill_color(255, 255, 255)
        pdf.cell(col_w[0], 8, row[0], border=1, fill=True)
        pdf.cell(col_w[1], 8, row[1], border=1, fill=True)
        pdf.cell(col_w[2], 8, row[2], border=1, fill=True, ln=True)
        fill = not fill

    pdf.ln(8)

    # Summary paragraph
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "Summary", ln=True)
    pdf.set_font("Helvetica", "", 11)
    summary = (
        f"In fiscal year {year}, the Kiban-A category received a total of {applications:,} applications "
        f"from research institutions across Japan. Following a rigorous competitive review process, "
        f"{grants:,} projects were selected for funding, yielding a pass rate of {pass_rate:.2f}%. "
        f"Funded projects will receive support for up to 3-5 years, enabling sustained research "
        f"activities in their respective scientific fields."
    )
    pdf.multi_cell(0, 6, summary)
    pdf.ln(5)

    # Footer note
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(
        0, 5,
        f"Source: Japan Society for the Promotion of Science (JSPS), Grants-in-Aid for Scientific Research "
        f"(Kakenhi) Statistics FY{year}. Published by JSPS Research Funding Division."
    )

    output_path = os.path.join(JSPS_DIR, f'JSPS_KakenA_{year}.pdf')
    pdf.output(output_path)
    print(f'  Created: {output_path}')


def create_initial():
    # Ensure Documents/JSPS directory exists
    os.makedirs(JSPS_DIR, exist_ok=True)
    print(f'Directory ensured: {JSPS_DIR}')

    # Create PDF for each year
    print('Creating JSPS Kakenhi Kiban-A statistics PDFs...')
    for entry in GRANT_DATA:
        create_pdf_for_year(entry['year'], entry['applications'], entry['grants'])

    print(f'All 5 PDFs created in {JSPS_DIR}')

    # Ensure JSPS_KakenA_rates.xlsx does NOT exist (task requires creating it)
    target_xlsx = f'{WORKDIR}/JSPS_KakenA_rates.xlsx'
    if os.path.exists(target_xlsx):
        os.remove(target_xlsx)
        print(f'Removed pre-existing {target_xlsx} to ensure clean initial state')

    # GUI-ready startup: open Nautilus showing Documents/JSPS
    # (Task context: "Nautilus shows ~/Documents/JSPS with 5 PDF files")
    launch_gui(f'nautilus "{JSPS_DIR}"', delay_sec=2.0)
    # Also open LibreOffice Calc (blank) so agent can start the table
    launch_gui('libreoffice --calc', delay_sec=2.0)

    print('GUI_READY: launched Nautilus and LibreOffice Calc with DISPLAY=:0')


create_initial()
