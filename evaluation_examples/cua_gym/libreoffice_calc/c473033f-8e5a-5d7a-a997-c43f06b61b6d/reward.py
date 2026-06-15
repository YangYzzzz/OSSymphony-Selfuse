"""
Reward Script: Ansible playbook for nginx web server provisioning
Task ID: os_gf2_014
Domain: os (Ansible)
Scoring:
  - Component 1 (0.15): File exists and is valid YAML
  - Component 2 (0.15): Targets webservers with become: yes
  - Component 3 (0.20): Apt task installs nginx + certbot, state present, update_cache
  - Component 4 (0.20): Template task deploys nginx_vhost.j2, notifies handler
  - Component 5 (0.10): File task creates symlink to sites-enabled
  - Component 6 (0.10): Service task ensures nginx started + enabled
  - Component 7 (0.10): Handler 'Reload nginx' with state: reloaded
"""

import os
import yaml

WORKDIR = '/opt/ansible'
TASK_ID = 'os_gf2_014'
PLAYBOOK_PATH = f'{WORKDIR}/webserver.yml'


def verify_task():
    """
    Verify Ansible playbook task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: File exists and is valid YAML (0.15 points)
    try:
        if not os.path.isfile(PLAYBOOK_PATH):
            print(f"FAIL: Component 1 — {PLAYBOOK_PATH} does not exist")
            print("REWARD: 0.0")
            return 0.0

        with open(PLAYBOOK_PATH, 'r') as f:
            content = f.read()

        data = yaml.safe_load(content)
        if not isinstance(data, list) or len(data) == 0:
            print("FAIL: Component 1 — YAML loaded but not a list of plays")
            print("REWARD: 0.0")
            return 0.0

        print(f"PASS: Component 1 — File exists and is valid YAML (0.15 pts)")
        total_score += 0.15
    except yaml.YAMLError as e:
        print(f"FAIL: Component 1 — Invalid YAML: {e}")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Work with the first play in the playbook
    play = data[0]

    # Component 2: Targets 'webservers' with become: yes (0.15 points)
    try:
        hosts_val = play.get('hosts', '')
        become_val = play.get('become', False)
        if str(hosts_val).strip() == 'webservers' and become_val is True:
            print(f"PASS: Component 2 — hosts: webservers, become: yes (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — hosts={hosts_val}, become={become_val}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Get tasks list
    tasks = play.get('tasks', [])

    # Component 3: Apt task installs nginx + certbot with state:present, update_cache:yes (0.20 points)
    try:
        apt_found = False
        for task in tasks:
            apt_conf = task.get('apt', task.get('ansible.builtin.apt', None))
            if apt_conf and isinstance(apt_conf, dict):
                pkg_names = apt_conf.get('name', [])
                if isinstance(pkg_names, str):
                    pkg_names = [pkg_names]
                pkg_set = set(pkg_names)
                has_nginx = 'nginx' in pkg_set
                has_certbot = 'python3-certbot-nginx' in pkg_set or 'certbot' in pkg_set
                state_present = apt_conf.get('state', '') == 'present'
                update_cache = apt_conf.get('update_cache', False)
                # update_cache can be yes/true/True
                if isinstance(update_cache, str):
                    update_cache = update_cache.lower() in ('yes', 'true')

                if has_nginx and has_certbot and state_present and update_cache:
                    apt_found = True
                    break

        if apt_found:
            print(f"PASS: Component 3 — Apt task installs nginx+certbot, state:present, update_cache:yes (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — No apt task found with correct packages/options")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Template task deploys nginx_vhost.j2 and notifies 'Reload nginx' (0.20 points)
    try:
        template_found = False
        for task in tasks:
            tpl_conf = task.get('template', task.get('ansible.builtin.template', None))
            if tpl_conf and isinstance(tpl_conf, dict):
                src = tpl_conf.get('src', '')
                dest = tpl_conf.get('dest', '')
                notify = task.get('notify', '')
                # notify can be a string or list
                if isinstance(notify, list):
                    notify_list = notify
                else:
                    notify_list = [notify]

                src_ok = 'nginx_vhost.j2' in str(src)
                dest_ok = 'sites-available' in str(dest)
                notify_ok = any('Reload nginx' in str(n) for n in notify_list)

                if src_ok and dest_ok and notify_ok:
                    template_found = True
                    break

        if template_found:
            print(f"PASS: Component 4 — Template task with nginx_vhost.j2, dest sites-available, notify Reload nginx (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — No template task found with correct src/dest/notify")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: File task for symlink to sites-enabled (0.10 points)
    try:
        file_found = False
        for task in tasks:
            file_conf = task.get('file', task.get('ansible.builtin.file', None))
            if file_conf and isinstance(file_conf, dict):
                state = file_conf.get('state', '')
                dest = str(file_conf.get('dest', file_conf.get('path', '')))
                src = str(file_conf.get('src', ''))
                if state == 'link' and 'sites-enabled' in dest:
                    file_found = True
                    break

        if file_found:
            print(f"PASS: Component 5 — File task creates symlink to sites-enabled (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — No file task with state:link to sites-enabled")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Service task ensures nginx started and enabled (0.10 points)
    try:
        service_found = False
        for task in tasks:
            svc_conf = task.get('service', task.get('ansible.builtin.service', None))
            if svc_conf and isinstance(svc_conf, dict):
                name = svc_conf.get('name', '')
                state = svc_conf.get('state', '')
                enabled = svc_conf.get('enabled', False)
                if isinstance(enabled, str):
                    enabled = enabled.lower() in ('yes', 'true')
                if name == 'nginx' and state == 'started' and enabled:
                    service_found = True
                    break

        if service_found:
            print(f"PASS: Component 6 — Service task: nginx started + enabled (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 — No service task with nginx started + enabled:yes")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: Handler 'Reload nginx' with state: reloaded (0.10 points)
    try:
        handlers = play.get('handlers', [])
        handler_found = False
        for handler in handlers:
            hname = handler.get('name', '')
            hsvc = handler.get('service', handler.get('ansible.builtin.service', None))
            if 'Reload nginx' in str(hname) and isinstance(hsvc, dict):
                hstate = hsvc.get('state', '')
                if hstate == 'reloaded':
                    handler_found = True
                    break

        if handler_found:
            print(f"PASS: Component 7 — Handler 'Reload nginx' with state:reloaded (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 7 — No handler 'Reload nginx' with state:reloaded found")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
verify_task()
