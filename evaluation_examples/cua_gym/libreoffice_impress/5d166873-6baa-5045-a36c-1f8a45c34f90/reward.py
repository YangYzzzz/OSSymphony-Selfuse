"""
Reward Script: Set master slide body text bullets to square (orange #FF8C00) for level 1
               and circle (light orange #FFB347) for level 2.
Task ID: impress_ma_027
Domain: libreoffice_impress
Scoring:
  Component 1 (0.25): Level 1 bullet character is square
  Component 2 (0.25): Level 1 bullet color is #FF8C00
  Component 3 (0.25): Level 2 bullet character is circle
  Component 4 (0.25): Level 2 bullet color is #FFB347
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'impress_ma_027'

NS_A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'

# Acceptable square bullet characters
SQUARE_CHARS = {'\u25A0', '\u25AA', '\u25FE', '\u25FC', '\u25FB', '\u25A1'}  # various square bullets
# Acceptable circle bullet characters
CIRCLE_CHARS = {'\u25CF', '\u25CB', '\u25CE', '\u25C9', '\u26AB', '\u25EF', '\u2022', '\u25E6', '\u25C6'}
# More specific: filled square and filled circle
SQUARE_CHAR_PRIMARY = '\u25A0'  # Black Square (filled)
CIRCLE_CHAR_PRIMARY = '\u25CF'  # Black Circle (filled)


def find_bullet_props_in_master(pptx_path):
    """
    Search the slide master for bullet character and color settings for levels 1 and 2.
    Checks both the bodyStyle element and body placeholder shapes in the master.
    Returns dict: {1: {'char': ..., 'color': ...}, 2: {'char': ..., 'color': ...}}
    """
    results = {1: {'char': None, 'color': None}, 2: {'char': None, 'color': None}}

    with zipfile.ZipFile(pptx_path, 'r') as zf:
        # --- Check bodyStyle in slide master ---
        try:
            with zf.open('ppt/slideMasters/slideMaster1.xml') as f:
                root = ET.parse(f).getroot()

            # Check bodyStyle element
            bodyStyle = root.find(f'.//{{{NS_P}}}bodyStyle')
            if bodyStyle is not None:
                for level in [1, 2]:
                    lvl_elem = bodyStyle.find(f'{{{NS_A}}}lvl{level}pPr')
                    if lvl_elem is not None:
                        buChar = lvl_elem.find(f'{{{NS_A}}}buChar')
                        buClr = lvl_elem.find(f'{{{NS_A}}}buClr')
                        if buChar is not None:
                            results[level]['char'] = buChar.get('char')
                        if buClr is not None:
                            srgb = buClr.find(f'{{{NS_A}}}srgbClr')
                            if srgb is not None:
                                results[level]['color'] = srgb.get('val')

            # Check body placeholder shapes in master (lstStyle overrides)
            for sp in root.iter(f'{{{NS_P}}}sp'):
                nvSpPr = sp.find(f'{{{NS_P}}}nvSpPr')
                if nvSpPr is not None:
                    ph = nvSpPr.find(f'.//{{{NS_P}}}ph')
                    if ph is not None:
                        ph_type = ph.get('type', '')
                        ph_idx = ph.get('idx', '')
                        # Body placeholder: type="body" or idx="1"
                        if ph_type == 'body' or ph_idx == '1':
                            txBody = sp.find(f'{{{NS_P}}}txBody')
                            if txBody is None:
                                txBody = sp.find(f'{{{NS_A}}}txBody')
                            if txBody is not None:
                                lstStyle = txBody.find(f'{{{NS_A}}}lstStyle')
                                if lstStyle is not None:
                                    for level in [1, 2]:
                                        lvl_elem = lstStyle.find(f'{{{NS_A}}}lvl{level}pPr')
                                        if lvl_elem is not None:
                                            buChar = lvl_elem.find(f'{{{NS_A}}}buChar')
                                            buClr = lvl_elem.find(f'{{{NS_A}}}buClr')
                                            if buChar is not None:
                                                results[level]['char'] = buChar.get('char')
                                            if buClr is not None:
                                                srgb = buClr.find(f'{{{NS_A}}}srgbClr')
                                                if srgb is not None:
                                                    results[level]['color'] = srgb.get('val')
        except KeyError:
            print("ERROR: slideMaster1.xml not found")

        # --- Also check slide layouts for consistent application ---
        # We look for layouts that have body placeholders with bullet overrides
        layout_count = 0
        layout_with_bullets = 0
        for name in sorted(zf.namelist()):
            if 'slideLayout' in name and name.endswith('.xml'):
                try:
                    with zf.open(name) as f:
                        content = f.read().decode('utf-8')
                    # Only count layouts that have body placeholders
                    if 'ph' in content and ('idx="1"' in content or 'type="body"' in content):
                        layout_count += 1
                        if 'buClr' in content or 'buChar' in content:
                            layout_with_bullets += 1
                except Exception:
                    pass

        results['layout_count'] = layout_count
        results['layout_with_bullets'] = layout_with_bullets

    return results


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

    try:
        bullet_props = find_bullet_props_in_master(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot analyze file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    lvl1 = bullet_props[1]
    lvl2 = bullet_props[2]

    print(f"Level 1 bullet: char='{lvl1['char']}' color='{lvl1['color']}'")
    print(f"Level 2 bullet: char='{lvl2['char']}' color='{lvl2['color']}'")
    print(f"Layouts with body ph: {bullet_props.get('layout_count', 0)}, "
          f"with bullet overrides: {bullet_props.get('layout_with_bullets', 0)}")

    # Component 1: Level 1 bullet character is square (0.25 points)
    try:
        lvl1_char = lvl1['char']
        if lvl1_char is not None and lvl1_char in SQUARE_CHARS:
            print(f"PASS: Component 1 — Level 1 bullet is square '{lvl1_char}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Level 1 bullet char is '{lvl1_char}', expected square")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Level 1 bullet color is #FF8C00 (0.25 points)
    try:
        lvl1_color = lvl1['color']
        if lvl1_color is not None and lvl1_color.upper() == 'FF8C00':
            print(f"PASS: Component 2 — Level 1 bullet color is #{lvl1_color} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Level 1 bullet color is '{lvl1_color}', expected FF8C00")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Level 2 bullet character is circle (0.25 points)
    try:
        lvl2_char = lvl2['char']
        if lvl2_char is not None and lvl2_char in CIRCLE_CHARS:
            print(f"PASS: Component 3 — Level 2 bullet is circle '{lvl2_char}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Level 2 bullet char is '{lvl2_char}', expected circle")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Level 2 bullet color is #FFB347 (0.25 points)
    try:
        lvl2_color = lvl2['color']
        if lvl2_color is not None and lvl2_color.upper() == 'FFB347':
            print(f"PASS: Component 4 — Level 2 bullet color is #{lvl2_color} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — Level 2 bullet color is '{lvl2_color}', expected FFB347")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice edits before scoring
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_impress")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.pptx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
