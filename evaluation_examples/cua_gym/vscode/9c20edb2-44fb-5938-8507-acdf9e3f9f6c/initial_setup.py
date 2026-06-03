"""
Initial Setup: VSCode with Ansible workspace, no setup-nginx.yml
Task ID: vscode_ops_038
Domain: vscode
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_038'
ANSIBLE_DIR = f'{WORKDIR}/ansible'

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
    # Create the ansible workspace directory
    os.makedirs(ANSIBLE_DIR, exist_ok=True)

    # Create some realistic existing Ansible files so the workspace isn't empty
    # but do NOT create setup-nginx.yml (that's the task)

    # ansible.cfg - standard Ansible configuration
    ansible_cfg = """[defaults]
inventory = inventory/hosts
remote_user = deploy
host_key_checking = False
retry_files_enabled = False
timeout = 30

[privilege_escalation]
become = True
become_method = sudo
become_user = root
become_ask_pass = False
"""
    with open(os.path.join(ANSIBLE_DIR, 'ansible.cfg'), 'w') as f:
        f.write(ansible_cfg)

    # inventory directory with hosts file
    inv_dir = os.path.join(ANSIBLE_DIR, 'inventory')
    os.makedirs(inv_dir, exist_ok=True)

    hosts_ini = """[webservers]
web01.example.com ansible_host=192.168.1.10
web02.example.com ansible_host=192.168.1.11
web03.example.com ansible_host=192.168.1.12

[dbservers]
db01.example.com ansible_host=192.168.1.20
db02.example.com ansible_host=192.168.1.21

[loadbalancers]
lb01.example.com ansible_host=192.168.1.5

[all:vars]
ansible_python_interpreter=/usr/bin/python3
"""
    with open(os.path.join(inv_dir, 'hosts'), 'w') as f:
        f.write(hosts_ini)

    # An existing playbook for reference (different task - setup postgres)
    existing_playbook = """---
- name: Setup PostgreSQL Database Server
  hosts: dbservers
  become: true

  tasks:
    - name: Install PostgreSQL
      apt:
        name: postgresql
        state: present
        update_cache: yes

    - name: Ensure PostgreSQL is running
      service:
        name: postgresql
        state: started
        enabled: yes

    - name: Create application database
      become_user: postgres
      postgresql_db:
        name: app_production
        state: present
"""
    with open(os.path.join(ANSIBLE_DIR, 'setup-postgres.yml'), 'w') as f:
        f.write(existing_playbook)

    # A roles directory with a placeholder
    roles_dir = os.path.join(ANSIBLE_DIR, 'roles')
    os.makedirs(os.path.join(roles_dir, 'common', 'tasks'), exist_ok=True)

    common_tasks = """---
- name: Update apt cache
  apt:
    update_cache: yes
    cache_valid_time: 3600

- name: Install common packages
  apt:
    name:
      - vim
      - curl
      - wget
      - htop
      - git
    state: present
"""
    with open(os.path.join(roles_dir, 'common', 'tasks', 'main.yml'), 'w') as f:
        f.write(common_tasks)

    # README for the workspace
    readme = """# Infrastructure Ansible Playbooks

This repository contains Ansible playbooks for managing our infrastructure.

## Directory Structure

- `inventory/` - Host inventory files
- `roles/` - Reusable Ansible roles
- `*.yml` - Playbook files

## Usage

```bash
ansible-playbook -i inventory/hosts <playbook>.yml
```

## Servers

| Group | Hosts | Purpose |
|-------|-------|---------|
| webservers | web01-03 | Nginx web servers |
| dbservers | db01-02 | PostgreSQL databases |
| loadbalancers | lb01 | HAProxy load balancer |
"""
    with open(os.path.join(ANSIBLE_DIR, 'README.md'), 'w') as f:
        f.write(readme)

    # Ensure setup-nginx.yml does NOT exist
    target_file = os.path.join(ANSIBLE_DIR, 'setup-nginx.yml')
    if os.path.exists(target_file):
        os.remove(target_file)

    print(f'Initial workspace created: {ANSIBLE_DIR}')
    print(f'Files: ansible.cfg, inventory/hosts, setup-postgres.yml, roles/common/tasks/main.yml, README.md')
    print(f'Confirmed: setup-nginx.yml does NOT exist')

    # Install YAML extension for VSCode
    try:
        subprocess.run(['code', '--install-extension', 'redhat.vscode-yaml'],
                       capture_output=True, text=True, timeout=60)
        print('YAML extension installed')
    except Exception as e:
        print(f'Extension install note: {e}')

    # Launch VSCode with the ansible workspace
    launch_gui(f'code "{ANSIBLE_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
