"""
Reward Script: Configure Chrome debugging launch configuration for React/Vite dev server
Task ID: vscode_web_022
Domain: vscode
Scoring:
  Component 1 — launch.json exists and is valid JSON with configurations array (0.15)
  Component 2 — Configuration named 'Debug in Chrome' exists (0.15)
  Component 3 — type is 'chrome' and request is 'launch' (0.20)
  Component 4 — url is 'http://localhost:5173' (0.20)
  Component 5 — webRoot is '${workspaceFolder}/src' (0.15)
  Component 6 — sourceMaps is enabled (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_022'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'react-app')
LAUNCH_JSON_PATH = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments). Try strict JSON first, then strip comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Try direct parse first (handles well-formed JSON without comments)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    # Fallback: strip comments outside of strings using a simple state machine
    result = []
    i = 0
    in_string = False
    while i < len(content):
        ch = content[i]
        if in_string:
            result.append(ch)
            if ch == '\\':
                # Skip escaped character
                i += 1
                if i < len(content):
                    result.append(content[i])
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
                result.append(ch)
            elif ch == '/' and i + 1 < len(content) and content[i + 1] == '/':
                # Single-line comment: skip to end of line
                while i < len(content) and content[i] != '\n':
                    i += 1
                continue
            elif ch == '/' and i + 1 < len(content) and content[i + 1] == '*':
                # Multi-line comment: skip to */
                i += 2
                while i + 1 < len(content) and not (content[i] == '*' and content[i + 1] == '/'):
                    i += 1
                i += 2
                continue
            else:
                result.append(ch)
        i += 1
    return json.loads(''.join(result))


def find_config_by_name(configurations, name):
    """Find a configuration entry by its 'name' field (case-insensitive)."""
    for cfg in configurations:
        if isinstance(cfg, dict) and cfg.get('name', '').lower() == name.lower():
            return cfg
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: launch.json must exist and be parseable
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
    except FileNotFoundError:
        print(f"CRITICAL: launch.json not found at {LAUNCH_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: launch.json has a valid 'configurations' array (0.15 points)
    try:
        configurations = data.get('configurations', None)
        if isinstance(configurations, list) and len(configurations) > 0:
            print(f"PASS: Component 1 — launch.json has {len(configurations)} configuration(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — 'configurations' missing or empty: {configurations}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if not isinstance(configurations, list) or len(configurations) == 0:
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: A configuration named 'Debug in Chrome' exists (0.15 points)
    config = None
    try:
        config = find_config_by_name(configurations, 'Debug in Chrome')
        if config is not None:
            print(f"PASS: Component 2 — Found configuration named 'Debug in Chrome' (0.15 pts)")
            total_score += 0.15
        else:
            names = [c.get('name', '<no name>') for c in configurations if isinstance(c, dict)]
            print(f"FAIL: Component 2 — No configuration named 'Debug in Chrome'. Found: {names}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    if config is None:
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 3: type is 'chrome' and request is 'launch' (0.20 points)
    try:
        cfg_type = config.get('type', '')
        cfg_request = config.get('request', '')
        if cfg_type == 'chrome' and cfg_request == 'launch':
            print(f"PASS: Component 3 — type='chrome', request='launch' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Expected type='chrome' request='launch', found type='{cfg_type}' request='{cfg_request}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: url is 'http://localhost:5173' (0.20 points)
    try:
        cfg_url = config.get('url', '')
        if cfg_url == 'http://localhost:5173':
            print(f"PASS: Component 4 — url='http://localhost:5173' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Expected url='http://localhost:5173', found '{cfg_url}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: webRoot is '${workspaceFolder}/src' (0.15 points)
    try:
        cfg_webroot = config.get('webRoot', '')
        if cfg_webroot == '${workspaceFolder}/src':
            print(f"PASS: Component 5 — webRoot='${{workspaceFolder}}/src' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — Expected webRoot='${{workspaceFolder}}/src', found '{cfg_webroot}'")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: sourceMaps is enabled (true) (0.15 points)
    try:
        cfg_sourcemaps = config.get('sourceMaps', None)
        if cfg_sourcemaps is True:
            print(f"PASS: Component 6 — sourceMaps=true (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 — Expected sourceMaps=true, found {cfg_sourcemaps}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
