"""
FINAL REWARD SCRIPT - SUCCESS
Task: Slide 64 looks too plain—could you change its background to the “25 %” pattern fill, using black (#000000) for the foreground dots and white (#FFFFFF) for the background?
Generated: 2025-09-11 00:51:24
Status: success
Model: azure-o3
Total Steps: 5
"""

import os
import re
import zipfile
from pptx import Presentation
from lxml import etree

def _color_matches(clr_elem, desired_hex, accepted_scheme):
    """Helper to check if the <a:fgClr> / <a:bgClr> matches desired hex or scheme."""
    if clr_elem is None:
        return False

    ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
    # 1) Direct RGB value
    srgb = clr_elem.find('./a:srgbClr', namespaces=ns)
    if srgb is not None and srgb.get('val', '').lower() == desired_hex.lower():
        return True

    # 2) Theme / scheme colour fallback (e.g., dk1 for black, lt1 for white)
    scheme = clr_elem.find('./a:schemeClr', namespaces=ns)
    if scheme is not None and scheme.get('val', '').lower() == accepted_scheme.lower():
        return True

    return False

def verify_slide_pattern_background(file_path):
    """Reward-script verification for Slide-64 pattern-fill background.

    Requirements (max score 1.0):
      1. Slide 64 exists ............................................. 0.3
      2. Slide-background uses 25 % pattern fill ...................... 0.4
      3. Pattern uses black (#000000) dots on white (#FFFFFF) background 0.3
    Progressive scoring: partial fulfilment yields partial credit.
    """
    print(f"Starting verification for: {file_path}")
    score = 0.0
    max_score = 1.0

    # ------------------------------------------------------------------
    # Pre-checks (no points): file must exist & load successfully
    # ------------------------------------------------------------------
    if not os.path.exists(file_path):
        print("✗ File does not exist")
        print("REWARD: 0.0")
        return 0.0
    try:
        prs = Presentation(file_path)
    except Exception as e:
        print(f"✗ Unable to load PPTX: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ------------------------------------------------------------------
    # 1) Slide presence ............................................... 0.3
    # ------------------------------------------------------------------
    if len(prs.slides) >= 64:
        print("✓ Slide 64 is present (0.3)")
        score += 0.3
    else:
        print("✗ Presentation has fewer than 64 slides → cannot verify background")
        print(f"REWARD: {score}")
        return score  # early exit – no further points possible

    # Locate slide64.xml inside the PPTX container (slides are 1-indexed)
    slide_xml_path = 'ppt/slides/slide64.xml'
    try:
        with zipfile.ZipFile(file_path) as z:
            if slide_xml_path not in z.namelist():
                print("✗ Slide XML not found inside PPTX")
                print(f"REWARD: {score}")
                return score
            slide_xml = z.read(slide_xml_path)
    except Exception as e:
        print(f"✗ Error reading slide XML: {e}")
        print(f"REWARD: {score}")
        return score

    # ------------------------------------------------------------------
    # Parse XML to inspect the background ................................
    # ------------------------------------------------------------------
    try:
        root = etree.fromstring(slide_xml)
    except Exception as e:
        print(f"✗ Error parsing slide XML: {e}")
        print(f"REWARD: {score}")
        return score

    ns = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
    }

    # Find any pattern-fill nodes in the slide background
    patt_fills = root.xpath('//p:bg/p:bgPr/a:pattFill', namespaces=ns)
    if not patt_fills:
        print("✗ No pattern fill found on slide 64 background")
        print(f"REWARD: {score}")
        return score

    # ------------------------------------------------------------------
    # 2) Correct 25 % pattern ......................................... 0.4
    # ------------------------------------------------------------------
    patt25_elem = None
    for pf in patt_fills:
        prst_attr = pf.get('prst', '').lower()
        # Normalise value by stripping punctuation (e.g., 'pct25', 'pct_25')
        simplified = re.sub(r'[^a-z0-9]', '', prst_attr)
        if simplified == 'pct25':
            patt25_elem = pf
            break

    if patt25_elem is None:
        print("✗ Pattern fill present but not 25 %")
        print(f"REWARD: {score}")
        return score

    print("✓ 25 % pattern fill found (0.4)")
    score += 0.4

    # ------------------------------------------------------------------
    # 3) Foreground & background colours .............................. 0.3
    # ------------------------------------------------------------------
    fg_elem = patt25_elem.find('./a:fgClr', namespaces=ns)
    bg_elem = patt25_elem.find('./a:bgClr', namespaces=ns)

    fg_ok = _color_matches(fg_elem, '000000', 'dk1')   # black
    bg_ok = _color_matches(bg_elem, 'ffffff', 'lt1')   # white

    if fg_ok and bg_ok:
        print("✓ Foreground and background colours are correct (0.3)")
        score += 0.3
    else:
        if not fg_ok:
            print("✗ Foreground colour incorrect (expected black #000000)")
        if not bg_ok:
            print("✗ Background colour incorrect (expected white #FFFFFF)")

    # ------------------------------------------------------------------
    # Final score (capped at 1.0) & output
    # ------------------------------------------------------------------
    final_score = min(score, max_score)
    print(f"Total score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score

# ----------------------------------------------------------------------
# Execute verification when script is run directly
# ----------------------------------------------------------------------
if __name__ == "__main__":
    FILE = "/home/user/slide_64_looks_too_plaincould_you_change_its_background_to_the_25_pattern_fill_using_black_000000_fo_golden.pptx"
    verify_slide_pattern_background(FILE)

