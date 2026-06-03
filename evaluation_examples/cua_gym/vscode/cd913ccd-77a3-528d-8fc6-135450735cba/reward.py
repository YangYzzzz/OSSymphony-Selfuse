"""
Reward Script: React Native mobile dev workflow in VSCode
Task ID: vscode_wf_090
Domain: vscode
Scoring:
  Component 1: Extension msjsdiag.vscode-react-native installed (0.15)
  Component 2: launch.json Android debug config (0.15)
  Component 3: launch.json iOS debug config (0.15)
  Component 4: launch.json Expo debug config with expoHostType (0.15)
  Component 5: tasks.json has start-metro, android, ios, lint, test (0.20)
  Component 6: workspace settings.json React Native IntelliSense (0.10)
  Component 7: .eslintrc.json extends @react-native-community (0.10)
"""

import os
import json
import re
import subprocess

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
VSCODE_DIR = os.path.join(PROJECT, '.vscode')
TASK_ID = 'vscode_wf_090'


def load_json_file(path):
    """Load a JSON file, tolerating JSONC and control chars."""
    with open(path, 'r') as f:
        content = f.read()
    # Try plain JSON first (most files are valid JSON)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    # Try with strict=False for control characters
    try:
        return json.loads(content, strict=False)
    except json.JSONDecodeError:
        pass
    # Last resort: strip single-line comments that are NOT inside strings
    # by removing lines that start with // after optional whitespace
    lines = content.split('\n')
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('//'):
            continue
        # Remove trailing comments only if not inside a string context
        cleaned.append(line)
    content = '\n'.join(cleaned)
    return json.loads(content, strict=False)


def verify_task():
    """Verify task completion with progressive scoring. Returns float 0.0-1.0."""
    total_score = 0.0

    # Component 1: Extension msjsdiag.vscode-react-native installed (0.15 points)
    try:
        result = subprocess.run(
            ["code", "--list-extensions"],
            capture_output=True, text=True, timeout=15
        )
        extensions = result.stdout.strip().lower().split('\n')
        if 'msjsdiag.vscode-react-native' in extensions:
            print("PASS: Component 1 -- Extension msjsdiag.vscode-react-native installed (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Extension not found. Installed: {extensions}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: launch.json Android debug config (0.15 points)
    try:
        launch_path = os.path.join(VSCODE_DIR, 'launch.json')
        launch = load_json_file(launch_path)
        configs = launch.get('configurations', [])
        android_found = False
        for cfg in configs:
            if (cfg.get('type') == 'reactnative' and
                cfg.get('platform') == 'android' and
                cfg.get('request') == 'launch'):
                android_found = True
                break
        if android_found:
            print("PASS: Component 2 -- launch.json has Android debug config (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 -- No Android reactnative launch config found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: launch.json iOS debug config (0.15 points)
    try:
        launch_path = os.path.join(VSCODE_DIR, 'launch.json')
        launch = load_json_file(launch_path)
        configs = launch.get('configurations', [])
        ios_found = False
        for cfg in configs:
            if (cfg.get('type') == 'reactnative' and
                cfg.get('platform') == 'ios' and
                cfg.get('request') == 'launch'):
                ios_found = True
                break
        if ios_found:
            print("PASS: Component 3 -- launch.json has iOS debug config (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 -- No iOS reactnative launch config found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: launch.json Expo debug config with expoHostType (0.15 points)
    try:
        launch_path = os.path.join(VSCODE_DIR, 'launch.json')
        launch = load_json_file(launch_path)
        configs = launch.get('configurations', [])
        expo_found = False
        for cfg in configs:
            if (cfg.get('type') == 'reactnative' and
                cfg.get('platform') == 'exponent' and
                cfg.get('request') == 'launch' and
                'expoHostType' in cfg):
                expo_found = True
                break
        if expo_found:
            print("PASS: Component 4 -- launch.json has Expo config with expoHostType (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 -- No Expo reactnative config with expoHostType found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: tasks.json has all 5 required tasks (0.20 points)
    # 0.04 per task label found
    try:
        tasks_path = os.path.join(VSCODE_DIR, 'tasks.json')
        tasks_data = load_json_file(tasks_path)
        task_list = tasks_data.get('tasks', [])
        labels = [t.get('label', '').lower() for t in task_list]
        required_labels = ['start-metro', 'android', 'ios', 'lint', 'test']
        found_count = 0
        for req in required_labels:
            if req in labels:
                found_count += 1
                print(f"  PASS: tasks.json has '{req}' task")
            else:
                print(f"  FAIL: tasks.json missing '{req}' task")
        if found_count == 5:
            print(f"PASS: Component 5 -- All 5 tasks present (0.20 pts)")
            total_score += 0.20
        elif found_count > 0:
            partial = round(found_count * 0.04, 2)
            print(f"PARTIAL: Component 5 -- {found_count}/5 tasks present ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 -- No required tasks found")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: workspace settings.json has React Native IntelliSense settings (0.10 points)
    try:
        settings_path = os.path.join(VSCODE_DIR, 'settings.json')
        settings = load_json_file(settings_path)
        # Check for React Native specific settings
        rn_settings_found = False
        # Check for react-native-tools settings or emmet/file associations for RN
        has_rn_tools = any(k.startswith('react-native-tools') for k in settings)
        has_js_auto_imports = settings.get('javascript.suggest.autoImports') is True
        has_emmet_jsx = isinstance(settings.get('emmet.includeLanguages'), dict)
        has_eslint_validate = isinstance(settings.get('eslint.validate'), list)

        rn_checks = sum([has_rn_tools, has_js_auto_imports, has_emmet_jsx, has_eslint_validate])
        if rn_checks >= 2:
            rn_settings_found = True

        if rn_settings_found:
            print(f"PASS: Component 6 -- settings.json has React Native IntelliSense settings ({rn_checks}/4 indicators) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 -- Insufficient RN settings ({rn_checks}/4 indicators)")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    # Component 7: .eslintrc.json extends @react-native-community (0.10 points)
    try:
        eslintrc_path = os.path.join(PROJECT, '.eslintrc.json')
        eslintrc = load_json_file(eslintrc_path)
        extends_val = eslintrc.get('extends', '')
        if isinstance(extends_val, str):
            extends_list = [extends_val]
        elif isinstance(extends_val, list):
            extends_list = extends_val
        else:
            extends_list = []

        extends_rn = any('@react-native-community' in ext for ext in extends_list)
        if extends_rn:
            print("PASS: Component 7 -- .eslintrc.json extends @react-native-community (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 7 -- .eslintrc.json extends: {extends_list}")
    except Exception as e:
        print(f"ERROR: Component 7 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
