"""
Initial Setup: Copy project tracker data from Calc to Writer formatted table
Task ID: osworld_multi_apps_doc_calc_to_writer_005
Domain: libreoffice_writer (multi-app: Calc + Writer)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doc_calc_to_writer_005'
DESKTOP = '/home/user/Desktop'
ODS_OUTPUT = f'{DESKTOP}/projects.ods'


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
    import subprocess as sp
    import sys

    # Ensure odfpy is available on the VM
    sp.run([sys.executable, '-m', 'pip', 'install', 'odfpy', '--quiet'], check=False)

    from odf.opendocument import OpenDocumentSpreadsheet
    from odf.table import Table, TableRow, TableCell
    from odf.text import P
    from odf.style import Style, TableCellProperties, TextProperties

    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # Create .ods spreadsheet
    doc = OpenDocumentSpreadsheet()

    # Define a bold style for header
    header_style = Style(name="HeaderCell", family="table-cell")
    header_style.addElement(TextProperties(fontweight="bold"))
    doc.automaticstyles.addElement(header_style)

    # Define normal style
    normal_style = Style(name="NormalCell", family="table-cell")
    doc.automaticstyles.addElement(normal_style)

    table = Table(name="Projects")

    # Header row
    headers = ['Project_Name', 'Owner', 'Status', 'Due_Date', 'Budget', 'Completion_Pct']
    hrow = TableRow()
    for h in headers:
        cell = TableCell(stylename=header_style)
        cell.addElement(P(text=h))
        hrow.addElement(cell)
    table.addElement(hrow)

    # 8 rows of realistic project data
    data = [
        ['Website Redesign',         'Sarah Chen',       'In Progress', '2024-10-31', '45000',  '65'],
        ['Mobile App Launch',         'Marcus Johnson',   'In Progress', '2024-11-15', '120000', '40'],
        ['CRM Integration',           'Emily Rodriguez',  'On Hold',     '2024-12-01', '78000',  '25'],
        ['Data Warehouse Migration',  'James Whitfield',  'In Progress', '2024-11-30', '230000', '55'],
        ['HR Portal Update',          'Priya Kapoor',     'Completed',   '2024-09-30', '35000',  '100'],
        ['Security Audit',            'Tom Nakamura',     'In Progress', '2024-10-15', '22000',  '80'],
        ['ERP Upgrade',               'Aisha Mohammed',   'Planning',    '2024-12-31', '310000', '10'],
        ['Customer Analytics Dashboard', 'Luke Eriksson', 'In Progress', '2024-11-20', '67500',  '50'],
    ]

    for row_data in data:
        row = TableRow()
        for val in row_data:
            cell = TableCell(stylename=normal_style)
            cell.addElement(P(text=val))
            row.addElement(cell)
        table.addElement(row)

    doc.spreadsheet.addElement(table)
    doc.save(ODS_OUTPUT)
    print(f'Initial file created: {ODS_OUTPUT}')

    # GUI-ready: open projects.ods in LibreOffice Calc
    launch_gui(f'libreoffice --calc "{ODS_OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Calc with projects.ods (DISPLAY=:0)')


create_initial()
