"""
Reward Script: Add tab stops to slide 4 text box
Task ID: impress_tct_094
Domain: libreoffice_impress
Scoring:
  Component 1 (0.35): Left tab stop at 1 inch (914400 EMU) exists
  Component 2 (0.35): Center tab stop at 3 inches (2743200 EMU) exists
  Component 3 (0.30): Right tab stop at 5 inches (4572000 EMU) exists
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_tct_094'

# Expected tab stops: (position_emu, alignment)
EXPECTED_TABS = [
    (914400, 'l'),      # left tab at 1 inch
    (2743200, 'ctr'),   # center tab at 3 inches
    (4572000, 'r'),     # right tab at 5 inches
]

# Tolerance for position: 2% of expected value
POSITION_TOLERANCE = 0.02


def persist_app_state(domain):
    """Save any unsaved LibreOffice changes before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for libreoffice_impress")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    We check that slide 4's text box (the one with tab characters)
    has custom tab stops defined in the XML. Specifically:
      - Left tab at 1 inch (914400 EMU)
      - Center tab at 3 inches (2743200 EMU)
      - Right tab at 5 inches (4572000 EMU)

    We require that at least one paragraph in the text box has
    each tab stop defined. Tab stops are checked with position tolerance.
    """
    total_score = 0.0

    ns = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    }

    # Load and parse slide 4 XML
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            with zf.open('ppt/slides/slide4.xml') as f:
                root = ET.parse(f).getroot()
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find all text boxes on slide 4 that contain tab characters
    # We need to find the specific text box with tabbed content (TextBox 3 / the data text box)
    try:
        # Find all shape trees
        sp_tree = root.find('.//p:cSld/p:spTree', ns)
        if sp_tree is None:
            print("FAIL: Cannot find shape tree in slide 4")
            print("REWARD: 0.0")
            return 0.0

        # Collect tab stops from all text boxes that contain tab characters
        all_tab_data = []  # list of lists of (pos, algn) tuples

        for sp in sp_tree:
            # Check if this shape has text with tab characters
            texts = sp.findall('.//a:t', ns)
            has_tabs = any('\t' in (t.text or '') for t in texts)

            if not has_tabs:
                continue

            # This shape has tab characters - collect its tab stops
            tab_lists = sp.findall('.//a:tabLst', ns)
            for tl in tab_lists:
                tabs_in_list = []
                for tab in tl:
                    pos_str = tab.get('pos')
                    algn = tab.get('algn')
                    if pos_str is not None:
                        tabs_in_list.append((int(pos_str), algn))
                if tabs_in_list:
                    all_tab_data.append(tabs_in_list)

        if not all_tab_data:
            print("FAIL: No tab stops found in any text box with tab characters on slide 4")
            print("REWARD: 0.0")
            return 0.0

        print(f"INFO: Found {len(all_tab_data)} paragraph(s) with tab stops in the tabbed text box")

    except Exception as e:
        print(f"ERROR: Failed to parse slide 4 XML: {e}")
        print("REWARD: 0.0")
        return 0.0

    def pos_matches(actual, expected, tolerance=POSITION_TOLERANCE):
        """Check if position matches within tolerance."""
        if expected == 0:
            return actual == 0
        return abs(actual - expected) / expected <= tolerance

    # Component 1: Left tab at 1 inch (914400 EMU) (0.35 points)
    try:
        found_left = False
        for tab_list in all_tab_data:
            for pos, algn in tab_list:
                if pos_matches(pos, 914400) and algn == 'l':
                    found_left = True
                    break
            if found_left:
                break

        if found_left:
            print(f"PASS: Component 1 - Left tab stop at ~1 inch found (0.35 pts)")
            total_score += 0.35
        else:
            # Check if there's a left-ish tab at any position
            all_tabs_flat = [(p, a) for tl in all_tab_data for p, a in tl]
            left_tabs = [(p, a) for p, a in all_tabs_flat if a == 'l']
            print(f"FAIL: Component 1 - No left tab at 914400 EMU. Left tabs found: {left_tabs}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Center tab at 3 inches (2743200 EMU) (0.35 points)
    try:
        found_center = False
        for tab_list in all_tab_data:
            for pos, algn in tab_list:
                if pos_matches(pos, 2743200) and algn == 'ctr':
                    found_center = True
                    break
            if found_center:
                break

        if found_center:
            print(f"PASS: Component 2 - Center tab stop at ~3 inches found (0.35 pts)")
            total_score += 0.35
        else:
            all_tabs_flat = [(p, a) for tl in all_tab_data for p, a in tl]
            ctr_tabs = [(p, a) for p, a in all_tabs_flat if a == 'ctr']
            print(f"FAIL: Component 2 - No center tab at 2743200 EMU. Center tabs found: {ctr_tabs}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Right tab at 5 inches (4572000 EMU) (0.30 points)
    try:
        found_right = False
        for tab_list in all_tab_data:
            for pos, algn in tab_list:
                if pos_matches(pos, 4572000) and algn == 'r':
                    found_right = True
                    break
            if found_right:
                break

        if found_right:
            print(f"PASS: Component 3 - Right tab stop at ~5 inches found (0.30 pts)")
            total_score += 0.30
        else:
            all_tabs_flat = [(p, a) for tl in all_tab_data for p, a in tl]
            right_tabs = [(p, a) for p, a in all_tabs_flat if a == 'r']
            print(f"FAIL: Component 3 - No right tab at 4572000 EMU. Right tabs found: {right_tabs}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_impress")

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
