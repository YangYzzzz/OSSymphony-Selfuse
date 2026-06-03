"""
Reward Script: Create launch.json with integratedTerminal for Python debugging
Task ID: vscode_py_037
Domain: vscode
Scoring:
  Component 1 (0.25): Valid launch.json with configurations array
  Component 2 (0.40): console set to integratedTerminal
  Component 3 (0.20): program set to ${file}
  Component 4 (0.15): Proper Python debug type and launch request
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_037'

# Possible locations for launch.json
LAUNCH_JSON_PATHS = [
    os.path.join(WORKDIR, 'workspace', '.vscode', 'launch.json'),
    os.path.join(WORKDIR, '.vscode', 'launch.json'),
]


def strip_jsonc_comments(text):
    """Strip single-line // comments and block /* */ comments from JSONC."""
    # Remove block comments
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    # Remove single-line comments (but not inside strings)
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        # Simple approach: remove // comments not inside strings
        in_string = False
        escape = False
        result = []
        i = 0
        while i < len(line):
            ch = line[i]
            if escape:
                result.append(ch)
                escape = not escape  # reset escape flag
                i += 1
                continue
            if ch == '\\' and in_string:
                result.append(ch)
                escape = not escape  # set escape flag
                i += 1
                continue
            if ch == '"':
                in_string = not in_string
                result.append(ch)
                i += 1
                continue
            if not in_string and ch == '/' and i + 1 < len(line) and line[i + 1] == '/':
                break  # rest of line is comment
            result.append(ch)
            i += 1
        cleaned.append(''.join(result))
    return '\n'.join(cleaned)


def find_launch_json():
    """Find launch.json in known locations."""
    for path in LAUNCH_JSON_PATHS:
        if os.path.exists(path):
            return path
    return None


def load_launch_json(path):
    """Load launch.json, handling JSONC comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Try direct JSON parse first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    # Try stripping comments
    cleaned = strip_jsonc_comments(content)
    return json.loads(cleaned)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Find launch.json
    launch_path = find_launch_json()
    if not launch_path:
        print(f"CRITICAL: launch.json not found in any expected location")
        print(f"  Checked: {LAUNCH_JSON_PATHS}")
        print("REWARD: 0.0")
        return 0.0

    # Load and parse
    try:
        data = load_launch_json(launch_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json at {launch_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid launch.json with configurations array (0.25 points)
    try:
        configs = data.get('configurations', None)
        if isinstance(configs, list) and len(configs) > 0:
            print(f"PASS: Component 1 -- Valid launch.json with {len(configs)} configuration(s) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 -- 'configurations' missing or empty. Found: {type(configs)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Find a Python debug configuration (search all configs)
    python_config = None
    if isinstance(data.get('configurations'), list):
        for cfg in data['configurations']:
            if not isinstance(cfg, dict):
                continue
            # Match by type containing 'python' or 'debugpy', or by name containing 'python'
            cfg_type = str(cfg.get('type', '')).lower()
            cfg_name = str(cfg.get('name', '')).lower()
            if 'python' in cfg_type or 'debugpy' in cfg_type or 'python' in cfg_name:
                python_config = cfg
                break
        # If no Python-specific config found, use the first one
        if python_config is None and len(data['configurations']) > 0:
            python_config = data['configurations'][0]

    if python_config is None:
        print("FAIL: No configuration found to evaluate")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: console set to integratedTerminal (0.40 points)
    try:
        console_val = python_config.get('console', None)
        if console_val == 'integratedTerminal':
            print(f"PASS: Component 2 -- console is 'integratedTerminal' (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 2 -- Expected console='integratedTerminal', found: '{console_val}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: program set to ${file} (0.20 points)
    try:
        program_val = python_config.get('program', None)
        if program_val and '${file}' in str(program_val):
            print(f"PASS: Component 3 -- program contains '${{file}}' (value: {program_val}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 -- Expected program containing '${{file}}', found: '{program_val}'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Proper Python debug type and launch request (0.15 points)
    try:
        cfg_type = str(python_config.get('type', '')).lower()
        cfg_request = str(python_config.get('request', '')).lower()
        type_ok = cfg_type in ('debugpy', 'python')
        request_ok = cfg_request == 'launch'
        if type_ok and request_ok:
            print(f"PASS: Component 4 -- type='{cfg_type}', request='{cfg_request}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 -- Expected type in (debugpy,python) and request=launch, found type='{cfg_type}', request='{cfg_request}'")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
