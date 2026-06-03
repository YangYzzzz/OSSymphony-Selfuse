"""
Reward Script: Rust Cargo workspace scaffold with VSCode config
Task ID: vscode_gf6_004
Domain: vscode
Scoring:
  - Component 1: Workspace Cargo.toml with [workspace] members (0.15)
  - Component 2: core_lib/src/lib.rs with pub fn process that reverses (0.20)
  - Component 3: cli_app/src/main.rs uses core_lib::process (0.15)
  - Component 4: cli_app/Cargo.toml has core_lib path dependency (0.15)
  - Component 5: .vscode/tasks.json with 3 workspace tasks (0.15)
  - Component 6: .vscode/launch.json targets cli_app (0.10)
  - Component 7: core_lib/Cargo.toml is valid library crate (0.10)
"""

import os
import re
import json

WORKDIR = '/home/user/projects/rust-scaffold'
TASK_ID = 'vscode_gf6_004'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Workspace Cargo.toml with [workspace] members (0.15 points)
    try:
        cargo_path = os.path.join(WORKDIR, 'Cargo.toml')
        if os.path.exists(cargo_path):
            with open(cargo_path, 'r') as f:
                content = f.read()
            # Check for [workspace] section with members containing both crates
            has_workspace = '[workspace]' in content
            has_core_lib = 'core_lib' in content
            has_cli_app = 'cli_app' in content
            if has_workspace and has_core_lib and has_cli_app:
                print(f"PASS: Component 1 — Workspace Cargo.toml has [workspace] with both members (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — workspace={has_workspace}, core_lib={has_core_lib}, cli_app={has_cli_app}")
        else:
            print(f"FAIL: Component 1 — {cargo_path} not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: core_lib/src/lib.rs with pub fn process that reverses input (0.20 points)
    try:
        lib_path = os.path.join(WORKDIR, 'core_lib', 'src', 'lib.rs')
        if os.path.exists(lib_path):
            with open(lib_path, 'r') as f:
                content = f.read()
            has_pub_fn = bool(re.search(r'pub\s+fn\s+process\s*\(', content))
            has_str_param = bool(re.search(r'input\s*:\s*&str', content))
            has_return_string = bool(re.search(r'->\s*String', content))
            # Check for reverse logic
            has_reverse = 'rev()' in content or 'reverse' in content
            if has_pub_fn and has_str_param and has_return_string and has_reverse:
                print(f"PASS: Component 2 — core_lib/src/lib.rs has pub fn process(&str) -> String with reverse (0.20 pts)")
                total_score += 0.20
            elif has_pub_fn and has_str_param and has_return_string:
                print(f"PARTIAL: Component 2 — process() signature correct but no reverse logic found (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 2 — pub_fn={has_pub_fn}, str_param={has_str_param}, return_string={has_return_string}, reverse={has_reverse}")
        else:
            print(f"FAIL: Component 2 — {lib_path} not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: cli_app/src/main.rs uses core_lib::process (0.15 points)
    try:
        main_path = os.path.join(WORKDIR, 'cli_app', 'src', 'main.rs')
        if os.path.exists(main_path):
            with open(main_path, 'r') as f:
                content = f.read()
            uses_core_lib = 'core_lib' in content
            calls_process = 'process' in content
            has_main = 'fn main' in content
            # Check it reads command-line args
            uses_args = 'args' in content.lower() or 'env::args' in content
            if uses_core_lib and calls_process and has_main and uses_args:
                print(f"PASS: Component 3 — cli_app/src/main.rs uses core_lib::process with args (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — core_lib={uses_core_lib}, process={calls_process}, main={has_main}, args={uses_args}")
        else:
            print(f"FAIL: Component 3 — {main_path} not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: cli_app/Cargo.toml has core_lib path dependency (0.15 points)
    try:
        cli_cargo_path = os.path.join(WORKDIR, 'cli_app', 'Cargo.toml')
        if os.path.exists(cli_cargo_path):
            with open(cli_cargo_path, 'r') as f:
                content = f.read()
            has_dependencies = '[dependencies]' in content
            has_core_lib_dep = 'core_lib' in content
            has_path = 'path' in content
            if has_dependencies and has_core_lib_dep and has_path:
                print(f"PASS: Component 4 — cli_app/Cargo.toml has core_lib path dependency (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — dependencies={has_dependencies}, core_lib={has_core_lib_dep}, path={has_path}")
        else:
            print(f"FAIL: Component 4 — {cli_cargo_path} not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: .vscode/tasks.json with 3 workspace tasks (0.15 points)
    try:
        tasks_path = os.path.join(WORKDIR, '.vscode', 'tasks.json')
        if os.path.exists(tasks_path):
            with open(tasks_path, 'r') as f:
                # Handle JSONC (strip comments)
                raw = f.read()
                cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
                tasks_config = json.loads(cleaned)
            tasks = tasks_config.get('tasks', [])
            # Check for the three required task commands
            task_labels_or_commands = []
            for t in tasks:
                label = t.get('label', '')
                command = t.get('command', '')
                task_labels_or_commands.append(label.lower() + ' ' + command.lower())

            combined = ' '.join(task_labels_or_commands)
            has_build = 'cargo build' in combined and '--workspace' in combined
            has_test = 'cargo test' in combined and '--workspace' in combined
            has_clippy = 'cargo clippy' in combined and '--workspace' in combined

            found_count = sum([has_build, has_test, has_clippy])
            if found_count == 3:
                print(f"PASS: Component 5 — tasks.json has all 3 workspace tasks (0.15 pts)")
                total_score += 0.15
            elif found_count >= 1:
                partial = round(0.05 * found_count, 2)
                print(f"PARTIAL: Component 5 — {found_count}/3 tasks found ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — No required workspace tasks found in tasks.json")
        else:
            print(f"FAIL: Component 5 — {tasks_path} not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: .vscode/launch.json targets cli_app (0.10 points)
    try:
        launch_path = os.path.join(WORKDIR, '.vscode', 'launch.json')
        if os.path.exists(launch_path):
            with open(launch_path, 'r') as f:
                raw = f.read()
                cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
                launch_config = json.loads(cleaned)
            configs = launch_config.get('configurations', [])
            # Check at least one configuration references cli_app
            targets_cli_app = any('cli_app' in json.dumps(c).lower() for c in configs)
            if targets_cli_app:
                print(f"PASS: Component 6 — launch.json targets cli_app (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 — No configuration targeting cli_app found")
        else:
            print(f"FAIL: Component 6 — {launch_path} not found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: core_lib/Cargo.toml exists and is a valid library crate (0.10 points)
    try:
        core_cargo_path = os.path.join(WORKDIR, 'core_lib', 'Cargo.toml')
        if os.path.exists(core_cargo_path):
            with open(core_cargo_path, 'r') as f:
                content = f.read()
            has_package = '[package]' in content
            has_name = 'name' in content and 'core_lib' in content
            has_edition = 'edition' in content
            if has_package and has_name and has_edition:
                print(f"PASS: Component 7 — core_lib/Cargo.toml is valid library crate (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 7 — package={has_package}, name_core_lib={has_name}, edition={has_edition}")
        else:
            print(f"FAIL: Component 7 — {core_cargo_path} not found")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
