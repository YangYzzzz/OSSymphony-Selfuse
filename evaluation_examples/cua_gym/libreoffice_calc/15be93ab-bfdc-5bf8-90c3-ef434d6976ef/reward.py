"""
Reward Script: Create named ranges for multi-sheet consolidation
Task ID: calc_nrv_039
Domain: libreoffice_calc
Scoring:
  Component 1: North_Sales named range on North!B2:B13 (0.15)
  Component 2: South_Sales named range on South!B2:B13 (0.15)
  Component 3: East_Sales named range on East!B2:B13 (0.15)
  Component 4: West_Sales named range on West!B2:B13 (0.15)
  Component 5: Consolidated B2 formula referencing all four named ranges (0.40)
"""

import os
import re
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_nrv_039'


def normalize_range_ref(attr_text):
    """
    Normalize a defined name attr_text for comparison.
    Strips dollar signs, lowercases, removes quotes around sheet names.
    Returns (sheet_name_lower, cell_range_lower) or None.
    Example: "North!$B$2:$B$13" -> ("north", "b2:b13")
    """
    if not attr_text:
        return None
    text = attr_text.replace('$', '')
    # Handle optional quotes around sheet name: 'North'!B2:B13
    text = text.replace("'", "")
    if '!' not in text:
        return None
    sheet_part, range_part = text.split('!', 1)
    return (sheet_part.strip().lower(), range_part.strip().lower())


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Build a map of defined names: name_lower -> (sheet_lower, range_lower)
    defined_names = {}
    try:
        for dn in wb.defined_names.values():
            parsed = normalize_range_ref(dn.attr_text)
            if parsed:
                defined_names[dn.name.lower()] = parsed
        print(f"INFO: Found defined names: {list(defined_names.keys())}")
    except Exception as e:
        print(f"ERROR: Could not read defined names: {e}")

    # Expected named ranges
    expected_ranges = {
        'north_sales': ('north', 'b2:b13'),
        'south_sales': ('south', 'b2:b13'),
        'east_sales': ('east', 'b2:b13'),
        'west_sales': ('west', 'b2:b13'),
    }

    # Component 1: North_Sales named range (0.15 points)
    try:
        if 'north_sales' in defined_names:
            actual = defined_names['north_sales']
            expected = expected_ranges['north_sales']
            if actual == expected:
                print(f"PASS: Component 1 -- North_Sales = North!B2:B13 (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 -- North_Sales has wrong ref: {actual}, expected {expected}")
        else:
            print(f"FAIL: Component 1 -- North_Sales named range not found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: South_Sales named range (0.15 points)
    try:
        if 'south_sales' in defined_names:
            actual = defined_names['south_sales']
            expected = expected_ranges['south_sales']
            if actual == expected:
                print(f"PASS: Component 2 -- South_Sales = South!B2:B13 (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 -- South_Sales has wrong ref: {actual}, expected {expected}")
        else:
            print(f"FAIL: Component 2 -- South_Sales named range not found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: East_Sales named range (0.15 points)
    try:
        if 'east_sales' in defined_names:
            actual = defined_names['east_sales']
            expected = expected_ranges['east_sales']
            if actual == expected:
                print(f"PASS: Component 3 -- East_Sales = East!B2:B13 (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 -- East_Sales has wrong ref: {actual}, expected {expected}")
        else:
            print(f"FAIL: Component 3 -- East_Sales named range not found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: West_Sales named range (0.15 points)
    try:
        if 'west_sales' in defined_names:
            actual = defined_names['west_sales']
            expected = expected_ranges['west_sales']
            if actual == expected:
                print(f"PASS: Component 4 -- West_Sales = West!B2:B13 (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 -- West_Sales has wrong ref: {actual}, expected {expected}")
        else:
            print(f"FAIL: Component 4 -- West_Sales named range not found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Consolidated B2 formula referencing all four named ranges (0.40 points)
    try:
        if 'Consolidated' not in wb.sheetnames:
            print(f"FAIL: Component 5 -- 'Consolidated' sheet not found")
        else:
            ws_con = wb['Consolidated']
            b2_val = ws_con['B2'].value
            if b2_val is None:
                print(f"FAIL: Component 5 -- Consolidated B2 is empty")
            elif not isinstance(b2_val, str) or not b2_val.startswith('='):
                print(f"FAIL: Component 5 -- Consolidated B2 is not a formula: {b2_val}")
            else:
                # Check the formula references all four named ranges
                formula_upper = b2_val.upper().replace(' ', '')
                required_refs = ['NORTH_SALES', 'SOUTH_SALES', 'EAST_SALES', 'WEST_SALES']
                found_refs = [ref for ref in required_refs if ref in formula_upper]
                missing_refs = [ref for ref in required_refs if ref not in formula_upper]

                if len(found_refs) == 4:
                    # Also verify it uses SUM or similar aggregation
                    if 'SUM' in formula_upper:
                        print(f"PASS: Component 5 -- Consolidated B2 formula references all 4 named ranges with SUM (0.40 pts)")
                        print(f"  Formula: {b2_val}")
                        total_score += 0.40
                    else:
                        # The formula references all 4 ranges but might use + or other aggregation
                        # Still award partial: references are correct even if aggregation differs
                        print(f"PASS: Component 5 -- Consolidated B2 formula references all 4 named ranges (0.40 pts)")
                        print(f"  Formula: {b2_val}")
                        total_score += 0.40
                else:
                    print(f"FAIL: Component 5 -- Formula missing refs: {missing_refs}")
                    print(f"  Formula: {b2_val}")
                    # Partial credit: 0.10 per found reference
                    partial = len(found_refs) * 0.10
                    if partial > 0:
                        print(f"  Partial credit for {len(found_refs)}/4 refs: {partial:.2f} pts")
                        total_score += partial
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
