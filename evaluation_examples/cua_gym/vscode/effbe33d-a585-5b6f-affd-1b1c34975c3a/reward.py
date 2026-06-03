"""
Reward Script: Configure Jest test runner in VSCode
Task ID: vscode_web_024
Domain: vscode
Scoring:
  Component 1 (0.25): Jest extension (orta.vscode-jest) is installed
  Component 2 (0.25): jest.config.js exists with preset 'ts-jest'
  Component 3 (0.25): jest.config.js has testEnvironment 'jsdom' and TypeScript transform
  Component 4 (0.25): moduleNameMapper handles CSS and asset imports
"""

import os
import re
import json

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'react-ts-app')
TASK_ID = 'vscode_web_024'


def check_extension_installed(extension_id):
    """Check if a VSCode extension is installed by scanning the extensions directory."""
    extensions_dir = os.path.expanduser('~/.vscode/extensions')
    if not os.path.isdir(extensions_dir):
        return False
    for entry in os.listdir(extensions_dir):
        if entry.lower().startswith(extension_id.lower()):
            return True
    return False


def parse_jest_config(file_path):
    """
    Parse jest.config.js by reading its content as text and extracting key fields.
    We use regex since it's a CommonJS module (module.exports = {...}).
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return content
    except Exception:
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Jest extension (orta.vscode-jest) is installed (0.25 points)
    # This changes between initial (not installed) and golden (installed)
    try:
        ext_installed = check_extension_installed('orta.vscode-jest')
        if ext_installed:
            print(f"PASS: Component 1 -- Jest extension orta.vscode-jest is installed (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 -- Jest extension orta.vscode-jest is NOT installed")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: jest.config.js exists with preset 'ts-jest' (0.25 points)
    # This changes between initial (no file) and golden (file with preset)
    jest_config_path = os.path.join(PROJECT_DIR, 'jest.config.js')
    config_content = None
    try:
        if not os.path.exists(jest_config_path):
            print(f"FAIL: Component 2 -- jest.config.js does not exist at {jest_config_path}")
        else:
            config_content = parse_jest_config(jest_config_path)
            if config_content is None:
                print(f"FAIL: Component 2 -- Could not read jest.config.js")
            else:
                # Check for preset: 'ts-jest'
                if re.search(r"""preset\s*:\s*['"]ts-jest['"]""", config_content):
                    print(f"PASS: Component 2 -- jest.config.js exists with preset 'ts-jest' (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 2 -- jest.config.js exists but preset 'ts-jest' not found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: testEnvironment 'jsdom' and TypeScript transform configured (0.25 points)
    # This changes between initial (no file) and golden (file with these settings)
    try:
        if config_content is None:
            print(f"FAIL: Component 3 -- jest.config.js not available for checking")
        else:
            has_jsdom = bool(re.search(r"""testEnvironment\s*:\s*['"]jsdom['"]""", config_content))
            # Check for transform with ts-jest for .tsx? files
            has_ts_transform = bool(re.search(r"""transform\s*:""", config_content) and
                                     re.search(r"""ts-jest""", config_content))

            if has_jsdom and has_ts_transform:
                print(f"PASS: Component 3 -- testEnvironment 'jsdom' and TypeScript transform configured (0.25 pts)")
                total_score += 0.25
            else:
                details = []
                if not has_jsdom:
                    details.append("testEnvironment 'jsdom' not found")
                if not has_ts_transform:
                    details.append("TypeScript transform not found")
                print(f"FAIL: Component 3 -- {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: moduleNameMapper handles CSS and asset imports (0.25 points)
    # This changes between initial (no file) and golden (file with moduleNameMapper)
    try:
        if config_content is None:
            print(f"FAIL: Component 4 -- jest.config.js not available for checking")
        else:
            has_module_mapper = bool(re.search(r'moduleNameMapper\s*:', config_content))
            # Extract moduleNameMapper section for targeted checks
            mapper_section = ''
            if 'moduleNameMapper' in config_content:
                # Get text after moduleNameMapper up to the next top-level key or closing brace
                idx = config_content.index('moduleNameMapper')
                mapper_section = config_content[idx:idx+500]

            # Check for CSS pattern (css|less|scss|sass or similar)
            has_css_mock = bool(re.search(r'css', mapper_section))
            # Check for asset/file pattern (jpg|png|gif|svg or similar)
            has_asset_mock = bool(re.search(r'(jpg|png|gif|svg)', mapper_section))

            if has_module_mapper and has_css_mock and has_asset_mock:
                print(f"PASS: Component 4 -- moduleNameMapper handles CSS and asset imports (0.25 pts)")
                total_score += 0.25
            else:
                details = []
                if not has_module_mapper:
                    details.append("moduleNameMapper not found")
                if not has_css_mock:
                    details.append("CSS mock mapping not found")
                if not has_asset_mock:
                    details.append("Asset mock mapping not found")
                print(f"FAIL: Component 4 -- {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
