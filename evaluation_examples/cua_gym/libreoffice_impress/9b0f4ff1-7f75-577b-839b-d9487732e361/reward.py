"""
FINAL REWARD SCRIPT - SUCCESS
Task: Slide 199 is still showing the default ● bullets, but I need them to use the ➡ (Unicode U+2192) arrow bullet that LibreOffice Impress offers. How do I switch just that slide’s list to the ➡ arrow style without affecting the others?
Generated: 2025-09-10 20:42:28
Status: success
Model: azure-o3
Total Steps: 5
"""

import os
import re
import zipfile
import traceback
from lxml import etree

# ---------------------------------------------
# Reward verification script for LibreOffice Impress task
# Task: Ensure ONLY slide 199 uses ➡ (U+2192 / U+27A1) arrow bullets
# ---------------------------------------------

# Bullet character sets
ARROW_CHARS = {
    "→",  # U+2192
    "➡",  # U+27A1 (black rightwards arrow)
    "➜",  # U+279C (heavy round-tipped rightwards arrow)
}
DEFAULT_BULLET_CHARS = {
    "•",  # U+2022
    "●",  # U+25CF
    "▪",  # U+25AA
    "",  # U+F0A7 (Wingdings)
    "",  # U+2022 (Word special)
}

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------

def _list_slide_xml_paths(pptx_zip):
    """Return a dict mapping slide number -> path inside pptx."""
    slide_paths = {}
    pattern = re.compile(r"ppt/slides/slide(\d+)\.xml")
    for fname in pptx_zip.namelist():
        m = pattern.match(fname)
        if m:
            slide_num = int(m.group(1))
            slide_paths[slide_num] = fname
    return slide_paths


def _extract_bullet_chars(xml_bytes):
    """Extract all <a:buChar char="…"> characters from slide XML."""
    chars = []
    try:
        root = etree.fromstring(xml_bytes)
    except Exception:
        return chars  # XML parse failure -> no bullets detected

    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    for bu_char in root.xpath(".//a:buChar", namespaces=ns):
        ch = bu_char.get("char")
        if ch:
            chars.append(ch)
    return chars

# ------------------------------------------------------------------
# Main verification function
# ------------------------------------------------------------------

def verify_task(file_path):
    """
    Verifies that:
      1. Slide 199 exists and uses an arrow bullet (→ / ➡ / ➜)
      2. Slide 199 no longer contains any default bullets (•, ●, ▪, …)
      3. No OTHER slide uses an arrow bullet (change applied only to slide 199)

    Progressive scoring (max 1.0):
      +0.6  Arrow bullet present on slide 199
      +0.2  Default bullet removed from slide 199
      +0.2  Arrow bullet absent from all other slides
    """
    print(f"Verifying bullet style modification in: {file_path}")
    max_score = 1.0
    score = 0.0

    if not os.path.exists(file_path):
        print("✗ Presentation file does not exist.")
        return 0.0

    try:
        with zipfile.ZipFile(file_path, "r") as pptx_zip:
            slide_paths = _list_slide_xml_paths(pptx_zip)
            print(f"✓ Loaded PPTX archive with {len(slide_paths)} slides")

            # --- Requirement: Slide 199 must exist ---
            if 199 not in slide_paths:
                print("✗ Slide 199 not found in the presentation.")
                return 0.0  # Cannot proceed further
            print("✓ Slide 199 exists")

            # --- Analyse slide 199 ---
            bullets_199 = _extract_bullet_chars(pptx_zip.read(slide_paths[199]))
            print(f"  Bullet chars on slide 199: {bullets_199}")

            arrow_present = any(ch in ARROW_CHARS for ch in bullets_199)
            default_present_199 = any(ch in DEFAULT_BULLET_CHARS for ch in bullets_199)

            # Condition A: Arrow bullet applied on slide 199 (0.6)
            if arrow_present:
                score += 0.6
                print("✓ Arrow bullet found on slide 199 (+0.6)")
            else:
                print("✗ Arrow bullet NOT found on slide 199")

            # Condition B: Default bullets removed from slide 199 (0.2)
            if arrow_present and not default_present_199:
                score += 0.2
                print("✓ Default bullets removed from slide 199 (+0.2)")
            elif arrow_present:
                print("✗ Default bullets still present on slide 199 (no points)")

            # Condition C: Other slides remain unchanged (no arrow bullets) (0.2)
            if arrow_present:
                arrow_found_elsewhere = False
                for num, path in slide_paths.items():
                    if num == 199:
                        continue  # skip target slide
                    other_bullets = _extract_bullet_chars(pptx_zip.read(path))
                    if any(ch in ARROW_CHARS for ch in other_bullets):
                        arrow_found_elsewhere = True
                        print(f"    Arrow bullet also found on slide {num}")
                        break

                if not arrow_found_elsewhere:
                    score += 0.2
                    print("✓ Arrow bullets absent from other slides (+0.2)")
                else:
                    print("✗ Arrow bullets unexpectedly present on other slides (no points)")

            # Cap score at 1.0
            final_score = min(score, max_score)
            print(f"Total score: {final_score}")
            print(f"REWARD: {final_score}")
            return final_score

    except Exception as exc:
        print("✗ Exception during verification:", exc)
        traceback.print_exc()
        return 0.0

# ------------------------------------------------------------------
# Execute when run as a script
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Path provided by the grading environment
    FILE_PATH = "/home/user/slide_199_is_still_showing_the_default_bullets_but_i_need_them_to_use_the_unicode_u2192_arrow_bullet_golden.pptx"
    verify_task(FILE_PATH)

