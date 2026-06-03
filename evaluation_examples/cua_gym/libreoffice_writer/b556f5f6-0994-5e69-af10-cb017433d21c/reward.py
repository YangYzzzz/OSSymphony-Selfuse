"""
Reward Script: Remove all trailing whitespace at the end of every line using regex Find & Replace
Task ID: writer_edit_015
Domain: libreoffice_writer
Scoring:
  - Component 1: All paragraphs have no trailing whitespace (1.0 pts)
    * Partial credit: score scales linearly with fraction of paragraphs cleaned
    * 0.0 on initial_env (51/76 paragraphs have trailing spaces)
    * 1.0 on golden_env (0/76 paragraphs have trailing spaces)

Content preservation is used as a precondition gate only (not a scoring component).
"""

import os
import re

# python-docx for reading .docx files
from docx import Document

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_edit_015'
FILE_NAME = 'code_documentation.docx'

# Ground truth from task context:
# - Initial: 51 out of 76 paragraphs have trailing whitespace (1-4 spaces)
# - Golden: 0 paragraphs have trailing whitespace
# - Both states: 76 paragraphs total, same content (minus trailing spaces)

EXPECTED_PARAGRAPH_COUNT = 76

# Number of paragraphs with trailing whitespace in the INITIAL state (ground truth)
INITIAL_TRAILING_COUNT = 51


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document — precondition gate
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs
    actual_para_count = len(paragraphs)

    # Precondition gate: verify the paragraph count is as expected
    if abs(actual_para_count - EXPECTED_PARAGRAPH_COUNT) > 3:
        print(f"CRITICAL: Paragraph count {actual_para_count} deviates too much from expected {EXPECTED_PARAGRAPH_COUNT}.")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: verify key content landmarks are present
    # If these are missing, the file is corrupted or wrong
    key_content_samples = [
        (0, 'DataProcessor Module'),
        (3, 'Installation'),
        (11, 'Quick Start'),
    ]
    for idx, expected_substr in key_content_samples:
        if idx < actual_para_count:
            if expected_substr not in paragraphs[idx].text:
                print(f"CRITICAL: Content corrupted at para {idx}: expected '{expected_substr}', "
                      f"found: {repr(paragraphs[idx].text[:60])}")
                print("REWARD: 0.0")
                return 0.0

    # Component 1: Trailing whitespace removal — all paragraphs (1.0 points total)
    # Task: remove ALL trailing whitespace from every paragraph.
    # Scoring:
    #   - 0.0 if no paragraphs have been cleaned (same count as initial)
    #   - Progressive partial credit proportional to fraction of previously-dirty paragraphs cleaned
    #   - 1.0 only when ALL paragraphs have no trailing whitespace
    #
    # On initial_env: 51 paragraphs have trailing spaces → score = 0.0 (nothing cleaned)
    # On golden_env:  0 paragraphs have trailing spaces → score = 1.0 (all cleaned)
    try:
        trailing_paras = []
        for i, para in enumerate(paragraphs):
            text = para.text
            if re.search(r'\s+$', text):
                trailing_paras.append((i, repr(text[-20:])))

        remaining_trailing = len(trailing_paras)

        if remaining_trailing == 0:
            # All trailing whitespace removed: full credit
            print(f"PASS: Component 1 — All paragraphs cleaned: 0 trailing-whitespace paragraphs remain (1.0 pts)")
            total_score += 1.0
        elif remaining_trailing >= INITIAL_TRAILING_COUNT:
            # No improvement from initial state
            print(f"FAIL: Component 1 — No paragraphs cleaned: {remaining_trailing} still have trailing whitespace "
                  f"(same or worse than initial state of {INITIAL_TRAILING_COUNT})")
            for idx, snippet in trailing_paras[:3]:
                print(f"  Para {idx}: ...{snippet}")
        else:
            # Partial cleaning: award partial credit proportional to improvement
            # cleaned = INITIAL_TRAILING_COUNT - remaining_trailing
            # partial_score = cleaned / INITIAL_TRAILING_COUNT * 1.0
            cleaned = INITIAL_TRAILING_COUNT - remaining_trailing
            partial = cleaned / INITIAL_TRAILING_COUNT
            # Round to 2 decimal places for clean output
            partial = round(partial, 2)
            # Cap at 0.9 to ensure full credit only when all are removed
            partial = min(partial, 0.9)
            print(f"PARTIAL: Component 1 — {cleaned}/{INITIAL_TRAILING_COUNT} paragraphs cleaned "
                  f"({remaining_trailing} still have trailing whitespace) ({partial:.2f} pts)")
            for idx, snippet in trailing_paras[:3]:
                print(f"  Para {idx}: ...{snippet}")
            if partial > 0:
                total_score += partial

    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path on the VM
file_path = f'{WORKDIR}/{FILE_NAME}'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
