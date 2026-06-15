"""
Initial Setup: Cherry-pick conflict setup in VSCode
Task ID: vscode_git_060
Domain: vs_code

Creates a git repository at /home/user/webapp with:
  - main branch: db.py with sync connection_pool() + error handling
  - feature/optimization branch: commit that refactors to async connection_pool()
The user must cherry-pick the feature commit onto main, resolve the conflict
using VSCode's merge tools, and complete the cherry-pick.
"""

import os
import shlex
import subprocess
import time
import shutil

WORKDIR = '/home/user'
REPO_PATH = f'{WORKDIR}/webapp'
TASK_ID = 'vscode_git_060'


def run_cmd(cmd, cwd=None, env=None, check=True):
    """Run a shell command, return stdout."""
    result = subprocess.run(
        cmd if isinstance(cmd, list) else shlex.split(cmd),
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}")
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


def create_initial():
    # Remove existing repo if present (idempotent)
    if os.path.exists(REPO_PATH):
        shutil.rmtree(REPO_PATH)

    os.makedirs(REPO_PATH, exist_ok=True)

    # Git environment: set user identity for commits
    git_env = os.environ.copy()
    git_env['GIT_AUTHOR_NAME'] = 'Dev User'
    git_env['GIT_AUTHOR_EMAIL'] = 'dev@example.com'
    git_env['GIT_COMMITTER_NAME'] = 'Dev User'
    git_env['GIT_COMMITTER_EMAIL'] = 'dev@example.com'

    def git(cmd, **kwargs):
        return run_cmd(['git'] + shlex.split(cmd), cwd=REPO_PATH, env=git_env, **kwargs)

    # Initialize repo
    git('init -b main')
    git('config user.email "dev@example.com"')
    git('config user.name "Dev User"')

    # -----------------------------------------------------------------------
    # Initial commit on main: basic db.py with sync connection_pool
    # -----------------------------------------------------------------------
    db_py_v1 = '''\
"""
Database module for webapp.
Provides connection pooling and query utilities.
"""

import psycopg2
from psycopg2 import pool as pg_pool
import logging

logger = logging.getLogger(__name__)

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "webapp_db",
    "user": "webapp_user",
    "password": "s3cr3tpassword",
    "connect_timeout": 10,
}

_connection_pool = None
MAX_CONNECTIONS = 10
MIN_CONNECTIONS = 2


def connection_pool():
    """Initialize and return a synchronous database connection pool."""
    global _connection_pool
    if _connection_pool is None:
        _connection_pool = pg_pool.ThreadedConnectionPool(
            MIN_CONNECTIONS,
            MAX_CONNECTIONS,
            **DB_CONFIG,
        )
        logger.info("Database connection pool initialized (sync, %d-%d connections)",
                    MIN_CONNECTIONS, MAX_CONNECTIONS)
    return _connection_pool


def get_connection():
    """Get a connection from the pool."""
    pool = connection_pool()
    conn = pool.getconn()
    return conn


def release_connection(conn):
    """Return a connection to the pool."""
    pool = connection_pool()
    pool.putconn(conn)


def execute_query(query, params=None):
    """Execute a query and return all results."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            results = cur.fetchall()
        conn.commit()
        return results
    except Exception as e:
        conn.rollback()
        logger.error("Query failed: %s", e)
        raise
    finally:
        release_connection(conn)


def execute_update(query, params=None):
    """Execute an INSERT/UPDATE/DELETE query."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            row_count = cur.rowcount
        conn.commit()
        return row_count
    except Exception as e:
        conn.rollback()
        logger.error("Update failed: %s", e)
        raise
    finally:
        release_connection(conn)
'''

    # Write initial db.py
    with open(os.path.join(REPO_PATH, 'db.py'), 'w') as f:
        f.write(db_py_v1)

    # Create a basic requirements.txt
    requirements = '''\
psycopg2-binary==2.9.9
asyncpg==0.29.0
aiohttp==3.9.3
Flask==3.0.2
SQLAlchemy==2.0.27
python-dotenv==1.0.1
'''
    with open(os.path.join(REPO_PATH, 'requirements.txt'), 'w') as f:
        f.write(requirements)

    # Create a basic app.py
    app_py = '''\
"""Main application entry point for webapp."""

from flask import Flask, jsonify
from db import execute_query

app = Flask(__name__)


@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})


@app.route('/api/users')
def get_users():
    rows = execute_query("SELECT id, username, email FROM users LIMIT 50")
    return jsonify([{"id": r[0], "username": r[1], "email": r[2]} for r in rows])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
'''
    with open(os.path.join(REPO_PATH, 'app.py'), 'w') as f:
        f.write(app_py)

    git('add .')
    git('commit -m "Initial commit: webapp with sync database connection pool"')

    # -----------------------------------------------------------------------
    # Commit on main: add error handling to connection_pool
    # This is what was added to main AFTER feature/optimization branched off
    # -----------------------------------------------------------------------
    db_py_main = '''\
"""
Database module for webapp.
Provides connection pooling and query utilities.
"""

import psycopg2
from psycopg2 import pool as pg_pool
import logging

logger = logging.getLogger(__name__)

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "webapp_db",
    "user": "webapp_user",
    "password": "s3cr3tpassword",
    "connect_timeout": 10,
}

_connection_pool = None
MAX_CONNECTIONS = 10
MIN_CONNECTIONS = 2


def connection_pool():
    """Initialize and return a synchronous database connection pool."""
    global _connection_pool
    if _connection_pool is None:
        try:
            _connection_pool = pg_pool.ThreadedConnectionPool(
                MIN_CONNECTIONS,
                MAX_CONNECTIONS,
                **DB_CONFIG,
            )
            logger.info("Database connection pool initialized (sync, %d-%d connections)",
                        MIN_CONNECTIONS, MAX_CONNECTIONS)
        except psycopg2.OperationalError as e:
            logger.critical("Failed to initialize connection pool: %s", e)
            raise RuntimeError("Database unavailable, cannot start application") from e
        except Exception as e:
            logger.error("Unexpected error initializing connection pool: %s", e)
            raise
    return _connection_pool


def get_connection():
    """Get a connection from the pool."""
    pool = connection_pool()
    conn = pool.getconn()
    if conn is None:
        raise RuntimeError("Connection pool exhausted")
    return conn


def release_connection(conn):
    """Return a connection to the pool."""
    pool = connection_pool()
    pool.putconn(conn)


def execute_query(query, params=None):
    """Execute a query and return all results."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            results = cur.fetchall()
        conn.commit()
        return results
    except Exception as e:
        conn.rollback()
        logger.error("Query failed: %s", e)
        raise
    finally:
        release_connection(conn)


def execute_update(query, params=None):
    """Execute an INSERT/UPDATE/DELETE query."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            row_count = cur.rowcount
        conn.commit()
        return row_count
    except Exception as e:
        conn.rollback()
        logger.error("Update failed: %s", e)
        raise
    finally:
        release_connection(conn)
'''

    with open(os.path.join(REPO_PATH, 'db.py'), 'w') as f:
        f.write(db_py_main)

    git('add db.py')
    git('commit -m "Add robust error handling to connection_pool initialization"')

    # -----------------------------------------------------------------------
    # Create feature/optimization branch from the INITIAL commit
    # (branch off before the error handling was added to main)
    # -----------------------------------------------------------------------
    # Get the hash of the first commit
    first_commit = run_cmd(
        ['git', 'log', '--oneline', '--reverse'],
        cwd=REPO_PATH, env=git_env
    ).split('\n')[0].split()[0]

    git(f'checkout -b feature/optimization {first_commit}')

    # Now on feature/optimization: refactor connection_pool to async
    db_py_feature = '''\
"""
Database module for webapp.
Provides connection pooling and query utilities.
"""

import asyncpg
import asyncio
import logging

logger = logging.getLogger(__name__)

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "webapp_db",
    "user": "webapp_user",
    "password": "s3cr3tpassword",
    "timeout": 10,
}

_connection_pool = None
MAX_CONNECTIONS = 10
MIN_CONNECTIONS = 2


async def connection_pool():
    """Initialize and return an async database connection pool."""
    global _connection_pool
    if _connection_pool is None:
        _connection_pool = await asyncpg.create_pool(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            min_size=MIN_CONNECTIONS,
            max_size=MAX_CONNECTIONS,
            command_timeout=DB_CONFIG["timeout"],
        )
        logger.info("Async database connection pool initialized (%d-%d connections)",
                    MIN_CONNECTIONS, MAX_CONNECTIONS)
    return _connection_pool


async def get_connection():
    """Acquire a connection from the async pool."""
    pool = await connection_pool()
    return pool.acquire()


async def execute_query(query, *args):
    """Execute a query asynchronously and return all results."""
    pool = await connection_pool()
    async with pool.acquire() as conn:
        results = await conn.fetch(query, *args)
    return results


async def execute_update(query, *args):
    """Execute an INSERT/UPDATE/DELETE query asynchronously."""
    pool = await connection_pool()
    async with pool.acquire() as conn:
        result = await conn.execute(query, *args)
    return result
'''

    with open(os.path.join(REPO_PATH, 'db.py'), 'w') as f:
        f.write(db_py_feature)

    git('add db.py')
    git('commit -m "Refactor database connection pool to use async/await with asyncpg"')

    # Record the feature commit hash for reference
    feature_commit = run_cmd(
        ['git', 'log', '--oneline', '-1'],
        cwd=REPO_PATH, env=git_env
    ).split()[0]

    # Write the commit hash to a reference file so the task knows the real hash
    with open(os.path.join(REPO_PATH, '.feature_commit_hash'), 'w') as f:
        f.write(feature_commit + '\n')

    print(f"Feature/optimization commit hash: {feature_commit}")

    # -----------------------------------------------------------------------
    # Switch back to main
    # -----------------------------------------------------------------------
    git('checkout main')

    # Verify the state: main should have 2 commits, feature should have 2
    print("Main branch log:")
    print(run_cmd(['git', 'log', '--oneline'], cwd=REPO_PATH, env=git_env))
    print("\nFeature branch log:")
    print(run_cmd(['git', 'log', '--oneline', 'feature/optimization'], cwd=REPO_PATH, env=git_env))

    print(f'\nInitial repository created: {REPO_PATH}')
    print(f'Feature commit to cherry-pick: {feature_commit}')

    # GUI-ready startup: open VSCode with the webapp folder
    launch_gui(f'code "{REPO_PATH}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
