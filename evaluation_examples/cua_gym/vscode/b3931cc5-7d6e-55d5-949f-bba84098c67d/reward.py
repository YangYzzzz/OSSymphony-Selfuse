"""
Reward Script: Create Kubernetes HorizontalPodAutoscaler YAML
Task ID: vscode_ops_074
Domain: vscode
Scoring:
  Component 1: hpa.yaml exists and is valid YAML (0.1 pts)
  Component 2: apiVersion and kind correct (0.2 pts)
  Component 3: scaleTargetRef targets Deployment/web-app (0.25 pts)
  Component 4: minReplicas=2, maxReplicas=10 (0.25 pts)
  Component 5: CPU averageUtilization=70 metric (0.2 pts)
"""

import os
import sys

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_074'
HPA_PATH = os.path.join(WORKDIR, 'k8s', 'hpa.yaml')


def verify_task(file_path):
    """
    Verify HPA YAML task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load YAML content
    try:
        import yaml
    except ImportError:
        # Fallback: try to parse YAML manually if pyyaml not available
        print("WARNING: pyyaml not available, attempting manual parse")
        try:
            _parse_yaml_simple(file_path)
        except Exception as e:
            print(f"CRITICAL: Cannot parse YAML: {e}")
            print("REWARD: 0.0")
            return 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
        docs = list(yaml.safe_load_all(content))
        # Use first document
        doc = docs[0] if docs else None
        if doc is None:
            print("CRITICAL: YAML file is empty or invalid")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot parse YAML file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File exists and is valid YAML (0.1 points)
    # Already confirmed above if we reach here
    try:
        if isinstance(doc, dict) and len(doc) > 0:
            print(f"PASS: Component 1 -- hpa.yaml exists and is valid YAML (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 -- YAML parsed but not a valid mapping")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: apiVersion is autoscaling/v2 or v2beta2, kind is HorizontalPodAutoscaler (0.2 pts)
    try:
        api_version = doc.get('apiVersion', '')
        kind = doc.get('kind', '')
        valid_api_versions = ['autoscaling/v2', 'autoscaling/v2beta2']
        api_ok = api_version in valid_api_versions
        kind_ok = kind == 'HorizontalPodAutoscaler'
        if api_ok and kind_ok:
            print(f"PASS: Component 2 -- apiVersion={api_version}, kind={kind} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 -- apiVersion={api_version} (valid: {valid_api_versions}), kind={kind}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: scaleTargetRef points to Deployment/web-app (0.25 pts)
    try:
        spec = doc.get('spec', {})
        scale_ref = spec.get('scaleTargetRef', {})
        ref_kind = scale_ref.get('kind', '')
        ref_name = scale_ref.get('name', '')
        ref_api = scale_ref.get('apiVersion', '')
        kind_match = ref_kind == 'Deployment'
        name_match = ref_name == 'web-app'
        # apiVersion in scaleTargetRef is optional but if present should be apps/v1
        if kind_match and name_match:
            print(f"PASS: Component 3 -- scaleTargetRef kind={ref_kind}, name={ref_name} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- scaleTargetRef kind={ref_kind} (expected Deployment), name={ref_name} (expected web-app)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: minReplicas=2, maxReplicas=10 (0.25 pts)
    try:
        spec = doc.get('spec', {})
        min_replicas = spec.get('minReplicas')
        max_replicas = spec.get('maxReplicas')
        min_ok = min_replicas == 2
        max_ok = max_replicas == 10
        if min_ok and max_ok:
            print(f"PASS: Component 4 -- minReplicas={min_replicas}, maxReplicas={max_replicas} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 -- minReplicas={min_replicas} (expected 2), maxReplicas={max_replicas} (expected 10)")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Metrics targeting CPU averageUtilization=70 (0.2 pts)
    try:
        spec = doc.get('spec', {})
        metrics = spec.get('metrics', [])
        # Search for a Resource metric with cpu/Utilization/70
        matching = [
            m for m in metrics
            if m.get('type') == 'Resource'
            and m.get('resource', {}).get('name') == 'cpu'
            and m.get('resource', {}).get('target', {}).get('type') == 'Utilization'
            and m.get('resource', {}).get('target', {}).get('averageUtilization') == 70
        ]
        if len(matching) > 0:
            print(f"PASS: Component 5 -- CPU averageUtilization=70 metric found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 -- CPU averageUtilization=70 metric not found in metrics: {metrics}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(HPA_PATH):
    print(f"File not found: {HPA_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(HPA_PATH)
