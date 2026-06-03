"""
Reward Script: Set gradient background on master slide
Task ID: impress_ma_013
Domain: libreoffice_impress
Scoring:
  Component 1 (0.30): Master slide has gradient fill (not solid/reference)
  Component 2 (0.40): Gradient colors are #0A1628 (top) and #1E3A5F (bottom)
  Component 3 (0.15): Gradient direction is linear top-to-bottom (angle ~5400000)
  Component 4 (0.15): All 18 slides inherit master bg (no individual overrides)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ma_013'

NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        zf = zipfile.ZipFile(file_path, 'r')
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # --- Parse master slide XML ---
    try:
        with zf.open('ppt/slideMasters/slideMaster1.xml') as f:
            master_root = ET.parse(f).getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot parse slideMaster1.xml: {e}")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    bg = master_root.find('.//p:cSld/p:bg', NS)
    if bg is None:
        print("FAIL: No background element found on master slide")
        zf.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Master slide has gradient fill (0.30 points)
    # The golden state uses bgPr > gradFill. Initial state uses bgRef (scheme color).
    try:
        bgPr = bg.find('p:bgPr', NS)
        grad_fill = None
        if bgPr is not None:
            grad_fill = bgPr.find('a:gradFill', NS)

        if grad_fill is not None:
            print(f"PASS: Component 1 — Master slide has gradient fill (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Master slide does not have gradient fill (bgPr/gradFill)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Gradient colors are correct (0.40 points)
    # Expected: pos=0 -> #0A1628, pos=100000 -> #1E3A5F
    try:
        if grad_fill is not None:
            gs_lst = grad_fill.find('a:gsLst', NS)
            if gs_lst is None:
                print("FAIL: Component 2 — No gradient stop list found")
            else:
                stops = gs_lst.findall('a:gs', NS)
                color_map = {}
                for gs in stops:
                    pos = gs.get('pos', '')
                    clr_elem = gs.find('a:srgbClr', NS)
                    if clr_elem is not None:
                        color_map[pos] = clr_elem.get('val', '').upper()

                start_color = color_map.get('0', '')
                end_color = color_map.get('100000', '')

                start_ok = start_color == '0A1628'
                end_ok = end_color == '1E3A5F'

                if start_ok and end_ok:
                    print(f"PASS: Component 2 — Gradient colors correct: start={start_color}, end={end_color} (0.40 pts)")
                    total_score += 0.40
                elif start_ok or end_ok:
                    # Partial credit: one color correct
                    print(f"PARTIAL: Component 2 — One color correct: start={start_color} (expect 0A1628), end={end_color} (expect 1E3A5F) (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 2 — Colors wrong: start={start_color} (expect 0A1628), end={end_color} (expect 1E3A5F)")
        else:
            print("FAIL: Component 2 — No gradient fill to check colors")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Gradient direction is linear top-to-bottom (0.15 points)
    # Expected: <a:lin ang="5400000" .../>  (5400000 = 90 degrees = top to bottom)
    try:
        if grad_fill is not None:
            lin = grad_fill.find('a:lin', NS)
            if lin is not None:
                ang = lin.get('ang', '')
                # 5400000 = top to bottom (90 degrees in 60000ths of a degree)
                if ang == '5400000':
                    print(f"PASS: Component 3 — Linear gradient angle={ang} (top-to-bottom) (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 3 — Linear gradient angle={ang}, expected 5400000 (top-to-bottom)")
            else:
                # Check for path gradient or other types
                print("FAIL: Component 3 — No linear gradient direction element found")
        else:
            print("FAIL: Component 3 — No gradient fill to check direction")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All slides inherit master bg (0.15 points)
    # No individual slide should have its own bg element that overrides the master
    try:
        slide_files = sorted([n for n in zf.namelist()
                              if n.startswith('ppt/slides/slide') and n.endswith('.xml')
                              and 'slideLayout' not in n and 'slideMaster' not in n])
        total_slides = len(slide_files)
        overrides = []

        for sf in slide_files:
            with zf.open(sf) as f:
                sroot = ET.parse(f).getroot()
                sbg = sroot.find('.//p:cSld/p:bg', NS)
                if sbg is not None:
                    overrides.append(sf)

        # This check only awards points if there IS a gradient on the master
        # (i.e., it's coupled with the task change)
        if grad_fill is not None and total_slides >= 18 and len(overrides) == 0:
            print(f"PASS: Component 4 — All {total_slides} slides inherit master gradient bg (0.15 pts)")
            total_score += 0.15
        elif grad_fill is None:
            print(f"FAIL: Component 4 — No gradient on master, so inheritance check is moot")
        elif len(overrides) > 0:
            print(f"FAIL: Component 4 — {len(overrides)} slides override master bg: {overrides}")
        else:
            print(f"FAIL: Component 4 — Only {total_slides} slides found, expected >= 18")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    zf.close()

    final_score = round(min(total_score, 1.0), 2)
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
