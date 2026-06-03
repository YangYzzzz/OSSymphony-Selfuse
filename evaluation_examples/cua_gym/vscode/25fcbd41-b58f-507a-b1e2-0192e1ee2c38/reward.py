"""
Reward Script: Replace all print( with logging.info( in debug_exercise.py
Task ID: vscode_stu_029
Domain: vscode
Scoring:
  Precondition gate: File integrity (structure preserved)
  Component 1 (0.5): No print( calls remain in the file
  Component 2 (0.5): Exactly 8 logging.info( calls present
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_029'
FILE_NAME = 'debug_exercise.py'


def verify_task(file_path):
    """
    Verify that all 8 print( statements were replaced with logging.info(.
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

    # Precondition gate: File integrity check
    # These are pre-existing properties -- used as a gate, not for scoring
    try:
        integrity_checks = [
            ('REQUEST_LOG definition', 'REQUEST_LOG' in content),
            ('analyze_requests function', 'def analyze_requests' in content),
            ('generate_report function', 'def generate_report' in content),
            ('main function', 'def main' in content),
            ('LATENCY_THRESHOLD_MS', 'LATENCY_THRESHOLD_MS = 1000' in content),
            ('defaultdict import', 'from collections import defaultdict' in content),
        ]

        failed = [name for name, ok in integrity_checks if not ok]
        if failed:
            print(f"GATE FAIL: File integrity broken, missing: {failed}")
            print("REWARD: 0.0")
            return 0.0
        else:
            print(f"GATE PASS: All {len(integrity_checks)} integrity checks passed")
    except Exception as e:
        print(f"GATE ERROR: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Helper: count pattern occurrences in code lines (skip docstrings/comments)
    def count_in_code(pattern):
        count = 0
        in_docstring = False
        for line in lines:
            stripped = line.strip()
            # Track triple-quote docstrings
            if '"""' in stripped or "'''" in stripped:
                quote = '"""' if '"""' in stripped else "'''"
                num_quotes = stripped.count(quote)
                if in_docstring:
                    in_docstring = False
                    continue
                elif num_quotes == 1:
                    in_docstring = True
                    continue
            if in_docstring:
                continue
            if stripped.startswith('#'):
                continue
            if re.search(pattern, stripped):
                count += 1
        return count

    # Component 1: No print( calls remain in the code (0.5 points)
    # Initial file has 8 print( calls; golden has 0. This check FAILS on initial, PASSES on golden.
    try:
        print_count = count_in_code(r'\bprint\s*\(')
        if print_count == 0:
            print(f"PASS: Component 1 -- No print() calls found in code (0.5 pts)")
            total_score += 0.5
        else:
            # Partial credit: each removal is worth a fraction
            removed = max(0, 8 - print_count)
            if removed > 0:
                partial = 0.5 * (removed / 8)
                print(f"PARTIAL: Component 1 -- {print_count} print() calls remain ({removed}/8 removed) ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 1 -- Found {print_count} print() calls, expected 0")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Exactly 8 logging.info( calls present (0.5 points)
    # Initial file has 0 logging.info( calls; golden has 8. This check FAILS on initial, PASSES on golden.
    try:
        logging_info_count = count_in_code(r'\blogging\.info\s*\(')
        if logging_info_count == 8:
            print(f"PASS: Component 2 -- Found exactly 8 logging.info() calls (0.5 pts)")
            total_score += 0.5
        elif logging_info_count > 0:
            partial = 0.5 * (logging_info_count / 8)
            print(f"PARTIAL: Component 2 -- Found {logging_info_count}/8 logging.info() calls ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- Found {logging_info_count} logging.info() calls, expected 8")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = os.path.join(WORKDIR, FILE_NAME)
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
