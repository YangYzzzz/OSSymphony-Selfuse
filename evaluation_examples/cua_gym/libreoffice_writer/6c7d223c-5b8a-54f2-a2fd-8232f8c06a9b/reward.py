"""
FINAL REWARD SCRIPT - SUCCESS
Task: LibreOffice keeps slapping page numbers on every sheet of my 10-page brochure. I only want a centered header that reads exactly “Page X of Y” (for example, “Page 3 of 10”) on pages 2, 3, 4, 5, and 6—nowhere else. What’s the cleanest way to set that up?
Generated: 2025-09-10 16:32:21
Status: success
Model: azure-o3
Total Steps: 7
"""

import os
import re
import zipfile
from typing import Dict

try:
    # lxml is available in the evaluation environment
    import lxml.etree as ET
except ImportError:
    from xml.etree import ElementTree as ET  # fallback (less powerful but keeps script functional)


def _parse_relationships(zipf: zipfile.ZipFile) -> Dict[str, str]:
    """Return a mapping rId -> target path (e.g., word/header2.xml)."""
    rels_map = {}
    rels_path = "word/_rels/document.xml.rels"
    if rels_path not in zipf.namelist():
        return rels_map

    rels_xml = zipf.read(rels_path)
    root = ET.fromstring(rels_xml)
    # Relationship elements are in the package relationships namespace
    for rel in root.findall(".//{http://schemas.openxmlformats.org/package/2006/relationships}Relationship"):
        r_id = rel.get("Id")
        target = rel.get("Target")
        if target.startswith("../"):
            target = target.split("../", 1)[1]
        if not target.startswith("word/"):
            target = "word/" + target
        rels_map[r_id] = target
    return rels_map


def _header_contains_page_fields(xml_bytes: bytes):
    """Inspect a header XML file and return detailed booleans about its content/formatting."""
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    root = ET.fromstring(xml_bytes)

    has_page_field = False  # PAGE field (current page number)
    has_numpages_field = False  # NUMPAGES field (total pages)
    has_word_page = False  # literal word "Page"
    is_center_aligned = False  # paragraph containing fields is centre-justified

    # Detect PAGE / NUMPAGES fields via fldSimple or instrText
    for fld in root.xpath(".//w:fldSimple", namespaces=ns):
        instr = fld.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}instr", "")
        if "PAGE" in instr:
            has_page_field = True
        if "NUMPAGES" in instr:
            has_numpages_field = True

    for instr in root.xpath(".//w:instrText", namespaces=ns):
        text = "".join(instr.itertext())
        if "PAGE" in text:
            has_page_field = True
        if "NUMPAGES" in text:
            has_numpages_field = True

    # Combine all text within <w:t> elements to search for literal word "Page"
    combined_text = " ".join(root.xpath(".//w:t/text()", namespaces=ns))
    if re.search(r"\bPage\b", combined_text, flags=re.I):
        has_word_page = True

    # Check alignment of paragraph that contains a field
    for p in root.xpath(".//w:p", namespaces=ns):
        contains_field = (
            p.xpath(".//w:fldSimple", namespaces=ns)
            or p.xpath(".//w:instrText", namespaces=ns)
        )
        if not contains_field:
            continue
        jc_elem = p.find(".//w:jc", namespaces=ns)
        if jc_elem is not None and jc_elem.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val") == "center":
            is_center_aligned = True
            break

    return has_page_field, has_numpages_field, has_word_page, is_center_aligned


