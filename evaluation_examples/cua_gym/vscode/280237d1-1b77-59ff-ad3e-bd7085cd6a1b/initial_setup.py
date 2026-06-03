"""
Initial Setup: Create settings.ini with three sections for VSCode Find and Replace task
Task ID: vscode_edit_066
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_066'
DESKTOP = f'{WORKDIR}/Desktop'
OUTPUT = f'{DESKTOP}/settings.ini'


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
    # Ensure Desktop directory exists
    os.makedirs(DESKTOP, exist_ok=True)

    # 40-line INI file matching context spec:
    # [development] lines 1-12
    # blank line 13
    # [testing] lines 14-26
    # blank line 27
    # [production] lines 28-40
    # Each section: header + 4 key-value pairs + comment lines
    # Values in [production] must NOT be REDACTED (task requires changing them)

    content = (
        '[development]\n'
        'database_url = postgres://dev-db.internal:5432/appdb_dev\n'
        'api_key = dev_api_key_a3f82bc91d4e\n'
        'debug_mode = true\n'
        'log_level = DEBUG\n'
        '; Development environment: local machines and CI runners\n'
        '; Connects to the shared development database cluster\n'
        '; Full debug logging enabled for troubleshooting\n'
        '; Secrets rotation: every 90 days\n'
        '; Contact: platform-team@example.com\n'
        '; Last modified: 2025-11-10 by devops\n'
        '; Do not use production credentials here\n'
        '\n'
        '[testing]\n'
        'database_url = postgres://test-db.internal:5432/appdb_test\n'
        'api_key = test_api_key_7c6d2ef04a91\n'
        'debug_mode = true\n'
        'log_level = INFO\n'
        '; Testing environment: automated QA and integration pipelines\n'
        '; Isolated database reset before each full test run\n'
        '; Info-level logging for test result traceability\n'
        '; Secrets rotation: every 60 days\n'
        '; Contact: qa-team@example.com\n'
        '; Last modified: 2025-11-12 by ci-bot\n'
        '; Do not use production credentials here\n'
        '; Managed by Terraform config module testing-infra\n'
        '\n'
        '[production]\n'
        'database_url = postgres://prod-db.internal:5432/appdb_prod\n'
        'api_key = prod_api_key_9b1e3dc57f28\n'
        'debug_mode = false\n'
        'log_level = WARNING\n'
        '; Production environment: live customer-facing service\n'
        '; High-availability PostgreSQL cluster with read replicas\n'
        '; Minimal logging to reduce I/O overhead\n'
        '; Secrets rotation: every 30 days\n'
        '; Contact: sre-team@example.com\n'
        '; Last modified: 2025-10-28 by sre-lead\n'
        '; Restricted: ops team access only\n'
        '; Managed by Terraform config module production-infra\n'
    )

    with open(OUTPUT, 'w') as f:
        f.write(content)

    # Verify line count
    with open(OUTPUT, 'r') as f:
        lines = f.readlines()
    print(f'Initial file created: {OUTPUT} ({len(lines)} lines)')

    # GUI-ready startup: open VSCode with the settings.ini file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with settings.ini using DISPLAY=:0')


create_initial()
