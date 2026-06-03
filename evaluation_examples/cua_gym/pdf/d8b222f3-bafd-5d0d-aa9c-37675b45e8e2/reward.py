"""
Reward Script: Create a PDF checklist with checkbox form fields
Task ID: pdf_cr_037
Domain: pdf
Scoring:
  Component 1 (0.15): Title 'Product Launch Checklist' present in text
  Component 2 (0.15): Category headings (Pre-Launch, Launch Day, Post-Launch) present
  Component 3 (0.30): At least 8 CheckBox form widgets exist
  Component 4 (0.20): Checkbox names match expected checklist items
  Component 5 (0.20): Exactly 2 checkboxes checked (Documentation complete, QA sign-off received)
"""

import os
try:
    import pymupdf
except ImportError:
    try:
        import fitz as pymupdf
    except ImportError:
        print("CRITICAL: pymupdf/fitz not available")
        print("REWARD: 0.0")
        import sys
        sys.exit(0)

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_037'

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid 1-page PDF
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(doc) < 1:
        print("CRITICAL: PDF has no pages")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    page = doc[0]
    text = page.get_text()

    # Component 1: Title 'Product Launch Checklist' present (0.15 points)
    try:
        if "Product Launch Checklist" in text:
            print(f"PASS: Component 1 -- Title 'Product Launch Checklist' found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Title 'Product Launch Checklist' not found in text")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Category headings present (0.15 points)
    try:
        categories = ["Pre-Launch", "Launch Day", "Post-Launch"]
        found_cats = [cat for cat in categories if cat in text]
        if len(found_cats) == 3:
            print(f"PASS: Component 2 -- All 3 category headings found: {found_cats} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 -- Only {len(found_cats)}/3 categories found: {found_cats}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Gather all widgets
    try:
        widgets = list(page.widgets())
        checkboxes = [w for w in widgets if w.field_type_string == "CheckBox"]
    except Exception as e:
        print(f"ERROR: Could not enumerate widgets: {e}")
        checkboxes = []

    # Component 3: At least 8 CheckBox form widgets (0.30 points)
    try:
        num_cb = len(checkboxes)
        if num_cb >= 8:
            print(f"PASS: Component 3 -- {num_cb} CheckBox widgets found (>= 8) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 -- Only {num_cb} CheckBox widgets found, need >= 8")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Checkbox names match expected checklist items (0.20 points)
    # At least 6 of 8 expected names should be present (allowing minor variation)
    try:
        expected_names = [
            "Documentation complete",
            "QA sign-off received",
            "Marketing materials ready",
            "Deploy to production",
            "Send announcement email",
            "Monitor system health",
            "Collect user feedback",
            "Fix critical bugs",
        ]
        cb_names = [w.field_name for w in checkboxes]
        matched = 0
        for expected in expected_names:
            # Check if any checkbox name contains the expected text (case-insensitive)
            for cb_name in cb_names:
                if cb_name and expected.lower() in cb_name.lower():
                    matched += 1
                    break
        if matched >= 6:
            print(f"PASS: Component 4 -- {matched}/8 expected checkbox names matched (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 -- Only {matched}/8 expected checkbox names matched. Found: {cb_names}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Exactly 2 checkboxes are checked (0.20 points)
    # Per task spec: 'Documentation complete' and 'QA sign-off received' should be checked
    try:
        checked_boxes = [w for w in checkboxes if w.field_value not in ("Off", "", None)]
        checked_names = [w.field_name for w in checked_boxes]
        num_checked = len(checked_boxes)

        # Check that at least 2 are checked AND the right ones
        has_doc = any("documentation complete" in (n or "").lower() for n in checked_names)
        has_qa = any("qa sign-off" in (n or "").lower() for n in checked_names)

        if num_checked >= 2 and has_doc and has_qa:
            print(f"PASS: Component 5 -- {num_checked} checked checkboxes, including 'Documentation complete' and 'QA sign-off received' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 5 -- {num_checked} checked. Checked names: {checked_names}. Need >= 2 with 'Documentation complete' and 'QA sign-off received'")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Desktop/checklist.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
