"""
Reward Script: Configure PgBouncer connection pooling for PostgreSQL
Task ID: os_adm_039
Domain: os (system administration)
Scoring:
  1. PgBouncer package installed (0.15 pts)
  2. PgBouncer service active/running (0.15 pts)
  3. listen_port = 6432 in config (0.15 pts)
  4. pool_mode = transaction in config (0.20 pts)
  5. default_pool_size = 25 in config (0.20 pts)
  6. databases section maps webapp_db to local PostgreSQL (0.15 pts)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'os_adm_039'
CONFIG_PATH = '/etc/pgbouncer/pgbouncer.ini'


def read_config_with_sudo():
    """Read pgbouncer.ini using sudo (file is owned by postgres with 640 perms)."""
    stream = os.popen('echo password | sudo -S cat /etc/pgbouncer/pgbouncer.ini 2>/dev/null')
    content = stream.read()
    stream.close()
    return content


def parse_ini_value(content, key):
    """Extract a value from INI-style config content."""
    pattern = rf'^\s*{re.escape(key)}\s*=\s*(.+?)\s*$'
    match = re.search(pattern, content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None


def verify_task():
    """
    Verify PgBouncer connection pooling configuration.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: PgBouncer package is installed (0.15 points)
    try:
        stream = os.popen('dpkg -l pgbouncer 2>&1')
        dpkg_output = stream.read()
        stream.close()
        if 'ii  pgbouncer' in dpkg_output:
            print(f"PASS: Component 1 — PgBouncer package is installed (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — PgBouncer package is not installed")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: PgBouncer service is active and running (0.15 points)
    try:
        stream = os.popen('systemctl is-active pgbouncer 2>&1')
        status = stream.read().strip()
        stream.close()
        if status == 'active':
            print(f"PASS: Component 2 — PgBouncer service is active (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — PgBouncer service status: {status}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Read config file for components 3-6
    config_content = ''
    try:
        config_content = read_config_with_sudo()
        if not config_content.strip():
            print(f"WARN: Config file is empty or unreadable")
    except Exception as e:
        print(f"ERROR: Cannot read config file: {e}")

    # Component 3: listen_port = 6432 (0.15 points)
    try:
        listen_port = parse_ini_value(config_content, 'listen_port')
        if listen_port and listen_port == '6432':
            print(f"PASS: Component 3 — listen_port = 6432 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — listen_port expected '6432', found: '{listen_port}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: pool_mode = transaction (0.20 points)
    try:
        pool_mode = parse_ini_value(config_content, 'pool_mode')
        if pool_mode and pool_mode.lower() == 'transaction':
            print(f"PASS: Component 4 — pool_mode = transaction (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — pool_mode expected 'transaction', found: '{pool_mode}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: default_pool_size = 25 (0.20 points)
    try:
        pool_size = parse_ini_value(config_content, 'default_pool_size')
        if pool_size and pool_size == '25':
            print(f"PASS: Component 5 — default_pool_size = 25 (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 5 — default_pool_size expected '25', found: '{pool_size}'")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: databases section maps webapp_db to local PostgreSQL (0.15 points)
    try:
        # Check that the [databases] section contains a webapp_db entry pointing to localhost:5432
        db_pattern = r'^\s*webapp_db\s*=\s*.*(?:host\s*=\s*127\.0\.0\.1|host\s*=\s*localhost).*(?:port\s*=\s*5432).*(?:dbname\s*=\s*webapp_db)'
        if re.search(db_pattern, config_content, re.MULTILINE):
            print(f"PASS: Component 6 — webapp_db mapped to local PostgreSQL (0.15 pts)")
            total_score += 0.15
        else:
            # Also check simpler pattern where dbname matches the key
            db_simple = r'^\s*webapp_db\s*=\s*.*'
            match = re.search(db_simple, config_content, re.MULTILINE)
            if match:
                line = match.group(0).strip()
                # Verify it references local postgres
                if ('127.0.0.1' in line or 'localhost' in line) and '5432' in line:
                    print(f"PASS: Component 6 — webapp_db mapped to local PostgreSQL (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 6 — webapp_db entry found but doesn't map to local PostgreSQL: {line}")
            else:
                print(f"FAIL: Component 6 — No webapp_db entry found in [databases] section")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
