"""
Reward Script: Configure pair programming workflow in ~/project
Task ID: vscode_wf_084
Domain: vscode
Scoring:
  Component 1: Live Share extension installed (0.2)
  Component 2: Live Share settings in settings.json (0.2)
  Component 3: Formatting settings in settings.json (0.2)
  Component 4: Collaboration editor settings (bracket colorization, indent guides, breadcrumbs) (0.2)
  Component 5: tasks.json with pair-setup and pair-test tasks (0.2)
"""

import os
import json
import re
import glob

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_084'
PROJECT_DIR = os.path.join(WORKDIR, 'project')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')
SETTINGS_PATH = os.path.join(VSCODE_DIR, 'settings.json')
TASKS_PATH = os.path.join(VSCODE_DIR, 'tasks.json')


def load_json_file(path):
    """Load a JSON file, handling JSONC comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def is_subset(expected, actual):
    """Check if expected is a subset of actual (recursive for dicts)."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        return expected == actual
    return expected == actual


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Live Share extension installed (0.2 points)
    # Check via filesystem: ~/.vscode/extensions/ms-vsliveshare.vsliveshare-*
    try:
        ext_dir = os.path.expanduser("~/.vscode/extensions")
        matches = glob.glob(os.path.join(ext_dir, "ms-vsliveshare.vsliveshare-*"))
        if len(matches) > 0:
            print(f"PASS: Component 1 - Live Share extension installed: {matches[0]} (0.2 pts)")
            total_score += 0.2
        else:
            all_exts = os.listdir(ext_dir) if os.path.isdir(ext_dir) else []
            print(f"FAIL: Component 1 - Live Share extension not found. Extensions: {all_exts}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Live Share settings in settings.json (0.2 points)
    # Checks liveshare.allowGuestTaskExecution, liveshare.allowGuestDebugControl,
    # and liveshare.autoShareTerminals
    try:
        settings = load_json_file(SETTINGS_PATH)
        liveshare_checks = {
            "liveshare.allowGuestTaskExecution": True,
            "liveshare.allowGuestDebugControl": True,
        }
        # Also check for shared terminals setting
        terminal_share = settings.get("liveshare.autoShareTerminals", None)

        passed_count = 0
        for key, expected_val in liveshare_checks.items():
            actual_val = settings.get(key, None)
            if actual_val == expected_val:
                passed_count += 1
            else:
                print(f"  DETAIL: {key} expected {expected_val}, found {actual_val}")

        if terminal_share is True:
            passed_count += 1
        else:
            print(f"  DETAIL: liveshare.autoShareTerminals expected True, found {terminal_share}")

        if passed_count == 3:
            print("PASS: Component 2 - All Live Share settings present (0.2 pts)")
            total_score += 0.2
        elif passed_count >= 2:
            partial = round(0.2 * passed_count / 3, 2)
            print(f"PARTIAL: Component 2 - {passed_count}/3 Live Share settings ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - Only {passed_count}/3 Live Share settings found")
    except FileNotFoundError:
        print("FAIL: Component 2 - settings.json not found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Consistent formatting settings (0.2 points)
    # Checks tabSize, insertSpaces, formatOnSave
    try:
        settings = load_json_file(SETTINGS_PATH)
        fmt_checks = {
            "editor.tabSize": 4,
            "editor.insertSpaces": True,
            "editor.formatOnSave": True,
        }
        passed_count = 0
        for key, expected_val in fmt_checks.items():
            actual_val = settings.get(key, None)
            if actual_val == expected_val:
                passed_count += 1
            else:
                print(f"  DETAIL: {key} expected {expected_val}, found {actual_val}")

        if passed_count == 3:
            print("PASS: Component 3 - All formatting settings correct (0.2 pts)")
            total_score += 0.2
        elif passed_count >= 2:
            partial = round(0.2 * passed_count / 3, 2)
            print(f"PARTIAL: Component 3 - {passed_count}/3 formatting settings ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 - Only {passed_count}/3 formatting settings found")
    except FileNotFoundError:
        print("FAIL: Component 3 - settings.json not found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Collaboration editor settings (0.2 points)
    # Checks bracket colorization, indent guides, breadcrumbs
    try:
        settings = load_json_file(SETTINGS_PATH)
        collab_passed = 0
        total_collab = 3

        # Bracket colorization enabled
        if settings.get("editor.bracketPairColorization.enabled", None) is True:
            collab_passed += 1
        else:
            print(f"  DETAIL: editor.bracketPairColorization.enabled expected True, found {settings.get('editor.bracketPairColorization.enabled', None)}")

        # Indent guides
        if settings.get("editor.guides.indentation", None) is True:
            collab_passed += 1
        else:
            print(f"  DETAIL: editor.guides.indentation expected True, found {settings.get('editor.guides.indentation', None)}")

        # Breadcrumbs
        if settings.get("breadcrumbs.enabled", None) is True:
            collab_passed += 1
        else:
            print(f"  DETAIL: breadcrumbs.enabled expected True, found {settings.get('breadcrumbs.enabled', None)}")

        if collab_passed == total_collab:
            print("PASS: Component 4 - All collaboration settings correct (0.2 pts)")
            total_score += 0.2
        elif collab_passed >= 1:
            partial = round(0.2 * collab_passed / total_collab, 2)
            print(f"PARTIAL: Component 4 - {collab_passed}/{total_collab} collaboration settings ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 - No collaboration settings found")
    except FileNotFoundError:
        print("FAIL: Component 4 - settings.json not found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: tasks.json with pair-setup and pair-test tasks (0.2 points)
    # Checks that tasks.json exists and contains both required task labels
    try:
        tasks_data = load_json_file(TASKS_PATH)
        tasks_list = tasks_data.get("tasks", [])
        task_labels = [t.get("label", "") for t in tasks_list]

        has_pair_setup = "pair-setup" in task_labels
        has_pair_test = "pair-test" in task_labels

        if has_pair_setup and has_pair_test:
            print("PASS: Component 5 - Both pair-setup and pair-test tasks found (0.2 pts)")
            total_score += 0.2
        elif has_pair_setup or has_pair_test:
            found = "pair-setup" if has_pair_setup else "pair-test"
            print(f"PARTIAL: Component 5 - Only '{found}' task found (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 5 - Neither pair-setup nor pair-test found. Labels: {task_labels}")
    except FileNotFoundError:
        print("FAIL: Component 5 - tasks.json not found")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
