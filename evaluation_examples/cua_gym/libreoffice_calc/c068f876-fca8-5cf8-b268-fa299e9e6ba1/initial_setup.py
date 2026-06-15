"""
Initial Setup: Python database migration script that crashes with sqlite3.OperationalError
Task ID: osworld_multi_apps_vscode_debug_crash_010
Domain: vscode (multi-app: VSCode + SQLite)

Creates:
  - /home/user/Desktop/db_migrate/migrate.py   (buggy: no column-existence check)
  - /home/user/Desktop/db_migrate/schema.py
  - /home/user/Desktop/db_migrate/db.py
  - /home/user/Desktop/db_migrate/main.py
  - /home/user/Desktop/test.db               (pre-seeded SQLite database)
Then opens VSCode with the project folder.
"""

import os
import shlex
import sqlite3
import subprocess
import time

WORKDIR = '/home/user'
PROJECT_DIR = '/home/user/Desktop/db_migrate'
TEST_DB = '/home/user/Desktop/test.db'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_project_files():
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # --- schema.py ---
    schema_py = '''\
"""
schema.py – Column/table definitions for the customer database migration.
"""

# The v1 schema: customers table without the 'loyalty_tier' column
SCHEMA_V1 = """
CREATE TABLE IF NOT EXISTS customers (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT    NOT NULL,
    email     TEXT    UNIQUE NOT NULL,
    joined_on TEXT    NOT NULL,
    purchases INTEGER NOT NULL DEFAULT 0
);
"""

# The v2 addition: loyalty_tier column
V2_ALTER = "ALTER TABLE customers ADD COLUMN loyalty_tier TEXT DEFAULT 'bronze'"

# Seed rows for testing
SEED_CUSTOMERS = [
    ("Alice Hartwell",   "alice@example.com",   "2023-04-12", 14),
    ("Brian Okonkwo",    "brian@example.com",    "2022-11-30",  7),
    ("Cynthia Mendoza",  "cynthia@example.com",  "2024-01-05", 23),
    ("Derek Pham",       "derek@example.com",    "2023-07-19",  3),
    ("Elspeth Callahan", "elspeth@example.com",  "2021-08-22", 41),
    ("Francesca Rossi",  "francesca@example.com","2024-03-01",  9),
    ("George Ndiaye",    "george@example.com",   "2022-05-17", 18),
    ("Hannah Xu",        "hannah@example.com",   "2023-12-28",  5),
]
'''

    # --- db.py ---
    db_py = '''\
"""
db.py – Database connection and helper utilities.
"""

import sqlite3
import os


def get_connection(db_path: str) -> sqlite3.Connection:
    """Return a sqlite3 connection to *db_path*."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    """Return True if *table_name* exists in the database."""
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type=\'table\' AND name=?",
        (table_name,)
    )
    return cur.fetchone() is not None


def get_row_count(conn: sqlite3.Connection, table_name: str) -> int:
    """Return the number of rows in *table_name*."""
    cur = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
    return cur.fetchone()[0]
'''

    # --- migrate.py  (BUGGY – no column-existence guard) ---
    migrate_py = '''\
"""
migrate.py – Database migration runner.

BUG: Running this script twice raises:
    sqlite3.OperationalError: duplicate column name: loyalty_tier

The fix is to check whether the column already exists before issuing
ALTER TABLE.
"""

import sqlite3
import os
import sys

from schema import SCHEMA_V1, V2_ALTER, SEED_CUSTOMERS
from db import get_connection, table_exists


DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'test.db')
DB_PATH = os.path.normpath(DB_PATH)


def run_migration(db_path: str) -> None:
    conn = get_connection(db_path)
    try:
        # Step 1: ensure base schema exists
        conn.executescript(SCHEMA_V1)
        conn.commit()
        print("[migrate] Step 1 complete: base schema ready.")

        # Step 2: seed data if table is empty
        if table_exists(conn, 'customers'):
            count = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
            if count == 0:
                conn.executemany(
                    "INSERT INTO customers (name, email, joined_on, purchases) VALUES (?,?,?,?)",
                    SEED_CUSTOMERS,
                )
                conn.commit()
                print(f"[migrate] Step 2 complete: seeded {len(SEED_CUSTOMERS)} customers.")
            else:
                print(f"[migrate] Step 2 skipped: table already has {count} rows.")

        # Step 3: apply v2 ALTER – BUG: no guard for existing column
        conn.execute(V2_ALTER)
        conn.commit()
        print("[migrate] Step 3 complete: loyalty_tier column added.")

    finally:
        conn.close()


if __name__ == '__main__':
    db = sys.argv[1] if len(sys.argv) > 1 else DB_PATH
    print(f"[migrate] Running migration on: {db}")
    run_migration(db)
    print("[migrate] Done.")
'''

    # --- main.py ---
    main_py = '''\
"""
main.py – Entry point for the db_migrate project.

Usage:
    python main.py [path/to/database.db]

If no path is given, uses ../test.db relative to this file.
"""

import sys
import os

# Allow running from any working directory
sys.path.insert(0, os.path.dirname(__file__))

from migrate import run_migration, DB_PATH


def main():
    db_path = sys.argv[1] if len(sys.argv) > 1 else DB_PATH
    if not os.path.exists(db_path):
        print(f"[main] Creating new database at: {db_path}")
    else:
        print(f"[main] Using existing database at: {db_path}")
    run_migration(db_path)


if __name__ == '__main__':
    main()
'''

    # Write all project files
    files = {
        'schema.py': schema_py,
        'db.py':     db_py,
        'migrate.py': migrate_py,
        'main.py':   main_py,
    }
    for fname, content in files.items():
        path = os.path.join(PROJECT_DIR, fname)
        with open(path, 'w') as fh:
            fh.write(content)
        print(f'Created: {path}')


def create_test_db():
    """Create a pre-populated v1 test database (no loyalty_tier column yet)."""
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    conn = sqlite3.connect(TEST_DB)
    # Create v1 schema (no loyalty_tier)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS customers (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT    NOT NULL,
            email     TEXT    UNIQUE NOT NULL,
            joined_on TEXT    NOT NULL,
            purchases INTEGER NOT NULL DEFAULT 0
        );
    """)
    seed = [
        ("Alice Hartwell",   "alice@example.com",   "2023-04-12", 14),
        ("Brian Okonkwo",    "brian@example.com",    "2022-11-30",  7),
        ("Cynthia Mendoza",  "cynthia@example.com",  "2024-01-05", 23),
        ("Derek Pham",       "derek@example.com",    "2023-07-19",  3),
        ("Elspeth Callahan", "elspeth@example.com",  "2021-08-22", 41),
        ("Francesca Rossi",  "francesca@example.com","2024-03-01",  9),
        ("George Ndiaye",    "george@example.com",   "2022-05-17", 18),
        ("Hannah Xu",        "hannah@example.com",   "2023-12-28",  5),
    ]
    conn.executemany(
        "INSERT INTO customers (name, email, joined_on, purchases) VALUES (?,?,?,?)",
        seed,
    )
    conn.commit()
    conn.close()
    print(f'Test database created: {TEST_DB}')


def main():
    create_project_files()
    create_test_db()

    # GUI-ready: open VSCode with the project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


main()
