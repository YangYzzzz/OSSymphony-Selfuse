"""
Initial Setup: HK University Grant Data in PDF Reports
Task ID: osworld_multi_apps_ecs_multi_report_012
Domain: libreoffice_calc (multi-app: PDF files + LibreOffice Calc)

Creates ~/Documents/HK_Grants/ with 4 PDF files (2020-2023) each containing
a table of HK university grant application and success data by category.
Opens Nautilus showing the HK_Grants folder.
"""

import os
import shlex
import subprocess
import time

# For PDF generation
from fpdf import FPDF

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_ecs_multi_report_012'
GRANTS_DIR = f'{WORKDIR}/Documents/HK_Grants'

# HK Universities
UNIVERSITIES = [
    'University of Hong Kong',
    'Hong Kong Univ. of Sci. and Tech.',
    'Chinese Univ. of Hong Kong',
    'Hong Kong Polytechnic Univ.',
    'City University of Hong Kong',
    'Hong Kong Baptist University',
]

# Grant categories
CATEGORIES = [
    'Innovation and Technology',
    'Research and Development',
    'Environmental Sustainability',
    'Digital Transformation',
    'Healthcare and Medicine',
]

# Grant data: {year: {university: {category: (applied, received)}}}
# Pass rates for Innovation and Technology (will be used by reward-gen):
# HKU:    2020=0.60, 2021=0.65, 2022=0.70, 2023=0.72
# HKUST:  2020=0.75, 2021=0.78, 2022=0.80, 2023=0.82
# CUHK:   2020=0.55, 2021=0.58, 2022=0.62, 2023=0.65
# PolyU:  2020=0.50, 2021=0.52, 2022=0.55, 2023=0.58
# CityU:  2020=0.45, 2021=0.48, 2022=0.52, 2023=0.55
# HKBU:   2020=0.40, 2021=0.42, 2022=0.45, 2023=0.48

