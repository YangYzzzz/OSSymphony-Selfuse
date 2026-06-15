"""
Reward Script: Go Microservice Project Setup in VSCode
Task ID: vscode_gf4_019
Domain: vscode (Go project)
Scoring:
  Component 1: go.mod with correct module path (0.15)
  Component 2: internal/config/config.go with Config struct and env var reading (0.20)
  Component 3: internal/middleware/logging.go with HTTP middleware (0.20)
  Component 4: cmd/server/main.go uses config and middleware (0.20)
  Component 5: Makefile with build/test/run targets (0.15)
  Component 6: .vscode/tasks.json with Makefile-based tasks (0.10)
"""

import os
import re
import json

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'go-microservice')


def verify_task():
    total_score = 0.0

    # Component 1: go.mod exists with correct module path (0.15 points)
    try:
        gomod_path = os.path.join(PROJECT, 'go.mod')
        with open(gomod_path, 'r') as f:
            content = f.read()
        if 'module github.com/user/go-microservice' in content:
            print(f"PASS: Component 1 — go.mod has correct module path (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — go.mod missing 'module github.com/user/go-microservice', found: {content[:100]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: internal/config/config.go with Config struct and env var reading (0.20 points)
    try:
        config_path = os.path.join(PROJECT, 'internal', 'config', 'config.go')
        with open(config_path, 'r') as f:
            content = f.read()

        config_score = 0.0
        # Check for Config struct
        if re.search(r'type\s+Config\s+struct', content):
            config_score += 0.05
            print(f"  PASS: Config struct found")
        else:
            print(f"  FAIL: Config struct not found")

        # Check for Load function
        if re.search(r'func\s+Load\s*\(', content):
            config_score += 0.05
            print(f"  PASS: Load() function found")
        else:
            print(f"  FAIL: Load() function not found")

        # Check for os.Getenv usage for DB_HOST, DB_PORT, APP_PORT
        env_vars_found = 0
        for var in ['DB_HOST', 'DB_PORT', 'APP_PORT']:
            if f'"{var}"' in content:
                env_vars_found += 1
        if env_vars_found == 3:
            config_score += 0.05
            print(f"  PASS: All 3 env vars (DB_HOST, DB_PORT, APP_PORT) referenced")
        else:
            print(f"  FAIL: Only {env_vars_found}/3 env vars found")

        # Check for default values (os.Getenv with fallback pattern)
        if 'os.Getenv' in content and ('==' in content or 'if' in content):
            config_score += 0.05
            print(f"  PASS: Default value handling found")
        else:
            print(f"  FAIL: No default value handling pattern found")

        if config_score > 0:
            print(f"PASS: Component 2 — config.go verified ({config_score} pts)")
            total_score += config_score
        else:
            print(f"FAIL: Component 2 — config.go missing required elements")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: internal/middleware/logging.go with HTTP middleware (0.20 points)
    try:
        middleware_path = os.path.join(PROJECT, 'internal', 'middleware', 'logging.go')
        with open(middleware_path, 'r') as f:
            content = f.read()

        mw_score = 0.0
        # Check it's a proper middleware wrapping http.Handler
        if 'http.Handler' in content:
            mw_score += 0.05
            print(f"  PASS: http.Handler reference found")
        else:
            print(f"  FAIL: http.Handler reference not found")

        # Check for logging of method
        if re.search(r'r\.Method|request\.Method|req\.Method', content) or 'Method' in content:
            mw_score += 0.05
            print(f"  PASS: Request method logging found")
        else:
            print(f"  FAIL: Request method logging not found")

        # Check for logging of path
        if re.search(r'r\.URL\.Path|request\.URL\.Path|URL\.Path', content) or 'Path' in content:
            mw_score += 0.05
            print(f"  PASS: Request path logging found")
        else:
            print(f"  FAIL: Request path logging not found")

        # Check for duration tracking
        if 'time.Since' in content or 'time.Now' in content or 'duration' in content.lower():
            mw_score += 0.05
            print(f"  PASS: Duration tracking found")
        else:
            print(f"  FAIL: Duration tracking not found")

        if mw_score > 0:
            print(f"PASS: Component 3 — logging.go verified ({mw_score} pts)")
            total_score += mw_score
        else:
            print(f"FAIL: Component 3 — logging.go missing required elements")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: cmd/server/main.go uses config and middleware (0.20 points)
    try:
        main_path = os.path.join(PROJECT, 'cmd', 'server', 'main.go')
        with open(main_path, 'r') as f:
            content = f.read()

        main_score = 0.0
        # Check for package main
        if 'package main' in content:
            main_score += 0.04
            print(f"  PASS: package main found")
        else:
            print(f"  FAIL: package main not found")

        # Check for config import/usage
        if 'internal/config' in content or 'config.Load' in content:
            main_score += 0.04
            print(f"  PASS: config package imported/used")
        else:
            print(f"  FAIL: config package not imported/used")

        # Check for middleware import/usage
        if 'internal/middleware' in content or 'middleware.Logging' in content or 'middleware.' in content:
            main_score += 0.04
            print(f"  PASS: middleware package imported/used")
        else:
            print(f"  FAIL: middleware package not imported/used")

        # Check for HTTP server start
        if 'http.ListenAndServe' in content or 'ListenAndServe' in content:
            main_score += 0.04
            print(f"  PASS: HTTP server (ListenAndServe) found")
        else:
            print(f"  FAIL: HTTP server start not found")

        # Check for func main()
        if re.search(r'func\s+main\s*\(', content):
            main_score += 0.04
            print(f"  PASS: func main() found")
        else:
            print(f"  FAIL: func main() not found")

        if main_score > 0:
            print(f"PASS: Component 4 — main.go verified ({main_score} pts)")
            total_score += main_score
        else:
            print(f"FAIL: Component 4 — main.go missing required elements")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Makefile with build, test, run targets (0.15 points)
    try:
        makefile_path = os.path.join(PROJECT, 'Makefile')
        with open(makefile_path, 'r') as f:
            content = f.read()

        mk_score = 0.0
        for target in ['build', 'test', 'run']:
            # Makefile target pattern: target_name: at start of line
            if re.search(r'^' + target + r'\s*:', content, re.MULTILINE):
                mk_score += 0.05
                print(f"  PASS: Makefile '{target}' target found")
            else:
                print(f"  FAIL: Makefile '{target}' target not found")

        if mk_score > 0:
            print(f"PASS: Component 5 — Makefile verified ({mk_score} pts)")
            total_score += mk_score
        else:
            print(f"FAIL: Component 5 — Makefile missing required targets")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: .vscode/tasks.json with Makefile-based tasks (0.10 points)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        with open(tasks_path, 'r') as f:
            content = f.read()

        # Strip JSONC comments
        clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        tasks_json = json.loads(clean)

        tasks_list = tasks_json.get('tasks', [])
        task_labels = [t.get('label', '') for t in tasks_list]
        task_commands = [t.get('command', '') for t in tasks_list]

        tasks_score = 0.0
        # Check that there are tasks referencing make targets
        make_refs = 0
        for cmd in task_commands:
            if 'make' in cmd.lower():
                make_refs += 1

        if make_refs >= 3:
            tasks_score += 0.05
            print(f"  PASS: 3+ tasks reference make commands")
        elif make_refs >= 1:
            tasks_score += 0.025
            print(f"  PARTIAL: Only {make_refs} tasks reference make commands")
        else:
            print(f"  FAIL: No tasks reference make commands")

        # Check that build/test/run labels or commands exist
        found_targets = 0
        for target in ['build', 'test', 'run']:
            if any(target in l.lower() for l in task_labels) or any(target in c.lower() for c in task_commands):
                found_targets += 1

        if found_targets >= 3:
            tasks_score += 0.05
            print(f"  PASS: All 3 Makefile targets represented in tasks")
        elif found_targets >= 1:
            tasks_score += 0.025
            print(f"  PARTIAL: Only {found_targets}/3 Makefile targets in tasks")
        else:
            print(f"  FAIL: No Makefile targets found in tasks")

        if tasks_score > 0:
            print(f"PASS: Component 6 — tasks.json verified ({tasks_score} pts)")
            total_score += tasks_score
        else:
            print(f"FAIL: Component 6 — tasks.json missing Makefile-based tasks")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
