"""
Reward Script: Create launch.json with Node.js backend and Chrome frontend debug configurations
Task ID: vscode_td_055
Domain: vscode
Scoring:
  Component 1: launch.json exists and is valid JSON with version and configurations array (0.15)
  Component 2: Node.js backend config present with correct type/program (0.35)
  Component 3: Chrome frontend config present with correct type/url/webRoot (0.35)
  Component 4: Both configs have proper request field and names (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_055'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'fullstack', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments) by stripping comments first."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (but not URLs like http://)
    # Only strip // comments that are NOT inside strings
    # Simpler approach: try plain JSON first, then strip comments as fallback
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    # Fallback: strip comments line by line (outside of strings)
    lines = content.split('\n')
    cleaned = []
    for line in lines:
        # Simple heuristic: strip trailing // comments not inside quotes
        in_string = False
        result = []
        i = 0
        while i < len(line):
            c = line[i]
            if c == '"' and (i == 0 or line[i-1] != '\\'):
                in_string = not in_string
                result.append(c)
            elif not in_string and c == '/' and i + 1 < len(line) and line[i+1] == '/':
                break  # rest of line is comment
            else:
                result.append(c)
            i += 1
        cleaned.append(''.join(result))
    return json.loads('\n'.join(cleaned))


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

    # Precondition: launch.json must be valid JSON(C)
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    configs = data.get("configurations", [])

    # Component 1: launch.json has version and a configurations array with exactly 2 entries (0.15 points)
    try:
        has_version = "version" in data
        has_configs = isinstance(configs, list) and len(configs) == 2
        if has_version and has_configs:
            print(f"PASS: Component 1 - launch.json has version and 2 configurations (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - version present: {has_version}, configs count: {len(configs) if isinstance(configs, list) else 'not a list'}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Node.js backend configuration (0.35 points)
    try:
        node_config = None
        for cfg in configs:
            cfg_type = str(cfg.get("type", "")).lower()
            if cfg_type == "node":
                node_config = cfg
                break

        if node_config is not None:
            program = str(node_config.get("program", ""))
            # The program should reference src/server.js (with or without ${workspaceFolder} prefix)
            program_ok = "src/server.js" in program
            if program_ok:
                print(f"PASS: Component 2 - Node.js config found with program='{program}' (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 - Node.js config found but program='{program}', expected path containing 'src/server.js'")
        else:
            print(f"FAIL: Component 2 - No configuration with type 'node' found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Chrome frontend configuration (0.35 points)
    try:
        chrome_config = None
        for cfg in configs:
            cfg_type = str(cfg.get("type", "")).lower()
            if cfg_type == "chrome":
                chrome_config = cfg
                break

        if chrome_config is not None:
            url = str(chrome_config.get("url", ""))
            web_root = str(chrome_config.get("webRoot", ""))
            url_ok = url == "http://localhost:3000"
            webroot_ok = "public" in web_root  # should contain ${workspaceFolder}/public or similar
            if url_ok and webroot_ok:
                print(f"PASS: Component 3 - Chrome config with url='{url}', webRoot='{web_root}' (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 3 - Chrome config found but url='{url}' (expected 'http://localhost:3000'), webRoot='{web_root}' (expected path with 'public')")
        else:
            print(f"FAIL: Component 3 - No configuration with type 'chrome' found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Both configs have proper request fields and names (0.15 points)
    try:
        points_earned = 0.0
        # Node config should have request "launch"
        if node_config is not None:
            node_request = str(node_config.get("request", "")).lower()
            node_name = node_config.get("name", "")
            if node_request == "launch" and node_name:
                points_earned += 0.075
                print(f"PASS: Component 4a - Node config has request='{node_request}', name='{node_name}'")
            else:
                print(f"FAIL: Component 4a - Node config request='{node_request}' (expected 'launch'), name='{node_name}'")
        else:
            print(f"FAIL: Component 4a - No node config to check request/name")

        # Chrome config should have request "launch"
        if chrome_config is not None:
            chrome_request = str(chrome_config.get("request", "")).lower()
            chrome_name = chrome_config.get("name", "")
            if chrome_request == "launch" and chrome_name:
                points_earned += 0.075
                print(f"PASS: Component 4b - Chrome config has request='{chrome_request}', name='{chrome_name}'")
            else:
                print(f"FAIL: Component 4b - Chrome config request='{chrome_request}' (expected 'launch'), name='{chrome_name}'")
        else:
            print(f"FAIL: Component 4b - No chrome config to check request/name")

        if points_earned > 0:
            total_score += points_earned
            print(f"PASS: Component 4 - request/name checks ({points_earned} pts)")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
