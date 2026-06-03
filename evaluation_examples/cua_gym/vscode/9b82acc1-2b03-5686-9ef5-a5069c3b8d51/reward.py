"""
Reward Script: Extract to Function and Extract to Constant refactoring in TypeScript
Task ID: vscode_web_045
Domain: vscode
Scoring:
  Component 1 (0.30): Magic number 0.0875 extracted to a named constant (UPPER_CASE)
  Component 2 (0.30): Extracted function for subtotal calculation exists
  Component 3 (0.25): Original functions call extracted function (no inline duplication)
  Component 4 (0.15): Old variable-style taxRate no longer present; new constant used
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_045'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'webapp', 'src', 'utils', 'pricing.ts')


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

    # Component 1: Magic number 0.0875 extracted to a named constant (0.30 points)
    # In the initial file, it's `const taxRate = 0.0875;` (camelCase, variable-style).
    # After refactoring, it should be a UPPER_CASE or PascalCase constant name.
    # We check: there exists a const declaration with 0.0875 whose name is ALL_UPPERCASE
    # (like TAX_RATE) and NOT the original camelCase `taxRate`.
    try:
        # Find all const declarations containing 0.0875
        const_pattern = re.compile(r'const\s+(\w+)\s*[=:]\s*.*0\.0875')
        const_matches = const_pattern.findall(content)

        # Filter for UPPER_CASE constants (e.g., TAX_RATE) that are not the original taxRate
        uppercase_consts = [n for n in const_matches
                           if n != 'taxRate' and re.match(r'^[A-Z][A-Z0-9_]*$', n)]
        renamed_consts = [n for n in const_matches if n != 'taxRate']

        if uppercase_consts:
            print(f"PASS: Component 1 — Found uppercase constant '{uppercase_consts[0]}' = 0.0875 (0.30 pts)")
            total_score += 0.30
        elif renamed_consts:
            # Accept PascalCase or other renamed constant
            print(f"PASS: Component 1 — Found renamed constant '{renamed_consts[0]}' = 0.0875 (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Magic number 0.0875 not extracted to named constant. Found: {const_matches}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Extracted function for subtotal calculation exists (0.30 points)
    # The golden file has a `function calculateSubtotal(items: CartItem[]): number`
    # We check that there is a new function definition that computes subtotal from items
    # using the calculation pattern (price * quantity, discount, etc.)
    try:
        # Look for a function that: (a) takes items/CartItem param, (b) contains the calculation
        # pattern (price * quantity or discountPercent), (c) returns subtotal
        func_pattern = re.compile(
            r'function\s+(\w+)\s*\([^)]*(?:CartItem|items)[^)]*\)\s*(?::\s*\w+)?\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}',
            re.DOTALL
        )
        func_matches = func_pattern.findall(content)

        # Filter: must not be one of the original exported functions
        original_funcs = {'calculateOrderTotal', 'calculateRefundAmount', 'previewCartSubtotal',
                          'getShippingCost', 'applyLoyaltyDiscount', 'formatCurrency',
                          'generateInvoiceSummary'}
        extracted_candidates = [
            (fn, fb) for fn, fb in func_matches
            if fn not in original_funcs
            and 'price' in fb.lower()
            and 'quantity' in fb.lower()
            and 'discount' in fb.lower()
            and 'subtotal' in fb.lower()
        ]

        if extracted_candidates:
            extracted_func_name = extracted_candidates[0][0]
            print(f"PASS: Component 2 — Found extracted function '{extracted_func_name}' with subtotal calculation (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — No extracted subtotal calculation function found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Original functions call extracted function instead of inline calc (0.25 points)
    # In golden, calculateOrderTotal, calculateRefundAmount, and previewCartSubtotal
    # should no longer have the inline loop. They should call the extracted function.
    try:
        # Check that these 3 functions no longer contain the inline calculation pattern
        # The inline pattern has: `for (const item of items)` with `basePrice` computation
        inline_pattern = re.compile(r'for\s*\(\s*const\s+item\s+of\s+items\s*\)')

        # Find function bodies for the 3 target functions
        target_funcs = ['calculateOrderTotal', 'calculateRefundAmount', 'previewCartSubtotal']
        funcs_using_call = 0

        for target in target_funcs:
            # Extract function body
            func_re = re.compile(
                r'function\s+' + re.escape(target) + r'\s*\([^)]*\)\s*(?::\s*\w+)?\s*\{',
                re.DOTALL
            )
            match = func_re.search(content)
            if match:
                # Find the matching closing brace
                start = match.end()
                brace_count = 1
                pos = start
                while pos < len(content) and brace_count > 0:
                    if content[pos] == '{':
                        brace_count += 1
                    elif content[pos] == '}':
                        brace_count -= 1
                    pos += 1
                func_body = content[start:pos-1]

                # Check: body should NOT contain the inline for-loop pattern
                has_inline = inline_pattern.search(func_body)

                if not has_inline:
                    funcs_using_call += 1
                    print(f"  OK: {target} uses extracted function (no inline loop)")
                else:
                    print(f"  FAIL: {target} still has inline calculation loop")

        if funcs_using_call == 3:
            print(f"PASS: Component 3 — All 3 functions call extracted function (0.25 pts)")
            total_score += 0.25
        elif funcs_using_call >= 1:
            partial = round(0.25 * funcs_using_call / 3, 2)
            print(f"PARTIAL: Component 3 — {funcs_using_call}/3 functions refactored ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No functions refactored to use extracted function")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Old variable-style `taxRate` no longer used; new constant referenced (0.15 points)
    # In initial, `taxRate` is used in lines like `subtotal * taxRate`.
    # After refactoring, all references should use the new constant name.
    try:
        # Check that `taxRate` (camelCase) does NOT appear as an identifier
        # But the new constant (e.g., TAX_RATE) IS used in expressions
        taxrate_usage = re.findall(r'\btaxRate\b', content)
        # Find uppercase constant usage (not in declaration)
        uppercase_const_usage = re.findall(r'\b([A-Z][A-Z0-9_]*)\b', content)
        # Filter for tax-related constants used in multiplication
        tax_const_in_expr = re.findall(r'\*\s*([A-Z][A-Z0-9_]*(?:_RATE|_TAX)?)\b', content)

        if len(taxrate_usage) == 0:
            # Also verify the new constant is actually used in expressions
            new_const_used = any(re.search(r'\*\s*' + re.escape(name), content)
                                for name in re.findall(r'const\s+([A-Z][A-Z0-9_]*)\s*=\s*0\.0875', content))
            if new_const_used:
                print(f"PASS: Component 4 — Old 'taxRate' removed, new constant used in expressions (0.15 pts)")
                total_score += 0.15
            else:
                # Accept if taxRate is just gone and some constant with 0.0875 exists
                has_const = bool(re.search(r'const\s+\w+\s*=\s*0\.0875', content))
                if has_const:
                    print(f"PASS: Component 4 — Old 'taxRate' removed, constant defined (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 4 — taxRate removed but no replacement constant found")
        else:
            print(f"FAIL: Component 4 — Old 'taxRate' still present ({len(taxrate_usage)} occurrences)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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
