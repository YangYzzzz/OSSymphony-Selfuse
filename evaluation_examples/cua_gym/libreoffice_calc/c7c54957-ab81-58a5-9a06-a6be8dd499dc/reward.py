"""
Reward Script: Install and configure Nginx as reverse proxy for Node.js app on port 3000
Task ID: os_adm_001
Domain: os (system administration)
Scoring:
  Component 1: Nginx package installed (0.20 pts)
  Component 2: Config file exists with correct server block (0.35 pts)
  Component 3: Symlink in sites-enabled (0.20 pts)
  Component 4: Nginx service active/running (0.15 pts)
  Component 5: Nginx service enabled at boot (0.10 pts)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'os_adm_001'

CONFIG_PATH = '/etc/nginx/sites-available/app.example.com'
SYMLINK_PATH = '/etc/nginx/sites-enabled/app.example.com'


def run_cmd(cmd):
    """Run a shell command and return stdout string."""
    stream = os.popen(cmd + " 2>&1")
    output = stream.read()
    rc = stream.close()
    # os.popen close() returns None on success (rc 0), else exit status
    returncode = 0 if rc is None else (rc >> 8)
    return output, returncode


def verify_task():
    """
    Verify Nginx reverse proxy setup with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Nginx package is installed (0.20 points)
    # This FAILS on initial (nginx not installed) -> PASSES on golden
    try:
        output, rc = run_cmd("dpkg -l nginx 2>/dev/null")
        if rc == 0 and 'ii  nginx' in output:
            print(f"PASS: Component 1 — Nginx package is installed (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Nginx package not installed (dpkg rc={rc})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Config file at /etc/nginx/sites-available/app.example.com
    # with correct server block: listen 80, server_name app.example.com,
    # proxy_pass http://localhost:3000 (0.35 points)
    # This FAILS on initial (file doesn't exist) -> PASSES on golden
    try:
        if os.path.isfile(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                content = f.read()

            checks_passed = 0
            total_checks = 3

            # Check 1: listen 80
            if re.search(r'listen\s+80\s*;', content):
                checks_passed += 1
                print(f"  PASS: Config has 'listen 80'")
            else:
                print(f"  FAIL: Config missing 'listen 80'")

            # Check 2: server_name app.example.com
            if re.search(r'server_name\s+app\.example\.com\s*;', content):
                checks_passed += 1
                print(f"  PASS: Config has 'server_name app.example.com'")
            else:
                print(f"  FAIL: Config missing 'server_name app.example.com'")

            # Check 3: proxy_pass http://localhost:3000
            if re.search(r'proxy_pass\s+http://localhost:3000\s*;', content):
                checks_passed += 1
                print(f"  PASS: Config has 'proxy_pass http://localhost:3000'")
            else:
                print(f"  FAIL: Config missing 'proxy_pass http://localhost:3000'")

            # Award proportional points based on how many sub-checks passed
            if checks_passed == total_checks:
                print(f"PASS: Component 2 — Config file has all required directives (0.35 pts)")
                total_score += 0.35
            elif checks_passed > 0:
                component_score = round(0.35 * (checks_passed / total_checks), 2)
                print(f"PARTIAL: Component 2 — {checks_passed}/{total_checks} directives ({component_score} pts)")
                total_score += component_score
            else:
                print(f"FAIL: Component 2 — No required directives found in config file")
        else:
            print(f"FAIL: Component 2 — Config file not found at {CONFIG_PATH}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Symlink /etc/nginx/sites-enabled/app.example.com
    # points to /etc/nginx/sites-available/app.example.com (0.20 points)
    # This FAILS on initial (no nginx dirs) -> PASSES on golden
    try:
        if os.path.islink(SYMLINK_PATH):
            target = os.readlink(SYMLINK_PATH)
            if target == CONFIG_PATH or os.path.realpath(SYMLINK_PATH) == os.path.realpath(CONFIG_PATH):
                print(f"PASS: Component 3 — Symlink correctly points to {target} (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — Symlink points to {target}, expected {CONFIG_PATH}")
        elif os.path.isfile(SYMLINK_PATH):
            print(f"FAIL: Component 3 — {SYMLINK_PATH} exists but is not a symlink")
        else:
            print(f"FAIL: Component 3 — Symlink not found at {SYMLINK_PATH}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Nginx service is active (running) (0.15 points)
    # This FAILS on initial (nginx not installed) -> PASSES on golden
    try:
        output, rc = run_cmd("systemctl is-active nginx")
        status = output.strip().split('\n')[0].strip()
        if status == 'active':
            print(f"PASS: Component 4 — Nginx service is active/running (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Nginx service status: '{status}', expected 'active'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Nginx service is enabled at boot (0.10 points)
    # This FAILS on initial (nginx not installed) -> PASSES on golden
    try:
        output, rc = run_cmd("systemctl is-enabled nginx")
        status = output.strip().split('\n')[0].strip()
        if status == 'enabled':
            print(f"PASS: Component 5 — Nginx service is enabled at boot (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — Nginx enabled status: '{status}', expected 'enabled'")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
