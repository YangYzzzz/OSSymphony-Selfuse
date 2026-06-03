"""
Reward Script: Extract table from PDF page 4 and save as CSV
Task ID: pdf_ro_019
Domain: pdf (libreoffice_calc domain label, but actual task is PDF extraction to CSV)
Scoring:
  Component 1: CSV file exists and is readable with correct header (0.2 pts)
  Component 2: Correct number of data rows — 8 rows (0.2 pts)
  Component 3: Department names match expected values (0.3 pts)
  Component 4: Numeric values (Q1-Q4) are correct (0.3 pts)
"""

import os
import csv

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_019'
CSV_PATH = os.path.join(WORKDIR, 'finance', 'budget_table.csv')

# Expected ground truth from the task context
EXPECTED_HEADER = ['Department', 'Q1', 'Q2', 'Q3', 'Q4']
EXPECTED_DEPARTMENTS = [
    'Engineering',
    'Marketing',
    'Sales',
    'Human Resources',
    'Operations',
    'Finance',
    'Research & Development',
    'Customer Support',
]
EXPECTED_DATA = {
    'Engineering': [185000, 192000, 198500, 205000],
    'Marketing': [95000, 102000, 98000, 110000],
    'Sales': [120000, 135000, 128000, 142000],
    'Human Resources': [68000, 70500, 72000, 74000],
    'Operations': [145000, 148000, 152000, 156000],
    'Finance': [82000, 84500, 86000, 88500],
    'Research & Development': [210000, 225000, 238000, 245000],
    'Customer Support': [76000, 78500, 81000, 83000],
}


def verify_task(csv_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: CSV file must exist and be parseable
    if not os.path.exists(csv_path):
        print(f"CRITICAL: CSV file not found at {csv_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(csv_path, 'r', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)
    except Exception as e:
        print(f"CRITICAL: Cannot read CSV file: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(rows) < 1:
        print("CRITICAL: CSV file is empty")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Header row matches expected columns (0.2 points)
    try:
        header = [col.strip() for col in rows[0]]
        if header == EXPECTED_HEADER:
            print(f"PASS: Component 1 — Header matches expected: {header} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected header {EXPECTED_HEADER}, found {header}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Correct number of data rows (0.2 points)
    try:
        data_rows = rows[1:]
        # Filter out empty rows
        data_rows = [r for r in data_rows if any(cell.strip() for cell in r)]
        num_data_rows = len(data_rows)
        if num_data_rows == 8:
            print(f"PASS: Component 2 — Correct number of data rows: {num_data_rows} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — Expected 8 data rows, found {num_data_rows}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Department names match (0.3 points)
    try:
        found_depts = []
        for row in data_rows:
            if len(row) >= 1:
                found_depts.append(row[0].strip())

        matching_depts = 0
        for dept in EXPECTED_DEPARTMENTS:
            if dept in found_depts:
                matching_depts += 1
            else:
                print(f"  MISS: Department '{dept}' not found in CSV")

        dept_ratio = matching_depts / len(EXPECTED_DEPARTMENTS) if EXPECTED_DEPARTMENTS else 0
        dept_score = 0.3 * dept_ratio
        if dept_ratio >= 1.0:
            print(f"PASS: Component 3 — All {matching_depts}/{len(EXPECTED_DEPARTMENTS)} departments found (0.3 pts)")
            total_score += 0.3
        elif dept_ratio > 0:
            print(f"PARTIAL: Component 3 — {matching_depts}/{len(EXPECTED_DEPARTMENTS)} departments found ({dept_score:.2f} pts)")
            total_score += dept_score
        else:
            print(f"FAIL: Component 3 — No expected departments found. Found: {found_depts}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Numeric values correct (0.3 points)
    try:
        correct_values = 0
        total_values = 0
        for row in data_rows:
            if len(row) >= 5:
                dept_name = row[0].strip()
                if dept_name in EXPECTED_DATA:
                    expected_vals = EXPECTED_DATA[dept_name]
                    for i in range(4):
                        total_values += 1
                        try:
                            # Handle potential formatting (commas, dollar signs, etc.)
                            raw_val = row[i + 1].strip().replace(',', '').replace('$', '').replace(' ', '')
                            actual_val = float(raw_val)
                            if abs(actual_val - expected_vals[i]) < 0.01:
                                correct_values += 1
                            else:
                                print(f"  VALUE MISMATCH: {dept_name} col {i+1}: expected {expected_vals[i]}, got {actual_val}")
                        except (ValueError, IndexError) as ve:
                            print(f"  PARSE ERROR: {dept_name} col {i+1}: {ve}")

        if total_values > 0:
            value_ratio = correct_values / total_values
            value_score = 0.3 * value_ratio
            if value_ratio >= 1.0:
                print(f"PASS: Component 4 — All {correct_values}/{total_values} numeric values correct (0.3 pts)")
                total_score += 0.3
            elif value_ratio > 0:
                print(f"PARTIAL: Component 4 — {correct_values}/{total_values} numeric values correct ({value_score:.2f} pts)")
                total_score += value_score
            else:
                print(f"FAIL: Component 4 — No numeric values matched")
        else:
            print(f"FAIL: Component 4 — No numeric values could be checked (no matching departments or insufficient columns)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(CSV_PATH):
    print(f"File not found: {CSV_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(CSV_PATH)
