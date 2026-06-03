"""
Reward Script: Validate PDF structure and write validation report
Task ID: pdf_cr_045
Domain: pdf
Scoring:
  - Component 1: Page count line correct (0.25)
  - Component 2: Metadata line correct (0.25)
  - Component 3: Page dimensions line correct (0.25)
  - Component 4: Blank pages line correct (0.25)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_045'
VALIDATION_PATH = os.path.join(WORKDIR, 'Desktop', 'validation.txt')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: validation.txt must exist
    if not os.path.exists(VALIDATION_PATH):
        print(f"PRECONDITION FAIL: {VALIDATION_PATH} does not exist")
        print("REWARD: 0.0")
        return 0.0

    try:
        content = open(VALIDATION_PATH, 'r').read().strip()
        lines = [l.strip() for l in content.split('\n') if l.strip()]
    except Exception as e:
        print(f"CRITICAL: Cannot read {VALIDATION_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Build a dict of key: value from the lines for flexible matching
    line_dict = {}
    for line in lines:
        if ':' in line:
            key, _, val = line.partition(':')
            line_dict[key.strip().lower()] = val.strip()

    # Component 1: Page count is correct (0.25 points)
    # The PDF has 7 pages. The validation report must state "Page count: 7"
    try:
        page_count_val = line_dict.get('page count', '')
        if page_count_val == '7':
            print(f"PASS: Component 1 — Page count is 7 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected page count '7', found '{page_count_val}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Metadata presence is correct (0.25 points)
    # The PDF has metadata (title, author, etc.). Report must say "Has metadata: Yes"
    try:
        metadata_val = line_dict.get('has metadata', '')
        if metadata_val.lower() == 'yes':
            print(f"PASS: Component 2 — Has metadata: Yes (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Expected 'Yes' for metadata, found '{metadata_val}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Page dimensions consistency is correct (0.25 points)
    # Page 5 is 612x792 while others are 595x842, so dimensions are NOT consistent.
    # Report must say "Consistent page dimensions: No"
    try:
        dims_val = line_dict.get('consistent page dimensions', '')
        if dims_val.lower() == 'no':
            print(f"PASS: Component 3 — Consistent page dimensions: No (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Expected 'No' for dimensions consistency, found '{dims_val}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Blank pages identified correctly (0.25 points)
    # Page 4 is blank (no text, no images). Report must say "Blank pages: [4]"
    try:
        blank_val = line_dict.get('blank pages', '')
        # Accept variations like "[4]", "4", "[4]" with spaces
        # The key check: page 4 must be identified as blank
        normalized = blank_val.replace(' ', '').replace('[', '').replace(']', '')
        if normalized == '4':
            print(f"PASS: Component 4 — Blank pages: [4] (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — Expected blank pages '[4]', found '{blank_val}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
