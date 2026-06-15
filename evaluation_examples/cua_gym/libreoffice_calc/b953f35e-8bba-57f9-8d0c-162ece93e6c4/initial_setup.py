"""
Initial Setup: researchers.ods with 4 existing researcher rows (not including Geoffrey Hinton)
Task ID: osworld_multi_apps_scholar_to_calc_002
Domain: libreoffice_calc
"""

import os
import shlex
import subprocess
import time

from odf.opendocument import OpenDocumentSpreadsheet
from odf.table import Table, TableRow, TableCell
from odf.text import P

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_scholar_to_calc_002'
OUTPUT = f'{WORKDIR}/researchers.ods'


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


def make_text_cell(text_value):
    """Create a table cell with a string value."""
    tc = TableCell(valuetype='string')
    p = P(text=str(text_value))
    tc.addElement(p)
    return tc


def make_float_cell(numeric_value):
    """Create a table cell with a numeric (float) value."""
    tc = TableCell(valuetype='float', value=str(numeric_value))
    p = P(text=str(numeric_value))
    tc.addElement(p)
    return tc


def create_initial():
    doc = OpenDocumentSpreadsheet()

    # Create the sheet
    sheet = Table(name="Sheet1")

    # --- Headers row ---
    headers = ["Name", "Affiliation", "H-Index", "Top Paper", "Year-of-Top-Paper"]
    header_row = TableRow()
    for h in headers:
        header_row.addElement(make_text_cell(h))
    sheet.addElement(header_row)

    # --- Existing researcher data (4 rows, NOT Geoffrey Hinton) ---
    researchers = [
        (
            "Yann LeCun",
            "New York University / Meta AI",
            185,
            "Gradient-based learning applied to document recognition",
            1998,
        ),
        (
            "Yoshua Bengio",
            "Universite de Montreal / Mila",
            172,
            "A neural probabilistic language model",
            2003,
        ),
        (
            "Andrew Ng",
            "Stanford University / DeepLearning.AI",
            134,
            "Building high-level features using large scale unsupervised learning",
            2012,
        ),
        (
            "Jurgen Schmidhuber",
            "IDSIA / University of Lugano",
            112,
            "Long Short-Term Memory",
            1997,
        ),
    ]

    for (name, affiliation, h_index, top_paper, year) in researchers:
        row = TableRow()
        row.addElement(make_text_cell(name))
        row.addElement(make_text_cell(affiliation))
        row.addElement(make_float_cell(h_index))
        row.addElement(make_text_cell(top_paper))
        row.addElement(make_float_cell(year))
        sheet.addElement(row)

    doc.spreadsheet.addElement(sheet)
    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup — open the file in LibreOffice Calc
    launch_gui(f'libreoffice --calc "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Calc with DISPLAY=:0')


create_initial()
