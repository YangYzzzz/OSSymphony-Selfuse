"""
Reward Script: Add command-line arguments to Node.js launch configuration in launch.json
Task ID: vscode_dbg_009
Domain: vs_code
Scoring:
  Component 1: 'args' property exists in the launch configuration (0.4 pts)
  Component 2: 'args' array contains exactly ['--verbose', '--port', '3000'] (0.4 pts)
  Component 3: Existing configuration properties preserved (type=node, program=cli.js) (0.2 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_009'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'node-cli', '.vscode', 'launch.json')

EXPECTED_ARGS = ["--verbose", "--port", "3000"]


def load_launch_json(file_path):
    """Load launch.json, handling JSONC (JSON with comments) format."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        content_stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_stripped)
    except Exception as e:
        raise e


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be valid JSON
    if not os.path.exists(file_path):
        print(f"CRITICAL: launch.json not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        data = load_launch_json(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must have a 'configurations' array with at least one entry
    configs = data.get('configurations', [])
    if not configs or not isinstance(configs, list):
        print("CRITICAL: No 'configurations' array found in launch.json")
        print("REWARD: 0.0")
        return 0.0

    # We look at the first (and presumably only) Node.js configuration
    config = configs[0]

    # Component 1: 'args' property exists in the launch configuration (0.4 points)
    # This FAILS on initial (no args key) → PASSES on golden (args key present)
    try:
        if 'args' in config:
            print(f"PASS: Component 1 — 'args' property exists in launch configuration (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — 'args' property is missing from launch configuration")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'args' array contains exactly ["--verbose", "--port", "3000"] (0.4 points)
    # This FAILS on initial (no args) → PASSES on golden (correct args values)
    try:
        actual_args = config.get('args', None)
        if actual_args == EXPECTED_ARGS:
            print(f"PASS: Component 2 — 'args' matches expected {EXPECTED_ARGS} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — expected args={EXPECTED_ARGS}, found args={actual_args}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Existing configuration properties are preserved (0.2 points)
    # Checks type=node, program ends with cli.js — these must remain unchanged
    # This FAILS on initial because args must be present AND these must be correct (compound check)
    # Actually, to ensure this component also fails on initial, we gate it on args being present
    try:
        config_type = config.get('type', '')
        config_program = config.get('program', '')
        config_request = config.get('request', '')
        has_correct_type = config_type == 'node'
        has_correct_program = 'cli.js' in config_program
        has_correct_request = config_request == 'launch'
        # This component only contributes if args are correctly set (compound check)
        # Ensures it cannot pass on initial_env (which lacks args)
        args_correct = config.get('args', None) == EXPECTED_ARGS
        if args_correct and has_correct_type and has_correct_program and has_correct_request:
            print(f"PASS: Component 3 — Configuration properties preserved: "
                  f"type={config_type}, program={config_program}, request={config_request} (0.2 pts)")
            total_score += 0.2
        elif not args_correct:
            print(f"FAIL: Component 3 — Skipped (args not correctly set)")
        else:
            print(f"FAIL: Component 3 — Existing config properties altered: "
                  f"type={config_type}, program={config_program}, request={config_request}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path on the VM
if not os.path.exists(LAUNCH_JSON_PATH):
    print(f"File not found: {LAUNCH_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(LAUNCH_JSON_PATH)
