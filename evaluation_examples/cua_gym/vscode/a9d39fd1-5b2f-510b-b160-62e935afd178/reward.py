"""
Reward Script: Initialize Rust project with VSCode tasks
Task ID: vscode_gf4_005
Domain: vscode
Scoring:
  Component 1 (0.25): Cargo.toml exists with valid package manifest
  Component 2 (0.30): src/main.rs contains println! with 'Rust service started on port 8080'
  Component 3 (0.25): .vscode/tasks.json has cargo build as default build task
  Component 4 (0.20): .vscode/tasks.json has cargo test task
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_005'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'rust-hello')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Cargo.toml exists with valid package manifest (0.25 points)
    # In initial_env, Cargo.toml does NOT exist (empty folder). In golden_env it does.
    try:
        cargo_path = os.path.join(PROJECT_DIR, 'Cargo.toml')
        if os.path.isfile(cargo_path):
            with open(cargo_path, 'r') as f:
                content = f.read()
            # Check it contains [package] section and name = "rust-hello"
            has_package = '[package]' in content
            has_name = re.search(r'name\s*=\s*"rust-hello"', content) is not None
            if has_package and has_name:
                print(f"PASS: Component 1 -- Cargo.toml has valid [package] with name='rust-hello' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 -- Cargo.toml missing [package] or name. has_package={has_package}, has_name={has_name}")
        else:
            print(f"FAIL: Component 1 -- Cargo.toml does not exist at {cargo_path}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: src/main.rs contains println! with the required message (0.30 points)
    # In initial_env, src/main.rs does NOT exist. In golden_env it contains the println! macro.
    try:
        main_rs_path = os.path.join(PROJECT_DIR, 'src', 'main.rs')
        if os.path.isfile(main_rs_path):
            with open(main_rs_path, 'r') as f:
                content = f.read()
            # Check for fn main function
            has_main_fn = 'fn main()' in content or 'fn main ()' in content
            # Check for the specific println! output
            has_println = re.search(r'println!\s*\(\s*"Rust service started on port 8080"\s*\)', content) is not None
            if has_main_fn and has_println:
                print(f"PASS: Component 2 -- src/main.rs has main fn with correct println! (0.30 pts)")
                total_score += 0.30
            elif has_println:
                # println exists but maybe main fn is slightly different syntax
                print(f"PASS: Component 2 -- src/main.rs has correct println! macro (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 -- src/main.rs missing required println!. has_main_fn={has_main_fn}, has_println={has_println}")
                print(f"  Content: {content[:200]}")
        else:
            print(f"FAIL: Component 2 -- src/main.rs does not exist at {main_rs_path}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: .vscode/tasks.json has cargo build as default build task (0.25 points)
    # In initial_env, .vscode/tasks.json does NOT exist.
    try:
        tasks_path = os.path.join(PROJECT_DIR, '.vscode', 'tasks.json')
        if os.path.isfile(tasks_path):
            with open(tasks_path, 'r') as f:
                raw = f.read()
            # Strip potential JSONC comments
            cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
            tasks_data = json.loads(cleaned)

            tasks_list = tasks_data.get('tasks', [])
            build_task_found = False
            for task in tasks_list:
                command = str(task.get('command', ''))
                label = str(task.get('label', ''))
                # Check if this is the cargo build task
                if 'cargo' in command and 'build' in command or 'cargo build' in label.lower():
                    # Check if it's set as default build
                    group = task.get('group', {})
                    if isinstance(group, dict):
                        is_build = group.get('kind', '') == 'build'
                        is_default = group.get('isDefault', False)
                        if is_build and is_default:
                            build_task_found = True
                            break
            if build_task_found:
                print(f"PASS: Component 3 -- tasks.json has 'cargo build' as default build task (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- tasks.json missing cargo build as default build task")
                print(f"  Tasks: {json.dumps(tasks_list, indent=2)[:300]}")
        else:
            print(f"FAIL: Component 3 -- .vscode/tasks.json does not exist at {tasks_path}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: .vscode/tasks.json has cargo test task (0.20 points)
    # In initial_env, .vscode/tasks.json does NOT exist.
    try:
        tasks_path = os.path.join(PROJECT_DIR, '.vscode', 'tasks.json')
        if os.path.isfile(tasks_path):
            with open(tasks_path, 'r') as f:
                raw = f.read()
            cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
            tasks_data = json.loads(cleaned)

            tasks_list = tasks_data.get('tasks', [])
            test_task_found = False
            for task in tasks_list:
                command = str(task.get('command', ''))
                label = str(task.get('label', ''))
                if ('cargo' in command and 'test' in command) or 'cargo test' in label.lower():
                    test_task_found = True
                    break
            if test_task_found:
                print(f"PASS: Component 4 -- tasks.json has 'cargo test' task (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 -- tasks.json missing cargo test task")
        else:
            print(f"FAIL: Component 4 -- .vscode/tasks.json does not exist at {tasks_path}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
