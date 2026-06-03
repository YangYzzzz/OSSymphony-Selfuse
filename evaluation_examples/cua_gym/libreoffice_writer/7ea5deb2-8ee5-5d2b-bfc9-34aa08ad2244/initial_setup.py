"""
Initial Setup: Create Employee Handbook with 25 tracked changes showing markup view
Task ID: writer_rm_022
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
import zipfile
import shutil
import tempfile
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_022'
OUTPUT = f'{WORKDIR}/{TASK_ID}.docx'

WURI = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
RURI = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NSMAP = {'w': WURI, 'r': RURI}


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


def W(tag):
    return f'{{{WURI}}}{tag}'


def create_run(text, bold=False, italic=False, font_name=None, font_size=None):
    """Create a w:r element with optional formatting."""
    r = etree.SubElement(etree.Element('dummy'), W('r'))
    if bold or italic or font_name or font_size:
        rPr = etree.SubElement(r, W('rPr'))
        if bold:
            etree.SubElement(rPr, W('b'))
        if italic:
            etree.SubElement(rPr, W('i'))
        if font_name:
            rFonts = etree.SubElement(rPr, W('rFonts'))
            rFonts.set(W('ascii'), font_name)
            rFonts.set(W('hAnsi'), font_name)
        if font_size:
            sz = etree.SubElement(rPr, W('sz'))
            sz.set(W('val'), str(font_size * 2))  # half-points
    t = etree.SubElement(r, W('t'))
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = text
    return r


def create_paragraph(runs_data, heading_level=None, alignment=None):
    """Create a w:p element. runs_data is list of (text, kwargs) tuples."""
    p = etree.Element(W('p'))
    pPr = etree.SubElement(p, W('pPr'))

    if heading_level is not None:
        pStyle = etree.SubElement(pPr, W('pStyle'))
        pStyle.set(W('val'), f'Heading{heading_level}')

    if alignment:
        jc = etree.SubElement(pPr, W('jc'))
        jc.set(W('val'), alignment)

    for text, kwargs in runs_data:
        r = create_run(text, **kwargs)
        p.append(r)

    return p


def create_insertion(text, author, date, rev_id, bold=False, italic=False, font_name=None, font_size=None):
    """Create a tracked insertion (w:ins) element."""
    ins = etree.Element(W('ins'))
    ins.set(W('id'), str(rev_id))
    ins.set(W('author'), author)
    ins.set(W('date'), date)
    r = create_run(text, bold=bold, italic=italic, font_name=font_name, font_size=font_size)
    ins.append(r)
    return ins


def create_deletion(text, author, date, rev_id, bold=False, italic=False, font_name=None, font_size=None):
    """Create a tracked deletion (w:del) element."""
    del_elem = etree.Element(W('del'))
    del_elem.set(W('id'), str(rev_id))
    del_elem.set(W('author'), author)
    del_elem.set(W('date'), date)
    r = etree.SubElement(del_elem, W('r'))
    if bold or italic or font_name or font_size:
        rPr = etree.SubElement(r, W('rPr'))
        if bold:
            etree.SubElement(rPr, W('b'))
        if italic:
            etree.SubElement(rPr, W('i'))
        if font_name:
            rFonts = etree.SubElement(rPr, W('rFonts'))
            rFonts.set(W('ascii'), font_name)
            rFonts.set(W('hAnsi'), font_name)
        if font_size:
            sz = etree.SubElement(rPr, W('sz'))
            sz.set(W('val'), str(font_size * 2))
    dt = etree.SubElement(r, W('delText'))
    dt.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    dt.text = text
    return del_elem


def build_document_xml():
    """Build a complete document.xml with realistic Employee Handbook content and 25 tracked changes."""

    # Root element
    document = etree.Element(W('document'), nsmap=NSMAP)
    body = etree.SubElement(document, W('body'))

    authors = [
        'Sarah Mitchell',
        'James Rodriguez',
        'Emily Watson',
        'David Kim',
        'Rachel Foster'
    ]
    dates = [
        '2025-11-10T09:30:00Z',
        '2025-11-12T14:15:00Z',
        '2025-11-15T11:00:00Z',
        '2025-11-18T16:45:00Z',
        '2025-11-20T10:20:00Z'
    ]

    rev_id = 1

    # --- Title ---
    p = create_paragraph([('Meridian Technologies Inc.', {'bold': True, 'font_size': 24})], alignment='center')
    body.append(p)

    p = create_paragraph([('Employee Handbook', {'bold': True, 'font_size': 20})], alignment='center')
    body.append(p)

    p = create_paragraph([('Revised Edition — ', {'font_size': 12})])
    # TC1: Insertion - year updated
    ins = create_insertion('November 2025', authors[0], dates[0], rev_id, font_size=12)
    rev_id += 1
    p.append(ins)
    # TC2: Deletion - old year
    dl = create_deletion('March 2024', authors[0], dates[0], rev_id, font_size=12)
    rev_id += 1
    p.append(dl)
    body.append(p)

    # Blank line
    body.append(create_paragraph([('', {})]))

    # --- Section 1: Welcome ---
    body.append(create_paragraph([('1. Welcome to Meridian Technologies', {'bold': True, 'font_size': 16})], heading_level=1))

    p = create_paragraph([('Welcome to the Meridian Technologies team! We are committed to fostering a ', {})])
    # TC3: Insertion
    ins = create_insertion('collaborative and inclusive ', authors[1], dates[1], rev_id)
    rev_id += 1
    p.append(ins)
    # TC4: Deletion
    dl = create_deletion('productive ', authors[1], dates[1], rev_id)
    rev_id += 1
    p.append(dl)
    r = create_run('work environment where every employee can thrive and contribute to our shared success.', )
    p.append(r)
    body.append(p)

    p = create_paragraph([('Our mission is to deliver innovative software solutions that empower businesses worldwide. ', {})])
    # TC5: Insertion
    ins = create_insertion('We believe that our people are our greatest asset, and we invest in their growth and well-being.', authors[2], dates[2], rev_id)
    rev_id += 1
    p.append(ins)
    body.append(p)

    # --- Section 2: Employment Policies ---
    body.append(create_paragraph([('2. Employment Policies', {'bold': True, 'font_size': 16})], heading_level=1))

    body.append(create_paragraph([('2.1 Equal Opportunity', {'bold': True, 'font_size': 13})], heading_level=2))

    p = create_paragraph([('Meridian Technologies is an equal opportunity employer. We do not discriminate based on race, color, religion, sex, national origin, age, disability, or ', {})])
    # TC6: Insertion
    ins = create_insertion('genetic information, gender identity, sexual orientation, veteran status, ', authors[2], dates[2], rev_id)
    rev_id += 1
    p.append(ins)
    r = create_run('or any other protected characteristic under applicable law.')
    p.append(r)
    body.append(p)

    body.append(create_paragraph([('2.2 At-Will Employment', {'bold': True, 'font_size': 13})], heading_level=2))

    p = create_paragraph([('Employment with Meridian Technologies is ', {})])
    # TC7: Deletion
    dl = create_deletion('strictly ', authors[3], dates[3], rev_id)
    rev_id += 1
    p.append(dl)
    r = create_run('at-will. Either party may terminate the employment relationship at any time, with or without cause or notice, subject to applicable law.')
    p.append(r)
    body.append(p)

    body.append(create_paragraph([('2.3 Probationary Period', {'bold': True, 'font_size': 13})], heading_level=2))

    p = create_paragraph([('All new employees are subject to a ', {})])
    # TC8: Insertion - duration change
    ins = create_insertion('90-day', authors[0], dates[0], rev_id)
    rev_id += 1
    p.append(ins)
    # TC9: Deletion - old duration
    dl = create_deletion('60-day', authors[0], dates[0], rev_id)
    rev_id += 1
    p.append(dl)
    r = create_run(' probationary period during which performance and cultural fit will be evaluated.')
    p.append(r)
    body.append(p)

    # --- Section 3: Work Hours & Remote Work ---
    body.append(create_paragraph([('3. Work Hours and Remote Work Policy', {'bold': True, 'font_size': 16})], heading_level=1))

    p = create_paragraph([('Standard work hours are Monday through Friday, ', {})])
    # TC10: Insertion
    ins = create_insertion('8:00 AM to 5:00 PM', authors[3], dates[3], rev_id)
    rev_id += 1
    p.append(ins)
    # TC11: Deletion
    dl = create_deletion('9:00 AM to 6:00 PM', authors[3], dates[3], rev_id)
    rev_id += 1
    p.append(dl)
    r = create_run(' with a one-hour lunch break. Core hours during which all employees must be available are 10:00 AM to 3:00 PM.')
    p.append(r)
    body.append(p)

    # TC12: Full inserted paragraph
    p_ins = etree.Element(W('p'))
    pPr = etree.SubElement(p_ins, W('pPr'))
    ins_whole = create_insertion(
        'Eligible employees may work remotely up to three days per week, subject to manager approval. Remote work arrangements must be documented using the Remote Work Agreement form available on the HR portal.',
        authors[4], dates[4], rev_id
    )
    rev_id += 1
    p_ins.append(ins_whole)
    body.append(p_ins)

    # --- Section 4: Compensation & Benefits ---
    body.append(create_paragraph([('4. Compensation and Benefits', {'bold': True, 'font_size': 16})], heading_level=1))

    body.append(create_paragraph([('4.1 Salary Reviews', {'bold': True, 'font_size': 13})], heading_level=2))

    p = create_paragraph([('Salary reviews are conducted ', {})])
    # TC13: Insertion
    ins = create_insertion('annually in January', authors[0], dates[0], rev_id)
    rev_id += 1
    p.append(ins)
    # TC14: Deletion
    dl = create_deletion('bi-annually in January and July', authors[0], dates[0], rev_id)
    rev_id += 1
    p.append(dl)
    r = create_run('. Adjustments are based on individual performance, market conditions, and company financial performance.')
    p.append(r)
    body.append(p)

    body.append(create_paragraph([('4.2 Health Insurance', {'bold': True, 'font_size': 13})], heading_level=2))

    p = create_paragraph([('The company provides comprehensive health insurance coverage including medical, dental, and vision plans. ', {})])
    # TC15: Insertion
    ins = create_insertion('Coverage begins on the first day of the month following your start date. Dependents and domestic partners are also eligible for coverage.', authors[2], dates[2], rev_id)
    rev_id += 1
    p.append(ins)
    body.append(p)

    body.append(create_paragraph([('4.3 Retirement Plan', {'bold': True, 'font_size': 13})], heading_level=2))

    p = create_paragraph([('Meridian Technologies offers a 401(k) retirement savings plan with employer matching up to ', {})])
    # TC16: Insertion
    ins = create_insertion('6%', authors[1], dates[1], rev_id)
    rev_id += 1
    p.append(ins)
    # TC17: Deletion
    dl = create_deletion('4%', authors[1], dates[1], rev_id)
    rev_id += 1
    p.append(dl)
    r = create_run(' of eligible compensation. Employees are eligible to participate after completing 30 days of employment.')
    p.append(r)
    body.append(p)

    # --- Section 5: Leave Policies ---
    body.append(create_paragraph([('5. Leave Policies', {'bold': True, 'font_size': 16})], heading_level=1))

    body.append(create_paragraph([('5.1 Paid Time Off (PTO)', {'bold': True, 'font_size': 13})], heading_level=2))

    p = create_paragraph([('Full-time employees accrue PTO at the following rates:', {})])
    body.append(p)

    p = create_paragraph([('  • 0-2 years of service: ', {})])
    # TC18: Insertion
    ins = create_insertion('18 days', authors[4], dates[4], rev_id)
    rev_id += 1
    p.append(ins)
    # TC19: Deletion
    dl = create_deletion('15 days', authors[4], dates[4], rev_id)
    rev_id += 1
    p.append(dl)
    r = create_run(' per year')
    p.append(r)
    body.append(p)

    body.append(create_paragraph([('  • 3-5 years of service: 22 days per year', {})]))
    body.append(create_paragraph([('  • 6+ years of service: 28 days per year', {})]))

    body.append(create_paragraph([('5.2 Parental Leave', {'bold': True, 'font_size': 13})], heading_level=2))

    p = create_paragraph([('Meridian Technologies provides ', {})])
    # TC20: Insertion
    ins = create_insertion('16 weeks', authors[3], dates[3], rev_id)
    rev_id += 1
    p.append(ins)
    # TC21: Deletion
    dl = create_deletion('12 weeks', authors[3], dates[3], rev_id)
    rev_id += 1
    p.append(dl)
    r = create_run(' of paid parental leave for the birth or adoption of a child. This leave is available to all eligible employees regardless of gender.')
    p.append(r)
    body.append(p)

    # --- Section 6: Code of Conduct ---
    body.append(create_paragraph([('6. Code of Conduct', {'bold': True, 'font_size': 16})], heading_level=1))

    p = create_paragraph([('All employees are expected to maintain the highest standards of professional conduct. This includes but is not limited to:', {})])
    body.append(p)

    body.append(create_paragraph([('  • Treating all colleagues, clients, and partners with respect and dignity', {})]))

    # TC22: Inserted bullet
    p22 = etree.Element(W('p'))
    ins22 = create_insertion('  • Maintaining confidentiality of proprietary information and trade secrets', authors[2], dates[2], rev_id)
    rev_id += 1
    p22.append(ins22)
    body.append(p22)

    body.append(create_paragraph([('  • Avoiding conflicts of interest or the appearance thereof', {})]))
    body.append(create_paragraph([('  • Complying with all applicable laws, regulations, and company policies', {})]))

    # --- Section 7: Disciplinary Procedures ---
    body.append(create_paragraph([('7. Disciplinary Procedures', {'bold': True, 'font_size': 16})], heading_level=1))

    p = create_paragraph([('Disciplinary actions follow a progressive approach:', {})])
    body.append(p)

    p = create_paragraph([('  1. ', {})])
    # TC23: Insertion
    ins = create_insertion('Verbal counseling and documentation', authors[1], dates[1], rev_id)
    rev_id += 1
    p.append(ins)
    # TC24: Deletion
    dl = create_deletion('Verbal warning', authors[1], dates[1], rev_id)
    rev_id += 1
    p.append(dl)
    body.append(p)

    body.append(create_paragraph([('  2. Written warning with performance improvement plan', {})]))
    body.append(create_paragraph([('  3. Final written warning', {})]))
    body.append(create_paragraph([('  4. Termination of employment', {})]))

    # --- Section 8: Acknowledgment ---
    body.append(create_paragraph([('8. Acknowledgment', {'bold': True, 'font_size': 16})], heading_level=1))

    p = create_paragraph([('By signing below, I acknowledge that I have received and read the Meridian Technologies Employee Handbook. ', {})])
    # TC25: Insertion
    ins = create_insertion('I understand that this handbook is not a contract of employment and that the company reserves the right to modify these policies at any time with reasonable notice.', authors[4], dates[4], rev_id)
    rev_id += 1
    p.append(ins)
    body.append(p)

    body.append(create_paragraph([('', {})]))
    body.append(create_paragraph([('Employee Signature: _________________________    Date: _______________', {})]))
    body.append(create_paragraph([('', {})]))
    body.append(create_paragraph([('Manager Signature: __________________________    Date: _______________', {})]))

    print(f'Total tracked changes created: {rev_id - 1}')

    return document


def build_settings_xml(show_markup=True):
    """Build word/settings.xml. If show_markup=True, revisions are shown with markup."""
    settings = etree.Element(W('settings'), nsmap={'w': WURI})

    # Track revisions enabled
    etree.SubElement(settings, W('trackRevisions'))

    # Show markup view (default for initial)
    if show_markup:
        # When showing markup, we do NOT add revisionView or we set markup="1"
        # Default behavior shows all markup
        pass

    return settings


def build_content_types():
    """Build [Content_Types].xml"""
    CT = 'http://schemas.openxmlformats.org/package/2006/content-types'
    types = etree.Element('{%s}Types' % CT)

    etree.SubElement(types, '{%s}Default' % CT, Extension='rels', ContentType='application/vnd.openxmlformats-package.relationships+xml')
    etree.SubElement(types, '{%s}Default' % CT, Extension='xml', ContentType='application/xml')
    etree.SubElement(types, '{%s}Override' % CT, PartName='/word/document.xml', ContentType='application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml')
    etree.SubElement(types, '{%s}Override' % CT, PartName='/word/settings.xml', ContentType='application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml')
    etree.SubElement(types, '{%s}Override' % CT, PartName='/word/styles.xml', ContentType='application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml')

    return types


def build_rels():
    """Build _rels/.rels"""
    RELPKG = 'http://schemas.openxmlformats.org/package/2006/relationships'
    rels = etree.Element('{%s}Relationships' % RELPKG)
    etree.SubElement(rels, '{%s}Relationship' % RELPKG,
                     Id='rId1',
                     Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument',
                     Target='word/document.xml')
    return rels


def build_word_rels():
    """Build word/_rels/document.xml.rels"""
    RELPKG = 'http://schemas.openxmlformats.org/package/2006/relationships'
    rels = etree.Element('{%s}Relationships' % RELPKG)
    etree.SubElement(rels, '{%s}Relationship' % RELPKG,
                     Id='rId1',
                     Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings',
                     Target='settings.xml')
    etree.SubElement(rels, '{%s}Relationship' % RELPKG,
                     Id='rId2',
                     Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles',
                     Target='styles.xml')
    return rels


def build_styles_xml():
    """Build word/styles.xml with basic heading styles."""
    styles = etree.Element(W('styles'), nsmap={'w': WURI})

    # Normal style
    style = etree.SubElement(styles, W('style'))
    style.set(W('type'), 'paragraph')
    style.set(W('default'), '1')
    style.set(W('styleId'), 'Normal')
    name = etree.SubElement(style, W('name'))
    name.set(W('val'), 'Normal')
    rPr = etree.SubElement(style, W('rPr'))
    rFonts = etree.SubElement(rPr, W('rFonts'))
    rFonts.set(W('ascii'), 'Calibri')
    rFonts.set(W('hAnsi'), 'Calibri')
    sz = etree.SubElement(rPr, W('sz'))
    sz.set(W('val'), '22')  # 11pt

    # Heading1 style
    style1 = etree.SubElement(styles, W('style'))
    style1.set(W('type'), 'paragraph')
    style1.set(W('styleId'), 'Heading1')
    name1 = etree.SubElement(style1, W('name'))
    name1.set(W('val'), 'heading 1')
    basedOn1 = etree.SubElement(style1, W('basedOn'))
    basedOn1.set(W('val'), 'Normal')
    rPr1 = etree.SubElement(style1, W('rPr'))
    b1 = etree.SubElement(rPr1, W('b'))
    sz1 = etree.SubElement(rPr1, W('sz'))
    sz1.set(W('val'), '32')  # 16pt

    # Heading2 style
    style2 = etree.SubElement(styles, W('style'))
    style2.set(W('type'), 'paragraph')
    style2.set(W('styleId'), 'Heading2')
    name2 = etree.SubElement(style2, W('name'))
    name2.set(W('val'), 'heading 2')
    basedOn2 = etree.SubElement(style2, W('basedOn'))
    basedOn2.set(W('val'), 'Normal')
    rPr2 = etree.SubElement(style2, W('rPr'))
    b2 = etree.SubElement(rPr2, W('b'))
    sz2 = etree.SubElement(rPr2, W('sz'))
    sz2.set(W('val'), '26')  # 13pt

    return styles


def write_xml(element, filepath):
    """Write an XML element to a file."""
    tree = etree.ElementTree(element)
    tree.write(filepath, xml_declaration=True, encoding='UTF-8', standalone=True, pretty_print=True)


def create_initial():
    """Create the initial Employee Handbook .docx with tracked changes and markup view."""
    tmpdir = tempfile.mkdtemp()

    try:
        # Create directory structure
        os.makedirs(os.path.join(tmpdir, '_rels'))
        os.makedirs(os.path.join(tmpdir, 'word', '_rels'))

        # Generate XML components
        write_xml(build_content_types(), os.path.join(tmpdir, '[Content_Types].xml'))
        write_xml(build_rels(), os.path.join(tmpdir, '_rels', '.rels'))
        write_xml(build_word_rels(), os.path.join(tmpdir, 'word', '_rels', 'document.xml.rels'))
        write_xml(build_document_xml(), os.path.join(tmpdir, 'word', 'document.xml'))
        write_xml(build_settings_xml(show_markup=True), os.path.join(tmpdir, 'word', 'settings.xml'))
        write_xml(build_styles_xml(), os.path.join(tmpdir, 'word', 'styles.xml'))

        # Package as .docx (ZIP)
        with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zf:
            for dirpath, dirnames, filenames in os.walk(tmpdir):
                for fn in filenames:
                    full = os.path.join(dirpath, fn)
                    arcname = os.path.relpath(full, tmpdir)
                    zf.write(full, arcname)

        print(f'Initial file created: {OUTPUT}')

    finally:
        shutil.rmtree(tmpdir)

    # GUI-ready startup: open file in LibreOffice Writer
    launch_gui(f'libreoffice --writer "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched LibreOffice Writer with DISPLAY=:0')


create_initial()
