"""
Reward Script: VSCode Go Wire Dependency Injection Setup
Task ID: vscode_gf6_077
Domain: vscode
Scoring:
  Component 1: go.mod includes google/wire dependency (0.10)
  Component 2: wire binary installed (0.10)
  Component 3: 4 constructor Go files exist with correct functions (0.30)
  Component 4: wire.go with wireinject build tag and wire.Build (0.15)
  Component 5: wire_gen.go exists with InitializeApp (0.10)
  Component 6: main.go calls InitializeApp (0.10)
  Component 7: Makefile has wire target (0.075)
  Component 8: .vscode/tasks.json has Wire: Generate task (0.075)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'go-wire-di')
TASK_ID = 'vscode_gf6_077'


def read_file(path):
    """Read file content, return empty string if not found."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception:
        return ''


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: project directory exists
    if not os.path.isdir(PROJECT_DIR):
        print(f"CRITICAL: Project directory not found: {PROJECT_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: go.mod includes google/wire dependency (0.10 points)
    try:
        go_mod = read_file(os.path.join(PROJECT_DIR, 'go.mod'))
        if 'github.com/google/wire' in go_mod:
            print(f"PASS: Component 1 — go.mod contains google/wire dependency (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — go.mod does not contain google/wire dependency")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: wire binary installed (0.10 points)
    try:
        wire_path = os.path.join(WORKDIR, 'go', 'bin', 'wire')
        if os.path.isfile(wire_path) and os.access(wire_path, os.X_OK):
            print(f"PASS: Component 2 — wire binary found at {wire_path} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 — wire binary not found or not executable at {wire_path}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 4 constructor Go files with correct functions (0.30 points, 0.075 each)
    constructor_checks = [
        ('internal/db/db.go', 'NewDB', r'func\s+NewDB\s*\('),
        ('internal/repository/user_repo.go', 'NewUserRepository', r'func\s+NewUserRepository\s*\('),
        ('internal/service/user_service.go', 'NewUserService', r'func\s+NewUserService\s*\('),
        ('internal/handler/user_handler.go', 'NewUserHandler', r'func\s+NewUserHandler\s*\('),
    ]
    comp3_score = 0.0
    for rel_path, func_name, pattern in constructor_checks:
        try:
            full_path = os.path.join(PROJECT_DIR, rel_path)
            content = read_file(full_path)
            if content and re.search(pattern, content):
                print(f"PASS: Component 3 — {rel_path} contains {func_name} (0.075 pts)")
                comp3_score += 0.075
            else:
                print(f"FAIL: Component 3 — {rel_path} missing or no {func_name} function")
        except Exception as e:
            print(f"ERROR: Component 3 ({rel_path}) — {e}")
    total_score += comp3_score

    # Component 4: wire.go exists with wireinject build tag and wire.Build call (0.15 points)
    try:
        wire_go_path = os.path.join(PROJECT_DIR, 'cmd', 'server', 'wire.go')
        wire_go = read_file(wire_go_path)
        if not wire_go:
            print(f"FAIL: Component 4 — wire.go not found at {wire_go_path}")
        else:
            has_wireinject = 'wireinject' in wire_go
            has_wire_build = 'wire.Build(' in wire_go
            has_initialize = 'InitializeApp' in wire_go
            if has_wireinject and has_wire_build and has_initialize:
                print(f"PASS: Component 4 — wire.go has wireinject tag, wire.Build(), and InitializeApp (0.15 pts)")
                total_score += 0.15
            else:
                missing = []
                if not has_wireinject:
                    missing.append('wireinject build tag')
                if not has_wire_build:
                    missing.append('wire.Build() call')
                if not has_initialize:
                    missing.append('InitializeApp function')
                print(f"FAIL: Component 4 — wire.go missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: wire_gen.go exists with InitializeApp (0.10 points)
    try:
        wire_gen_path = os.path.join(PROJECT_DIR, 'cmd', 'server', 'wire_gen.go')
        wire_gen = read_file(wire_gen_path)
        if wire_gen and 'InitializeApp' in wire_gen:
            print(f"PASS: Component 5 — wire_gen.go exists and contains InitializeApp (0.10 pts)")
            total_score += 0.10
        else:
            if not wire_gen:
                print(f"FAIL: Component 5 — wire_gen.go not found")
            else:
                print(f"FAIL: Component 5 — wire_gen.go exists but missing InitializeApp")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: main.go calls InitializeApp (0.10 points)
    try:
        main_go_path = os.path.join(PROJECT_DIR, 'cmd', 'server', 'main.go')
        main_go = read_file(main_go_path)
        if main_go and 'InitializeApp' in main_go:
            print(f"PASS: Component 6 — main.go calls InitializeApp (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 — main.go does not call InitializeApp")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: Makefile has wire target (0.075 points)
    try:
        makefile_path = os.path.join(PROJECT_DIR, 'Makefile')
        makefile = read_file(makefile_path)
        if makefile and re.search(r'^wire\s*:', makefile, re.MULTILINE):
            print(f"PASS: Component 7 — Makefile has 'wire' target (0.075 pts)")
            total_score += 0.075
        else:
            print(f"FAIL: Component 7 — Makefile missing or no 'wire' target")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    # Component 8: .vscode/tasks.json has Wire: Generate task (0.075 points)
    try:
        tasks_path = os.path.join(PROJECT_DIR, '.vscode', 'tasks.json')
        tasks_content = read_file(tasks_path)
        if tasks_content:
            # Strip potential JSONC comments
            cleaned = re.sub(r'//.*$', '', tasks_content, flags=re.MULTILINE)
            tasks_json = json.loads(cleaned)
            tasks_list = tasks_json.get('tasks', [])
            wire_task_found = any(
                t.get('label', '') == 'Wire: Generate'
                for t in tasks_list
            )
            if wire_task_found:
                print(f"PASS: Component 8 — tasks.json has 'Wire: Generate' task (0.075 pts)")
                total_score += 0.075
            else:
                labels = [t.get('label', '') for t in tasks_list]
                print(f"FAIL: Component 8 — 'Wire: Generate' not found in tasks. Labels: {labels}")
        else:
            print(f"FAIL: Component 8 — .vscode/tasks.json not found")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
