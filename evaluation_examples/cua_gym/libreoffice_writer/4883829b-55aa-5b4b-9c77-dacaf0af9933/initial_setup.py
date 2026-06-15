"""
Initial Setup: comparison.odt with empty 2-column table and Overlap section
Task ID: osworld_multi_apps_hf_papers_writer_014
Domain: libreoffice_writer

Creates comparison.odt with:
- A 2-column table with headers 'HuggingFace Featured' and 'ArXiv cs.CL Total' (empty rows below)
- A heading 'Overlap' below the table (empty, ready for the agent to fill in)
Opens Chrome and LibreOffice Writer on the VM.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_hf_papers_writer_014'
OUTPUT = f'{WORKDIR}/comparison.odt'


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
    # Use python-docx to create an .odt-compatible document
    # Note: python-docx creates .docx format internally; we save as .odt
    # For proper ODT format, we use the odfpy library
    from odf.opendocument import OpenDocumentText
    from odf.style import Style, TextProperties, ParagraphProperties, TableColumnProperties
    from odf.text import H, P, Span
    from odf.table import Table, TableColumn, TableRow, TableCell
    from odf import text as odftext

    doc = OpenDocumentText()

    # Define heading style
    heading_style = Style(name="Heading1", family="paragraph", parentstylename="Heading_20_1")
    doc.styles.addElement(heading_style)

    # Add a brief intro paragraph
    intro = P(text="Paper Comparison: HuggingFace Featured vs ArXiv cs.CL (2024-02-05)")
    doc.text.addElement(intro)

    # Add empty paragraph for spacing
    doc.text.addElement(P())

    # Create the 2-column table
    table = Table(name="ComparisonTable")

    # Define two columns
    col1 = TableColumn()
    col2 = TableColumn()
    table.addElement(col1)
    table.addElement(col2)

    # Header row
    header_row = TableRow()

    cell_hf = TableCell()
    cell_hf.addElement(P(text="HuggingFace Featured"))
    header_row.addElement(cell_hf)

    cell_arxiv = TableCell()
    cell_arxiv.addElement(P(text="ArXiv cs.CL Total"))
    header_row.addElement(cell_arxiv)

    table.addElement(header_row)

    # Add 5 empty rows below the header (ready for the agent to fill)
    for _ in range(5):
        empty_row = TableRow()
        empty_row.addElement(TableCell(valuetype="string"))
        empty_row.addElement(TableCell(valuetype="string"))
        table.addElement(empty_row)

    doc.text.addElement(table)

    # Add spacing paragraph after table
    doc.text.addElement(P())

    # Add 'Overlap' section heading
    overlap_heading = H(outlinelevel=1, text="Overlap")
    doc.text.addElement(overlap_heading)

    # Add empty paragraph under Overlap for the agent to fill
    doc.text.addElement(P())

    # Save
    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: launch Chrome and LibreOffice Writer
    launch_gui('google-chrome --new-window "https://huggingface.co/papers"', delay_sec=3.0)
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Chrome and LibreOffice Writer with DISPLAY=:0')


create_initial()
