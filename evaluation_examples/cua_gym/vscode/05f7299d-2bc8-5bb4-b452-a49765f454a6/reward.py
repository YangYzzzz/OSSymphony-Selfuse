"""
Reward Script: Fix compound launch configuration typo in VSCode
Task ID: vscode_fix_056
Domain: vscode
Scoring:
  Component 1 (0.6): Compound "Full Stack" configurations array contains "Backend" (exact case)
  Component 2 (0.4): All compound config references match defined configuration names exactly
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_056'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'fullstack-app', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments), handling control chars and comments."""
    with open(path, 'r') as f:
        content = f.read()
    # First try direct parse with strict=False (handles control chars in strings)
    try:
        return json.loads(content, strict=False)
    except json.JSONDecodeError:
        pass
    # Fallback: strip comments outside of strings, then parse
    # Remove single-line comments that are NOT inside strings
    # Simple approach: remove lines that start with optional whitespace + //
    lines = content.split('\n')
    cleaned = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith('//'):
            continue
        # Remove trailing comments (only if not inside a string value)
        cleaned.append(line)
    content = '\n'.join(cleaned)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content, strict=False)


def verify_task(launch_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load launch.json
    try:
        data = load_jsonc(launch_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load launch.json at {launch_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract defined configuration names
    defined_configs = []
    try:
        configurations = data.get('configurations', [])
        defined_configs = [cfg.get('name', '') for cfg in configurations]
        print(f"INFO: Defined configuration names: {defined_configs}")
    except Exception as e:
        print(f"ERROR: Could not read configurations: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract compound configurations
    compounds = data.get('compounds', [])
    if not compounds:
        print("FAIL: No compounds section found in launch.json")
        print("REWARD: 0.0")
        return 0.0

    # Find the "Full Stack" compound
    full_stack = None
    for compound in compounds:
        if compound.get('name') == 'Full Stack':
            full_stack = compound
            break

    if full_stack is None:
        print("FAIL: No compound named 'Full Stack' found")
        print("REWARD: 0.0")
        return 0.0

    compound_configs = full_stack.get('configurations', [])
    print(f"INFO: Compound 'Full Stack' references: {compound_configs}")

    # Component 1: Compound contains "Backend" with exact case (0.6 points)
    # Initial has "backend" (lowercase) which is the typo. Golden has "Backend".
    try:
        if "Backend" in compound_configs:
            print(f"PASS: Component 1 - 'Backend' (exact case) found in compound configurations (0.6 pts)")
            total_score += 0.6
        else:
            # Check if there's a case-insensitive match to give diagnostic info
            lower_matches = [c for c in compound_configs if c.lower() == 'backend']
            if lower_matches:
                print(f"FAIL: Component 1 - Found '{lower_matches[0]}' but expected exact 'Backend' (case mismatch)")
            else:
                print(f"FAIL: Component 1 - 'Backend' not found in compound configurations: {compound_configs}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: All compound config references match defined configuration names exactly (0.4 points)
    # This ensures there are no typos/mismatches in the compound's configurations array.
    # Initial fails because "backend" doesn't match any defined name ("Backend").
    try:
        all_match = len(compound_configs) > 0
        mismatches = []
        for ref_name in compound_configs:
            if ref_name not in defined_configs:
                all_match = False
                mismatches.append(ref_name)

        if all_match:
            print(f"PASS: Component 2 - All compound references {compound_configs} match defined configs {defined_configs} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 - Mismatched references: {mismatches} not in defined configs {defined_configs}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(LAUNCH_JSON_PATH):
    print(f"File not found: {LAUNCH_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(LAUNCH_JSON_PATH)
