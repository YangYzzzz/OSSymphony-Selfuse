"""
Reward Script: Extract lines 15-25 into function 'process_data' in analysis.py
Task ID: vscode_stu_079
Domain: vs-code (Python refactoring)
Scoring:
  - Component 1 (0.25): 'process_data' function exists as a top-level def
  - Component 2 (0.30): 'process_data' contains the core processing logic
  - Component 3 (0.25): 'analyze_quarterly_report' calls process_data()
  - Component 4 (0.20): Module imports and runs without errors, functional correctness
"""

import os
import ast
import sys
import importlib.util

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_079'
FILE_PATH = os.path.join(WORKDIR, 'analysis.py')


def verify_task(file_path):
    """
    Verify that lines 15-25 were extracted into a 'process_data' function
    and the original function calls it.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Pre-condition: file must exist and be parseable
    try:
        with open(file_path, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
    except FileNotFoundError:
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0
    except SyntaxError as e:
        print(f"CRITICAL: Syntax error in {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect top-level function definitions
    top_level_funcs = {}
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            top_level_funcs[node.name] = node

    # Component 1: 'process_data' function exists as a top-level def (0.25 points)
    try:
        if 'process_data' in top_level_funcs:
            pd_node = top_level_funcs['process_data']
            # Must have at least one parameter (records)
            num_args = len(pd_node.args.args)
            if num_args >= 1:
                print(f"PASS: Component 1 — 'process_data' function exists with {num_args} parameter(s) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 — 'process_data' exists but has no parameters (expected at least 1)")
        else:
            print(f"FAIL: Component 1 — 'process_data' function not found as a top-level definition")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'process_data' contains core processing logic (0.30 points)
    # The extracted code should contain: filtering by amount > 100, tax calculation, running_total
    try:
        if 'process_data' in top_level_funcs:
            pd_source = ast.get_source_segment(source, top_level_funcs['process_data'])
            if pd_source is None:
                # Fallback: reconstruct from line numbers
                lines = source.splitlines()
                pd_node = top_level_funcs['process_data']
                pd_source = '\n'.join(lines[pd_node.lineno - 1:pd_node.end_lineno])

            checks_passed = 0
            checks_total = 4

            # Check for key logic elements in process_data
            if 'amount' in pd_source and '100' in pd_source:
                checks_passed += 1
                print("  - process_data contains amount > 100 filtering logic")
            else:
                print("  - process_data MISSING amount > 100 filtering logic")

            if 'tax' in pd_source or '0.08' in pd_source:
                checks_passed += 1
                print("  - process_data contains tax calculation")
            else:
                print("  - process_data MISSING tax calculation")

            if 'running_total' in pd_source:
                checks_passed += 1
                print("  - process_data contains running_total accumulation")
            else:
                print("  - process_data MISSING running_total accumulation")

            if 'filtered' in pd_source and ('append' in pd_source or 'filtered' in pd_source):
                checks_passed += 1
                print("  - process_data contains filtered list building")
            else:
                print("  - process_data MISSING filtered list building")

            if checks_passed >= 3:
                score = 0.30
                print(f"PASS: Component 2 — process_data contains core logic ({checks_passed}/{checks_total} checks) (0.30 pts)")
                total_score += score
            elif checks_passed >= 2:
                score = 0.15
                print(f"PARTIAL: Component 2 — process_data has partial logic ({checks_passed}/{checks_total} checks) (0.15 pts)")
                total_score += score
            else:
                print(f"FAIL: Component 2 — process_data missing core logic ({checks_passed}/{checks_total} checks)")
        else:
            print(f"FAIL: Component 2 — 'process_data' function does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'analyze_quarterly_report' calls process_data() (0.25 points)
    try:
        if 'analyze_quarterly_report' in top_level_funcs:
            aqr_node = top_level_funcs['analyze_quarterly_report']
            aqr_source = ast.get_source_segment(source, aqr_node)
            if aqr_source is None:
                lines = source.splitlines()
                aqr_source = '\n'.join(lines[aqr_node.lineno - 1:aqr_node.end_lineno])

            # Check that analyze_quarterly_report calls process_data
            calls_process_data = False
            for node in ast.walk(aqr_node):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id == 'process_data':
                        calls_process_data = True
                        break

            # Also check that the inline processing code is removed
            # The original had the for-loop with tax/net calc directly in analyze_quarterly_report
            has_inline_tax_calc = ('0.08' in aqr_source or 'tax' in aqr_source) and 'for record in' in aqr_source

            if calls_process_data and not has_inline_tax_calc:
                print(f"PASS: Component 3 — analyze_quarterly_report calls process_data() and inline code removed (0.25 pts)")
                total_score += 0.25
            elif calls_process_data:
                print(f"PARTIAL: Component 3 — analyze_quarterly_report calls process_data() but may still have inline code (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — analyze_quarterly_report does not call process_data()")
        else:
            print(f"FAIL: Component 3 — 'analyze_quarterly_report' function not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Module can be imported and is functionally correct (0.20 points)
    try:
        # Try to compile the module (syntax check already passed above)
        # Now try to actually import and check that key functions exist and are callable
        spec = importlib.util.spec_from_file_location("analysis_check", file_path)
        module = importlib.util.module_from_spec(spec)

        # Temporarily suppress any __main__ execution
        old_name = None
        spec.loader.exec_module(module)

        has_load = hasattr(module, 'load_sales_data') and callable(module.load_sales_data)
        has_analyze = hasattr(module, 'analyze_quarterly_report') and callable(module.analyze_quarterly_report)
        has_process = hasattr(module, 'process_data') and callable(module.process_data)
        has_write = hasattr(module, 'write_report') and callable(module.write_report)

        if has_load and has_analyze and has_process and has_write:
            print(f"PASS: Component 4 — Module imports successfully, all 4 functions present and callable (0.20 pts)")
            total_score += 0.20
        elif has_process and has_analyze:
            print(f"PARTIAL: Component 4 — Module imports, process_data and analyze present but other functions missing (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — Module import issues: load={has_load}, analyze={has_analyze}, process={has_process}, write={has_write}")
    except Exception as e:
        print(f"ERROR: Component 4 — Module import failed: {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
