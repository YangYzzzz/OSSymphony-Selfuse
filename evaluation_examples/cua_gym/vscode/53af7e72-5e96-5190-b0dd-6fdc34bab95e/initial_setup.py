"""
Initial Setup: Create infrastructure workspace with ops/ directory for Ansible automation.
Task ID: vscode_td_018
Domain: vscode

Sets up:
- ~/infrastructure workspace folder
- ops/inventory.yml with realistic Ansible inventory
- ops/deploy.yml with realistic Ansible playbook
- NO .vscode folder (task requires agent to create it)
- Opens VSCode with the workspace
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_018'
PROJECT_DIR = os.path.join(WORKDIR, 'infrastructure')
OPS_DIR = os.path.join(PROJECT_DIR, 'ops')


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
    os.makedirs(OPS_DIR, exist_ok=True)

    # Create ops/inventory.yml - realistic Ansible inventory
    inventory_content = """---
all:
  hosts:
    web-prod-01:
      ansible_host: 10.200.1.10
      ansible_user: deploy
      server_role: web
    web-prod-02:
      ansible_host: 10.200.1.11
      ansible_user: deploy
      server_role: web
    db-prod-01:
      ansible_host: 10.200.2.10
      ansible_user: deploy
      server_role: database
    cache-prod-01:
      ansible_host: 10.200.3.10
      ansible_user: deploy
      server_role: cache

  children:
    webservers:
      hosts:
        web-prod-01:
        web-prod-02:
    databases:
      hosts:
        db-prod-01:
    caching:
      hosts:
        cache-prod-01:

  vars:
    ansible_python_interpreter: /usr/bin/python3
    deploy_env: production
    app_version: "2.4.1"
    nginx_worker_processes: 4
    db_backup_enabled: true
"""
    with open(os.path.join(OPS_DIR, 'inventory.yml'), 'w') as f:
        f.write(inventory_content)

    # Create ops/deploy.yml - realistic Ansible playbook
    deploy_content = """---
- name: Deploy application to production servers
  hosts: webservers
  become: true
  serial: 1
  vars:
    app_name: acme-platform
    deploy_path: /opt/{{ app_name }}
    release_dir: "{{ deploy_path }}/releases/{{ app_version }}"

  pre_tasks:
    - name: Verify connectivity
      ping:

    - name: Check disk space
      assert:
        that: ansible_mounts | selectattr('mount', 'equalto', '/') | map(attribute='size_available') | first > 1073741824
        fail_msg: "Less than 1GB free disk space on root partition"

  tasks:
    - name: Create release directory
      file:
        path: "{{ release_dir }}"
        state: directory
        owner: www-data
        group: www-data
        mode: '0755'

    - name: Download application artifact
      get_url:
        url: "https://artifacts.acme-corp.internal/releases/{{ app_name }}-{{ app_version }}.tar.gz"
        dest: "/tmp/{{ app_name }}-{{ app_version }}.tar.gz"
        checksum: "sha256:{{ artifact_checksum }}"

    - name: Extract application
      unarchive:
        src: "/tmp/{{ app_name }}-{{ app_version }}.tar.gz"
        dest: "{{ release_dir }}"
        remote_src: true

    - name: Update symlink to current release
      file:
        src: "{{ release_dir }}"
        dest: "{{ deploy_path }}/current"
        state: link

    - name: Restart application service
      systemd:
        name: "{{ app_name }}"
        state: restarted
        daemon_reload: true

  post_tasks:
    - name: Verify application is responding
      uri:
        url: "http://localhost:8080/health"
        status_code: 200
      retries: 5
      delay: 3

- name: Refresh cache servers
  hosts: caching
  become: true
  tasks:
    - name: Flush application cache
      command: redis-cli FLUSHDB
      changed_when: true

    - name: Warm up cache
      uri:
        url: "http://{{ hostvars[groups['webservers'][0]]['ansible_host'] }}:8080/api/cache/warm"
        method: POST
"""
    with open(os.path.join(OPS_DIR, 'deploy.yml'), 'w') as f:
        f.write(deploy_content)

    # Create a README at the project root for realism
    readme_content = """# Infrastructure Automation

Production infrastructure management for Acme Platform.

## Directory Structure

- `ops/` - Ansible playbooks and inventory for server automation
  - `inventory.yml` - Production server inventory
  - `deploy.yml` - Application deployment playbook

## Usage

Run deployments from the `ops/` directory:

```bash
cd ops/
ansible-playbook -i inventory.yml deploy.yml
```

## Team

- DevOps: platform-ops@acme-corp.internal
- On-call: #ops-oncall (Slack)
"""
    with open(os.path.join(PROJECT_DIR, 'README.md'), 'w') as f:
        f.write(readme_content)

    # Ensure NO .vscode folder exists (task requires creating it)
    vscode_dir = os.path.join(PROJECT_DIR, '.vscode')
    if os.path.exists(vscode_dir):
        import shutil
        shutil.rmtree(vscode_dir)

    print(f'Initial workspace created: {PROJECT_DIR}')
    print(f'  ops/inventory.yml: present')
    print(f'  ops/deploy.yml: present')
    print(f'  .vscode/: does NOT exist (task requires agent to create it)')

    # Launch VSCode with the infrastructure folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
