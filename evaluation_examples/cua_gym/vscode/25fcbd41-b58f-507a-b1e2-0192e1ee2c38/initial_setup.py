"""
Initial Setup: Replace print() with logging.info() in a Python debugging exercise
Task ID: vscode_stu_029
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_029'
OUTPUT = f'{WORKDIR}/debug_exercise.py'


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
    content = '''\
#!/usr/bin/env python3
"""
debug_exercise.py - Student Debugging Assignment
Course: CS201 - Software Engineering
Author: Emily Rodriguez
Date: 2025-09-14

Exercise: Analyze server request logs and report anomalies.
"""

import os
import sys
import datetime
from collections import defaultdict


REQUEST_LOG = [
    {"timestamp": "2025-09-14 08:12:33", "endpoint": "/api/users", "status": 200, "latency_ms": 45},
    {"timestamp": "2025-09-14 08:13:01", "endpoint": "/api/orders", "status": 500, "latency_ms": 3200},
    {"timestamp": "2025-09-14 08:14:22", "endpoint": "/api/users", "status": 200, "latency_ms": 52},
    {"timestamp": "2025-09-14 08:15:47", "endpoint": "/api/products", "status": 404, "latency_ms": 12},
    {"timestamp": "2025-09-14 08:16:05", "endpoint": "/api/orders", "status": 200, "latency_ms": 89},
    {"timestamp": "2025-09-14 08:17:30", "endpoint": "/api/auth/login", "status": 401, "latency_ms": 150},
    {"timestamp": "2025-09-14 08:18:55", "endpoint": "/api/orders", "status": 500, "latency_ms": 4500},
    {"timestamp": "2025-09-14 08:19:12", "endpoint": "/api/users", "status": 200, "latency_ms": 38},
    {"timestamp": "2025-09-14 08:20:44", "endpoint": "/api/products", "status": 200, "latency_ms": 67},
    {"timestamp": "2025-09-14 08:21:59", "endpoint": "/api/auth/login", "status": 200, "latency_ms": 112},
    {"timestamp": "2025-09-14 08:23:10", "endpoint": "/api/orders", "status": 200, "latency_ms": 95},
    {"timestamp": "2025-09-14 08:24:38", "endpoint": "/api/users", "status": 503, "latency_ms": 8100},
]

LATENCY_THRESHOLD_MS = 1000


def analyze_requests(log_entries):
    """Analyze request log entries and report findings."""
    error_counts = defaultdict(int)
    slow_requests = []
    endpoint_hits = defaultdict(int)

    print(f"Starting analysis of {len(log_entries)} log entries")

    for entry in log_entries:
        endpoint = entry["endpoint"]
        status = entry["status"]
        latency = entry["latency_ms"]
        endpoint_hits[endpoint] += 1

        if status >= 400:
            error_counts[status] += 1
            print(f"Error detected: {endpoint} returned {status} at {entry['timestamp']}")

        if latency > LATENCY_THRESHOLD_MS:
            slow_requests.append(entry)
            print(f"Slow request: {endpoint} took {latency}ms at {entry['timestamp']}")

    return error_counts, slow_requests, endpoint_hits


def generate_report(error_counts, slow_requests, endpoint_hits):
    """Generate a summary report of the analysis."""
    print("=" * 60)
    print("SERVER REQUEST ANALYSIS REPORT")
    print("=" * 60)

    total_errors = sum(error_counts.values())
    print(f"Total errors found: {total_errors}")

    if error_counts:
        for status_code, count in sorted(error_counts.items()):
            pass  # individual status codes logged elsewhere

    if slow_requests:
        avg_latency = sum(r["latency_ms"] for r in slow_requests) / len(slow_requests)
        print(f"Slow requests (>{LATENCY_THRESHOLD_MS}ms): {len(slow_requests)}, avg latency: {avg_latency:.0f}ms")


def main():
    error_counts, slow_requests, endpoint_hits = analyze_requests(REQUEST_LOG)
    generate_report(error_counts, slow_requests, endpoint_hits)


if __name__ == "__main__":
    main()
'''

    os.makedirs(WORKDIR, exist_ok=True)
    with open(OUTPUT, 'w') as f:
        f.write(content)
    print(f'Initial file created: {OUTPUT}')

    # Open VSCode with the file
    launch_gui(f'code "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
