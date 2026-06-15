"""
Initial Setup: Configure /etc/hosts for local development hostnames
Task ID: os_adm_016
Domain: os
"""

import os
import shlex
import subprocess
import time
import tempfile

WORKDIR = '/home/user'
TASK_ID = 'os_adm_016'

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
    # Ensure /etc/hosts has only default entries (no devdb.local or devredis.local)
    # Read current hosts file
    with open('/etc/hosts', 'r') as f:
        lines = f.readlines()

    # Filter out any existing devdb.local or devredis.local entries (idempotent)
    filtered = [line for line in lines if 'devdb.local' not in line and 'devredis.local' not in line]

    # Check if default entries exist, if not create a clean default
    has_localhost_v4 = any('127.0.0.1' in line and 'localhost' in line for line in filtered)
    has_localhost_v6 = any('::1' in line and 'localhost' in line for line in filtered)

    if not has_localhost_v4 or not has_localhost_v6:
        # Write a clean default hosts file
        new_content = """127.0.0.1\tlocalhost
127.0.1.1\tubuntu-dev-server

# The following lines are desirable for IPv6 capable hosts
::1\tip6-localhost ip6-loopback
fe00::0\tip6-localnet
ff00::0\tip6-mcastprefix
ff02::1\tip6-allnodes
ff02::2\tip6-allrouters
"""
    else:
        new_content = ''.join(filtered)

    # Write via sudo using a temp file
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.hosts', delete=False)
    tmp.write(new_content)
    tmp.close()
    subprocess.run(f"echo 'password' | sudo -S cp {tmp.name} /etc/hosts", shell=True, check=True)
    subprocess.run("echo 'password' | sudo -S chmod 644 /etc/hosts", shell=True, check=True)
    os.unlink(tmp.name)

    print(f'Initial /etc/hosts configured (default entries only)')

    # Verify no dev entries exist
    with open('/etc/hosts', 'r') as f:
        content = f.read()
    assert 'devdb.local' not in content, "devdb.local should not be in initial hosts"
    assert 'devredis.local' not in content, "devredis.local should not be in initial hosts"
    print('Verified: no devdb.local or devredis.local in /etc/hosts')

    # Print current hosts file for reference
    print('Current /etc/hosts:')
    print(content)

    # Open a terminal for the user to work in
    launch_gui('gnome-terminal', delay_sec=1.5)
    print('GUI_READY: launched terminal with DISPLAY=:0')

create_initial()
