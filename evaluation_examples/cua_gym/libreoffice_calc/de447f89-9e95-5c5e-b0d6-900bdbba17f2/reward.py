"""
Reward Script: Highlight duplicate Order IDs in column A with red conditional formatting
Task ID: calc_dop_dedup_highlight_068
Domain: libreoffice_calc

Scoring Rubric:
  Component 1: Conditional formatting applied to range A2:A120         — 0.3 points
  Component 2: CF uses a COUNTIF formula rule for detecting duplicates  — 0.4 points
  Component 3: CF fill color is red (#FF0000)                           — 0.3 points
  Total: 1.0
"""

import os
import re
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_dop_dedup_highlight_068'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.

    The task requires applying conditional formatting on A2:A120 using:
      - A formula-based rule: =COUNTIF($A$2:$A$120,A2)>1
      - A red fill color (hex #FF0000) for cells where the condition is met

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Verify the sheet exists
    if 'OrderLog' not in wb.sheetnames:
        print("FAIL: Sheet 'OrderLog' not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['OrderLog']

    # Component 1: Conditional formatting is applied to the range A2:A120 (0.3 points)
    # This FAILS on the initial file (no CF rules) and PASSES on golden.
    try:
        cf_list = list(ws.conditional_formatting)
        found_range = False
        matching_cf = None

        for cf_range in cf_list:
            # Check if the CF range covers A2:A120
            range_str = str(cf_range).upper().replace(' ', '')
            # The range should be exactly A2:A120 or contain it
            if 'A2:A120' in range_str or range_str == 'A2:A120':
                found_range = True
                matching_cf = cf_range
                break

        if found_range and matching_cf is not None:
            print(f"PASS: Component 1 — Conditional formatting applied on A2:A120 (0.3 pts)")
            total_score += 0.3
        else:
            cf_ranges = [str(c) for c in cf_list]
            print(f"FAIL: Component 1 — No CF on A2:A120. Found ranges: {cf_ranges}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: CF rule uses a COUNTIF formula for detecting duplicates (0.4 points)
    # The expected formula is: COUNTIF($A$2:$A$120,A2)>1
    # This FAILS on the initial file (no CF rules) and PASSES on golden.
    try:
        if matching_cf is None:
            print("FAIL: Component 2 — No matching CF range found to check formula")
        else:
            formula_found = False
            for rule in matching_cf.rules:
                if rule.type == 'expression':
                    formulas = getattr(rule, 'formula', [])
                    for formula_str in formulas:
                        # Normalize: remove spaces and uppercase
                        norm_formula = str(formula_str).upper().replace(' ', '')
                        # Check for COUNTIF pattern targeting A2:A120 with >1 threshold
                        if 'COUNTIF' in norm_formula and '>1' in norm_formula:
                            # Verify the range covers $A$2:$A$120
                            if ('$A$2:$A$120' in norm_formula or 'A2:A120' in norm_formula):
                                formula_found = True
                                print(f"PASS: Component 2 — COUNTIF formula for duplicates found: {formula_str} (0.4 pts)")
                                total_score += 0.4
                                break
                    if formula_found:
                        break

            if not formula_found:
                # Try to show what formulas were found
                found_formulas = []
                for rule in matching_cf.rules:
                    rule_formula = getattr(rule, 'formula', [])
                    found_formulas.extend(rule_formula)
                print(f"FAIL: Component 2 — Expected COUNTIF($A$2:$A$120,A2)>1 formula, found: {found_formulas}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: CF fill color is red (#FF0000) (0.3 points)
    # The task specifies red background; golden should use FFFF0000 (ARGB red).
    # This FAILS on the initial file (no CF rules) and PASSES on golden.
    try:
        if matching_cf is None:
            print("FAIL: Component 3 — No matching CF range found to check fill color")
        else:
            red_fill_found = False
            for rule in matching_cf.rules:
                if hasattr(rule, 'dxf') and rule.dxf is not None:
                    dxf_fill = rule.dxf.fill
                    if dxf_fill is not None:
                        fg_color = dxf_fill.fgColor
                        if fg_color is not None:
                            color_rgb = None
                            try:
                                color_rgb = fg_color.rgb
                            except Exception:
                                pass

                            if color_rgb is not None:
                                # Accept FFFF0000 (8-char ARGB opaque red) or FF0000 (6-char RGB red)
                                color_upper = color_rgb.upper().replace(' ', '')
                                if color_upper in ('FFFF0000', 'FF0000'):
                                    red_fill_found = True
                                    print(f"PASS: Component 3 — Red fill color found: {color_rgb} (0.3 pts)")
                                    total_score += 0.3
                                    break
                                else:
                                    print(f"FAIL: Component 3 — Fill color is {color_rgb}, expected red (FFFF0000 or FF0000)")
                            else:
                                print("FAIL: Component 3 — Could not read fgColor.rgb (possibly theme color)")
                        else:
                            print("FAIL: Component 3 — dxf.fill has no fgColor")
                    else:
                        print("FAIL: Component 3 — dxf has no fill")
                else:
                    print("FAIL: Component 3 — Rule has no dxf (differential formatting)")

            if not red_fill_found and total_score >= 0.7:
                # Only print summary failure if we haven't already printed it above
                pass
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against golden file (path on VM)
file_path = f'{WORKDIR}/{TASK_ID}_initial.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
