"""
Reward Script: Set up TypeScript path aliases in tsconfig.json
Task ID: vscode_lp_039
Domain: vs_code
Scoring:
  - Component 1: baseUrl is "." (0.25)
  - Component 2: @components/* alias correct (0.25)
  - Component 3: @utils/* alias correct (0.25)
  - Component 4: @services/* alias correct (0.25)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_039'


def load_jsonc(file_path):
    """Load a JSON or JSONC file (strips // comments)."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load tsconfig.json
    try:
        config = load_jsonc(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    compiler_options = config.get('compilerOptions', {})

    # Component 1: baseUrl is set to "." (0.25 points)
    try:
        base_url = compiler_options.get('baseUrl')
        if base_url == '.':
            print(f"PASS: Component 1 -- baseUrl is '.' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 -- expected baseUrl='.', found: {base_url!r}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Get paths object for components 2-4
    paths = compiler_options.get('paths', {})

    # Component 2: @components/* alias maps to ["src/components/*"] (0.25 points)
    try:
        comp_alias = paths.get('@components/*')
        if isinstance(comp_alias, list) and 'src/components/*' in comp_alias:
            print(f"PASS: Component 2 -- @components/* -> {comp_alias} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- expected @components/* -> ['src/components/*'], found: {comp_alias!r}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: @utils/* alias maps to ["src/utils/*"] (0.25 points)
    try:
        utils_alias = paths.get('@utils/*')
        if isinstance(utils_alias, list) and 'src/utils/*' in utils_alias:
            print(f"PASS: Component 3 -- @utils/* -> {utils_alias} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- expected @utils/* -> ['src/utils/*'], found: {utils_alias!r}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: @services/* alias maps to ["src/services/*"] (0.25 points)
    try:
        svc_alias = paths.get('@services/*')
        if isinstance(svc_alias, list) and 'src/services/*' in svc_alias:
            print(f"PASS: Component 4 -- @services/* -> {svc_alias} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 -- expected @services/* -> ['src/services/*'], found: {svc_alias!r}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}/tsconfig.json'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
