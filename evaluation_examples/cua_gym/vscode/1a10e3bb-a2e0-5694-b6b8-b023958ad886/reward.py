"""
Reward Script: VSCode Go debug project — launch.json, tasks.json, and bug fix
Task ID: vscode_gf6_014
Domain: vscode
Scoring:
  Component 1 (0.25): launch.json "Launch API" config with env vars
  Component 2 (0.20): launch.json "Debug Tests" config with test mode
  Component 3 (0.30): Bug fix — minPrice/maxPrice correctly mapped in products.go
  Component 4 (0.25): tasks.json "go vet" task
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'go-debug')
TASK_ID = 'vscode_gf6_014'


def strip_jsonc_comments(text):
    """Remove // and /* */ comments from JSONC content."""
    # Remove single-line comments
    text = re.sub(r'//.*$', '', text, flags=re.MULTILINE)
    # Remove multi-line comments
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    return text


def load_json_file(path):
    """Load a JSON/JSONC file, stripping comments if needed."""
    with open(path, 'r') as f:
        content = f.read()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        cleaned = strip_jsonc_comments(content)
        return json.loads(cleaned)


def verify_task():
    """Verify task completion with progressive scoring."""
    total_score = 0.0

    # Component 1: launch.json "Launch API" configuration (0.25 points)
    try:
        launch_path = os.path.join(PROJECT, '.vscode', 'launch.json')
        if not os.path.exists(launch_path):
            print(f"FAIL: Component 1 — .vscode/launch.json does not exist")
        else:
            launch = load_json_file(launch_path)
            configs = launch.get('configurations', [])
            launch_api = None
            for cfg in configs:
                if cfg.get('name') == 'Launch API':
                    launch_api = cfg
                    break
            if launch_api is None:
                print(f"FAIL: Component 1 — No 'Launch API' configuration found in launch.json")
            else:
                env = launch_api.get('env', {})
                has_db_host = env.get('DB_HOST') == 'localhost'
                has_app_port = env.get('APP_PORT') == '8080'
                # Check program targets cmd/server/main.go
                program = launch_api.get('program', '')
                has_program = 'cmd/server/main.go' in program or 'cmd\\server\\main.go' in program
                if has_db_host and has_app_port and has_program:
                    print(f"PASS: Component 1 — 'Launch API' config correct: program={program}, env={env} (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 1 — 'Launch API' config incomplete: DB_HOST={has_db_host}, APP_PORT={has_app_port}, program={has_program} (program={program}, env={env})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: launch.json "Debug Tests" configuration (0.20 points)
    try:
        launch_path = os.path.join(PROJECT, '.vscode', 'launch.json')
        if not os.path.exists(launch_path):
            print(f"FAIL: Component 2 — .vscode/launch.json does not exist")
        else:
            launch = load_json_file(launch_path)
            configs = launch.get('configurations', [])
            debug_tests = None
            for cfg in configs:
                if cfg.get('name') == 'Debug Tests':
                    debug_tests = cfg
                    break
            if debug_tests is None:
                print(f"FAIL: Component 2 — No 'Debug Tests' configuration found in launch.json")
            else:
                mode = debug_tests.get('mode', '')
                has_test_mode = mode == 'test'
                # Check for -v flag and ./... pattern in args
                args = debug_tests.get('args', [])
                args_str = ' '.join(str(a) for a in args)
                has_v_flag = '-v' in args
                has_pattern = './...' in args_str
                if has_test_mode and has_v_flag and has_pattern:
                    print(f"PASS: Component 2 — 'Debug Tests' config correct: mode={mode}, args={args} (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 2 — 'Debug Tests' config incomplete: test_mode={has_test_mode}, -v={has_v_flag}, ./...={has_pattern} (mode={mode}, args={args})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Bug fix in products.go (0.30 points)
    # The bug is: minStr was parsed into maxPrice, maxStr into minPrice (swapped)
    # Fixed: minStr -> minPrice, maxStr -> maxPrice
    try:
        products_path = os.path.join(PROJECT, 'internal', 'handlers', 'products.go')
        with open(products_path, 'r') as f:
            content = f.read()

        # Check that minPrice is parsed from minStr (not maxStr)
        # And maxPrice is parsed from maxStr (not minStr)
        # The buggy version has: maxPrice, err := strconv.ParseFloat(minStr, 64)
        #                         minPrice, err := strconv.ParseFloat(maxStr, 64)
        # The fixed version has:  minPrice, err := strconv.ParseFloat(minStr, 64)
        #                         maxPrice, err := strconv.ParseFloat(maxStr, 64)

        # Check for the buggy pattern (should NOT be present)
        buggy_pattern1 = re.search(r'maxPrice.*:=.*ParseFloat\(minStr', content)
        buggy_pattern2 = re.search(r'minPrice.*:=.*ParseFloat\(maxStr', content)

        # Check for the fixed pattern (should be present)
        fixed_pattern1 = re.search(r'minPrice.*:=.*ParseFloat\(minStr', content)
        fixed_pattern2 = re.search(r'maxPrice.*:=.*ParseFloat\(maxStr', content)

        if buggy_pattern1 or buggy_pattern2:
            print(f"FAIL: Component 3 — Bug still present: min/max variables are still swapped")
        elif fixed_pattern1 and fixed_pattern2:
            print(f"PASS: Component 3 — Bug fixed: minPrice parsed from minStr, maxPrice from maxStr (0.30 pts)")
            total_score += 0.30
        else:
            # Partial: maybe restructured differently but still correct logic
            # Check that minStr maps to minPrice somewhere and maxStr maps to maxPrice
            has_min_correct = 'minStr' in content and 'minPrice' in content
            has_max_correct = 'maxStr' in content and 'maxPrice' in content
            if has_min_correct and has_max_correct and not buggy_pattern1 and not buggy_pattern2:
                print(f"PASS: Component 3 — Bug appears fixed (alternative structure) (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 — Cannot confirm bug is fixed. Content snippet around ParseFloat:")
                for line in content.split('\n'):
                    if 'ParseFloat' in line:
                        print(f"  {line.strip()}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: tasks.json with "go vet" task (0.25 points)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        if not os.path.exists(tasks_path):
            print(f"FAIL: Component 4 — .vscode/tasks.json does not exist")
        else:
            tasks = load_json_file(tasks_path)
            task_list = tasks.get('tasks', [])
            go_vet_task = None
            for t in task_list:
                if t.get('label', '').lower() == 'go vet':
                    go_vet_task = t
                    break
            if go_vet_task is None:
                print(f"FAIL: Component 4 — No 'go vet' task found in tasks.json")
            else:
                command = go_vet_task.get('command', '')
                # Check the command runs go vet ./...
                has_go_vet = 'go vet' in command and './...' in command
                # Check it has a problem matcher
                has_problem_matcher = 'problemMatcher' in go_vet_task
                if has_go_vet:
                    print(f"PASS: Component 4 — 'go vet' task found with command='{command}', problemMatcher={has_problem_matcher} (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 4 — 'go vet' task command incorrect: '{command}' (expected 'go vet ./...')")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
