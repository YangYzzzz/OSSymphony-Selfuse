"""
Reward Script: Create a Python user snippet that generates a class with __init__ method.
Task ID: vscode_code_018
Domain: vs_code
Scoring:
  Component 1: python.json exists and contains 'Python Class' snippet entry (0.4 pts)
  Component 2: Snippet has prefix 'pyclass' and correct description (0.3 pts)
  Component 3: Snippet body includes __init__ with type hint placeholders (0.3 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_018'
SNIPPET_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'snippets', 'python.json')


def load_json_with_comments(path):
    """Load a JSON file that may contain // comments (JSONC format)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Pre-condition gate: python.json must exist
    if not os.path.exists(SNIPPET_PATH):
        print(f"FAIL: python.json not found at {SNIPPET_PATH}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load snippets file
    try:
        snippets = load_json_with_comments(SNIPPET_PATH)
    except json.JSONDecodeError as e:
        print(f"FAIL: python.json is invalid JSON: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score
    except Exception as e:
        print(f"ERROR: Could not load python.json: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 1: python.json contains 'Python Class' snippet entry (0.4 points)
    # This fails on initial_env (no python.json) and passes on golden_env
    try:
        has_python_class = isinstance(snippets, dict) and 'Python Class' in snippets
        has_valid_entry = has_python_class and isinstance(snippets.get('Python Class'), dict)
        if has_valid_entry:
            print(f"PASS: Component 1 — python.json contains 'Python Class' dict entry (0.4 pts)")
            total_score += 0.4
        elif has_python_class:
            print(f"FAIL: Component 1 — 'Python Class' entry is not a dict, got: {type(snippets.get('Python Class'))}")
        else:
            keys_found = list(snippets.keys()) if isinstance(snippets, dict) else type(snippets)
            print(f"FAIL: Component 1 — 'Python Class' key not found in python.json. Keys found: {keys_found}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Snippet has prefix 'pyclass' and a description referencing class/__init__ (0.3 points)
    # This fails on initial_env (no python.json) and passes on golden_env
    try:
        snippet = snippets.get('Python Class', {}) if isinstance(snippets, dict) else {}
        prefix = snippet.get('prefix', '') if isinstance(snippet, dict) else ''
        description = snippet.get('description', '') if isinstance(snippet, dict) else ''

        prefix_ok = (prefix == 'pyclass')
        description_ok = ('__init__' in description.lower() or 'class' in description.lower())

        if prefix_ok and description_ok:
            print(f"PASS: Component 2 — prefix='{prefix}', description='{description}' (0.3 pts)")
            total_score += 0.3
        else:
            if not prefix_ok:
                print(f"FAIL: Component 2 — expected prefix 'pyclass', found '{prefix}'")
            if not description_ok:
                print(f"FAIL: Component 2 — description should reference class or __init__, found '{description}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Body contains __init__ method with type hint placeholders and class tab stop (0.3 points)
    # This fails on initial_env (no python.json) and passes on golden_env
    try:
        snippet = snippets.get('Python Class', {}) if isinstance(snippets, dict) else {}
        body = snippet.get('body', []) if isinstance(snippet, dict) else []

        if not isinstance(body, list) or len(body) == 0:
            print(f"FAIL: Component 3 — body is missing or empty: {body}")
        else:
            body_text = '\n'.join(body)

            # Check for __init__ method definition
            has_init = '__init__' in body_text
            # Check for type hint placeholder — ${N:type} pattern indicating type annotation
            has_type_hint = bool(re.search(r'\$\{\d+:type\}', body_text))
            # Check for -> None return type annotation
            has_return_type = '-> None' in body_text
            # Check for class definition with tab stop (e.g., class ${1:ClassName}:)
            has_class_def = bool(re.search(r'class\s+\$\{', body_text))

            all_checks_pass = has_init and has_type_hint and has_return_type and has_class_def
            if all_checks_pass:
                print(f"PASS: Component 3 — body has __init__, type hint '{{N:type}}', '-> None', and 'class ${{' tab stop (0.3 pts)")
                total_score += 0.3
            else:
                if not has_init:
                    print(f"FAIL: Component 3 — body does not contain '__init__'")
                if not has_type_hint:
                    print(f"FAIL: Component 3 — body does not contain type hint placeholder (e.g., ${{4:type}})")
                if not has_return_type:
                    print(f"FAIL: Component 3 — body does not contain '-> None' return type annotation")
                if not has_class_def:
                    print(f"FAIL: Component 3 — body does not contain class definition with tab stop (e.g., 'class ${{1:ClassName}}:')")
                print(f"  Body content: {body}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
