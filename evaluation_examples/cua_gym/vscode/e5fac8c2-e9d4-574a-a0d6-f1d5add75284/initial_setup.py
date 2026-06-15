"""
Initial Setup: Format only the SQL query string inside the getUsers function
Task ID: vscode_code_007
Domain: vs_code

Creates /home/user/project/db.js with an unformatted single-line SQL template literal
inside the getUsers function, then opens the file in VSCode.
"""

import os
import json
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_007'
PROJECT_DIR = f'{WORKDIR}/project'
OUTPUT = f'{PROJECT_DIR}/db.js'


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

    # The initial file content — SQL query is a single-line template literal (unformatted)
    # This matches exactly the context specification
    content = "const db = require('./database');\n\nasync function getUsers() {\n  const query = `SELECT u.id,u.name,u.email,p.role,p.department FROM users u INNER JOIN profiles p ON u.id=p.user_id WHERE u.active=true AND p.department IN ('engineering','product','design') ORDER BY u.name ASC LIMIT 100`;\n  return db.execute(query);\n}\n\nmodule.exports = { getUsers };\n"

    with open(OUTPUT, 'w') as f:
        f.write(content)
    print(f'Initial file created: {OUTPUT}')

    # Create a stub database.js so VSCode doesn't show import errors
    database_js_content = "const { Pool } = require('pg');\n\nconst pool = new Pool({\n  host: process.env.DB_HOST || 'localhost',\n  port: process.env.DB_PORT || 5432,\n  database: process.env.DB_NAME || 'userdb',\n  user: process.env.DB_USER || 'postgres',\n  password: process.env.DB_PASSWORD || '',\n});\n\nmodule.exports = {\n  execute: (query, params = []) => pool.query(query, params),\n};\n"
    database_js_path = f'{PROJECT_DIR}/database.js'
    with open(database_js_path, 'w') as f:
        f.write(database_js_content)
    print(f'database.js created: {database_js_path}')

    # Create package.json for a realistic Node.js project structure
    package_json = {
        "name": "user-service",
        "version": "1.0.0",
        "description": "User management service",
        "main": "index.js",
        "scripts": {
            "start": "node index.js",
            "test": "jest"
        },
        "dependencies": {
            "pg": "^8.11.0"
        },
        "devDependencies": {
            "jest": "^29.0.0"
        }
    }
    package_json_path = f'{PROJECT_DIR}/package.json'
    with open(package_json_path, 'w') as f:
        json.dump(package_json, f, indent=2)
        f.write('\n')
    print(f'package.json created: {package_json_path}')

    # GUI-ready startup: open VSCode with the specific db.js file
    launch_gui(f'code "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
