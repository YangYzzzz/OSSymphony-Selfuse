"""
Reward Script: Create .vscode/launch.json for Docker Node debugging
Task ID: vscode_gf3_027
Domain: vscode
Scoring:
  Component 1: File exists and is valid JSON with version + configurations array (0.15 pts)
  Component 2: Configuration named "Docker: Attach to Node" with type "node", request "attach" (0.20 pts)
  Component 3: Port is 9229 (0.15 pts)
  Component 4: localRoot is "${workspaceFolder}/backend/src" (0.20 pts)
  Component 5: remoteRoot is "/app/src" (0.15 pts)
  Component 6: restart is true (boolean) (0.15 pts)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_027'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'fullstack', '.vscode', 'launch.json')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be valid JSON
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0
    except json.JSONDecodeError as e:
        print(f"CRITICAL: Invalid JSON in {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid structure with "version" and "configurations" array (0.15 pts)
    try:
        has_version = "version" in data
        has_configs = isinstance(data.get("configurations"), list) and len(data["configurations"]) > 0
        if has_version and has_configs:
            print(f"PASS: Component 1 — version='{data['version']}', configurations has {len(data['configurations'])} entry/entries (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — version present: {has_version}, configurations is non-empty list: {has_configs}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Find the target configuration by name
    target_config = None
    configs = data.get("configurations", [])
    for cfg in configs:
        if isinstance(cfg, dict) and cfg.get("name") == "Docker: Attach to Node":
            target_config = cfg
            break

    # Component 2: Configuration named "Docker: Attach to Node" with type "node" and request "attach" (0.20 pts)
    try:
        if target_config is None:
            print(f"FAIL: Component 2 — No configuration named 'Docker: Attach to Node' found. Names found: {[c.get('name') for c in configs if isinstance(c, dict)]}")
        else:
            cfg_type = target_config.get("type")
            cfg_request = target_config.get("request")
            if cfg_type == "node" and cfg_request == "attach":
                print(f"PASS: Component 2 — name='Docker: Attach to Node', type='node', request='attach' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — type='{cfg_type}' (expected 'node'), request='{cfg_request}' (expected 'attach')")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Components 3-6 require the target config to exist
    if target_config is None:
        print("SKIP: Components 3-6 — target configuration not found")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 3: Port is 9229 (0.15 pts)
    try:
        port_val = target_config.get("port")
        if port_val == 9229:
            print(f"PASS: Component 3 — port=9229 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — port={port_val} (expected 9229)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: localRoot is "${workspaceFolder}/backend/src" (0.20 pts)
    try:
        local_root = target_config.get("localRoot")
        expected_local = "${workspaceFolder}/backend/src"
        if local_root == expected_local:
            print(f"PASS: Component 4 — localRoot='{local_root}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — localRoot='{local_root}' (expected '{expected_local}')")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: remoteRoot is "/app/src" (0.15 pts)
    try:
        remote_root = target_config.get("remoteRoot")
        expected_remote = "/app/src"
        if remote_root == expected_remote:
            print(f"PASS: Component 5 — remoteRoot='{remote_root}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — remoteRoot='{remote_root}' (expected '{expected_remote}')")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: restart is true (boolean True, not string) (0.15 pts)
    try:
        restart_val = target_config.get("restart")
        if restart_val is True:
            print(f"PASS: Component 6 — restart=True (boolean) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 — restart={restart_val!r} (expected boolean True)")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

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
