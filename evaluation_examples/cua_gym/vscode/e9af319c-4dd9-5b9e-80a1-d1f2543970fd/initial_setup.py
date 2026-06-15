"""
Initial Setup: Extract selected code into a new method called 'buildQueryString' in TypeScript class.
Task ID: vscode_rrt_051
Domain: vscode

Creates the initial ApiClient.ts file with inline query string building in the search method.
VSCode is opened with the file ready for the agent to perform the extract-method refactoring.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_051'
PROJECT_DIR = f'{WORKDIR}/projects/api'
OUTPUT = f'{PROJECT_DIR}/ApiClient.ts'


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

    # Write the initial TypeScript file with inline query string building
    content = '''\
class ApiClient {
    private baseUrl: string;

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
    }

    async search(params: Record<string, string>) {
        const parts: string[] = [];
        for (const [key, value] of Object.entries(params)) {
            parts.push(`${encodeURIComponent(key)}=${encodeURIComponent(value)}`);
        }
        const queryString = parts.join('&');
        const url = `${this.baseUrl}/search?${queryString}`;
        return fetch(url);
    }
}
'''
    with open(OUTPUT, 'w') as f:
        f.write(content)

    print(f'Initial file created: {OUTPUT}')

    # Also create a tsconfig.json so VSCode recognizes it as a TS project
    tsconfig = '''\
{
    "compilerOptions": {
        "target": "ES2020",
        "module": "commonjs",
        "strict": true,
        "esModuleInterop": true,
        "outDir": "./dist",
        "rootDir": "./",
        "lib": ["ES2020", "DOM"]
    },
    "include": ["./**/*.ts"]
}
'''
    tsconfig_path = f'{PROJECT_DIR}/tsconfig.json'
    with open(tsconfig_path, 'w') as f:
        f.write(tsconfig)

    print(f'tsconfig.json created: {tsconfig_path}')

    # Launch VSCode with the file open
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
