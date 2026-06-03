"""
Reward Script: Set up tabstops in a play script document
Task ID: osworld_writer_tabstop_006
Domain: libreoffice_writer
Scoring:
  Component 1: Right-aligned tab stop at ~12cm set in all 20 paragraphs (0.5 pts)
  Component 2: Tab character inserted after 2nd word (character name) in all 20 paragraphs (0.3 pts)
  Component 3: Left-aligned tab stop at 0cm set in all 20 paragraphs (0.2 pts)
  Total: 1.0
"""

import os
from docx import Document
from docx.enum.text import WD_TAB_ALIGNMENT

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_tabstop_006'

# Tolerance for position comparison: ±5000 EMU (~0.013cm)
POSITION_TOLERANCE = 5000
# 12cm in EMU (exact: 4320000, golden uses 4319905)
TARGET_RIGHT_POS_EMU = 4320000


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Set left-aligned tabstop at 0cm and right-aligned tabstop at 12cm
    for each of 20 dialogue lines. Insert a tab character after the two-word
    character name in each line so character names are left-aligned and spoken
    text is right-aligned at 12cm.
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = [p for p in doc.paragraphs]
    num_paras = len(paragraphs)

    # Precondition gate: document must have exactly 20 paragraphs
    if num_paras == 0:
        print(f"CRITICAL: Document has no paragraphs")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Document has {num_paras} paragraphs")

    # Component 1: Right-aligned tab stop at ~12cm in all paragraphs (0.5 points)
    # This is the primary formatting task: right-align dialogue text at 12cm
    try:
        paras_with_right_tabstop = 0
        paras_without_right_tabstop = []
        for i, para in enumerate(paragraphs):
            ts_list = list(para.paragraph_format.tab_stops)
            has_right_12cm = any(
                t.alignment == WD_TAB_ALIGNMENT.RIGHT
                and abs(t.position - TARGET_RIGHT_POS_EMU) <= POSITION_TOLERANCE
                for t in ts_list
            )
            if has_right_12cm:
                paras_with_right_tabstop += 1
            else:
                paras_without_right_tabstop.append(i)

        if paras_with_right_tabstop == num_paras:
            print(f"PASS: Component 1 — RIGHT tab stop at ~12cm present in all {num_paras} paragraphs (0.5 pts)")
            total_score += 0.5
        elif paras_with_right_tabstop > 0:
            partial = round(0.5 * paras_with_right_tabstop / num_paras, 4)
            print(f"PARTIAL: Component 1 — RIGHT tab stop at ~12cm in {paras_with_right_tabstop}/{num_paras} paragraphs ({partial} pts)")
            print(f"  Missing in paragraphs: {paras_without_right_tabstop[:5]}{'...' if len(paras_without_right_tabstop) > 5 else ''}")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No paragraphs have RIGHT tab stop at ~12cm (expected {num_paras})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Tab character inserted after 2nd word (character name separator) (0.3 points)
    # Each line should split as: "WORD1 WORD2\tDialogue text..."
    try:
        paras_with_tab_char = 0
        paras_without_tab_char = []
        for i, para in enumerate(paragraphs):
            text = para.text
            # Check that a tab character exists and appears after the 2nd word
            # The format should be: "WORD1 WORD2\trest of dialogue"
            if '\t' in text:
                before_tab = text.split('\t')[0].strip()
                words_before = before_tab.split()
                if len(words_before) == 2:
                    paras_with_tab_char += 1
                else:
                    paras_without_tab_char.append((i, f"tab found but {len(words_before)} words before it: {repr(before_tab[:40])}"))
            else:
                paras_without_tab_char.append((i, f"no tab char found in: {repr(text[:40])}"))

        if paras_with_tab_char == num_paras:
            print(f"PASS: Component 2 — Tab character after 2nd word in all {num_paras} paragraphs (0.3 pts)")
            total_score += 0.3
        elif paras_with_tab_char > 0:
            partial = round(0.3 * paras_with_tab_char / num_paras, 4)
            print(f"PARTIAL: Component 2 — Tab character correctly placed in {paras_with_tab_char}/{num_paras} paragraphs ({partial} pts)")
            for idx, reason in paras_without_tab_char[:3]:
                print(f"  Para {idx}: {reason}")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No paragraphs have tab character after 2nd word (expected {num_paras})")
            if paras_without_tab_char:
                for idx, reason in paras_without_tab_char[:3]:
                    print(f"  Para {idx}: {reason}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Left-aligned tab stop at position 0 in all paragraphs (0.2 points)
    # Ground truth specifies left-aligned tabstop at 0cm
    try:
        paras_with_left0_tabstop = 0
        paras_without_left0_tabstop = []
        for i, para in enumerate(paragraphs):
            ts_list = list(para.paragraph_format.tab_stops)
            has_left_0 = any(
                t.alignment == WD_TAB_ALIGNMENT.LEFT
                and abs(t.position) <= POSITION_TOLERANCE
                for t in ts_list
            )
            if has_left_0:
                paras_with_left0_tabstop += 1
            else:
                paras_without_left0_tabstop.append(i)

        if paras_with_left0_tabstop == num_paras:
            print(f"PASS: Component 3 — LEFT tab stop at 0cm present in all {num_paras} paragraphs (0.2 pts)")
            total_score += 0.2
        elif paras_with_left0_tabstop > 0:
            partial = round(0.2 * paras_with_left0_tabstop / num_paras, 4)
            print(f"PARTIAL: Component 3 — LEFT tab stop at 0cm in {paras_with_left0_tabstop}/{num_paras} paragraphs ({partial} pts)")
            print(f"  Missing in paragraphs: {paras_without_left0_tabstop[:5]}{'...' if len(paras_without_left0_tabstop) > 5 else ''}")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No paragraphs have LEFT tab stop at 0cm (expected {num_paras})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/play_script_draft.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
