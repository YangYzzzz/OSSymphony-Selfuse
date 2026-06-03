"""
Initial Setup: Insert a new section named 'Executive Summary' at the beginning of a report document.
Task ID: writer_fs_051
Domain: libreoffice_writer

Creates a report document starting with 'Introduction' heading followed by body text.
No sections are present - the agent needs to insert one.
Uses .odt format because the task requires named sections (Format > Sections),
which is an ODF-native feature not preserved in .docx format.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_051'
OUTPUT = f'{WORKDIR}/{TASK_ID}.odt'


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
    from odf.opendocument import OpenDocumentText
    from odf.text import P, H, List, ListItem
    from odf.table import Table, TableColumn, TableRow, TableCell
    from odf.style import Style, TextProperties, ParagraphProperties, \
        TableProperties, TableColumnProperties, TableCellProperties

    doc = OpenDocumentText()

    # --- Define styles ---
    # Title style
    title_style = Style(name="ReportTitle", family="paragraph")
    title_style.addElement(ParagraphProperties(textalign="center",
                                                marginbottom="0.3in",
                                                margintop="0.2in"))
    title_style.addElement(TextProperties(fontsize="26pt", fontweight="bold",
                                           color="#1F3864"))
    doc.automaticstyles.addElement(title_style)

    # Heading 1 style
    h1_style = Style(name="ReportH1", family="paragraph")
    h1_style.addElement(ParagraphProperties(margintop="0.25in",
                                             marginbottom="0.1in"))
    h1_style.addElement(TextProperties(fontsize="18pt", fontweight="bold",
                                        color="#2E74B5"))
    doc.automaticstyles.addElement(h1_style)

    # Heading 2 style
    h2_style = Style(name="ReportH2", family="paragraph")
    h2_style.addElement(ParagraphProperties(margintop="0.2in",
                                             marginbottom="0.08in"))
    h2_style.addElement(TextProperties(fontsize="14pt", fontweight="bold",
                                        color="#4472C4"))
    doc.automaticstyles.addElement(h2_style)

    # Body text style
    body_style = Style(name="ReportBody", family="paragraph")
    body_style.addElement(ParagraphProperties(marginbottom="0.08in",
                                               textalign="justify"))
    body_style.addElement(TextProperties(fontsize="11pt"))
    doc.automaticstyles.addElement(body_style)

    # Bold text style
    bold_style = Style(name="BoldText", family="text")
    bold_style.addElement(TextProperties(fontweight="bold"))
    doc.automaticstyles.addElement(bold_style)

    # Table cell style
    cell_style = Style(name="TableCell", family="table-cell")
    cell_style.addElement(TableCellProperties(
        padding="0.04in", border="0.5pt solid #000000"))
    doc.automaticstyles.addElement(cell_style)

    # Table column style
    col_style = Style(name="TableCol", family="table-column")
    col_style.addElement(TableColumnProperties(columnwidth="2.2in"))
    doc.automaticstyles.addElement(col_style)

    # --- Title ---
    doc.text.addElement(P(stylename=title_style,
                          text='Quarterly Performance Report'))

    # --- Introduction ---
    doc.text.addElement(H(outlinelevel=1, stylename=h1_style,
                          text='Introduction'))

    doc.text.addElement(P(stylename=body_style, text=(
        'This report provides a comprehensive overview of the company\'s performance '
        'during the third quarter of fiscal year 2025. The analysis covers key financial '
        'metrics, operational highlights, and strategic initiatives that shaped our '
        'business outcomes over the past three months.'
    )))

    doc.text.addElement(P(stylename=body_style, text=(
        'Our organization continued to navigate a dynamic market environment, '
        'characterized by evolving customer demands, competitive pressures, and '
        'macroeconomic uncertainties. Despite these challenges, the team demonstrated '
        'remarkable resilience and adaptability across all business units.'
    )))

    # --- Financial Overview ---
    doc.text.addElement(H(outlinelevel=1, stylename=h1_style,
                          text='Financial Overview'))

    doc.text.addElement(P(stylename=body_style, text=(
        'Total revenue for Q3 2025 reached $12.8 million, representing a 15% increase '
        'compared to the same period last year. Gross margins improved to 42.3%, driven '
        'by operational efficiencies and favorable product mix shifts. Operating expenses '
        'remained well-controlled at $4.2 million, reflecting disciplined cost management.'
    )))

    doc.text.addElement(P(stylename=body_style, text=(
        'The engineering division contributed $5.6 million in revenue, while the '
        'consulting services arm generated $4.1 million. Our emerging digital products '
        'segment showed promising growth, adding $3.1 million to the top line, a 28% '
        'year-over-year improvement.'
    )))

    # --- Key Performance Metrics ---
    doc.text.addElement(H(outlinelevel=2, stylename=h2_style,
                          text='Key Performance Metrics'))

    # Table
    table = Table(name="MetricsTable")
    for _ in range(3):
        table.addElement(TableColumn(stylename=col_style))

    from odf.text import Span

    # Header row
    header_data = ['Metric', 'Q3 2025', 'Q3 2024']
    tr = TableRow()
    for h_text in header_data:
        tc = TableCell(stylename=cell_style)
        p = P()
        span = Span(stylename=bold_style, text=h_text)
        p.addElement(span)
        tc.addElement(p)
        tr.addElement(tc)
    table.addElement(tr)

    # Data rows
    data = [
        ['Total Revenue', '$12.8M', '$11.1M'],
        ['Gross Margin', '42.3%', '39.8%'],
        ['Operating Expenses', '$4.2M', '$4.0M'],
        ['Net Income', '$1.9M', '$1.4M'],
        ['Employee Count', '347', '312'],
    ]
    for row_data in data:
        tr = TableRow()
        for val in row_data:
            tc = TableCell(stylename=cell_style)
            tc.addElement(P(text=val))
            tr.addElement(tc)
        table.addElement(tr)

    doc.text.addElement(table)

    # --- Operational Highlights ---
    doc.text.addElement(H(outlinelevel=1, stylename=h1_style,
                          text='Operational Highlights'))

    doc.text.addElement(P(stylename=body_style, text=(
        'Several strategic initiatives delivered meaningful results during the quarter:'
    )))

    bullets = [
        ('Successfully launched the CloudSync Pro platform, acquiring 1,200 enterprise '
         'customers within the first 60 days of availability.'),
        ('Completed the integration of Nextera Analytics acquisition, achieving $800K '
         'in annualized cost synergies ahead of the original timeline.'),
        ('Expanded our Asia-Pacific presence with new offices in Singapore and Sydney, '
         'supporting regional revenue growth of 22%.'),
        ('Achieved ISO 27001 certification across all data center operations, '
         'strengthening our security posture and customer trust.'),
    ]

    bullet_list = List()
    for b_text in bullets:
        li = ListItem()
        li.addElement(P(text=b_text))
        bullet_list.addElement(li)
    doc.text.addElement(bullet_list)

    # --- Looking Ahead ---
    doc.text.addElement(H(outlinelevel=1, stylename=h1_style,
                          text='Looking Ahead'))

    doc.text.addElement(P(stylename=body_style, text=(
        'As we enter Q4 2025, we remain focused on sustaining growth momentum while '
        'preparing for the upcoming fiscal year. Key priorities include expanding our '
        'digital product portfolio, deepening customer relationships in core markets, '
        'and investing in talent development to support long-term scalability.'
    )))

    doc.text.addElement(P(stylename=body_style, text=(
        'The leadership team is confident that the strategic foundations laid this '
        'quarter will position the company for continued success in an increasingly '
        'competitive landscape.'
    )))

    doc.save(OUTPUT)
    print('Initial file created: ' + OUTPUT)

    # GUI-ready startup
    launch_gui('libreoffice --writer "' + OUTPUT + '"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
