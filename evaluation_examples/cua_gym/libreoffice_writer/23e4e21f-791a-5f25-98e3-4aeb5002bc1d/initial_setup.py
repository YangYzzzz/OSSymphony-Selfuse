"""
Initial Setup: Contract with tracked changes from two authors
Task ID: writer_legal_055
Domain: libreoffice_writer

Creates a legal contract .docx with exactly 20 tracked changes:
  - 12 from 'Partner_Review' (5 del+ins pairs + 2 standalone ins)
  - 8 from 'Associate_Draft' (2 del+ins pairs + 2 standalone del + 2 standalone ins)
"""

import os
import shlex
import subprocess
import time
import zipfile
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_055'
OUTPUT = f'{WORKDIR}/{TASK_ID}.docx'

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NSMAP = {'w': W_NS, 'r': R_NS}


def launch_gui(command: str, delay_sec: float = 1.0):
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


rev_id_counter = [1]

def next_rev_id():
    val = rev_id_counter[0]
    rev_id_counter[0] += 1
    return str(val)


def make_run(text, bold=False, italic=False):
    """Create a w:r element with Times New Roman 12pt."""
    r = etree.SubElement(etree.Element('dummy'), f'{{{W_NS}}}r')
    rPr = etree.SubElement(r, f'{{{W_NS}}}rPr')
    rFonts = etree.SubElement(rPr, f'{{{W_NS}}}rFonts')
    rFonts.set(f'{{{W_NS}}}ascii', "Times New Roman")
    rFonts.set(f'{{{W_NS}}}hAnsi', "Times New Roman")
    sz = etree.SubElement(rPr, f'{{{W_NS}}}sz')
    sz.set(f'{{{W_NS}}}val', '24')  # 24 half-pts = 12pt
    szCs = etree.SubElement(rPr, f'{{{W_NS}}}szCs')
    szCs.set(f'{{{W_NS}}}val', '24')
    if bold:
        etree.SubElement(rPr, f'{{{W_NS}}}b')
    if italic:
        etree.SubElement(rPr, f'{{{W_NS}}}i')
    t = etree.SubElement(r, f'{{{W_NS}}}t')
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = text
    return r


def make_ins(text, author, date_str, bold=False):
    ins = etree.Element(f'{{{W_NS}}}ins')
    ins.set(f'{{{W_NS}}}id', next_rev_id())
    ins.set(f'{{{W_NS}}}author', author)
    ins.set(f'{{{W_NS}}}date', date_str)
    ins.append(make_run(text, bold=bold))
    return ins


def make_del(text, author, date_str, bold=False):
    del_elem = etree.Element(f'{{{W_NS}}}del')
    del_elem.set(f'{{{W_NS}}}id', next_rev_id())
    del_elem.set(f'{{{W_NS}}}author', author)
    del_elem.set(f'{{{W_NS}}}date', date_str)
    r = etree.SubElement(del_elem, f'{{{W_NS}}}r')
    rPr = etree.SubElement(r, f'{{{W_NS}}}rPr')
    rFonts = etree.SubElement(rPr, f'{{{W_NS}}}rFonts')
    rFonts.set(f'{{{W_NS}}}ascii', "Times New Roman")
    rFonts.set(f'{{{W_NS}}}hAnsi', "Times New Roman")
    sz = etree.SubElement(rPr, f'{{{W_NS}}}sz')
    sz.set(f'{{{W_NS}}}val', '24')
    szCs = etree.SubElement(rPr, f'{{{W_NS}}}szCs')
    szCs.set(f'{{{W_NS}}}val', '24')
    if bold:
        etree.SubElement(rPr, f'{{{W_NS}}}b')
    dt = etree.SubElement(r, f'{{{W_NS}}}delText')
    dt.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    dt.text = text
    return del_elem


def R(text, bold=False, italic=False):
    """Shorthand for a normal-run tuple."""
    return (text, bold, italic)


def make_para(items, alignment=None, spacing_after=200):
    p = etree.Element(f'{{{W_NS}}}p')
    pPr = etree.SubElement(p, f'{{{W_NS}}}pPr')
    if alignment:
        jc = etree.SubElement(pPr, f'{{{W_NS}}}jc')
        jc.set(f'{{{W_NS}}}val', alignment)
    if spacing_after is not None:
        sp = etree.SubElement(pPr, f'{{{W_NS}}}spacing')
        sp.set(f'{{{W_NS}}}after', str(spacing_after))
    for item in items:
        if isinstance(item, tuple):
            text, bold, italic = item
            p.append(make_run(text, bold=bold, italic=italic))
        else:
            # lxml Element (tracked change)
            p.append(item)
    return p


