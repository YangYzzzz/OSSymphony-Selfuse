"""
Initial Setup: Research workflow with queries.ods for academic search automation
Task ID: osworld_multi_apps_multi_simple_012
Domain: libreoffice_calc (multi-app: calc + chrome)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'  # VM path — all scripts run on the VM
TASK_ID = 'osworld_multi_apps_multi_simple_012'
RESEARCH_DIR = f'{WORKDIR}/research'
OUTPUT = f'{RESEARCH_DIR}/queries.ods'


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
    # Create research directory
    os.makedirs(RESEARCH_DIR, exist_ok=True)

    # Create queries.ods using odfpy
    from odf.opendocument import OpenDocumentSpreadsheet
    from odf.table import Table, TableRow, TableCell
    from odf.text import P
    from odf.style import Style, TableCellProperties, TextProperties
    from odf.namespaces import OFFICENS

    doc = OpenDocumentSpreadsheet()

    # Create a bold header style
    header_style = Style(name="HeaderCell", family="table-cell")
    header_style.addElement(TableCellProperties(backgroundcolor="#4472C4"))
    header_style.addElement(TextProperties(fontweight="bold", color="#FFFFFF"))
    doc.automaticstyles.addElement(header_style)

    table = Table(name="Queries")

    def make_cell(value="", style_name=None):
        if style_name:
            tc = TableCell(stylename=style_name, valuetype="string")
        else:
            tc = TableCell(valuetype="string")
        if value:
            tc.addElement(P(text=str(value)))
        return tc

    # Header row
    header_row = TableRow()
    for h in ["Query", "Target URL", "Result Title", "Result Link"]:
        header_row.addElement(make_cell(h, style_name="HeaderCell"))
    table.addElement(header_row)

    # 4 academic queries with target site URLs
    # NOTE: Columns C (Result Title) and D (Result Link) are LEFT EMPTY
    # — the agent must fill these in by searching the web
    queries_data = [
        (
            "machine learning interpretability survey 2023",
            "https://scholar.google.com"
        ),
        (
            "transformer architecture natural language processing",
            "https://arxiv.org"
        ),
        (
            "reinforcement learning from human feedback RLHF",
            "https://semanticscholar.org"
        ),
        (
            "large language model evaluation benchmarks 2024",
            "https://paperswithcode.com"
        ),
    ]

    for query, url in queries_data:
        row = TableRow()
        row.addElement(make_cell(query))     # Column A: Query
        row.addElement(make_cell(url))       # Column B: Target URL
        row.addElement(make_cell(""))        # Column C: Result Title (EMPTY - agent fills)
        row.addElement(make_cell(""))        # Column D: Result Link (EMPTY - agent fills)
        table.addElement(row)

    doc.spreadsheet.addElement(table)
    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open LibreOffice Calc with the queries file AND Chrome
    launch_gui(f'libreoffice --calc "{OUTPUT}"', delay_sec=2.0)
    launch_gui('google-chrome', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Calc and Chrome with DISPLAY=:0')


create_initial()
