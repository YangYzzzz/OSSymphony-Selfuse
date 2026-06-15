"""
Reward Script: Insert non-breaking space between Dr. and Williams
Task ID: writer_txtfmt_028
Domain: libreoffice_writer
Scoring:
  Component 1 (0.6): Non-breaking space (U+00A0) present between 'Dr.' and 'Williams'
                      in the first paragraph — fails on initial, passes on golden
  Component 2 (0.4): Regular space (U+0020) NOT present between 'Dr.' and 'Williams',
                      confirming the replacement was made, not just an addition
"""

import os
from docx import Document

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_txtfmt_028'
FILE_PATH = f'{WORKDIR}/medical_report.docx'

NBSP = '\u00a0'  # Non-breaking space, U+00A0
REGULAR_SPACE = ' '  # U+0020


def verify_task(file_path):
    """
    Verify that the regular space between 'Dr.' and 'Williams' in the first paragraph
    has been replaced with a non-breaking space (Unicode U+00A0).

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: load the file
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: confirm first paragraph exists and contains expected text context
    try:
        first_para = doc.paragraphs[0]
        para_text = first_para.text
        if 'Dr.' not in para_text or 'Williams' not in para_text:
            print(f"CRITICAL: First paragraph does not contain expected 'Dr. Williams' context.")
            print(f"  First paragraph text (first 120 chars): {repr(para_text[:120])}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot read first paragraph: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Non-breaking space (U+00A0) present between 'Dr.' and 'Williams' (0.6 points)
    # This FAILS on initial_env (has regular space), PASSES on golden_env (has non-breaking space)
    try:
        # Find the position of 'Dr.' in the first paragraph text
        idx = para_text.find('Dr.')
        if idx == -1:
            print("FAIL: Component 1 — 'Dr.' not found in first paragraph")
        else:
            # The character immediately after 'Dr.' should be a non-breaking space
            char_after_dr = para_text[idx + 3] if idx + 3 < len(para_text) else ''
            if char_after_dr == NBSP:
                print(f"PASS: Component 1 — Non-breaking space (U+00A0) found after 'Dr.' (ord={ord(char_after_dr)}) (0.6 pts)")
                total_score += 0.6
            else:
                print(f"FAIL: Component 1 — Expected non-breaking space (U+00A0) after 'Dr.', found: {repr(char_after_dr)} (ord={ord(char_after_dr) if char_after_dr else 'N/A'})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Regular space NOT present between 'Dr.' and 'Williams' (0.4 points)
    # Confirms the replacement was done (not just an insertion alongside the old space).
    # This FAILS on initial_env (has regular space "Dr. Williams"), PASSES on golden_env.
    try:
        # Check that 'Dr. Williams' with a regular space does NOT appear in the first paragraph
        regular_space_pattern = 'Dr.' + REGULAR_SPACE + 'Williams'
        nbsp_pattern = 'Dr.' + NBSP + 'Williams'

        if regular_space_pattern in para_text:
            print(f"FAIL: Component 2 — Regular space still present: 'Dr. Williams' (U+0020) found in first paragraph")
        elif nbsp_pattern in para_text:
            print(f"PASS: Component 2 — Regular space removed; 'Dr.\\u00a0Williams' (non-breaking space) confirmed in first paragraph (0.4 pts)")
            total_score += 0.4
        else:
            # Possible edge case: other content between Dr. and Williams
            print(f"FAIL: Component 2 — Neither regular nor NBSP pattern of 'Dr. Williams' found. Paragraph text: {repr(para_text[:120])}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path on the VM
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
