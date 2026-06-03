"""
Reward Script: Configure C/C++ clang-tidy static analysis in VSCode
Task ID: vscode_lang_092
Domain: vscode
Scoring:
  Component 1 (0.35): clangTidy.enabled is true in settings.json
  Component 2 (0.30): clangTidy.checks.enabled contains readability-* and performance-*
  Component 3 (0.35): .clang-tidy file exists with correct Checks line
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_092'

SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')
CLANG_TIDY_PATH = os.path.join(WORKDIR, 'workspace', '.clang-tidy')


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments before parsing
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARNING: Could not load settings.json: {e}")
        return {}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    settings = load_settings()

    # Component 1: C_Cpp.codeAnalysis.clangTidy.enabled is true (0.35 points)
    # This setting enables clang-tidy as the static analysis tool.
    # In initial_env, settings.json is empty, so this will FAIL.
    try:
        clang_tidy_enabled = settings.get('C_Cpp.codeAnalysis.clangTidy.enabled')
        if clang_tidy_enabled is True:
            print(f"PASS: Component 1 - clangTidy.enabled is true (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 - Expected clangTidy.enabled=true, found: {clang_tidy_enabled}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: C_Cpp.codeAnalysis.clangTidy.checks.enabled contains
    # readability-* and performance-* (0.30 points)
    # In initial_env, this key does not exist.
    try:
        checks_enabled = settings.get('C_Cpp.codeAnalysis.clangTidy.checks.enabled')
        if isinstance(checks_enabled, list):
            has_readability = any('readability-*' in str(c) for c in checks_enabled)
            has_performance = any('performance-*' in str(c) for c in checks_enabled)
            if has_readability and has_performance:
                print(f"PASS: Component 2 - checks.enabled contains readability-* and performance-* (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 - Missing checks. readability={has_readability}, performance={has_performance}. Found: {checks_enabled}")
        else:
            print(f"FAIL: Component 2 - checks.enabled is not a list, found: {type(checks_enabled).__name__} = {checks_enabled}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: .clang-tidy file exists in workspace with readability-* and
    # performance-* in the Checks line (0.35 points)
    # In initial_env, .clang-tidy does not exist.
    try:
        if os.path.isfile(CLANG_TIDY_PATH):
            with open(CLANG_TIDY_PATH, 'r') as f:
                content = f.read()
            # Look for a Checks line that includes both readability-* and performance-*
            checks_match = re.search(r"Checks:\s*['\"]?(.+?)['\"]?\s*$", content, re.MULTILINE)
            if checks_match:
                checks_value = checks_match.group(1)
                has_readability = 'readability-*' in checks_value
                has_performance = 'performance-*' in checks_value
                if has_readability and has_performance:
                    print(f"PASS: Component 3 - .clang-tidy has correct Checks: {checks_value} (0.35 pts)")
                    total_score += 0.35
                else:
                    print(f"FAIL: Component 3 - .clang-tidy Checks missing required patterns. readability={has_readability}, performance={has_performance}. Found: {checks_value}")
            else:
                print(f"FAIL: Component 3 - .clang-tidy exists but no Checks line found. Content:\n{content}")
        else:
            print(f"FAIL: Component 3 - .clang-tidy file not found at {CLANG_TIDY_PATH}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
