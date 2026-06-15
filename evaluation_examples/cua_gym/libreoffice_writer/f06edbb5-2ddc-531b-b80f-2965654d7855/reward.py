"""
Reward Script: Set first-line indentation to 0.5 inches for all body paragraphs in HR policy memo
Task ID: writer_hr_016
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): Majority of body paragraphs (>=6/8) have first-line indent ~0.5 in
  Component 2 (0.3): ALL 8 body paragraphs have first-line indent ~0.5 in
  Component 3 (0.2): Non-body paragraphs (heading, metadata) do NOT have first-line indent
"""

import os
from docx import Document
from docx.shared import Inches

WORKDIR = '/home/user'
TASK_ID = 'writer_hr_016'

# 0.5 inches = 457200 EMU. Allow 5% tolerance.
TARGET_EMU = 457200
TOLERANCE = 0.05 * TARGET_EMU  # ~22860 EMU


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
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

    # Identify body paragraphs: P3 through P10 (indices 3-10)
    # P0 = Heading, P1-P2 = metadata, P3-P10 = body text
    all_paras = doc.paragraphs
    if len(all_paras) < 11:
        print(f"FAIL: Expected at least 11 paragraphs, found {len(all_paras)}")
        print("REWARD: 0.0")
        return 0.0

    # Determine body paragraphs: Normal style paragraphs that are actual body text
    # (skip heading and short metadata-like paragraphs at top)
    body_indices = list(range(3, 11))  # P3 through P10
    non_body_indices = list(range(0, 3))  # P0 (heading), P1-P2 (metadata)

    # Component 1: Majority of body paragraphs (>=6 of 8) have correct first-line indent (0.5 points)
    try:
        body_correct_count = 0
        for idx in body_indices:
            para = all_paras[idx]
            fl_indent = para.paragraph_format.first_line_indent
            if fl_indent is not None and abs(fl_indent - TARGET_EMU) <= TOLERANCE:
                body_correct_count += 1
            else:
                print(f"  P{idx}: first_line_indent={fl_indent} (expected ~{TARGET_EMU})")

        print(f"Body paragraphs with correct indent: {body_correct_count}/8")
        if body_correct_count >= 6:
            print(f"PASS: Component 1 -- majority ({body_correct_count}/8) have 0.5in indent (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 -- only {body_correct_count}/8 body paragraphs have 0.5in indent")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: ALL 8 body paragraphs have correct first-line indent (0.3 points)
    try:
        if body_correct_count == 8:
            print(f"PASS: Component 2 -- all 8 body paragraphs have 0.5in indent (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- {body_correct_count}/8 have correct indent, need 8/8")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Non-body paragraphs do NOT have first-line indent (0.2 points)
    # This verifies the task was applied selectively to body paragraphs only
    try:
        non_body_has_indent = False
        for idx in non_body_indices:
            para = all_paras[idx]
            fl_indent = para.paragraph_format.first_line_indent
            if fl_indent is not None and fl_indent > TOLERANCE:
                non_body_has_indent = True
                print(f"  P{idx} ({para.style.name}): unexpected first_line_indent={fl_indent}")

        # This component only awards points if body paragraphs DO have indent
        # (to avoid awarding points on initial_env where nothing has indent)
        if not non_body_has_indent and body_correct_count >= 6:
            print(f"PASS: Component 3 -- non-body paragraphs correctly lack indent (0.2 pts)")
            total_score += 0.2
        elif non_body_has_indent:
            print(f"FAIL: Component 3 -- non-body paragraphs incorrectly have indent")
        else:
            print(f"FAIL: Component 3 -- skipped (body paragraphs not indented)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
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
