"""
Reward Script: PDF Table Extractor
Task ID: pdf_gf3_021
Domain: pdf / scripting
Scoring:
  Component 1: extract_tables.py script exists and is valid Python (0.15)
  Component 2: /home/user/reports/tables/ dir created with 8 CSV files (0.25)
  Component 3: CSV files have correct content (headers + data rows) (0.25)
  Component 4: summary.json exists with correct structure and 8 entries (0.20)
  Component 5: Script is runnable (syntax-valid, has main logic) (0.15)
"""

import os
import json
import csv
import ast

WORKDIR = '/home/user'

# Expected CSV files (from golden ground truth)
EXPECTED_CSVS = [
    'table_page2_table1.csv',
    'table_page4_table1.csv',
    'table_page5_table1.csv',
    'table_page7_table1.csv',
    'table_page9_table1.csv',
    'table_page10_table1.csv',
    'table_page12_table1.csv',
    'table_page14_table1.csv',
]

# Expected headers per CSV (from task ground truth)
EXPECTED_HEADERS = {
    'table_page2_table1.csv': ['Quarter', 'Revenue ($M)', 'COGS ($M)', 'Gross Profit ($M)', 'Margin (%)'],
    'table_page4_table1.csv': ['Department', 'Salaries', 'Marketing', 'Travel', 'Software', 'Total'],
    'table_page5_table1.csv': ['Product', 'Units Sold', 'Avg Price', 'Revenue', 'YoY Growth'],
    'table_page7_table1.csv': ['Region', 'Q1', 'Q2', 'Q3', 'Q4', 'Annual Total'],
    'table_page9_table1.csv': ['Division', 'Full-Time', 'Part-Time', 'Contractors', 'Total', 'Budget'],
    'table_page10_table1.csv': ['Category', 'FY2023', 'FY2024', 'Change'],
    'table_page12_table1.csv': ['Channel', 'Leads', 'Conversions', 'Conv. Rate', 'CAC', 'LTV'],
    'table_page14_table1.csv': ['Item', 'Dec 2023', 'Dec 2024', 'Change (%)'],
}

# Expected minimum data rows per CSV (header row excluded)
EXPECTED_MIN_ROWS = {
    'table_page2_table1.csv': 4,
    'table_page4_table1.csv': 5,
    'table_page5_table1.csv': 4,
    'table_page7_table1.csv': 4,
    'table_page9_table1.csv': 4,
    'table_page10_table1.csv': 5,
    'table_page12_table1.csv': 5,
    'table_page14_table1.csv': 5,
}


