"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please change the base font to Times New Roman for newly created Writer documents.
Generated: 2025-10-14 10:57:19
Status: success
Model: azure-o3
Total Steps: 6
"""

import os
import zipfile
import xml.etree.ElementTree as ET
from docx import Document


def verify_base_font_docx(file_path: str, expected_font: str = "Times New Roman") -> float:
    """
    Reward-script verification for the task:
      "Please change the base font to Times New Roman for newly created Writer documents."

    The script awards up to 1.0 points based on two REAL checks:
      1. (0.7 pts) The document-wide default font (docDefaults in styles.xml)
         is set to the expected font.
      2. (0.3 pts) No paragraph/run explicitly overrides the base font with
         a different face.

    The score is progressive and reaches exactly 1.0 only when BOTH conditions
    are satisfied.
    """

    max_score = 1.0
    score = 0.0
    expected_lower = expected_font.lower()

    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # -------------------------------------------------------------
    # Part 1: Check docDefaults base font in styles.xml (0.7 pts)
    # -------------------------------------------------------------
    try:
        with zipfile.ZipFile(file_path) as docx_zip:
            if "word/styles.xml" not in docx_zip.namelist():
                print("✗ styles.xml missing inside DOCX – cannot verify base font")
            else:
                styles_xml = docx_zip.read("word/styles.xml")
                root = ET.fromstring(styles_xml)
                ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

                doc_defaults = root.find("w:docDefaults", ns)
                base_font_correct = False
                found_fonts = []

                if doc_defaults is not None:
                    rpr_default = doc_defaults.find("w:rPrDefault", ns)
                    if rpr_default is not None:
                        rpr = rpr_default.find("w:rPr", ns)
                        if rpr is not None:
                            rfonts = rpr.find("w:rFonts", ns)
                            if rfonts is not None:
                                # gather font names for different script types
                                for attr in ["ascii", "hAnsi", "eastAsia", "cs"]:
                                    val = rfonts.attrib.get(f"{{{ns['w']}}}{attr}")
                                    if val:
                                        found_fonts.append(val)
                                if found_fonts and all(f.lower() == expected_lower for f in found_fonts):
                                    base_font_correct = True

                print("Base font(s) found in docDefaults:", found_fonts if found_fonts else "<none>")
                if base_font_correct:
                    score += 0.7
                    print("✓ Base font in docDefaults is set to Times New Roman (0.7 points)")
                else:
                    print("✗ Base font in docDefaults is NOT set to Times New Roman (0 points)")
    except Exception as e:
        print(f"✗ Error while analysing styles.xml: {e}")

    # -------------------------------------------------------------
    # Part 2: Ensure no explicit font overrides differ (0.3 pts)
    # -------------------------------------------------------------
    try:
        doc = Document(file_path)
        overrides = []
        total_runs = 0

        for para in doc.paragraphs:
            for run in para.runs:
                total_runs += 1
                run_font = run.font.name
                # only consider runs that explicitly set a font face
                if run_font and run_font.lower() != expected_lower:
                    overrides.append(run_font)

        print(f"Total runs scanned: {total_runs}")
        if overrides:
            print(f"✗ Found {len(overrides)} run(s) overriding base font. Sample: {overrides[:5]}")
        else:
            score += 0.3
            print("✓ No runs override the base font (0.3 points)")
    except Exception as e:
        print(f"✗ Error while scanning runs for font overrides: {e}")

    final_score = min(score, max_score)
    print(f"\nTotal Score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score


# -----------------------------------------------------------------
# MAIN EXECUTION (path comes from the task context)
# -----------------------------------------------------------------
if __name__ == "__main__":
    FILE_PATH = "/home/user/please_change_the_base_font_to_times_new_roman_for_newly_created_writer_documents.docx"
    verify_base_font_docx(FILE_PATH)

