"""
Reward Script: Insert a 'switch' statement using the built-in JavaScript snippet inside the processCommand function.
Task ID: vscode_code_022
Domain: vs_code
Scoring:
  Component 1: switch(command) statement inserted inside processCommand (0.3 pts)
  Component 2: Cases for 'start', 'stop', 'restart' are all present (0.4 pts)
  Component 3: Default case present AND all cases have break statements (0.3 pts)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_022'
FILE_PATH = os.path.join(WORKDIR, 'project', 'commands.js')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Checks that a switch statement was inserted inside processCommand,
    with cases for 'start', 'stop', 'restart', a default case, and break statements.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be readable
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        print(f"INFO: File loaded successfully from {file_path}")
        print(f"INFO: File content:\n{content}")
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: processCommand function must still be present
    if 'processCommand' not in content:
        print("CRITICAL: processCommand function not found in file")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: switch(command) statement inserted inside processCommand (0.3 points)
    # This must FAIL on initial_env (no switch) and PASS on golden_env (switch present)
    try:
        # Look for switch statement with 'command' as the expression inside processCommand
        # Extract the processCommand function body
        func_match = re.search(
            r'function\s+processCommand\s*\([^)]*\)\s*\{([\s\S]*?)\n\}',
            content
        )
        if func_match:
            func_body = func_match.group(1)
            # Check for switch(command) — allow optional whitespace
            switch_match = re.search(r'switch\s*\(\s*command\s*\)', func_body)
            if switch_match:
                print(f"PASS: Component 1 — switch(command) statement found inside processCommand (0.3 pts)")
                total_score += 0.3
            else:
                # Check if any switch statement exists in function body
                any_switch = re.search(r'switch\s*\(', func_body)
                if any_switch:
                    print(f"FAIL: Component 1 — switch statement found but not switch(command); found: {any_switch.group()}")
                else:
                    print(f"FAIL: Component 1 — no switch statement found inside processCommand")
        else:
            print("FAIL: Component 1 — could not extract processCommand function body")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Cases for 'start', 'stop', 'restart' are all present (0.4 points)
    # This must FAIL on initial_env and PASS on golden_env
    try:
        required_cases = ["'start'", "'stop'", "'restart'"]
        # Also accept double-quoted variants
        required_cases_double = ['"start"', '"stop"', '"restart"']

        cases_found = []
        cases_missing = []

        for i, (single, double) in enumerate(zip(required_cases, required_cases_double)):
            case_pattern = rf'case\s+({re.escape(single)}|{re.escape(double)})\s*:'
            if re.search(case_pattern, content):
                cases_found.append(single.strip("'"))
            else:
                cases_missing.append(single.strip("'"))

        if len(cases_found) == 3:
            print(f"PASS: Component 2 — all required cases found: {cases_found} (0.4 pts)")
            total_score += 0.4
        elif len(cases_found) > 0:
            print(f"PARTIAL: Component 2 — only {len(cases_found)}/3 required cases found: {cases_found}; missing: {cases_missing}")
            # No partial credit at this level — all 3 must be present
        else:
            print(f"FAIL: Component 2 — no required cases ('start', 'stop', 'restart') found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Default case present AND all cases have break statements (0.3 points)
    # This must FAIL on initial_env and PASS on golden_env
    try:
        # Check for default case
        default_match = re.search(r'default\s*:', content)
        has_default = default_match is not None

        # Count break statements in the switch body
        # Extract the switch block if it exists
        switch_block_match = re.search(
            r'switch\s*\(\s*command\s*\)\s*\{([\s\S]*?)\n\s*\}',
            content
        )
        if switch_block_match:
            switch_body = switch_block_match.group(1)
            break_count = len(re.findall(r'\bbreak\s*;', switch_body))
            # We expect 4 breaks: one for each of start, stop, restart, and default
            has_breaks = break_count >= 4
        else:
            break_count = len(re.findall(r'\bbreak\s*;', content))
            has_breaks = break_count >= 4

        if has_default and has_breaks:
            print(f"PASS: Component 3 — default case present AND {break_count} break statement(s) found (0.3 pts)")
            total_score += 0.3
        elif has_default and not has_breaks:
            print(f"FAIL: Component 3 — default case present but only {break_count} break statement(s) found (expected 4)")
        elif not has_default and has_breaks:
            print(f"FAIL: Component 3 — {break_count} break statement(s) found but no default case")
        else:
            print(f"FAIL: Component 3 — no default case and insufficient break statements ({break_count} found, expected 4)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical file path on VM
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
