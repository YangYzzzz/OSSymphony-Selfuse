"""
Reward Script: Extract Variable refactoring in calculator.py
Task ID: vscode_py_041
Domain: vs_code
Scoring:
  Component 1 (0.4): discount_rate variable assignment exists with correct expression
  Component 2 (0.3): total line uses discount_rate instead of inline expression
  Component 3 (0.3): Code behavior is preserved (outputs match original)
"""

import os
import re
import importlib.util
import sys

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_041'
FILE_PATH = os.path.join(WORKDIR, 'calculator.py')

# Expected output from running the calculator (must match original behavior)
EXPECTED_DISCOUNTED = 210.0
EXPECTED_INVOICE = 240.92


def verify_task():
    """
    Verify that the Extract Variable refactoring was performed correctly.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(FILE_PATH):
        print(f"CRITICAL: File not found: {FILE_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(FILE_PATH, 'r') as f:
            content = f.read()
        lines = content.split('\n')
    except Exception as e:
        print(f"CRITICAL: Cannot read file {FILE_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: discount_rate variable assignment exists (0.4 points)
    # Look for a line like: discount_rate = loyalty_years * 0.02 + membership_level * 0.05
    # The extracted expression should contain both loyalty_years * 0.02 and membership_level * 0.05
    try:
        found_assignment = False
        assignment_line_num = -1
        for i, line in enumerate(lines):
            stripped = line.strip()
            # Match: discount_rate = <expression containing the two terms>
            if re.match(r'^discount_rate\s*=\s*', stripped):
                rhs = stripped.split('=', 1)[1].strip()
                # Check the expression contains both components
                has_loyalty = 'loyalty_years' in rhs and '0.02' in rhs
                has_membership = 'membership_level' in rhs and '0.05' in rhs
                if has_loyalty and has_membership:
                    found_assignment = True
                    assignment_line_num = i
                    break

        if found_assignment:
            print(f"PASS: Component 1 — discount_rate assignment found on line {assignment_line_num + 1} (0.4 pts)")
            total_score += 0.4
        else:
            print("FAIL: Component 1 — No line with 'discount_rate = <expression with loyalty_years*0.02 + membership_level*0.05>' found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: total line uses discount_rate variable (0.3 points)
    # The total line should reference discount_rate and NOT contain the inline expression
    try:
        found_total_with_var = False
        for i, line in enumerate(lines):
            stripped = line.strip()
            if re.match(r'^total\s*=\s*', stripped):
                rhs = stripped.split('=', 1)[1].strip()
                # Must use discount_rate
                uses_var = 'discount_rate' in rhs
                # Must NOT contain the old inline expression parts
                no_inline = 'loyalty_years' not in rhs and 'membership_level' not in rhs
                if uses_var and no_inline:
                    found_total_with_var = True
                    break

        if found_total_with_var:
            print(f"PASS: Component 2 — total line uses discount_rate variable (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 2 — total line does not use discount_rate or still contains inline expression")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Code behavior preserved AND refactoring was done (0.3 points)
    # Only awards points if at least one refactoring component passed (gates on task change)
    # This ensures initial_env scores 0.0 since no refactoring exists there
    refactoring_done = total_score > 0.0
    if not refactoring_done:
        print("FAIL: Component 3 — Skipped: no refactoring detected (prerequisite for behavior check)")
    else:
        try:
            # Import the module dynamically
            spec = importlib.util.spec_from_file_location("calculator", FILE_PATH)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            calc = module.PricingCalculator()

            # Test calculate_discounted_total
            discounted = calc.calculate_discounted_total(250.00, 3, 2)
            # Test generate_invoice_total
            invoice = calc.generate_invoice_total(250.00, 3, 2, 2.5, is_express=True)

            behavior_ok = (discounted == EXPECTED_DISCOUNTED and invoice == EXPECTED_INVOICE)

            if behavior_ok:
                print(f"PASS: Component 3 — Code behavior preserved: discounted={discounted}, invoice={invoice} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Output mismatch: discounted={discounted} (expected {EXPECTED_DISCOUNTED}), invoice={invoice} (expected {EXPECTED_INVOICE})")
        except Exception as e:
            print(f"ERROR: Component 3 — Could not run calculator: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
