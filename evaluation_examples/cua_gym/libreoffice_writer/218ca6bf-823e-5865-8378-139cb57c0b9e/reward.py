"""
Reward Script: Find & Replace misspellings of 'recieve' with 'receive'
Task ID: writer_frd_039
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): All 'recieve' -> 'receive' (3 occurrences)
  Component 2 (0.3): All 'recieves' -> 'receives' (2 occurrences)
  Component 3 (0.2): All 'recieved' -> 'received' (1 occurrence)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_039'


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


def get_full_text(doc):
    """Extract all text from paragraphs, joining into a single string."""
    return '\n'.join(para.text for para in doc.paragraphs)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Strategy: Check that each misspelling variant has been corrected.
    The initial document contains:
      - 'recieve' 3 times (should become 'receive')
      - 'recieves' 2 times (should become 'receives')
      - 'recieved' 1 time (should become 'received')

    We verify by checking:
      1. No remaining misspellings (recieve/recieves/recieved)
      2. Correct replacements present (receive/receives/received)
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    full_text = get_full_text(doc)

    # Component 1: 'recieve' (exact, not recieves/recieved) replaced with 'receive' (0.5 points)
    # Initial has 3 occurrences of standalone 'recieve' (not followed by 's' or 'd')
    try:
        # Count remaining misspelled 'recieve' (not followed by s or d)
        remaining_recieve = len(re.findall(r'recieve(?![sd])', full_text, re.IGNORECASE))
        # Count correct 'receive' (not followed by s or d)
        correct_receive = len(re.findall(r'receive(?![sd])', full_text, re.IGNORECASE))

        if remaining_recieve == 0 and correct_receive >= 3:
            print(f"PASS: Component 1 - All 'recieve' replaced with 'receive' "
                  f"(0 misspelled, {correct_receive} correct) (0.5 pts)")
            total_score += 0.5
        elif remaining_recieve == 0 and correct_receive > 0:
            partial = min(0.5 * (correct_receive / 3.0), 0.5)
            if partial > 0:
                print(f"PARTIAL: Component 1 - {correct_receive}/3 'receive' found ({partial:.2f} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 1 - {remaining_recieve} 'recieve' still present, "
                  f"{correct_receive} 'receive' found")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: 'recieves' replaced with 'receives' (0.3 points)
    # Initial has 2 occurrences of 'recieves'
    try:
        remaining_recieves = len(re.findall(r'recieves', full_text, re.IGNORECASE))
        correct_receives = len(re.findall(r'receives', full_text, re.IGNORECASE))

        if remaining_recieves == 0 and correct_receives >= 2:
            print(f"PASS: Component 2 - All 'recieves' replaced with 'receives' "
                  f"(0 misspelled, {correct_receives} correct) (0.3 pts)")
            total_score += 0.3
        elif remaining_recieves == 0 and correct_receives > 0:
            partial = min(0.3 * (correct_receives / 2.0), 0.3)
            if partial > 0:
                print(f"PARTIAL: Component 2 - {correct_receives}/2 'receives' found ({partial:.2f} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 2 - {remaining_recieves} 'recieves' still present, "
                  f"{correct_receives} 'receives' found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: 'recieved' replaced with 'received' (0.2 points)
    # Initial has 1 occurrence of 'recieved'
    try:
        remaining_recieved = len(re.findall(r'recieved', full_text, re.IGNORECASE))
        correct_received = len(re.findall(r'received', full_text, re.IGNORECASE))

        if remaining_recieved == 0 and correct_received >= 1:
            print(f"PASS: Component 3 - All 'recieved' replaced with 'received' "
                  f"(0 misspelled, {correct_received} correct) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 - {remaining_recieved} 'recieved' still present, "
                  f"{correct_received} 'received' found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved LibreOffice state before checking
persist_app_state("libreoffice_writer")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
