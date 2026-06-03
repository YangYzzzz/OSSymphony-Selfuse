"""
Reward Script: Form layout with tab stops
Task ID: wrpara_029
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): 5 paragraphs with correct field labels (Name, Address, Phone, Email, Date)
  Component 2 (0.4): Tab stops at 2cm (LEFT), 6cm (LEFT), 15cm (RIGHT) on form paragraphs
  Component 3 (0.3): RIGHT tab at 15cm uses underscore/heavy leader character
"""

import os
from docx import Document
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER

WORKDIR = '/home/user'
TASK_ID = 'wrpara_029'

# Expected field labels in the form
EXPECTED_LABELS = ['Name', 'Address', 'Phone', 'Email', 'Date']

# Tab stop positions in EMU (1 cm = 360000 EMU)
# Allow 5% tolerance for position matching
TAB_2CM = 2.0 * 360000   # 720000
TAB_6CM = 6.0 * 360000   # 2160000
TAB_15CM = 15.0 * 360000  # 5400000
POS_TOLERANCE = 0.05  # 5% tolerance


def position_matches(actual_emu, expected_emu, tolerance=POS_TOLERANCE):
    """Check if actual position is within tolerance of expected."""
    if expected_emu == 0:
        return abs(actual_emu) < 36000  # within 1mm
    return abs(actual_emu - expected_emu) / expected_emu <= tolerance


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

    # Get non-empty paragraphs (paragraphs that contain meaningful text)
    form_paras = []
    for para in doc.paragraphs:
        # Strip tabs and whitespace, check for label content
        text_clean = para.text.replace('\t', '').strip()
        if text_clean:
            form_paras.append(para)

    # Component 1: 5 paragraphs with correct field labels (0.3 points)
    try:
        found_labels = []
        for para in form_paras:
            text = para.text.replace('\t', '').strip().rstrip(':').strip()
            for label in EXPECTED_LABELS:
                if label.lower() in text.lower():
                    found_labels.append(label)
                    break

        found_labels_unique = list(set(found_labels))
        label_count = len(found_labels_unique)

        if label_count >= 5:
            print(f"PASS: Component 1 - All 5 field labels found: {found_labels_unique} (0.3 pts)")
            total_score += 0.3
        elif label_count >= 3:
            partial = 0.3 * (label_count / 5)
            print(f"PARTIAL: Component 1 - {label_count}/5 labels found: {found_labels_unique} ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 - Only {label_count}/5 labels found: {found_labels_unique}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Tab stops at 2cm (LEFT), 6cm (LEFT), 15cm (RIGHT) (0.4 points)
    try:
        paras_with_correct_tabs = 0
        for para in form_paras:
            tabs = para.paragraph_format.tab_stops
            # Collect non-default tab stops
            tab_list = []
            for ts in tabs:
                if ts.alignment == WD_TAB_ALIGNMENT.CLEAR:
                    continue
                if ts.alignment == WD_TAB_ALIGNMENT.LEFT and ts.position == 0:
                    continue
                tab_list.append(ts)

            # Check for required tab stops using any() on actual API data
            has_left_2cm = any(
                ts.alignment == WD_TAB_ALIGNMENT.LEFT and position_matches(ts.position, TAB_2CM)
                for ts in tab_list
            )
            has_left_6cm = any(
                ts.alignment == WD_TAB_ALIGNMENT.LEFT and position_matches(ts.position, TAB_6CM)
                for ts in tab_list
            )
            has_right_15cm = any(
                ts.alignment == WD_TAB_ALIGNMENT.RIGHT and position_matches(ts.position, TAB_15CM)
                for ts in tab_list
            )

            if has_left_2cm and has_left_6cm and has_right_15cm:
                paras_with_correct_tabs += 1

        if paras_with_correct_tabs >= 5:
            print(f"PASS: Component 2 - All 5 form paragraphs have correct tab stops (0.4 pts)")
            total_score += 0.4
        elif paras_with_correct_tabs >= 1:
            partial = 0.4 * (min(paras_with_correct_tabs, 5) / 5)
            print(f"PARTIAL: Component 2 - {paras_with_correct_tabs}/5 paragraphs have correct tabs ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - No paragraphs have the required tab stop configuration")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: RIGHT tab at 15cm uses underscore/heavy leader (0.3 points)
    try:
        paras_with_leader = 0
        for para in form_paras:
            tabs = para.paragraph_format.tab_stops
            for ts in tabs:
                if ts.alignment == WD_TAB_ALIGNMENT.CLEAR:
                    continue
                # Check for RIGHT tab at 15cm with underscore-like leader
                # Accept HEAVY (4) or LINES (3) as valid underscore leaders
                if (ts.alignment == WD_TAB_ALIGNMENT.RIGHT
                        and position_matches(ts.position, TAB_15CM)
                        and ts.leader in (WD_TAB_LEADER.HEAVY, WD_TAB_LEADER.LINES)):
                    paras_with_leader += 1
                    break

        if paras_with_leader >= 5:
            print(f"PASS: Component 3 - All 5 form paragraphs have underscore leader on right tab (0.3 pts)")
            total_score += 0.3
        elif paras_with_leader >= 1:
            partial = 0.3 * (min(paras_with_leader, 5) / 5)
            print(f"PARTIAL: Component 3 - {paras_with_leader}/5 paragraphs have underscore leader ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 - No paragraphs have underscore leader on the right tab stop")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
