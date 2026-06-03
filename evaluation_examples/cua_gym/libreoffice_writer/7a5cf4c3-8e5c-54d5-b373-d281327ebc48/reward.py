"""
Reward Script: Configure employee roster tab stops for left-name + right-department layout
Task ID: osworld_writer_tabstop_split_line_005
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): All 8 roster lines have RIGHT tab stop at ~16 cm
  Component 2 (0.3): All 8 roster lines have LEFT tab stop at 0 cm
  Component 3 (0.2): All 8 roster lines use a tab character to separate name and department
"""

import os
from docx import Document
from docx.enum.text import WD_TAB_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_tabstop_split_line_005'

# Expected tab stop positions (in EMU = English Metric Units)
# 16 cm = 16 * 914400 / 2.54 = 5760000 EMU (approx 5760085 observed)
# Allow ±182880 EMU (0.2 cm) tolerance for right tab
RIGHT_TAB_CM_TARGET = 16.0
RIGHT_TAB_EMU_TARGET = int(RIGHT_TAB_CM_TARGET / 2.54 * 914400)  # ~5760000
RIGHT_TAB_TOLERANCE = 182880  # ~0.2 cm in EMU

# Roster lines are paragraphs 5 through 12 (0-indexed) — 8 lines
ROSTER_START_IDX = 5
ROSTER_END_IDX = 13  # exclusive


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

    # Collect roster paragraphs (paragraphs 5-12 inclusive)
    roster_paras = doc.paragraphs[ROSTER_START_IDX:ROSTER_END_IDX]
    if len(roster_paras) != 8:
        print(f"PRECONDITION FAIL: Expected 8 roster paragraphs, found {len(roster_paras)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All 8 roster lines have a RIGHT tab stop at ~16 cm (0.5 points)
    # RIGHT tab at 16 cm allows department text to be right-aligned at the 16 cm position.
    try:
        right_tab_count = 0
        for i, para in enumerate(roster_paras):
            has_right_tab_at_16 = False
            for ts in para.paragraph_format.tab_stops:
                if ts.alignment == WD_TAB_ALIGNMENT.RIGHT:
                    if abs(ts.position - RIGHT_TAB_EMU_TARGET) <= RIGHT_TAB_TOLERANCE:
                        has_right_tab_at_16 = True
                        break
            if has_right_tab_at_16:
                right_tab_count += 1
            else:
                # Report what tab stops this line actually has
                actual_ts = [
                    f"align={ts.alignment}, pos={ts.position/914400*2.54:.2f}cm"
                    for ts in para.paragraph_format.tab_stops
                ]
                print(f"FAIL C1: Line {i+1} ('{para.text[:30]}') missing RIGHT tab at 16cm. Has: {actual_ts}")

        if right_tab_count == 8:
            print(f"PASS: Component 1 — All 8 roster lines have RIGHT tab stop at ~16 cm (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Only {right_tab_count}/8 lines have RIGHT tab stop at ~16 cm")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 8 roster lines have a LEFT tab stop at 0 cm (0.3 points)
    # LEFT tab at 0 cm anchors the name at the left margin.
    try:
        left_tab_count = 0
        for i, para in enumerate(roster_paras):
            has_left_tab_at_0 = False
            for ts in para.paragraph_format.tab_stops:
                if ts.alignment == WD_TAB_ALIGNMENT.LEFT and ts.position == 0:
                    has_left_tab_at_0 = True
                    break
            if has_left_tab_at_0:
                left_tab_count += 1
            else:
                actual_ts = [
                    f"align={ts.alignment}, pos={ts.position/914400*2.54:.2f}cm"
                    for ts in para.paragraph_format.tab_stops
                ]
                print(f"FAIL C2: Line {i+1} ('{para.text[:30]}') missing LEFT tab at 0cm. Has: {actual_ts}")

        if left_tab_count == 8:
            print(f"PASS: Component 2 — All 8 roster lines have LEFT tab stop at 0 cm (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Only {left_tab_count}/8 lines have LEFT tab stop at 0 cm")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 8 roster lines use a tab character to separate name and department (0.2 points)
    # The tab character routes the department text to the right-aligned tab stop position.
    try:
        tab_char_count = 0
        for i, para in enumerate(roster_paras):
            if '\t' in para.text:
                tab_char_count += 1
            else:
                print(f"FAIL C3: Line {i+1} ('{para.text[:40]}') has no tab character (uses spaces instead)")

        if tab_char_count == 8:
            print(f"PASS: Component 3 — All 8 roster lines use tab character separator (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Only {tab_char_count}/8 lines use tab character separator")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
