"""
Reward Script: Employee Roster Tab Stop Formatting
Task ID: osworld_writer_tabstop_005
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.5 pts): Center-aligned tab stop at ~10cm added to all 15 employee paragraphs
  - Component 2 (0.5 pts): Tab character inserted after third name word in all 15 employee paragraphs
"""

import os
from docx import Document
from docx.enum.text import WD_TAB_ALIGNMENT
from docx.shared import Cm

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_tabstop_005'

# 10cm in EMU = 3600000; allow small tolerance (+/- 36000, i.e. 1mm)
CENTER_TAB_TARGET_EMU = int(Cm(10))
CENTER_TAB_TOLERANCE_EMU = 36000  # 1mm tolerance


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task requirements:
    1. Each of the 15 employee lines (paragraphs 1-15) has a CENTER tab stop at ~10cm
    2. Each of the 15 employee lines has a tab character inserted after the third name word
       so that the department word is separated by a tab (not a space)
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: must have exactly 16 paragraphs (1 header + 15 employee lines)
    all_paras = doc.paragraphs
    if len(all_paras) < 2:
        print(f"CRITICAL: Document has only {len(all_paras)} paragraph(s), expected 16")
        print("REWARD: 0.0")
        return 0.0

    # Employee lines are paragraphs 1 through 15 (index 1-15), skip header at index 0
    employee_paras = all_paras[1:]
    num_employee_paras = len(employee_paras)
    if num_employee_paras == 0:
        print("CRITICAL: No employee paragraphs found")
        print("REWARD: 0.0")
        return 0.0

    # ------------------------------------------------------------------
    # Component 1: CENTER tab stop at ~10cm present in employee paragraphs (0.5 pts)
    # Each employee paragraph should have exactly one CENTER tab stop at ~10cm
    # This FAILS on initial (no tab stops) and PASSES on golden (CENTER@10cm)
    # ------------------------------------------------------------------
    try:
        paras_with_center_tab = 0
        paras_with_wrong_tab = 0
        for para in employee_paras:
            tab_stops = list(para.paragraph_format.tab_stops)
            # Filter out default LEFT@0 and CLEAR stops (bitter lesson #7)
            meaningful_tabs = [
                ts for ts in tab_stops
                if not (ts.alignment == WD_TAB_ALIGNMENT.CLEAR)
                and not (ts.alignment == WD_TAB_ALIGNMENT.LEFT and ts.position == 0)
            ]
            # Check if at least one CENTER tab stop is within tolerance of 10cm
            has_center_at_10cm = any(
                ts.alignment == WD_TAB_ALIGNMENT.CENTER
                and abs(ts.position - CENTER_TAB_TARGET_EMU) <= CENTER_TAB_TOLERANCE_EMU
                for ts in meaningful_tabs
            )
            if has_center_at_10cm:
                paras_with_center_tab += 1
            else:
                paras_with_wrong_tab += 1

        if paras_with_center_tab == num_employee_paras:
            print(f"PASS: Component 1 — All {num_employee_paras} employee paragraphs have CENTER tab stop at ~10cm (0.5 pts)")
            total_score += 0.5
        elif paras_with_center_tab > 0:
            partial = round(0.5 * paras_with_center_tab / num_employee_paras, 4)
            print(f"PARTIAL: Component 1 — {paras_with_center_tab}/{num_employee_paras} paragraphs have CENTER tab stop at ~10cm ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No employee paragraphs have a CENTER tab stop near 10cm (found {paras_with_center_tab}/{num_employee_paras})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ------------------------------------------------------------------
    # Component 2: Tab character inserted after third name word (0.5 pts)
    # Each employee paragraph text should contain '\t' separating the name from department
    # This FAILS on initial (no tabs, all spaces) and PASSES on golden (tab before dept)
    # ------------------------------------------------------------------
    try:
        paras_with_tab_char = 0
        paras_tab_correct_position = 0
        for para in employee_paras:
            text = para.text
            if '\t' not in text:
                # No tab character at all — skip
                continue
            paras_with_tab_char += 1

            # Verify tab is placed correctly: after the 3rd word (name part)
            # Text should be: "Word1 Word2 Word3\tDepartment"
            tab_idx = text.index('\t')
            before_tab = text[:tab_idx].strip()
            after_tab = text[tab_idx + 1:].strip()

            # Before tab should be 3 words (the name); after tab should be 1+ words (department)
            words_before = before_tab.split()
            words_after = after_tab.split()
            if len(words_before) == 3 and len(words_after) >= 1:
                paras_tab_correct_position += 1

        if paras_with_tab_char == num_employee_paras and paras_tab_correct_position == num_employee_paras:
            print(f"PASS: Component 2 — All {num_employee_paras} employee paragraphs have tab character after 3rd name word (0.5 pts)")
            total_score += 0.5
        elif paras_with_tab_char > 0:
            # Give partial credit: average of two sub-checks
            partial_presence = paras_with_tab_char / num_employee_paras
            partial_position = paras_tab_correct_position / num_employee_paras
            partial = round(0.5 * (partial_presence + partial_position) / 2, 4)
            print(f"PARTIAL: Component 2 — {paras_with_tab_char}/{num_employee_paras} have tab char, "
                  f"{paras_tab_correct_position}/{num_employee_paras} correctly positioned after 3rd word ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No employee paragraphs contain a tab character (found {paras_with_tab_char}/{num_employee_paras})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in the VM environment
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
