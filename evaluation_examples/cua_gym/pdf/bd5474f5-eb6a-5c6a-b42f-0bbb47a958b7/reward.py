"""
Reward Script: Add form fields to petty cash log template
Task ID: pdf_fin_069
Domain: pdf
Scoring:
  Component 1 (0.20): fund_custodian text field exists on page 1
  Component 2 (0.40): 20 rows of fillable fields (date_N, description_N, amount_in_N, amount_out_N)
  Component 3 (0.15): balance text field exists
  Component 4 (0.25): Total widget count == 82, all Text type
"""

import os
import pymupdf  # PyMuPDF (fitz)

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_069'
OUTPUT_FILE = f'{WORKDIR}/finance/petty_cash_log_fillable.pdf'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be loadable
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

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

    # Collect all widgets into a dict by name
    widgets = {}
    try:
        for w in page.widgets():
            widgets[w.field_name] = {
                "type": w.field_type,
                "type_name": w.field_type_string,
                "rect": tuple(w.rect),
            }
    except Exception as e:
        print(f"CRITICAL: Cannot iterate widgets: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: fund_custodian text field exists (0.20 points)
    try:
        if "fund_custodian" in widgets and widgets["fund_custodian"]["type_name"] == "Text":
            print(f"PASS: Component 1 — fund_custodian text field found at {widgets['fund_custodian']['rect']} (0.20 pts)")
            total_score += 0.20
        else:
            if "fund_custodian" in widgets:
                print(f"FAIL: Component 1 — fund_custodian exists but type is {widgets['fund_custodian']['type_name']}, expected Text")
            else:
                print(f"FAIL: Component 1 — fund_custodian field not found among {len(widgets)} widgets")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 20 rows of fillable fields (0.40 points)
    # Each row should have: date_N, description_N, amount_in_N, amount_out_N
    try:
        complete_rows = 0
        row_prefixes = ["date", "description", "amount_in", "amount_out"]
        for row_num in range(1, 21):
            row_fields = [f"{prefix}_{row_num}" for prefix in row_prefixes]
            row_ok = (
                all(f in widgets for f in row_fields)
                and all(widgets[f]["type_name"] == "Text" for f in row_fields if f in widgets)
            )
            if row_ok:
                complete_rows += 1

        # Award proportional credit: 0.40 * (complete_rows / 20)
        if complete_rows == 20:
            print(f"PASS: Component 2 — All 20 rows of fillable fields found (0.40 pts)")
            total_score += 0.40
        elif complete_rows > 0:
            row_score = 0.40 * (complete_rows / 20.0)
            print(f"PARTIAL: Component 2 — {complete_rows}/20 rows complete ({row_score:.2f} pts)")
            total_score += row_score
        else:
            print(f"FAIL: Component 2 — No complete rows found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: balance text field exists (0.15 points)
    try:
        if "balance" in widgets and widgets["balance"]["type_name"] == "Text":
            print(f"PASS: Component 3 — balance text field found at {widgets['balance']['rect']} (0.15 pts)")
            total_score += 0.15
        else:
            if "balance" in widgets:
                print(f"FAIL: Component 3 — balance exists but type is {widgets['balance']['type_name']}, expected Text")
            else:
                print(f"FAIL: Component 3 — balance field not found among {len(widgets)} widgets")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Total widget count == 82 and all are Text type (0.25 points)
    # Expected: 1 (custodian) + 80 (4 fields x 20 rows) + 1 (balance) = 82
    try:
        total_widgets = len(widgets)
        all_text = all(w["type_name"] == "Text" for w in widgets.values())

        if total_widgets == 82 and all_text:
            print(f"PASS: Component 4 — Total widget count is 82 and all are Text type (0.25 pts)")
            total_score += 0.25
        elif total_widgets >= 80 and all_text:
            partial = min(0.25 * (total_widgets / 82.0), 0.20)
            total_score += partial
            print(f"PARTIAL: Component 4 — Widget count is {total_widgets} (expected 82), all Text ({partial:.2f} pts)")
        else:
            non_text = [name for name, w in widgets.items() if w["type_name"] != "Text"]
            print(f"FAIL: Component 4 — Widget count: {total_widgets} (expected 82), all_text: {all_text}")
            if non_text:
                print(f"  Non-text widgets: {non_text[:5]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
if not os.path.exists(OUTPUT_FILE):
    print(f"File not found: {OUTPUT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_FILE)
