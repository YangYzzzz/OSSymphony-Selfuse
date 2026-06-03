"""
Reward Script: Compound launch configuration for Flask backend + Chrome frontend
Task ID: vscode_stu_092
Domain: vscode
Scoring:
  - Component 1 (0.2): launch.json exists and is valid JSON with configurations array
  - Component 2 (0.3): Python/Flask debug configuration present
  - Component 3 (0.25): Chrome debug configuration present
  - Component 4 (0.25): Compound configuration referencing both configs
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_092'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, TASK_ID, '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments) by stripping comments first.
    Handles // inside strings correctly by only stripping comments outside strings."""
    with open(path, 'r') as f:
        content = f.read()
    # First try direct parse
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    # Strip comments carefully: remove // only when not inside a string
    # Simple approach: process line by line, track if we're inside a string
    result_lines = []
    for line in content.split('\n'):
        new_line = []
        in_string = False
        escape = False
        i = 0
        while i < len(line):
            ch = line[i]
            if escape:
                new_line.append(ch)
                escape = False
                i += 1
                continue
            if ch == '\\' and in_string:
                new_line.append(ch)
                escape = True
                i += 1
                continue
            if ch == '"':
                in_string = not in_string
                new_line.append(ch)
                i += 1
                continue
            if not in_string and ch == '/' and i + 1 < len(line) and line[i + 1] == '/':
                # Rest of line is a comment
                break
            new_line.append(ch)
            i += 1
        result_lines.append(''.join(new_line))
    cleaned = '\n'.join(result_lines)
    # Also strip block comments
    cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
    return json.loads(cleaned)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: launch.json must exist
    if not os.path.exists(LAUNCH_JSON_PATH):
        print(f"CRITICAL: launch.json not found at {LAUNCH_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: launch.json must be valid JSON
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    configurations = data.get('configurations', [])

    # Component 1: launch.json has configurations array with at least 2 entries (0.2 points)
    # This checks that the file is structurally sound for a compound setup
    try:
        if isinstance(configurations, list) and len(configurations) >= 2:
            print(f"PASS: Component 1 — launch.json has {len(configurations)} configurations (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected >= 2 configurations, found {len(configurations) if isinstance(configurations, list) else 'non-list'}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Python/Flask debug configuration (0.3 points)
    # Must have a configuration with type for Python debugging and flask module
    try:
        flask_config = None
        for cfg in configurations:
            cfg_type = str(cfg.get('type', '')).lower()
            cfg_module = str(cfg.get('module', '')).lower()
            cfg_program = str(cfg.get('program', '')).lower()
            # Accept debugpy or python type, with flask as module or in program
            is_python_type = cfg_type in ('debugpy', 'python', 'pythondebug')
            is_flask = cfg_module == 'flask' or 'flask' in cfg_program
            if is_python_type and is_flask:
                flask_config = cfg
                break

        if flask_config is not None:
            flask_name = flask_config.get('name', '<unnamed>')
            print(f"PASS: Component 2 — Flask debug config found: '{flask_name}' (type={flask_config.get('type')}, module={flask_config.get('module')}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — No Python/Flask debug configuration found in configurations")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Chrome debug configuration (0.25 points)
    # Must have a configuration with type 'chrome' for frontend debugging
    try:
        chrome_config = None
        for cfg in configurations:
            cfg_type = str(cfg.get('type', '')).lower()
            cfg_request = str(cfg.get('request', '')).lower()
            if cfg_type == 'chrome' and cfg_request == 'launch':
                chrome_config = cfg
                break

        if chrome_config is not None:
            chrome_name = chrome_config.get('name', '<unnamed>')
            print(f"PASS: Component 3 — Chrome debug config found: '{chrome_name}' (type={chrome_config.get('type')}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — No Chrome launch configuration found in configurations")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Compound configuration that references both Flask and Chrome (0.25 points)
    # Must have a 'compounds' array with an entry that lists both configuration names
    try:
        compounds = data.get('compounds', [])
        if not isinstance(compounds, list) or len(compounds) == 0:
            print(f"FAIL: Component 4 — No compounds array found or it is empty")
        else:
            # Gather all configuration names
            config_names = [cfg.get('name', '') for cfg in configurations]

            # Find a compound that references at least 2 configurations
            found_compound = None
            for compound in compounds:
                compound_configs = compound.get('configurations', [])
                if isinstance(compound_configs, list) and len(compound_configs) >= 2:
                    # Check that referenced configs exist in the configurations array
                    # (compound_configs can be strings or objects with 'name' key)
                    ref_names = []
                    for ref in compound_configs:
                        if isinstance(ref, str):
                            ref_names.append(ref)
                        elif isinstance(ref, dict):
                            ref_names.append(ref.get('name', ''))

                    # Verify that the referenced names match actual configuration names
                    matched = sum(1 for r in ref_names if r in config_names)
                    if matched >= 2:
                        found_compound = compound
                        break

            if found_compound is not None:
                compound_name = found_compound.get('name', '<unnamed>')
                print(f"PASS: Component 4 — Compound config found: '{compound_name}' referencing {found_compound.get('configurations')} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 — No compound configuration found that references >= 2 existing configs")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
