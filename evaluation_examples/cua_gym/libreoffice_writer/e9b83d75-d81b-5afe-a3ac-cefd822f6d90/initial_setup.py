"""
Initial Setup: cs.CL Papers Bibliography Task
Task ID: osworld_multi_apps_hf_papers_writer_012
Domain: libreoffice_writer
Description: Creates cls_papers.odt with heading 'cs.CL Papers February 2024'
             and a 'Keywords' section heading at the bottom, with no paper entries.
             Chrome is also opened to the arxiv listing page.
"""

import os
import shlex
import subprocess
import time

from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties
from odf.text import H, P, Span

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_hf_papers_writer_012'
OUTPUT = f'{WORKDIR}/cls_papers.odt'


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

    # --- Define Styles ---
    # Heading 1 style
    h1_style = Style(name="Heading1Setup", family="paragraph")
    h1_style.addElement(ParagraphProperties(breakbefore="auto"))
    h1_style.addElement(TextProperties(fontsize="18pt", fontweight="bold"))
    doc.automaticstyles.addElement(h1_style)

    # Heading 2 style (for Keywords section)
    h2_style = Style(name="Heading2Setup", family="paragraph")
    h2_style.addElement(TextProperties(fontsize="14pt", fontweight="bold"))
    doc.automaticstyles.addElement(h2_style)

    # --- Main Title Heading ---
    title = H(outlinelevel=1, text="cs.CL Papers February 2024")
    doc.text.addElement(title)

    # Empty paragraph as spacer
    doc.text.addElement(P(text=""))

    # --- Keywords Section Heading (at the bottom) ---
    keywords_heading = H(outlinelevel=2, text="Keywords")
    doc.text.addElement(keywords_heading)

    # Save the file
    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # --- GUI-ready startup ---
    # Open LibreOffice Writer with the initial file
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)

    # Open Chrome with the arxiv cs.CL listing page
    launch_gui(
        'google-chrome --no-sandbox "https://arxiv.org/list/cs.CL/2024-02"',
        delay_sec=2.0
    )

    print('GUI_READY: launched LibreOffice Writer and Chrome with DISPLAY=:0')


create_initial()
