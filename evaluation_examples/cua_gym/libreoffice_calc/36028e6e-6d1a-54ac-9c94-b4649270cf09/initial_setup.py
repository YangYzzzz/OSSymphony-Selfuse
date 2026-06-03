"""
Initial Setup: Log Analyzer Python Scripting Task
Task ID: osworld_multi_apps_vscode_run_capture_009
Domain: multi_apps / vscode
Description: Creates stub log_analyzer.py and server.log on Desktop, opens VSCode with the file.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_run_capture_009'
DESKTOP = f'{WORKDIR}/Desktop'


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

    # --- Create server.log with realistic Apache-format access log entries ---
    server_log_content = """\
192.168.1.10 - alice [15/Mar/2025:08:01:22 +0000] "GET /index.html HTTP/1.1" 200 2326
192.168.1.11 - bob [15/Mar/2025:08:01:45 +0000] "POST /api/login HTTP/1.1" 200 487
192.168.1.12 - carol [15/Mar/2025:08:02:03 +0000] "GET /dashboard HTTP/1.1" 200 8541
192.168.1.10 - alice [15/Mar/2025:08:02:17 +0000] "GET /static/main.css HTTP/1.1" 304 0
192.168.1.13 - dave [15/Mar/2025:08:03:05 +0000] "GET /api/users HTTP/1.1" 401 213
192.168.1.14 - eve [15/Mar/2025:08:03:28 +0000] "DELETE /api/users/5 HTTP/1.1" 403 189
192.168.1.15 - frank [15/Mar/2025:08:04:01 +0000] "GET /nonexistent HTTP/1.1" 404 512
192.168.1.11 - bob [15/Mar/2025:08:04:33 +0000] "GET /products HTTP/1.1" 200 15234
192.168.1.16 - grace [15/Mar/2025:08:05:02 +0000] "PUT /api/products/3 HTTP/1.1" 500 321
192.168.1.12 - carol [15/Mar/2025:08:05:44 +0000] "GET /api/orders HTTP/1.1" 200 6721
192.168.1.17 - heidi [15/Mar/2025:08:06:11 +0000] "POST /api/orders HTTP/1.1" 201 445
192.168.1.10 - alice [15/Mar/2025:08:06:55 +0000] "GET /reports HTTP/1.1" 200 19023
192.168.1.13 - dave [15/Mar/2025:08:07:30 +0000] "GET /admin HTTP/1.1" 403 201
192.168.1.18 - ivan [15/Mar/2025:08:08:03 +0000] "GET /api/metrics HTTP/1.1" 200 3421
192.168.1.15 - frank [15/Mar/2025:08:08:47 +0000] "POST /api/upload HTTP/1.1" 500 289
192.168.1.19 - judy [15/Mar/2025:08:09:15 +0000] "GET /profile HTTP/1.1" 200 4521
192.168.1.14 - eve [15/Mar/2025:08:09:52 +0000] "GET /api/config HTTP/1.1" 404 198
192.168.1.20 - karl [15/Mar/2025:08:10:21 +0000] "POST /api/login HTTP/1.1" 200 512
192.168.1.11 - bob [15/Mar/2025:08:10:48 +0000] "GET /logout HTTP/1.1" 302 0
192.168.1.16 - grace [15/Mar/2025:08:11:33 +0000] "GET /settings HTTP/1.1" 200 7234
"""

    log_path = f'{DESKTOP}/server.log'
    with open(log_path, 'w') as f:
        f.write(server_log_content)
    print(f'Created: {log_path}')

    # --- Create stub log_analyzer.py ---
    # The script has stub/incomplete parsing and calculation logic
    log_analyzer_content = '''\
#!/usr/bin/env python3
"""
log_analyzer.py - Analyzes server access logs to summarize HTTP status codes.

Usage:
    python3 log_analyzer.py > log_summary.txt
"""

import sys
import os
from collections import defaultdict

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'server.log')


def parse_status_code(line):
    """
    Parse a single Apache-format log line and return the HTTP status code.
    Apache log format: IP - user [timestamp] "METHOD /path HTTP/ver" STATUS size

    Returns:
        int: HTTP status code, or None if the line cannot be parsed.
    """
    # TODO: Implement parsing logic to extract the status code
    # Hint: The status code appears after the quoted request field
    pass


def count_status_codes(log_file):
    """
    Read the log file and count occurrences of each HTTP status code.

    Args:
        log_file (str): Path to the log file.

    Returns:
        dict: A dictionary mapping status code (int) to count (int).
    """
    counts = defaultdict(int)
    # TODO: Open log_file, iterate through lines, call parse_status_code,
    # and accumulate counts
    pass
    return counts


def calculate_error_rate(counts):
    """
    Calculate the error rate: (4xx + 5xx requests) / total requests.

    Args:
        counts (dict): Status code counts from count_status_codes().

    Returns:
        float: Error rate as a value between 0.0 and 1.0.
               Returns 0.0 if there are no log entries.
    """
    # TODO: Sum total requests, sum 4xx and 5xx requests, return error rate
    pass


def print_report(counts, error_rate):
    """Print a formatted summary report."""
    print("=== Server Log Summary Report ===")
    print()
    print("HTTP Status Code Counts:")
    for code in sorted(counts.keys()):
        print(f"  {code}: {counts[code]}")
    print()
    total = sum(counts.values())
    print(f"Total Requests: {total}")
    print(f"Error Rate (4xx+5xx): {error_rate:.2%}")


def main():
    if not os.path.exists(LOG_FILE):
        print(f"Error: Log file not found: {LOG_FILE}", file=sys.stderr)
        sys.exit(1)

    counts = count_status_codes(LOG_FILE)
    error_rate = calculate_error_rate(counts)
    print_report(counts, error_rate)


if __name__ == "__main__":
    main()
'''

    analyzer_path = f'{DESKTOP}/log_analyzer.py'
    with open(analyzer_path, 'w') as f:
        f.write(log_analyzer_content)
    print(f'Created: {analyzer_path}')

    # Make log_analyzer.py executable
    os.chmod(analyzer_path, 0o755)

    # Ensure log_summary.txt does NOT exist in initial state
    summary_path = f'{DESKTOP}/log_summary.txt'
    if os.path.exists(summary_path):
        os.remove(summary_path)
        print(f'Removed pre-existing: {summary_path}')

    # GUI-ready startup: open VSCode with log_analyzer.py
    launch_gui(f'code "{analyzer_path}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with log_analyzer.py and DISPLAY=:0')


create_initial()
