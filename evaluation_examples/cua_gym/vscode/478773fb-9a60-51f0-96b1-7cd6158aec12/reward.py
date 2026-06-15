"""
Reward Script: Create Kubernetes Ingress YAML with TLS termination
Task ID: vscode_ops_080
Domain: vscode
Scoring:
  Component 1: File exists and is valid YAML with correct apiVersion/kind (0.2)
  Component 2: TLS configuration with correct host and secretName (0.3)
  Component 3: Routing rule with correct host, service name, and port (0.3)
  Component 4: Ingress controller annotations present (0.2)
"""

import os
import sys

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_080'
FILE_PATH = os.path.join(WORKDIR, 'k8s', 'ingress.yaml')


def verify_task(file_path):
    """
    Verify Kubernetes Ingress YAML task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load and parse YAML
    try:
        # Use PyYAML if available, otherwise fall back to manual parsing
        try:
            import yaml
            with open(file_path, 'r') as f:
                doc = yaml.safe_load(f)
        except ImportError:
            # Fallback: parse YAML manually for the fields we need
            doc = _parse_yaml_fallback(file_path)

        if not isinstance(doc, dict):
            print(f"CRITICAL: YAML did not parse to a dict, got {type(doc)}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot parse YAML file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid YAML with correct apiVersion and kind (0.2 points)
    try:
        api_version = doc.get('apiVersion', '')
        kind = doc.get('kind', '')
        if api_version == 'networking.k8s.io/v1' and kind == 'Ingress':
            print(f"PASS: Component 1 — apiVersion={api_version}, kind={kind} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — expected apiVersion=networking.k8s.io/v1 and kind=Ingress, found apiVersion={api_version}, kind={kind}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: TLS configuration (0.3 points)
    # Check spec.tls has entry with host app.example.com and secretName app-tls-cert
    try:
        spec = doc.get('spec', {})
        tls_list = spec.get('tls', [])
        tls_pass = False
        if isinstance(tls_list, list):
            for tls_entry in tls_list:
                if not isinstance(tls_entry, dict):
                    continue
                hosts = tls_entry.get('hosts', [])
                secret = tls_entry.get('secretName', '')
                if 'app.example.com' in hosts and secret == 'app-tls-cert':
                    tls_pass = True
                    break
        if tls_pass:
            print(f"PASS: Component 2 — TLS with host app.example.com and secretName app-tls-cert (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — TLS config missing or incorrect. tls entries: {tls_list}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Routing rule (0.3 points)
    # Check spec.rules has host app.example.com routing to web-service port 80
    try:
        spec = doc.get('spec', {})
        rules = spec.get('rules', [])
        rule_pass = False
        if isinstance(rules, list):
            for rule in rules:
                if not isinstance(rule, dict):
                    continue
                host = rule.get('host', '')
                if host != 'app.example.com':
                    continue
                http = rule.get('http', {})
                paths = http.get('paths', []) if isinstance(http, dict) else []
                for path_entry in paths:
                    if not isinstance(path_entry, dict):
                        continue
                    backend = path_entry.get('backend', {})
                    service = backend.get('service', {}) if isinstance(backend, dict) else {}
                    svc_name = service.get('name', '')
                    port_info = service.get('port', {})
                    port_num = None
                    if isinstance(port_info, dict):
                        port_num = port_info.get('number')
                    elif isinstance(port_info, int):
                        port_num = port_info
                    if svc_name == 'web-service' and port_num == 80:
                        rule_pass = True
                        break
                if rule_pass:
                    break
        if rule_pass:
            print(f"PASS: Component 3 — Rule routes app.example.com to web-service:80 (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Routing rule missing or incorrect. rules: {rules}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Ingress controller annotations (0.2 points)
    # Check for nginx ingress class annotation or ingressClassName
    try:
        metadata = doc.get('metadata', {})
        annotations = metadata.get('annotations', {}) if isinstance(metadata, dict) else {}
        spec = doc.get('spec', {})

        has_ingress_class = False
        # Check annotation-based ingress class
        if isinstance(annotations, dict):
            ingress_class_ann = annotations.get('kubernetes.io/ingress.class', '')
            if ingress_class_ann:
                has_ingress_class = True
        # Also check spec.ingressClassName (newer API)
        if isinstance(spec, dict) and spec.get('ingressClassName'):
            has_ingress_class = True

        # Also check for any ssl/redirect related annotations
        has_ssl_annotation = False
        if isinstance(annotations, dict):
            for key in annotations:
                if 'ssl' in key.lower() or 'redirect' in key.lower():
                    has_ssl_annotation = True
                    break

        if has_ingress_class and has_ssl_annotation:
            print(f"PASS: Component 4 — Ingress class and SSL annotations present (0.2 pts)")
            total_score += 0.2
        elif has_ingress_class:
            print(f"PARTIAL: Component 4 — Ingress class annotation present but no SSL annotations (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 4 — No ingress class annotation or ingressClassName found. annotations: {annotations}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


def _parse_yaml_fallback(file_path):
    """Minimal YAML parser fallback using only stdlib."""
    # This is a very basic fallback; prefer PyYAML
    import json
    # Try converting simple YAML to JSON-like structure
    # For this task, we'll just try PyYAML import again with error
    raise ImportError("PyYAML not available and fallback not sufficient for complex YAML")


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
