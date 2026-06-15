"""
Initial Setup: Configure PostgreSQL connection pooling using PgBouncer
Task ID: os_adm_039
Domain: os (system administration)

Initial state: Install PostgreSQL 14, create webapp_db and webapp_user.
PgBouncer is NOT installed. Opens a terminal for the agent.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'os_adm_039'
SUDO_PASS = 'password'


def run_shell_script(script_content):
    """Write a shell script to /tmp and execute it with sudo."""
    # Write the script
    with open('/tmp/setup_script.sh', 'w') as f:
        f.write("#!/bin/bash\nset -e\n" + script_content)
    os.chmod('/tmp/setup_script.sh', 0o755)

    result = subprocess.run(
        f"echo '{SUDO_PASS}' | sudo -S bash /tmp/setup_script.sh",
        shell=True, capture_output=True, text=True
    )
    print(f"stdout: {result.stdout}")
    if result.returncode != 0:
        print(f"stderr: {result.stderr}")
    return result


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


def main():
    # Step 1: Install PostgreSQL
    print("=== Installing PostgreSQL ===")
    run_shell_script("""
apt-get update -qq
apt-get install -y postgresql postgresql-client
systemctl start postgresql
systemctl enable postgresql
sleep 2
systemctl is-active postgresql && echo "PostgreSQL is active"
""")

    # Step 2: Create database and user
    print("=== Setting up database ===")
    run_shell_script("""
su - postgres -c "psql -c \\"CREATE ROLE webapp_user WITH LOGIN PASSWORD 'webapp_pass123';\\"" 2>/dev/null || true
su - postgres -c "createdb -O webapp_user webapp_db" 2>/dev/null || true

# Find pg_hba.conf
HBA_FILE=$(su - postgres -c "psql -tc \\"SHOW hba_file;\\"" | tr -d ' ')
echo "HBA file: $HBA_FILE"

# Add md5 auth entries for webapp_user
if ! grep -q 'webapp_user' "$HBA_FILE"; then
    sed -i '1i\\host    webapp_db    webapp_user    127.0.0.1/32    md5' "$HBA_FILE"
    sed -i '1i\\local   webapp_db    webapp_user                     md5' "$HBA_FILE"
fi

# Set max_connections = 100
PG_CONF_DIR=$(dirname "$HBA_FILE")
PG_CONF="$PG_CONF_DIR/postgresql.conf"
sed -i "s/^#*max_connections.*/max_connections = 100/" "$PG_CONF"

systemctl restart postgresql
sleep 2
echo "Database setup done"
""")

    # Step 3: Ensure PgBouncer is NOT installed
    print("=== Ensuring PgBouncer not installed ===")
    run_shell_script("""
systemctl stop pgbouncer 2>/dev/null || true
apt-get remove -y pgbouncer 2>/dev/null || true
apt-get autoremove -y 2>/dev/null || true
which pgbouncer 2>/dev/null && echo "WARNING: PgBouncer still found" || echo "PgBouncer not installed - OK"
""")

    # Step 4: Verify PostgreSQL is working
    print("=== Verifying PostgreSQL ===")
    run_shell_script("""
su - postgres -c "psql -c \\"SELECT datname FROM pg_database WHERE datname='webapp_db';\\""
su - postgres -c "psql -c \\"SELECT rolname FROM pg_roles WHERE rolname='webapp_user';\\""
systemctl is-active postgresql && echo "PostgreSQL active - OK"
""")

    # Step 5: Create readme
    readme_content = """# PostgreSQL Connection Pooling Setup

## Current Problem
The web application (webapp_db) connects directly to PostgreSQL on port 5432.
During peak traffic, the application is hitting the max_connections=100 limit,
causing connection exhaustion errors.

## PostgreSQL Details
- Version: PostgreSQL 14
- Port: 5432
- Database: webapp_db
- User: webapp_user
- Password: webapp_pass123
- max_connections: 100

## Task
Configure PgBouncer for connection pooling to solve the connection exhaustion issue.
"""
    with open(f'{WORKDIR}/connection_pooling_task.txt', 'w') as f:
        f.write(readme_content)
    print(f"Task readme created at {WORKDIR}/connection_pooling_task.txt")

    # Step 6: Open terminal for the agent
    launch_gui('gnome-terminal', delay_sec=2.0)
    print('GUI_READY: launched terminal with DISPLAY=:0')
    print('Initial setup complete.')


main()
