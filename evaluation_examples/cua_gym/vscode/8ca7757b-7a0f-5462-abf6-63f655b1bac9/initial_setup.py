"""
Initial Setup: Create project directory for REST Client GraphQL testing
Task ID: vscode_gf3_047
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_047'
PROJECT_DIR = f'{WORKDIR}/projects/api-tests'

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
    # Create the project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Create some existing project files to make the workspace look realistic
    # but do NOT create graphql.http - that's the task target

    # A README for the api-tests project
    readme_content = """# API Test Collection

This directory contains HTTP request files for testing various API endpoints
using the REST Client extension for VSCode.

## Usage

1. Install the REST Client extension (`humao.rest-client`)
2. Open any `.http` file
3. Click "Send Request" above any request block

## Endpoints

- **REST API**: `https://api.example.com/v2`
- **GraphQL API**: `https://api.example.com/graphql`

## Files

- `users.http` - User management endpoints
- `auth.http` - Authentication flows
"""
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme_content)

    # An existing REST Client file for user endpoints
    users_http = """# User Management API Tests
# Base URL: https://api.example.com/v2

### Get all users
GET https://api.example.com/v2/users
Authorization: Bearer {{auth_token}}

### Get user by ID
GET https://api.example.com/v2/users/42
Authorization: Bearer {{auth_token}}

### Create a new user
POST https://api.example.com/v2/users
Content-Type: application/json
Authorization: Bearer {{auth_token}}

{
    "name": "Elena Rodriguez",
    "email": "elena.rodriguez@example.com",
    "role": "developer"
}

### Update user email
PATCH https://api.example.com/v2/users/42
Content-Type: application/json
Authorization: Bearer {{auth_token}}

{
    "email": "elena.r@newdomain.com"
}

### Delete user
DELETE https://api.example.com/v2/users/42
Authorization: Bearer {{auth_token}}
"""
    with open(os.path.join(PROJECT_DIR, 'users.http'), 'w') as f:
        f.write(users_http)

    # An existing REST Client file for auth endpoints
    auth_http = """# Authentication API Tests
# Base URL: https://api.example.com/v2/auth

### Login with credentials
POST https://api.example.com/v2/auth/login
Content-Type: application/json

{
    "username": "developer@example.com",
    "password": "securePassword123"
}

### Refresh token
POST https://api.example.com/v2/auth/refresh
Content-Type: application/json

{
    "refresh_token": "{{refresh_token}}"
}

### Logout
POST https://api.example.com/v2/auth/logout
Authorization: Bearer {{auth_token}}
"""
    with open(os.path.join(PROJECT_DIR, 'auth.http'), 'w') as f:
        f.write(auth_http)

    # Verify graphql.http does NOT exist
    graphql_path = os.path.join(PROJECT_DIR, 'graphql.http')
    if os.path.exists(graphql_path):
        os.remove(graphql_path)

    print(f'Initial project directory created: {PROJECT_DIR}')
    print(f'Files: {os.listdir(PROJECT_DIR)}')

    # Open VSCode with the project directory
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
