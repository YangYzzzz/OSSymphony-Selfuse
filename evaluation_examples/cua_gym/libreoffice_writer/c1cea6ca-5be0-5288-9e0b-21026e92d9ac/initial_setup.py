"""
Initial Setup: Import styles from thesis_styles.odt into current document
Task ID: writer_bs_083
Domain: libreoffice_writer

Creates:
  /home/user/writer_bs_083.odt  - Main document with custom 'My Note' and 'My Quote' styles
  /home/user/thesis_styles.odt  - Source template with 'Thesis Heading', 'Thesis Body', modified 'Heading 1'
"""

import os
import shlex
import subprocess
import time

# ODF imports
from odf.opendocument import OpenDocumentText
from odf.style import (
    Style, TextProperties, ParagraphProperties, TabStop, TabStops
)
from odf.text import P, H, Span
from odf.draw import Frame, Image


WORKDIR = '/home/user'
TASK_ID = 'writer_bs_083'
OUTPUT_MAIN = f'{WORKDIR}/{TASK_ID}.odt'
OUTPUT_TEMPLATE = f'{WORKDIR}/thesis_styles.odt'


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


def create_main_document():
    """Create the main document with default styles + 'My Note' and 'My Quote' custom styles."""
    doc = OpenDocumentText()

    # --- Define custom paragraph style: 'My Note' ---
    # Indented, italic, smaller font, grey text - like a side note
    my_note_style = Style(name="My Note", family="paragraph")
    my_note_style.addElement(ParagraphProperties(
        marginleft="1.5cm",
        marginright="1.5cm",
        margintop="0.3cm",
        marginbottom="0.3cm",
    ))
    my_note_style.addElement(TextProperties(
        fontsize="10pt",
        fontsizecomplex="10pt",
        fontsizeasian="10pt",
        fontstyle="italic",
        fontstylecomplex="italic",
        fontstyleasian="italic",
        color="#666666",
    ))
    doc.styles.addElement(my_note_style)

    # --- Define custom paragraph style: 'My Quote' ---
    # Centered, larger font, serif, dark blue text - for block quotes
    my_quote_style = Style(name="My Quote", family="paragraph")
    my_quote_style.addElement(ParagraphProperties(
        textalign="center",
        marginleft="2cm",
        marginright="2cm",
        margintop="0.5cm",
        marginbottom="0.5cm",
        borderlinewidthbottom="0.018cm 0.018cm 0.018cm",
    ))
    my_quote_style.addElement(TextProperties(
        fontsize="12pt",
        fontsizecomplex="12pt",
        fontsizeasian="12pt",
        fontname="Times New Roman",
        color="#1a3c6e",
    ))
    doc.styles.addElement(my_quote_style)

    # --- Default Heading 1 style override (standard look) ---
    # We do NOT modify Heading 1 here; it stays at its ODF default.
    # The task requires the agent to import a modified Heading 1 from thesis_styles.odt.

    # --- Document content ---
    # Title area
    h1 = H(outlinelevel=1, text="Research Methodology Overview")
    doc.text.addElement(h1)

    p1 = P(text="This document outlines the research methodology used in our comprehensive study of urban transportation patterns across three metropolitan areas. The data collection period spanned from January 2024 through December 2025, covering seasonal variations in commuter behavior.")
    doc.text.addElement(p1)

    p2 = P(text="The primary research objectives included identifying peak congestion corridors, evaluating the effectiveness of recent infrastructure investments, and projecting future demand based on demographic trends.")
    doc.text.addElement(p2)

    # Use My Note style
    note1 = P(stylename=my_note_style, text="Note: All statistical analyses were performed using R version 4.3.2 with the tidyverse package suite. Significance levels were set at alpha = 0.05 unless otherwise specified.")
    doc.text.addElement(note1)

    h2 = H(outlinelevel=2, text="Data Collection Framework")
    doc.text.addElement(h2)

    p3 = P(text="Survey instruments were distributed to 4,500 households across the selected metropolitan areas. Response rates averaged 67.3%, yielding a final sample of 3,028 complete responses suitable for analysis.")
    doc.text.addElement(p3)

    p4 = P(text="Automated traffic counters were installed at 142 key intersections, recording vehicle counts, speed measurements, and classification data at 15-minute intervals throughout the study period.")
    doc.text.addElement(p4)

    # Use My Quote style
    quote1 = P(stylename=my_quote_style, text='"Transportation infrastructure investment decisions must be guided by empirical evidence rather than political convenience." - Dr. Elena Vasquez, Urban Planning Review, 2024')
    doc.text.addElement(quote1)

    p5 = P(text="Complementary data sources included GPS trajectory data from ride-sharing platforms (anonymized), municipal transit authority ridership records, and satellite imagery for parking utilization analysis.")
    doc.text.addElement(p5)

    h2b = H(outlinelevel=2, text="Analytical Methods")
    doc.text.addElement(h2b)

    p6 = P(text="We employed a mixed-methods approach combining quantitative spatial analysis with qualitative stakeholder interviews. Geographic Information Systems (GIS) mapping was used to visualize congestion patterns and identify spatial clusters of high-delay corridors.")
    doc.text.addElement(p6)

    # Another note
    note2 = P(stylename=my_note_style, text="Note: GIS processing was conducted using QGIS 3.34 with the Network Analysis Toolbox plugin for route optimization calculations.")
    doc.text.addElement(note2)

    p7 = P(text="Regression models were fitted to predict commute times based on distance, mode choice, time of day, and neighborhood density. Random forest classifiers achieved 84.7% accuracy in predicting mode choice from demographic and geographic features.")
    doc.text.addElement(p7)

    # Another quote
    quote2 = P(stylename=my_quote_style, text='"The shift toward multimodal transportation networks requires a fundamental rethinking of how we measure system performance." - Metropolitan Transit Commission Annual Report, 2025')
    doc.text.addElement(quote2)

    p8 = P(text="Preliminary findings suggest that infrastructure investments in dedicated bus lanes yielded a 23% reduction in average commute times along affected corridors, while cycling infrastructure improvements correlated with a 15% increase in non-motorized transport mode share.")
    doc.text.addElement(p8)

    doc.save(OUTPUT_MAIN)
    print(f"Main document created: {OUTPUT_MAIN}")


