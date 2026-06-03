"""
Initial Setup: annual_budget_review.docx with 10 tracked changes
Task ID: writer_struct_070
Domain: libreoffice_writer

Creates a 7-page budget review document with 10 tracked changes:
  - Page 1: 'Fiscal Year 2024' -> 'Fiscal Year 2025' (to accept)
  - Page 2: '$2.5M' -> '$3.0M' (to reject)
  - Page 3: 'department head' -> 'division head' (to accept)
  - Page 4: '$500K' -> '$750K' (to reject)
  - Page 5: 'annual review' -> 'quarterly review' (to accept)
  - Pages 6-7: 5 more tracked changes (remain unresolved)
"""

import os
import shlex
import subprocess
import time
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_struct_070'
OUTPUT = f'{WORKDIR}/Desktop/annual_budget_review.docx'

# Ensure Desktop directory exists
os.makedirs(f'{WORKDIR}/Desktop', exist_ok=True)

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


def create_docx_with_tracked_changes():
    """
    Build the docx from scratch by constructing OOXML directly.
    We use python-docx to write the base structure then inject tracked change
    XML (w:ins / w:del) into the document body.
    """
    import zipfile
    import io

    # Word namespace
    W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    W14 = 'http://schemas.microsoft.com/office/word/2010/wordml'
    R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

    def w(tag):
        return f'{{{W}}}{tag}'

    # -----------------------------------------------------------------------
    # Helper: build a tracked-change paragraph block
    # A tracked deletion shows old text with w:del, insertion shows new text
    # with w:ins.  Both appear so the reader sees BOTH old and new.
    # Author / date are fixed for realism.
    # -----------------------------------------------------------------------
    AUTHOR = "James Mitchell"
    DATE   = "2025-01-15T09:30:00Z"
    rev_counter = [1]   # mutable counter

    def next_id():
        v = rev_counter[0]
        rev_counter[0] += 1
        return str(v)

    def make_rpr(bold=False, size_half=24):
        """Return a <w:rPr> element."""
        rpr = etree.Element(w('rPr'))
        if bold:
            b = etree.SubElement(rpr, w('b'))
        sz = etree.SubElement(rpr, w('sz'))
        sz.set(w('val'), str(size_half))
        szCs = etree.SubElement(rpr, w('szCs'))
        szCs.set(w('val'), str(size_half))
        return rpr

    def make_run(text, bold=False, size_half=24):
        r = etree.Element(w('r'))
        rpr = make_rpr(bold=bold, size_half=size_half)
        r.append(rpr)
        t = etree.SubElement(r, w('t'))
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        t.text = text
        return r

    def make_del_run(text, rev_id, bold=False, size_half=24):
        """w:del containing a w:delText run."""
        d = etree.Element(w('del'))
        d.set(w('id'), rev_id)
        d.set(w('author'), AUTHOR)
        d.set(w('date'), DATE)
        r = etree.SubElement(d, w('r'))
        rpr = make_rpr(bold=bold, size_half=size_half)
        r.append(rpr)
        dt = etree.SubElement(r, w('delText'))
        dt.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        dt.text = text
        return d

    def make_ins_run(text, rev_id, bold=False, size_half=24):
        """w:ins containing a normal run."""
        ins = etree.Element(w('ins'))
        ins.set(w('id'), rev_id)
        ins.set(w('author'), AUTHOR)
        ins.set(w('date'), DATE)
        r = make_run(text, bold=bold, size_half=size_half)
        ins.append(r)
        return ins

    def make_ppr(style='Normal', heading_level=None, page_break_before=False):
        ppr = etree.Element(w('pPr'))
        pstyle = etree.SubElement(ppr, w('pStyle'))
        if heading_level:
            pstyle.set(w('val'), f'Heading{heading_level}')
        else:
            pstyle.set(w('val'), style)
        if page_break_before:
            pb = etree.SubElement(ppr, w('pageBreakBefore'))
        return ppr

    def para(*children, style='Normal', heading_level=None, page_break_before=False):
        p = etree.Element(w('p'))
        p.append(make_ppr(style=style, heading_level=heading_level,
                          page_break_before=page_break_before))
        for ch in children:
            p.append(ch)
        return p

    def plain_para(text, style='Normal', heading_level=None, page_break_before=False, bold=False, size_half=24):
        return para(make_run(text, bold=bold, size_half=size_half),
                    style=style, heading_level=heading_level,
                    page_break_before=page_break_before)

    def page_break_para():
        """A paragraph whose only content is a page break run."""
        p = etree.Element(w('p'))
        r = etree.SubElement(p, w('r'))
        br = etree.SubElement(r, w('br'))
        br.set(w('type'), 'page')
        return p

    # -----------------------------------------------------------------------
    # Build document body paragraphs page by page
    # -----------------------------------------------------------------------
    body_children = []

    # === PAGE 1 ===
    # Heading with tracked change: 'Fiscal Year 2024' -> 'Fiscal Year 2025'
    body_children.append(plain_para(
        'Annual Budget Review',
        heading_level=1, bold=True, size_half=32
    ))
    body_children.append(plain_para(
        'Executive Summary',
        heading_level=2, bold=True, size_half=28
    ))
    # Tracked change paragraph: "Fiscal Year 2024" → "Fiscal Year 2025"
    p_p1 = etree.Element(w('p'))
    p_p1.append(make_ppr())
    p_p1.append(make_run('This budget report covers '))
    p_p1.append(make_del_run('Fiscal Year 2024', next_id()))
    p_p1.append(make_ins_run('Fiscal Year 2025', next_id()))
    p_p1.append(make_run(' financial performance and strategic allocations.'))
    body_children.append(p_p1)

    body_children.append(plain_para(
        'The organization achieved significant milestones in revenue generation, '
        'cost optimization, and capital investment during the reporting period. '
        'This document provides a comprehensive overview of financial activities '
        'across all business units and departments.'
    ))
    body_children.append(plain_para(
        'Key highlights include a 12% increase in total revenue, successful '
        'implementation of cost-reduction initiatives, and strategic investments '
        'in technology infrastructure to support future growth objectives.'
    ))
    body_children.append(plain_para(
        'Overall financial performance exceeded targets in Q1 and Q2, with minor '
        'shortfalls in Q3 due to supply chain disruptions. Q4 recovery was robust, '
        'positioning the organization well for the upcoming fiscal period.'
    ))
    body_children.append(page_break_para())

    # === PAGE 2 ===
    body_children.append(plain_para(
        'Revenue Overview',
        heading_level=2, bold=True, size_half=28
    ))
    body_children.append(plain_para(
        'Total revenue for the period reached $48.7M, driven by strong performance '
        'across the technology and services divisions. The breakdown by segment is '
        'presented in the following sections.'
    ))
    # Tracked change: '$2.5M' -> '$3.0M' (to REJECT)
    p_p2 = etree.Element(w('p'))
    p_p2.append(make_ppr())
    p_p2.append(make_run('The Research & Development division allocated '))
    p_p2.append(make_del_run('$2.5M', next_id()))
    p_p2.append(make_ins_run('$3.0M', next_id()))
    p_p2.append(make_run(
        ' toward innovation projects, representing a notable increase '
        'from the prior year allocation.'
    ))
    body_children.append(p_p2)

    body_children.append(plain_para(
        'Sales performance was particularly strong in the enterprise segment, '
        'contributing $18.2M to total revenues. The consumer segment added $14.1M, '
        'while professional services generated $10.9M.'
    ))
    body_children.append(plain_para(
        'International markets contributed $5.5M, reflecting a 22% year-over-year '
        'growth rate. North American revenues remained the dominant segment at $43.2M.'
    ))
    body_children.append(page_break_para())

    # === PAGE 3 ===
    body_children.append(plain_para(
        'Organizational Structure & Governance',
        heading_level=2, bold=True, size_half=28
    ))
    body_children.append(plain_para(
        'Budget approval authority is delegated according to established governance '
        'policies. Expenditures above $100K require executive-level sign-off, while '
        'routine operational budgets are managed at the departmental level.'
    ))
    # Tracked change: 'department head' -> 'division head' (to ACCEPT)
    p_p3 = etree.Element(w('p'))
    p_p3.append(make_ppr())
    p_p3.append(make_run('Each budget center is overseen by a designated '))
    p_p3.append(make_del_run('department head', next_id()))
    p_p3.append(make_ins_run('division head', next_id()))
    p_p3.append(make_run(
        ' who is responsible for monitoring expenditures and ensuring '
        'alignment with strategic objectives.'
    ))
    body_children.append(p_p3)

    body_children.append(plain_para(
        'The Finance Committee meets quarterly to review budget utilization reports, '
        'approve reallocations exceeding defined thresholds, and provide guidance on '
        'emerging financial risks and opportunities.'
    ))
    body_children.append(plain_para(
        'Internal audit processes were strengthened during the year, with two '
        'additional auditors joining the team. Cross-functional budget reviews now '
        'occur on a bi-monthly basis to improve visibility and accountability.'
    ))
    body_children.append(page_break_para())

    # === PAGE 4 ===
    body_children.append(plain_para(
        'Capital Expenditure Analysis',
        heading_level=2, bold=True, size_half=28
    ))
    body_children.append(plain_para(
        'Capital expenditures for the period totaled $8.3M, primarily invested in '
        'facility upgrades, IT infrastructure, and manufacturing equipment upgrades '
        'to improve operational efficiency.'
    ))
    # Tracked change: '$500K' -> '$750K' (to REJECT)
    p_p4 = etree.Element(w('p'))
    p_p4.append(make_ppr())
    p_p4.append(make_run('The Technology Upgrade Program received a capital budget of '))
    p_p4.append(make_del_run('$500K', next_id()))
    p_p4.append(make_ins_run('$750K', next_id()))
    p_p4.append(make_run(
        ', which was utilized for server infrastructure, network '
        'security enhancements, and cloud migration activities.'
    ))
    body_children.append(p_p4)

    body_children.append(plain_para(
        'Facility renovation projects consumed $2.1M of the capital budget, '
        'including upgrades to the main headquarters building and establishment '
        'of two new regional office locations.'
    ))
    body_children.append(plain_para(
        'Manufacturing equipment investments totaling $3.8M are expected to yield '
        'a 15% improvement in production efficiency within 18 months of installation, '
        'based on vendor performance specifications.'
    ))
    body_children.append(page_break_para())

    # === PAGE 5 ===
    body_children.append(plain_para(
        'Operational Budget Review',
        heading_level=2, bold=True, size_half=28
    ))
    body_children.append(plain_para(
        'Operational budgets were managed within approved parameters for the majority '
        'of the reporting period. Variance analysis identified several areas where '
        'spending deviated from plan by more than 5%.'
    ))
    # Tracked change: 'annual review' -> 'quarterly review' (to ACCEPT)
    p_p5 = etree.Element(w('p'))
    p_p5.append(make_ppr())
    p_p5.append(make_run(
        'The Finance Department recommends transitioning from an '
    ))
    p_p5.append(make_del_run('annual review', next_id()))
    p_p5.append(make_ins_run('quarterly review', next_id()))
    p_p5.append(make_run(
        ' cycle to improve responsiveness to business conditions and '
        'enable more timely budget adjustments.'
    ))
    body_children.append(p_p5)

    body_children.append(plain_para(
        'Human Resources costs represented 58% of total operational expenditure, '
        'consistent with prior year ratios. Staff headcount grew by 45 full-time '
        'equivalents, primarily in engineering and customer service roles.'
    ))
    body_children.append(plain_para(
        'Marketing expenditures increased 18% year-over-year, reflecting greater '
        'investment in digital channels and brand awareness campaigns targeting '
        'new market segments.'
    ))
    body_children.append(page_break_para())

    # === PAGE 6 ===
    body_children.append(plain_para(
        'Risk Management & Compliance',
        heading_level=2, bold=True, size_half=28
    ))
    body_children.append(plain_para(
        'The Risk Management framework was updated to incorporate emerging '
        'regulatory requirements and market risks identified through ongoing '
        'monitoring activities.'
    ))
    # Tracked change 6: 'compliance officer' -> 'risk director'
    p_p6a = etree.Element(w('p'))
    p_p6a.append(make_ppr())
    p_p6a.append(make_run('All compliance activities are coordinated by the '))
    p_p6a.append(make_del_run('compliance officer', next_id()))
    p_p6a.append(make_ins_run('risk director', next_id()))
    p_p6a.append(make_run(
        ', who reports directly to the Chief Financial Officer on a '
        'monthly basis regarding regulatory adherence.'
    ))
    body_children.append(p_p6a)

    body_children.append(plain_para(
        'Insurance coverage was reviewed and updated, resulting in a 3% premium '
        'reduction through consolidation of policies across multiple carriers. '
        'Total insurance costs for the period were $1.2M.'
    ))

    # Tracked change 7: '$4.2M' -> '$4.8M' (budget reserve)
    p_p6b = etree.Element(w('p'))
    p_p6b.append(make_ppr())
    p_p6b.append(make_run('The contingency reserve was maintained at '))
    p_p6b.append(make_del_run('$4.2M', next_id()))
    p_p6b.append(make_ins_run('$4.8M', next_id()))
    p_p6b.append(make_run(
        ', representing approximately 8.7% of total operational budget, '
        'in line with board-approved risk tolerance parameters.'
    ))
    body_children.append(p_p6b)

    body_children.append(plain_para(
        'Regulatory compliance costs increased by $280K due to new reporting '
        'requirements introduced in Q2. These costs are expected to stabilize '
        'in the following period as processes are optimized.'
    ))
    body_children.append(page_break_para())

    # === PAGE 7 ===
    body_children.append(plain_para(
        'Forward-Looking Budget Projections',
        heading_level=2, bold=True, size_half=28
    ))
    body_children.append(plain_para(
        'Based on current performance trends and strategic initiatives, the '
        'Finance Department has prepared forward-looking projections for the '
        'next 24-month period.'
    ))

    # Tracked change 8: 'conservative estimate' -> 'baseline forecast'
    p_p7a = etree.Element(w('p'))
    p_p7a.append(make_ppr())
    p_p7a.append(make_run('The '))
    p_p7a.append(make_del_run('conservative estimate', next_id()))
    p_p7a.append(make_ins_run('baseline forecast', next_id()))
    p_p7a.append(make_run(
        ' projects total revenue growth of 9-11% over the next fiscal year, '
        'assuming stable market conditions and execution of planned initiatives.'
    ))
    body_children.append(p_p7a)

    body_children.append(plain_para(
        'Capital investment requirements for the upcoming period are estimated '
        'at $10.5M, with major allocations toward digital transformation, '
        'expanded manufacturing capacity, and talent acquisition programs.'
    ))

    # Tracked change 9: '$15.2M' -> '$16.8M' (projected revenue)
    p_p7b = etree.Element(w('p'))
    p_p7b.append(make_ppr())
    p_p7b.append(make_run('Projected revenue for the Services division stands at '))
    p_p7b.append(make_del_run('$15.2M', next_id()))
    p_p7b.append(make_ins_run('$16.8M', next_id()))
    p_p7b.append(make_run(
        ', reflecting anticipated contract renewals and new customer '
        'acquisition targets for the upcoming fiscal period.'
    ))
    body_children.append(p_p7b)

    body_children.append(plain_para(
        'The board will review these projections at the upcoming strategic '
        'planning session, where final budget allocations for the next fiscal '
        'year will be approved and communicated to all budget holders.'
    ))

    # Tracked change 10: 'finance team' -> 'treasury department'
    p_p7c = etree.Element(w('p'))
    p_p7c.append(make_ppr())
    p_p7c.append(make_run('Detailed supporting analysis is available from the '))
    p_p7c.append(make_del_run('finance team', next_id()))
    p_p7c.append(make_ins_run('treasury department', next_id()))
    p_p7c.append(make_run(
        ' upon request. All projections are based on assumptions documented '
        'in the accompanying financial model appendix.'
    ))
    body_children.append(p_p7c)

    body_children.append(plain_para(
        'This report was prepared by the Corporate Finance team in collaboration '
        'with business unit finance partners. All figures are presented in USD '
        'and have been reviewed by external auditors for accuracy.'
    ))

    # -----------------------------------------------------------------------
    # Assemble the document XML
    # -----------------------------------------------------------------------
    # Build document.xml
    doc_el = etree.Element(
        w('document'),
        nsmap={
            'wpc': 'http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas',
            'cx': 'http://schemas.microsoft.com/office/drawing/2014/chartex',
            'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
            'aink': 'http://schemas.microsoft.com/office/drawing/2016/ink',
            'am3d': 'http://schemas.microsoft.com/office/drawing/2017/model3d',
            'o': 'urn:schemas-microsoft-com:office:office',
            'oel': 'http://schemas.microsoft.com/office/2019/extlst',
            'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
            'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
            'v': 'urn:schemas-microsoft-com:vml',
            'wp14': 'http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing',
            'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
            'w10': 'urn:schemas-microsoft-com:office:word',
            'w': W,
            'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
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
    )
    body_el = etree.SubElement(doc_el, w('body'))
    for ch in body_children:
        body_el.append(ch)

    # sectPr
    sect = etree.SubElement(body_el, w('sectPr'))
    pgSz = etree.SubElement(sect, w('pgSz'))
    pgSz.set(w('w'), '12240')
    pgSz.set(w('h'), '15840')
    pgMar = etree.SubElement(sect, w('pgMar'))
    pgMar.set(w('top'), '1440')
    pgMar.set(w('right'), '1440')
    pgMar.set(w('bottom'), '1440')
    pgMar.set(w('left'), '1440')
    pgMar.set(w('header'), '720')
    pgMar.set(w('footer'), '720')
    pgMar.set(w('gutter'), '0')

    document_xml = etree.tostring(doc_el, xml_declaration=True,
                                   encoding='UTF-8', standalone=True)

    # -----------------------------------------------------------------------
    # Minimal styles.xml
    # -----------------------------------------------------------------------
    styles_xml = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
          xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="en-US"/>
      </w:rPr>
    </w:rPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:outlineLvl w:val="0"/>
    </w:pPr>
    <w:rPr>
      <w:b/>
      <w:sz w:val="32"/>
      <w:szCs w:val="32"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:outlineLvl w:val="1"/>
    </w:pPr>
    <w:rPr>
      <w:b/>
      <w:sz w:val="28"/>
      <w:szCs w:val="28"/>
    </w:rPr>
  </w:style>
</w:styles>'''

    # -----------------------------------------------------------------------
    # settings.xml — enable track changes recording
    # -----------------------------------------------------------------------
    settings_xml = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:trackChanges/>
  <w:defaultTabStop w:val="720"/>
  <w:rsids>
    <w:rsidDel w:val="00AB1234"/>
  </w:rsids>
</w:settings>'''

    # -----------------------------------------------------------------------
    # [Content_Types].xml
    # -----------------------------------------------------------------------
    content_types_xml = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml"
    ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml"
    ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/settings.xml"
    ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
</Types>'''

    # -----------------------------------------------------------------------
    # _rels/.rels
    # -----------------------------------------------------------------------
    rels_xml = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
    Target="word/document.xml"/>
</Relationships>'''

    # -----------------------------------------------------------------------
    # word/_rels/document.xml.rels
    # -----------------------------------------------------------------------
    doc_rels_xml = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles"
    Target="styles.xml"/>
  <Relationship Id="rId2"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings"
    Target="settings.xml"/>
</Relationships>'''

    # -----------------------------------------------------------------------
    # Write the zip (docx)
    # -----------------------------------------------------------------------
    with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types_xml)
        zf.writestr('_rels/.rels', rels_xml)
        zf.writestr('word/document.xml', document_xml)
        zf.writestr('word/styles.xml', styles_xml)
        zf.writestr('word/settings.xml', settings_xml)
        zf.writestr('word/_rels/document.xml.rels', doc_rels_xml)

    print(f'Initial file created: {OUTPUT}')
    print(f'Tracked changes embedded: 10 (5 pairs of del+ins)')
    print(f'Total revision IDs used: {rev_counter[0] - 1}')


def main():
    create_docx_with_tracked_changes()

    # GUI-ready startup: open the file in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


main()
