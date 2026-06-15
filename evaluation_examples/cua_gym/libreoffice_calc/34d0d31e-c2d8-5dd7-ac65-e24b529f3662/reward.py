"""
Reward Script: VSCode Jupyter Notebook Data Analysis Setup
Task ID: vscode_gf5_014
Domain: vscode / libreoffice_calc (mixed)
Scoring:
  Component 1: Virtual environment exists (0.15)
  Component 2: pandas installed in venv (0.15)
  Component 3: matplotlib installed in venv (0.15)
  Component 4: data_analysis.ipynb exists with >= 3 cells (0.15)
  Component 5: Cell 1 imports + CSV loading (0.15)
  Component 6: Cell 2 uses df.head() (0.10)
  Component 7: Cell 3 uses plt.bar() (0.15)
"""

import os
import json

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'python-data')
VENV_DIR = os.path.join(PROJECT_DIR, 'venv')
NOTEBOOK_PATH = os.path.join(PROJECT_DIR, 'data_analysis.ipynb')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Virtual environment exists at ~/projects/python-data/venv (0.15 points)
    try:
        venv_python = os.path.join(VENV_DIR, 'bin', 'python')
        venv_pip = os.path.join(VENV_DIR, 'bin', 'pip')
        if os.path.isdir(VENV_DIR) and os.path.isfile(venv_python) and os.path.isfile(venv_pip):
            print(f"PASS: Component 1 — venv exists with python and pip binaries (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — venv dir exists={os.path.isdir(VENV_DIR)}, python={os.path.isfile(venv_python)}, pip={os.path.isfile(venv_pip)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: pandas installed in the venv (0.15 points)
    try:
        # Check if pandas package directory exists in venv site-packages
        site_packages_candidates = []
        venv_lib = os.path.join(VENV_DIR, 'lib')
        if os.path.isdir(venv_lib):
            for py_dir in os.listdir(venv_lib):
                sp = os.path.join(venv_lib, py_dir, 'site-packages')
                if os.path.isdir(sp):
                    site_packages_candidates.append(sp)

        pandas_found = any(
            os.path.isdir(os.path.join(sp, 'pandas'))
            for sp in site_packages_candidates
        )

        if pandas_found:
            print(f"PASS: Component 2 — pandas is installed in venv (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — pandas not found in venv site-packages")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: matplotlib installed in the venv (0.15 points)
    try:
        matplotlib_found = any(
            os.path.isdir(os.path.join(sp, 'matplotlib'))
            for sp in site_packages_candidates
        )

        if matplotlib_found:
            print(f"PASS: Component 3 — matplotlib is installed in venv (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — matplotlib not found in venv site-packages")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: data_analysis.ipynb exists with at least 3 cells (0.15 points)
    try:
        if not os.path.isfile(NOTEBOOK_PATH):
            print(f"FAIL: Component 4 — data_analysis.ipynb not found at {NOTEBOOK_PATH}")
        else:
            with open(NOTEBOOK_PATH, 'r') as f:
                nb = json.load(f)
            cells = nb.get('cells', [])
            if len(cells) >= 3:
                print(f"PASS: Component 4 — notebook has {len(cells)} cells (>= 3) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — notebook has {len(cells)} cells, expected >= 3")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Load notebook cells for remaining checks
    cells = []
    try:
        if os.path.isfile(NOTEBOOK_PATH):
            with open(NOTEBOOK_PATH, 'r') as f:
                nb = json.load(f)
            cells = nb.get('cells', [])
    except Exception:
        pass

    # Helper: get source text for a cell
    def get_cell_source(cell):
        src = cell.get('source', '')
        if isinstance(src, list):
            return ''.join(src)
        return str(src)

    # Component 5: Cell 1 imports pandas/matplotlib and loads CSV with pd.read_csv (0.15 points)
    try:
        if len(cells) >= 1:
            src = get_cell_source(cells[0]).lower()
            has_pandas_import = 'import pandas' in src
            has_matplotlib_import = 'import matplotlib' in src or 'from matplotlib' in src
            has_read_csv = 'read_csv' in src
            if has_pandas_import and has_matplotlib_import and has_read_csv:
                print(f"PASS: Component 5 — Cell 1 imports pandas, matplotlib and loads CSV (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — Cell 1: pandas_import={has_pandas_import}, matplotlib_import={has_matplotlib_import}, read_csv={has_read_csv}")
        else:
            print(f"FAIL: Component 5 — no cells found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Cell 2 uses df.head() to show first 5 rows (0.10 points)
    try:
        if len(cells) >= 2:
            src = get_cell_source(cells[1]).lower()
            # Look for .head() call anywhere in the cell
            if '.head()' in src or '.head(5)' in src:
                print(f"PASS: Component 6 — Cell 2 uses .head() (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 — Cell 2 does not contain .head() call. Source: {src[:100]}")
        else:
            print(f"FAIL: Component 6 — fewer than 2 cells")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: Cell 3 uses plt.bar() for bar chart of monthly sales (0.15 points)
    try:
        if len(cells) >= 3:
            src = get_cell_source(cells[2]).lower()
            # Check for bar chart call
            has_bar = 'plt.bar(' in src or '.bar(' in src
            if has_bar:
                print(f"PASS: Component 7 — Cell 3 uses bar chart (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 7 — Cell 3 does not contain plt.bar() or .bar(). Source: {src[:100]}")
        else:
            print(f"FAIL: Component 7 — fewer than 3 cells")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
