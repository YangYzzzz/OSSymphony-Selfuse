"""
Reward Script: Jupyter notebook — add DataFrame code cell and execute it
Task ID: vscode_prod_009
Domain: libreoffice_calc (VSCode / Jupyter)
Scoring:
  Component 1 (0.30) — New code cell exists below the original two cells
  Component 2 (0.30) — New cell contains a pd.DataFrame creation statement
  Component 3 (0.20) — New cell has been executed (execution_count is set)
  Component 4 (0.20) — New cell has rendered output containing DataFrame data
"""

import json
import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_prod_009'
NOTEBOOK_PATH = os.path.join(WORKDIR, 'projects', 'data-science', 'analysis.ipynb')


def verify_task(nb_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load notebook
    try:
        with open(nb_path, 'r') as f:
            nb = json.load(f)
    except Exception as e:
        print(f"CRITICAL: Cannot load notebook {nb_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    cells = nb.get('cells', [])

    # The initial notebook has exactly 2 cells (markdown + import code).
    # The task asks the agent to add a NEW code cell below the existing ones.
    # We check for at least 3 cells and inspect the third (index 2+).

    # Component 1: A new code cell exists below the original two cells (0.30 pts)
    try:
        # There must be more than 2 cells, and the new cell(s) must be code type
        new_cells = cells[2:]  # everything after the original 2
        has_new_code_cell = any(c.get('cell_type') == 'code' for c in new_cells)
        if has_new_code_cell:
            print(f"PASS: Component 1 — Found new code cell(s) after original 2 (total cells: {len(cells)}) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — No new code cell found after original 2 cells (total cells: {len(cells)})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Find the first new code cell for components 2-4
    new_code_cell = None
    for c in cells[2:]:
        if c.get('cell_type') == 'code':
            new_code_cell = c
            break

    if new_code_cell is None:
        # No new code cell — remaining components all fail
        print("FAIL: Components 2-4 — No new code cell to inspect")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Get source text of the new cell
    source = new_code_cell.get('source', '')
    if isinstance(source, list):
        source = ''.join(source)

    # Component 2: Cell contains a pd.DataFrame (or DataFrame) creation statement (0.30 pts)
    try:
        # Accept various forms: pd.DataFrame(...), pandas.DataFrame(...), DataFrame(...)
        has_dataframe = bool(re.search(r'DataFrame\s*\(', source))
        if has_dataframe:
            print(f"PASS: Component 2 — Cell source contains DataFrame creation (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — No DataFrame creation found in cell source: {source[:120]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Cell has been executed — execution_count is a positive integer (0.20 pts)
    try:
        exec_count = new_code_cell.get('execution_count')
        if exec_count is not None and isinstance(exec_count, int) and exec_count > 0:
            print(f"PASS: Component 3 — Cell executed with execution_count={exec_count} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — execution_count is {exec_count}, expected a positive integer")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Cell has output containing DataFrame data (0.20 pts)
    try:
        outputs = new_code_cell.get('outputs', [])
        has_df_output = False
        for out in outputs:
            # Check text/html output (rendered DataFrame table) or text/plain
            data = out.get('data', {})
            text_html = data.get('text/html', '')
            text_plain = data.get('text/plain', '')
            if isinstance(text_html, list):
                text_html = ''.join(text_html)
            if isinstance(text_plain, list):
                text_plain = ''.join(text_plain)
            # A rendered DataFrame produces an HTML <table> or a text table
            if '<table' in text_html or 'DataFrame' in text_plain or re.search(r'\w+\s+\w+', text_plain):
                has_df_output = True
                break
            # Also check stdout stream output
            text_stream = out.get('text', '')
            if isinstance(text_stream, list):
                text_stream = ''.join(text_stream)
            if 'DataFrame' in text_stream or '<table' in text_stream:
                has_df_output = True
                break

        if has_df_output:
            print(f"PASS: Component 4 — Cell output contains rendered DataFrame data (0.20 pts)")
            total_score += 0.20
        else:
            output_types = [o.get('output_type', 'unknown') for o in outputs]
            print(f"FAIL: Component 4 — No DataFrame output found. Output types: {output_types}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(NOTEBOOK_PATH):
    print(f"File not found: {NOTEBOOK_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(NOTEBOOK_PATH)
