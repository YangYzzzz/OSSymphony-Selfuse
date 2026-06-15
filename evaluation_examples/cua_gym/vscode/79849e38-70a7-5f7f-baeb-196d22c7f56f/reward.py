"""
Reward Script: Move preprocessing cells above training cell in Jupyter notebook
Task ID: vscode_rf_009
Domain: vscode
Scoring:
  Component 1 (0.3): Cell 2 starts with "# Data Cleaning" (preprocessing moved up)
  Component 2 (0.3): Cells 2-4 are Cleaning, Normalization, Feature Engineering in order
  Component 3 (0.2): Cell 5 starts with "# Model Training" (moved down)
  Component 4 (0.2): Full 7-cell order is correct and all content preserved
"""

import json
import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_rf_009'
NOTEBOOK_PATH = os.path.join(WORKDIR, 'projects', 'ml_pipeline', 'pipeline.ipynb')

# Expected cell order after task completion (first comment line of each cell)
EXPECTED_ORDER = [
    "import numpy as np",        # Cell 1: imports
    "# Data Cleaning",           # Cell 2: was cell 3
    "# Data Normalization",      # Cell 3: was cell 4
    "# Feature Engineering",     # Cell 4: was cell 5
    "# Model Training",          # Cell 5: was cell 2
    "# Model Evaluation",        # Cell 6: unchanged
    "# Visualization",           # Cell 7: unchanged
]

# Initial order (before task) for reference
INITIAL_ORDER = [
    "import numpy as np",
    "# Model Training",
    "# Data Cleaning",
    "# Data Normalization",
    "# Feature Engineering",
    "# Model Evaluation",
    "# Visualization",
]


def get_cell_first_lines(nb_path):
    """Read notebook and return list of first lines of each cell."""
    with open(nb_path) as f:
        nb = json.load(f)
    cells = nb.get("cells", [])
    first_lines = []
    for cell in cells:
        src = "".join(cell.get("source", []))
        first_line = src.strip().split("\n")[0] if src.strip() else "(empty)"
        first_lines.append(first_line)
    return first_lines, cells


def verify_task(nb_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        first_lines, cells = get_cell_first_lines(nb_path)
    except Exception as e:
        print("CRITICAL: Cannot load notebook %s: %s" % (nb_path, e))
        print("REWARD: 0.0")
        return 0.0

    print("Detected cell order:")
    for i, fl in enumerate(first_lines):
        print("  Cell %d: %s" % (i + 1, fl))

    # Component 1: Cell 2 is "# Data Cleaning" (0.3 points)
    # In initial state, cell 2 is "# Model Training", so this only passes after the move
    try:
        if len(first_lines) >= 2 and first_lines[1] == "# Data Cleaning":
            print("PASS: Component 1 - Cell 2 is '# Data Cleaning' (0.3 pts)")
            total_score += 0.3
        else:
            actual = first_lines[1] if len(first_lines) >= 2 else "(missing)"
            print("FAIL: Component 1 - Expected cell 2 to be '# Data Cleaning', found: %s" % actual)
    except Exception as e:
        print("ERROR: Component 1 - %s" % e)

    # Component 2: Cells 2-4 are the three preprocessing cells in correct order (0.3 points)
    # In initial state, cell 2 is Model Training, so this check fails on initial
    try:
        if len(first_lines) >= 4:
            expected_trio = ["# Data Cleaning", "# Data Normalization", "# Feature Engineering"]
            actual_trio = first_lines[1:4]
            if actual_trio == expected_trio:
                print("PASS: Component 2 - Cells 2-4 are preprocessing trio in correct order (0.3 pts)")
                total_score += 0.3
            else:
                print("FAIL: Component 2 - Expected cells 2-4 = %s, found %s" % (expected_trio, actual_trio))
        else:
            print("FAIL: Component 2 - Not enough cells (need at least 4, have %d)" % len(first_lines))
    except Exception as e:
        print("ERROR: Component 2 - %s" % e)

    # Component 3: Cell 5 is "# Model Training" (0.2 points)
    # In initial state, cell 5 is "# Feature Engineering", so this only passes after the move
    try:
        if len(first_lines) >= 5 and first_lines[4] == "# Model Training":
            print("PASS: Component 3 - Cell 5 is '# Model Training' (0.2 pts)")
            total_score += 0.2
        else:
            actual = first_lines[4] if len(first_lines) >= 5 else "(missing)"
            print("FAIL: Component 3 - Expected cell 5 to be '# Model Training', found: %s" % actual)
    except Exception as e:
        print("ERROR: Component 3 - %s" % e)

    # Component 4: Full 7-cell order matches expected AND all content is preserved (0.2 points)
    # This checks that the notebook has exactly 7 cells with the complete expected order
    try:
        if len(first_lines) == 7 and first_lines == EXPECTED_ORDER:
            # Also verify cell contents are non-trivial (not just headers)
            all_have_content = all(
                len("".join(cell.get("source", [])).strip()) > 20 for cell in cells
            )
            if all_have_content:
                print("PASS: Component 4 - Full 7-cell order correct and content preserved (0.2 pts)")
                total_score += 0.2
            else:
                print("FAIL: Component 4 - Some cells have missing/truncated content")
        else:
            if len(first_lines) != 7:
                print("FAIL: Component 4 - Expected 7 cells, found %d" % len(first_lines))
            else:
                mismatches = []
                for i in range(7):
                    if first_lines[i] != EXPECTED_ORDER[i]:
                        mismatches.append("Cell %d: expected '%s', got '%s'" % (i+1, EXPECTED_ORDER[i], first_lines[i]))
                print("FAIL: Component 4 - Order mismatch: %s" % "; ".join(mismatches))
    except Exception as e:
        print("ERROR: Component 4 - %s" % e)

    final_score = min(total_score, 1.0)
    print("\nScore: %.1f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


# Entry point
if not os.path.exists(NOTEBOOK_PATH):
    print("File not found: %s" % NOTEBOOK_PATH)
    print("REWARD: 0.0")
else:
    verify_task(NOTEBOOK_PATH)
