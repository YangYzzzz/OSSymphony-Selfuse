"""
Reward Script: Kubernetes Development Workflow in VSCode
Task ID: vscode_wf_088
Domain: vscode
Scoring:
  Component 1: K8s extension installed (0.15)
  Component 2: deployment.yaml with proper K8s Deployment spec (0.25)
  Component 3: service.yaml with proper K8s Service spec (0.15)
  Component 4: configmap.yaml with proper K8s ConfigMap spec (0.15)
  Component 5: tasks.json with all 5 k8s tasks (0.20)
  Component 6: settings.json with yaml.schemas for kubernetes (0.10)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
K8S_DIR = os.path.join(PROJECT, 'k8s')
VSCODE_DIR = os.path.join(PROJECT, '.vscode')
TASK_ID = 'vscode_wf_088'


def load_yaml_as_text(path):
    """Load a YAML file as text for pattern-based verification."""
    with open(path, 'r') as f:
        return f.read()


def load_json_safe(path):
    """Load a JSON file, handling JSONC comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Try direct parse first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    # Strip JSONC comments: only full-line comments (avoid stripping // inside URLs)
    cleaned = re.sub(r'^\s*//.*$', '', content, flags=re.MULTILINE)
    return json.loads(cleaned)


def check_deployment(content):
    """Check deployment.yaml content. Returns (score, checks_list)."""
    sub_score = 0.0
    checks = []
    if re.search(r'apiVersion:\s*apps/v1', content):
        sub_score += 0.05
        checks.append("apiVersion=apps/v1")
    if re.search(r'kind:\s*Deployment', content):
        sub_score += 0.05
        checks.append("kind=Deployment")
    if re.search(r'replicas:\s*\d+', content):
        sub_score += 0.03
        checks.append("replicas set")
    if re.search(r'containerPort:\s*\d+', content):
        sub_score += 0.03
        checks.append("containerPort set")
    if re.search(r'livenessProbe:', content) or re.search(r'readinessProbe:', content):
        sub_score += 0.05
        checks.append("health probes present")
    if re.search(r'matchLabels:', content):
        sub_score += 0.04
        checks.append("matchLabels present")
    return sub_score, checks


def check_service(content):
    """Check service.yaml content. Returns (score, checks_list)."""
    sub_score = 0.0
    checks = []
    if re.search(r'apiVersion:\s*v1', content):
        sub_score += 0.03
        checks.append("apiVersion=v1")
    if re.search(r'kind:\s*Service', content):
        sub_score += 0.03
        checks.append("kind=Service")
    if re.search(r'type:\s*(ClusterIP|NodePort)', content):
        sub_score += 0.04
        checks.append("type=ClusterIP/NodePort")
    if re.search(r'port:\s*\d+', content) and re.search(r'targetPort:\s*\d+', content):
        sub_score += 0.03
        checks.append("ports configured")
    if re.search(r'selector:', content):
        sub_score += 0.02
        checks.append("selector present")
    return sub_score, checks


def check_configmap(content):
    """Check configmap.yaml content. Returns (score, checks_list)."""
    sub_score = 0.0
    checks = []
    if re.search(r'apiVersion:\s*v1', content):
        sub_score += 0.03
        checks.append("apiVersion=v1")
    if re.search(r'kind:\s*ConfigMap', content):
        sub_score += 0.04
        checks.append("kind=ConfigMap")
    if re.search(r'data:', content) and re.search(r'data:\s*\n\s+\S+:', content):
        sub_score += 0.05
        checks.append("data section with keys")
    if re.search(r'name:\s*\S+', content):
        sub_score += 0.03
        checks.append("metadata name present")
    return sub_score, checks


def count_valid_k8s_tasks(tasks_list):
    """Count how many of the 5 required k8s tasks have valid kubectl commands."""
    valid = 0
    for t in tasks_list:
        label = t.get('label', '')
        cmd = t.get('command', '')
        if label == 'k8s-apply' and 'kubectl' in cmd and 'apply' in cmd:
            valid += 1
        elif label == 'k8s-delete' and 'kubectl' in cmd and 'delete' in cmd:
            valid += 1
        elif label == 'k8s-logs' and 'kubectl' in cmd and 'log' in cmd:
            valid += 1
        elif label == 'k8s-port-forward' and 'kubectl' in cmd and 'port-forward' in cmd:
            valid += 1
        elif label == 'k8s-status' and 'kubectl' in cmd and ('get' in cmd or 'status' in cmd):
            valid += 1
    return valid


def count_k8s_schema_urls(yaml_schemas):
    """Count schema URLs that reference kubernetes JSON schemas."""
    count = 0
    for url in yaml_schemas.keys():
        if 'kubernetes' in url.lower() or 'k8s' in url.lower():
            count += 1
    return count


