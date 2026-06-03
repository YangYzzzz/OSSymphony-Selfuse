"""
Initial Setup: MySQL replication slave - pre-configuration state
Task ID: os_adm_034
Domain: os (MySQL administration)

Sets up:
- MySQL 8.0 installed on the slave server
- server-id=2 configured in mysqld.cnf
- Binary logging enabled
- No replication configured yet (SHOW SLAVE STATUS returns empty)
- A terminal window open for the user to configure replication
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'os_adm_034'
SUDO_PASS = 'password'

def run(cmd, check=True, timeout=300):
    """Run a shell command with sudo password piped."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if check and result.returncode != 0:
        print(f"CMD FAILED: {cmd}")
        print(f"STDOUT: {result.stdout[-500:]}")
        print(f"STDERR: {result.stderr[-500:]}")
    return result

def sudo(cmd, timeout=300):
    """Run command with sudo, piping password."""
    return run(f"echo '{SUDO_PASS}' | sudo -S {cmd}", timeout=timeout)

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

def setup_mysql():
    """Install and configure MySQL as a slave server (pre-replication state)."""

    os.environ['DEBIAN_FRONTEND'] = 'noninteractive'

    # Install MySQL server
    print("Installing MySQL server...")
    sudo("apt-get update -qq", timeout=120)
    sudo("apt-get install -y -qq mysql-server-8.0", timeout=300)

    # Configure MySQL as slave with server-id=2
    print("Configuring MySQL slave (server-id=2)...")
    config_content = """[mysqld]
server-id = 2
log_bin = /var/log/mysql/mysql-bin.log
relay_log = /var/log/mysql/mysql-relay-bin.log
read_only = 1
bind-address = 0.0.0.0
"""
    # Write config file
    with open('/tmp/replication.cnf', 'w') as f:
        f.write(config_content)
    sudo("cp /tmp/replication.cnf /etc/mysql/mysql.conf.d/replication.cnf")
    sudo("chown root:root /etc/mysql/mysql.conf.d/replication.cnf")
    sudo("chmod 644 /etc/mysql/mysql.conf.d/replication.cnf")

    # Start/restart MySQL
    print("Starting MySQL...")
    sudo("systemctl start mysql", timeout=60)
    time.sleep(2)
    print("Restarting MySQL to apply replication config...")
    sudo("systemctl restart mysql", timeout=60)
    time.sleep(3)

    # Verify server-id is set
    result = sudo("mysql -e \"SHOW VARIABLES LIKE 'server_id';\"")
    print(f"Server ID check: {result.stdout}")

    # Verify NO replication is configured
    result = sudo("mysql -e \"SHOW SLAVE STATUS\\G\"")
    print(f"Slave status (should be empty): '{result.stdout.strip()}'")

    # Create reference doc with master info for the user
    master_info = """MySQL Replication Setup - Slave Configuration Task
===================================================

Master Server Information:
  Host: 10.0.0.10
  Replication User: repl_user
  Replication Password: R3pl!cAte2024#Secure
  Master Log File: mysql-bin.000003
  Master Log Position: 157

Current Slave Configuration:
  Server ID: 2 (already configured)
  Binary Logging: Enabled
  Relay Log: Enabled
  Read Only: Yes

TODO:
  1. Run CHANGE MASTER TO with the above credentials
  2. Run START SLAVE
  3. Verify with SHOW SLAVE STATUS\\G
"""
    with open(f'{WORKDIR}/{TASK_ID}_master_info.txt', 'w') as f:
        f.write(master_info)
    print(f"Master info reference created: {WORKDIR}/{TASK_ID}_master_info.txt")

    # Open terminal for the user to do the task
    launch_gui('gnome-terminal', delay_sec=2.0)
    print('GUI_READY: launched terminal with DISPLAY=:0')

setup_mysql()
print("Initial setup complete - MySQL slave ready for replication configuration")
