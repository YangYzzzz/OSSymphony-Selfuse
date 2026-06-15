"""
Reward Script: Find & Replace 12pt font to 11pt in Business Letter
Task ID: writer_frd_033
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): No 12pt text remains in the document
  Component 2 (0.3): Formerly-12pt runs are now 11pt
  Component 3 (0.15): 16pt headings are preserved unchanged
  Component 4 (0.15): 9pt footnotes are preserved unchanged
"""

import os
from docx import Document
from docx.shared import Pt

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_033'


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Change all 12pt font text to 11pt, leaving 16pt and 9pt unchanged.
    Initial state: 15 runs at 12pt, 4 runs at 16pt, 3 runs at 9pt (22 total).
    Golden state:  15 runs at 11pt, 4 runs at 16pt, 3 runs at 9pt (22 total).
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all run font sizes
    all_sizes = []
    for para in doc.paragraphs:
        for run in para.runs:
            if run.font.size is not None:
                all_sizes.append(run.font.size.pt)
            else:
                all_sizes.append(None)

    count_12 = sum(1 for s in all_sizes if s == 12.0)
    count_11 = sum(1 for s in all_sizes if s == 11.0)
    count_16 = sum(1 for s in all_sizes if s == 16.0)
    count_9 = sum(1 for s in all_sizes if s == 9.0)

    print(f"DEBUG: Font size counts — 9pt:{count_9}, 11pt:{count_11}, 12pt:{count_12}, 16pt:{count_16}, total runs:{len(all_sizes)}")

    # Component 1: No 12pt text remains (0.4 points)
    # This FAILS on initial (has 15 runs at 12pt) and PASSES on golden (0 runs at 12pt)
    try:
        if count_12 == 0:
            print(f"PASS: Component 1 — No 12pt text remains in document (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Found {count_12} runs still at 12pt (expected 0)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Formerly-12pt runs are now 11pt (0.3 points)
    # Initial had 15 runs at 12pt; golden should have 15 runs at 11pt
    # This FAILS on initial (0 runs at 11pt) and PASSES on golden (15 runs at 11pt)
    try:
        if count_11 >= 15:
            print(f"PASS: Component 2 — Found {count_11} runs at 11pt (expected >=15) (0.3 pts)")
            total_score += 0.3
        elif count_11 > 0 and count_12 == 0:
            # Partial credit: some 11pt runs exist and no 12pt remains
            partial = 0.3 * (count_11 / 15.0)
            print(f"PARTIAL: Component 2 — Found {count_11}/15 runs at 11pt ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Found {count_11} runs at 11pt (expected 15)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 16pt headings preserved (0.15 points)
    # This is a compound check: ONLY scores if 12pt->11pt change happened (count_12 == 0)
    # AND headings are still 16pt. On initial_env, count_12 != 0 so this won't score.
    try:
        if count_12 == 0 and count_16 >= 4:
            print(f"PASS: Component 3 — {count_16} heading runs preserved at 16pt (0.15 pts)")
            total_score += 0.15
        elif count_12 == 0 and count_16 > 0:
            partial = 0.15 * (count_16 / 4.0)
            print(f"PARTIAL: Component 3 — {count_16}/4 heading runs at 16pt ({partial:.2f} pts)")
            total_score += partial
        elif count_12 > 0:
            print(f"FAIL: Component 3 — Skipped (12pt text still present, task not started)")
        else:
            print(f"FAIL: Component 3 — Found {count_16} runs at 16pt (expected 4)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 9pt footnotes preserved (0.15 points)
    # Same compound-check pattern: only scores if 12pt->11pt change happened
    try:
        if count_12 == 0 and count_9 >= 3:
            print(f"PASS: Component 4 — {count_9} footnote runs preserved at 9pt (0.15 pts)")
            total_score += 0.15
        elif count_12 == 0 and count_9 > 0:
            partial = 0.15 * (count_9 / 3.0)
            print(f"PARTIAL: Component 4 — {count_9}/3 footnote runs at 9pt ({partial:.2f} pts)")
            total_score += partial
        elif count_12 > 0:
            print(f"FAIL: Component 4 — Skipped (12pt text still present, task not started)")
        else:
            print(f"FAIL: Component 4 — Found {count_9} runs at 9pt (expected 3)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook — save any unsaved LibreOffice edits
persist_app_state("libreoffice_writer")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
