"""
Reward Script: Use Find & Replace with regex to add a period at end of every line
               that doesn't already end with punctuation.
Task ID: writer_edit_028
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6): All 6 lines originally missing periods now end with a period
                     (0.1 per line; FAILS on initial_env, PASSES on golden_env)
  Component 2 (0.4): Each of the 6 fixed lines has EXACTLY the expected text (original + '.')
                     — confirms no corruption, no double-period, no extra whitespace
                     (0.0667 per line; FAILS on initial_env, PASSES on golden_env)
"""

import os
from docx import Document

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_edit_028'

# Ground truth from task_config.json context:
# Lines originally WITHOUT periods — their EXPECTED final text after task completion:
LINES_EXPECTED_AFTER_FIX = {
    1: 'Submit expense reports.',
    3: 'Update project timeline.',
    4: 'Review vendor contracts.',
    6: 'Order office supplies.',
    8: 'Organize training session.',
    9: 'Send client invoices.',
}

# Lines originally WITH periods (used as precondition gate, not scored):
LINES_ORIGINALLY_WITH_PERIOD = {
    0: 'Complete the budget review.',
    2: 'Schedule team meeting.',
    5: 'Prepare presentation slides.',
    7: 'File quarterly taxes.',
}


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

    paragraphs = doc.paragraphs
    print(f"Document has {len(paragraphs)} paragraphs")

    # Gate: document must have at least 10 paragraphs
    if len(paragraphs) < 10:
        print(f"FAIL: Expected at least 10 paragraphs, found {len(paragraphs)}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: check that originally-period lines are intact (no corruption)
    # These are non-scored; if corrupted, document integrity is broken.
    for idx, expected_text in LINES_ORIGINALLY_WITH_PERIOD.items():
        actual_text = paragraphs[idx].text
        if actual_text != expected_text:
            print(f"PRECONDITION FAIL: Line {idx} was unexpectedly changed: {repr(actual_text)}")
            print("REWARD: 0.0")
            return 0.0
    print("PRECONDITION OK: All pre-existing period lines are intact")

    # Component 1: Each of the 6 lines originally missing periods now ends with a period (0.1 each = 0.6 total)
    # This FAILS on initial_env (no period added) and PASSES on golden_env (period added).
    try:
        for idx, expected_final in LINES_EXPECTED_AFTER_FIX.items():
            actual_text = paragraphs[idx].text
            if actual_text.endswith('.'):
                print(f"PASS C1: Line {idx} ends with period: {repr(actual_text)}")
                total_score += 0.1
            else:
                print(f"FAIL C1: Line {idx} missing period: {repr(actual_text)}")
    except Exception as e:
        print(f"ERROR: Component 1 check failed: {e}")

    # Component 2: Each of the 6 fixed lines has EXACTLY the expected text (original + '.')
    # This FAILS on initial_env (text is still missing period) and PASSES on golden_env (exact match).
    # Confirms no corruption, no double-period, no extra whitespace on the modified lines.
    try:
        per_line_score = round(0.4 / 6, 6)  # ~0.066667 per line
        for idx, expected_final in LINES_EXPECTED_AFTER_FIX.items():
            actual_text = paragraphs[idx].text
            if actual_text == expected_final:
                print(f"PASS C2: Line {idx} exact match: {repr(actual_text)}")
                total_score += per_line_score
            else:
                print(f"FAIL C2: Line {idx} not exact: got {repr(actual_text)}, expected {repr(expected_final)}")
    except Exception as e:
        print(f"ERROR: Component 2 check failed: {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/task_list.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
