"""
Reward Script: Add new paragraph at end of document
Task ID: writer_edit_051
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6): Last paragraph has exact text 'Document last updated: March 4, 2025'
  Component 2 (0.2): Previous last paragraph ('For questions...') is now second-to-last (content preserved)
  Component 3 (0.2): New paragraph uses Normal (default) paragraph style
Total: 1.0
"""

import os

from docx import Document

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_edit_051'

TARGET_TEXT = 'Document last updated: March 4, 2025'
PREV_LAST_TEXT = 'For questions regarding these policies, please contact the Human Resources department.'


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
    if len(paragraphs) == 0:
        print("CRITICAL: Document has no paragraphs")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Last paragraph has exact target text (0.6 points)
    # This FAILS on initial (last para is the HR paragraph), PASSES on golden
    try:
        last_para = paragraphs[-1]
        last_text = last_para.text.strip()
        if last_text == TARGET_TEXT:
            print(f"PASS: Component 1 — Last paragraph is '{TARGET_TEXT}' (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — Expected last paragraph '{TARGET_TEXT}', found '{last_text}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Previous content preserved — HR paragraph is now second-to-last (0.2 points)
    # This FAILS on initial (the HR paragraph IS the last, no 'Document last updated' after it)
    try:
        if len(paragraphs) >= 2:
            second_last_para = paragraphs[-2]
            second_last_text = second_last_para.text.strip()
            if second_last_text == PREV_LAST_TEXT:
                print(f"PASS: Component 2 — Previous last paragraph is intact as second-to-last (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — Expected second-to-last paragraph to be HR text, found '{second_last_text}'")
        else:
            print("FAIL: Component 2 — Not enough paragraphs to check second-to-last")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: New last paragraph uses Normal (default) paragraph style (0.2 points)
    # This FAILS on initial (no 'Document last updated' paragraph exists),
    # PASSES on golden only if Component 1 passed AND the style is Normal
    try:
        last_para = paragraphs[-1]
        last_text = last_para.text.strip()
        if last_text == TARGET_TEXT:
            style_name = last_para.style.name if last_para.style else None
            # Accept 'Normal', 'Default', or 'Body Text' as default paragraph style
            if style_name and ('Normal' in style_name or 'Default' in style_name or 'Body Text' in style_name):
                print(f"PASS: Component 3 — New paragraph uses default style '{style_name}' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Expected Normal/Default style, found '{style_name}'")
        else:
            print(f"FAIL: Component 3 — Cannot check style, last paragraph is not the target text")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in the env
file_path = f'{WORKDIR}/policy_manual.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
