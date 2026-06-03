"""
Reward Script: Bold 'Sarah Johnson' in offer letter
Task ID: writer_hr_005
Domain: libreoffice_writer
Scoring: 0.25 points per bold 'Sarah Johnson' instance (4 total = 1.0)
"""

import os
import time


WORKDIR = '/home/user'
TASK_ID = 'writer_hr_005'
TARGET_NAME = 'Sarah Johnson'
EXPECTED_COUNT = 4


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
    Verify that all instances of 'Sarah Johnson' in the document are bold.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
    except ImportError:
        print("CRITICAL: python-docx not available")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find all runs containing 'Sarah Johnson' and check bold status
    # We iterate all paragraphs and look for runs whose text matches TARGET_NAME
    bold_instances = 0
    total_instances = 0

    for i, para in enumerate(doc.paragraphs):
        if TARGET_NAME not in para.text:
            continue
        for run in para.runs:
            if TARGET_NAME in run.text:
                total_instances += 1
                is_bold = run.font.bold is True
                if is_bold:
                    bold_instances += 1
                    print(f"PASS: Instance {total_instances} in para {i} — '{TARGET_NAME}' is bold (0.25 pts)")
                else:
                    print(f"FAIL: Instance {total_instances} in para {i} — '{TARGET_NAME}' is not bold (bold={run.font.bold})")

    print(f"\nFound {total_instances} instances of '{TARGET_NAME}', {bold_instances} are bold")

    if total_instances == 0:
        print(f"FAIL: No instances of '{TARGET_NAME}' found in runs — document may have unexpected structure")
        print("REWARD: 0.0")
        return 0.0

    # Score: each bold instance earns proportional credit
    # We expect 4 instances; score 0.25 each
    points_per_instance = 1.0 / EXPECTED_COUNT
    total_score = bold_instances * points_per_instance

    # Cap at 1.0
    final_score = min(total_score, 1.0)
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
