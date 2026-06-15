"""
Reward Script: Jupyter notebook workflow setup in VSCode
Task ID: vscode_wf_058
Domain: vscode
Scoring:
  - Component 1: Jupyter extension installed (0.20)
  - Component 2: data_analysis.ipynb exists with 4+ code cells (0.25)
  - Component 3: VSCode Jupyter settings configured (0.25)
  - Component 4: tasks.json with export-notebook nbconvert task (0.20)
  - Component 5: Notebook cells contain required analysis steps (0.10)
"""

import os
import json
import re

HOME = '/home/user'
PROJECT = os.path.join(HOME, 'project')
NOTEBOOK_PATH = os.path.join(PROJECT, 'data_analysis.ipynb')
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
TASKS_PATH = os.path.join(PROJECT, '.vscode', 'tasks.json')


def load_json_file(path):
    """Load a JSON file, handling JSONC comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip // comments for JSONC
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify Jupyter notebook workflow setup with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Jupyter extension installed (0.20 points)
    # This changes between initial (no extension dirs) and golden (extension installed)
    try:
        ext_dir = os.path.join(HOME, '.vscode', 'extensions')
        jupyter_ext_dirs = []
        if os.path.isdir(ext_dir):
            jupyter_ext_dirs = [
                e for e in os.listdir(ext_dir)
                if 'ms-toolsai.jupyter' in e.lower() and os.path.isdir(os.path.join(ext_dir, e))
            ]
        if len(jupyter_ext_dirs) > 0:
            print(f"PASS: Component 1 — Jupyter extension ms-toolsai.jupyter is installed (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — ms-toolsai.jupyter not found in {ext_dir}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: data_analysis.ipynb exists with 4+ code cells (0.25 points)
    # Initial state has no notebook; golden has it with 4 cells
    try:
        if not os.path.exists(NOTEBOOK_PATH):
            print(f"FAIL: Component 2 — data_analysis.ipynb does not exist at {NOTEBOOK_PATH}")
        else:
            with open(NOTEBOOK_PATH, 'r') as f:
                nb = json.load(f)
            cells = nb.get('cells', [])
            code_cells = [c for c in cells if c.get('cell_type') == 'code']
            if len(code_cells) >= 4:
                print(f"PASS: Component 2 — data_analysis.ipynb has {len(code_cells)} code cells (>= 4) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — data_analysis.ipynb has only {len(code_cells)} code cells, need >= 4")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: VSCode Jupyter settings configured (0.25 points)
    # Initial settings have no Jupyter keys; golden has several
    try:
        if not os.path.exists(SETTINGS_PATH):
            print(f"FAIL: Component 3 — settings.json not found at {SETTINGS_PATH}")
        else:
            settings = load_json_file(SETTINGS_PATH)
            checks_passed = 0
            checks_total = 3

            # Check jupyter.autoScrollOutput
            if settings.get('jupyter.autoScrollOutput') is True:
                checks_passed += 1
                print(f"  Component 3a: jupyter.autoScrollOutput = true  OK")
            else:
                print(f"  Component 3a: jupyter.autoScrollOutput missing or not true, found: {settings.get('jupyter.autoScrollOutput')}")

            # Check notebook-related settings (at least one notebook.* key)
            notebook_keys = [k for k in settings if k.startswith('notebook.')]
            if len(notebook_keys) >= 1:
                checks_passed += 1
                print(f"  Component 3b: Found {len(notebook_keys)} notebook.* settings  OK")
            else:
                print(f"  Component 3b: No notebook.* settings found")

            # Check jupyter kernel settings (any jupyter.kernels* key or jupyter.notebookFileRoot)
            jupyter_kernel_keys = [k for k in settings if 'kernel' in k.lower() or k == 'jupyter.notebookFileRoot']
            if len(jupyter_kernel_keys) >= 1:
                checks_passed += 1
                print(f"  Component 3c: Found kernel/notebook config keys: {jupyter_kernel_keys}  OK")
            else:
                print(f"  Component 3c: No jupyter kernel/notebook config keys found")

            if checks_passed == checks_total:
                print(f"PASS: Component 3 — All {checks_total} Jupyter settings checks passed (0.25 pts)")
                total_score += 0.25
            elif checks_passed >= 2:
                partial = round(0.25 * checks_passed / checks_total, 2)
                print(f"PARTIAL: Component 3 — {checks_passed}/{checks_total} checks passed ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — Only {checks_passed}/{checks_total} Jupyter settings checks passed")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: tasks.json with export-notebook task (0.20 points)
    # Initial state has no .vscode/tasks.json; golden has one with nbconvert task
    try:
        if not os.path.exists(TASKS_PATH):
            print(f"FAIL: Component 4 — tasks.json not found at {TASKS_PATH}")
        else:
            tasks_config = load_json_file(TASKS_PATH)
            tasks = tasks_config.get('tasks', [])
            # Find a task that mentions nbconvert and html
            export_task = None
            for t in tasks:
                label = str(t.get('label', '')).lower()
                command = str(t.get('command', '')).lower()
                if ('export' in label or 'notebook' in label or 'nbconvert' in label or 'convert' in label):
                    export_task = t
                    break
                if 'nbconvert' in command and 'html' in command:
                    export_task = t
                    break

            if export_task is not None:
                cmd = str(export_task.get('command', ''))
                if 'nbconvert' in cmd.lower() and 'html' in cmd.lower():
                    print(f"PASS: Component 4 — tasks.json has export-notebook task with nbconvert --to html (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 4 — Found task '{export_task.get('label')}' but command doesn't use nbconvert --to html: {cmd}")
            else:
                print(f"FAIL: Component 4 — No export-notebook task found in tasks.json. Tasks: {[t.get('label') for t in tasks]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Notebook cells contain required analysis steps (0.10 points)
    # Verify cells actually have pandas/matplotlib import, CSV loading, stats, visualization
    try:
        if not os.path.exists(NOTEBOOK_PATH):
            print(f"FAIL: Component 5 — data_analysis.ipynb not found")
        else:
            with open(NOTEBOOK_PATH, 'r') as f:
                nb = json.load(f)
            cells = nb.get('cells', [])
            # Combine all cell sources into one string for searching
            all_source = ''
            for c in cells:
                src = c.get('source', [])
                if isinstance(src, list):
                    all_source += '\n'.join(src) + '\n'
                else:
                    all_source += str(src) + '\n'

            content_checks = 0
            content_total = 4

            # Check for pandas import
            if 'import pandas' in all_source or 'from pandas' in all_source:
                content_checks += 1
            # Check for matplotlib import
            if 'import matplotlib' in all_source or 'from matplotlib' in all_source:
                content_checks += 1
            # Check for CSV loading
            if 'read_csv' in all_source or 'csv' in all_source.lower():
                content_checks += 1
            # Check for visualization (plt.show, plt.savefig, plot, etc.)
            if 'plt.' in all_source or '.plot(' in all_source or 'savefig' in all_source:
                content_checks += 1

            if content_checks == content_total:
                print(f"PASS: Component 5 — Notebook contains all required analysis steps ({content_checks}/{content_total}) (0.10 pts)")
                total_score += 0.10
            elif content_checks >= 3:
                partial = round(0.10 * content_checks / content_total, 2)
                print(f"PARTIAL: Component 5 — {content_checks}/{content_total} content checks passed ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — Only {content_checks}/{content_total} content checks passed")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
