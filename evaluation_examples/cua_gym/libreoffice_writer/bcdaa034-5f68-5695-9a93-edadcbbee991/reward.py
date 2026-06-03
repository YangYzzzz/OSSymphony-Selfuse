"""
Reward Script: Set document properties (Title, Subject, Author)
Task ID: writer_biz_055
Domain: libreoffice_writer
Scoring:
  Component 1: Title == 'Annual Business Review 2025'       — 0.4 pts
  Component 2: Subject == 'Company Performance Analysis'     — 0.3 pts
  Component 3: Author == 'Sarah Mitchell, VP of Strategy'    — 0.3 pts
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_biz_055'


def persist_app_state(domain: str):
    """Best-effort save of any unsaved GUI edits."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            import time
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify document properties are correctly set.
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

    props = doc.core_properties

    # Component 1: Title == 'Annual Business Review 2025' (0.4 points)
    try:
        actual_title = (props.title or '').strip()
        expected_title = 'Annual Business Review 2025'
        if actual_title == expected_title:
            print(f"PASS: Component 1 — Title is '{actual_title}' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Expected title '{expected_title}', found '{actual_title}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Subject == 'Company Performance Analysis' (0.3 points)
    try:
        actual_subject = (props.subject or '').strip()
        expected_subject = 'Company Performance Analysis'
        if actual_subject == expected_subject:
            print(f"PASS: Component 2 — Subject is '{actual_subject}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected subject '{expected_subject}', found '{actual_subject}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Author == 'Sarah Mitchell, VP of Strategy' (0.3 points)
    try:
        actual_author = (props.author or '').strip()
        expected_author = 'Sarah Mitchell, VP of Strategy'
        if actual_author == expected_author:
            print(f"PASS: Component 3 — Author is '{actual_author}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Expected author '{expected_author}', found '{actual_author}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved GUI edits before verification
persist_app_state("libreoffice_writer")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
