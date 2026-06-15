"""
Initial Setup: Extract IP addresses from tab-separated log file using VSCode column selection
Task ID: vscode_edit_059
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user/Desktop'
TASK_ID = 'vscode_edit_059'
LOG_FILE = f'{WORKDIR}/access.log'

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
    os.makedirs(WORKDIR, exist_ok=True)

    # 20-line tab-separated access log: timestamp, method, IP, status, response_time_ms
    log_lines = [
        "2025-03-01 08:12:04\tGET\t192.168.1.101\t200\t134",
        "2025-03-01 08:14:22\tPOST\t10.0.0.47\t201\t287",
        "2025-03-01 08:17:09\tGET\t172.16.5.23\t200\t98",
        "2025-03-01 08:20:45\tDELETE\t192.168.2.88\t204\t312",
        "2025-03-01 08:23:11\tGET\t10.10.1.15\t404\t45",
        "2025-03-01 08:26:53\tPUT\t172.31.0.200\t200\t521",
        "2025-03-01 08:29:30\tGET\t192.168.1.101\t200\t112",
        "2025-03-01 08:32:17\tPOST\t10.0.0.55\t400\t67",
        "2025-03-01 08:35:44\tGET\t172.16.8.9\t200\t199",
        "2025-03-01 08:38:02\tGET\t10.0.0.47\t200\t88",
        "2025-03-01 08:41:29\tPUT\t192.168.3.142\t200\t445",
        "2025-03-01 08:44:55\tGET\t172.16.5.23\t301\t33",
        "2025-03-01 08:47:18\tPOST\t10.20.1.77\t201\t376",
        "2025-03-01 08:50:34\tGET\t192.168.1.200\t200\t153",
        "2025-03-01 08:53:07\tDELETE\t172.31.4.18\t204\t289",
        "2025-03-01 08:56:43\tGET\t10.0.0.47\t200\t104",
        "2025-03-01 08:59:21\tPOST\t192.168.5.66\t500\t1203",
        "2025-03-01 09:02:48\tGET\t172.16.2.34\t200\t77",
        "2025-03-01 09:05:15\tPUT\t10.0.1.99\t200\t331",
        "2025-03-01 09:08:39\tGET\t192.168.1.101\t200\t118",
    ]

    with open(LOG_FILE, 'w') as f:
        f.write('\n'.join(log_lines) + '\n')

    print(f'Initial log file created: {LOG_FILE}')

    # GUI-ready startup: open VSCode with the log file
    launch_gui(f'code "{LOG_FILE}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with access.log using DISPLAY=:0')

create_initial()
