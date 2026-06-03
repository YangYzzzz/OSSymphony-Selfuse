"""
Initial Setup: Open Chrome with HuggingFace papers page and LibreOffice Writer with hf_papers.odt
Task ID: osworld_multi_apps_hf_papers_writer_005
Domain: libreoffice_writer

Creates hf_papers.odt containing only the heading 'HuggingFace Daily Papers - 2024-01-15'.
Opens Chrome with HuggingFace papers page and LibreOffice Writer with the file.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_hf_papers_writer_005'
OUTPUT = f'{WORKDIR}/hf_papers.odt'


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
    # Create hf_papers.odt with only the heading using odfpy
    from odf.opendocument import OpenDocumentText
    from odf.style import Style, TextProperties, ParagraphProperties
    from odf.text import H, P

    doc = OpenDocumentText()

    # Create heading style (Heading 1)
    h1_style = Style(name="Heading 1", family="paragraph")
    h1_style.addElement(TextProperties(
        fontsize="20pt",
        fontweight="bold",
    ))
    doc.automaticstyles.addElement(h1_style)

    # Add the heading
    heading = H(outlinelevel=1, stylename="Heading 1")
    heading.addText("HuggingFace Daily Papers - 2024-01-15")
    doc.text.addElement(heading)

    # Save the document
    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open Chrome with HuggingFace papers page
    launch_gui(
        'google-chrome --no-sandbox --disable-dev-shm-usage "https://huggingface.co/papers?date=2024-01-15"',
        delay_sec=3.0
    )

    # Open LibreOffice Writer with the initial file
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)

    print('GUI_READY: launched Chrome and LibreOffice Writer with DISPLAY=:0')


create_initial()
