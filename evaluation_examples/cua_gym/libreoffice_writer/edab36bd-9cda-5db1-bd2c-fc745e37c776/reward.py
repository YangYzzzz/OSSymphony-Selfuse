"""
Reward Script: Tab stops for budget line items
Task ID: writer_biz_049
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): All 10 budget line items have LEFT tab stop at ~0.5 inches
  Component 2 (0.4): All 10 budget line items have RIGHT tab stop with DOT leader at ~5.5 inches
  Component 3 (0.2): All 10 budget line items use tab characters for alignment
"""

import os

from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER

WORKDIR = '/home/user'
TASK_ID = 'writer_biz_049'

# Expected tab stop positions (EMU)
LEFT_TAB_POS = 457200    # 0.5 inches
RIGHT_TAB_POS = 5029200  # 5.5 inches
# Allow 10% tolerance on positions (~0.05 inches = 45720 EMU)
POS_TOLERANCE = 50000

# The 10 budget line item paragraphs are indices 5 through 14
LINE_ITEM_START = 5
LINE_ITEM_END = 14  # inclusive
NUM_LINE_ITEMS = 10


def persist_app_state(domain):
    """Save any unsaved GUI edits before verification."""
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


def get_meaningful_tab_stops(paragraph):
    """Get tab stops excluding defaults (CLEAR and LEFT@0)."""
    stops = []
    if paragraph.paragraph_format.tab_stops:
        for ts in paragraph.paragraph_format.tab_stops:
            if ts.alignment == WD_TAB_ALIGNMENT.CLEAR:
                continue
            if ts.alignment == WD_TAB_ALIGNMENT.LEFT and ts.position == 0:
                continue
            stops.append(ts)
    return stops


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

    paras = doc.paragraphs
    if len(paras) < LINE_ITEM_END + 1:
        print(f"CRITICAL: Document has only {len(paras)} paragraphs, expected at least {LINE_ITEM_END + 1}")
        print("REWARD: 0.0")
        return 0.0

    line_items = paras[LINE_ITEM_START:LINE_ITEM_END + 1]

    # Component 1: LEFT tab stop at ~0.5 inches on all 10 line items (0.4 points)
    try:
        left_tab_count = 0
        for i, para in enumerate(line_items):
            tabs = get_meaningful_tab_stops(para)
            found_left = any(
                ts.alignment == WD_TAB_ALIGNMENT.LEFT
                and abs(ts.position - LEFT_TAB_POS) <= POS_TOLERANCE
                for ts in tabs
            )
            if found_left:
                left_tab_count += 1
            else:
                print(f"FAIL: Component 1 — P{LINE_ITEM_START + i} missing LEFT tab at ~0.5in")

        if left_tab_count == NUM_LINE_ITEMS:
            print(f"PASS: Component 1 — All {NUM_LINE_ITEMS} line items have LEFT tab at ~0.5in (0.4 pts)")
            total_score += 0.4
        elif left_tab_count > 0:
            partial = round(0.4 * left_tab_count / NUM_LINE_ITEMS, 2)
            print(f"PARTIAL: Component 1 — {left_tab_count}/{NUM_LINE_ITEMS} have LEFT tab ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No line items have LEFT tab at ~0.5in")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: RIGHT tab stop with DOT leader at ~5.5 inches on all 10 line items (0.4 points)
    try:
        right_tab_count = 0
        for i, para in enumerate(line_items):
            tabs = get_meaningful_tab_stops(para)
            found_right_dot = any(
                ts.alignment == WD_TAB_ALIGNMENT.RIGHT
                and abs(ts.position - RIGHT_TAB_POS) <= POS_TOLERANCE
                and ts.leader == WD_TAB_LEADER.DOTS
                for ts in tabs
            )
            if found_right_dot:
                right_tab_count += 1
            else:
                # Log details for debugging
                tab_details = [(str(ts.alignment), ts.position, str(ts.leader)) for ts in tabs]
                print(f"FAIL: Component 2 — P{LINE_ITEM_START + i} missing RIGHT+DOT tab at ~5.5in (found: {tab_details})")

        if right_tab_count == NUM_LINE_ITEMS:
            print(f"PASS: Component 2 — All {NUM_LINE_ITEMS} line items have RIGHT+DOT tab at ~5.5in (0.4 pts)")
            total_score += 0.4
        elif right_tab_count > 0:
            partial = round(0.4 * right_tab_count / NUM_LINE_ITEMS, 2)
            print(f"PARTIAL: Component 2 — {right_tab_count}/{NUM_LINE_ITEMS} have RIGHT+DOT tab ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No line items have RIGHT+DOT tab at ~5.5in")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 10 line items use tab characters for alignment (0.2 points)
    try:
        tab_char_count = 0
        for i, para in enumerate(line_items):
            if '\t' in para.text:
                tab_char_count += 1
            else:
                print(f"FAIL: Component 3 — P{LINE_ITEM_START + i} has no tab characters in text")

        if tab_char_count == NUM_LINE_ITEMS:
            print(f"PASS: Component 3 — All {NUM_LINE_ITEMS} line items use tab characters (0.2 pts)")
            total_score += 0.2
        elif tab_char_count > 0:
            partial = round(0.2 * tab_char_count / NUM_LINE_ITEMS, 2)
            print(f"PARTIAL: Component 3 — {tab_char_count}/{NUM_LINE_ITEMS} use tab chars ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No line items use tab characters")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook — the file may still be open in LibreOffice
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
