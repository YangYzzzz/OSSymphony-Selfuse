"""
Reward Script: Cut the last paragraph and paste it as the first paragraph
Task ID: writer_edit_021
Domain: libreoffice_writer
Scoring:
  Precondition gate: Document has exactly 4 non-empty paragraphs (no points, just a gate)
  Component 1 (0.5 pts): The conclusion paragraph is the FIRST paragraph
  Component 2 (0.5 pts): Original paragraphs 1, 2, 3 follow at positions 2, 3, 4 in correct order
"""

import os
from docx import Document

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_edit_021'

# Known paragraph starting text (used for matching)
CONCLUSION_START = 'In conclusion, sustainable development requires'
ORIG_PARA1_START = 'Sustainable development has emerged as one of the most pressing global priorities'
ORIG_PARA2_START = 'Environmental challenges such as climate change, biodiversity loss'
ORIG_PARA3_START = 'Social equity is equally central to the concept of sustainability'


def get_non_empty_paragraphs(doc):
    """Return list of non-empty paragraph texts (stripped)."""
    return [p.text.strip() for p in doc.paragraphs if p.text.strip()]


def verify_task(file_path):
    """
    Verify that the last paragraph has been moved to the first position.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paras = get_non_empty_paragraphs(doc)
    print(f"INFO: Found {len(paras)} non-empty paragraphs")
    for i, t in enumerate(paras):
        print(f"  Para {i+1}: {t[:80]}...")

    # Precondition gate: Document must have exactly 4 paragraphs
    # (This is true in both initial and golden, so it awards no points — just a gate)
    if len(paras) != 4:
        print(f"GATE FAIL: Expected 4 non-empty paragraphs, found {len(paras)}. "
              f"Text may have been duplicated or lost.")
        print(f"\nScore: 0.0/1.0")
        print(f"REWARD: 0.0")
        return 0.0

    # Component 1: The conclusion paragraph is the FIRST paragraph (0.5 points)
    # In initial_env, the conclusion is at position 4 (last) — this FAILS
    # In golden_env, the conclusion is at position 1 (first) — this PASSES
    try:
        first_para = paras[0]
        if first_para.startswith(CONCLUSION_START):
            print(f"PASS: Component 1 — Conclusion paragraph is first (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — First paragraph should be conclusion. "
                  f"Found: '{first_para[:80]}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Original paragraphs 1, 2, 3 follow at positions 2, 3, 4 in correct order (0.5 points)
    # In initial_env, position 2 = original para 2 (not para 1) — this FAILS
    # In golden_env, positions 2,3,4 = original paras 1,2,3 — this PASSES
    try:
        para2 = paras[1]
        para3 = paras[2]
        para4 = paras[3]

        p2_ok = para2.startswith(ORIG_PARA1_START)
        p3_ok = para3.startswith(ORIG_PARA2_START)
        p4_ok = para4.startswith(ORIG_PARA3_START)

        if p2_ok and p3_ok and p4_ok:
            print(f"PASS: Component 2 — Original 3 paragraphs follow at positions 2-4 in correct order (0.5 pts)")
            total_score += 0.5
        else:
            if not p2_ok:
                print(f"FAIL: Component 2 — Position 2 wrong. "
                      f"Expected start: '{ORIG_PARA1_START[:60]}', "
                      f"found: '{para2[:60]}'")
            if not p3_ok:
                print(f"FAIL: Component 2 — Position 3 wrong. "
                      f"Expected start: '{ORIG_PARA2_START[:60]}', "
                      f"found: '{para3[:60]}'")
            if not p4_ok:
                print(f"FAIL: Component 2 — Position 4 wrong. "
                      f"Expected start: '{ORIG_PARA3_START[:60]}', "
                      f"found: '{para4[:60]}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


file_path = f'{WORKDIR}/essay_draft.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
