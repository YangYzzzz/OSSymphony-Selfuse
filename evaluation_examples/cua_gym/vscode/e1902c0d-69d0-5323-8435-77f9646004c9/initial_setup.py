"""
Initial Setup: Multi-cursor editing workflow with fetchData deprecation
Task ID: vscode_code_100
Domain: vs_code

Creates a TypeScript project with legacy.ts, api.ts, and dashboard.ts.
The fetchData function has NOT yet been renamed or marked deprecated.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_100'
PROJECT_DIR = f'{WORKDIR}/project'


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

    # --- legacy.ts: contains fetchData (NOT yet deprecated/renamed) ---
    legacy_content = """\
export function fetchData(url: string): Promise<any> {
  return fetch(url).then(res => res.json());
}

export function fetchDataV2(url: string, options?: RequestInit): Promise<any> {
  return fetch(url, { ...options, headers: { 'Content-Type': 'application/json', ...options?.headers } }).then(res => res.json());
}
"""
    with open(f'{PROJECT_DIR}/legacy.ts', 'w') as f:
        f.write(legacy_content)
    print(f'Created: {PROJECT_DIR}/legacy.ts')

    # --- api.ts: imports and calls fetchData ---
    api_content = """\
import { fetchData } from './legacy';

export async function getUsers() {
  return fetchData('/api/users');
}

export async function getProducts() {
  return fetchData('/api/products');
}
"""
    with open(f'{PROJECT_DIR}/api.ts', 'w') as f:
        f.write(api_content)
    print(f'Created: {PROJECT_DIR}/api.ts')

    # --- dashboard.ts: imports and calls fetchData ---
    dashboard_content = """\
import { fetchData } from './legacy';

export async function loadDashboard() {
  const stats = await fetchData('/api/stats');
  const notifications = await fetchData('/api/notifications');
  return { stats, notifications };
}
"""
    with open(f'{PROJECT_DIR}/dashboard.ts', 'w') as f:
        f.write(dashboard_content)
    print(f'Created: {PROJECT_DIR}/dashboard.ts')

    # --- tsconfig.json for TypeScript project context ---
    tsconfig_content = """\
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020", "DOM"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "./dist"
  },
  "include": ["**/*.ts"],
  "exclude": ["node_modules", "dist"]
}
"""
    with open(f'{PROJECT_DIR}/tsconfig.json', 'w') as f:
        f.write(tsconfig_content)
    print(f'Created: {PROJECT_DIR}/tsconfig.json')

    print('All initial files created successfully.')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    # Then open legacy.ts directly so the cursor is on fetchData
    time.sleep(1.0)
    launch_gui(f'code "{PROJECT_DIR}/legacy.ts"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with project folder and legacy.ts — DISPLAY=:0')


create_initial()
