"""
Initial Setup: Accept all tracked changes in the document
Task ID: writer_struct_015
Domain: libreoffice_writer

Creates a 4-page book chapter with 6 tracked changes embedded in the OOXML:
  - 3 text insertions (shown in green, w:ins elements)
  - 3 deletions (shown in strikethrough red, w:del elements)
The agent must accept all changes via Edit > Track Changes > Accept All Changes.
"""

import os
import shlex
import subprocess
import time
import zipfile
import shutil
from io import BytesIO
from lxml import etree

WORKDIR = '/home/user/Desktop'
TASK_ID = 'edited_manuscript'
OUTPUT = f'{WORKDIR}/{TASK_ID}.docx'

# ── XML namespace constants ──────────────────────────────────────────────────
W  = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R  = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
W14 = 'http://schemas.microsoft.com/office/word/2010/wordml'

def qn(tag):
    """Expand a namespaced tag like 'w:p' → '{...ns...}p'."""
    ns = {
        'w':   W,
        'r':   R,
        'w14': W14,
    }
    prefix, local = tag.split(':')
    return f'{{{ns[prefix]}}}{local}'


def make_run(text, rpr_xml=None):
    """Build a <w:r> element with optional <w:rPr>."""
    r_el = etree.Element(qn('w:r'))
    if rpr_xml is not None:
        r_el.append(rpr_xml)
    t_el = etree.SubElement(r_el, qn('w:t'))
    t_el.text = text
    if text.startswith(' ') or text.endswith(' '):
        t_el.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    return r_el


def make_ins(text, author='Dr. Elena Vasquez', date='2025-03-12T14:22:00Z', rev_id='1'):
    """Build a <w:ins> tracked-insertion element."""
    ins = etree.Element(qn('w:ins'))
    ins.set(qn('w:id'), rev_id)
    ins.set(qn('w:author'), author)
    ins.set(qn('w:date'), date)
    # green rPr
    rpr = etree.Element(qn('w:rPr'))
    color = etree.SubElement(rpr, qn('w:color'))
    color.set(qn('w:val'), '00B050')
    ins.append(make_run(text, rpr))
    return ins


def make_del(text, author='Prof. Marcus Chen', date='2025-03-10T09:15:00Z', rev_id='10'):
    """Build a <w:del> tracked-deletion element (strikethrough red)."""
    del_el = etree.Element(qn('w:del'))
    del_el.set(qn('w:id'), rev_id)
    del_el.set(qn('w:author'), author)
    del_el.set(qn('w:date'), date)
    rpr = etree.Element(qn('w:rPr'))
    color = etree.SubElement(rpr, qn('w:color'))
    color.set(qn('w:val'), 'FF0000')
    dstrike = etree.SubElement(rpr, qn('w:dstrike'))
    # Inside w:del runs use w:delText
    r_el = etree.Element(qn('w:r'))
    r_el.append(rpr)
    dt = etree.SubElement(r_el, qn('w:delText'))
    dt.text = text
    if text.startswith(' ') or text.endswith(' '):
        dt.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    del_el.append(r_el)
    return del_el


def make_paragraph(body, style_id=None):
    """Append a new <w:p> to body and return it."""
    p = etree.SubElement(body, qn('w:p'))
    if style_id:
        ppr = etree.SubElement(p, qn('w:pPr'))
        pstyle = etree.SubElement(ppr, qn('w:pStyle'))
        pstyle.set(qn('w:val'), style_id)
    return p


