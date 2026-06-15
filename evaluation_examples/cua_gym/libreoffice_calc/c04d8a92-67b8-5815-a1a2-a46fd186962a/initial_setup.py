"""
Initial Setup: researchers.ods with 3 existing researcher rows on the Desktop
Task ID: osworld_multi_apps_web_scholar_001
Domain: libreoffice_calc
"""

import os
import shlex
import subprocess
import time
from odf.opendocument import OpenDocumentSpreadsheet
from odf.table import Table, TableRow, TableCell
from odf.text import P

WORKDIR = '/home/user/Desktop'
FILENAME = 'researchers.ods'
OUTPUT = f'{WORKDIR}/{FILENAME}'


def make_string_cell(text):
    """Create an ODS string cell."""
    tc = TableCell(valuetype='string')
    tc.addElement(P(text=str(text)))
    return tc


def make_float_cell(value):
    """Create an ODS numeric float cell."""
    tc = TableCell(valuetype='float', value=str(value))
    tc.addElement(P(text=str(value)))
    return tc


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
    os.makedirs(WORKDIR, exist_ok=True)

    doc = OpenDocumentSpreadsheet()
    table = Table(name='Sheet1')
    doc.spreadsheet.addElement(table)

    # --- Header row ---
    headers = [
        'Name', 'Affiliation', 'H_Index', 'Total_Citations',
        'Top_Paper', 'Top_Paper_Citations'
    ]
    tr_header = TableRow()
    table.addElement(tr_header)
    for h in headers:
        tr_header.addElement(make_string_cell(h))

    # --- 3 existing researcher rows (realistic ML researchers) ---
    researchers = [
        {
            'name': 'Geoffrey Hinton',
            'affiliation': 'University of Toronto / Google Brain',
            'h_index': 150,
            'total_citations': 870000,
            'top_paper': 'Learning representations by back-propagating errors',
            'top_paper_citations': 32000,
        },
        {
            'name': 'Yoshua Bengio',
            'affiliation': 'Universite de Montreal / Mila',
            'h_index': 181,
            'total_citations': 800000,
            'top_paper': 'A neural probabilistic language model',
            'top_paper_citations': 15000,
        },
        {
            'name': 'Andrew Ng',
            'affiliation': 'Stanford University / DeepLearning.AI',
            'h_index': 103,
            'total_citations': 310000,
            'top_paper': 'Building high-level features using large scale unsupervised learning',
            'top_paper_citations': 5800,
        },
    ]

    for r in researchers:
        tr = TableRow()
        table.addElement(tr)
        tr.addElement(make_string_cell(r['name']))
        tr.addElement(make_string_cell(r['affiliation']))
        tr.addElement(make_float_cell(r['h_index']))
        tr.addElement(make_float_cell(r['total_citations']))
        tr.addElement(make_string_cell(r['top_paper']))
        tr.addElement(make_float_cell(r['top_paper_citations']))

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the file in LibreOffice Calc
    launch_gui(f'libreoffice --calc "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Calc with DISPLAY=:0')


create_initial()
