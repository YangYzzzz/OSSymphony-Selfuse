"""
Initial Setup: Three-way merge conflict in VSCode for vscode_git_058
Task ID: vscode_git_058
Domain: vs_code

Creates a git repository with a three-way merge conflict scenario:
  - main branch: has Redis cache settings (merged from feature/cache-config), TIMEOUT=60
  - feature/database-config branch: adds PostgreSQL settings, TIMEOUT=45
  - A `git merge` is initiated, leaving settings.py in conflict state for VSCode to resolve
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_058'
PROJECT_DIR = f'{WORKDIR}/project'


def run(cmd, cwd=None, check=True, env=None):
    """Run a shell command."""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd, check=check,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, env=env
    )
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
    if os.path.exists(PROJECT_DIR):
        run(f'rm -rf "{PROJECT_DIR}"')

    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Git config for commits
    git_env = os.environ.copy()
    git_env['GIT_AUTHOR_NAME'] = 'Dev Team'
    git_env['GIT_AUTHOR_EMAIL'] = 'dev@example.com'
    git_env['GIT_COMMITTER_NAME'] = 'Dev Team'
    git_env['GIT_COMMITTER_EMAIL'] = 'dev@example.com'

    def git(cmd, cwd=PROJECT_DIR):
        return run(f'git {cmd}', cwd=cwd, env=git_env)

    # -------------------------
    # 1. Init repo and create base commit (origin/main baseline)
    # -------------------------
    git('init -b main')
    git('config user.email "dev@example.com"')
    git('config user.name "Dev Team"')

    # Base settings.py — before any feature branches
    base_settings = """\
# Application Configuration
# This file contains core settings for the web application

DEBUG = False
SECRET_KEY = 'prod-secret-key-xK9mP2nQ'

# Application Settings
APP_NAME = 'WebApp'
APP_VERSION = '2.1.0'
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'app.example.com']

# Database (base config)
DATABASE = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'db.sqlite3',
}

# Timeout (in seconds)
TIMEOUT = 30

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = '/var/log/webapp/app.log'

# Static files
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/media/'
"""

    with open(f'{PROJECT_DIR}/settings.py', 'w') as f:
        f.write(base_settings)

    # Also add a README and another file for realism
    readme = """\
# WebApp

A production web application.

## Configuration

Edit `settings.py` to configure the application.

## Branches

- `main` — stable production config
- `feature/cache-config` — Redis caching layer
- `feature/database-config` — PostgreSQL database migration
"""
    with open(f'{PROJECT_DIR}/README.md', 'w') as f:
        f.write(readme)

    requirements = """\
Django==4.2.0
redis==4.6.0
psycopg2-binary==2.9.7
celery==5.3.1
gunicorn==21.2.0
"""
    with open(f'{PROJECT_DIR}/requirements.txt', 'w') as f:
        f.write(requirements)

    git('add -A')
    git('commit -m "Initial commit: base application configuration"')

    # -------------------------
    # 2. Create feature/cache-config branch from base
    # -------------------------
    git('checkout -b feature/cache-config')

    cache_settings = """\
# Application Configuration
# This file contains core settings for the web application

DEBUG = False
SECRET_KEY = 'prod-secret-key-xK9mP2nQ'

# Application Settings
APP_NAME = 'WebApp'
APP_VERSION = '2.1.0'
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'app.example.com']

# Database (base config)
DATABASE = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'db.sqlite3',
}

# Timeout (in seconds)
TIMEOUT = 60

# Cache Configuration (Redis)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'IGNORE_EXCEPTIONS': True,
        },
        'KEY_PREFIX': 'webapp',
        'TIMEOUT': 300,
    }
}

CACHE_MIDDLEWARE_SECONDS = 600
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = '/var/log/webapp/app.log'

# Static files
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/media/'
"""

    with open(f'{PROJECT_DIR}/settings.py', 'w') as f:
        f.write(cache_settings)

    git('add -A')
    git('commit -m "feat(cache): add Redis cache configuration with session support"')

    # -------------------------
    # 3. Switch back to main and merge feature/cache-config
    # -------------------------
    git('checkout main')
    git('merge feature/cache-config -m "Merge branch feature/cache-config into main"')

    # -------------------------
    # 4. Create feature/database-config branch from base (original main before merge)
    # -------------------------
    # Branch from the initial commit (before cache-config was merged)
    result = git('log --oneline')
    # Get the base commit hash
    base_commit = git('log --oneline --reverse').stdout.strip().split('\n')[0].split()[0]

    git(f'checkout -b feature/database-config {base_commit}')

    db_settings = """\
