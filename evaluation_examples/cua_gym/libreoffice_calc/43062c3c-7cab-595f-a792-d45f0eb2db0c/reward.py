"""
Reward Script: Export financial_report.xlsx to CSV, then write Python to compute YoY changes
Task ID: osworld_multi_apps_calc_vscode_011
Domain: multi_apps (libreoffice_calc + vscode)
Scoring:
  - Component 1: financial_report.csv exists on Desktop with correct structure (0.3 pts)
  - Component 2: yoy_changes.txt exists on Desktop with all 5 metrics mentioned (0.4 pts)
  - Component 3: yoy_changes.txt contains correct YoY percentage values (0.3 pts)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_calc_vscode_011'

# Expected metrics and their YoY percentage changes (from golden artifact)
EXPECTED_METRICS = [
    "Revenue",
    "Expenses",
    "Net Profit",
    "Units Sold",
    "Marketing Spend",
]

# Expected YoY values from golden artifact (year 2024 -> 2025)
EXPECTED_YOY = {
    "Revenue": 14.05,
    "Expenses": 11.41,
    "Net Profit": 18.22,
    "Units Sold": 12.46,
    "Marketing Spend": 12.45,
}

CSV_PATH = os.path.join(WORKDIR, 'financial_report.csv')
YOY_PATH = os.path.join(WORKDIR, 'yoy_changes.txt')

EXPECTED_CSV_HEADERS = ["Month", "Revenue", "Expenses", "Net Profit", "Units Sold", "Marketing Spend"]
EXPECTED_CSV_ROW_COUNT = 24  # 12 months for 2024 + 12 months for 2025


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Component 1: financial_report.csv exists with correct structure (0.3 pts) ---
    # This should FAIL on initial_env (no CSV exists) and PASS on golden_env
    try:
        if not os.path.exists(CSV_PATH):
            print(f"FAIL: Component 1 — financial_report.csv not found at {CSV_PATH}")
        else:
            import csv
            with open(CSV_PATH, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)

            if len(rows) < 2:
                print(f"FAIL: Component 1 — CSV has too few rows ({len(rows)}), expected at least 25 (header + 24 data rows)")
            else:
                headers = rows[0]
                # Check that all expected columns are present
                missing_cols = [col for col in EXPECTED_CSV_HEADERS if col not in headers]
                data_rows = [r for r in rows[1:] if any(cell.strip() for cell in r)]

                if missing_cols:
                    print(f"FAIL: Component 1 — CSV missing columns: {missing_cols}. Found: {headers}")
                elif len(data_rows) < EXPECTED_CSV_ROW_COUNT:
                    print(f"FAIL: Component 1 — CSV has {len(data_rows)} data rows, expected {EXPECTED_CSV_ROW_COUNT}")
                else:
                    # Verify that both 2024 and 2025 data are present
                    months_found = [r[0] for r in data_rows if r]
                    has_2024 = any('2024' in m for m in months_found)
                    has_2025 = any('2025' in m for m in months_found)
                    if has_2024 and has_2025:
                        print(f"PASS: Component 1 — financial_report.csv exists with {len(data_rows)} data rows, "
                              f"all required columns present, 2024 and 2025 data found (0.3 pts)")
                        total_score += 0.3
                    else:
                        print(f"FAIL: Component 1 — CSV is missing year data. has_2024={has_2024}, has_2025={has_2025}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --- Component 2: yoy_changes.txt exists with all 5 metrics mentioned (0.4 pts) ---
    # This should FAIL on initial_env (no TXT exists) and PASS on golden_env
    try:
        if not os.path.exists(YOY_PATH):
            print(f"FAIL: Component 2 — yoy_changes.txt not found at {YOY_PATH}")
        else:
            with open(YOY_PATH, 'r', encoding='utf-8') as f:
                yoy_content = f.read()

            found_metrics = []
            missing_metrics = []
            for metric in EXPECTED_METRICS:
                if metric in yoy_content:
                    found_metrics.append(metric)
                else:
                    missing_metrics.append(metric)

            # Also check that YoY percentage change data is present (e.g., "YoY Change:" or "%" symbol)
            has_percentage = '%' in yoy_content
            has_yoy_label = ('YoY' in yoy_content or 'year-over-year' in yoy_content.lower()
                             or 'Year-over-Year' in yoy_content)

            comp2_ok = (not missing_metrics) and has_percentage and has_yoy_label
            if missing_metrics:
                print(f"FAIL: Component 2 — yoy_changes.txt missing metrics: {missing_metrics}")
            elif not has_percentage:
                print(f"FAIL: Component 2 — yoy_changes.txt has all metrics but no percentage values found")
            elif not has_yoy_label:
                print(f"FAIL: Component 2 — yoy_changes.txt missing YoY label/header")
            if comp2_ok:
                print(f"PASS: Component 2 — yoy_changes.txt found with all 5 metrics and YoY percentage data (0.4 pts)")
                total_score += 0.4
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --- Component 3: yoy_changes.txt contains correct YoY percentage values (0.3 pts) ---
    # This verifies that linear interpolation and YoY calculation were done correctly
    # Values are taken from the golden artifact: Revenue+14.05%, Expenses+11.41%, etc.
    # This should FAIL on initial_env (no TXT) and PASS on golden_env
    try:
        if not os.path.exists(YOY_PATH):
            print(f"FAIL: Component 3 — yoy_changes.txt not found at {YOY_PATH}")
        else:
            with open(YOY_PATH, 'r', encoding='utf-8') as f:
                yoy_content = f.read()

            # Extract all numeric values from the file
            # Look for percentage patterns like "+14.05%" or "-12.46%"
            pct_pattern = re.compile(r'([+-]?\d+\.\d+)%')
            pct_values_found = [float(m.group(1)) for m in pct_pattern.finditer(yoy_content)]

            if not pct_values_found:
                print(f"FAIL: Component 3 — No percentage values found in yoy_changes.txt")
            else:
                # Check that expected percentages are present (within tolerance of 0.1%)
                tolerance = 0.1
                matched = []
                unmatched = []

                for metric, expected_pct in EXPECTED_YOY.items():
                    found = any(abs(v - expected_pct) <= tolerance for v in pct_values_found)
                    if found:
                        matched.append(f"{metric}: {expected_pct:+.2f}%")
                    else:
                        unmatched.append(f"{metric}: expected {expected_pct:+.2f}%, found values {pct_values_found}")

                if len(matched) >= 4:  # Allow 4/5 to account for minor rounding differences
                    print(f"PASS: Component 3 — Correct YoY percentages found: {matched} (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — Only {len(matched)}/5 YoY values matched. "
                          f"Matched: {matched}. Unmatched: {unmatched}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: verify on VM
verify_task()
