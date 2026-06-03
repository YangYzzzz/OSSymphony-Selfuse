"""
Initial Setup: Stash changes, apply to different branch, resolve conflicts
Task ID: vscode_git_068
Domain: vs_code (git operations)

Creates a git repo at /home/user/project on branch 'feature/api' with:
  - routes.py: modified (will apply cleanly to develop)
  - middleware.py: modified (will conflict with develop's middleware structure)
  - 'develop' branch exists with diverged middleware structure
  - No stash (agent must perform the stash)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_068'
PROJECT_DIR = f'{WORKDIR}/project'


def run_cmd(cmd, cwd=None, env=None):
    """Run a shell command and return stdout."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    if result.returncode != 0:
        print(f'CMD: {cmd}')
        print(f'STDOUT: {result.stdout}')
        print(f'STDERR: {result.stderr}')
    return result


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
    # Remove existing project if present
    run_cmd(f'rm -rf "{PROJECT_DIR}"')

    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Initialize git repo
    git_env = os.environ.copy()
    git_env['GIT_AUTHOR_NAME'] = 'Dev User'
    git_env['GIT_AUTHOR_EMAIL'] = 'dev@example.com'
    git_env['GIT_COMMITTER_NAME'] = 'Dev User'
    git_env['GIT_COMMITTER_EMAIL'] = 'dev@example.com'

    run_cmd('git init', cwd=PROJECT_DIR, env=git_env)
    run_cmd('git config user.email "dev@example.com"', cwd=PROJECT_DIR, env=git_env)
    run_cmd('git config user.name "Dev User"', cwd=PROJECT_DIR, env=git_env)

    # ----------------------------------------------------------------
    # Create the base commit on main (shared ancestry for both branches)
    # ----------------------------------------------------------------

    # Base routes.py (original, before feature/api changes)
    routes_base = '''\
"""
API Routes for the web application.
"""
from flask import Flask, jsonify, request
from middleware import authenticate, rate_limit

app = Flask(__name__)


@app.route('/api/users', methods=['GET'])
def get_users():
    """Return list of users."""
    users = [
        {'id': 1, 'name': 'Alice Smith', 'role': 'admin'},
        {'id': 2, 'name': 'Bob Johnson', 'role': 'user'},
        {'id': 3, 'name': 'Carol Williams', 'role': 'user'},
    ]
    return jsonify(users)


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Return a single user by ID."""
    return jsonify({'id': user_id, 'name': 'Alice Smith', 'role': 'admin'})


@app.route('/api/products', methods=['GET'])
def get_products():
    """Return list of products."""
    products = [
        {'id': 101, 'name': 'Widget A', 'price': 29.99},
        {'id': 102, 'name': 'Widget B', 'price': 49.99},
    ]
    return jsonify(products)


if __name__ == '__main__':
    app.run(debug=True)
'''

    # Base middleware.py (original, before either branch diverged)
    middleware_base = '''\
"""
Middleware functions for the web application.
"""
import functools
from flask import request, jsonify


def authenticate(f):
    """Basic authentication middleware."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated


def rate_limit(f):
    """Basic rate limiting middleware."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        # Simple passthrough for now
        return f(*args, **kwargs)
    return decorated
'''

    # app.py base
    app_base = '''\
"""
Main application entry point.
"""
from routes import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
'''

    # requirements.txt
    requirements = 'Flask>=2.0.0\nrequests>=2.28.0\n'

    # Write base files
    with open(os.path.join(PROJECT_DIR, 'routes.py'), 'w') as f:
        f.write(routes_base)
    with open(os.path.join(PROJECT_DIR, 'middleware.py'), 'w') as f:
        f.write(middleware_base)
    with open(os.path.join(PROJECT_DIR, 'app.py'), 'w') as f:
        f.write(app_base)
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write(requirements)

    # Initial commit on main
    run_cmd('git add -A', cwd=PROJECT_DIR, env=git_env)
    run_cmd('git commit -m "Initial project setup with Flask API"', cwd=PROJECT_DIR, env=git_env)

    # ----------------------------------------------------------------
    # Create 'develop' branch with diverged middleware structure
    # ----------------------------------------------------------------
    run_cmd('git checkout -b develop', cwd=PROJECT_DIR, env=git_env)

    # develop has a significantly different middleware.py (class-based pattern)
    middleware_develop = '''\
"""
Middleware module for develop branch.
Uses a class-based middleware pattern with centralized configuration.
"""
import functools
import time
import logging
from flask import request, jsonify, g

logger = logging.getLogger(__name__)


class MiddlewareStack:
    """Central registry for all middleware components."""

    def __init__(self):
        self._handlers = []

    def register(self, handler):
        self._handlers.append(handler)
        return handler

    def apply(self, f):
        """Apply all registered middleware to a route handler."""
        for handler in reversed(self._handlers):
            f = handler(f)
        return f


_stack = MiddlewareStack()


def authenticate(f):
    """JWT-based authentication middleware for develop branch."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Unauthorized', 'code': 'NO_TOKEN'}), 401
        token = auth_header.split(' ', 1)[1]
        # Validate JWT token structure
        parts = token.split('.')
        if len(parts) != 3:
            return jsonify({'error': 'Invalid token format', 'code': 'BAD_TOKEN'}), 401
        g.current_user = {'token': token}
        return f(*args, **kwargs)
    return decorated


def rate_limit(f):
    """Token-bucket rate limiter for develop branch."""
    _bucket = {'tokens': 100, 'last_refill': time.time()}

    @functools.wraps(f)
    def decorated(*args, **kwargs):
        now = time.time()
        elapsed = now - _bucket['last_refill']
        # Refill at 10 tokens/second
        _bucket['tokens'] = min(100, _bucket['tokens'] + elapsed * 10)
        _bucket['last_refill'] = now
        if _bucket['tokens'] < 1:
            return jsonify({'error': 'Rate limit exceeded', 'code': 'RATE_LIMIT'}), 429
        _bucket['tokens'] -= 1
        return f(*args, **kwargs)
    return decorated


def log_request(f):
    """Request logging middleware."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        start = time.time()
        response = f(*args, **kwargs)
        duration = time.time() - start
        logger.info(f'{request.method} {request.path} -> {duration:.3f}s')
        return response
    return decorated
'''

    # develop also has updated routes.py with class-based middleware usage
    routes_develop = '''\
"""
API Routes for the web application (develop branch).
Uses centralized middleware stack.
"""
from flask import Flask, jsonify, request
from middleware import authenticate, rate_limit, log_request

app = Flask(__name__)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'version': '2.0.0'})


@app.route('/api/users', methods=['GET'])
@authenticate
@rate_limit
@log_request
def get_users():
    """Return list of users."""
    users = [
        {'id': 1, 'name': 'Alice Smith', 'role': 'admin', 'active': True},
        {'id': 2, 'name': 'Bob Johnson', 'role': 'user', 'active': True},
        {'id': 3, 'name': 'Carol Williams', 'role': 'user', 'active': False},
        {'id': 4, 'name': 'David Brown', 'role': 'user', 'active': True},
    ]
    return jsonify(users)


@app.route('/api/users/<int:user_id>', methods=['GET'])
@authenticate
def get_user(user_id):
    """Return a single user by ID."""
    return jsonify({'id': user_id, 'name': 'Alice Smith', 'role': 'admin', 'active': True})


@app.route('/api/products', methods=['GET'])
@rate_limit
def get_products():
    """Return list of products with inventory."""
    products = [
        {'id': 101, 'name': 'Widget A', 'price': 29.99, 'stock': 150},
        {'id': 102, 'name': 'Widget B', 'price': 49.99, 'stock': 75},
        {'id': 103, 'name': 'Widget C', 'price': 19.99, 'stock': 200},
    ]
    return jsonify(products)


@app.route('/api/orders', methods=['POST'])
@authenticate
@rate_limit
def create_order():
    """Create a new order."""
    data = request.get_json()
    return jsonify({'order_id': 12345, 'status': 'created', 'items': data.get('items', [])}), 201


if __name__ == '__main__':
    app.run(debug=True)
'''

    with open(os.path.join(PROJECT_DIR, 'middleware.py'), 'w') as f:
        f.write(middleware_develop)
    with open(os.path.join(PROJECT_DIR, 'routes.py'), 'w') as f:
        f.write(routes_develop)

    run_cmd('git add -A', cwd=PROJECT_DIR, env=git_env)
    run_cmd('git commit -m "Refactor: class-based middleware stack, add orders endpoint"', cwd=PROJECT_DIR, env=git_env)

    # ----------------------------------------------------------------
    # Create 'feature/api' branch from main (not from develop)
    # ----------------------------------------------------------------
    # Get the hash of the initial commit
    result = run_cmd('git log --oneline', cwd=PROJECT_DIR, env=git_env)
    print(f'Commits: {result.stdout}')

    # Checkout the first (initial) commit to branch feature/api
    result = run_cmd('git log --oneline --reverse', cwd=PROJECT_DIR, env=git_env)
    first_commit = result.stdout.strip().split('\n')[0].split(' ')[0]
    print(f'First commit: {first_commit}')

    run_cmd(f'git checkout -b feature/api {first_commit}', cwd=PROJECT_DIR, env=git_env)

    # feature/api has modified routes.py and middleware.py relative to base
    # routes.py: add new /api/search endpoint and /api/stats endpoint
    routes_feature = '''\
"""
API Routes for the web application.
Feature/api branch: added search and stats endpoints.
"""
from flask import Flask, jsonify, request
from middleware import authenticate, rate_limit

app = Flask(__name__)


@app.route('/api/users', methods=['GET'])
def get_users():
    """Return list of users."""
    users = [
        {'id': 1, 'name': 'Alice Smith', 'role': 'admin'},
        {'id': 2, 'name': 'Bob Johnson', 'role': 'user'},
        {'id': 3, 'name': 'Carol Williams', 'role': 'user'},
    ]
    return jsonify(users)


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Return a single user by ID."""
    return jsonify({'id': user_id, 'name': 'Alice Smith', 'role': 'admin'})


@app.route('/api/products', methods=['GET'])
def get_products():
    """Return list of products."""
    products = [
        {'id': 101, 'name': 'Widget A', 'price': 29.99},
        {'id': 102, 'name': 'Widget B', 'price': 49.99},
    ]
    return jsonify(products)


@app.route('/api/search', methods=['GET'])
def search():
    """Search across users and products."""
    query = request.args.get('q', '')
    results = {
        'query': query,
        'users': [],
        'products': [],
        'total': 0,
    }
    return jsonify(results)


@app.route('/api/stats', methods=['GET'])
@authenticate
def get_stats():
    """Return application statistics. Requires authentication."""
    stats = {
        'total_users': 3,
        'active_sessions': 12,
        'requests_today': 1547,
        'uptime_hours': 72,
    }
    return jsonify(stats)


if __name__ == '__main__':
    app.run(debug=True)
'''

    # middleware.py: add caching decorator and cors support
    middleware_feature = '''\
"""
Middleware functions for the web application.
Feature/api branch: added caching and CORS support.
"""
import functools
from flask import request, jsonify


def authenticate(f):
    """Basic authentication middleware."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated


def rate_limit(f):
    """Basic rate limiting middleware."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        # Simple passthrough for now
        return f(*args, **kwargs)
    return decorated


def cache_response(timeout=300):
    """Cache decorator for route responses."""
    def decorator(f):
        _cache = {}

        @functools.wraps(f)
        def decorated(*args, **kwargs):
            cache_key = f'{request.path}?{request.query_string.decode()}'
            if cache_key in _cache:
                cached_data, cached_time = _cache[cache_key]
                import time
                if time.time() - cached_time < timeout:
                    return cached_data
            response = f(*args, **kwargs)
            import time
            _cache[cache_key] = (response, time.time())
            return response
        return decorated
    return decorator


def cors_allow(f):
    """Add CORS headers to response."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        response = f(*args, **kwargs)
        if hasattr(response, 'headers'):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
        return response
    return decorated
'''

    with open(os.path.join(PROJECT_DIR, 'routes.py'), 'w') as f:
        f.write(routes_feature)
    with open(os.path.join(PROJECT_DIR, 'middleware.py'), 'w') as f:
        f.write(middleware_feature)

    # Stage the changes (but do NOT commit — these are the changes to be stashed)
    run_cmd('git add routes.py middleware.py', cwd=PROJECT_DIR, env=git_env)

    print(f'Project created at: {PROJECT_DIR}')

    # Verify state
    result = run_cmd('git status', cwd=PROJECT_DIR, env=git_env)
    print(f'Git status:\n{result.stdout}')

    result = run_cmd('git branch -a', cwd=PROJECT_DIR, env=git_env)
    print(f'Branches:\n{result.stdout}')

    result = run_cmd('git stash list', cwd=PROJECT_DIR, env=git_env)
    print(f'Stash list (should be empty): {result.stdout}')

    # GUI-ready startup: open VSCode with the project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with project directory on DISPLAY=:0')


create_initial()
