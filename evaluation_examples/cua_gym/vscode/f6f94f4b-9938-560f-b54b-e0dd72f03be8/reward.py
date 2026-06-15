"""
Reward Script: Modernize JS file by replacing var with const/let
Task ID: vscode_edit_062
Domain: vs_code

Task: Use multi-cursor editing with Ctrl+D to incrementally select and replace
each occurrence of 'var' with 'const' in '~/Desktop/modernize.js', reviewing
each one before confirming.

Context: 8 'var' declarations. 6 become 'const', 2 become 'let' (lines 15 and 28
where variable is reassigned). After task: lines 15 and 28 use 'let', other 6 use
'const', and ALL instances of 'var' are gone.

Scoring:
  Component 1: No 'var' declarations remain in file (0.30 pts)
  Component 2: Lines 15 and 28 use 'let' (variables that are reassigned) (0.35 pts)
  Component 3: The 6 const declarations are correct (0.35 pts)
  Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_062'

FILE_PATH = os.path.join(WORKDIR, 'Desktop', 'modernize.js')

def verify_task(file_path):
    """
    Verify that modernize.js has been properly updated:
    - No 'var' declarations remain
    - Line 15 uses 'let' (total variable, which is reassigned)
    - Line 28 uses 'let' (shippingCost variable, which is reassigned)
    - The other 6 declarations use 'const'
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the file — gate: if file doesn't exist or can't be read, return 0.0
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        lines = content.split('\n')
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"File loaded: {len(lines)} lines")

    # Component 1: No 'var' declarations remain (0.30 points)
    # This checks the core requirement: all 'var' must be gone
    try:
        # Match 'var' used as a declaration keyword (word boundary)
        var_pattern = re.compile(r'\bvar\b')
        var_lines = [(i + 1, line) for i, line in enumerate(lines) if var_pattern.search(line)]
        if len(var_lines) == 0:
            print(f"PASS: Component 1 — No 'var' declarations found in file (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Found {len(var_lines)} 'var' declaration(s) remaining:")
            for lineno, linetext in var_lines:
                print(f"  Line {lineno}: {linetext.strip()}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Lines 15 and 28 use 'let' (0.35 points)
    # These are the two variables that are reassigned later ('total' and 'shippingCost')
    # Both must use 'let', not 'const'
    try:
        # Line numbers are 1-indexed; list is 0-indexed
        line_15 = lines[14] if len(lines) >= 15 else ''  # index 14 = line 15
        line_28 = lines[27] if len(lines) >= 28 else ''  # index 27 = line 28

        line15_uses_let = bool(re.search(r'\blet\b', line_15))
        line28_uses_let = bool(re.search(r'\blet\b', line_28))

        # Also verify line 15 contains 'total' and line 28 contains 'shippingCost'
        line15_has_total = 'total' in line_15
        line28_has_shipping = 'shippingCost' in line_28

        if line15_uses_let and line28_uses_let and line15_has_total and line28_has_shipping:
            print(f"PASS: Component 2 — Lines 15 and 28 both use 'let' (0.35 pts)")
            print(f"  Line 15: {line_15.strip()}")
            print(f"  Line 28: {line_28.strip()}")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — Lines 15 and/or 28 do not correctly use 'let'")
            print(f"  Line 15 uses let: {line15_uses_let}, has 'total': {line15_has_total} — '{line_15.strip()}'")
            print(f"  Line 28 uses let: {line28_uses_let}, has 'shippingCost': {line28_has_shipping} — '{line_28.strip()}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Exactly 6 'const' declarations exist for the 6 non-reassigned variables (0.35 points)
    # The 6 const variables should be: TAX_RATE, FREE_SHIPPING_THRESHOLD, MAX_ITEMS_PER_ORDER,
    # formatter, DISCOUNT_RATES, BASE_RATE
    try:
        expected_const_vars = [
            'TAX_RATE',
            'FREE_SHIPPING_THRESHOLD',
            'MAX_ITEMS_PER_ORDER',
            'formatter',
            'DISCOUNT_RATES',
            'BASE_RATE',
        ]

        # Find all 'const <varname>' declarations in the file
        const_pattern = re.compile(r'\bconst\s+(\w+)\b')
        found_const_vars = []
        for line in lines:
            matches = const_pattern.findall(line)
            found_const_vars.extend(matches)

        # Check that all 6 expected vars are declared as const
        missing_const = [v for v in expected_const_vars if v not in found_const_vars]
        unexpected_const = [v for v in found_const_vars if v not in expected_const_vars]

        if len(missing_const) == 0 and len(found_const_vars) == 6:
            print(f"PASS: Component 3 — All 6 expected 'const' declarations found (0.35 pts)")
            print(f"  const vars: {', '.join(found_const_vars)}")
            total_score += 0.35
        else:
            print(f"FAIL: Component 3 — Expected 6 const declarations, found {len(found_const_vars)}")
            if missing_const:
                print(f"  Missing const: {missing_const}")
            if unexpected_const:
                print(f"  Unexpected const (not in expected list): {unexpected_const}")
            print(f"  All found const vars: {found_const_vars}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
