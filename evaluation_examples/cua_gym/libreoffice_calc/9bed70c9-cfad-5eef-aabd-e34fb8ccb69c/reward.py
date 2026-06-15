"""
Reward Script: Configure YAML extension Kubernetes schema association
Task ID: vscode_ops_016
Domain: vscode (settings configuration)
Scoring:
  Component 1 (0.3): yaml.schemas key exists in settings.json
  Component 2 (0.3): kubernetes schema key exists within yaml.schemas
  Component 3 (0.4): kubernetes schema maps to exactly "k8s-*.yaml"
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")
TASK_ID = "vscode_ops_016"


def load_settings(path):
    """Load VSCode settings.json, handling JSONC (comments)."""
    try:
        with open(path, "r") as f:
            content = f.read()
        # Strip JSONC comments before parsing
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings from {path}: {e}")
        return None


def verify_task():
    """
    Verify that VSCode settings.json contains:
      "yaml.schemas": {"kubernetes": "k8s-*.yaml"}

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load settings file
    settings = load_settings(SETTINGS_PATH)
    if settings is None:
        print(f"CRITICAL: Cannot load settings.json at {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: yaml.schemas key exists in settings (0.3 points)
    try:
        if "yaml.schemas" in settings:
            yaml_schemas = settings["yaml.schemas"]
            if isinstance(yaml_schemas, dict):
                print(f"PASS: Component 1 -- yaml.schemas key exists and is a dict (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 -- yaml.schemas exists but is not a dict: {type(yaml_schemas)}")
        else:
            print(f"FAIL: Component 1 -- yaml.schemas key not found in settings. Keys: {list(settings.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: kubernetes schema key exists within yaml.schemas (0.3 points)
    try:
        yaml_schemas = settings.get("yaml.schemas", {})
        if isinstance(yaml_schemas, dict) and "kubernetes" in yaml_schemas:
            print(f"PASS: Component 2 -- 'kubernetes' key found in yaml.schemas (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- 'kubernetes' key not in yaml.schemas. Keys: {list(yaml_schemas.keys()) if isinstance(yaml_schemas, dict) else 'N/A'}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: kubernetes schema maps to exactly "k8s-*.yaml" (0.4 points)
    try:
        yaml_schemas = settings.get("yaml.schemas", {})
        if isinstance(yaml_schemas, dict):
            k8s_value = yaml_schemas.get("kubernetes")
            if k8s_value == "k8s-*.yaml":
                print(f"PASS: Component 3 -- kubernetes maps to 'k8s-*.yaml' (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 3 -- kubernetes maps to '{k8s_value}', expected 'k8s-*.yaml'")
        else:
            print(f"FAIL: Component 3 -- yaml.schemas is not a dict")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    # Round to avoid floating point noise
    final_score = round(final_score, 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
