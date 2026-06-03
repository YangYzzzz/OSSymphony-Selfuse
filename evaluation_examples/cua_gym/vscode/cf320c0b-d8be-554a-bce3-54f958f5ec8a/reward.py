"""
Reward Script: Create complex .vscode/settings.json with file exclusions, search exclusions,
language-specific formatting, default encoding, and line endings.
Task ID: vscode_file_076
Domain: vs_code

Scoring:
  Component 1: files.exclude has node_modules, __pycache__, .git all set to true  — 0.30 pts
  Component 2: search.exclude has node_modules, __pycache__ all set to true         — 0.20 pts
  Component 3: [typescript] language settings: tabSize=2, formatOnSave=true         — 0.20 pts
  Component 4: [python] language settings: tabSize=4, formatOnSave=true             — 0.20 pts
  Component 5: files.encoding="utf8" AND files.eol="\n"                             — 0.10 pts
  Total: 1.0
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_076'
SETTINGS_PATH = '/home/user/fullstack-app/.vscode/settings.json'


def load_settings(path):
    """Load a JSON settings file, stripping JSONC-style // comments if present."""
    try:
        with open(path, 'r') as f:
            raw = f.read()
        # Strip single-line comments (JSONC style) before parsing
        cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
        return json.loads(cleaned)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: settings.json is not valid JSON: {e}")
        return None


def _is_subset(expected, actual) -> bool:
    """Recursively check that all expected key-value pairs exist in actual."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and _is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        return expected == actual
    return expected == actual


def verify_task(settings_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: settings.json must exist and be valid JSON
    settings = load_settings(settings_path)
    if settings is None:
        print(f"CRITICAL: Cannot load {settings_path} — file missing or invalid JSON")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: files.exclude contains node_modules, __pycache__, .git (all true) (0.30 pts)
    try:
        expected_file_exclude = {
            "files.exclude": {
                "**/node_modules": True,
                "**/__pycache__": True,
                "**/.git": True
            }
        }
        if _is_subset(expected_file_exclude, settings):
            print("PASS: Component 1 — files.exclude contains **/node_modules, **/__pycache__, **/.git all set to true (0.30 pts)")
            total_score += 0.30
        else:
            actual_fe = settings.get("files.exclude", {})
            print(f"FAIL: Component 1 — files.exclude expected {{**/node_modules: true, **/__pycache__: true, **/.git: true}}, found: {actual_fe}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: search.exclude contains node_modules, __pycache__ (all true) (0.20 pts)
    try:
        expected_search_exclude = {
            "search.exclude": {
                "**/node_modules": True,
                "**/__pycache__": True
            }
        }
        if _is_subset(expected_search_exclude, settings):
            print("PASS: Component 2 — search.exclude contains **/node_modules, **/__pycache__ all set to true (0.20 pts)")
            total_score += 0.20
        else:
            actual_se = settings.get("search.exclude", {})
            print(f"FAIL: Component 2 — search.exclude expected {{**/node_modules: true, **/__pycache__: true}}, found: {actual_se}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: [typescript] language-specific settings: tabSize=2, formatOnSave=true (0.20 pts)
    try:
        expected_ts = {
            "[typescript]": {
                "editor.tabSize": 2,
                "editor.formatOnSave": True
            }
        }
        if _is_subset(expected_ts, settings):
            print("PASS: Component 3 — [typescript] settings: editor.tabSize=2, editor.formatOnSave=true (0.20 pts)")
            total_score += 0.20
        else:
            actual_ts = settings.get("[typescript]", {})
            print(f"FAIL: Component 3 — [typescript] settings expected {{editor.tabSize: 2, editor.formatOnSave: true}}, found: {actual_ts}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: [python] language-specific settings: tabSize=4, formatOnSave=true (0.20 pts)
    try:
        expected_py = {
            "[python]": {
                "editor.tabSize": 4,
                "editor.formatOnSave": True
            }
        }
        if _is_subset(expected_py, settings):
            print("PASS: Component 4 — [python] settings: editor.tabSize=4, editor.formatOnSave=true (0.20 pts)")
            total_score += 0.20
        else:
            actual_py = settings.get("[python]", {})
            print(f"FAIL: Component 4 — [python] settings expected {{editor.tabSize: 4, editor.formatOnSave: true}}, found: {actual_py}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: files.encoding="utf8" AND files.eol="\n" (0.10 pts)
    try:
        actual_encoding = settings.get("files.encoding")
        actual_eol = settings.get("files.eol")
        encoding_ok = actual_encoding == "utf8"
        eol_ok = actual_eol == "\n"
        if encoding_ok and eol_ok:
            print(f"PASS: Component 5 — files.encoding='utf8' and files.eol='\\n' (0.10 pts)")
            total_score += 0.10
        else:
            reasons = []
            if not encoding_ok:
                reasons.append(f"files.encoding expected 'utf8', found '{actual_encoding}'")
            if not eol_ok:
                reasons.append(f"files.eol expected '\\n', found '{actual_eol}'")
            print(f"FAIL: Component 5 — {'; '.join(reasons)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: verify the workspace settings.json
if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(SETTINGS_PATH)
