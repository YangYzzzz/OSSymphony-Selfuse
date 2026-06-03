"""
Initial Setup: Create financials.ods on Desktop and empty Q4_report.odt in Documents
Task ID: osworld_multi_apps_doc_calc_to_writer_007
Domain: libreoffice_writer (multi-app: calc + writer)
"""

import os
import shlex
import subprocess
import time

# VM paths
DESKTOP = '/home/user/Desktop'
DOCUMENTS = '/home/user/Documents'
FINANCIALS_PATH = f'{DESKTOP}/financials.ods'
REPORT_PATH = f'{DOCUMENTS}/Q4_report.odt'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    try:
        subprocess.Popen(
            shlex.split(command),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env,
        )
        time.sleep(delay_sec)
    except FileNotFoundError as e:
        print(f'Warning: could not launch GUI ({e}); continuing.')


def create_financials_ods():
    """Create financials.ods with 3 data tables on Desktop using odfpy."""
    from odf.opendocument import OpenDocumentSpreadsheet
    from odf.style import Style, TextProperties, TableColumnProperties, TableCellProperties
    from odf.table import Table, TableColumn, TableRow, TableCell
    from odf.text import P
    from odf.namespaces import OFFICENS

    doc = OpenDocumentSpreadsheet()

    # Define styles
    # Bold style for header cells
    bold_style = Style(name='BoldCell', family='table-cell')
    bold_style.addElement(TextProperties(fontweight='bold'))
    doc.styles.addElement(bold_style)

    # Normal style
    normal_style = Style(name='NormalCell', family='table-cell')
    doc.styles.addElement(normal_style)

    # Number style for currency
    num_style = Style(name='NumCell', family='table-cell')
    doc.styles.addElement(num_style)

    table = Table(name='Financials')

    def add_row(cells_data, is_header=False):
        """Add a row to the table with given cell values."""
        row = TableRow()
        style = bold_style if is_header else normal_style
        for val in cells_data:
            cell = TableCell()
            if val is None or val == '':
                row.addElement(cell)
                continue
            if isinstance(val, (int, float)):
                cell.setAttribute('valuetype', 'float')
                cell.setAttribute('value', str(val))
                cell.addElement(P(text=str(val)))
            else:
                cell.setAttribute('valuetype', 'string')
                p = P()
                if is_header:
                    from odf.text import Span
                    span = Span(stylename=bold_style)
                    span.addText(str(val))
                    p.addElement(span)
                else:
                    p.addText(str(val))
                cell.addElement(p)
            row.addElement(cell)
        table.addElement(row)

    def add_empty_row():
        """Add an empty separator row."""
        row = TableRow()
        cell = TableCell()
        row.addElement(cell)
        table.addElement(row)

    # ── Revenue Table: A1:D6 ──────────────────────────────────────────────
    add_row(['Product Line', 'Q1 ($)', 'Q2 ($)', 'Q3 ($)'], is_header=True)
    add_row(['Software Licenses',      345200, 378900, 412100])
    add_row(['Professional Services',  128400, 145600, 162300])
    add_row(['Hardware Sales',          89700,  95400, 103200])
    add_row(['Maintenance Contracts',   67800,  71200,  74500])
    add_row(['Cloud Subscriptions',    156300, 189700, 224800])

    # ── Empty row 7 ────────────────────────────────────────────────────────
    add_empty_row()

    # ── Expenses Table: A8:D12 ────────────────────────────────────────────
    add_row(['Cost Category', 'Q1 ($)', 'Q2 ($)', 'Q3 ($)'], is_header=True)
    add_row(['Salaries & Benefits', 198400, 204300, 211700])
    add_row(['Marketing & Sales',    45600,  52100,  48900])
    add_row(['Infrastructure',       38200,  39800,  41200])
    add_row(['R&D',                  67500,  71000,  73400])

    # ── Empty row 13 ───────────────────────────────────────────────────────
    add_empty_row()
    add_empty_row()

    # ── Profit Summary: A14:B17 ───────────────────────────────────────────
    add_row(['Quarter', 'Net Profit ($)'], is_header=True)
    add_row(['Q1',            112000])
    add_row(['Q2',            139900])
    add_row(['Q3',            158500])
    add_row(['Q4 (Forecast)', 172400])

    doc.spreadsheet.addElement(table)
    doc.save(FINANCIALS_PATH)
    print(f'financials.ods created at: {FINANCIALS_PATH}')


def create_empty_report_odt():
    """Create empty Q4_report.odt in Documents folder."""
    from docx import Document

    os.makedirs(DOCUMENTS, exist_ok=True)

    doc = Document()
    # Remove default content — keep minimal empty document
    # The default doc has one empty paragraph; leave it as-is (truly empty doc)
    # Clear the default paragraph text
    for p in doc.paragraphs:
        for run in p.runs:
            run.text = ''
    doc.save(REPORT_PATH)
    print(f'Empty Q4_report.odt created at: {REPORT_PATH}')


def main():
    # Ensure directories exist
    os.makedirs(DESKTOP, exist_ok=True)
    os.makedirs(DOCUMENTS, exist_ok=True)

    # Create the source file
    create_financials_ods()

    # Create the empty target document
    create_empty_report_odt()

    # GUI-ready startup: open both files
    # Open financials.ods in LibreOffice Calc
    launch_gui(f'libreoffice --calc "{FINANCIALS_PATH}"', delay_sec=2.0)

    # Open Q4_report.odt in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{REPORT_PATH}"', delay_sec=2.0)

    print('GUI_READY: Launched LibreOffice Calc and LibreOffice Writer with DISPLAY=:0')


main()
