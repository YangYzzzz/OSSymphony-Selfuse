"""
Reward Script: Add custom formula validation to D2:D100 using =AND(D2>=C2, D2<=C2*2)
Task ID: calc_dop_validate_formula_067
Domain: libreoffice_calc
Scoring:
  - Component 1: Data validation exists on D2:D100 (0.30 pts)
  - Component 2: Validation type is 'custom' with correct formula (0.35 pts)
  - Component 3: Error style is 'stop' with correct title and message (0.35 pts)
Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_dop_validate_formula_067'


def normalize_formula(f):
    """Normalize formula for comparison: uppercase, remove spaces."""
    if not f:
        return ''
    return f.upper().replace(' ', '')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: Sheet 'ProjectHours' must exist
    if 'ProjectHours' not in wb.sheetnames:
        print("CRITICAL: Sheet 'ProjectHours' not found.")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['ProjectHours']

    # Retrieve all data validations from the sheet
    try:
        dvs = ws.data_validations.dataValidation
    except Exception as e:
        print(f"ERROR: Cannot read data validations: {e}")
        dvs = []

    # Component 1: Data validation exists on D2:D100 (0.30 points)
    # This check FAILS on initial (0 validations) and PASSES on golden (1 validation on D2:D100)
    target_dv = None
    try:
        for dv in dvs:
            sqref_str = str(dv.sqref)
            # Check that the validation covers D2:D100 (exact or contains D2:D100)
            if 'D2:D100' in sqref_str.upper():
                target_dv = dv
                break

        if target_dv is not None:
            print(f"PASS: Component 1 — Data validation found on D2:D100 (sqref: {target_dv.sqref}) (0.30 pts)")
            total_score += 0.30
        else:
            found_ranges = [str(dv.sqref) for dv in dvs] if dvs else []
            print(f"FAIL: Component 1 — No data validation found on D2:D100. Found validations: {found_ranges}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Validation type is 'custom' with correct formula (0.35 points)
    # Expected formula: =AND(D2>=C2,D2<=C2*2)
    # This check FAILS on initial (no validation) and PASSES on golden (correct custom formula)
    if target_dv is not None:
        try:
            EXPECTED_FORMULA_NORMALIZED = normalize_formula('=AND(D2>=C2,D2<=C2*2)')
            actual_type = target_dv.type
            actual_formula = target_dv.formula1

            formula_normalized = normalize_formula(actual_formula)

            # Accept both with and without leading '='
            # The formula1 in openpyxl is typically stored without leading '='
            # but may appear with it depending on how it was added
            formula_match = (
                formula_normalized == EXPECTED_FORMULA_NORMALIZED or
                formula_normalized == normalize_formula('AND(D2>=C2,D2<=C2*2)')
            )
            type_match = (actual_type == 'custom')

            if type_match and formula_match:
                print(f"PASS: Component 2 — type='custom', formula='{actual_formula}' matches expected (0.35 pts)")
                total_score += 0.35
            elif type_match and not formula_match:
                print(f"FAIL: Component 2 — type='custom' OK, but formula '{actual_formula}' does not match "
                      f"expected '=AND(D2>=C2,D2<=C2*2)'")
            elif not type_match and formula_match:
                print(f"FAIL: Component 2 — formula OK, but type='{actual_type}' (expected 'custom')")
            else:
                print(f"FAIL: Component 2 — type='{actual_type}', formula='{actual_formula}' "
                      f"(expected type='custom', formula='=AND(D2>=C2,D2<=C2*2)')")
        except Exception as e:
            print(f"ERROR: Component 2 — {e}")
    else:
        print("SKIP: Component 2 — no validation found on D2:D100")

    # Component 3: Error style is 'stop', errorTitle is 'Hours Out of Range',
    # error message is 'Actual hours must be between Planned Hours and twice Planned Hours' (0.35 points)
    # This check FAILS on initial (no validation) and PASSES on golden (correct error config)
    if target_dv is not None:
        try:
            actual_style = target_dv.errorStyle
            actual_title = target_dv.errorTitle
            actual_error = target_dv.error
            actual_show_error = target_dv.showErrorMessage

            EXPECTED_STYLE = 'stop'
            EXPECTED_TITLE = 'Hours Out of Range'
            EXPECTED_ERROR = 'Actual hours must be between Planned Hours and twice Planned Hours'

            style_ok = (actual_style == EXPECTED_STYLE)
            title_ok = (actual_title == EXPECTED_TITLE)
            error_ok = (actual_error == EXPECTED_ERROR)
            show_ok = (actual_show_error is True or actual_show_error is None or actual_show_error)

            if style_ok and title_ok and error_ok:
                print(f"PASS: Component 3 — errorStyle='stop', errorTitle='{actual_title}', "
                      f"error='{actual_error}' (0.35 pts)")
                total_score += 0.35
            else:
                issues = []
                if not style_ok:
                    issues.append(f"errorStyle='{actual_style}' (expected 'stop')")
                if not title_ok:
                    issues.append(f"errorTitle='{actual_title}' (expected '{EXPECTED_TITLE}')")
                if not error_ok:
                    issues.append(f"error='{actual_error}' (expected '{EXPECTED_ERROR}')")
                print(f"FAIL: Component 3 — " + "; ".join(issues))
        except Exception as e:
            print(f"ERROR: Component 3 — {e}")
    else:
        print("SKIP: Component 3 — no validation found on D2:D100")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
