"""
Initial Setup: arxiv LLM alignment papers tracker
Task ID: osworld_multi_apps_arxiv_llms_calc_006
Domain: libreoffice_calc (multi-app: Chrome + LibreOffice Calc)

Creates alignment_papers.ods with headers only (no data rows).
Opens Chrome navigated to arxiv cs.LG Feb 2024 listing.
Opens LibreOffice Calc with the created file.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_arxiv_llms_calc_006'
OUTPUT = f'{WORKDIR}/alignment_papers.ods'
ARXIV_URL = 'https://arxiv.org/list/cs.LG/2024-02'


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
    # Use Python to create an ODS file with headers only via subprocess with LibreOffice
    # First, create a minimal ODS using odfpy
    try:
        from odf.opendocument import OpenDocumentSpreadsheet
        from odf.table import Table, TableRow, TableCell
        from odf.text import P
        from odf import style as odstyle
        from odf.style import Style, TableCellProperties

        doc = OpenDocumentSpreadsheet()

        # Create header bold style
        header_style = Style(name="HeaderStyle", family="table-cell")
        header_text_prop = odstyle.TextProperties(fontweight="bold")
        header_style.addElement(header_text_prop)
        doc.styles.addElement(header_style)

        sheet = Table(name="Sheet1")
        doc.spreadsheet.addElement(sheet)

        # Header row: arXiv ID, Title, Authors, Date, Topic
        header_row = TableRow()
        sheet.addElement(header_row)

        headers = ['arXiv ID', 'Title', 'Authors', 'Date', 'Topic']
        for h in headers:
            cell = TableCell(valuetype="string", stylename="HeaderStyle")
            cell.addElement(P(text=h))
            header_row.addElement(cell)

        # No data rows - agent must fill these in

        doc.save(OUTPUT)
        print(f'Initial file created: {OUTPUT}')

    except ImportError:
        # Fallback: create via openpyxl then convert using LibreOffice
        import openpyxl
        xlsx_path = f'{WORKDIR}/alignment_papers_tmp.xlsx'
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Sheet1'
        headers = ['arXiv ID', 'Title', 'Authors', 'Date', 'Topic']
        for col, h in enumerate(headers, 1):
            ws.cell(row=1, column=col, value=h)
        wb.save(xlsx_path)
        print(f'Temporary xlsx created: {xlsx_path}')

        # Convert to ODS using LibreOffice headless
        env = os.environ.copy()
        env["DISPLAY"] = ":0"
        result = subprocess.run(
            ['libreoffice', '--headless', '--convert-to', 'ods', '--outdir', WORKDIR, xlsx_path],
            capture_output=True, text=True, timeout=30, env=env
        )
        # Rename if needed
        ods_converted = f'{WORKDIR}/alignment_papers_tmp.ods'
        if os.path.exists(ods_converted):
            os.rename(ods_converted, OUTPUT)
        # Remove tmp xlsx
        if os.path.exists(xlsx_path):
            os.remove(xlsx_path)
        print(f'Initial ODS file created: {OUTPUT}')

    # GUI-ready startup: open Chrome with arxiv URL, then LibreOffice Calc
    # Kill any existing LibreOffice instances first to avoid conflicts
    subprocess.run(['pkill', '-f', 'soffice'], capture_output=True)
    time.sleep(1.0)

    # Open Chrome with arxiv cs.LG Feb 2024 listing
    launch_gui(f'google-chrome "{ARXIV_URL}"', delay_sec=2.0)

    # Open LibreOffice Calc with the alignment_papers.ods file
    launch_gui(f'libreoffice --calc "{OUTPUT}"', delay_sec=2.0)

    print('GUI_READY: launched Chrome and LibreOffice Calc with DISPLAY=:0')


create_initial()
