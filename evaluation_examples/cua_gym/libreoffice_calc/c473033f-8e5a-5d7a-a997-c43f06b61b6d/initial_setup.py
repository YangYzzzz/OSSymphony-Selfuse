"""
Initial Setup: Create Ansible directory structure with inventory and Jinja2 template
Task ID: os_gf2_014
Domain: os
"""

import os
import shlex
import subprocess
import time
from pathlib import Path

WORKDIR = '/home/user'
TASK_ID = 'os_gf2_014'

def sudo_run(cmd: str, check: bool = True):
    """Run a command with sudo, piping password via stdin."""
    return subprocess.run(
        f"echo 'password' | sudo -S {cmd}",
        shell=True, check=check,
        capture_output=True, text=True
    )

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
    # 1. Create directory structure (need sudo for /opt)
    sudo_run('mkdir -p /opt/ansible/templates')
    sudo_run('chmod -R 777 /opt/ansible')

    # 2. Create inventory.ini with a realistic webservers group
    inventory_content = """\
[webservers]
web01.example.com ansible_host=192.168.1.10 ansible_user=deploy
web02.example.com ansible_host=192.168.1.11 ansible_user=deploy

[webservers:vars]
server_name=www.example.com
document_root=/var/www/mysite
ansible_ssh_private_key_file=~/.ssh/deploy_key
"""
    Path('/opt/ansible/inventory.ini').write_text(inventory_content)
    print('Created /opt/ansible/inventory.ini')

    # 3. Create Jinja2 template for nginx virtual host config
    template_content = """\
server {
    listen 80;
    server_name {{ server_name }};
    root {{ document_root }};

    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }

    access_log /var/log/nginx/{{ server_name }}_access.log;
    error_log /var/log/nginx/{{ server_name }}_error.log;
}
"""
    Path('/opt/ansible/templates/nginx_vhost.j2').write_text(template_content)
    print('Created /opt/ansible/templates/nginx_vhost.j2')

    # 4. Make sure webserver.yml does NOT exist (the task goal)
    playbook_path = '/opt/ansible/webserver.yml'
    if os.path.exists(playbook_path):
        os.remove(playbook_path)
        print(f'Removed pre-existing {playbook_path}')

    # 5. Install ansible if not present (needed for syntax-check verification)
    sudo_run('apt-get update -qq', check=False)
    sudo_run('apt-get install -y -qq ansible', check=False)
    print('Ensured ansible is installed')

    # 6. Open a terminal and file manager showing the ansible directory
    launch_gui('nautilus /opt/ansible', delay_sec=1.5)
    launch_gui('gnome-terminal --working-directory=/opt/ansible', delay_sec=1.5)
    print('GUI_READY: launched nautilus and terminal with DISPLAY=:0')

create_initial()
