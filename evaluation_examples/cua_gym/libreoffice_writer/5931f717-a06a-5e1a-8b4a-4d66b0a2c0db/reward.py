"""
FINAL REWARD SCRIPT - SUCCESS
Task: My lab report starts with a cover, an abstract, and a table of contents—those first three pages stay blank. From the introduction (page 4) onward I need normal Arabic numbers, starting at 1 and sitting dead-center in the footer. Can you walk me through the exact steps in LibreOffice Writer to set that up so the earlier pages stay unnumbered?
Generated: 2025-09-10 12:14:16
Status: success
Model: azure-o3
Total Steps: 2
"""

import os
import zipfile
from lxml import etree

"""
Reward script for verifying LibreOffice Writer pagination task:
1. First three pages (cover, abstract, TOC) must remain unnumbered.
2. From page 4 (new section) numbering restarts at 1.
3. Page number appears in the footer, centred, using Arabic numerals.
   - Implemented in DOCX with a PAGE field in the second section’s footer.

Verification approach (progressive scoring):
• 0.4 – At least two sections exist (section break after page 3).
• 0.3 – Second section restarts numbering at 1 (pgNumType/@w:start = 1).
• 0.2 – Second-section footer contains a PAGE field that is centred.
• 0.1 – First-section footer contains NO page-number field.
Total adds to 1.0 only when every requirement passes.

The script parses the underlying XML of the DOCX file, avoiding any
hard-coded truths and granting points solely when real evidence is
found. It prints diagnostic messages for every check and finally prints
"REWARD: X.X".
"""

# XML namespaces used in DOCX
NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def _extract_xml(zipf: zipfile.ZipFile, name: str):
    """Helper to read and parse an XML part from the DOCX package."""
    with zipf.open(name) as fp:
        return etree.fromstring(fp.read())


def _build_rels_map(zipf: zipfile.ZipFile):
    """Return mapping of relationship IDs → part targets for document rels."""
    rels_map = {}
    try:
        rels_root = _extract_xml(zipf, "word/_rels/document.xml.rels")
        for rel in rels_root.xpath("//r:Relationship", namespaces={"r": "http://schemas.openxmlformats.org/package/2006/relationships"}):
            rels_map[rel.get("Id")] = rel.get("Target")
    except KeyError:
        # relationships part missing (highly unusual) – leave map empty
        pass
    return rels_map


def _load_footer(zipf: zipfile.ZipFile, rels_map: dict, rid: str):
    """Given a relationship id, return parsed footer XML or None."""
    target = rels_map.get(rid)
    if not target:
        return None
    path = target if target.startswith("word/") else f"word/{target}"
    try:
        return _extract_xml(zipf, path)
    except KeyError:
        return None


def verify_pagination(file_path: str) -> float:
    print(f"Verifying file: {file_path}")

    if not os.path.exists(file_path):
        print("✗ File not found")
        return 0.0

    # Try opening the DOCX package
    try:
        docx_zip = zipfile.ZipFile(file_path)
    except Exception as e:
        print(f"✗ Unable to open DOCX: {e}")
        return 0.0

    # Load main document XML
    try:
        document_xml = _extract_xml(docx_zip, "word/document.xml")
    except KeyError:
        print("✗ word/document.xml missing in package")
        return 0.0

    sections = document_xml.xpath("//w:sectPr", namespaces=NS)
    print("Sections found:", len(sections))

    score = 0.0  # progressive score

    # --- 1) Must have at least two sections (section break) ---
    if len(sections) >= 2:
        score += 0.4
        print("✓ Multiple sections detected (0.4 points)")
    else:
        print("✗ Less than two sections – no section break (0 points)")
        return round(score, 4)  # cannot achieve more without second section

    # Build relationship map to resolve footer targets
    rels_map = _build_rels_map(docx_zip)

    # Helpers for later checks
    second_pg_restart = False
    second_footer_ok = False
    first_section_clean = False

    # ----------------- SECOND SECTION CHECKS -----------------
    second_sect = sections[1]

    # (a) Page-number restart at 1
    pgnum = second_sect.find("w:pgNumType", NS)
    if pgnum is not None and pgnum.get(f"{{{NS['w']}}}start") == "1":
        second_pg_restart = True
        score += 0.3
        print("✓ Second section restarts page numbering at 1 (0.3 points)")
    else:
        print("✗ Second section does not restart numbering at 1 (0 points)")

    # (b) Footer contains centred PAGE field
    footer_ref = second_sect.xpath('w:footerReference[@w:type="default"]', namespaces=NS)
    if footer_ref:
        footer_id = footer_ref[0].get(f"{{{NS['r']}}}id")
        footer_xml = _load_footer(docx_zip, rels_map, footer_id)
        if footer_xml is not None:
            # Detect PAGE field (simple or complex field codes)
            page_field_nodes = footer_xml.xpath('.//w:fldSimple[contains(@w:instr, "PAGE")]', namespaces=NS)
            if not page_field_nodes:
                for instr in footer_xml.xpath('.//w:instrText', namespaces=NS):
                    if instr.text and "PAGE" in instr.text:
                        page_field_nodes.append(instr)
                        break
            if page_field_nodes:
                # Ascend to containing paragraph and check justification
                node = page_field_nodes[0]
                while node is not None and node.tag != f"{{{NS['w']}}}p":
                    node = node.getparent()
                if node is not None:
                    jc = node.find('.//w:jc', NS)
                    if jc is not None and jc.get(f"{{{NS['w']}}}val") == "center":
                        second_footer_ok = True
    if second_footer_ok:
        score += 0.2
        print("✓ Second section footer has centred PAGE field (0.2 points)")
    else:
        print("✗ Second section footer missing centred PAGE field (0 points)")

    # ----------------- FIRST SECTION CHECK -----------------
    first_sect = sections[0]
    footer_ref1 = first_sect.xpath('w:footerReference[@w:type="default"]', namespaces=NS)
    footer_contains_page = False
    if footer_ref1:
        footer_id1 = footer_ref1[0].get(f"{{{NS['r']}}}id")
        footer_xml1 = _load_footer(docx_zip, rels_map, footer_id1)
        if footer_xml1 is not None:
            # Look for any PAGE field
            if footer_xml1.xpath('.//w:fldSimple[contains(@w:instr, "PAGE")]', namespaces=NS):
                footer_contains_page = True
            else:
                for instr in footer_xml1.xpath('.//w:instrText', namespaces=NS):
                    if instr.text and "PAGE" in instr.text:
                        footer_contains_page = True
                        break
    if not footer_contains_page:
        first_section_clean = True
        score += 0.1
        print("✓ First section footer has NO page number (0.1 points)")
    else:
        print("✗ First section footer contains a page number (0 points)")

    # ----------------- FINAL SCORING -----------------
    final_score = round(min(score, 1.0), 4)  # cap at 1.0, round to avoid FP glitches
    print(f"Total Score: {final_score}")
    return final_score


if __name__ == "__main__":
    DOC_PATH = "/home/user/my_lab_report_starts_with_a_cover_an_abstract_and_a_table_of_contentsthose_first_three_pages_stay_bl.docx"
    reward = verify_pagination(DOC_PATH)
    print("REWARD:", reward)

