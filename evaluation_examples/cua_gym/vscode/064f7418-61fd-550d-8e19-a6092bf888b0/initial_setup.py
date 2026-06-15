"""
Initial Setup: Create Ansible role workspace for app-setup role
Task ID: vscode_ops_082
Domain: vscode

Creates the directory structure for an Ansible role (tasks/, templates/, handlers/)
with supporting files but WITHOUT tasks/main.yml (the agent must create that).
Opens VSCode with the workspace folder.
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_082'
ROLE_DIR = f'{WORKDIR}/ansible/roles/app-setup'


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
    for subdir in ['tasks', 'templates', 'handlers', 'defaults', 'meta']:
        os.makedirs(os.path.join(ROLE_DIR, subdir), exist_ok=True)

    # --- templates/app.service.j2 ---
    # A realistic Jinja2 systemd service template that the task references
    template_content = """\
[Unit]
Description={{ app_description | default('Application Service') }}
After=network.target
Wants=network-online.target

[Service]
Type=simple
User={{ app_user }}
Group={{ app_group | default(app_user) }}
WorkingDirectory={{ app_home }}
ExecStart={{ app_home }}/bin/start.sh
ExecStop=/bin/kill -SIGTERM $MAINPID
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
"""
    with open(os.path.join(ROLE_DIR, 'templates', 'app.service.j2'), 'w') as f:
        f.write(template_content)

    # --- handlers/main.yml ---
    handlers_content = """\
---
- name: Reload systemd daemon
  ansible.builtin.systemd:
    daemon_reload: yes
  listen: "reload systemd"

- name: Restart app service
  ansible.builtin.systemd:
    name: app
    state: restarted
  listen: "restart app"
"""
    with open(os.path.join(ROLE_DIR, 'handlers', 'main.yml'), 'w') as f:
        f.write(handlers_content)

    # --- defaults/main.yml ---
    defaults_content = """\
---
# Default variables for app-setup role
app_user: appuser
app_group: appuser
app_home: /opt/app
app_description: "Application Service"
app_service_name: app
"""
    with open(os.path.join(ROLE_DIR, 'defaults', 'main.yml'), 'w') as f:
        f.write(defaults_content)

    # --- meta/main.yml ---
    meta_content = """\
---
galaxy_info:
  author: DevOps Team
  description: Role to set up the application service user, deploy config, and manage systemd service
  company: Acme Corp
  license: MIT
  min_ansible_version: "2.9"
  platforms:
    - name: Ubuntu
      versions:
        - focal
        - jammy
    - name: Debian
      versions:
        - bullseye
        - bookworm

dependencies: []
"""
    with open(os.path.join(ROLE_DIR, 'meta', 'main.yml'), 'w') as f:
        f.write(meta_content)

    # --- README.md for the role ---
    readme_content = """\
# app-setup

Ansible role to provision the application environment.

## Requirements

- Target must be a Debian/Ubuntu system with systemd.
- Python 3 must be available on the target host.

## Role Variables

| Variable           | Default              | Description                        |
|--------------------|----------------------|------------------------------------|
| `app_user`         | `appuser`            | System user to create              |
| `app_group`        | `appuser`            | Primary group for the user         |
| `app_home`         | `/opt/app`           | Home directory for the user        |
| `app_description`  | `Application Service`| Systemd service description        |
| `app_service_name` | `app`                | Name of the systemd service unit   |

## Usage

```yaml
- hosts: app_servers
  roles:
    - app-setup
```

## TODO

- [ ] Write tasks/main.yml to implement the role logic
"""
    with open(os.path.join(ROLE_DIR, 'README.md'), 'w') as f:
        f.write(readme_content)

    # Ensure tasks/ directory exists but tasks/main.yml does NOT exist
    tasks_main = os.path.join(ROLE_DIR, 'tasks', 'main.yml')
    if os.path.exists(tasks_main):
        os.remove(tasks_main)

    print(f'Initial workspace created: {ROLE_DIR}')
    print(f'Directory structure:')
    for root, dirs, files in os.walk(ROLE_DIR):
        level = root.replace(ROLE_DIR, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f'{subindent}{file}')

    # Open VSCode with the workspace
    launch_gui(f'code "{ROLE_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
