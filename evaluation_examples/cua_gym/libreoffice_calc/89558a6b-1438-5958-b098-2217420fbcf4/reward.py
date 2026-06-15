"""
Reward Script: Multi-app terminal + calc task — coordinates.csv generation
Task ID: osworld_multi_apps_terminal_calc_013
Domain: libreoffice_calc (CSV output)
Scoring:
  Component 1: CSV header is exactly 'Lat,Lon,Distance'                  (0.30 pts)
  Component 2: CSV has exactly 12 data rows (all coordinate pairs)        (0.10 pts)
  Component 3: Distance column values are correct (sqrt(lat^2 + lon^2))  (0.40 pts)
  Component 4: Rows are sorted ascending by Distance                      (0.20 pts)
Total: 1.0
"""

import os
import csv
import math

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_terminal_calc_013'
CSV_PATH = os.path.join(WORKDIR, 'coordinates.csv')

TOLERANCE = 1e-3  # numeric tolerance for distance comparison


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Task: Convert latitude.xlsx and longitude.ods to CSV, combine as
          coordinates.csv with Lat, Lon, Distance columns sorted by Distance ascending.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: coordinates.csv must exist
    if not os.path.exists(file_path):
        print(f"GATE FAIL: coordinates.csv not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load CSV
    try:
        with open(file_path, 'r', newline='') as f:
            reader = csv.reader(f)
            all_rows = list(reader)
    except Exception as e:
        print(f"CRITICAL: Cannot read {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(all_rows) < 1:
        print("CRITICAL: CSV is empty")
        print("REWARD: 0.0")
        return 0.0

    header = all_rows[0]
    data_rows = all_rows[1:]

    # Component 1: Correct header (0.30 points)
    # Header must be exactly ['Lat', 'Lon', 'Distance']
    try:
        expected_header = ['Lat', 'Lon', 'Distance']
        if header == expected_header:
            print(f"PASS: Component 1 — Header is correct {header} (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Expected header {expected_header}, found {header}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Correct number of rows (0.10 points)
    # Must have exactly 12 data rows (12 coordinate pairs from the source files)
    try:
        expected_rows = 12
        if len(data_rows) == expected_rows:
            print(f"PASS: Component 2 — Row count is {len(data_rows)} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 — Expected {expected_rows} rows, found {len(data_rows)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Parse numeric rows for components 3 and 4
    parsed_rows = []
    parse_errors = 0
    for i, row in enumerate(data_rows):
        try:
            if len(row) < 3:
                parse_errors += 1
                continue
            lat = float(row[0])
            lon = float(row[1])
            dist = float(row[2])
            parsed_rows.append((lat, lon, dist))
        except (ValueError, IndexError):
            parse_errors += 1

    if parse_errors > 0:
        print(f"WARN: {parse_errors} rows had parse errors and were skipped")

    # Component 3: Distance column values are correct (0.40 points)
    # Each Distance value must equal sqrt(Lat^2 + Lon^2) within tolerance
    try:
        if len(parsed_rows) == 0:
            print("FAIL: Component 3 — No parseable data rows")
        else:
            correct_distances = 0
            for lat, lon, dist in parsed_rows:
                expected_dist = math.sqrt(lat ** 2 + lon ** 2)
                if abs(dist - expected_dist) <= TOLERANCE:
                    correct_distances += 1
                else:
                    print(f"  MISMATCH: Lat={lat}, Lon={lon}, Dist={dist:.6f}, Expected={expected_dist:.6f}")

            partial = 0.40 * (correct_distances / 12)
            if correct_distances == 12:
                print(f"PASS: Component 3 — All {correct_distances} distance values are correct (0.40 pts)")
                total_score += 0.40
            elif correct_distances > 0:
                # Partial: some rows have correct distances
                print(f"PARTIAL: Component 3 — {correct_distances}/12 distances correct ({partial:.2f} pts)")
                if partial > 0:
                    total_score += partial
            else:
                print(f"FAIL: Component 3 — 0/{len(parsed_rows)} distance values correct")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Rows are sorted ascending by Distance (0.20 points)
    # The full CSV must be sorted by Distance from smallest to largest
    try:
        if len(parsed_rows) < 2:
            print("FAIL: Component 4 — Not enough rows to verify sorting")
        else:
            distances = [row[2] for row in parsed_rows]
            is_sorted = all(distances[i] <= distances[i + 1] for i in range(len(distances) - 1))
            if is_sorted:
                print(f"PASS: Component 4 — Rows sorted ascending by Distance (0.20 pts)")
                total_score += 0.20
            else:
                # Find first out-of-order pair
                for i in range(len(distances) - 1):
                    if distances[i] > distances[i + 1]:
                        print(f"FAIL: Component 4 — Sort order violated at row {i+1}: "
                              f"{distances[i]:.6f} > {distances[i+1]:.6f}")
                        break
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(CSV_PATH):
    print(f"File not found: {CSV_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(CSV_PATH)
