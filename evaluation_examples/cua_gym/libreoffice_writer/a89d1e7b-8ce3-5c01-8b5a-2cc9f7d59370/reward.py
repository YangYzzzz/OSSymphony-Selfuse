"""
FINAL REWARD SCRIPT - SUCCESS
Task: In LibreOffice Writer I want the footer to auto-display “Page X of Y” (for example, “Page 3 of 20”) and have that text centered on every page. How do I set this up?
Generated: 2025-09-10 12:36:41
Status: success
Model: azure-o3
Total Steps: 6
"""

import os
import re
import zipfile
from lxml import etree


def verify_page_x_of_y_footer(file_path: str) -> float:
    """Verify that the document has a centred footer displaying
    the automatic text "Page X of Y" using PAGE and NUMPAGES fields.

    Scoring (progressive):
        • 0.25 – PAGE field detected
        • 0.25 – NUMPAGES field detected
        • 0.20 – Static words "Page … of …" present in footer
        • 0.30 – Footer paragraph is centre-aligned

    Returns a float between 0.0 and 1.0
    """

    max_score = 1.0
    score = 0.0

    # ---------- 1.  Basic existence check (no points) ----------
    if not os.path.exists(file_path):
        print("✗ File not found:", file_path)
        return 0.0  # cannot verify anything

    # Namespace used in DOCX XML
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

    try:
        with zipfile.ZipFile(file_path) as docx_zip:
            # ---------- 2. Locate footer parts ----------
            footer_files = [f for f in docx_zip.namelist()
                            if f.startswith("word/footer") and f.endswith(".xml")]
            if not footer_files:
                print("✗ No footer parts found in document")
                return 0.0
            print(f"✓ Found {len(footer_files)} footer part(s): {footer_files}")

            # Flags for the four separate requirements
            found_page_field = False
            found_numpages_field = False
            found_static_words = False
            found_center_alignment = False

            # ---------- 3. Inspect each footer ----------
            for footer in footer_files:
                xml_bytes = docx_zip.read(footer)
                root = etree.fromstring(xml_bytes)

                for p in root.findall(".//w:p", namespaces=ns):
                    # a) Check for PAGE / NUMPAGES fields
                    instr_texts = [t.text.strip() for t in p.findall('.//w:instrText', namespaces=ns) if t.text]
                    combined_instr = " ".join(instr_texts).upper()
                    if "PAGE" in combined_instr:
                        found_page_field = True
                    if "NUMPAGES" in combined_instr:
                        found_numpages_field = True

                    # b) Check for literal text "Page" and "of" (human-readable words)
                    all_run_text = "".join([t.text for t in p.findall('.//w:t', namespaces=ns) if t.text])
                    if re.search(r"page\s", all_run_text, re.IGNORECASE) and re.search(r"\sof\s", all_run_text, re.IGNORECASE):
                        found_static_words = True

                    # c) Check centre alignment for this paragraph
                    jc = p.find('./w:pPr/w:jc', namespaces=ns)
                    if jc is not None and jc.get(f'{{{ns["w"]}}}val') == 'center':
                        found_center_alignment = True

            # ---------- 4. Progressive Scoring ----------
            if found_page_field:
                score += 0.25
                print("✓ PAGE field detected (0.25)")
            else:
                print("✗ PAGE field NOT detected")

            if found_numpages_field:
                score += 0.25
                print("✓ NUMPAGES field detected (0.25)")
            else:
                print("✗ NUMPAGES field NOT detected")

            if found_static_words:
                score += 0.20
                print("✓ Literal words 'Page … of …' found (0.20)")
            else:
                print("✗ Expected literal words 'Page … of …' NOT found")

            if found_center_alignment:
                score += 0.30
                print("✓ Footer paragraph centred (0.30)")
            else:
                print("✗ Footer paragraph NOT centred")

            final_score = min(score, max_score)
            print(f"Total score: {final_score}")
            return final_score

    except Exception as e:
        print("✗ Error during verification:", e)
        return 0.0


if __name__ == "__main__":
    # Default path – adjust if the evaluation environment uses a different location
    default_path = "/home/user/in_libreoffice_writer_i_want_the_footer_to_auto_display_page_x_of_y_for_example_page_3_of_20_and_hav.docx"

    # If the default path does not exist, try to locate any *.docx in home directory
    if not os.path.exists(default_path):
        from glob import glob
        candidates = glob("/home/user/*.docx")
        default_path = candidates[0] if candidates else ""

    reward = verify_page_x_of_y_footer(default_path)
    print("REWARD:", reward)
