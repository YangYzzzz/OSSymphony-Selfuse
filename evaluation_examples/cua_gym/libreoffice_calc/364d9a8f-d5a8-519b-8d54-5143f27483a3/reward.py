"""
Reward Script: Extract configuration object literal into DEFAULT_CONFIG constant
Task ID: vscode_rrt_056
Domain: vscode (text file verification)
Scoring:
  - Component 1 (0.4): DEFAULT_CONFIG declared at module level
  - Component 2 (0.3): DEFAULT_CONFIG contains correct properties
  - Component 3 (0.3): createMiddleware returns DEFAULT_CONFIG
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_056'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'server', 'app.js')

# Expected properties that must be in DEFAULT_CONFIG
EXPECTED_PROPS = {
    'cors': 'true',
    'maxAge': '86400',
    'methods': "['GET', 'POST', 'PUT', 'DELETE']",
    'allowedHeaders': "['Content-Type', 'Authorization']",
    'credentials': 'true',
}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    lines = content.split('\n')

    # Locate function boundaries and module-level declarations
    # We need to determine if DEFAULT_CONFIG is declared OUTSIDE any function
    # and BEFORE createMiddleware uses it.

    # Component 1: DEFAULT_CONFIG is declared at module level (0.4 points)
    # Check that there's a line like "const DEFAULT_CONFIG = {" or "var/let DEFAULT_CONFIG = {"
    # at the top level (not indented inside a function body)
    try:
        # Find DEFAULT_CONFIG declaration at module level
        # Module-level declarations start at column 0 (no leading whitespace or minimal)
        decl_pattern = re.compile(
            r'^(?:const|let|var)\s+DEFAULT_CONFIG\s*=\s*\{',
            re.MULTILINE
        )
        decl_match = decl_pattern.search(content)

        if decl_match:
            # Verify it's at module level: the line should not be inside a function
            # Check that the declaration appears before createMiddleware function
            decl_pos = decl_match.start()
            func_pattern = re.compile(r'function\s+createMiddleware\s*\(')
            func_match = func_pattern.search(content)

            if func_match and decl_pos < func_match.start():
                print(f"PASS: Component 1 — DEFAULT_CONFIG declared at module level before createMiddleware (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — DEFAULT_CONFIG not declared before createMiddleware")
        else:
            print(f"FAIL: Component 1 — No module-level DEFAULT_CONFIG declaration found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: DEFAULT_CONFIG contains the correct properties (0.3 points)
    # Extract the object assigned to DEFAULT_CONFIG and check key properties
    try:
        # Find the DEFAULT_CONFIG object body
        # Match from "DEFAULT_CONFIG = {" to the closing "}"
        obj_pattern = re.compile(
            r'(?:const|let|var)\s+DEFAULT_CONFIG\s*=\s*(\{[^}]*\})',
            re.DOTALL
        )
        obj_match = obj_pattern.search(content)

        if obj_match:
            obj_body = obj_match.group(1)
            props_found = 0
            total_props = 5  # cors, maxAge, methods, allowedHeaders, credentials

            # Check each expected property exists in the object
            if re.search(r'cors\s*:\s*true', obj_body):
                props_found += 1
            else:
                print(f"  DETAIL: Missing or wrong 'cors' property")

            if re.search(r'maxAge\s*:\s*86400', obj_body):
                props_found += 1
            else:
                print(f"  DETAIL: Missing or wrong 'maxAge' property")

            if re.search(r"methods\s*:\s*\[\s*['\"]GET['\"]", obj_body):
                props_found += 1
            else:
                print(f"  DETAIL: Missing or wrong 'methods' property")

            if re.search(r"allowedHeaders\s*:\s*\[\s*['\"]Content-Type['\"]", obj_body):
                props_found += 1
            else:
                print(f"  DETAIL: Missing or wrong 'allowedHeaders' property")

            if re.search(r'credentials\s*:\s*true', obj_body):
                props_found += 1
            else:
                print(f"  DETAIL: Missing or wrong 'credentials' property")

            if props_found == total_props:
                print(f"PASS: Component 2 — DEFAULT_CONFIG has all {total_props} expected properties (0.3 pts)")
                total_score += 0.3
            elif props_found > 0:
                partial = round(0.3 * props_found / total_props, 2)
                print(f"PARTIAL: Component 2 — {props_found}/{total_props} properties found ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — No expected properties found in DEFAULT_CONFIG")
        else:
            print(f"FAIL: Component 2 — Could not find DEFAULT_CONFIG object body")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: createMiddleware returns DEFAULT_CONFIG (0.3 points)
    # The function should return DEFAULT_CONFIG (or a spread/copy of it), NOT the inline object literal
    try:
        # Extract the createMiddleware function body
        func_pattern = re.compile(
            r'function\s+createMiddleware\s*\(\s*\)\s*\{(.*?)\}',
            re.DOTALL
        )
        func_match = func_pattern.search(content)

        if func_match:
            func_body = func_match.group(1)

            # Check that the function returns DEFAULT_CONFIG (or a copy like {...DEFAULT_CONFIG})
            returns_config = bool(re.search(r'return\s+DEFAULT_CONFIG\s*;?', func_body))
            returns_spread = bool(re.search(r'return\s+\{\s*\.\.\.DEFAULT_CONFIG\s*\}', func_body))
            returns_assign = bool(re.search(r'return\s+Object\.assign\(\s*\{\}\s*,\s*DEFAULT_CONFIG\s*\)', func_body))

            # Also verify the function does NOT still contain the inline object literal
            has_inline_object = bool(re.search(r'return\s*\{[^}]*cors\s*:', func_body))

            if (returns_config or returns_spread or returns_assign) and not has_inline_object:
                print(f"PASS: Component 3 — createMiddleware returns DEFAULT_CONFIG (0.3 pts)")
                total_score += 0.3
            elif returns_config or returns_spread or returns_assign:
                # Returns DEFAULT_CONFIG but also has inline — partial credit
                print(f"PARTIAL: Component 3 — returns DEFAULT_CONFIG but inline object still present (0.15 pts)")
                total_score += 0.15
            elif has_inline_object:
                print(f"FAIL: Component 3 — createMiddleware still returns inline object literal")
            else:
                print(f"FAIL: Component 3 — createMiddleware does not return DEFAULT_CONFIG")
        else:
            print(f"FAIL: Component 3 — createMiddleware function not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
