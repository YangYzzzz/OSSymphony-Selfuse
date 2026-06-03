"""
Reward Script: VSCode Custom Code Snippets Creation
Task ID: vscode_gf6_043
Domain: vscode
Scoring:
  - Component 1 (0.30): Python snippets file with pytest-class, dataclass-model, async-handler
  - Component 2 (0.25): TypeScript snippets file with react-component, api-slice
  - Component 3 (0.20): .vscode/PROJECT.code-snippets with domain-entity snippet
  - Component 4 (0.15): Snippet bodies contain tab stops ($1/$2 or $TM_FILENAME_BASE)
  - Component 5 (0.10): Snippet structural correctness (prefix, body array, description)
"""

import os
import json
import re

HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SNIPPETS_DIR = os.path.join(VSCODE_USER, 'snippets')
PROJECT_DIR = os.path.join(HOME, 'projects', 'vscode-snippets')
PROJECT_SNIPPETS = os.path.join(PROJECT_DIR, '.vscode', 'PROJECT.code-snippets')

TASK_ID = 'vscode_gf6_043'

PYTHON_REQUIRED = ['pytest-class', 'dataclass-model', 'async-handler']
TS_REQUIRED = ['react-component', 'api-slice']


def load_json_safe(path):
    """Load JSON, handling JSONC comments."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip // comments (JSONC)
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(cleaned)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  Cannot load {path}: {e}")
        return None


def has_tab_stops(body_lines):
    """Check if snippet body contains tab stops ($1, $2, etc.) or $TM_FILENAME_BASE."""
    body_text = '\n'.join(body_lines) if isinstance(body_lines, list) else str(body_lines)
    return bool(re.search(r'\$(\d+|{[^}]+}|TM_FILENAME_BASE)', body_text))


def is_valid_snippet(snippet):
    """Check snippet has required structure: prefix (str), body (list), description (str)."""
    if not isinstance(snippet, dict):
        return False
    has_prefix = 'prefix' in snippet and isinstance(snippet['prefix'], str) and len(snippet['prefix']) > 0
    has_body = 'body' in snippet and isinstance(snippet['body'], list) and len(snippet['body']) > 0
    has_desc = 'description' in snippet and isinstance(snippet['description'], str) and len(snippet['description']) > 0
    return has_prefix and has_body and has_desc


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Python snippets file with 3 required entries (0.30 points)
    try:
        py_snippets_path = os.path.join(SNIPPETS_DIR, 'python.json')
        py_data = load_json_safe(py_snippets_path)
        if py_data is not None:
            found_keys = [k for k in PYTHON_REQUIRED if k in py_data]
            if len(found_keys) == len(PYTHON_REQUIRED):
                print(f"PASS: Component 1 — All 3 Python snippets found: {found_keys} (0.30 pts)")
                total_score += 0.30
            else:
                missing = [k for k in PYTHON_REQUIRED if k not in py_data]
                print(f"FAIL: Component 1 — Missing Python snippets: {missing}. Found: {found_keys}")
        else:
            print(f"FAIL: Component 1 — Python snippets file not found or invalid at {py_snippets_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: TypeScript snippets file with 2 required entries (0.25 points)
    try:
        ts_snippets_path = os.path.join(SNIPPETS_DIR, 'typescript.json')
        ts_data = load_json_safe(ts_snippets_path)
        if ts_data is not None:
            found_keys = [k for k in TS_REQUIRED if k in ts_data]
            if len(found_keys) == len(TS_REQUIRED):
                print(f"PASS: Component 2 — All 2 TypeScript snippets found: {found_keys} (0.25 pts)")
                total_score += 0.25
            else:
                missing = [k for k in TS_REQUIRED if k not in ts_data]
                print(f"FAIL: Component 2 — Missing TypeScript snippets: {missing}. Found: {found_keys}")
        else:
            print(f"FAIL: Component 2 — TypeScript snippets file not found or invalid at {ts_snippets_path}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: PROJECT.code-snippets with domain-entity snippet (0.20 points)
    try:
        proj_data = load_json_safe(PROJECT_SNIPPETS)
        if proj_data is not None and 'domain-entity' in proj_data:
            print(f"PASS: Component 3 — PROJECT.code-snippets has 'domain-entity' snippet (0.20 pts)")
            total_score += 0.20
        elif proj_data is not None:
            print(f"FAIL: Component 3 — PROJECT.code-snippets exists but missing 'domain-entity'. Keys: {list(proj_data.keys())}")
        else:
            print(f"FAIL: Component 3 — PROJECT.code-snippets not found at {PROJECT_SNIPPETS}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Snippet bodies contain tab stops or $TM_FILENAME_BASE (0.15 points)
    # Check across all snippet files — at least 4 of 6 snippets must have tab stops
    try:
        snippets_with_tabs = 0
        total_snippets = 0
        all_snippet_data = []

        # Gather all snippet data from files that exist
        for path in [os.path.join(SNIPPETS_DIR, 'python.json'),
                     os.path.join(SNIPPETS_DIR, 'typescript.json'),
                     PROJECT_SNIPPETS]:
            data = load_json_safe(path)
            if data:
                all_snippet_data.append(data)

        for data in all_snippet_data:
            for name, snippet in data.items():
                if isinstance(snippet, dict) and 'body' in snippet:
                    total_snippets += 1
                    if has_tab_stops(snippet['body']):
                        snippets_with_tabs += 1

        if total_snippets >= 5 and snippets_with_tabs >= 4:
            print(f"PASS: Component 4 — {snippets_with_tabs}/{total_snippets} snippets have tab stops (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Only {snippets_with_tabs}/{total_snippets} snippets have tab stops (need >= 4 of >= 5)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Snippet structural correctness — all snippets have prefix, body array, description (0.10 points)
    try:
        valid_count = 0
        total_check = 0
        for data in all_snippet_data:
            for name, snippet in data.items():
                total_check += 1
                if is_valid_snippet(snippet):
                    valid_count += 1
                else:
                    print(f"  WARN: Snippet '{name}' has invalid structure")

        if total_check >= 5 and valid_count == total_check:
            print(f"PASS: Component 5 — All {valid_count} snippets have valid structure (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — {valid_count}/{total_check} snippets have valid structure (need all >= 5)")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
