"""
Reward Script: Swap FirstName LastName to LastName, FirstName in Class_Roster.docx
Task ID: writer_frd_021
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): All lines match 'LastName, FirstName' format
  Component 2 (0.3): Specific name spot-checks (first, middle, last)
  Component 3 (0.3): No lines remain in original 'FirstName LastName' format
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_021'


def persist_app_state(domain):
    """Save any unsaved LibreOffice edits before verification."""
    import time
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

    # Extract all non-empty paragraph texts
    lines = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    print(f"INFO: Found {len(lines)} non-empty paragraphs")

    if len(lines) == 0:
        print("FAIL: No text content found in document")
        print("REWARD: 0.0")
        return 0.0

    # Pattern for correctly swapped format: "LastName, FirstName"
    swapped_pattern = re.compile(r'^[A-Z][a-z]+,\s+[A-Z][a-z]+$')
    # Pattern for original format: "FirstName LastName" (no comma)
    original_pattern = re.compile(r'^[A-Z][a-z]+\s+[A-Z][a-z]+$')

    # Component 1: All lines match 'LastName, FirstName' format (0.4 points)
    try:
        swapped_count = sum(1 for line in lines if swapped_pattern.match(line))
        ratio = swapped_count / len(lines) if lines else 0
        print(f"INFO: {swapped_count}/{len(lines)} lines match 'LastName, FirstName' format")

        if ratio == 1.0:
            print(f"PASS: Component 1 - All {len(lines)} lines in correct format (0.4 pts)")
            total_score += 0.4
        elif ratio >= 0.8:
            partial = 0.4 * ratio
            print(f"PARTIAL: Component 1 - {swapped_count}/{len(lines)} lines correct ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 - Only {swapped_count}/{len(lines)} lines in correct format")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Specific name spot-checks (0.3 points)
    # Check first, middle, and last names against known ground truth
    expected_checks = {
        "Johnson, Alice": False,     # line 0
        "Okonkwo, James": False,     # line 9 (middle-ish)
        "Abdi, Yusuf": False,        # line 24 (last)
        "Kim, Grace": False,         # line 6
        "Stein, Rachel": False,      # line 17
    }
    try:
        for line in lines:
            stripped = line.strip()
            if stripped in expected_checks:
                expected_checks[stripped] = True

        matches = sum(1 for v in expected_checks.values() if v)
        total_checks = len(expected_checks)
        if matches == total_checks:
            print(f"PASS: Component 2 - All {total_checks} spot-checks passed (0.3 pts)")
            total_score += 0.3
        elif matches > 0:
            partial = 0.3 * (matches / total_checks)
            print(f"PARTIAL: Component 2 - {matches}/{total_checks} spot-checks passed ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - No spot-checks matched")
            for name, found in expected_checks.items():
                print(f"  Expected '{name}': {'found' if found else 'NOT found'}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: No lines remain in original 'FirstName LastName' format (0.3 points)
    try:
        original_count = sum(1 for line in lines if original_pattern.match(line) and ',' not in line)
        if original_count == 0:
            print(f"PASS: Component 3 - No lines in original format (0.3 pts)")
            total_score += 0.3
        elif original_count < len(lines):
            # Partial: deduct proportionally for remaining originals
            remaining_ratio = original_count / len(lines)
            partial = 0.3 * (1.0 - remaining_ratio)
            print(f"FAIL: Component 3 - {original_count} lines still in original format ({partial:.2f} pts)")
            if partial > 0:
                total_score += partial
        else:
            print(f"FAIL: Component 3 - All {original_count} lines still in original format")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
