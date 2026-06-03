"""
Reward Script: Data engineering workspace extension configuration
Task ID: vscode_we_090
Domain: vscode
Scoring:
  Component 1 (0.30): ms-toolsai.jupyter and redhat.vscode-yaml extensions installed
  Component 2 (0.40): Workspace settings.json with correct configuration entries
  Component 3 (0.30): extensions.json with correct recommendations
"""

import json
import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_090'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'data-pipeline')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')
SETTINGS_PATH = os.path.join(VSCODE_DIR, 'settings.json')
EXTENSIONS_PATH = os.path.join(VSCODE_DIR, 'extensions.json')


def _is_subset(expected, actual):
    """Check that expected is a subset of actual (for nested dicts)."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and _is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        return expected == actual
    return expected == actual


def load_json_file(path):
    """Load a JSON file, handling JSONC comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Try direct parse first; fall back to stripping JSONC comments
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Strip single-line comments but not inside strings
        # Simple approach: strip lines that start with // (after whitespace)
        lines = content.split('\n')
        cleaned = []
        for line in lines:
            stripped = line.lstrip()
            if stripped.startswith('//'):
                continue
            cleaned.append(line)
        return json.loads('\n'.join(cleaned))


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Extensions ms-toolsai.jupyter and redhat.vscode-yaml installed (0.30 pts)
    # These extensions are NOT present in initial_env, only in golden_env.
    # Check by scanning the extensions directory on the filesystem (no subprocess needed).
    try:
        ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
        if os.path.isdir(ext_dir):
            ext_folders = os.listdir(ext_dir)
        else:
            ext_folders = []

        # Extension folders are named like "publisher.name-version"
        installed_ids = set()
        for folder in ext_folders:
            # Extract publisher.name by splitting off the version suffix
            # e.g. "ms-toolsai.jupyter-2023.11.1100101639-linux-x64" -> "ms-toolsai.jupyter"
            parts = folder.split('-')
            # The publisher.name part contains a dot; find where version starts
            name_parts = []
            for i, part in enumerate(parts):
                if '.' in part and not any(c.isdigit() for c in part.split('.')[0]):
                    name_parts.append(part)
                elif name_parts:
                    break
                else:
                    name_parts.append(part)
            ext_id = '-'.join(name_parts).lower()
            installed_ids.add(ext_id)

        jupyter_installed = any('ms-toolsai.jupyter' == eid for eid in installed_ids)
        yaml_installed = any('redhat.vscode-yaml' == eid for eid in installed_ids)

        # Fallback: also check by prefix matching on folder names
        if not jupyter_installed:
            jupyter_installed = any(f.lower().startswith('ms-toolsai.jupyter-') for f in ext_folders)
        if not yaml_installed:
            yaml_installed = any(f.lower().startswith('redhat.vscode-yaml-') for f in ext_folders)

        if jupyter_installed and yaml_installed:
            print(f"PASS: Component 1 -- Both ms-toolsai.jupyter and redhat.vscode-yaml installed (0.30 pts)")
            total_score += 0.30
        elif jupyter_installed or yaml_installed:
            found = 'ms-toolsai.jupyter' if jupyter_installed else 'redhat.vscode-yaml'
            missing = 'redhat.vscode-yaml' if jupyter_installed else 'ms-toolsai.jupyter'
            print(f"PARTIAL: Component 1 -- {found} installed, {missing} missing (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Neither ms-toolsai.jupyter nor redhat.vscode-yaml installed. Found folders: {ext_folders}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Workspace settings.json with correct configuration (0.40 pts)
    # .vscode/settings.json does NOT exist in initial_env.
    try:
        if not os.path.exists(SETTINGS_PATH):
            print(f"FAIL: Component 2 -- {SETTINGS_PATH} does not exist")
        else:
            settings = load_json_file(SETTINGS_PATH)
            comp2_score = 0.0

            # Check each required setting (0.10 pts each)
            expected_settings = {
                "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
                "python.analysis.typeCheckingMode": "basic",
                "jupyter.executionTimeout": 300,
                "yaml.schemas": {
                    "https://json.schemastore.org/github-workflow.json": ".github/workflows/*.yml"
                }
            }

            for key, expected_val in expected_settings.items():
                if key in settings and _is_subset(expected_val, settings[key]):
                    print(f"  PASS: settings['{key}'] = {json.dumps(settings[key])}")
                    comp2_score += 0.10
                else:
                    actual = settings.get(key, '<missing>')
                    print(f"  FAIL: settings['{key}'] expected {json.dumps(expected_val)}, found {json.dumps(actual) if actual != '<missing>' else actual}")

            if comp2_score > 0:
                print(f"PASS: Component 2 -- settings.json verified ({comp2_score:.2f} pts)")
                total_score += comp2_score
            else:
                print(f"FAIL: Component 2 -- No matching settings found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: extensions.json with correct recommendations (0.30 pts)
    # .vscode/extensions.json does NOT exist in initial_env.
    try:
        if not os.path.exists(EXTENSIONS_PATH):
            print(f"FAIL: Component 3 -- {EXTENSIONS_PATH} does not exist")
        else:
            ext_config = load_json_file(EXTENSIONS_PATH)
            recommendations = ext_config.get('recommendations', [])
            recommendations_lower = [r.lower() for r in recommendations]

            required_recs = [
                'ms-python.python',
                'ms-toolsai.jupyter',
                'redhat.vscode-yaml',
                'mtxr.sqltools'
            ]

            found_count = sum(1 for r in required_recs if r in recommendations_lower)

            if found_count == len(required_recs):
                print(f"PASS: Component 3 -- extensions.json recommends all 4 extensions (0.30 pts)")
                total_score += 0.30
            elif found_count > 0:
                partial = round(0.30 * found_count / len(required_recs), 2)
                print(f"PARTIAL: Component 3 -- {found_count}/{len(required_recs)} recommendations found (0.{int(partial*100):02d} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 -- No required recommendations found. Got: {recommendations}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
