"""
Reward Script: Flatten all form fields in filled_form.pdf
Task ID: pdf_gf1_022
Domain: pdf
Scoring:
  Component 1 (0.15): Output file exists (task-introduced — file doesn't exist in initial_env)
  Component 2 (0.15): Correct page count (3 pages)
  Component 3 (0.30): No interactive form widgets across all pages
  Component 4 (0.20): No /AcroForm entry in PDF root structure
  Component 5 (0.20): Original field values preserved as static text content
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_022'

# Expected field values that should be preserved as static text
EXPECTED_VALUES = [
    "Alexandra Petrova",
    "a.petrova@meridiantech.com",
    "Cloud Infrastructure Engineering",
    "2025-04-14",
    "MER-78234",
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists (0.15 points)
    # This is a task-introduced change — file does not exist in initial_env
    if os.path.exists(file_path):
        print(f"PASS: Component 1 — Output file exists (0.15 pts)")
        total_score += 0.15
    else:
        print(f"FAIL: Component 1 — Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load with PyMuPDF for widget and text checks
    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Correct page count — 3 pages (0.15 points)
    try:
        page_count = len(doc)
        if page_count == 3:
            print(f"PASS: Component 2 — Page count is 3 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected 3 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: No interactive form widgets across all pages (0.30 points)
    try:
        total_widgets = 0
        for i, page in enumerate(doc):
            widgets = list(page.widgets())
            total_widgets += len(widgets)
            if len(widgets) > 0:
                print(f"  Page {i}: found {len(widgets)} widgets (should be 0)")
        if total_widgets == 0:
            print(f"PASS: Component 3 — No form widgets found (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — Found {total_widgets} widgets, expected 0")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: No /AcroForm in PDF structure (0.20 points)
    try:
        import pikepdf
        pdf = pikepdf.open(file_path)
        has_acroform = '/AcroForm' in pdf.Root
        if not has_acroform:
            print(f"PASS: Component 4 — No /AcroForm in PDF root (0.20 pts)")
            total_score += 0.20
        else:
            # Even if AcroForm exists, check if it has fields
            acroform = pdf.Root['/AcroForm']
            field_count = 0
            if '/Fields' in acroform:
                field_count = len(acroform['/Fields'])
            if field_count == 0:
                print(f"PASS: Component 4 — /AcroForm exists but has 0 fields (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — /AcroForm has {field_count} fields")
        pdf.close()
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Original field values preserved as static text (0.20 points)
    try:
        all_text = ""
        for page in doc:
            all_text += page.get_text("text")

        found_count = 0
        for val in EXPECTED_VALUES:
            if val in all_text:
                found_count += 1
                print(f"  Found value in text: '{val}'")
            else:
                print(f"  MISSING value in text: '{val}'")

        if found_count == len(EXPECTED_VALUES):
            print(f"PASS: Component 5 — All {found_count}/{len(EXPECTED_VALUES)} field values preserved as static text (0.20 pts)")
            total_score += 0.20
        elif found_count > 0:
            partial = 0.20 * (found_count / len(EXPECTED_VALUES))
            print(f"PARTIAL: Component 5 — {found_count}/{len(EXPECTED_VALUES)} values preserved ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — No field values found as static text")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/filled_form_flat.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
