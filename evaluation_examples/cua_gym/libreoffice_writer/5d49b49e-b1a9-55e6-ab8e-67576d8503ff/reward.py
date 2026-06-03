"""
FINAL REWARD SCRIPT - SUCCESS
Task: LibreOffice keeps sticking page numbers on every page, but for this booklet I only want them centered in the footer on pages 2, 3, 4, and 5—nowhere else. How do I set that up?
Generated: 2025-09-10 14:42:05
Status: success
Model: azure-o3
Total Steps: 5
"""

import os
import zipfile
from lxml import etree as ET

def verify_booklet_page_numbers(file_path):
    """
    Reward-script verification for the LibreOffice/Word booklet task.

    Requirement: page numbers must appear ONLY on pages 2-5, centred in
    the footer.  In a DOCX this manifests as exactly four footer parts
    containing a PAGE field with centre alignment; all other footers must
    lack page fields.

    Progressive scoring (max 1.0):
      1. Correct quantity of page-numbered footers  … 0.40 pts
      2. Those footers are centre-aligned            … 0.30 pts
      3. No PAGE field in any remaining footer       … 0.30 pts
    """

    print(f"Verifying document: {file_path}")

    if not os.path.exists(file_path):
        print("✗ File not found")
        print("REWARD: 0.0")
        return 0.0

    try:
        with zipfile.ZipFile(file_path) as doc_zip:
            footer_files = [n for n in doc_zip.namelist()
                            if n.startswith("word/footer") and n.endswith(".xml")]
            print(f"Found {len(footer_files)} footer part(s)")
            if not footer_files:
                print("✗ No footer parts detected – cannot verify page numbers")
                print("REWARD: 0.0")
                return 0.0

            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            footers_with_page, centered_page_footers, footers_without_page = [], [], []

            for footer in footer_files:
                root = ET.fromstring(doc_zip.read(footer))

                # Detect PAGE field (fldSimple w/ PAGE or instrText containing PAGE)
                page_nodes = root.xpath('.//w:fldSimple[contains(@w:instr, "PAGE")] | '
                                        './/w:instrText[contains(text(), "PAGE")]', namespaces=ns)
                has_page = len(page_nodes) > 0

                if has_page:
                    footers_with_page.append(footer)
                    para = root.xpath('.//w:p[w:fldSimple[contains(@w:instr, "PAGE")] '
                                      'or w:r/w:instrText[contains(text(), "PAGE")]]', namespaces=ns)
                    alignment = None
                    if para:
                        jc = para[0].find('.//w:pPr/w:jc', namespaces=ns)
                        if jc is not None:
                            alignment = jc.get(f"{{{ns['w']}}}val")
                    if alignment == 'center':
                        centered_page_footers.append(footer)
                    print(f"  {footer}: PAGE field present, alignment={alignment}")
                else:
                    footers_without_page.append(footer)
                    print(f"  {footer}: no PAGE field")

            # ---------------- Progressive scoring ----------------
            score = 0.0
            expected_count = 4  # pages 2-5

            # Part 1 – correct number of page-numbered footers
            if footers_with_page:
                ratio = min(len(footers_with_page), expected_count) / expected_count
                part1 = ratio * 0.40
                score += part1
                print(f"Part 1 – correct count: {part1:.2f}/0.40")
            else:
                print("✗ No footers with page numbers")

            # Part 2 – centre alignment in those footers
            if footers_with_page:
                align_ratio = len(centered_page_footers) / len(footers_with_page)
                part2 = align_ratio * 0.30
                score += part2
                print(f"Part 2 – centre alignment ratio {align_ratio:.2f}: {part2:.2f}/0.30")

            # Part 3 – remaining footers have NO page field
            extras_with_page = max(0, len(footers_with_page) - expected_count)
            if extras_with_page == 0:
                part3 = 0.30
            else:
                penalty = extras_with_page / len(footer_files)
                part3 = 0.30 * (1 - penalty)
            score += part3
            print(f"Part 3 – clean other footers: {part3:.2f}/0.30")

            final_score = round(min(score, 1.0), 2)
            print(f"Final score: {final_score}")
            print(f"REWARD: {final_score}")
            return final_score

    except Exception as exc:
        print("✗ Error during verification:", exc)
        import traceback; traceback.print_exc()
        print("REWARD: 0.0")
        return 0.0

# ---------------------------------------------------------------------------
# Auto-execute when run as a script (needed for evaluation environment)
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    DOC_PATH = '/home/user/libreoffice_keeps_sticking_page_numbers_on_every_page_but_for_this_booklet_i_only_want_them_centered.docx'
    verify_booklet_page_numbers(DOC_PATH)

