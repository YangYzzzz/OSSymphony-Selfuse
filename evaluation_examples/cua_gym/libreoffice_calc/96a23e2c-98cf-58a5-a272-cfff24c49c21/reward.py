"""
Reward Script: Write the title of the cookbook with fewest recipes in fewest_recipes.docx
Task ID: osworld_multi_apps_book_reading_rate_010
Domain: multi_apps (libreoffice_calc + libreoffice_writer)
Scoring:
  Component 1 (0.4): fewest_recipes.docx contains non-empty text (task was attempted)
  Component 2 (0.6): The text in fewest_recipes.docx matches the correct cookbook title
                     "Salt Fat Acid Heat" (the cookbook with fewest recipes: 100)
Total: 1.0
"""

import os
from docx import Document

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_book_reading_rate_010'

# The expected answer based on Goodreads data:
# Jerusalem: 120, Salt Fat Acid Heat: 100, The Food Lab: 300,
# Plenty: 120, Mastering the Art of French Cooking: 524
# Fewest = Salt Fat Acid Heat (100 recipes)
EXPECTED_TITLE = "Salt Fat Acid Heat"


def verify_task(docx_path):
    """
    Verify that fewest_recipes.docx contains the title of the cookbook
    with the fewest recipes (Salt Fat Acid Heat).
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(docx_path):
        print(f"CRITICAL: fewest_recipes.docx not found at {docx_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load the document
    try:
        doc = Document(docx_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load {docx_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract all text from the document (concatenate all non-empty paragraphs)
    all_text_parts = []
    try:
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                all_text_parts.append(text)
    except Exception as e:
        print(f"ERROR: Could not read paragraphs: {e}")

    full_text = " ".join(all_text_parts).strip()

    # Component 1: Document contains non-empty text (0.4 points)
    # This FAILS on initial_env (empty doc) and PASSES on golden_env (has content)
    try:
        if len(full_text) > 0:
            print(f"PASS: Component 1 — document contains text: {repr(full_text[:100])} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — document is empty, no text found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The document text matches "Salt Fat Acid Heat" (0.6 points)
    # This verifies the agent correctly identified the cookbook with fewest recipes.
    # FAILS on initial_env (empty doc) and PASSES on golden_env (correct title present)
    try:
        # Normalize for comparison: strip whitespace, case-insensitive
        normalized_full = full_text.strip().lower()
        normalized_expected = EXPECTED_TITLE.strip().lower()

        # Check if the expected title is the primary/sole content of the document,
        # or at least clearly present as the answer
        if normalized_full == normalized_expected:
            print(f"PASS: Component 2 — document contains exact title '{EXPECTED_TITLE}' (0.6 pts)")
            total_score += 0.6
        elif normalized_expected in normalized_full and len(full_text.strip()) <= len(EXPECTED_TITLE) * 3:
            # Title is present and the document is not heavily polluted with extra text
            print(f"PASS: Component 2 — document contains title '{EXPECTED_TITLE}' (0.6 pts)")
            total_score += 0.6
        elif normalized_expected in normalized_full:
            # Title is present but surrounded by a lot of other text — partial credit
            print(f"PARTIAL: Component 2 — title '{EXPECTED_TITLE}' found but document has extra content: {repr(full_text[:200])} (0.3 pts)")
            total_score += 0.3
        else:
            # Check for very close / common misspellings or partial matches
            # e.g., agent may write just "Salt Fat Acid Heat" with minor variation
            words_expected = set(normalized_expected.split())
            words_found = set(normalized_full.split())
            overlap = words_expected & words_found
            if len(overlap) >= 3:
                print(f"PARTIAL: Component 2 — partial title match, words found: {overlap} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — expected '{EXPECTED_TITLE}', got: {repr(full_text[:200])}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
docx_path = f'{WORKDIR}/fewest_recipes.docx'
if not os.path.exists(docx_path):
    print(f"File not found: {docx_path}")
    print("REWARD: 0.0")
else:
    verify_task(docx_path)
