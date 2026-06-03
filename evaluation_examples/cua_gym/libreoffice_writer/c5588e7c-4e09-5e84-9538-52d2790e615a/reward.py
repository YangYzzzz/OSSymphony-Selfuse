"""
Reward Script: Run the existing macro 'CleanupFormatting' from the document's macro library.
Task ID: writer_tm_066
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): No multiple consecutive spaces in any paragraph
  Component 2 (0.3): No trailing whitespace in any paragraph
  Component 3 (0.3): Document structure preserved and content cleaned (same paragraphs, same styles, text integrity)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_tm_066'


def verify_task(file_path):
    """
    Verify that the CleanupFormatting macro was executed.
    The macro should:
      - Remove multiple consecutive spaces (replace with single space)
      - Remove trailing whitespace from all paragraphs
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs
    if len(paragraphs) == 0:
        print("FAIL: Document has no paragraphs")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: No multiple consecutive spaces in any paragraph (0.4 points)
    # The initial document has "  " (double+ spaces) in ALL 20 paragraphs.
    # After cleanup, none should have them.
    try:
        paras_with_multi_spaces = 0
        for p in paragraphs:
            if '  ' in p.text:
                paras_with_multi_spaces += 1

        if paras_with_multi_spaces == 0:
            print(f"PASS: Component 1 — No paragraphs contain multiple consecutive spaces (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — {paras_with_multi_spaces}/{len(paragraphs)} paragraphs still contain multiple consecutive spaces")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: No trailing whitespace in any paragraph (0.3 points)
    # The initial document has trailing whitespace in ALL 20 paragraphs.
    # After cleanup, none should have them.
    try:
        paras_with_trailing_ws = 0
        for p in paragraphs:
            text = p.text
            if text and text != text.rstrip():
                paras_with_trailing_ws += 1

        if paras_with_trailing_ws == 0:
            print(f"PASS: Component 2 — No paragraphs contain trailing whitespace (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — {paras_with_trailing_ws}/{len(paragraphs)} paragraphs still have trailing whitespace")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Document structure preserved and content cleaned (0.3 points)
    # The macro should only clean whitespace, not alter structure or meaningful content.
    # Check: same number of paragraphs (20), same styles, and text after normalization matches expected.
    try:
        expected_styles = [
            'Heading 1', 'Normal', 'Normal',
            'List Bullet', 'List Bullet', 'List Bullet', 'List Bullet', 'List Bullet',
            'Heading 2', 'Normal', 'Normal',
            'Heading 2', 'Normal',
            'Heading 2', 'Normal',
            'List Number', 'List Number', 'List Number', 'List Number',
            'Normal'
        ]

        failures = []

        # Check paragraph count
        if len(paragraphs) != 20:
            failures.append(f"Expected 20 paragraphs, found {len(paragraphs)}")

        # Check styles match
        if not failures:
            style_mismatches = 0
            for i, p in enumerate(paragraphs):
                if i < len(expected_styles) and p.style.name != expected_styles[i]:
                    style_mismatches += 1
            if style_mismatches > 0:
                failures.append(f"{style_mismatches} paragraph style mismatches")

        # Check key content is preserved (spot-check a few distinctive values)
        if not failures:
            all_text = ' '.join(p.text for p in paragraphs)
            key_phrases = ['$4.2 million', '94.7%', 'Sarah Chen', 'David Park', 'November 15th']
            missing = [phrase for phrase in key_phrases if phrase not in all_text]
            if missing:
                failures.append(f"Key content missing after cleanup: {missing}")

        # Also verify that multi-space cleanup didn't just delete content
        # The first heading should be exactly "Quarterly Sales Report" (no extra spaces)
        if not failures:
            heading = paragraphs[0].text.strip()
            normalized = re.sub(r'\s+', ' ', heading)
            if normalized != 'Quarterly Sales Report':
                failures.append(f"First heading is '{normalized}', expected 'Quarterly Sales Report'")

        if not failures:
            print(f"PASS: Component 3 — Document structure preserved, 20 paragraphs with correct styles and content (0.3 pts)")
            total_score += 0.3
        else:
            for f in failures:
                print(f"FAIL: Component 3 — {f}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice state before verification
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
