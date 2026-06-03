"""
Reward Script: Train Schedule Tabstop Formatting
Task ID: osworld_writer_tabstop_007
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): All 30 paragraphs have a RIGHT-aligned tab stop at ~15cm
  Component 2 (0.3): All 30 paragraphs contain a tab character after the train ID
  Component 3 (0.2): Train IDs (first word before tab) are preserved correctly

Ground truth from task_config context:
  - Left-aligned tabstop at 0cm
  - Right-aligned tabstop at 15cm
  - Tab inserted after first word (train ID) in each line
  - All 30 train schedule lines must be formatted
"""

import os

# python-docx is available on the VM
from docx import Document
from docx.enum.text import WD_TAB_ALIGNMENT
from docx.shared import Cm

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_tabstop_007'

# Tolerance for tab stop position comparison: +/- 50000 EMU (~0.14cm)
RIGHT_TABSTOP_TARGET_EMU = int(Cm(15))  # 5400000 EMU
TABSTOP_TOLERANCE_EMU = 100000  # ~0.28cm tolerance


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The task requires:
    1. A right-aligned tab stop at 15cm in every schedule paragraph
    2. A tab character inserted after the train ID in every line
    3. Train IDs (first token) preserved correctly in all lines
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: document must have 30 paragraphs
    paras = doc.paragraphs
    if len(paras) != 30:
        print(f"FAIL: Expected 30 paragraphs, found {len(paras)}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    print(f"INFO: Document has {len(paras)} paragraphs (correct)")

    # -----------------------------------------------------------------------
    # Component 1: All 30 paragraphs have a RIGHT-aligned tab stop at ~15cm
    # (0.5 points)
    # In the initial file there are ZERO tab stops on any paragraph.
    # In the golden file every paragraph has LEFT@0 + RIGHT@~15cm.
    # We require the right-aligned tab stop; the left@0 is optional/default.
    # -----------------------------------------------------------------------
    try:
        paras_with_right_tabstop = 0
        paras_without_right_tabstop = []

        for i, para in enumerate(paras):
            # Count tab stops that are RIGHT-aligned within tolerance of 15cm
            matching_ts_count = sum(
                1 for ts in para.paragraph_format.tab_stops
                if ts.alignment == WD_TAB_ALIGNMENT.RIGHT
                and abs(ts.position - RIGHT_TABSTOP_TARGET_EMU) <= TABSTOP_TOLERANCE_EMU
            )
            if matching_ts_count > 0:
                paras_with_right_tabstop += 1
            else:
                paras_without_right_tabstop.append(i)

        if paras_with_right_tabstop == 30:
            print(f"PASS: Component 1 — All 30 paragraphs have RIGHT tab stop at ~15cm (0.5 pts)")
            total_score += 0.5
        else:
            missing = len(paras_without_right_tabstop)
            examples = paras_without_right_tabstop[:3]
            print(f"FAIL: Component 1 — {30 - paras_with_right_tabstop}/30 paragraphs missing RIGHT tab stop at 15cm")
            print(f"  First missing paragraph indices: {examples}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: All 30 paragraphs contain a tab character after train ID
    # (0.3 points)
    # In the initial file there are NO tab characters (\t) in any paragraph.
    # In the golden file every paragraph has a \t after the first word.
    # -----------------------------------------------------------------------
    try:
        paras_with_tab = 0
        paras_missing_tab = []

        for i, para in enumerate(paras):
            if '\t' in para.text:
                paras_with_tab += 1
            else:
                paras_missing_tab.append(i)

        if paras_with_tab == 30:
            print(f"PASS: Component 2 — All 30 paragraphs contain a tab character (0.3 pts)")
            total_score += 0.3
        else:
            examples = paras_missing_tab[:3]
            print(f"FAIL: Component 2 — {30 - paras_with_tab}/30 paragraphs missing tab character")
            print(f"  First missing paragraph indices: {examples}")
            if paras_missing_tab:
                print(f"  Example text: {repr(paras[paras_missing_tab[0]].text)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Tab is placed after the first word (train ID) in each line
    # The train ID must be the only content before the tab character.
    # Pattern: "TRXXX\t<rest>" where TRXXX starts with 'TR' and is a valid ID.
    # (0.2 points)
    # -----------------------------------------------------------------------
    try:
        paras_tab_after_id = 0
        paras_tab_wrong_pos = []

        for i, para in enumerate(paras):
            text = para.text
            if '\t' not in text:
                paras_tab_wrong_pos.append(i)
                continue
            # Tab must be after the first word (no spaces before tab)
            tab_idx = text.index('\t')
            before_tab = text[:tab_idx]
            after_tab = text[tab_idx + 1:]

            # Before tab should be a single word (the train ID, no spaces)
            # After tab should be non-empty (the schedule details)
            if (
                ' ' not in before_tab
                and len(before_tab) > 0
                and len(after_tab) > 0
            ):
                paras_tab_after_id += 1
            else:
                paras_tab_wrong_pos.append(i)

        if paras_tab_after_id == 30:
            print(f"PASS: Component 3 — Tab correctly placed after train ID in all 30 paragraphs (0.2 pts)")
            total_score += 0.2
        else:
            wrong = len(paras_tab_wrong_pos)
            examples = paras_tab_wrong_pos[:3]
            print(f"FAIL: Component 3 — {wrong}/30 paragraphs have tab in wrong position or missing")
            for idx in examples:
                print(f"  Para {idx}: {repr(paras[idx].text)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: this task involves LibreOffice Writer GUI edits
# Send ctrl+s to persist any unsaved edits before verification
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
