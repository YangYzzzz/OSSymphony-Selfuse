"""
Reward Script: Add missing type imports for api_types.py
Task ID: vscode_py_089
Domain: vscode
Scoring:
  Component 1 (0.3): from typing import statement exists with at least 3 of 5 required types
  Component 2 (0.3): All 5 required types (Optional, List, Dict, Union, Tuple) are imported
  Component 3 (0.4): Imports placed correctly at top of file and file body preserved
"""

import os
import re
import ast

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_089'

# The 5 types that must be imported from typing
REQUIRED_TYPES = {'Optional', 'List', 'Dict', 'Union', 'Tuple'}


def parse_typing_imports(content):
    """Extract type names imported from typing module."""
    imported_types = set()
    # Match: from typing import X, Y, Z (possibly multiline with parens)
    # Single-line pattern
    pattern_single = r'^from\s+typing\s+import\s+(.+)$'
    for line in content.split('\n'):
        m = re.match(pattern_single, line.strip())
        if m:
            names = m.group(1).strip()
            # Remove trailing comments
            names = re.sub(r'#.*$', '', names)
            # Remove parens if present
            names = names.strip('()')
            for name in names.split(','):
                name = name.strip()
                if name:
                    imported_types.add(name)

    # Also handle multiline: from typing import (\n  X,\n  Y\n)
    pattern_multi = r'from\s+typing\s+import\s*\(([\s\S]*?)\)'
    for m in re.finditer(pattern_multi, content):
        names_block = m.group(1)
        for name in names_block.split(','):
            name = name.strip()
            if name:
                imported_types.add(name)

    return imported_types


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: from typing import statement with at least 3 of 5 required types (0.3 pts)
    try:
        imported_types = parse_typing_imports(content)
        matched = imported_types & REQUIRED_TYPES
        if len(matched) >= 3:
            print(f"PASS: Component 1 -- typing import found with {len(matched)}/5 required types: {matched} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 -- typing import has only {len(matched)}/5 required types: {matched} (need >= 3)")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: All 5 required types are imported (0.3 pts)
    try:
        imported_types = parse_typing_imports(content)
        missing = REQUIRED_TYPES - imported_types
        if len(missing) == 0:
            print(f"PASS: Component 2 -- All 5 required types imported: {REQUIRED_TYPES} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- Missing types: {missing}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Imports placed at top (before first class/def) AND file body preserved (0.4 pts)
    try:
        lines = content.split('\n')

        # Find line number of typing import
        typing_import_line = -1
        for i, line in enumerate(lines):
            if re.match(r'^from\s+typing\s+import', line.strip()):
                typing_import_line = i
                break

        # Find line number of first class or def
        first_class_def_line = -1
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('class ') or (stripped.startswith('def ') and not stripped.startswith('def build_query') is False):
                if re.match(r'^(class|def)\s+', stripped):
                    first_class_def_line = i
                    break

        # Check: typing import exists AND is before the first class/def
        import_at_top = (typing_import_line >= 0 and first_class_def_line >= 0 and typing_import_line < first_class_def_line)

        # Check file body is preserved: key classes and functions must still exist
        has_pagination = 'class PaginationParams' in content
        has_user_profile = 'class UserProfile' in content
        has_api_response = 'class ApiResponse' in content
        has_build_query = 'def build_query' in content
        has_merge_responses = 'def merge_responses' in content
        body_preserved = all([has_pagination, has_user_profile, has_api_response, has_build_query, has_merge_responses])

        if import_at_top and body_preserved:
            print(f"PASS: Component 3 -- typing import at line {typing_import_line+1}, before first class at line {first_class_def_line+1}, body intact (0.4 pts)")
            total_score += 0.4
        elif not import_at_top:
            print(f"FAIL: Component 3 -- typing import line: {typing_import_line+1 if typing_import_line >= 0 else 'NOT FOUND'}, first class/def line: {first_class_def_line+1 if first_class_def_line >= 0 else 'NOT FOUND'}")
        else:
            print(f"FAIL: Component 3 -- File body not preserved. Missing key definitions.")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}/api_types.py'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
