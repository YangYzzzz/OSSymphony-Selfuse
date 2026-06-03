"""
Reward Script: Batch PDF Form Filling
Task ID: pdf_fm_050
Domain: pdf
Scoring:
  Component 1: All 5 filled PDF files exist (0.2 pts)
  Component 2: employee_name fields correctly filled (0.4 pts, 0.08 per file)
  Component 3: employee_id fields correctly filled (0.4 pts, 0.08 per file)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_050'
FORMS_DIR = os.path.join(WORKDIR, 'Documents', 'forms', 'batch_forms')

# Expected data mapping: form_NN_filled.pdf -> (name, id)
EXPECTED = {
    'form_01_filled.pdf': ('Alice Brown', 'EMP001'),
    'form_02_filled.pdf': ('Bob Smith', 'EMP002'),
    'form_03_filled.pdf': ('Carol White', 'EMP003'),
    'form_04_filled.pdf': ('Dan Green', 'EMP004'),
    'form_05_filled.pdf': ('Eve Black', 'EMP005'),
}


def get_field_values(pdf_path):
    """Extract employee_name and employee_id field values from a PDF."""
    doc = pymupdf.open(pdf_path)
    name_val = None
    id_val = None
    for page in doc:
        for widget in page.widgets():
            if widget.field_name == 'employee_name':
                name_val = widget.field_value
            elif widget.field_name == 'employee_id':
                id_val = widget.field_value
    doc.close()
    return name_val, id_val


def verify_task():
    """Verify task completion with progressive scoring."""
    total_score = 0.0

    # Component 1: All 5 filled files exist (0.2 points)
    # Each file that exists earns 0.04 points
    try:
        files_found = 0
        for fname in EXPECTED:
            fpath = os.path.join(FORMS_DIR, fname)
            if os.path.isfile(fpath):
                files_found += 1
                print(f"  Found: {fname}")
            else:
                print(f"  Missing: {fname}")

        if files_found == 5:
            print(f"PASS: Component 1 - All 5 filled files exist (0.2 pts)")
            total_score += 0.2
        elif files_found > 0:
            partial = round(files_found * 0.04, 2)
            print(f"PARTIAL: Component 1 - {files_found}/5 filled files exist ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 - No filled files found")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: employee_name fields correctly filled (0.4 points, 0.08 per file)
    try:
        names_correct = 0
        for fname, (expected_name, _) in EXPECTED.items():
            fpath = os.path.join(FORMS_DIR, fname)
            if not os.path.isfile(fpath):
                print(f"  SKIP name check for {fname} - file missing")
                continue
            actual_name, _ = get_field_values(fpath)
            if actual_name is not None and str(actual_name).strip() == expected_name:
                names_correct += 1
                print(f"  Name OK: {fname} -> '{actual_name}'")
            else:
                print(f"  Name FAIL: {fname} -> expected '{expected_name}', got '{actual_name}'")

        if names_correct > 0:
            name_score = round(names_correct * 0.08, 2)
            if names_correct == 5:
                print(f"PASS: Component 2 - All 5 employee_name fields correct ({name_score} pts)")
            else:
                print(f"PARTIAL: Component 2 - {names_correct}/5 employee_name fields correct ({name_score} pts)")
            total_score += name_score
        else:
            print(f"FAIL: Component 2 - No employee_name fields correct")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: employee_id fields correctly filled (0.4 points, 0.08 per file)
    try:
        ids_correct = 0
        for fname, (_, expected_id) in EXPECTED.items():
            fpath = os.path.join(FORMS_DIR, fname)
            if not os.path.isfile(fpath):
                print(f"  SKIP id check for {fname} - file missing")
                continue
            _, actual_id = get_field_values(fpath)
            if actual_id is not None and str(actual_id).strip() == expected_id:
                ids_correct += 1
                print(f"  ID OK: {fname} -> '{actual_id}'")
            else:
                print(f"  ID FAIL: {fname} -> expected '{expected_id}', got '{actual_id}'")

        if ids_correct > 0:
            id_score = round(ids_correct * 0.08, 2)
            if ids_correct == 5:
                print(f"PASS: Component 3 - All 5 employee_id fields correct ({id_score} pts)")
            else:
                print(f"PARTIAL: Component 3 - {ids_correct}/5 employee_id fields correct ({id_score} pts)")
            total_score += id_score
        else:
            print(f"FAIL: Component 3 - No employee_id fields correct")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
