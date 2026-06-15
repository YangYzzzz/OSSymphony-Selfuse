"""
Reward Script: Configure VSCode pylint with pyproject.toml
Task ID: vscode_stu_070
Domain: vscode
Scoring:
  Component 1: pyproject.toml has pylint max-line-length = 100 (0.3 pts)
  Component 2: pyproject.toml disables missing-docstring warning (0.3 pts)
  Component 3: VSCode settings enable pylint as the linter (0.4 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_070'
PROJECT_DIR = os.path.join(WORKDIR, 'cs301', 'project')
PYPROJECT_PATH = os.path.join(PROJECT_DIR, 'pyproject.toml')
VSCODE_SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def parse_toml_simple(content):
    """
    Minimal TOML parser sufficient for pyproject.toml pylint config.
    Returns a nested dict.
    """
    result = {}
    current_section = None
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        # Match section headers like [tool.pylint.format] or [tool.pylint."messages control"]
        section_match = re.match(r'^\[(.+)\]$', line)
        if section_match:
            current_section = section_match.group(1)
            continue
        # Match key = value
        kv_match = re.match(r'^([a-zA-Z_-]+)\s*=\s*(.+)$', line)
        if kv_match and current_section:
            key = kv_match.group(1).strip()
            value_str = kv_match.group(2).strip()
            # Parse value
            if value_str.startswith('[') and value_str.endswith(']'):
                # Array of strings
                items = re.findall(r'"([^"]*)"', value_str)
                value = items
            elif value_str.startswith('"') and value_str.endswith('"'):
                value = value_str.strip('"')
            else:
                try:
                    value = int(value_str)
                except ValueError:
                    try:
                        value = float(value_str)
                    except ValueError:
                        value = value_str
            if current_section not in result:
                result[current_section] = {}
            result[current_section][key] = value
    return result


def load_vscode_settings(path):
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        # Strip trailing commas before } or ]
        content = re.sub(r',\s*([}\]])', r'\1', content)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARN: Could not load settings: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # =========================================================
    # Component 1: pyproject.toml has max-line-length = 100 (0.3 pts)
    # =========================================================
    try:
        if not os.path.exists(PYPROJECT_PATH):
            print(f"FAIL: Component 1 -- pyproject.toml does not exist at {PYPROJECT_PATH}")
        else:
            with open(PYPROJECT_PATH, 'r') as f:
                toml_content = f.read()
            parsed = parse_toml_simple(toml_content)

            # Look for max-line-length = 100 under [tool.pylint.format]
            format_section = parsed.get('tool.pylint.format', {})
            max_line = format_section.get('max-line-length')
            if max_line == 100:
                print(f"PASS: Component 1 -- max-line-length = {max_line} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 -- max-line-length expected 100, found: {max_line}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # =========================================================
    # Component 2: pyproject.toml disables missing-docstring (0.3 pts)
    # =========================================================
    try:
        if not os.path.exists(PYPROJECT_PATH):
            print(f"FAIL: Component 2 -- pyproject.toml does not exist")
        else:
            with open(PYPROJECT_PATH, 'r') as f:
                toml_content = f.read()
            parsed = parse_toml_simple(toml_content)

            # Look for disable containing "missing-docstring" under messages control section
            # Section could be [tool.pylint."messages control"] or [tool.pylint.messages_control]
            disable_list = None
            for section_name, section_data in parsed.items():
                if 'pylint' in section_name and ('messages' in section_name.lower() or 'message' in section_name.lower()):
                    disable_list = section_data.get('disable', None)
                    break

            if disable_list is not None:
                # Handle both list and string formats
                if isinstance(disable_list, list):
                    has_missing_docstring = any('missing-docstring' in item for item in disable_list)
                elif isinstance(disable_list, str):
                    has_missing_docstring = 'missing-docstring' in disable_list
                else:
                    has_missing_docstring = False

                if has_missing_docstring:
                    print(f"PASS: Component 2 -- missing-docstring is disabled (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 -- disable list does not contain 'missing-docstring': {disable_list}")
            else:
                print(f"FAIL: Component 2 -- no pylint messages control section found with 'disable' key")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # =========================================================
    # Component 3: VSCode settings enable pylint (0.4 pts)
    # =========================================================
    try:
        settings = load_vscode_settings(VSCODE_SETTINGS_PATH)
        if settings is None:
            print(f"FAIL: Component 3 -- Could not load VSCode settings")
        else:
            # Check for pylint being enabled in VSCode settings
            # Possible keys: "pylint.enabled", "python.linting.pylintEnabled", "python.linting.enabled"
            # Check new-style or legacy pylint extension setting
            pylint_enabled = (settings.get('pylint.enabled') is True
                              or settings.get('python.linting.pylintEnabled') is True)

            if pylint_enabled:
                print(f"PASS: Component 3 -- VSCode pylint is enabled (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 3 -- pylint not enabled in settings. Keys found: pylint.enabled={settings.get('pylint.enabled')}, python.linting.pylintEnabled={settings.get('python.linting.pylintEnabled')}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
