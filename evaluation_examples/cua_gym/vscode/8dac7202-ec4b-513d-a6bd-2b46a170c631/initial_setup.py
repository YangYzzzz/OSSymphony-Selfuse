"""
Initial Setup: Stage only hunk covering lines 10-25 of api_handler.py in git diff
Task ID: vscode_git_023
Domain: vs_code (VSCode + Git)

Creates a git repository at /home/user/backend with api_handler.py modified
in three distinct hunks — all changes are unstaged (working tree only).
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_023'
REPO_DIR = f'{WORKDIR}/backend'

def run(cmd, cwd=None, check=True):
    """Run a shell command locally (on the VM)."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd,
        capture_output=True, text=True
    )
    if check and result.returncode != 0:
        raise RuntimeError(f'Command failed: {cmd}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}')
    return result.stdout.strip()


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


# --- Committed (original) content of api_handler.py ---
# This is the file as it exists in git history (before any modifications)
ORIGINAL_CONTENT = '''\
"""
API Handler Module
==================
Handles routing and processing for the REST API.
"""
import flask
from flask import request, jsonify

app = flask.Flask(__name__)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"})


def handle_request(data):
    """Process incoming API request data."""
    if not data:
        return None
    return {"processed": True, "data": data}


def validate_request(req):
    """Validate the API request structure."""
    required_fields = ["method", "path", "body"]
    for field in required_fields:
        if field not in req:
            raise ValueError(f"Missing required field: {field}")
    return True


def parse_params(raw_params):
    """Parse URL query parameters into a dict."""
    if not raw_params:
        return {}
    params = {}
    for pair in raw_params.split("&"):
        if "=" in pair:
            key, value = pair.split("=", 1)
            params[key.strip()] = value.strip()
    return params


def log_request(req_id, method, path, status_code):
    """Write request details to application log."""
    import logging
    logger = logging.getLogger("api_handler")
    logger.info(f"[{req_id}] {method} {path} -> {status_code}")


def build_response(status_code, body, headers=None):
    """Construct a standardized API response dict."""
    response = {
        "status_code": status_code,
        "body": body,
        "headers": headers or {"Content-Type": "application/json"},
    }
    return response


def get_client_ip(request_obj):
    """Extract the real client IP, respecting proxy headers."""
    forwarded_for = request_obj.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request_obj.remote_addr


def authenticate(token):
    """Validate Bearer token and return user identity or None."""
    # Placeholder: real auth would call identity service
    if token and token.startswith("Bearer "):
        return {"user": "api_user", "role": "read"}
    return None


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)
'''

# --- Modified (working tree) content of api_handler.py ---
# Three hunks of changes relative to ORIGINAL_CONTENT:
#
#  Hunk 1 (lines 10-25): new /users endpoint added after health_check
#  Hunk 2 (lines 45-50): refactored error handling in validate_request
#  Hunk 3 (lines 80-90): updated imports section inside authenticate()
MODIFIED_CONTENT = '''\
"""
API Handler Module
==================
Handles routing and processing for the REST API.
"""
import flask
from flask import request, jsonify

app = flask.Flask(__name__)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"})


# New: Users endpoint (v2 API)
@app.route('/api/v2/users', methods=['GET'])
def list_users():
    """Return paginated list of active users."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    # TODO: query database
    return jsonify({"users": [], "page": page, "per_page": per_page})


def handle_request(data):
    """Process incoming API request data."""
    if not data:
        return None
    return {"processed": True, "data": data}


def validate_request(req):
    """Validate the API request structure."""
    required_fields = ["method", "path", "body"]
    missing = [f for f in required_fields if f not in req]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
    return True


def parse_params(raw_params):
    """Parse URL query parameters into a dict."""
    if not raw_params:
        return {}
    params = {}
    for pair in raw_params.split("&"):
        if "=" in pair:
            key, value = pair.split("=", 1)
            params[key.strip()] = value.strip()
    return params


def log_request(req_id, method, path, status_code):
    """Write request details to application log."""
    import logging
    logger = logging.getLogger("api_handler")
    logger.info(f"[{req_id}] {method} {path} -> {status_code}")


def build_response(status_code, body, headers=None):
    """Construct a standardized API response dict."""
    response = {
        "status_code": status_code,
        "body": body,
        "headers": headers or {"Content-Type": "application/json"},
    }
    return response


def get_client_ip(request_obj):
    """Extract the real client IP, respecting proxy headers."""
    forwarded_for = request_obj.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request_obj.remote_addr


def authenticate(token):
    """Validate Bearer token and return user identity or None."""
    import hashlib
    import hmac
    import base64
    # Updated: use HMAC-based token verification
    if token and token.startswith("Bearer "):
        raw = token[7:]
        decoded = base64.b64decode(raw + "==").decode("utf-8", errors="ignore")
        return {"user": decoded.split(":")[0], "role": "read"}
    return None


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)
'''


