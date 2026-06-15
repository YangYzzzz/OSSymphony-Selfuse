"""
Reward Script: Configure TypeScript project references for Angular project
Task ID: vscode_fix_095
Domain: vscode
Scoring:
  Component 1 (0.35): tsconfig.json has "references" array with tsconfig.app.json entry
  Component 2 (0.35): tsconfig.json has "references" array with tsconfig.spec.json entry
  Component 3 (0.30): tsconfig.spec.json has "types": ["jasmine"] in compilerOptions
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_095'
PROJECT_DIR = os.path.join(WORKDIR, 'angular-project')


def load_jsonc(file_path):
    """Load a JSON/JSONC file, stripping comments."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip multi-line comments (/* ... */)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    tsconfig_path = os.path.join(PROJECT_DIR, 'tsconfig.json')
    tsconfig_spec_path = os.path.join(PROJECT_DIR, 'tsconfig.spec.json')

    # Precondition: tsconfig.json must exist and be valid JSON
    try:
        tsconfig = load_jsonc(tsconfig_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load {tsconfig_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: tsconfig.json references tsconfig.app.json (0.35 points)
    try:
        refs = tsconfig.get('references', [])
        if isinstance(refs, list):
            app_ref_found = any(
                isinstance(r, dict) and
                r.get('path', '').replace('\\', '/').rstrip('/') in (
                    './tsconfig.app.json', 'tsconfig.app.json'
                )
                for r in refs
            )
            if app_ref_found:
                print(f"PASS: Component 1 - tsconfig.json has reference to tsconfig.app.json (0.35 pts)")
                total_score += 0.35
            else:
                ref_paths = [r.get('path', '') for r in refs if isinstance(r, dict)]
                print(f"FAIL: Component 1 - tsconfig.app.json not in references. Found: {ref_paths}")
        else:
            print(f"FAIL: Component 1 - 'references' is not a list, got: {type(refs).__name__}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: tsconfig.json references tsconfig.spec.json (0.35 points)
    try:
        refs = tsconfig.get('references', [])
        if isinstance(refs, list):
            spec_ref_found = any(
                isinstance(r, dict) and
                r.get('path', '').replace('\\', '/').rstrip('/') in (
                    './tsconfig.spec.json', 'tsconfig.spec.json'
                )
                for r in refs
            )
            if spec_ref_found:
                print(f"PASS: Component 2 - tsconfig.json has reference to tsconfig.spec.json (0.35 pts)")
                total_score += 0.35
            else:
                ref_paths = [r.get('path', '') for r in refs if isinstance(r, dict)]
                print(f"FAIL: Component 2 - tsconfig.spec.json not in references. Found: {ref_paths}")
        else:
            print(f"FAIL: Component 2 - 'references' is not a list, got: {type(refs).__name__}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: tsconfig.spec.json has "types": ["jasmine"] in compilerOptions (0.30 points)
    try:
        tsconfig_spec = load_jsonc(tsconfig_spec_path)
        compiler_options = tsconfig_spec.get('compilerOptions', {})
        types_list = compiler_options.get('types', [])
        if isinstance(types_list, list) and 'jasmine' in types_list:
            print(f"PASS: Component 3 - tsconfig.spec.json has 'jasmine' in compilerOptions.types (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 - Expected 'jasmine' in compilerOptions.types, found: {types_list}")
    except FileNotFoundError:
        print(f"FAIL: Component 3 - tsconfig.spec.json not found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
