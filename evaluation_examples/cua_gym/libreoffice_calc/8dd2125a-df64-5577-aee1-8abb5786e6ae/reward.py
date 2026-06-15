"""
Reward Script: Add Ansible task blocks to playbook.yml
Task ID: osworld_multi_apps_vscode_config_edit_007
Domain: vs-code / yaml (Ansible playbook)
Scoring:
  - Component 1: 'Install git' task present using apt module (0.35 pts)
  - Component 2: 'Start and enable nginx' service task present (0.35 pts)
  - Component 3: 'Copy index.html template' copy task present (0.20 pts)
  - Component 4: YAML is valid (bonus gate, 0.10 pts when other tasks correct)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_config_edit_007'
PLAYBOOK_PATH = '/home/user/Code/infra/playbook.yml'


def verify_task(file_path):
    """
    Verify that playbook.yml contains the three required new task blocks.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be readable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Parse YAML using PyYAML (available on VM)
    try:
        import yaml
        with open(file_path, 'r') as f:
            content = f.read()
        playbook = yaml.safe_load(content)
        yaml_valid = True
        print("INFO: YAML parsed successfully")
    except Exception as e:
        print(f"CRITICAL: YAML parse error: {e}")
        # If YAML can't be parsed, fall back to text-based checks
        playbook = None
        yaml_valid = False
        with open(file_path, 'r') as f:
            content = f.read()

    # Helper: get the tasks list from the first play
    tasks = []
    if playbook and isinstance(playbook, list) and len(playbook) > 0:
        play = playbook[0]
        if isinstance(play, dict):
            tasks = play.get('tasks', [])

    # -----------------------------------------------------------------------
    # Component 1: 'Install git' task via apt module (0.35 points)
    # This task must NOT exist in initial_env; it's added in golden_env.
    # -----------------------------------------------------------------------
    try:
        git_task_found = False
        if tasks:
            for task in tasks:
                if not isinstance(task, dict):
                    continue
                # Check for apt module with name=git
                apt_conf = task.get('apt', {})
                if isinstance(apt_conf, dict):
                    name_val = apt_conf.get('name', '')
                    state_val = apt_conf.get('state', '')
                    if str(name_val).lower() == 'git' and str(state_val).lower() == 'present':
                        git_task_found = True
                        break
        else:
            # Fallback: text search
            # Look for an apt task with name: git and state: present
            if re.search(r'apt:\s*\n\s+name:\s*git\b', content) or \
               re.search(r'- name:.*[Ii]nstall.*git', content):
                git_task_found = True

        if git_task_found:
            print("PASS: Component 1 — 'Install git' apt task found (0.35 pts)")
            total_score += 0.35
        else:
            print("FAIL: Component 1 — 'Install git' apt task not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: 'Start and enable nginx' service task (0.35 points)
    # Must have service module with name=nginx, state=started, enabled=yes
    # -----------------------------------------------------------------------
    try:
        nginx_task_found = False
        if tasks:
            for task in tasks:
                if not isinstance(task, dict):
                    continue
                svc_conf = task.get('service', {})
                if isinstance(svc_conf, dict):
                    name_val = svc_conf.get('name', '')
                    state_val = svc_conf.get('state', '')
                    enabled_val = svc_conf.get('enabled', None)
                    if (str(name_val).lower() == 'nginx' and
                            str(state_val).lower() == 'started' and
                            enabled_val in (True, 'yes', 'true', True)):
                        nginx_task_found = True
                        break
        else:
            # Fallback text search
            if re.search(r'service:\s*\n\s+name:\s*nginx', content) and \
               re.search(r'state:\s*started', content) and \
               re.search(r'enabled:\s*(yes|true)', content):
                nginx_task_found = True

        if nginx_task_found:
            print("PASS: Component 2 — 'Start and enable nginx' service task found (0.35 pts)")
            total_score += 0.35
        else:
            print("FAIL: Component 2 — 'Start and enable nginx' service task not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Copy templates/index.html to /var/www/html/index.html (0.20 points)
    # Must have copy module with src=templates/index.html and dest=/var/www/html/index.html
    # -----------------------------------------------------------------------
    try:
        copy_task_found = False
        if tasks:
            for task in tasks:
                if not isinstance(task, dict):
                    continue
                copy_conf = task.get('copy', {})
                if isinstance(copy_conf, dict):
                    src_val = str(copy_conf.get('src', ''))
                    dest_val = str(copy_conf.get('dest', ''))
                    # Accept src containing 'templates/index.html'
                    if ('templates/index.html' in src_val and
                            dest_val.rstrip('/').endswith('/var/www/html/index.html')):
                        copy_task_found = True
                        break
        else:
            # Fallback text search
            if re.search(r'copy:\s*\n\s+src:\s*templates/index\.html', content) and \
               re.search(r'dest:\s*/var/www/html/index\.html', content):
                copy_task_found = True

        if copy_task_found:
            print("PASS: Component 3 — Copy 'templates/index.html' task found (0.20 pts)")
            total_score += 0.20
        else:
            print("FAIL: Component 3 — Copy templates/index.html task not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: YAML is syntactically valid (0.10 points)
    # Only awarded when at least one task component passed (avoids rewarding
    # a trivially valid but empty file).
    # -----------------------------------------------------------------------
    try:
        if yaml_valid and total_score > 0.0:
            print("PASS: Component 4 — YAML syntax is valid (0.10 pts)")
            total_score += 0.10
        elif not yaml_valid:
            print("FAIL: Component 4 — YAML syntax is invalid")
        else:
            print("FAIL: Component 4 — YAML valid but no task components passed")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(PLAYBOOK_PATH):
    print(f"File not found: {PLAYBOOK_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(PLAYBOOK_PATH)
