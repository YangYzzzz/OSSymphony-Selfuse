"""
Reward Script: Vite project debug configuration with serverReadyAction
Task ID: vscode_web_067
Domain: vs_code
Scoring:
  Component 1: launch.json exists with valid structure (0.15)
  Component 2: Node launch config runs npm run dev (0.25)
  Component 3: serverReadyAction pattern matches Vite output (0.25)
  Component 4: serverReadyAction action is debugWithChrome (0.20)
  Component 5: serverReadyAction webRoot is ${workspaceFolder} (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_067'

LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'vite-app', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments), stripping // comments.
    First tries standard json.loads; falls back to comment stripping only if needed."""
    with open(path, 'r') as f:
        content = f.read()
    # Try parsing as-is first (valid JSON)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    # Fallback: strip single-line comments that start a line (after optional whitespace)
    # This avoids breaking URLs like http://localhost
    cleaned = re.sub(r'^\s*//.*$', '', content, flags=re.MULTILINE)
    # Also strip trailing commas before } or ]
    cleaned = re.sub(r',\s*([}\]])', r'\1', cleaned)
    return json.loads(cleaned)


def find_vite_debug_config(configs):
    """Find a configuration that starts the Vite dev server.
    Returns the first config that uses npm run dev or npx vite."""
    for cfg in configs:
        # Check runtimeArgs for "run" + "dev" pattern (npm run dev)
        runtime_args = cfg.get('runtimeArgs', [])
        args_str = ' '.join(str(a) for a in runtime_args).lower()

        # Also check 'args' field and 'program' field
        program = str(cfg.get('program', '')).lower()
        regular_args = cfg.get('args', [])
        regular_args_str = ' '.join(str(a) for a in regular_args).lower()

        is_npm_run_dev = (
            cfg.get('runtimeExecutable', '').lower() in ('npm', 'npx', 'yarn', 'pnpm')
            and ('run' in args_str and 'dev' in args_str)
        )
        is_vite_direct = 'vite' in program or 'vite' in regular_args_str

        if is_npm_run_dev or is_vite_direct:
            return cfg
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

    # Precondition: launch.json must be valid JSON(C)
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    configs = data.get('configurations', [])

    # Component 1: launch.json has valid structure with version and configurations (0.15 points)
    try:
        has_version = data.get('version') == '0.2.0'
        has_configs = isinstance(configs, list) and len(configs) > 0
        if has_version and has_configs:
            print(f"PASS: Component 1 - launch.json has version 0.2.0 and {len(configs)} configuration(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - version={data.get('version')}, configs count={len(configs) if isinstance(configs, list) else 'not a list'}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Find the Vite debug configuration
    vite_cfg = find_vite_debug_config(configs)

    # Component 2: Configuration launches Vite dev server via npm run dev (0.25 points)
    try:
        if vite_cfg is not None:
            cfg_type = vite_cfg.get('type', '')
            request = vite_cfg.get('request', '')
            # Must be a launch config (not attach)
            if request == 'launch':
                print(f"PASS: Component 2 - Found Vite dev server launch config (type={cfg_type}, request={request}) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 - Config found but request is '{request}', expected 'launch'")
        else:
            print(f"FAIL: Component 2 - No configuration found that starts Vite dev server (npm run dev)")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: serverReadyAction.pattern matches Vite dev server output (0.25 points)
    try:
        if vite_cfg is not None:
            sra = vite_cfg.get('serverReadyAction', {})
            pattern = sra.get('pattern', '')
            # The pattern should match "Local:  http://localhost:5173/" or similar
            # Expected pattern contains "Local:" and captures a port number
            if pattern and 'Local' in pattern and ('([0-9]+)' in pattern or '(\\d+)' in pattern or '[0-9]' in pattern):
                print(f"PASS: Component 3 - serverReadyAction.pattern='{pattern}' matches Vite output format (0.25 pts)")
                total_score += 0.25
            elif pattern:
                # Partial: pattern exists but may not match Vite output specifically
                # Check if it at least captures a port from localhost
                if 'localhost' in pattern and ('([0-9]+)' in pattern or '(\\d+)' in pattern or '[0-9]' in pattern):
                    print(f"PARTIAL: Component 3 - pattern captures localhost port but missing 'Local:' prefix: '{pattern}' (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 3 - pattern='{pattern}' does not match expected Vite output format")
            else:
                print(f"FAIL: Component 3 - No serverReadyAction.pattern found")
        else:
            print(f"FAIL: Component 3 - No Vite config found to check serverReadyAction")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: serverReadyAction.action is 'debugWithChrome' (0.20 points)
    try:
        if vite_cfg is not None:
            sra = vite_cfg.get('serverReadyAction', {})
            action = sra.get('action', '')
            if action == 'debugWithChrome':
                print(f"PASS: Component 4 - serverReadyAction.action='debugWithChrome' (0.20 pts)")
                total_score += 0.20
            elif action in ('openExternally', 'startDebugging'):
                # Acceptable alternatives that open Chrome
                print(f"PARTIAL: Component 4 - action='{action}' (acceptable but not ideal) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 - serverReadyAction.action='{action}', expected 'debugWithChrome'")
        else:
            print(f"FAIL: Component 4 - No Vite config found to check serverReadyAction.action")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: serverReadyAction.webRoot is '${workspaceFolder}' (0.15 points)
    try:
        if vite_cfg is not None:
            sra = vite_cfg.get('serverReadyAction', {})
            web_root = sra.get('webRoot', '')
            if web_root == '${workspaceFolder}':
                print(f"PASS: Component 5 - serverReadyAction.webRoot='${{workspaceFolder}}' (0.15 pts)")
                total_score += 0.15
            elif '${workspaceFolder}' in web_root:
                # e.g. "${workspaceFolder}/src" - partial credit
                print(f"PARTIAL: Component 5 - webRoot='{web_root}' contains workspaceFolder but not exact (0.08 pts)")
                total_score += 0.08
            else:
                print(f"FAIL: Component 5 - serverReadyAction.webRoot='{web_root}', expected '${{workspaceFolder}}'")
        else:
            print(f"FAIL: Component 5 - No Vite config found to check serverReadyAction.webRoot")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
