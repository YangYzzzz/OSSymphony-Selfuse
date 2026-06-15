"""
Reward Script: Fix Python analysis settings for cross-package imports in monorepo
Task ID: vscode_fix_046
Domain: vscode
Scoring:
  Component 1 (0.4): extraPaths includes packages/core/src
  Component 2 (0.4): extraPaths includes packages/api/src
  Component 3 (0.2): Both paths present in a single config (completeness)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_046'
MONOREPO = os.path.join(WORKDIR, 'monorepo')
SETTINGS_PATH = os.path.join(MONOREPO, '.vscode', 'settings.json')
PYRIGHT_PATH = os.path.join(MONOREPO, 'pyrightconfig.json')


def load_json_with_comments(path):
    """Load a JSON/JSONC file, stripping // comments."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments (// ...)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        # Strip trailing commas before } or ]
        content = re.sub(r',\s*([}\]])', r'\1', content)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  Could not load {path}: {e}")
        return None


def get_extra_paths():
    """
    Extract extraPaths from either .vscode/settings.json or pyrightconfig.json.
    Returns a tuple: (source_name, list_of_paths) or (None, []).
    The task says either location is acceptable.
    """
    # Check .vscode/settings.json first
    settings = load_json_with_comments(SETTINGS_PATH)
    if settings is not None:
        extra = settings.get('python.analysis.extraPaths', None)
        if isinstance(extra, list) and len(extra) > 0:
            print(f"  Found extraPaths in settings.json: {extra}")
            return ('settings.json', extra)

    # Check pyrightconfig.json
    pyright = load_json_with_comments(PYRIGHT_PATH)
    if pyright is not None:
        extra = pyright.get('extraPaths', None)
        if isinstance(extra, list) and len(extra) > 0:
            print(f"  Found extraPaths in pyrightconfig.json: {extra}")
            return ('pyrightconfig.json', extra)

    print("  No non-empty extraPaths found in settings.json or pyrightconfig.json")
    return (None, [])


def normalize_path(p):
    """Normalize a path for comparison: strip, remove trailing slash, collapse separators."""
    return p.strip().rstrip('/').replace('\\', '/')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: monorepo directory exists
    if not os.path.isdir(MONOREPO):
        print(f"CRITICAL: Monorepo directory not found at {MONOREPO}")
        print("REWARD: 0.0")
        return 0.0

    source, paths = get_extra_paths()

    if source is None:
        print("FAIL: No extraPaths configuration found")
        print("\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Normalize all paths for comparison
    normalized_paths = [normalize_path(p) for p in paths]
    print(f"  Normalized paths: {normalized_paths}")

    # Expected paths (task ground truth)
    CORE_PATH = 'packages/core/src'
    API_PATH = 'packages/api/src'

    has_core = any(normalize_path(CORE_PATH) == np for np in normalized_paths)
    has_api = any(normalize_path(API_PATH) == np for np in normalized_paths)

    # Component 1: extraPaths includes packages/core/src (0.4 points)
    try:
        if has_core:
            print(f"PASS: Component 1 -- extraPaths contains '{CORE_PATH}' in {source} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- extraPaths missing '{CORE_PATH}'. Found: {normalized_paths}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: extraPaths includes packages/api/src (0.4 points)
    try:
        if has_api:
            print(f"PASS: Component 2 -- extraPaths contains '{API_PATH}' in {source} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 -- extraPaths missing '{API_PATH}'. Found: {normalized_paths}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Both paths present together (0.2 points)
    # This checks completeness -- an agent that only added one path gets partial credit
    # but not full marks
    try:
        if has_core and has_api:
            print(f"PASS: Component 3 -- Both core and api paths present in {source} (0.2 pts)")
            total_score += 0.2
        else:
            missing = []
            if not has_core:
                missing.append(CORE_PATH)
            if not has_api:
                missing.append(API_PATH)
            print(f"FAIL: Component 3 -- Missing paths: {missing}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
