"""
Reward Script: Increase font size of all section headings from 12pt to 16pt bold
Task ID: writer_hr_013
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): All 6 Heading 1 runs have font size 16pt
  Component 2 (0.3): All 6 Heading 1 runs have bold=True
  Component 3 (0.3): Heading 1 style definition has size=16pt and bold=True
"""

import os
from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'writer_hr_013'


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

    # Collect all Heading 1 paragraphs
    heading1_paras = [p for p in doc.paragraphs if p.style and p.style.name == 'Heading 1']
    print(f"INFO: Found {len(heading1_paras)} Heading 1 paragraphs")

    if len(heading1_paras) == 0:
        print("FAIL: No Heading 1 paragraphs found")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All Heading 1 runs have font size 16pt (0.4 points)
    # This checks the task-introduced change: size was 12pt, should now be 16pt
    try:
        size_pass_count = 0
        size_total_count = 0
        for para in heading1_paras:
            for run in para.runs:
                if not run.text.strip():
                    continue
                size_total_count += 1
                if run.font.size is not None and abs(run.font.size.pt - 16.0) < 0.5:
                    size_pass_count += 1
                else:
                    actual_pt = run.font.size.pt if run.font.size else None
                    print(f"FAIL detail: Run '{run.text[:40]}' has size={actual_pt}pt, expected 16pt")

        if size_total_count > 0 and size_pass_count == size_total_count:
            print(f"PASS: Component 1 - All {size_pass_count} heading runs have 16pt font size (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 - {size_pass_count}/{size_total_count} heading runs have 16pt font size")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: All Heading 1 runs have bold=True (0.3 points)
    # This checks the task-introduced change: bold was False, should now be True
    try:
        bold_pass_count = 0
        bold_total_count = 0
        for para in heading1_paras:
            for run in para.runs:
                if not run.text.strip():
                    continue
                bold_total_count += 1
                if run.font.bold is True:
                    bold_pass_count += 1
                else:
                    print(f"FAIL detail: Run '{run.text[:40]}' has bold={run.font.bold}, expected True")

        if bold_total_count > 0 and bold_pass_count == bold_total_count:
            print(f"PASS: Component 2 - All {bold_pass_count} heading runs have bold=True (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 - {bold_pass_count}/{bold_total_count} heading runs have bold=True")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Heading 1 style definition has size=16pt and bold=True (0.3 points)
    # Verifying the style was modified (not just individual run overrides)
    try:
        style_found = False
        for s in doc.styles:
            if s.name == 'Heading 1':
                style_found = True
                style_size_ok = s.font.size is not None and abs(s.font.size.pt - 16.0) < 0.5
                style_bold_ok = s.font.bold is True
                print(f"INFO: Heading 1 style: size={s.font.size.pt if s.font.size else None}pt, bold={s.font.bold}")

                if style_size_ok and style_bold_ok:
                    print(f"PASS: Component 3 - Heading 1 style has 16pt bold (0.3 pts)")
                    total_score += 0.3
                else:
                    if not style_size_ok:
                        print(f"FAIL: Component 3 - Heading 1 style size is not 16pt")
                    if not style_bold_ok:
                        print(f"FAIL: Component 3 - Heading 1 style bold is not True")
                break

        if not style_found:
            print("FAIL: Component 3 - Heading 1 style not found in document")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

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
