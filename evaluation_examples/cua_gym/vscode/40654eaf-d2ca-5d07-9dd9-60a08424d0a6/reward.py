"""
Reward Script: Configure Chrome Debugger extension settings for React dev workflow
Task ID: vscode_we_093
Domain: vscode
Scoring:
  Component 1: launch.json exists with valid configurations array (0.15)
  Component 2: Config has type "chrome" and request "launch" (0.15)
  Component 3: url is "http://localhost:3000" (0.15)
  Component 4: webRoot is "${workspaceFolder}/src" (0.20)
  Component 5: port is 9222 (0.20)
  Component 6: sourceMapPathOverrides has webpack mapping (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_093'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'my-react-app', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments). Try plain JSON first, then strip comments."""
    with open(path, 'r') as f:
        content = f.read()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Strip single-line comments that are NOT inside strings
        # Simple approach: remove lines that start with // (after whitespace)
        lines = content.split('\n')
        cleaned = []
        for line in lines:
            stripped = line.lstrip()
            if stripped.startswith('//'):
                continue
            cleaned.append(line)
        return json.loads('\n'.join(cleaned))


def find_chrome_config(configurations):
    """Find the first configuration with type 'chrome'."""
    for cfg in configurations:
        if isinstance(cfg, dict) and cfg.get('type') == 'chrome':
            return cfg
    return None


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

    # Precondition: launch.json must be valid JSON with configurations
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    configs = data.get('configurations', [])
    if not isinstance(configs, list) or len(configs) == 0:
        print("FAIL: launch.json has no configurations array or it is empty")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: launch.json has a Chrome configuration entry (0.15 points)
    try:
        chrome_cfg = find_chrome_config(configs)
        if chrome_cfg is not None:
            print(f"PASS: Component 1 — Found Chrome configuration entry (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — No configuration with type 'chrome' found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if chrome_cfg is None:
        # Cannot check remaining components without a chrome config
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: request is "launch" (0.15 points)
    try:
        request_val = chrome_cfg.get('request')
        if request_val == 'launch':
            print(f"PASS: Component 2 — request is 'launch' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — expected request 'launch', found '{request_val}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: url is "http://localhost:3000" (0.15 points)
    try:
        url_val = chrome_cfg.get('url')
        if url_val == 'http://localhost:3000':
            print(f"PASS: Component 3 — url is 'http://localhost:3000' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — expected url 'http://localhost:3000', found '{url_val}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: webRoot is "${workspaceFolder}/src" (0.20 points)
    try:
        webroot_val = chrome_cfg.get('webRoot')
        expected_webroot = "$" + "{workspaceFolder}/src"
        if webroot_val == expected_webroot:
            print("PASS: Component 4 — webRoot is correct (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — expected webRoot '{expected_webroot}', found '{webroot_val}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: port is 9222 (0.20 points)
    try:
        port_val = chrome_cfg.get('port')
        if port_val == 9222:
            print(f"PASS: Component 5 — port is 9222 (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 5 — expected port 9222, found '{port_val}'")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: sourceMapPathOverrides has webpack mapping (0.15 points)
    try:
        overrides = chrome_cfg.get('sourceMapPathOverrides', {})
        if isinstance(overrides, dict):
            expected_key = 'webpack:///src/*'
            expected_val = "$" + "{webRoot}/*"
            actual_val = overrides.get(expected_key)
            if actual_val == expected_val:
                print("PASS: Component 6 — sourceMapPathOverrides has correct webpack mapping (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 6 — expected '{expected_key}': '{expected_val}', found: {overrides}")
        else:
            print(f"FAIL: Component 6 — sourceMapPathOverrides is not a dict: {overrides}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
