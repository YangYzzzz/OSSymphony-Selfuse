"""
Reward Script: Jupyter notebook with IPython magic commands
Task ID: vscode_gf2_032
Domain: vscode
Scoring:
  - Component 1: Notebook exists and is valid ipynb (0.10)
  - Component 2: Contains %matplotlib inline magic cell (0.20)
  - Component 3: Contains %%time cell magic (0.20)
  - Component 4: Contains %%writefile config.py cell magic (0.20)
  - Component 5: config.py file created with valid content (0.15)
  - Component 6: Cells have execution_count (ran successfully) (0.15)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_032'

NOTEBOOK_PATH = os.path.join(WORKDIR, 'projects', 'jupyter-ml', 'notebooks', 'model_training.ipynb')
CONFIG_PATH = os.path.join(WORKDIR, 'projects', 'jupyter-ml', 'notebooks', 'config.py')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: notebook must exist
    if not os.path.exists(NOTEBOOK_PATH):
        print(f"CRITICAL: Notebook not found at {NOTEBOOK_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Load notebook
    try:
        with open(NOTEBOOK_PATH, 'r') as f:
            nb = json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse notebook as JSON: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid ipynb structure with cells (0.10 points)
    try:
        cells = nb.get('cells', [])
        nbformat = nb.get('nbformat', 0)
        if nbformat >= 4 and len(cells) >= 3:
            print(f"PASS: Component 1 — Valid ipynb (nbformat={nbformat}, {len(cells)} cells) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — Expected nbformat>=4 and >=3 cells, got nbformat={nbformat}, {len(cells)} cells")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Extract all code cell sources for magic command checks
    code_cells = [c for c in cells if c.get('cell_type') == 'code']
    code_sources = []
    for c in code_cells:
        src = c.get('source', '')
        if isinstance(src, list):
            src = ''.join(src)
        code_sources.append(src)

    # Component 2: %matplotlib inline magic (0.20 points)
    try:
        has_matplotlib = any(
            any(line.strip() == '%matplotlib inline' or line.strip().startswith('%matplotlib inline')
                for line in src.split('\n'))
            for src in code_sources
        )
        if has_matplotlib:
            print(f"PASS: Component 2 — Found %matplotlib inline magic (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — No cell contains '%matplotlib inline'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: %%time cell magic (0.20 points)
    try:
        has_time = any(
            src.split('\n')[0].strip().startswith('%%time')
            for src in code_sources if src.strip()
        )
        if has_time:
            print(f"PASS: Component 3 — Found %%time cell magic (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — No cell starts with '%%time'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: %%writefile config.py cell magic (0.20 points)
    try:
        has_writefile = any(
            src.split('\n')[0].strip().startswith('%%writefile') and 'config.py' in src.split('\n')[0]
            for src in code_sources if src.strip()
        )
        if has_writefile:
            print(f"PASS: Component 4 — Found %%writefile config.py cell magic (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — No cell starts with '%%writefile config.py'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: config.py file exists with content (0.15 points)
    # This file is created by the %%writefile magic when executed
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                config_content = f.read().strip()
            if len(config_content) > 10:
                print(f"PASS: Component 5 — config.py exists ({len(config_content)} chars) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — config.py exists but too short ({len(config_content)} chars)")
        else:
            print(f"FAIL: Component 5 — config.py not found at {CONFIG_PATH}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Code cells have been executed (execution_count > 0) (0.15 points)
    try:
        executed_cells = 0
        for c in code_cells:
            ec = c.get('execution_count')
            if ec is not None and isinstance(ec, int) and ec > 0:
                executed_cells += 1
        if executed_cells >= 3:
            print(f"PASS: Component 6 — {executed_cells} cells executed (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 — Only {executed_cells}/3 cells have execution_count > 0")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
