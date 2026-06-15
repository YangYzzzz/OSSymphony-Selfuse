"""
Reward Script: Write an Ansible playbook setup-nginx.yml
Task ID: vscode_ops_038
Domain: vscode
Scoring:
  Component 1 (0.2): File exists and is valid YAML
  Component 2 (0.2): hosts is set to 'webservers'
  Component 3 (0.2): Has task to install nginx (apt or yum)
  Component 4 (0.2): Has task to start nginx service
  Component 5 (0.2): Has task to enable nginx on boot
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_038'
FILE_PATH = os.path.join(WORKDIR, 'ansible', 'setup-nginx.yml')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
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

    # Component 1: File is valid YAML with Ansible playbook structure (0.2 points)
    try:
        import yaml
        parsed = yaml.safe_load(content)
        if isinstance(parsed, list) and len(parsed) > 0 and isinstance(parsed[0], dict):
            print(f"PASS: Component 1 — Valid YAML with playbook structure (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — YAML parsed but not a valid playbook list structure, got type: {type(parsed)}")
    except ImportError:
        # Fallback: check basic YAML-like structure without yaml module
        # Check it starts with '---' or '- ' which indicates YAML list
        stripped = content.strip()
        if stripped.startswith('---') or stripped.startswith('- '):
            print(f"PASS: Component 1 — File has YAML structure (yaml module unavailable, basic check) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — File does not appear to be valid YAML")
    except Exception as e:
        print(f"FAIL: Component 1 — YAML parse error: {e}")

    # Component 2: Contains hosts: webservers (0.2 points)
    try:
        # Check for hosts: webservers pattern in the content
        # Allow variations like hosts: webservers, hosts: 'webservers', hosts: "webservers"
        hosts_pattern = re.compile(r'hosts\s*:\s*["\']?webservers["\']?\s*$', re.MULTILINE)
        if hosts_pattern.search(content):
            print(f"PASS: Component 2 — Found hosts: webservers (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — hosts: webservers not found in playbook")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Has task to install nginx (apt or yum) (0.2 points)
    try:
        # Check for apt or yum module installing nginx
        has_apt_nginx = bool(re.search(r'apt\s*:', content)) and bool(re.search(r'name\s*:\s*nginx', content))
        has_yum_nginx = bool(re.search(r'yum\s*:', content)) and bool(re.search(r'name\s*:\s*nginx', content))
        has_package_nginx = bool(re.search(r'package\s*:', content)) and bool(re.search(r'name\s*:\s*nginx', content))
        if has_apt_nginx or has_yum_nginx or has_package_nginx:
            print(f"PASS: Component 3 — Found nginx installation task (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — No apt/yum/package task installing nginx found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Has task to start nginx service (0.2 points)
    try:
        # Check for service module with name: nginx and state: started
        has_service_start = bool(re.search(r'service\s*:', content)) and bool(re.search(r'state\s*:\s*started', content))
        # Also check systemd module
        has_systemd_start = bool(re.search(r'systemd\s*:', content)) and bool(re.search(r'state\s*:\s*started', content))
        if has_service_start or has_systemd_start:
            print(f"PASS: Component 4 — Found nginx service start task (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — No service/systemd task starting nginx found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Has task to enable nginx on boot (0.2 points)
    try:
        # Check for enabled: yes/true in service or systemd module
        has_enabled = bool(re.search(r'enabled\s*:\s*(yes|true|Yes|True)', content))
        if has_enabled:
            print(f"PASS: Component 5 — Found nginx service enable on boot (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 — No enabled: yes/true found for nginx service")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
