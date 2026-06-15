"""
Initial Setup: DFG Emmy Noether Program statistics PDFs
Task ID: osworld_multi_apps_pdf_stats_table_014
Domain: libreoffice_calc (multi-app: PDF files + Nautilus + LibreOffice Calc)

Creates ~/Documents/DFG/ with 5 annual PDF files (2018-2022),
each containing DFG Emmy Noether Program statistics.
The agent will read the PDFs and create ~/DFG_Emmy_rates.xlsx.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_stats_table_014'
DFG_DIR = f'{WORKDIR}/Documents/DFG'

# DFG Emmy Noether data per year: (year, applications, approvals)
DFG_DATA = [
    (2018, 2341, 312),
    (2019, 2489, 334),
    (2020, 2256, 289),
    (2021, 2512, 348),
    (2022, 2678, 361),
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


def create_pdf_for_year(year, applications, approvals):
    """Create a DFG annual report PDF for a given year with Emmy Noether stats."""
    try:
        from fpdf import FPDF
    except ImportError:
        subprocess.run(['pip3', 'install', 'fpdf2'], check=True, capture_output=True)
        from fpdf import FPDF

    approval_rate = round(approvals / applications * 100, 2)

    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 12, f'DFG Annual Report {year}', new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.ln(4)

    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, 'Emmy Noether Programme - Statistical Overview', new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.ln(6)

    # Introduction paragraph
    pdf.set_font('Helvetica', '', 11)
    intro = (
        f'This report summarizes the Emmy Noether Programme statistics for the year {year}. '
        'The Emmy Noether Programme of the Deutsche Forschungsgemeinschaft (DFG) enables '
        'outstanding young researchers to qualify for a university professorship by leading '
        'an independent junior research group for a period of six years.'
    )
    pdf.multi_cell(0, 7, intro)
    pdf.ln(6)

    # Section header
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Programme Statistics', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(3)

    # Stats table header
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_fill_color(200, 220, 255)
    col_widths = [80, 50, 50]
    headers = ['Category', 'Count', 'Percentage']
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 9, h, border=1, fill=True)
    pdf.ln()

    # Stats table rows
    pdf.set_font('Helvetica', '', 11)
    pdf.set_fill_color(255, 255, 255)

    rows = [
        ('Applications submitted', str(applications), '100.00%'),
        ('Applications approved', str(approvals), f'{approval_rate:.2f}%'),
        ('Applications rejected', str(applications - approvals), f'{(100 - approval_rate):.2f}%'),
    ]
    for row in rows:
        for i, val in enumerate(row):
            pdf.cell(col_widths[i], 8, val, border=1)
        pdf.ln()

    pdf.ln(6)

    # Additional context section
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Key Figures Summary', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(3)

    pdf.set_font('Helvetica', '', 11)
    summary_lines = [
        f'Total applications received in {year}: {applications}',
        f'Total approvals granted in {year}: {approvals}',
        f'Overall approval rate: {approval_rate:.2f}%',
        f'Average funding per approved project: approx. EUR 1.5 million over 6 years',
        f'Funding period covered: {year} to {year + 6}',
    ]
    for line in summary_lines:
        pdf.cell(0, 7, line, new_x='LMARGIN', new_y='NEXT')

    pdf.ln(6)

    # Disciplinary breakdown (fictional but realistic)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Distribution by Research Area', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(3)

    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_fill_color(200, 220, 255)
    area_col_widths = [100, 50, 50]
    area_headers = ['Research Area', 'Applications', 'Approvals']
    for i, h in enumerate(area_headers):
        pdf.cell(area_col_widths[i], 9, h, border=1, fill=True)
    pdf.ln()

    # Distribute applications among research areas realistically
    import math
    areas = [
        ('Natural Sciences', 0.31),
        ('Life Sciences', 0.27),
        ('Engineering Sciences', 0.22),
        ('Humanities and Social Sciences', 0.20),
    ]
    pdf.set_font('Helvetica', '', 11)
    for area_name, fraction in areas:
        area_apps = math.floor(applications * fraction)
        area_approvals = math.floor(approvals * fraction)
        pdf.cell(area_col_widths[0], 8, area_name, border=1)
        pdf.cell(area_col_widths[1], 8, str(area_apps), border=1)
        pdf.cell(area_col_widths[2], 8, str(area_approvals), border=1)
        pdf.ln()

    pdf.ln(8)

    # Footer note
    pdf.set_font('Helvetica', 'I', 9)
    pdf.multi_cell(0, 6,
        'Source: Deutsche Forschungsgemeinschaft (DFG), German Research Foundation. '
        'Annual Statistics Report. All figures are final and subject to DFG verification procedures.')

    out_path = f'{DFG_DIR}/DFG_Emmy_{year}.pdf'
    pdf.output(out_path)
    print(f'  Created: {out_path}  (applications={applications}, approvals={approvals}, rate={approval_rate:.2f}%)')


def create_initial():
    # Create DFG directory
    os.makedirs(DFG_DIR, exist_ok=True)
    print(f'DFG directory ready: {DFG_DIR}')

    # Ensure the output file does NOT exist yet (agent must create it)
    output_xlsx = f'{WORKDIR}/DFG_Emmy_rates.xlsx'
    if os.path.exists(output_xlsx):
        os.remove(output_xlsx)
        print(f'Removed pre-existing {output_xlsx}')

    # Create a PDF for each year
    print('Creating annual PDF reports...')
    for year, applications, approvals in DFG_DATA:
        create_pdf_for_year(year, applications, approvals)

    print(f'\nAll 5 PDF files created in {DFG_DIR}')

    # GUI-ready startup: open Nautilus showing the DFG folder,
    # then open LibreOffice Calc (blank) so the agent can start working
    print('\nLaunching GUI applications...')
    launch_gui(f'nautilus "{DFG_DIR}"', delay_sec=2.0)
    launch_gui('libreoffice --calc', delay_sec=2.0)
    print('GUI_READY: Nautilus (DFG folder) and LibreOffice Calc launched with DISPLAY=:0')


create_initial()
