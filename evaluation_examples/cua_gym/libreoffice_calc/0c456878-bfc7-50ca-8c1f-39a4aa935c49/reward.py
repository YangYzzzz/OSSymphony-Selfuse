"""
Reward Script: Jupyter Notebook with matplotlib visualizations
Task ID: vscode_prod_026
Domain: vscode (Jupyter notebook)
Scoring:
  Component 1 (0.15): Notebook exists with exactly 3 code cells
  Component 2 (0.15): Cell 0 imports matplotlib.pyplot and numpy
  Component 3 (0.20): Cell 1 contains sine wave plot code
  Component 4 (0.20): Cell 2 contains bar chart code
  Component 5 (0.15): All 3 cells have been executed (execution_count > 0)
  Component 6 (0.15): Cells 1 and 2 have display_data outputs with image/png
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_prod_026'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load notebook JSON
    try:
        with open(file_path, 'r') as f:
            nb = json.load(f)
    except Exception as e:
        print(f"CRITICAL: Cannot load notebook {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    cells = nb.get('cells', [])

    # Component 1: Notebook has exactly 3 code cells (0.15 points)
    try:
        code_cells = [c for c in cells if c.get('cell_type') == 'code']
        if len(code_cells) == 3:
            print(f"PASS: Component 1 — Found 3 code cells (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected 3 code cells, found {len(code_cells)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # For remaining checks, use code_cells if available
    if len(code_cells) < 3:
        print(f"CRITICAL: Not enough code cells to verify remaining components")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Cell 0 imports matplotlib.pyplot and numpy (0.15 points)
    try:
        cell0_source = ''.join(code_cells[0].get('source', []))
        has_matplotlib = 'import matplotlib.pyplot' in cell0_source or 'from matplotlib' in cell0_source
        has_numpy = 'import numpy' in cell0_source or 'from numpy' in cell0_source

        if has_matplotlib and has_numpy:
            print(f"PASS: Component 2 — Cell 0 imports matplotlib and numpy (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Cell 0 missing imports. matplotlib={has_matplotlib}, numpy={has_numpy}")
            print(f"  Source: {cell0_source[:200]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Cell 1 contains sine wave plot code (0.20 points)
    try:
        cell1_source = ''.join(code_cells[1].get('source', []))
        cell1_lower = cell1_source.lower()
        # Check for sine-related code: np.sin or sin( and plot
        has_sin = 'np.sin' in cell1_source or 'sin(' in cell1_lower or 'numpy.sin' in cell1_source
        has_plot = 'plt.plot' in cell1_source or 'plot(' in cell1_lower
        has_show = 'plt.show' in cell1_source or '.show()' in cell1_source

        if has_sin and has_plot:
            print(f"PASS: Component 3 — Cell 1 has sine wave plot code (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Cell 1 sine wave check: sin={has_sin}, plot={has_plot}")
            print(f"  Source: {cell1_source[:200]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Cell 2 contains bar chart code (0.20 points)
    try:
        cell2_source = ''.join(code_cells[2].get('source', []))
        cell2_lower = cell2_source.lower()
        # Check for bar chart: plt.bar or .bar(
        has_bar = 'plt.bar' in cell2_source or '.bar(' in cell2_lower or 'bar(' in cell2_lower
        has_show_c2 = 'plt.show' in cell2_source or '.show()' in cell2_source

        if has_bar:
            print(f"PASS: Component 4 — Cell 2 has bar chart code (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Cell 2 bar chart check: bar={has_bar}")
            print(f"  Source: {cell2_source[:200]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: All 3 cells have been executed (execution_count > 0) (0.15 points)
    try:
        exec_counts = [code_cells[i].get('execution_count') for i in range(3)]
        all_executed = all(ec is not None and isinstance(ec, int) and ec > 0 for ec in exec_counts)
        if all_executed:
            print(f"PASS: Component 5 — All cells executed: counts={exec_counts} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — Not all cells executed: counts={exec_counts}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Cells 1 and 2 have display_data outputs with image/png (0.15 points)
    try:
        def has_display_output(cell):
            outputs = cell.get('outputs', [])
            for out in outputs:
                if out.get('output_type') == 'display_data':
                    data = out.get('data', {})
                    if 'image/png' in data:
                        return True
            return False

        cell1_has_display = has_display_output(code_cells[1])
        cell2_has_display = has_display_output(code_cells[2])

        if cell1_has_display and cell2_has_display:
            print(f"PASS: Component 6 — Both cells 1 and 2 have display_data with image/png (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 — display_data outputs: cell1={cell1_has_display}, cell2={cell2_has_display}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.ipynb'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
