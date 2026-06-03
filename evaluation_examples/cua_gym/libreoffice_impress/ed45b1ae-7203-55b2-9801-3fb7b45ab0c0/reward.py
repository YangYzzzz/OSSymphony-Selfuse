"""
Reward Script: Add four guide lines to create a safe margin on a 16:9 slide
Task ID: impress_el_077
Domain: libreoffice_impress
Scoring:
  - Component 1 (0.1): guideLst element exists in viewProps.xml
  - Component 2 (0.225): Horizontal guide at 1.5cm (top margin)
  - Component 3 (0.225): Horizontal guide at 17.55cm (bottom margin)
  - Component 4 (0.225): Vertical guide at 1.5cm (left margin)
  - Component 5 (0.225): Vertical guide at 32.37cm (right margin)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_el_077'

# Guide positions in OOXML viewProps.xml use units of 1/576 inch.
# Convert cm to guide position units: pos = round(cm / 2.54 * 576)
EXPECTED_GUIDES = {
    'top':    {'orient': 'horz', 'cm': 1.5},
    'bottom': {'orient': 'horz', 'cm': 17.55},
    'left':   {'orient': 'vert', 'cm': 1.5},
    'right':  {'orient': 'vert', 'cm': 32.37},
}

GUIDE_POS_TOLERANCE = 5  # tolerance in guide position units (~0.02cm)


def cm_to_guide_pos(cm_val):
    """Convert centimeters to OOXML guide position units (1/576 inch)."""
    return round(cm_val / 2.54 * 576)


def persist_app_state(domain):
    """Try to save any unsaved LibreOffice state via Ctrl+S."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def extract_guides(pptx_path):
    """
    Extract guide lines from ppt/viewProps.xml.
    Returns a list of dicts: {'orient': 'horz'|'vert', 'pos': int}
    In OOXML, guides without orient attribute default to vertical.
    """
    ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
    guides = []
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            if 'ppt/viewProps.xml' not in zf.namelist():
                return None  # viewProps.xml doesn't exist
            with zf.open('ppt/viewProps.xml') as f:
                root = ET.parse(f).getroot()
                guide_lst = root.find('.//p:guideLst', ns)
                if guide_lst is None:
                    return []  # viewProps exists but no guideLst
                for guide in guide_lst.findall('p:guide', ns):
                    orient = guide.get('orient', 'vert')  # default is vertical
                    pos = int(guide.get('pos', '0'))
                    guides.append({'orient': orient, 'pos': pos})
    except Exception as e:
        print(f"ERROR: Failed to parse viewProps.xml: {e}")
        return None
    return guides


def find_matching_guide(guides, expected_orient, expected_cm):
    """
    Check if there's a guide matching the expected orientation and position.
    Returns True if a match is found within tolerance.
    """
    expected_pos = cm_to_guide_pos(expected_cm)
    for g in guides:
        if g['orient'] == expected_orient:
            if abs(g['pos'] - expected_pos) <= GUIDE_POS_TOLERANCE:
                return True, g['pos'], expected_pos
    return False, None, expected_pos


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Extract guides from the file
    guides = extract_guides(file_path)

    # Component 1: guideLst element exists with guides (0.1 points)
    # This checks that guide lines were added at all
    try:
        if guides is not None and len(guides) >= 4:
            print(f"PASS: Component 1 -- guideLst exists with {len(guides)} guides (0.1 pts)")
            total_score += 0.1
        elif guides is not None and len(guides) > 0:
            print(f"FAIL: Component 1 -- guideLst exists but only {len(guides)} guides (need 4)")
        elif guides is not None:
            print(f"FAIL: Component 1 -- guideLst is empty (no guides)")
        else:
            print(f"FAIL: Component 1 -- No guideLst found in viewProps.xml")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    if guides is None or len(guides) == 0:
        # No guides at all, no point checking further
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Horizontal guide at 1.5cm - top margin (0.225 points)
    try:
        found, actual_pos, expected_pos = find_matching_guide(guides, 'horz', 1.5)
        if found:
            print(f"PASS: Component 2 -- Top horizontal guide at pos={actual_pos} (expected ~{expected_pos}) (0.225 pts)")
            total_score += 0.225
        else:
            horz_guides = [g['pos'] for g in guides if g['orient'] == 'horz']
            print(f"FAIL: Component 2 -- No horizontal guide at ~{expected_pos} (1.5cm). Found horz positions: {horz_guides}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Horizontal guide at 17.55cm - bottom margin (0.225 points)
    try:
        found, actual_pos, expected_pos = find_matching_guide(guides, 'horz', 17.55)
        if found:
            print(f"PASS: Component 3 -- Bottom horizontal guide at pos={actual_pos} (expected ~{expected_pos}) (0.225 pts)")
            total_score += 0.225
        else:
            horz_guides = [g['pos'] for g in guides if g['orient'] == 'horz']
            print(f"FAIL: Component 3 -- No horizontal guide at ~{expected_pos} (17.55cm). Found horz positions: {horz_guides}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Vertical guide at 1.5cm - left margin (0.225 points)
    try:
        found, actual_pos, expected_pos = find_matching_guide(guides, 'vert', 1.5)
        if found:
            print(f"PASS: Component 4 -- Left vertical guide at pos={actual_pos} (expected ~{expected_pos}) (0.225 pts)")
            total_score += 0.225
        else:
            vert_guides = [g['pos'] for g in guides if g['orient'] == 'vert']
            print(f"FAIL: Component 4 -- No vertical guide at ~{expected_pos} (1.5cm). Found vert positions: {vert_guides}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Vertical guide at 32.37cm - right margin (0.225 points)
    try:
        found, actual_pos, expected_pos = find_matching_guide(guides, 'vert', 32.37)
        if found:
            print(f"PASS: Component 5 -- Right vertical guide at pos={actual_pos} (expected ~{expected_pos}) (0.225 pts)")
            total_score += 0.225
        else:
            vert_guides = [g['pos'] for g in guides if g['orient'] == 'vert']
            print(f"FAIL: Component 5 -- No vertical guide at ~{expected_pos} (32.37cm). Found vert positions: {vert_guides}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved state before verification
persist_app_state("libreoffice_impress")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
