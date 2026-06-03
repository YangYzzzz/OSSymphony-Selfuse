"""
Initial Setup: Reminder doc update - style guide and assignment draft
Task ID: osworld_multi_apps_reminder_doc_update_writer_002
Domain: libreoffice_writer

Creates:
  - /home/user/Desktop/style_guide.odt  — checklist with 2 formatting rules
  - /home/user/Desktop/assignment_draft.odt — draft with single spacing & black headings
Then opens both files in LibreOffice Writer.
"""

import os
import shlex
import subprocess
import time

from odf.opendocument import OpenDocumentText
from odf.style import (
    Style, TextProperties, ParagraphProperties,
)
from odf.text import H, P

DESKTOP = '/home/user/Desktop'
STYLE_GUIDE = f'{DESKTOP}/style_guide.odt'
ASSIGNMENT_DRAFT = f'{DESKTOP}/assignment_draft.odt'


def launch_gui(command: str, delay_sec: float = 1.5):
    """Launch a GUI application on the VM display without blocking."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_style_guide():
    """Create style_guide.odt with a 2-item formatting checklist."""
    doc = OpenDocumentText()

    # ----- Styles -----
    # Title style
    title_style = Style(name="TitleStyle", family="paragraph")
    title_tp = TextProperties(fontsize="16pt", fontweight="bold")
    title_style.addElement(title_tp)
    doc.automaticstyles.addElement(title_style)

    # Body text style
    body_style = Style(name="BodyStyle", family="paragraph")
    body_tp = TextProperties(fontsize="12pt")
    body_style.addElement(body_tp)
    doc.automaticstyles.addElement(body_style)

    # Instruction style
    instr_style = Style(name="InstrStyle", family="paragraph")
    instr_tp = TextProperties(fontsize="12pt", fontstyle="italic")
    instr_style.addElement(instr_tp)
    doc.automaticstyles.addElement(instr_style)

    # Checklist item style
    item_style = Style(name="ItemStyle", family="paragraph")
    item_pp = ParagraphProperties(marginleft="0.50in", textindent="-0.25in")
    item_style.addElement(item_pp)
    item_tp2 = TextProperties(fontsize="12pt")
    item_style.addElement(item_tp2)
    doc.automaticstyles.addElement(item_style)

    # ----- Content -----
    # Title
    title_p = P(stylename="TitleStyle")
    title_p.addText("Assignment Formatting Style Guide")
    doc.text.addElement(title_p)

    # Subtitle / intro
    intro_p = P(stylename="InstrStyle")
    intro_p.addText("Please apply the following formatting rules to your assignment draft:")
    doc.text.addElement(intro_p)

    # Empty line
    doc.text.addElement(P())

    # Checklist items
    item1_p = P(stylename="ItemStyle")
    item1_p.addText("1.  Set line spacing to double throughout the document.")
    doc.text.addElement(item1_p)

    item2_p = P(stylename="ItemStyle")
    item2_p.addText("2.  Change all headings to dark blue (#003366).")
    doc.text.addElement(item2_p)

    # Empty line
    doc.text.addElement(P())

    # Note
    note_p = P(stylename="InstrStyle")
    note_p.addText("Note: Save the assignment draft after applying all changes.")
    doc.text.addElement(note_p)

    doc.save(STYLE_GUIDE)
    print(f"Style guide created: {STYLE_GUIDE}")


def create_assignment_draft():
    """
    Create assignment_draft.odt with:
    - Single line spacing (NOT double — agent must apply this)
    - Black headings (NOT dark blue — agent must apply this)
    - Realistic academic content (multiple headings and paragraphs)
    """
    doc = OpenDocumentText()

    # ----- Paragraph Styles -----
    # Single line spacing normal paragraph
    para_style = Style(name="NormalPara", family="paragraph")
    para_pp = ParagraphProperties(lineheight="100%")   # single spacing
    para_style.addElement(para_pp)
    para_tp = TextProperties(fontsize="12pt", color="#000000")
    para_style.addElement(para_tp)
    doc.automaticstyles.addElement(para_style)

    # Heading 1 — black, single spacing (NOT dark blue)
    h1_style = Style(name="AssignH1", family="paragraph", parentstylename="Heading 1")
    h1_pp = ParagraphProperties(lineheight="100%")
    h1_style.addElement(h1_pp)
    h1_tp = TextProperties(fontsize="16pt", fontweight="bold", color="#000000")
    h1_style.addElement(h1_tp)
    doc.automaticstyles.addElement(h1_style)

    # Heading 2 — black, single spacing
    h2_style = Style(name="AssignH2", family="paragraph", parentstylename="Heading 2")
    h2_pp = ParagraphProperties(lineheight="100%")
    h2_style.addElement(h2_pp)
    h2_tp = TextProperties(fontsize="14pt", fontweight="bold", color="#000000")
    h2_style.addElement(h2_tp)
    doc.automaticstyles.addElement(h2_style)

    # ----- Content -----
    # Title heading
    t = H(outlinelevel=1, stylename="AssignH1")
    t.addText("The Role of Renewable Energy in Modern Society")
    doc.text.addElement(t)

    # Section 1
    h_intro = H(outlinelevel=2, stylename="AssignH2")
    h_intro.addText("Introduction")
    doc.text.addElement(h_intro)

    p1 = P(stylename="NormalPara")
    p1.addText(
        "Renewable energy has emerged as one of the most critical topics in contemporary "
        "environmental policy and global economic planning. As fossil fuel reserves dwindle "
        "and climate change accelerates, governments and corporations worldwide are investing "
        "heavily in sustainable alternatives such as solar, wind, and hydroelectric power."
    )
    doc.text.addElement(p1)

    p2 = P(stylename="NormalPara")
    p2.addText(
        "This essay examines the current state of renewable energy adoption, explores the "
        "technological challenges that remain, and argues for a coordinated international "
        "approach to accelerating the energy transition."
    )
    doc.text.addElement(p2)

    # Section 2
    h_solar = H(outlinelevel=2, stylename="AssignH2")
    h_solar.addText("Solar Energy: Progress and Potential")
    doc.text.addElement(h_solar)

    p3 = P(stylename="NormalPara")
    p3.addText(
        "Solar photovoltaic technology has experienced remarkable growth over the past decade. "
        "The cost per kilowatt-hour of solar electricity has fallen by approximately 89% since "
        "2010, making it the cheapest source of electricity in history in many regions. "
        "Countries such as Germany, China, and the United States have led large-scale "
        "installations that now power millions of homes."
    )
    doc.text.addElement(p3)

    p4 = P(stylename="NormalPara")
    p4.addText(
        "Despite these advances, challenges related to energy storage and grid integration "
        "persist. Solar generation is intermittent by nature, producing power only when sunlight "
        "is available. Battery storage technologies, including lithium-ion and emerging "
        "solid-state batteries, are being developed to address this limitation."
    )
    doc.text.addElement(p4)

    # Section 3
    h_wind = H(outlinelevel=2, stylename="AssignH2")
    h_wind.addText("Wind Power and Offshore Development")
    doc.text.addElement(h_wind)

    p5 = P(stylename="NormalPara")
    p5.addText(
        "Wind energy is another pillar of the renewable transition. Onshore wind farms have "
        "proliferated across plains and highlands, while offshore installations harness the "
        "stronger and more consistent winds available over open water. The United Kingdom's "
        "Hornsea One project, completed in 2019, became the world's largest offshore wind farm, "
        "supplying electricity to over one million homes."
    )
    doc.text.addElement(p5)

    p6 = P(stylename="NormalPara")
    p6.addText(
        "Engineers continue to refine turbine design, increasing blade length and improving "
        "efficiency at lower wind speeds. Floating wind platforms now allow installation in "
        "deeper waters previously inaccessible to fixed-bottom turbines, significantly expanding "
        "the viable deployment area."
    )
    doc.text.addElement(p6)

    # Section 4
    h_policy = H(outlinelevel=2, stylename="AssignH2")
    h_policy.addText("Policy Frameworks and International Cooperation")
    doc.text.addElement(h_policy)

    p7 = P(stylename="NormalPara")
    p7.addText(
        "Effective policy is essential for driving the transition to renewable energy. "
        "Instruments such as feed-in tariffs, renewable portfolio standards, and carbon pricing "
        "mechanisms create economic incentives for clean energy investment. The Paris Agreement "
        "of 2015 established a global framework committing signatory nations to reduce greenhouse "
        "gas emissions and limit warming to well below 2°C."
    )
    doc.text.addElement(p7)

    p8 = P(stylename="NormalPara")
    p8.addText(
        "However, implementation varies widely. Developing nations often face financing barriers "
        "that prevent rapid deployment of renewable infrastructure, highlighting the need for "
        "international funding mechanisms and technology transfer agreements."
    )
    doc.text.addElement(p8)

    # Conclusion
    h_conc = H(outlinelevel=2, stylename="AssignH2")
    h_conc.addText("Conclusion")
    doc.text.addElement(h_conc)

    p9 = P(stylename="NormalPara")
    p9.addText(
        "Renewable energy represents both an environmental imperative and an economic opportunity. "
        "Continued innovation in storage, grid management, and policy design will be crucial to "
        "realizing its full potential. A collaborative, well-funded international effort offers "
        "the best path toward a sustainable and equitable energy future."
    )
    doc.text.addElement(p9)

    doc.save(ASSIGNMENT_DRAFT)
    print(f"Assignment draft created: {ASSIGNMENT_DRAFT}")


def main():
    os.makedirs(DESKTOP, exist_ok=True)

    create_style_guide()
    create_assignment_draft()

    # Open style_guide.odt first (it's referenced as the "reminder")
    launch_gui(f'libreoffice --writer "{STYLE_GUIDE}"', delay_sec=2.0)
    # Open assignment_draft.odt in a second Writer window
    launch_gui(f'libreoffice --writer "{ASSIGNMENT_DRAFT}"', delay_sec=2.0)

    print("GUI_READY: launched LibreOffice Writer with both ODT files (DISPLAY=:0)")


main()
