"""
Initial Setup: Create a Writer document with a section named 'Old_Notes'
Task ID: writer_fs_095
Domain: libreoffice_writer
The document has a named section 'Old_Notes' with gray background
and write protection, containing three paragraphs of text.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_fs_095'
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
    from odf.text import P, Section, H
    from odf.style import (
        Style, TextProperties, ParagraphProperties, SectionProperties,
    )

    doc = OpenDocumentText()

    # --- Heading style ---
    h1_style = Style(name="Heading1Custom", family="paragraph")
    h1_style.addElement(TextProperties(
        fontsize="18pt", fontweight="bold",
    ))
    h1_style.addElement(ParagraphProperties(margintop="0.2in", marginbottom="0.1in"))
    doc.automaticstyles.addElement(h1_style)

    # --- Section style with gray background ---
    sec_style = Style(name="SectOldNotes", family="section")
    sec_props = SectionProperties()
    sec_props.setAttribute("backgroundcolor", "#d0d0d0")
    sec_style.addElement(sec_props)
    doc.automaticstyles.addElement(sec_style)

    # --- Body text style ---
    body_style = Style(name="BodyText", family="paragraph")
    body_style.addElement(TextProperties(fontsize="12pt", fontname="Liberation Serif"))
    body_style.addElement(ParagraphProperties(marginbottom="0.08in"))
    doc.automaticstyles.addElement(body_style)

    # === Document content ===

    # Title
    h = H(outlinelevel=1, stylename=h1_style, text="Project Status Report")
    doc.text.addElement(h)

    # Intro paragraphs
    p1 = P(stylename=body_style, text=(
        "This document contains the current project status update for Q1 2025. "
        "All team leads are expected to review the information below and provide "
        "feedback by March 28, 2025."
    ))
    doc.text.addElement(p1)

    p2 = P(stylename=body_style, text=(
        "The engineering team has completed the migration to the new cloud "
        "infrastructure. Performance benchmarks show a 35% improvement in "
        "response times across all services."
    ))
    doc.text.addElement(p2)

    # --- Section 'Old_Notes' with protection and gray background ---
    section = Section(name="Old_Notes", stylename=sec_style)
    section.setAttribute("protected", "true")

    sp1 = P(stylename=body_style, text=(
        "Meeting with stakeholders on Feb 12 concluded that the legacy API "
        "endpoints should be deprecated by end of Q2. Migration documentation "
        "has been shared with all affected teams."
    ))
    sp2 = P(stylename=body_style, text=(
        "Budget allocation for the server upgrade was approved on Jan 30. "
        "The total approved amount is $142,500, which covers hardware procurement, "
        "installation, and three months of extended support."
    ))
    sp3 = P(stylename=body_style, text=(
        "Action items from the retrospective: (1) implement automated regression "
        "testing for the payment module, (2) schedule weekly sync meetings with "
        "the QA team, (3) update the deployment runbook with the new rollback "
        "procedures."
    ))
    section.addElement(sp1)
    section.addElement(sp2)
    section.addElement(sp3)
    doc.text.addElement(section)

    # Closing paragraph (outside the section)
    closing = P(stylename=body_style, text=(
        "Please direct any questions to the project management office at "
        "pmo@company.example.com."
    ))
    doc.text.addElement(closing)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup - open the document in Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
