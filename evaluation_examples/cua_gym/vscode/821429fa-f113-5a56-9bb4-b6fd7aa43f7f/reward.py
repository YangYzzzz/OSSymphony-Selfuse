"""
Reward Script: Delete lines 5-12 (discontinued products) from inventory.csv
Task ID: vscode_edit_073
Domain: vs_code
Scoring:
  Component 1 (0.5 pts): File has exactly 22 lines after deletion of lines 5-12
  Component 2 (0.3 pts): Discontinued products P004-P011 are absent from the file
  Component 3 (0.2 pts): All active products (P001-P003, P012-P029) are still present
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_073'
FILE_PATH = '/home/user/Desktop/inventory.csv'

# The 8 discontinued product IDs that should have been deleted (were on lines 5-12)
DISCONTINUED_IDS = {'P004', 'P005', 'P006', 'P007', 'P008', 'P009', 'P010', 'P011'}

# The active product IDs that should remain (were on lines 2-4 and 13-30)
ACTIVE_IDS = {
    'P001', 'P002', 'P003',
    'P012', 'P013', 'P014', 'P015', 'P016', 'P017', 'P018', 'P019', 'P020',
    'P021', 'P022', 'P023', 'P024', 'P025', 'P026', 'P027', 'P028', 'P029'
}

EXPECTED_LINE_COUNT = 22  # 1 header + 21 active product rows


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load file as precondition gate
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Validate file has at least a header
    if len(lines) == 0:
        print("CRITICAL: File is empty")
        print("REWARD: 0.0")
        return 0.0

    # Strip trailing newlines and gather content
    stripped_lines = [line.rstrip('\n') for line in lines]
    actual_line_count = len(stripped_lines)

    # Extract all product IDs present in the file (skip header on line 1)
    present_ids = set()
    for line in stripped_lines[1:]:
        parts = line.split(',')
        if parts:
            pid = parts[0].strip()
            if pid:
                present_ids.add(pid)

    # Component 1: File has exactly 22 lines (0.5 points)
    # Initial state has 30 lines; 22 lines means the 8 discontinued lines were deleted.
    # This FAILS on initial (30 lines) and PASSES on golden (22 lines).
    try:
        if actual_line_count == EXPECTED_LINE_COUNT:
            print(f"PASS: Component 1 — file has exactly {EXPECTED_LINE_COUNT} lines (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — expected {EXPECTED_LINE_COUNT} lines, found {actual_line_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Discontinued products P004-P011 are absent (0.3 points)
    # These IDs were on lines 5-12 of the initial file (all discontinued).
    # This FAILS on initial (all 8 IDs present) and PASSES on golden (none present).
    try:
        still_present = DISCONTINUED_IDS.intersection(present_ids)
        if len(still_present) == 0:
            print(f"PASS: Component 2 — all discontinued products (P004-P011) removed (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — discontinued products still present: {sorted(still_present)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All active products (P001-P003, P012-P029) are still present (0.2 points)
    # This verifies data integrity — the task should only remove discontinued products.
    # This FAILS on initial if any active product is missing, and PASSES on golden.
    # NOTE: On initial_env, all active products ARE present so this component could pass on initial.
    # To ensure it only awards points for the complete task (conjunction with Component 1),
    # we check: active products present AND discontinued products absent.
    # However to keep this independently scoreable, we make it conditional:
    # It only awards if active products are all present AND at least one discontinued product was removed.
    try:
        missing_active = ACTIVE_IDS - present_ids
        at_least_one_discontinued_removed = len(DISCONTINUED_IDS - present_ids) > 0
        if len(missing_active) == 0 and at_least_one_discontinued_removed:
            print(f"PASS: Component 3 — all 21 active products present and deletions confirmed (0.2 pts)")
            total_score += 0.2
        elif len(missing_active) > 0:
            print(f"FAIL: Component 3 — missing active products: {sorted(missing_active)}")
        else:
            print(f"FAIL: Component 3 — active products intact but no discontinued products removed yet")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in the VM environment
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
