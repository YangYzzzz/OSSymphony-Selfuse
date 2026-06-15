"""
Reward Script: Create launch.json for remote debugging Python via SSH
Task ID: vscode_td_057
Domain: vscode
Scoring:
  Component 1 (0.15): launch.json exists and is valid JSON with configurations array
  Component 2 (0.20): Configuration has type "debugpy" and request "attach"
  Component 3 (0.25): connect block has host "192.168.1.100" and port 5678
  Component 4 (0.20): pathMappings with localRoot "${workspaceFolder}" and remoteRoot "/app"
  Component 5 (0.20): Configuration has a non-empty name field
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_057'

LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'remote-debug', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load JSON file, stripping // comments (VSCode JSONC format)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_attach_config(configs):
    """Find the first configuration with request 'attach'."""
    for cfg in configs:
        if isinstance(cfg, dict) and cfg.get('request') == 'attach':
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

    # Component 1: launch.json is valid JSON with configurations array (0.15 points)
    data = None
    configs = None
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
        configs = data.get('configurations', [])
        if isinstance(configs, list) and len(configs) > 0:
            print(f"PASS: Component 1 -- launch.json is valid JSON with {len(configs)} configuration(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- 'configurations' is empty or not a list: {type(configs)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the relevant attach configuration
    cfg = find_attach_config(configs)
    if cfg is None:
        # Fallback: use first config
        cfg = configs[0] if configs else {}

    # Component 2: type is "debugpy" and request is "attach" (0.20 points)
    try:
        cfg_type = cfg.get('type', '')
        cfg_request = cfg.get('request', '')
        if cfg_type == 'debugpy' and cfg_request == 'attach':
            print(f"PASS: Component 2 -- type='debugpy', request='attach' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 -- Expected type='debugpy' and request='attach', found type='{cfg_type}', request='{cfg_request}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: connect block has host "192.168.1.100" and port 5678 (0.25 points)
    try:
        connect = cfg.get('connect', {})
        if isinstance(connect, dict):
            host = connect.get('host', '')
            port = connect.get('port', None)
            if host == '192.168.1.100' and port == 5678:
                print(f"PASS: Component 3 -- connect.host='192.168.1.100', connect.port=5678 (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- Expected host='192.168.1.100' port=5678, found host='{host}' port={port}")
        else:
            print(f"FAIL: Component 3 -- 'connect' is not a dict: {type(connect)}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: pathMappings with localRoot "${workspaceFolder}" and remoteRoot "/app" (0.20 points)
    try:
        path_mappings = cfg.get('pathMappings', [])
        if isinstance(path_mappings, list) and len(path_mappings) > 0:
            found_mapping = False
            for mapping in path_mappings:
                local_root = mapping.get('localRoot', '')
                remote_root = mapping.get('remoteRoot', '')
                if '${workspaceFolder}' in local_root and remote_root == '/app':
                    found_mapping = True
                    break
            if found_mapping:
                print(f"PASS: Component 4 -- pathMappings has localRoot='${{workspaceFolder}}', remoteRoot='/app' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 -- pathMappings entries don't match expected values: {path_mappings}")
        else:
            print(f"FAIL: Component 4 -- pathMappings missing or empty: {path_mappings}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Configuration has a non-empty name field (0.20 points)
    try:
        name = cfg.get('name', '')
        if isinstance(name, str) and len(name.strip()) > 0:
            print(f"PASS: Component 5 -- Configuration name='{name}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 5 -- Configuration has no name or empty name: '{name}'")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
