"""
Reward Script: Create launch.json with Mocha debug configuration
Task ID: vscode_td_075
Domain: vscode
Scoring:
  Component 1 (0.15): launch.json exists, valid JSON with version+configurations
  Component 2 (0.20): type=node, request=launch present in a configuration
  Component 3 (0.25): program references mocha binary
  Component 4 (0.20): args include --timeout 10000
  Component 5 (0.20): args include test/ directory
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_075'

LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'node-lib', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments) by stripping comments first."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip multi-line comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: launch.json must exist
    if not os.path.exists(LAUNCH_JSON_PATH):
        print(f"CRITICAL: launch.json not found at {LAUNCH_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must be valid JSON(C)
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get configurations list
    configurations = data.get("configurations", [])
    if not isinstance(configurations, list) or len(configurations) == 0:
        print("FAIL: No configurations array found or it is empty")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: launch.json has version and configurations structure (0.15 pts)
    # This checks that the file is a proper launch.json, not just any JSON file.
    # Initial env has no .vscode dir at all, so this only passes on golden.
    try:
        has_version = "version" in data
        has_configs = len(configurations) > 0
        if has_version and has_configs:
            print(f"PASS: Component 1 -- launch.json has version='{data.get('version')}' and {len(configurations)} configuration(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- version present: {has_version}, configs present: {has_configs}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Find the Mocha-related configuration (search all configs)
    mocha_config = None
    for cfg in configurations:
        name = str(cfg.get("name", "")).lower()
        program = str(cfg.get("program", "")).lower()
        args_str = " ".join(str(a) for a in cfg.get("args", []))
        # Identify mocha config by name, program, or args referencing mocha
        if "mocha" in name or "mocha" in program or "mocha" in args_str.lower():
            mocha_config = cfg
            break

    # If no explicit mocha reference found, use first config as candidate
    if mocha_config is None:
        mocha_config = configurations[0]

    # Component 2: type=node and request=launch (0.20 pts)
    try:
        cfg_type = mocha_config.get("type", "")
        cfg_request = mocha_config.get("request", "")
        if cfg_type == "node" and cfg_request == "launch":
            print(f"PASS: Component 2 -- type='node', request='launch' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 -- expected type='node' and request='launch', found type='{cfg_type}', request='{cfg_request}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: program references mocha binary (0.25 pts)
    # Accepts variations: node_modules/.bin/mocha, npx mocha, mocha path
    try:
        program = str(mocha_config.get("program", ""))
        runtime_exec = str(mocha_config.get("runtimeExecutable", ""))
        runtime_args = mocha_config.get("runtimeArgs", [])
        runtime_args_str = " ".join(str(a) for a in runtime_args) if isinstance(runtime_args, list) else str(runtime_args)

        mocha_in_program = "mocha" in program.lower()
        mocha_via_npx = ("npx" in runtime_exec.lower() and "mocha" in runtime_args_str.lower())
        mocha_via_runtime = "mocha" in runtime_exec.lower()

        if mocha_in_program or mocha_via_npx or mocha_via_runtime:
            detail = program if mocha_in_program else f"runtimeExecutable={runtime_exec}, runtimeArgs={runtime_args}"
            print(f"PASS: Component 3 -- mocha reference found: {detail} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- no mocha reference found. program='{program}', runtimeExecutable='{runtime_exec}'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: args include --timeout 10000 (0.20 pts)
    try:
        args = mocha_config.get("args", [])
        if not isinstance(args, list):
            args = []
        args_str_list = [str(a) for a in args]
        args_joined = " ".join(args_str_list)

        # Also check runtimeArgs for npx-style configs
        runtime_args = mocha_config.get("runtimeArgs", [])
        if isinstance(runtime_args, list):
            runtime_args_str_list = [str(a) for a in runtime_args]
            all_args_joined = args_joined + " " + " ".join(runtime_args_str_list)
        else:
            all_args_joined = args_joined

        has_timeout_flag = "--timeout" in all_args_joined
        has_timeout_value = "10000" in all_args_joined

        if has_timeout_flag and has_timeout_value:
            print(f"PASS: Component 4 -- --timeout 10000 found in args (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 -- expected --timeout 10000, found args={args_str_list}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: args include test/ directory (0.20 pts)
    try:
        args = mocha_config.get("args", [])
        if not isinstance(args, list):
            args = []
        args_str_list = [str(a) for a in args]

        runtime_args = mocha_config.get("runtimeArgs", [])
        if isinstance(runtime_args, list):
            all_args = args_str_list + [str(a) for a in runtime_args]
        else:
            all_args = args_str_list

        all_args_joined = " ".join(all_args)

        # Accept "test/", "test", "./test/", "./test", "test/**", etc.
        has_test_dir = any(
            a.strip().rstrip('/') == 'test' or
            a.strip().startswith('test/') or
            a.strip().startswith('./test')
            for a in all_args
        )

        if has_test_dir:
            matching = [a for a in all_args if 'test' in a.lower()]
            print(f"PASS: Component 5 -- test/ directory found in args: {matching} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 5 -- expected test/ in args, found: {all_args}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
