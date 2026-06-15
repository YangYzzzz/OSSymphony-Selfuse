"""
Reward Script: Write a Kubernetes ConfigMap YAML file with nginx.conf multi-line config
Task ID: vscode_ops_062
Domain: vscode
Scoring:
  Component 1 (0.25): File exists, valid YAML, apiVersion=v1, kind=ConfigMap
  Component 2 (0.25): data section has nginx.conf key with multi-line string (literal block scalar)
  Component 3 (0.25): nginx.conf contains a server block with listen directive
  Component 4 (0.25): nginx.conf contains location block with proxy_pass directive
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_062'


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

    # Read raw content for block scalar check
    try:
        with open(file_path, 'r') as f:
            raw_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse YAML
    try:
        import yaml
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"CRITICAL: Invalid YAML in {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not isinstance(data, dict):
        print(f"CRITICAL: YAML root is not a mapping, got {type(data)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: apiVersion=v1 and kind=ConfigMap (0.25 points)
    try:
        api_version = data.get('apiVersion', '')
        kind = data.get('kind', '')
        if api_version == 'v1' and kind == 'ConfigMap':
            print(f"PASS: Component 1 — apiVersion={api_version}, kind={kind} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — expected apiVersion=v1 and kind=ConfigMap, found apiVersion={api_version}, kind={kind}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: data section has nginx.conf key with multi-line string using | (literal block scalar) (0.25 points)
    try:
        data_section = data.get('data', {})
        nginx_conf = data_section.get('nginx.conf', None)
        if nginx_conf is None:
            print(f"FAIL: Component 2 — no nginx.conf key in data section")
        elif not isinstance(nginx_conf, str):
            print(f"FAIL: Component 2 — nginx.conf value is not a string, got {type(nginx_conf)}")
        elif '\n' not in nginx_conf:
            print(f"FAIL: Component 2 — nginx.conf is not multi-line")
        else:
            # Check that the raw YAML uses the literal block scalar | notation
            # Look for pattern: nginx.conf: | (or nginx.conf: |+, |-, |2, etc.)
            if re.search(r'nginx\.conf:\s*\|', raw_content):
                print(f"PASS: Component 2 — nginx.conf is multi-line string with | block scalar (0.25 pts)")
                total_score += 0.25
            else:
                # Also accept > (folded block scalar) as it's also block scalar notation
                if re.search(r'nginx\.conf:\s*[|>]', raw_content):
                    print(f"PASS: Component 2 — nginx.conf uses block scalar notation (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 2 — nginx.conf is multi-line but does not use | block scalar notation in raw YAML")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: nginx config contains a server block with listen directive (0.25 points)
    try:
        nginx_conf = data.get('data', {}).get('nginx.conf', '')
        if not isinstance(nginx_conf, str):
            nginx_conf = ''

        has_server = re.search(r'server\s*\{', nginx_conf) is not None
        has_listen = re.search(r'listen\s+\S+', nginx_conf) is not None

        if has_server and has_listen:
            print(f"PASS: Component 3 — server block with listen directive found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — server block: {has_server}, listen: {has_listen}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: nginx config contains location block with proxy_pass directive (0.25 points)
    try:
        nginx_conf = data.get('data', {}).get('nginx.conf', '')
        if not isinstance(nginx_conf, str):
            nginx_conf = ''

        has_location = re.search(r'location\s+\S+', nginx_conf) is not None
        has_proxy_pass = re.search(r'proxy_pass\s+\S+', nginx_conf) is not None

        if has_location and has_proxy_pass:
            print(f"PASS: Component 4 — location block with proxy_pass directive found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — location: {has_location}, proxy_pass: {has_proxy_pass}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/k8s/configmap.yaml'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
