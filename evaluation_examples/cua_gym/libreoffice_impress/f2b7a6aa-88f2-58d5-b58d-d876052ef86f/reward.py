"""
Reward Script: Linear gradient background on slide 1
Task ID: impress_design_020
Domain: libreoffice_impress
Scoring:
  Component 1 (0.25): Slide 1 background is gradient fill
  Component 2 (0.25): First gradient stop is #2D1B69 at position 0%
  Component 3 (0.25): Second gradient stop is #0D1B2A at position 100%
  Component 4 (0.25): Gradient angle is top-to-bottom (270 deg = 16200000 EMU-angle)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_design_020'

# XML namespaces used in OOXML slide files
NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
}


def verify_task(file_path):
    """
    Verify that slide 1 has a linear gradient background from
    #2D1B69 (top) to #0D1B2A (bottom).
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Parse slide1.xml directly from the ZIP for full gradient details
    # (python-pptx API does not expose gradient stops/angle reliably)
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            with zf.open('ppt/slides/slide1.xml') as f:
                root = ET.parse(f).getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot parse slide1.xml from {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    bg = root.find('.//p:bg', NS)
    if bg is None:
        print("FAIL: No background element found on slide 1")
        print("REWARD: 0.0")
        return 0.0

    # ---------------------------------------------------------------
    # Component 1: Background uses gradient fill (0.25 points)
    # ---------------------------------------------------------------
    try:
        grad_fill = bg.find('.//a:gradFill', NS)
        if grad_fill is not None:
            print(f"PASS: Component 1 -- Slide 1 background is gradient fill (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 -- Background is not gradient fill")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # If no gradient fill, remaining checks cannot pass; still try for diagnostics
    if grad_fill is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Collect gradient stops
    gs_list = grad_fill.findall('.//a:gsLst/a:gs', NS)

    # ---------------------------------------------------------------
    # Component 2: First stop is #2D1B69 at position 0% (0.25 points)
    # ---------------------------------------------------------------
    try:
        if len(gs_list) >= 1:
            stop0 = gs_list[0]
            pos0 = stop0.get('pos', '')
            clr_elem0 = stop0.find('a:srgbClr', NS)
            color0 = clr_elem0.get('val', '').upper() if clr_elem0 is not None else None

            pos_ok = (pos0 == '0')
            color_ok = (color0 == '2D1B69')

            if pos_ok and color_ok:
                print(f"PASS: Component 2 -- First stop color #2D1B69 at pos 0% (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 -- First stop: pos={pos0} (expect 0), color={color0} (expect 2D1B69)")
        else:
            print(f"FAIL: Component 2 -- No gradient stops found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # ---------------------------------------------------------------
    # Component 3: Second stop is #0D1B2A at position 100% (0.25 points)
    # ---------------------------------------------------------------
    try:
        if len(gs_list) >= 2:
            stop1 = gs_list[1]
            pos1 = stop1.get('pos', '')
            clr_elem1 = stop1.find('a:srgbClr', NS)
            color1 = clr_elem1.get('val', '').upper() if clr_elem1 is not None else None

            pos_ok = (pos1 == '100000')
            color_ok = (color1 == '0D1B2A')

            if pos_ok and color_ok:
                print(f"PASS: Component 3 -- Second stop color #0D1B2A at pos 100% (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- Second stop: pos={pos1} (expect 100000), color={color1} (expect 0D1B2A)")
        else:
            print(f"FAIL: Component 3 -- Less than 2 gradient stops found (found {len(gs_list)})")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # ---------------------------------------------------------------
    # Component 4: Linear gradient angle = 16200000 (top-to-bottom) (0.25 points)
    # ---------------------------------------------------------------
    try:
        lin = grad_fill.find('a:lin', NS)
        if lin is not None:
            ang = lin.get('ang', '')
            if ang == '16200000':
                print(f"PASS: Component 4 -- Gradient angle is 16200000 (top-to-bottom) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 -- Gradient angle is {ang}, expected 16200000")
        else:
            print(f"FAIL: Component 4 -- No linear gradient element found (may be radial or other)")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
