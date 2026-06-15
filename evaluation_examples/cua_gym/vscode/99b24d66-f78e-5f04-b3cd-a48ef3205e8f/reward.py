"""
Reward Script: Verify custom VSCode Python snippet for class template
Task ID: vscode_stu_064
Domain: vscode
Scoring:
  Component 1 (0.20): python.json snippet file exists and is valid JSON
  Component 2 (0.30): A snippet entry with prefix 'myclass' exists
  Component 3 (0.25): The snippet body contains __init__ method definition
  Component 4 (0.25): The snippet body contains __repr__ method definition
"""

import os
import json
import re

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SNIPPETS_DIR = os.path.join(VSCODE_USER, "snippets")
PYTHON_SNIPPETS = os.path.join(SNIPPETS_DIR, "python.json")

TASK_ID = "vscode_stu_064"


def strip_jsonc_comments(text):
    """Strip // and /* */ comments from JSONC content."""
    text = re.sub(r'//.*?$', '', text, flags=re.MULTILINE)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    return text


def load_python_snippets():
    """Load python.json snippet file, handling JSONC comments."""
    with open(PYTHON_SNIPPETS, "r") as f:
        content = f.read()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        cleaned = strip_jsonc_comments(content)
        return json.loads(cleaned)


def find_snippet_by_prefix(snippets, target_prefix):
    """Find a snippet entry whose prefix matches target_prefix."""
    for name, snippet in snippets.items():
        prefix = snippet.get("prefix", "")
        # prefix can be a string or a list of strings
        if isinstance(prefix, list):
            if target_prefix in prefix:
                return name, snippet
        elif isinstance(prefix, str):
            if prefix == target_prefix:
                return name, snippet
    return None, None


def body_contains_method(body, method_name):
    """Check if the snippet body list contains a def <method_name> line."""
    if isinstance(body, list):
        joined = "\n".join(body)
    elif isinstance(body, str):
        joined = body
    else:
        return False
    # Match 'def __init__' or 'def __repr__' allowing for tabstops/placeholders
    pattern = rf'def\s+{re.escape(method_name)}\s*\('
    return bool(re.search(pattern, joined))


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: python.json exists and is valid JSON (0.20 points)
    snippets = None
    try:
        if os.path.isfile(PYTHON_SNIPPETS):
            snippets = load_python_snippets()
            if isinstance(snippets, dict):
                print(f"PASS: Component 1 -- python.json exists and is valid JSON with {len(snippets)} snippet(s) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 -- python.json is not a JSON object, got {type(snippets).__name__}")
        else:
            print(f"FAIL: Component 1 -- python.json not found at {PYTHON_SNIPPETS}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    if snippets is None or not isinstance(snippets, dict):
        # Cannot proceed without valid snippets
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: A snippet with prefix 'myclass' exists (0.30 points)
    snippet_name = None
    snippet_data = None
    try:
        snippet_name, snippet_data = find_snippet_by_prefix(snippets, "myclass")
        if snippet_data is not None:
            print(f"PASS: Component 2 -- Found snippet '{snippet_name}' with prefix 'myclass' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 -- No snippet with prefix 'myclass' found. Available prefixes: {[s.get('prefix') for s in snippets.values()]}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    if snippet_data is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    body = snippet_data.get("body", [])

    # Component 3: Body contains __init__ method (0.25 points)
    try:
        if body_contains_method(body, "__init__"):
            print(f"PASS: Component 3 -- Snippet body contains __init__ method definition (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- Snippet body does not contain 'def __init__('. Body: {body}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Body contains __repr__ method (0.25 points)
    try:
        if body_contains_method(body, "__repr__"):
            print(f"PASS: Component 4 -- Snippet body contains __repr__ method definition (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 -- Snippet body does not contain 'def __repr__('. Body: {body}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
