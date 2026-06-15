"""
Reward Script: Make 'FINAL WARNING' text red and bold
Task ID: writer_hr_011
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): 'FINAL WARNING' text is bold
  Component 2 (0.5): 'FINAL WARNING' text has red font color (FF0000 or perceptually close)
"""

import os
from math import sqrt

WORKDIR = '/home/user'
TASK_ID = 'writer_hr_011'


def color_distance(c1_tuple, c2_tuple):
    """Euclidean distance between two RGB tuples."""
    return sqrt(sum((a - b) ** 2 for a, b in zip(c1_tuple, c2_tuple)))


def find_final_warning_paragraph(doc):
    """Find the paragraph containing 'FINAL WARNING' text."""
    for para in doc.paragraphs:
        if 'FINAL WARNING' in para.text:
            return para
    return None


def check_all_runs_red(runs):
    """Check if all runs have a red font color (within distance 50 of RGB 255,0,0)."""
    for run in runs:
        rgb = run.font.color.rgb if run.font.color and run.font.color.rgb else None
        if rgb is None:
            print(f"FAIL: Component 2 -- Run '{run.text[:30]}' has no explicit color (inherited/None)")
            return False
        r_val, g_val, b_val = int(rgb[0]), int(rgb[1]), int(rgb[2])
        dist = color_distance((r_val, g_val, b_val), (255, 0, 0))
        if dist > 50:
            print(f"FAIL: Component 2 -- Run '{run.text[:30]}' color ({r_val},{g_val},{b_val}) too far from red (dist={dist:.1f})")
            return False
    return True


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    from docx import Document
    from docx.shared import RGBColor

    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the paragraph with 'FINAL WARNING'
    para = find_final_warning_paragraph(doc)
    if para is None:
        print("FAIL: Could not find paragraph containing 'FINAL WARNING'")
        print("REWARD: 0.0")
        return 0.0

    # Collect runs that contain the 'FINAL WARNING' text
    # (could be one run or split across runs)
    fw_runs = []
    for run in para.runs:
        if run.text.strip():
            fw_runs.append(run)

    if not fw_runs:
        print("FAIL: No non-empty runs found in 'FINAL WARNING' paragraph")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 'FINAL WARNING' text is bold (0.5 points)
    # In initial_env: bold=False. In golden_env: bold=True.
    try:
        all_bold = all(run.font.bold is True for run in fw_runs)
        if all_bold:
            print(f"PASS: Component 1 -- All runs in 'FINAL WARNING' are bold (0.5 pts)")
            total_score += 0.5
        else:
            bold_states = [(run.text[:30], run.font.bold) for run in fw_runs]
            print(f"FAIL: Component 1 -- Not all runs are bold. States: {bold_states}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: 'FINAL WARNING' text has red font color (0.5 points)
    # In initial_env: color=000000 (black). In golden_env: color=FF0000 (red).
    # Accept any color perceptually close to red (255, 0, 0) with distance < 50.
    try:
        red_pass = check_all_runs_red(fw_runs)
        if red_pass:
            print(f"PASS: Component 2 -- All runs in 'FINAL WARNING' have red color (0.5 pts)")
            total_score += 0.5
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved GUI edits before verification
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
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)
