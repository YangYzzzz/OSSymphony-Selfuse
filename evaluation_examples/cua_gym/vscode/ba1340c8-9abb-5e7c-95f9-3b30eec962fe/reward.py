"""
Reward Script: Only format the calculateTotal function in the JavaScript file
Task ID: vscode_code_005
Domain: vs_code
Scoring:
  - Component 1 (0.5 pts): calculateTotal function body is properly formatted (multi-line with indentation)
  - Component 2 (0.3 pts): Compound — function is reformatted AND all original logic patterns are present
  - Component 3 (0.2 pts): Compound — function is reformatted AND non-function odd-spaced lines unchanged
  (Components 2 and 3 are gated on Component 1, so initial_env scores 0.0)
Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_005'
FILE_PATH = '/home/user/project/utils.js'

# These lines outside the function must remain byte-for-byte unchanged
PRESERVED_LINES = [
    "const   API_URL =   'https://api.example.com';",
    "const   TIMEOUT =   5000;",
    "var   x =   1;",
    "var   y =   2;",
]


def find_function_bounds_by_brace(lines, func_name):
    """
    Find start/end indices of a named JS function using brace counting.
    Returns (start_index, end_index) or (None, None) if not found.
    """
    func_start = None
    for i, line in enumerate(lines):
        if re.match(r'\s*function\s+' + re.escape(func_name) + r'\s*\(', line):
            func_start = i
            break

    if func_start is None:
        return None, None

    brace_depth = 0
    for i in range(func_start, len(lines)):
        brace_depth += lines[i].count('{') - lines[i].count('}')
        if i > func_start and brace_depth == 0:
            return func_start, i

    return func_start, None


def check_function_formatted(lines):
    """
    Returns True if calculateTotal is properly multi-line formatted.
    Initial state (minified): 3 lines, no indentation.
    Golden state (formatted): 9+ lines with properly indented statements.
    """
    func_start, func_end = find_function_bounds_by_brace(lines, 'calculateTotal')
    if func_start is None or func_end is None:
        return False, "function not found or unclosed"

    func_lines = lines[func_start:func_end + 1]
    num_func_lines = func_end - func_start + 1

    has_indented_let = any(re.match(r'^\s{2,}let\s+total', l) for l in func_lines)
    has_indented_for = any(re.match(r'^\s{2,}for\s*\(', l) for l in func_lines)
    has_indented_return = any(re.match(r'^\s{2,}return\s+total', l) for l in func_lines)
    is_multiline = num_func_lines >= 7

    if is_multiline and has_indented_let and has_indented_for and has_indented_return:
        return True, f"{num_func_lines} lines, indented let/for/return"
    return False, (f"lines={num_func_lines}(need>=7), "
                   f"indented_let={has_indented_let}, "
                   f"indented_for={has_indented_for}, "
                   f"indented_return={has_indented_return}")


def check_logic_preserved(lines):
    """
    Returns True if calculateTotal still contains all required logic patterns.
    """
    func_start, func_end = find_function_bounds_by_brace(lines, 'calculateTotal')
    if func_start is None or func_end is None:
        return False, ["function not found"]

    func_body = '\n'.join(lines[func_start:func_end + 1])
    func_body_norm = re.sub(r'\s+', ' ', func_body)

    required = [
        (r'let\s+total\s*=\s*0', "let total=0"),
        (r'for\s*\(let\s+i\s*=', "for loop init"),
        (r'items\.length', "items.length"),
        (r'items\[i\]\.price', "items[i].price"),
        (r'items\[i\]\.quantity', "items[i].quantity"),
        (r'return\s+total', "return total"),
    ]
    missing = [desc for pat, desc in required if not re.search(pat, func_body_norm)]
    return len(missing) == 0, missing


def check_preserved_lines(lines):
    """
    Returns True if all non-function odd-spaced lines are intact.
    """
    missing = [pl for pl in PRESERVED_LINES if pl not in lines]
    return len(missing) == 0, missing


def verify_task(file_path):
    """
    Verify that ONLY the calculateTotal function was reformatted.
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

    lines = content.splitlines()

    # -----------------------------------------------------------------------
    # Component 1: calculateTotal function is properly formatted — 0.5 pts
    # FAILS on initial (3-line minified body), PASSES on golden (9-line indented body)
    # -----------------------------------------------------------------------
    try:
        fmt_ok, fmt_detail = check_function_formatted(lines)
        if fmt_ok:
            print(f"PASS: Component 1 — calculateTotal is properly formatted ({fmt_detail}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Function NOT properly formatted: {fmt_detail}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        fmt_ok = False

    # -----------------------------------------------------------------------
    # Component 2: Logic preserved after reformatting — 0.3 pts (compound with Component 1)
    # Gated on Component 1: only awarded when function is reformatted.
    # This ensures initial_env (where Component 1 fails) scores 0 here.
    # -----------------------------------------------------------------------
    if fmt_ok:
        try:
            logic_ok, missing_patterns = check_logic_preserved(lines)
            if logic_ok:
                print(f"PASS: Component 2 — All logic patterns present in reformatted function (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Missing logic patterns after reformatting: {missing_patterns}")
        except Exception as e:
            print(f"ERROR: Component 2 — {e}")
    else:
        print("SKIP: Component 2 — Skipped (Component 1 failed)")

    # -----------------------------------------------------------------------
    # Component 3: Non-function odd-spaced lines unchanged — 0.2 pts (compound with Component 1)
    # Gated on Component 1: only awarded when function is reformatted.
    # On initial_env: Component 1 fails → this is skipped → 0 points.
    # On golden_env: Component 1 passes → check preserved lines → should pass.
    # -----------------------------------------------------------------------
    if fmt_ok:
        try:
            preserved_ok, missing_lines = check_preserved_lines(lines)
            if preserved_ok:
                print(f"PASS: Component 3 — All {len(PRESERVED_LINES)} non-function "
                      f"odd-spaced lines are unchanged (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — {len(missing_lines)} preserved lines modified or missing:")
                for ml in missing_lines:
                    print(f"  Missing: {repr(ml)}")
        except Exception as e:
            print(f"ERROR: Component 3 — {e}")
    else:
        print("SKIP: Component 3 — Skipped (Component 1 failed)")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
