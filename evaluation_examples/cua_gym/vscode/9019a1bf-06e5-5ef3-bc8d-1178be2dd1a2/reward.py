"""
Reward Script: Go service project initialization with VSCode debug config
Task ID: vscode_gf4_004
Domain: vscode
Scoring:
  Component 1: go.mod exists with correct module path (0.25)
  Component 2: main.go exists, imports net/http, registers handler on "/" (0.35)
  Component 3: main.go listens on :8080 and returns "Hello, World!" (0.15)
  Component 4: .vscode/launch.json has Go debug launch config (0.25)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_004'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'go-service')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: go.mod exists with correct module path (0.25 points)
    try:
        go_mod_path = os.path.join(PROJECT_DIR, 'go.mod')
        if os.path.exists(go_mod_path):
            with open(go_mod_path, 'r') as f:
                content = f.read()
            # Check for correct module path
            if 'module github.com/user/go-service' in content:
                print(f"PASS: Component 1 -- go.mod has correct module path 'github.com/user/go-service' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 -- go.mod exists but module path is wrong. Content: {content[:200]}")
        else:
            print(f"FAIL: Component 1 -- go.mod not found at {go_mod_path}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: main.go exists, imports net/http, registers handler on "/" (0.35 points)
    try:
        main_go_path = os.path.join(PROJECT_DIR, 'main.go')
        if os.path.exists(main_go_path):
            with open(main_go_path, 'r') as f:
                content = f.read()

            has_net_http = '"net/http"' in content
            # Check for handler registration on "/" - various patterns
            has_handler = bool(re.search(r'(HandleFunc|Handle)\s*\(\s*["\']/', content))

            if has_net_http and has_handler:
                print(f"PASS: Component 2 -- main.go imports net/http and registers handler on '/' (0.35 pts)")
                total_score += 0.35
            else:
                missing = []
                if not has_net_http:
                    missing.append("net/http import")
                if not has_handler:
                    missing.append("handler on '/'")
                print(f"FAIL: Component 2 -- main.go missing: {', '.join(missing)}")
        else:
            print(f"FAIL: Component 2 -- main.go not found at {main_go_path}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: main.go listens on port 8080 and returns "Hello, World!" (0.15 points)
    try:
        main_go_path = os.path.join(PROJECT_DIR, 'main.go')
        if os.path.exists(main_go_path):
            with open(main_go_path, 'r') as f:
                content = f.read()

            has_port_8080 = bool(re.search(r'[:\"]8080', content))
            has_hello_world = 'Hello, World!' in content

            if has_port_8080 and has_hello_world:
                print(f"PASS: Component 3 -- main.go listens on :8080 and returns 'Hello, World!' (0.15 pts)")
                total_score += 0.15
            else:
                missing = []
                if not has_port_8080:
                    missing.append("port 8080")
                if not has_hello_world:
                    missing.append("'Hello, World!' response")
                print(f"FAIL: Component 3 -- main.go missing: {', '.join(missing)}")
        else:
            print(f"FAIL: Component 3 -- main.go not found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: .vscode/launch.json has Go debug launch config (0.25 points)
    try:
        launch_json_path = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')
        if os.path.exists(launch_json_path):
            with open(launch_json_path, 'r') as f:
                raw = f.read()
            # Strip JSONC comments before parsing
            cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
            data = json.loads(cleaned)

            configs = data.get('configurations', [])
            found_go_launch = False
            for cfg in configs:
                cfg_type = cfg.get('type', '').lower()
                cfg_request = cfg.get('request', '').lower()
                if cfg_type == 'go' and cfg_request == 'launch':
                    found_go_launch = True
                    break

            if found_go_launch:
                print(f"PASS: Component 4 -- launch.json has Go debug launch configuration (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 -- launch.json found but no config with type='go' and request='launch'. Configs: {configs}")
        else:
            print(f"FAIL: Component 4 -- launch.json not found at {launch_json_path}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
