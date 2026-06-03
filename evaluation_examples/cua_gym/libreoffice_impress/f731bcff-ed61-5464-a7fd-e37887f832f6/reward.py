"""
Reward Script: Duplicate master slide, rename to 'Alternate Layout', change background to #F8F9FA
Task ID: impress_ma_037
Domain: libreoffice_impress
Scoring:
  Component 1: Two master slides exist (0.25 pts)
  Component 2: Second master named 'Alternate Layout' (0.25 pts)
  Component 3: 'Alternate Layout' background is #F8F9FA (0.30 pts)
  Component 4: Original 'Default' master still has #FFFFFF background (0.20 pts)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ma_037'

P_NS = 'http://schemas.openxmlformats.org/presentationml/2006/main'
A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'


def get_master_info(pptx_path):
    """Parse all slide masters from the pptx ZIP, returning list of (name, bg_color_hex)."""
    masters = []
    with zipfile.ZipFile(pptx_path, 'r') as z:
        master_files = sorted([
            f for f in z.namelist()
            if 'slideMaster' in f and f.endswith('.xml') and '/_rels/' not in f
        ])
        for mf in master_files:
            root = ET.parse(z.open(mf)).getroot()
            csld = root.find(f'{{{P_NS}}}cSld')
            name = csld.get('name', '') if csld is not None else ''

            # Extract background color
            bg_color = None
            bg = root.find(f'.//{{{P_NS}}}bg')
            if bg is not None:
                solid = bg.find(f'.//{{{A_NS}}}srgbClr')
                if solid is not None:
                    bg_color = solid.get('val', '').upper()
            masters.append((name, bg_color))
    return masters


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        masters = get_master_info(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(masters)} master slide(s):")
    for i, (name, bg) in enumerate(masters):
        print(f"  Master {i}: name='{name}', bg=#{bg}")

    # Component 1: Two master slides exist (0.25 points)
    # Initial has 1 master; golden should have 2.
    try:
        if len(masters) >= 2:
            print(f"PASS: Component 1 - Found {len(masters)} master slides (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 - Expected >= 2 master slides, found {len(masters)}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: A master slide named 'Alternate Layout' exists (0.25 points)
    try:
        alt_masters = [(name, bg) for name, bg in masters if name == 'Alternate Layout']
        if len(alt_masters) >= 1:
            print(f"PASS: Component 2 - Found master named 'Alternate Layout' (0.25 pts)")
            total_score += 0.25
        else:
            all_names = [name for name, _ in masters]
            print(f"FAIL: Component 2 - No master named 'Alternate Layout'. Found: {all_names}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: 'Alternate Layout' master has background #F8F9FA (0.30 points)
    try:
        alt_masters = [(name, bg) for name, bg in masters if name == 'Alternate Layout']
        if len(alt_masters) >= 1:
            alt_bg = alt_masters[0][1]
            if alt_bg is not None and alt_bg == 'F8F9FA':
                print(f"PASS: Component 3 - 'Alternate Layout' background is #F8F9FA (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 - 'Alternate Layout' background is #{alt_bg}, expected #F8F9FA")
        else:
            print(f"FAIL: Component 3 - No 'Alternate Layout' master to check background")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: 'Default' master still has #FFFFFF background (0.20 points)
    # This ensures the original was not modified. Only scores if 'Alternate Layout' also exists
    # (otherwise the task hasn't been attempted, and this check would pass vacuously on initial).
    try:
        default_masters = [(name, bg) for name, bg in masters if name == 'Default']
        alt_exists = any(name == 'Alternate Layout' for name, _ in masters)
        if len(default_masters) >= 1 and alt_exists:
            default_bg = default_masters[0][1]
            if default_bg is not None and default_bg == 'FFFFFF':
                print(f"PASS: Component 4 - 'Default' master still has #FFFFFF background (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 - 'Default' background is #{default_bg}, expected #FFFFFF")
        elif not alt_exists:
            print(f"FAIL: Component 4 - Skipped (no 'Alternate Layout' master found, task not attempted)")
        else:
            print(f"FAIL: Component 4 - No 'Default' master found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

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
