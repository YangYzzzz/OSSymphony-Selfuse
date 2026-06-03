"""
Reward Script: Extract code cells from Jupyter notebook and save as numpy_code.py
Task ID: osworld_multi_apps_code_to_writer_file_005
Domain: libreoffice_writer / multi_apps
Scoring:
  Component 1: numpy_code.py exists on Desktop (precondition gate)
  Component 2: File starts with correct Python import content (0.3 pts)
  Component 3: File has correct total length matching notebook code cells (0.3 pts)
  Component 4: File content exactly matches concatenation of all code cells from notebook (0.4 pts)
"""

import os
import urllib.request
import json

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_to_writer_file_005'
DESKTOP_PATH = os.path.join(WORKDIR, 'Desktop', 'numpy_code.py')
NOTEBOOK_URL = 'https://raw.githubusercontent.com/jakevdp/PythonDataScienceHandbook/master/notebooks/02.02-The-Basics-Of-NumPy-Arrays.ipynb'

# Expected content from the notebook (what code cells concatenated should look like)
EXPECTED_START = 'import numpy as np'
EXPECTED_CODE_CELL_COUNT = 51
EXPECTED_LENGTH = 2132


def get_expected_content():
    """
    Fetch the notebook from the URL and return the concatenated code cell content.
    Returns None if the fetch fails.
    """
    try:
        req = urllib.request.urlopen(NOTEBOOK_URL, timeout=20)
        nb = json.loads(req.read())
        all_cells = nb['cells']
        code_cells = [c for c in all_cells if c['cell_type'] == 'code']
        expected = ''.join(
            ''.join(c['source']) if isinstance(c['source'], list) else c['source']
            for c in code_cells
        )
        return expected, len(code_cells)
    except Exception as e:
        print(f"WARN: Could not fetch notebook from URL: {e}")
        return None, None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The task requires:
    1. numpy_code.py exists on Desktop
    2. Content is sourced only from code cells (no markdown)
    3. Code cells are concatenated in order
    4. File content exactly matches expected concatenation
    """
    total_score = 0.0

    # --- Precondition Gate: File must exist ---
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load actual file content
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            actual_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    actual_length = len(actual_content)
    print(f"INFO: File found at {file_path}, length={actual_length}")

    # --- Component 1: File starts with Python code from first code cell (0.3 pts) ---
    # The first code cell of the notebook starts with 'import numpy as np'
    # This FAILS on initial_env (no file) and PASSES on golden_env (correct content)
    try:
        if actual_content.startswith(EXPECTED_START):
            print(f"PASS: Component 1 — file starts with '{EXPECTED_START}' (0.3 pts)")
            total_score += 0.3
        else:
            first_line = actual_content.split('\n')[0] if actual_content else ''
            print(f"FAIL: Component 1 — expected file to start with '{EXPECTED_START}', found: '{first_line[:80]}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --- Component 2: File length approximately matches expected concatenation (0.3 pts) ---
    # Expected length is ~2132 bytes based on the 51 code cells from the notebook
    # Allow a tolerance of ±200 bytes for minor variations in whitespace handling
    try:
        tolerance = 200
        if abs(actual_length - EXPECTED_LENGTH) <= tolerance:
            print(f"PASS: Component 2 — file length {actual_length} within expected range "
                  f"[{EXPECTED_LENGTH - tolerance}, {EXPECTED_LENGTH + tolerance}] (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — file length {actual_length} not within tolerance "
                  f"of expected {EXPECTED_LENGTH} (+/-{tolerance})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --- Component 3: File content exactly matches expected concatenation (0.4 pts) ---
    # Fetch expected content from the notebook URL and compare
    try:
        expected_content, code_cell_count = get_expected_content()
        if expected_content is not None:
            if actual_content == expected_content:
                print(f"PASS: Component 3 — file content exactly matches concatenation "
                      f"of {code_cell_count} code cells from notebook (0.4 pts)")
                total_score += 0.4
            else:
                # Compute a rough similarity
                actual_lines = set(actual_content.split('\n'))
                expected_lines = set(expected_content.split('\n'))
                overlap = len(actual_lines & expected_lines)
                total_expected = len(expected_lines)
                similarity = overlap / total_expected if total_expected > 0 else 0
                print(f"FAIL: Component 3 — content mismatch. "
                      f"Expected length: {len(expected_content)}, Actual: {actual_length}, "
                      f"Line similarity: {similarity:.1%}")
                # Show first difference
                exp_lines = expected_content.split('\n')
                act_lines = actual_content.split('\n')
                for i, (e, a) in enumerate(zip(exp_lines, act_lines)):
                    if e != a:
                        print(f"  First diff at line {i}: expected {repr(e[:80])}, got {repr(a[:80])}")
                        break
        else:
            # Fallback: if network fetch fails, rely on length+start check
            print("WARN: Component 3 — could not fetch notebook to verify exact content; skipping")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Main entry: test against canonical artifact path on the VM
if not os.path.exists(DESKTOP_PATH):
    print(f"File not found: {DESKTOP_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(DESKTOP_PATH)
