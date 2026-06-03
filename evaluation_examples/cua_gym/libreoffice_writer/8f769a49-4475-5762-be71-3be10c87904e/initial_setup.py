"""
Initial Setup: Three-day HuggingFace paper survey document
Task ID: osworld_multi_apps_hf_papers_writer_011
Domain: libreoffice_writer

Creates three_day_survey.odt with:
  - Three date section headings (2024-01-10, 2024-01-11, 2024-01-12)
  - A Duplicates section heading at the end
  - No paper content (agent must fill in from HuggingFace)

Opens Chrome and LibreOffice Writer for the GUI agent.
"""

import os
import shlex
import subprocess
import time

from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties
from odf.text import H, P

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_hf_papers_writer_011'
OUTPUT = f'{WORKDIR}/three_day_survey.odt'


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
    doc = OpenDocumentText()

    # --- Define heading style for date sections (Heading 1) ---
    h1_style = Style(name="Heading1", family="paragraph", parentstylename="Heading 1")
    doc.automaticstyles.addElement(h1_style)

    # --- Define heading style for Duplicates section (Heading 1) ---
    # We reuse Heading 1 style for all section headings

    # Add date headings and placeholder body paragraphs
    dates = ["2024-01-10", "2024-01-11", "2024-01-12"]
    for date_str in dates:
        # Heading using built-in Heading 1 style
        heading = H(outlinelevel=1, stylename="Heading 1", text=date_str)
        doc.text.addElement(heading)
        # Empty paragraph below heading as placeholder
        empty_para = P(stylename="Text Body", text="")
        doc.text.addElement(empty_para)

    # Add Duplicates section heading
    dup_heading = H(outlinelevel=1, stylename="Heading 1", text="Duplicates")
    doc.text.addElement(dup_heading)
    # Empty paragraph placeholder
    dup_para = P(stylename="Text Body", text="")
    doc.text.addElement(dup_para)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open Chrome first, then LibreOffice Writer
    launch_gui('google-chrome --new-window "https://huggingface.co/papers"', delay_sec=3.0)
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched Chrome and LibreOffice Writer with DISPLAY=:0')


create_initial()
