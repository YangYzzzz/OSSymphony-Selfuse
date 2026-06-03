"""
Reward Script: VSCode YAML Schema Configuration
Task ID: vscode_ops_050
Domain: vscode
Scoring:
  Component 1 (0.25) — .vscode/settings.json exists and is valid JSON with yaml.schemas key
  Component 2 (0.35) — Docker Compose schema URL mapped to docker-compose*.yml pattern
  Component 3 (0.35) — Kubernetes schema URL mapped to k8s/*.yaml pattern
  Component 4 (0.05) — Both mappings coexist in a single yaml.schemas object
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_050'
WORKSPACE = os.path.join(WORKDIR, 'infra')
SETTINGS_PATH = os.path.join(WORKSPACE, '.vscode', 'settings.json')


def load_json_with_comments(path):
    """Load a JSONC file (JSON with comments) — strips // comments before parsing.
    Careful not to strip // inside strings (e.g. URLs)."""
    with open(path, 'r') as f:
        content = f.read()
    # First try direct parse (valid JSON)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    # Strip single-line comments outside of strings
    # Simple approach: remove lines that start with // (possibly with whitespace)
    lines = content.split('\n')
    cleaned = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith('//'):
            continue
        cleaned.append(line)
    return json.loads('\n'.join(cleaned))


def find_compose_mapping(schemas):
    """Find a Docker Compose schema mapping. Returns (url, pattern) or None."""
    for schema_url, file_pattern in schemas.items():
        url_lower = schema_url.lower()
        if 'compose' in url_lower or 'docker-compose' in url_lower:
            pattern_str = str(file_pattern) if not isinstance(file_pattern, list) else ' '.join(file_pattern)
            if 'docker-compose' in pattern_str.lower():
                return (schema_url, file_pattern)
    return None


def find_k8s_mapping(schemas):
    """Find a Kubernetes schema mapping. Returns (url, pattern) or None."""
    for schema_url, file_pattern in schemas.items():
        url_lower = schema_url.lower()
        if 'kubernetes' in url_lower:
            pattern_str = str(file_pattern) if not isinstance(file_pattern, list) else ' '.join(file_pattern)
            if 'k8s' in pattern_str.lower():
                return (schema_url, file_pattern)
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ------------------------------------------------------------------
    # Component 1: .vscode/settings.json exists and contains yaml.schemas
    # (0.25 points)
    # ------------------------------------------------------------------
    try:
        if not os.path.isfile(SETTINGS_PATH):
            print(f"FAIL: Component 1 — {SETTINGS_PATH} does not exist")
            print("REWARD: 0.0")
            return 0.0

        settings = load_json_with_comments(SETTINGS_PATH)

        if 'yaml.schemas' not in settings:
            print("FAIL: Component 1 — 'yaml.schemas' key missing from settings.json")
            print("REWARD: 0.0")
            return 0.0

        schemas = settings['yaml.schemas']
        if not isinstance(schemas, dict):
            print(f"FAIL: Component 1 — yaml.schemas is not a dict, got {type(schemas)}")
            print("REWARD: 0.0")
            return 0.0

        if isinstance(schemas, dict) and len(schemas) > 0:
            print(f"PASS: Component 1 — settings.json exists with yaml.schemas ({len(schemas)} entries) (0.25 pts)")
            total_score += 0.25
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 1 — settings.json is invalid JSON: {e}")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # ------------------------------------------------------------------
    # Component 2: Docker Compose schema mapped to docker-compose files
    # (0.35 points)
    # ------------------------------------------------------------------
    try:
        compose_match = find_compose_mapping(schemas)
        if compose_match is not None:
            print(f"PASS: Component 2 — Docker Compose schema found: {compose_match[0]} -> {compose_match[1]} (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — No Docker Compose schema mapping found in yaml.schemas: {schemas}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ------------------------------------------------------------------
    # Component 3: Kubernetes schema mapped to k8s/*.yaml files
    # (0.35 points)
    # ------------------------------------------------------------------
    try:
        k8s_match = find_k8s_mapping(schemas)
        if k8s_match is not None:
            print(f"PASS: Component 3 — Kubernetes schema found: {k8s_match[0]} -> {k8s_match[1]} (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 3 — No Kubernetes schema mapping found in yaml.schemas: {schemas}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ------------------------------------------------------------------
    # Component 4: Both mappings coexist in yaml.schemas
    # (0.05 points)
    # ------------------------------------------------------------------
    try:
        if total_score >= 0.94:
            print(f"PASS: Component 4 — Both Docker Compose and Kubernetes schemas configured together (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 4 — Not both schemas are properly configured")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
