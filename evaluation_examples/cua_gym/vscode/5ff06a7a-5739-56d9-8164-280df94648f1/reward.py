"""
Reward Script: Accept all incoming changes in VSCode diff editor for schema.sql
Task ID: vscode_rf_028
Domain: vscode
Scoring:
  Component 1 (0.3): Version header updated to 4.0.0
  Component 2 (0.3): New tables present (brands, product_reviews, wishlists, discount_codes, inventory_log)
  Component 3 (0.2): Deprecated tables removed (legacy_user_profiles, deprecated_product_tags, old_review_system)
  Component 4 (0.2): Key structural changes (new columns, new indexes, new views)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_rf_028'


def verify_task(file_path):
    """
    Verify that all incoming diff changes were accepted in schema.sql.
    The file should match the incoming version (v4.0.0) after accepting all changes.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Version header updated to 4.0.0 (0.3 points)
    # Initial has "Version: 3.2.1" and "Last updated: 2025-08-10"
    # Golden has "Version: 4.0.0" and "Last updated: 2025-11-22"
    try:
        has_new_version = 'Version: 4.0.0' in content
        has_new_date = '2025-11-22' in content
        has_old_version = 'Version: 3.2.1' in content

        if has_new_version and has_new_date and not has_old_version:
            print(f"PASS: Component 1 -- Version updated to 4.0.0, date to 2025-11-22 (0.3 pts)")
            total_score += 0.3
        elif has_new_version and not has_old_version:
            print(f"PARTIAL: Component 1 -- Version updated but date may be wrong (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Version header not updated. Has v4.0.0: {has_new_version}, has v3.2.1: {has_old_version}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: New tables present (0.3 points)
    # These tables exist in incoming but NOT in initial:
    # brands, product_reviews, wishlists, discount_codes, inventory_log
    try:
        new_tables = ['brands', 'product_reviews', 'wishlists', 'discount_codes', 'inventory_log']
        found_count = 0
        for table in new_tables:
            # Check for CREATE TABLE <name> pattern
            if f'CREATE TABLE {table}' in content:
                found_count += 1
            else:
                print(f"  MISS: New table '{table}' not found")

        if found_count == len(new_tables):
            print(f"PASS: Component 2 -- All {len(new_tables)} new tables present (0.3 pts)")
            total_score += 0.3
        elif found_count > 0:
            partial = round(0.3 * found_count / len(new_tables), 2)
            print(f"PARTIAL: Component 2 -- {found_count}/{len(new_tables)} new tables found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No new tables found (0/5)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Deprecated tables removed (0.2 points)
    # These tables exist in initial but NOT in incoming:
    # legacy_user_profiles, deprecated_product_tags, old_review_system
    try:
        deprecated_tables = ['legacy_user_profiles', 'deprecated_product_tags', 'old_review_system']
        removed_count = 0
        for table in deprecated_tables:
            if f'CREATE TABLE {table}' not in content:
                removed_count += 1
            else:
                print(f"  STILL PRESENT: Deprecated table '{table}' should be removed")

        if removed_count == len(deprecated_tables):
            print(f"PASS: Component 3 -- All {len(deprecated_tables)} deprecated tables removed (0.2 pts)")
            total_score += 0.2
        elif removed_count > 0:
            partial = round(0.2 * removed_count / len(deprecated_tables), 2)
            print(f"PARTIAL: Component 3 -- {removed_count}/{len(deprecated_tables)} deprecated tables removed ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- No deprecated tables removed")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Key structural changes applied (0.2 points)
    # Check for specific changes that differentiate v4.0.0 from v3.2.1:
    # - users table has 'role' column and 'display_name' column
    # - products table has 'sku' column
    # - product_catalog view exists
    # - New indexes like idx_products_brand, idx_orders_status
    try:
        structural_checks = {
            'users.role column': "role            VARCHAR(30) DEFAULT 'customer'" in content,
            'users.display_name column': 'display_name    VARCHAR(120)' in content,
            'products.sku column': 'sku             VARCHAR(50) NOT NULL UNIQUE' in content,
            'product_catalog view': 'CREATE VIEW product_catalog' in content,
            'idx_products_brand index': 'idx_products_brand' in content,
            'idx_orders_status index': 'idx_orders_status' in content,
        }

        passed = sum(1 for v in structural_checks.values() if v)
        total_checks = len(structural_checks)

        for name, result in structural_checks.items():
            if not result:
                print(f"  MISS: {name}")

        if passed == total_checks:
            print(f"PASS: Component 4 -- All {total_checks} structural changes verified (0.2 pts)")
            total_score += 0.2
        elif passed > 0:
            partial = round(0.2 * passed / total_checks, 2)
            print(f"PARTIAL: Component 4 -- {passed}/{total_checks} structural changes present ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- No structural changes found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/projects/database/schema.sql'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
