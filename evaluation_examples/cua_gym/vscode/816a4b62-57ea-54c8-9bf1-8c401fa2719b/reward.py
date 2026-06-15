"""
Reward Script: Sort import statements alphabetically and remove duplicate import of 'json'
Task ID: vscode_rrt_049
Domain: vscode
Scoring:
  Component 1 (0.30): Duplicate 'import json' removed (only one 'import json' line)
  Component 2 (0.30): Standard library imports sorted alphabetically
  Component 3 (0.20): Flask imports consolidated into single grouped import
  Component 4 (0.20): Proper blank-line separation between stdlib and third-party groups
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_049'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'app', 'server.py')


def extract_import_section(lines):
    """Extract the import block at the top of the file (before any non-import, non-blank code)."""
    import_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped == '' or stripped.startswith('import ') or stripped.startswith('from '):
            import_lines.append(line)
        else:
            break
    return import_lines


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
        lines = content.split('\n')
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract the import section (top of file before first non-import code)
    import_section = extract_import_section(lines)
    import_text = '\n'.join(import_section)

    # Collect actual import statements (non-blank lines in import section)
    import_stmts = [l.strip() for l in import_section if l.strip() != '']

    # Component 1: Duplicate 'import json' removed (0.30 points)
    # In initial state, 'import json' appears twice. In golden, only once.
    try:
        json_import_count = sum(1 for stmt in import_stmts if stmt == 'import json')
        if json_import_count == 1:
            print(f"PASS: Component 1 -- 'import json' appears exactly once ({json_import_count}) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 -- 'import json' appears {json_import_count} times, expected 1")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Standard library imports sorted alphabetically (0.30 points)
    # Expected stdlib imports in order: json, logging, os, sys, datetime (via from), pathlib (via from)
    # We check that direct 'import X' statements are alphabetically ordered
    # and 'from X import Y' statements for stdlib are alphabetically ordered by module name
    try:
        # Separate stdlib direct imports and stdlib from-imports
        stdlib_modules = {'json', 'logging', 'os', 'sys', 'datetime', 'pathlib',
                          'collections', 'functools', 'typing', 're', 'io', 'math',
                          'time', 'random', 'copy', 'itertools', 'abc', 'enum',
                          'dataclasses', 'unittest', 'argparse', 'string', 'textwrap',
                          'shutil', 'glob', 'csv', 'hashlib', 'uuid', 'socket',
                          'threading', 'multiprocessing', 'contextlib', 'operator'}

        direct_imports = []
        from_imports_stdlib = []
        for stmt in import_stmts:
            if stmt.startswith('import '):
                mod = stmt.split()[1].split('.')[0]
                if mod in stdlib_modules:
                    direct_imports.append(mod)
            elif stmt.startswith('from '):
                mod = stmt.split()[1].split('.')[0]
                if mod in stdlib_modules:
                    from_imports_stdlib.append(mod)

        # Check direct imports are sorted
        direct_sorted = direct_imports == sorted(direct_imports)
        # Check from-imports are sorted by module name
        from_sorted = from_imports_stdlib == sorted(from_imports_stdlib)
        # Additionally, direct imports should come before from-imports for stdlib
        # (PEP8/isort: 'import X' before 'from X import Y' within a group)
        # But the golden shows: import json, import logging, import os, import sys, from datetime..., from pathlib...
        # So direct 'import' first, then 'from' - both sorted alphabetically within their sub-group

        all_sorted = direct_sorted and from_sorted
        if all_sorted:
            print(f"PASS: Component 2 -- Stdlib imports are alphabetically sorted (0.30 pts)")
            print(f"  Direct imports order: {direct_imports}")
            print(f"  From imports order: {from_imports_stdlib}")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 -- Stdlib imports not sorted")
            print(f"  Direct imports: {direct_imports} (sorted: {direct_sorted})")
            print(f"  From imports: {from_imports_stdlib} (sorted: {from_sorted})")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Flask imports consolidated into single line (0.20 points)
    # Initial has two separate flask import lines:
    #   from flask import Flask, request
    #   from flask import jsonify
    # Golden should have one consolidated line:
    #   from flask import Flask, jsonify, request
    try:
        flask_import_lines = [stmt for stmt in import_stmts if 'flask' in stmt.lower() and stmt.startswith('from flask')]
        if len(flask_import_lines) == 1:
            # Check that all three names are present
            flask_line = flask_import_lines[0]
            imported_names = set()
            # Parse "from flask import X, Y, Z"
            after_import = flask_line.split('import', 1)[1]
            for name in after_import.split(','):
                imported_names.add(name.strip())
            expected_names = {'Flask', 'jsonify', 'request'}
            if expected_names.issubset(imported_names):
                print(f"PASS: Component 3 -- Flask imports consolidated into one line with all names (0.20 pts)")
                print(f"  Found: {flask_line}")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 -- Flask import line missing names. Found: {imported_names}, expected: {expected_names}")
        else:
            print(f"FAIL: Component 3 -- Expected 1 flask import line, found {len(flask_import_lines)}: {flask_import_lines}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Proper blank-line separation between stdlib and third-party groups (0.20 points)
    # Golden state has a blank line between 'from pathlib import Path' and 'from flask import ...'
    # We check that there is at least one blank line separating stdlib imports from third-party imports
    try:
        # Find the position of the last stdlib import and first third-party import
        last_stdlib_idx = -1
        first_thirdparty_idx = -1
        for i, line in enumerate(import_section):
            stripped = line.strip()
            if stripped == '':
                continue
            if stripped.startswith('import ') or stripped.startswith('from '):
                mod = stripped.split()[1].split('.')[0]
                if mod in stdlib_modules:
                    last_stdlib_idx = i
                else:
                    if first_thirdparty_idx == -1:
                        first_thirdparty_idx = i

        if last_stdlib_idx >= 0 and first_thirdparty_idx > last_stdlib_idx:
            # Check if there's a blank line between them
            has_blank = False
            for i in range(last_stdlib_idx + 1, first_thirdparty_idx):
                if import_section[i].strip() == '':
                    has_blank = True
                    break
            if has_blank:
                print(f"PASS: Component 4 -- Blank line separates stdlib and third-party imports (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 -- No blank line between stdlib (line {last_stdlib_idx}) and third-party (line {first_thirdparty_idx})")
        elif first_thirdparty_idx == -1:
            print(f"FAIL: Component 4 -- No third-party imports found")
        else:
            print(f"FAIL: Component 4 -- Third-party imports appear before stdlib imports")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
