"""
Reward Script: Protect 'Test Cases' sheet with password, only allow sorting
Task ID: calc_ps_042
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): Sheet protection is enabled
  Component 2 (0.2): Password is set
  Component 3 (0.2): Sorting is allowed (sort=False in openpyxl)
  Component 4 (0.3): All other operations are blocked
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_ps_042'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    In openpyxl SheetProtection, attribute=True means the action is BLOCKED,
    attribute=False means the action is ALLOWED.
    - sort=False → sorting allowed
    - autoFilter=True → filtering blocked
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'Test Cases' sheet must exist
    if 'Test Cases' not in wb.sheetnames:
        print("FAIL: 'Test Cases' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Test Cases']
    prot = ws.protection

    # Component 1: Sheet protection is enabled (0.3 points)
    # Initial: sheet=False, Golden: sheet=True
    try:
        if prot.sheet is True:
            print(f"PASS: Component 1 — Sheet protection is enabled (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Sheet protection not enabled (sheet={prot.sheet})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Password is set (0.2 points)
    # Initial: password=None, Golden: password is a non-empty hash
    try:
        if prot.password is not None and str(prot.password).strip() != '':
            print(f"PASS: Component 2 — Password is set (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — No password set (password={prot.password})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Sorting is allowed (0.2 points)
    # In openpyxl, sort=False means sorting IS allowed
    # Initial: sort=True (blocked), Golden: sort=False (allowed)
    try:
        if prot.sort is False:
            print(f"PASS: Component 3 — Sorting is allowed (sort=False) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Sorting not allowed (sort={prot.sort})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All other operations are blocked (0.3 points)
    # These should all be True (blocked) in the golden state
    # Initial: these are also True, BUT since sheet=False initially, protection
    # isn't active. We only award points here if sheet IS protected (Component 1),
    # ensuring this component only scores when combined with actual protection.
    try:
        blocked_attrs = {
            'autoFilter': prot.autoFilter,
            'insertRows': prot.insertRows,
            'insertColumns': prot.insertColumns,
            'deleteRows': prot.deleteRows,
            'deleteColumns': prot.deleteColumns,
            'formatCells': prot.formatCells,
            'formatColumns': prot.formatColumns,
            'formatRows': prot.formatRows,
        }

        # Only score if sheet protection is active (prevents scoring on initial_env)
        if prot.sheet is True:
            all_blocked = all(v is True for v in blocked_attrs.values())
            if all_blocked:
                print(f"PASS: Component 4 — All other operations blocked (0.3 pts)")
                total_score += 0.3
            else:
                failed = {k: v for k, v in blocked_attrs.items() if v is not True}
                print(f"FAIL: Component 4 — Some operations not blocked: {failed}")
        else:
            print(f"FAIL: Component 4 — Sheet not protected, cannot verify operation restrictions")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
