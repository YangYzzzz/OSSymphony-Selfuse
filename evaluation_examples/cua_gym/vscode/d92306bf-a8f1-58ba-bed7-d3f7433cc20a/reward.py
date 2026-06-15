"""
Reward Script: Create Kubernetes deployment YAML file
Task ID: vscode_ops_041
Domain: vscode
Scoring:
  Component 1: File exists and is valid YAML with Deployment structure (0.15)
  Component 2: apiVersion apps/v1 and kind Deployment (0.15)
  Component 3: spec.replicas == 3 (0.15)
  Component 4: Container image == myapp:v2.0 (0.2)
  Component 5: Container port == 8080 (0.15)
  Component 6: Resource limits memory 256Mi and cpu 500m (0.2)
"""

import os
import sys

# PyYAML may not be available; use a simple YAML parser fallback
try:
    import yaml
except ImportError:
    yaml = None

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_041'
FILE_PATH = os.path.join(WORKDIR, 'k8s-manifests', 'app-deployment.yaml')


def parse_yaml_simple(content):
    """Simple YAML-like parser using json if yaml is unavailable.
    Falls back to basic string parsing for common K8s YAML structures."""
    if yaml is not None:
        return yaml.safe_load(content)
    # Try json as last resort (won't work for YAML but worth trying)
    import json
    try:
        return json.loads(content)
    except:
        return None


def get_nested(data, keys, default=None):
    """Safely traverse nested dict with a list of keys."""
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        elif isinstance(current, list) and isinstance(key, int) and key < len(current):
            current = current[key]
        else:
            return default
    return current


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(FILE_PATH):
        print(f"CRITICAL: File not found: {FILE_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Load and parse the YAML file
    try:
        with open(FILE_PATH, 'r') as f:
            content = f.read()
        data = parse_yaml_simple(content)
        if data is None:
            print("CRITICAL: Could not parse YAML file")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Error reading file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid YAML with basic Deployment structure (0.15 points)
    # Checks that the file parses as a dict with kind field
    try:
        if isinstance(data, dict) and 'kind' in data and 'apiVersion' in data:
            print(f"PASS: Component 1 - Valid YAML with kind={data.get('kind')} and apiVersion={data.get('apiVersion')} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - Missing kind or apiVersion fields. Data type: {type(data)}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: apiVersion == apps/v1 AND kind == Deployment (0.15 points)
    try:
        api_version = data.get('apiVersion', '')
        kind = data.get('kind', '')
        if api_version == 'apps/v1' and kind == 'Deployment':
            print(f"PASS: Component 2 - apiVersion=apps/v1 and kind=Deployment (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 - Expected apiVersion=apps/v1 and kind=Deployment, found apiVersion={api_version}, kind={kind}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: spec.replicas == 3 (0.15 points)
    try:
        replicas = get_nested(data, ['spec', 'replicas'])
        if replicas is not None and int(replicas) == 3:
            print(f"PASS: Component 3 - spec.replicas=3 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 - Expected spec.replicas=3, found: {replicas}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Container image == myapp:v2.0 (0.2 points)
    try:
        containers = get_nested(data, ['spec', 'template', 'spec', 'containers'])
        if containers and isinstance(containers, list):
            images = [c.get('image', '') for c in containers if isinstance(c, dict)]
            if 'myapp:v2.0' in images:
                print(f"PASS: Component 4 - Container image myapp:v2.0 found (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 - Expected image myapp:v2.0, found: {images}")
        else:
            print(f"FAIL: Component 4 - No containers found in spec.template.spec.containers")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Container port == 8080 (0.15 points)
    try:
        containers = get_nested(data, ['spec', 'template', 'spec', 'containers'])
        port_found = False
        if containers and isinstance(containers, list):
            for c in containers:
                if not isinstance(c, dict):
                    continue
                ports = c.get('ports', [])
                if isinstance(ports, list):
                    for p in ports:
                        if isinstance(p, dict):
                            cp = p.get('containerPort')
                            if cp is not None and int(cp) == 8080:
                                port_found = True
                                break
                if port_found:
                    break
        if port_found:
            print(f"PASS: Component 5 - containerPort 8080 found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 - Expected containerPort 8080 not found")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: Resource limits memory=256Mi and cpu=500m (0.2 points)
    try:
        containers = get_nested(data, ['spec', 'template', 'spec', 'containers'])
        limits_correct = False
        if containers and isinstance(containers, list):
            for c in containers:
                if not isinstance(c, dict):
                    continue
                limits = get_nested(c, ['resources', 'limits'])
                if isinstance(limits, dict):
                    memory = str(limits.get('memory', ''))
                    cpu = str(limits.get('cpu', ''))
                    if memory == '256Mi' and cpu == '500m':
                        limits_correct = True
                        break
        if limits_correct:
            print(f"PASS: Component 6 - Resource limits memory=256Mi, cpu=500m (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 6 - Expected resource limits memory=256Mi and cpu=500m")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
