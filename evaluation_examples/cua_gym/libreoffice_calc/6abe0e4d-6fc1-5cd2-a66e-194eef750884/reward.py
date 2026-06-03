"""
Reward Script: Set up Rust development environment in VSCode
Task ID: vscode_wf_046
Domain: libreoffice_calc (actually vscode)
Scoring:
  Component 1: rust-analyzer extension installed (0.15 pts)
  Component 2: Cargo.toml exists (cargo init ran) (0.15 pts)
  Component 3: src/lib.rs has pub function with #[cfg(test)] module and unit tests (0.25 pts)
  Component 4: settings.json has rust-analyzer.checkOnSave.command = clippy (0.15 pts)
  Component 5: settings.json has rust-analyzer inlay hints enabled (0.15 pts)
  Component 6: launch.json has Rust/LLDB debug configuration (0.15 pts)
"""

import os
import json
import re
import subprocess

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_046'
HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
PROJECT_DIR = os.path.join(HOME, 'project')


def load_json_file(path):
    """Load a JSON file, stripping JSONC comments if needed."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify Rust development environment setup with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: rust-analyzer extension installed (0.15 points)
    # This checks whether the extension was installed — initial_env has NO extensions.
    try:
        result = subprocess.run(
            ['code', '--list-extensions'],
            capture_output=True, text=True, timeout=15
        )
        extensions = result.stdout.strip().lower().split('\n')
        if any('rust-analyzer' in ext for ext in extensions):
            print(f"PASS: Component 1 — rust-analyzer extension installed (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — rust-analyzer extension not found in: {extensions}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Cargo.toml exists with valid package section (0.15 points)
    # Initial_env has empty ~/project, so Cargo.toml does NOT exist initially.
    try:
        cargo_path = os.path.join(PROJECT_DIR, 'Cargo.toml')
        if os.path.isfile(cargo_path):
            with open(cargo_path, 'r') as f:
                cargo_content = f.read()
            if '[package]' in cargo_content and 'name' in cargo_content:
                print(f"PASS: Component 2 — Cargo.toml exists with [package] section (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — Cargo.toml exists but missing [package] or name")
        else:
            print(f"FAIL: Component 2 — Cargo.toml not found at {cargo_path}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: src/lib.rs has pub function + #[cfg(test)] module with unit tests (0.25 points)
    # Initial_env has no src/lib.rs at all.
    try:
        lib_path = os.path.join(PROJECT_DIR, 'src', 'lib.rs')
        if os.path.isfile(lib_path):
            with open(lib_path, 'r') as f:
                lib_content = f.read()

            has_pub_fn = bool(re.search(r'pub\s+fn\s+\w+', lib_content))
            has_cfg_test = '#[cfg(test)]' in lib_content
            has_test_attr = '#[test]' in lib_content
            has_mod_tests = bool(re.search(r'mod\s+tests', lib_content))

            sub_score = 0.0
            if has_pub_fn:
                sub_score += 0.08
            if has_cfg_test and has_mod_tests:
                sub_score += 0.09
            if has_test_attr:
                sub_score += 0.08

            if sub_score > 0:
                print(f"PASS: Component 3 — src/lib.rs: pub_fn={has_pub_fn}, cfg_test={has_cfg_test}, mod_tests={has_mod_tests}, test_attr={has_test_attr} ({sub_score:.2f} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 3 — src/lib.rs exists but missing required elements")
        else:
            print(f"FAIL: Component 3 — src/lib.rs not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: settings.json has rust-analyzer.checkOnSave.command = "clippy" (0.15 points)
    # Initial_env settings.json does NOT have any rust-analyzer keys.
    try:
        if os.path.isfile(SETTINGS_PATH):
            settings = load_json_file(SETTINGS_PATH)
            check_on_save = settings.get('rust-analyzer.checkOnSave.command', None)
            if check_on_save == 'clippy':
                print(f"PASS: Component 4 — rust-analyzer.checkOnSave.command = 'clippy' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — rust-analyzer.checkOnSave.command = '{check_on_save}', expected 'clippy'")
        else:
            print(f"FAIL: Component 4 — settings.json not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: settings.json has rust-analyzer inlay hints enabled (0.15 points)
    # Initial_env has no inlay hints settings.
    try:
        if os.path.isfile(SETTINGS_PATH):
            settings = load_json_file(SETTINGS_PATH)

            # Check for type hints enabled
            type_hints = settings.get('rust-analyzer.inlayHints.typeHints.enable', None)
            # Check for lifetime hints enabled
            lifetime_hints = settings.get('rust-analyzer.inlayHints.lifetimeElisionHints.enable', None)

            hints_score = 0.0
            if type_hints is True:
                hints_score += 0.075
            if lifetime_hints is not None and lifetime_hints != 'never' and lifetime_hints is not False:
                hints_score += 0.075

            if hints_score > 0:
                print(f"PASS: Component 5 — inlay hints: typeHints={type_hints}, lifetimeHints={lifetime_hints} ({hints_score:.3f} pts)")
                total_score += hints_score
            else:
                print(f"FAIL: Component 5 — inlay hints not properly configured: typeHints={type_hints}, lifetimeHints={lifetime_hints}")
        else:
            print(f"FAIL: Component 5 — settings.json not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: launch.json has Rust/LLDB debug configuration (0.15 points)
    # Initial_env has no .vscode/launch.json.
    try:
        launch_path = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')
        if os.path.isfile(launch_path):
            launch = load_json_file(launch_path)
            configurations = launch.get('configurations', [])

            lldb_configs = [
                c for c in configurations
                if c.get('type', '') in ('lldb', 'codelldb')
            ]

            if len(lldb_configs) > 0:
                print(f"PASS: Component 6 — launch.json has LLDB debug configuration (0.15 pts)")
                total_score += 0.15
            else:
                types_found = [c.get('type', 'unknown') for c in configurations]
                print(f"FAIL: Component 6 — No LLDB config found. Types: {types_found}")
        else:
            print(f"FAIL: Component 6 — launch.json not found at {launch_path}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
