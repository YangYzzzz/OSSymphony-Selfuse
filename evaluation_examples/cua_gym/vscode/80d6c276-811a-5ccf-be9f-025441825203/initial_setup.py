"""
Initial Setup: Create a Django project with test directories for VSCode tasks.json task
Task ID: vscode_td_015
Domain: vscode
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'django-app')

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

def create_initial():
    # Create project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create test directories with sample test files
    test_dirs = {
        'tests/unit': [
            ('test_models.py', '''import pytest


class TestUserModel:
    def test_user_creation(self):
        """Test that a user can be created with valid data."""
        user_data = {"username": "sarah_chen", "email": "sarah@example.com"}
        assert user_data["username"] == "sarah_chen"
        assert "@" in user_data["email"]

    def test_user_str_representation(self):
        """Test the string representation of a user."""
        username = "marcus_johnson"
        assert len(username) > 0

    def test_user_email_validation(self):
        """Test email validation logic."""
        valid_emails = ["test@example.com", "admin@company.org"]
        for email in valid_emails:
            assert "@" in email and "." in email
'''),
            ('test_utils.py', '''import pytest


class TestStringUtils:
    def test_slugify(self):
        """Test slug generation from title strings."""
        title = "My Blog Post Title"
        slug = title.lower().replace(" ", "-")
        assert slug == "my-blog-post-title"

    def test_truncate(self):
        """Test string truncation with ellipsis."""
        text = "This is a long description that should be truncated"
        truncated = text[:20] + "..." if len(text) > 20 else text
        assert truncated.endswith("...")
'''),
        ],
        'tests/integration': [
            ('test_api.py', '''import pytest


class TestAPIEndpoints:
    def test_list_products(self):
        """Test the product listing endpoint returns valid data."""
        products = [
            {"id": 1, "name": "Widget A", "price": 29.99},
            {"id": 2, "name": "Widget B", "price": 49.99},
        ]
        assert len(products) == 2
        assert all("price" in p for p in products)

    def test_create_order(self):
        """Test creating a new order via the API."""
        order = {"product_id": 1, "quantity": 3, "customer": "Acme Corp"}
        assert order["quantity"] > 0
        assert order["customer"] != ""

    def test_authentication_flow(self):
        """Test the login and token refresh flow."""
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.mock"
        assert token.startswith("eyJ")
'''),
            ('test_database.py', '''import pytest


class TestDatabaseOperations:
    def test_connection_pool(self):
        """Test database connection pooling behavior."""
        pool_size = 5
        assert pool_size > 0

    def test_migration_integrity(self):
        """Test that migrations apply cleanly."""
        migrations = ["0001_initial", "0002_add_products", "0003_add_orders"]
        assert len(migrations) == 3
        assert migrations[0].startswith("0001")
'''),
        ],
        'tests/e2e': [
            ('test_checkout.py', '''import pytest


class TestCheckoutFlow:
    def test_add_to_cart_and_checkout(self):
        """Test the full checkout flow from cart to payment."""
        cart_items = [
            {"name": "Laptop Stand", "price": 45.00, "qty": 1},
            {"name": "USB-C Hub", "price": 35.00, "qty": 2},
        ]
        total = sum(item["price"] * item["qty"] for item in cart_items)
        assert total == 115.00

    def test_guest_checkout(self):
        """Test checkout as a guest user without registration."""
        guest_email = "guest@tempmail.com"
        assert "@" in guest_email
'''),
            ('test_user_registration.py', '''import pytest


class TestUserRegistration:
    def test_full_registration_flow(self):
        """Test registration from form fill to email verification."""
        registration_data = {
            "username": "new_user_2025",
            "email": "newuser@example.com",
            "password": "SecureP@ss123",
        }
        assert len(registration_data["password"]) >= 8

    def test_duplicate_email_rejection(self):
        """Test that duplicate emails are rejected during registration."""
        existing_emails = ["admin@example.com", "user@example.com"]
        new_email = "admin@example.com"
        assert new_email in existing_emails
'''),
        ],
    }

    for test_dir, files in test_dirs.items():
        dir_path = os.path.join(PROJECT_DIR, test_dir)
        os.makedirs(dir_path, exist_ok=True)
        # Create __init__.py for proper Python package
        init_path = os.path.join(dir_path, '__init__.py')
        if not os.path.exists(init_path):
            with open(init_path, 'w') as f:
                f.write('')
        for filename, content in files:
            filepath = os.path.join(dir_path, filename)
            with open(filepath, 'w') as f:
                f.write(content)

    # Create tests/__init__.py
    tests_init = os.path.join(PROJECT_DIR, 'tests', '__init__.py')
    if not os.path.exists(tests_init):
        with open(tests_init, 'w') as f:
            f.write('')

    # Create a basic manage.py for the django-app feel
    manage_py = os.path.join(PROJECT_DIR, 'manage.py')
    with open(manage_py, 'w') as f:
        f.write('''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
''')

    # Create a basic requirements.txt
    req_path = os.path.join(PROJECT_DIR, 'requirements.txt')
    with open(req_path, 'w') as f:
        f.write('''Django==4.2.7
djangorestframework==3.14.0
pytest==7.4.3
pytest-django==4.7.0
psycopg2-binary==2.9.9
redis==5.0.1
celery==5.3.6
''')

    # Create a conftest.py at the project root
    conftest_path = os.path.join(PROJECT_DIR, 'conftest.py')
    with open(conftest_path, 'w') as f:
        f.write('''import pytest


@pytest.fixture
def sample_user():
    return {"username": "testuser", "email": "test@example.com"}


@pytest.fixture
def api_client():
    """Simulated API client fixture."""
    return {"base_url": "http://localhost:8000/api/v1"}
''')

    # Create .vscode directory but NO tasks.json
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    os.makedirs(vscode_dir, exist_ok=True)

    # Create a basic settings.json in .vscode so the directory isn't empty
    vscode_settings = os.path.join(vscode_dir, 'settings.json')
    with open(vscode_settings, 'w') as f:
        json.dump({
            "python.testing.pytestEnabled": True,
            "python.testing.pytestArgs": ["tests"],
            "editor.formatOnSave": True
        }, f, indent=4)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Test directories: tests/unit/, tests/integration/, tests/e2e/')
    print(f'No .vscode/tasks.json exists (as required)')

    # Launch VSCode with the project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
