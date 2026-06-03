"""
Reward Script: Create a comprehensive .code-workspace file at /home/user/projects/team.code-workspace
Task ID: vscode_file_080
Domain: vs_code

Scoring:
- Component 1: Folders array contains 3 folders with correct paths and custom names (0.4 pts)
- Component 2: Settings section contains all required settings (0.3 pts)
- Component 3: Extensions recommendations contain all 3 required extensions (0.3 pts)
Total: 1.0
"""

import os
import json

WORKDIR = '/home/user/projects'
TASK_ID = 'vscode_file_080'
WORKSPACE_PATH = '/home/user/projects/team.code-workspace'


def _is_subset(expected, actual):
    """Recursively check that expected is a subset of actual."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and _is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        # For lists, check exact equality (order matters for folders/extensions)
        return expected == actual
    return expected == actual


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be valid JSON
    if not os.path.exists(file_path):
        print(f"CRITICAL: Workspace file not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            workspace = json.load(f)
        print(f"PASS: File exists and is valid JSON at {file_path}")
    except json.JSONDecodeError as e:
        print(f"CRITICAL: File is not valid JSON: {e}")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: folders array contains 3 entries with correct paths and custom names (0.4 pts)
    try:
        folders = workspace.get("folders", [])
        expected_folders = [
            {"path": "web-client", "name": "Frontend"},
            {"path": "api-server", "name": "Backend"},
            {"path": "shared-utils", "name": "Shared Libraries"},
        ]

        if not isinstance(folders, list) or len(folders) == 0:
            print(f"FAIL: Component 1 — folders array is empty or missing, found: {folders}")
        elif len(folders) != 3:
            print(f"FAIL: Component 1 — expected 3 folders, found {len(folders)}")
        else:
            # Check each folder has correct path and name
            actual_folder_entries = [(f.get("path"), f.get("name")) for f in folders]
            expected_folder_entries = [(f["path"], f["name"]) for f in expected_folders]

            # Check all expected folder entries are present (order-independent)
            all_found = all(entry in actual_folder_entries for entry in expected_folder_entries)
            if all_found:
                print(f"PASS: Component 1 — all 3 folders with correct paths and names found: {actual_folder_entries} (0.4 pts)")
                total_score += 0.4
            else:
                # Partial check: count how many are correct
                found_count = sum(1 for entry in expected_folder_entries if entry in actual_folder_entries)
                print(f"FAIL: Component 1 — found {found_count}/3 correct folder entries. Actual: {actual_folder_entries}, Expected: {expected_folder_entries}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: settings section contains all required settings (0.3 pts)
    try:
        settings = workspace.get("settings", {})
        if not isinstance(settings, dict):
            print(f"FAIL: Component 2 — settings is not a dict, found: {type(settings)}")
        else:
            expected_settings = {
                "editor.formatOnSave": True,
                "editor.tabSize": 2,
                "files.exclude": {
                    "**/node_modules": True,
                    "**/__pycache__": True
                },
                "files.eol": "\n"
            }

            settings_match = _is_subset(expected_settings, settings)
            if settings_match:
                print(f"PASS: Component 2 — all required settings present (0.3 pts)")
                total_score += 0.3
            else:
                # Check individual settings for diagnostic info
                missing = []
                for k, v in expected_settings.items():
                    if k not in settings:
                        missing.append(f"missing key '{k}'")
                    elif not _is_subset(v, settings[k]):
                        missing.append(f"key '{k}' wrong value: expected {v}, found {settings[k]}")
                print(f"FAIL: Component 2 — settings mismatch: {'; '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: extensions.recommendations contains all 3 required extensions (0.3 pts)
    try:
        extensions = workspace.get("extensions", {})
        recommendations = extensions.get("recommendations", []) if isinstance(extensions, dict) else []

        required_extensions = [
            "ms-python.python",
            "dbaeumer.vscode-eslint",
            "esbenp.prettier-vscode"
        ]

        if not isinstance(recommendations, list):
            print(f"FAIL: Component 3 — recommendations is not a list, found: {type(recommendations)}")
        else:
            # Check all required extensions are present (order-independent, case-insensitive match)
            recommendations_lower = [r.lower() for r in recommendations]
            all_ext_found = all(ext.lower() in recommendations_lower for ext in required_extensions)
            if all_ext_found:
                print(f"PASS: Component 3 — all 3 required extension recommendations found: {recommendations} (0.3 pts)")
                total_score += 0.3
            else:
                found_exts = [ext for ext in required_extensions if ext.lower() in recommendations_lower]
                missing_exts = [ext for ext in required_extensions if ext.lower() not in recommendations_lower]
                print(f"FAIL: Component 3 — found {len(found_exts)}/3 extensions. Missing: {missing_exts}, Actual: {recommendations}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path on the VM
if not os.path.exists(WORKSPACE_PATH):
    print(f"File not found: {WORKSPACE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(WORKSPACE_PATH)
