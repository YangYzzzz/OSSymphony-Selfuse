"""
Reward Script: MySQL Replication Slave Configuration
Task ID: os_adm_034
Domain: os (MySQL administration)
Scoring:
  Component 1 (0.25): SHOW SLAVE STATUS returns results (replication configured)
  Component 2 (0.25): Master_Host is 10.0.0.10
  Component 3 (0.25): Master_User is repl_user and Master_Port is 3306
  Component 4 (0.25): START SLAVE was executed (Slave_SQL_Running = Yes, Slave_IO not "No")
"""

import subprocess
import re


def run_mysql_query(query):
    """Run a MySQL query via sudo and return stdout."""
    result = subprocess.run(
        ["sudo", "-S", "mysql", "-e", query],
        input="password\n",
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout, result.stderr, result.returncode


def parse_slave_status(output):
    """Parse SHOW SLAVE STATUS\\G output into a dict."""
    status = {}
    for line in output.strip().split('\n'):
        line = line.strip()
        if ':' in line and not line.startswith('*'):
            key, _, value = line.partition(':')
            status[key.strip()] = value.strip()
    return status


def verify_task():
    """
    Verify MySQL replication slave configuration.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # First, check if MySQL is running at all (precondition gate)
    try:
        stdout, stderr, rc = run_mysql_query("SELECT 1;")
        if rc != 0:
            print(f"CRITICAL: Cannot connect to MySQL: {stderr}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: MySQL connection failed: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get SHOW SLAVE STATUS output
    try:
        stdout, stderr, rc = run_mysql_query("SHOW SLAVE STATUS\\G")
        slave_status = parse_slave_status(stdout)
    except Exception as e:
        print(f"CRITICAL: Could not run SHOW SLAVE STATUS: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Replication is configured (SHOW SLAVE STATUS returns data) (0.25 pts)
    # In initial_env, SHOW SLAVE STATUS returns empty (no replication configured)
    # In golden_env, it returns a full status block
    try:
        if slave_status and 'Master_Host' in slave_status:
            print(f"PASS: Component 1 - Replication is configured (SHOW SLAVE STATUS has data) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 - SHOW SLAVE STATUS returned no data (replication not configured)")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Master_Host is 10.0.0.10 (0.25 pts)
    try:
        master_host = slave_status.get('Master_Host', '')
        if master_host == '10.0.0.10':
            print(f"PASS: Component 2 - Master_Host is 10.0.0.10 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 - Expected Master_Host=10.0.0.10, found: '{master_host}'")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Master_User is repl_user AND Master_Port is 3306 (0.25 pts)
    try:
        master_user = slave_status.get('Master_User', '')
        master_port = slave_status.get('Master_Port', '')
        user_ok = (master_user == 'repl_user')
        port_ok = (str(master_port) == '3306')
        if user_ok and port_ok:
            print(f"PASS: Component 3 - Master_User=repl_user, Master_Port=3306 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 - Master_User='{master_user}' (expect repl_user), Master_Port='{master_port}' (expect 3306)")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: START SLAVE was executed (0.25 pts)
    # Slave_SQL_Running should be "Yes"
    # Slave_IO_Running should NOT be "No" (it may be "Yes" or "Connecting" if master is unreachable)
    try:
        sql_running = slave_status.get('Slave_SQL_Running', 'No')
        io_running = slave_status.get('Slave_IO_Running', 'No')
        sql_ok = (sql_running == 'Yes')
        io_started = (io_running != 'No')  # "Yes" or "Connecting" both count
        if sql_ok and io_started:
            print(f"PASS: Component 4 - START SLAVE executed (SQL_Running={sql_running}, IO_Running={io_running}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 - Slave_SQL_Running='{sql_running}', Slave_IO_Running='{io_running}' (expected SQL=Yes, IO!=No)")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
