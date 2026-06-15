"""
Reward Script: Inventory analysis script implementation and report generation
Task ID: osworld_multi_apps_code_script_output_007
Domain: libreoffice_calc (multi-app: Python script + LibreOffice Calc .ods)

Task Summary:
  1. Implement three functions in /home/user/scripts/inventory.py:
     - low_stock_items(data, threshold)
     - category_totals(data)
     - reorder_cost(low_stock, unit_price_col)
  2. Run the script and redirect output to /home/user/data/inventory_report.txt
  3. Open inventory.ods, navigate to Sheet2, enter total inventory value in cell A1.

Ground Truth (computed from inventory.csv, 25 items, 4 categories):
  - Total inventory value: 36190.55
  - Low stock items (qty < 10): 7 items
  - Category totals: Electronics=140, Furniture=86, Office=279, Supplies=440
  - Total reorder cost: $87546.97

Scoring Rubric:
  Component 1: inventory_report.txt exists with correct output values (0.35 pts)
  Component 2: inventory.py — all 3 functions properly implemented (AST check) (0.30 pts)
  Component 3: inventory.ods Sheet2 A1 = 36190.55 (total inventory value) (0.35 pts)
  Total: 1.0
"""

import os
import ast

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_script_output_007'

# Ground truth values (computed from inventory.csv)
EXPECTED_TOTAL_VALUE = 36190.55
EXPECTED_LOW_STOCK_COUNT = 7
EXPECTED_REORDER_COST = 87546.97

