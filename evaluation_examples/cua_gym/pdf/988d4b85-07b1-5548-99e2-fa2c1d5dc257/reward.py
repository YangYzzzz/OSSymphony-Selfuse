"""
Reward Script: Extract all tables from a PDF and save as CSV files
Task ID: pdf_res_070
Domain: pdf
Scoring:
  Component 1 (0.3): 5 CSV files named table_1.csv..table_5.csv exist in tables/
  Component 2 (0.3): Each CSV has >= 2 columns and >= 3 data rows (valid structure)
  Component 3 (0.4): Content quality - each CSV contains expected column headers
"""

import os
import csv

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_070'
TABLES_DIR = os.path.join(WORKDIR, 'papers', 'tables')
EXPECTED_COUNT = 5

# Expected first-row headers (partial match) for each table in order
# These are derived from the task description: 5 tables from a data paper
EXPECTED_HEADERS = {
    'table_1.csv': ['Country', 'Population', 'GDP'],
    'table_2.csv': ['Variable', 'Mean', 'Std'],
    'table_3.csv': ['Model', 'Accuracy', 'Precision'],
    'table_4.csv': ['Region', 'Sample', 'Prevalence'],
    'table_5.csv': ['Parameter', 'Estimate', 'Std'],
}


def read_csv_safe(filepath):
    """Read a CSV file and return rows as list of lists."""
    try:
        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = [row for row in reader if any(cell.strip() for cell in row)]
        return rows
    except Exception as e:
        print(f"  WARN: Could not read {filepath}: {e}")
        return []


def verify_task():
    """Verify task completion with progressive scoring. Returns float 0.0-1.0."""
    total_score = 0.0

    # Precondition gate: tables directory must exist
    if not os.path.isdir(TABLES_DIR):
        print(f"FAIL: Directory {TABLES_DIR} does not exist")
        print("REWARD: 0.0")
        return 0.0

    # --- Component 1: 5 CSV files with correct naming (0.3 points) ---
    try:
        expected_files = [f'table_{i}.csv' for i in range(1, EXPECTED_COUNT + 1)]
        found_files = []
        for fname in expected_files:
            fpath = os.path.join(TABLES_DIR, fname)
            if os.path.isfile(fpath):
                found_files.append(fname)

        file_ratio = len(found_files) / EXPECTED_COUNT
        comp1_score = 0.3 * file_ratio
        if comp1_score > 0:
            total_score += comp1_score

        if len(found_files) == EXPECTED_COUNT:
            print(f"PASS: Component 1 — All {EXPECTED_COUNT} CSV files found ({comp1_score:.2f} pts)")
        else:
            print(f"PARTIAL: Component 1 — {len(found_files)}/{EXPECTED_COUNT} CSV files found: {found_files} ({comp1_score:.2f} pts)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --- Component 2: Each CSV has >= 2 columns and >= 3 data rows (0.3 points) ---
    try:
        valid_structure_count = 0
        for fname in found_files:
            fpath = os.path.join(TABLES_DIR, fname)
            rows = read_csv_safe(fpath)
            if len(rows) < 4:  # 1 header + 3 data rows minimum
                print(f"  FAIL: {fname} has {len(rows)} rows (need >= 4 including header)")
                continue
            # Check that at least the header row has >= 2 columns
            if len(rows[0]) < 2:
                print(f"  FAIL: {fname} header has {len(rows[0])} columns (need >= 2)")
                continue
            # Check data rows have >= 2 columns
            data_rows_ok = sum(1 for r in rows[1:] if len(r) >= 2)
            if data_rows_ok < 3:
                print(f"  FAIL: {fname} has only {data_rows_ok} data rows with >= 2 cols (need >= 3)")
                continue
            valid_structure_count += 1

        if len(found_files) > 0:
            struct_ratio = valid_structure_count / EXPECTED_COUNT
        else:
            struct_ratio = 0.0
        comp2_score = 0.3 * struct_ratio
        if comp2_score > 0:
            total_score += comp2_score

        if valid_structure_count == EXPECTED_COUNT:
            print(f"PASS: Component 2 — All {EXPECTED_COUNT} CSVs have valid structure ({comp2_score:.2f} pts)")
        else:
            print(f"PARTIAL: Component 2 — {valid_structure_count}/{EXPECTED_COUNT} CSVs with valid structure ({comp2_score:.2f} pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --- Component 3: Content quality - expected headers present (0.4 points) ---
    try:
        content_match_count = 0
        for fname, expected_hdrs in EXPECTED_HEADERS.items():
            fpath = os.path.join(TABLES_DIR, fname)
            if not os.path.isfile(fpath):
                print(f"  SKIP: {fname} not found for content check")
                continue
            rows = read_csv_safe(fpath)
            if len(rows) < 1:
                print(f"  FAIL: {fname} is empty, cannot check headers")
                continue

            # Check if expected header keywords appear in the first row
            header_str = ','.join(rows[0]).lower()
            matches = sum(1 for h in expected_hdrs if h.lower() in header_str)
            if matches >= len(expected_hdrs):
                content_match_count += 1
                print(f"  PASS: {fname} headers match ({matches}/{len(expected_hdrs)} keywords)")
            else:
                print(f"  FAIL: {fname} headers partial match ({matches}/{len(expected_hdrs)} keywords). Header: {rows[0]}")

        content_ratio = content_match_count / EXPECTED_COUNT
        comp3_score = 0.4 * content_ratio
        if comp3_score > 0:
            total_score += comp3_score

        if content_match_count == EXPECTED_COUNT:
            print(f"PASS: Component 3 — All {EXPECTED_COUNT} CSVs have correct headers ({comp3_score:.2f} pts)")
        else:
            print(f"PARTIAL: Component 3 — {content_match_count}/{EXPECTED_COUNT} CSVs with correct headers ({comp3_score:.2f} pts)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
