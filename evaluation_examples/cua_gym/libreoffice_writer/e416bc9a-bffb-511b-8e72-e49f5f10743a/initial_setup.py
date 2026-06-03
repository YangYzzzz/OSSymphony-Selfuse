"""
Initial Setup: incomplete_bibliography.odt — 7 references with title and authors only.
Task ID: osworld_multi_apps_doi_resolve_writer_006
Domain: libreoffice_writer

Creates /home/user/incomplete_bibliography.odt with 7 bibliography entries that each contain
only a title and author names — no year, no DOI, no venue information.

The agent's task is to open Chrome, look up each reference on https://search.crossref.org/,
and update each entry with year in parentheses and an 'Available at: [DOI hyperlink]' line.
"""

import os
import shlex
import subprocess
import time

from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties
from odf.text import P, Span, H

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doi_resolve_writer_006'
OUTPUT = f'{WORKDIR}/incomplete_bibliography.odt'


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

    # Define a bold style for the title
    title_style = Style(name="BibTitle", family="text")
    title_style.addElement(TextProperties(fontweight="bold"))
    doc.automaticstyles.addElement(title_style)

    # Define a normal paragraph style
    para_style = Style(name="BibPara", family="paragraph")
    para_style.addElement(ParagraphProperties(marginbottom="0.2cm", margintop="0.1cm"))
    doc.automaticstyles.addElement(para_style)

    # Heading paragraph style
    heading_style = Style(name="BibHeading", family="paragraph")
    heading_style.addElement(ParagraphProperties(marginbottom="0.4cm", margintop="0.4cm"))
    heading_text_props = TextProperties(fontweight="bold", fontsize="14pt")
    heading_style.addElement(heading_text_props)
    doc.automaticstyles.addElement(heading_style)

    # Add a heading
    heading = P(stylename=heading_style)
    heading.addText("Bibliography")
    doc.text.addElement(heading)

    # Add a brief intro paragraph
    intro = P()
    intro.addText(
        "The following references are cited in this work. "
        "Full publication details including DOIs are pending verification."
    )
    doc.text.addElement(intro)

    # Add a blank line
    doc.text.addElement(P())

    # The 7 references — title and authors only (no year, no DOI, no venue)
    references = [
        {
            "title": "Efficient Estimation of Word Representations in Vector Space",
            "authors": "Mikolov, T., Chen, K., Corrado, G., and Dean, J.",
        },
        {
            "title": "GloVe: Global Vectors for Word Representation",
            "authors": "Pennington, J., Socher, R., and Manning, C. D.",
        },
        {
            "title": "Deep Contextualized Word Representations",
            "authors": "Peters, M. E., Neumann, M., Iyyer, M., Gardner, M., Clark, C., Lee, K., and Zettlemoyer, L.",
        },
        {
            "title": "Convolutional Neural Networks for Sentence Classification",
            "authors": "Kim, Y.",
        },
        {
            "title": "Sequence to Sequence Learning with Neural Networks",
            "authors": "Sutskever, I., Vinyals, O., and Le, Q. V.",
        },
        {
            "title": "Neural Machine Translation by Jointly Learning to Align and Translate",
            "authors": "Bahdanau, D., Cho, K., and Bengio, Y.",
        },
        {
            "title": "Get To The Point: Summarization with Pointer-Generator Networks",
            "authors": "See, A., Liu, P. J., and Manning, C. D.",
        },
    ]

    for i, ref in enumerate(references, 1):
        # Reference paragraph: "[N]. Title. Authors."
        ref_para = P(stylename=para_style)
        # Bold title with number
        title_span = Span(stylename=title_style)
        title_span.addText(f"[{i}] {ref['title']}.")
        ref_para.addElement(title_span)
        ref_para.addText(f" {ref['authors']}")
        doc.text.addElement(ref_para)

        # Add a small spacer between entries
        if i < len(references):
            doc.text.addElement(P())

    doc.save(OUTPUT)
    print(f"Initial file created: {OUTPUT}")

    # GUI-ready startup: open the ODT in LibreOffice Writer and Chrome for Crossref
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    launch_gui('google-chrome --new-window "https://search.crossref.org/"', delay_sec=2.0)
    print("GUI_READY: launched LibreOffice Writer and Chrome with DISPLAY=:0")


create_initial()
