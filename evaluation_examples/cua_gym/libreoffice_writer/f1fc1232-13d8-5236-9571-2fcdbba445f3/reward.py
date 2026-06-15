"""
Reward Script: Delete the entire last line of the document which contains a stray test note.
Task ID: writer_edit_067
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5 pts): Test note paragraph is absent from document
  Component 2 (0.3 pts): Last paragraph is the correct closing sentence
  Component 3 (0.2 pts): Document has exactly 43 paragraphs (1 removed from original 44)
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_edit_067'

# The test note text to be removed
TEST_NOTE_TEXT = 'DELETE THIS - test note by editor, do not include in final version'
# The expected closing sentence after removal
EXPECTED_LAST_LINE = 'We look forward to your continued partnership and support.'
# Expected total paragraph count in golden state
EXPECTED_PARA_COUNT = 43


def verify_task(file_path):
    """
    Verify that the stray test note was removed from the document.
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

    # Component 1: Test note paragraph is absent (0.5 points)
    # This FAILS on initial_env (note is present) and PASSES on golden_env (note removed)
    try:
        note_found = False
        for para in paragraphs:
            if TEST_NOTE_TEXT.lower() in para.text.lower():
                note_found = True
                print(f"FAIL: Component 1 — test note paragraph still found: {repr(para.text[:80])}")
                break
        if not note_found:
            print(f"PASS: Component 1 — test note paragraph is absent (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — expected test note to be removed")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Last paragraph is the correct closing sentence (0.3 points)
    # This FAILS on initial_env (last para is the test note) and PASSES on golden_env
    try:
        last_para_text = paragraphs[-1].text.strip() if paragraphs else ""
        if last_para_text == EXPECTED_LAST_LINE:
            print(f"PASS: Component 2 — last paragraph is the correct closing sentence (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — expected last paragraph: {repr(EXPECTED_LAST_LINE)}, found: {repr(last_para_text[:80])}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Document has exactly 43 paragraphs (1 removed from original 44) (0.2 points)
    # This FAILS on initial_env (44 paragraphs) and PASSES on golden_env (43 paragraphs)
    try:
        actual_count = len(paragraphs)
        if actual_count == EXPECTED_PARA_COUNT:
            print(f"PASS: Component 3 — document has exactly {EXPECTED_PARA_COUNT} paragraphs (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — expected {EXPECTED_PARA_COUNT} paragraphs, found {actual_count}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path on the VM
file_path = f'{WORKDIR}/Desktop/final_draft.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
