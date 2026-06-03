"""
Reward Script: Look up fastest marathon winning time and write race name to docx
Task ID: osworld_multi_apps_book_reading_rate_013
Domain: libreoffice_calc / libreoffice_writer (multi-app)
Scoring:
  - Component 1 (0.4 pts): fastest_marathon.docx exists on Desktop and has non-empty text content
  - Component 2 (0.6 pts): The document text contains "Berlin Marathon 2023" (the correct answer)
Total: 1.0
"""

import os

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_book_reading_rate_013'
DOC_PATH = f'{WORKDIR}/Desktop/fastest_marathon.docx'

# Expected answer: Berlin Marathon 2023 had the fastest men's winning time in 2023
# Eliud Kipchoge won Berlin 2023 with 2:01:09 — the fastest of the five major marathons that year
EXPECTED_RACE_NAME = 'Berlin Marathon 2023'


def verify_task(file_path):
    """
    Verify that fastest_marathon.docx contains the correct race name.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: ensure the file exists
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load the document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load docx file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Gather all text from the document
    all_text_parts = []
    for para in doc.paragraphs:
        if para.text.strip():
            all_text_parts.append(para.text.strip())
    full_text = ' '.join(all_text_parts)

    # Component 1: Document has non-empty text content (0.4 points)
    # This FAILS on initial_env (empty doc) and PASSES on golden_env (has content)
    try:
        if full_text:
            print(f"PASS: Component 1 — document has non-empty text content: '{full_text[:80]}' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — document is empty (no text content)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Document contains the correct race name "Berlin Marathon 2023" (0.6 points)
    # This FAILS on initial_env (empty) and PASSES on golden_env (contains correct answer)
    try:
        # Case-insensitive check to be robust against capitalization variants
        if EXPECTED_RACE_NAME.lower() in full_text.lower():
            print(f"PASS: Component 2 — found '{EXPECTED_RACE_NAME}' in document (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 2 — expected '{EXPECTED_RACE_NAME}' but document contains: '{full_text}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(DOC_PATH):
    print(f"File not found: {DOC_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(DOC_PATH)
