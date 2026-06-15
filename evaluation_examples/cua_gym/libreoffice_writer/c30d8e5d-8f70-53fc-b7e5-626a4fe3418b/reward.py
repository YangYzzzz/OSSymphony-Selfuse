"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m giving my 40-page report one last polish in LibreOffice Writer, and the reviewers insist that every paragraph—no exceptions—be in Times New Roman 12 pt. What’s the quickest way to tweak the Default Paragraph Style so the entire document flips to that font in a single shot?
Generated: 2025-09-10 14:08:50
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
import zipfile
import xml.etree.ElementTree as ET
from docx import Document

FILE_PATH = "/home/user/im_giving_my_40_page_report_one_last_polish_in_libreoffice_writer_and_the_reviewers_insist_that_ever.docx"

# ---------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------

def _extract_normal_style_properties(styles_root):
    """Return (font_name, font_size_half_points) for the Normal style."""
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    normal = styles_root.find("./w:style[@w:styleId='Normal']", ns)
    font_name = None
    font_size_val = None  # stored in half-points (e.g., 24 == 12 pt)

    if normal is not None:
        rPr = normal.find("w:rPr", ns)
        if rPr is not None:
            rFonts = rPr.find("w:rFonts", ns)
            if rFonts is not None:
                font_name = (
                    rFonts.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ascii")
                    or rFonts.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hAnsi")
                )
            sz = rPr.find("w:sz", ns)
            if sz is not None:
                font_size_val = sz.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val")
    return font_name, font_size_val


# ---------------------------------------------------------------
# Verification Function
# ---------------------------------------------------------------

def verify_times_new_roman_default(file_path):
    """Verify that the DOCX's Default (Normal) Paragraph Style is Times New Roman 12 pt,
    and that no run overrides break this rule. Returns a progressive score (0-1)."""

    max_score = 1.0
    score = 0.0
    print(f"Verifying document fonts for: {file_path}")

    # ---------- 1. Basic existence check (NO points awarded) ----------
    if not os.path.exists(file_path):
        print("✗ Document not found")
        return 0.0  # Cannot proceed without the file

    # ---------- 2. Inspect styles.xml for Normal style properties ----------
    try:
        with zipfile.ZipFile(file_path) as z:
            if "word/styles.xml" not in z.namelist():
                print("✗ styles.xml missing in DOCX – cannot verify styles")
                return 0.0
            styles_xml = z.read("word/styles.xml")
            styles_root = ET.fromstring(styles_xml)
    except Exception as e:
        print(f"✗ Error reading styles.xml: {e}")
        return 0.0

    font_name, font_size_val = _extract_normal_style_properties(styles_root)

    # 2a. Font name check (0.4 pts)
    if font_name and font_name.strip().lower() == "times new roman":
        print("✓ Default style font set to Times New Roman (0.4 points)")
        score += 0.4
    else:
        print(f"✗ Default style font incorrect: {font_name}")

    # 2b. Font size check (0.4 pts) – expect 24 half-points = 12 pt
    if font_size_val and font_size_val.isdigit() and int(font_size_val) == 24:
        print("✓ Default style size set to 12 pt (0.4 points)")
        score += 0.4
    else:
        print(f"✗ Default style size incorrect: {font_size_val}")

    # ---------- 3. Scan every run for overrides (0.2 pts) ----------
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Failed to load DOCX with python-docx: {e}")
        return score  # return whatever we have so far

    bad_runs = 0
    total_runs = 0
    for para in doc.paragraphs:
        for run in para.runs:
            total_runs += 1
            r_name = run.font.name
            r_size = run.font.size  # returns a Length object or None

            # If either attribute is explicitly set AND wrong, count as bad
            if r_name and r_name.strip().lower() != "times new roman":
                bad_runs += 1
            if r_size and abs(r_size.pt - 12) > 0.1:
                bad_runs += 1

    if total_runs == 0:
        print("✗ No text runs detected in document – unusual!")
    elif bad_runs == 0:
        print("✓ All runs inherit/correctly use Times New Roman 12 pt (0.2 points)")
        score += 0.2
    else:
        print(f"✗ Found {bad_runs} run(s) overriding font or size incorrectly")

    # ---------- 4. Final score ----------
    final_score = min(score, max_score)
    print(f"Final Score: {final_score}")
    return final_score


# ---------------------------------------------------------------
# Execute verification and print reward
# ---------------------------------------------------------------

if __name__ == "__main__":
    reward = verify_times_new_roman_default(FILE_PATH)
    print(f"REWARD: {reward}")

