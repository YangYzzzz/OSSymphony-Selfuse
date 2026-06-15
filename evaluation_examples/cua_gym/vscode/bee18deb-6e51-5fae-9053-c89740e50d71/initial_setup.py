"""
Initial Setup: Commit changes to three files in a specific order with three separate commits
Task ID: vscode_git_093
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_093'
PROJECT_DIR = f'{WORKDIR}/project'


def run_cmd(cmd, cwd=None, env=None):
    """Run a shell command and return output."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=cwd,
        env=env,
    )
    if result.returncode != 0:
        print(f'WARN: Command failed: {cmd}')
        print(f'  stdout: {result.stdout}')
        print(f'  stderr: {result.stderr}')
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
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Set up git config environment for consistent commits
    git_env = os.environ.copy()
    git_env['GIT_AUTHOR_NAME'] = 'Dev User'
    git_env['GIT_AUTHOR_EMAIL'] = 'dev@example.com'
    git_env['GIT_COMMITTER_NAME'] = 'Dev User'
    git_env['GIT_COMMITTER_EMAIL'] = 'dev@example.com'

    # Initialize git repo (idempotent)
    if not os.path.exists(os.path.join(PROJECT_DIR, '.git')):
        run_cmd('git init', cwd=PROJECT_DIR, env=git_env)
        run_cmd('git config user.email "dev@example.com"', cwd=PROJECT_DIR, env=git_env)
        run_cmd('git config user.name "Dev User"', cwd=PROJECT_DIR, env=git_env)
    else:
        run_cmd('git config user.email "dev@example.com"', cwd=PROJECT_DIR, env=git_env)
        run_cmd('git config user.name "Dev User"', cwd=PROJECT_DIR, env=git_env)

    # Create initial versions of all three files with realistic content
    database_py_initial = '''\
"""
Database module for the application.
Handles connection management and query execution.
"""
import psycopg2
import logging

logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'appdb',
    'user': 'appuser',
    'password': 'secret123',
}

# Simple single connection (not pooled)
_connection = None


def get_connection():
    """Get a database connection (no pooling)."""
    global _connection
    if _connection is None or _connection.closed:
        _connection = psycopg2.connect(**DB_CONFIG)
        logger.info("Database connection established")
    return _connection


def execute_query(query, params=None):
    """Execute a query and return results."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor.fetchall()
    except Exception as e:
        conn.rollback()
        logger.error(f"Query failed: {e}")
        raise
    finally:
        cursor.close()


def close_connection():
    """Close the database connection."""
    global _connection
    if _connection and not _connection.closed:
        _connection.close()
        _connection = None
        logger.info("Database connection closed")
'''

    api_py_initial = '''\
"""
API module for the application.
Provides REST endpoints for client applications.
"""
from flask import Flask, request, jsonify
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/api/users', methods=['GET'])
def get_users():
    """Return list of users."""
    users = [
        {'id': 1, 'name': 'Alice Johnson', 'email': 'alice@example.com', 'role': 'admin'},
        {'id': 2, 'name': 'Bob Smith', 'email': 'bob@example.com', 'role': 'user'},
        {'id': 3, 'name': 'Carol White', 'email': 'carol@example.com', 'role': 'user'},
    ]
    return jsonify(users)


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Return a specific user by ID."""
    return jsonify({'id': user_id, 'name': 'Alice Johnson', 'email': 'alice@example.com'})


@app.route('/api/products', methods=['GET'])
def get_products():
    """Return list of products."""
    products = [
        {'id': 101, 'name': 'Widget Pro', 'price': 29.99, 'stock': 150},
        {'id': 102, 'name': 'Gadget Plus', 'price': 49.99, 'stock': 75},
        {'id': 103, 'name': 'Tool Master', 'price': 89.99, 'stock': 30},
    ]
    return jsonify(products)


@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create a new order."""
    data = request.get_json()
    order_id = 5001
    logger.info(f"Order created: {order_id} for user {data.get('user_id')}")
    return jsonify({'order_id': order_id, 'status': 'pending'}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
'''

    frontend_js_initial = '''\
/**
 * Frontend JavaScript module
 * Handles UI interactions and API communication.
 */

// Application state
const AppState = {
  currentUser: null,
  products: [],
  cart: [],
};

/**
 * Fetch users from the API
 */
async function fetchUsers() {
  const response = await fetch('/api/users');
  const users = await response.json();
  return users;
}

/**
 * Render user list to DOM
 */
function renderUsers(users) {
  const container = document.getElementById('user-list');
  container.innerHTML = '';
  users.forEach(user => {
    const item = document.createElement('li');
    item.className = 'user-item';
    item.textContent = `${user.name} (${user.role})`;
    container.appendChild(item);
  });
}

/**
 * Product card component
 * @param {Object} product - Product data
 * @returns {HTMLElement} - Product card element
 */
function createProductCard(product) {
  const card = document.createElement('div');
  card.className = 'product-card';
  // Layout is not responsive yet — fixed width causes overflow on mobile
  card.style.width = '300px';
  card.innerHTML = `
    <h3>${product.name}</h3>
    <p class="price">$${product.price.toFixed(2)}</p>
    <p class="stock">In stock: ${product.stock}</p>
    <button onclick="addToCart(${product.id})">Add to Cart</button>
  `;
  return card;
}

/**
 * Add product to cart
 */
function addToCart(productId) {
  const product = AppState.products.find(p => p.id === productId);
  if (product) {
    AppState.cart.push(product);
    updateCartBadge();
  }
}

/**
 * Update cart badge count
 */
function updateCartBadge() {
  const badge = document.getElementById('cart-badge');
  if (badge) {
    badge.textContent = AppState.cart.length;
  }
}

// Initialize app
document.addEventListener('DOMContentLoaded', async () => {
  const users = await fetchUsers();
  renderUsers(users);
});
'''

    # Write initial files
    with open(os.path.join(PROJECT_DIR, 'database.py'), 'w') as f:
        f.write(database_py_initial)
    with open(os.path.join(PROJECT_DIR, 'api.py'), 'w') as f:
        f.write(api_py_initial)
    with open(os.path.join(PROJECT_DIR, 'frontend.js'), 'w') as f:
        f.write(frontend_js_initial)

    # Create a README for the project
    readme_content = '''\
# Web Application Project

A full-stack web application with Python backend and JavaScript frontend.

## Structure

- `database.py` - Database connection and query management
- `api.py` - REST API endpoints (Flask)
- `frontend.js` - Client-side UI logic
- `requirements.txt` - Python dependencies

## Setup

```bash
pip install -r requirements.txt
python api.py
```

## Development

See CONTRIBUTING.md for development guidelines.
'''
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme_content)

    # Create requirements.txt
    requirements_content = '''\
flask>=2.0.0
psycopg2-binary>=2.9.0
requests>=2.28.0
'''
    with open(os.path.join(PROJECT_DIR, 'requirements.txt'), 'w') as f:
        f.write(requirements_content)

    # Make an initial commit with all files (baseline state)
    run_cmd('git add README.md requirements.txt database.py api.py frontend.js', cwd=PROJECT_DIR, env=git_env)
    run_cmd('git commit -m "Initial project setup"', cwd=PROJECT_DIR, env=git_env)
    print("Initial commit created.")

    # Now modify all three files to represent the work done (to be committed by the agent)
    database_py_modified = '''\
"""
Database module for the application.
Handles connection management and query execution with connection pooling.
"""
import psycopg2
import psycopg2.pool
import logging

logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'appdb',
    'user': 'appuser',
    'password': 'secret123',
}

# Connection pool configuration
POOL_MIN_CONNECTIONS = 2
POOL_MAX_CONNECTIONS = 10

# Connection pool instance
_pool = None


def get_pool():
    """Get or create the connection pool."""
    global _pool
    if _pool is None:
        _pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=POOL_MIN_CONNECTIONS,
            maxconn=POOL_MAX_CONNECTIONS,
            **DB_CONFIG
        )
        logger.info(f"Connection pool created (min={POOL_MIN_CONNECTIONS}, max={POOL_MAX_CONNECTIONS})")
    return _pool


def get_connection():
    """Get a connection from the pool."""
    pool = get_pool()
    conn = pool.getconn()
    logger.debug("Connection acquired from pool")
    return conn


def release_connection(conn):
    """Return a connection to the pool."""
    pool = get_pool()
    pool.putconn(conn)
    logger.debug("Connection returned to pool")


def execute_query(query, params=None):
    """Execute a query using a pooled connection and return results."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor.fetchall()
    except Exception as e:
        conn.rollback()
        logger.error(f"Query failed: {e}")
        raise
    finally:
        cursor.close()
        release_connection(conn)


def close_pool():
    """Close all connections in the pool."""
    global _pool
    if _pool:
        _pool.closeall()
        _pool = None
        logger.info("Connection pool closed")
'''

    api_py_modified = '''\
"""
API module for the application.
Provides REST endpoints with rate limiting for client applications.
"""
from flask import Flask, request, jsonify
from functools import wraps
import time
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

# Rate limiting configuration
RATE_LIMIT_REQUESTS = 100   # requests per window
RATE_LIMIT_WINDOW = 60      # seconds
_rate_limit_store = {}       # {ip: [timestamps]}


def rate_limit(f):
    """Decorator to apply rate limiting to API endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = request.remote_addr
        now = time.time()
        window_start = now - RATE_LIMIT_WINDOW

        # Clean up old entries
        if client_ip in _rate_limit_store:
            _rate_limit_store[client_ip] = [
                t for t in _rate_limit_store[client_ip] if t > window_start
            ]
        else:
            _rate_limit_store[client_ip] = []

        # Check rate limit
        if len(_rate_limit_store[client_ip]) >= RATE_LIMIT_REQUESTS:
            logger.warning(f"Rate limit exceeded for {client_ip}")
            return jsonify({'error': 'Rate limit exceeded. Try again later.'}), 429

        # Record this request
        _rate_limit_store[client_ip].append(now)
        return f(*args, **kwargs)
    return decorated_function


@app.route('/api/users', methods=['GET'])
@rate_limit
def get_users():
    """Return list of users."""
    users = [
        {'id': 1, 'name': 'Alice Johnson', 'email': 'alice@example.com', 'role': 'admin'},
        {'id': 2, 'name': 'Bob Smith', 'email': 'bob@example.com', 'role': 'user'},
        {'id': 3, 'name': 'Carol White', 'email': 'carol@example.com', 'role': 'user'},
    ]
    return jsonify(users)


@app.route('/api/users/<int:user_id>', methods=['GET'])
@rate_limit
def get_user(user_id):
    """Return a specific user by ID."""
    return jsonify({'id': user_id, 'name': 'Alice Johnson', 'email': 'alice@example.com'})


@app.route('/api/products', methods=['GET'])
@rate_limit
def get_products():
    """Return list of products."""
    products = [
        {'id': 101, 'name': 'Widget Pro', 'price': 29.99, 'stock': 150},
        {'id': 102, 'name': 'Gadget Plus', 'price': 49.99, 'stock': 75},
        {'id': 103, 'name': 'Tool Master', 'price': 89.99, 'stock': 30},
    ]
    return jsonify(products)


@app.route('/api/orders', methods=['POST'])
@rate_limit
def create_order():
    """Create a new order."""
    data = request.get_json()
    order_id = 5001
    logger.info(f"Order created: {order_id} for user {data.get('user_id')}")
    return jsonify({'order_id': order_id, 'status': 'pending'}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
'''

    frontend_js_modified = '''\
/**
 * Frontend JavaScript module
 * Handles UI interactions and API communication.
 * Responsive layout support added for mobile and tablet screens.
 */

// Application state
const AppState = {
  currentUser: null,
  products: [],
  cart: [],
};

/**
 * Fetch users from the API
 */
async function fetchUsers() {
  const response = await fetch('/api/users');
  const users = await response.json();
  return users;
}

/**
 * Render user list to DOM
 */
function renderUsers(users) {
  const container = document.getElementById('user-list');
  container.innerHTML = '';
  users.forEach(user => {
    const item = document.createElement('li');
    item.className = 'user-item';
    item.textContent = `${user.name} (${user.role})`;
    container.appendChild(item);
  });
}

/**
 * Product card component — responsive layout
 * @param {Object} product - Product data
 * @returns {HTMLElement} - Product card element
 */
function createProductCard(product) {
  const card = document.createElement('div');
  card.className = 'product-card';
  // Responsive layout: use percentage width and max-width instead of fixed pixels
  card.style.width = '100%';
  card.style.maxWidth = '320px';
  card.style.boxSizing = 'border-box';
  card.innerHTML = `
    <h3>${product.name}</h3>
    <p class="price">$${product.price.toFixed(2)}</p>
    <p class="stock">In stock: ${product.stock}</p>
    <button onclick="addToCart(${product.id})">Add to Cart</button>
  `;
  return card;
}

/**
 * Responsive grid layout for product cards
 */
function renderProductGrid(products) {
  const grid = document.getElementById('product-grid');
  if (!grid) return;
  grid.style.display = 'grid';
  grid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(280px, 1fr))';
  grid.style.gap = '16px';
  grid.style.padding = '16px';
  grid.innerHTML = '';
  products.forEach(product => {
    grid.appendChild(createProductCard(product));
  });
}

/**
 * Add product to cart
 */
function addToCart(productId) {
  const product = AppState.products.find(p => p.id === productId);
  if (product) {
    AppState.cart.push(product);
    updateCartBadge();
  }
}

/**
 * Update cart badge count
 */
function updateCartBadge() {
  const badge = document.getElementById('cart-badge');
  if (badge) {
    badge.textContent = AppState.cart.length;
  }
}

// Initialize app
document.addEventListener('DOMContentLoaded', async () => {
  const users = await fetchUsers();
  renderUsers(users);
});
'''

    # Overwrite files with modified versions (these represent work done, need to be committed)
    with open(os.path.join(PROJECT_DIR, 'database.py'), 'w') as f:
        f.write(database_py_modified)
    with open(os.path.join(PROJECT_DIR, 'api.py'), 'w') as f:
        f.write(api_py_modified)
    with open(os.path.join(PROJECT_DIR, 'frontend.js'), 'w') as f:
        f.write(frontend_js_modified)

    print(f"Modified files in {PROJECT_DIR}: database.py, api.py, frontend.js")
    print("All three files have uncommitted changes ready for agent to commit separately.")

    # Verify git status shows the three modified files
    status_result = run_cmd('git status', cwd=PROJECT_DIR, env=git_env)
    print(f"Git status:\n{status_result.stdout}")

    # GUI-ready startup: open VSCode with the project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with project directory, DISPLAY=:0')


create_initial()