def verify_brochure_header(docx_path: str) -> float:
    """Reward script verifying precise header/page-number requirements for the brochure task.

    Scoring breakdown (progressive – totals to 1.0):
      • 0.25 – At least 3 sections (front/middle/back) indicating page-range control capability
      • 0.25 – A header file actually contains PAGE field (current page) AND NUMPAGES field (total pages)
      • 0.10 – That header also contains literal word "Page"
      • 0.10 – The paragraph with the fields is centre-aligned
      • 0.15 – No footers contain PAGE or NUMPAGES fields (numbers must be in header only)
      • 0.15 – Page-numbering header is NOT linked to first or last section but is linked to at least one middle section (pages 2-6)
    """

    print(f"Verifying brochure headers in: {docx_path}")
    if not os.path.exists(docx_path):
        print("✗ File not found – cannot evaluate task")
        print("REWARD: 0.0")
        return 0.0

    score = 0.0
    max_score = 1.0

    try:
        with zipfile.ZipFile(docx_path) as z:
            # --------------- SECTION ANALYSIS ---------------
            document_xml = z.read("word/document.xml")
            ns = {
                "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
                "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
            }
            doc_root = ET.fromstring(document_xml)
            sect_prs = doc_root.xpath("//w:sectPr", namespaces=ns)
            num_sections = len(sect_prs)
            if num_sections >= 3:
                print(f"✓ Found {num_sections} sections (>=3)")
                score += 0.25
            else:
                print(f"✗ Only {num_sections} section(s) found – need at least 3 for separate page-ranges")

            # --------------- HEADER / FOOTER COLLECTION ---------------
            rels_map = _parse_relationships(z)

            header_info: Dict[str, dict] = {}
            for member in z.namelist():
                if member.startswith("word/header") and member.endswith(".xml"):
                    has_page, has_numpages, has_word_page, centered = _header_contains_page_fields(z.read(member))
                    header_info[member] = {
                        "page": has_page,
                        "numpages": has_numpages,
                        "word_page": has_word_page,
                        "centered": centered,
                    }

            # FOOTERS – ensure no page fields exist there
            footer_page_field_count = 0
            for member in z.namelist():
                if member.startswith("word/footer") and member.endswith(".xml"):
                    footer_xml = z.read(member)
                    if b"PAGE" in footer_xml or b"NUMPAGES" in footer_xml:
                        footer_page_field_count += 1

            # --------------- HEADER WITH PAGE INFO ---------------
            headers_with_page_fields = [h for h, info in header_info.items() if info["page"] and info["numpages"]]
            if headers_with_page_fields:
                print(
                    f"✓ Header(s) containing both PAGE and NUMPAGES fields: {headers_with_page_fields}"
                )
                score += 0.25
                # Evaluate formatting details on first qualifying header
                first_header = headers_with_page_fields[0]
                h_info = header_info[first_header]
                if h_info["word_page"]:
                    print("✓ Header includes literal word 'Page'")
                    score += 0.10
                else:
                    print("✗ Header missing literal word 'Page'")
                if h_info["centered"]:
                    print("✓ Header paragraph is centre-aligned")
                    score += 0.10
                else:
                    print("✗ Header paragraph is not centre-aligned")
            else:
                print("✗ No header contains both PAGE and NUMPAGES fields – cannot display 'Page X of Y'")

            # --------------- FOOTER CHECK ---------------
            if footer_page_field_count == 0:
                print("✓ No footers contain PAGE/NUMPAGES fields")
                score += 0.15
            else:
                print(f"✗ {footer_page_field_count} footer(s) improperly contain PAGE/NUMPAGES fields")

            # --------------- RANGE RESTRICTION CHECK ---------------
            passes_range_restriction = False
            if headers_with_page_fields and num_sections >= 3:
                # Map each section's default header file
                sect_headers = []
                for sect in sect_prs:
                    ref = sect.find("./w:headerReference[@w:type='default']", namespaces=ns)
                    header_file = None
                    if ref is not None:
                        r_id = ref.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
                        header_file = rels_map.get(r_id)
                    sect_headers.append(header_file)

                first_header_file = sect_headers[0]
                last_header_file = sect_headers[-1]
                middle_header_set = set(sect_headers[1:-1])
                page_header_set = set(headers_with_page_fields)

                if (
                    first_header_file not in page_header_set
                    and last_header_file not in page_header_set
                    and middle_header_set.intersection(page_header_set)
                ):
                    passes_range_restriction = True

            if passes_range_restriction:
                print("✓ Page-numbering header appears only on middle section(s) – not on first/last pages")
                score += 0.15
            else:
                print("✗ Page-numbering header incorrectly linked to first/last section or missing from middle section(s)")

    except Exception as exc:
        print(f"✗ Error during verification: {exc}")
        print("REWARD: 0.0")
        return 0.0

    final_score = min(score, max_score)
    print(f"Total score: {final_score:.2f}")
    print(f"REWARD: {final_score}")
    return final_score


# --------------- ACTUAL EXECUTION (MANDATORY) ---------------
if __name__ == "__main__":
    DOCX_PATH = "/home/user/libreoffice_keeps_slapping_page_numbers_on_every_sheet_of_my_10_page_brochure_i_only_want_a_centered.docx"
    verify_brochure_header(DOCX_PATH)

