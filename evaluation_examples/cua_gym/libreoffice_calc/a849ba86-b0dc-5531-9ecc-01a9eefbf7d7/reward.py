"""
Reward Script: Export employees.xlsx to CSV and compute 75th percentile salary
Task ID: osworld_multi_apps_calc_vscode_008
Domain: libreoffice_calc (multi-app: LibreOffice Calc + VSCode)

Task Requirements:
  1. Export employees.xlsx to employees.csv on the Desktop
  2. Write a Python script that fills missing Salary values with department averages,
     computes 75th percentile salary, and saves to p75_salary.txt on Desktop

Scoring Rubric:
  Component 1: employees.csv exists with correct structure (Name, Department, Salary, StartDate;
               20 data rows) — 0.4 points
  Component 2: p75_salary.txt exists and contains the correct 75th percentile value
               (93500.0, within tolerance) — 0.6 points
  Total: 1.0
"""

import os
import csv

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_calc_vscode_008'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: employees.csv exists on Desktop with correct structure (0.4 points)
    # - The task requires exporting employees.xlsx to employees.csv
    # - Correct structure: 4 columns (Name, Department, Salary, StartDate), 20 data rows
    try:
        csv_path = os.path.join(WORKDIR, 'employees.csv')
        if not os.path.exists(csv_path):
            print(f"FAIL: Component 1 — employees.csv not found at {csv_path}")
        else:
            with open(csv_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                fieldnames = reader.fieldnames

            # Check expected columns
            expected_columns = {'Name', 'Department', 'Salary', 'StartDate'}
            if fieldnames is None or not expected_columns.issubset(set(fieldnames)):
                print(f"FAIL: Component 1 — employees.csv missing required columns. "
                      f"Found: {fieldnames}, expected columns: {expected_columns}")
            elif len(rows) != 20:
                print(f"FAIL: Component 1 — employees.csv has {len(rows)} data rows, expected 20")
            else:
                # Verify at least some salary values are present (real export, not empty file)
                salary_values = [r['Salary'] for r in rows if r.get('Salary', '').strip()]
                csv_valid = len(salary_values) >= 15
                if csv_valid:
                    print(f"PASS: Component 1 — employees.csv found with {len(rows)} data rows and "
                          f"correct columns {list(fieldnames)} ({len(salary_values)} salary values present) (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 1 — employees.csv has too few salary values "
                          f"({len(salary_values)} non-empty), expected at least 15 valid entries")

    except Exception as e:
        print(f"ERROR: Component 1 — Could not read employees.csv: {e}")

    # Component 2: p75_salary.txt exists and contains the correct 75th percentile value (0.6 points)
    # - The task requires computing 75th percentile of all employees after filling missing salaries
    #   with department averages, then saving to p75_salary.txt
    # - Expected value: 93500.0 (computed: np.percentile with linear interpolation)
    # - Tolerance: allow values within ±1.0 to account for rounding differences between
    #   implementations (e.g., different interpolation methods)
    try:
        txt_path = os.path.join(WORKDIR, 'p75_salary.txt')
        if not os.path.exists(txt_path):
            print(f"FAIL: Component 2 — p75_salary.txt not found at {txt_path}")
        else:
            with open(txt_path, 'r') as f:
                content = f.read().strip()

            if not content:
                print("FAIL: Component 2 — p75_salary.txt is empty")
            else:
                try:
                    actual_value = float(content)
                    # Expected 75th percentile after filling with dept averages
                    # Engineering avg: 98333.33, Marketing avg: 72333.33, Sales avg: 57666.67,
                    # HR avg: 61666.67, Finance avg: 89250.0
                    # All 20 filled salaries sorted, p75 = 93500.0 (numpy linear interpolation)
                    expected_value = 93500.0
                    tolerance = 1.0  # Allow 1 unit tolerance for rounding differences

                    if abs(actual_value - expected_value) <= tolerance:
                        print(f"PASS: Component 2 — p75_salary.txt contains {actual_value}, "
                              f"matches expected {expected_value} within tolerance ±{tolerance} (0.6 pts)")
                        total_score += 0.6
                    else:
                        print(f"FAIL: Component 2 — p75_salary.txt contains {actual_value}, "
                              f"expected {expected_value} (±{tolerance}). "
                              f"Check: department averages and 75th percentile computation.")
                except ValueError:
                    print(f"FAIL: Component 2 — p75_salary.txt content '{content}' is not a valid number")

    except Exception as e:
        print(f"ERROR: Component 2 — Could not read p75_salary.txt: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