def verify_task():
    """Verify task completion with progressive scoring. Returns float 0.0-1.0."""
    total_score = 0.0

    script_path = os.path.join(WORKDIR, 'scripts', 'extract_tables.py')
    tables_dir = os.path.join(WORKDIR, 'reports', 'tables')
    summary_path = os.path.join(tables_dir, 'summary.json')

    # ------------------------------------------------------------------
    # Component 1: extract_tables.py exists and is valid Python (0.15 pts)
    # ------------------------------------------------------------------
    try:
        if not os.path.isfile(script_path):
            print(f"FAIL: Component 1 — script not found at {script_path}")
        else:
            with open(script_path, 'r') as f:
                source = f.read()
            # Check it parses as valid Python
            ast.parse(source)
            # Check it references the expected PDF path and output dir
            has_pdf_ref = 'financial_tables.pdf' in source
            has_csv_logic = ('csv' in source.lower() or 'write' in source.lower())
            if has_pdf_ref and has_csv_logic:
                print(f"PASS: Component 1 — extract_tables.py exists, valid Python, references PDF and CSV logic (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — script exists but missing PDF reference or CSV logic (has_pdf_ref={has_pdf_ref}, has_csv_logic={has_csv_logic})")
    except SyntaxError as e:
        print(f"FAIL: Component 1 — script has syntax error: {e}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ------------------------------------------------------------------
    # Component 2: tables/ dir with 8 CSV files correctly named (0.25 pts)
    # ------------------------------------------------------------------
    try:
        if not os.path.isdir(tables_dir):
            print(f"FAIL: Component 2 — tables directory not found at {tables_dir}")
        else:
            csv_files = [f for f in os.listdir(tables_dir) if f.endswith('.csv')]
            found_expected = [f for f in EXPECTED_CSVS if f in csv_files]
            match_ratio = len(found_expected) / len(EXPECTED_CSVS)

            if match_ratio >= 1.0:
                print(f"PASS: Component 2 — all 8 expected CSV files found in tables/ (0.25 pts)")
                total_score += 0.25
            elif match_ratio >= 0.5:
                partial = round(0.25 * match_ratio, 3)
                print(f"PARTIAL: Component 2 — {len(found_expected)}/8 expected CSVs found ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — only {len(found_expected)}/8 expected CSVs found. Found: {csv_files}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ------------------------------------------------------------------
    # Component 3: CSV content is correct (headers + data rows) (0.25 pts)
    # ------------------------------------------------------------------
    try:
        csv_content_score = 0.0
        per_csv_weight = 0.25 / len(EXPECTED_CSVS)  # ~0.03125 each
        csv_checks_done = 0

        for csv_name in EXPECTED_CSVS:
            csv_path = os.path.join(tables_dir, csv_name)
            if not os.path.isfile(csv_path):
                print(f"FAIL: Component 3 [{csv_name}] — file not found")
                continue

            with open(csv_path, 'r', newline='') as f:
                reader = csv.reader(f)
                rows = list(reader)

            if len(rows) < 2:
                print(f"FAIL: Component 3 [{csv_name}] — too few rows ({len(rows)})")
                continue

            # Check headers match expected
            actual_headers = [h.strip() for h in rows[0]]
            expected_hdrs = EXPECTED_HEADERS.get(csv_name, [])
            headers_match = (actual_headers == expected_hdrs)

            # Check minimum data rows
            min_rows = EXPECTED_MIN_ROWS.get(csv_name, 2)
            data_rows = len(rows) - 1  # exclude header
            enough_rows = data_rows >= min_rows

            # Check columns are consistent
            expected_cols = len(expected_hdrs) if expected_hdrs else len(rows[0])
            cols_consistent = all(len(r) == expected_cols for r in rows)

            if headers_match and enough_rows and cols_consistent:
                csv_content_score += per_csv_weight
                print(f"PASS: Component 3 [{csv_name}] — headers match, {data_rows} data rows, cols consistent ({round(per_csv_weight, 4)} pts)")
                csv_checks_done += 1
            else:
                print(f"FAIL: Component 3 [{csv_name}] — headers_match={headers_match}, enough_rows={enough_rows} ({data_rows}>={min_rows}), cols_consistent={cols_consistent}")
                if not headers_match:
                    print(f"  Expected headers: {expected_hdrs}")
                    print(f"  Actual headers:   {actual_headers}")

        if csv_content_score > 0:
            total_score += round(csv_content_score, 4)
        print(f"Component 3 total: {csv_checks_done}/{len(EXPECTED_CSVS)} CSVs valid ({round(csv_content_score, 4)} pts)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ------------------------------------------------------------------
    # Component 4: summary.json with correct structure (0.20 pts)
    # ------------------------------------------------------------------
    try:
        if not os.path.isfile(summary_path):
            print(f"FAIL: Component 4 — summary.json not found at {summary_path}")
        else:
            with open(summary_path, 'r') as f:
                summary = json.load(f)

            checks_passed = 0
            total_checks = 4

            # Check total_tables == 8
            if summary.get('total_tables') == 8:
                checks_passed += 1
                print(f"  PASS: Component 4a — total_tables == 8")
            else:
                print(f"  FAIL: Component 4a — total_tables={summary.get('total_tables')}, expected 8")

            # Check tables list has 8 entries
            tables_list = summary.get('tables', [])
            if len(tables_list) == 8:
                checks_passed += 1
                print(f"  PASS: Component 4b — tables list has 8 entries")
            else:
                print(f"  FAIL: Component 4b — tables list has {len(tables_list)} entries, expected 8")

            # Check each table entry has required fields (page, rows, columns, csv_file)
            required_fields = {'page', 'rows', 'columns', 'csv_file'}
            all_have_fields = all(
                required_fields.issubset(set(t.keys())) for t in tables_list
            ) if tables_list else False
            if all_have_fields:
                checks_passed += 1
                print(f"  PASS: Component 4c — all table entries have required fields")
            else:
                missing_examples = []
                for i, t in enumerate(tables_list):
                    missing = required_fields - set(t.keys())
                    if missing:
                        missing_examples.append(f"table {i}: missing {missing}")
                print(f"  FAIL: Component 4c — some entries missing fields: {missing_examples[:3]}")

            # Check table pages match expected pages
            expected_pages = [2, 4, 5, 7, 9, 10, 12, 14]
            actual_pages = sorted([t.get('page', 0) for t in tables_list])
            if actual_pages == expected_pages:
                checks_passed += 1
                print(f"  PASS: Component 4d — table pages match expected {expected_pages}")
            else:
                print(f"  FAIL: Component 4d — pages {actual_pages} != expected {expected_pages}")

            comp4_score = round(0.20 * (checks_passed / total_checks), 4)
            if comp4_score > 0:
                total_score += comp4_score
            print(f"COMPONENT 4: {checks_passed}/{total_checks} checks passed ({comp4_score} pts)")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 4 — summary.json is not valid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ------------------------------------------------------------------
    # Component 5: Script is runnable (contains import+function structure) (0.15 pts)
    # ------------------------------------------------------------------
    try:
        if not os.path.isfile(script_path):
            print(f"FAIL: Component 5 — script not found")
        else:
            with open(script_path, 'r') as f:
                source = f.read()

            checks_passed = 0
            total_checks = 3

            # Has necessary imports (os, json, csv + a PDF library)
            has_os = 'import os' in source
            has_json = 'import json' in source or 'json.' in source
            has_csv_import = 'import csv' in source or 'csv.' in source
            has_pdf_lib = any(lib in source for lib in ['pdfplumber', 'camelot', 'pymupdf', 'fitz', 'tabula'])

            if has_os and has_json and has_pdf_lib:
                checks_passed += 1
                print(f"  PASS: Component 5a — has os, json, and PDF library imports")
            else:
                print(f"  FAIL: Component 5a — missing imports (os={has_os}, json={has_json}, pdf_lib={has_pdf_lib})")

            # Has main execution block
            has_main = '__main__' in source or 'def extract' in source or 'def main' in source
            if has_main:
                checks_passed += 1
                print(f"  PASS: Component 5b — has main/extract function")
            else:
                print(f"  FAIL: Component 5b — no main block or extract function found")

            # Has output directory creation logic
            has_mkdir = 'makedirs' in source or 'mkdir' in source
            if has_mkdir:
                checks_passed += 1
                print(f"  PASS: Component 5c — has directory creation logic")
            else:
                print(f"  FAIL: Component 5c — no makedirs/mkdir found")

            comp5_score = round(0.15 * (checks_passed / total_checks), 4)
            if comp5_score > 0:
                total_score += comp5_score
            print(f"COMPONENT 5: {checks_passed}/{total_checks} checks passed ({comp5_score} pts)")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # ------------------------------------------------------------------
    # Final score
    # ------------------------------------------------------------------
    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
