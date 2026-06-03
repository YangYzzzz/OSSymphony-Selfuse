"""
Reward Script: Indent lines 10-20 by one level in logic.py
Task ID: vscode_stu_045
Domain: vscode
Scoring:
  Precondition gate: Lines outside 10-20 unchanged (fail => 0.0)
  Component 1 (0.5): All 11 content lines (10-20) have >0 leading spaces (were 0)
  Component 2 (0.3): Indentation is exactly 4 spaces on each content line 10-20
  Component 3 (0.2): Lines 10-20 are indented AND content (stripped) is preserved
"""

import os

WORKDIR = '/home/user'
FILE_NAME = 'logic.py'

# Expected leading spaces in golden: 4 (one indent level added from 0)
EXPECTED_INDENT = 4

# Reference lines outside 10-20 that must be unchanged (precondition gate)
REFERENCE_LINES_OUTSIDE = {
    1: '"""',
    6: 'import datetime',
    7: 'from decimal import Decimal, ROUND_HALF_UP',
    8: 'from typing import List, Dict, Optional',
    23: 'def validate_order(order: Dict) -> bool:',
    45: 'def calculate_subtotal(items: List[Dict], price_catalog: Dict) -> Decimal:',
    58: 'def apply_discount(subtotal: Decimal) -> Decimal:',
}

# Original stripped content of lines 10-20
ORIGINAL_STRIPPED_CONTENT = {
    10: 'TAX_RATE = Decimal("0.085")',
    11: 'DISCOUNT_THRESHOLDS = {500: Decimal("0.05"), 1000: Decimal("0.10"), 5000: Decimal("0.15")}',
    12: 'FREE_SHIPPING_MIN = Decimal("150.00")',
    13: 'EXPEDITED_FEE = Decimal("25.00")',
    14: 'HANDLING_FEE = Decimal("3.50")',
    15: 'WAREHOUSE_ZONES = ["A", "B", "C", "D"]',
    16: 'MAX_ITEMS_PER_ORDER = 200',
    17: 'BACKORDER_LIMIT = 50',
    18: 'CURRENCY_PRECISION = Decimal("0.01")',
    19: 'LOW_STOCK_ALERT = 10',
    20: 'REORDER_POINT = 25',
}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(lines) < 20:
        print(f"FAIL: File has only {len(lines)} lines, expected at least 20")
        print("REWARD: 0.0")
        return 0.0

    # PRECONDITION GATE: Lines outside 10-20 must be unchanged
    try:
        for line_num, expected_stripped in REFERENCE_LINES_OUTSIDE.items():
            idx = line_num - 1
            if idx >= len(lines):
                print(f"GATE FAIL: Line {line_num} missing")
                print("REWARD: 0.0")
                return 0.0
            actual_stripped = lines[idx].strip()
            if actual_stripped != expected_stripped:
                print(f"GATE FAIL: Line {line_num} changed")
                print("REWARD: 0.0")
                return 0.0
        print("GATE PASS: Lines outside 10-20 are unchanged")
    except Exception as e:
        print(f"GATE ERROR: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All content lines 10-20 have added indentation (0.5 points)
    # Originally all had 0 leading spaces; now they must have > 0.
    try:
        indented_count = 0
        content_line_count = 0
        for line_num in range(10, 21):
            idx = line_num - 1
            line = lines[idx]
            if line.strip() == '':
                continue
            content_line_count += 1
            leading = len(line) - len(line.lstrip())
            if leading > 0:
                indented_count += 1
            else:
                print(f"  Line {line_num}: NOT indented (leading=0)")

        if content_line_count > 0 and indented_count == content_line_count:
            print(f"PASS: Component 1 -- All {content_line_count} content lines indented (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 -- {indented_count}/{content_line_count} lines indented")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Indentation is exactly 4 spaces on each content line 10-20 (0.3 points)
    try:
        exact_count = 0
        content_lines = 0
        for line_num in range(10, 21):
            idx = line_num - 1
            line = lines[idx]
            if line.strip() == '':
                continue
            content_lines += 1
            leading = len(line) - len(line.lstrip())
            if leading == EXPECTED_INDENT:
                exact_count += 1
            else:
                print(f"  Line {line_num}: leading={leading}, expected={EXPECTED_INDENT}")

        if content_lines > 0 and exact_count == content_lines:
            print(f"PASS: Component 2 -- All {content_lines} lines have exactly 4-space indent (0.3 pts)")
            total_score += 0.3
        elif content_lines > 0 and exact_count > 0:
            partial = round(0.3 * (exact_count / content_lines), 2)
            if partial > 0:
                total_score += partial
            print(f"PARTIAL: Component 2 -- {exact_count}/{content_lines} correct ({partial} pts)")
        else:
            print(f"FAIL: Component 2 -- 0/{content_lines} lines correct")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Lines are indented AND content preserved (0.2 points)
    # Compound check: line must be indented (leading > 0) AND stripped content matches original.
    # This fails on initial (not indented) and passes on golden (indented + content intact).
    try:
        ok_count = 0
        total_checks = 0
        for line_num, expected_content in ORIGINAL_STRIPPED_CONTENT.items():
            idx = line_num - 1
            line = lines[idx]
            if line.strip() == '':
                continue
            total_checks += 1
            leading = len(line) - len(line.lstrip())
            actual_content = line.strip()
            if leading > 0 and actual_content == expected_content:
                ok_count += 1
            else:
                if leading == 0:
                    print(f"  Line {line_num}: not indented")
                elif actual_content != expected_content:
                    print(f"  Line {line_num}: content changed")

        if total_checks > 0 and ok_count == total_checks:
            print(f"PASS: Component 3 -- All {total_checks} lines indented with content preserved (0.2 pts)")
            total_score += 0.2
        elif total_checks > 0 and ok_count > 0:
            partial = round(0.2 * (ok_count / total_checks), 2)
            if partial > 0:
                total_score += partial
            print(f"PARTIAL: Component 3 -- {ok_count}/{total_checks} lines ok ({partial} pts)")
        else:
            print(f"FAIL: Component 3 -- 0/{total_checks} lines ok")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{FILE_NAME}'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
