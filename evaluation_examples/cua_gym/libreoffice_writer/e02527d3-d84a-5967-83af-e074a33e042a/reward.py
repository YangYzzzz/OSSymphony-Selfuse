"""
Reward Script: Set thesis margins (left=1.5in, top/bottom/right=1.0in)
Task ID: writer_acad_001
Domain: libreoffice_writer
Scoring:
  Component 1 — Left margin = 1.5 inches  (0.4 pts)
  Component 2 — Top margin = 1.0 inch     (0.2 pts)
  Component 3 — Bottom margin = 1.0 inch  (0.2 pts)
  Component 4 — Right margin = 1.0 inch   (0.2 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_acad_001'

# Conversion: 1 inch = 914400 EMU
INCH = 914400
TOLERANCE = 0.02 * INCH  # ~0.02 inch tolerance


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def check_margin(actual_emu, expected_inches, name):
    """Check if a margin is within tolerance of the expected value in inches."""
    expected_emu = expected_inches * INCH
    diff = abs(actual_emu - expected_emu)
    actual_in = actual_emu / INCH
    if diff <= TOLERANCE:
        print(f"PASS: {name} = {actual_in:.4f} in (expected {expected_inches} in, diff={diff/INCH:.4f} in)")
        return True
    else:
        print(f"FAIL: {name} = {actual_in:.4f} in (expected {expected_inches} in, diff={diff/INCH:.4f} in)")
        return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
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

    # Precondition: document has at least one section
    if len(doc.sections) == 0:
        print("CRITICAL: Document has no sections")
        print("REWARD: 0.0")
        return 0.0

    section = doc.sections[0]

    # Component 1: Left margin = 1.5 inches (0.4 points)
    try:
        if check_margin(section.left_margin, 1.5, "Left margin"):
            total_score += 0.4
    except Exception as e:
        print(f"ERROR: Component 1 (left margin) - {e}")

    # Component 2: Top margin = 1.0 inch (0.2 points)
    try:
        if check_margin(section.top_margin, 1.0, "Top margin"):
            total_score += 0.2
    except Exception as e:
        print(f"ERROR: Component 2 (top margin) - {e}")

    # Component 3: Bottom margin = 1.0 inch (0.2 points)
    try:
        if check_margin(section.bottom_margin, 1.0, "Bottom margin"):
            total_score += 0.2
    except Exception as e:
        print(f"ERROR: Component 3 (bottom margin) - {e}")

    # Component 4: Right margin = 1.0 inch (0.2 points)
    try:
        if check_margin(section.right_margin, 1.0, "Right margin"):
            total_score += 0.2
    except Exception as e:
        print(f"ERROR: Component 4 (right margin) - {e}")

    final_score = round(min(total_score, 1.0), 1)
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
