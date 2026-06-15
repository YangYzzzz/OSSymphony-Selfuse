"""
Reward Script: Database schema management workflow in VSCode
Task ID: vscode_wf_064
Domain: vscode
Scoring:
  Component 1 (0.30): Migration SQL files exist with proper CREATE TABLE/INDEX statements
  Component 2 (0.15): SQLite extension installed
  Component 3 (0.25): tasks.json with migrate-up, migrate-down, db-seed tasks
  Component 4 (0.15): settings.json with SQL language configuration
  Component 5 (0.15): Seed data file exists with INSERT statements
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
TASK_ID = 'vscode_wf_064'


def strip_jsonc_comments(text):
    """Strip // and /* */ comments from JSONC (VSCode config files)."""
    text = re.sub(r'//.*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    return text


def check_extension_installed(ext_id):
    """Check if a VSCode extension is installed via filesystem."""
    extensions_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
    if os.path.isdir(extensions_dir):
        for entry in os.listdir(extensions_dir):
            if entry.lower().startswith(ext_id.lower()):
                return entry
    return None


def find_seed_file():
    """Find a seed data file containing INSERT statements."""
    candidates = [
        os.path.join(PROJECT, 'seeds', 'data.sql'),
        os.path.join(PROJECT, 'scripts', 'seed.py'),
        os.path.join(PROJECT, 'seeds', 'seed.sql'),
        os.path.join(PROJECT, 'scripts', 'seed.sql'),
        os.path.join(PROJECT, 'seed.sql'),
        os.path.join(PROJECT, 'seed_data.sql'),
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            content = open(candidate, 'r').read()
            if candidate.endswith('.sql') and 'INSERT' in content.upper():
                return candidate
            elif candidate.endswith('.py') and ('INSERT' in content.upper() or 'execute' in content.lower()):
                return candidate
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # =========================================================================
    # Component 1: Migration SQL files (0.30 points)
    # Check that migrations/ dir has 3 numbered .sql files with proper SQL DDL
    # =========================================================================
    try:
        migrations_dir = os.path.join(PROJECT, 'migrations')
        if not os.path.isdir(migrations_dir):
            print("FAIL: Component 1 — migrations/ directory does not exist")
        else:
            sql_files = sorted([f for f in os.listdir(migrations_dir) if f.endswith('.sql')])
            expected_patterns = [
                ('001', 'CREATE TABLE'),
                ('002', 'CREATE TABLE'),
                ('003', 'CREATE INDEX'),
            ]
            for prefix, sql_keyword in expected_patterns:
                matching = [f for f in sql_files if f.startswith(prefix)]
                if not matching:
                    print(f"FAIL: Component 1 — No migration file starting with '{prefix}' found")
                    continue
                fpath = os.path.join(migrations_dir, matching[0])
                content = open(fpath, 'r').read()
                if sql_keyword.upper() in content.upper():
                    print(f"PASS: Component 1 — {matching[0]} contains {sql_keyword} (0.10 pts)")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 1 — {matching[0]} missing {sql_keyword} statement")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # =========================================================================
    # Component 2: SQLite extension installed (0.15 points)
    # Check via filesystem: ~/.vscode/extensions/alexcvzz.vscode-sqlite-*
    # =========================================================================
    try:
        ext_entry = check_extension_installed('alexcvzz.vscode-sqlite')
        if ext_entry is not None:
            print(f"PASS: Component 2 — alexcvzz.vscode-sqlite extension found at {ext_entry} (0.15 pts)")
            total_score += 0.15
        else:
            extensions_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
            installed = os.listdir(extensions_dir) if os.path.isdir(extensions_dir) else []
            print(f"FAIL: Component 2 — alexcvzz.vscode-sqlite not found. Installed: {installed}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # =========================================================================
    # Component 3: tasks.json with required task labels (0.25 points)
    # Must have tasks labeled: migrate-up, migrate-down, db-seed
    # =========================================================================
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        if not os.path.exists(tasks_path):
            print("FAIL: Component 3 — .vscode/tasks.json does not exist")
        else:
            raw = open(tasks_path, 'r').read()
            cleaned = strip_jsonc_comments(raw)
            tasks_config = json.loads(cleaned)
            task_labels = set()
            for t in tasks_config.get('tasks', []):
                label = t.get('label', '')
                task_labels.add(label.lower().strip())

            required_labels = ['migrate-up', 'migrate-down', 'db-seed']
            for label in required_labels:
                if label in task_labels:
                    pts = round(0.25 / 3, 4)
                    print(f"PASS: Component 3 — Task '{label}' found ({pts} pts)")
                    total_score += pts
                else:
                    print(f"FAIL: Component 3 — Task '{label}' not found. Available: {task_labels}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # =========================================================================
    # Component 4: settings.json with SQL language configuration (0.15 points)
    # Must have SQL-related settings (e.g., [sql] section, formatOnSave, etc.)
    # =========================================================================
    try:
        settings_path = os.path.join(PROJECT, '.vscode', 'settings.json')
        if not os.path.exists(settings_path):
            print("FAIL: Component 4 — .vscode/settings.json does not exist")
        else:
            raw = open(settings_path, 'r').read()
            cleaned = strip_jsonc_comments(raw)
            settings = json.loads(cleaned)

            sql_indicators = 0

            if '[sql]' in settings:
                sql_indicators += 2
                print("  Found [sql] language-specific configuration block")

            for key in settings:
                if 'sql' in key.lower():
                    sql_indicators += 1

            assoc = settings.get('files.associations', {})
            if isinstance(assoc, dict) and any('sql' in k.lower() for k in assoc):
                sql_indicators += 1

            if sql_indicators >= 2:
                print(f"PASS: Component 4 — SQL language settings configured ({sql_indicators} SQL indicators found) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — Insufficient SQL configuration. Only {sql_indicators} SQL-related settings found (need >= 2)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # =========================================================================
    # Component 5: Seed data file with INSERT statements (0.15 points)
    # Check seeds/data.sql or scripts/seed.py or similar
    # =========================================================================
    try:
        seed_path = find_seed_file()
        if seed_path is not None:
            print(f"PASS: Component 5 — Seed file {seed_path} contains data insertion statements (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 5 — No seed data file found in expected locations")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
