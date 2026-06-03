"""
Reward Script: Change paper size from A4 to US Letter
Task ID: writer_hr_009
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): Page width matches US Letter (8.5 in / 7772400 EMU)
  Component 2 (0.5): Page height matches US Letter (11 in / 10058400 EMU)
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_hr_009'

# US Letter dimensions in EMU
# 8.5 inches = 7772400 EMU, 11 inches = 10058400 EMU
LETTER_WIDTH_EMU = 7772400
LETTER_HEIGHT_EMU = 10058400

# Tolerance: ~0.1 inch = 9144 EMU (generous for rounding differences)
TOLERANCE_EMU = 50000


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
    Verify that the document paper size has been changed to US Letter.
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

    # Precondition: document must have at least one section
    if len(doc.sections) == 0:
        print("FAIL: No sections found in document")
        print("REWARD: 0.0")
        return 0.0

    section = doc.sections[0]
    actual_width = section.page_width
    actual_height = section.page_height

    print(f"INFO: Page width  = {actual_width} EMU (expected ~{LETTER_WIDTH_EMU} for US Letter)")
    print(f"INFO: Page height = {actual_height} EMU (expected ~{LETTER_HEIGHT_EMU} for US Letter)")

    # Component 1: Page width matches US Letter (0.5 points)
    try:
        width_diff = abs(actual_width - LETTER_WIDTH_EMU)
        if width_diff <= TOLERANCE_EMU:
            print(f"PASS: Component 1 -- Page width is US Letter ({actual_width} EMU, diff={width_diff}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 -- Page width {actual_width} EMU differs from Letter {LETTER_WIDTH_EMU} by {width_diff}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Page height matches US Letter (0.5 points)
    try:
        height_diff = abs(actual_height - LETTER_HEIGHT_EMU)
        if height_diff <= TOLERANCE_EMU:
            print(f"PASS: Component 2 -- Page height is US Letter ({actual_height} EMU, diff={height_diff}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 -- Page height {actual_height} EMU differs from Letter {LETTER_HEIGHT_EMU} by {height_diff}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved GUI state before verification
persist_app_state("libreoffice_writer")

# Test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
