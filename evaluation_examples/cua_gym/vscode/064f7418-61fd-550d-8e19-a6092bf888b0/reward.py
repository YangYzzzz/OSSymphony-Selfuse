"""
Reward Script: Ansible role task file verification
Task ID: vscode_ops_082
Domain: vscode
Scoring:
  Component 1 (0.15): tasks/main.yml exists and is valid YAML with task list
  Component 2 (0.25): User creation task (system user 'appuser', home /opt/app)
  Component 3 (0.20): Template deployment task for systemd service
  Component 4 (0.20): Systemd daemon reload + enable/start service tasks
  Component 5 (0.20): Proper Ansible module usage (FQCN or short names)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_082'
TASK_FILE = os.path.join(WORKDIR, 'ansible', 'roles', 'app-setup', 'tasks', 'main.yml')


def verify_task(file_path):
    """
    Verify Ansible role task file with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Read file content
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid YAML with task list (0.15 points)
    # tasks/main.yml must parse as valid YAML and contain a list of tasks
    try:
        import yaml
        parsed = yaml.safe_load(content)
        if isinstance(parsed, list) and len(parsed) >= 3:
            print(f"PASS: Component 1 - Valid YAML with {len(parsed)} tasks (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - Expected list of >=3 tasks, got: {type(parsed).__name__} with {len(parsed) if isinstance(parsed, list) else 0} items")
    except ImportError:
        # Fallback: basic structure check without yaml module
        # Check if content looks like a YAML task list
        if re.search(r'^\s*-\s+name:', content, re.MULTILINE):
            task_names = re.findall(r'^\s*-\s+name:', content, re.MULTILINE)
            if len(task_names) >= 3:
                print(f"PASS: Component 1 - YAML structure found with {len(task_names)} tasks (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 - Only {len(task_names)} tasks found, need >=3")
        else:
            print("FAIL: Component 1 - No YAML task structure found")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: User creation task (0.25 points)
    # Must create system user 'appuser' with home directory /opt/app
    try:
        content_lower = content.lower()
        has_user_module = bool(re.search(r'(ansible\.builtin\.)?user:', content))
        has_appuser = 'appuser' in content
        has_system_user = bool(re.search(r'system:\s*(yes|true)', content_lower))
        has_home_dir = bool(re.search(r'home:\s*/opt/app', content))

        user_checks = sum([has_user_module, has_appuser, has_system_user, has_home_dir])
        if user_checks == 4:
            print(f"PASS: Component 2 - User creation task complete: user module, appuser, system=yes, home=/opt/app (0.25 pts)")
            total_score += 0.25
        elif user_checks >= 2:
            partial = round(0.25 * (user_checks / 4), 2)
            print(f"PARTIAL: Component 2 - User creation {user_checks}/4 checks passed ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - User creation task missing or incomplete (module={has_user_module}, appuser={has_appuser}, system={has_system_user}, home={has_home_dir})")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Template deployment for systemd service (0.20 points)
    # Must deploy systemd service file from a Jinja2 template
    try:
        has_template_module = bool(re.search(r'(ansible\.builtin\.)?template:', content))
        has_service_src = bool(re.search(r'src:.*\.j2', content))
        has_systemd_dest = bool(re.search(r'dest:.*(/etc/systemd/system/|/lib/systemd/system/).*\.service', content))

        template_checks = sum([has_template_module, has_service_src, has_systemd_dest])
        if template_checks == 3:
            print(f"PASS: Component 3 - Template deployment complete: template module, j2 source, systemd dest (0.20 pts)")
            total_score += 0.20
        elif template_checks >= 1:
            partial = round(0.20 * (template_checks / 3), 2)
            print(f"PARTIAL: Component 3 - Template deployment {template_checks}/3 checks passed ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 - Template deployment task missing (module={has_template_module}, src={has_service_src}, dest={has_systemd_dest})")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Systemd daemon reload and enable/start service (0.20 points)
    # Must reload systemd daemon and enable+start the service
    try:
        has_systemd_module = bool(re.search(r'(ansible\.builtin\.)?systemd:', content))
        has_daemon_reload = bool(re.search(r'daemon_reload:\s*(yes|true)', content_lower))
        has_enabled = bool(re.search(r'enabled:\s*(yes|true)', content_lower))
        has_started = bool(re.search(r'state:\s*started', content_lower))

        systemd_checks = sum([has_systemd_module, has_daemon_reload, has_enabled, has_started])
        if systemd_checks == 4:
            print(f"PASS: Component 4 - Systemd management complete: module, daemon_reload, enabled, started (0.20 pts)")
            total_score += 0.20
        elif systemd_checks >= 1:
            partial = round(0.20 * (systemd_checks / 4), 2)
            print(f"PARTIAL: Component 4 - Systemd management {systemd_checks}/4 checks passed ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 - Systemd management tasks missing (module={has_systemd_module}, reload={has_daemon_reload}, enabled={has_enabled}, started={has_started})")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Proper Ansible module usage (0.20 points)
    # Must use proper Ansible modules (user, template, systemd/file)
    try:
        # Check for proper module references (either FQCN or short name in task context)
        modules_found = set()
        # Check for user module
        if re.search(r'(ansible\.builtin\.)?user:', content):
            modules_found.add('user')
        # Check for template module
        if re.search(r'(ansible\.builtin\.)?template:', content):
            modules_found.add('template')
        # Check for systemd module
        if re.search(r'(ansible\.builtin\.)?systemd:', content):
            modules_found.add('systemd')
        # Check for file module (optional but good for directory permissions)
        if re.search(r'(ansible\.builtin\.)?file:', content):
            modules_found.add('file')

        # Need at least user, template, and systemd
        required_modules = {'user', 'template', 'systemd'}
        found_required = required_modules.intersection(modules_found)

        if len(found_required) == 3:
            print(f"PASS: Component 5 - All required Ansible modules found: {modules_found} (0.20 pts)")
            total_score += 0.20
        elif len(found_required) >= 1:
            partial = round(0.20 * (len(found_required) / 3), 2)
            print(f"PARTIAL: Component 5 - {len(found_required)}/3 required modules found: {found_required} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 - No required Ansible modules found. Expected: {required_modules}")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(TASK_FILE):
    print(f"File not found: {TASK_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(TASK_FILE)
