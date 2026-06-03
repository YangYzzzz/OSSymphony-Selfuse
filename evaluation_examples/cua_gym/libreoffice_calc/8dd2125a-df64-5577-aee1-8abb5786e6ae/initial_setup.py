"""
Initial Setup: Ansible playbook with one existing task (Install packages)
Task ID: osworld_multi_apps_vscode_config_edit_007
Domain: multi_apps (VSCode + YAML file editing)
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_config_edit_007'
PLAYBOOK_DIR = f'{WORKDIR}/Code/infra'
PLAYBOOK_PATH = f'{PLAYBOOK_DIR}/playbook.yml'
TEMPLATES_DIR = f'{PLAYBOOK_DIR}/templates'


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
    # Create directory structure
    os.makedirs(PLAYBOOK_DIR, exist_ok=True)
    os.makedirs(TEMPLATES_DIR, exist_ok=True)

    # Create the initial Ansible playbook with one task: Install packages
    playbook_content = """\
---
- name: Configure web server
  hosts: webservers
  become: yes
  vars:
    packages:
      - curl
      - wget
      - vim
      - htop
      - unzip
    web_root: /var/www/html

  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
        cache_valid_time: 3600

    - name: Install packages
      apt:
        name: "{{ packages }}"
        state: present
"""

    with open(PLAYBOOK_PATH, 'w') as f:
        f.write(playbook_content)
    print(f'Playbook created: {PLAYBOOK_PATH}')

    # Create a realistic templates/index.html file
    index_html_content = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Our Server</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f5f5f5;
        }
        h1 { color: #333; }
        p { color: #666; }
    </style>
</head>
<body>
    <h1>Welcome to Our Web Server</h1>
    <p>This server is managed by Ansible automation.</p>
    <p>Deployment successful.</p>
</body>
</html>
"""

    with open(f'{TEMPLATES_DIR}/index.html', 'w') as f:
        f.write(index_html_content)
    print(f'Template file created: {TEMPLATES_DIR}/index.html')

    # Create an inventory file to make the project more realistic
    inventory_content = """\
[webservers]
web01.example.com ansible_user=ubuntu
web02.example.com ansible_user=ubuntu

[webservers:vars]
ansible_python_interpreter=/usr/bin/python3
"""

    with open(f'{PLAYBOOK_DIR}/inventory.ini', 'w') as f:
        f.write(inventory_content)
    print(f'Inventory file created: {PLAYBOOK_DIR}/inventory.ini')

    # Create a README for the project
    readme_content = """\
# Infrastructure Playbooks

This repository contains Ansible playbooks for configuring web servers.

## Usage

```bash
ansible-playbook -i inventory.ini playbook.yml
```

## Requirements

- Ansible 2.9+
- Python 3.6+
"""

    with open(f'{PLAYBOOK_DIR}/README.md', 'w') as f:
        f.write(readme_content)
    print(f'README created: {PLAYBOOK_DIR}/README.md')

    # GUI-ready startup
    # 1. Open Chrome with Ansible docs (already open per task, but launch anyway)
    launch_gui('google-chrome --new-window "https://docs.ansible.com/"', delay_sec=2.0)

    # 2. Open VSCode with the playbook file
    launch_gui(f'code "{PLAYBOOK_PATH}"', delay_sec=2.0)

    print('GUI_READY: launched Chrome with Ansible docs and VSCode with playbook.yml')


create_initial()
