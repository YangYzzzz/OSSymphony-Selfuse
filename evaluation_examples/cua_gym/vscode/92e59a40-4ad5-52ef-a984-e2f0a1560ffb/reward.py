"""
Reward Script: Create launch.json with source map debugging configuration
Task ID: vscode_td_076
Domain: vs_code
Scoring:
  Component 1: launch.json exists and is valid JSON with configurations array (0.2)
  Component 2: Configuration has type "node" and request "launch" (0.2)
  Component 3: sourceMaps is set to true (0.2)
  Component 4: outFiles matches expected pattern (0.2)
  Component 5: program is set to correct path (0.2)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_076'

# Possible locations for launch.json
LAUNCH_JSON_PATHS = [
    os.path.join(WORKDIR, 'projects', 'bundled-app', '.vscode', 'launch.json'),
]


def load_json_with_comments(file_path):
    """Load a JSON file, stripping // comments (JSONC support)."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip trailing commas before } or ]
    content = re.sub(r',\s*([}\]])', r'\1', content)
    return json.loads(content)


def find_launch_json():
    """Find launch.json in expected locations."""
    for path in LAUNCH_JSON_PATHS:
        if os.path.exists(path):
            return path
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Find launch.json
    launch_path = find_launch_json()

    # Component 1: launch.json exists and is valid JSON with configurations array (0.2 points)
    config = None
    try:
        if launch_path is None:
            print("FAIL: Component 1 -- launch.json not found in expected locations")
            print("REWARD: 0.0")
            return 0.0

        data = load_json_with_comments(launch_path)

        if not isinstance(data, dict):
            print(f"FAIL: Component 1 -- launch.json is not a JSON object")
            print("REWARD: 0.0")
            return 0.0

        configurations = data.get('configurations')
        if not isinstance(configurations, list) or len(configurations) == 0:
            print(f"FAIL: Component 1 -- 'configurations' array missing or empty")
            print("REWARD: 0.0")
            return 0.0

        # Use the first configuration (or find one with Node.js type)
        config = None
        for cfg in configurations:
            if isinstance(cfg, dict) and cfg.get('type', '').lower() == 'node':
                config = cfg
                break
        if config is None:
            # Fall back to first configuration
            config = configurations[0] if isinstance(configurations[0], dict) else None

        if config is None:
            print(f"FAIL: Component 1 -- No valid configuration object found")
            print("REWARD: 0.0")
            return 0.0

        if config is not None:
            print(f"PASS: Component 1 -- launch.json exists with valid configurations (0.2 pts)")
            total_score += 0.2
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 1 -- launch.json is not valid JSON: {e}")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: type is "node" and request is "launch" (0.2 points)
    try:
        cfg_type = config.get('type', '')
        cfg_request = config.get('request', '')
        if str(cfg_type).lower() == 'node' and str(cfg_request).lower() == 'launch':
            print(f"PASS: Component 2 -- type='node', request='launch' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 -- expected type='node' request='launch', found type='{cfg_type}' request='{cfg_request}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: sourceMaps is set to true (0.2 points)
    try:
        source_maps = config.get('sourceMaps')
        if source_maps is True:
            print(f"PASS: Component 3 -- sourceMaps=true (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- expected sourceMaps=true, found: {source_maps}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: outFiles matches expected pattern (0.2 points)
    try:
        out_files = config.get('outFiles')
        expected_out_files = ["${workspaceFolder}/dist/**/*.js"]
        if isinstance(out_files, list) and len(out_files) > 0:
            # Check if the expected pattern is in the outFiles list
            if expected_out_files[0] in out_files:
                print(f"PASS: Component 4 -- outFiles contains expected pattern (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 -- expected outFiles to contain '{expected_out_files[0]}', found: {out_files}")
        else:
            print(f"FAIL: Component 4 -- outFiles missing or empty, found: {out_files}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: program is set to correct path (0.2 points)
    try:
        program = config.get('program', '')
        expected_program = "${workspaceFolder}/dist/bundle.js"
        if str(program) == expected_program:
            print(f"PASS: Component 5 -- program='{program}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 -- expected program='{expected_program}', found: '{program}'")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
