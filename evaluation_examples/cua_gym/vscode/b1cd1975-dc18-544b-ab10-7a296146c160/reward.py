"""
Reward Script: Create debug configuration for Python asyncio application
Task ID: vscode_py_072
Domain: vscode
Scoring:
  - Component 1 (0.30): New async debug launch configuration exists with correct type/request
  - Component 2 (0.25): justMyCode=false and subProcess=true in async launch config
  - Component 3 (0.20): PYTHONASYNCIODEBUG env variable set in async launch config
  - Component 4 (0.25): Attach configuration exists for async process debugging
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_072'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'async_project', '.vscode', 'launch.json')


def load_launch_json(path):
    """Load launch.json, stripping JSONC comments if present."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip // comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_config_by_criteria(configs, criteria_fn):
    """Find a configuration matching given criteria function."""
    for cfg in configs:
        if criteria_fn(cfg):
            return cfg
    return None


def verify_task(launch_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        data = load_launch_json(launch_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load launch.json at {launch_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    configs = data.get("configurations", [])
    print(f"INFO: Found {len(configs)} configurations in launch.json")

    # We need to find NEW configurations beyond the basic "Python: Current File"
    # The basic config is: type=debugpy, request=launch, program=${file}
    # We look for async-specific debug configs that were ADDED by the task

    # Component 1: New async debug launch configuration exists (0.30 points)
    # Must be a NEW launch config (not the basic ${file} one) targeting async_server.py
    # or at least a debugpy launch config that is NOT the basic one
    try:
        def is_new_async_launch(cfg):
            """A new launch config that is NOT the basic 'Python: Current File'."""
            if cfg.get("type") != "debugpy":
                return False
            if cfg.get("request") != "launch":
                return False
            # Must not be the basic config (which uses ${file} and has no async features)
            program = cfg.get("program", "")
            # The new config should reference async_server.py or have async-related settings
            has_async_indicator = (
                "async" in cfg.get("name", "").lower()
                or "async_server" in program
                or cfg.get("justMyCode") is not None
                or cfg.get("subProcess") is not None
                or "PYTHONASYNCIODEBUG" in str(cfg.get("env", {}))
            )
            is_basic = (program == "${file}" and
                        cfg.get("justMyCode") is None and
                        cfg.get("subProcess") is None and
                        not cfg.get("env"))
            return has_async_indicator and not is_basic

        async_launch = find_config_by_criteria(configs, is_new_async_launch)
        if async_launch:
            print(f"PASS: Component 1 -- Found new async launch config: '{async_launch.get('name', 'unnamed')}' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 -- No new async-specific launch configuration found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: justMyCode=false and subProcess=true in the async launch config (0.25 points)
    try:
        if async_launch:
            just_my_code = async_launch.get("justMyCode")
            sub_process = async_launch.get("subProcess")
            c2_score = 0.0
            if just_my_code is False:
                c2_score += 0.125
                print(f"  PASS: justMyCode is false")
            else:
                print(f"  FAIL: justMyCode expected false, found: {just_my_code}")
            if sub_process is True:
                c2_score += 0.125
                print(f"  PASS: subProcess is true")
            else:
                print(f"  FAIL: subProcess expected true, found: {sub_process}")
            if c2_score > 0:
                print(f"PASS: Component 2 -- async debug settings ({c2_score} pts)")
                total_score += c2_score
            else:
                print(f"FAIL: Component 2 -- neither justMyCode nor subProcess set correctly")
        else:
            print(f"FAIL: Component 2 -- No async launch config found (prerequisite)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: PYTHONASYNCIODEBUG env variable set (0.20 points)
    try:
        if async_launch:
            env_vars = async_launch.get("env", {})
            asyncio_debug = env_vars.get("PYTHONASYNCIODEBUG")
            if asyncio_debug == "1":
                print(f"PASS: Component 3 -- PYTHONASYNCIODEBUG='1' is set (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 -- PYTHONASYNCIODEBUG expected '1', found: {asyncio_debug}")
        else:
            print(f"FAIL: Component 3 -- No async launch config found (prerequisite)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Attach configuration for async process debugging (0.25 points)
    # Must be a debugpy "attach" config with justMyCode=false or subProcess=true
    try:
        def is_attach_config(cfg):
            return (cfg.get("type") == "debugpy" and
                    cfg.get("request") == "attach")

        attach_cfg = find_config_by_criteria(configs, is_attach_config)
        if attach_cfg:
            c4_score = 0.0
            # Base: attach config exists
            c4_score += 0.10
            # Bonus: has justMyCode=false
            if attach_cfg.get("justMyCode") is False:
                c4_score += 0.075
            # Bonus: has subProcess=true
            if attach_cfg.get("subProcess") is True:
                c4_score += 0.075
            print(f"PASS: Component 4 -- Attach config '{attach_cfg.get('name', 'unnamed')}' found ({c4_score} pts)")
            total_score += c4_score
        else:
            print(f"FAIL: Component 4 -- No debugpy attach configuration found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(LAUNCH_JSON_PATH):
    print(f"File not found: {LAUNCH_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(LAUNCH_JSON_PATH)
