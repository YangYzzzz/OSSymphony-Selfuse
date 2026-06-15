"""
Reward Script: Export test_scores.xlsx to CSV and create analysis script that ranks students by GPA
Task ID: osworld_multi_apps_calc_vscode_010
Domain: libreoffice_calc + vscode (multi-app)
Scoring:
  Component 1: test_scores.csv exists on Desktop with correct data (0.30 pts)
  Component 2: ranking.txt exists on Desktop (0.30 pts)
  Component 3: ranking.txt contains correct student names and GPAs in descending order (0.40 pts)
  Total: 1.0
"""

import os
import csv

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_calc_vscode_010'

# Ground truth: expected ranking order and GPA values (computed from task data)
EXPECTED_RANKING = [
    ("Elena Foster", 89.50),
    ("Isabella Torres", 87.08),
    ("Chloe Martin", 87.02),
    ("Grace Chen", 86.38),
    ("Karen Liu", 86.30),
    ("Alice Nguyen", 85.66),
    ("Ben Carter", 81.18),
    ("Liam Scott", 80.18),
    ("James Wright", 77.82),
    ("Henry Patel", 77.26),
    ("David Kim", 76.88),
    ("Frank Lopez", 71.62),
]

# Expected CSV columns (from the task data)
EXPECTED_CSV_SUBJECTS = ["StudentName", "Math", "Science", "English", "History", "Art"]

def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    csv_path = os.path.join(WORKDIR, 'test_scores.csv')
    ranking_path = os.path.join(WORKDIR, 'ranking.txt')

    # Component 1: test_scores.csv exists on Desktop with correct data (0.30 points)
    # This verifies that the agent exported test_scores.xlsx to CSV format.
    # The initial_env does NOT have test_scores.csv, so this is a task-introduced change.
    try:
        if not os.path.exists(csv_path):
            print(f"FAIL: Component 1 — test_scores.csv not found at {csv_path}")
        else:
            with open(csv_path, 'r', newline='') as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                rows = list(reader)

            if fieldnames is None or list(fieldnames) != EXPECTED_CSV_SUBJECTS:
                print(f"FAIL: Component 1 — CSV columns mismatch: expected {EXPECTED_CSV_SUBJECTS}, found {fieldnames}")
            elif len(rows) != 12:
                print(f"FAIL: Component 1 — CSV has {len(rows)} data rows, expected 12")
            else:
                # Check a few spot values to ensure CSV was properly exported from xlsx
                # (not just a hand-crafted file)
                alice_row = next((r for r in rows if r['StudentName'] == 'Alice Nguyen'), None)
                elena_row = next((r for r in rows if r['StudentName'] == 'Elena Foster'), None)
                if alice_row and elena_row:
                    alice_math = alice_row.get('Math', '')
                    elena_math = elena_row.get('Math', '')
                    if alice_math == '92' and elena_math == '95':
                        print(f"PASS: Component 1 — test_scores.csv exists with 12 rows and correct data (0.30 pts)")
                        total_score += 0.30
                    else:
                        print(f"FAIL: Component 1 — CSV data values incorrect (Alice Math={alice_math}, Elena Math={elena_math})")
                else:
                    print(f"FAIL: Component 1 — Expected students not found in CSV")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: ranking.txt exists on Desktop (0.30 points)
    # The initial_env does NOT have ranking.txt, so this is a task-introduced change.
    try:
        if not os.path.exists(ranking_path):
            print(f"FAIL: Component 2 — ranking.txt not found at {ranking_path}")
        elif os.stat(ranking_path).st_size == 0:
            print(f"FAIL: Component 2 — ranking.txt exists but is empty")
        elif os.stat(ranking_path).st_size > 0:
            print(f"PASS: Component 2 — ranking.txt exists and is non-empty (0.30 pts)")
            total_score += 0.30
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: ranking.txt has correct content (0.40 points)
    # Verify all 12 students appear in descending GPA order with correct names and GPA values.
    # GPA tolerance: 0.05 (to allow for minor floating-point rounding differences)
    try:
        if not os.path.exists(ranking_path):
            print(f"FAIL: Component 3 — ranking.txt not found, cannot verify content")
        else:
            with open(ranking_path, 'r') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]

            if len(lines) != 12:
                print(f"FAIL: Component 3 — ranking.txt has {len(lines)} lines, expected 12")
            else:
                # Parse each line: "Name: GPA"
                parsed = []
                parse_errors = []
                for i, line in enumerate(lines):
                    if ': ' not in line:
                        parse_errors.append(f"Line {i+1} malformed: {repr(line)}")
                        continue
                    # Split on last ': ' to handle names with colons
                    parts = line.rsplit(': ', 1)
                    if len(parts) != 2:
                        parse_errors.append(f"Line {i+1} parse error: {repr(line)}")
                        continue
                    name = parts[0].strip()
                    try:
                        gpa = float(parts[1].strip())
                    except ValueError:
                        parse_errors.append(f"Line {i+1} GPA not a number: {repr(parts[1])}")
                        continue
                    parsed.append((name, gpa))

                if parse_errors:
                    print(f"FAIL: Component 3 — Parse errors: {parse_errors}")
                elif len(parsed) != 12:
                    print(f"FAIL: Component 3 — Only {len(parsed)} lines parsed successfully")
                else:
                    # Check all names are present and GPAs are correct
                    name_errors = []
                    gpa_errors = []
                    order_errors = []
                    tolerance = 0.05

                    # Build expected as dict for lookup
                    expected_dict = {name: gpa for name, gpa in EXPECTED_RANKING}

                    for i, (actual_name, actual_gpa) in enumerate(parsed):
                        expected_name, expected_gpa = EXPECTED_RANKING[i]

                        if actual_name != expected_name:
                            # Check if name exists at all in ranking but in wrong position
                            if actual_name in expected_dict:
                                order_errors.append(f"rank {i+1}: got {actual_name}, expected {expected_name}")
                                print(f"FAIL: Component 3 — Wrong order at rank {i+1}: got {actual_name}, expected {expected_name}")
                            else:
                                name_errors.append(f"rank {i+1}: unexpected {actual_name}")
                                print(f"FAIL: Component 3 — Unexpected student at rank {i+1}: {actual_name}")
                        else:
                            # Name matches expected position; check GPA
                            if abs(actual_gpa - expected_gpa) > tolerance:
                                gpa_errors.append(f"{actual_name}: got {actual_gpa:.2f}, expected {expected_gpa:.2f}")
                                print(f"FAIL: Component 3 — GPA mismatch for {actual_name}: got {actual_gpa:.2f}, expected {expected_gpa:.2f}")

                    if not name_errors and not gpa_errors and not order_errors:
                        print(f"PASS: Component 3 — ranking.txt has 12 students in correct descending GPA order with correct values (0.40 pts)")
                        total_score += 0.40
                    else:
                        # No partial credit within this component since correctness is required
                        if name_errors:
                            print(f"FAIL: Component 3 — Student name errors: {name_errors}")
                        if gpa_errors:
                            print(f"FAIL: Component 3 — GPA value errors: {gpa_errors}")
                        if order_errors:
                            print(f"FAIL: Component 3 — Order errors: {order_errors}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_task()
