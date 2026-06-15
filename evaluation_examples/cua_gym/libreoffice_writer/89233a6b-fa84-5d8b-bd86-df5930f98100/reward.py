"""
Reward Script: Highlight 'effective immediately' in yellow
Task ID: writer_hr_021
Domain: libreoffice_writer
Scoring:
  Component 1 (0.33 each x3): Each of the 3 instances of 'effective immediately'
  has yellow character highlighting applied.
  Total: ~1.0 (0.33 + 0.33 + 0.34 = 1.0)
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_hr_021'
TARGET_PHRASE = 'effective immediately'
EXPECTED_COUNT = 3


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that all instances of 'effective immediately' have yellow highlighting.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from docx.enum.text import WD_COLOR_INDEX
    except ImportError as e:
        print(f"CRITICAL: Missing library: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all runs that contain the target phrase and check highlighting
    yellow_highlighted_count = 0
    phrase_run_count = 0

    for para in doc.paragraphs:
        for run in para.runs:
            if TARGET_PHRASE.lower() in run.text.lower():
                phrase_run_count += 1
                hl = run.font.highlight_color
                if hl is not None and hl == WD_COLOR_INDEX.YELLOW:
                    yellow_highlighted_count += 1
                    print(f"PASS: Found yellow-highlighted '{run.text.strip()}' (highlight={hl})")
                else:
                    print(f"FAIL: Run '{run.text.strip()}' has highlight={hl}, expected YELLOW")

    print(f"\nPhrase runs found: {phrase_run_count}")
    print(f"Yellow-highlighted: {yellow_highlighted_count}")

    # Component 1: First instance highlighted in yellow (0.33 pts)
    # Component 2: Second instance highlighted in yellow (0.33 pts)
    # Component 3: Third instance highlighted in yellow (0.34 pts)
    weights = [0.33, 0.33, 0.34]
    for i in range(EXPECTED_COUNT):
        if i < yellow_highlighted_count:
            total_score += weights[i]
            print(f"PASS: Component {i+1} -- instance {i+1} highlighted in yellow ({weights[i]} pts)")
        else:
            print(f"FAIL: Component {i+1} -- instance {i+1} not highlighted in yellow")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
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
