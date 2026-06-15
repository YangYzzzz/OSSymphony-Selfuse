"""
Reward Script: Fix YAML indentation in GitHub Actions deploy.yml
Task ID: vscode_gf3_023
Domain: vscode
Scoring:
  Component 1 (0.35): 'steps' key is properly indented under each job (4 spaces)
  Component 2 (0.35): Step items (- name:) are properly indented under steps (6 spaces)
  Component 3 (0.30): Step sub-keys (uses/with/run) are properly indented (8 spaces)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_023'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'ci-demo', '.github', 'workflows', 'deploy.yml')


def verify_task(file_path):
    """
    Verify that the deploy.yml indentation has been fixed.
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

    # Precondition: file must contain 'jobs:' section
    if 'jobs:' not in content:
        print("FAIL: Precondition - file does not contain 'jobs:' section")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 'steps:' key is properly indented at 4 spaces under each job (0.35 points)
    # In valid GitHub Actions YAML, 'steps:' should be a direct child of the job,
    # indented at 4 spaces (2 for jobs content + 2 for job properties).
    try:
        steps_lines = [l for l in lines if l.strip() == 'steps:' or l.strip().startswith('steps:')]
        steps_at_4_spaces = 0
        steps_total = 0
        for line in lines:
            stripped = line.strip()
            if stripped == 'steps:':
                steps_total += 1
                leading_spaces = len(line) - len(line.lstrip())
                if leading_spaces == 4:
                    steps_at_4_spaces += 1
                else:
                    print(f"  DETAIL: Found 'steps:' at {leading_spaces} spaces, expected 4")

        if steps_total == 0:
            print("FAIL: Component 1 - no 'steps:' lines found")
        elif steps_at_4_spaces == steps_total:
            print(f"PASS: Component 1 - all {steps_total} 'steps:' keys at 4-space indent (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 - {steps_at_4_spaces}/{steps_total} 'steps:' keys properly indented")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Step list items ('- name:') are at 6 spaces indent (0.35 points)
    # Each step in the steps list should start with '- name:' or '- uses:' at 6 spaces
    # (4 for steps level + 2 for list item)
    try:
        step_items = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('- name:') or stripped.startswith('- uses:') or stripped.startswith('- run:'):
                leading_spaces = len(line) - len(line.lstrip())
                step_items.append(leading_spaces)

        if len(step_items) == 0:
            print("FAIL: Component 2 - no step items found")
        else:
            correct_items = sum(1 for s in step_items if s == 6)
            if correct_items == len(step_items):
                print(f"PASS: Component 2 - all {len(step_items)} step items at 6-space indent (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 - {correct_items}/{len(step_items)} step items at 6 spaces (found indents: {step_items})")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Step sub-keys (uses, with, run, name after first) are at 8 spaces (0.30 points)
    # Keys like 'uses:', 'with:', 'run:' that are NOT list items should be at 8 spaces
    try:
        sub_keys = []
        for line in lines:
            stripped = line.strip()
            # Match non-list-item keys that are step properties
            if (not stripped.startswith('-')) and any(stripped.startswith(k) for k in ['uses:', 'with:', 'run:', 'name:', 'if:']):
                leading_spaces = len(line) - len(line.lstrip())
                # Only count those that are step sub-keys (not top-level or job-level)
                if leading_spaces >= 6:
                    sub_keys.append(leading_spaces)

        if len(sub_keys) == 0:
            print("FAIL: Component 3 - no step sub-keys found")
        else:
            correct_sub = sum(1 for s in sub_keys if s == 8)
            if correct_sub == len(sub_keys):
                print(f"PASS: Component 3 - all {len(sub_keys)} step sub-keys at 8-space indent (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 - {correct_sub}/{len(sub_keys)} sub-keys at 8 spaces (found indents: {sub_keys})")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
