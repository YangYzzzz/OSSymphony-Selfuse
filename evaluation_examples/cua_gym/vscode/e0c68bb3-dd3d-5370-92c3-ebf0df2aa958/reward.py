"""
Reward Script: Create launch.json for Docker Node.js attach debugging
Task ID: vscode_td_084
Domain: vscode
Scoring:
  Component 1: launch.json exists and is valid JSON with configurations array (0.15)
  Component 2: request is "attach" (0.20)
  Component 3: port is 9229 (0.20)
  Component 4: remoteRoot is "/app" (0.20)
  Component 5: localRoot is "${workspaceFolder}" (0.15)
  Component 6: type is "node" (0.10)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_084'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'dockerized-node')
LAUNCH_JSON_PATH = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: launch.json must exist and be parseable
    if not os.path.exists(LAUNCH_JSON_PATH):
        print(f"CRITICAL: launch.json not found at {LAUNCH_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(LAUNCH_JSON_PATH, 'r') as f:
            content = f.read()
        # Handle JSONC (strip comments)
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
        data = json.loads(cleaned)
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid structure with configurations array (0.15 points)
    try:
        configs = data.get('configurations', None)
        if isinstance(configs, list) and len(configs) > 0:
            print(f"PASS: Component 1 -- launch.json has {len(configs)} configuration(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- 'configurations' missing or empty, found: {type(configs)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Find the attach configuration (look through all configs for one matching attach/node)
    config = None
    if isinstance(data.get('configurations'), list):
        for c in data['configurations']:
            if isinstance(c, dict) and c.get('request') == 'attach':
                config = c
                break
        # Fallback: just use first config if no attach found
        if config is None and len(data['configurations']) > 0:
            config = data['configurations'][0]

    if config is None:
        print("CRITICAL: No configuration entry found in launch.json")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: request is "attach" (0.20 points)
    try:
        req = config.get('request', None)
        if req == 'attach':
            print(f"PASS: Component 2 -- request is 'attach' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 -- expected request='attach', found: {req!r}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: port is 9229 (0.20 points)
    try:
        port = config.get('port', None)
        if port == 9229:
            print(f"PASS: Component 3 -- port is 9229 (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 -- expected port=9229, found: {port!r}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: remoteRoot is "/app" (0.20 points)
    try:
        remote_root = config.get('remoteRoot', None)
        if remote_root == '/app':
            print(f"PASS: Component 4 -- remoteRoot is '/app' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 -- expected remoteRoot='/app', found: {remote_root!r}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: localRoot is "${workspaceFolder}" (0.15 points)
    try:
        local_root = config.get('localRoot', None)
        if local_root == '${workspaceFolder}':
            print(f"PASS: Component 5 -- localRoot is '${{workspaceFolder}}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 -- expected localRoot='${{workspaceFolder}}', found: {local_root!r}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: type is "node" (0.10 points)
    try:
        node_type = config.get('type', None)
        if node_type == 'node':
            print(f"PASS: Component 6 -- type is 'node' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 -- expected type='node', found: {node_type!r}")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
