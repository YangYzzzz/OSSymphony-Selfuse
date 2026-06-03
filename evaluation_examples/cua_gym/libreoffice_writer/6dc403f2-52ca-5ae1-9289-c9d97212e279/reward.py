"""
FINAL REWARD SCRIPT - SUCCESS
Task: Set the default font in Writer to Times New Roman at 12 pt.
Generated: 2025-10-14 11:47:15
Status: success
Model: azure-o3
Total Steps: 1
"""

import os
import zipfile
from lxml import etree

"""
Reward Script: Verify that the default font in the provided Writer/Word document
(DOCX) has been set to Times New Roman at 12 pt.

Verification Strategy
--------------------
1. Open the DOCX as a ZIP file and read `word/styles.xml` (where default
   paragraph/run properties are stored).
2. Check *docDefaults* first (ideal place for application-wide default font).
   • Verify that the run‐properties (`w:rPrDefault`) contains
     `w:rFonts` with ASCII/HAnsi="Times New Roman".
   • Verify that it contains `w:sz` whose value is 24 (half-points, i.e. 12 pt).
3. If either font family or size is missing in *docDefaults*, fall back to the
   Normal style (styleId="Normal", type="paragraph") and repeat the same
   checks inside its `w:rPr`.
4. Progressive Scoring (max 1.0):
   • 0.5 points for correct font family (Times New Roman)
   • 0.5 points for correct font size (12 pt -> 24 half-points)
   Only award points when the conditions are actually met.
5. Print detailed diagnostics for transparency and debugging.
6. Output final reward as "REWARD: X.X".

The script purposefully avoids giving points for natural conditions such as the
file merely existing or being readable. All points require positive evidence of
proper defaults.
"""

def verify_default_font(docx_path: str) -> float:
    """Return a score between 0.0 and 1.0 based on default font correctness."""
    print(f"Checking default font in: {docx_path}")

    if not os.path.exists(docx_path):
        print("✗ File not found")
        print("REWARD: 0.0")
        return 0.0  # No progress if file is missing

    font_family_correct = False
    font_size_correct = False

    try:
        with zipfile.ZipFile(docx_path) as z:
            # styles.xml holds style/default definitions
            if "word/styles.xml" not in z.namelist():
                print("✗ word/styles.xml not present – cannot verify")
                print("REWARD: 0.0")
                return 0.0

            styles_xml = z.read("word/styles.xml")
            ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
            root = etree.fromstring(styles_xml)

            # 1) Check docDefaults section (best-practice location)
            rpr_defaults = root.xpath(".//w:docDefaults/w:rPrDefault/w:rPr", namespaces=ns)
            if rpr_defaults:
                rpr = rpr_defaults[0]

                # Font family check
                rFonts = rpr.find("w:rFonts", namespaces=ns)
                if rFonts is not None:
                    ascii_font = rFonts.get(f"{{{ns['w']}}}ascii")
                    hAnsi_font = rFonts.get(f"{{{ns['w']}}}hAnsi")
                    if ascii_font == "Times New Roman" or hAnsi_font == "Times New Roman":
                        font_family_correct = True
                        print("✓ Times New Roman set in docDefaults")

                # Font size check (24 half-points = 12 pt)
                sz = rpr.find("w:sz", namespaces=ns)
                if sz is not None:
                    val = sz.get(f"{{{ns['w']}}}val")
                    if val and val.isdigit() and int(val) == 24:
                        font_size_correct = True
                        print("✓ Font size 12 pt (24 half-points) set in docDefaults")

            # 2) Fallback to Normal style if needed
            if not font_family_correct or not font_size_correct:
                normal_style = root.xpath(
                    ".//w:style[@w:styleId='Normal' and @w:type='paragraph']",
                    namespaces=ns,
                )
                if normal_style:
                    rpr = normal_style[0].find("w:rPr", namespaces=ns)
                    if rpr is not None:
                        # Font family check fallback
                        if not font_family_correct:
                            rFonts = rpr.find("w:rFonts", namespaces=ns)
                            if rFonts is not None:
                                ascii_font = rFonts.get(f"{{{ns['w']}}}ascii")
                                hAnsi_font = rFonts.get(f"{{{ns['w']}}}hAnsi")
                                if ascii_font == "Times New Roman" or hAnsi_font == "Times New Roman":
                                    font_family_correct = True
                                    print("✓ Times New Roman set in Normal style")
                        # Font size check fallback
                        if not font_size_correct:
                            sz = rpr.find("w:sz", namespaces=ns)
                            if sz is not None:
                                val = sz.get(f"{{{ns['w']}}}val")
                                if val and val.isdigit() and int(val) == 24:
                                    font_size_correct = True
                                    print("✓ Font size 12 pt set in Normal style")

    except Exception as e:
        print(f"✗ Error parsing DOCX: {e}")
        print("REWARD: 0.0")
        return 0.0  # Parsing failure = no progress

    # Progressive scoring
    score = 0.0
    if font_family_correct:
        score += 0.5
    if font_size_correct:
        score += 0.5

    print(f"Font family correct: {font_family_correct}")
    print(f"Font size   correct: {font_size_correct}")
    print(f"REWARD: {score}")
    return score


# ----------------- EXECUTION ENTRY POINT -----------------
if __name__ == "__main__":
    DOC_PATH = "/home/user/set_the_default_font_in_writer_to_times_new_roman_at_12_pt.docx"
    verify_default_font(DOC_PATH)

