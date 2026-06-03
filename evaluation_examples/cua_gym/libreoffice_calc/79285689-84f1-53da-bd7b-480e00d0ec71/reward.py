"""
Reward Script: Find lowest-grossing animated film and write title + gross to docx
Task ID: osworld_multi_apps_book_reading_rate_015
Domain: multi_apps (libreoffice_writer + web research)

Task: Look up worldwide gross for animated films from 2020-2023 from boxofficemojo.com,
      find the film with the lowest worldwide gross, and write its title on line 1 and
      its gross (in USD) on line 2 of lowest_grossing_animated.docx.

Expected result:
  - Line 1: "Turning Red" (lowest grossing at $20,566,156)
  - Line 2: "$20,566,156" (or some USD representation of 20566156)

Scoring Rubric:
  Component 1: Document has content (at least 2 non-empty paragraphs)  — 0.1 points
  Component 2: Line 1 contains the correct film title "Turning Red"    — 0.5 points
  Component 3: Line 2 contains the correct gross figure (~20,566,156)  — 0.4 points
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_book_reading_rate_015'
DOC_PATH = f'{WORKDIR}/lowest_grossing_animated.docx'

# Known correct answer
CORRECT_TITLE = 'Turning Red'
CORRECT_GROSS_VALUE = 20566156  # exact value in USD


def parse_usd_value(text):
    """Parse a USD gross figure from a text string. Returns integer or None."""
    # Remove dollar sign, commas, spaces, and try to parse
    cleaned = re.sub(r'[\$,\s]', '', text.strip())
    try:
        return int(cleaned)
    except ValueError:
        try:
            return int(float(cleaned))
        except ValueError:
            return None


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

    # Gather all non-empty paragraph texts
    all_paragraphs = [p.text.strip() for p in doc.paragraphs]
    non_empty_paragraphs = [p for p in all_paragraphs if p]

    print(f"INFO: Total paragraphs: {len(all_paragraphs)}, Non-empty: {len(non_empty_paragraphs)}")
    for i, p in enumerate(all_paragraphs):
        print(f"  Para {i}: [{repr(p)}]")

    # Component 1: Document has content (at least 2 non-empty paragraphs) (0.1 points)
    # This checks the document was filled in with both title and gross
    try:
        if len(non_empty_paragraphs) >= 2:
            print(f"PASS: Component 1 — Document has at least 2 non-empty paragraphs (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — Expected >= 2 non-empty paragraphs, found {len(non_empty_paragraphs)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Line 1 contains the correct film title "Turning Red" (0.5 points)
    try:
        if non_empty_paragraphs:
            first_line = non_empty_paragraphs[0]
            # Check for exact match (case-insensitive for robustness)
            if first_line.lower() == CORRECT_TITLE.lower():
                print(f"PASS: Component 2 — Line 1 is exactly '{CORRECT_TITLE}' (0.5 pts)")
                total_score += 0.5
            elif CORRECT_TITLE.lower() in first_line.lower():
                print(f"PASS: Component 2 — Line 1 contains '{CORRECT_TITLE}' (partial, 0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Line 1 is '{first_line}', expected '{CORRECT_TITLE}'")
        else:
            print(f"FAIL: Component 2 — No non-empty paragraphs found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Line 2 contains the correct gross figure approximately matching 20,566,156 (0.4 points)
    try:
        if len(non_empty_paragraphs) >= 2:
            second_line = non_empty_paragraphs[1]
            parsed_value = parse_usd_value(second_line)
            if parsed_value is not None:
                # Allow a small tolerance (0.1%) for rounding differences
                tolerance = CORRECT_GROSS_VALUE * 0.001
                if abs(parsed_value - CORRECT_GROSS_VALUE) <= tolerance:
                    print(f"PASS: Component 3 — Line 2 gross value {parsed_value} matches expected {CORRECT_GROSS_VALUE} (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 3 — Line 2 gross value {parsed_value} does not match expected {CORRECT_GROSS_VALUE}")
            else:
                # Try to check if the raw number appears in the text at all
                raw_digits = str(CORRECT_GROSS_VALUE)
                # Check if key digits appear (e.g., '20566156' or '20,566,156')
                digits_in_line = re.sub(r'[^\d]', '', second_line)
                if digits_in_line == raw_digits:
                    print(f"PASS: Component 3 — Line 2 contains correct gross digits '{raw_digits}' (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 3 — Could not parse gross from '{second_line}', expected ~{CORRECT_GROSS_VALUE}")
        else:
            print(f"FAIL: Component 3 — No second paragraph found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
if not os.path.exists(DOC_PATH):
    print(f"File not found: {DOC_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(DOC_PATH)
