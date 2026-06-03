"""
Reward Script: Set up Spring Boot development in VSCode
Task ID: vscode_lang_058
Domain: vscode
Scoring:
  Component 1 (0.40): Spring Boot Extension Pack installed
  Component 2 (0.35): launch.json exists with Spring Boot debug configuration
  Component 3 (0.25): launch.json mainClass matches SpringAppApplication
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_058'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'spring-app')
LAUNCH_JSON_PATH = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')
EXTENSIONS_DIR = os.path.join(WORKDIR, '.vscode', 'extensions')


def get_installed_extensions():
    """Get list of installed VSCode extensions by scanning the extensions directory."""
    try:
        if not os.path.isdir(EXTENSIONS_DIR):
            return []
        entries = os.listdir(EXTENSIONS_DIR)
        # Extension directories are named like "publisher.name-version"
        # Extract the publisher.name part (everything before the last hyphen+version)
        ext_ids = []
        for entry in entries:
            if entry == 'extensions.json' or entry.startswith('.'):
                continue
            # Pattern: publisher.name-version (e.g., vmware.vscode-boot-dev-pack-0.2.2)
            # Split from the right on the last occurrence of -<digit>
            match = re.match(r'^(.+?)-\d+\.\d+', entry)
            if match:
                ext_ids.append(match.group(1).lower())
            else:
                ext_ids.append(entry.lower())
        return ext_ids
    except Exception as e:
        print(f"ERROR: Could not scan extensions directory: {e}")
        return []


def load_jsonc(path):
    """Load a JSON file, stripping // comments (JSONC format)."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Could not load {path}: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Spring Boot Extension Pack installed (0.40 points)
    # The extension pack ID is vmware.vscode-boot-dev-pack
    # This FAILS on initial_env (no extensions) and PASSES on golden_env
    try:
        extensions = get_installed_extensions()
        target_ext = 'vmware.vscode-boot-dev-pack'
        if target_ext in extensions:
            print(f"PASS: Component 1 — Spring Boot Extension Pack '{target_ext}' is installed (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 1 — '{target_ext}' not found in installed extensions: {extensions}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: launch.json exists with a Spring Boot debug configuration (0.35 points)
    # Must have at least one configuration with type "java" and request "launch"
    # This FAILS on initial_env (no launch.json) and PASSES on golden_env
    try:
        if not os.path.exists(LAUNCH_JSON_PATH):
            print(f"FAIL: Component 2 — launch.json does not exist at {LAUNCH_JSON_PATH}")
        else:
            launch_data = load_jsonc(LAUNCH_JSON_PATH)
            if launch_data is None:
                print(f"FAIL: Component 2 — Could not parse launch.json")
            else:
                configurations = launch_data.get('configurations', [])
                # Find a Spring Boot launch configuration
                matching_configs = [
                    config for config in configurations
                    if str(config.get('type', '')).lower() == 'java'
                    and str(config.get('request', '')).lower() == 'launch'
                ]
                if len(matching_configs) > 0:
                    print(f"PASS: Component 2 — Found Java launch configuration: '{matching_configs[0].get('name', 'unnamed')}' (0.35 pts)")
                    total_score += 0.35
                else:
                    print(f"FAIL: Component 2 — No configuration with type='java' and request='launch' found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: launch.json mainClass references SpringAppApplication (0.25 points)
    # The golden state has mainClass = "com.example.springapp.SpringAppApplication"
    # This FAILS on initial_env (no launch.json) and PASSES on golden_env
    try:
        if not os.path.exists(LAUNCH_JSON_PATH):
            print(f"FAIL: Component 3 — launch.json does not exist")
        else:
            launch_data = load_jsonc(LAUNCH_JSON_PATH)
            if launch_data is None:
                print(f"FAIL: Component 3 — Could not parse launch.json")
            else:
                configurations = launch_data.get('configurations', [])
                matching_main = [
                    config for config in configurations
                    if 'SpringAppApplication' in str(config.get('mainClass', ''))
                ]
                if len(matching_main) > 0:
                    main_class = matching_main[0].get('mainClass', '')
                    print(f"PASS: Component 3 — mainClass '{main_class}' references SpringAppApplication (0.25 pts)")
                    total_score += 0.25
                else:
                    all_main_classes = [config.get('mainClass', 'none') for config in configurations]
                    print(f"FAIL: Component 3 — No configuration has mainClass with 'SpringAppApplication'. Found: {all_main_classes}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
