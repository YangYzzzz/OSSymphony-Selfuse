"""
Initial Setup: Git cherry-pick security fixes from main to release/v2.0
Task ID: vscode_gf6_019
Domain: vscode

Creates a git repository ~/projects/git-cherry-pick with:
- main branch: 15 commits, 3 tagged [SECURITY]
- release/v2.0 branch: 8 commits, diverged before security fixes
- config/security.py differs between branches (causes conflict on 2nd cherry-pick)
- CHANGELOG.md exists on release/v2.0
- VSCode opened with the project folder
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_019'
PROJECT_DIR = f'{WORKDIR}/projects/git-cherry-pick'


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


def run_git(cmd, cwd=PROJECT_DIR):
    """Run a git command in the project directory."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd, capture_output=True, text=True,
        env={**os.environ, 'GIT_AUTHOR_NAME': 'Developer',
             'GIT_AUTHOR_EMAIL': 'dev@example.com',
             'GIT_COMMITTER_NAME': 'Developer',
             'GIT_COMMITTER_EMAIL': 'dev@example.com'}
    )
    if result.returncode != 0:
        print(f"CMD FAILED: {cmd}")
        print(f"STDERR: {result.stderr}")
    return result


def write_file(path, content):
    """Write content to a file, creating directories as needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


def create_initial():
    # Clean up any existing repo
    if os.path.exists(PROJECT_DIR):
        import shutil
        shutil.rmtree(PROJECT_DIR)

    os.makedirs(PROJECT_DIR, exist_ok=True)
    run_git('git init -b main')
    run_git('git config user.name "Developer"')
    run_git('git config user.email "dev@example.com"')

    # ==========================================
    # Build shared history (commits 1-8, on main)
    # These will be common to both main and release/v2.0
    # ==========================================

    # Commit 1: Initial project structure
    write_file(f'{PROJECT_DIR}/README.md', """# SecureApp v2.0

A secure web application framework with built-in authentication,
authorization, and audit logging capabilities.

## Quick Start

```bash
pip install -r requirements.txt
python manage.py runserver
```

## Documentation
See docs/ directory for full documentation.
""")
    write_file(f'{PROJECT_DIR}/requirements.txt', """flask==3.0.2
sqlalchemy==2.0.25
bcrypt==4.1.2
pyjwt==2.8.0
redis==5.0.1
celery==5.3.6
pytest==8.0.0
""")
    write_file(f'{PROJECT_DIR}/manage.py', """#!/usr/bin/env python3
\"\"\"Application management script.\"\"\"
import sys
from app import create_app

def main():
    app = create_app()
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        app.run(host='0.0.0.0', port=8080, debug=True)
    elif len(sys.argv) > 1 and sys.argv[1] == 'test':
        import pytest
        sys.exit(pytest.main(['-v', 'tests/']))
    else:
        print("Usage: manage.py [runserver|test]")

if __name__ == '__main__':
    main()
""")
    run_git('git add -A && git commit -m "Initial project structure with README and requirements"')

    # Commit 2: App module
    write_file(f'{PROJECT_DIR}/app/__init__.py', """from flask import Flask

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    return app
""")
    write_file(f'{PROJECT_DIR}/app/models.py', """from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    action = Column(String(200), nullable=False)
    resource = Column(String(200))
    ip_address = Column(String(45))
    timestamp = Column(DateTime, default=datetime.utcnow)
""")
    run_git('git add -A && git commit -m "Add core app module with User and AuditLog models"')

    # Commit 3: Authentication module
    write_file(f'{PROJECT_DIR}/app/auth.py', """import hashlib
import hmac
from datetime import datetime, timedelta

SECRET_KEY = 'change-me-in-production'

