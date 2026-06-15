"""
Reward Script: Data science workspace setup in VSCode
Task ID: vscode_wf_071
Domain: vscode
Scoring:
  C1: Extensions installed (Python, Jupyter, Pylance) - 0.15
  C2: Directory structure (notebooks/, data/, src/, models/) - 0.15
  C3: requirements.txt with correct packages - 0.15
  C4: Jupyter notebook data_pipeline.ipynb with proper cells - 0.15
  C5: VSCode settings.json with Jupyter/Python settings - 0.15
  C6: tasks.json with install-deps, run-pipeline, export-results - 0.15
  C7: src/ utility modules - 0.10
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
TASK_ID = 'vscode_wf_071'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Extensions installed (0.15 points)
    # Task requires Python, Jupyter, and Pylance extensions
    try:
        ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
        alt_ext_dir = os.path.expanduser('~/.vscode/extensions')

        # Use `code --list-extensions` output by reading from a temp approach
        # Instead, check extensions filesystem directly
        extensions_found = 0
        required_ext_ids = ['ms-python.python', 'ms-toolsai.jupyter', 'ms-python.vscode-pylance']

        # Check common extension directories
        for ext_base in [alt_ext_dir, ext_dir]:
            if os.path.isdir(ext_base):
                ext_contents = os.listdir(ext_base)
                for req_ext in required_ext_ids:
                    # Extension dirs are named like "ms-python.python-2024.1.1"
                    publisher, name = req_ext.split('.', 1)
                    pattern = req_ext.lower()
                    for d in ext_contents:
                        if d.lower().startswith(pattern):
                            extensions_found += 1
                            break

        if extensions_found >= 3:
            print(f"PASS: Component 1 — All 3 required extensions found ({extensions_found}) (0.15 pts)")
            total_score += 0.15
        elif extensions_found >= 2:
            print(f"PARTIAL: Component 1 — {extensions_found}/3 extensions found (0.10 pts)")
            total_score += 0.10
        elif extensions_found >= 1:
            print(f"PARTIAL: Component 1 — {extensions_found}/3 extensions found (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 1 — No required extensions found in filesystem")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Directory structure (0.15 points)
    # Task requires notebooks/, data/, src/, models/ under ~/project
    try:
        required_dirs = ['notebooks', 'data', 'src', 'models']
        dirs_found = 0
        for d in required_dirs:
            dir_path = os.path.join(PROJECT, d)
            if os.path.isdir(dir_path):
                dirs_found += 1
            else:
                print(f"  MISS: Directory {d}/ not found")

        if dirs_found == 4:
            print(f"PASS: Component 2 — All 4 directories found (0.15 pts)")
            total_score += 0.15
        elif dirs_found >= 2:
            print(f"PARTIAL: Component 2 — {dirs_found}/4 directories found (0.075 pts)")
            total_score += 0.075
        else:
            print(f"FAIL: Component 2 — Only {dirs_found}/4 directories found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: requirements.txt with correct packages (0.15 points)
    # Task requires numpy, pandas, scikit-learn, matplotlib
    try:
        req_path = os.path.join(PROJECT, 'requirements.txt')
        if os.path.isfile(req_path):
            with open(req_path, 'r') as f:
                content = f.read().lower()
            required_packages = ['numpy', 'pandas', 'scikit-learn', 'matplotlib']
            pkgs_found = sum(1 for pkg in required_packages if pkg in content)
            if pkgs_found == 4:
                print(f"PASS: Component 3 — All 4 packages in requirements.txt (0.15 pts)")
                total_score += 0.15
            elif pkgs_found >= 2:
                print(f"PARTIAL: Component 3 — {pkgs_found}/4 packages found (0.075 pts)")
                total_score += 0.075
            else:
                print(f"FAIL: Component 3 — Only {pkgs_found}/4 packages in requirements.txt")
        else:
            print(f"FAIL: Component 3 — requirements.txt not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Jupyter notebook data_pipeline.ipynb (0.15 points)
    # Task requires a notebook with data loading, processing, and visualization cells
    try:
        nb_path = os.path.join(PROJECT, 'notebooks', 'data_pipeline.ipynb')
        if os.path.isfile(nb_path):
            with open(nb_path, 'r') as f:
                nb = json.load(f)

            cells = nb.get('cells', [])
            if len(cells) < 2:
                print(f"FAIL: Component 4 — Notebook has only {len(cells)} cells, need at least 3")
            else:
                # Check for key content patterns in the notebook
                all_source = ''
                for cell in cells:
                    src = cell.get('source', [])
                    if isinstance(src, list):
                        all_source += ''.join(src)
                    else:
                        all_source += str(src)

                has_data_loading = any(kw in all_source.lower() for kw in ['load', 'read_csv', 'dataset', 'data loading'])
                has_processing = any(kw in all_source.lower() for kw in ['clean', 'preprocess', 'processing', 'feature'])
                has_visualization = any(kw in all_source.lower() for kw in ['plot', 'plt', 'matplotlib', 'visualization', 'hist', 'chart'])

                checks_passed = sum([has_data_loading, has_processing, has_visualization])
                if checks_passed == 3:
                    print(f"PASS: Component 4 — Notebook has data loading, processing, and visualization (0.15 pts)")
                    total_score += 0.15
                elif checks_passed >= 2:
                    print(f"PARTIAL: Component 4 — {checks_passed}/3 notebook content areas found (0.10 pts)")
                    total_score += 0.10
                elif checks_passed >= 1:
                    print(f"PARTIAL: Component 4 — {checks_passed}/3 notebook content areas found (0.05 pts)")
                    total_score += 0.05
                else:
                    print(f"FAIL: Component 4 — Notebook lacks data loading, processing, and visualization content")
        else:
            print(f"FAIL: Component 4 — notebooks/data_pipeline.ipynb not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: VSCode settings.json with Jupyter/Python settings (0.15 points)
    # Task requires Jupyter auto-scroll, variable explorer, and cell execution settings
    try:
        settings_path = os.path.join(PROJECT, '.vscode', 'settings.json')
        if os.path.isfile(settings_path):
            with open(settings_path, 'r') as f:
                content = f.read()
            # Strip JSONC comments
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            settings = json.loads(content_clean)

            setting_checks = 0
            total_setting_checks = 3

            # Check Jupyter auto-scroll / output scrolling
            scroll_keys = ['notebook.output.scrolling', 'jupyter.output.scrolling']
            if any(settings.get(k) is True for k in scroll_keys):
                setting_checks += 1
                print(f"  OK: Jupyter/notebook output scrolling enabled")
            else:
                print(f"  MISS: No Jupyter output scrolling setting found")

            # Check variable explorer
            var_explorer_keys = ['notebook.variableExplorer.enabled', 'jupyter.variableExplorer.enabled']
            if any(settings.get(k) is True for k in var_explorer_keys):
                setting_checks += 1
                print(f"  OK: Variable explorer enabled")
            else:
                print(f"  MISS: No variable explorer setting found")

            # Check cell execution related settings
            cell_exec_keys = [
                'notebook.executeWithoutSelection',
                'jupyter.interactiveWindow.textEditor.executeSelection',
                'jupyter.sendSelectionToInteractiveWindow',
            ]
            if any(settings.get(k) is True for k in cell_exec_keys):
                setting_checks += 1
                print(f"  OK: Cell execution setting found")
            else:
                print(f"  MISS: No cell execution setting found")

            if setting_checks == 3:
                print(f"PASS: Component 5 — All 3 Jupyter/Python settings present (0.15 pts)")
                total_score += 0.15
            elif setting_checks >= 2:
                print(f"PARTIAL: Component 5 — {setting_checks}/3 settings found (0.10 pts)")
                total_score += 0.10
            elif setting_checks >= 1:
                print(f"PARTIAL: Component 5 — {setting_checks}/3 settings found (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 5 — No required Jupyter settings found")
        else:
            print(f"FAIL: Component 5 — .vscode/settings.json not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: tasks.json with install-deps, run-pipeline, export-results (0.15 points)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        if os.path.isfile(tasks_path):
            with open(tasks_path, 'r') as f:
                content = f.read()
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            tasks_config = json.loads(content_clean)

            tasks_list = tasks_config.get('tasks', [])
            task_labels = [t.get('label', '') for t in tasks_list]

            required_tasks = ['install-deps', 'run-pipeline', 'export-results']
            tasks_found = sum(1 for rt in required_tasks if rt in task_labels)

            if tasks_found == 3:
                print(f"PASS: Component 6 — All 3 required tasks found in tasks.json (0.15 pts)")
                total_score += 0.15
            elif tasks_found >= 2:
                print(f"PARTIAL: Component 6 — {tasks_found}/3 tasks found (0.10 pts)")
                total_score += 0.10
            elif tasks_found >= 1:
                print(f"PARTIAL: Component 6 — {tasks_found}/3 tasks found (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 6 — No required tasks found. Labels: {task_labels}")
        else:
            print(f"FAIL: Component 6 — .vscode/tasks.json not found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: src/ has utility modules (0.10 points)
    # Task mentions "src/ has utility modules for the pipeline"
    try:
        src_dir = os.path.join(PROJECT, 'src')
        if os.path.isdir(src_dir):
            py_files = [f for f in os.listdir(src_dir) if f.endswith('.py') and f != '__init__.py']
            has_init = os.path.isfile(os.path.join(src_dir, '__init__.py'))

            if len(py_files) >= 1 and has_init:
                # Verify at least one module has meaningful content (not just empty)
                meaningful = False
                for pyf in py_files:
                    fpath = os.path.join(src_dir, pyf)
                    with open(fpath, 'r') as f:
                        content = f.read()
                    if len(content.strip()) > 50:  # More than a trivial file
                        meaningful = True
                        break

                if meaningful:
                    print(f"PASS: Component 7 — src/ has __init__.py and {len(py_files)} utility module(s) (0.10 pts)")
                    total_score += 0.10
                else:
                    print(f"PARTIAL: Component 7 — src/ has files but they appear trivial (0.05 pts)")
                    total_score += 0.05
            elif len(py_files) >= 1:
                print(f"PARTIAL: Component 7 — src/ has modules but no __init__.py (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 7 — src/ exists but has no utility modules")
        else:
            print(f"FAIL: Component 7 — src/ directory not found")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
