"""
Reward Script: Convert class component to functional component with hooks
Task ID: vscode_rrt_046
Domain: vscode
Scoring:
  - Component 1: Import updated to hooks (0.15)
  - Component 2: Function component declaration (0.25)
  - Component 3: useState hooks for state variables (0.25)
  - Component 4: useRef for interval reference (0.15)
  - Component 5: No class component syntax remaining (0.10)
  - Component 6: Export default preserved (0.10)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_046'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'app', 'Timer.jsx')


def verify_task(file_path):
    """
    Verify that the React class component has been converted to a
    functional component using hooks (useState, useRef).
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Read file content
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Import updated to use hooks instead of Component (0.15 points)
    # The import should include useState (and optionally useRef/useEffect)
    # and should NOT import Component
    try:
        has_usestate_import = bool(re.search(r'import\s+React\s*,\s*\{[^}]*useState[^}]*\}', content))
        has_component_import = bool(re.search(r'import\s+React\s*,\s*\{[^}]*Component[^}]*\}', content))
        if has_usestate_import and not has_component_import:
            print(f"PASS: Component 1 — Import uses hooks (useState), no Component import (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected useState import without Component. "
                  f"Has useState: {has_usestate_import}, Has Component: {has_component_import}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Function component declaration (0.25 points)
    # Should be a function declaration (function Timer or const Timer = ...)
    # and NOT a class declaration
    try:
        has_function_decl = bool(re.search(
            r'(function\s+Timer\s*\(|const\s+Timer\s*=\s*(function|\())', content
        ))
        has_class_decl = bool(re.search(r'class\s+Timer\s+extends\s+Component', content))
        if has_function_decl and not has_class_decl:
            print(f"PASS: Component 2 — Function component declaration found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Expected function declaration, no class. "
                  f"Has function: {has_function_decl}, Has class: {has_class_decl}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: useState hooks for state variables (0.25 points)
    # Should have useState for 'seconds' and 'running'
    try:
        has_seconds_state = bool(re.search(
            r'(const\s+\[seconds\s*,\s*setSeconds\]\s*=\s*useState|useState\s*\(\s*0\s*\))', content
        ))
        has_running_state = bool(re.search(
            r'(const\s+\[running\s*,\s*setRunning\]\s*=\s*useState|useState\s*\(\s*false\s*\))', content
        ))
        if has_seconds_state and has_running_state:
            print(f"PASS: Component 3 — Both useState hooks found (seconds, running) (0.25 pts)")
            total_score += 0.25
        elif has_seconds_state or has_running_state:
            print(f"PARTIAL: Component 3 — Only one useState hook found (0.125 pts)")
            total_score += 0.125
        else:
            print(f"FAIL: Component 3 — No useState hooks found for seconds/running")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: useRef for interval reference (0.15 points)
    # Should use useRef for storing the interval ID
    try:
        has_useref_import = bool(re.search(r'import\s+React\s*,\s*\{[^}]*useRef[^}]*\}', content))
        has_useref_call = bool(re.search(r'useRef\s*\(', content))
        if has_useref_import and has_useref_call:
            print(f"PASS: Component 4 — useRef imported and used for interval (0.15 pts)")
            total_score += 0.15
        elif has_useref_call:
            # useRef used but maybe imported differently
            print(f"PARTIAL: Component 4 — useRef called but import not standard (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — useRef not found for interval reference")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: No class component syntax remaining (0.10 points)
    # Should not contain this.state, this.setState, constructor, render()
    try:
        class_patterns = [
            r'this\.state\b',
            r'this\.setState\b',
            r'constructor\s*\(',
            r'render\s*\(\s*\)\s*\{',
        ]
        class_remnants = []
        for pattern in class_patterns:
            if re.search(pattern, content):
                class_remnants.append(pattern)

        if not class_remnants:
            print(f"PASS: Component 5 — No class component syntax remaining (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — Class syntax remnants found: {class_remnants}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Export default preserved AND function component (0.10 points)
    # Compound check: export must be preserved AND the component must be a function
    # (not a class). This ensures we only score the converted state.
    try:
        has_export = bool(re.search(r'export\s+default\s+Timer', content))
        is_functional = bool(re.search(
            r'(function\s+Timer\s*\(|const\s+Timer\s*=\s*(function|\())', content
        )) and not bool(re.search(r'class\s+Timer\s+extends', content))
        if has_export and is_functional:
            print(f"PASS: Component 6 — export default Timer preserved with functional component (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 — export: {has_export}, functional: {is_functional}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