def create_initial():
    P = 'Partner_Review'
    A = 'Associate_Draft'
    pd = '2026-03-25T14:30:00Z'
    ad = '2026-03-20T09:15:00Z'

    body = etree.Element(f'{{{W_NS}}}body')

    # ═══ Title ═══
    body.append(make_para([R("PROFESSIONAL SERVICES AGREEMENT", True)], alignment='center', spacing_after=400))

    # ═══ Preamble ═══
    body.append(make_para([R("This Professional Services Agreement (the \"Agreement\") is entered into as of March 15, 2026, by and between:")]))

    # P-ins#6: standalone insertion "duly organized and "
    body.append(make_para([
        R("Meridian Technologies Inc., a corporation "),
        make_ins("duly organized and ", P, pd),
        R("existing under the laws of the State of Delaware (\"Client\"), and"),
    ]))

    # A-ins#3: standalone insertion "formerly known as Apex Solutions, "
    body.append(make_para([
        R("Sterling Consulting Group LLC, "),
        make_ins("formerly known as Apex Solutions, ", A, ad),
        R("a limited liability company organized under the laws of the State of New York (\"Consultant\")."),
    ]))

    # ═══ 1. SCOPE OF SERVICES ═══
    body.append(make_para([R("1. SCOPE OF SERVICES", True)], spacing_after=200))

    # P-del#1 "basic" + P-ins#1 "comprehensive"
    body.append(make_para([
        R("1.1 The Consultant shall provide "),
        make_del("basic", P, pd),
        make_ins("comprehensive", P, pd),
        R(" technology consulting services as described in Exhibit A attached hereto."),
    ]))

    # A-del#3: standalone deletion " at Consultant's discretion"
    body.append(make_para([
        R("1.2 Services shall be performed at the Client's principal office or such other locations as mutually agreed upon"),
        make_del(" at Consultant's discretion", A, ad),
        R("."),
    ]))

    body.append(make_para([R("1.3 The Consultant shall assign qualified personnel to perform the Services and shall ensure continuity of staffing throughout the engagement period.")]))

    # ═══ 2. COMPENSATION ═══
    body.append(make_para([R("2. COMPENSATION", True)], spacing_after=200))

    # P-del#2 "$150" + P-ins#2 "$200"
    body.append(make_para([
        R("2.1 Client shall pay Consultant at the rate of "),
        make_del("$150", P, pd),
        make_ins("$200", P, pd),
        R(" per hour for services rendered under this Agreement."),
    ]))

    body.append(make_para([R("2.2 All invoices shall be submitted on a monthly basis within fifteen (15) business days following the end of each calendar month.")]))

    # P-del#3 "sixty (60)" + P-ins#3 "thirty (30)"
    body.append(make_para([
        R("2.3 Payment shall be due within "),
        make_del("sixty (60)", P, pd),
        make_ins("thirty (30)", P, pd),
        R(" days of receipt of a proper invoice."),
    ]))

    body.append(make_para([R("2.4 Late payments shall accrue interest at the rate of one and one-half percent (1.5%) per month or the maximum rate permitted by law, whichever is less.")]))

    # ═══ 3. TERM AND TERMINATION ═══
    body.append(make_para([R("3. TERM AND TERMINATION", True)], spacing_after=200))

    # A-del#1 "one (1) year" + A-ins#1 "two (2) years"
    body.append(make_para([
        R("3.1 This Agreement shall commence on the Effective Date and continue for a period of "),
        make_del("one (1) year", A, ad),
        make_ins("two (2) years", A, ad),
        R(" unless terminated earlier in accordance with this Section."),
    ]))

    body.append(make_para([R("3.2 Either party may terminate this Agreement for cause upon thirty (30) days written notice if the other party materially breaches any provision of this Agreement.")]))

    body.append(make_para([R("3.3 Upon expiration of the initial term, this Agreement may be renewed by mutual written consent of both parties.")]))

    body.append(make_para([R("3.4 Upon termination, Consultant shall promptly deliver all work product completed to date and Client shall pay for all services rendered through the termination date.")]))

    # ═══ 4. CONFIDENTIALITY ═══
    body.append(make_para([R("4. CONFIDENTIALITY", True)], spacing_after=200))

    body.append(make_para([R("4.1 Each party agrees to maintain in strict confidence all Confidential Information received from the other party.")]))

    # P-del#4 "anyone" + P-ins#4 "any third party without prior written consent"
    body.append(make_para([
        R("4.2 Confidential Information shall not be disclosed to "),
        make_del("anyone", P, pd),
        make_ins("any third party without prior written consent", P, pd),
        R(" except as required by law or court order."),
    ]))

    # A-del#2 "five (5) years" + A-ins#2 "two (2) years"
    body.append(make_para([
        R("4.3 The obligations of confidentiality shall survive termination of this Agreement for a period of "),
        make_del("five (5) years", A, ad),
        make_ins("two (2) years", A, ad),
        R("."),
    ]))

    body.append(make_para([R("4.4 Confidential Information does not include information that is or becomes publicly available through no fault of the receiving party, or was independently developed without use of Confidential Information.")]))

    # ═══ 5. INTELLECTUAL PROPERTY ═══
    body.append(make_para([R("5. INTELLECTUAL PROPERTY", True)], spacing_after=200))

    # P-ins#7: standalone insertion (work-for-hire clause)
    body.append(make_para([
        R("5.1 All work product created by Consultant in the performance of Services shall be the exclusive property of the Client."),
        make_ins(" Such work product shall be deemed 'work made for hire' under applicable copyright law.", P, pd),
    ]))

    body.append(make_para([R("5.2 Consultant retains ownership of its pre-existing intellectual property and general knowledge, skills, and experience.")]))

    # A-del#4: standalone deletion "irrevocable, "
    body.append(make_para([
        R("5.3 Consultant hereby grants Client a perpetual, "),
        make_del("irrevocable, ", A, ad),
        R("royalty-free license to use any pre-existing IP incorporated into the deliverables."),
    ]))

    # ═══ 6. LIMITATION OF LIABILITY ═══
    body.append(make_para([R("6. LIMITATION OF LIABILITY", True)], spacing_after=200))

    body.append(make_para([R("6.1 In no event shall either party's total liability exceed the total fees paid under this Agreement during the preceding twelve (12) months.")]))

    body.append(make_para([R("6.2 Neither party shall be liable for any indirect, incidental, or consequential damages arising out of or related to this Agreement.")]))

    # ═══ 7. INDEMNIFICATION ═══
    body.append(make_para([R("7. INDEMNIFICATION", True)], spacing_after=200))

    body.append(make_para([R("7.1 Consultant shall indemnify and hold harmless Client from any claims arising from Consultant's negligence or willful misconduct in the performance of Services.")]))

    body.append(make_para([R("7.2 Client shall indemnify Consultant from claims arising from Client's use of deliverables in a manner inconsistent with the terms of this Agreement.")]))

    # ═══ 8. GENERAL PROVISIONS ═══
    body.append(make_para([R("8. GENERAL PROVISIONS", True)], spacing_after=200))

    # P-del#5 "California" + P-ins#5 "Delaware"
    body.append(make_para([
        R("8.1 This Agreement shall be governed by the laws of the State of "),
        make_del("California", P, pd),
        make_ins("Delaware", P, pd),
        R("."),
    ]))

    body.append(make_para([R("8.2 Any disputes arising under this Agreement shall be resolved through binding arbitration in the jurisdiction specified above.")]))

    body.append(make_para([R("8.3 This Agreement constitutes the entire agreement between the parties and supersedes all prior negotiations, representations, and agreements.")]))

    # A-ins#4: standalone insertion (affiliate assignment exception)
    body.append(make_para([
        R("8.4 Neither party may assign this Agreement without the prior written consent of the other party."),
        make_ins(" Notwithstanding the foregoing, Consultant may assign this Agreement to an affiliate without Client consent.", A, ad),
    ]))

    body.append(make_para([R("8.5 If any provision of this Agreement is held to be invalid or unenforceable, the remaining provisions shall continue in full force and effect.")]))

    # ═══ Signature Block ═══
    body.append(make_para([R("IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.")], spacing_after=400))

    body.append(make_para([R("_________________________________")]))
    body.append(make_para([R("Meridian Technologies Inc.")]))
    body.append(make_para([R("By: ________________________  Title: ________________________")]))

    body.append(make_para([R("")], spacing_after=200))

    body.append(make_para([R("_________________________________")]))
    body.append(make_para([R("Sterling Consulting Group LLC")]))
    body.append(make_para([R("By: ________________________  Title: ________________________")]))

    # ─── Build .docx ZIP ───
    document = etree.Element(f'{{{W_NS}}}document', nsmap=NSMAP)
    document.append(body)
    doc_xml = etree.tostring(document, xml_declaration=True, encoding='UTF-8', standalone=True)

    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>'''

    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

    word_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
</Relationships>'''

    with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/_rels/document.xml.rels', word_rels)
        zf.writestr('word/document.xml', doc_xml)

    print(f'Initial file created: {OUTPUT}')

    # ─── Verify counts ───
    tree = etree.fromstring(doc_xml)
    p_ins = len(tree.findall(f'.//{{{W_NS}}}ins[@{{{W_NS}}}author="{P}"]'))
    p_del = len(tree.findall(f'.//{{{W_NS}}}del[@{{{W_NS}}}author="{P}"]'))
    a_ins = len(tree.findall(f'.//{{{W_NS}}}ins[@{{{W_NS}}}author="{A}"]'))
    a_del = len(tree.findall(f'.//{{{W_NS}}}del[@{{{W_NS}}}author="{A}"]'))
    print(f'Partner_Review: {p_ins} ins + {p_del} del = {p_ins+p_del} total')
    print(f'Associate_Draft: {a_ins} ins + {a_del} del = {a_ins+a_del} total')
    print(f'Grand total: {p_ins+p_del+a_ins+a_del} tracked changes')

    assert p_ins + p_del == 12, f"Expected 12 Partner_Review changes, got {p_ins+p_del}"
    assert a_ins + a_del == 8, f"Expected 8 Associate_Draft changes, got {a_ins+a_del}"

    # ─── GUI startup ───
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
