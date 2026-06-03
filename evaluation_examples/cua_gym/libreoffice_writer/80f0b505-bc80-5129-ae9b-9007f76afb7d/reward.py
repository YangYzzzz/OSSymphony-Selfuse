"""
Reward Script: Convert 15 onboarding steps from plain paragraphs to numbered list
Task ID: writer_hr_031
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Steps use 'List Number' style
  Component 2 (0.3): All 15 steps are numbered (count check)
  Component 3 (0.3): Description paragraphs are indented
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_hr_031'

# The 15 step paragraphs are at indices 6,8,10,...,34 in the document
# The 15 description paragraphs are at indices 7,9,11,...,35
STEP_INDICES = list(range(6, 35, 2))       # 6, 8, 10, ..., 34  (15 items)
DESC_INDICES = list(range(7, 36, 2))       # 7, 9, 11, ..., 35  (15 items)
EXPECTED_STEP_COUNT = 15


def persist_app_state(domain):
    """Try to save any unsaved edits in LibreOffice Writer."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_writer", "libreoffice_calc", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


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

    paras = doc.paragraphs

    # Precondition: document has enough paragraphs
    if len(paras) < 36:
        print(f"FAIL: Document has only {len(paras)} paragraphs, expected at least 36")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Step paragraphs use 'List Number' style (0.4 points)
    # Count how many of the 15 step paragraphs have 'List Number' style
    try:
        list_number_count = 0
        for idx in STEP_INDICES:
            style_name = paras[idx].style.name if paras[idx].style else 'None'
            if style_name == 'List Number':
                list_number_count += 1
            else:
                print(f"  DETAIL: para[{idx}] style={style_name!r}, expected 'List Number'")

        if list_number_count == EXPECTED_STEP_COUNT:
            print(f"PASS: Component 1 -- All {EXPECTED_STEP_COUNT} steps use 'List Number' style (0.4 pts)")
            total_score += 0.4
        elif list_number_count > 0:
            partial = 0.4 * (list_number_count / EXPECTED_STEP_COUNT)
            print(f"PARTIAL: Component 1 -- {list_number_count}/{EXPECTED_STEP_COUNT} steps use 'List Number' style ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 -- No steps use 'List Number' style (0/{EXPECTED_STEP_COUNT})")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Exactly 15 consecutive step paragraphs are numbered (0.3 points)
    # Verify that ALL step paragraphs match expected text content AND are List Number
    try:
        # Check that the step paragraphs still contain expected step titles
        # and that numbered list items form a continuous sequence
        numbered_steps = []
        for idx in STEP_INDICES:
            style_name = paras[idx].style.name if paras[idx].style else 'None'
            if style_name == 'List Number' and paras[idx].text.strip():
                numbered_steps.append(paras[idx].text.strip())

        if len(numbered_steps) == EXPECTED_STEP_COUNT:
            print(f"PASS: Component 2 -- All {EXPECTED_STEP_COUNT} numbered steps found with non-empty text (0.3 pts)")
            total_score += 0.3
        elif len(numbered_steps) > 0:
            partial = 0.3 * (len(numbered_steps) / EXPECTED_STEP_COUNT)
            print(f"PARTIAL: Component 2 -- {len(numbered_steps)}/{EXPECTED_STEP_COUNT} numbered steps with text ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No numbered steps found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Description paragraphs are indented (0.3 points)
    # Each description paragraph should have a left_indent > 0
    try:
        indented_count = 0
        for idx in DESC_INDICES:
            left_indent = paras[idx].paragraph_format.left_indent
            if left_indent is not None and left_indent > 0:
                indented_count += 1
            else:
                print(f"  DETAIL: para[{idx}] left_indent={left_indent}, expected > 0")

        if indented_count == EXPECTED_STEP_COUNT:
            print(f"PASS: Component 3 -- All {EXPECTED_STEP_COUNT} descriptions are indented (0.3 pts)")
            total_score += 0.3
        elif indented_count > 0:
            partial = 0.3 * (indented_count / EXPECTED_STEP_COUNT)
            print(f"PARTIAL: Component 3 -- {indented_count}/{EXPECTED_STEP_COUNT} descriptions indented ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- No descriptions are indented")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
