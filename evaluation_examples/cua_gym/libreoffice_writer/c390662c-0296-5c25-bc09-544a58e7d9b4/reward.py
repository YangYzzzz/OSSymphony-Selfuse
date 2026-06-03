"""
Reward Script: Copy paragraph 2 and paste it after paragraph 4
Task ID: writer_edit_062
Domain: libreoffice_writer
Scoring:
  Component 1: Document has exactly 6 paragraphs (0.4 pts)
  Component 2: Inserted paragraph at index 4 matches paragraph 2 text (0.4 pts)
  Component 3: All original 5 paragraphs are preserved in correct positions (0.2 pts)
"""

import os
from docx import Document

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_edit_062'

# Ground truth values from task context
PARA_2_TEXT = 'Safety is our top priority. All personnel must complete the safety orientation before accessing the facility.'

EXPECTED_ORDER_6 = [
    'Welcome to the training program.',
    'Safety is our top priority. All personnel must complete the safety orientation before accessing the facility.',
    'Training sessions are held every Monday and Wednesday.',
    'Please bring your employee ID badge to all sessions.',
    'Safety is our top priority. All personnel must complete the safety orientation before accessing the facility.',
    'Contact the training coordinator for schedule changes.',
]


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

    paragraphs = [p.text for p in doc.paragraphs]
    print(f"INFO: Found {len(paragraphs)} paragraphs")
    for i, text in enumerate(paragraphs):
        print(f"  [{i}] {text!r}")

    # Component 1: Document has exactly 6 paragraphs (0.4 points)
    # Initial env has 5 paragraphs; after copy-paste it should have 6
    try:
        if len(paragraphs) == 6:
            print(f"PASS: Component 1 — document has 6 paragraphs (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — expected 6 paragraphs, found {len(paragraphs)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Paragraph at index 4 (between original para 4 and para 5) is
    # a copy of paragraph 2 text (0.4 points)
    try:
        if len(paragraphs) >= 5 and paragraphs[4].strip() == PARA_2_TEXT:
            print(f"PASS: Component 2 — inserted duplicate at index 4 matches paragraph 2 text (0.4 pts)")
            total_score += 0.4
        else:
            found = paragraphs[4] if len(paragraphs) >= 5 else '(index out of range)'
            print(f"FAIL: Component 2 — expected para 2 copy at index 4, found: {found!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All original paragraphs are preserved in correct positions (0.2 points)
    # Checks that paragraphs 0-3 and 5 in golden match the expected values
    try:
        if len(paragraphs) == 6:
            matches = all(paragraphs[i].strip() == EXPECTED_ORDER_6[i] for i in range(6))
            if matches:
                print(f"PASS: Component 3 — all 6 paragraphs in correct order including original para 5 preserved at index 5 (0.2 pts)")
                total_score += 0.2
            else:
                mismatches = [(i, paragraphs[i], EXPECTED_ORDER_6[i]) for i in range(6) if paragraphs[i].strip() != EXPECTED_ORDER_6[i]]
                print(f"FAIL: Component 3 — paragraph order/content mismatch: {mismatches}")
        else:
            print(f"FAIL: Component 3 — cannot verify paragraph order with {len(paragraphs)} paragraphs (expected 6)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


file_path = f'{WORKDIR}/training_manual.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
