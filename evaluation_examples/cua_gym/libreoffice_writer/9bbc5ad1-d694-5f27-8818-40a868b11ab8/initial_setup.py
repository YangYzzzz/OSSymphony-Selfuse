"""
Initial Setup: Company policy document without conditional text fields
Task ID: writer_rd_073
Domain: libreoffice_writer

Creates a realistic company policy document in ODF format.
The header has plain text (no conditional content).
No user-defined variables exist.
"""

import os
import shlex
import subprocess
import time

from odf.opendocument import OpenDocumentText
from odf.text import P, H, Span, Section, List, ListItem
from odf.style import Style, TextProperties, ParagraphProperties, HeaderFooterProperties, MasterPage, PageLayout, PageLayoutProperties
from odf.draw import Frame, Image

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_073'
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
    doc = OpenDocumentText()

    # --- Styles ---
    # Title style
    title_style = Style(name="DocTitle", family="paragraph")
    title_style.addElement(TextProperties(
        fontsize="18pt", fontweight="bold", color="#1a3c6e"
    ))
    title_style.addElement(ParagraphProperties(textalign="center", marginbottom="0.3in"))
    doc.styles.addElement(title_style)

    # Heading style
    h1_style = Style(name="SectionHeading", family="paragraph")
    h1_style.addElement(TextProperties(
        fontsize="14pt", fontweight="bold", color="#2c5f8a"
    ))
    h1_style.addElement(ParagraphProperties(margintop="0.2in", marginbottom="0.1in"))
    doc.styles.addElement(h1_style)

    # Body style
    body_style = Style(name="BodyText", family="paragraph")
    body_style.addElement(TextProperties(fontsize="11pt", fontfamily="Liberation Serif"))
    body_style.addElement(ParagraphProperties(marginbottom="0.08in", textalign="justify"))
    doc.styles.addElement(body_style)

    # Bold inline style
    bold_style = Style(name="BoldText", family="text")
    bold_style.addElement(TextProperties(fontweight="bold"))
    doc.styles.addElement(bold_style)

    # Header style
    header_style = Style(name="HeaderStyle", family="paragraph")
    header_style.addElement(TextProperties(fontsize="9pt", fontstyle="italic", color="#666666"))
    header_style.addElement(ParagraphProperties(textalign="right"))
    doc.styles.addElement(header_style)

    # Footer style
    footer_style = Style(name="FooterStyle", family="paragraph")
    footer_style.addElement(TextProperties(fontsize="8pt", color="#999999"))
    footer_style.addElement(ParagraphProperties(textalign="center"))
    doc.styles.addElement(footer_style)

    # --- Page Layout with Header/Footer ---
    from odf.style import PageLayout as PL, PageLayoutProperties as PLP
    from odf.style import HeaderStyle as HS, FooterStyle as FS
    from odf.style import Header, Footer

    pl = PL(name="pm1")
    pl.addElement(PLP(
        pagewidth="8.5in", pageheight="11in",
        marginleft="1in", marginright="1in",
        margintop="1in", marginbottom="0.8in"
    ))
    # Header and footer properties
    hs = HS()
    hs.addElement(HeaderFooterProperties(minheight="0.3in", marginbottom="0.1in"))
    pl.addElement(hs)
    fs = FS()
    fs.addElement(HeaderFooterProperties(minheight="0.2in", margintop="0.1in"))
    pl.addElement(fs)
    doc.automaticstyles.addElement(pl)

    # Master page with header and footer
    mp = MasterPage(name="Standard", pagelayoutname="pm1")

    # Header - plain text, NO conditional content
    hdr = Header()
    hp = P(stylename=header_style)
    hp.addText("Meridian Technologies Inc. - Policy Document")
    hdr.addElement(hp)
    mp.addElement(hdr)

    # Footer
    ftr = Footer()
    fp = P(stylename=footer_style)
    fp.addText("Confidential - Meridian Technologies Inc. - 2025")
    ftr.addElement(fp)
    mp.addElement(ftr)

    doc.masterstyles.addElement(mp)

    # --- Document Body ---

    # Title
    title = P(stylename=title_style)
    title.addText("Meridian Technologies Inc.")
    doc.text.addElement(title)

    subtitle = P(stylename=title_style)
    subtitle.addText("Information Security Policy")
    doc.text.addElement(subtitle)

    # Effective date
    date_para = P(stylename=body_style)
    date_para.addText("Effective Date: January 15, 2025  |  Version 3.2  |  Last Reviewed: March 10, 2025")
    doc.text.addElement(date_para)

    # Blank separator
    doc.text.addElement(P())

    # Section 1: Purpose
    h1 = P(stylename=h1_style)
    h1.addText("1. Purpose and Scope")
    doc.text.addElement(h1)

    p1 = P(stylename=body_style)
    p1.addText(
        "This Information Security Policy establishes the framework for protecting "
        "Meridian Technologies' information assets, including intellectual property, "
        "client data, employee records, and proprietary software systems. This policy "
        "applies to all employees, contractors, consultants, and third-party partners "
        "who access company information systems or handle company data."
    )
    doc.text.addElement(p1)

    p1b = P(stylename=body_style)
    p1b.addText(
        "The scope of this policy covers all digital and physical information assets, "
        "including but not limited to: servers, workstations, mobile devices, cloud "
        "services, printed documents, and verbal communications containing sensitive "
        "information."
    )
    doc.text.addElement(p1b)

    # Section 2: Data Classification
    h2 = P(stylename=h1_style)
    h2.addText("2. Data Classification")
    doc.text.addElement(h2)

    p2 = P(stylename=body_style)
    p2.addText(
        "All information assets shall be classified into one of the following categories "
        "based on sensitivity and potential impact of unauthorized disclosure:"
    )
    doc.text.addElement(p2)

    classifications = [
        ("Public", "Information approved for unrestricted distribution, including marketing materials, press releases, and published research papers."),
        ("Internal", "Information intended for use within Meridian Technologies only. Includes internal memos, project plans, and organizational charts."),
        ("Confidential", "Sensitive business information that could harm the company if disclosed. Includes financial reports, strategic plans, and client contracts."),
        ("Restricted", "Highly sensitive information requiring the strictest controls. Includes encryption keys, security audit results, and personally identifiable information (PII)."),
    ]

    for label, desc in classifications:
        cp = P(stylename=body_style)
        sp = Span(stylename=bold_style)
        sp.addText(f"{label}: ")
        cp.addElement(sp)
        cp.addText(desc)
        doc.text.addElement(cp)

    # Section 3: Access Control
    h3 = P(stylename=h1_style)
    h3.addText("3. Access Control")
    doc.text.addElement(h3)

    p3 = P(stylename=body_style)
    p3.addText(
        "Access to information systems and data must follow the principle of least "
        "privilege. Employees shall be granted access only to the resources necessary "
        "to perform their job functions. All access requests must be approved by the "
        "employee's direct manager and the Information Security team."
    )
    doc.text.addElement(p3)

    p3b = P(stylename=body_style)
    p3b.addText(
        "Multi-factor authentication (MFA) is mandatory for all remote access "
        "connections, administrator accounts, and systems containing Confidential "
        "or Restricted data. Password requirements include a minimum of 12 characters "
        "with a combination of uppercase, lowercase, numbers, and special characters."
    )
    doc.text.addElement(p3b)

    # Section 4: Incident Response
    h4 = P(stylename=h1_style)
    h4.addText("4. Incident Response")
    doc.text.addElement(h4)

    p4 = P(stylename=body_style)
    p4.addText(
        "All security incidents must be reported to the Security Operations Center "
        "(SOC) within 30 minutes of detection. The incident response team, led by "
        "Chief Information Security Officer Elena Rodriguez, will coordinate "
        "containment, investigation, and recovery efforts according to the Incident "
        "Response Plan (IRP-2025-v2)."
    )
    doc.text.addElement(p4)

    p4b = P(stylename=body_style)
    p4b.addText(
        "Post-incident reviews shall be conducted within five business days following "
        "incident resolution. Findings and lessons learned will be documented and used "
        "to update security controls and training materials."
    )
    doc.text.addElement(p4b)

    # Section 5: Acceptable Use
    h5 = P(stylename=h1_style)
    h5.addText("5. Acceptable Use")
    doc.text.addElement(h5)

    p5 = P(stylename=body_style)
    p5.addText(
        "Company-provided equipment and network resources are to be used primarily "
        "for business purposes. Limited personal use is permitted provided it does not "
        "interfere with job performance, consume excessive bandwidth, or violate any "
        "laws, regulations, or other company policies."
    )
    doc.text.addElement(p5)

    p5b = P(stylename=body_style)
    p5b.addText(
        "The following activities are strictly prohibited: installing unauthorized "
        "software, connecting personal storage devices without IT approval, sharing "
        "credentials, accessing or distributing illegal content, and attempting to "
        "circumvent security controls."
    )
    doc.text.addElement(p5b)

    # Section 6: Compliance
    h6 = P(stylename=h1_style)
    h6.addText("6. Compliance and Enforcement")
    doc.text.addElement(h6)

    p6 = P(stylename=body_style)
    p6.addText(
        "Compliance with this policy is mandatory. Violations may result in "
        "disciplinary action, up to and including termination of employment and "
        "legal proceedings. The Information Security team will conduct quarterly "
        "audits to ensure adherence to this policy."
    )
    doc.text.addElement(p6)

    # Signature block
    doc.text.addElement(P())
    sig1 = P(stylename=body_style)
    sig1.addText("Approved by:")
    doc.text.addElement(sig1)

    sig2 = P(stylename=body_style)
    sp2 = Span(stylename=bold_style)
    sp2.addText("David Park")
    sig2.addElement(sp2)
    sig2.addText(", Chief Technology Officer")
    doc.text.addElement(sig2)

    sig3 = P(stylename=body_style)
    sp3 = Span(stylename=bold_style)
    sp3.addText("Elena Rodriguez")
    sig3.addElement(sp3)
    sig3.addText(", Chief Information Security Officer")
    doc.text.addElement(sig3)

    sig4 = P(stylename=body_style)
    sig4.addText("Date: January 15, 2025")
    doc.text.addElement(sig4)

    # Save
    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
