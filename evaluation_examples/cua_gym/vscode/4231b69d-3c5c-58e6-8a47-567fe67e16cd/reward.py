"""
Reward Script: VSCode performance profiling and optimization task
Task ID: vscode_gf6_026
Domain: vscode
Scoring:
  Component 1 (0.30): data_processor.py uses set() for seen_transactions
  Component 2 (0.20): data_processor.py uses .add() instead of .append() for dedup
  Component 3 (0.20): profile.out exists in project root
  Component 4 (0.20): .vscode/launch.json has 'Profile Script' configuration
  Component 5 (0.10): snakeviz is installed in venv
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_026'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'perf-profiling')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Component 1: seen_transactions initialized as set() (0.30 points) ---
    # In the initial state, seen_transactions = [] (a list).
    # After optimization, it should be seen_transactions = set().
    try:
        dp_path = os.path.join(PROJECT_DIR, 'src', 'data_processor.py')
        with open(dp_path, 'r') as f:
            source_code = f.read()

        # Check that seen_transactions is initialized as a set, not a list
        # Look for pattern: seen_transactions = set() (or similar set initialization)
        has_set_init = bool(re.search(r'seen_transactions\s*=\s*set\s*\(', source_code))
        # Also ensure the old list pattern is gone
        has_list_init = bool(re.search(r'seen_transactions\s*=\s*\[\s*\]', source_code))

        if has_set_init and not has_list_init:
            print(f"PASS: Component 1 - seen_transactions uses set() initialization (0.30 pts)")
            total_score += 0.30
        elif has_set_init and has_list_init:
            print(f"PARTIAL: Component 1 - set() found but list [] also present (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - seen_transactions not initialized as set(). "
                  f"has_set={has_set_init}, has_list={has_list_init}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # --- Component 2: .add() used instead of .append() for seen_transactions (0.20 points) ---
    # In the initial state, process_row uses seen_transactions.append(txn_id).
    # After optimization, it should use seen_transactions.add(txn_id).
    try:
        # Check for .add() usage on seen_transactions
        has_add = bool(re.search(r'seen_transactions\.add\s*\(', source_code))
        # Check that old .append() on seen_transactions is gone
        has_append = bool(re.search(r'seen_transactions\.append\s*\(', source_code))

        if has_add and not has_append:
            print(f"PASS: Component 2 - uses .add() for deduplication (0.20 pts)")
            total_score += 0.20
        elif has_add and has_append:
            print(f"PARTIAL: Component 2 - .add() found but .append() also present (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 - expected .add() on seen_transactions, "
                  f"has_add={has_add}, has_append={has_append}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # --- Component 3: profile.out exists in project root (0.20 points) ---
    # In the initial state, profile.out does not exist.
    # After profiling, it should exist.
    try:
        profile_path = os.path.join(PROJECT_DIR, 'profile.out')
        if os.path.exists(profile_path):
            file_size = os.path.getsize(profile_path)
            if file_size > 100:
                print(f"PASS: Component 3 - profile.out exists ({file_size} bytes) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 - profile.out exists but too small ({file_size} bytes)")
        else:
            print(f"FAIL: Component 3 - profile.out not found at {profile_path}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # --- Component 4: .vscode/launch.json with 'Profile Script' config (0.20 points) ---
    # In the initial state, .vscode/launch.json does not exist.
    # After setup, it should have a configuration named 'Profile Script'.
    try:
        launch_path = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')
        if os.path.exists(launch_path):
            with open(launch_path, 'r') as f:
                content = f.read()
            # Strip potential JSONC comments
            cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            launch_data = json.loads(cleaned)

            configs = launch_data.get('configurations', [])
            profile_config = None
            for cfg in configs:
                if cfg.get('name', '') == 'Profile Script':
                    profile_config = cfg
                    break

            if profile_config is not None:
                # Verify it runs cProfile and outputs to profile.out
                # Check module-based launch (module: cProfile) or args containing cProfile
                args = profile_config.get('args', [])
                args_str = ' '.join(str(a) for a in args)
                uses_cprofile = (profile_config.get('module', '') == 'cProfile') or ('cProfile' in args_str)
                outputs_profile = ('profile.out' in args_str)

                if uses_cprofile and outputs_profile:
                    print(f"PASS: Component 4 - launch.json has 'Profile Script' with cProfile -> profile.out (0.20 pts)")
                    total_score += 0.20
                elif uses_cprofile or outputs_profile:
                    print(f"PARTIAL: Component 4 - 'Profile Script' incomplete (cProfile={uses_cprofile}, profile.out={outputs_profile}) (0.10 pts)")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 4 - 'Profile Script' config lacks cProfile and profile.out")
            else:
                config_names = [c.get('name', '?') for c in configs]
                print(f"FAIL: Component 4 - No 'Profile Script' config found. Configs: {config_names}")
        else:
            print(f"FAIL: Component 4 - .vscode/launch.json not found at {launch_path}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # --- Component 5: snakeviz installed in venv (0.10 points) ---
    # In the initial state, snakeviz is not installed.
    # After setup, it should be installed in the project's venv.
    try:
        # Check if snakeviz binary exists in venv
        snakeviz_bin = os.path.join(PROJECT_DIR, 'venv', 'bin', 'snakeviz')
        # Fallback: check if snakeviz package directory exists in site-packages
        snakeviz_in_sitepackages = False
        lib_dir = os.path.join(PROJECT_DIR, 'venv', 'lib')
        if os.path.exists(lib_dir):
            snakeviz_in_sitepackages = any(
                os.path.isdir(os.path.join(lib_dir, pydir, 'site-packages', 'snakeviz'))
                for pydir in os.listdir(lib_dir)
            )

        if os.path.exists(snakeviz_bin):
            print(f"PASS: Component 5 - snakeviz binary found in venv/bin (0.10 pts)")
            total_score += 0.10
        elif snakeviz_in_sitepackages:
            print(f"PASS: Component 5 - snakeviz package found in venv site-packages (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 - snakeviz not found in venv")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = min(total_score, 1.0)
    # Round to avoid floating point issues
    final_score = round(final_score, 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
verify_task()
