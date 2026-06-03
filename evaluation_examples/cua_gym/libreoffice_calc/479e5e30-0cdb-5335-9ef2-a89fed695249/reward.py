"""
Reward Script: Create a dependent dropdown system for Region/Subregion columns
Task ID: osworld_calc_data_validation_dropdown_007
Domain: libreoffice_calc
Scoring:
  Component 1 (0.30): Named ranges 'North', 'South', 'East', 'West' exist in the workbook
  Component 2 (0.35): Column B (B2:B16) has a list data validation with North/South/East/West options
  Component 3 (0.35): Column C (C2:C16) has an INDIRECT-based list data validation referencing column B
  Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'osworld_calc_data_validation_dropdown_007'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The task requires:
    1. Named ranges 'North', 'South', 'East', 'West' defined in the workbook
       pointing to subregion lists in the RegionData sheet.
    2. Column B has a dropdown data validation listing the four regions.
    3. Column C has an INDIRECT-based data validation that depends on B,
       creating a dependent dropdown system.
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: TerritoryAssignment sheet must exist
    if 'TerritoryAssignment' not in wb.sheetnames:
        print("CRITICAL: Sheet 'TerritoryAssignment' not found in workbook.")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['TerritoryAssignment']

    # Component 1: Named ranges 'North', 'South', 'East', 'West' must exist (0.30 points)
    # These named ranges are required to support the INDIRECT-based dependent dropdown.
    # In initial_env, no named ranges exist.
    try:
        defined_names = wb.defined_names
        required_names = {'North', 'South', 'East', 'West'}
        found_names = set()

        for name in required_names:
            if name in defined_names:
                found_names.add(name)

        if found_names == required_names:
            print(f"PASS: Component 1 — All 4 named ranges found: {sorted(found_names)} (0.30 pts)")
            total_score += 0.30
        elif len(found_names) > 0:
            # Partial: some named ranges present
            fraction = len(found_names) / len(required_names)
            partial = round(0.30 * fraction, 2)
            print(f"PARTIAL: Component 1 — Found {len(found_names)}/4 named ranges: {sorted(found_names)} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No named ranges found (expected North, South, East, West)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Column B (B2:B16) has a list data validation with regions (0.35 points)
    # The dropdown in column B must offer North, South, East, West as options.
    # In initial_env, there are no data validations.
    try:
        dvs = ws.data_validations.dataValidation
        region_dv_found = False

        for dv in dvs:
            if dv.type != 'list':
                continue

            # Check that the validation covers column B (at least partially)
            sqref_str = str(dv.sqref)
            covers_b = False
            for ref_part in sqref_str.split():
                if 'B' in ref_part.upper() and not ref_part.upper().startswith('A'):
                    covers_b = True
                    break

            if not covers_b:
                continue

            # Check that formula1 contains the four regions
            formula = (dv.formula1 or '').strip('"').upper()
            regions_in_formula = all(r.upper() in formula for r in ['NORTH', 'SOUTH', 'EAST', 'WEST'])

            if regions_in_formula:
                region_dv_found = True
                print(f"PASS: Component 2 — Column B has list DV with regions (formula1={dv.formula1}, sqref={dv.sqref}) (0.35 pts)")
                total_score += 0.35
                break

        if not region_dv_found:
            # Check if there's any DV on column B even without exact content
            any_b_dv = any(
                dv.type == 'list' and 'B' in str(dv.sqref).upper()
                for dv in dvs
            )
            if any_b_dv:
                print(f"FAIL: Component 2 — Column B has a list DV but it does not contain North/South/East/West")
            else:
                print(f"FAIL: Component 2 — No list data validation found on column B")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Column C (C2:C16) has an INDIRECT-based data validation referencing column B (0.35 points)
    # The dependent dropdown uses INDIRECT(Bx) so selecting a region in B filters subregions in C.
    # In initial_env, there are no data validations.
    try:
        dvs = ws.data_validations.dataValidation
        indirect_dv_found = False

        for dv in dvs:
            if dv.type != 'list':
                continue

            # Check that the validation covers column C
            sqref_str = str(dv.sqref)
            covers_c = False
            for ref_part in sqref_str.split():
                if ref_part.upper().startswith('C'):
                    covers_c = True
                    break

            if not covers_c:
                continue

            # Check that formula1 uses INDIRECT referencing column B
            formula = (dv.formula1 or '').upper().replace(' ', '')
            uses_indirect = 'INDIRECT' in formula
            references_b = 'B' in formula

            if uses_indirect and references_b:
                indirect_dv_found = True
                print(f"PASS: Component 3 — Column C has INDIRECT-based DV (formula1={dv.formula1}, sqref={dv.sqref}) (0.35 pts)")
                total_score += 0.35
                break

        if not indirect_dv_found:
            # Check if there is ANY DV on column C
            any_c_dv = any(
                dv.type == 'list' and str(dv.sqref).upper().startswith('C')
                for dv in dvs
            )
            if any_c_dv:
                print(f"FAIL: Component 3 — Column C has a list DV but it does not use INDIRECT referencing column B")
            else:
                print(f"FAIL: Component 3 — No list data validation found on column C")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {round(total_score, 2)}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
