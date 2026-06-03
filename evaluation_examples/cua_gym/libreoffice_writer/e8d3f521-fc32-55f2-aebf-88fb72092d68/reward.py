"""
Reward Script: Apply tab stops to format a cast list in a theater program
Task ID: writer_rd_078
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): LEFT tab stop at ~1.0 cm on cast paragraphs
  Component 2 (0.35): CENTER tab stop at ~8.0 cm with DOT leader on cast paragraphs
  Component 3 (0.30): RIGHT tab stop at ~15.0 cm on cast paragraphs
"""

import os

from docx import Document
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER

WORKDIR = '/home/user'
TASK_ID = 'writer_rd_078'

# Tab stop position tolerance: +/- 0.3 cm in EMU (1 cm = 360000 EMU)
CM_TO_EMU = 360000
TOLERANCE_EMU = int(0.3 * CM_TO_EMU)  # 108000 EMU

# Expected tab positions
LEFT_POS = int(1.0 * CM_TO_EMU)    # 360000
CENTER_POS = int(8.0 * CM_TO_EMU)  # 2880000
RIGHT_POS = int(15.0 * CM_TO_EMU)  # 5400000

# Cast character names to identify cast paragraphs
CAST_NAMES = ['Antonio', 'Portia', 'Shylock', 'Bassanio', 'Nerissa', 'Gratiano', 'Jessica', 'Lorenzo']


def find_cast_paragraphs(doc):
    """Find paragraphs that belong to the cast list section."""
    cast_paras = []
    in_cast_section = False
    for para in doc.paragraphs:
        # Detect 'Cast' heading
        if para.style and 'Heading' in para.style.name and 'Cast' in para.text:
            in_cast_section = True
            continue
        # Detect next heading (exit cast section)
        if in_cast_section and para.style and 'Heading' in para.style.name:
            break
        # Collect non-empty paragraphs in cast section
        if in_cast_section and para.text.strip():
            # Verify it contains a known cast name
            text = para.text.strip()
            if any(name in text for name in CAST_NAMES):
                cast_paras.append(para)
    return cast_paras


def get_custom_tab_stops(para):
    """Get non-default tab stops from a paragraph, filtering CLEAR and LEFT@0."""
    tabs = []
    tab_stops = para.paragraph_format.tab_stops
    if tab_stops is None:
        return tabs
    for ts in tab_stops:
        if ts.alignment == WD_TAB_ALIGNMENT.CLEAR:
            continue
        if ts.alignment == WD_TAB_ALIGNMENT.LEFT and ts.position == 0:
            continue
        tabs.append(ts)
    return tabs


def has_tab_near(tabs, target_pos, target_align, tolerance=TOLERANCE_EMU):
    """Check if any tab stop matches the target alignment and is within tolerance of target position."""
    for ts in tabs:
        if ts.alignment == target_align and abs(ts.position - target_pos) <= tolerance:
            return ts
    return None


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

    # Find cast paragraphs
    cast_paras = find_cast_paragraphs(doc)
    if len(cast_paras) == 0:
        print("FAIL: No cast paragraphs found in the document")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(cast_paras)} cast paragraphs")

    # Component 1: LEFT tab stop at ~1.0 cm on cast paragraphs (0.35 points)
    try:
        left_pass = 0
        for para in cast_paras:
            tabs = get_custom_tab_stops(para)
            match = has_tab_near(tabs, LEFT_POS, WD_TAB_ALIGNMENT.LEFT)
            if match:
                left_pass += 1
            else:
                print(f"  FAIL(C1): Para '{para.text[:40]}' missing LEFT tab at ~1cm")

        if left_pass == len(cast_paras):
            print(f"PASS: Component 1 -- LEFT tab at ~1.0cm on all {left_pass} cast lines (0.35 pts)")
            total_score += 0.35
        elif left_pass > 0:
            partial = 0.35 * (left_pass / len(cast_paras))
            print(f"PARTIAL: Component 1 -- LEFT tab on {left_pass}/{len(cast_paras)} lines ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 -- No cast paragraphs have LEFT tab at ~1.0cm")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: CENTER tab stop at ~8.0 cm with DOT leader on cast paragraphs (0.35 points)
    try:
        center_pass = 0
        for para in cast_paras:
            tabs = get_custom_tab_stops(para)
            match = has_tab_near(tabs, CENTER_POS, WD_TAB_ALIGNMENT.CENTER)
            if match:
                # Also check for dot leader
                if match.leader == WD_TAB_LEADER.DOTS:
                    center_pass += 1
                else:
                    print(f"  FAIL(C2): Para '{para.text[:40]}' has CENTER tab but leader={match.leader}, expected DOTS")
            else:
                print(f"  FAIL(C2): Para '{para.text[:40]}' missing CENTER tab at ~8cm")

        if center_pass == len(cast_paras):
            print(f"PASS: Component 2 -- CENTER tab at ~8.0cm with DOT leader on all {center_pass} cast lines (0.35 pts)")
            total_score += 0.35
        elif center_pass > 0:
            partial = 0.35 * (center_pass / len(cast_paras))
            print(f"PARTIAL: Component 2 -- CENTER+DOTS tab on {center_pass}/{len(cast_paras)} lines ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No cast paragraphs have CENTER tab at ~8.0cm with DOT leader")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: RIGHT tab stop at ~15.0 cm on cast paragraphs (0.30 points)
    try:
        right_pass = 0
        for para in cast_paras:
            tabs = get_custom_tab_stops(para)
            match = has_tab_near(tabs, RIGHT_POS, WD_TAB_ALIGNMENT.RIGHT)
            if match:
                right_pass += 1
            else:
                print(f"  FAIL(C3): Para '{para.text[:40]}' missing RIGHT tab at ~15cm")

        if right_pass == len(cast_paras):
            print(f"PASS: Component 3 -- RIGHT tab at ~15.0cm on all {right_pass} cast lines (0.30 pts)")
            total_score += 0.30
        elif right_pass > 0:
            partial = 0.30 * (right_pass / len(cast_paras))
            print(f"PARTIAL: Component 3 -- RIGHT tab on {right_pass}/{len(cast_paras)} lines ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- No cast paragraphs have RIGHT tab at ~15.0cm")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook for LibreOffice Writer
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
