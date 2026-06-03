"""
Initial Setup: Weekly Digest document for HuggingFace daily papers (2024-03-04 to 2024-03-08)
Task ID: osworld_multi_apps_hf_papers_writer_015
Domain: libreoffice_writer

Creates weekly_digest.odt with:
- Summary table placeholder (headers only, no data)
- Five date section headings (2024-03-04 through 2024-03-08) with empty entry placeholders
- Trends section with placeholder text (no bullet points)

Chrome and LibreOffice Writer are both launched at the end.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_hf_papers_writer_015'
OUTPUT = f'{WORKDIR}/weekly_digest.odt'


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
    from odf.style import Style, TextProperties, ParagraphProperties, TableColumnProperties, TableProperties
    from odf.text import H, P, List, ListItem, Span
    from odf.table import Table, TableColumn, TableRow, TableCell
    from odf import teletype

    doc = OpenDocumentText()

    # --- Define styles ---
    # Heading 1 style
    h1_style = Style(name="Heading1Custom", family="paragraph", parentstylename="Heading 1")
    doc.automaticstyles.addElement(h1_style)

    # Heading 2 style
    h2_style = Style(name="Heading2Custom", family="paragraph", parentstylename="Heading 2")
    doc.automaticstyles.addElement(h2_style)

    # Bold text style
    bold_style = Style(name="BoldText", family="text")
    bold_style.addElement(TextProperties(fontweight="bold"))
    doc.automaticstyles.addElement(bold_style)

    # Table style
    table_style = Style(name="WeeklyTable", family="table")
    table_style.addElement(TableProperties(width="17cm", align="left"))
    doc.automaticstyles.addElement(table_style)

    # Table column style
    col_style1 = Style(name="TableCol1", family="table-column")
    col_style1.addElement(TableColumnProperties(columnwidth="4cm"))
    doc.automaticstyles.addElement(col_style1)

    col_style2 = Style(name="TableCol2", family="table-column")
    col_style2.addElement(TableColumnProperties(columnwidth="4cm"))
    doc.automaticstyles.addElement(col_style2)

    col_style3 = Style(name="TableCol3", family="table-column")
    col_style3.addElement(TableColumnProperties(columnwidth="9cm"))
    doc.automaticstyles.addElement(col_style3)

    # --- Document Title ---
    title_para = H(outlinelevel=1, stylename="Heading 1")
    title_para.addText("HuggingFace Weekly Digest: March 4-8, 2024")
    doc.text.addElement(title_para)

    # --- Summary Table Section ---
    section_heading = H(outlinelevel=2, stylename="Heading 2")
    section_heading.addText("Summary")
    doc.text.addElement(section_heading)

    intro_para = P(stylename="Text Body")
    intro_para.addText("The table below summarizes the papers featured on HuggingFace Daily Papers for each day of the week.")
    doc.text.addElement(intro_para)

    # Summary table with headers only (no data rows - agent must fill these in)
    table = Table(name="SummaryTable", stylename="WeeklyTable")
    table.addElement(TableColumn(stylename="TableCol1"))
    table.addElement(TableColumn(stylename="TableCol2"))
    table.addElement(TableColumn(stylename="TableCol3"))

    # Header row
    header_row = TableRow()
    table.addElement(header_row)

    for header_text in ["Day", "Paper Count", "Top Paper Title"]:
        cell = TableCell(valuetype="string")
        cell_para = P()
        bold_span = Span(stylename="BoldText")
        bold_span.addText(header_text)
        cell_para.addElement(bold_span)
        cell.addElement(cell_para)
        header_row.addElement(cell)

    # Five empty data rows (one per day) — agent must fill these
    dates = ["2024-03-04", "2024-03-05", "2024-03-06", "2024-03-07", "2024-03-08"]
    for date in dates:
        data_row = TableRow()
        table.addElement(data_row)
        # Day cell (pre-filled with date)
        date_cell = TableCell(valuetype="string")
        date_para = P()
        date_para.addText(date)
        date_cell.addElement(date_para)
        data_row.addElement(date_cell)
        # Paper Count cell (empty)
        count_cell = TableCell(valuetype="string")
        count_para = P()
        count_para.addText("")
        count_cell.addElement(count_para)
        data_row.addElement(count_cell)
        # Top Paper Title cell (empty)
        title_cell = TableCell(valuetype="string")
        title_para = P()
        title_para.addText("")
        title_cell.addElement(title_para)
        data_row.addElement(title_cell)

    doc.text.addElement(table)

    # Spacer paragraph
    doc.text.addElement(P())

    # --- Daily Sections ---
    day_labels = {
        "2024-03-04": "Monday, March 4, 2024",
        "2024-03-05": "Tuesday, March 5, 2024",
        "2024-03-06": "Wednesday, March 6, 2024",
        "2024-03-07": "Thursday, March 7, 2024",
        "2024-03-08": "Friday, March 8, 2024",
    }

    for date in dates:
        # Date section heading
        day_heading = H(outlinelevel=2, stylename="Heading 2")
        day_heading.addText(f"{date} — {day_labels[date]}")
        doc.text.addElement(day_heading)

        # Placeholder paragraph for paper entries
        placeholder_para = P(stylename="Text Body")
        placeholder_para.addText("[Paper entries for this day will be added here. Include: bold title, authors, arXiv ID, and abstract for each paper.]")
        doc.text.addElement(placeholder_para)

        # Spacer
        doc.text.addElement(P())

    # --- Trends Section ---
    trends_heading = H(outlinelevel=2, stylename="Heading 2")
    trends_heading.addText("Trends")
    doc.text.addElement(trends_heading)

    trends_intro = P(stylename="Text Body")
    trends_intro.addText("[Add 3-5 bullet points here summarizing the key research themes and trends observed across the papers featured this week.]")
    doc.text.addElement(trends_intro)

    # Save the document
    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open Chrome and LibreOffice Writer
    # First launch Chrome pointing to HuggingFace daily papers
    launch_gui('google-chrome --new-window "https://huggingface.co/papers" --no-first-run --no-default-browser-check', delay_sec=2.0)

    # Then launch LibreOffice Writer with the weekly digest file
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)

    print('GUI_READY: launched Chrome and LibreOffice Writer with DISPLAY=:0')


create_initial()
