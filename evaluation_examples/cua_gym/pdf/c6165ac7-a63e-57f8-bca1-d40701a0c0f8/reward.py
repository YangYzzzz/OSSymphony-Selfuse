"""
Reward Script: Add digital signature fields to retainer agreement PDF
Task ID: pdf_legal_020
Domain: pdf
Scoring:
  - Component 1: ClientSignature field exists on page 3 as Signature type (0.25)
  - Component 2: AttorneySignature field exists on page 3 as Signature type (0.25)
  - Component 3: ClientSignature at correct position (72, 600, 300, 650) (0.2)
  - Component 4: AttorneySignature at correct position (350, 600, 550, 650) (0.2)
  - Component 5: Exactly 2 signature fields on page 3 (0.1)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_020'
OUTPUT_FILE = os.path.join(WORKDIR, 'legal', 'retainer_agreement_sigfields.pdf')

# Tolerance for position comparison (in points)
POS_TOLERANCE = 5.0


def rect_close(actual, expected, tol=POS_TOLERANCE):
    """Check if two rectangles are close within tolerance."""
    if len(actual) != 4 or len(expected) != 4:
        return False
    return all(abs(a - e) <= tol for a, e in zip(actual, expected))


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: Output file must exist and be a valid PDF
    if not os.path.exists(OUTPUT_FILE):
        print(f"CRITICAL: Output file not found: {OUTPUT_FILE}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(OUTPUT_FILE)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {OUTPUT_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(doc) < 3:
        print(f"CRITICAL: PDF has only {len(doc)} pages, expected at least 3")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Get all widgets on page 3 (0-indexed page 2)
    page3 = doc[2]
    widgets = []
    try:
        for w in page3.widgets():
            widgets.append({
                "name": w.field_name,
                "type_str": w.field_type_string,
                "rect": tuple(w.rect),
            })
    except Exception as e:
        print(f"ERROR: Could not enumerate widgets on page 3: {e}")

    print(f"INFO: Found {len(widgets)} widget(s) on page 3:")
    for w in widgets:
        print(f"  name={w['name']}, type={w['type_str']}, rect={w['rect']}")

    # Build lookup by name
    widget_by_name = {w["name"]: w for w in widgets}

    # Component 1: ClientSignature field exists on page 3 as Signature type (0.25 points)
    try:
        if "ClientSignature" in widget_by_name:
            cs = widget_by_name["ClientSignature"]
            if cs["type_str"] == "Signature":
                print(f"PASS: Component 1 — ClientSignature exists as Signature type (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 — ClientSignature exists but type is '{cs['type_str']}', expected 'Signature'")
        else:
            print(f"FAIL: Component 1 — ClientSignature field not found on page 3")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: AttorneySignature field exists on page 3 as Signature type (0.25 points)
    try:
        if "AttorneySignature" in widget_by_name:
            ats = widget_by_name["AttorneySignature"]
            if ats["type_str"] == "Signature":
                print(f"PASS: Component 2 — AttorneySignature exists as Signature type (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — AttorneySignature exists but type is '{ats['type_str']}', expected 'Signature'")
        else:
            print(f"FAIL: Component 2 — AttorneySignature field not found on page 3")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: ClientSignature at correct position (72, 600, 300, 650) (0.2 points)
    try:
        if "ClientSignature" in widget_by_name:
            cs_rect = widget_by_name["ClientSignature"]["rect"]
            expected_rect = (72.0, 600.0, 300.0, 650.0)
            if rect_close(cs_rect, expected_rect):
                print(f"PASS: Component 3 — ClientSignature position {cs_rect} matches expected {expected_rect} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — ClientSignature position {cs_rect} does not match expected {expected_rect}")
        else:
            print(f"FAIL: Component 3 — ClientSignature not found, cannot check position")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: AttorneySignature at correct position (350, 600, 550, 650) (0.2 points)
    try:
        if "AttorneySignature" in widget_by_name:
            ats_rect = widget_by_name["AttorneySignature"]["rect"]
            expected_rect = (350.0, 600.0, 550.0, 650.0)
            if rect_close(ats_rect, expected_rect):
                print(f"PASS: Component 4 — AttorneySignature position {ats_rect} matches expected {expected_rect} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 — AttorneySignature position {ats_rect} does not match expected {expected_rect}")
        else:
            print(f"FAIL: Component 4 — AttorneySignature not found, cannot check position")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Exactly 2 signature fields on page 3 (0.1 points)
    try:
        sig_widgets = [w for w in widgets if w["type_str"] == "Signature"]
        if len(sig_widgets) == 2:
            print(f"PASS: Component 5 — Exactly 2 signature fields on page 3 (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 5 — Found {len(sig_widgets)} signature fields on page 3, expected 2")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
