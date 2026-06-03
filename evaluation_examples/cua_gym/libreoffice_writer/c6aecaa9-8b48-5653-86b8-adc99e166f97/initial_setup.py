"""
Initial Setup: paper_list.odt with 4 paper titles (no URLs)
Task ID: osworld_multi_apps_doi_resolve_writer_003
Domain: libreoffice_writer

Creates a paper_list.odt file with 4 lines, each containing only a paper title.
No arXiv URLs are included — the agent must add them.
"""

import os
import shlex
import subprocess
import time

from odf.opendocument import OpenDocumentText
from odf.text import P
from odf.style import Style, TextProperties, ParagraphProperties
from odf import style as odf_style

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doi_resolve_writer_003'
OUTPUT = f'{WORKDIR}/paper_list.odt'

# Papers: titles only (no URLs in initial state)
PAPERS = [
    "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models",
    "Self-Consistency Improves Chain of Thought Reasoning in Language Models",
    "Tree of Thoughts: Deliberate Problem Solving with Large Language Models",
    "ReAct: Synergizing Reasoning and Acting in Language Models",
]


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

    # Add each paper title as its own paragraph
    for title in PAPERS:
        para = P(text=title)
        doc.text.addElement(para)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the file in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
