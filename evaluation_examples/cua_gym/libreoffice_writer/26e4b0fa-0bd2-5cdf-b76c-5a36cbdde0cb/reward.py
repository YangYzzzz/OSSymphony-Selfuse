"""
Reward Script: Add 0.5 cm bullet-text spacing and 1.0 cm list indent
Task ID: writer_lec_028
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Bullet position at 1.0 cm (left - hanging) for majority of list items
  Component 2 (0.3): Text indent at 1.5 cm (0.5 cm gap) with tab stop for majority of list items
  Component 3 (0.3): All 10 list bullet items have consistent formatting
"""

import os
from docx import Document
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_028'

# Namespace for Word XML
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W_NS}

# Expected XML values (in the OOXML unit used by w:ind, which maps to EMU in the XML)
# Task: bullet at 1.0 cm, text at 1.5 cm (0.5 cm spacing between bullet and text)
# In OOXML units: 1 cm ~ 360000
# w:left = 540000 (1.5 cm = text indent position)
# w:hanging = 180000 (0.5 cm = hanging indent, so bullet = left - hanging = 1.0 cm)
# Tab at 540000 (text starts at 1.5 cm)
#
# We use a tolerance of 10% to allow for slight rounding differences
EXPECTED_LEFT = 540000       # 1.5 cm text indent
EXPECTED_HANGING = 180000    # 0.5 cm hanging
TOLERANCE = 54000            # ~10% tolerance


def get_list_bullet_paras(doc):
    """Return list of paragraphs with ListBullet style."""
    bullet_paras = []
    for para in doc.paragraphs:
        if para.style and para.style.name == 'List Bullet':
            bullet_paras.append(para)
    return bullet_paras


def get_indent_values(para):
    """Extract w:ind left and hanging values from paragraph XML.
    Returns (left, hanging) as integers, or (None, None) if not set.
    """
    pPr = para._element.find(f'{{{W_NS}}}pPr')
    if pPr is None:
        return (None, None)
    ind = pPr.find(f'{{{W_NS}}}ind')
    if ind is None:
        return (None, None)
    left_val = ind.get(f'{{{W_NS}}}left')
    hanging_val = ind.get(f'{{{W_NS}}}hanging')
    left = int(left_val) if left_val else None
    hanging = int(hanging_val) if hanging_val else None
    return (left, hanging)


def get_tab_positions(para):
    """Extract tab stop positions from paragraph XML.
    Returns list of (val, pos) tuples.
    """
    pPr = para._element.find(f'{{{W_NS}}}pPr')
    if pPr is None:
        return []
    tabs_elem = pPr.find(f'{{{W_NS}}}tabs')
    if tabs_elem is None:
        return []
    result = []
    for tab in tabs_elem.findall(f'{{{W_NS}}}tab'):
        val = tab.get(f'{{{W_NS}}}val')
        pos = tab.get(f'{{{W_NS}}}pos')
        if pos:
            result.append((val, int(pos)))
    return result


def within_tolerance(actual, expected, tol):
    """Check if actual value is within tolerance of expected."""
    return abs(actual - expected) <= tol


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get all list bullet paragraphs
    bullet_paras = get_list_bullet_paras(doc)
    num_bullets = len(bullet_paras)
    print(f"INFO: Found {num_bullets} List Bullet paragraphs")

    if num_bullets == 0:
        print("FAIL: No List Bullet paragraphs found")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Bullet position at ~1.0 cm (0.4 points)
    # Bullet position = w:left - w:hanging
    # Expected: 540000 - 180000 = 360000 (1.0 cm)
    try:
        correct_bullet_pos = 0
        for para in bullet_paras:
            left, hanging = get_indent_values(para)
            if left is not None and hanging is not None:
                bullet_pos = left - hanging
                expected_bullet_pos = EXPECTED_LEFT - EXPECTED_HANGING  # 360000
                if within_tolerance(bullet_pos, expected_bullet_pos, TOLERANCE):
                    correct_bullet_pos += 1

        ratio = correct_bullet_pos / num_bullets if num_bullets > 0 else 0
        if ratio >= 0.8:
            pts = 0.4
            print(f"PASS: Component 1 -- Bullet at ~1.0 cm for {correct_bullet_pos}/{num_bullets} items ({pts} pts)")
            total_score += pts
        elif ratio >= 0.5:
            pts = 0.2
            print(f"PARTIAL: Component 1 -- Bullet at ~1.0 cm for {correct_bullet_pos}/{num_bullets} items ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 1 -- Bullet at ~1.0 cm for only {correct_bullet_pos}/{num_bullets} items")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Text indent at ~1.5 cm with proper hanging indent (0.3 points)
    # w:left should be ~540000 (1.5 cm) and w:hanging should be ~180000 (0.5 cm)
    try:
        correct_indent = 0
        for para in bullet_paras:
            left, hanging = get_indent_values(para)
            if (left is not None and hanging is not None and
                within_tolerance(left, EXPECTED_LEFT, TOLERANCE) and
                within_tolerance(hanging, EXPECTED_HANGING, TOLERANCE)):
                correct_indent += 1

        ratio = correct_indent / num_bullets if num_bullets > 0 else 0
        if ratio >= 0.8:
            pts = 0.3
            print(f"PASS: Component 2 -- Correct indent values for {correct_indent}/{num_bullets} items ({pts} pts)")
            total_score += pts
        elif ratio >= 0.5:
            pts = 0.15
            print(f"PARTIAL: Component 2 -- Correct indent values for {correct_indent}/{num_bullets} items ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 2 -- Correct indent values for only {correct_indent}/{num_bullets} items")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Tab stop at text position (~540000) for all items (0.3 points)
    # The tab stop ensures the text starts at the correct position after the bullet
    try:
        correct_tab = 0
        for para in bullet_paras:
            tabs = get_tab_positions(para)
            matching_tabs = [pos for val, pos in tabs
                             if within_tolerance(pos, EXPECTED_LEFT, TOLERANCE)]
            if len(matching_tabs) > 0:
                correct_tab += 1

        ratio = correct_tab / num_bullets if num_bullets > 0 else 0
        if ratio >= 0.8:
            pts = 0.3
            print(f"PASS: Component 3 -- Tab stop at ~1.5 cm for {correct_tab}/{num_bullets} items ({pts} pts)")
            total_score += pts
        elif ratio >= 0.5:
            pts = 0.15
            print(f"PARTIAL: Component 3 -- Tab stop at ~1.5 cm for {correct_tab}/{num_bullets} items ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 3 -- Tab stop at ~1.5 cm for only {correct_tab}/{num_bullets} items")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification (LibreOffice may have unsaved edits)
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)
