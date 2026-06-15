"""
Initial Setup: system_config.odt containing raw nested JSON structure
Task ID: osworld_multi_apps_json_reformat_writer_008
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time

# odfpy imports for creating ODT files
from odf.opendocument import OpenDocumentText
from odf.text import P, Span
from odf.style import Style, TextProperties, ParagraphProperties
from odf.namespaces import TEXTNS

WORKDIR = '/home/user'  # VM path — all scripts run on the VM
TASK_ID = 'osworld_multi_apps_json_reformat_writer_008'
# Task says open from Documents folder
OUTPUT = f'{WORKDIR}/Documents/system_config.odt'


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
    # Ensure Documents directory exists
    docs_dir = f'{WORKDIR}/Documents'
    os.makedirs(docs_dir, exist_ok=True)

    # Create ODT document with raw nested JSON text
    doc = OpenDocumentText()

    # Define a default paragraph style
    default_style = Style(name="Default", family="paragraph")
    doc.styles.addElement(default_style)

    # The raw JSON text to put in the document
    # Formatted nicely as the agent would see it
    json_text = '''{
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "prod_db",
    "ssl": true
  },
  "server": {
    "host": "0.0.0.0",
    "port": 8080,
    "workers": 4,
    "debug": false
  },
  "cache": {
    "backend": "redis",
    "host": "redis-host",
    "port": 6379,
    "ttl": 3600
  }
}'''

    # Add an introductory line
    intro = P()
    intro.addText("System Configuration File")
    doc.text.addElement(intro)

    # Add empty line
    doc.text.addElement(P())

    # Add the raw JSON as lines
    for line in json_text.split('\n'):
        para = P()
        para.addText(line)
        doc.text.addElement(para)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the ODT in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
