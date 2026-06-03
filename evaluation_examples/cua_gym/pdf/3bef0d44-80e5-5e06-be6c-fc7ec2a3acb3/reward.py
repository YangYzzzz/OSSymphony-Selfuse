"""
Reward Script: Flatten all form fields in signed_contract.pdf
Task ID: pdf_ro_007
Domain: pdf
Scoring:
  Component 1 (0.15): Output file exists at expected path
  Component 2 (0.35): Zero interactive form fields (widgets) in output
  Component 3 (0.15): Page count preserved (6 pages)
  Component 4 (0.35): Field values preserved as static text
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_007'

OUTPUT_PATH = os.path.join(WORKDIR, 'forms', 'signed_contract_final.pdf')

# Key field values that must be preserved as static text after flattening
EXPECTED_VALUES = [
    'Alexandra Petrova',
    'Northwind Technologies',
    '87,500',
    'Daniel R. Whitmore',
    'March 15, 2025',
    'March 12, 2025',
    'September 15, 2025',
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists (0.15 points)
    # This fails on initial_env (file does not exist) and passes on golden_env
    try:
        if os.path.isfile(OUTPUT_PATH):
            file_size = os.path.getsize(OUTPUT_PATH)
            if file_size > 100:
                print(f"PASS: Component 1 — Output file exists at {OUTPUT_PATH} ({file_size} bytes) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — File exists but too small ({file_size} bytes)")
        else:
            print(f"FAIL: Component 1 — Output file not found at {OUTPUT_PATH}")
            # No file means nothing else can pass
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load the PDF for subsequent checks
    try:
        import fitz
        doc = fitz.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {OUTPUT_PATH}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Zero interactive form fields / widgets (0.35 points)
    # The core requirement: all form fields must be flattened (no widgets remain)
    try:
        widget_count = 0
        for page in doc:
            widget_count += len(list(page.widgets()))
        if widget_count == 0:
            print(f"PASS: Component 2 — Zero form widgets found (flattened) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — Found {widget_count} remaining form widgets (expected 0)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Page count preserved at 6 (0.15 points)
    try:
        page_count = len(doc)
        if page_count == 6:
            print(f"PASS: Component 3 — Page count is 6 as expected (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Page count is {page_count}, expected 6")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Field values preserved as static text (0.35 points)
    # After flattening, the form field values should be rendered as static text
    # and extractable via text extraction
    try:
        full_text = ''
        for page in doc:
            full_text += page.get_text()

        found_count = 0
        for value in EXPECTED_VALUES:
            if value in full_text:
                found_count += 1
                print(f"  TEXT CHECK: '{value}' — found")
            else:
                print(f"  TEXT CHECK: '{value}' — MISSING")

        if found_count == len(EXPECTED_VALUES):
            print(f"PASS: Component 4 — All {found_count}/{len(EXPECTED_VALUES)} field values preserved as text (0.35 pts)")
            total_score += 0.35
        elif found_count >= len(EXPECTED_VALUES) - 1:
            partial = round(0.35 * found_count / len(EXPECTED_VALUES), 2)
            print(f"PARTIAL: Component 4 — {found_count}/{len(EXPECTED_VALUES)} values found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Only {found_count}/{len(EXPECTED_VALUES)} field values found in text")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
