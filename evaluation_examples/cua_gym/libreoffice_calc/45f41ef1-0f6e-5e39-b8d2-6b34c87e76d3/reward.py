"""
Reward Script: Split analysis.ipynb into data_cleaning.ipynb and visualization.ipynb,
update imports, and configure a papermill task.
Task ID: vscode_gf1_086
Domain: vscode / notebook refactoring
Scoring:
  Component 1 (0.20): data_cleaning.ipynb exists with 8 cells
  Component 2 (0.20): visualization.ipynb exists with 6 cells
  Component 3 (0.15): data_cleaning first cell has appropriate imports (data-focused, no viz libs)
  Component 4 (0.15): visualization first cell has appropriate imports (viz libs, loads cleaned CSV)
  Component 5 (0.15): tasks.json with papermill pipeline command
  Component 6 (0.15): cell content continuity (cells match original analysis.ipynb)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf1_086'
NOTEBOOKS_DIR = os.path.join(WORKDIR, 'notebooks')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load original analysis.ipynb as reference for cell content checks
    analysis_path = os.path.join(NOTEBOOKS_DIR, 'analysis.ipynb')
    try:
        with open(analysis_path) as f:
            analysis_nb = json.load(f)
        analysis_cells = analysis_nb.get('cells', [])
    except Exception as e:
        print(f"WARNING: Cannot load analysis.ipynb for reference: {e}")
        analysis_cells = []

    # -------------------------------------------------------
    # Component 1: data_cleaning.ipynb exists with 8 cells (0.20 pts)
    # -------------------------------------------------------
    dc_path = os.path.join(NOTEBOOKS_DIR, 'data_cleaning.ipynb')
    dc_nb = None
    try:
        with open(dc_path) as f:
            dc_nb = json.load(f)
        dc_cells = dc_nb.get('cells', [])
        if len(dc_cells) == 8:
            print(f"PASS: Component 1 — data_cleaning.ipynb has 8 cells (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — data_cleaning.ipynb has {len(dc_cells)} cells, expected 8")
    except FileNotFoundError:
        print(f"FAIL: Component 1 — data_cleaning.ipynb not found at {dc_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------
    # Component 2: visualization.ipynb exists with 6 cells (0.20 pts)
    # -------------------------------------------------------
    viz_path = os.path.join(NOTEBOOKS_DIR, 'visualization.ipynb')
    viz_nb = None
    try:
        with open(viz_path) as f:
            viz_nb = json.load(f)
        viz_cells = viz_nb.get('cells', [])
        if len(viz_cells) == 6:
            print(f"PASS: Component 2 — visualization.ipynb has 6 cells (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — visualization.ipynb has {len(viz_cells)} cells, expected 6")
    except FileNotFoundError:
        print(f"FAIL: Component 2 — visualization.ipynb not found at {viz_path}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------
    # Component 3: data_cleaning first cell has appropriate imports (0.15 pts)
    # Must have data-focused imports (pandas, numpy, os) and NOT have
    # matplotlib/seaborn (those belong in visualization). This differs from
    # the original analysis.ipynb cell 0 which had all imports together.
    # -------------------------------------------------------
    try:
        if dc_nb is None:
            raise FileNotFoundError("data_cleaning.ipynb not loaded")
        dc_cells = dc_nb.get('cells', [])
        first_cell_src = ''.join(dc_cells[0].get('source', []))

        has_pandas = 'import pandas' in first_cell_src
        has_numpy = 'import numpy' in first_cell_src
        no_matplotlib = 'matplotlib' not in first_cell_src
        no_seaborn = 'seaborn' not in first_cell_src

        # The original cell 0 had matplotlib and seaborn - those should be removed
        if has_pandas and has_numpy and no_matplotlib and no_seaborn:
            print(f"PASS: Component 3 — data_cleaning imports are data-focused (pandas, numpy, no viz libs) (0.15 pts)")
            total_score += 0.15
        else:
            details = []
            if not has_pandas:
                details.append("missing pandas")
            if not has_numpy:
                details.append("missing numpy")
            if not no_matplotlib:
                details.append("still has matplotlib")
            if not no_seaborn:
                details.append("still has seaborn")
            print(f"FAIL: Component 3 — data_cleaning imports issues: {', '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------
    # Component 4: visualization first cell has appropriate imports (0.15 pts)
    # Must have viz imports (matplotlib, seaborn) and load cleaned CSV data.
    # The original cell 8 (markdown header) didn't have imports, so this is
    # a new cell added by the task.
    # -------------------------------------------------------
    try:
        if viz_nb is None:
            raise FileNotFoundError("visualization.ipynb not loaded")
        viz_cells = viz_nb.get('cells', [])
        first_cell_src = ''.join(viz_cells[0].get('source', []))

        has_matplotlib = 'matplotlib' in first_cell_src
        has_seaborn = 'seaborn' in first_cell_src or 'sns' in first_cell_src
        has_pandas = 'import pandas' in first_cell_src or 'pd' in first_cell_src
        loads_csv = 'read_csv' in first_cell_src or 'cleaned' in first_cell_src.lower()

        checks_passed = sum([has_matplotlib, has_seaborn, has_pandas, loads_csv])
        if checks_passed >= 3:
            print(f"PASS: Component 4 — visualization imports include viz libs and data loading ({checks_passed}/4 sub-checks) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — visualization first cell missing requirements: "
                  f"matplotlib={has_matplotlib}, seaborn={has_seaborn}, pandas={has_pandas}, loads_csv={loads_csv}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -------------------------------------------------------
    # Component 5: tasks.json with papermill pipeline (0.15 pts)
    # Must have a task that runs papermill on both notebooks in sequence.
    # -------------------------------------------------------
    try:
        tasks_json_path = os.path.join(NOTEBOOKS_DIR, '.vscode', 'tasks.json')
        if not os.path.exists(tasks_json_path):
            # Also check workspace root
            tasks_json_path = os.path.join(WORKDIR, '.vscode', 'tasks.json')

        with open(tasks_json_path) as f:
            tasks_config = json.load(f)

        tasks = tasks_config.get('tasks', [])
        papermill_tasks = [t for t in tasks
                           if 'papermill' in t.get('command', '')
                           and 'data_cleaning' in t.get('command', '')
                           and 'visualization' in t.get('command', '')]

        if len(papermill_tasks) > 0:
            print(f"PASS: Component 5 — tasks.json contains papermill pipeline command (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — tasks.json missing papermill pipeline task. "
                  f"Found {len(tasks)} tasks, none matching papermill with both notebooks")
    except FileNotFoundError:
        print(f"FAIL: Component 5 — tasks.json not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # -------------------------------------------------------
    # Component 6: Cell content continuity (0.15 pts)
    # data_cleaning cells 1-7 should match analysis cells 1-7
    # visualization cells 1-5 should match analysis cells 8-13
    # (cell 0 in each is the updated imports cell, so we skip it)
    # -------------------------------------------------------
    try:
        if dc_nb is None or viz_nb is None:
            raise FileNotFoundError("One or both split notebooks not loaded")
        if len(analysis_cells) < 14:
            raise ValueError(f"analysis.ipynb has {len(analysis_cells)} cells, expected 14")

        dc_cells = dc_nb.get('cells', [])
        viz_cells = viz_nb.get('cells', [])

        matches = 0
        total_checks = 0

        # Check data_cleaning cells 1-7 match analysis cells 1-7
        for i in range(1, min(8, len(dc_cells))):
            total_checks += 1
            dc_src = ''.join(dc_cells[i].get('source', []))
            an_src = ''.join(analysis_cells[i].get('source', []))
            if dc_src.strip() == an_src.strip():
                matches += 1

        # Check visualization cells 1-5 match analysis cells 8-13
        # viz[0] = new imports cell, viz[1] = analysis[8], viz[2] = analysis[9], etc.
        for i in range(1, min(6, len(viz_cells))):
            total_checks += 1
            viz_src = ''.join(viz_cells[i].get('source', []))
            an_idx = i + 7  # viz[1]->an[8], viz[2]->an[9], ..., viz[5]->an[12]
            if an_idx < len(analysis_cells):
                an_src = ''.join(analysis_cells[an_idx].get('source', []))
                if viz_src.strip() == an_src.strip():
                    matches += 1

        if total_checks > 0 and matches >= total_checks * 0.8:
            print(f"PASS: Component 6 — cell content continuity verified ({matches}/{total_checks} cells match) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 — cell content mismatch ({matches}/{total_checks} cells match, need 80%)")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
