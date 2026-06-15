"""
Reward Script: Change notebook kernel to ml-env conda environment and run verification cell
Task ID: vscode_rf_041
Domain: vscode
Scoring:
  Component 1 (0.35): Kernel name changed to 'ml-env' in metadata
  Component 2 (0.25): Kernel display name contains 'ml-env'
  Component 3 (0.25): Cell 1 has been executed (execution_count not null)
  Component 4 (0.15): Cell 1 output contains ml-env conda Python path
"""

import json
import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_rf_041'
NOTEBOOK_PATH = os.path.join(WORKDIR, 'projects', 'ml', 'train.ipynb')


def verify_task(nb_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load notebook JSON
    try:
        with open(nb_path, 'r') as f:
            nb = json.load(f)
    except Exception as e:
        print(f"CRITICAL: Cannot load notebook {nb_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract metadata kernel info
    kernelspec = nb.get('metadata', {}).get('kernelspec', {})
    kernel_name = kernelspec.get('name', '')
    kernel_display = kernelspec.get('display_name', '')

    # Extract cells
    cells = nb.get('cells', [])

    # Component 1: Kernel name changed to 'ml-env' (0.35 points)
    # Initial has "python3", golden should have "ml-env"
    try:
        if kernel_name == 'ml-env':
            print(f"PASS: Component 1 -- kernel name is 'ml-env' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 -- expected kernel name 'ml-env', found: '{kernel_name}'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Kernel display name contains 'ml-env' (0.25 points)
    # Initial has "Python 3", golden should show ml-env
    try:
        if 'ml-env' in kernel_display.lower():
            print(f"PASS: Component 2 -- kernel display name contains 'ml-env': '{kernel_display}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- expected display name containing 'ml-env', found: '{kernel_display}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Cell 1 has been executed (0.25 points)
    # Initial has execution_count=null, golden should have a number
    try:
        if len(cells) > 0:
            cell1 = cells[0]
            exec_count = cell1.get('execution_count')
            if exec_count is not None and isinstance(exec_count, int) and exec_count > 0:
                print(f"PASS: Component 3 -- cell 1 executed, execution_count={exec_count} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- cell 1 not executed, execution_count={exec_count}")
        else:
            print("FAIL: Component 3 -- no cells found in notebook")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Cell 1 output contains ml-env conda Python path (0.15 points)
    # Golden output should show a path like /home/user/miniconda3/envs/ml-env/bin/python
    try:
        if len(cells) > 0:
            cell1 = cells[0]
            outputs = cell1.get('outputs', [])
            output_text = ''
            for out in outputs:
                if out.get('output_type') == 'stream' and out.get('name') == 'stdout':
                    output_text += ''.join(out.get('text', []))
                elif out.get('output_type') == 'execute_result':
                    output_text += ''.join(out.get('data', {}).get('text/plain', []))

            if 'ml-env' in output_text:
                print(f"PASS: Component 4 -- cell output contains ml-env path: '{output_text.strip()}' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 -- cell output does not contain 'ml-env', found: '{output_text.strip()}'")
        else:
            print("FAIL: Component 4 -- no cells found in notebook")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

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
