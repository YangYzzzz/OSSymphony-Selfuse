"""
Initial Setup: Create a Writer document with six footnotes using default Footnote paragraph style.
Task ID: writer_bs_041
Domain: libreoffice_writer

The document contains a research report on renewable energy with 6 footnotes.
Footnotes use the default FootnoteText style: 10pt, no special indent or tab config.
The footnote number is followed by a space (default), NOT a period+tab.
"""

import os
import shlex
import subprocess
import time
import zipfile
import io
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_041'
OUTPUT = f'{WORKDIR}/{TASK_ID}.docx'

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NSMAP_WR = {'w': W, 'r': R_NS}


def qn(tag):
    prefix, local = tag.split(':')
    ns = {'w': W, 'r': R_NS}[prefix]
    return f'{{{ns}}}{local}'


# Body content: (text, optional_heading_style, optional_footnote_text)
BODY_CONTENT = [
    ("Advances in Renewable Energy Technology", "Heading1", None),

    ("Solar photovoltaic efficiency has increased dramatically over the past decade, "
     "with multi-junction cells now exceeding 47% conversion rates under laboratory "
     "conditions. Researchers at the Fraunhofer Institute have demonstrated that "
     "tandem perovskite-silicon architectures offer a commercially viable pathway to "
     "surpass the theoretical Shockley-Queisser limit for single-junction devices.",
     None,
     "According to the National Renewable Energy Laboratory (NREL) efficiency chart, updated March 2025."),

    ("Wind turbine capacity factors have improved substantially due to larger rotor "
     "diameters and taller hub heights, enabling economic viability in previously "
     "marginal wind resource areas. The latest generation of 15 MW offshore turbines "
     "features rotor diameters exceeding 230 meters, sweeping an area larger than "
     "six football pitches.",
     None,
     "Global Wind Energy Council, Annual Report 2024, pp. 34-38."),

    ("Battery energy storage systems have experienced a cost reduction of approximately "
     "89% since 2010, making grid-scale storage increasingly competitive with peaking "
     "gas plants. Lithium iron phosphate chemistry has emerged as the dominant technology "
     "for stationary applications owing to its superior cycle life and thermal stability.",
     None,
     "BloombergNEF, New Energy Outlook 2025, Chapter 4: Energy Storage."),

    ("Current Developments", "Heading2", None),

    ("Green hydrogen production via electrolysis is projected to reach cost parity "
     "with grey hydrogen by 2030 in regions with abundant renewable resources. "
     "Proton exchange membrane electrolysers have achieved stack efficiencies above "
     "80%, while alkaline systems benefit from lower capital expenditure per megawatt.",
     None,
     "International Energy Agency, Global Hydrogen Review 2025, Executive Summary."),

    ("Offshore floating wind platforms represent a breakthrough technology that could "
     "unlock wind resources in deep water areas previously inaccessible to fixed-bottom "
     "turbines. Semi-submersible and tension-leg platform designs have completed "
     "multi-year pilot programmes in the North Sea and off the coast of Portugal.",
     None,
     "European Wind Energy Association, Floating Offshore Wind Vision Statement, 2024."),

    ("Concentrated solar power with integrated thermal storage provides dispatchable "
     "renewable electricity, complementing the variable output of photovoltaic "
     "installations. Molten salt towers in the Atacama Desert now deliver capacity "
     "factors above 90%, rivalling conventional baseload generation.",
     None,
     "SolarPACES Task I, Annual Report on CSP Technology Status, December 2024."),
]


CT_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/footnotes.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
</Types>'''

ROOT_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

DOC_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes" Target="footnotes.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
</Relationships>'''


