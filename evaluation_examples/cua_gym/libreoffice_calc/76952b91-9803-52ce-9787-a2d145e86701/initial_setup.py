"""
Initial Setup: daily_papers.ods - ArXiv cs.LG paper tracker
Task ID: osworld_multi_apps_web_papers_005
Domain: libreoffice_calc

Creates an ODS spreadsheet on the Desktop with headers and 3 pre-existing paper rows.
The agent's task is to find 6 new papers from ArXiv cs.LG/recent and append them to rows 5-10.
"""

import os
import shlex
import subprocess
import time

from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import Style, TableColumnProperties, TableCellProperties, TextProperties, ParagraphProperties
from odf.table import Table, TableColumn, TableRow, TableCell
from odf.text import P
from odf.namespaces import OFFICENS

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_web_papers_005'
OUTPUT = f'{WORKDIR}/daily_papers.ods'


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
    doc = OpenDocumentSpreadsheet()

    # Create column width styles
    col_style_id = Style(name="co1", family="table-column")
    col_style_id.addElement(TableColumnProperties(columnwidth="3.5cm", breakbefore="auto"))
    doc.automaticstyles.addElement(col_style_id)

    col_style_title = Style(name="co2", family="table-column")
    col_style_title.addElement(TableColumnProperties(columnwidth="12cm", breakbefore="auto"))
    doc.automaticstyles.addElement(col_style_title)

    col_style_author = Style(name="co3", family="table-column")
    col_style_author.addElement(TableColumnProperties(columnwidth="5cm", breakbefore="auto"))
    doc.automaticstyles.addElement(col_style_author)

    col_style_date = Style(name="co4", family="table-column")
    col_style_date.addElement(TableColumnProperties(columnwidth="4cm", breakbefore="auto"))
    doc.automaticstyles.addElement(col_style_date)

    # Header cell style (bold)
    header_style = Style(name="header_cell", family="table-cell")
    header_style.addElement(TextProperties(fontweight="bold"))
    doc.automaticstyles.addElement(header_style)

    # Create the spreadsheet table
    table = Table(name="Papers")
    table.addElement(TableColumn(stylename="co1"))
    table.addElement(TableColumn(stylename="co2"))
    table.addElement(TableColumn(stylename="co3"))
    table.addElement(TableColumn(stylename="co4"))

    def make_cell(value, style=None):
        if style:
            tc = TableCell(valuetype="string", stylename=style)
        else:
            tc = TableCell(valuetype="string")
        tc.addElement(P(text=str(value)))
        return tc

    # Row 1: Headers
    header_row = TableRow()
    for h in ["arXiv_ID", "Title", "First_Author", "Date_Added"]:
        header_row.addElement(make_cell(h, style="header_cell"))
    table.addElement(header_row)

    # Rows 2-4: 3 older papers (pre-existing realistic data)
    older_papers = [
        ("2412.08765", "Scaling Laws for Reward Model Overoptimization in Direct Alignment Algorithms",
         "Rafael Rafailov", "2026-03-01"),
        ("2501.03430", "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning",
         "DeepSeek-AI", "2026-03-03"),
        ("2502.11157", "Transformers Can In-Context Learn Linear Dynamical Systems",
         "Yingcong Li", "2026-03-04"),
    ]

    for arxiv_id, title, first_author, date_added in older_papers:
        row = TableRow()
        for val in [arxiv_id, title, first_author, date_added]:
            row.addElement(make_cell(val))
        table.addElement(row)

    doc.spreadsheet.addElement(table)
    doc.save(OUTPUT)
    print(f"Initial file created: {OUTPUT}")

    # Kill any existing LibreOffice instance to avoid conflicts
    subprocess.run(["pkill", "-f", "soffice"], capture_output=True)
    time.sleep(1.5)

    # GUI-ready startup: open the file in LibreOffice Calc
    launch_gui(f'libreoffice --calc "{OUTPUT}"', delay_sec=2.0)
    print("GUI_READY: launched LibreOffice Calc with DISPLAY=:0")


create_initial()
