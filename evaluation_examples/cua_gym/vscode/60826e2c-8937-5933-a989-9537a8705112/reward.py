"""
Reward Script: Configure a custom Python snippet for try/except/finally block
Task ID: vscode_prod_037
Domain: vscode
Scoring:
  - Component 1 (0.15): python.json snippet file exists with valid JSON
  - Component 2 (0.25): A snippet with prefix 'tryf' exists
  - Component 3 (0.30): Body contains try/except/finally block structure
  - Component 4 (0.20): Body has tab-stop placeholders ($1, $2, $3, $4)
  - Component 5 (0.10): Exception type placeholder defaults to 'Exception'
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_prod_037'

# Possible locations for the snippet file
SNIPPET_PATHS = [
    os.path.join(WORKDIR, '.config', 'Code', 'User', 'snippets', 'python.json'),
    os.path.join(WORKDIR, '.vscode', 'python.json'),
]


def strip_jsonc_comments(text):
    """Strip // and /* */ comments from JSONC content."""
    # Remove single-line comments
    text = re.sub(r'//.*$', '', text, flags=re.MULTILINE)
    # Remove multi-line comments
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    return text


def load_snippet_file():
    """Try to load the python.json snippet file from known locations."""
    for path in SNIPPET_PATHS:
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    content = f.read()
                # Try direct JSON parse first
                try:
                    data = json.loads(content)
                except json.JSONDecodeError:
                    # Try stripping JSONC comments
                    data = json.loads(strip_jsonc_comments(content))
                return path, data
            except Exception as e:
                print(f"ERROR: Found {path} but cannot parse: {e}")
                return path, None
    return None, None


def find_tryf_snippet(snippets):
    """Find a snippet entry whose prefix is or contains 'tryf'."""
    if not isinstance(snippets, dict):
        return None, None
    for name, entry in snippets.items():
        if not isinstance(entry, dict):
            continue
        prefix = entry.get('prefix', '')
        # prefix can be a string or list of strings
        if isinstance(prefix, str) and prefix.lower() == 'tryf':
            return name, entry
        if isinstance(prefix, list):
            for p in prefix:
                if isinstance(p, str) and p.lower() == 'tryf':
                    return name, entry
    return None, None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: python.json snippet file exists with valid JSON (0.15 points)
    try:
        path, snippets = load_snippet_file()
        if path is not None and snippets is not None:
            print(f"PASS: Component 1 -- python.json found at {path} with valid JSON (0.15 pts)")
            total_score += 0.15
        elif path is not None:
            print(f"FAIL: Component 1 -- python.json found at {path} but invalid JSON")
        else:
            print("FAIL: Component 1 -- No python.json snippet file found")
            print(f"  Searched: {SNIPPET_PATHS}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: A snippet with prefix 'tryf' exists (0.25 points)
    try:
        snippet_name, snippet_entry = find_tryf_snippet(snippets)
        if snippet_entry is not None:
            print(f"PASS: Component 2 -- Snippet '{snippet_name}' has prefix 'tryf' (0.25 pts)")
            total_score += 0.25
        else:
            print("FAIL: Component 2 -- No snippet with prefix 'tryf' found")
            prefixes = []
            for name, entry in snippets.items():
                if isinstance(entry, dict):
                    prefixes.append(f"  '{name}': prefix='{entry.get('prefix', '')}'")
            if prefixes:
                print("  Available snippets:")
                for p in prefixes:
                    print(p)
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    if snippet_entry is None:
        # Cannot continue checking body without a snippet
        final_score = round(min(total_score, 1.0), 2)
        print(f"\nScore: {final_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    body = snippet_entry.get('body', [])
    if isinstance(body, str):
        body_lines = body.split('\n')
    elif isinstance(body, list):
        body_lines = body
    else:
        body_lines = []

    body_text = '\n'.join(str(line) for line in body_lines)

    # Component 3: Body contains try/except/finally block structure (0.30 points)
    try:
        has_try = any('try:' in str(line) for line in body_lines)
        has_except = any('except' in str(line).lower() for line in body_lines)
        has_finally = any('finally:' in str(line) for line in body_lines)

        parts_found = sum([has_try, has_except, has_finally])
        if parts_found == 3:
            print(f"PASS: Component 3 -- Body contains try/except/finally structure (0.30 pts)")
            total_score += 0.30
        else:
            missing = []
            if not has_try:
                missing.append('try:')
            if not has_except:
                missing.append('except')
            if not has_finally:
                missing.append('finally:')
            print(f"FAIL: Component 3 -- Body missing: {missing} (found {parts_found}/3)")
            print(f"  Body: {body_lines}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Body has tab-stop placeholders ($1, $2, $3, $4) (0.20 points)
    try:
        placeholders_found = set()
        for i in range(1, 5):
            # Match ${N:...} or $N patterns
            pattern = rf'\${i}(?:\b|:|\}})|(\$\{{{i}(?::|\}}))'
            if re.search(pattern, body_text):
                placeholders_found.add(i)

        if len(placeholders_found) >= 4:
            print(f"PASS: Component 4 -- All 4 tab-stop placeholders found: {sorted(placeholders_found)} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 -- Found placeholders {sorted(placeholders_found)}, expected {{1,2,3,4}}")
            print(f"  Body text: {body_text}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Exception type placeholder defaults to 'Exception' (0.10 points)
    try:
        # Look for ${N:Exception} pattern in the except line
        except_lines_with_default = [
            str(line) for line in body_lines
            if 'except' in str(line).lower()
            and re.search(r'\$\{\d+:Exception\}', str(line))
        ]

        if len(except_lines_with_default) > 0:
            print(f"PASS: Component 5 -- Exception type placeholder defaults to 'Exception' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 -- No placeholder with default 'Exception' found in except line")
            except_lines = [str(l) for l in body_lines if 'except' in str(l).lower()]
            print(f"  Except lines: {except_lines}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
