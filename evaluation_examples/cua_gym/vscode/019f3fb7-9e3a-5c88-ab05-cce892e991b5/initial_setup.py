"""
Initial Setup: Configure Python test discovery to use 'check_*.py' pattern
Task ID: vscode_py_055
Domain: vscode

Creates a Python project with test files using 'check_' prefix.
pytest is configured but uses default test_*.py discovery (no custom pattern).
VSCode is opened with the project folder.
"""

import json
import os
import shlex
import subprocess
import time

HOME = "/home/user"
WORKSPACE = os.path.join(HOME, "workspace")
TESTS_DIR = os.path.join(WORKSPACE, "tests")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")
VSCODE_WS = os.path.join(WORKSPACE, ".vscode")
WS_SETTINGS_PATH = os.path.join(VSCODE_WS, "settings.json")


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


def create_project():
    """Create a realistic Python project with check_* test files."""
    os.makedirs(TESTS_DIR, exist_ok=True)
    os.makedirs(VSCODE_WS, exist_ok=True)

    # --- Main application files ---

    # app.py - a simple authentication module
    app_py = '''\
"""
Simple user authentication and database utility module.
"""

import hashlib
import sqlite3
import os


class AuthManager:
    """Handles user authentication with hashed passwords."""

    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        conn.commit()
        conn.close()

    def _hash_password(self, password: str) -> str:
        salt = os.urandom(16).hex()
        hashed = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
        return f"{salt}:{hashed}"

    def _verify_hash(self, password: str, stored_hash: str) -> bool:
        salt, expected = stored_hash.split(":")
        actual = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
        return actual == expected

    def register(self, username: str, password: str, email: str = None) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            pw_hash = self._hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
                (username, pw_hash, email),
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def authenticate(self, username: str, password: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password_hash FROM users WHERE username = ? AND is_active = 1",
            (username,),
        )
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return False
        return self._verify_hash(password, row[0])

    def deactivate_user(self, username: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET is_active = 0 WHERE username = ?", (username,)
        )
        changed = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return changed


class DatabaseManager:
    """Manages product inventory in a SQLite database."""

    def __init__(self, db_path="inventory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                sku TEXT UNIQUE NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER DEFAULT 0,
                category TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def add_product(self, name: str, sku: str, price: float,
                    quantity: int = 0, category: str = None) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO products (name, sku, price, quantity, category) "
                "VALUES (?, ?, ?, ?, ?)",
                (name, sku, price, quantity, category),
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_product(self, sku: str) -> dict | None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE sku = ?", (sku,))
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return None
        cols = ["id", "name", "sku", "price", "quantity", "category", "last_updated"]
        return dict(zip(cols, row))

    def update_quantity(self, sku: str, delta: int) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE products SET quantity = quantity + ?, "
            "last_updated = CURRENT_TIMESTAMP WHERE sku = ?",
            (delta, sku),
        )
        changed = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return changed

    def low_stock_report(self, threshold: int = 5) -> list:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, sku, quantity FROM products WHERE quantity <= ?",
            (threshold,),
        )
        rows = cursor.fetchall()
        conn.close()
        return [{"name": r[0], "sku": r[1], "quantity": r[2]} for r in rows]
'''
    with open(os.path.join(WORKSPACE, "app.py"), "w") as f:
        f.write(app_py)

    # --- tests/__init__.py ---
    with open(os.path.join(TESTS_DIR, "__init__.py"), "w") as f:
        f.write("")

    # --- tests/check_auth.py - Authentication tests using check_ prefix ---
    check_auth = '''\
"""
Authentication module tests.
These tests verify user registration, login, and account deactivation.
"""

import os
import sys
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import AuthManager


class TestAuthManager:
    """Test suite for AuthManager."""

    def setup_method(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.tmp.close()
        self.auth = AuthManager(db_path=self.tmp.name)

    def teardown_method(self):
        os.unlink(self.tmp.name)

    def test_register_new_user(self):
        assert self.auth.register("alice", "securePass123", "alice@example.com")

    def test_register_duplicate_user(self):
        self.auth.register("bob", "password1", "bob@example.com")
        assert not self.auth.register("bob", "password2", "bob2@example.com")

    def test_authenticate_valid_credentials(self):
        self.auth.register("charlie", "myP@ssw0rd")
        assert self.auth.authenticate("charlie", "myP@ssw0rd")

    def test_authenticate_wrong_password(self):
        self.auth.register("diana", "correctPass")
        assert not self.auth.authenticate("diana", "wrongPass")

    def test_authenticate_nonexistent_user(self):
        assert not self.auth.authenticate("nobody", "anything")

    def test_deactivate_user(self):
        self.auth.register("eve", "pass123")
        assert self.auth.deactivate_user("eve")
        assert not self.auth.authenticate("eve", "pass123")

    def test_deactivate_nonexistent_user(self):
        assert not self.auth.deactivate_user("ghost_user")
'''
    with open(os.path.join(TESTS_DIR, "check_auth.py"), "w") as f:
        f.write(check_auth)

    # --- tests/check_database.py - Database tests using check_ prefix ---
    check_database = '''\
"""
Database manager tests.
These tests verify product CRUD operations and inventory reports.
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import DatabaseManager


class TestDatabaseManager:
    """Test suite for DatabaseManager."""

    def setup_method(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.tmp.close()
        self.db = DatabaseManager(db_path=self.tmp.name)

    def teardown_method(self):
        os.unlink(self.tmp.name)

    def test_add_product(self):
        assert self.db.add_product(
            "Wireless Mouse", "WM-001", 29.99, 50, "Electronics"
        )

    def test_add_duplicate_sku(self):
        self.db.add_product("Item A", "SKU-100", 10.00)
        assert not self.db.add_product("Item B", "SKU-100", 20.00)

    def test_get_product(self):
        self.db.add_product("USB Cable", "UC-042", 8.50, 200, "Accessories")
        product = self.db.get_product("UC-042")
        assert product is not None
        assert product["name"] == "USB Cable"
        assert product["price"] == 8.50

    def test_get_nonexistent_product(self):
        assert self.db.get_product("FAKE-999") is None

    def test_update_quantity(self):
        self.db.add_product("Keyboard", "KB-007", 45.00, 30)
        assert self.db.update_quantity("KB-007", -5)
        product = self.db.get_product("KB-007")
        assert product["quantity"] == 25

    def test_low_stock_report(self):
        self.db.add_product("Widget A", "WA-01", 5.00, 3)
        self.db.add_product("Widget B", "WB-02", 7.00, 100)
        self.db.add_product("Widget C", "WC-03", 3.50, 1)
        report = self.db.low_stock_report(threshold=5)
        skus = [item["sku"] for item in report]
        assert "WA-01" in skus
        assert "WC-03" in skus
        assert "WB-02" not in skus
'''
    with open(os.path.join(TESTS_DIR, "check_database.py"), "w") as f:
        f.write(check_database)

    # --- requirements.txt ---
    with open(os.path.join(WORKSPACE, "requirements.txt"), "w") as f:
        f.write("pytest>=7.0\n")

    # --- .vscode/settings.json - pytest enabled but using defaults ---
    ws_settings = {
        "python.testing.pytestEnabled": True,
        "python.testing.unittestEnabled": False,
        "python.defaultInterpreterPath": "/usr/bin/python3",
    }
    with open(WS_SETTINGS_PATH, "w") as f:
        json.dump(ws_settings, f, indent=4)

    # --- Global VSCode settings (merge, don't overwrite) ---
    os.makedirs(VSCODE_USER, exist_ok=True)
    global_settings = {}
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                global_settings = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            global_settings = {}

    global_settings.update({
        "python.testing.pytestEnabled": True,
        "python.testing.unittestEnabled": False,
    })
    with open(SETTINGS_PATH, "w") as f:
        json.dump(global_settings, f, indent=4)

    print(f"Project created at: {WORKSPACE}")
    print(f"Test files: {os.listdir(TESTS_DIR)}")

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE}"', delay_sec=3.0)
    print("GUI_READY: launched VSCode with DISPLAY=:0")


create_project()
