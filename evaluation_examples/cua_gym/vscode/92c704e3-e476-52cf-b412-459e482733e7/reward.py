"""
Reward Script: Rename 'callback' to 'handler' only in registerEvent function
Task ID: vscode_gs_081
Domain: vscode
Scoring:
  Component 1 (0.4): 'callback' replaced with 'handler' in registerEvent function params/body
  Component 2 (0.3): No 'callback' remains in registerEvent function
  Component 3 (0.3): 'callback' in onLoad and fetchData is untouched (6 occurrences remain)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gs_081'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'webapp', 'events.js')


def find_function_block(lines, func_name):
    """Find the start and end line indices (0-based) of a function block."""
    start = None
    brace_count = 0
    for i, line in enumerate(lines):
        if start is None:
            # Look for function declaration
            if re.search(rf'\bfunction\s+{func_name}\b', line):
                start = i
                brace_count = line.count('{') - line.count('}')
        else:
            brace_count += line.count('{') - line.count('}')
            if brace_count <= 0:
                return start, i
    return start, len(lines) - 1 if start is not None else None


def count_word_in_lines(lines, word):
    """Count occurrences of a word (whole word match) in a list of lines."""
    count = 0
    for line in lines:
        count += len(re.findall(rf'\b{word}\b', line))
    return count


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
        lines = content.split('\n')
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Locate the registerEvent function block
    try:
        reg_start, reg_end = find_function_block(lines, 'registerEvent')
        if reg_start is None:
            print("CRITICAL: registerEvent function not found in file")
            print("REWARD: 0.0")
            return 0.0
        register_lines = lines[reg_start:reg_end + 1]
    except Exception as e:
        print(f"ERROR: Could not parse registerEvent function: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Locate onLoad and fetchData function blocks
    try:
        ol_start, ol_end = find_function_block(lines, 'onLoad')
        fd_start, fd_end = find_function_block(lines, 'fetchData')
        onload_lines = lines[ol_start:ol_end + 1] if ol_start is not None else []
        fetchdata_lines = lines[fd_start:fd_end + 1] if fd_start is not None else []
    except Exception as e:
        print(f"ERROR: Could not parse onLoad/fetchData functions: {e}")
        onload_lines = []
        fetchdata_lines = []

    # Component 1: 'handler' appears in registerEvent (should be 4 occurrences) (0.4 points)
    # This checks that the rename actually happened
    try:
        handler_in_register = count_word_in_lines(register_lines, 'handler')
        if handler_in_register >= 4:
            print(f"PASS: Component 1 — 'handler' found {handler_in_register} times in registerEvent (expected >= 4) (0.4 pts)")
            total_score += 0.4
        elif handler_in_register >= 2:
            partial = 0.2
            print(f"PARTIAL: Component 1 — 'handler' found {handler_in_register} times in registerEvent (expected 4), awarding {partial} pts")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — 'handler' found {handler_in_register} times in registerEvent (expected 4)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: No 'callback' remains in registerEvent (0.3 points)
    # Ensures the rename is complete within the function
    try:
        callback_in_register = count_word_in_lines(register_lines, 'callback')
        if callback_in_register == 0:
            print(f"PASS: Component 2 — No 'callback' remains in registerEvent (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — 'callback' still appears {callback_in_register} times in registerEvent")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Scoped rename — 'handler' in registerEvent AND 'callback' preserved in other functions (0.3 points)
    # Compound check: both conditions must hold. This ensures the rename was scoped correctly.
    # Anchored to the task change: requires handler_in_register >= 4 (which only happens after rename).
    try:
        callback_in_onload = count_word_in_lines(onload_lines, 'callback')
        callback_in_fetchdata = count_word_in_lines(fetchdata_lines, 'callback')
        other_callback_count = callback_in_onload + callback_in_fetchdata

        # Both conditions required: rename happened AND other functions untouched
        if handler_in_register >= 4 and other_callback_count >= 6:
            print(f"PASS: Component 3 — Scoped rename verified: 'handler' in registerEvent ({handler_in_register}), 'callback' preserved in onLoad ({callback_in_onload}) + fetchData ({callback_in_fetchdata}) = {other_callback_count} (0.3 pts)")
            total_score += 0.3
        elif handler_in_register >= 4 and other_callback_count >= 4:
            partial = 0.15
            print(f"PARTIAL: Component 3 — Rename done but some 'callback' lost in other functions: onLoad ({callback_in_onload}), fetchData ({callback_in_fetchdata}), total={other_callback_count} (expected 6), awarding {partial} pts")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Scoped rename not verified: 'handler' in registerEvent={handler_in_register} (need 4), 'callback' in others={other_callback_count} (need 6)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
