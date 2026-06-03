"""
Reward Script: Set document properties (metadata) for CloudSync API Reference
Task ID: writer_tech_081
Domain: libreoffice_writer
Scoring:
  Component 1 — Title is 'CloudSync API Reference'       (0.30 pts)
  Component 2 — Subject is 'REST API Documentation'      (0.25 pts)
  Component 3 — Keywords is 'API, REST, CloudSync, v2.1' (0.25 pts)
  Component 4 — Author is 'Engineering Team'             (0.20 pts)
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_081'


def persist_app_state():
    """Send Ctrl+S to save any unsaved edits in LibreOffice Writer."""
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that document properties (metadata) have been set correctly.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
        props = doc.core_properties
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Title is 'CloudSync API Reference' (0.30 points)
    try:
        title = props.title or ''
        if title.strip() == 'CloudSync API Reference':
            print(f"PASS: Component 1 — Title is '{title}' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Expected Title 'CloudSync API Reference', found: '{title}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Subject is 'REST API Documentation' (0.25 points)
    try:
        subject = props.subject or ''
        if subject.strip() == 'REST API Documentation':
            print(f"PASS: Component 2 — Subject is '{subject}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Expected Subject 'REST API Documentation', found: '{subject}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Keywords is 'API, REST, CloudSync, v2.1' (0.25 points)
    try:
        keywords = props.keywords or ''
        # Normalize: split by comma, strip each, sort, compare
        expected_kw = sorted([k.strip() for k in 'API, REST, CloudSync, v2.1'.split(',')])
        actual_kw = sorted([k.strip() for k in keywords.split(',')]) if keywords.strip() else []
        if actual_kw == expected_kw:
            print(f"PASS: Component 3 — Keywords is '{keywords}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Expected Keywords {expected_kw}, found: {actual_kw} (raw: '{keywords}')")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Author is 'Engineering Team' (0.20 points)
    try:
        author = props.author or ''
        if author.strip() == 'Engineering Team':
            print(f"PASS: Component 4 — Author is '{author}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Expected Author 'Engineering Team', found: '{author}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state()

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
