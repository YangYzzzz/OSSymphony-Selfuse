"""
Initial Setup: Annotated Bibliography with 10 paper titles only (no APA citations or annotations)
Task ID: osworld_multi_apps_doi_resolve_writer_014
Domain: libreoffice_writer

Creates annotated_bibliography.odt in /home/user with:
- Title: "Annotated Bibliography"
- 10 paper titles as plain text (no citations, no DOI hyperlinks, no annotations)
- "Bibliography Statistics" placeholder section at the bottom
- Opens file in LibreOffice Writer and Chrome
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doi_resolve_writer_014'
OUTPUT = f'{WORKDIR}/annotated_bibliography.odt'


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
    from odf.text import P

    doc = OpenDocumentText()

    # Define styles using odfpy keyword args (no namespace prefix, hyphens as underscores are not needed -
    # odfpy maps the kwarg names directly to ODF attribute names)
    # Title style
    title_style = Style(name="DocTitle", family="paragraph")
    title_style.addElement(TextProperties(fontsize="20pt", fontweight="bold"))
    title_style.addElement(ParagraphProperties(textalign="center", marginbottom="0.5cm"))
    doc.automaticstyles.addElement(title_style)

    # Section heading style
    heading_style = Style(name="SectionHeading", family="paragraph")
    heading_style.addElement(TextProperties(fontsize="14pt", fontweight="bold"))
    heading_style.addElement(ParagraphProperties(margintop="0.5cm", marginbottom="0.2cm"))
    doc.automaticstyles.addElement(heading_style)

    # Subtitle style
    subtitle_style = Style(name="Subtitle", family="paragraph")
    subtitle_style.addElement(TextProperties(fontsize="11pt", fontstyle="italic"))
    subtitle_style.addElement(ParagraphProperties(marginbottom="0.4cm"))
    doc.automaticstyles.addElement(subtitle_style)

    # Normal text style
    normal_style = Style(name="NormalText", family="paragraph")
    normal_style.addElement(TextProperties(fontsize="12pt"))
    normal_style.addElement(ParagraphProperties(marginbottom="0.3cm"))
    doc.automaticstyles.addElement(normal_style)

    # Paper entry style
    entry_style = Style(name="PaperEntry", family="paragraph")
    entry_style.addElement(TextProperties(fontsize="12pt"))
    entry_style.addElement(ParagraphProperties(marginbottom="0.4cm", marginleft="0.5cm"))
    doc.automaticstyles.addElement(entry_style)

    # --- Document title ---
    title_para = P(stylename="DocTitle")
    title_para.addText("Annotated Bibliography")
    doc.text.addElement(title_para)

    # Subtitle / description
    subtitle_para = P(stylename="Subtitle")
    subtitle_para.addText("Natural Language Processing — Foundational Papers")
    doc.text.addElement(subtitle_para)

    # Blank line
    doc.text.addElement(P())

    # "References" heading
    refs_heading = P(stylename="SectionHeading")
    refs_heading.addText("References")
    doc.text.addElement(refs_heading)

    doc.text.addElement(P())

    # The 10 paper titles — PLAIN TEXT ONLY
    # No APA citations, no DOIs, no annotations (task requires agent to add these)
    papers = [
        "Attention Is All You Need",
        "BERT",
        "GPT-2",
        "GPT-3",
        "T5",
        "RoBERTa",
        "ELECTRA",
        "BART",
        "LLaMA",
        "Mistral 7B",
    ]

    for i, title in enumerate(papers, 1):
        entry_para = P(stylename="PaperEntry")
        entry_para.addText(f"{i}. {title}")
        doc.text.addElement(entry_para)

    # Blank lines before statistics section
    doc.text.addElement(P())
    doc.text.addElement(P())

    # "Bibliography Statistics" placeholder section
    stats_heading = P(stylename="SectionHeading")
    stats_heading.addText("Bibliography Statistics")
    doc.text.addElement(stats_heading)

    doc.text.addElement(P())

    placeholder = P(stylename="NormalText")
    placeholder.addText("[To be filled after completing all citations and annotations]")
    doc.text.addElement(placeholder)

    for item in [
        "Total references: [number]",
        "Date range of publications: [year] - [year]",
        "Most common venue: [venue name]",
        "Academic vs. industry author ratio: [ratio]",
    ]:
        item_para = P(stylename="NormalText")
        item_para.addText(f"- {item}")
        doc.text.addElement(item_para)

    # Save
    doc.save(OUTPUT)
    print(f"Initial file created: {OUTPUT}")

    # GUI-ready startup
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=3.0)
    launch_gui('google-chrome --new-window "https://www.crossref.org/"', delay_sec=2.0)
    print("GUI_READY: launched LibreOffice Writer and Chrome with DISPLAY=:0")


create_initial()
