"""
Reward Script: Next.js server-side debug configuration
Task ID: vscode_web_044
Domain: vscode
Scoring:
  - Component 1 (0.20): launch.json exists with config named 'Next.js: debug server-side'
  - Component 2 (0.20): Config type is 'node' with request 'attach'
  - Component 3 (0.20): Config specifies port 9229 for Node inspector
  - Component 4 (0.15): Config has sourceMapPathOverrides for webpack/Next.js
  - Component 5 (0.25): package.json has debug script with NODE_OPTIONS='--inspect' and next dev
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'next-app')
LAUNCH_JSON = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')
PACKAGE_JSON = os.path.join(PROJECT_DIR, 'package.json')
TASK_ID = 'vscode_web_044'


def load_jsonc(path):
    """Load a JSON or JSONC file, stripping // comments outside strings."""
    with open(path, 'r') as f:
        content = f.read()
    # First try direct JSON parse
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    # Fallback: strip lines that are comment-only (start with optional whitespace then //)
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('//'):
            continue
        cleaned_lines.append(line)
    return json.loads('\n'.join(cleaned_lines))


def find_debug_config(launch_data):
    """Find the 'Next.js: debug server-side' configuration in launch.json."""
    configs = launch_data.get('configurations', [])
    for cfg in configs:
        name = cfg.get('name', '')
        if 'next' in name.lower() and 'debug' in name.lower() and 'server' in name.lower():
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
        launch_data = load_jsonc(LAUNCH_JSON)
    except FileNotFoundError:
        print(f"CRITICAL: launch.json not found at {LAUNCH_JSON}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the relevant debug configuration
    config = find_debug_config(launch_data)

    # Component 1: launch.json has a config named 'Next.js: debug server-side' (0.20 points)
    try:
        if config is not None:
            print(f"PASS: Component 1 -- Found debug config named '{config.get('name')}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 -- No config with Next.js debug server-side name found in launch.json")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Config has type 'node' and request 'attach' (0.20 points)
    try:
        if config is not None:
            cfg_type = config.get('type', '')
            cfg_request = config.get('request', '')
            if cfg_type == 'node' and cfg_request == 'attach':
                print(f"PASS: Component 2 -- type='node', request='attach' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 -- Expected type='node' request='attach', found type='{cfg_type}' request='{cfg_request}'")
        else:
            print(f"FAIL: Component 2 -- No matching debug config found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Config has port 9229 (0.20 points)
    try:
        if config is not None:
            port = config.get('port')
            if port == 9229:
                print(f"PASS: Component 3 -- port=9229 (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 -- Expected port=9229, found port={port}")
        else:
            print(f"FAIL: Component 3 -- No matching debug config found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Config has sourceMapPathOverrides for webpack/Next.js (0.15 points)
    try:
        if config is not None:
            overrides = config.get('sourceMapPathOverrides', {})
            # Check for any webpack-related key in the overrides
            has_webpack = any('webpack' in k.lower() for k in overrides.keys())
            if has_webpack and len(overrides) > 0:
                print(f"PASS: Component 4 -- sourceMapPathOverrides has webpack mapping: {overrides} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 -- sourceMapPathOverrides missing or no webpack key, found: {overrides}")
        else:
            print(f"FAIL: Component 4 -- No matching debug config found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: package.json has a debug script with NODE_OPTIONS='--inspect' and next dev (0.25 points)
    try:
        with open(PACKAGE_JSON, 'r') as f:
            pkg = json.load(f)
        scripts = pkg.get('scripts', {})
        # Look for any script that contains both --inspect and next dev
        matching = [(n, c) for n, c in scripts.items()
                     if '--inspect' in c and 'next' in c.lower() and 'dev' in c.lower()]
        if matching:
            sname, scmd = matching[0]
            print(f"PASS: Component 5 -- Found script '{sname}': '{scmd}' with --inspect and next dev (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 5 -- No script with --inspect and 'next dev' found. Scripts: {scripts}")
    except FileNotFoundError:
        print(f"FAIL: Component 5 -- package.json not found at {PACKAGE_JSON}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