def launch_gui(command, delay_sec=1.0):
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def build_styles():
    """Build styles.xml with default FootnoteText (10pt, no indent, no tab)."""
    root = etree.Element(qn('w:styles'), nsmap=NSMAP_WR)

    # Normal
    s = etree.SubElement(root, qn('w:style'))
    s.set(qn('w:type'), 'paragraph')
    s.set(qn('w:default'), '1')
    s.set(qn('w:styleId'), 'Normal')
    etree.SubElement(s, qn('w:name')).set(qn('w:val'), 'Normal')
    rpr = etree.SubElement(s, qn('w:rPr'))
    sz = etree.SubElement(rpr, qn('w:sz'))
    sz.set(qn('w:val'), '24')  # 12pt default
    szcs = etree.SubElement(rpr, qn('w:szCs'))
    szcs.set(qn('w:val'), '24')

    # Heading1
    s = etree.SubElement(root, qn('w:style'))
    s.set(qn('w:type'), 'paragraph')
    s.set(qn('w:styleId'), 'Heading1')
    etree.SubElement(s, qn('w:name')).set(qn('w:val'), 'heading 1')
    etree.SubElement(s, qn('w:basedOn')).set(qn('w:val'), 'Normal')
    ppr = etree.SubElement(s, qn('w:pPr'))
    sp = etree.SubElement(ppr, qn('w:spacing'))
    sp.set(qn('w:before'), '240')
    sp.set(qn('w:after'), '120')
    rpr = etree.SubElement(s, qn('w:rPr'))
    etree.SubElement(rpr, qn('w:b'))
    sz = etree.SubElement(rpr, qn('w:sz'))
    sz.set(qn('w:val'), '36')  # 18pt
    szcs = etree.SubElement(rpr, qn('w:szCs'))
    szcs.set(qn('w:val'), '36')

    # Heading2
    s = etree.SubElement(root, qn('w:style'))
    s.set(qn('w:type'), 'paragraph')
    s.set(qn('w:styleId'), 'Heading2')
    etree.SubElement(s, qn('w:name')).set(qn('w:val'), 'heading 2')
    etree.SubElement(s, qn('w:basedOn')).set(qn('w:val'), 'Normal')
    ppr = etree.SubElement(s, qn('w:pPr'))
    sp = etree.SubElement(ppr, qn('w:spacing'))
    sp.set(qn('w:before'), '200')
    sp.set(qn('w:after'), '80')
    rpr = etree.SubElement(s, qn('w:rPr'))
    etree.SubElement(rpr, qn('w:b'))
    sz = etree.SubElement(rpr, qn('w:sz'))
    sz.set(qn('w:val'), '30')  # 15pt
    szcs = etree.SubElement(rpr, qn('w:szCs'))
    szcs.set(qn('w:val'), '30')

    # FootnoteText — DEFAULT: 10pt, no indent, no tab stop
    s = etree.SubElement(root, qn('w:style'))
    s.set(qn('w:type'), 'paragraph')
    s.set(qn('w:styleId'), 'FootnoteText')
    etree.SubElement(s, qn('w:name')).set(qn('w:val'), 'footnote text')
    etree.SubElement(s, qn('w:basedOn')).set(qn('w:val'), 'Normal')
    ppr = etree.SubElement(s, qn('w:pPr'))
    sp = etree.SubElement(ppr, qn('w:spacing'))
    sp.set(qn('w:after'), '0')
    sp.set(qn('w:line'), '240')
    sp.set(qn('w:lineRule'), 'auto')
    rpr = etree.SubElement(s, qn('w:rPr'))
    sz = etree.SubElement(rpr, qn('w:sz'))
    sz.set(qn('w:val'), '20')  # 10pt
    szcs = etree.SubElement(rpr, qn('w:szCs'))
    szcs.set(qn('w:val'), '20')

    # FootnoteReference
    s = etree.SubElement(root, qn('w:style'))
    s.set(qn('w:type'), 'character')
    s.set(qn('w:styleId'), 'FootnoteReference')
    etree.SubElement(s, qn('w:name')).set(qn('w:val'), 'footnote reference')
    rpr = etree.SubElement(s, qn('w:rPr'))
    etree.SubElement(rpr, qn('w:vertAlign')).set(qn('w:val'), 'superscript')

    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)


