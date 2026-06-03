"""
Reward Script: VSCode pytest-xdist debug launch configuration
Task ID: vscode_gf1_085
Domain: vscode (launch.json)
Scoring:
  1. launch.json exists and is valid JSON with configurations array  (0.10)
  2. Args contain '-p no:xdist' to disable parallel plugin            (0.25)
  3. stopOnEntry is false                                              (0.15)
  4. console is 'integratedTerminal'                                   (0.15)
  5. PYTEST_CURRENT_TEST env variable is present                       (0.20)
  6. type=debugpy, request=launch, module=pytest                       (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf1_085'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'parallel-tests', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments) by stripping comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_pytest_debug_config(configs):
    """Find the configuration that is a pytest debug config (has '-p no:xdist' or module=pytest)."""
    # First try to find one with -p no:xdist in args
    for cfg in configs:
        args = cfg.get('args', [])
        if '-p' in args:
            idx = args.index('-p')
            if idx + 1 < len(args) and args[idx + 1] == 'no:xdist':
                return cfg
        # Also check for combined arg form
        if '-p no:xdist' in args or '--override-ini=-p no:xdist' in args:
            return cfg
        # Check as joined string
        args_str = ' '.join(str(a) for a in args)
        if '-p no:xdist' in args_str:
            return cfg
    # Fallback: find any pytest config
    for cfg in configs:
        if cfg.get('module') == 'pytest':
            return cfg
    # Last resort: return first config
    if configs:
        return configs[0]
    return None


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

    # Load and parse launch.json
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    configs = data.get('configurations', [])
    if not configs:
        print("CRITICAL: No configurations array or it is empty")
        print("REWARD: 0.0")
        return 0.0

    cfg = find_pytest_debug_config(configs)
    if cfg is None:
        print("CRITICAL: No suitable debug configuration found")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: launch.json is valid with configurations (0.10 points)
    # We already verified this above — the file exists, parses, and has configurations
    try:
        if isinstance(configs, list) and len(configs) > 0 and 'version' in data:
            print(f"PASS: Component 1 — launch.json valid with {len(configs)} configuration(s) (0.10 pts)")
            total_score += 0.10
        elif isinstance(configs, list) and len(configs) > 0:
            # version field is optional but configs must exist
            print(f"PASS: Component 1 — launch.json valid with {len(configs)} configuration(s), no version field (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — configurations is not a non-empty list")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Args contain '-p no:xdist' (0.25 points)
    try:
        args = cfg.get('args', [])
        args_str = ' '.join(str(a) for a in args)
        # Check multiple valid representations of '-p no:xdist'
        found_no_xdist = (
            ('-p' in args and args.index('-p') + 1 < len(args) and args[args.index('-p') + 1] == 'no:xdist')
            or ('-p no:xdist' in args)
            or ('-p no:xdist' in args_str)
        )

        if found_no_xdist:
            print(f"PASS: Component 2 — args contain '-p no:xdist' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — args do not contain '-p no:xdist'. Found args: {args}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: stopOnEntry is false (0.15 points)
    try:
        if 'stopOnEntry' in cfg:
            stop_on_entry = cfg['stopOnEntry']
            if stop_on_entry is False:
                print(f"PASS: Component 3 — stopOnEntry is false (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — stopOnEntry is {stop_on_entry}, expected false")
        else:
            print(f"FAIL: Component 3 — stopOnEntry key not found in configuration")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: console is 'integratedTerminal' (0.15 points)
    try:
        console_val = cfg.get('console')
        if console_val == 'integratedTerminal':
            print(f"PASS: Component 4 — console is 'integratedTerminal' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — console is '{console_val}', expected 'integratedTerminal'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: PYTEST_CURRENT_TEST env variable is set (0.20 points)
    try:
        env_vars = cfg.get('env', {})
        if isinstance(env_vars, dict) and 'PYTEST_CURRENT_TEST' in env_vars:
            print(f"PASS: Component 5 — PYTEST_CURRENT_TEST env variable present, value='{env_vars['PYTEST_CURRENT_TEST']}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 5 — PYTEST_CURRENT_TEST not found in env. Found env: {env_vars}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: type=debugpy, request=launch, module=pytest (0.15 points)
    try:
        cfg_type = cfg.get('type', '')
        cfg_request = cfg.get('request', '')
        cfg_module = cfg.get('module', '')

        checks_passed = 0
        details = []

        if cfg_type == 'debugpy':
            checks_passed += 1
            details.append(f"type=debugpy OK")
        else:
            details.append(f"type='{cfg_type}' (expected 'debugpy')")

        if cfg_request == 'launch':
            checks_passed += 1
            details.append(f"request=launch OK")
        else:
            details.append(f"request='{cfg_request}' (expected 'launch')")

        if cfg_module == 'pytest':
            checks_passed += 1
            details.append(f"module=pytest OK")
        else:
            details.append(f"module='{cfg_module}' (expected 'pytest')")

        # Award partial: 0.05 per sub-check
        if checks_passed == 3:
            print(f"PASS: Component 6 — {', '.join(details)} (0.15 pts)")
            total_score += 0.15
        elif checks_passed > 0:
            partial = round((checks_passed / 3) * 0.15, 2)
            print(f"PARTIAL: Component 6 — {', '.join(details)} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 6 — {', '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
