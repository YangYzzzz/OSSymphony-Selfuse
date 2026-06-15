"""
Initial Setup: EU Horizon Europe Marie Curie Fellowship Statistics PDFs
Task ID: osworld_multi_apps_pdf_stats_table_008
Domain: libreoffice_calc (multi-app: PDF files + Nautilus)

Creates 5 PDF reports in ~/Documents/Horizon/ directory, one per year (2020-2024),
each containing Marie Curie fellowship application and selection statistics.
Opens Nautilus showing the Horizon directory.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_stats_table_008'
HORIZON_DIR = f'{WORKDIR}/Documents/Horizon'

# Realistic Marie Curie Individual Fellowship / Postdoctoral Fellowship statistics
# Based on Horizon 2020 and Horizon Europe programme data patterns
YEAR_DATA = {
    2020: {
        'applications': 11185,
        'selected': 1610,
        'budget_meur': 358.2,
        'countries': 45,
        'note': 'Horizon 2020 - Marie Sklodowska-Curie Actions Individual Fellowships'
    },
    2021: {
        'applications': 8880,
        'selected': 1270,
        'budget_meur': 295.7,
        'countries': 47,
        'note': 'Horizon Europe - Marie Sklodowska-Curie Actions Postdoctoral Fellowships (PF) - first call'
    },
    2022: {
        'applications': 9614,
        'selected': 1437,
        'budget_meur': 312.4,
        'countries': 48,
        'note': 'Horizon Europe - Marie Sklodowska-Curie Actions Postdoctoral Fellowships (PF)'
    },
    2023: {
        'applications': 10342,
        'selected': 1523,
        'budget_meur': 329.8,
        'countries': 49,
        'note': 'Horizon Europe - Marie Sklodowska-Curie Actions Postdoctoral Fellowships (PF)'
    },
    2024: {
        'applications': 10891,
        'selected': 1598,
        'budget_meur': 347.5,
        'countries': 50,
        'note': 'Horizon Europe - Marie Sklodowska-Curie Actions Postdoctoral Fellowships (PF)'
    },
}


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


def create_pdf_report(year: int, data: dict, output_path: str):
    """Create a PDF report for a given year with Marie Curie fellowship statistics."""
    try:
        from fpdf import FPDF
    except ImportError:
        subprocess.run(['pip3', 'install', 'fpdf2'], check=True)
        from fpdf import FPDF

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title section
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_fill_color(0, 51, 153)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 15, f'EU Horizon Europe', new_x='LMARGIN', new_y='NEXT', align='C', fill=True)

    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 12, f'Marie Sklodowska-Curie Actions', new_x='LMARGIN', new_y='NEXT', align='C', fill=True)

    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, f'Fellowship Success Rate Report {year}', new_x='LMARGIN', new_y='NEXT', align='C', fill=True)
    pdf.ln(5)

    # Reset colors
    pdf.set_text_color(0, 0, 0)

    # Programme note
    pdf.set_font('Helvetica', 'I', 10)
    pdf.set_fill_color(230, 230, 250)
    pdf.cell(0, 8, data['note'], new_x='LMARGIN', new_y='NEXT', align='C', fill=True)
    pdf.ln(8)

    # Introduction paragraph
    pdf.set_font('Helvetica', '', 11)
    intro_text = (
        f"This report presents the official statistics for Marie Sklodowska-Curie Actions "
        f"(MSCA) fellowship applications received and evaluated during the {year} call period. "
        f"The data covers proposals submitted by researchers from {data['countries']} participating "
        f"countries across the European Research Area and associated nations."
    )
    pdf.multi_cell(0, 6, intro_text)
    pdf.ln(6)

    # Key Statistics section header
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_fill_color(0, 51, 153)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 9, f'Key Statistics - Call Year {year}', new_x='LMARGIN', new_y='NEXT', align='L', fill=True)
    pdf.ln(4)
    pdf.set_text_color(0, 0, 0)

    # Statistics table
    applications = data['applications']
    selected = data['selected']
    rate = (selected / applications) * 100

    # Table header
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_fill_color(200, 210, 240)
    pdf.cell(90, 10, 'Indicator', border=1, fill=True)
    pdf.cell(90, 10, 'Value', border=1, fill=True, new_x='LMARGIN', new_y='NEXT')

    # Table rows
    pdf.set_font('Helvetica', '', 11)
    rows = [
        ('Call Year', str(year)),
        ('Total Applications Submitted', f'{applications:,}'),
        ('Proposals Selected for Funding', f'{selected:,}'),
        ('Selection Rate (%)', f'{rate:.2f}%'),
        ('Total Budget (M EUR)', f'{data["budget_meur"]:.1f}'),
        ('Participating Countries', str(data['countries'])),
    ]

    fill = False
    for label, value in rows:
        pdf.set_fill_color(245, 245, 245) if fill else pdf.set_fill_color(255, 255, 255)
        pdf.cell(90, 9, label, border=1, fill=True)
        pdf.cell(90, 9, value, border=1, fill=True, new_x='LMARGIN', new_y='NEXT')
        fill = not fill

    pdf.ln(8)

    # Application breakdown section
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_fill_color(0, 51, 153)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 9, 'Application Breakdown by Fellowship Type', new_x='LMARGIN', new_y='NEXT', align='L', fill=True)
    pdf.ln(4)
    pdf.set_text_color(0, 0, 0)

    # European and Global Fellowships breakdown
    eu_apps = int(applications * 0.62)
    global_apps = applications - eu_apps
    eu_selected = int(selected * 0.65)
    global_selected = selected - eu_selected

    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_fill_color(200, 210, 240)
    pdf.cell(70, 10, 'Fellowship Type', border=1, fill=True)
    pdf.cell(55, 10, 'Applications', border=1, fill=True)
    pdf.cell(55, 10, 'Selected', border=1, fill=True, new_x='LMARGIN', new_y='NEXT')

    pdf.set_font('Helvetica', '', 11)
    for ftype, apps, sel in [
        ('European Fellowships', f'{eu_apps:,}', f'{eu_selected:,}'),
        ('Global Fellowships', f'{global_apps:,}', f'{global_selected:,}'),
        ('Total', f'{applications:,}', f'{selected:,}'),
    ]:
        fill_color = (230, 230, 250) if ftype == 'Total' else (255, 255, 255)
        pdf.set_fill_color(*fill_color)
        bold = ftype == 'Total'
        if bold:
            pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(70, 9, ftype, border=1, fill=True)
        pdf.cell(55, 9, apps, border=1, fill=True)
        pdf.cell(55, 9, sel, border=1, fill=True, new_x='LMARGIN', new_y='NEXT')
        if bold:
            pdf.set_font('Helvetica', '', 11)

    pdf.ln(8)

    # Evaluation process section
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_fill_color(0, 51, 153)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 9, 'Evaluation Process Summary', new_x='LMARGIN', new_y='NEXT', align='L', fill=True)
    pdf.ln(4)
    pdf.set_text_color(0, 0, 0)

    pdf.set_font('Helvetica', '', 11)
    eval_text = (
        f"All {applications:,} proposals submitted for the {year} call were evaluated by "
        f"independent expert reviewers following the standard MSCA evaluation criteria: "
        f"Excellence, Impact, and Implementation. Proposals achieving the threshold score "
        f"were ranked and funded within the available budget envelope of EUR {data['budget_meur']:.1f} million. "
        f"A total of {selected:,} projects were awarded grants, representing a selection rate "
        f"of {rate:.2f}%."
    )
    pdf.multi_cell(0, 6, eval_text)
    pdf.ln(6)

    # Footer
    pdf.set_y(-30)
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f'European Commission - DG Research & Innovation - MSCA Statistics Report {year}',
             new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.cell(0, 6, 'Data source: Participant Portal - CORDIS - Official EU Research Information System',
             new_x='LMARGIN', new_y='NEXT', align='C')

    pdf.output(output_path)
    print(f'  Created PDF: {output_path}')


def create_initial():
    # Create the Documents/Horizon directory
    os.makedirs(HORIZON_DIR, exist_ok=True)
    print(f'Created directory: {HORIZON_DIR}')

    # Create Desktop directory (may already exist)
    desktop_dir = f'{WORKDIR}/Desktop'
    os.makedirs(desktop_dir, exist_ok=True)

    # Create one PDF per year
    for year, data in YEAR_DATA.items():
        pdf_path = os.path.join(HORIZON_DIR, f'{year}.pdf')
        create_pdf_report(year, data, pdf_path)

    print(f'All 5 PDF files created in {HORIZON_DIR}')

    # Verify files exist
    for year in YEAR_DATA.keys():
        path = os.path.join(HORIZON_DIR, f'{year}.pdf')
        assert os.path.exists(path), f'Missing: {path}'
    print('File verification passed.')

    # GUI-ready startup: Open Nautilus showing the Horizon directory
    launch_gui(f'nautilus "{HORIZON_DIR}"', delay_sec=2.0)
    print(f'GUI_READY: launched Nautilus at {HORIZON_DIR} with DISPLAY=:0')


create_initial()
