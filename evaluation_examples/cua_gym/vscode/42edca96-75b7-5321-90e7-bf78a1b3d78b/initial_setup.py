"""
Initial Setup: Force push after rebase scenario
Task ID: vscode_gs_044
Domain: vscode

Creates a git repo ~/projects/webapp/ with a bare remote origin at ~/projects/webapp.git.
The local 'feature/rewrite' branch has been rebased (3 new commits), while
origin/feature/rewrite still has the old (pre-rebase) commits. A normal push fails.
VSCode is opened with the project folder.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gs_044'
PROJECT_DIR = f'{WORKDIR}/projects/webapp'
BARE_REMOTE = f'{WORKDIR}/projects/webapp.git'


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


def run(cmd, cwd=None, check=True):
    """Run a shell command."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd,
        capture_output=True, text=True
    )
    if check and result.returncode != 0:
        print(f"CMD FAILED: {cmd}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        raise RuntimeError(f"Command failed: {cmd}")
    return result


def create_initial():
    # Clean up any existing dirs
    subprocess.run(f"rm -rf {PROJECT_DIR} {BARE_REMOTE}", shell=True)
    os.makedirs(f'{WORKDIR}/projects', exist_ok=True)

    # --- Step 1: Create the bare remote repo ---
    os.makedirs(BARE_REMOTE, exist_ok=True)
    run(f"git init --bare {BARE_REMOTE}")

    # --- Step 2: Create the working repo ---
    run(f"git init {PROJECT_DIR}")
    run("git config user.email 'dev@webapp.io'", cwd=PROJECT_DIR)
    run("git config user.name 'Alex Rivera'", cwd=PROJECT_DIR)
    run(f"git remote add origin {BARE_REMOTE}", cwd=PROJECT_DIR)

    # --- Step 3: Create main branch with initial content ---
    # Commit 1: Initial project structure
    os.makedirs(f'{PROJECT_DIR}/src', exist_ok=True)
    os.makedirs(f'{PROJECT_DIR}/tests', exist_ok=True)

    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write("""# WebApp - Customer Portal

A modern customer portal built with Flask and React.

## Getting Started

```bash
pip install -r requirements.txt
python src/app.py
```

## Architecture

- `src/app.py` - Main Flask application
- `src/models.py` - SQLAlchemy models
- `src/routes/` - API route handlers
- `tests/` - Test suite
""")

    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write("""flask==3.0.2
sqlalchemy==2.0.25
flask-cors==4.0.0
pytest==8.0.0
gunicorn==21.2.0
redis==5.0.1
""")

    with open(f'{PROJECT_DIR}/src/app.py', 'w') as f:
        f.write("""from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/api/customers')
def get_customers():
    # TODO: implement customer listing
    return jsonify({"customers": []})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
""")

    with open(f'{PROJECT_DIR}/src/models.py', 'w') as f:
        f.write("""from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    total = Column(Integer, default=0)
    status = Column(String(20), default='pending')
""")

    with open(f'{PROJECT_DIR}/tests/test_app.py', 'w') as f:
        f.write("""import pytest

def test_health_endpoint():
    # TODO: implement
    pass

def test_customer_listing():
    # TODO: implement
    pass
""")

    with open(f'{PROJECT_DIR}/.gitignore', 'w') as f:
        f.write("""__pycache__/
*.pyc
.env
venv/
*.db
.vscode/
""")

    run("git add -A", cwd=PROJECT_DIR)
    run('git commit -m "Initial project setup with Flask backend"', cwd=PROJECT_DIR)

    # Commit 2: Add configuration
    with open(f'{PROJECT_DIR}/config.py', 'w') as f:
        f.write("""import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass
""")

    run("git add -A", cwd=PROJECT_DIR)
    run('git commit -m "Add application configuration module"', cwd=PROJECT_DIR)

    # Push main to origin
    run("git push origin main", cwd=PROJECT_DIR, check=False)
    # In case default branch name is 'master', handle both
    result = run("git branch --show-current", cwd=PROJECT_DIR)
    main_branch = result.stdout.strip()
    if main_branch != 'main':
        run(f"git branch -m {main_branch} main", cwd=PROJECT_DIR)
    run("git push -u origin main", cwd=PROJECT_DIR)

    # --- Step 4: Create feature/rewrite branch with OLD commits (pre-rebase) ---
    run("git checkout -b feature/rewrite", cwd=PROJECT_DIR)

    # Old commit 1: Refactor models (pre-rebase version)
    with open(f'{PROJECT_DIR}/src/models.py', 'w') as f:
        f.write("""from sqlalchemy import Column, Integer, String, DateTime, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True)
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    total = Column(Float, default=0.0)
    status = Column(String(20), default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
""")

    run("git add -A", cwd=PROJECT_DIR)
    run('git commit -m "Refactor models with additional fields"', cwd=PROJECT_DIR)

    # Old commit 2: Add routes
    os.makedirs(f'{PROJECT_DIR}/src/routes', exist_ok=True)
    with open(f'{PROJECT_DIR}/src/routes/__init__.py', 'w') as f:
        f.write("")

    with open(f'{PROJECT_DIR}/src/routes/customers.py', 'w') as f:
        f.write("""from flask import Blueprint, jsonify, request

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/api/customers', methods=['GET'])
def list_customers():
    return jsonify({"customers": [], "total": 0})

@customers_bp.route('/api/customers/<int:cid>', methods=['GET'])
def get_customer(cid):
    return jsonify({"error": "not found"}), 404
""")

    run("git add -A", cwd=PROJECT_DIR)
    run('git commit -m "Add customer API routes"', cwd=PROJECT_DIR)

    # Old commit 3: Update tests
    with open(f'{PROJECT_DIR}/tests/test_app.py', 'w') as f:
        f.write("""import pytest
from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'

def test_customer_listing(client):
    response = client.get('/api/customers')
    assert response.status_code == 200
    assert 'customers' in response.json
""")

    run("git add -A", cwd=PROJECT_DIR)
    run('git commit -m "Update test suite with proper fixtures"', cwd=PROJECT_DIR)

    # Push old feature/rewrite to origin
    run("git push -u origin feature/rewrite", cwd=PROJECT_DIR)

    # Save the old commit hashes for reference
    old_log = run("git log --oneline -3", cwd=PROJECT_DIR)
    print(f"Old (pre-rebase) commits on origin:\n{old_log.stdout}")

    # --- Step 5: Simulate rebase ---
    # First, add a new commit on main that we'll "rebase onto"
    run("git checkout main", cwd=PROJECT_DIR)

    with open(f'{PROJECT_DIR}/src/utils.py', 'w') as f:
        f.write("""import logging

logger = logging.getLogger(__name__)

def setup_logging(level='INFO'):
    logging.basicConfig(
        level=getattr(logging, level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logger
""")

    run("git add -A", cwd=PROJECT_DIR)
    run('git commit -m "Add logging utility module"', cwd=PROJECT_DIR)
    run("git push origin main", cwd=PROJECT_DIR)

    # Now rebase feature/rewrite onto updated main
    # This will replay the 3 feature commits on top of the new main tip
    run("git checkout feature/rewrite", cwd=PROJECT_DIR)
    run("git rebase main", cwd=PROJECT_DIR)

    new_log = run("git log --oneline -5", cwd=PROJECT_DIR)
    print(f"New (post-rebase) local commits:\n{new_log.stdout}")

    # Verify push would fail
    push_result = run("git push origin feature/rewrite", cwd=PROJECT_DIR, check=False)
    print(f"Normal push result (should fail): returncode={push_result.returncode}")
    print(f"Push stderr: {push_result.stderr}")

    # --- Step 6: Verify the divergence state ---
    status = run("git status", cwd=PROJECT_DIR)
    print(f"Git status:\n{status.stdout}")

    print(f'Initial setup complete: {PROJECT_DIR}')

    # --- Step 7: Launch VSCode with the project ---
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
