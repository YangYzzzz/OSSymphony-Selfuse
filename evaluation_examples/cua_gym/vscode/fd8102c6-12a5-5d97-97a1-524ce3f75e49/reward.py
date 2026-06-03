"""
Reward Script: Configure C/C++ extension to use clang-format with LLVM style
Task ID: vscode_lang_083
Domain: vscode
Scoring:
  Component 1 (0.35): .clang-format file exists in workspace with BasedOnStyle: LLVM
  Component 2 (0.35): settings.json contains C_Cpp.formatting = clangFormat
  Component 3 (0.30): settings.json contains C_Cpp.clang_format_style = file
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_083'
WORKSPACE_DIR = os.path.join(WORKDIR, 'workspace')
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_settings(path):
    """Load VSCode settings.json, handling JSONC (comments)."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        # Strip trailing commas before } or ]
        content = re.sub(r',\s*([}\]])', r'\1', content)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARNING: Could not load settings from {path}: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: .clang-format file exists in workspace with BasedOnStyle: LLVM (0.35 points)
    try:
        clang_format_path = os.path.join(WORKSPACE_DIR, '.clang-format')
        if os.path.isfile(clang_format_path):
            with open(clang_format_path, 'r') as f:
                content = f.read()
            # Check that the file contains BasedOnStyle: LLVM
            # Allow variations: spaces, quotes, case
            if re.search(r'BasedOnStyle\s*:\s*LLVM', content):
                print(f"PASS: Component 1 -- .clang-format has BasedOnStyle: LLVM (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 -- .clang-format exists but does not contain 'BasedOnStyle: LLVM'. Content: {content.strip()!r}")
        else:
            print(f"FAIL: Component 1 -- .clang-format not found at {clang_format_path}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: settings.json contains C_Cpp.formatting = clangFormat (0.35 points)
    try:
        settings = load_settings(SETTINGS_PATH)
        if settings is None:
            print(f"FAIL: Component 2 -- Could not load settings.json")
        else:
            formatting_value = settings.get('C_Cpp.formatting')
            if formatting_value == 'clangFormat':
                print(f"PASS: Component 2 -- C_Cpp.formatting = 'clangFormat' (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 -- C_Cpp.formatting = {formatting_value!r}, expected 'clangFormat'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: settings.json contains C_Cpp.clang_format_style = file (0.30 points)
    try:
        settings = load_settings(SETTINGS_PATH)
        if settings is None:
            print(f"FAIL: Component 3 -- Could not load settings.json")
        else:
            style_value = settings.get('C_Cpp.clang_format_style')
            if style_value == 'file':
                print(f"PASS: Component 3 -- C_Cpp.clang_format_style = 'file' (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 -- C_Cpp.clang_format_style = {style_value!r}, expected 'file'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
