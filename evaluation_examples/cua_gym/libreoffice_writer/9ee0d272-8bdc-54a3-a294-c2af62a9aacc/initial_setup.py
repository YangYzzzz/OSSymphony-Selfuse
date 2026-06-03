"""
Initial Setup: DOI Resolution Task for LibreOffice Writer
Task ID: osworld_multi_apps_doi_resolve_writer_005
Domain: libreoffice_writer

Creates survey_refs.odt with 5 reference entries (title + authors only, no DOI, no year).
Then opens LibreOffice Writer and Chrome for the agent.
"""

import os
import shlex
import subprocess
import sys
import time

# Ensure odfpy is available on the VM
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'odfpy', '-q'])

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doi_resolve_writer_005'
OUTPUT = f'{WORKDIR}/survey_refs.odt'


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
    from odf.text import P, H
    from odf.style import Style, TextProperties, ParagraphProperties
    from odf.namespaces import TEXTNS

    doc = OpenDocumentText()

    # Create a heading style for the document title
    heading_style = Style(name="DocumentTitle", family="paragraph")
    heading_style.addElement(TextProperties(
        fontsize="16pt",
        fontweight="bold"
    ))
    doc.styles.addElement(heading_style)

    # Create reference paragraph style
    ref_style = Style(name="RefPara", family="paragraph")
    ref_style.addElement(ParagraphProperties(
        marginbottom="0.2cm",
        margintop="0.1cm"
    ))
    doc.styles.addElement(ref_style)

    # Document title
    title_para = H(outlinelevel=1, text="Survey References")
    doc.text.addElement(title_para)

    # Intro paragraph
    intro = P(text="The following references are listed for the survey paper. Please complete each entry by finding the publication year and DOI using Crossref.")
    doc.text.addElement(intro)

    # Blank line
    doc.text.addElement(P(text=""))

    # Five references — title + authors only, NO year, NO DOI
    references = [
        {
            "num": "1",
            "title": "Attention Is All You Need",
            "authors": "Vaswani et al."
        },
        {
            "num": "2",
            "title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
            "authors": "Devlin et al."
        },
        {
            "num": "3",
            "title": "Dropout: A Simple Way to Prevent Neural Networks from Overfitting",
            "authors": "Srivastava et al."
        },
        {
            "num": "4",
            "title": "Adam: A Method for Stochastic Optimization",
            "authors": "Kingma, Ba."
        },
        {
            "num": "5",
            "title": "Deep Residual Learning for Image Recognition",
            "authors": "He et al."
        },
    ]

    for ref in references:
        # Each reference as: [N] Title. Authors.
        ref_text = f"[{ref['num']}] {ref['title']}. {ref['authors']}."
        p = P(text=ref_text)
        doc.text.addElement(p)
        # Add blank line after each reference
        doc.text.addElement(P(text=""))

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: Open LibreOffice Writer with the file, and Chrome
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=3.0)
    launch_gui('google-chrome --new-window "https://search.crossref.org/"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer and Chrome with DISPLAY=:0')


create_initial()
