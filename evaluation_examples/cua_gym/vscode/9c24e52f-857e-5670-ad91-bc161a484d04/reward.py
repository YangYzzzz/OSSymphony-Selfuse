"""
Reward Script: Extract repeated expression into variable 'outputElement'
Task ID: vscode_rrt_033
Domain: vscode
Scoring:
  Component 1 (0.3): const outputElement declaration with correct assignment
  Component 2 (0.4): All 4 occurrences replaced with outputElement usage
  Component 3 (0.3): No remaining document.getElementById("output") calls after declaration
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_033'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'web', 'app.js')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be readable
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        lines = content.strip().split('\n')
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: const outputElement declaration with correct RHS (0.3 points)
    # The refactored code should have a line declaring:
    #   const outputElement = document.getElementById("output");
    try:
        decl_pattern = r'const\s+outputElement\s*=\s*document\.getElementById\(\s*["\']output["\']\s*\)\s*;?'
        decl_match = re.search(decl_pattern, content)
        if decl_match:
            print(f"PASS: Component 1 — outputElement declaration found: '{decl_match.group().strip()}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No 'const outputElement = document.getElementById(\"output\")' declaration found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 4 usages replaced with outputElement (0.4 points)
    # Expected usages: outputElement.innerHTML, outputElement.style.color,
    #   outputElement.classList.add, outputElement.setAttribute
    try:
        expected_usages = [
            r'outputElement\.innerHTML\s*=',
            r'outputElement\.style\.color\s*=',
            r'outputElement\.classList\.add\(',
            r'outputElement\.setAttribute\(',
        ]
        usage_count = 0
        for pattern in expected_usages:
            if re.search(pattern, content):
                usage_count += 1

        if usage_count == 4:
            print(f"PASS: Component 2 — All 4 outputElement usages found (0.4 pts)")
            total_score += 0.4
        elif usage_count > 0:
            partial = round(0.4 * (usage_count / 4), 2)
            print(f"PARTIAL: Component 2 — {usage_count}/4 outputElement usages found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No outputElement usages found (0/4)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: No remaining document.getElementById("output") calls
    # after the declaration line (0.3 points)
    # In the golden file, the ONLY occurrence of document.getElementById("output")
    # should be in the declaration. All other uses should be outputElement.
    try:
        # Count all occurrences of document.getElementById("output") or ('output')
        all_gebi = re.findall(r'document\.getElementById\(\s*["\']output["\']\s*\)', content)
        gebi_count = len(all_gebi)

        if decl_match and gebi_count == 1:
            # Exactly one occurrence (the declaration) — all others replaced
            print(f"PASS: Component 3 — Only 1 getElementById call remains (in declaration), all others replaced (0.3 pts)")
            total_score += 0.3
        elif not decl_match and gebi_count == 0:
            # No declaration AND no getElementById calls — wrong approach
            print(f"FAIL: Component 3 — No getElementById calls and no declaration found")
        elif gebi_count > 1:
            print(f"FAIL: Component 3 — {gebi_count} getElementById calls remain (expected exactly 1 in declaration)")
        elif gebi_count == 0 and decl_match:
            # Declaration exists but uses a different pattern — unusual but check
            print(f"FAIL: Component 3 — Declaration found but 0 getElementById calls (unexpected)")
        else:
            print(f"FAIL: Component 3 — getElementById count: {gebi_count}, declaration found: {bool(decl_match)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