def build_docx():
    """Build the .docx bytes with tracked changes embedded."""

    # ── Styles XML (minimal) ────────────────────────────────────────────────
    styles_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
        '          xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml">'
        '  <w:docDefaults>'
        '    <w:rPrDefault><w:rPr>'
        '      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
        '      <w:sz w:val="24"/>'
        '    </w:rPr></w:rPrDefault>'
        '  </w:docDefaults>'
        '  <w:style w:type="paragraph" w:styleId="Normal" w:default="1">'
        '    <w:name w:val="Normal"/>'
        '    <w:pPr><w:spacing w:after="160"/></w:pPr>'
        '  </w:style>'
        '  <w:style w:type="paragraph" w:styleId="Heading1">'
        '    <w:name w:val="heading 1"/>'
        '    <w:basedOn w:val="Normal"/>'
        '    <w:rPr><w:b/><w:sz w:val="32"/></w:rPr>'
        '  </w:style>'
        '  <w:style w:type="paragraph" w:styleId="Heading2">'
        '    <w:name w:val="heading 2"/>'
        '    <w:basedOn w:val="Normal"/>'
        '    <w:rPr><w:b/><w:sz w:val="28"/></w:rPr>'
        '  </w:style>'
        '</w:styles>'
    )

    # ── Settings XML — enable track changes ─────────────────────────────────
    settings_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '  <w:trackChanges/>'
        '  <w:rsids><w:rsidDel w:val="00A31234"/><w:rsidR w:val="00A31234"/></w:rsids>'
        '</w:settings>'
    )

    # ── document.xml body ───────────────────────────────────────────────────
    NSMAP = {
        'wpc': 'http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas',
        'cx':  'http://schemas.microsoft.com/office/drawing/2014/chartex',
        'mc':  'http://schemas.openxmlformats.org/markup-compatibility/2006',
        'aink':'http://schemas.microsoft.com/office/drawing/2016/ink',
        'am3d':'http://schemas.microsoft.com/office/drawing/2017/model3d',
        'o':   'urn:schemas-microsoft-com:office:office',
        'oel': 'http://schemas.microsoft.com/office/2019/extlst',
        'r':   'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'm':   'http://schemas.openxmlformats.org/officeDocument/2006/math',
        'v':   'urn:schemas-microsoft-com:vml',
        'wp14':'http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing',
        'wp':  'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
        'w10': 'urn:schemas-microsoft-com:office:word',
        'w':   W,
        'w14': W14,
        'w15': 'http://schemas.microsoft.com/office/word/2012/wordml',
        'w16cex': 'http://schemas.microsoft.com/office/word/2018/wordml/cex',
        'w16cid': 'http://schemas.microsoft.com/office/word/2016/wordml/cid',
        'w16': 'http://schemas.microsoft.com/office/word/2018/wordml',
        'w16sdtdh': 'http://schemas.microsoft.com/office/word/2020/wordml/sdtdatahash',
        'w16se': 'http://schemas.microsoft.com/office/word/2015/wordml/symex',
        'wpg': 'http://schemas.microsoft.com/office/word/2010/wordprocessingGroup',
        'wpi': 'http://schemas.microsoft.com/office/word/2010/wordprocessingInk',
        'wne': 'http://schemas.microsoft.com/office/word/2006/wordml',
        'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape',
    }

    root = etree.Element(f'{{{W}}}document', nsmap=NSMAP)
    body = etree.SubElement(root, qn('w:body'))

    # ── Chapter Title ────────────────────────────────────────────────────────
    p_title = make_paragraph(body, 'Heading1')
    p_title.append(make_run('Chapter 3: The Architecture of Memory'))

    # ── Author line ──────────────────────────────────────────────────────────
    p_author = make_paragraph(body)
    ppr = etree.SubElement(p_author, qn('w:pPr'))
    rpr_a = etree.SubElement(ppr, qn('w:rPr'))
    italic_a = etree.SubElement(rpr_a, qn('w:i'))
    p_author.append(make_run('Dr. Elena Vasquez, Department of Cognitive Neuroscience'))

    # ── Page break ──────────────────────────────────────────────────────────
    pb = etree.SubElement(body, qn('w:p'))
    pb_r = etree.SubElement(pb, qn('w:r'))
    pb_br = etree.SubElement(pb_r, qn('w:br'))
    pb_br.set(qn('w:type'), 'page')

    # ── Section 1 heading ───────────────────────────────────────────────────
    p_h2 = make_paragraph(body, 'Heading2')
    p_h2.append(make_run('3.1 Introduction to Hippocampal Function'))

    # ── Para 1 — contains INSERTION 1 ───────────────────────────────────────
    # Original: "The hippocampus plays a central role in encoding declarative memories."
    # Change: insert "and consolidating " before "declarative"
    p1 = make_paragraph(body)
    p1.append(make_run('The hippocampus plays a central role in encoding '))
    p1.append(make_ins('and consolidating ', rev_id='1'))
    p1.append(make_run('declarative memories, including both episodic '
                       'and semantic information. Located in the medial temporal lobe, '
                       'it serves as a critical gateway for information to enter '
                       'long-term storage.'))

    # ── Para 2 — contains DELETION 1 ────────────────────────────────────────
    # Original: "Early research by Scoville and Milner (1957) demonstrated, through the famous case
    #            of patient H.M., the critical nature of the hippocampus in forming new memories
    #            while leaving older memories relatively intact."
    # Change: delete "relatively "
    p2 = make_paragraph(body)
    p2.append(make_run(
        'Early research by Scoville and Milner (1957) demonstrated, through the '
        'famous case of patient H.M., the critical nature of the hippocampus in '
        'forming new memories while leaving older memories '
    ))
    p2.append(make_del('relatively ', rev_id='10',
                       author='Prof. Marcus Chen', date='2025-03-10T09:15:00Z'))
    p2.append(make_run('intact.'))

    # ── Para 3 ───────────────────────────────────────────────────────────────
    p3 = make_paragraph(body)
    p3.append(make_run(
        'Subsequent animal studies and advanced neuroimaging techniques have '
        'expanded our understanding substantially. The hippocampus does not act '
        'in isolation; it operates as part of a broader medial temporal lobe '
        'memory system that includes the entorhinal, perirhinal, and parahippocampal '
        'cortices.'
    ))

    # ── Page break ──────────────────────────────────────────────────────────
    pb2 = etree.SubElement(body, qn('w:p'))
    pb2_r = etree.SubElement(pb2, qn('w:r'))
    pb2_br = etree.SubElement(pb2_r, qn('w:br'))
    pb2_br.set(qn('w:type'), 'page')

    # ── Section 2 heading ───────────────────────────────────────────────────
    p_h2b = make_paragraph(body, 'Heading2')
    p_h2b.append(make_run('3.2 Synaptic Plasticity and Long-Term Potentiation'))

    # ── Para 4 — contains INSERTION 2 ───────────────────────────────────────
    # Insert "Hebbian " before "plasticity"
    p4 = make_paragraph(body)
    p4.append(make_run('Long-term potentiation (LTP) is widely regarded as the primary '
                       'cellular mechanism underlying synaptic '))
    p4.append(make_ins('Hebbian ', rev_id='2',
                       author='Dr. Elena Vasquez', date='2025-03-12T14:45:00Z'))
    p4.append(make_run(
        'plasticity in the hippocampus. First described by Bliss and Lømo in 1973, '
        'LTP refers to the long-lasting enhancement of synaptic transmission following '
        'high-frequency stimulation.'
    ))

    # ── Para 5 — contains DELETION 2 ────────────────────────────────────────
    # Delete "it is generally accepted that "
    p5 = make_paragraph(body)
    p5.append(make_run('While the precise molecular mechanisms remain an active area of research, '))
    p5.append(make_del('it is generally accepted that ', rev_id='11',
                       author='Prof. Marcus Chen', date='2025-03-10T10:30:00Z'))
    p5.append(make_run(
        'NMDA receptor activation is a critical trigger for LTP induction. '
        'AMPA receptor trafficking to the synapse then sustains the potentiated state, '
        'providing a molecular basis for memory storage.'
    ))

    # ── Para 6 ───────────────────────────────────────────────────────────────
    p6 = make_paragraph(body)
    p6.append(make_run(
        'The CREB transcription factor pathway links synaptic activity to gene '
        'expression, enabling the synthesis of new proteins required for late-phase '
        'LTP. This transition from early to late LTP corresponds to the consolidation '
        'of short-term into long-term memory at the cellular level.'
    ))

    # ── Page break ──────────────────────────────────────────────────────────
    pb3 = etree.SubElement(body, qn('w:p'))
    pb3_r = etree.SubElement(pb3, qn('w:r'))
    pb3_br = etree.SubElement(pb3_r, qn('w:br'))
    pb3_br.set(qn('w:type'), 'page')

    # ── Section 3 heading ───────────────────────────────────────────────────
    p_h2c = make_paragraph(body, 'Heading2')
    p_h2c.append(make_run('3.3 Memory Consolidation and Systems-Level Integration'))

    # ── Para 7 — contains INSERTION 3 ───────────────────────────────────────
    # Insert "gradual " before "systems"
    p7 = make_paragraph(body)
    p7.append(make_run(
        'The standard model of systems consolidation proposes that memories initially '
        'dependent on the hippocampus become gradually independent of it through '
    ))
    p7.append(make_ins('gradual ', rev_id='3',
                       author='Dr. Elena Vasquez', date='2025-03-12T15:10:00Z'))
    p7.append(make_run(
        'systems-level reorganization. Repeated reactivation of hippocampal-neocortical '
        'ensembles during sleep strengthens direct neocortical connections, eventually '
        'allowing the neocortex to store memories independently.'
    ))

    # ── Para 8 — contains DELETION 3 ────────────────────────────────────────
    # Delete "simply "
    p8 = make_paragraph(body)
    p8.append(make_run('This model, however, does not '))
    p8.append(make_del('simply ', rev_id='12',
                       author='Prof. Marcus Chen', date='2025-03-10T11:00:00Z'))
    p8.append(make_run(
        'account for episodic memories, which may remain hippocampus-dependent '
        'indefinitely. The multiple trace theory posits that each reactivation creates '
        'a new hippocampal trace, preserving the contextual richness of autobiographical '
        'memories throughout a lifetime.'
    ))

    # ── Para 9 ───────────────────────────────────────────────────────────────
    p9 = make_paragraph(body)
    p9.append(make_run(
        'Future research directions include the use of optogenetic tools to dissect '
        'the precise timing and sequence of hippocampal-neocortical dialogue during '
        'offline consolidation, and computational models that bridge cellular-level '
        'plasticity with network-level memory representations.'
    ))

    # ── Page break ──────────────────────────────────────────────────────────
    pb4 = etree.SubElement(body, qn('w:p'))
    pb4_r = etree.SubElement(pb4, qn('w:r'))
    pb4_br = etree.SubElement(pb4_r, qn('w:br'))
    pb4_br.set(qn('w:type'), 'page')

    # ── References heading ───────────────────────────────────────────────────
    p_ref = make_paragraph(body, 'Heading2')
    p_ref.append(make_run('References'))

    refs = [
        'Bliss, T. V. P., & Lømo, T. (1973). Long-lasting potentiation of synaptic '
        'transmission in the dentate area of the anaesthetized rabbit. '
        'Journal of Physiology, 232(2), 331–356.',

        'McClelland, J. L., McNaughton, B. L., & O\'Reilly, R. C. (1995). Why there '
        'are complementary learning systems in the hippocampus and neocortex: Insights '
        'from the successes and failures of connectionist models. '
        'Psychological Review, 102(3), 419–457.',

        'Nadel, L., & Moscovitch, M. (1997). Memory consolidation, retrograde amnesia '
        'and the hippocampal complex. Current Opinion in Neurobiology, 7(2), 217–227.',

        'Scoville, W. B., & Milner, B. (1957). Loss of recent memory after bilateral '
        'hippocampal lesions. Journal of Neurology, Neurosurgery & Psychiatry, 20(1), 11–21.',

        'Squire, L. R., & Alvarez, P. (1995). Retrograde amnesia and memory '
        'consolidation: A neurobiological perspective. '
        'Current Opinion in Neurobiology, 5(2), 169–177.',
    ]
    for ref in refs:
        pr = make_paragraph(body)
        ppr_r = etree.SubElement(pr, qn('w:pPr'))
        ind = etree.SubElement(ppr_r, qn('w:ind'))
        ind.set(qn('w:left'), '720')
        ind.set(qn('w:hanging'), '720')
        pr.append(make_run(ref))

    # ── Section properties (end of body) ────────────────────────────────────
    sect = etree.SubElement(body, qn('w:sectPr'))
    pgSz = etree.SubElement(sect, qn('w:pgSz'))
    pgSz.set(qn('w:w'), '12240')
    pgSz.set(qn('w:h'), '15840')
    pgMar = etree.SubElement(sect, qn('w:pgMar'))
    pgMar.set(qn('w:top'), '1440')
    pgMar.set(qn('w:right'), '1440')
    pgMar.set(qn('w:bottom'), '1440')
    pgMar.set(qn('w:left'), '1440')

    doc_xml = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)

    # ── .rels for document ───────────────────────────────────────────────────
    doc_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '  <Relationship Id="rId1"'
        '    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles"'
        '    Target="styles.xml"/>'
        '  <Relationship Id="rId2"'
        '    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings"'
        '    Target="settings.xml"/>'
        '</Relationships>'
    )

    # ── Package relationships ────────────────────────────────────────────────
    pkg_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '  <Relationship Id="rId1"'
        '    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"'
        '    Target="word/document.xml"/>'
        '</Relationships>'
    )

    # ── [Content_Types].xml ──────────────────────────────────────────────────
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '  <Default Extension="rels"'
        '    ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '  <Default Extension="xml" ContentType="application/xml"/>'
        '  <Override PartName="/word/document.xml"'
        '    ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '  <Override PartName="/word/styles.xml"'
        '    ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        '  <Override PartName="/word/settings.xml"'
        '    ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
        '</Types>'
    )

    # ── Assemble the .docx ZIP ───────────────────────────────────────────────
    buf = BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', pkg_rels)
        zf.writestr('word/document.xml', doc_xml)
        zf.writestr('word/_rels/document.xml.rels', doc_rels)
        zf.writestr('word/styles.xml', styles_xml)
        zf.writestr('word/settings.xml', settings_xml)
    return buf.getvalue()


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch a GUI app on the VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    os.makedirs(WORKDIR, exist_ok=True)
    docx_bytes = build_docx()
    with open(OUTPUT, 'wb') as f:
        f.write(docx_bytes)
    print(f'Initial file created: {OUTPUT}')
    # Open in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
