"""
Initial Setup: Cut line 7 from ~/Desktop/todo.txt and paste it at line 3.
Task ID: vscode_edit_016
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_016'
OUTPUT = f'{WORKDIR}/Desktop/todo.txt'


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
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    # 10-line todo list; line 7 is '- Urgent: fix production bug'
    lines = [
        '- Review project milestones for Q2\n',
        '- Schedule team sync meeting\n',
        '- Update documentation for API endpoints\n',
        '- Code review for pull request #42\n',
        '- Write unit tests for auth module\n',
        '- Send weekly status report to manager\n',
        '- Urgent: fix production bug\n',
        '- Deploy hotfix to staging server\n',
        '- Follow up on client feedback\n',
        '- Prepare demo for Friday presentation\n',
    ]

    with open(OUTPUT, 'w') as f:
        f.writelines(lines)

    print(f'Initial file created: {OUTPUT}')
    print(f'Total lines: {len(lines)}')

    # GUI-ready startup: open the file in VSCode
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with todo.txt using DISPLAY=:0')


create_initial()
