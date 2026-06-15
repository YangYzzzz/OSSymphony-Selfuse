"""
FINAL REWARD SCRIPT - SUCCESS
Task: Whenever I insert page numbers in LibreOffice Writer, they keep jumping to the center or start at 0. I just need them in the footer, bottom-right, with the very first page showing "1". How do I set that up so it sticks?
Generated: 2025-09-10 14:32:23
Status: success
Model: azure-o3
Total Steps: 5
"""

import os
import sys
import zipfile
import traceback
from lxml import etree


def verify_writer_page_numbers(docx_path: str) -> float:
    """Verify that a LibreOffice Writer document has correct page numbering.

    Scoring (progressive):
        0.4  – A PAGE field exists in at least one footer.
        0.3  – The paragraph that contains the PAGE field is right-aligned
                (w:jc value "right" or "end").
        0.3  – Page numbering starts at 1 (first section either omits the
                w:start attribute or sets it to "1").

    Returns a float in the range [0.0, 1.0].
    """

    ns = {
        "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    }

    if not os.path.exists(docx_path):
        print(f"✗ File not found: {docx_path}")
        return 0.0

    score = 0.0

    try:
        with zipfile.ZipFile(docx_path, "r") as pkg:
            # -------------------- Collect parts --------------------
            footer_parts = [p for p in pkg.namelist()
                            if p.startswith("word/footer") and p.endswith(".xml")]
            header_parts = [p for p in pkg.namelist()
                            if p.startswith("word/header") and p.endswith(".xml")]

            print(f"Found footer parts: {footer_parts}")
            print(f"Found header parts: {header_parts}")

            # ---------------- Footer analysis ---------------------
            page_field_in_footer = False
            right_aligned = False

            def paragraph_contains_page_field(p_el):
                """Detect PAGE field inside a <w:p> element."""
                # <w:fldSimple w:instr=" PAGE   \* MERGEFORMAT ">
                for fld in p_el.xpath('.//w:fldSimple', namespaces=ns):
                    instr = fld.get(f'{{{ns["w"]}}}instr')
                    if instr and "PAGE" in instr.upper():
                        return True
                # Complex field: look for <w:instrText>PAGE</w:instrText>
                for instr in p_el.xpath('.//w:instrText', namespaces=ns):
                    if instr.text and "PAGE" in instr.text.upper():
                        return True
                return False

            for part in footer_parts:
                root = etree.fromstring(pkg.read(part))
                for p in root.xpath('.//w:p', namespaces=ns):
                    if paragraph_contains_page_field(p):
                        page_field_in_footer = True
                        jc = p.find('.//w:pPr/w:jc', namespaces=ns)
                        align_val = jc.get(f'{{{ns["w"]}}}val') if jc is not None else "left"
                        print(f"  ✓ PAGE field found in {part} (alignment='{align_val}')")
                        if align_val in ("right", "end"):
                            right_aligned = True

            # ---------------- Header check (info only) ------------
            page_field_in_header = False
            for part in header_parts:
                root = etree.fromstring(pkg.read(part))
                if root.xpath('.//w:fldSimple[contains(@w:instr, "PAGE")]', namespaces=ns):
                    page_field_in_header = True
                elif root.xpath('.//w:instrText[contains(translate(text(), "page", "PAGE"), "PAGE")]', namespaces=ns):
                    page_field_in_header = True

            # --------------- Section start value ------------------
            numbering_starts_at_one = False
            if "word/document.xml" in pkg.namelist():
                doc_root = etree.fromstring(pkg.read("word/document.xml"))
                sect_prs = doc_root.xpath('//w:sectPr', namespaces=ns)
                if sect_prs:
                    pg_num = sect_prs[0].find('.//w:pgNumType', namespaces=ns)
                    start_val = pg_num.get(f'{{{ns["w"]}}}start') if pg_num is not None else None
                    print(f"First section pgNumType @start: {start_val}")
                    if start_val is None or start_val == "1":
                        numbering_starts_at_one = True

            # -------------------- Scoring -------------------------
            if page_field_in_footer:
                score += 0.4
                print("✓ PAGE field present in footer (+0.4)")
            else:
                print("✗ No PAGE field found in any footer")

            if right_aligned:
                score += 0.3
                print("✓ PAGE field paragraph is right-aligned (+0.3)")
            else:
                print("✗ PAGE field paragraph not right-aligned")

            if numbering_starts_at_one:
                score += 0.3
                print("✓ Page numbering starts at 1 (+0.3)")
            else:
                print("✗ Page numbering does not start at 1")

            if page_field_in_header:
                print("⚠ PAGE field also present in header (informational, no penalty)")

    except Exception as exc:
        print("✗ Error analysing DOCX file:")
        traceback.print_exc()
        return 0.0

    final_score = min(score, 1.0)
    print(f"Computed reward score: {final_score}")
    return final_score


def main():
    # Determine path: CLI argument or auto-detect typical file.
    path = sys.argv[1] if len(sys.argv) > 1 else None

    if not path:
        default_name = (
            "whenever_i_insert_page_numbers_in_libreoffice_writer_they_keep_jumping_to_the_center_or_start_at_0_i.docx"
        )
        if os.path.exists(default_name):
            path = default_name
        else:
            # Fallback: use first .docx in current directory
            for fname in os.listdir('.'):
                if fname.lower().endswith('.docx'):
                    path = fname
                    break

    if not path:
        print("✗ No DOCX file provided and none found automatically.")
        print("REWARD: 0.0")
        return

    reward_value = verify_writer_page_numbers(path)
    print(f"REWARD: {reward_value}")


if __name__ == "__main__":
    main()

