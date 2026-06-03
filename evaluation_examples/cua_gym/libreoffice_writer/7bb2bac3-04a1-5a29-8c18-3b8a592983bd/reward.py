"""
Reward Script: Insert 'TODO: Add citation here' after 'according to recent studies.' sentence
Task ID: writer_edit_043
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): 'TODO: Add citation here' text is present in the target paragraph
  Component 2 (0.3): The inserted text is in the same paragraph as the original sentence (not a new para)
  Component 3 (0.2): Full paragraph text exactly matches the expected string (correct placement)
"""

import os
from docx import Document

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_edit_043'
FILE_PATH = f'{WORKDIR}/literature_review.docx'

# Expected text values from task_config context
ORIGINAL_SENTENCE = 'The prevalence of remote work has increased by 300% since 2020, according to recent studies.'
INSERTED_TEXT = 'TODO: Add citation here'
EXPECTED_FULL_TEXT = 'The prevalence of remote work has increased by 300% since 2020, according to recent studies. TODO: Add citation here'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must be loadable
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the target paragraph containing the original sentence or the modified version
    target_para = None
    target_para_idx = None
    for i, para in enumerate(doc.paragraphs):
        if ORIGINAL_SENTENCE in para.text or INSERTED_TEXT in para.text:
            target_para = para
            target_para_idx = i
            break

    if target_para is None:
        print(f"FAIL: Could not find paragraph containing '{ORIGINAL_SENTENCE[:50]}...' in document")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    print(f"INFO: Found target paragraph at index {target_para_idx}: '{target_para.text[:100]}...'")

    # Component 1: 'TODO: Add citation here' is present in the target paragraph (0.5 points)
    # This FAILS on initial (no TODO text) and PASSES on golden (TODO text present)
    try:
        if INSERTED_TEXT in target_para.text:
            print(f"PASS: Component 1 — 'TODO: Add citation here' text found in target paragraph (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Expected 'TODO: Add citation here' not found in paragraph. "
                  f"Actual text: '{target_para.text[:150]}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The TODO text is in the SAME paragraph as the original sentence (0.3 points)
    # Ensures the insert was inline, not a new paragraph
    # This FAILS on initial (TODO not present anywhere as a paragraph) and PASSES on golden
    try:
        # Check: the paragraph must contain BOTH the original sentence AND the TODO text
        has_original = ORIGINAL_SENTENCE in target_para.text
        has_todo = INSERTED_TEXT in target_para.text
        if has_original and has_todo:
            print(f"PASS: Component 2 — Both original sentence and 'TODO: Add citation here' are in the same paragraph (0.3 pts)")
            total_score += 0.3
        elif not has_original:
            print(f"FAIL: Component 2 — Original sentence not found in target paragraph. Text: '{target_para.text[:150]}'")
        else:
            print(f"FAIL: Component 2 — 'TODO: Add citation here' not in same paragraph as original sentence")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Exact paragraph text matches the expected full string (0.2 points)
    # Verifies correct placement: space after period, exact wording
    # This FAILS on initial (missing TODO) and PASSES on golden (exact match)
    try:
        actual_text = target_para.text.strip()
        if actual_text == EXPECTED_FULL_TEXT:
            print(f"PASS: Component 3 — Paragraph text exactly matches expected output (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Paragraph text does not exactly match expected.")
            print(f"  Expected: '{EXPECTED_FULL_TEXT}'")
            print(f"  Actual  : '{actual_text}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path on VM
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
