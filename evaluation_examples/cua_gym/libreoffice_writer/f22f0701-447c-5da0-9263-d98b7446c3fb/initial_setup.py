"""
Initial Setup: Reformat JSON content as a two-column table in LibreOffice Writer
Task ID: osworld_multi_apps_json_reformat_writer_001
Domain: libreoffice_writer

Creates product_data.odt on the Desktop with raw JSON text content (no table).
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user/Desktop'
TASK_ID = 'product_data'
OUTPUT = f'{WORKDIR}/{TASK_ID}.odt'


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
    # Use odfpy to create an ODT file with raw JSON text
    from odf.opendocument import OpenDocumentText
    from odf.text import P

    doc = OpenDocumentText()

    # Add a paragraph with the raw JSON content
    json_text = '{"name": "Widget Pro", "price": 29.99, "category": "Tools", "stock": 150, "sku": "WP-001"}'
    p = P(text=json_text)
    doc.text.addElement(p)

    # Ensure Desktop directory exists
    os.makedirs(WORKDIR, exist_ok=True)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the file in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