# Application Configuration
# This file contains core settings for the web application

DEBUG = False
SECRET_KEY = 'prod-secret-key-xK9mP2nQ'

# Application Settings
APP_NAME = 'WebApp'
APP_VERSION = '2.1.0'
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'app.example.com']

# Database Configuration (PostgreSQL)
DATABASE = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'webapp_production',
    'USER': 'webapp_user',
    'PASSWORD': 'db-pass-9Kx2mN',
    'HOST': 'db.internal.example.com',
    'PORT': '5432',
    'CONN_MAX_AGE': 60,
    'OPTIONS': {
        'sslmode': 'require',
        'connect_timeout': 10,
    },
}

# Timeout (in seconds)
TIMEOUT = 45

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = '/var/log/webapp/app.log'

# Static files
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/media/'
"""

    with open(f'{PROJECT_DIR}/settings.py', 'w') as f:
        f.write(db_settings)

    git('add -A')
    git('commit -m "feat(db): migrate to PostgreSQL with production settings"')

    # -------------------------
    # 5. Switch to main and start merging feature/database-config (creating conflict)
    # -------------------------
    git('checkout main')

    # Attempt the merge — this will create conflicts
    run('git merge feature/database-config --no-commit --no-ff || true',
        cwd=PROJECT_DIR, check=False, env=git_env)

    # Verify conflict state
    status_result = run('git status', cwd=PROJECT_DIR, env=git_env)
    print("Git status after merge attempt:")
    print(status_result.stdout)

    # Check that settings.py has conflicts
    with open(f'{PROJECT_DIR}/settings.py', 'r') as f:
        content = f.read()

    if '<<<<<<' in content:
        print("SUCCESS: settings.py has merge conflict markers as expected")
    else:
        print("WARNING: No conflict markers found, creating them manually")
        # Manually create conflict state if auto-merge succeeded
        conflict_content = """\
# Application Configuration
# This file contains core settings for the web application

DEBUG = False
SECRET_KEY = 'prod-secret-key-xK9mP2nQ'

# Application Settings
APP_NAME = 'WebApp'
APP_VERSION = '2.1.0'
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'app.example.com']

<<<<<<< HEAD
# Database (base config)
DATABASE = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'db.sqlite3',
}

# Timeout (in seconds)
TIMEOUT = 60

# Cache Configuration (Redis)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'IGNORE_EXCEPTIONS': True,
        },
        'KEY_PREFIX': 'webapp',
        'TIMEOUT': 300,
    }
}

CACHE_MIDDLEWARE_SECONDS = 600
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
=======
# Database Configuration (PostgreSQL)
DATABASE = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'webapp_production',
    'USER': 'webapp_user',
    'PASSWORD': 'db-pass-9Kx2mN',
    'HOST': 'db.internal.example.com',
    'PORT': '5432',
    'CONN_MAX_AGE': 60,
    'OPTIONS': {
        'sslmode': 'require',
        'connect_timeout': 10,
    },
}

# Timeout (in seconds)
TIMEOUT = 45
>>>>>>> feature/database-config

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = '/var/log/webapp/app.log'

# Static files
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/media/'
"""
        with open(f'{PROJECT_DIR}/settings.py', 'w') as f:
            f.write(conflict_content)
        # Stage as conflicted
        run('git checkout --merge settings.py || true', cwd=PROJECT_DIR, check=False, env=git_env)

    print(f"Project directory created at: {PROJECT_DIR}")
    print("settings.py is in merge conflict state")

    # Print the conflict content for verification
    with open(f'{PROJECT_DIR}/settings.py', 'r') as f:
        final_content = f.read()
    print("\nsettings.py content:")
    print(final_content[:500])

    # -------------------------
    # 6. Launch VSCode with the project
    # -------------------------
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project directory at DISPLAY=:0')


create_initial()
