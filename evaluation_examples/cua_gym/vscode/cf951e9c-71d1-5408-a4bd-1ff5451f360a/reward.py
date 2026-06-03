"""
Reward Script: Create a custom JavaScript snippet for arrow function with try-catch
Task ID: vscode_code_016
Domain: vs_code
Scoring:
  Component 1: Snippet entry "Try-Catch Arrow Function" exists in javascript.json (0.2 pts)
  Component 2: Snippet prefix is "trycatch-arrow" (0.3 pts)
  Component 3: Snippet body contains correct arrow function and try-catch structure (0.3 pts)
  Component 4: Snippet description is "Async arrow function with try-catch" (0.2 pts)
Total: 1.0
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_016'
SNIPPET_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'snippets', 'javascript.json')

EXPECTED_SNIPPET_NAME = "Try-Catch Arrow Function"
EXPECTED_PREFIX = "trycatch-arrow"
EXPECTED_DESCRIPTION = "Async arrow function with try-catch"

# Expected body lines (order and content matter)
EXPECTED_BODY = [
    "const ${1:functionName} = async (${2:params}) => {",
    "  try {",
    "    ${3:// code}",
    "  } catch (${4:error}) {",
    "    console.error(${4:error});",
    "  }",
    "};"
]


def verify_task(snippet_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be valid JSON
    try:
        with open(snippet_path, 'r') as f:
            snippets = json.load(f)
    except FileNotFoundError:
        print(f"CRITICAL: Snippet file not found: {snippet_path}")
        print("REWARD: 0.0")
        return 0.0
    except json.JSONDecodeError as e:
        print(f"CRITICAL: Cannot parse JSON in {snippet_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: file must not be empty (just {})
    if not snippets:
        print("FAIL: javascript.json is empty — no snippets defined")
        print("\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Snippet entry "Try-Catch Arrow Function" exists (0.2 points)
    try:
        if EXPECTED_SNIPPET_NAME in snippets:
            print(f"PASS: Component 1 — Snippet entry '{EXPECTED_SNIPPET_NAME}' found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected snippet named '{EXPECTED_SNIPPET_NAME}', "
                  f"found keys: {list(snippets.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Only proceed with inner checks if the snippet entry exists
    snippet = snippets.get(EXPECTED_SNIPPET_NAME, {})

    # Component 2: Prefix is "trycatch-arrow" (0.3 points)
    try:
        actual_prefix = snippet.get('prefix', None)
        if actual_prefix == EXPECTED_PREFIX:
            print(f"PASS: Component 2 — Prefix is '{EXPECTED_PREFIX}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected prefix '{EXPECTED_PREFIX}', found: '{actual_prefix}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Body contains correct arrow function and try-catch structure (0.3 points)
    try:
        actual_body = snippet.get('body', None)
        if not isinstance(actual_body, list):
            print(f"FAIL: Component 3 — 'body' is not a list, found: {type(actual_body)}")
        else:
            # Check all expected body lines are present and in order
            if actual_body == EXPECTED_BODY:
                print(f"PASS: Component 3 — Body matches expected arrow function with try-catch (0.3 pts)")
                total_score += 0.3
            else:
                # Partial check: verify key structural elements
                # Check for arrow function declaration with tab stops
                has_arrow_func = any('async' in line and '=>' in line for line in actual_body)
                has_try = any(line.strip().startswith('try {') or line.strip() == 'try {' for line in actual_body)
                has_catch = any('catch' in line for line in actual_body)
                has_console_error = any('console.error' in line for line in actual_body)
                has_tab_stops = any('${1:' in line and '${2:' in line or '${1:' in ''.join(actual_body) for line in actual_body)

                if has_arrow_func and has_try and has_catch:
                    print(f"FAIL: Component 3 — Body has correct structure but doesn't match exactly. "
                          f"Expected: {EXPECTED_BODY}, Found: {actual_body}")
                else:
                    print(f"FAIL: Component 3 — Body missing required elements. "
                          f"has_arrow_func={has_arrow_func}, has_try={has_try}, "
                          f"has_catch={has_catch}, has_console_error={has_console_error}. "
                          f"Found body: {actual_body}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Description is "Async arrow function with try-catch" (0.2 points)
    try:
        actual_description = snippet.get('description', None)
        if actual_description == EXPECTED_DESCRIPTION:
            print(f"PASS: Component 4 — Description is '{EXPECTED_DESCRIPTION}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — Expected description '{EXPECTED_DESCRIPTION}', "
                  f"found: '{actual_description}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(SNIPPET_PATH):
    print(f"File not found: {SNIPPET_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(SNIPPET_PATH)