REPORT_PATH = f'{WORKDIR}/data/inventory_report.txt'
SCRIPT_PATH = f'{WORKDIR}/scripts/inventory.py'
ODS_PATH = f'{WORKDIR}/data/inventory.ods'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # -----------------------------------------------------------------------
    # Component 1: inventory_report.txt exists and contains correct output
    # (0.35 points)
    # This FAILS on initial_env (file does not exist) and PASSES on golden_env.
    # -----------------------------------------------------------------------
    try:
        if not os.path.exists(REPORT_PATH):
            print(f"FAIL: Component 1 — inventory_report.txt not found at {REPORT_PATH}")
        else:
            with open(REPORT_PATH, 'r') as f:
                report_content = f.read()

            checks_passed = 0
            checks_total = 4

            # Check 1a: total inventory value present in report
            if '36190.55' in report_content:
                print("PASS: Component 1a — Total inventory value $36190.55 found in report")
                checks_passed += 1
            else:
                print("FAIL: Component 1a — Expected '36190.55' not found in report")

            # Check 1b: low stock count = 7
            if 'Low stock items (qty < 10): 7' in report_content:
                print("PASS: Component 1b — Low stock count (7) found in report")
                checks_passed += 1
            else:
                print("FAIL: Component 1b — Expected 'Low stock items (qty < 10): 7' not in report")

            # Check 1c: reorder cost present in report
            if '87546.97' in report_content:
                print("PASS: Component 1c — Reorder cost $87546.97 found in report")
                checks_passed += 1
            else:
                print("FAIL: Component 1c — Expected '87546.97' not found in report")

            # Check 1d: category total for Electronics present
            if 'Electronics: 140' in report_content:
                print("PASS: Component 1d — Category totals (Electronics: 140) found in report")
                checks_passed += 1
            else:
                print("FAIL: Component 1d — Expected 'Electronics: 140' not found in report")

            comp1_score = round(0.35 * (checks_passed / checks_total), 4)
            if checks_passed > 0:
                print(f"INFO: Component 1 — {checks_passed}/{checks_total} report checks pass ({comp1_score:.4f} pts)")
                total_score += comp1_score
            else:
                print(f"FAIL: Component 1 — report file exists but 0/{checks_total} key values found")

    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: inventory.py — all three functions properly implemented
    # Uses Python AST to check that each function body contains non-trivial
    # statements beyond just a docstring and `pass`.
    # (0.30 points)
    # This FAILS on initial_env (stubs: only docstring + pass) and PASSES on golden_env.
    # -----------------------------------------------------------------------
    try:
        if not os.path.exists(SCRIPT_PATH):
            print(f"FAIL: Component 2 — Script not found at {SCRIPT_PATH}")
        else:
            with open(SCRIPT_PATH, 'r') as f:
                script_content = f.read()

            tree = ast.parse(script_content)
            funcs_implemented = 0
            target_funcs = ['low_stock_items', 'category_totals', 'reorder_cost']

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name in target_funcs:
                    # Count real statements (skip docstring constant and bare pass)
                    real_stmts = []
                    for stmt in node.body:
                        # Skip docstring (Expr containing a string constant)
                        if (isinstance(stmt, ast.Expr) and
                                isinstance(stmt.value, ast.Constant) and
                                isinstance(stmt.value.value, str)):
                            continue
                        # Skip bare pass
                        if isinstance(stmt, ast.Pass):
                            continue
                        real_stmts.append(stmt)

                    if real_stmts:
                        print(f"PASS: Component 2 — '{node.name}' is implemented ({len(real_stmts)} real statements)")
                        funcs_implemented += 1
                    else:
                        print(f"FAIL: Component 2 — '{node.name}' is a stub (only docstring/pass)")

            # Verify all three target functions exist in the file
            for fname in target_funcs:
                found = any(
                    isinstance(n, ast.FunctionDef) and n.name == fname
                    for n in ast.walk(tree)
                )
                if not found:
                    print(f"FAIL: Component 2 — Function '{fname}' not found in script")

            if funcs_implemented == 3:
                print("PASS: Component 2 — All 3 functions implemented (0.30 pts)")
                total_score += 0.30
            elif funcs_implemented == 2:
                print("INFO: Component 2 — 2/3 functions implemented (0.20 pts)")
                total_score += 0.20
            elif funcs_implemented == 1:
                print("INFO: Component 2 — 1/3 functions implemented (0.10 pts)")
                total_score += 0.10
            else:
                print("FAIL: Component 2 — No functions are implemented (0 pts)")

    except SyntaxError as e:
        print(f"ERROR: Component 2 — Script has syntax errors: {e}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: inventory.ods Sheet2 A1 contains the correct total inventory value
    # (0.35 points)
    # Uses odfpy to read the ODS file directly (no subprocess required).
    # This FAILS on initial_env (Sheet2 is blank/empty) and PASSES on golden_env.
    # -----------------------------------------------------------------------
    try:
        if not os.path.exists(ODS_PATH):
            print(f"FAIL: Component 3 — ODS file not found at {ODS_PATH}")
        else:
            from odf.opendocument import load as load_ods
            from odf.table import Table, TableRow, TableCell
            from odf import text as odf_text

            doc = load_ods(ODS_PATH)
            tables = doc.spreadsheet.getElementsByType(Table)

            if len(tables) < 2:
                print(f"FAIL: Component 3 — ODS has only {len(tables)} sheet(s), expected at least 2")
            else:
                sheet2 = tables[1]
                rows = sheet2.getElementsByType(TableRow)

                if not rows:
                    print(f"FAIL: Component 3 — Sheet2 is empty (no rows); expected A1 = {EXPECTED_TOTAL_VALUE}")
                else:
                    row1 = rows[0]
                    cells = row1.getElementsByType(TableCell)

                    if not cells:
                        print(f"FAIL: Component 3 — Sheet2 row 1 has no cells; expected A1 = {EXPECTED_TOTAL_VALUE}")
                    else:
                        cell_a1 = cells[0]
                        # Read the numeric value attribute (set by LibreOffice for float cells)
                        a1_val_str = cell_a1.getAttribute('value')

                        if a1_val_str is None:
                            # Fallback: read text content
                            text_nodes = cell_a1.getElementsByType(odf_text.P)
                            if text_nodes and text_nodes[0].firstChild:
                                a1_val_str = str(text_nodes[0].firstChild)

                        if a1_val_str is None:
                            print(f"FAIL: Component 3 — Sheet2 A1 is empty/None (expected {EXPECTED_TOTAL_VALUE})")
                        else:
                            try:
                                a1_float = float(a1_val_str)
                                tolerance = 0.02  # allow 2 cents tolerance for floating point
                                if abs(a1_float - EXPECTED_TOTAL_VALUE) <= tolerance:
                                    print(f"PASS: Component 3 — Sheet2 A1 = {a1_float} (expected {EXPECTED_TOTAL_VALUE}) (0.35 pts)")
                                    total_score += 0.35
                                else:
                                    print(f"FAIL: Component 3 — Sheet2 A1 = {a1_float}, expected {EXPECTED_TOTAL_VALUE} "
                                          f"(diff = {abs(a1_float - EXPECTED_TOTAL_VALUE):.4f})")
                            except (ValueError, TypeError):
                                print(f"FAIL: Component 3 — Sheet2 A1 value '{a1_val_str}' is not numeric")

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


if __name__ == '__main__':
    verify_task()
