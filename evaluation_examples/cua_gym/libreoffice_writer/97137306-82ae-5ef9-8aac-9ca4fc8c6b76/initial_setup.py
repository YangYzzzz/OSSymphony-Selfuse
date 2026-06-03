"""
Initial Setup: systematic_review.odt with two sections (Primary Studies + Secondary Sources)
Task ID: osworld_multi_apps_doi_resolve_writer_013
Domain: libreoffice_writer

Creates a systematic review document with:
- Table of Contents placeholder at the top
- Section 'Primary Studies' with 8 plain-text paper titles
- Section 'Secondary Sources' with 7 plain-text paper titles
- NO Chicago formatting, NO DOI links, NO abstracts, NO clickable ToC
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_doi_resolve_writer_013'
OUTPUT = f'{WORKDIR}/systematic_review.odt'


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
    from odf.text import H, P, Span, TableOfContent, TableOfContentSource, IndexTitleTemplate

    doc = OpenDocumentText()

    # Define styles
    # Heading 1 style
    h1_style = Style(name="Heading1", family="paragraph", parentstylename="Heading 1")
    doc.automaticstyles.addElement(h1_style)

    # Heading 2 style
    h2_style = Style(name="Heading2", family="paragraph", parentstylename="Heading 2")
    doc.automaticstyles.addElement(h2_style)

    # Normal paragraph style
    p_style = Style(name="TextBody", family="paragraph")
    tp = TextProperties(fontsize="12pt", fontfamily="Times New Roman")
    p_style.addElement(tp)
    doc.automaticstyles.addElement(p_style)

    # Bold style for section headings
    bold_style = Style(name="BoldHeading", family="paragraph")
    tp_bold = TextProperties(fontsize="14pt", fontweight="bold", fontfamily="Times New Roman")
    bold_style.addElement(tp_bold)
    doc.automaticstyles.addElement(bold_style)

    # ---- Title ----
    title_para = H(outlinelevel=1, stylename="Heading 1")
    title_para.addText("Systematic Review: Machine Learning in Healthcare")
    doc.text.addElement(title_para)

    # ---- Table of Contents Placeholder ----
    toc_heading = P(stylename="Heading 2")
    toc_heading.addText("Table of Contents")
    doc.text.addElement(toc_heading)

    toc_placeholder = P(stylename="Text Body")
    toc_placeholder.addText("[Table of Contents — to be generated]")
    doc.text.addElement(toc_placeholder)

    # Empty paragraph after ToC
    doc.text.addElement(P(stylename="Text Body"))

    # ---- Primary Studies Section ----
    primary_heading = H(outlinelevel=2, stylename="Heading 2")
    primary_heading.addText("Primary Studies")
    doc.text.addElement(primary_heading)

    primary_studies = [
        "Deep Learning for Early Detection of Diabetic Retinopathy in Fundus Photographs",
        "Predicting Hospital Readmission Using Convolutional Neural Networks on Electronic Health Records",
        "Transformer-Based Models for Clinical Named Entity Recognition in Medical Notes",
        "Federated Learning for Privacy-Preserving Predictive Modeling in Multi-Site Clinical Trials",
        "Graph Neural Networks for Drug-Drug Interaction Prediction in Polypharmacy Patients",
        "Explainable AI for Sepsis Prediction in Intensive Care Units: A Retrospective Cohort Study",
        "Natural Language Processing for Automated ICD-10 Coding from Discharge Summaries",
        "Multi-Modal Deep Learning for Breast Cancer Diagnosis Using Mammography and Ultrasound",
    ]

    for i, title in enumerate(primary_studies, 1):
        ref_para = P(stylename="Text Body")
        ref_para.addText(f"{i}. {title}")
        doc.text.addElement(ref_para)

    # Empty paragraph between sections
    doc.text.addElement(P(stylename="Text Body"))

    # ---- Secondary Sources Section ----
    secondary_heading = H(outlinelevel=2, stylename="Heading 2")
    secondary_heading.addText("Secondary Sources")
    doc.text.addElement(secondary_heading)

    secondary_sources = [
        "Machine Learning in Healthcare: A Systematic Review of Applications and Challenges",
        "Artificial Intelligence and the Future of Medicine: Trends, Challenges, and Opportunities",
        "Evaluating Clinical Decision Support Systems: A Framework for Assessing AI in Healthcare",
        "Regulatory Considerations for Artificial Intelligence in Medical Devices",
        "Bias and Fairness in Healthcare AI: Ethical Implications and Mitigation Strategies",
        "From Bench to Bedside: Translating AI Research into Clinical Practice",
        "Data Privacy and Security in Health Information Systems: A Comprehensive Review",
    ]

    for i, title in enumerate(secondary_sources, 1):
        ref_para = P(stylename="Text Body")
        ref_para.addText(f"{i}. {title}")
        doc.text.addElement(ref_para)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the file in LibreOffice Writer
    # Kill any existing LibreOffice processes first for idempotency
    subprocess.run(['pkill', '-f', 'soffice'], capture_output=True)
    time.sleep(1.0)

    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    # Also ensure Chrome is open (task mentions Chrome for DOI lookup)
    launch_gui('google-chrome --new-window', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer and Chrome with DISPLAY=:0')


create_initial()
