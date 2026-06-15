"""
Reward Script: Helm values.yaml override file verification
Task ID: vscode_ops_094
Domain: vscode
Scoring:
  - Component 1: File exists and is valid YAML (0.10)
  - Component 2: replicaCount is 3 (0.15)
  - Component 3: resource limits (memory 512Mi, cpu 1) (0.20)
  - Component 4: ingress.enabled is true (0.10)
  - Component 5: ingress.hosts contains app.company.com (0.15)
  - Component 6: ingress.tls configured with app.company.com host (0.15)
  - Component 7: cert-manager annotation with letsencrypt-prod issuer (0.15)
"""

import os
import yaml

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_094'
FILE_PATH = os.path.join(WORKDIR, 'helm-deploy', 'custom-values.yaml')


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

    # Component 1: File is valid YAML (0.10 points)
    data = None
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        if isinstance(data, dict) and len(data) > 0:
            print(f"PASS: Component 1 - File is valid YAML with {len(data)} top-level keys (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 - File is not a valid YAML dict, got: {type(data)}")
    except Exception as e:
        print(f"ERROR: Component 1 - Cannot parse YAML: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: replicaCount is 3 (0.15 points)
    try:
        replica_count = data.get('replicaCount')
        if replica_count == 3:
            print(f"PASS: Component 2 - replicaCount is 3 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 - Expected replicaCount=3, found: {replica_count}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: resource limits - memory 512Mi, cpu 1 (0.20 points)
    try:
        resources = data.get('resources', {})
        limits = resources.get('limits', {}) if isinstance(resources, dict) else {}
        memory_val = limits.get('memory', '') if isinstance(limits, dict) else ''
        cpu_val = limits.get('cpu', None) if isinstance(limits, dict) else None

        memory_ok = str(memory_val).strip() == '512Mi'
        # cpu can be int 1 or string "1"
        cpu_ok = str(cpu_val).strip() in ('1', '1.0')

        if memory_ok and cpu_ok:
            print(f"PASS: Component 3 - resources.limits.memory={memory_val}, cpu={cpu_val} (0.20 pts)")
            total_score += 0.20
        elif memory_ok or cpu_ok:
            print(f"PARTIAL: Component 3 - memory_ok={memory_ok} ({memory_val}), cpu_ok={cpu_ok} ({cpu_val}) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 - Expected memory=512Mi, cpu=1; found memory={memory_val}, cpu={cpu_val}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: ingress.enabled is true (0.10 points)
    try:
        ingress = data.get('ingress', {})
        if not isinstance(ingress, dict):
            ingress = {}
        ingress_enabled = ingress.get('enabled')
        if ingress_enabled is True:
            print(f"PASS: Component 4 - ingress.enabled is true (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 - Expected ingress.enabled=true, found: {ingress_enabled}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: ingress.hosts contains app.company.com (0.15 points)
    try:
        ingress = data.get('ingress', {})
        if not isinstance(ingress, dict):
            ingress = {}
        hosts = ingress.get('hosts', [])
        host_found = False
        if isinstance(hosts, list):
            for host_entry in hosts:
                if isinstance(host_entry, dict):
                    if host_entry.get('host') == 'app.company.com':
                        host_found = True
                        break
                elif isinstance(host_entry, str):
                    if host_entry == 'app.company.com':
                        host_found = True
                        break
        if host_found:
            print(f"PASS: Component 5 - ingress.hosts contains app.company.com (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 - app.company.com not found in ingress.hosts: {hosts}")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: ingress.tls configured with app.company.com (0.15 points)
    try:
        ingress = data.get('ingress', {})
        if not isinstance(ingress, dict):
            ingress = {}
        tls = ingress.get('tls', [])
        tls_host_found = False
        if isinstance(tls, list):
            for tls_entry in tls:
                if isinstance(tls_entry, dict):
                    tls_hosts = tls_entry.get('hosts', [])
                    if isinstance(tls_hosts, list) and 'app.company.com' in tls_hosts:
                        tls_host_found = True
                        break
        if tls_host_found:
            print(f"PASS: Component 6 - ingress.tls has app.company.com host (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 - app.company.com not found in ingress.tls hosts: {tls}")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    # Component 7: cert-manager annotation with letsencrypt-prod issuer (0.15 points)
    try:
        ingress = data.get('ingress', {})
        if not isinstance(ingress, dict):
            ingress = {}
        annotations = ingress.get('annotations', {})
        issuer_found = False
        if isinstance(annotations, dict):
            # Check common cert-manager annotation keys
            for key in ['cert-manager.io/cluster-issuer', 'certmanager.io/cluster-issuer',
                        'cert-manager.io/issuer']:
                val = annotations.get(key, '')
                if 'letsencrypt-prod' in str(val):
                    issuer_found = True
                    break
        if issuer_found:
            print(f"PASS: Component 7 - cert-manager annotation with letsencrypt-prod (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 7 - letsencrypt-prod not found in ingress.annotations: {annotations}")
    except Exception as e:
        print(f"ERROR: Component 7 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