def hash_password(password):
    \"\"\"Hash password using SHA-256 (legacy method).\"\"\"
    salt = 'static-salt-v1'
    return hashlib.sha256(f'{salt}{password}'.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

def generate_token(user_id):
    payload = f'{user_id}:{datetime.utcnow().isoformat()}'
    signature = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f'{payload}:{signature}'
""")
    run_git('git add -A && git commit -m "Add authentication module with password hashing and token generation"')

    # Commit 4: Database queries
    write_file(f'{PROJECT_DIR}/app/queries.py', """from app.models import User, AuditLog

def get_user_by_username(session, username):
    \"\"\"Fetch user by username using string interpolation (legacy).\"\"\"
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return session.execute(query).fetchone()

def get_user_by_email(session, email):
    query = f"SELECT * FROM users WHERE email = '{email}'"
    return session.execute(query).fetchone()

def search_users(session, search_term):
    query = f"SELECT * FROM users WHERE username LIKE '%{search_term}%' OR email LIKE '%{search_term}%'"
    return session.execute(query).fetchall()

def get_audit_logs(session, user_id=None, limit=100):
    if user_id:
        query = f"SELECT * FROM audit_logs WHERE user_id = {user_id} ORDER BY timestamp DESC LIMIT {limit}"
    else:
        query = f"SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT {limit}"
    return session.execute(query).fetchall()
""")
    run_git('git add -A && git commit -m "Add database query functions for user and audit log retrieval"')

    # Commit 5: Config module (this is the file that will conflict)
    write_file(f'{PROJECT_DIR}/config/__init__.py', "")
    write_file(f'{PROJECT_DIR}/config/security.py', """\"\"\"Security configuration for SecureApp.\"\"\"

# Authentication settings
AUTH_TOKEN_EXPIRY = 3600  # 1 hour
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 900  # 15 minutes

# Password policy
MIN_PASSWORD_LENGTH = 8
REQUIRE_UPPERCASE = True
REQUIRE_NUMBERS = True
REQUIRE_SPECIAL_CHARS = False

# Session settings
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# HTTP settings
FORCE_HTTPS = False
HSTS_ENABLED = False
HSTS_MAX_AGE = 0

# CORS settings
CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:8080']
CORS_ALLOW_CREDENTIALS = True

# Rate limiting
RATE_LIMIT_ENABLED = True
RATE_LIMIT_DEFAULT = '100/hour'
RATE_LIMIT_LOGIN = '10/minute'
""")
    run_git('git add -A && git commit -m "Add security configuration module"')

    # Commit 6: API routes
    write_file(f'{PROJECT_DIR}/app/routes.py', """from flask import Blueprint, request, jsonify
from app.auth import hash_password, verify_password, generate_token
from app.queries import get_user_by_username, search_users

api = Blueprint('api', __name__)

@api.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # TODO: implement proper login logic
    return jsonify({'status': 'not implemented'}), 501

@api.route('/api/users/search', methods=['GET'])
def user_search():
    term = request.args.get('q', '')
    # TODO: implement search
    return jsonify({'results': []})

@api.route('/api/profile', methods=['GET'])
def profile():
    # TODO: implement profile endpoint
    return jsonify({'status': 'not implemented'}), 501
""")
    run_git('git add -A && git commit -m "Add API route blueprints for login, search, and profile"')

    # Commit 7: Tests
    write_file(f'{PROJECT_DIR}/tests/__init__.py', "")
    write_file(f'{PROJECT_DIR}/tests/test_auth.py', """import pytest
from app.auth import hash_password, verify_password

def test_hash_password():
    hashed = hash_password('testpass123')
    assert isinstance(hashed, str)
    assert len(hashed) == 64  # SHA-256 hex digest

def test_verify_password():
    hashed = hash_password('mypassword')
    assert verify_password('mypassword', hashed)
    assert not verify_password('wrongpass', hashed)

def test_different_passwords_different_hashes():
    h1 = hash_password('password1')
    h2 = hash_password('password2')
    assert h1 != h2
""")
    run_git('git add -A && git commit -m "Add unit tests for authentication module"')

    # Commit 8: CHANGELOG
    write_file(f'{PROJECT_DIR}/CHANGELOG.md', """# Changelog

All notable changes to SecureApp will be documented in this file.

## [2.0.0] - 2025-03-01

### Added
- Core application framework with Flask
- User and AuditLog database models
- Authentication module with password hashing
- Database query functions
- Security configuration module
- API route blueprints
- Unit tests for auth module

### Changed
- Migrated from Django to Flask framework
- Updated SQLAlchemy to 2.x API

## [1.0.0] - 2024-11-15

### Added
- Initial release with basic user management
- Simple authentication system
- Admin dashboard
""")
    run_git('git add -A && git commit -m "Add CHANGELOG with v2.0.0 release notes"')

    # ==========================================
    # Create release/v2.0 branch from here
    # ==========================================
    run_git('git checkout -b release/v2.0')

    # Modify config/security.py on release/v2.0 to create future conflict
    # This version enables HTTPS but with different formatting/structure
    write_file(f'{PROJECT_DIR}/config/security.py', """\"\"\"Security configuration for SecureApp.\"\"\"

# Authentication settings
AUTH_TOKEN_EXPIRY = 3600  # 1 hour
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 900  # 15 minutes

# Password policy
MIN_PASSWORD_LENGTH = 8
REQUIRE_UPPERCASE = True
REQUIRE_NUMBERS = True
REQUIRE_SPECIAL_CHARS = False

# Session settings
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'

# HTTP settings - release hardening
FORCE_HTTPS = True
HSTS_ENABLED = True
HSTS_MAX_AGE = 31536000  # 1 year

# CORS settings - production only
CORS_ORIGINS = ['https://secureapp.example.com']
CORS_ALLOW_CREDENTIALS = True

# Rate limiting
RATE_LIMIT_ENABLED = True
RATE_LIMIT_DEFAULT = '60/hour'
RATE_LIMIT_LOGIN = '5/minute'

# Content Security Policy
CSP_ENABLED = True
CSP_DEFAULT_SRC = "'self'"
CSP_SCRIPT_SRC = "'self' 'nonce'"
""")
    run_git('git add -A && git commit -m "Harden security config for release: enable HTTPS, strict cookies, CSP"')

    run_git('git checkout main')

    # ==========================================
    # Continue building main branch (commits 9-15)
    # Commits 10, 12, 14 are the [SECURITY] commits
    # ==========================================

    # Commit 9: Logging improvements
    write_file(f'{PROJECT_DIR}/app/logging_config.py', """import logging
import sys

def setup_logging(level=logging.INFO):
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger = logging.getLogger('secureapp')
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger
""")
    run_git('git add -A && git commit -m "Add structured logging configuration"')

    # Commit 10: [SECURITY] Fix password hashing - use bcrypt
    write_file(f'{PROJECT_DIR}/app/auth.py', """import bcrypt
import hmac
import hashlib
from datetime import datetime, timedelta

SECRET_KEY = 'change-me-in-production'

def hash_password(password):
    \"\"\"Hash password using bcrypt with automatic salt generation.\"\"\"
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    \"\"\"Verify password against bcrypt hash.\"\"\"
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def generate_token(user_id):
    payload = f'{user_id}:{datetime.utcnow().isoformat()}'
    signature = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f'{payload}:{signature}'
""")
    run_git('git add -A && git commit -m "[SECURITY] Update password hashing to bcrypt"')

    # Commit 11: Add caching layer
    write_file(f'{PROJECT_DIR}/app/cache.py', """import redis
import json

_redis_client = None

def get_redis():
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.Redis(host='localhost', port=6379, db=0)
    return _redis_client

def cache_get(key):
    val = get_redis().get(key)
    return json.loads(val) if val else None

def cache_set(key, value, ttl=300):
    get_redis().setex(key, ttl, json.dumps(value))

def cache_delete(key):
    get_redis().delete(key)
""")
    run_git('git add -A && git commit -m "Add Redis caching layer for session and query results"')

    # Commit 12: [SECURITY] Fix SQL injection in user query
    # Also modify config/security.py on main to create conflict
    write_file(f'{PROJECT_DIR}/app/queries.py', """from sqlalchemy import text
from app.models import User, AuditLog

def get_user_by_username(session, username):
    \"\"\"Fetch user by username using parameterized query.\"\"\"
    query = text("SELECT * FROM users WHERE username = :username")
    return session.execute(query, {'username': username}).fetchone()

def get_user_by_email(session, email):
    query = text("SELECT * FROM users WHERE email = :email")
    return session.execute(query, {'email': email}).fetchone()

def search_users(session, search_term):
    query = text("SELECT * FROM users WHERE username LIKE :term OR email LIKE :term")
    return session.execute(query, {'term': f'%{search_term}%'}).fetchall()

def get_audit_logs(session, user_id=None, limit=100):
    if user_id:
        query = text("SELECT * FROM audit_logs WHERE user_id = :uid ORDER BY timestamp DESC LIMIT :lim")
        return session.execute(query, {'uid': user_id, 'lim': limit}).fetchall()
    else:
        query = text("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT :lim")
        return session.execute(query, {'lim': limit}).fetchall()
""")
    # Also update config/security.py on main - different changes that will conflict with release/v2.0
    write_file(f'{PROJECT_DIR}/config/security.py', """\"\"\"Security configuration for SecureApp.\"\"\"

# Authentication settings
AUTH_TOKEN_EXPIRY = 3600  # 1 hour
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 900  # 15 minutes

# Password policy
MIN_PASSWORD_LENGTH = 8
REQUIRE_UPPERCASE = True
REQUIRE_NUMBERS = True
REQUIRE_SPECIAL_CHARS = False

# Session settings
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# HTTP settings
FORCE_HTTPS = False
HSTS_ENABLED = False
HSTS_MAX_AGE = 0

# CORS settings
CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:8080']
CORS_ALLOW_CREDENTIALS = True

# Rate limiting
RATE_LIMIT_ENABLED = True
RATE_LIMIT_DEFAULT = '100/hour'
RATE_LIMIT_LOGIN = '10/minute'

# SQL Injection Protection
PARAMETERIZED_QUERIES_ONLY = True
SQL_LOGGING_ENABLED = True
""")
    run_git('git add -A && git commit -m "[SECURITY] Fix SQL injection in user query"')

    # Commit 13: Add middleware
    write_file(f'{PROJECT_DIR}/app/middleware.py', """from functools import wraps
from flask import request, jsonify, g
from app.auth import verify_password, generate_token

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'Authentication required'}), 401
        # TODO: validate token properly
        g.current_user_id = None
        return f(*args, **kwargs)
    return decorated