GRANT_DATA = {
    2020: {
        'University of Hong Kong': {
            'Innovation and Technology':   (20, 12),
            'Research and Development':    (18, 11),
            'Environmental Sustainability':(12,  7),
            'Digital Transformation':      (10,  5),
            'Healthcare and Medicine':     (15,  9),
        },
        'Hong Kong Univ. of Sci. and Tech.': {
            'Innovation and Technology':   (24, 18),
            'Research and Development':    (20, 13),
            'Environmental Sustainability':(10,  6),
            'Digital Transformation':      (14,  8),
            'Healthcare and Medicine':     (12,  7),
        },
        'Chinese Univ. of Hong Kong': {
            'Innovation and Technology':   (20, 11),
            'Research and Development':    (16, 10),
            'Environmental Sustainability':(11,  6),
            'Digital Transformation':      ( 9,  4),
            'Healthcare and Medicine':     (14,  8),
        },
        'Hong Kong Polytechnic Univ.': {
            'Innovation and Technology':   (22, 11),
            'Research and Development':    (15,  8),
            'Environmental Sustainability':(13,  7),
            'Digital Transformation':      (12,  6),
            'Healthcare and Medicine':     (10,  5),
        },
        'City University of Hong Kong': {
            'Innovation and Technology':   (20,  9),
            'Research and Development':    (14,  7),
            'Environmental Sustainability':(10,  5),
            'Digital Transformation':      (11,  5),
            'Healthcare and Medicine':     ( 9,  4),
        },
        'Hong Kong Baptist University': {
            'Innovation and Technology':   (15,  6),
            'Research and Development':    (12,  6),
            'Environmental Sustainability':( 8,  4),
            'Digital Transformation':      ( 7,  3),
            'Healthcare and Medicine':     (11,  5),
        },
    },
    2021: {
        'University of Hong Kong': {
            'Innovation and Technology':   (20, 13),
            'Research and Development':    (19, 12),
            'Environmental Sustainability':(13,  8),
            'Digital Transformation':      (11,  6),
            'Healthcare and Medicine':     (16, 10),
        },
        'Hong Kong Univ. of Sci. and Tech.': {
            'Innovation and Technology':   (23, 18),
            'Research and Development':    (21, 14),
            'Environmental Sustainability':(11,  7),
            'Digital Transformation':      (15,  9),
            'Healthcare and Medicine':     (13,  8),
        },
        'Chinese Univ. of Hong Kong': {
            'Innovation and Technology':   (19, 11),
            'Research and Development':    (17, 11),
            'Environmental Sustainability':(12,  7),
            'Digital Transformation':      (10,  5),
            'Healthcare and Medicine':     (15,  9),
        },
        'Hong Kong Polytechnic Univ.': {
            'Innovation and Technology':   (21, 11),
            'Research and Development':    (16,  9),
            'Environmental Sustainability':(14,  8),
            'Digital Transformation':      (13,  7),
            'Healthcare and Medicine':     (11,  6),
        },
        'City University of Hong Kong': {
            'Innovation and Technology':   (21, 10),
            'Research and Development':    (15,  8),
            'Environmental Sustainability':(11,  6),
            'Digital Transformation':      (12,  6),
            'Healthcare and Medicine':     (10,  5),
        },
        'Hong Kong Baptist University': {
            'Innovation and Technology':   (14,  6),  # ~0.43 rounds to 0.43
            'Research and Development':    (13,  7),
            'Environmental Sustainability':( 9,  5),
            'Digital Transformation':      ( 8,  4),
            'Healthcare and Medicine':     (12,  6),
        },
    },
    2022: {
        'University of Hong Kong': {
            'Innovation and Technology':   (20, 14),
            'Research and Development':    (20, 13),
            'Environmental Sustainability':(14,  9),
            'Digital Transformation':      (12,  7),
            'Healthcare and Medicine':     (17, 11),
        },
        'Hong Kong Univ. of Sci. and Tech.': {
            'Innovation and Technology':   (25, 20),
            'Research and Development':    (22, 15),
            'Environmental Sustainability':(12,  8),
            'Digital Transformation':      (16, 10),
            'Healthcare and Medicine':     (14,  9),
        },
        'Chinese Univ. of Hong Kong': {
            'Innovation and Technology':   (21, 13),
            'Research and Development':    (18, 12),
            'Environmental Sustainability':(13,  8),
            'Digital Transformation':      (11,  6),
            'Healthcare and Medicine':     (16, 10),
        },
        'Hong Kong Polytechnic Univ.': {
            'Innovation and Technology':   (20, 11),
            'Research and Development':    (17, 10),
            'Environmental Sustainability':(15,  9),
            'Digital Transformation':      (14,  8),
            'Healthcare and Medicine':     (12,  7),
        },
        'City University of Hong Kong': {
            'Innovation and Technology':   (21, 11),  # ~0.52
            'Research and Development':    (16,  9),
            'Environmental Sustainability':(12,  7),
            'Digital Transformation':      (13,  7),
            'Healthcare and Medicine':     (11,  6),
        },
        'Hong Kong Baptist University': {
            'Innovation and Technology':   (20,  9),
            'Research and Development':    (14,  8),
            'Environmental Sustainability':(10,  6),
            'Digital Transformation':      ( 9,  5),
            'Healthcare and Medicine':     (13,  7),
        },
    },
    2023: {
        'University of Hong Kong': {
            'Innovation and Technology':   (25, 18),
            'Research and Development':    (22, 15),
            'Environmental Sustainability':(15, 10),
            'Digital Transformation':      (14,  8),
            'Healthcare and Medicine':     (18, 12),
        },
        'Hong Kong Univ. of Sci. and Tech.': {
            'Innovation and Technology':   (28, 23),  # ~0.82
            'Research and Development':    (24, 17),
            'Environmental Sustainability':(13,  9),
            'Digital Transformation':      (18, 12),
            'Healthcare and Medicine':     (15, 10),
        },
        'Chinese Univ. of Hong Kong': {
            'Innovation and Technology':   (20, 13),
            'Research and Development':    (19, 13),
            'Environmental Sustainability':(14,  9),
            'Digital Transformation':      (12,  7),
            'Healthcare and Medicine':     (17, 11),
        },
        'Hong Kong Polytechnic Univ.': {
            'Innovation and Technology':   (24, 14),  # ~0.58
            'Research and Development':    (18, 11),
            'Environmental Sustainability':(16, 10),
            'Digital Transformation':      (15,  9),
            'Healthcare and Medicine':     (13,  8),
        },
        'City University of Hong Kong': {
            'Innovation and Technology':   (20, 11),
            'Research and Development':    (17, 10),
            'Environmental Sustainability':(13,  8),
            'Digital Transformation':      (14,  8),
            'Healthcare and Medicine':     (12,  7),
        },
        'Hong Kong Baptist University': {
            'Innovation and Technology':   (25, 12),
            'Research and Development':    (15,  9),
            'Environmental Sustainability':(11,  7),
            'Digital Transformation':      (10,  6),
            'Healthcare and Medicine':     (14,  8),
        },
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


def create_pdf_for_year(year: int) -> str:
    """Create a PDF report for the given year with HK university grant data."""
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, f'Hong Kong University Grant Funding Report {year}', ln=True, align='C')
    pdf.ln(5)

    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 8, 'Annual Summary of Grant Applications and Awards by Category', ln=True, align='C')
    pdf.ln(8)

    year_data = GRANT_DATA[year]

    for category in CATEGORIES:
        # Category header
        pdf.set_font('Helvetica', 'B', 13)
        pdf.set_fill_color(220, 230, 242)
        pdf.cell(0, 9, f'Category: {category}', ln=True, fill=True)
        pdf.ln(2)

        # Table header
        pdf.set_font('Helvetica', 'B', 10)
        col_widths = [75, 35, 35, 35]
        headers = ['University', 'Applied', 'Received', 'Pass Rate']
        for i, h in enumerate(headers):
            pdf.cell(col_widths[i], 8, h, border=1, align='C')
        pdf.ln()

        # Table rows
        pdf.set_font('Helvetica', '', 10)
        for uni in UNIVERSITIES:
            applied, received = year_data[uni][category]
            pass_rate = received / applied
            row = [uni, str(applied), str(received), f'{pass_rate:.2%}']
            fills = [False, False, False, False]
            for i, val in enumerate(row):
                align = 'L' if i == 0 else 'C'
                pdf.cell(col_widths[i], 7, val, border=1, align=align, fill=fills[i])
            pdf.ln()

        pdf.ln(5)

    # Footer
    pdf.set_y(-20)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.cell(0, 5, f'Hong Kong Research Grants Council - Annual Report {year}', align='C')

    output_path = f'{GRANTS_DIR}/{year}.pdf'
    pdf.output(output_path)
    return output_path


def create_initial():
    # Create directory structure
    os.makedirs(GRANTS_DIR, exist_ok=True)
    print(f'Created directory: {GRANTS_DIR}')

    # Generate PDF for each year
    for year in [2020, 2021, 2022, 2023]:
        path = create_pdf_for_year(year)
        print(f'Created PDF: {path}')

    # GUI-ready startup: open Nautilus showing HK_Grants folder + LibreOffice Calc
    launch_gui(f'nautilus "{GRANTS_DIR}"', delay_sec=2.0)
    launch_gui('libreoffice --calc', delay_sec=2.0)
    print('GUI_READY: launched Nautilus and LibreOffice Calc with DISPLAY=:0')


create_initial()
