"""
Reward Script: Configure Go development in VSCode
Task ID: vscode_gf5_041
Domain: vscode
Scoring:
  Component 1: Go extension installed (0.15 pts)
  Component 2: go.mod with correct module name (0.20 pts)
  Component 3: main.go with HTTP handler (0.35 pts)
  Component 4: .vscode/launch.json with Go debug config (0.30 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'go-server')


def verify_task():
    """
    Verify Go development setup in VSCode.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Go extension is installed in VSCode (0.15 points)
    # Check the extensions directory on disk for a golang.go-* folder
    try:
        ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
        entries = os.listdir(ext_dir) if os.path.isdir(ext_dir) else []
        go_ext_matches = [e for e in entries if e.lower().startswith('golang.go')]
        if len(go_ext_matches) > 0:
            print(f"PASS: Component 1 — Go extension found: {go_ext_matches[0]} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Go extension not found in {ext_dir}. Entries: {entries}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: go.mod exists with module name 'example.com/server' (0.20 points)
    try:
        gomod_path = os.path.join(PROJECT_DIR, 'go.mod')
        if os.path.exists(gomod_path):
            with open(gomod_path, 'r') as f:
                gomod_content = f.read()
            # Check for module declaration with the correct name
            if re.search(r'module\s+example\.com/server', gomod_content):
                print(f"PASS: Component 2 — go.mod has module example.com/server (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — go.mod exists but module name is wrong. Content: {gomod_content[:200]}")
        else:
            print(f"FAIL: Component 2 — go.mod not found at {gomod_path}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: main.go exists with HTTP handler (http.HandleFunc + http.ListenAndServe) (0.35 points)
    # Sub-scores: file exists with package main (0.05), has http.HandleFunc (0.15), has http.ListenAndServe (0.15)
    try:
        main_go_path = os.path.join(PROJECT_DIR, 'main.go')
        if os.path.exists(main_go_path):
            with open(main_go_path, 'r') as f:
                main_content = f.read()

            has_handle_func = 'http.HandleFunc' in main_content or 'http.Handle(' in main_content
            has_listen_serve = 'http.ListenAndServe' in main_content

            if has_handle_func and has_listen_serve:
                print(f"PASS: Component 3 — main.go has http.HandleFunc and http.ListenAndServe (0.35 pts)")
                total_score += 0.35
            elif has_handle_func or has_listen_serve:
                # Partial credit: has one of the two
                print(f"PARTIAL: Component 3 — main.go has {'HandleFunc' if has_handle_func else 'ListenAndServe'} but missing {'ListenAndServe' if has_handle_func else 'HandleFunc'} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — main.go exists but missing HTTP handler code")
        else:
            print(f"FAIL: Component 3 — main.go not found at {main_go_path}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: .vscode/launch.json with Go debug configuration (0.30 points)
    # Sub-checks: file exists and is valid JSON (0.05), has a Go-type configuration (0.25)
    try:
        launch_json_path = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')
        if os.path.exists(launch_json_path):
            with open(launch_json_path, 'r') as f:
                raw = f.read()
            # Strip JSONC comments (// style)
            cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
            launch_config = json.loads(cleaned)

            configurations = launch_config.get('configurations', [])
            # Look for a Go debug configuration: type "go" and request "launch"
            go_configs = [c for c in configurations
                          if str(c.get('type', '')).lower() == 'go'
                          and str(c.get('request', '')).lower() == 'launch']

            if len(go_configs) > 0:
                print(f"PASS: Component 4 — launch.json has Go debug configuration (type=go, request=launch) (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 4 — launch.json exists but no Go debug config found. Configs: {configurations}")
        else:
            print(f"FAIL: Component 4 — launch.json not found at {launch_json_path}")
    except json.JSONDecodeError as e:
        print(f"ERROR: Component 4 — launch.json is not valid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
