"""
Initial Setup: Broken hyperlinks in reading_list.odt
Task ID: osworld_multi_apps_web_references_009
Domain: libreoffice_writer (ODT file with hyperlinks)

Creates a reading list document with 8 paper references, some URLs broken.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_references_009'
DOCUMENTS_DIR = f'{WORKDIR}/Documents'
OUTPUT = f'{DOCUMENTS_DIR}/reading_list.odt'


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
    # Ensure Documents directory exists
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)

    # Build ODT content using raw XML to support hyperlinks properly
    odt_content = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
    xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"
    xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
    xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0"
    xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0"
    xmlns:math="http://www.w3.org/1998/Math/MathML"
    xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0"
    xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0"
    xmlns:ooo="http://openoffice.org/2004/office"
    xmlns:ooow="http://openoffice.org/2004/writer"
    xmlns:oooc="http://openoffice.org/2004/calc"
    xmlns:dom="http://www.w3.org/2001/xml-events"
    xmlns:xforms="http://www.w3.org/2002/xforms"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:rpt="http://openoffice.org/2005/report"
    xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2"
    xmlns:xhtml="http://www.w3.org/1999/xhtml"
    xmlns:grddl="http://www.w3.org/2003/g/data-view#"
    xmlns:tableooo="http://openoffice.org/2009/table"
    xmlns:drawooo="http://openoffice.org/2010/draw"
    xmlns:calcext="urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0"
    xmlns:loext="urn:org:documentfoundation:names:experimental:ooxml-odf-interop:xmlns:field:1.0"
    xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0"
    xmlns:formx="urn:openoffice:names:experimental:ooxml-odf-interop:xmlns:form:1.0"
    xmlns:css3t="http://www.w3.org/TR/css3-text/"
    office:version="1.2">
  <office:automatic-styles>
    <style:style style:name="P1" style:family="paragraph" style:parent-style-name="Text_20_Body">
      <style:paragraph-properties fo:margin-bottom="0.1in"/>
    </style:style>
    <style:style style:name="P2" style:family="paragraph" style:parent-style-name="Heading_20_1">
    </style:style>
  </office:automatic-styles>
  <office:body>
    <office:text>
      <text:p text:style-name="Heading 1">Machine Learning Research Reading List</text:p>
      <text:p text:style-name="Text Body">A curated collection of seminal papers in deep learning and natural language processing. This list is maintained for research reference purposes.</text:p>
      <text:p text:style-name="Text Body"></text:p>
      <text:p text:style-name="Heading 2">Core References</text:p>
      <text:p text:style-name="Text Body">1. Vaswani, A. et al. (2017). Attention Is All You Need. <text:a xlink:type="simple" xlink:href="https://arxiv.org/abs/1706.03762">https://arxiv.org/abs/1706.03762</text:a></text:p>
      <text:p text:style-name="Text Body">2. Brown, T. et al. (2020). Language Models are Few-Shot Learners (GPT-3). <text:a xlink:type="simple" xlink:href="https://arxiv.org/abs/2001.08361">https://arxiv.org/abs/2001.08361</text:a></text:p>
      <text:p text:style-name="Text Body">3. Krizhevsky, A., Sutskever, I., &amp; Hinton, G. (2012). ImageNet Classification with Deep CNNs (AlexNet). <text:a xlink:type="simple" xlink:href="https://papers.nips.cc/paper/2012/hash/wrong-url.html">https://papers.nips.cc/paper/2012/hash/wrong-url.html</text:a></text:p>
      <text:p text:style-name="Text Body">4. Liu, Y. et al. (2019). RoBERTa: A Robustly Optimized BERT Pretraining Approach. <text:a xlink:type="simple" xlink:href="https://openreview.net/forum?id=HJzdEWY7">https://openreview.net/forum?id=HJzdEWY7</text:a></text:p>
      <text:p text:style-name="Text Body">5. Chen, T. &amp; Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. <text:a xlink:type="simple" xlink:href="https://dl.acm.org/doi/invalid/10.1145/wrong">https://dl.acm.org/doi/invalid/10.1145/wrong</text:a></text:p>
      <text:p text:style-name="Text Body">6. Devlin, J. et al. (2019). BERT: Pre-training of Deep Bidirectional Transformers. <text:a xlink:type="simple" xlink:href="https://aclanthology.org/N19-1423">https://aclanthology.org/N19-1423</text:a></text:p>
      <text:p text:style-name="Text Body">7. Duchi, J., Hazan, E., &amp; Singer, Y. (2011). Adaptive Subgradient Methods for Online Learning. <text:a xlink:type="simple" xlink:href="https://jmlr.org/papers/volume12/gone.html">https://jmlr.org/papers/volume12/gone.html</text:a></text:p>
      <text:p text:style-name="Text Body">8. Radford, A. et al. (2021). Learning Transferable Visual Models From Natural Language Supervision (CLIP). <text:a xlink:type="simple" xlink:href="https://arxiv.org/abs/2103.00020">https://arxiv.org/abs/2103.00020</text:a></text:p>
      <text:p text:style-name="Text Body"></text:p>
      <text:p text:style-name="Text Body">Note: Please verify all URLs are accessible before citing.</text:p>
    </office:text>
  </office:body>
</office:document-content>'''

    # Write ODT file using odfpy
    from odf.opendocument import OpenDocumentText, load
    from odf.style import Style, TextProperties, ParagraphProperties, ListLevelProperties
    from odf.text import P, Span, A, H
    from odf.namespaces import TEXTNS, XLINKNS

    doc = OpenDocumentText()

    # Define styles
    h1_style = Style(name="Heading 1", family="paragraph")
    h1_style.addElement(TextProperties(fontsize="16pt", fontweight="bold"))
    doc.automaticstyles.addElement(h1_style)

    h2_style = Style(name="Heading 2", family="paragraph")
    h2_style.addElement(TextProperties(fontsize="13pt", fontweight="bold"))
    doc.automaticstyles.addElement(h2_style)

    body_style = Style(name="Text Body", family="paragraph")
    body_style.addElement(ParagraphProperties(marginbottom="0.1in"))
    doc.automaticstyles.addElement(body_style)

    # Helper to add hyperlink paragraph
    def add_para_with_link(doc_body, prefix_text, url, display_url=None):
        if display_url is None:
            display_url = url
        p = P(stylename="Text Body")
        if prefix_text:
            p.addText(prefix_text + " ")
        link = A(stylename="Internet_20_Link", href=url)
        link.addText(display_url)
        p.addElement(link)
        doc_body.addElement(p)

    text = doc.text

    # Title
    h1 = H(outlinelevel=1)
    h1.addText("Machine Learning Research Reading List")
    text.addElement(h1)

    # Introduction
    intro = P(stylename="Text Body")
    intro.addText("A curated collection of seminal papers in deep learning and natural language processing. This list is maintained for research reference purposes.")
    text.addElement(intro)

    # Empty line
    text.addElement(P(stylename="Text Body"))

    # Subheading
    h2 = H(outlinelevel=2)
    h2.addText("Core References")
    text.addElement(h2)

    # Papers list
    # 1. Attention Is All You Need (working URL)
    add_para_with_link(text,
        "1. Vaswani, A. et al. (2017). Attention Is All You Need.",
        "https://arxiv.org/abs/1706.03762")

    # 2. GPT-3 (working URL)
    add_para_with_link(text,
        "2. Brown, T. et al. (2020). Language Models are Few-Shot Learners (GPT-3).",
        "https://arxiv.org/abs/2001.08361")

    # 3. AlexNet (BROKEN URL)
    add_para_with_link(text,
        "3. Krizhevsky, A., Sutskever, I., & Hinton, G. (2012). ImageNet Classification with Deep Convolutional Neural Networks (AlexNet).",
        "https://papers.nips.cc/paper/2012/hash/wrong-url.html")

    # 4. RoBERTa (working URL)
    add_para_with_link(text,
        "4. Liu, Y. et al. (2019). RoBERTa: A Robustly Optimized BERT Pretraining Approach.",
        "https://openreview.net/forum?id=HJzdEWY7")

    # 5. XGBoost (BROKEN URL)
    add_para_with_link(text,
        "5. Chen, T. & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System.",
        "https://dl.acm.org/doi/invalid/10.1145/wrong")

    # 6. BERT (working URL)
    add_para_with_link(text,
        "6. Devlin, J. et al. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.",
        "https://aclanthology.org/N19-1423")

    # 7. Adaptive Subgradient / AdaGrad (BROKEN URL)
    add_para_with_link(text,
        "7. Duchi, J., Hazan, E., & Singer, Y. (2011). Adaptive Subgradient Methods for Online Learning and Stochastic Optimization.",
        "https://jmlr.org/papers/volume12/gone.html")

    # 8. CLIP (working URL)
    add_para_with_link(text,
        "8. Radford, A. et al. (2021). Learning Transferable Visual Models From Natural Language Supervision (CLIP).",
        "https://arxiv.org/abs/2103.00020")

    # Empty line
    text.addElement(P(stylename="Text Body"))

    # Footer note
    note = P(stylename="Text Body")
    note.addText("Note: Please verify all URLs are accessible before citing.")
    text.addElement(note)

    doc.save(OUTPUT)
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup: open the ODT file in LibreOffice Writer
    # Also open Chrome so it's ready for URL verification
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    launch_gui('google-chrome', delay_sec=1.5)
    print('GUI_READY: launched LibreOffice Writer and Chrome with DISPLAY=:0')


create_initial()
