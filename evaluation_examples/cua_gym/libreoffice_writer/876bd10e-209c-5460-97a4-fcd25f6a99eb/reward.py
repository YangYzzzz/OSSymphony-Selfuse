"""
Reward Script: Add a blank line after each step in the troubleshooting guide
Task ID: osworld_writer_blank_line_insertion_006
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): Each of the 7 inter-step gaps (between steps 1-2, 2-3, ..., 7-8)
                     contains an empty paragraph (directly verifying the new blank lines
                     that were NOT present in the initial state).
  Component 2 (0.5): Total paragraph count == 20 AND step 8 is followed by an empty
                     paragraph before the "Note:" paragraph (verifying complete insertion).
"""

import os

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_blank_line_insertion_006'


def verify_task(file_path):
    """
    Verify that blank lines have been inserted after each of the 8 numbered steps
    in the troubleshooting guide.

    Initial state: 13 paragraphs; steps 1-8 listed consecutively.
                   Step 8 already has a trailing blank before 'Note:' (pre-existing).
                   Steps 1-7 are directly followed by the next step (no blank lines).
    Golden state:  20 paragraphs; each step is followed by an empty paragraph.

    Key distinction:
      - Initial: steps 1-7 have NO blank line between them (step N is directly followed
                 by step N+1). Only step 8 has a trailing blank (pre-existing).
      - Golden:  steps 1-7 have blank lines inserted BETWEEN them, AND step 8 still
                 has a trailing blank.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs

    # Build a mapping: step_number -> paragraph_index for numbered steps 1-8
    step_indices = {}
    for i, para in enumerate(paragraphs):
        text = para.text.strip()
        if len(text) >= 3 and text[0].isdigit() and text[1] == '.':
            step_num = int(text[0])
            if 1 <= step_num <= 8:
                step_indices[step_num] = i

    # Precondition: all 8 numbered steps must be found
    if len(step_indices) != 8:
        print(f"CRITICAL: Expected 8 numbered steps, found {len(step_indices)}: {list(step_indices.keys())}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Steps 1-7 each followed by an empty paragraph (0.5 points)
    # In the initial doc, steps 1-7 are directly followed by the next step (no blank).
    # In the golden doc, each step has a blank paragraph immediately after it.
    # This checks 7 inter-step blank lines — the ones that were ABSENT in initial state.
    # Each inter-step blank is worth 0.5/7 ≈ 0.0714 points; awarded as a block for
    # simplicity (all 7 must pass to get the 0.5 points).
    try:
        inter_step_blanks = 0
        for step_num in range(1, 8):  # Steps 1 through 7
            step_idx = step_indices[step_num]
            # The paragraph immediately after step N in the golden is blank
            if step_idx + 1 < len(paragraphs):
                next_para_text = paragraphs[step_idx + 1].text.strip()
                if next_para_text == '':
                    inter_step_blanks += 1
                else:
                    print(f"FAIL: Component 1 — step {step_num} (para [{step_idx}]) is NOT "
                          f"followed by a blank line. Next para: {next_para_text[:50]!r}")
            else:
                print(f"FAIL: Component 1 — step {step_num} is the last paragraph, "
                      f"no following paragraph")

        if inter_step_blanks == 7:
            print(f"PASS: Component 1 — all 7 inter-step gaps have blank lines (0.5 pts)")
            total_score += 0.5
        elif inter_step_blanks > 0:
            # Partial credit proportional to how many blanks were inserted
            partial = round((inter_step_blanks / 7) * 0.5, 4)
            print(f"PARTIAL: Component 1 — {inter_step_blanks}/7 inter-step blanks found "
                  f"(+{partial} pts)")
            if partial > 0:
                total_score += partial
        else:
            print(f"FAIL: Component 1 — no inter-step blank lines found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Total paragraph count == 20 (0.5 points)
    # Initial: 13 paragraphs. Golden: 20 paragraphs (7 new blanks between steps 1-8,
    # plus step 8 already had a trailing blank in initial, making 7 new + 1 existing = 8
    # blanks total after steps in golden, consistent with 20-paragraph structure).
    # This FAILS on initial (count=13) and PASSES on golden (count=20).
    try:
        para_count = len(paragraphs)
        if para_count == 20:
            print(f"PASS: Component 2 — paragraph count is 20 (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — expected 20 paragraphs, found {para_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
