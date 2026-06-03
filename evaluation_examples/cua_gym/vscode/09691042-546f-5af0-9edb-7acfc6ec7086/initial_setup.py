"""
Initial Setup: Git rebase --onto practice repository
Task ID: vscode_gf6_063
Domain: vscode

Creates a git repository with three branches:
- main (10 commits)
- feature/base (branched from commit 5, 3 more commits)
- feature/dependent (branched from feature/base tip, 4 more commits)
A conflict exists in src/config.py between main and feature/base.
feature/dependent commits are self-contained so rebase --onto main feature/base works.
"""

import os
import shlex
import subprocess
import time
import shutil

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_063'
REPO_DIR = f'{WORKDIR}/projects/git-rebase-onto'


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


def run(cmd, cwd=None):
    """Run shell command, raising on failure."""
    result = subprocess.run(
        ['bash', '-c', cmd], cwd=cwd or REPO_DIR,
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"CMD FAILED: {cmd}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        raise RuntimeError(f"Command failed: {cmd}")
    return result.stdout.strip()


def create_initial():
    # Clean up any existing repo
    if os.path.exists(REPO_DIR):
        shutil.rmtree(REPO_DIR)

    os.makedirs(REPO_DIR, exist_ok=True)

    # Initialize git repo with main branch
    run('git init', cwd=REPO_DIR)
    run('git checkout -b main', cwd=REPO_DIR)
    run('git config user.email "developer@example.com"', cwd=REPO_DIR)
    run('git config user.name "Developer"', cwd=REPO_DIR)

    # Create directory structure
    os.makedirs(f'{REPO_DIR}/src', exist_ok=True)
    os.makedirs(f'{REPO_DIR}/tests', exist_ok=True)

    # ========== MAIN BRANCH: Commits 1-5 ==========

    # Commit 1: Initial project structure
    with open(f'{REPO_DIR}/README.md', 'w') as f:
        f.write("# Git Rebase Onto Practice\n\nA Python project for practicing git rebase --onto.\n")
    with open(f'{REPO_DIR}/requirements.txt', 'w') as f:
        f.write("pytest>=7.0\nrequests>=2.28\n")
    run('git add -A')
    run('git commit -m "Initial project structure with README and requirements"')

    # Commit 2: Add main app module
    with open(f'{REPO_DIR}/src/__init__.py', 'w') as f:
        f.write("")
    with open(f'{REPO_DIR}/src/app.py', 'w') as f:
        f.write('''"""Main application module."""


class Application:
    """Core application class."""

    def __init__(self, name="GitRebaseApp"):
        self.name = name
        self.version = "1.0.0"
        self.modules = []

    def register_module(self, module_name):
        """Register a new module with the application."""
        if module_name not in self.modules:
            self.modules.append(module_name)
            return True
        return False

    def get_status(self):
        """Return application status summary."""
        return {
            "name": self.name,
            "version": self.version,
            "modules_loaded": len(self.modules),
        }
''')
    run('git add -A')
    run('git commit -m "Add core application module"')

    # Commit 3: Add src/config.py (will be the conflict file)
    with open(f'{REPO_DIR}/src/config.py', 'w') as f:
        f.write('''"""Application configuration module."""

# Database settings
DATABASE = {
    "host": "localhost",
    "port": 5432,
    "name": "app_db",
}

# API settings
API_VERSION = "v1"
API_TIMEOUT = 30

# Feature flags
FEATURES = {
    "caching": True,
    "logging": True,
    "debug_mode": False,
}


def get_config():
    """Return the full configuration dictionary."""
    return {
        "database": DATABASE,
        "api_version": API_VERSION,
        "api_timeout": API_TIMEOUT,
        "features": FEATURES,
    }
''')
    run('git add -A')
    run('git commit -m "Add configuration module with database and API settings"')

    # Commit 4: Add test infrastructure
    with open(f'{REPO_DIR}/tests/__init__.py', 'w') as f:
        f.write("")
    with open(f'{REPO_DIR}/tests/test_app.py', 'w') as f:
        f.write('''"""Tests for the application module."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.app import Application


def test_application_init():
    app = Application()
    assert app.name == "GitRebaseApp"
    assert app.version == "1.0.0"


def test_register_module():
    app = Application()
    assert app.register_module("auth") is True
    assert app.register_module("auth") is False


def test_get_status():
    app = Application()
    app.register_module("auth")
    status = app.get_status()
    assert status["modules_loaded"] == 1
''')
    with open(f'{REPO_DIR}/tests/test_config.py', 'w') as f:
        f.write('''"""Tests for the configuration module."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config import get_config


def test_get_config():
    config = get_config()
    assert "database" in config
    assert "api_version" in config


def test_database_config():
    config = get_config()
    db = config["database"]
    assert db["host"] == "localhost"
    assert db["port"] == 5432
''')
    run('git add -A')
    run('git commit -m "Add test infrastructure with app and config tests"')

    # Commit 5: Add utility module (feature/base branches from here)
    with open(f'{REPO_DIR}/src/utils.py', 'w') as f:
        f.write('''"""Utility functions for the application."""

import hashlib
import datetime


def generate_id(prefix="item"):
    """Generate a unique ID with timestamp."""
    timestamp = datetime.datetime.now().isoformat()
    hash_val = hashlib.md5(timestamp.encode()).hexdigest()[:8]
    return f"{prefix}_{hash_val}"


def format_timestamp(dt=None):
    """Format a datetime object as a readable string."""
    if dt is None:
        dt = datetime.datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def validate_email(email):
    """Basic email validation."""
    return "@" in email and "." in email.split("@")[-1]
''')
    run('git add -A')
    run('git commit -m "Add utility module with ID generation and validation"')

    commit5_hash = run('git rev-parse HEAD')

    # ========== Continue MAIN: Commits 6-10 ==========

    # Commit 6: Update src/config.py on main (creates conflict with feature/base)
    with open(f'{REPO_DIR}/src/config.py', 'w') as f:
        f.write('''"""Application configuration module."""

# Database settings
DATABASE = {
    "host": "localhost",
    "port": 5432,
    "name": "app_db",
    "pool_size": 10,
    "timeout": 60,
}

# API settings
API_VERSION = "v2"
API_TIMEOUT = 45
API_RATE_LIMIT = 100

# Feature flags
FEATURES = {
    "caching": True,
    "logging": True,
    "debug_mode": False,
    "rate_limiting": True,
    "monitoring": True,
}

# Security settings
SECURITY = {
    "jwt_secret_key": "change-me-in-production",
    "token_expiry": 3600,
    "cors_origins": ["http://localhost:3000"],
}


def get_config():
    """Return the full configuration dictionary."""
    return {
        "database": DATABASE,
        "api_version": API_VERSION,
        "api_timeout": API_TIMEOUT,
        "api_rate_limit": API_RATE_LIMIT,
        "features": FEATURES,
        "security": SECURITY,
    }
''')
    run('git add -A')
    run('git commit -m "Upgrade API to v2, add security settings and rate limiting"')

    # Commit 7: Add authentication module
    with open(f'{REPO_DIR}/src/auth.py', 'w') as f:
        f.write('''"""Authentication module."""


class AuthManager:
    """Handles user authentication."""

    def __init__(self):
        self.sessions = {}

    def login(self, username, password):
        """Authenticate a user and create a session."""
        if username and password:
            session_id = f"session_{username}"
            self.sessions[session_id] = {"user": username, "active": True}
            return session_id
        return None

    def logout(self, session_id):
        """End a user session."""
        if session_id in self.sessions:
            self.sessions[session_id]["active"] = False
            return True
        return False

    def is_authenticated(self, session_id):
        """Check if a session is active."""
        session = self.sessions.get(session_id)
        return session is not None and session.get("active", False)
''')
    run('git add -A')
    run('git commit -m "Add authentication module with session management"')

    # Commit 8: Add logging module
    with open(f'{REPO_DIR}/src/logger.py', 'w') as f:
        f.write('''"""Logging module for the application."""

import logging


def setup_logger(name="app", level=logging.INFO):
    """Configure and return a logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger


app_logger = setup_logger()
''')
    run('git add -A')
    run('git commit -m "Add structured logging module"')

    # Commit 9: Add data models
    with open(f'{REPO_DIR}/src/models.py', 'w') as f:
        f.write('''"""Data models for the application."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class User:
    """User model."""
    username: str
    email: str
    display_name: str
    roles: List[str] = field(default_factory=list)


@dataclass
class Project:
    """Project model."""
    name: str
    description: str
    owner: str
    tags: List[str] = field(default_factory=list)
    active: bool = True
''')
    run('git add -A')
    run('git commit -m "Add data models for users and projects"')

    # Commit 10: Add CLI entry point
    with open(f'{REPO_DIR}/src/cli.py', 'w') as f:
        f.write('''"""Command-line interface for the application."""

import argparse
from src.app import Application


def main():
    parser = argparse.ArgumentParser(description="Git Rebase Practice App")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("--status", action="store_true", help="Show status")
    args = parser.parse_args()

    app = Application()

    if args.version:
        print(f"{app.name} v{app.version}")
    elif args.status:
        print(app.get_status())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
''')
    run('git add -A')
    run('git commit -m "Add CLI entry point with argument parsing"')

    # ========== FEATURE/BASE BRANCH (3 commits) ==========
    run(f'git checkout -b feature/base {commit5_hash}')

    # feature/base commit 1: Add config/base_settings.py
    os.makedirs(f'{REPO_DIR}/config', exist_ok=True)
    with open(f'{REPO_DIR}/config/__init__.py', 'w') as f:
        f.write("")
    with open(f'{REPO_DIR}/config/base_settings.py', 'w') as f:
        f.write('''"""Base settings for modular configuration."""

BASE_SETTINGS = {
    "app_name": "GitRebaseApp",
    "environment": "development",
    "log_level": "INFO",
    "max_retries": 3,
    "retry_delay": 1.5,
}

SERVICE_DEFAULTS = {
    "timeout": 30,
    "max_connections": 50,
    "keep_alive": True,
}


def get_base_settings():
    """Return base configuration settings."""
    return {**BASE_SETTINGS, **SERVICE_DEFAULTS}


def get_setting(key, default=None):
    """Get a specific setting by key."""
    all_settings = get_base_settings()
    return all_settings.get(key, default)
''')
    run('git add -A')
    run('git commit -m "Add base settings module for modular configuration"')

    # feature/base commit 2: Modify src/config.py (creates conflict with main commit 6)
    with open(f'{REPO_DIR}/src/config.py', 'w') as f:
        f.write('''"""Application configuration module."""

from config.base_settings import get_base_settings

# Database settings
DATABASE = {
    "host": "localhost",
    "port": 5432,
    "name": "app_db",
    "connection_pool": 5,
}

# API settings
API_VERSION = "v1"
API_TIMEOUT = 30

# Feature flags
FEATURES = {
    "caching": True,
    "logging": True,
    "debug_mode": False,
    "base_settings_integration": True,
}


def get_config():
    """Return the full configuration dictionary, merged with base settings."""
    base = get_base_settings()
    return {
        "database": DATABASE,
        "api_version": API_VERSION,
        "api_timeout": API_TIMEOUT,
        "features": FEATURES,
        "base_settings": base,
    }
''')
    run('git add -A')
    run('git commit -m "Integrate base settings into config module"')

    # feature/base commit 3: Add config validation
    with open(f'{REPO_DIR}/config/validator.py', 'w') as f:
        f.write('''"""Configuration validation utilities."""

from config.base_settings import get_base_settings

REQUIRED_KEYS = ["app_name", "environment", "log_level"]


def validate_settings():
    """Validate that all required settings are present."""
    settings = get_base_settings()
    missing = [k for k in REQUIRED_KEYS if k not in settings]
    if missing:
        raise ValueError(f"Missing required settings: {missing}")
    return True


def validate_environment(env_name):
    """Check if environment name is valid."""
    valid_envs = ["development", "staging", "production"]
    return env_name in valid_envs
''')
    run('git add -A')
    run('git commit -m "Add configuration validation utilities"')

    # ========== FEATURE/DEPENDENT BRANCH (4 commits) ==========
    # Branches from feature/base tip
    run('git checkout -b feature/dependent')

    # IMPORTANT: feature/dependent commits must be self-contained.
    # D1 also modifies src/config.py to add service config, which creates
    # a conflict during rebase --onto since main commit 6 also modifies config.py.

    # feature/dependent commit 1: Add service module + update config.py
    with open(f'{REPO_DIR}/src/service.py', 'w') as f:
        f.write('''"""Service layer for managing application services."""


# Service defaults (self-contained)
SERVICE_DEFAULTS = {
    "timeout": 30,
    "max_connections": 50,
    "keep_alive": True,
}


class ServiceManager:
    """Manages application services."""

    def __init__(self, settings=None):
        settings = settings or SERVICE_DEFAULTS
        self.timeout = settings.get("timeout", 30)
        self.max_connections = settings.get("max_connections", 50)
        self.services = {}

    def register_service(self, name, endpoint):
        """Register a new service."""
        self.services[name] = {
            "endpoint": endpoint,
            "active": True,
            "timeout": self.timeout,
        }
        return True

    def get_service(self, name):
        """Retrieve a registered service."""
        return self.services.get(name)

    def health_check(self):
        """Check health of all registered services."""
        results = {}
        for name, svc in self.services.items():
            results[name] = {
                "status": "healthy" if svc["active"] else "unhealthy",
                "endpoint": svc["endpoint"],
            }
        return results
''')
    # Also modify src/config.py to add service-related configuration
    # This modification, combined with main's commit 6, creates the rebase conflict
    with open(f'{REPO_DIR}/src/config.py', 'w') as f:
        f.write('''"""Application configuration module."""

from config.base_settings import get_base_settings

# Database settings
DATABASE = {
    "host": "localhost",
    "port": 5432,
    "name": "app_db",
    "connection_pool": 5,
}

# API settings
API_VERSION = "v1"
API_TIMEOUT = 30

# Service registry settings (added for service layer)
SERVICE_REGISTRY = {
    "default_timeout": 30,
    "max_services": 20,
    "health_check_interval": 60,
}

# Feature flags
FEATURES = {
    "caching": True,
    "logging": True,
    "debug_mode": False,
    "base_settings_integration": True,
    "service_registry": True,
}


def get_config():
    """Return the full configuration dictionary, merged with base settings."""
    base = get_base_settings()
    return {
        "database": DATABASE,
        "api_version": API_VERSION,
        "api_timeout": API_TIMEOUT,
        "features": FEATURES,
        "base_settings": base,
        "service_registry": SERVICE_REGISTRY,
    }
''')
    # Update test_config.py for the new config structure
    with open(f'{REPO_DIR}/tests/test_config.py', 'w') as f:
        f.write('''"""Tests for the configuration module."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config import get_config


def test_get_config():
    config = get_config()
    assert "database" in config
    assert "api_version" in config
    assert "service_registry" in config


def test_database_config():
    config = get_config()
    db = config["database"]
    assert db["host"] == "localhost"
    assert db["port"] == 5432


def test_service_registry_config():
    config = get_config()
    sr = config["service_registry"]
    assert sr["default_timeout"] == 30
    assert sr["max_services"] == 20
''')
    run('git add -A')
    run('git commit -m "Add service manager with built-in defaults"')

    # feature/dependent commit 2: Add service tests
    with open(f'{REPO_DIR}/tests/test_service.py', 'w') as f:
        f.write('''"""Tests for the service module."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.service import ServiceManager


def test_service_init():
    sm = ServiceManager()
    assert sm.timeout == 30
    assert sm.max_connections == 50


def test_register_service():
    sm = ServiceManager()
    result = sm.register_service("api", "http://localhost:8000")
    assert result is True
    svc = sm.get_service("api")
    assert svc["endpoint"] == "http://localhost:8000"
    assert svc["active"] is True


def test_health_check():
    sm = ServiceManager()
    sm.register_service("api", "http://localhost:8000")
    sm.register_service("worker", "http://localhost:8001")
    health = sm.health_check()
    assert len(health) == 2
    assert health["api"]["status"] == "healthy"
''')
    run('git add -A')
    run('git commit -m "Add comprehensive service manager tests"')

    # feature/dependent commit 3: Add service configuration and routing
    with open(f'{REPO_DIR}/src/router.py', 'w') as f:
        f.write('''"""Request routing for services."""

from src.service import ServiceManager


class Router:
    """Routes requests to registered services."""

    def __init__(self):
        self.manager = ServiceManager()
        self.routes = {}

    def add_route(self, path, service_name, endpoint):
        """Add a route that maps a path to a service."""
        self.manager.register_service(service_name, endpoint)
        self.routes[path] = service_name
        return True

    def resolve(self, path):
        """Resolve a path to its service configuration."""
        service_name = self.routes.get(path)
        if service_name:
            return self.manager.get_service(service_name)
        return None

    def list_routes(self):
        """List all registered routes."""
        return dict(self.routes)
''')
    run('git add -A')
    run('git commit -m "Add request routing layer for services"')

    # feature/dependent commit 4: Add integration tests
    with open(f'{REPO_DIR}/tests/test_integration.py', 'w') as f:
        f.write('''"""Integration tests for service and routing modules."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.service import ServiceManager
from src.router import Router


def test_service_defaults():
    """Test that ServiceManager uses correct defaults."""
    sm = ServiceManager()
    assert sm.timeout == 30
    assert sm.max_connections == 50


def test_router_add_and_resolve():
    """Test adding routes and resolving them."""
    router = Router()
    router.add_route("/api/users", "user_service", "http://localhost:8000")
    svc = router.resolve("/api/users")
    assert svc is not None
    assert svc["endpoint"] == "http://localhost:8000"


def test_router_unknown_path():
    """Test resolving an unknown path returns None."""
    router = Router()
    assert router.resolve("/unknown") is None


def test_full_workflow():
    """Test complete service registration, routing, and health check."""
    sm = ServiceManager()
    sm.register_service("api", "http://localhost:8000")
    sm.register_service("worker", "http://localhost:8001")

    health = sm.health_check()
    assert all(s["status"] == "healthy" for s in health.values())

    router = Router()
    router.add_route("/api", "api_gateway", "http://localhost:8000")
    router.add_route("/jobs", "job_worker", "http://localhost:8001")
    assert len(router.list_routes()) == 2
''')
    run('git add -A')
    run('git commit -m "Add integration tests for service and routing modules"')

    # Verify we're on feature/dependent
    current_branch = run('git branch --show-current')
    print(f"Current branch: {current_branch}")

    # Verify branch topology
    print("\n=== Branch Topology ===")
    log = run('git log --graph --oneline --all')
    print(log)

    # Verify tests pass on feature/dependent
    print("\n=== Running tests ===")
    test_result = subprocess.run(
        ['bash', '-c', 'python3 -m pytest tests/ -v'],
        cwd=REPO_DIR, capture_output=True, text=True
    )
    print(test_result.stdout)
    if test_result.returncode != 0:
        print(f"STDERR: {test_result.stderr}")
        print("WARNING: Tests did not pass on feature/dependent!")
    else:
        print("All tests passed on feature/dependent.")

    print(f'\nInitial repository created: {REPO_DIR}')

    # GUI-ready startup: open VSCode with the project
    launch_gui(f'code "{REPO_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
