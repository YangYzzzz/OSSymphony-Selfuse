"""
Initial Setup: Annotated Bibliography - HuggingFace Papers 2024-04-01
Task ID: osworld_multi_apps_hf_papers_writer_013
Domain: libreoffice_writer

Creates: /home/user/annotated_bib.odt with only the heading
'Annotated Bibliography - HuggingFace Papers 2024-04-01'.
No paper entries are added (agent must gather and add them).
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'annotated_bib'
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
    from odf.opendocument import OpenDocumentText
    from odf.style import Style, TextProperties, ParagraphProperties
    from odf.text import H, P

    doc = OpenDocumentText()

    # Define a heading style
    h1_style = Style(name="BibHeading", family="paragraph")
    h1_style.addElement(TextProperties(fontsize="18pt", fontweight="bold"))
    h1_style.addElement(ParagraphProperties(marginbottom="12pt"))
    doc.automaticstyles.addElement(h1_style)

    # Add heading
    heading = H(outlinelevel=1, stylename="BibHeading")
    heading.addText("Annotated Bibliography - HuggingFace Papers 2024-04-01")
    doc.text.addElement(heading)

    # Add an empty paragraph after the heading
    doc.text.addElement(P(text=""))

    doc.save(OUTPUT)
    print(f"Initial file created: {OUTPUT}")

    # GUI-ready startup: open Chrome with HuggingFace papers page and LibreOffice Writer
    launch_gui('google-chrome --no-sandbox "https://huggingface.co/papers" --new-window', delay_sec=2.0)
    # Open the ODT file in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print("GUI_READY: launched Chrome and LibreOffice Writer with DISPLAY=:0")


create_initial()
