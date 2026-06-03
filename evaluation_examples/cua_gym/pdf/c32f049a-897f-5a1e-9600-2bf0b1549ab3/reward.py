"""
Reward Script: Verify timesheet.pdf has correct form fields.
Task ID: pdf_adv_188
Domain: pdf

Scoring rubric (only task-introduced changes are scored):
  Precondition: File exists and is a valid 2-page PDF (gate only, not scored)
  Component 1 (0.25): Page 1 has exactly 4 text fields
  Component 2 (0.25): Page 1 text fields are named correctly
  Component 3 (0.25): Page 2 has exactly 6 text fields + 1 checkbox (7 total)
  Component 4 (0.25): Page 2 text field names correct AND checkbox named 'supervisor_approved'
  Total: 1.0

NOTE: Page count (2) is a precondition/gate — it is true in the initial state and is
NOT scored to avoid reward(initial_env) > 0.0.
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = "/home/user/Documents"
FILE_PATH = f"{WORKDIR}/timesheet.pdf"

# Expected field names per page
P1_EXPECTED_FIELDS = {"employee_name", "employee_id", "department", "week_ending"}
P2_EXPECTED_TEXT_FIELDS = {
    "monday_hours", "tuesday_hours", "wednesday_hours",
    "thursday_hours", "friday_hours", "total_hours"
}
P2_EXPECTED_CHECKBOX = "supervisor_approved"


def verify_task(file_path):
    """
    Verify timesheet.pdf has the correct interactive form fields.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ── Precondition: file must exist ────────────────────────────────────────
    if not os.path.exists(file_path):
        print(f"FAIL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ── Precondition gate: 2-page PDF (not scored — true in initial state too) ─
    try:
        page_count = doc.page_count
        if page_count != 2:
            print(f"GATE FAIL: Expected 2-page PDF, found {page_count} pages")
            doc.close()
            print("REWARD: 0.0")
            return 0.0
        else:
            print(f"GATE PASS: PDF has 2 pages (precondition — not scored)")
    except Exception as e:
        print(f"GATE ERROR: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # ── Collect widgets per page ──────────────────────────────────────────────
    try:
        p1_widgets = list(doc[0].widgets())
    except Exception:
        p1_widgets = []
    try:
        p2_widgets = list(doc[1].widgets())
    except Exception:
        p2_widgets = []

    # ── Component 1: Page 1 has exactly 4 text fields (0.25 pts) ─────────────
    try:
        p1_text_fields = [w for w in p1_widgets if w.field_type_string == "Text"]
        if len(p1_text_fields) == 4:
            print(f"PASS: Component 1 — Page 1 has 4 text fields (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected 4 text fields on page 1, found {len(p1_text_fields)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ── Component 2: Page 1 text field names correct (0.25 pts) ──────────────
    try:
        p1_names = {w.field_name for w in p1_widgets if w.field_type_string == "Text"}
        if p1_names == P1_EXPECTED_FIELDS:
            print(f"PASS: Component 2 — Page 1 field names correct: {sorted(p1_names)} (0.25 pts)")
            total_score += 0.25
        else:
            missing = P1_EXPECTED_FIELDS - p1_names
            extra = p1_names - P1_EXPECTED_FIELDS
            print(f"FAIL: Component 2 — Page 1 field names mismatch. "
                  f"Missing: {missing}, Extra: {extra}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ── Component 3: Page 2 has exactly 6 text fields + 1 checkbox (0.25 pts) ─
    try:
        p2_text_fields = [w for w in p2_widgets if w.field_type_string == "Text"]
        p2_checkboxes = [w for w in p2_widgets if w.field_type_string == "CheckBox"]
        if len(p2_text_fields) == 6 and len(p2_checkboxes) == 1:
            print(f"PASS: Component 3 — Page 2 has 6 text fields + 1 checkbox (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Expected 6 text fields + 1 checkbox on page 2; "
                  f"found {len(p2_text_fields)} text fields, {len(p2_checkboxes)} checkboxes")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ── Component 4: Page 2 field names correct (0.25 pts) ────────────────────
    try:
        p2_text_names = {w.field_name for w in p2_widgets if w.field_type_string == "Text"}
        p2_checkboxes_all = [w for w in p2_widgets if w.field_type_string == "CheckBox"]
        cb_name_ok = (len(p2_checkboxes_all) == 1 and
                      p2_checkboxes_all[0].field_name == P2_EXPECTED_CHECKBOX)
        if p2_text_names == P2_EXPECTED_TEXT_FIELDS and cb_name_ok:
            print(f"PASS: Component 4 — Page 2 field names correct: "
                  f"text={sorted(p2_text_names)}, checkbox='supervisor_approved' (0.25 pts)")
            total_score += 0.25
        else:
            missing_text = P2_EXPECTED_TEXT_FIELDS - p2_text_names
            extra_text = p2_text_names - P2_EXPECTED_TEXT_FIELDS
            cb_names = [w.field_name for w in p2_checkboxes_all]
            print(f"FAIL: Component 4 — Page 2 field names mismatch. "
                  f"Text missing: {missing_text}, extra: {extra_text}; "
                  f"checkbox names found: {cb_names}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task(FILE_PATH)
