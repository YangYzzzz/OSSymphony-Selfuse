"""
Reward Script: Configure Kubernetes Ingress resource for api-server
Task ID: os_gf2_040
Domain: os (Kubernetes YAML manifest)
Scoring:
  Component 1 (0.15): Valid YAML with correct apiVersion and kind
  Component 2 (0.20): Correct metadata (name, namespace)
  Component 3 (0.20): Rate limiting annotation
  Component 4 (0.20): TLS configuration
  Component 5 (0.25): Ingress rule with correct backend
"""

import os
import yaml  # PyYAML is available on the VM

WORKDIR = '/home/user'
TASK_ID = 'os_gf2_040'
INGRESS_PATH = os.path.join(WORKDIR, 'k8s-manifests', 'production', 'api-ingress.yaml')


def verify_task(file_path):
    """
    Verify Kubernetes Ingress manifest with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be valid YAML
    if not os.path.isfile(file_path):
        print(f"CRITICAL: Ingress file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            doc = yaml.safe_load(f)
    except Exception as e:
        print(f"CRITICAL: Cannot parse YAML file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not isinstance(doc, dict):
        print(f"CRITICAL: YAML root is not a mapping: {type(doc)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Correct apiVersion and kind (0.15 points)
    try:
        api_version = doc.get('apiVersion', '')
        kind = doc.get('kind', '')
        if api_version == 'networking.k8s.io/v1' and kind == 'Ingress':
            print(f"PASS: Component 1 — apiVersion={api_version}, kind={kind} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — expected apiVersion=networking.k8s.io/v1 kind=Ingress, "
                  f"found apiVersion={api_version} kind={kind}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Correct metadata name and namespace (0.20 points)
    try:
        metadata = doc.get('metadata', {})
        name = metadata.get('name', '')
        namespace = metadata.get('namespace', '')
        if name == 'api-ingress' and namespace == 'production':
            print(f"PASS: Component 2 — name={name}, namespace={namespace} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — expected name=api-ingress namespace=production, "
                  f"found name={name} namespace={namespace}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Rate limiting annotation (0.20 points)
    try:
        annotations = doc.get('metadata', {}).get('annotations', {})
        rpm_value = annotations.get('nginx.ingress.kubernetes.io/limit-rpm', None)
        # Accept both string "100" and integer 100
        if rpm_value is not None and str(rpm_value) == '100':
            print(f"PASS: Component 3 — rate limit annotation limit-rpm={rpm_value} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — expected annotation limit-rpm=100, found: {rpm_value}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: TLS configuration (0.20 points)
    try:
        spec = doc.get('spec', {})
        tls_list = spec.get('tls', [])
        tls_ok = False
        if isinstance(tls_list, list) and len(tls_list) > 0:
            tls_entry = tls_list[0]
            hosts = tls_entry.get('hosts', [])
            secret_name = tls_entry.get('secretName', '')
            if 'api.company.com' in hosts and secret_name == 'api-tls-secret':
                tls_ok = True
        if tls_ok:
            print(f"PASS: Component 4 — TLS host=api.company.com, secretName=api-tls-secret (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — TLS config incorrect. tls section: {tls_list}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Ingress rule with correct host, path, pathType, and backend (0.25 points)
    try:
        spec = doc.get('spec', {})
        rules = spec.get('rules', [])
        rule_ok = False
        if isinstance(rules, list) and len(rules) > 0:
            rule = rules[0]
            host = rule.get('host', '')
            paths = rule.get('http', {}).get('paths', [])
            if host == 'api.company.com' and isinstance(paths, list) and len(paths) > 0:
                path_entry = paths[0]
                path_val = path_entry.get('path', '')
                path_type = path_entry.get('pathType', '')
                backend = path_entry.get('backend', {})
                svc = backend.get('service', {})
                svc_name = svc.get('name', '')
                svc_port = svc.get('port', {})
                # Port can be specified as 'number' (int) or 'name' (string)
                port_number = svc_port.get('number', None)
                if (path_val == '/' and path_type == 'Prefix' and
                        svc_name == 'api-server' and port_number == 8080):
                    rule_ok = True
        if rule_ok:
            print(f"PASS: Component 5 — rule host=api.company.com path=/ pathType=Prefix "
                  f"backend=api-server:8080 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 5 — Ingress rule incorrect. rules section: {rules}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(INGRESS_PATH):
    print(f"File not found: {INGRESS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(INGRESS_PATH)
