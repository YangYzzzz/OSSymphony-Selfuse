"""
Reward Script: VSCode workspace backup and sync workflow
Task ID: vscode_wf_095
Domain: vscode (file-based)
Scoring:
  Component 1 (0.15): workspace-setup.sh exists and is executable
  Component 2 (0.20): workspace-setup.sh content quality
  Component 3 (0.30): tasks.json has all 4 required task labels
  Component 4 (0.15): tasks.json task command correctness
  Component 5 (0.20): extensions.json has 10+ recommendations
"""

import os
import json
import stat
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'project')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')
TASK_ID = 'vscode_wf_095'

REQUIRED_TASK_LABELS = ['backup-config', 'restore-config', 'sync-extensions', 'verify-setup']


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ── Component 1: workspace-setup.sh exists and is executable (0.15 points) ──
    setup_sh_path = os.path.join(VSCODE_DIR, 'workspace-setup.sh')
    try:
        if os.path.isfile(setup_sh_path):
            mode = os.stat(setup_sh_path).st_mode
            if mode & stat.S_IXUSR:
                print(f"PASS: Component 1 — workspace-setup.sh exists and is executable (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — workspace-setup.sh exists but is NOT executable (mode={oct(mode)})")
        else:
            print(f"FAIL: Component 1 — workspace-setup.sh does not exist at {setup_sh_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ── Component 2: workspace-setup.sh content quality (0.20 points) ──
    # Must: install extensions, apply settings, configure git hooks, be idempotent
    try:
        if os.path.isfile(setup_sh_path):
            with open(setup_sh_path, 'r') as f:
                sh_content = f.read().lower()
            sub_score = 0.0
            checks_passed = []
            checks_failed = []

            # 2a: References extensions / installs them
            if 'install-extension' in sh_content or 'extensions.json' in sh_content:
                sub_score += 0.05
                checks_passed.append('installs extensions')
            else:
                checks_failed.append('does not install extensions')

            # 2b: Applies settings
            if 'settings' in sh_content:
                sub_score += 0.05
                checks_passed.append('applies settings')
            else:
                checks_failed.append('does not apply settings')

            # 2c: Configures git hooks
            if 'hook' in sh_content or 'git' in sh_content:
                sub_score += 0.05
                checks_passed.append('configures git hooks')
            else:
                checks_failed.append('does not configure git hooks')

            # 2d: Idempotent indicators (mkdir -p, --force, conditional checks)
            if 'mkdir -p' in sh_content or '--force' in sh_content or 'if ' in sh_content:
                sub_score += 0.05
                checks_passed.append('idempotent patterns')
            else:
                checks_failed.append('no idempotent patterns found')

            if sub_score > 0:
                print(f"PASS: Component 2 — workspace-setup.sh content ({sub_score:.2f} pts) passed=[{', '.join(checks_passed)}]")
                if checks_failed:
                    print(f"  partial fails: [{', '.join(checks_failed)}]")
                total_score += sub_score
            else:
                print(f"FAIL: Component 2 — workspace-setup.sh content has none of the required elements")
        else:
            print(f"FAIL: Component 2 — workspace-setup.sh does not exist, cannot check content")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ── Component 3: tasks.json has all 4 required task labels (0.30 points) ──
    tasks_path = os.path.join(VSCODE_DIR, 'tasks.json')
    tasks_data = None
    try:
        if os.path.isfile(tasks_path):
            with open(tasks_path, 'r') as f:
                content = f.read()
            # Strip JSONC comments
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            tasks_data = json.loads(content_clean)
            task_labels = set()
            for task in tasks_data.get('tasks', []):
                label = task.get('label', '')
                task_labels.add(label)

            found_labels = []
            missing_labels = []
            per_label_pts = 0.30 / len(REQUIRED_TASK_LABELS)  # 0.075 each
            label_score = 0.0
            for req_label in REQUIRED_TASK_LABELS:
                if req_label in task_labels:
                    found_labels.append(req_label)
                    label_score += per_label_pts
                else:
                    missing_labels.append(req_label)

            if label_score > 0:
                print(f"PASS: Component 3 — tasks.json labels ({label_score:.2f} pts) found={found_labels}")
                if missing_labels:
                    print(f"  missing labels: {missing_labels}")
                total_score += label_score
            else:
                print(f"FAIL: Component 3 — tasks.json has none of the required labels. Found: {task_labels}")
        else:
            print(f"FAIL: Component 3 — tasks.json does not exist at {tasks_path}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ── Component 4: tasks.json task command correctness (0.15 points) ──
    try:
        if tasks_data and 'tasks' in tasks_data:
            task_map = {}
            for task in tasks_data['tasks']:
                label = task.get('label', '')
                cmd = task.get('command', '')
                task_map[label] = cmd

            cmd_score = 0.0
            cmd_checks_passed = []
            cmd_checks_failed = []

            # 4a: backup-config copies .vscode files to backup location
            backup_cmd = task_map.get('backup-config', '').lower()
            if backup_cmd and ('cp' in backup_cmd or 'copy' in backup_cmd or 'rsync' in backup_cmd) and ('backup' in backup_cmd or '.vscode-backup' in backup_cmd):
                cmd_score += 0.0375
                cmd_checks_passed.append('backup-config copies to backup')
            else:
                cmd_checks_failed.append('backup-config missing or wrong')

            # 4b: restore-config restores from backup
            restore_cmd = task_map.get('restore-config', '').lower()
            if restore_cmd and ('cp' in restore_cmd or 'copy' in restore_cmd or 'rsync' in restore_cmd) and ('backup' in restore_cmd or '.vscode-backup' in restore_cmd):
                cmd_score += 0.0375
                cmd_checks_passed.append('restore-config restores from backup')
            else:
                cmd_checks_failed.append('restore-config missing or wrong')

            # 4c: sync-extensions reads extensions.json or installs extensions
            sync_cmd = task_map.get('sync-extensions', '').lower()
            if sync_cmd and ('extensions' in sync_cmd or 'install-extension' in sync_cmd):
                cmd_score += 0.0375
                cmd_checks_passed.append('sync-extensions installs from list')
            else:
                cmd_checks_failed.append('sync-extensions missing or wrong')

            # 4d: verify-setup checks tools
            verify_cmd = task_map.get('verify-setup', '').lower()
            if verify_cmd and ('which' in verify_cmd or 'version' in verify_cmd or '--version' in verify_cmd or 'command -v' in verify_cmd):
                cmd_score += 0.0375
                cmd_checks_passed.append('verify-setup checks tools')
            else:
                cmd_checks_failed.append('verify-setup missing or wrong')

            if cmd_score > 0:
                print(f"PASS: Component 4 — task commands ({cmd_score:.4f} pts) passed=[{', '.join(cmd_checks_passed)}]")
                if cmd_checks_failed:
                    print(f"  partial fails: [{', '.join(cmd_checks_failed)}]")
                total_score += cmd_score
            else:
                print(f"FAIL: Component 4 — no task commands pass correctness checks")
        else:
            print(f"FAIL: Component 4 — tasks.json not loaded, cannot check commands")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ── Component 5: extensions.json has 10+ recommendations (0.20 points) ──
    ext_path = os.path.join(VSCODE_DIR, 'extensions.json')
    try:
        if os.path.isfile(ext_path):
            with open(ext_path, 'r') as f:
                ext_content = f.read()
            ext_clean = re.sub(r'//.*$', '', ext_content, flags=re.MULTILINE)
            ext_data = json.loads(ext_clean)
            recommendations = ext_data.get('recommendations', [])
            count = len(recommendations)

            if count >= 10:
                print(f"PASS: Component 5 — extensions.json has {count} recommendations (>=10) (0.20 pts)")
                total_score += 0.20
            elif count >= 5:
                partial = 0.10
                print(f"PARTIAL: Component 5 — extensions.json has {count} recommendations (>=5 but <10) ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — extensions.json has only {count} recommendations (need >=10)")
        else:
            print(f"FAIL: Component 5 — extensions.json does not exist at {ext_path}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
