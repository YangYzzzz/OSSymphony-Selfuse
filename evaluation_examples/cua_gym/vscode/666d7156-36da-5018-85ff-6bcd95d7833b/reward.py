"""
Reward Script: Create launch.json with preLaunchTask and serverReadyAction
Task ID: vscode_td_093
Domain: vscode
Scoring:
  - Component 1 (0.15): launch.json exists and is valid JSON with configurations array
  - Component 2 (0.25): preLaunchTask is "Start Server"
  - Component 3 (0.25): serverReadyAction.pattern matches "Listening on port ([0-9]+)"
  - Component 4 (0.20): serverReadyAction.action is "openExternally" or "debugWithChrome"
  - Component 5 (0.15): serverReadyAction.uriFormat is "http://localhost:%s"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_093'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'web-server', '.vscode', 'launch.json')


def load_jsonc(file_path):
    """Load a JSON file, stripping JSONC-style comments while preserving strings."""
    with open(file_path, 'r') as f:
        content = f.read()
    # First try direct parse (works if no comments)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    # Strip comments outside of strings using a token-aware approach
    result = []
    i = 0
    while i < len(content):
        # String literal - copy as-is
        if content[i] == '"':
            j = i + 1
            while j < len(content):
                if content[j] == '\\':
                    j += 2
                    continue
                if content[j] == '"':
                    j += 1
                    break
                j += 1
            result.append(content[i:j])
            i = j
        # Line comment
        elif content[i:i+2] == '//':
            while i < len(content) and content[i] != '\n':
                i += 1
        # Block comment
        elif content[i:i+2] == '/*':
            i += 2
            while i < len(content) - 1 and content[i:i+2] != '*/':
                i += 1
            i += 2
        else:
            result.append(content[i])
            i += 1
    return json.loads(''.join(result))


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

    # Get configurations array
    configurations = data.get('configurations', [])

    # Component 1: launch.json has a valid configurations array with at least one entry (0.15 points)
    try:
        if isinstance(configurations, list) and len(configurations) > 0:
            print(f"PASS: Component 1 -- launch.json has {len(configurations)} configuration(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- configurations is empty or not a list: {type(configurations)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Find the configuration that has preLaunchTask or serverReadyAction
    config = None
    for c in configurations:
        if isinstance(c, dict) and ('preLaunchTask' in c or 'serverReadyAction' in c):
            config = c
            break
    # Fallback to first config if none matched
    if config is None and len(configurations) > 0:
        config = configurations[0]

    if config is None:
        print("FAIL: No configuration found in launch.json")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: preLaunchTask is "Start Server" (0.25 points)
    try:
        pre_launch = config.get('preLaunchTask', None)
        if pre_launch == "Start Server":
            print(f"PASS: Component 2 -- preLaunchTask is 'Start Server' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- preLaunchTask expected 'Start Server', found: {pre_launch!r}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: serverReadyAction.pattern matches "Listening on port ([0-9]+)" (0.25 points)
    try:
        sra = config.get('serverReadyAction', {})
        pattern = sra.get('pattern', None) if isinstance(sra, dict) else None
        if pattern == "Listening on port ([0-9]+)":
            print(f"PASS: Component 3 -- serverReadyAction.pattern is correct (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- serverReadyAction.pattern expected 'Listening on port ([0-9]+)', found: {pattern!r}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: serverReadyAction.action is "openExternally" or "debugWithChrome" (0.20 points)
    try:
        sra = config.get('serverReadyAction', {})
        action = sra.get('action', None) if isinstance(sra, dict) else None
        if action in ("openExternally", "debugWithChrome"):
            print(f"PASS: Component 4 -- serverReadyAction.action is '{action}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 -- serverReadyAction.action expected 'openExternally' or 'debugWithChrome', found: {action!r}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: serverReadyAction.uriFormat is "http://localhost:%s" (0.15 points)
    try:
        sra = config.get('serverReadyAction', {})
        uri_format = sra.get('uriFormat', None) if isinstance(sra, dict) else None
        if uri_format == "http://localhost:%s":
            print(f"PASS: Component 5 -- serverReadyAction.uriFormat is correct (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 -- serverReadyAction.uriFormat expected 'http://localhost:%s', found: {uri_format!r}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
