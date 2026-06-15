"""
FINAL REWARD SCRIPT - SUCCESS
Task: Is there a quick trick in LibreOffice Writer to automatically pop the built-in Author field into the footer of the Default Page Style and keep it left-aligned? I’m tired of manually typing my name on every page.
Generated: 2025-09-10 15:51:59
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
import zipfile
from lxml import etree
import traceback


def verify_author_field_in_footer(docx_path: str) -> float:
    """Verify that the DOCX contains the built-in AUTHOR field in the footer of
    the *Default Page Style* (i.e., first section) and that the paragraph is
    left-aligned.

    Returns a progressive score between 0.0 and 1.0:
        • 0.6 points – AUTHOR field detected in at least one footer paragraph
        • 0.4 points – that paragraph is left-aligned (or has no explicit
          alignment, meaning the default is left)
    """

    print(f"Verifying Author field in footer for: {docx_path}")
    max_score = 1.0
    total_score = 0.0

    # ---------- Preliminary checks (NO POINTS AWARDED) ----------
    if not os.path.exists(docx_path):
        print("✗ File does not exist")
        return 0.0
    if not docx_path.lower().endswith(".docx"):
        print("✗ File is not a DOCX file – current script supports only DOCX")
        return 0.0

    # ---------- Deep inspection of the DOCX package ----------
    try:
        with zipfile.ZipFile(docx_path) as z:
            # Collect all footer XML parts
            footer_files = [f for f in z.namelist() if f.startswith("word/footer") and f.endswith(".xml")]
            if not footer_files:
                print("✗ No footer files found in DOCX")
                return 0.0
            print(f"✓ Found {len(footer_files)} footer file(s): {footer_files}")

            # XML namespace map for WordprocessingML
            ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

            author_field_found = False
            left_aligned = False

            # Examine every footer part
            for footer_file in footer_files:
                footer_xml = z.read(footer_file)
                root = etree.fromstring(footer_xml)

                # Iterate through paragraphs (<w:p>) in the footer
                for p in root.xpath(".//w:p", namespaces=ns):
                    # Gather field instructions present in this paragraph
                    instr_texts = []

                    # 1) <w:fldSimple instr=" AUTHOR "> form
                    for node in p.xpath(".//w:fldSimple", namespaces=ns):
                        instr = node.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}instr")
                        if instr:
                            instr_texts.append(instr)

                    # 2) Complex field code split across <w:instrText>
                    for node in p.xpath(".//w:instrText", namespaces=ns):
                        if node.text:
                            instr_texts.append(node.text)

                    if not instr_texts:
                        continue  # No field codes in this paragraph

                    combined_instr = " ".join(instr_texts).upper()
                    if "AUTHOR" in combined_instr:
                        author_field_found = True

                        # Determine alignment of the paragraph
                        jc_node = p.xpath("./w:pPr/w:jc", namespaces=ns)
                        if jc_node:
                            val = jc_node[0].get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val")
                            alignment = val or "left(default)"
                        else:
                            alignment = "left(default)"  # No <w:jc> => default left
                        print(f"  ✓ Found AUTHOR field in paragraph. Alignment = {alignment}")

                        if alignment in ("left", "left(default)"):
                            left_aligned = True
            # ---------------- Scoring ----------------
            if author_field_found:
                print("✓ AUTHOR field found in footer (0.6 points)")
                total_score += 0.6
            else:
                print("✗ AUTHOR field not found in any footer")

            if author_field_found and left_aligned:
                print("✓ AUTHOR field paragraph is left-aligned (0.4 points)")
                total_score += 0.4
            elif author_field_found:
                print("✗ AUTHOR field paragraph is not left-aligned – 0 alignment points")

            final_score = min(total_score, max_score)
            print(f"Total score: {final_score}/{max_score}")
            return final_score
    except Exception as e:
        print("✗ Exception during verification:", e)
        traceback.print_exc()
        return 0.0


# ---------------- Execute verification when run as script ----------------
if __name__ == "__main__":
    FILE_PATH = "/home/user/is_there_a_quick_trick_in_libreoffice_writer_to_automatically_pop_the_built_in_author_field_into_the.docx"
    reward = verify_author_field_in_footer(FILE_PATH)
    print(f"REWARD: {reward}")
