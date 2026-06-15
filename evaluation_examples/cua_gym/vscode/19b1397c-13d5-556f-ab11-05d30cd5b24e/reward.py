"""
Reward Script: Create a Jupyter notebook with three cells — pip install matplotlib,
generate sample data with numpy, and create a scatter plot. Execute all cells.
Task ID: vscode_py_060
Domain: vs_code
Scoring:
  Component 1 (0.20): Notebook exists, valid, has exactly 3 code cells
  Component 2 (0.15): Cell 0 contains pip install matplotlib command
  Component 3 (0.15): Cell 1 imports numpy and generates data
  Component 4 (0.15): Cell 2 imports matplotlib.pyplot and creates scatter plot
  Component 5 (0.10): Cell 0 has been executed (has output)
  Component 6 (0.10): Cell 1 has been executed (has output)
  Component 7 (0.15): Cell 2 has image/png output (scatter plot rendered inline)
"""

import json
import os
import glob

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_060'


def find_notebook():
    """Find the .ipynb notebook file. Try canonical path first, then search."""
    canonical = os.path.join(WORKDIR, f'{TASK_ID}.ipynb')
    if os.path.exists(canonical):
        return canonical
    # Search for any .ipynb file in /home/user (non-hidden, top-level)
    candidates = glob.glob(os.path.join(WORKDIR, '*.ipynb'))
    if candidates:
        # Return the most recently modified one
        candidates.sort(key=os.path.getmtime, reverse=True)
        return candidates[0]
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Find the notebook
    nb_path = find_notebook()
    if nb_path is None:
        print("CRITICAL: No .ipynb notebook found in /home/user/")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found notebook: {nb_path}")

    # Load notebook
    try:
        with open(nb_path, 'r') as f:
            nb = json.load(f)
    except Exception as e:
        print(f"CRITICAL: Cannot parse notebook as JSON: {e}")
        print("REWARD: 0.0")
        return 0.0

    cells = nb.get('cells', [])
    code_cells = [c for c in cells if c.get('cell_type') == 'code']

    # Component 1: Notebook has exactly 3 code cells (0.20 points)
    try:
        num_code = len(code_cells)
        if num_code >= 3:
            print(f"PASS: Component 1 — Notebook has {num_code} code cells (>= 3) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Expected >= 3 code cells, found {num_code}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if len(code_cells) < 3:
        print("CRITICAL: Not enough code cells to check remaining components")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Helper to get cell source as a single string
    def cell_source(cell):
        src = cell.get('source', [])
        if isinstance(src, list):
            return ''.join(src)
        return str(src)

    # Component 2: Cell 0 contains pip install matplotlib (0.15 points)
    try:
        src0 = cell_source(code_cells[0]).lower()
        if 'pip install' in src0 and 'matplotlib' in src0:
            print(f"PASS: Component 2 — Cell 0 contains pip install matplotlib (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Cell 0 does not contain pip install matplotlib. Source: {repr(src0[:200])}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Cell 1 imports numpy and generates data (0.15 points)
    try:
        src1 = cell_source(code_cells[1]).lower()
        has_numpy = 'import numpy' in src1 or 'from numpy' in src1
        has_data_gen = ('random' in src1 or 'arange' in src1 or 'linspace' in src1
                        or 'array' in src1)
        if has_numpy and has_data_gen:
            print(f"PASS: Component 3 — Cell 1 imports numpy and generates data (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Cell 1: numpy_import={has_numpy}, data_gen={has_data_gen}. Source: {repr(src1[:200])}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Cell 2 imports matplotlib.pyplot and creates scatter plot (0.15 points)
    try:
        src2 = cell_source(code_cells[2]).lower()
        has_matplotlib = 'matplotlib.pyplot' in src2 or 'matplotlib' in src2
        has_scatter = 'scatter' in src2
        if has_matplotlib and has_scatter:
            print(f"PASS: Component 4 — Cell 2 imports matplotlib and creates scatter plot (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Cell 2: matplotlib={has_matplotlib}, scatter={has_scatter}. Source: {repr(src2[:200])}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Cell 0 has been executed — has at least one output (0.10 points)
    try:
        outputs0 = code_cells[0].get('outputs', [])
        if len(outputs0) > 0:
            print(f"PASS: Component 5 — Cell 0 executed, {len(outputs0)} output(s) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — Cell 0 has no outputs (not executed)")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Cell 1 has been executed — has at least one output (0.10 points)
    try:
        outputs1 = code_cells[1].get('outputs', [])
        if len(outputs1) > 0:
            print(f"PASS: Component 6 — Cell 1 executed, {len(outputs1)} output(s) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 — Cell 1 has no outputs (not executed)")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: Cell 2 has image/png output — scatter plot rendered inline (0.15 points)
    try:
        outputs2 = code_cells[2].get('outputs', [])
        image_count = sum(1 for out in outputs2 if 'image/png' in out.get('data', {}))
        if image_count > 0:
            print(f"PASS: Component 7 — Cell 2 has {image_count} image/png output(s) (scatter plot inline) (0.15 pts)")
            total_score += 0.15
        else:
            output_types = [out.get('output_type', 'unknown') for out in outputs2]
            print(f"FAIL: Component 7 — Cell 2 has no image/png output. Output types: {output_types}")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
