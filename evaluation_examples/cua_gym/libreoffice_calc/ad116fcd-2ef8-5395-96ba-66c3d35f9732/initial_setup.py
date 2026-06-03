"""
Initial Setup: PostgreSQL backup script and cron scheduling
Task ID: os_adm_030
Domain: os (system administration)

Sets up the initial state:
- Ensures PostgreSQL is installed and running with sample databases
- Creates /backup/postgres/ directory
- Ensures no backup script exists at /usr/local/bin/pg_backup.sh
- Ensures no cron entries for pg_backup
- Opens a terminal window for the user
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'


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


def sudo_run(cmd):
    """Run a command with sudo."""
    full = f"echo 'password' | sudo -S {cmd}"
    r = subprocess.run(full, shell=True, capture_output=True, text=True)
    return r


def setup_initial():
    # Write a setup script to handle all privileged operations
    setup_script = r'''#!/bin/bash
set -e

# Install PostgreSQL and cron
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq postgresql postgresql-client cron 2>/dev/null

# Start PostgreSQL
systemctl start postgresql
systemctl enable postgresql
sleep 2

# Create sample databases
su - postgres -c "psql -c \"CREATE DATABASE inventory_db;\"" 2>/dev/null || true
su - postgres -c "psql -c \"CREATE DATABASE hr_records;\"" 2>/dev/null || true
su - postgres -c "psql -c \"CREATE DATABASE analytics;\"" 2>/dev/null || true

# Add data to inventory_db
su - postgres -c "psql -d inventory_db" <<'EOSQL'
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2),
    stock INTEGER
);
INSERT INTO products (name, category, price, stock) VALUES
    ('Wireless Mouse', 'Electronics', 29.99, 150),
    ('USB-C Hub', 'Electronics', 49.95, 85),
    ('Standing Desk', 'Furniture', 399.00, 22),
    ('Monitor Arm', 'Furniture', 79.50, 64),
    ('Mechanical Keyboard', 'Electronics', 129.00, 43)
ON CONFLICT DO NOTHING;
EOSQL

# Add data to hr_records
su - postgres -c "psql -d hr_records" <<'EOSQL'
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50),
    hire_date DATE,
    salary DECIMAL(10,2)
);
INSERT INTO employees (name, department, hire_date, salary) VALUES
    ('Sarah Chen', 'Engineering', '2023-01-15', 95000.00),
    ('Marcus Johnson', 'Marketing', '2022-06-01', 78000.00),
    ('Aisha Patel', 'Finance', '2021-11-20', 88500.00),
    ('Carlos Rivera', 'Engineering', '2024-03-10', 92000.00)
ON CONFLICT DO NOTHING;
EOSQL

# Add data to analytics
su - postgres -c "psql -d analytics" <<'EOSQL'
CREATE TABLE IF NOT EXISTS page_views (
    id SERIAL PRIMARY KEY,
    page_url VARCHAR(255),
    visitor_ip VARCHAR(45),
    visit_time TIMESTAMP DEFAULT NOW(),
    duration_sec INTEGER
);
INSERT INTO page_views (page_url, visitor_ip, duration_sec) VALUES
    ('/home', '192.168.1.45', 120),
    ('/products', '10.0.0.12', 45),
    ('/about', '172.16.0.88', 30),
    ('/contact', '192.168.1.45', 15)
ON CONFLICT DO NOTHING;
EOSQL

# Create backup directory
mkdir -p /backup/postgres
chown postgres:postgres /backup/postgres
chmod 755 /backup/postgres

# Remove any existing backup script (clean state)
rm -f /usr/local/bin/pg_backup.sh

# Clear crontab entries
crontab -r 2>/dev/null || true
su - postgres -c "crontab -r" 2>/dev/null || true

echo "=== Verification ==="
echo "--- Databases ---"
su - postgres -c "psql -l" 2>/dev/null | head -15
echo "--- Backup dir ---"
ls -la /backup/postgres/
echo "--- Script check ---"
ls /usr/local/bin/pg_backup.sh 2>&1 || echo "No backup script (expected)"
echo "--- Crontab ---"
crontab -l 2>&1 || echo "No crontab (expected)"
echo "=== Setup Complete ==="
'''

    # Write the setup script
    script_path = '/tmp/os_adm_030_setup.sh'
    with open(script_path, 'w') as f:
        f.write(setup_script)
    os.chmod(script_path, 0o755)

    # Execute with sudo
    print("Running privileged setup...")
    r = sudo_run(f"bash {script_path}")
    print(r.stdout[-1500:] if r.stdout else "")
    if r.stderr:
        # Filter out the sudo password prompt noise
        stderr_lines = [l for l in r.stderr.split('\n')
                       if l.strip() and 'password' not in l.lower() and '[sudo]' not in l]
        if stderr_lines:
            print("Stderr (filtered):", '\n'.join(stderr_lines[-10:]))

    # Clean up temp script
    os.remove(script_path)

    print("\nInitial state configured.")

    # Open a terminal for the user (GUI-ready state)
    launch_gui('gnome-terminal', delay_sec=2.0)
    print('GUI_READY: launched terminal with DISPLAY=:0')


setup_initial()
