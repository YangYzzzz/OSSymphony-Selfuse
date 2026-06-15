"""
Initial Setup: Fellowship grant pass rates across science disciplines
Task ID: osworld_multi_apps_ecs_multi_report_006
Domain: multi_apps (PDF + LibreOffice Calc)

Creates:
  - ~/Documents/Fellowships/ directory with 5 annual PDF reports (2019-2023)
  - Each PDF contains applications and awards by discipline
  - Opens Nautilus showing ~/Documents/Fellowships for the agent to work from
  - Does NOT create the output file (fellowship_by_discipline.xlsx)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
FELLOWSHIP_DIR = f'{WORKDIR}/Documents/Fellowships'

# Fellowship data: year -> discipline -> (applications, awards)
# Pass rate = awards / applications
FELLOWSHIP_DATA = {
    2019: {
        'Biology':         (124, 47),
        'Chemistry':       (98,  36),
        'Physics':         (87,  31),
        'Computer Science':(112, 45),
        'Mathematics':     (76,  26),
    },
    2020: {
        'Biology':         (131, 52),
        'Chemistry':       (103, 40),
        'Physics':         (91,  34),
        'Computer Science':(128, 54),
        'Mathematics':     (82,  29),
    },
    2021: {
        'Biology':         (118, 46),
        'Chemistry':       (95,  38),
        'Physics':         (84,  33),
        'Computer Science':(143, 62),
        'Mathematics':     (79,  28),
    },
    2022: {
        'Biology':         (126, 51),
        'Chemistry':       (107, 44),
        'Physics':         (89,  36),
        'Computer Science':(157, 70),
        'Mathematics':     (85,  32),
    },
    2023: {
        'Biology':         (135, 56),
        'Chemistry':       (112, 47),
        'Physics':         (93,  39),
        'Computer Science':(168, 78),
        'Mathematics':     (91,  35),
    },
}


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch a GUI app on the VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_fellowship_pdfs():
    """Create annual fellowship report PDFs in ~/Documents/Fellowships/."""
    from fpdf import FPDF

    os.makedirs(FELLOWSHIP_DIR, exist_ok=True)

    disciplines = ['Biology', 'Chemistry', 'Physics', 'Computer Science', 'Mathematics']

    for year, disc_data in FELLOWSHIP_DATA.items():
        pdf = FPDF()
        pdf.add_page()

        # Title
        pdf.set_font('Helvetica', 'B', 18)
        pdf.cell(0, 12, f'Annual Fellowship Grant Report {year}', align='C', new_x='LMARGIN', new_y='NEXT')
        pdf.ln(4)

        # Subtitle
        pdf.set_font('Helvetica', '', 11)
        pdf.cell(0, 8, 'National Science Foundation - Fellowship Programs Division', align='C', new_x='LMARGIN', new_y='NEXT')
        pdf.ln(8)

        # Section header
        pdf.set_font('Helvetica', 'B', 13)
        pdf.cell(0, 8, 'Fellowship Applications and Awards by Discipline', new_x='LMARGIN', new_y='NEXT')
        pdf.ln(4)

        # Table header
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(70, 8, 'Discipline', border=1, fill=True)
        pdf.cell(40, 8, 'Applications', border=1, fill=True, align='C')
        pdf.cell(40, 8, 'Awards', border=1, fill=True, align='C')
        pdf.cell(40, 8, 'Pass Rate (%)', border=1, fill=True, align='C', new_x='LMARGIN', new_y='NEXT')

        # Data rows
        pdf.set_font('Helvetica', '', 11)
        fill = False
        for disc in disciplines:
            apps, awards = disc_data[disc]
            rate = awards / apps * 100
            pdf.set_fill_color(235, 245, 255) if fill else pdf.set_fill_color(255, 255, 255)
            pdf.cell(70, 8, disc, border=1, fill=True)
            pdf.cell(40, 8, str(apps), border=1, fill=True, align='C')
            pdf.cell(40, 8, str(awards), border=1, fill=True, align='C')
            pdf.cell(40, 8, f'{rate:.2f}%', border=1, fill=True, align='C', new_x='LMARGIN', new_y='NEXT')
            fill = not fill

        pdf.ln(8)

        # Totals row
        total_apps = sum(v[0] for v in disc_data.values())
        total_awards = sum(v[1] for v in disc_data.values())
        total_rate = total_awards / total_apps * 100
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_fill_color(180, 210, 240)
        pdf.cell(70, 8, 'TOTAL', border=1, fill=True)
        pdf.cell(40, 8, str(total_apps), border=1, fill=True, align='C')
        pdf.cell(40, 8, str(total_awards), border=1, fill=True, align='C')
        pdf.cell(40, 8, f'{total_rate:.2f}%', border=1, fill=True, align='C', new_x='LMARGIN', new_y='NEXT')

        pdf.ln(10)

        # Summary note
        pdf.set_font('Helvetica', 'I', 10)
        pdf.multi_cell(0, 6,
            f'This report covers fellowship grant applications submitted during the {year} '
            'academic year. Pass rate is calculated as the number of awards divided by the '
            'total number of applications received in each discipline.'
        )

        # Save
        out_path = os.path.join(FELLOWSHIP_DIR, f'fellowship_{year}.pdf')
        pdf.output(out_path)
        print(f'  Created: {out_path}')


def main():
    print('Creating fellowship PDF reports...')
    create_fellowship_pdfs()

    # Ensure Desktop exists (it should, but just in case)
    os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)

    # Make sure fellowship_by_discipline.xlsx does NOT exist (task result should not pre-exist)
    target = f'{WORKDIR}/Desktop/fellowship_by_discipline.xlsx'
    if os.path.exists(target):
        os.remove(target)
        print(f'Removed pre-existing target file: {target}')

    print('All fellowship PDFs created.')
    print(f'Directory: {FELLOWSHIP_DIR}')
    print()

    # GUI-ready startup: open Nautilus showing the Fellowships directory
    launch_gui(f'nautilus "{FELLOWSHIP_DIR}"', delay_sec=1.5)
    print(f'GUI_READY: Nautilus opened at {FELLOWSHIP_DIR} with DISPLAY=:0')


main()
