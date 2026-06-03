"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’ve got a title page and a table of contents that shouldn’t be numbered, but everything after that needs regular Arabic page numbers. How do I make LibreOffice Writer start numbering with “1” on the third page and put that number smack in the middle of the footer?
Generated: 2025-09-10 13:02:57
Status: success
Model: azure-o3
Total Steps: 9
"""

import os
import zipfile
from lxml import etree
import traceback


def _get_rels_map(z):
    """Return a mapping from relationship Id -> Target for the main document."""
    rel_xml = z.read('word/_rels/document.xml.rels')
    rel_root = etree.fromstring(rel_xml)
    rels = {}
    for rel in rel_root.findall('.//{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
        rels[rel.get('Id')] = rel.get('Target')
    return rels


def _collect_sections(z, rels):
    """Extract section information (page-number settings & footer references)."""
    doc_xml = z.read('word/document.xml')
    root = etree.fromstring(doc_xml)
    ns = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    }
    sections = []
    for sect in root.xpath('//w:sectPr', namespaces=ns):
        info = {}
        pg = sect.find('w:pgNumType', namespaces=ns)
        info['start'] = pg.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}start') if pg is not None else None
        info['format'] = pg.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}format') if pg is not None else None
        info['footers'] = []
        for fr in sect.findall('w:footerReference', namespaces=ns):
            rid = fr.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
            if rid in rels:
                info['footers'].append('word/' + rels[rid])
        sections.append(info)
    return sections


def _footer_has_page_field(z, footer_path):
    """Check if a footer contains a PAGE field and whether it is centred."""
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    try:
        xml = z.read(footer_path)
        root = etree.fromstring(xml)

        def _check_paragraph_alignment(p_el):
            pPr = p_el.find('w:pPr', namespaces=ns)
            if pPr is not None:
                jc = pPr.find('w:jc', namespaces=ns)
                if jc is not None and jc.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val') == 'center':
                    return True
            return False

        # Simple field form
        for fld in root.findall('.//w:fldSimple', namespaces=ns):
            instr = fld.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}instr')
            if instr and 'PAGE' in instr.upper():
                p = fld.getparent()
                while p is not None and p.tag != '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p':
                    p = p.getparent()
                return True, _check_paragraph_alignment(p) if p is not None else False
        # Complex field form
        for instr in root.findall('.//w:instrText', namespaces=ns):
            if instr.text and 'PAGE' in instr.text.upper():
                p = instr.getparent()
                while p is not None and p.tag != '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p':
                    p = p.getparent()
                return True, _check_paragraph_alignment(p) if p is not None else False
        return False, False
    except KeyError:
        # footer file not present in archive (shouldn't happen)
        return False, False


def verify_writer_page_numbering(doc_path):
    """Verify LibreOffice Writer task:
       - first two pages unnumbered
       - regular Arabic numbering starts at 1 on third page
       - page number centred in footer
    Returns a progressive score 0.0 – 1.0.
    """
    print(f"Starting verification for: {doc_path}")

    if not os.path.exists(doc_path):
        print("✗ File not found.")
        print("REWARD: 0.0")
        return 0.0

    score = 0.0
    try:
        with zipfile.ZipFile(doc_path, 'r') as z:
            rels = _get_rels_map(z)
            sections = _collect_sections(z, rels)
            print(f"Document has {len(sections)} section(s)")

            # 1) Look for a section after the first one whose numbering restarts at 1
            restart_idx = None
            for idx, sect in enumerate(sections):
                if sect['start'] == '1':
                    restart_idx = idx
                    break

            if restart_idx is not None and restart_idx >= 1:
                score += 0.5  # Major requirement met
                print(f"✓ Page numbering restarts at 1 in section {restart_idx+1} (0.5 points)")
            else:
                print("✗ Proper page-number restart not found")

            # 2) Footer(s) contain a PAGE field
            all_footer_paths = set()
            for sect in sections:
                all_footer_paths.update(sect['footers'])
            # Also add any loose footers just in case
            all_footer_paths.update([f for f in z.namelist() if f.startswith('word/footer') and f.endswith('.xml')])

            page_field_found = False
            centred_found = False
            for fp in all_footer_paths:
                has_page, is_centred = _footer_has_page_field(z, fp)
                if has_page:
                    page_field_found = True
                    if is_centred:
                        centred_found = True
                    # once centred field found, we can stop
                    if centred_found:
                        break

            if page_field_found:
                score += 0.3
                print("✓ Page number field present in footer (0.3 points)")
            else:
                print("✗ No page number field detected in any footer")

            if centred_found:
                score += 0.2
                print("✓ Page number is centred in footer (0.2 points)")
            else:
                print("✗ Page number not centred in footer")

            final_score = min(score, 1.0)
            print(f"Final score: {final_score}")
            print(f"REWARD: {final_score}")
            return final_score
    except Exception as e:
        traceback.print_exc()
        print("REWARD: 0.0")
        return 0.0


if __name__ == "__main__":
    # Path to the document provided by the task
    DOC_PATH = "/home/user/ive_got_a_title_page_and_a_table_of_contents_that_shouldnt_be_numbered_but_everything_after_that_nee.docx"
    verify_writer_page_numbering(DOC_PATH)
