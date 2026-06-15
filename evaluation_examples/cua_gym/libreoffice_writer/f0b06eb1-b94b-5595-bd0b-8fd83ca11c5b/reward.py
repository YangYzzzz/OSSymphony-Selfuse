"""
FINAL REWARD SCRIPT - SUCCESS
Task: Center the page numbers along the bottom on all pages.
Generated: 2025-10-14 10:41:48
Status: success
Model: azure-o3
Total Steps: 3
"""

import os
import zipfile
from lxml import etree as ET


def verify_centered_page_numbers(file_path: str) -> float:
    """Return a progressive score (0-1) for the task:
    "Center the page numbers along the bottom on all pages".

    Logic:
    1. Open the DOCX as a zip archive and locate every footer part (word/footer*.xml).
    2. For each footer, verify there is at least one paragraph that:
       a. Contains a PAGE field (simple or complex field).
       b. Has its justification set to centre (w:jc w:val="center").
    3. Score = (footers that satisfy both conditions) / (total footers).
       This yields a progressive score; 1.0 only when **all** footers pass.
    """

    # Preliminary file checks ─ no points awarded for these (natural conditions)
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return 0.0
    if not file_path.lower().endswith('.docx'):
        print(f"✗ Unsupported file type (expected .docx): {file_path}")
        return 0.0

    try:
        with zipfile.ZipFile(file_path, 'r') as docx:
            footer_files = [f for f in docx.namelist()
                            if f.startswith('word/footer') and f.endswith('.xml')]
            total_footers = len(footer_files)
            print(f"Found {total_footers} footer part(s).")

            if total_footers == 0:
                print("✗ No footer parts detected – cannot verify page numbers.")
                return 0.0

            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            passed = 0

            for footer in footer_files:
                xml_root = ET.fromstring(docx.read(footer))
                footer_ok = False

                # Iterate through each paragraph in the footer
                for p in xml_root.findall('.//w:p', ns):
                    # -------- Check if paragraph contains a PAGE field --------
                    page_field = False
                    # 1) <w:fldSimple w:instr=" PAGE \* MERGEFORMAT "/> pattern
                    for fld in p.findall('.//w:fldSimple', ns):
                        instr = fld.get(f"{{{ns['w']}}}instr")
                        if instr and 'PAGE' in instr.upper():
                            page_field = True
                            break
                    # 2) Complex field “PAGE” contained in <w:instrText>
                    if not page_field:
                        for instr in p.findall('.//w:instrText', ns):
                            if instr.text and 'PAGE' in instr.text.upper():
                                page_field = True
                                break
                    if not page_field:
                        continue  # Next paragraph

                    # -------- Check if paragraph is centred --------
                    jc = p.find('.//w:pPr/w:jc', ns)
                    if jc is not None and jc.get(f"{{{ns['w']}}}val") == 'center':
                        footer_ok = True
                        break  # This footer passes; go to next footer

                print(f"  Footer '{footer}': {'✓' if footer_ok else '✗'}")
                if footer_ok:
                    passed += 1

            score = passed / total_footers
            print(f"Footers passed: {passed}/{total_footers}")
            print(f"Calculated score: {score}")
            return round(score, 2)

    except Exception as e:
        print(f"✗ Error during verification: {e}")
        return 0.0


def main():
    target_doc = '/home/user/center_the_page_numbers_along_the_bottom_on_all_pages.docx'
    reward = verify_centered_page_numbers(target_doc)
    print(f"REWARD: {reward}")
    return reward


if __name__ == '__main__':
    main()

