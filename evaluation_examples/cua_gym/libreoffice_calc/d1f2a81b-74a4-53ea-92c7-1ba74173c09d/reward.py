"""
Reward Script: Export products.xlsx to CSV, fill blank prices with mean,
               compute standard deviation and append stats to stats.txt
Task ID: osworld_multi_apps_calc_vscode_007
Domain: multi_apps (libreoffice_calc + vscode)

Scoring Rubric:
  Component 1: products.csv exists on Desktop with expected columns and data rows  (0.30 pts)
  Component 2: stats.txt contains at least one 'Mean Price' line with correct value (0.35 pts)
  Component 3: stats.txt contains at least one 'Standard Deviation' line with correct value (0.35 pts)
  Total: 1.00

Expected ground-truth values (computed from products.xlsx data):
  - 9 non-blank prices: 12.99, 34.5, 8.75, 22.0, 45.8, 18.25, 67.9, 15.5, 29.99
  - mean  = sum(prices) / 9 = 255.68 / 9 = 28.408888...
  - 3 blank entries filled with mean -> 12 prices total
  - std dev (sample, ddof=1) over the 12 prices = 16.058785...
"""

import os
import csv

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_calc_vscode_007'

DESKTOP = os.path.join(WORKDIR, 'Desktop')
CSV_PATH = os.path.join(DESKTOP, 'products.csv')
STATS_PATH = os.path.join(DESKTOP, 'stats.txt')

# Expected ground-truth values (from golden_env)
EXPECTED_MEAN = 28.408888888888892
EXPECTED_STD  = 16.058785442834395
TOLERANCE     = 0.01   # absolute tolerance for floating-point comparison


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --------------------------------------------------------------------------
    # Component 1: products.csv exists with expected header + data rows (0.30 pts)
    # This fails on initial_env (no products.csv) and passes on golden_env.
    # --------------------------------------------------------------------------
    try:
        if not os.path.exists(CSV_PATH):
            print(f"FAIL: Component 1 — products.csv not found at {CSV_PATH}")
        else:
            with open(CSV_PATH, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            # Verify required columns
            expected_cols = {'Product', 'Category', 'Price', 'Quantity'}
            actual_cols = set(reader.fieldnames) if reader.fieldnames else set()
            # re-open for fieldnames after iteration
            with open(CSV_PATH, newline='', encoding='utf-8') as f2:
                r2 = csv.DictReader(f2)
                fieldnames = set(r2.fieldnames or [])

            if not expected_cols.issubset(fieldnames):
                print(f"FAIL: Component 1 — expected columns {expected_cols}, found {fieldnames}")
            elif len(rows) < 5:
                print(f"FAIL: Component 1 — products.csv has too few rows: {len(rows)}")
            else:
                print(f"PASS: Component 1 — products.csv exists with {len(rows)} data rows and correct columns (0.30 pts)")
                total_score += 0.30
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --------------------------------------------------------------------------
    # Component 2: stats.txt contains correct Mean Price value (0.35 pts)
    # This fails on initial_env (no stats.txt) and passes on golden_env.
    # --------------------------------------------------------------------------
    try:
        if not os.path.exists(STATS_PATH):
            print(f"FAIL: Component 2 — stats.txt not found at {STATS_PATH}")
        else:
            with open(STATS_PATH, 'r', encoding='utf-8') as f:
                content = f.read()

            mean_found = False
            for line in content.splitlines():
                line = line.strip()
                # Accept lines like "Mean Price: 28.408888888888892"
                if line.lower().startswith('mean price'):
                    # Extract the numeric part after the colon
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        try:
                            val = float(parts[1].strip())
                            if abs(val - EXPECTED_MEAN) <= TOLERANCE:
                                mean_found = True
                                break
                            else:
                                print(f"FAIL: Component 2 — Mean Price line found but value {val} "
                                      f"differs from expected {EXPECTED_MEAN} by {abs(val - EXPECTED_MEAN):.6f}")
                        except ValueError:
                            print(f"FAIL: Component 2 — Could not parse mean value from line: {line}")

            if mean_found:
                print(f"PASS: Component 2 — stats.txt contains correct Mean Price "
                      f"({EXPECTED_MEAN}) (0.35 pts)")
                total_score += 0.35
            elif os.path.exists(STATS_PATH):
                # If file exists but no valid mean line found, provide diagnostics
                print(f"FAIL: Component 2 — No correct 'Mean Price' line found in stats.txt")
                print(f"      File contents: {content[:300]!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --------------------------------------------------------------------------
    # Component 3: stats.txt contains correct Standard Deviation value (0.35 pts)
    # This fails on initial_env (no stats.txt) and passes on golden_env.
    # --------------------------------------------------------------------------
    try:
        if not os.path.exists(STATS_PATH):
            print(f"FAIL: Component 3 — stats.txt not found at {STATS_PATH}")
        else:
            with open(STATS_PATH, 'r', encoding='utf-8') as f:
                content = f.read()

            std_found = False
            for line in content.splitlines():
                line = line.strip()
                # Accept lines like "Standard Deviation: 16.058785442834395"
                if line.lower().startswith('standard deviation'):
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        try:
                            val = float(parts[1].strip())
                            if abs(val - EXPECTED_STD) <= TOLERANCE:
                                std_found = True
                                break
                            else:
                                print(f"FAIL: Component 3 — Standard Deviation line found but value {val} "
                                      f"differs from expected {EXPECTED_STD} by {abs(val - EXPECTED_STD):.6f}")
                        except ValueError:
                            print(f"FAIL: Component 3 — Could not parse std value from line: {line}")

            if std_found:
                print(f"PASS: Component 3 — stats.txt contains correct Standard Deviation "
                      f"({EXPECTED_STD}) (0.35 pts)")
                total_score += 0.35
            elif os.path.exists(STATS_PATH):
                print(f"FAIL: Component 3 — No correct 'Standard Deviation' line found in stats.txt")
                print(f"      File contents: {content[:300]!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # --------------------------------------------------------------------------
    # Final score
    # --------------------------------------------------------------------------
    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
