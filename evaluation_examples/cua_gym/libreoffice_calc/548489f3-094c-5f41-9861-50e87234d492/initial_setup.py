"""
Initial Setup: VSCode project with JSON config files for concat-to-doc task
Task ID: osworld_multi_apps_vscode_concat_doc_009
Domain: multi_apps (VSCode + LibreOffice Writer)
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_concat_doc_009'
DESKTOP = f'{WORKDIR}/Desktop'
PROJECT_DIR = f'{DESKTOP}/config_files'


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
    # Create Desktop directory if it doesn't exist
    os.makedirs(DESKTOP, exist_ok=True)
    # Create project directory
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # --- database.json ---
    database_config = {
        "database": {
            "host": "db.internal.example.com",
            "port": 5432,
            "name": "production_db",
            "username": "app_user",
            "password_env": "DB_PASSWORD",
            "pool": {
                "min_connections": 5,
                "max_connections": 20,
                "idle_timeout_ms": 30000
            },
            "ssl": {
                "enabled": True,
                "cert_path": "/etc/ssl/certs/db-cert.pem",
                "verify_hostname": True
            }
        },
        "migrations": {
            "directory": "./migrations",
            "auto_run": False,
            "table": "schema_migrations"
        }
    }
    with open(f'{PROJECT_DIR}/database.json', 'w') as f:
        json.dump(database_config, f, indent=2)

    # --- server.json ---
    server_config = {
        "server": {
            "host": "0.0.0.0",
            "port": 8080,
            "workers": 4,
            "timeout_seconds": 30,
            "max_request_size_mb": 10
        },
        "cors": {
            "enabled": True,
            "allowed_origins": [
                "https://app.example.com",
                "https://admin.example.com"
            ],
            "allowed_methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_credentials": True
        },
        "rate_limiting": {
            "enabled": True,
            "requests_per_minute": 120,
            "burst_limit": 200
        },
        "logging": {
            "level": "info",
            "format": "json",
            "output": "/var/log/app/server.log"
        }
    }
    with open(f'{PROJECT_DIR}/server.json', 'w') as f:
        json.dump(server_config, f, indent=2)

    # --- auth.json ---
    auth_config = {
        "authentication": {
            "provider": "jwt",
            "secret_env": "JWT_SECRET",
            "token_expiry_hours": 24,
            "refresh_token_expiry_days": 30,
            "algorithm": "HS256"
        },
        "oauth2": {
            "google": {
                "client_id_env": "GOOGLE_CLIENT_ID",
                "client_secret_env": "GOOGLE_CLIENT_SECRET",
                "scopes": ["openid", "email", "profile"],
                "redirect_uri": "https://app.example.com/auth/google/callback"
            },
            "github": {
                "client_id_env": "GITHUB_CLIENT_ID",
                "client_secret_env": "GITHUB_CLIENT_SECRET",
                "scopes": ["read:user", "user:email"],
                "redirect_uri": "https://app.example.com/auth/github/callback"
            }
        },
        "password_policy": {
            "min_length": 12,
            "require_uppercase": True,
            "require_lowercase": True,
            "require_numbers": True,
            "require_special_chars": True,
            "max_failed_attempts": 5,
            "lockout_duration_minutes": 15
        }
    }
    with open(f'{PROJECT_DIR}/auth.json', 'w') as f:
        json.dump(auth_config, f, indent=2)

    # --- cache.json ---
    cache_config = {
        "cache": {
            "backend": "redis",
            "host": "cache.internal.example.com",
            "port": 6379,
            "db": 0,
            "password_env": "REDIS_PASSWORD",
            "ttl_seconds": 3600,
            "max_memory_mb": 512
        },
        "session": {
            "store": "redis",
            "key_prefix": "sess:",
            "ttl_seconds": 86400,
            "secure_cookie": True
        },
        "invalidation": {
            "strategy": "LRU",
            "max_keys": 10000
        }
    }
    with open(f'{PROJECT_DIR}/cache.json', 'w') as f:
        json.dump(cache_config, f, indent=2)

    print(f'Project directory created: {PROJECT_DIR}')
    print('JSON config files created: auth.json, cache.json, database.json, server.json')

    # Ensure configs_doc.docx does NOT exist on the Desktop (task is to create it)
    doc_path = f'{DESKTOP}/configs_doc.docx'
    if os.path.exists(doc_path):
        os.remove(doc_path)
        print(f'Removed pre-existing {doc_path}')

    # GUI-ready startup: open VSCode with the config_files project
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with config_files project (DISPLAY=:0)')


create_initial()
