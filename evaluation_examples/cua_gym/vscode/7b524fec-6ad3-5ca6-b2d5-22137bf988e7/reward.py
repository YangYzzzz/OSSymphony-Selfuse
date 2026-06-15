"""
Reward Script: Create launch.json for Streamlit debugging
Task ID: vscode_py_085
Domain: vscode
Scoring:
  Component 1 (0.20): launch.json exists in .vscode directory
  Component 2 (0.20): Valid JSON with version and configurations array
  Component 3 (0.20): Configuration uses "module": "streamlit"
  Component 4 (0.20): Args include "run" and "app.py"
  Component 5 (0.20): Args include "--server.port" and "8501"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_085'
PROJECT_DIR = os.path.join(WORKDIR, 'streamlit_project')
LAUNCH_JSON_PATH = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')


def verify_task():
    """
    Verify that a valid Streamlit debug launch.json has been created.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: launch.json exists in .vscode directory (0.20 points)
    try:
        if os.path.isfile(LAUNCH_JSON_PATH):
            print(f"PASS: Component 1 — launch.json exists at {LAUNCH_JSON_PATH} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — launch.json not found at {LAUNCH_JSON_PATH}")
            # No launch.json means nothing else can pass
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"REWARD: 0.0")
        return 0.0

    # Load the JSON content (needed for all subsequent checks)
    try:
        with open(LAUNCH_JSON_PATH, 'r') as f:
            content = f.read()
        # Handle JSONC (strip // comments)
        clean_content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        launch_data = json.loads(clean_content)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Valid JSON with version and configurations array (0.20 points)
    try:
        has_version = "version" in launch_data
        has_configs = isinstance(launch_data.get("configurations"), list) and len(launch_data["configurations"]) > 0
        if has_version and has_configs:
            print(f"PASS: Component 2 — Valid JSON with version='{launch_data.get('version')}' and {len(launch_data['configurations'])} configuration(s) (0.20 pts)")
            total_score += 0.20
        else:
            missing = []
            if not has_version:
                missing.append("version field")
            if not has_configs:
                missing.append("non-empty configurations array")
            print(f"FAIL: Component 2 — Missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Find the Streamlit debug configuration (look through all configs)
    configs = launch_data.get("configurations", [])
    streamlit_config = None
    for cfg in configs:
        # Match any config that uses module streamlit
        if isinstance(cfg, dict) and cfg.get("module") == "streamlit":
            streamlit_config = cfg
            break

    # If no config with module=streamlit, also check for one with "streamlit" in name
    if streamlit_config is None:
        for cfg in configs:
            if isinstance(cfg, dict):
                name = str(cfg.get("name", "")).lower()
                if "streamlit" in name:
                    streamlit_config = cfg
                    break

    # Fallback: use first config if only one exists
    if streamlit_config is None and len(configs) == 1:
        streamlit_config = configs[0]

    if streamlit_config is None:
        print(f"FAIL: No Streamlit-related configuration found in launch.json")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 3: Configuration uses "module": "streamlit" (0.20 points)
    try:
        module_val = streamlit_config.get("module")
        if module_val == "streamlit":
            print(f"PASS: Component 3 — Configuration uses \"module\": \"streamlit\" (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Expected \"module\": \"streamlit\", found module={module_val!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Args include "run" and "app.py" (0.20 points)
    try:
        args = streamlit_config.get("args", [])
        if not isinstance(args, list):
            args = []
        has_run = "run" in args
        has_app_py = "app.py" in args
        if has_run and has_app_py:
            print(f"PASS: Component 4 — Args contain 'run' and 'app.py': {args} (0.20 pts)")
            total_score += 0.20
        else:
            missing = []
            if not has_run:
                missing.append("'run'")
            if not has_app_py:
                missing.append("'app.py'")
            print(f"FAIL: Component 4 — Args missing {', '.join(missing)}. Found args={args}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Args include "--server.port" and "8501" (0.20 points)
    try:
        args = streamlit_config.get("args", [])
        if not isinstance(args, list):
            args = []
        has_port_flag = "--server.port" in args
        has_port_val = "8501" in args
        if has_port_flag and has_port_val:
            print(f"PASS: Component 5 — Args contain '--server.port' and '8501': {args} (0.20 pts)")
            total_score += 0.20
        else:
            missing = []
            if not has_port_flag:
                missing.append("'--server.port'")
            if not has_port_val:
                missing.append("'8501'")
            print(f"FAIL: Component 5 — Args missing {', '.join(missing)}. Found args={args}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
