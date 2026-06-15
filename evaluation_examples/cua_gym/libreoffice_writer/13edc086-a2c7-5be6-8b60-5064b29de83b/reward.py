"""
Reward Script: US phone number format conversion via regex find-and-replace
Task ID: writer_frd_013
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): No parenthesized phone numbers remain
  Component 2 (0.4): All 15 phone numbers converted to XXX-XXX-XXXX
  Component 3 (0.2): Document integrity - non-phone content preserved
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_013'

# Regex patterns for the two phone formats
PAREN_PATTERN = re.compile(r'\(\d{3}\)\s\d{3}-\d{4}')
DASH_PATTERN = re.compile(r'(?<!\()\b\d{3}-\d{3}-\d{4}\b')

# Expected number of phone numbers in the document
EXPECTED_PHONE_COUNT = 15

# Expected minimum paragraph count (document structure integrity)
EXPECTED_MIN_PARAGRAPHS = 90


def persist_app_state(domain):
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

    # Collect all paragraph text
    all_text = []
    for para in doc.paragraphs:
        all_text.append(para.text)

    full_text = '\n'.join(all_text)

    # Count phone numbers in each format
    paren_matches = PAREN_PATTERN.findall(full_text)
    dash_matches = DASH_PATTERN.findall(full_text)
    paren_count = len(paren_matches)
    dash_count = len(dash_matches)

    print(f"INFO: Found {paren_count} parenthesized phone numbers")
    print(f"INFO: Found {dash_count} dash-format phone numbers")
    print(f"INFO: Total paragraphs: {len(all_text)}")

    # Component 1: No parenthesized phone numbers remain (0.4 points)
    # This FAILS on initial (15 paren numbers) and PASSES on golden (0 paren numbers)
    try:
        if paren_count == 0:
            print(f"PASS: Component 1 -- No parenthesized phone numbers remain (0.4 pts)")
            total_score += 0.4
        else:
            # Partial credit: proportional to how many were removed
            # Initial has 15, so partial = (15 - remaining) / 15 * 0.4
            removed_fraction = max(0, (EXPECTED_PHONE_COUNT - paren_count)) / EXPECTED_PHONE_COUNT
            partial = round(removed_fraction * 0.4, 2)
            if partial > 0 and partial < 0.4:
                print(f"PARTIAL: Component 1 -- {paren_count} parenthesized numbers remain ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 1 -- {paren_count} parenthesized phone numbers still present")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: All 15 phone numbers in XXX-XXX-XXXX format (0.4 points)
    # This FAILS on initial (0 dash numbers) and PASSES on golden (15 dash numbers)
    try:
        if dash_count >= EXPECTED_PHONE_COUNT:
            print(f"PASS: Component 2 -- All {dash_count} phone numbers in XXX-XXX-XXXX format (0.4 pts)")
            total_score += 0.4
        elif dash_count > 0:
            # Partial credit: proportional to how many were converted
            partial = round((dash_count / EXPECTED_PHONE_COUNT) * 0.4, 2)
            print(f"PARTIAL: Component 2 -- {dash_count}/{EXPECTED_PHONE_COUNT} numbers converted ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No phone numbers in XXX-XXX-XXXX format found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Document integrity preserved (0.2 points)
    # Verify non-phone content is intact: paragraph count and key structural text
    # This check is COMPOUND: anchored to the phone format change.
    # It awards points only when at least one phone number is in the new format
    # AND the document structure is preserved. On initial_env, dash_count==0, so this fails.
    try:
        para_count = len(all_text)
        has_title = any('Client Directory' in p for p in all_text)
        has_email = any('Email:' in p for p in all_text)
        has_structure = para_count >= EXPECTED_MIN_PARAGRAPHS and has_title and has_email

        # Compound check: structure intact AND at least some conversion happened
        if has_structure and dash_count > 0:
            print(f"PASS: Component 3 -- Document integrity preserved with {para_count} paragraphs (0.2 pts)")
            total_score += 0.2
        elif not has_structure:
            print(f"FAIL: Component 3 -- Document structure compromised (paras={para_count}, title={has_title}, email={has_email})")
        else:
            print(f"FAIL: Component 3 -- No converted phone numbers found (compound check)")
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
