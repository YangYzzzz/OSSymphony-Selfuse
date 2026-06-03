"""
Reward Script: Create a Gantt-like schedule with conditional formatting on ProjectPlan
Task ID: calc_ops_project_tracking_gantt_011
Domain: libreoffice_calc
Scoring:
  Component 1: Conditional formatting rule exists on E2:AL16 range (0.5 pts)
  Component 2: CF formula is correct AND fill color is blue-ish (0.3 pts)
  Component 3: Column A frozen (freeze_panes set to freeze column A) (0.2 pts)
Total: 1.0
"""

import os
import openpyxl

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_ops_project_tracking_gantt_011'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.

    Changes from initial → golden:
    1. Conditional formatting added to E2:AL16 with formula =AND(E$1>=$B2, E$1<$B2+$C2)
       and solid blue fill. (Initial has NO conditional formatting at all.)
    2. Freeze panes set to B1 (freezes column A so task names stay visible).
       (Initial has freeze_panes=None.)

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Validate sheet exists
    if 'ProjectPlan' not in wb.sheetnames:
        print("CRITICAL: 'ProjectPlan' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['ProjectPlan']

    # ------------------------------------------------------------------
    # Component 1: Conditional formatting rule exists on E2:AL16 (0.5 pts)
    # The initial file has NO conditional formatting. The task requires
    # adding a CF rule to highlight active cells in the Gantt range.
    # ------------------------------------------------------------------
    try:
        cf_rules_found = False
        gantt_range_covered = False

        for cf in ws.conditional_formatting:
            cf_str = str(cf)
            # Check if the CF covers E2:AL16 (or starts at E2)
            if 'E2' in cf_str:
                cf_rules_found = True
                # Check if it spans at least some columns toward AL
                rules_list = list(ws.conditional_formatting[cf])
                if len(rules_list) > 0:
                    gantt_range_covered = True
                    print(f"PASS: Component 1 — Conditional formatting found on range '{cf_str}' (0.5 pts)")
                    total_score += 0.5
                    break

        if not cf_rules_found:
            print("FAIL: Component 1 — No conditional formatting found starting at E2. "
                  "Expected a CF rule on E2:AL16 for Gantt schedule.")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ------------------------------------------------------------------
    # Component 2: CF formula is correct (AND logic) AND fill color is
    # a solid blue-ish color (0.3 pts)
    # The formula must reference row-locked date header ($1) and
    # column-locked task data ($B, $C), enabling the Gantt pattern.
    # ------------------------------------------------------------------
    try:
        formula_correct = False
        fill_blue = False

        for cf in ws.conditional_formatting:
            cf_str = str(cf)
            if 'E2' in cf_str:
                for rule in ws.conditional_formatting[cf]:
                    # Check formula contains AND with the correct references
                    if rule.formula:
                        formula_str = rule.formula[0].upper().replace(' ', '')
                        # The formula should be AND(E$1>=$B2, E$1<$B2+$C2) or similar
                        has_and = 'AND(' in formula_str
                        has_date_ref = '$1' in formula_str  # row-locked date header
                        has_b_col = '$B' in formula_str      # start date column
                        has_c_col = '$C' in formula_str      # duration column
                        if has_and and has_date_ref and has_b_col and has_c_col:
                            formula_correct = True
                            print(f"  Formula check PASS: '{rule.formula[0]}' contains AND with correct references")

                    # Check fill color — should be solid and blue-ish
                    if hasattr(rule, 'dxf') and rule.dxf and rule.dxf.fill:
                        fill = rule.dxf.fill
                        try:
                            fg_rgb = fill.fgColor.rgb  # 8-char ARGB
                            # Blue-ish: R component < 80, B component > 100
                            # FF4472C4 = alpha:FF R:44 G:72 B:C4
                            if fg_rgb and len(fg_rgb) == 8:
                                r = int(fg_rgb[2:4], 16)
                                g = int(fg_rgb[4:6], 16)
                                b = int(fg_rgb[6:8], 16)
                                # Accept any solid color (task says "e.g., blue")
                                # The key requirement is a solid fill is present
                                if fill.patternType == 'solid':
                                    fill_blue = True
                                    print(f"  Fill check PASS: solid fill with color #{fg_rgb} (R={r} G={g} B={b})")
                        except Exception as fe:
                            print(f"  Fill color read error: {fe}")

        if formula_correct and fill_blue:
            print(f"PASS: Component 2 — CF formula correct AND solid fill color present (0.3 pts)")
            total_score += 0.3
        elif formula_correct:
            print(f"PARTIAL: Component 2 — CF formula is correct but fill is not solid-colored")
        elif fill_blue:
            print(f"PARTIAL: Component 2 — Fill color is solid but formula is incorrect")
        else:
            print(f"FAIL: Component 2 — CF formula incorrect or no solid fill. "
                  f"Expected formula =AND(E$1>=$B2,E$1<$B2+$C2) with solid color fill.")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ------------------------------------------------------------------
    # Component 3: Column A frozen (freeze_panes set so column A is frozen) (0.2 pts)
    # Task context says "Column A should be frozen so task names stay visible".
    # In openpyxl, freezing column A means freeze_panes is set to B1 (or B<N>).
    # Initial file has freeze_panes=None.
    # ------------------------------------------------------------------
    try:
        fp = ws.freeze_panes
        # Freeze panes that freeze column A: must start with 'B' (e.g. B1, B2)
        # The task says freeze column A so task names stay visible when scrolling right
        if fp is not None and str(fp).startswith('B'):
            print(f"PASS: Component 3 — Column A frozen (freeze_panes='{fp}') (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Column A not frozen. "
                  f"Expected freeze_panes to start with 'B' (e.g. 'B1'), found: {repr(fp)}")
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
