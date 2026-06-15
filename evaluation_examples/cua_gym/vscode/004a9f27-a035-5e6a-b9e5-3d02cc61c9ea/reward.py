"""
Reward Script: Go scaffold project creation in VSCode
Task ID: vscode_gf6_003
Domain: vscode
Scoring:
  - go.mod with correct module (0.10)
  - cmd/server/main.go with main() (0.10)
  - internal/api/handler.go with Handler struct (0.10)
  - internal/api/routes.go with route registration (0.10)
  - internal/config/config.go with Config struct + env loading (0.15)
  - internal/middleware/cors.go with CORS function (0.10)
  - pkg/logger/logger.go wrapping slog/log (0.10)
  - Makefile with build/test/run/lint targets (0.10)
  - .vscode/tasks.json with Makefile tasks (0.075)
  - .vscode/launch.json with Go debug config (0.075)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'go-scaffold')


def read_file(path):
    """Read file content, return None if not found."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception:
        return None


def verify_task():
    total_score = 0.0

    # Component 1: go.mod with correct module path (0.10 points)
    try:
        content = read_file(os.path.join(PROJECT, 'go.mod'))
        if content and 'module github.com/user/go-scaffold' in content:
            print(f"PASS: Component 1 — go.mod has correct module path (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — go.mod missing or wrong module path. Content: {content!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: cmd/server/main.go with main() function (0.10 points)
    try:
        content = read_file(os.path.join(PROJECT, 'cmd', 'server', 'main.go'))
        if content and 'package main' in content and re.search(r'func\s+main\s*\(', content):
            print(f"PASS: Component 2 — cmd/server/main.go has main() (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 — cmd/server/main.go missing or no main(). Content: {content!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: internal/api/handler.go with Handler struct (0.10 points)
    try:
        content = read_file(os.path.join(PROJECT, 'internal', 'api', 'handler.go'))
        if content and re.search(r'type\s+Handler\s+struct', content):
            print(f"PASS: Component 3 — handler.go has Handler struct (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — handler.go missing or no Handler struct. Content: {content!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: internal/api/routes.go with route registration function (0.10 points)
    try:
        content = read_file(os.path.join(PROJECT, 'internal', 'api', 'routes.go'))
        # Must have a function that sets up routes (e.g., RegisterRoutes, SetupRoutes, etc.)
        if content and re.search(r'func\s+\w*[Rr]oute', content):
            print(f"PASS: Component 4 — routes.go has route registration function (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — routes.go missing or no route function. Content: {content!r}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: internal/config/config.go with Config struct + env loading (0.15 points)
    try:
        content = read_file(os.path.join(PROJECT, 'internal', 'config', 'config.go'))
        has_struct = False
        has_fields = False
        has_env = False
        if content:
            has_struct = bool(re.search(r'type\s+Config\s+struct', content))
            # Check for Port, DBHost, DBPort fields
            has_port = bool(re.search(r'Port\s+', content))
            has_dbhost = bool(re.search(r'DBHost\s+', content))
            has_dbport = bool(re.search(r'DBPort\s+', content))
            has_fields = has_port and has_dbhost and has_dbport
            has_env = 'os.Getenv' in content or 'Getenv' in content

        sub_score = 0.0
        if has_struct:
            sub_score += 0.05
        if has_fields:
            sub_score += 0.05
        if has_env:
            sub_score += 0.05

        if sub_score > 0:
            print(f"PASS: Component 5 — config.go: struct={has_struct}, fields={has_fields}, env={has_env} ({sub_score} pts)")
            total_score += sub_score
        else:
            print(f"FAIL: Component 5 — config.go missing or incomplete. Content: {content!r}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: internal/middleware/cors.go with CORS middleware (0.10 points)
    try:
        content = read_file(os.path.join(PROJECT, 'internal', 'middleware', 'cors.go'))
        if content and re.search(r'(CORS|cors)', content) and 'http' in content:
            print(f"PASS: Component 6 — cors.go has CORS middleware (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 — cors.go missing or no CORS middleware. Content: {content!r}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: pkg/logger/logger.go wrapping slog or log (0.10 points)
    try:
        content = read_file(os.path.join(PROJECT, 'pkg', 'logger', 'logger.go'))
        if content and ('slog' in content or '"log"' in content or 'log/' in content):
            print(f"PASS: Component 7 — logger.go wraps slog/log (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 7 — logger.go missing or doesn't wrap slog/log. Content: {content!r}")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    # Component 8: Makefile with build, test, run, lint targets (0.10 points)
    try:
        content = read_file(os.path.join(PROJECT, 'Makefile'))
        if content:
            has_build = bool(re.search(r'^build\s*:', content, re.MULTILINE))
            has_test = bool(re.search(r'^test\s*:', content, re.MULTILINE))
            has_run = bool(re.search(r'^run\s*:', content, re.MULTILINE))
            has_lint = bool(re.search(r'^lint\s*:', content, re.MULTILINE))
            targets_found = sum([has_build, has_test, has_run, has_lint])
            if targets_found == 4:
                print(f"PASS: Component 8 — Makefile has all 4 targets (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 8 — Makefile has {targets_found}/4 targets: build={has_build} test={has_test} run={has_run} lint={has_lint}")
        else:
            print(f"FAIL: Component 8 — Makefile not found")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

    # Component 9: .vscode/tasks.json with Makefile task references (0.075 points)
    try:
        content = read_file(os.path.join(PROJECT, '.vscode', 'tasks.json'))
        if content:
            # Strip potential JSONC comments
            stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            data = json.loads(stripped)
            tasks = data.get('tasks', [])
            # Check that tasks reference make commands
            make_refs = [t for t in tasks if 'make' in str(t.get('command', '')).lower()]
            if len(make_refs) >= 2:
                print(f"PASS: Component 9 — tasks.json has {len(make_refs)} Makefile tasks (0.075 pts)")
                total_score += 0.075
            else:
                print(f"FAIL: Component 9 — tasks.json has {len(make_refs)} Makefile tasks (need >=2)")
        else:
            print(f"FAIL: Component 9 — tasks.json not found")
    except Exception as e:
        print(f"ERROR: Component 9 — {e}")

    # Component 10: .vscode/launch.json with Go debug config (0.075 points)
    try:
        content = read_file(os.path.join(PROJECT, '.vscode', 'launch.json'))
        if content:
            stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            data = json.loads(stripped)
            configs = data.get('configurations', [])
            go_configs = [c for c in configs if c.get('type') == 'go']
            if len(go_configs) >= 1:
                print(f"PASS: Component 10 — launch.json has Go debug config (0.075 pts)")
                total_score += 0.075
            else:
                print(f"FAIL: Component 10 — launch.json has no Go-type configurations")
        else:
            print(f"FAIL: Component 10 — launch.json not found")
    except Exception as e:
        print(f"ERROR: Component 10 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
