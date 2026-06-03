"""
Reward Script: Multi-configuration launch.json with Run Current File and Run Tests configs
Task ID: vscode_py_051
Domain: vscode
Scoring:
  - Component 1 (0.15): launch.json exists, valid JSON, version "0.2.0"
  - Component 2 (0.15): Exactly 2 configurations present
  - Component 3 (0.35): "Run Current File" config with program="${file}"
  - Component 4 (0.35): "Run Tests with Coverage" config with module="pytest" and correct args
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_051'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'workspace', '.vscode', 'launch.json')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load launch.json — handle JSONC (comments)
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        # Strip single-line comments for JSONC compatibility
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        data = json.loads(cleaned)
    except FileNotFoundError:
        print(f"CRITICAL: launch.json not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid launch.json with version "0.2.0" (0.15 points)
    try:
        version = data.get("version", "")
        if version == "0.2.0":
            print(f"PASS: Component 1 — launch.json valid with version '{version}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — expected version '0.2.0', found '{version}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Exactly 2 configurations (0.15 points)
    try:
        configs = data.get("configurations", [])
        num_configs = len(configs)
        if num_configs >= 2:
            print(f"PASS: Component 2 — Found {num_configs} configurations (>= 2) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — expected >= 2 configurations, found {num_configs}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: "Run Current File" configuration (0.35 points)
    try:
        configs = data.get("configurations", [])
        run_current = None
        for cfg in configs:
            name = cfg.get("name", "")
            if "run current file" in name.lower():
                run_current = cfg
                break

        if run_current is None:
            print("FAIL: Component 3 — No 'Run Current File' configuration found")
        else:
            program = run_current.get("program", "")
            request_type = run_current.get("request", "")
            # Check program is "${file}"
            if program == "${file}" and request_type == "launch":
                print(f"PASS: Component 3 — 'Run Current File' config correct: program='{program}', request='{request_type}' (0.35 pts)")
                total_score += 0.35
            elif program == "${file}":
                # Partial: program correct but request type wrong
                print(f"PARTIAL: Component 3 — program correct but request='{request_type}' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — expected program='${{file}}', found program='{program}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: "Run Tests with Coverage" configuration (0.35 points)
    try:
        configs = data.get("configurations", [])
        run_tests = None
        for cfg in configs:
            name = cfg.get("name", "")
            if "run tests" in name.lower() or "test" in name.lower():
                run_tests = cfg
                break

        if run_tests is None:
            print("FAIL: Component 4 — No test configuration found")
        else:
            module = run_tests.get("module", "")
            args = run_tests.get("args", [])
            request_type = run_tests.get("request", "")

            sub_score = 0.0

            # Check module is pytest
            if module == "pytest":
                sub_score += 0.15
            else:
                print(f"FAIL: Component 4a — expected module='pytest', found '{module}'")

            # Check args contain --cov=src (or similar --cov)
            args_str = " ".join(str(a) for a in args)
            has_cov = any("--cov" in str(a) and "report" not in str(a) for a in args)
            has_cov_report = any("--cov-report" in str(a) for a in args)
            has_tests_dir = any("tests" in str(a) for a in args)

            if has_cov:
                sub_score += 0.08
            else:
                print(f"FAIL: Component 4b — missing --cov argument in args: {args}")

            if has_cov_report:
                sub_score += 0.07
            else:
                print(f"FAIL: Component 4c — missing --cov-report argument in args: {args}")

            if has_tests_dir:
                sub_score += 0.05
            else:
                print(f"FAIL: Component 4d — missing tests/ directory argument in args: {args}")

            if sub_score > 0:
                print(f"PASS: Component 4 — Test config: module='{module}', args={args} ({sub_score:.2f} pts)")
                total_score += sub_score
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(LAUNCH_JSON_PATH):
    print(f"File not found: {LAUNCH_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(LAUNCH_JSON_PATH)
