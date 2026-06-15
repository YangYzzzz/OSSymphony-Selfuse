"""
Reward Script: Create checklist.pdf with form fields (10 checkboxes + 1 text field)
Task ID: pdf_adv_181
Domain: pdf
Scoring:
  - Precondition gate: file exists at ~/Documents/checklist.pdf
  - Component 1: PDF has exactly 1 page and is A4 size (~595x842 pts) (0.2 pts)
  - Component 2: Text field named 'inspector_name' exists (0.2 pts)
  - Component 3: All 10 checkboxes (item_1 through item_10) exist (0.4 pts)
  - Component 4: Total form fields == 11 (10 checkboxes + 1 text field) (0.2 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_adv_181'
FILE_PATH = f'{WORKDIR}/Documents/checklist.pdf'

# A4 dimensions in points (within 2pt tolerance)
A4_WIDTH = 595.0
A4_HEIGHT = 842.0
A4_TOLERANCE = 2.0


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    # Import pymupdf inside function (after file existence gate has passed)
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf
        except ImportError:
            print("CRITICAL: pymupdf/fitz library not available")
            print("REWARD: 0.0")
            return 0.0

    total_score = 0.0

    # Load PDF
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Exactly 1 page and A4 dimensions (0.2 points)
    # This FAILS on initial_env (file doesn't exist) and PASSES on golden_env.
    try:
        page_count = doc.page_count
        page = doc[0]
        width = page.rect.width
        height = page.rect.height

        is_single_page = (page_count == 1)
        is_a4 = (
            abs(width - A4_WIDTH) <= A4_TOLERANCE and
            abs(height - A4_HEIGHT) <= A4_TOLERANCE
        )

        if is_single_page and is_a4:
            print(f"PASS: Component 1 — 1 page, A4 size ({width:.1f}x{height:.1f} pts) (0.2 pts)")
            total_score += 0.2
        elif is_single_page:
            print(f"FAIL: Component 1 — 1 page but wrong size {width:.1f}x{height:.1f} pts, expected ~{A4_WIDTH}x{A4_HEIGHT}")
        else:
            print(f"FAIL: Component 1 — expected 1 page, found {page_count} pages")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Collect all form fields from page 0
    all_fields = []
    try:
        page = doc[0]
        for widget in page.widgets():
            all_fields.append({
                "name": widget.field_name,
                "type_name": widget.field_type_string,
            })
    except Exception as e:
        print(f"ERROR: Cannot read form fields: {e}")
        doc.close()
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Text field 'inspector_name' exists (0.2 points)
    # Task requires inspector_name text field at the top; absent in initial_env.
    try:
        inspector_field = [f for f in all_fields
                           if f["name"] == "inspector_name" and f["type_name"] == "Text"]
        if inspector_field:
            print("PASS: Component 2 — text field 'inspector_name' found (0.2 pts)")
            total_score += 0.2
        else:
            present = [f["name"] for f in all_fields]
            print(f"FAIL: Component 2 — text field 'inspector_name' not found. Fields present: {present}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 10 checkboxes item_1 through item_10 exist (0.4 points)
    # Task requires exactly 10 checkbox fields labeled item_1 to item_10; absent in initial_env.
    try:
        expected_checkboxes = [f"item_{i}" for i in range(1, 11)]
        checkbox_names = {f["name"] for f in all_fields if f["type_name"] == "CheckBox"}
        missing = [name for name in expected_checkboxes if name not in checkbox_names]
        found_count = len(expected_checkboxes) - len(missing)

        if not missing:
            print(f"PASS: Component 3 — all 10 checkboxes (item_1 to item_10) found (0.4 pts)")
            total_score += 0.4
        else:
            # Partial credit: 0.04 pts per found checkbox
            partial = round(found_count * 0.04, 4)
            print(f"PARTIAL: Component 3 — found {found_count}/10 checkboxes, missing: {missing} ({partial:.2f} pts)")
            total_score += partial
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Exactly 11 total form fields (10 checkboxes + 1 text field) (0.2 points)
    # This verifies the complete form structure; absent in initial_env.
    try:
        total_fields = len(all_fields)
        if total_fields == 11:
            print(f"PASS: Component 4 — exactly 11 form fields total (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — expected 11 form fields, found {total_fields}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Precondition gate: if file does not exist, score is 0.0 immediately
if not os.path.exists(FILE_PATH):
    print(f"FAIL: File not found at {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
