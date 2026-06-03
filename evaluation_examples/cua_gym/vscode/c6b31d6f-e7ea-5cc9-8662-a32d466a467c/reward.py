"""
Reward Script: Add 'async' keyword before function declarations that use 'await' in fetcher.js
Task ID: vscode_edit_082
Domain: vs_code
Scoring:
  Component 1: fetchUser declared as 'async function'     — 0.34 pts
  Component 2: fetchPosts declared as 'async function'    — 0.33 pts
  Component 3: fetchComments declared as 'async function' — 0.33 pts
  Precondition gate: parseData and formatOutput remain plain 'function' (no async)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_082'

FILE_PATH = f'{WORKDIR}/Desktop/fetcher.js'

# These three functions contain 'await' in their bodies and MUST be async after task
ASYNC_REQUIRED = ['fetchUser', 'fetchPosts', 'fetchComments']

# These two functions do NOT use 'await' and MUST remain plain functions
NO_ASYNC_REQUIRED = ['parseData', 'formatOutput']


def verify_task(file_path):
    """
    Verify that the three await-using functions have been made async,
    while the two non-await functions remain unchanged.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: File must be readable
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -------------------------------------------------------------------------
    # Integrity Gate: parseData and formatOutput must remain plain 'function'
    # If these are incorrectly made async, cap the score at 0.0 (task corrupted)
    # -------------------------------------------------------------------------
    integrity_failures = []
    for func_name in NO_ASYNC_REQUIRED:
        # Match a declaration like 'async function parseData' which would be wrong
        wrong_pattern = re.search(
            r'async\s+function\s+' + re.escape(func_name) + r'\s*\(',
            content
        )
        if wrong_pattern:
            print(f"INTEGRITY FAIL: {func_name} was incorrectly made async — "
                  f"it does not use 'await' and must remain a plain function.")
            integrity_failures.append(func_name)
        else:
            # Verify it still exists as a plain function (just a sanity check)
            correct_pattern = re.search(
                r'(?<!async\s)function\s+' + re.escape(func_name) + r'\s*\(',
                content
            )
            if correct_pattern:
                print(f"INTEGRITY OK: {func_name} correctly remains a plain function.")
            else:
                print(f"INTEGRITY WARN: {func_name} declaration not found in file.")

    if len(integrity_failures) > 0:
        print("Integrity gate FAILED: non-await functions were incorrectly made async.")
        print("REWARD: 0.0")
        return 0.0

    # -------------------------------------------------------------------------
    # Component 1: fetchUser is declared as 'async function fetchUser' (0.34 pts)
    # This check FAILS on initial_env (plain function) and PASSES on golden_env (async function)
    # -------------------------------------------------------------------------
    try:
        match = re.search(
            r'async\s+function\s+fetchUser\s*\(',
            content
        )
        if match:
            print(f"PASS: Component 1 — fetchUser declared as 'async function' (0.34 pts)")
            total_score += 0.34
        else:
            # Check if it exists at all as a plain function
            plain = re.search(r'function\s+fetchUser\s*\(', content)
            if plain:
                print(f"FAIL: Component 1 — fetchUser exists but is NOT async; "
                      f"expected 'async function fetchUser('")
            else:
                print(f"FAIL: Component 1 — fetchUser declaration not found in file")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: fetchPosts is declared as 'async function fetchPosts' (0.33 pts)
    # This check FAILS on initial_env (plain function) and PASSES on golden_env (async function)
    # -------------------------------------------------------------------------
    try:
        match = re.search(
            r'async\s+function\s+fetchPosts\s*\(',
            content
        )
        if match:
            print(f"PASS: Component 2 — fetchPosts declared as 'async function' (0.33 pts)")
            total_score += 0.33
        else:
            plain = re.search(r'function\s+fetchPosts\s*\(', content)
            if plain:
                print(f"FAIL: Component 2 — fetchPosts exists but is NOT async; "
                      f"expected 'async function fetchPosts('")
            else:
                print(f"FAIL: Component 2 — fetchPosts declaration not found in file")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: fetchComments is declared as 'async function fetchComments' (0.33 pts)
    # This check FAILS on initial_env (plain function) and PASSES on golden_env (async function)
    # -------------------------------------------------------------------------
    try:
        match = re.search(
            r'async\s+function\s+fetchComments\s*\(',
            content
        )
        if match:
            print(f"PASS: Component 3 — fetchComments declared as 'async function' (0.33 pts)")
            total_score += 0.33
        else:
            plain = re.search(r'function\s+fetchComments\s*\(', content)
            if plain:
                print(f"FAIL: Component 3 — fetchComments exists but is NOT async; "
                      f"expected 'async function fetchComments('")
            else:
                print(f"FAIL: Component 3 — fetchComments declaration not found in file")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------------
    # Final score
    # -------------------------------------------------------------------------
    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: test against canonical artifact path on the VM
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