def create_thesis_styles_template():
    """Create thesis_styles.odt with 'Thesis Heading', 'Thesis Body', and a modified 'Heading 1'."""
    doc = OpenDocumentText()

    # --- Custom style: 'Thesis Heading' ---
    # Large, bold, dark red, serif font
    thesis_heading = Style(name="Thesis Heading", family="paragraph")
    thesis_heading.addElement(ParagraphProperties(
        textalign="center",
        margintop="1cm",
        marginbottom="0.5cm",
        keepwithnext="always",
    ))
    thesis_heading.addElement(TextProperties(
        fontsize="18pt",
        fontsizecomplex="18pt",
        fontsizeasian="18pt",
        fontweight="bold",
        fontweightcomplex="bold",
        fontweightasian="bold",
        fontname="Times New Roman",
        color="#8b0000",
    ))
    doc.styles.addElement(thesis_heading)

    # --- Custom style: 'Thesis Body' ---
    # Justified, 1.5 line spacing, first line indent, serif
    thesis_body = Style(name="Thesis Body", family="paragraph")
    thesis_body.addElement(ParagraphProperties(
        textalign="justify",
        textindent="1.27cm",
        margintop="0cm",
        marginbottom="0.2cm",
        lineheight="150%",
    ))
    thesis_body.addElement(TextProperties(
        fontsize="12pt",
        fontsizecomplex="12pt",
        fontsizeasian="12pt",
        fontname="Times New Roman",
        color="#000000",
    ))
    doc.styles.addElement(thesis_body)

    # --- Modified 'Heading 1' ---
    # Override default Heading 1: dark green, bold, underlined, larger
    heading1_mod = Style(name="Heading 1", family="paragraph")
    heading1_mod.addElement(ParagraphProperties(
        margintop="0.8cm",
        marginbottom="0.4cm",
        keepwithnext="always",
    ))
    heading1_mod.addElement(TextProperties(
        fontsize="20pt",
        fontsizecomplex="20pt",
        fontsizeasian="20pt",
        fontweight="bold",
        fontweightcomplex="bold",
        fontweightasian="bold",
        fontname="Times New Roman",
        color="#006400",
        textunderlinestyle="solid",
        textunderlinewidth="auto",
        textunderlinecolor="font-color",
    ))
    doc.styles.addElement(heading1_mod)

    # --- Sample content showing these styles in use ---
    h = P(stylename=thesis_heading, text="Sample Thesis Chapter Title")
    doc.text.addElement(h)

    b1 = P(stylename=thesis_body, text="This is a sample paragraph demonstrating the Thesis Body style. It features justified alignment with a first-line indent, 1.5 line spacing, and Times New Roman font at 12 points. These formatting choices follow the university's thesis submission guidelines.")
    doc.text.addElement(b1)

    h1 = H(outlinelevel=1, stylename=heading1_mod, text="Modified Heading 1 Example")
    doc.text.addElement(h1)

    b2 = P(stylename=thesis_body, text="Additional content under the modified heading demonstrates how the imported styles would appear in practice. The heading now uses dark green color with underline formatting.")
    doc.text.addElement(b2)

    doc.save(OUTPUT_TEMPLATE)
    print(f"Thesis styles template created: {OUTPUT_TEMPLATE}")


if __name__ == '__main__':
    create_main_document()
    create_thesis_styles_template()

    # Open the main document in LibreOffice Writer for the agent
    launch_gui(f'libreoffice --writer "{OUTPUT_MAIN}"', delay_sec=2.0)
    print(f'GUI_READY: launched LibreOffice Writer with {OUTPUT_MAIN}')
