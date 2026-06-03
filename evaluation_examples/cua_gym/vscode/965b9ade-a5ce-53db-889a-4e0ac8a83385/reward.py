"""
Reward Script: Configure VSCode Python black formatter with skip-string-normalization via pyproject.toml
Task ID: vscode_py_094
Domain: vscode
Scoring:
  Component 1 (0.40): pyproject.toml has [tool.black] with skip-string-normalization = true
  Component 2 (0.35): VSCode settings configure black as default Python formatter
  Component 3 (0.25): VSCode settings enable formatOnSave for Python
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_094'

WORKSPACE_DIR = os.path.join(WORKDIR, 'workspace')
PYPROJECT_PATH = os.path.join(WORKSPACE_DIR, 'pyproject.toml')
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def parse_toml_simple(content):
    """Simple TOML parser to extract [tool.black] section values."""
    sections = {}
    current_section = None
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        # Match section headers like [tool.black]
        section_match = re.match(r'^\[(.+)\]$', line)
        if section_match:
            current_section = section_match.group(1)
            sections[current_section] = {}
            continue
        if current_section and '=' in line:
            key, _, value = line.partition('=')
            key = key.strip()
            value = value.strip()
            # Parse boolean
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            # Parse integers
            elif value.isdigit():
                value = int(value)
            # Parse strings (remove quotes)
            elif (value.startswith('"') and value.endswith('"')) or \
                 (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            sections[current_section][key] = value
    return sections


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip single-line comments for JSONC
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        # Strip trailing commas before } or ]
        content = re.sub(r',\s*([}\]])', r'\1', content)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: pyproject.toml has [tool.black] with skip-string-normalization = true (0.40 points)
    try:
        if not os.path.exists(PYPROJECT_PATH):
            print(f"FAIL: Component 1 -- pyproject.toml not found at {PYPROJECT_PATH}")
        else:
            with open(PYPROJECT_PATH, 'r') as f:
                toml_content = f.read()
            sections = parse_toml_simple(toml_content)
            if 'tool.black' not in sections:
                print("FAIL: Component 1 -- [tool.black] section not found in pyproject.toml")
            else:
                black_config = sections['tool.black']
                skip_val = black_config.get('skip-string-normalization')
                if skip_val is True:
                    print(f"PASS: Component 1 -- [tool.black] skip-string-normalization = true (0.40 pts)")
                    total_score += 0.40
                else:
                    print(f"FAIL: Component 1 -- skip-string-normalization = {skip_val}, expected true")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: VSCode settings have black as default formatter for Python (0.35 points)
    try:
        settings = load_settings()
        if settings is None:
            print("FAIL: Component 2 -- cannot load settings.json")
        else:
            # Check [python] language-specific settings OR top-level default formatter
            python_section = settings.get('[python]', {})
            python_formatter = python_section.get('editor.defaultFormatter', '')
            top_formatter = settings.get('editor.defaultFormatter', '')

            # The formatter should be black - check common extension IDs
            black_ids = ['ms-python.black-formatter', 'mikoz.black-formatter']
            formatter_found = any(
                fid in python_formatter.lower() or fid in top_formatter.lower()
                for fid in black_ids
            )

            if not formatter_found:
                # Also check case-insensitively
                formatter_found = 'black' in python_formatter.lower() or 'black' in top_formatter.lower()

            if formatter_found:
                print(f"PASS: Component 2 -- Black configured as Python formatter "
                      f"(python: '{python_formatter}', top: '{top_formatter}') (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 -- Black not configured as formatter. "
                      f"[python].editor.defaultFormatter='{python_formatter}', "
                      f"editor.defaultFormatter='{top_formatter}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: VSCode settings enable formatOnSave for Python (0.25 points)
    try:
        settings = load_settings()
        if settings is None:
            print("FAIL: Component 3 -- cannot load settings.json")
        else:
            python_section = settings.get('[python]', {})
            format_on_save_python = python_section.get('editor.formatOnSave', None)
            format_on_save_global = settings.get('editor.formatOnSave', None)

            # formatOnSave should be true either in [python] section or globally
            if format_on_save_python is True or format_on_save_global is True:
                print(f"PASS: Component 3 -- formatOnSave enabled "
                      f"(python: {format_on_save_python}, global: {format_on_save_global}) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- formatOnSave not enabled. "
                      f"[python].editor.formatOnSave={format_on_save_python}, "
                      f"editor.formatOnSave={format_on_save_global}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
