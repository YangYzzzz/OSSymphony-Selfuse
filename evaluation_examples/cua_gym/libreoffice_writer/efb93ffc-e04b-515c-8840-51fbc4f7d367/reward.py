"""
Reward Script: Extract Python code lines from python_tutorial.odt into extracted_code.py
Task ID: osworld_multi_apps_code_to_writer_file_001
Domain: libreoffice_writer (multi-apps: odt -> .py file)
Scoring:
  Component 1: extracted_code.py exists on Desktop (0.2 pts)
  Component 2: All expected Python code lines are present (0.5 pts)
  Component 3: No explanatory English text lines are included (0.2 pts)
  Component 4: Lines are in the correct original order (0.1 pts)
Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_to_writer_file_001'

# Expected Python code lines extracted from python_tutorial.odt (in order)
EXPECTED_CODE_LINES = [
    'import os',
    'import sys',
    'import math',
    'data = [3, 7, 12, 5, 9, 14, 2, 8, 11, 6]',
    'total = 0',
    'def calculate_average(numbers):',
    '    if len(numbers) == 0:',
    '        return 0',
    '    result = sum(numbers) / len(numbers)',
    '    return result',
    'for item in data:',
    '    total = total + item',
    'average = calculate_average(data)',
    "print('Data:', data)",
    "print('Total:', total)",
    "print('Average:', average)",
    'if average > 7:',
    "    print('Above threshold')",
    'max_value = max(data)',
    "print('Max:', max_value)",
]

# Patterns that identify explanatory English prose (should NOT be in extracted_code.py)
ENGLISH_PROSE_PATTERNS = [
    r'^This tutorial',
    r'^The os module',
    r'^We also import',
    r'^The math module',
    r'^Here we define',
    r'^We initialize',
    r'^This function',
    r'^We first check',
    r'^If the list',
    r'^Otherwise we',
    r'^The function returns',
    r'^We iterate',
    r'^During each iteration',
    r'^After the loop',
    r'^We print',
    r'^Printing the',
    r'^Now we check',
    r'^If the average',
    r'^We also find',
]


def verify_task():
    """
    Verify that extracted_code.py exists on Desktop and contains
    only the Python code lines from python_tutorial.odt in original order.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    target_path = os.path.join(WORKDIR, 'Desktop', 'extracted_code.py')

    # Component 1: extracted_code.py exists on the Desktop (0.2 points)
    # This file does NOT exist in initial_env, so existence is a task-introduced change.
    try:
        if os.path.exists(target_path):
            print(f"PASS: Component 1 — extracted_code.py exists on Desktop (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — extracted_code.py not found at {target_path}")
            # Cannot proceed with further checks
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load the extracted file
    try:
        with open(target_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {target_path}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Get non-empty lines from the extracted file
    extracted_lines = [line.rstrip('\n') for line in raw_content.splitlines() if line.strip() != '']

    # Component 2: All expected Python code lines are present (0.5 points)
    # Each expected line must appear somewhere in the extracted file.
    try:
        present_count = 0
        missing_lines = []
        for expected_line in EXPECTED_CODE_LINES:
            if expected_line in extracted_lines:
                present_count += 1
            else:
                missing_lines.append(expected_line)

        ratio = present_count / len(EXPECTED_CODE_LINES)

        if present_count == len(EXPECTED_CODE_LINES):
            print(f"PASS: Component 2 — All {len(EXPECTED_CODE_LINES)} expected code lines present (0.5 pts)")
            total_score += 0.5
        elif present_count > 0:
            component2_score = round(0.5 * ratio, 4)
            print(f"PARTIAL: Component 2 — {present_count}/{len(EXPECTED_CODE_LINES)} code lines present ({component2_score:.4f} pts)")
            if missing_lines:
                print(f"  Missing lines: {missing_lines[:5]}")
            total_score += component2_score
        else:
            print(f"FAIL: Component 2 — No expected code lines found in extracted file")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: No explanatory English prose lines included (0.2 points)
    # Check that none of the explanatory text lines from the tutorial appear in the file.
    try:
        english_found = []
        for line in extracted_lines:
            for pattern in ENGLISH_PROSE_PATTERNS:
                if re.match(pattern, line.strip()):
                    english_found.append(line)
                    break

        if len(english_found) == 0:
            print(f"PASS: Component 3 — No explanatory English prose found in extracted file (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Found {len(english_found)} English prose line(s) in extracted file:")
            for el in english_found[:3]:
                print(f"  '{el}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Lines are in the correct original order (0.1 points)
    # The extracted code lines that DO appear in the file should be in the same
    # relative order as they appear in the source document.
    try:
        # Build the subsequence of expected lines that appear in extracted_lines
        extracted_set_positions = {}
        for i, line in enumerate(extracted_lines):
            if line not in extracted_set_positions:
                extracted_set_positions[line] = i

        order_sequence = []
        for expected_line in EXPECTED_CODE_LINES:
            if expected_line in extracted_set_positions:
                order_sequence.append(extracted_set_positions[expected_line])

        # Check if the positions are in non-decreasing order (preserving relative order)
        is_ordered = all(order_sequence[i] <= order_sequence[i + 1]
                         for i in range(len(order_sequence) - 1))

        if is_ordered and len(order_sequence) > 0:
            print(f"PASS: Component 4 — Code lines are in correct original order (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 4 — Code lines are NOT in correct original order")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