def create_initial():
    # 1. Create repo directory
    os.makedirs(REPO_DIR, exist_ok=True)

    # 2. Initialize git repo with user config
    run('git init', cwd=REPO_DIR)
    run('git config user.email "dev@example.com"', cwd=REPO_DIR)
    run('git config user.name "Dev User"', cwd=REPO_DIR)

    # 3. Add other realistic project files
    files = {
        'requirements.txt': (
            'flask==3.0.3\n'
            'gunicorn==22.0.0\n'
            'python-dotenv==1.0.1\n'
            'requests==2.32.3\n'
        ),
        'README.md': (
            '# Backend API\n\n'
            'REST API service for the application backend.\n\n'
            '## Setup\n\n'
            '```bash\n'
            'pip install -r requirements.txt\n'
            'python api_handler.py\n'
            '```\n\n'
            '## Endpoints\n\n'
            '- `GET /health` — Health check\n'
        ),
        'config.py': (
            '"""Application configuration."""\n'
            'import os\n\n'
            'DEBUG = os.getenv("DEBUG", "false").lower() == "true"\n'
            'HOST = os.getenv("HOST", "0.0.0.0")\n'
            'PORT = int(os.getenv("PORT", "8080"))\n'
            'SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")\n'
        ),
        'tests/test_api.py': (
            '"""Unit tests for api_handler."""\n'
            'import pytest\n'
            'import sys\n'
            'import os\n'
            'sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))\n'
            'from api_handler import handle_request, validate_request, parse_params\n\n'
            'def test_handle_request_empty():\n'
            '    assert handle_request(None) is None\n\n'
            'def test_handle_request_data():\n'
            '    result = handle_request({"key": "val"})\n'
            '    assert result["processed"] is True\n\n'
            'def test_parse_params_empty():\n'
            '    assert parse_params("") == {}\n\n'
            'def test_parse_params_single():\n'
            '    assert parse_params("foo=bar") == {"foo": "bar"}\n'
        ),
    }

    for rel_path, content in files.items():
        full_path = os.path.join(REPO_DIR, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)

    # 4. Write the ORIGINAL (committed) version of api_handler.py
    api_path = os.path.join(REPO_DIR, 'api_handler.py')
    with open(api_path, 'w') as f:
        f.write(ORIGINAL_CONTENT)

    # 5. Stage and commit everything (this is the "before" state)
    run('git add .', cwd=REPO_DIR)
    run('git commit -m "Initial commit: add API handler and project structure"', cwd=REPO_DIR)

    # 6. Now overwrite api_handler.py with MODIFIED content (3 hunks of changes)
    #    Do NOT stage — all changes stay in working tree only
    with open(api_path, 'w') as f:
        f.write(MODIFIED_CONTENT)

    # 7. Verify the working tree has unstaged changes in 3 hunks
    diff_out = run('git diff api_handler.py', cwd=REPO_DIR)
    print('--- git diff preview (truncated) ---')
    print(diff_out[:500])
    print('...')

    status_out = run('git status', cwd=REPO_DIR)
    print('--- git status ---')
    print(status_out)

    print(f'Initial repository created at: {REPO_DIR}')
    print('api_handler.py has 3 unstaged hunks:')
    print('  Hunk 1: lines ~10-25 (new /api/v2/users endpoint)')
    print('  Hunk 2: lines ~34-39 (refactored validate_request error handling)')
    print('  Hunk 3: lines ~76-88 (updated authenticate() with HMAC imports)')

    # 8. GUI-ready startup: open VSCode with the repository folder
    launch_gui(f'code "{REPO_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0 pointing at /home/user/backend')


create_initial()
