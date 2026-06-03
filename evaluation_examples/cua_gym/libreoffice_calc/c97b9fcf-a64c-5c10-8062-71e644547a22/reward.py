"""
Reward Script: Set up named ranges for tax/discount/inflation rates and update formulas
Task ID: calc_gen_namedranges_050
Domain: libreoffice_calc
Scoring:
  - Component 1: Named ranges TaxRate, DiscountRate, InflationRate defined at workbook scope (0.30)
  - Component 2: Income sheet row 10 uses TaxRate named range in formulas (0.15)
  - Component 3: Balance sheet rows 4 & 6 use InflationRate & TaxRate named ranges (0.20)
  - Component 4: Cashflow sheet rows 4, 6, 7 use TaxRate, InflationRate, DiscountRate (0.20)
  - Component 5: Valuation sheet rows 9-14, 16 use DiscountRate, InflationRate, TaxRate (0.15)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gen_namedranges_050'


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

    # Component 1: Named ranges TaxRate, DiscountRate, InflationRate defined at workbook scope (0.30)
    # These do NOT exist in the initial file — only in the golden file.
    try:
        defined_names = wb.defined_names
        required_names = {
            'TaxRate': 'Assumptions!$B$2',
            'DiscountRate': 'Assumptions!$B$3',
            'InflationRate': 'Assumptions!$B$4',
        }
        found_names = {}
        for name_key, expected_ref in required_names.items():
            if name_key in defined_names:
                dn = defined_names[name_key]
                # Check localSheetId is None (workbook scope)
                is_workbook_scope = (dn.localSheetId is None)
                # Check destinations match expected reference
                dests = list(dn.destinations)
                has_correct_dest = any(
                    sheet == 'Assumptions' and '$B$' in cell_ref
                    for sheet, cell_ref in dests
                )
                found_names[name_key] = (is_workbook_scope and has_correct_dest)
            else:
                found_names[name_key] = False

        all_found = all(found_names.values())
        if all_found:
            print(f"PASS: Component 1 — All 3 named ranges defined at workbook scope: TaxRate, DiscountRate, InflationRate (0.30 pts)")
            total_score += 0.30
        else:
            missing = [k for k, v in found_names.items() if not v]
            print(f"FAIL: Component 1 — Missing or incorrect named ranges: {missing}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Income sheet row 10 — all 5 tax cells use TaxRate named range (0.15)
    # Initial has: =B9*0.21, =C9*0.21, etc.
    # Golden has: =B9*TaxRate, =C9*TaxRate, etc.
    try:
        ws_income = wb['Income']
        taxrate_cols = ['B', 'C', 'D', 'E', 'F']
        income_passes = 0
        for col in taxrate_cols:
            cell_val = ws_income[f'{col}10'].value
            if isinstance(cell_val, str) and 'TaxRate' in cell_val:
                income_passes += 1
            else:
                print(f"  FAIL: Income!{col}10 = {repr(cell_val)}, expected formula containing 'TaxRate'")

        if income_passes == 5:
            print(f"PASS: Component 2 — Income sheet B10:F10 all use TaxRate named range (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Only {income_passes}/5 Income row 10 cells use TaxRate")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Balance sheet — rows 4 (InflationRate) and row 6 (TaxRate), 5 cols each (0.20)
    # Initial B4: =B3*(1+0.025), B6: =B5*0.21
    # Golden B4: =B3*(1+InflationRate), B6: =B5*TaxRate
    try:
        ws_balance = wb['Balance']
        balance_passes = 0
        total_balance_checks = 10

        # Row 4: should use InflationRate
        for col in ['B', 'C', 'D', 'E', 'F']:
            cell_val = ws_balance[f'{col}4'].value
            if isinstance(cell_val, str) and 'InflationRate' in cell_val:
                balance_passes += 1
            else:
                print(f"  FAIL: Balance!{col}4 = {repr(cell_val)}, expected formula containing 'InflationRate'")

        # Row 6: should use TaxRate
        for col in ['B', 'C', 'D', 'E', 'F']:
            cell_val = ws_balance[f'{col}6'].value
            if isinstance(cell_val, str) and 'TaxRate' in cell_val:
                balance_passes += 1
            else:
                print(f"  FAIL: Balance!{col}6 = {repr(cell_val)}, expected formula containing 'TaxRate'")

        if balance_passes == total_balance_checks:
            print(f"PASS: Component 3 — Balance sheet rows 4 & 6 use InflationRate & TaxRate (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Only {balance_passes}/{total_balance_checks} Balance cells use named ranges")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Cashflow sheet — row 4 (TaxRate), row 6 (InflationRate), row 7 (DiscountRate), 5 cols each (0.20)
    # Initial B4: =B3*0.21, B6: =B5*0.025, B7: =1/(1+0.10)^1
    # Golden B4: =B3*TaxRate, B6: =B5*InflationRate, B7: =1/(1+DiscountRate)^1
    try:
        ws_cf = wb['Cashflow']
        cf_passes = 0
        total_cf_checks = 15

        # Row 4: TaxRate
        for col in ['B', 'C', 'D', 'E', 'F']:
            cell_val = ws_cf[f'{col}4'].value
            if isinstance(cell_val, str) and 'TaxRate' in cell_val:
                cf_passes += 1
            else:
                print(f"  FAIL: Cashflow!{col}4 = {repr(cell_val)}, expected formula containing 'TaxRate'")

        # Row 6: InflationRate
        for col in ['B', 'C', 'D', 'E', 'F']:
            cell_val = ws_cf[f'{col}6'].value
            if isinstance(cell_val, str) and 'InflationRate' in cell_val:
                cf_passes += 1
            else:
                print(f"  FAIL: Cashflow!{col}6 = {repr(cell_val)}, expected formula containing 'InflationRate'")

        # Row 7: DiscountRate
        for col in ['B', 'C', 'D', 'E', 'F']:
            cell_val = ws_cf[f'{col}7'].value
            if isinstance(cell_val, str) and 'DiscountRate' in cell_val:
                cf_passes += 1
            else:
                print(f"  FAIL: Cashflow!{col}7 = {repr(cell_val)}, expected formula containing 'DiscountRate'")

        if cf_passes == total_cf_checks:
            print(f"PASS: Component 4 — Cashflow sheet rows 4, 6, 7 all use named ranges (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Only {cf_passes}/{total_cf_checks} Cashflow cells use named ranges")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Valuation sheet — DiscountRate in C9:C14, InflationRate in B14, TaxRate in B16 (0.15)
    # Initial: 0.10 hardcoded in C9-C14, 0.025 in B14, 0.10 in B14, 0.21 in B16
    # Golden: DiscountRate in C9-C14, InflationRate+DiscountRate in B14, TaxRate in B16
    try:
        ws_val = wb['Valuation']
        val_passes = 0
        total_val_checks = 8  # C9-C13 (5) + C14 (1) + B14 (1) + B16 (1)

        # C9:C13: DiscountRate
        for row in range(9, 14):
            cell_val = ws_val[f'C{row}'].value
            if isinstance(cell_val, str) and 'DiscountRate' in cell_val:
                val_passes += 1
            else:
                print(f"  FAIL: Valuation!C{row} = {repr(cell_val)}, expected formula containing 'DiscountRate'")

        # C14: DiscountRate
        cell_c14 = ws_val['C14'].value
        if isinstance(cell_c14, str) and 'DiscountRate' in cell_c14:
            val_passes += 1
        else:
            print(f"  FAIL: Valuation!C14 = {repr(cell_c14)}, expected formula containing 'DiscountRate'")

        # B14: InflationRate AND DiscountRate
        cell_b14 = ws_val['B14'].value
        if isinstance(cell_b14, str) and 'InflationRate' in cell_b14 and 'DiscountRate' in cell_b14:
            val_passes += 1
        else:
            print(f"  FAIL: Valuation!B14 = {repr(cell_b14)}, expected formula containing 'InflationRate' and 'DiscountRate'")

        # B16: TaxRate
        cell_b16 = ws_val['B16'].value
        if isinstance(cell_b16, str) and 'TaxRate' in cell_b16:
            val_passes += 1
        else:
            print(f"  FAIL: Valuation!B16 = {repr(cell_b16)}, expected formula containing 'TaxRate'")

        if val_passes == total_val_checks:
            print(f"PASS: Component 5 — Valuation sheet uses DiscountRate, InflationRate, TaxRate (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — Only {val_passes}/{total_val_checks} Valuation cells use named ranges")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

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
