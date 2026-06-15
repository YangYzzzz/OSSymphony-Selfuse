"""
Reward Script: Fix wrongly styled heading paragraphs and update TOC
Task ID: writer_mt_094
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): 'Note: This data is preliminary' is NOT Heading 2
  Component 2 (0.35): 'Source: Annual Survey 2024' is NOT Heading 2
  Component 3 (0.30): Total Heading 2 count is exactly 8 (was 10 with the 2 erroneous entries)
"""

import os
from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_094'

# The two paragraphs that were erroneously styled as Heading 2
TARGET_PARA_1 = 'Note: This data is preliminary'
TARGET_PARA_2 = 'Source: Annual Survey 2024'

# After fixing, there should be exactly 8 Heading 2 paragraphs (was 10)
EXPECTED_HEADING2_COUNT = 8


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

    # Collect paragraph info: map target texts to their styles, collect Heading 2 entries
    heading2_texts = []
    target_styles = {}  # maps target text -> style name

    for para in doc.paragraphs:
        style_name = para.style.name if para.style else 'None'
        text = para.text.strip()

        if TARGET_PARA_1 in text:
            target_styles[TARGET_PARA_1] = style_name

        if TARGET_PARA_2 in text:
            target_styles[TARGET_PARA_2] = style_name

        if style_name == 'Heading 2':
            heading2_texts.append(text)

    # Precondition: both target paragraphs must still exist in the document
    if TARGET_PARA_1 not in target_styles:
        print(f"CRITICAL: Target paragraph '{TARGET_PARA_1}' not found in document")
        print("REWARD: 0.0")
        return 0.0

    if TARGET_PARA_2 not in target_styles:
        print(f"CRITICAL: Target paragraph '{TARGET_PARA_2}' not found in document")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 'Note: This data is preliminary' is no longer Heading 2 (0.35 points)
    # In initial_env this is Heading 2, in golden_env it should NOT be Heading 2
    try:
        style1 = target_styles[TARGET_PARA_1]
        if style1 != 'Heading 2':
            print(f"PASS: Component 1 — '{TARGET_PARA_1}' style is '{style1}' (not Heading 2) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — '{TARGET_PARA_1}' is still styled as 'Heading 2'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'Source: Annual Survey 2024' is no longer Heading 2 (0.35 points)
    # In initial_env this is Heading 2, in golden_env it should NOT be Heading 2
    try:
        style2 = target_styles[TARGET_PARA_2]
        if style2 != 'Heading 2':
            print(f"PASS: Component 2 — '{TARGET_PARA_2}' style is '{style2}' (not Heading 2) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — '{TARGET_PARA_2}' is still styled as 'Heading 2'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Total Heading 2 count is exactly 8 (0.30 points)
    # In initial_env there are 10 Heading 2 paragraphs; after fixing the 2 erroneous ones, should be 8
    try:
        h2_count = len(heading2_texts)
        if h2_count == EXPECTED_HEADING2_COUNT:
            print(f"PASS: Component 3 — Heading 2 count is {h2_count} (expected {EXPECTED_HEADING2_COUNT}) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — Heading 2 count is {h2_count}, expected {EXPECTED_HEADING2_COUNT}")
            print(f"  Current Heading 2 entries: {heading2_texts}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: persist app state then verify
def persist_app_state(domain):
    """Best-effort save for LibreOffice Writer documents."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
