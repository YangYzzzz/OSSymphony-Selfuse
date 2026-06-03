"""
Initial Setup: Set up a complete code editing environment for a new TypeScript project
Task ID: vscode_code_095
Domain: vs_code

This script creates an empty workspace at /home/user/new-project with NO .vscode/settings.json.
The agent's task is to create and configure the settings file.
"""

import os
import shlex
import subprocess
import time
import shutil

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_095'
WORKSPACE_DIR = f'{WORKDIR}/new-project'


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
    # Create the workspace directory
    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # Remove any existing .vscode directory so initial state has no settings
    vscode_dir = os.path.join(WORKSPACE_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        shutil.rmtree(vscode_dir)

    # Create some basic TypeScript project files to make the workspace look realistic
    # package.json
    package_json = os.path.join(WORKSPACE_DIR, 'package.json')
    with open(package_json, 'w') as f:
        f.write('''{
  "name": "new-project",
  "version": "1.0.0",
  "description": "A new TypeScript project",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "ts-node src/index.ts"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/node": "^20.0.0"
  }
}
''')

    # tsconfig.json
    tsconfig_json = os.path.join(WORKSPACE_DIR, 'tsconfig.json')
    with open(tsconfig_json, 'w') as f:
        f.write('''{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
''')

    # src/index.ts
    src_dir = os.path.join(WORKSPACE_DIR, 'src')
    os.makedirs(src_dir, exist_ok=True)
    index_ts = os.path.join(src_dir, 'index.ts')
    with open(index_ts, 'w') as f:
        f.write('''import { greet } from './utils';

const name: string = 'World';
const message = greet(name);
console.log(message);
''')

    # src/utils.ts
    utils_ts = os.path.join(src_dir, 'utils.ts')
    with open(utils_ts, 'w') as f:
        f.write('''export function greet(name: string): string {
    return `Hello, ${name}!`;
}

export function formatDate(date: Date): string {
    return date.toISOString().split('T')[0];
}
''')

    # .gitignore
    gitignore = os.path.join(WORKSPACE_DIR, '.gitignore')
    with open(gitignore, 'w') as f:
        f.write('''node_modules/
dist/
*.js.map
.env
''')

    print(f'Workspace created: {WORKSPACE_DIR}')
    print(f'No .vscode/settings.json exists (agent must create it)')

    # GUI-ready startup: open VSCode with the workspace
    launch_gui(f'code "{WORKSPACE_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with workspace at DISPLAY=:0')


create_initial()
