"""
Reward Script: Verify JSDoc comment block for calculateDiscount function
Task ID: vscode_gf3_018
Domain: vscode
Scoring:
  Component 1: JSDoc block exists above calculateDiscount (0.2 pts)
  Component 2: @param for price with {number} type (0.2 pts)
  Component 3: @param for percentage with {number} type (0.2 pts)
  Component 4: @param for maxDiscount with {number} type (0.2 pts)
  Component 5: @returns tag with {number} type (0.2 pts)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_018'

FILE_PATH = os.path.join(WORKDIR, 'projects', 'lib', 'utils.js')


def verify_task(file_path):
    """
    Verify that a JSDoc comment block documenting all three parameters
    and the return value has been added above calculateDiscount.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be readable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract the JSDoc comment block immediately preceding calculateDiscount.
    # We look for a /** ... */ block followed (possibly with whitespace) by
    # "function calculateDiscount".
    pattern = r'(/\*\*[\s\S]*?\*/)\s*\nfunction calculateDiscount'
    match = re.search(pattern, content)

    # Component 1: JSDoc comment block exists above calculateDiscount (0.2 points)
    try:
        if match:
            jsdoc_block = match.group(1)
            print(f"PASS: Component 1 — JSDoc block found above calculateDiscount (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — No JSDoc block found above calculateDiscount")
            # Without a JSDoc block, no further checks are possible
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: @param for price with {number} type (0.2 points)
    try:
        # Match @param {number} price with any description
        price_pattern = r'@param\s+\{number\}\s+(?:\[)?price(?:\])?\s'
        if re.search(price_pattern, jsdoc_block):
            print(f"PASS: Component 2 — @param {{number}} price found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — @param {{number}} price not found in JSDoc block")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: @param for percentage with {number} type (0.2 points)
    try:
        percentage_pattern = r'@param\s+\{number\}\s+(?:\[)?percentage(?:\])?\s'
        if re.search(percentage_pattern, jsdoc_block):
            print(f"PASS: Component 3 — @param {{number}} percentage found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — @param {{number}} percentage not found in JSDoc block")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: @param for maxDiscount with {number} type (0.2 points)
    try:
        maxdiscount_pattern = r'@param\s+\{number\}\s+(?:\[)?maxDiscount(?:\])?\s'
        if re.search(maxdiscount_pattern, jsdoc_block):
            print(f"PASS: Component 4 — @param {{number}} maxDiscount found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — @param {{number}} maxDiscount not found in JSDoc block")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: @returns tag with {number} type (0.2 points)
    try:
        # Accept both @returns and @return
        returns_pattern = r'@returns?\s+\{number\}'
        if re.search(returns_pattern, jsdoc_block):
            print(f"PASS: Component 5 — @returns {{number}} found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 — @returns {{number}} not found in JSDoc block")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

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
