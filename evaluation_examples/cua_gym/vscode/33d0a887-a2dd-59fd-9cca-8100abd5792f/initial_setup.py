"""
Initial Setup: Git blame and log investigation task
Task ID: vscode_git_069
Domain: vs_code

Creates a git repository at /home/user/project with orders.py
having 5 distinct commits from different authors, ready for
the agent to perform a code archaeology investigation.
"""

import os
import subprocess
import shlex
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_069'
PROJECT_DIR = f'{WORKDIR}/project'


def run(cmd, cwd=None, env=None):
    """Run a shell command, print output."""
    result = subprocess.run(
        cmd if isinstance(cmd, list) else shlex.split(cmd),
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f'STDERR: {result.stderr}')
    return result


def git(args, cwd=PROJECT_DIR, env=None):
    """Run a git command in the project directory."""
    return run(['git'] + (args if isinstance(args, list) else shlex.split(args)), cwd=cwd, env=env)


def make_git_env(name, email):
    env = os.environ.copy()
    env['GIT_AUTHOR_NAME'] = name
    env['GIT_AUTHOR_EMAIL'] = f'{name}@example.com'
    env['GIT_COMMITTER_NAME'] = name
    env['GIT_COMMITTER_EMAIL'] = f'{name}@example.com'
    return env


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env['DISPLAY'] = ':0'
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    # Clean up and recreate project directory
    if os.path.exists(PROJECT_DIR):
        run(f'rm -rf {PROJECT_DIR}')
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Initialize git repo
    git(['init'])
    git(['config', 'user.email', 'setup@example.com'])
    git(['config', 'user.name', 'Setup'])

    # ----------------------------------------------------------------
    # Commit 1 — alice: initial version of process_order()
    # ----------------------------------------------------------------
    orders_v1 = '''\
"""Order processing module."""


def process_order(order_id, items, customer_id):
    """Process a customer order."""
    total = 0
    for item in items:
        total += item['price'] * item['quantity']

    order = {
        'id': order_id,
        'customer_id': customer_id,
        'items': items,
        'total': total,
        'status': 'pending',
    }

    # Save order to database
    save_order(order)
    return order


def save_order(order):
    """Persist order to the database."""
    db.insert('orders', order)
'''
    orders_path = os.path.join(PROJECT_DIR, 'orders.py')
    with open(orders_path, 'w') as f:
        f.write(orders_v1)

    alice_env = make_git_env('alice', 'alice@example.com')
    git(['add', 'orders.py'])
    git(['commit', '-m', 'Initial implementation of process_order()'], env=alice_env)

    # ----------------------------------------------------------------
    # Commit 2 — bob: added error handling
    # ----------------------------------------------------------------
    orders_v2 = '''\
"""Order processing module."""


def process_order(order_id, items, customer_id):
    """Process a customer order."""
    if not order_id:
        raise ValueError("order_id must not be empty")
    if not items:
        raise ValueError("items list must not be empty")
    if not customer_id:
        raise ValueError("customer_id must not be empty")

    total = 0
    for item in items:
        if 'price' not in item or 'quantity' not in item:
            raise KeyError(f"Item missing required fields: {item}")
        total += item['price'] * item['quantity']

    order = {
        'id': order_id,
        'customer_id': customer_id,
        'items': items,
        'total': total,
        'status': 'pending',
    }

    # Save order to database
    save_order(order)
    return order


def save_order(order):
    """Persist order to the database."""
    db.insert('orders', order)
'''
    with open(orders_path, 'w') as f:
        f.write(orders_v2)

    bob_env = make_git_env('bob', 'bob@example.com')
    git(['add', 'orders.py'])
    git(['commit', '-m', 'Add input validation and error handling to process_order()'], env=bob_env)

    # ----------------------------------------------------------------
    # Commit 3 — charlie: refactored to async
    # ----------------------------------------------------------------
    orders_v3 = '''\
"""Order processing module."""

import asyncio


async def process_order(order_id, items, customer_id):
    """Process a customer order asynchronously."""
    if not order_id:
        raise ValueError("order_id must not be empty")
    if not items:
        raise ValueError("items list must not be empty")
    if not customer_id:
        raise ValueError("customer_id must not be empty")

    total = 0
    for item in items:
        if 'price' not in item or 'quantity' not in item:
            raise KeyError(f"Item missing required fields: {item}")
        total += item['price'] * item['quantity']

    order = {
        'id': order_id,
        'customer_id': customer_id,
        'items': items,
        'total': total,
        'status': 'pending',
    }

    # Save order to database asynchronously
    await save_order(order)
    return order


async def save_order(order):
    """Persist order to the database asynchronously."""
    await db.insert_async('orders', order)
'''
    with open(orders_path, 'w') as f:
        f.write(orders_v3)

    charlie_env = make_git_env('charlie', 'charlie@example.com')
    git(['add', 'orders.py'])
    git(['commit', '-m', 'Refactor process_order() to async/await pattern'], env=charlie_env)

    # ----------------------------------------------------------------
    # Commit 4 — alice: added caching
    # ----------------------------------------------------------------
    orders_v4 = '''\
"""Order processing module."""

import asyncio
import functools

_order_cache = {}


async def process_order(order_id, items, customer_id):
    """Process a customer order asynchronously with caching."""
    if not order_id:
        raise ValueError("order_id must not be empty")
    if not items:
        raise ValueError("items list must not be empty")
    if not customer_id:
        raise ValueError("customer_id must not be empty")

    # Check cache first
    cache_key = (order_id, customer_id)
    if cache_key in _order_cache:
        return _order_cache[cache_key]

    total = 0
    for item in items:
        if 'price' not in item or 'quantity' not in item:
            raise KeyError(f"Item missing required fields: {item}")
        total += item['price'] * item['quantity']

    order = {
        'id': order_id,
        'customer_id': customer_id,
        'items': items,
        'total': total,
        'status': 'pending',
    }

    # Save order to database asynchronously
    await save_order(order)

    # Store in cache
    _order_cache[cache_key] = order
    return order


async def save_order(order):
    """Persist order to the database asynchronously."""
    await db.insert_async('orders', order)
'''
    with open(orders_path, 'w') as f:
        f.write(orders_v4)

    git(['add', 'orders.py'])
    git(['commit', '-m', 'Add in-memory caching to process_order()'], env=alice_env)

    # ----------------------------------------------------------------
    # Commit 5 — dave: fixed a race condition
    # ----------------------------------------------------------------
    orders_v5 = '''\
"""Order processing module."""

import asyncio
import functools

_order_cache = {}
_cache_lock = asyncio.Lock()


async def process_order(order_id, items, customer_id):
    """Process a customer order asynchronously with thread-safe caching."""
    if not order_id:
        raise ValueError("order_id must not be empty")
    if not items:
        raise ValueError("items list must not be empty")
    if not customer_id:
        raise ValueError("customer_id must not be empty")

    # Check cache first (with lock to prevent race condition)
    cache_key = (order_id, customer_id)
    async with _cache_lock:
        if cache_key in _order_cache:
            return _order_cache[cache_key]

    total = 0
    for item in items:
        if 'price' not in item or 'quantity' not in item:
            raise KeyError(f"Item missing required fields: {item}")
        total += item['price'] * item['quantity']

    order = {
        'id': order_id,
        'customer_id': customer_id,
        'items': items,
        'total': total,
        'status': 'pending',
    }

    # Save order to database asynchronously
    await save_order(order)

    # Store in cache (with lock to prevent race condition)
    async with _cache_lock:
        _order_cache[cache_key] = order
    return order


async def save_order(order):
    """Persist order to the database asynchronously."""
    await db.insert_async('orders', order)
'''
    with open(orders_path, 'w') as f:
        f.write(orders_v5)

    dave_env = make_git_env('dave', 'dave@example.com')
    git(['add', 'orders.py'])
    git(['commit', '-m', 'Fix race condition in process_order() cache with asyncio.Lock'], env=dave_env)

    # Verify git log
    log_result = git(['log', '--oneline', '--all'])
    print('Git log:')
    print(log_result.stdout)

    blame_result = git(['blame', 'orders.py'])
    print('Git blame (sample):')
    print(blame_result.stdout[:500])

    print(f'Initial project created at: {PROJECT_DIR}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project folder (DISPLAY=:0)')


create_initial()
