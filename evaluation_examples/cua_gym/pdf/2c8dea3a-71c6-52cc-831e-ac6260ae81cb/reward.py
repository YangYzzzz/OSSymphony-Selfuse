"""
Reward Script: Add digital signature field placeholder to agreement PDF
Task ID: pdf_gf1_043
Domain: pdf
Scoring:
  Component 1 (0.3): agreement_signable.pdf exists, is valid PDF, has 2 pages
  Component 2 (0.3): Page 0 has a Signature widget named 'Signature1'
  Component 3 (0.4): Widget bounding rect matches ~(350, 100, 550, 150) within tolerance
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_043'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must be a valid PDF
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid PDF with 2 pages (0.3 points)
    # This checks that the output file is structurally correct and preserves page count.
    # Fails on initial_env because agreement_signable.pdf does not exist there.
    try:
        page_count = doc.page_count
        if page_count == 2:
            print(f"PASS: Component 1 — agreement_signable.pdf has 2 pages (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — expected 2 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Page 0 has a Signature widget named 'Signature1' (0.3 points)
    # Fails on initial_env because there are no signature fields in agreement.pdf.
    try:
        page = doc[0]
        sig_widgets = []
        for widget in page.widgets():
            if widget.field_type_string == "Signature":
                sig_widgets.append(widget)

        found_sig1 = any(w.field_name == "Signature1" for w in sig_widgets)

        if found_sig1:
            print(f"PASS: Component 2 — Signature widget 'Signature1' found on page 0 (0.3 pts)")
            total_score += 0.3
        else:
            sig_names = [w.field_name for w in sig_widgets]
            print(f"FAIL: Component 2 — No Signature widget named 'Signature1' on page 0. "
                  f"Found signature widgets: {sig_names}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Widget rect matches approximately (350, 100, 550, 150) (0.4 points)
    # Uses tolerance of 5 points for each coordinate.
    # Fails on initial_env because there is no such widget.
    try:
        page = doc[0]
        expected_rect = (350.0, 100.0, 550.0, 150.0)
        tolerance = 5.0  # points

        actual_rect = None
        for widget in page.widgets():
            if widget.field_name == "Signature1" and widget.field_type_string == "Signature":
                actual_rect = tuple(widget.rect)
                break

        rect_ok = (actual_rect is not None and
                   all(abs(actual_rect[i] - expected_rect[i]) <= tolerance for i in range(4)))

        if rect_ok:
            print(f"PASS: Component 3 — Widget rect {actual_rect} matches expected "
                  f"{expected_rect} within tolerance {tolerance} (0.4 pts)")
            total_score += 0.4
        else:
            if actual_rect is not None:
                print(f"FAIL: Component 3 — Widget rect {actual_rect} does not match "
                      f"expected {expected_rect} (tolerance={tolerance})")
            else:
                print(f"FAIL: Component 3 — Signature1 widget not found, cannot check rect")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/agreement_signable.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
