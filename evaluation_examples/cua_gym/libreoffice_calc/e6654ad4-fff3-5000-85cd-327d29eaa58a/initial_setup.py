"""
Initial Setup: Cross-category arXiv LLM papers spreadsheet
Task ID: osworld_multi_apps_arxiv_llms_calc_009
Domain: libreoffice_calc (ODS format)

Creates cross_category.ods with:
  - Row 1: headers (arXiv ID, Title, Authors, Source Category, Duplicate)
  - H1: "Duplicate Count" label, I1: empty (agent will add COUNTIF formula)
  - Rows 2-11: Empty data rows (agent fills these with 10 papers from arXiv)

The agent's task is to browse arXiv cs.CL and cs.LG February 2024,
find 5 papers each about "large language models", fill them in,
add IF+COUNTIF Duplicate formulas, and add COUNTIF summary.

MUST NOT contain: paper data, duplicate formulas, COUNTIF formulas
"""

import os
import shlex
import subprocess
import time

from odf.opendocument import OpenDocumentSpreadsheet
from odf.table import Table, TableRow, TableCell
from odf.text import P

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_arxiv_llms_calc_009'
OUTPUT = f'{WORKDIR}/cross_category.ods'


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


def make_string_cell(text):
    """Create a string-type table cell."""
    cell = TableCell(valuetype='string')
    cell.addElement(P(text=str(text) if text is not None else ''))
    return cell


def make_empty_cell():
    """Create an empty string cell."""
    cell = TableCell(valuetype='string')
    cell.addElement(P(text=''))
    return cell


def create_initial():
    doc = OpenDocumentSpreadsheet()
    table = Table(name='Papers')

    # --- Row 1: Headers ---
    header_row = TableRow()
    # A1-E1: column headers
    for h in ['arXiv ID', 'Title', 'Authors', 'Source Category', 'Duplicate']:
        header_row.addElement(make_string_cell(h))
    # F1, G1: empty spacers
    header_row.addElement(make_empty_cell())  # F1
    header_row.addElement(make_empty_cell())  # G1
    # H1: summary label (present in initial state)
    header_row.addElement(make_string_cell('Duplicate Count'))
    # I1: empty - agent will add COUNTIF formula here
    header_row.addElement(make_empty_cell())  # I1
    table.addElement(header_row)

    # --- Rows 2-11: Empty data rows ---
    for _ in range(10):
        data_row = TableRow()
        for _ in range(5):  # A-E: empty data cells
            data_row.addElement(make_empty_cell())
        table.addElement(data_row)

    doc.spreadsheet.addElement(table)
    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open Chrome for arXiv browsing AND LibreOffice Calc
    launch_gui(
        'google-chrome --new-window "https://arxiv.org/list/cs.CL/2024-02"',
        delay_sec=3.0
    )
    launch_gui(f'libreoffice --calc "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Chrome (arXiv) and LibreOffice Calc with DISPLAY=:0')


create_initial()
