"""
Reward Script: VSCode Remote Development SSH Configuration
Task ID: vscode_gf6_023
Domain: vscode
Scoring:
  Component 1 (0.35): SSH config has Host dev-server with correct fields
  Component 2 (0.25): .vscode/settings.json has remote.SSH.defaultExtensions with 3+ IDs
  Component 3 (0.20): remote-workspace.code-workspace exists with remote SSH folder
  Component 4 (0.20): .vscode/tasks.json has 'Remote: Deploy' task using scp
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'remote-setup')
TASK_ID = 'vscode_gf6_023'


def parse_ssh_config(path):
    """Parse ~/.ssh/config into a dict of {host_alias: {key: value, ...}}."""
    hosts = {}
    current_host = None
    try:
        with open(path, 'r') as f:
            for line in f:
                stripped = line.strip()
                if not stripped or stripped.startswith('#'):
                    continue
                # Match Host directive
                m = re.match(r'^Host\s+(.+)$', stripped, re.IGNORECASE)
                if m:
                    current_host = m.group(1).strip()
                    hosts[current_host] = {}
                    continue
                # Match key-value pairs under a Host block
                if current_host:
                    parts = stripped.split(None, 1)
                    if len(parts) == 2:
                        hosts[current_host][parts[0].lower()] = parts[1]
    except Exception as e:
        print(f"ERROR: Cannot parse SSH config: {e}")
    return hosts


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: SSH config has Host dev-server entry with correct fields (0.35 points)
    try:
        ssh_config_path = os.path.join(WORKDIR, '.ssh', 'config')
        hosts = parse_ssh_config(ssh_config_path)

        if 'dev-server' not in hosts:
            print("FAIL: Component 1 — No 'dev-server' host entry in ~/.ssh/config")
        else:
            entry = hosts['dev-server']
            required_fields = {
                'hostname': '192.168.1.100',
                'user': 'ubuntu',
                'identityfile': '~/.ssh/dev-key',
                'serveraliveinterval': '60',
                'serveralivecountmax': '3',
            }
            matches = 0
            for key, expected in required_fields.items():
                actual = entry.get(key, '')
                if actual.strip() == expected:
                    matches += 1
                else:
                    print(f"FAIL: Component 1 — dev-server.{key}: expected '{expected}', found '{actual}'")

            if matches == len(required_fields):
                print(f"PASS: Component 1 — dev-server entry has all 5 correct fields (0.35 pts)")
                total_score += 0.35
            elif matches >= 3:
                partial = round(0.35 * matches / len(required_fields), 2)
                print(f"PARTIAL: Component 1 — {matches}/5 fields correct ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 1 — Only {matches}/5 fields correct")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: .vscode/settings.json with remote.SSH.defaultExtensions (0.25 points)
    try:
        settings_path = os.path.join(PROJECT_DIR, '.vscode', 'settings.json')
        if not os.path.exists(settings_path):
            print(f"FAIL: Component 2 — {settings_path} does not exist")
        else:
            with open(settings_path, 'r') as f:
                content = f.read()
            # Strip JSONC comments
            clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            settings = json.loads(clean)

            ext_list = settings.get('remote.SSH.defaultExtensions', [])
            if not isinstance(ext_list, list):
                print(f"FAIL: Component 2 — remote.SSH.defaultExtensions is not a list")
            elif len(ext_list) < 3:
                print(f"FAIL: Component 2 — remote.SSH.defaultExtensions has {len(ext_list)} entries, need >= 3")
            else:
                # Check that entries look like extension IDs (publisher.name format)
                valid_ids = [e for e in ext_list if isinstance(e, str) and '.' in e]
                if len(valid_ids) >= 3:
                    print(f"PASS: Component 2 — remote.SSH.defaultExtensions has {len(valid_ids)} valid extension IDs (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 2 — Only {len(valid_ids)} entries look like valid extension IDs (need >= 3)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: remote-workspace.code-workspace exists with remote SSH folder (0.20 points)
    try:
        ws_path = os.path.join(PROJECT_DIR, 'remote-workspace.code-workspace')
        if not os.path.exists(ws_path):
            print(f"FAIL: Component 3 — {ws_path} does not exist")
        else:
            with open(ws_path, 'r') as f:
                ws_data = json.load(f)

            folders = ws_data.get('folders', [])
            if not folders:
                print("FAIL: Component 3 — workspace has no folders defined")
            else:
                # Check that at least one folder references /home/ubuntu/projects on dev-server
                matching = [
                    f for f in folders
                    if (('/home/ubuntu/projects' in (f.get('uri', '') or f.get('path', ''))
                         and ('dev-server' in (f.get('uri', '') or '') or 'ssh' in (f.get('uri', '') or '').lower()))
                        or f.get('path', '') == '/home/ubuntu/projects')
                ]

                if len(matching) > 0:
                    print(f"PASS: Component 3 — workspace references remote /home/ubuntu/projects (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 3 — workspace folders don't reference /home/ubuntu/projects on remote: {folders}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: .vscode/tasks.json has 'Remote: Deploy' task with scp (0.20 points)
    try:
        tasks_path = os.path.join(PROJECT_DIR, '.vscode', 'tasks.json')
        if not os.path.exists(tasks_path):
            print(f"FAIL: Component 4 — {tasks_path} does not exist")
        else:
            with open(tasks_path, 'r') as f:
                content = f.read()
            clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            tasks_data = json.loads(clean)

            tasks = tasks_data.get('tasks', [])
            deploy_task = None
            for t in tasks:
                if t.get('label', '').lower() == 'remote: deploy':
                    deploy_task = t
                    break

            if deploy_task is None:
                print("FAIL: Component 4 — No task with label 'Remote: Deploy' found")
            else:
                # Check it uses scp
                command = deploy_task.get('command', '')
                args = deploy_task.get('args', [])
                # Combine command and args for analysis
                full_cmd = command + ' ' + ' '.join(str(a) for a in args)

                has_scp = 'scp' in command.lower() or 'scp' in full_cmd.lower()
                has_dist = 'dist' in full_cmd
                has_dest = 'dev-server' in full_cmd and '/home/ubuntu/projects/app' in full_cmd

                if has_scp and has_dist and has_dest:
                    print(f"PASS: Component 4 — 'Remote: Deploy' task uses scp with dist/ -> dev-server (0.20 pts)")
                    total_score += 0.20
                else:
                    details = []
                    if not has_scp:
                        details.append("missing scp command")
                    if not has_dist:
                        details.append("missing dist/ source")
                    if not has_dest:
                        details.append("missing dev-server:/home/ubuntu/projects/app/ destination")
                    print(f"FAIL: Component 4 — 'Remote: Deploy' issues: {', '.join(details)}")
                    print(f"  Full command: {full_cmd}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
