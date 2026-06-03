"""
Reward Script: Database Migration Framework with Flyway
Task ID: os_adm_078
Domain: os (libreoffice_calc label but actually OS/PostgreSQL task)

Scoring Rubric:
  Component 1: flyway.conf exists and is properly configured (0.20)
  Component 2: safe_migrate.sh exists, is executable, and has correct shebang (0.15)
  Component 3: safe_migrate.sh contains backup and rollback logic (0.15)
  Component 4: V2 migration applied - user_preferences table exists (0.20)
  Component 5: V3 migration applied - performance indexes exist (0.15)
  Component 6: flyway_schema_history tracks V2 and V3 as successful (0.15)
  Total: 1.0
"""

import os
import re

# NOTE: This script runs on the VM. We use subprocess to query PostgreSQL.
import subprocess


def run_psql(query, dbname="production_app"):
    """Run a psql query and return stdout."""
    try:
        result = subprocess.run(
            ["sudo", "-u", "postgres", "psql", "-d", dbname, "-t", "-A", "-c", query],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"  psql error: {e}")
        return ""


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: flyway.conf exists and is properly configured (0.20 points)
    try:
        conf_path = "/opt/migrations/flyway.conf"
        if os.path.isfile(conf_path):
            with open(conf_path, "r") as f:
                conf_content = f.read()
            # Must reference production_app database
            has_url = "production_app" in conf_content and "postgresql" in conf_content
            # Must have sql location
            has_location = "locations" in conf_content and "/opt/migrations/sql" in conf_content
            if has_url and has_location:
                print(f"PASS: Component 1 — flyway.conf exists with production_app URL and sql location (0.20 pts)")
                total_score += 0.20
            elif has_url:
                print(f"PARTIAL: Component 1 — flyway.conf has URL but missing sql location (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 1 — flyway.conf missing required config (has_url={has_url}, has_location={has_location})")
        else:
            print(f"FAIL: Component 1 — {conf_path} does not exist")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: safe_migrate.sh exists, is executable, has correct shebang (0.15 points)
    try:
        script_path = "/usr/local/bin/safe_migrate.sh"
        if os.path.isfile(script_path):
            import stat
            mode = os.stat(script_path).st_mode
            is_executable = bool(mode & stat.S_IXUSR)
            with open(script_path, "r") as f:
                first_line = f.readline().strip()
            has_shebang = first_line.startswith("#!/bin/bash") or first_line.startswith("#!/usr/bin/env bash")
            if is_executable and has_shebang:
                print(f"PASS: Component 2 — safe_migrate.sh exists, executable, bash shebang (0.15 pts)")
                total_score += 0.15
            elif is_executable:
                print(f"PARTIAL: Component 2 — safe_migrate.sh executable but no bash shebang (0.08 pts)")
                total_score += 0.08
            else:
                print(f"FAIL: Component 2 — safe_migrate.sh exists but not executable or missing shebang")
        else:
            print(f"FAIL: Component 2 — {script_path} does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: safe_migrate.sh contains backup and rollback logic (0.15 points)
    try:
        script_path = "/usr/local/bin/safe_migrate.sh"
        if os.path.isfile(script_path):
            with open(script_path, "r") as f:
                script_content = f.read()
            # Must have backup (pg_dump), flyway migrate, and restore/rollback
            has_backup = "pg_dump" in script_content
            has_migrate = "flyway" in script_content and "migrate" in script_content
            has_rollback = ("restore" in script_content.lower() or "rollback" in script_content.lower()
                          or "dropdb" in script_content or "psql" in script_content)

            checks_passed = sum([has_backup, has_migrate, has_rollback])
            if checks_passed == 3:
                print(f"PASS: Component 3 — safe_migrate.sh has backup, migrate, and rollback logic (0.15 pts)")
                total_score += 0.15
            elif checks_passed >= 2:
                print(f"PARTIAL: Component 3 — safe_migrate.sh has {checks_passed}/3 required sections (0.08 pts)")
                total_score += 0.08
            else:
                print(f"FAIL: Component 3 — safe_migrate.sh missing key logic (backup={has_backup}, migrate={has_migrate}, rollback={has_rollback})")
        else:
            print(f"FAIL: Component 3 — safe_migrate.sh does not exist, cannot check content")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: V2 migration applied - user_preferences table exists (0.20 points)
    try:
        tables_output = run_psql(
            "SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename;"
        )
        tables = [t.strip() for t in tables_output.split("\n") if t.strip()]
        if "user_preferences" in tables:
            print(f"PASS: Component 4 — user_preferences table exists in production_app (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — user_preferences table not found. Tables: {tables}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: V3 migration applied - performance indexes exist (0.15 points)
    try:
        indexes_output = run_psql(
            "SELECT indexname FROM pg_indexes WHERE schemaname='public' ORDER BY indexname;"
        )
        indexes = [i.strip() for i in indexes_output.split("\n") if i.strip()]
        # V3 should create: idx_users_email, idx_users_username, idx_users_created_at, idx_users_is_active
        expected_indexes = {"idx_users_email", "idx_users_username", "idx_users_created_at", "idx_users_is_active"}
        found = expected_indexes.intersection(set(indexes))
        if len(found) == len(expected_indexes):
            print(f"PASS: Component 5 — All 4 performance indexes from V3 exist (0.15 pts)")
            total_score += 0.15
        elif len(found) >= 2:
            partial = round(0.15 * len(found) / len(expected_indexes), 2)
            print(f"PARTIAL: Component 5 — {len(found)}/{len(expected_indexes)} indexes found: {found} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — Expected indexes {expected_indexes}, found only {found}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: flyway_schema_history tracks V2 and V3 as successful (0.15 points)
    try:
        history_output = run_psql(
            "SELECT version, success FROM flyway_schema_history WHERE type='SQL' ORDER BY version;"
        )
        rows = [r.strip() for r in history_output.split("\n") if r.strip()]
        # Expect "2|t" and "3|t"
        v2_success = any("2|t" in r for r in rows)
        v3_success = any("3|t" in r for r in rows)
        if v2_success and v3_success:
            print(f"PASS: Component 6 — flyway_schema_history shows V2 and V3 as successful (0.15 pts)")
            total_score += 0.15
        elif v2_success or v3_success:
            print(f"PARTIAL: Component 6 — Only one migration tracked (V2={v2_success}, V3={v3_success}) (0.08 pts)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 6 — Neither V2 nor V3 found as successful in schema history. Rows: {rows}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
