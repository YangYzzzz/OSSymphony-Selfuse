"""
Reward Script: Go REST API project setup in VSCode
Task ID: vscode_gf4_013
Domain: vscode
Scoring:
  Component 1 (0.15): go.mod with correct module declaration
  Component 2 (0.30): handlers.go with ProductHandler, GetAll, GetByID returning JSON
  Component 3 (0.25): main.go imports handlers and registers HTTP routes
  Component 4 (0.15): .vscode/launch.json with Go debug configuration
  Component 5 (0.15): .vscode/tasks.json with build and test tasks
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_013'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'go-rest-api')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: go.mod exists with correct module declaration (0.15 points)
    try:
        gomod_path = os.path.join(PROJECT_DIR, 'go.mod')
        if os.path.exists(gomod_path):
            with open(gomod_path, 'r') as f:
                gomod_content = f.read()
            # Must contain module declaration for github.com/user/go-rest-api
            if 'module github.com/user/go-rest-api' in gomod_content:
                print(f"PASS: Component 1 — go.mod has correct module path (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — go.mod missing correct module declaration. Content: {gomod_content[:200]}")
        else:
            print(f"FAIL: Component 1 — go.mod does not exist at {gomod_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: handlers.go with ProductHandler struct, GetAll, GetByID methods (0.30 points)
    try:
        handlers_path = os.path.join(PROJECT_DIR, 'internal', 'handlers', 'handlers.go')
        if os.path.exists(handlers_path):
            with open(handlers_path, 'r') as f:
                handlers_content = f.read()

            # 2a: package declaration is "handlers"
            if re.search(r'^\s*package\s+handlers\s*$', handlers_content, re.MULTILINE):
                # 2b: ProductHandler struct defined
                if re.search(r'type\s+ProductHandler\s+struct\s*\{', handlers_content):
                    total_score += 0.10
                    print(f"PASS: Component 2a — ProductHandler struct found (0.10 pts)")
                else:
                    print(f"FAIL: Component 2a — ProductHandler struct not found")

                # 2c: GetAll method on ProductHandler writing JSON
                if re.search(r'func\s*\(\s*\w+\s+\*?ProductHandler\s*\)\s*GetAll\s*\(', handlers_content):
                    if 'encoding/json' in handlers_content:
                        total_score += 0.10
                        print(f"PASS: Component 2b — GetAll method with JSON encoding found (0.10 pts)")
                    else:
                        print(f"FAIL: Component 2b — GetAll method exists but no JSON encoding import")
                else:
                    print(f"FAIL: Component 2b — GetAll method not found on ProductHandler")

                # 2d: GetByID method on ProductHandler writing JSON
                if re.search(r'func\s*\(\s*\w+\s+\*?ProductHandler\s*\)\s*GetByID\s*\(', handlers_content):
                    total_score += 0.10
                    print(f"PASS: Component 2c — GetByID method found (0.10 pts)")
                else:
                    print(f"FAIL: Component 2c — GetByID method not found on ProductHandler")
            else:
                print(f"FAIL: Component 2 — package is not 'handlers'")
        else:
            print(f"FAIL: Component 2 — handlers.go does not exist at {handlers_path}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: main.go imports handlers and registers HTTP routes (0.25 points)
    try:
        main_path = os.path.join(PROJECT_DIR, 'main.go')
        if os.path.exists(main_path):
            with open(main_path, 'r') as f:
                main_content = f.read()

            # 3a: package main declaration
            if re.search(r'^\s*package\s+main\s*$', main_content, re.MULTILINE):
                # 3b: imports the handlers package
                if re.search(r'"github\.com/user/go-rest-api/internal/handlers"', main_content):
                    total_score += 0.10
                    print(f"PASS: Component 3a — main.go imports handlers package (0.10 pts)")
                else:
                    print(f"FAIL: Component 3a — main.go does not import handlers package")

                # 3c: registers HTTP routes using net/http
                if '"net/http"' in main_content:
                    # Check for route registration patterns (HandleFunc, Handle, etc.)
                    if re.search(r'http\.(HandleFunc|Handle)\s*\(', main_content):
                        total_score += 0.10
                        print(f"PASS: Component 3b — HTTP routes registered via net/http (0.10 pts)")
                    else:
                        print(f"FAIL: Component 3b — net/http imported but no route registration found")
                else:
                    print(f"FAIL: Component 3b — net/http not imported in main.go")

                # 3d: has a main function
                if re.search(r'func\s+main\s*\(\s*\)', main_content):
                    total_score += 0.05
                    print(f"PASS: Component 3c — main function defined (0.05 pts)")
                else:
                    print(f"FAIL: Component 3c — main function not found")
            else:
                print(f"FAIL: Component 3 — package is not 'main'")
        else:
            print(f"FAIL: Component 3 — main.go does not exist at {main_path}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: .vscode/launch.json with Go debug configuration (0.15 points)
    try:
        launch_path = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')
        if os.path.exists(launch_path):
            with open(launch_path, 'r') as f:
                content = f.read()
            # Strip JSONC comments
            cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            launch_data = json.loads(cleaned)

            configs = launch_data.get('configurations', [])
            # Find a Go debug configuration
            go_debug_configs = [
                cfg for cfg in configs
                if str(cfg.get('type', '')).lower() == 'go'
                and str(cfg.get('request', '')).lower() == 'launch'
            ]

            if len(go_debug_configs) > 0:
                print(f"PASS: Component 4 — launch.json has Go debug config (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — launch.json exists but no Go debug config (type=go, request=launch)")
        else:
            print(f"FAIL: Component 4 — launch.json does not exist at {launch_path}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: .vscode/tasks.json with build and test tasks (0.15 points)
    try:
        tasks_path = os.path.join(PROJECT_DIR, '.vscode', 'tasks.json')
        if os.path.exists(tasks_path):
            with open(tasks_path, 'r') as f:
                content = f.read()
            # Strip JSONC comments
            cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            tasks_data = json.loads(cleaned)

            tasks = tasks_data.get('tasks', [])
            task_labels = [t.get('label', '').lower() for t in tasks]
            task_commands = [str(t.get('command', '')).lower() for t in tasks]

            def _is_build_task(t):
                label = str(t.get('label', '')).lower()
                command = str(t.get('command', '')).lower()
                group = t.get('group', {})
                gk = str(group.get('kind', '')).lower() if isinstance(group, dict) else str(group).lower()
                return ('build' in label or 'build' in command or gk == 'build') and 'go' in command

            def _is_test_task(t):
                label = str(t.get('label', '')).lower()
                command = str(t.get('command', '')).lower()
                group = t.get('group', {})
                gk = str(group.get('kind', '')).lower() if isinstance(group, dict) else str(group).lower()
                return ('test' in label or 'test' in command or gk == 'test') and 'go' in command

            if any(_is_build_task(t) for t in tasks):
                total_score += 0.075
                print(f"PASS: Component 5a — build task found (0.075 pts)")
            else:
                print(f"FAIL: Component 5a — no build task found. Labels: {task_labels}, Commands: {task_commands}")

            if any(_is_test_task(t) for t in tasks):
                total_score += 0.075
                print(f"PASS: Component 5b — test task found (0.075 pts)")
            else:
                print(f"FAIL: Component 5b — no test task found. Labels: {task_labels}, Commands: {task_commands}")
        else:
            print(f"FAIL: Component 5 — tasks.json does not exist at {tasks_path}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