def verify_task():
    """
    Verify Kubernetes development workflow task completion.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: K8s extension installed (0.15 points)
    try:
        result = os.popen('code --list-extensions 2>/dev/null').read()
        ext_list = [e.strip().lower() for e in result.strip().split('\n') if e.strip()]
        if 'ms-kubernetes-tools.vscode-kubernetes-tools' in ext_list:
            print(f"PASS: Component 1 — K8s extension installed (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — K8s extension not found. Extensions: {ext_list}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: deployment.yaml with proper K8s Deployment spec (0.25 points)
    try:
        deploy_path = os.path.join(K8S_DIR, 'deployment.yaml')
        if os.path.isfile(deploy_path):
            content = load_yaml_as_text(deploy_path)
            sub_score, checks = check_deployment(content)
            if sub_score > 0:
                total_score += sub_score
            if sub_score >= 0.25:
                print(f"PASS: Component 2 — deployment.yaml valid: {', '.join(checks)} ({sub_score} pts)")
            else:
                print(f"PARTIAL: Component 2 — deployment.yaml: {', '.join(checks)} ({sub_score}/0.25 pts)")
        else:
            print(f"FAIL: Component 2 — deployment.yaml not found at {deploy_path}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: service.yaml with proper K8s Service spec (0.15 points)
    try:
        svc_path = os.path.join(K8S_DIR, 'service.yaml')
        if os.path.isfile(svc_path):
            content = load_yaml_as_text(svc_path)
            sub_score, checks = check_service(content)
            if sub_score > 0:
                total_score += sub_score
            if sub_score >= 0.15:
                print(f"PASS: Component 3 — service.yaml valid: {', '.join(checks)} ({sub_score} pts)")
            else:
                print(f"PARTIAL: Component 3 — service.yaml: {', '.join(checks)} ({sub_score}/0.15 pts)")
        else:
            print(f"FAIL: Component 3 — service.yaml not found at {svc_path}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: configmap.yaml with proper K8s ConfigMap spec (0.15 points)
    try:
        cm_path = os.path.join(K8S_DIR, 'configmap.yaml')
        if os.path.isfile(cm_path):
            content = load_yaml_as_text(cm_path)
            sub_score, checks = check_configmap(content)
            if sub_score > 0:
                total_score += sub_score
            if sub_score >= 0.15:
                print(f"PASS: Component 4 — configmap.yaml valid: {', '.join(checks)} ({sub_score} pts)")
            else:
                print(f"PARTIAL: Component 4 — configmap.yaml: {', '.join(checks)} ({sub_score}/0.15 pts)")
        else:
            print(f"FAIL: Component 4 — configmap.yaml not found at {cm_path}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: tasks.json with all 5 k8s tasks (0.20 points)
    try:
        tasks_path = os.path.join(VSCODE_DIR, 'tasks.json')
        if os.path.isfile(tasks_path):
            tasks_config = load_json_safe(tasks_path)
            tasks_list = tasks_config.get('tasks', [])
            task_labels = [t.get('label', '') for t in tasks_list]

            required_tasks = ['k8s-apply', 'k8s-delete', 'k8s-logs', 'k8s-port-forward', 'k8s-status']
            found_tasks = [rt for rt in required_tasks if rt in task_labels]
            missing_tasks = [rt for rt in required_tasks if rt not in task_labels]
            found_count = len(found_tasks)

            valid_count = count_valid_k8s_tasks(tasks_list)

            # 0.02 per found label + 0.02 per valid command = 0.04 per task, 0.20 total
            if found_count > 0 or valid_count > 0:
                sub_score = (found_count * 0.02) + (valid_count * 0.02)
                total_score += sub_score
                if sub_score >= 0.20:
                    print(f"PASS: Component 5 — All 5 k8s tasks with valid commands ({sub_score} pts)")
                else:
                    print(f"PARTIAL: Component 5 — Found: {found_tasks}, missing: {missing_tasks}, valid cmds: {valid_count}/5 ({sub_score}/0.20 pts)")
            else:
                print(f"FAIL: Component 5 — No k8s tasks found in tasks.json. Labels: {task_labels}")
        else:
            print(f"FAIL: Component 5 — tasks.json not found at {tasks_path}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: settings.json has yaml.schemas for kubernetes (0.10 points)
    try:
        settings_path = os.path.join(VSCODE_DIR, 'settings.json')
        if os.path.isfile(settings_path):
            settings = load_json_safe(settings_path)
            yaml_schemas = settings.get('yaml.schemas', {})

            if yaml_schemas:
                k8s_count = count_k8s_schema_urls(yaml_schemas)
                if k8s_count >= 1:
                    total_score += 0.10
                    print(f"PASS: Component 6 — yaml.schemas configured with {k8s_count} kubernetes schemas (0.10 pts)")
                else:
                    print(f"FAIL: Component 6 — yaml.schemas present but no kubernetes schema URLs: {list(yaml_schemas.keys())}")
            else:
                print(f"FAIL: Component 6 — yaml.schemas not found in settings.json")
        else:
            print(f"FAIL: Component 6 — settings.json not found at {settings_path}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
