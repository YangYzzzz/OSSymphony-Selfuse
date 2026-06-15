"""
Initial Setup: Create nginx access log and /opt/scripts/ directory for log parser task
Task ID: os_gf1_031
Domain: os (scripting)
"""

import os
import shlex
import subprocess
import time
import random

WORKDIR = '/home/user'
TASK_ID = 'os_gf1_031'

def sudo_run(cmd: str):
    """Run a command with sudo using password from stdin."""
    subprocess.run(f"echo 'password' | sudo -S {cmd}", shell=True, check=True,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
    # 1. Ensure /opt/scripts/ directory exists (empty — no script yet)
    sudo_run('mkdir -p /opt/scripts')
    sudo_run('chmod 755 /opt/scripts')
    print('Created /opt/scripts/ directory')

    # 2. Create /var/log/nginx/ directory and a realistic access.log
    sudo_run('mkdir -p /var/log/nginx')

    # Generate a realistic nginx combined-format access log
    ips = [
        '192.168.1.42', '10.0.0.15', '172.16.8.201', '203.0.113.55',
        '198.51.100.12', '192.168.5.88', '10.10.20.30', '172.20.0.99',
        '203.0.113.100', '198.51.100.77', '192.168.10.5', '10.0.2.15',
        '172.16.0.44', '203.0.113.210', '198.51.100.33',
    ]

    paths = [
        '/', '/index.html', '/about', '/contact', '/api/v1/users',
        '/api/v1/products', '/api/v1/orders', '/static/css/main.css',
        '/static/js/app.js', '/static/images/logo.png', '/login',
        '/dashboard', '/api/v1/auth/token', '/health', '/favicon.ico',
        '/api/v1/search?q=widget', '/products/detail/42', '/cart',
        '/checkout', '/api/v1/inventory', '/docs', '/robots.txt',
        '/sitemap.xml', '/admin', '/api/v1/reports/monthly',
        '/nonexistent-page', '/old-link', '/broken/resource',
        '/api/v1/missing-endpoint', '/uploads/../etc/passwd',
    ]

    methods = ['GET', 'POST', 'PUT', 'DELETE', 'GET', 'GET', 'GET', 'GET']
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'curl/8.4.0',
        'python-requests/2.31.0',
        'Googlebot/2.1 (+http://www.google.com/bot.html)',
    ]
    referrers = [
        '-', 'https://www.google.com/', 'https://example.com/',
        'https://news.ycombinator.com/', '-', '-', '-',
    ]

    # Status code distribution (realistic):
    status_weights = [
        (200, 1523), (301, 85), (304, 210), (400, 32),
        (401, 18), (403, 25), (404, 47), (500, 12), (502, 8),
    ]

    log_lines = []
    random.seed(42)  # Deterministic for reproducibility

    for status_code, count in status_weights:
        for i in range(count):
            ip = random.choice(ips)
            method = random.choice(methods)
            path = random.choice(paths)
            ua = random.choice(user_agents)
            ref = random.choice(referrers)
            size = random.randint(200, 50000)
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            day = random.randint(14, 16)

            timestamp = f'{day}/Mar/2025:{hour:02d}:{minute:02d}:{second:02d} +0000'
            line = f'{ip} - - [{timestamp}] "{method} {path} HTTP/1.1" {status_code} {size} "{ref}" "{ua}"'
            log_lines.append((hour, minute, second, day, line))

    # Sort by time for realism
    log_lines.sort(key=lambda x: (x[3], x[0], x[1], x[2]))
    log_content = '\n'.join(entry[4] for entry in log_lines) + '\n'

    # Write to temp file, then copy with sudo
    with open('/tmp/access.log', 'w') as f:
        f.write(log_content)
    sudo_run('cp /tmp/access.log /var/log/nginx/access.log')
    sudo_run('chmod 644 /var/log/nginx/access.log')
    os.remove('/tmp/access.log')

    total_lines = len(log_lines)
    print(f'Created /var/log/nginx/access.log with {total_lines} entries')

    # 3. Open a terminal for the user to work in
    launch_gui('gnome-terminal', delay_sec=1.5)
    print('GUI_READY: launched gnome-terminal with DISPLAY=:0')

create_initial()
