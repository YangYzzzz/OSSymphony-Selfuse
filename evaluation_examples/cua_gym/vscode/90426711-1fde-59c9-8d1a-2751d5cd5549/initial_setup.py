"""
Initial Setup: Open ~/Desktop/notes.md in VSCode and prepare for line 8 selection task.
Task ID: vscode_edit_005
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_005'
DESKTOP = f'{WORKDIR}/Desktop'
OUTPUT = f'{DESKTOP}/notes.md'


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
    os.makedirs(DESKTOP, exist_ok=True)

    # 30-line Markdown notes file with realistic content.
    # Line 8 (1-indexed) MUST be: "- Review pull request #42 before Friday"
    content = """\
# Project Notes — March 2025

## Upcoming Deadlines

- Submit quarterly budget report by March 20
- Finalize onboarding docs for new hires
- Schedule retrospective meeting for Sprint 14
- Review pull request #42 before Friday
- Update CI/CD pipeline configuration
- Respond to client feedback on demo v2.3

## Team Updates

- Alice is OOO March 18-22; coordinate coverage
- Bob joined the backend team on March 10
- Conduct 1:1 with Marcus on Thursday at 3 PM
- Ping design team about new icon assets

## Infrastructure Tasks

- Migrate staging DB to new region by end of month
- Rotate API keys for production services
- Enable 2FA enforcement across all admin accounts
- Archive old S3 buckets from 2023 projects
- Review CloudWatch alarm thresholds

## Miscellaneous

- Book travel for conference April 5-7
- Read through RFC-0031 before Wednesday
"""

    with open(OUTPUT, 'w') as f:
        f.write(content)

    print(f'Initial file created: {OUTPUT}')

    # Verify line count and line 8 content
    file_lines = content.splitlines()
    print(f'Total lines: {len(file_lines)}')
    print(f'Line 8: {repr(file_lines[7])}')

    # GUI-ready startup: open notes.md in VSCode
    launch_gui(f'code "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with notes.md using DISPLAY=:0')


create_initial()