def require_role(role):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not hasattr(g, 'current_user_id') or g.current_user_id is None:
                return jsonify({'error': 'Unauthorized'}), 403
            # TODO: check user role
            return f(*args, **kwargs)
        return decorated
    return decorator
""")
    run_git('git add -A && git commit -m "Add authentication and role-based middleware"')

    # Commit 14: [SECURITY] Enforce HTTPS redirect
    write_file(f'{PROJECT_DIR}/app/https_redirect.py', """from flask import request, redirect

def enforce_https(app):
    \"\"\"Middleware to enforce HTTPS redirect on all requests.\"\"\"
    @app.before_request
    def redirect_to_https():
        if not request.is_secure and request.headers.get('X-Forwarded-Proto', 'http') != 'https':
            url = request.url.replace('http://', 'https://', 1)
            return redirect(url, code=301)

    @app.after_request
    def add_security_headers(response):
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response
""")
    run_git('git add -A && git commit -m "[SECURITY] Enforce HTTPS redirect"')

    # Commit 15: Documentation updates
    write_file(f'{PROJECT_DIR}/docs/deployment.md', """# Deployment Guide

## Prerequisites
- Python 3.10+
- PostgreSQL 15+
- Redis 7+

## Steps
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables
4. Run migrations: `python manage.py migrate`
5. Start the server: `python manage.py runserver`

## Environment Variables
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `SECRET_KEY` - Application secret key
- `FORCE_HTTPS` - Set to 'true' in production
""")
    run_git('git add -A && git commit -m "Add deployment documentation"')

    print(f'Repository created at: {PROJECT_DIR}')

    # Verify the setup
    result = run_git('git log --oneline')
    print(f"\nmain branch commits:\n{result.stdout}")

    result = run_git('git log release/v2.0 --oneline')
    print(f"release/v2.0 commits:\n{result.stdout}")

    result = run_git('git log main --oneline --grep="\\[SECURITY\\]"')
    print(f"Security commits on main:\n{result.stdout}")

    # GUI-ready startup: open VSCode with the project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
