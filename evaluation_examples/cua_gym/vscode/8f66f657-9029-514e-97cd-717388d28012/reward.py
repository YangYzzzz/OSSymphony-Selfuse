"""
Reward Script: Extract to inner function refactoring - isValidRange
Task ID: vscode_rrt_048
Domain: vscode
Scoring:
  Component 1 (0.3): isValidRange function is defined with correct signature
  Component 2 (0.15): age check uses isValidRange(data.age, 0, 150)
  Component 3 (0.15): score check uses isValidRange(data.score, 0, 100)
  Component 4 (0.15): temperature check uses isValidRange(data.temperature, -50, 60)
  Component 5 (0.25): Function behavior is preserved (functional equivalence test)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_048'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'form', 'validation.js')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be readable
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: isValidRange inner function is defined (0.3 points)
    # Check that a function named isValidRange exists with parameters for value, min, max
    try:
        # Match function definition - could be inner function or standalone
        # Accept various parameter names but must have 3 params
        func_pattern = r'function\s+isValidRange\s*\(\s*(\w+)\s*,\s*(\w+)\s*,\s*(\w+)\s*\)'
        # Also accept arrow function form: const isValidRange = (value, min, max) =>
        arrow_pattern = r'(?:const|let|var)\s+isValidRange\s*=\s*\(\s*(\w+)\s*,\s*(\w+)\s*,\s*(\w+)\s*\)\s*=>'

        func_match = re.search(func_pattern, content)
        arrow_match = re.search(arrow_pattern, content)

        if func_match or arrow_match:
            print(f"PASS: Component 1 — isValidRange function defined with 3 parameters (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — isValidRange function not found with expected signature")
            print(f"  Content snippet: {content[:300]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: age check uses isValidRange (0.15 points)
    try:
        # Look for isValidRange call with data.age and bounds 0, 150
        age_pattern = r'isValidRange\s*\(\s*data\.age\s*,\s*0\s*,\s*150\s*\)'
        if re.search(age_pattern, content):
            print(f"PASS: Component 2 — age check uses isValidRange(data.age, 0, 150) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — age check does not use isValidRange(data.age, 0, 150)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: score check uses isValidRange (0.15 points)
    try:
        score_pattern = r'isValidRange\s*\(\s*data\.score\s*,\s*0\s*,\s*100\s*\)'
        if re.search(score_pattern, content):
            print(f"PASS: Component 3 — score check uses isValidRange(data.score, 0, 100) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — score check does not use isValidRange(data.score, 0, 100)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: temperature check uses isValidRange (0.15 points)
    try:
        temp_pattern = r'isValidRange\s*\(\s*data\.temperature\s*,\s*-50\s*,\s*60\s*\)'
        if re.search(temp_pattern, content):
            print(f"PASS: Component 4 — temperature check uses isValidRange(data.temperature, -50, 60) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — temperature check does not use isValidRange(data.temperature, -50, 60)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Old inline comparisons removed AND structure preserved (0.25 points)
    # This component is anchored to the task change: it requires that the old inline
    # comparisons are gone (proving refactoring happened) AND the function structure is intact.
    # Both sub-conditions must pass for any points to be awarded.
    try:
        # Check that the old inline pattern is gone (data.age < 0 || data.age > 150)
        old_inline_pattern = r'data\.\w+\s*<\s*-?\d+\s*\|\|\s*data\.\w+\s*>\s*-?\d+'
        has_old_inline = re.search(old_inline_pattern, content)

        # Check that validateForm function still exists
        has_validate_form = re.search(r'function\s+validateForm\s*\(\s*data\s*\)', content)

        # Check that return { valid: true } still exists (final return)
        has_valid_return = re.search(r'return\s*\{\s*valid\s*:\s*true\s*\}', content)

        # Check that return { valid: false, field: 'age' } etc. still exist
        has_age_return = re.search(r"return\s*\{\s*valid\s*:\s*false\s*,\s*field\s*:\s*['\"]age['\"]", content)
        has_score_return = re.search(r"return\s*\{\s*valid\s*:\s*false\s*,\s*field\s*:\s*['\"]score['\"]", content)
        has_temp_return = re.search(r"return\s*\{\s*valid\s*:\s*false\s*,\s*field\s*:\s*['\"]temperature['\"]", content)

        inline_removed = not has_old_inline
        structure_intact = (has_validate_form and has_valid_return and
                           has_age_return and has_score_return and has_temp_return)

        if inline_removed and structure_intact:
            print(f"PASS: Component 5 — old inline checks removed AND structure preserved (0.25 pts)")
            total_score += 0.25
        else:
            if not inline_removed:
                print(f"FAIL: Component 5 — old inline comparisons still present")
            if not structure_intact:
                missing = []
                if not has_validate_form:
                    missing.append("validateForm function")
                if not has_valid_return:
                    missing.append("return {valid: true}")
                if not has_age_return:
                    missing.append("return {valid: false, field: 'age'}")
                if not has_score_return:
                    missing.append("return {valid: false, field: 'score'}")
                if not has_temp_return:
                    missing.append("return {valid: false, field: 'temperature'}")
                print(f"FAIL: Component 5 — missing structural elements: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
