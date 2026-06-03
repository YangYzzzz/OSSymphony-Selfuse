"""
Initial Setup: Create a Python package project with .env file, no launch.json
Task ID: vscode_py_040
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_040'
WORKSPACE = f'{WORKDIR}/workspace'

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
    # Create workspace directory
    os.makedirs(WORKSPACE, exist_ok=True)

    # Create mypackage directory with __init__.py and __main__.py
    pkg_dir = os.path.join(WORKSPACE, 'mypackage')
    os.makedirs(pkg_dir, exist_ok=True)

    # __init__.py
    with open(os.path.join(pkg_dir, '__init__.py'), 'w') as f:
        f.write('"""MyPackage - A data processing toolkit for analytics pipelines."""\n\n'
                '__version__ = "1.2.0"\n'
                '__author__ = "Sarah Chen"\n')

    # __main__.py
    with open(os.path.join(pkg_dir, '__main__.py'), 'w') as f:
        f.write('"""Entry point for running mypackage as a module: python -m mypackage"""\n\n'
                'import os\n'
                'import sys\n\n'
                'from mypackage import __version__\n\n\n'
                'def main():\n'
                '    db_url = os.environ.get("DATABASE_URL", "")\n'
                '    api_key = os.environ.get("API_KEY", "")\n\n'
                '    if not db_url:\n'
                '        print("WARNING: DATABASE_URL not set", file=sys.stderr)\n'
                '    if not api_key:\n'
                '        print("WARNING: API_KEY not set", file=sys.stderr)\n\n'
                '    print(f"MyPackage v{__version__} starting...")\n'
                '    print(f"Database: {db_url[:20]}..." if db_url else "Database: not configured")\n'
                '    print("Pipeline initialized successfully.")\n\n\n'
                'if __name__ == "__main__":\n'
                '    main()\n')

    # Additional module file for realism
    with open(os.path.join(pkg_dir, 'pipeline.py'), 'w') as f:
        f.write('"""Core data pipeline module."""\n\n'
                'import os\n'
                'from typing import Dict, List, Optional\n\n\n'
                'class DataPipeline:\n'
                '    """Manages ETL operations for analytics data."""\n\n'
                '    def __init__(self, db_url: str, api_key: str):\n'
                '        self.db_url = db_url\n'
                '        self.api_key = api_key\n'
                '        self._connected = False\n\n'
                '    def connect(self) -> bool:\n'
                '        """Establish database connection."""\n'
                '        if not self.db_url:\n'
                '            raise ValueError("DATABASE_URL is required")\n'
                '        self._connected = True\n'
                '        return True\n\n'
                '    def fetch_records(self, table: str, limit: int = 100) -> List[Dict]:\n'
                '        """Fetch records from the specified table."""\n'
                '        if not self._connected:\n'
                '            raise RuntimeError("Not connected. Call connect() first.")\n'
                '        return []\n\n'
                '    def transform(self, records: List[Dict], mapping: Optional[Dict] = None) -> List[Dict]:\n'
                '        """Apply transformations to records."""\n'
                '        if mapping is None:\n'
                '            return records\n'
                '        return [{mapping.get(k, k): v for k, v in r.items()} for r in records]\n')

    # Create .env file at workspace root
    with open(os.path.join(WORKSPACE, '.env'), 'w') as f:
        f.write('# Environment variables for mypackage\n'
                'DATABASE_URL=postgresql://admin:secretpass@db.analytics-prod.internal:5432/warehouse\n'
                'API_KEY=sk-prod-a3f8b2c1d4e5f67890abcdef12345678\n')

    # Create a simple README for realism
    with open(os.path.join(WORKSPACE, 'README.md'), 'w') as f:
        f.write('# MyPackage\n\n'
                'A data processing toolkit for analytics pipelines.\n\n'
                '## Running\n\n'
                '```bash\n'
                'python -m mypackage\n'
                '```\n\n'
                '## Configuration\n\n'
                'Set environment variables in `.env`:\n'
                '- `DATABASE_URL` - PostgreSQL connection string\n'
                '- `API_KEY` - API authentication key\n')

    # Ensure NO .vscode/launch.json exists (this is what the task asks to create)
    vscode_dir = os.path.join(WORKSPACE, '.vscode')
    launch_json = os.path.join(vscode_dir, 'launch.json')
    if os.path.exists(launch_json):
        os.remove(launch_json)

    print(f'Initial workspace created: {WORKSPACE}')
    print(f'  mypackage/__init__.py')
    print(f'  mypackage/__main__.py')
    print(f'  mypackage/pipeline.py')
    print(f'  .env')
    print(f'  README.md')
    print(f'  NO .vscode/launch.json (task target)')

    # Launch VSCode with the workspace folder
    launch_gui(f'code "{WORKSPACE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
