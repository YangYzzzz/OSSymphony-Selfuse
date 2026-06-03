"""
Reward Script: Extract Python code from ODT and save as analysis_code.py on Desktop
Task ID: osworld_multi_apps_code_to_writer_file_002
Domain: libreoffice_writer / multi_apps
Scoring:
  Component 1: analysis_code.py exists on Desktop (0.3 points)
  Component 2: File contains Python import statements (pandas, numpy, matplotlib) (0.4 points)
  Component 3: File contains key pandas operations (groupby, def functions, print) (0.3 points)
"""

import os
import ast

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_to_writer_file_002'

DESKTOP_PY_FILE = '/home/user/Desktop/analysis_code.py'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.

    The task required:
    1. Extract Python code from data_analysis_notes.odt (in Documents)
    2. Save extracted code as analysis_code.py on the Desktop
    3. Open the file in LibreOffice Writer to verify

    We score based on:
    - Component 1: File exists on Desktop (precondition for all others)
    - Component 2: File contains expected Python imports (pandas, numpy, matplotlib)
    - Component 3: File contains expected pandas operations (groupby, def functions, print statements)

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # -----------------------------------------------------------------------
    # Component 1: analysis_code.py exists on Desktop (0.3 points)
    # FAILS on initial_env (no file), PASSES on golden_env
    # -----------------------------------------------------------------------
    try:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            if file_size > 0:
                print(f"PASS: Component 1 — analysis_code.py exists on Desktop (size: {file_size} bytes) (0.3 pts)")
                total_score += 0.3
            else:
                print("FAIL: Component 1 — analysis_code.py exists but is empty")
        else:
            print(f"FAIL: Component 1 — analysis_code.py not found at {file_path}")
            # If file doesn't exist, all subsequent checks fail
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load file content for subsequent checks
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        lines = content.splitlines()
    except Exception as e:
        print(f"ERROR: Cannot read {file_path}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # -----------------------------------------------------------------------
    # Component 2: File contains Python import statements for key libraries (0.4 points)
    # The extracted code should include: import pandas, import numpy, import matplotlib
    # FAILS on initial_env (no file), PASSES on golden_env
    # -----------------------------------------------------------------------
    try:
        # Check for key import lines
        has_pandas_import = any(
            'import pandas' in line or 'from pandas' in line
            for line in lines
        )
        has_numpy_import = any(
            'import numpy' in line or 'from numpy' in line
            for line in lines
        )
        has_matplotlib_import = any(
            'import matplotlib' in line or 'from matplotlib' in line
            for line in lines
        )

        import_count = sum([has_pandas_import, has_numpy_import, has_matplotlib_import])

        comp2_pass = import_count >= 2
        if comp2_pass:
            comp2_msg = (f"PASS: Component 2 — File contains {import_count}/3 expected import statements "
                         f"(pandas={has_pandas_import}, numpy={has_numpy_import}, "
                         f"matplotlib={has_matplotlib_import}) (0.4 pts)")
        else:
            comp2_msg = (f"FAIL: Component 2 — File contains only {import_count}/3 expected imports "
                         f"(pandas={has_pandas_import}, numpy={has_numpy_import}, "
                         f"matplotlib={has_matplotlib_import}). Expected at least 2.")
        print(comp2_msg)
        if comp2_pass:
            total_score += 0.4
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: File contains key pandas data analysis operations (0.3 points)
    # The extracted code should include: groupby, def functions, print, read_csv
    # FAILS on initial_env (no file), PASSES on golden_env
    # -----------------------------------------------------------------------
    try:
        has_groupby = 'groupby' in content
        has_read_csv = 'read_csv' in content
        has_def = any(line.strip().startswith('def ') for line in lines)
        has_print = any(line.strip().startswith('print(') for line in lines)

        ops_count = sum([has_groupby, has_read_csv, has_def, has_print])

        comp3_pass = ops_count >= 3
        if comp3_pass:
            comp3_msg = (f"PASS: Component 3 — File contains {ops_count}/4 expected pandas operations "
                         f"(groupby={has_groupby}, read_csv={has_read_csv}, "
                         f"def={has_def}, print={has_print}) (0.3 pts)")
        else:
            comp3_msg = (f"FAIL: Component 3 — File contains only {ops_count}/4 expected pandas operations "
                         f"(groupby={has_groupby}, read_csv={has_read_csv}, "
                         f"def={has_def}, print={has_print}). Expected at least 3.")
        print(comp3_msg)
        if comp3_pass:
            total_score += 0.3
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = DESKTOP_PY_FILE
verify_task(file_path)
