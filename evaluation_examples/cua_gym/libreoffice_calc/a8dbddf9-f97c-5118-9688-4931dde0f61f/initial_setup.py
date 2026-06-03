"""
Initial Setup: Create NIH R01 grant funding rate PDFs in ~/Documents/NIH/
Task ID: osworld_multi_apps_pdf_stats_table_003
Domain: multi_apps (PDF + libreoffice_calc)

Creates nih18.pdf through nih22.pdf in ~/Documents/NIH/, each containing
NIH R01 grant funding data for biomedical engineering.
Opens Nautilus showing ~/Documents/NIH.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_stats_table_003'
NIH_DIR = f'{WORKDIR}/Documents/NIH'

# Realistic NIH R01 Biomedical Engineering funding data by year
NIH_DATA = {
    2018: {'submitted': 4631, 'funded': 850},
    2019: {'submitted': 4892, 'funded': 891},
    2020: {'submitted': 5124, 'funded': 942},
    2021: {'submitted': 5380, 'funded': 991},
    2022: {'submitted': 5612, 'funded': 1018},
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


def create_pdf_for_year(year, data, output_path):
    """Create a realistic NIH R01 funding rate PDF report for a given year using reportlab."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT

    submitted = data['submitted']
    funded = data['funded']
    rate = round((funded / submitted) * 100, 2)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72, leftMargin=72,
        topMargin=72, bottomMargin=72
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=16,
        spaceAfter=6,
        alignment=TA_CENTER
    )
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=13,
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    body_style = styles['Normal']
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceBefore=12,
        spaceAfter=6
    )

    story = []

    # Title
    story.append(Paragraph('NIH R01 Grant Funding Report', title_style))
    story.append(Paragraph('Biomedical Engineering (NIBIB)', subtitle_style))
    story.append(Paragraph(f'Fiscal Year {year}', subtitle_style))
    story.append(Spacer(1, 0.2 * inch))

    # Introduction paragraph
    intro_text = (
        f"This report summarizes the R01 research project grant application and award data "
        f"for the National Institute of Biomedical Imaging and Bioengineering (NIBIB) "
        f"for fiscal year {year}. The data presented here reflects peer-reviewed research "
        f"applications submitted through standard R01 mechanisms and represents the "
        f"biomedical engineering portfolio."
    )
    story.append(Paragraph(intro_text, body_style))
    story.append(Spacer(1, 0.15 * inch))

    # Statistics table
    story.append(Paragraph('R01 Application and Award Statistics', heading_style))

    table_data = [
        ['Metric', 'Value', 'Notes'],
        ['Applications Submitted', f'{submitted:,}', 'Total R01 applications received'],
        ['Applications Funded', f'{funded:,}', 'Total R01 awards made'],
        ['Success Rate (%)', f'{rate:.2f}', 'Funded / Submitted x 100'],
        ['Average Award Duration', '4 years', 'Standard R01 project period'],
        ['Review Cycles per Year', '3', 'February, June, October'],
    ]

    table = Table(table_data, colWidths=[2.5 * inch, 1.5 * inch, 3.0 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4682B4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F0F8FF'), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.2 * inch))

    # Key findings
    story.append(Paragraph('Key Findings', heading_style))
    findings = [
        f'Total R01 applications received in FY{year}: {submitted:,}',
        f'Total R01 awards made in FY{year}: {funded:,}',
        f'Overall R01 success rate for FY{year}: {rate:.2f}%',
        'Biomedical engineering applications represent a growing segment of the NIH R01 portfolio.',
        'Peer review scores reflect high competition among qualified applicants.',
    ]
    for finding in findings:
        story.append(Paragraph(f'• {finding}', body_style))
    story.append(Spacer(1, 0.15 * inch))

    # Methodology note
    note_style = ParagraphStyle(
        'Note',
        parent=styles['Normal'],
        fontSize=8,
        fontName='Helvetica-Oblique',
        textColor=colors.grey
    )
    note_text = (
        "Note: Success rate is calculated as the number of funded applications divided by "
        "the total number of applications reviewed. "
        "Data sourced from NIH Research Portfolio Online Reporting Tools (RePORTER)."
    )
    story.append(Paragraph(note_text, note_style))

    doc.build(story)
    print(f'  Created: {output_path}')


def create_initial():
    # Ensure Documents/NIH directory exists
    os.makedirs(NIH_DIR, exist_ok=True)
    print(f'Directory ready: {NIH_DIR}')

    # Create PDF for each year
    print('Creating NIH R01 PDF reports...')
    for year, data in NIH_DATA.items():
        short_year = str(year)[2:]  # e.g., 2018 -> '18'
        pdf_path = os.path.join(NIH_DIR, f'nih{short_year}.pdf')
        create_pdf_for_year(year, data, pdf_path)

    print(f'All 5 PDF reports created in {NIH_DIR}')

    # Ensure Desktop exists
    desktop_dir = f'{WORKDIR}/Desktop'
    os.makedirs(desktop_dir, exist_ok=True)

    # Remove any leftover output file from previous runs (idempotent)
    output_xlsx = f'{desktop_dir}/NIH_R01_rates.xlsx'
    if os.path.exists(output_xlsx):
        os.remove(output_xlsx)
        print(f'Removed pre-existing output file: {output_xlsx}')

    # GUI-ready: Open Nautilus showing ~/Documents/NIH
    launch_gui(f'nautilus "{NIH_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched Nautilus showing ~/Documents/NIH with DISPLAY=:0')


create_initial()
