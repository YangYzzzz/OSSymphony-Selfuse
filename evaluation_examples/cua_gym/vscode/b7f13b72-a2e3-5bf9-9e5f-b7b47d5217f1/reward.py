"""
Reward Script: Verify .vscode/tasks.json with Terraform tasks
Task ID: vscode_ops_095
Domain: vscode
Scoring:
  1. File exists, valid JSON, version 2.0.0, has 4 tasks (0.15)
  2. Terraform Init task correct (0.15)
  3. Terraform Plan task correct with dependsOn Init (0.20)
  4. Terraform Apply task correct using tfplan, dependsOn Plan (0.25)
  5. Terraform Destroy task correct, independent (0.10)
  6. Presentation options on all tasks (0.15)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_095'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'terraform-iac', '.vscode', 'tasks.json')


def find_task_by_label(tasks, label):
    """Find a task dict by its label (case-insensitive)."""
    for t in tasks:
        if isinstance(t, dict) and t.get('label', '').lower() == label.lower():
            return t
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be valid JSON
    if not os.path.exists(TASKS_JSON_PATH):
        print(f"CRITICAL: tasks.json not found at {TASKS_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(TASKS_JSON_PATH, 'r') as f:
            content = f.read()
        # Handle JSONC (strip comments)
        import re
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        data = json.loads(cleaned)
    except Exception as e:
        print(f"CRITICAL: Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    tasks = data.get('tasks', [])

    # Component 1: Structure — version 2.0.0 and exactly 4 tasks (0.15 pts)
    try:
        version_ok = data.get('version') == '2.0.0'
        count_ok = len(tasks) == 4
        if version_ok and count_ok:
            print(f"PASS: Component 1 — version=2.0.0, task count=4 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — version={data.get('version')}, task count={len(tasks)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Terraform Init task (0.15 pts)
    try:
        init_task = find_task_by_label(tasks, 'Terraform Init')
        if init_task is None:
            print("FAIL: Component 2 — 'Terraform Init' task not found")
        else:
            cmd = init_task.get('command', '')
            if 'terraform init' in cmd.lower():
                print(f"PASS: Component 2 — Terraform Init command='{cmd}' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — Terraform Init command='{cmd}', expected 'terraform init'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Terraform Plan task with dependsOn Init (0.20 pts)
    try:
        plan_task = find_task_by_label(tasks, 'Terraform Plan')
        if plan_task is None:
            print("FAIL: Component 3 — 'Terraform Plan' task not found")
        else:
            cmd = plan_task.get('command', '')
            depends = plan_task.get('dependsOn', [])
            cmd_ok = 'terraform plan' in cmd.lower() and '-out=' in cmd and 'tfplan' in cmd
            depends_ok = any('terraform init' in d.lower() if isinstance(d, str) else False for d in depends)
            if cmd_ok and depends_ok:
                print(f"PASS: Component 3 — Plan command='{cmd}', dependsOn includes Init (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — cmd_ok={cmd_ok} (cmd='{cmd}'), depends_ok={depends_ok} (deps={depends})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Terraform Apply task using tfplan, dependsOn Plan (0.25 pts)
    try:
        apply_task = find_task_by_label(tasks, 'Terraform Apply')
        if apply_task is None:
            print("FAIL: Component 4 — 'Terraform Apply' task not found")
        else:
            cmd = apply_task.get('command', '')
            depends = apply_task.get('dependsOn', [])
            cmd_ok = 'terraform apply' in cmd.lower() and 'tfplan' in cmd
            depends_ok = any('terraform plan' in d.lower() if isinstance(d, str) else False for d in depends)
            if cmd_ok and depends_ok:
                print(f"PASS: Component 4 — Apply command='{cmd}', dependsOn includes Plan (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 — cmd_ok={cmd_ok} (cmd='{cmd}'), depends_ok={depends_ok} (deps={depends})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Terraform Destroy task, independent (0.10 pts)
    try:
        destroy_task = find_task_by_label(tasks, 'Terraform Destroy')
        if destroy_task is None:
            print("FAIL: Component 5 — 'Terraform Destroy' task not found")
        else:
            cmd = destroy_task.get('command', '')
            depends = destroy_task.get('dependsOn', [])
            cmd_ok = 'terraform destroy' in cmd.lower()
            independent = len(depends) == 0
            if cmd_ok and independent:
                print(f"PASS: Component 5 — Destroy command='{cmd}', no dependencies (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — cmd_ok={cmd_ok} (cmd='{cmd}'), independent={independent} (deps={depends})")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Presentation options on all 4 tasks (0.15 pts)
    try:
        all_labels = ['Terraform Init', 'Terraform Plan', 'Terraform Apply', 'Terraform Destroy']
        pres_ok_count = 0
        for label in all_labels:
            t = find_task_by_label(tasks, label)
            if t is not None:
                pres = t.get('presentation', {})
                if pres.get('reveal') == 'always' and pres.get('panel') == 'shared':
                    pres_ok_count += 1
                else:
                    print(f"  INFO: '{label}' presentation: {pres}")
        if pres_ok_count == 4:
            print(f"PASS: Component 6 — All 4 tasks have reveal=always, panel=shared (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 — Only {pres_ok_count}/4 tasks have correct presentation options")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
