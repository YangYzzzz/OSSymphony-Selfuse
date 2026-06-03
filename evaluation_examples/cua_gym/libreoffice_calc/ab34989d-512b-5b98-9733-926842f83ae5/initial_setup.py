"""
Initial Setup: Create survey_results.pdf with 30 participant ratings and open it
Task ID: pdf_cross_041
Domain: pdf + libreoffice_calc (cross-app)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user/Documents'
TASK_ID = 'pdf_cross_041'
PDF_OUTPUT = f'{WORKDIR}/survey_results.pdf'

# Fixed survey data: 30 participants x 5 categories (Usability, Performance, Design, Support, Value)
# Ratings are integers 1-5
SURVEY_DATA = [
    # Participant, Usability, Performance, Design, Support, Value
    [1,  4, 3, 5, 4, 3],
    [2,  5, 4, 4, 3, 4],
    [3,  3, 3, 3, 4, 5],
    [4,  4, 5, 4, 5, 4],
    [5,  5, 4, 5, 3, 3],
    [6,  2, 3, 3, 4, 4],
    [7,  4, 4, 4, 4, 4],
    [8,  3, 2, 4, 3, 5],
    [9,  5, 5, 5, 5, 5],
    [10, 4, 4, 3, 4, 3],
    [11, 3, 3, 4, 2, 4],
    [12, 4, 5, 5, 4, 4],
    [13, 5, 4, 4, 3, 3],
    [14, 2, 3, 3, 4, 4],
    [15, 4, 4, 4, 5, 5],
    [16, 3, 3, 3, 3, 3],
    [17, 5, 5, 5, 4, 4],
    [18, 4, 3, 4, 3, 4],
    [19, 3, 4, 3, 4, 3],
    [20, 4, 4, 4, 4, 4],
    [21, 5, 3, 5, 5, 3],
    [22, 3, 3, 3, 3, 4],
    [23, 4, 4, 4, 4, 5],
    [24, 5, 5, 4, 3, 4],
    [25, 2, 3, 3, 4, 3],
    [26, 4, 4, 5, 4, 4],
    [27, 3, 3, 3, 3, 3],
    [28, 5, 4, 4, 5, 5],
    [29, 4, 3, 4, 4, 4],
    [30, 3, 4, 3, 3, 4],
]

CATEGORIES = ['Usability', 'Performance', 'Design', 'Support', 'Value']


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


def create_survey_pdf():
    """Create a 2-page PDF with survey data table using reportlab."""
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.colors import black, white, HexColor
    from reportlab.lib.units import inch

    # Ensure Documents directory exists
    os.makedirs(WORKDIR, exist_ok=True)

    doc = SimpleDocTemplate(
        PDF_OUTPUT,
        pagesize=A4,
        leftMargin=72, rightMargin=72, topMargin=72, bottomMargin=72
    )

    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'SurveyTitle',
        parent=styles['Title'],
        fontSize=18,
        spaceAfter=12,
    )
    story.append(Paragraph("User Satisfaction Survey Results", title_style))

    # Subtitle
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=16,
    )
    story.append(Paragraph(
        "Survey of 30 participants rating 5 categories on a 1-5 scale.<br/>"
        "Categories: Usability, Performance, Design, Support, Value",
        subtitle_style
    ))

    story.append(Spacer(1, 10))

    # Table header
    header = ['Participant', 'Usability', 'Performance', 'Design', 'Support', 'Value']

    # Build table data: header + all 30 rows
    table_data = [header]
    for row in SURVEY_DATA:
        table_data.append([str(v) for v in row])

    # Split into two pages: first 15 rows on page 1, next 15 on page 2
    # Page 1: rows 1-15
    page1_data = [header] + [[str(v) for v in row] for row in SURVEY_DATA[:15]]
    page2_data = [header] + [[str(v) for v in row] for row in SURVEY_DATA[15:]]

    col_widths = [70, 75, 80, 65, 65, 60]

    header_bg = HexColor('#2E4A7A')
    alt_bg = HexColor('#F0F4FA')

    def make_table_style(data):
        style = TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), header_bg),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.5, black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ])
        # Alternating row colors
        for i in range(1, len(data)):
            if i % 2 == 0:
                style.add('BACKGROUND', (0, i), (-1, i), alt_bg)
        return style

    # Page 1 table
    t1 = Table(page1_data, colWidths=col_widths)
    t1.setStyle(make_table_style(page1_data))
    story.append(t1)

    # Page break and page 2
    from reportlab.platypus import PageBreak
    story.append(PageBreak())

    story.append(Paragraph("User Satisfaction Survey Results (Continued)", title_style))
    story.append(Paragraph("Participants 16-30", subtitle_style))
    story.append(Spacer(1, 10))

    t2 = Table(page2_data, colWidths=col_widths)
    t2.setStyle(make_table_style(page2_data))
    story.append(t2)

    doc.build(story)
    print(f'Survey PDF created: {PDF_OUTPUT}')


def main():
    create_survey_pdf()

    # GUI-ready startup: Open the PDF in evince for the agent to read data from
    launch_gui(f'evince "{PDF_OUTPUT}"', delay_sec=2.0)

    # Also open LibreOffice Calc with a new spreadsheet so agent can start entering data
    # The agent needs to create ~/Documents/survey_analysis.ods
    launch_gui('libreoffice --calc', delay_sec=2.0)

    print('GUI_READY: launched evince (PDF) and LibreOffice Calc with DISPLAY=:0')


main()
