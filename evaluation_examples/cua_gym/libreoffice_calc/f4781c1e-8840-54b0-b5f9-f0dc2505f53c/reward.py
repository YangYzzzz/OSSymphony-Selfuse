"""
Reward Script: Export sensor_data.xlsx to CSV, fill missing values with mean,
               compute 3-hour rolling averages, and save to rolling_avg.txt.
Task ID: osworld_multi_apps_calc_vscode_009
Domain: multi_apps (libreoffice_calc + vscode)
Scoring:
  Component 1 (0.35): sensor_data.csv exists on Desktop with correct structure and data
  Component 2 (0.35): rolling_avg.txt exists on Desktop with 24 lines (one value per line)
  Component 3 (0.30): rolling_avg.txt values are numerically correct (within tolerance)
"""

import os
import csv

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_calc_vscode_009'

# Expected values derived from task specification:
# - sensor_data.xlsx has 24 hourly readings with some missing
# - Missing values filled with column mean of non-null readings
# - 3-hour rolling average computed over filled data
# - 24 rolling average values expected (one per row)

EXPECTED_CSV_HEADER = ['Timestamp', 'Sensor_ID', 'Reading']
EXPECTED_ROW_COUNT = 24  # 24 hourly readings

# Ground truth rolling averages (computed from task data)
EXPECTED_ROLLING_AVGS = [
    23.400000,
    24.041667,
    23.627778,
    23.527778,
    23.527778,
    24.094444,
    24.794444,
    25.166667,
    25.766667,
    25.594444,
    26.027778,
    26.227778,
    26.800000,
    25.994444,
    25.594444,
    25.227778,
    25.300000,
    24.961111,
    24.561111,
    24.194444,
    23.800000,
    23.994444,
    23.694444,
    23.394444,
]

ROLLING_AVG_TOLERANCE = 0.01  # allow 1% tolerance for floating point rounding


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    csv_path = os.path.join(WORKDIR, 'sensor_data.csv')
    rolling_avg_path = os.path.join(WORKDIR, 'rolling_avg.txt')

    # ----------------------------------------------------------------
    # Component 1: sensor_data.csv exists and has correct structure
    #              (this file does NOT exist on initial_env — only on golden)
    #              (0.35 points)
    # ----------------------------------------------------------------
    try:
        if not os.path.exists(csv_path):
            print(f"FAIL: Component 1 — sensor_data.csv not found at {csv_path}")
        else:
            with open(csv_path, 'r', newline='') as f:
                reader = csv.reader(f)
                rows = list(reader)

            if len(rows) == 0:
                print("FAIL: Component 1 — sensor_data.csv is empty")
            else:
                # Check header
                header = [h.strip() for h in rows[0]]
                # Verify header contains expected columns
                header_ok = (
                    len(header) == 3 and
                    header[0] == 'Timestamp' and
                    header[1] == 'Sensor_ID' and
                    header[2] == 'Reading'
                )
                # Check number of data rows (24 hourly readings)
                data_rows = rows[1:]
                row_count_ok = len(data_rows) == EXPECTED_ROW_COUNT

                if header_ok and row_count_ok:
                    print(f"PASS: Component 1 — sensor_data.csv has correct header and {len(data_rows)} data rows (0.35 pts)")
                    total_score += 0.35
                elif header_ok:
                    print(f"FAIL: Component 1 — header correct but expected {EXPECTED_ROW_COUNT} data rows, found {len(data_rows)}")
                else:
                    print(f"FAIL: Component 1 — incorrect header. Expected {EXPECTED_CSV_HEADER}, found {header}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ----------------------------------------------------------------
    # Component 2: rolling_avg.txt exists with correct number of lines
    #              (this file does NOT exist on initial_env — only on golden)
    #              (0.35 points)
    # ----------------------------------------------------------------
    try:
        if not os.path.exists(rolling_avg_path):
            print(f"FAIL: Component 2 — rolling_avg.txt not found at {rolling_avg_path}")
        else:
            with open(rolling_avg_path, 'r') as f:
                content = f.read()

            # Get non-empty lines
            lines = [line.strip() for line in content.strip().split('\n') if line.strip()]

            if len(lines) == 0:
                print("FAIL: Component 2 — rolling_avg.txt is empty")
            elif len(lines) == EXPECTED_ROW_COUNT:
                # Check all lines are parseable as float
                invalid_lines = []
                for i, line in enumerate(lines):
                    try:
                        float(line)
                    except ValueError:
                        invalid_lines.append(f"line {i+1}: '{line}'")
                if len(invalid_lines) == 0:
                    print(f"PASS: Component 2 — rolling_avg.txt has {len(lines)} numeric lines (0.35 pts)")
                    total_score += 0.35
                else:
                    print(f"FAIL: Component 2 — non-numeric lines: {invalid_lines[:3]}")
            else:
                print(f"FAIL: Component 2 — expected {EXPECTED_ROW_COUNT} lines, found {len(lines)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ----------------------------------------------------------------
    # Component 3: rolling_avg.txt values are numerically correct
    #              (verifies that fill-with-mean and rolling avg logic is correct)
    #              (0.30 points)
    # ----------------------------------------------------------------
    try:
        if not os.path.exists(rolling_avg_path):
            print(f"FAIL: Component 3 — rolling_avg.txt not found, cannot verify values")
        else:
            with open(rolling_avg_path, 'r') as f:
                content = f.read()

            lines = [line.strip() for line in content.strip().split('\n') if line.strip()]

            if len(lines) != EXPECTED_ROW_COUNT:
                print(f"FAIL: Component 3 — wrong number of lines ({len(lines)}), cannot verify values")
            else:
                actual_values = []
                unparseable = []
                for line in lines:
                    try:
                        actual_values.append(float(line))
                    except ValueError:
                        unparseable.append(line)

                if len(unparseable) > 0:
                    print(f"FAIL: Component 3 — could not parse {len(unparseable)} line(s) as floats")
                else:
                    # Compare each value against expected with tolerance
                    mismatches = []
                    for i, (actual, expected) in enumerate(zip(actual_values, EXPECTED_ROLLING_AVGS)):
                        if abs(actual - expected) > ROLLING_AVG_TOLERANCE:
                            mismatches.append(
                                f"Line {i+1}: expected {expected:.6f}, got {actual:.6f}"
                            )

                    if len(mismatches) == 0:
                        print(f"PASS: Component 3 — all {EXPECTED_ROW_COUNT} rolling avg values are correct within tolerance {ROLLING_AVG_TOLERANCE} (0.30 pts)")
                        total_score += 0.30
                    else:
                        print(f"FAIL: Component 3 — {len(mismatches)} value(s) incorrect:")
                        for m in mismatches[:5]:  # show first 5 mismatches
                            print(f"  {m}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
