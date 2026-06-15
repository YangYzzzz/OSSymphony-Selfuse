"""
Reward Script: Using only the command line, read item_ids.xlsx and warehouse_quantities.ods
from the Desktop (each one column), merge them into inventory_check.csv with columns
ItemID and Quantity, flag items where Quantity < 5 as 'Reorder' and others as 'OK' in a
Status column, compute the total quantity across all items in a summary line appended at
the bottom, and open inventory_check.csv in LibreOffice Calc via the terminal.

Task ID: osworld_multi_apps_terminal_calc_011
Domain: libreoffice_calc (multi_apps/terminal)

Scoring:
  Component 1: inventory_check.csv exists at /home/user/Desktop/inventory_check.csv (0.20 pts)
  Component 2: CSV has correct header row with columns ItemID, Quantity, Status (0.20 pts)
  Component 3: Data rows correctly populate ItemID and Quantity (0.20 pts)
  Component 4: Status column correctly flags Reorder vs OK based on Quantity < 5 (0.20 pts)
  Component 5: Summary row at the bottom with total quantity = 282 (0.20 pts)
  Total: 1.0
"""

import os
import csv

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_terminal_calc_011'

CSV_PATH = '/home/user/Desktop/inventory_check.csv'

# Expected data: ItemID -> Quantity (derived from source files)
EXPECTED_ITEMS = [
    ('SKU-1001', 23),
    ('SKU-1002', 3),
    ('SKU-1003', 47),
    ('SKU-1004', 2),
    ('SKU-1005', 15),
    ('SKU-1006', 1),
    ('SKU-1007', 88),
    ('SKU-1008', 4),
    ('SKU-1009', 31),
    ('SKU-1010', 0),
    ('SKU-1011', 56),
    ('SKU-1012', 12),
]
EXPECTED_TOTAL = 282


def verify_task(csv_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: inventory_check.csv exists at Desktop (0.20 points)
    # This is a task-introduced file (not present in initial_env)
    try:
        if os.path.exists(csv_path):
            print(f"PASS: Component 1 — inventory_check.csv exists at {csv_path} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — inventory_check.csv not found at {csv_path}")
            # File doesn't exist — cannot score further components
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Read CSV file for further checks
    try:
        with open(csv_path, 'r', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)
    except Exception as e:
        print(f"ERROR: Cannot read CSV file: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    if len(rows) == 0:
        print("FAIL: CSV file is empty")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    header = rows[0]

    # Component 2: CSV has correct header row with columns ItemID, Quantity, Status (0.20 points)
    # These are the required columns per task specification
    try:
        # Strip whitespace for robustness
        header_stripped = [col.strip() for col in header]
        has_item_id = 'ItemID' in header_stripped
        has_quantity = 'Quantity' in header_stripped
        has_status = 'Status' in header_stripped

        if has_item_id and has_quantity and has_status:
            print(f"PASS: Component 2 — Header has ItemID, Quantity, Status columns (0.20 pts)")
            total_score += 0.20
        else:
            missing = []
            if not has_item_id:
                missing.append('ItemID')
            if not has_quantity:
                missing.append('Quantity')
            if not has_status:
                missing.append('Status')
            print(f"FAIL: Component 2 — Missing columns: {missing}, found header: {header}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Determine column indices for further checks
    try:
        header_stripped = [col.strip() for col in header]
        idx_item_id = header_stripped.index('ItemID')
        idx_quantity = header_stripped.index('Quantity')
        idx_status = header_stripped.index('Status')
    except (ValueError, IndexError) as e:
        print(f"ERROR: Cannot find required column indices ({e}), cannot score components 3-5")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Data rows (exclude header and potential summary row)
    data_rows = rows[1:]

    # Component 3: Data rows correctly populate ItemID and Quantity (0.20 points)
    # Checks that the 12 items are present with their quantities
    try:
        # Find the summary row (last row with 'Total' or non-SKU ItemID)
        # Data rows exclude summary row at the bottom
        item_rows = []
        summary_row = None
        for row in data_rows:
            if len(row) > idx_item_id:
                item_id_val = row[idx_item_id].strip()
                if item_id_val.lower() == 'total' or item_id_val == '':
                    summary_row = row
                else:
                    item_rows.append(row)

        # Build actual mapping
        actual_items = {}
        for row in item_rows:
            if len(row) > max(idx_item_id, idx_quantity):
                item_id = row[idx_item_id].strip()
                try:
                    qty = int(row[idx_quantity].strip())
                except (ValueError, IndexError):
                    try:
                        qty = float(row[idx_quantity].strip())
                    except (ValueError, IndexError):
                        qty = None
                actual_items[item_id] = qty

        # Check all expected items are present with correct quantities
        match_count = 0
        for exp_id, exp_qty in EXPECTED_ITEMS:
            if exp_id in actual_items and actual_items[exp_id] == exp_qty:
                match_count += 1
            else:
                actual_val = actual_items.get(exp_id, 'MISSING')
                print(f"  MISMATCH: {exp_id} expected qty={exp_qty}, found={actual_val}")

        if match_count == len(EXPECTED_ITEMS):
            print(f"PASS: Component 3 — All {len(EXPECTED_ITEMS)} items have correct ItemID and Quantity (0.20 pts)")
            total_score += 0.20
        elif match_count >= len(EXPECTED_ITEMS) // 2:
            print(f"PARTIAL: Component 3 — {match_count}/{len(EXPECTED_ITEMS)} items correct. Partial credit not applied (0.0 pts)")
        else:
            print(f"FAIL: Component 3 — Only {match_count}/{len(EXPECTED_ITEMS)} items correct")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Status column correctly flags Reorder vs OK based on Quantity < 5 (0.20 points)
    # Items with Quantity < 5 must be 'Reorder', others 'OK'
    try:
        status_correct = 0
        status_total = 0
        for row in item_rows:
            if len(row) > max(idx_quantity, idx_status):
                try:
                    qty_val = row[idx_quantity].strip()
                    qty = int(qty_val)
                except (ValueError, IndexError):
                    try:
                        qty = float(row[idx_quantity].strip())
                    except (ValueError, IndexError):
                        continue

                status_val = row[idx_status].strip()
                expected_status = 'Reorder' if qty < 5 else 'OK'
                status_total += 1
                if status_val == expected_status:
                    status_correct += 1
                else:
                    print(f"  STATUS MISMATCH: {row[idx_item_id]} qty={qty} expected='{expected_status}' found='{status_val}'")

        if status_total > 0 and status_correct == status_total:
            print(f"PASS: Component 4 — All {status_total} items have correct Status (Reorder/OK) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — {status_correct}/{status_total} items have correct Status")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Summary row at the bottom with total quantity = 282 (0.20 points)
    # Task requires computing total quantity and appending at bottom
    try:
        if summary_row is not None:
            # Check total quantity value
            if len(summary_row) > idx_quantity:
                try:
                    total_qty = int(summary_row[idx_quantity].strip())
                except (ValueError, IndexError):
                    try:
                        total_qty = float(summary_row[idx_quantity].strip())
                    except (ValueError, IndexError):
                        total_qty = None

                if total_qty == EXPECTED_TOTAL:
                    print(f"PASS: Component 5 — Summary row found with total quantity = {EXPECTED_TOTAL} (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 5 — Summary row found but total quantity = {total_qty}, expected {EXPECTED_TOTAL}")
            else:
                print(f"FAIL: Component 5 — Summary row found but Quantity column is missing")
        else:
            print(f"FAIL: Component 5 — No summary row found at bottom of CSV")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(CSV_PATH):
    print(f"File not found: {CSV_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(CSV_PATH)