def build_footnotes(use_period_tab=False):
    """Build footnotes.xml. If use_period_tab=False, uses space after ref (default)."""
    root = etree.Element(qn('w:footnotes'), nsmap=NSMAP_WR)

    # Separators
    for fid, sep_type in [(0, 'separator'), (1, 'continuationSeparator')]:
        fn = etree.SubElement(root, qn('w:footnote'))
        fn.set(qn('w:type'), sep_type)
        fn.set(qn('w:id'), str(fid))
        p = etree.SubElement(fn, qn('w:p'))
        ppr = etree.SubElement(p, qn('w:pPr'))
        sp = etree.SubElement(ppr, qn('w:spacing'))
        sp.set(qn('w:after'), '0')
        sp.set(qn('w:line'), '240')
        sp.set(qn('w:lineRule'), 'auto')
        r = etree.SubElement(p, qn('w:r'))
        etree.SubElement(r, qn('w:' + sep_type))

    fn_id = 2
    for text, style, fn_text in BODY_CONTENT:
        if fn_text is None:
            continue
        fn = etree.SubElement(root, qn('w:footnote'))
        fn.set(qn('w:id'), str(fn_id))
        p = etree.SubElement(fn, qn('w:p'))

        ppr = etree.SubElement(p, qn('w:pPr'))
        etree.SubElement(ppr, qn('w:pStyle')).set(qn('w:val'), 'FootnoteText')

        # Footnote reference marker
        r_ref = etree.SubElement(p, qn('w:r'))
        rpr_ref = etree.SubElement(r_ref, qn('w:rPr'))
        etree.SubElement(rpr_ref, qn('w:rStyle')).set(qn('w:val'), 'FootnoteReference')
        etree.SubElement(r_ref, qn('w:footnoteRef'))

        if use_period_tab:
            # Period then tab
            r_p = etree.SubElement(p, qn('w:r'))
            t_p = etree.SubElement(r_p, qn('w:t'))
            t_p.text = '.'
            r_tab = etree.SubElement(p, qn('w:r'))
            etree.SubElement(r_tab, qn('w:tab'))
        else:
            # Default: just a space
            r_sp = etree.SubElement(p, qn('w:r'))
            t_sp = etree.SubElement(r_sp, qn('w:t'))
            t_sp.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
            t_sp.text = ' '

        # Footnote body text
        r_txt = etree.SubElement(p, qn('w:r'))
        t_txt = etree.SubElement(r_txt, qn('w:t'))
        t_txt.text = fn_text

        fn_id += 1

    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)


def build_document():
    """Build document.xml with body paragraphs and footnote references."""
    root = etree.Element(qn('w:document'), nsmap=NSMAP_WR)
    body = etree.SubElement(root, qn('w:body'))

    fn_id = 2
    for text, style, fn_text in BODY_CONTENT:
        p = etree.SubElement(body, qn('w:p'))
        if style:
            ppr = etree.SubElement(p, qn('w:pPr'))
            etree.SubElement(ppr, qn('w:pStyle')).set(qn('w:val'), style)
        r = etree.SubElement(p, qn('w:r'))
        t = etree.SubElement(r, qn('w:t'))
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        t.text = text

        if fn_text is not None:
            r_fn = etree.SubElement(p, qn('w:r'))
            rpr_fn = etree.SubElement(r_fn, qn('w:rPr'))
            etree.SubElement(rpr_fn, qn('w:rStyle')).set(qn('w:val'), 'FootnoteReference')
            fnr = etree.SubElement(r_fn, qn('w:footnoteReference'))
            fnr.set(qn('w:id'), str(fn_id))
            fn_id += 1

    # Section properties
    sp = etree.SubElement(body, qn('w:sectPr'))
    pgsz = etree.SubElement(sp, qn('w:pgSz'))
    pgsz.set(qn('w:w'), '12240')
    pgsz.set(qn('w:h'), '15840')
    pgmar = etree.SubElement(sp, qn('w:pgMar'))
    pgmar.set(qn('w:top'), '1440')
    pgmar.set(qn('w:right'), '1440')
    pgmar.set(qn('w:bottom'), '1440')
    pgmar.set(qn('w:left'), '1440')
    pgmar.set(qn('w:header'), '720')
    pgmar.set(qn('w:footer'), '720')
    pgmar.set(qn('w:gutter'), '0')

    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)


def build_settings():
    """Minimal settings.xml."""
    root = etree.Element(qn('w:settings'), nsmap=NSMAP_WR)
    etree.SubElement(root, qn('w:defaultTabStop')).set(qn('w:val'), '720')
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)


def create_initial():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', CT_XML)
        z.writestr('_rels/.rels', ROOT_RELS)
        z.writestr('word/_rels/document.xml.rels', DOC_RELS)
        z.writestr('word/styles.xml', build_styles())
        z.writestr('word/footnotes.xml', build_footnotes(use_period_tab=False))
        z.writestr('word/document.xml', build_document())
        z.writestr('word/settings.xml', build_settings())

    buf.seek(0)
    with open(OUTPUT, 'wb') as f:
        f.write(buf.read())
    print(f'Initial file created: {OUTPUT}')

    # GUI-ready startup
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
