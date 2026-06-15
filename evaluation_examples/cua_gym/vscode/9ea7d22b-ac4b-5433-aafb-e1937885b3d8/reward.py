"""
Reward Script: Remote development preparation workflow in ~/project
Task ID: vscode_wf_065
Domain: vscode
Scoring:
  Component 1: SSH config has 'devserver' entry with required fields (0.20)
  Component 2: Remote-SSH extension installed (0.20)
  Component 3: .vscode/settings.json has remote.SSH.defaultExtensions + terminal settings (0.20)
  Component 4: setup.sh exists, is executable, installs Python/Node/Git (0.20)
  Component 5: .devcontainer/devcontainer.json with Python/Node image + extensions (0.20)
"""

import os
import json
import re
import stat

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_065'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: SSH config has 'devserver' entry (0.20 points)
    # Must have Host devserver with HostName, User, IdentityFile
    try:
        ssh_config_path = os.path.join(WORKDIR, '.ssh', 'config')
        if not os.path.exists(ssh_config_path):
            print("FAIL: Component 1 -- ~/.ssh/config not found")
        else:
            with open(ssh_config_path, 'r') as f:
                content = f.read()
            # Parse SSH config to find devserver block
            # Split into host blocks
            has_devserver = False
            has_hostname = False
            has_user = False
            has_identityfile = False

            in_devserver_block = False
            for line in content.splitlines():
                stripped = line.strip()
                if stripped.lower().startswith('host ') and not stripped.lower().startswith('hostname'):
                    hosts = stripped.split()[1:]
                    if 'devserver' in hosts:
                        in_devserver_block = True
                        has_devserver = True
                    else:
                        in_devserver_block = False
                elif in_devserver_block:
                    lower = stripped.lower()
                    if lower.startswith('hostname ') or lower.startswith('hostname='):
                        has_hostname = True
                    elif lower.startswith('user ') or lower.startswith('user='):
                        has_user = True
                    elif lower.startswith('identityfile ') or lower.startswith('identityfile='):
                        has_identityfile = True

            if has_devserver and has_hostname and has_user and has_identityfile:
                print(f"PASS: Component 1 -- SSH config has devserver with HostName, User, IdentityFile (0.20 pts)")
                total_score += 0.20
            else:
                missing = []
                if not has_devserver:
                    missing.append("Host devserver")
                if not has_hostname:
                    missing.append("HostName")
                if not has_user:
                    missing.append("User")
                if not has_identityfile:
                    missing.append("IdentityFile")
                print(f"FAIL: Component 1 -- SSH devserver missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Remote-SSH extension installed (0.20 points)
    # Check via filesystem: ~/.vscode/extensions/ contains ms-vscode-remote.remote-ssh-*
    try:
        ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
        ext_id = 'ms-vscode-remote.remote-ssh'
        found = False
        if os.path.isdir(ext_dir):
            for entry in os.listdir(ext_dir):
                if entry.lower().startswith(ext_id.lower()):
                    found = True
                    break
        if found:
            print(f"PASS: Component 2 -- Extension {ext_id} is installed (0.20 pts)")
            total_score += 0.20
        else:
            installed = os.listdir(ext_dir) if os.path.isdir(ext_dir) else []
            print(f"FAIL: Component 2 -- Extension {ext_id} not found. Extensions dir: {installed}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: .vscode/settings.json with remote.SSH.defaultExtensions and terminal settings (0.20 points)
    try:
        settings_path = os.path.join(WORKDIR, 'project', '.vscode', 'settings.json')
        if not os.path.exists(settings_path):
            print("FAIL: Component 3 -- .vscode/settings.json not found")
        else:
            with open(settings_path, 'r') as f:
                content = f.read()
            # Strip JSONC comments
            cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            settings = json.loads(cleaned)

            comp3_score = 0.0
            # Check remote.SSH.defaultExtensions (list with at least 1 extension)
            default_exts = settings.get('remote.SSH.defaultExtensions', None)
            if isinstance(default_exts, list) and len(default_exts) >= 1:
                comp3_score += 0.10
                print(f"  Component 3a: remote.SSH.defaultExtensions has {len(default_exts)} extensions")
            else:
                print(f"  FAIL: Component 3a -- remote.SSH.defaultExtensions missing or empty")

            # Check terminal settings (at least one terminal.integrated.* key)
            terminal_keys = [k for k in settings.keys() if k.startswith('terminal.integrated.')]
            if len(terminal_keys) >= 1:
                comp3_score += 0.10
                print(f"  Component 3b: Found {len(terminal_keys)} terminal settings: {terminal_keys[:3]}")
            else:
                print(f"  FAIL: Component 3b -- No terminal.integrated.* settings found")

            if comp3_score > 0:
                total_score += comp3_score
                print(f"PASS: Component 3 -- .vscode/settings.json verified ({comp3_score} pts)")
            else:
                print(f"FAIL: Component 3 -- .vscode/settings.json missing required keys")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: setup.sh exists, is executable, installs Python/Node/Git (0.20 points)
    try:
        setup_path = os.path.join(WORKDIR, 'project', 'setup.sh')
        if not os.path.exists(setup_path):
            print("FAIL: Component 4 -- setup.sh not found")
        else:
            # Check executable permission
            mode = os.stat(setup_path).st_mode
            is_executable = bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))

            with open(setup_path, 'r') as f:
                script_content = f.read().lower()

            comp4_score = 0.0
            # Must be executable
            if is_executable:
                comp4_score += 0.05
                print(f"  Component 4a: setup.sh is executable")
            else:
                print(f"  FAIL: Component 4a -- setup.sh not executable (mode: {oct(mode)})")

            # Must reference python installation
            if 'python' in script_content:
                comp4_score += 0.05
                print(f"  Component 4b: setup.sh references python")
            else:
                print(f"  FAIL: Component 4b -- setup.sh does not reference python")

            # Must reference node installation
            if 'node' in script_content:
                comp4_score += 0.05
                print(f"  Component 4c: setup.sh references node")
            else:
                print(f"  FAIL: Component 4c -- setup.sh does not reference node")

            # Must reference git installation
            if 'git' in script_content:
                comp4_score += 0.05
                print(f"  Component 4d: setup.sh references git")
            else:
                print(f"  FAIL: Component 4d -- setup.sh does not reference git")

            total_score += comp4_score
            print(f"PASS: Component 4 -- setup.sh verified ({comp4_score} pts)")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: .devcontainer/devcontainer.json with Python/Node image and extensions (0.20 points)
    try:
        devcontainer_path = os.path.join(WORKDIR, 'project', '.devcontainer', 'devcontainer.json')
        if not os.path.exists(devcontainer_path):
            print("FAIL: Component 5 -- .devcontainer/devcontainer.json not found")
        else:
            with open(devcontainer_path, 'r') as f:
                content = f.read()
            # Strip JSONC comments
            cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            dc = json.loads(cleaned)

            comp5_score = 0.0

            # Check image contains python or node reference, OR features include python/node
            image = dc.get('image', '')
            features = dc.get('features', {})
            features_str = json.dumps(features).lower()

            has_python = 'python' in image.lower() or 'python' in features_str
            has_node = 'node' in image.lower() or 'node' in features_str

            if has_python and has_node:
                comp5_score += 0.10
                print(f"  Component 5a: devcontainer has Python and Node support")
            elif has_python or has_node:
                comp5_score += 0.05
                print(f"  Component 5a: devcontainer has partial Python/Node support (python={has_python}, node={has_node})")
            else:
                print(f"  FAIL: Component 5a -- devcontainer missing Python/Node references")

            # Check extensions list exists
            exts = (dc.get('customizations', {}).get('vscode', {}).get('extensions', [])
                    or dc.get('extensions', []))
            if isinstance(exts, list) and len(exts) >= 1:
                comp5_score += 0.10
                print(f"  Component 5b: devcontainer has {len(exts)} extensions")
            else:
                print(f"  FAIL: Component 5b -- devcontainer missing extensions list")

            total_score += comp5_score
            print(f"PASS: Component 5 -- devcontainer.json verified ({comp5_score} pts)")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
