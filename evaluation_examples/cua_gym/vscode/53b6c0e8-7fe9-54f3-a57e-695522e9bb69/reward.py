"""
Reward Script: Create launch.json with compound debug configuration
Task ID: vscode_td_056
Domain: vscode
Scoring:
  Component 1 (0.15): launch.json exists and is valid JSON with version field
  Component 2 (0.25): "Server" config with type=node, program=${workspaceFolder}/server/index.js
  Component 3 (0.25): "Client" config with type=chrome, url=http://localhost:3000
  Component 4 (0.35): "Full Stack" compound referencing both Server and Client
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_056'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'webapp', '.vscode', 'launch.json')


def load_jsonc(file_path):
    """Load a JSON or JSONC file (strips // comments carefully)."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Try plain JSON first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    # Fallback: strip single-line comments that are NOT inside strings
    # Only strip // at start of line (possibly with leading whitespace)
    content_stripped = re.sub(r'^\s*//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content_stripped, strict=False)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: launch.json exists and is valid JSON with version (0.15 points)
    try:
        if not os.path.exists(LAUNCH_JSON_PATH):
            print(f"FAIL: Component 1 — launch.json not found at {LAUNCH_JSON_PATH}")
            print("REWARD: 0.0")
            return 0.0

        data = load_jsonc(LAUNCH_JSON_PATH)

        if isinstance(data, dict) and "version" in data:
            print(f"PASS: Component 1 — launch.json is valid JSON with version={data['version']} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — launch.json missing 'version' field or not a dict")
    except Exception as e:
        print(f"ERROR: Component 1 — Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get configurations list for components 2 and 3
    configurations = data.get("configurations", [])
    if not isinstance(configurations, list):
        configurations = []

    # Build a lookup by config name
    config_by_name = {}
    for cfg in configurations:
        if isinstance(cfg, dict) and "name" in cfg:
            config_by_name[cfg["name"]] = cfg

    # Component 2: "Server" configuration with type=node and correct program (0.25 points)
    try:
        server_cfg = config_by_name.get("Server")
        if server_cfg is not None:
            server_type = server_cfg.get("type", "")
            server_program = server_cfg.get("program", "")
            type_ok = server_type == "node"
            program_ok = server_program == "${workspaceFolder}/server/index.js"

            if type_ok and program_ok:
                print(f"PASS: Component 2 — Server config: type={server_type}, program={server_program} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — Server config issues: type={server_type} (expect node), program={server_program} (expect ${{workspaceFolder}}/server/index.js)")
        else:
            print(f"FAIL: Component 2 — No configuration named 'Server' found. Available: {list(config_by_name.keys())}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: "Client" configuration with type=chrome and correct url (0.25 points)
    try:
        client_cfg = config_by_name.get("Client")
        if client_cfg is not None:
            client_type = client_cfg.get("type", "")
            client_url = client_cfg.get("url", "")
            type_ok = client_type == "chrome"
            url_ok = client_url == "http://localhost:3000"

            if type_ok and url_ok:
                print(f"PASS: Component 3 — Client config: type={client_type}, url={client_url} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Client config issues: type={client_type} (expect chrome), url={client_url} (expect http://localhost:3000)")
        else:
            print(f"FAIL: Component 3 — No configuration named 'Client' found. Available: {list(config_by_name.keys())}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: "Full Stack" compound referencing both Server and Client (0.35 points)
    try:
        compounds = data.get("compounds", [])
        if not isinstance(compounds, list):
            compounds = []

        compound_by_name = {}
        for comp in compounds:
            if isinstance(comp, dict) and "name" in comp:
                compound_by_name[comp["name"]] = comp

        full_stack = compound_by_name.get("Full Stack")
        if full_stack is not None:
            compound_configs = full_stack.get("configurations", [])
            if isinstance(compound_configs, list):
                has_server = "Server" in compound_configs
                has_client = "Client" in compound_configs

                if has_server and has_client:
                    print(f"PASS: Component 4 — 'Full Stack' compound references Server and Client: {compound_configs} (0.35 pts)")
                    total_score += 0.35
                else:
                    print(f"FAIL: Component 4 — 'Full Stack' compound missing references. Has Server={has_server}, Client={has_client}. Configs: {compound_configs}")
            else:
                print(f"FAIL: Component 4 — 'Full Stack' compound 'configurations' is not a list: {compound_configs}")
        else:
            print(f"FAIL: Component 4 — No compound named 'Full Stack' found. Available: {list(compound_by_name.keys())}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
