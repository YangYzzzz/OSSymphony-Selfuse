"""
Reward Script: Add 'namespace: production' to Kubernetes YAML files missing it
Task ID: vscode_ops_049
Domain: vscode
Scoring: 4 components (0.25 each) - one per file that needs namespace added.
         Files that already had namespace are checked as preconditions only.
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_049'
K8S_DIR = os.path.join(WORKDIR, 'k8s')

# These 4 files are missing 'namespace: production' in initial state
# and should have it added in golden state
FILES_NEEDING_NAMESPACE = [
    'cronjob-cleanup.yaml',
    'frontend-service.yaml',
    'postgres-statefulset.yaml',
    'worker-deployment.yaml',
]

# These 4 files already have 'namespace: production' in initial state
FILES_ALREADY_HAVE_NAMESPACE = [
    'api-deployment.yaml',
    'ingress.yaml',
    'monitoring-configmap.yaml',
    'redis-service.yaml',
]

POINTS_PER_FILE = 0.25


def has_namespace_production_under_metadata(content):
    """
    Check if the YAML content has 'namespace: production' under the top-level metadata block.
    We parse this with regex since we only need standard libs.
    Returns True if 'namespace: production' appears in the metadata section.
    """
    lines = content.split('\n')
    in_metadata = False
    for line in lines:
        stripped = line.strip()
        # Detect top-level 'metadata:' (no leading spaces or exactly at top-level indent)
        if re.match(r'^metadata:\s*$', line):
            in_metadata = True
            continue
        if in_metadata:
            # If we hit a line at the same or lesser indent level (top-level key), stop
            if stripped and not line.startswith(' ') and not line.startswith('\t'):
                in_metadata = False
                continue
            # Check for namespace: production within metadata block
            if re.match(r'^\s+namespace:\s*production\s*$', line):
                return True
    return False


def yaml_is_valid_structure(content):
    """
    Basic check that the YAML file still has valid structure:
    - Has 'apiVersion' or 'kind' at top level
    - Has 'metadata:' section
    """
    has_api = bool(re.search(r'^apiVersion:', content, re.MULTILINE))
    has_kind = bool(re.search(r'^kind:', content, re.MULTILINE))
    has_metadata = bool(re.search(r'^metadata:', content, re.MULTILINE))
    return (has_api or has_kind) and has_metadata


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: k8s directory exists
    if not os.path.isdir(K8S_DIR):
        print(f"CRITICAL: Directory {K8S_DIR} not found")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: files that already had namespace should still have it
    for fname in FILES_ALREADY_HAVE_NAMESPACE:
        fpath = os.path.join(K8S_DIR, fname)
        try:
            with open(fpath, 'r') as f:
                content = f.read()
            if not has_namespace_production_under_metadata(content):
                print(f"PRECONDITION_FAIL: {fname} lost its namespace: production")
                print("REWARD: 0.0")
                return 0.0
        except Exception as e:
            print(f"PRECONDITION_WARN: Could not read {fname}: {e}")

    # Component 1-4: Each file that was missing namespace now has it (0.25 each)
    for i, fname in enumerate(FILES_NEEDING_NAMESPACE, 1):
        fpath = os.path.join(K8S_DIR, fname)
        try:
            with open(fpath, 'r') as f:
                content = f.read()

            if not yaml_is_valid_structure(content):
                print(f"FAIL: Component {i} -- {fname} has corrupted YAML structure")
                continue

            if has_namespace_production_under_metadata(content):
                print(f"PASS: Component {i} -- {fname} now has namespace: production ({POINTS_PER_FILE} pts)")
                total_score += POINTS_PER_FILE
            else:
                print(f"FAIL: Component {i} -- {fname} still missing namespace: production")
        except Exception as e:
            print(f"ERROR: Component {i} -- Could not check {fname}: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
