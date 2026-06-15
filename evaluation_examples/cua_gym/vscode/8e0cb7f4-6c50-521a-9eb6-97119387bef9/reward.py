"""
Reward Script: Multi-root workspace with per-folder settings and extension recommendations
Task ID: vscode_we_095
Domain: vscode
Scoring:
  - Component 1: Workspace-level shared settings (0.15)
  - Component 2: Frontend .vscode/settings.json (0.15)
  - Component 3: Backend .vscode/settings.json (0.15)
  - Component 4: Infra .vscode/settings.json (0.15)
  - Component 5: Frontend .vscode/extensions.json (0.15)
  - Component 6: Backend .vscode/extensions.json (0.15)
  - Component 7: Infra .vscode/extensions.json (0.10)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECTS = os.path.join(WORKDIR, 'projects')
WORKSPACE_FILE = os.path.join(PROJECTS, 'saas-platform.code-workspace')
TASK_ID = 'vscode_we_095'


def _load_json(path):
    """Load a JSON file, handling JSONC (comments)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments for JSONC support
    cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(cleaned)


def _is_subset(expected, actual):
    """Check if expected is a subset of actual (recursive for dicts)."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and _is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        if not isinstance(actual, list):
            return False
        # For lists, check that all expected items are present (order-independent for recommendations)
        return set(str(x) for x in expected).issubset(set(str(x) for x in actual))
    return expected == actual


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: workspace file must exist
    if not os.path.exists(WORKSPACE_FILE):
        print(f"CRITICAL: Workspace file not found: {WORKSPACE_FILE}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Workspace-level shared settings (0.15 points)
    # Task requires: editor.formatOnSave=true, files.trimTrailingWhitespace=true
    # Initial state: settings: {} (empty)
    try:
        ws_data = _load_json(WORKSPACE_FILE)
        ws_settings = ws_data.get('settings', {})
        expected_ws = {
            "editor.formatOnSave": True,
            "files.trimTrailingWhitespace": True
        }
        if _is_subset(expected_ws, ws_settings):
            print(f"PASS: Component 1 — Workspace shared settings correct (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Workspace settings expected {expected_ws}, found {ws_settings}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Frontend .vscode/settings.json (0.15 points)
    # Must contain: defaultFormatter=prettier, tabSize=2, eslint.validate=[js, ts, tsxreact]
    try:
        fe_settings_path = os.path.join(PROJECTS, 'frontend', '.vscode', 'settings.json')
        if not os.path.exists(fe_settings_path):
            print(f"FAIL: Component 2 — Frontend settings.json not found")
        else:
            fe_settings = _load_json(fe_settings_path)
            expected_fe = {
                "editor.defaultFormatter": "esbenp.prettier-vscode",
                "editor.tabSize": 2,
            }
            # Check base settings
            base_ok = _is_subset(expected_fe, fe_settings)
            # Check eslint.validate contains the required languages
            eslint_validate = fe_settings.get("eslint.validate", [])
            eslint_ok = all(lang in eslint_validate for lang in ["javascript", "typescript", "typescriptreact"])
            if base_ok and eslint_ok:
                print(f"PASS: Component 2 — Frontend settings correct (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — Frontend settings: base_ok={base_ok}, eslint_ok={eslint_ok}, found {fe_settings}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Backend .vscode/settings.json (0.15 points)
    # Must contain: defaultFormatter=black, tabSize=4, pytestEnabled=true, typeCheckingMode=basic
    try:
        be_settings_path = os.path.join(PROJECTS, 'backend', '.vscode', 'settings.json')
        if not os.path.exists(be_settings_path):
            print(f"FAIL: Component 3 — Backend settings.json not found")
        else:
            be_settings = _load_json(be_settings_path)
            expected_be = {
                "editor.defaultFormatter": "ms-python.black-formatter",
                "editor.tabSize": 4,
                "python.testing.pytestEnabled": True,
                "python.analysis.typeCheckingMode": "basic"
            }
            if _is_subset(expected_be, be_settings):
                print(f"PASS: Component 3 — Backend settings correct (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — Backend settings expected {expected_be}, found {be_settings}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Infra .vscode/settings.json (0.15 points)
    # Must contain: tabSize=2, [terraform].editor.defaultFormatter=hashicorp, yaml.schemas
    try:
        infra_settings_path = os.path.join(PROJECTS, 'infra', '.vscode', 'settings.json')
        if not os.path.exists(infra_settings_path):
            print(f"FAIL: Component 4 — Infra settings.json not found")
        else:
            infra_settings = _load_json(infra_settings_path)
            expected_infra = {
                "editor.tabSize": 2,
                "[terraform]": {
                    "editor.defaultFormatter": "hashicorp.terraform"
                },
            }
            base_ok = _is_subset(expected_infra, infra_settings)
            # Check yaml.schemas has kubernetes mapping
            yaml_schemas = infra_settings.get("yaml.schemas", {})
            yaml_ok = "kubernetes" in yaml_schemas
            if base_ok and yaml_ok:
                print(f"PASS: Component 4 — Infra settings correct (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — Infra settings: base_ok={base_ok}, yaml_ok={yaml_ok}, found {infra_settings}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Frontend .vscode/extensions.json (0.15 points)
    # Must recommend: prettier, eslint, tailwindcss
    try:
        fe_ext_path = os.path.join(PROJECTS, 'frontend', '.vscode', 'extensions.json')
        if not os.path.exists(fe_ext_path):
            print(f"FAIL: Component 5 — Frontend extensions.json not found")
        else:
            fe_ext = _load_json(fe_ext_path)
            recs = fe_ext.get("recommendations", [])
            expected_recs = ["esbenp.prettier-vscode", "dbaeumer.vscode-eslint", "bradlc.vscode-tailwindcss"]
            if all(ext in recs for ext in expected_recs):
                print(f"PASS: Component 5 — Frontend extensions correct (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — Frontend extensions expected {expected_recs}, found {recs}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Backend .vscode/extensions.json (0.15 points)
    # Must recommend: python, black-formatter, pylance
    try:
        be_ext_path = os.path.join(PROJECTS, 'backend', '.vscode', 'extensions.json')
        if not os.path.exists(be_ext_path):
            print(f"FAIL: Component 6 — Backend extensions.json not found")
        else:
            be_ext = _load_json(be_ext_path)
            recs = be_ext.get("recommendations", [])
            expected_recs = ["ms-python.python", "ms-python.black-formatter", "ms-python.vscode-pylance"]
            if all(ext in recs for ext in expected_recs):
                print(f"PASS: Component 6 — Backend extensions correct (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 6 — Backend extensions expected {expected_recs}, found {recs}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: Infra .vscode/extensions.json (0.10 points)
    # Must recommend: terraform, vscode-yaml
    try:
        infra_ext_path = os.path.join(PROJECTS, 'infra', '.vscode', 'extensions.json')
        if not os.path.exists(infra_ext_path):
            print(f"FAIL: Component 7 — Infra extensions.json not found")
        else:
            infra_ext = _load_json(infra_ext_path)
            recs = infra_ext.get("recommendations", [])
            expected_recs = ["hashicorp.terraform", "redhat.vscode-yaml"]
            if all(ext in recs for ext in expected_recs):
                print(f"PASS: Component 7 — Infra extensions correct (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 7 — Infra extensions expected {expected_recs}, found {recs}")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
