"""
Reward Script: Create tasks.json with pickString input for test suite selection
Task ID: vscode_td_015
Domain: vscode
Scoring:
  Component 1: tasks.json exists and is valid JSON with version 2.0.0 — 0.15 pts
  Component 2: inputs array has a pickString input with id "testSuite" — 0.25 pts
  Component 3: Input options are exactly ["unit", "integration", "e2e"] — 0.25 pts
  Component 4: A task command references ${input:testSuite} — 0.20 pts
  Component 5: Task command is "pytest tests/${input:testSuite}/" — 0.15 pts
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_015'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'django-app', '.vscode', 'tasks.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: tasks.json must exist — if not, nothing to verify
    if not os.path.exists(TASKS_JSON_PATH):
        print(f"CRITICAL: tasks.json not found at {TASKS_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Try to load the JSON (handles JSONC with comments)
    try:
        with open(TASKS_JSON_PATH, 'r') as f:
            raw = f.read()
        # Strip single-line comments (// ...) for JSONC compatibility
        cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
        # Strip trailing commas before } or ]
        cleaned = re.sub(r',\s*([}\]])', r'\1', cleaned)
        data = json.loads(cleaned)
    except Exception as e:
        print(f"CRITICAL: Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid JSON with version "2.0.0" (0.15 points)
    try:
        version = data.get("version", "")
        if version == "2.0.0":
            print(f"PASS: Component 1 — version is '2.0.0' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — expected version '2.0.0', found '{version}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: inputs array has a pickString input with id "testSuite" (0.25 points)
    try:
        inputs = data.get("inputs", [])
        found_pick_string_input = False
        for inp in inputs:
            if (isinstance(inp, dict)
                    and inp.get("id") == "testSuite"
                    and inp.get("type") == "pickString"):
                found_pick_string_input = True
                break
        if found_pick_string_input:
            print(f"PASS: Component 2 — pickString input with id 'testSuite' found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — no pickString input with id 'testSuite' in inputs: {inputs}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Input options are exactly ["unit", "integration", "e2e"] (0.25 points)
    try:
        inputs = data.get("inputs", [])
        options_correct = False
        for inp in inputs:
            if isinstance(inp, dict) and inp.get("id") == "testSuite":
                options = inp.get("options", [])
                # Check all three required options are present (order-independent)
                expected_options = {"unit", "integration", "e2e"}
                actual_options = set(options) if isinstance(options, list) else set()
                if expected_options == actual_options:
                    options_correct = True
                break
        if options_correct:
            print(f"PASS: Component 3 — options contain 'unit', 'integration', 'e2e' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — options mismatch, expected {{'unit', 'integration', 'e2e'}}, found: {options if 'options' in dir() else 'N/A'}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: A task command references ${input:testSuite} (0.20 points)
    try:
        tasks = data.get("tasks", [])
        found_input_ref = False
        for task in tasks:
            if isinstance(task, dict):
                cmd = task.get("command", "")
                if "${input:testSuite}" in str(cmd):
                    found_input_ref = True
                    break
        if found_input_ref:
            print(f"PASS: Component 4 — task command references ${{input:testSuite}} (0.20 pts)")
            total_score += 0.20
        else:
            cmds = [t.get("command", "") for t in tasks if isinstance(t, dict)]
            print(f"FAIL: Component 4 — no task command references ${{input:testSuite}}. Commands found: {cmds}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Task command is "pytest tests/${input:testSuite}/" (0.15 points)
    try:
        tasks = data.get("tasks", [])
        cmd_correct = False
        for task in tasks:
            if isinstance(task, dict):
                cmd = str(task.get("command", ""))
                # Normalize: check the command contains the pytest pattern
                if "pytest" in cmd and "tests/${input:testSuite}/" in cmd:
                    cmd_correct = True
                    break
        if cmd_correct:
            print(f"PASS: Component 5 — command is 'pytest tests/${{input:testSuite}}/' (0.15 pts)")
            total_score += 0.15
        else:
            cmds = [t.get("command", "") for t in tasks if isinstance(t, dict)]
            print(f"FAIL: Component 5 — command doesn't match expected pattern. Commands: {cmds}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    # Round to avoid floating point issues
    final_score = round(final_score, 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
