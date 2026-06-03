"""
Reward Script: Multi-cell Jupyter notebook with CSV loading, summary stats, and bar chart
Task ID: vscode_lp_036
Domain: vscode
Scoring:
  Component 1 (0.20): .ipynb file exists with >= 3 code cells
  Component 2 (0.20): Cell imports pandas+matplotlib and loads data.csv
  Component 3 (0.20): Cell calls describe() for summary statistics
  Component 4 (0.20): Cell creates bar chart of Sales by Product
  Component 5 (0.20): All cells executed with outputs
"""

import os
import json
import glob

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_036'
ANALYSIS_DIR = os.path.join(WORKDIR, 'projects', 'analysis')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Find .ipynb files in the analysis directory
    ipynb_files = glob.glob(os.path.join(ANALYSIS_DIR, '*.ipynb'))
    if not ipynb_files:
        print("CRITICAL: No .ipynb notebook found in ~/projects/analysis/")
        print("REWARD: 0.0")
        return 0.0

    # Use the first notebook found
    nb_path = ipynb_files[0]
    print(f"Found notebook: {nb_path}")

    try:
        with open(nb_path, 'r') as f:
            nb = json.load(f)
    except Exception as e:
        print(f"CRITICAL: Cannot parse notebook {nb_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    cells = nb.get('cells', [])
    code_cells = [c for c in cells if c.get('cell_type') == 'code']

    # Component 1: Notebook has at least 3 code cells (0.2 points)
    try:
        num_code_cells = len(code_cells)
        if num_code_cells >= 3:
            print(f"PASS: Component 1 -- Notebook has {num_code_cells} code cells (>= 3) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- Notebook has {num_code_cells} code cells, need >= 3")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Helper: get source text from a cell
    def cell_source(cell):
        src = cell.get('source', [])
        if isinstance(src, list):
            return ''.join(src)
        return str(src)

    # Component 2: A cell imports pandas and matplotlib AND loads data.csv (0.2 points)
    try:
        found_imports_and_load = False
        for cell in code_cells:
            src = cell_source(cell).lower()
            has_pandas = 'import pandas' in src or 'from pandas' in src
            has_matplotlib = 'import matplotlib' in src or 'from matplotlib' in src
            has_csv_load = 'read_csv' in src and 'data.csv' in src
            if has_pandas and has_matplotlib and has_csv_load:
                found_imports_and_load = True
                break
        if found_imports_and_load:
            print("PASS: Component 2 -- Cell imports pandas+matplotlib and loads data.csv (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 2 -- No cell found with pandas+matplotlib imports AND data.csv loading")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: A cell calls describe() for summary statistics (0.2 points)
    try:
        found_describe = False
        for cell in code_cells:
            src = cell_source(cell)
            if '.describe()' in src or 'describe(' in src:
                found_describe = True
                break
        if found_describe:
            print("PASS: Component 3 -- Cell calls describe() for summary statistics (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 3 -- No cell found with describe() call")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: A cell creates a bar chart of Sales by Product (0.2 points)
    try:
        found_bar_chart = False
        for cell in code_cells:
            src = cell_source(cell).lower()
            # Check for bar chart creation referencing sales and product
            has_bar = ("kind='bar'" in src or 'kind="bar"' in src or
                       '.bar(' in src or "bar(" in src)
            has_sales = 'sales' in src
            has_product = 'product' in src
            if has_bar and has_sales and has_product:
                found_bar_chart = True
                break
        if found_bar_chart:
            print("PASS: Component 4 -- Cell creates bar chart of Sales by Product (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 4 -- No cell found creating bar chart with Sales by Product")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: All code cells have been executed (execution_count != None, outputs present) (0.2 points)
    try:
        all_executed = True
        for i, cell in enumerate(code_cells):
            exec_count = cell.get('execution_count')
            outputs = cell.get('outputs', [])
            if exec_count is None or len(outputs) == 0:
                all_executed = False
                print(f"  Cell {i}: exec_count={exec_count}, outputs={len(outputs)} -- NOT executed")
                break
        if all_executed and len(code_cells) >= 3:
            print(f"PASS: Component 5 -- All {len(code_cells)} code cells executed with outputs (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 -- Not all cells executed")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
