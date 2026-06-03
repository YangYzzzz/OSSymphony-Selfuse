"""
Reward Script: Create a Python snippet in VSCode with prefix 'trylog' for try-except-finally with logging
Task ID: vscode_py_031
Domain: vs-code (snippets)
Scoring:
  Component 1 (0.2): python.json exists and is valid JSON with at least one snippet
  Component 2 (0.3): A snippet with prefix 'trylog' exists
  Component 3 (0.3): Snippet body contains try/except/finally structure
  Component 4 (0.2): Snippet body contains logging.exception() in the except block
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_031'
SNIPPET_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'snippets', 'python.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: python.json exists and is valid JSON with at least one snippet (0.2 points)
    snippets = None
    try:
        with open(SNIPPET_PATH, 'r') as f:
            content = f.read()
        # Handle JSONC (strip // comments)
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        snippets = json.loads(cleaned)
        if isinstance(snippets, dict) and len(snippets) > 0:
            print(f"PASS: Component 1 -- python.json exists, valid JSON with {len(snippets)} snippet(s) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- python.json exists but is empty or not a dict")
    except FileNotFoundError:
        print(f"FAIL: Component 1 -- python.json not found at {SNIPPET_PATH}")
    except (json.JSONDecodeError, Exception) as e:
        print(f"ERROR: Component 1 -- Could not parse python.json: {e}")

    if snippets is None or not isinstance(snippets, dict):
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: A snippet with prefix 'trylog' exists (0.3 points)
    trylog_snippet = None
    try:
        for name, snippet in snippets.items():
            prefix = snippet.get('prefix', '')
            # prefix can be a string or list of strings
            if isinstance(prefix, str) and prefix.lower() == 'trylog':
                trylog_snippet = snippet
                break
            elif isinstance(prefix, list):
                for p in prefix:
                    if isinstance(p, str) and p.lower() == 'trylog':
                        trylog_snippet = snippet
                        break
                if trylog_snippet:
                    break

        if trylog_snippet is not None:
            print(f"PASS: Component 2 -- Found snippet with prefix 'trylog' (0.3 pts)")
            total_score += 0.3
        else:
            prefixes = [s.get('prefix', '???') for s in snippets.values()]
            print(f"FAIL: Component 2 -- No snippet with prefix 'trylog'. Found prefixes: {prefixes}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    if trylog_snippet is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 3: Snippet body contains try/except/finally structure (0.3 points)
    try:
        body = trylog_snippet.get('body', [])
        if isinstance(body, str):
            body_text = body
        elif isinstance(body, list):
            body_text = '\n'.join(str(line) for line in body)
        else:
            body_text = str(body)

        has_try = bool(re.search(r'\btry\s*:', body_text))
        has_except = bool(re.search(r'\bexcept\b', body_text))
        has_finally = bool(re.search(r'\bfinally\s*:', body_text))

        if has_try and has_except and has_finally:
            print(f"PASS: Component 3 -- Body contains try/except/finally structure (0.3 pts)")
            total_score += 0.3
        else:
            missing = []
            if not has_try:
                missing.append('try')
            if not has_except:
                missing.append('except')
            if not has_finally:
                missing.append('finally')
            print(f"FAIL: Component 3 -- Missing keywords in body: {missing}")
            print(f"  Body text: {body_text[:200]}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Snippet body contains logging.exception() in the except block (0.2 points)
    try:
        body = trylog_snippet.get('body', [])
        if isinstance(body, str):
            body_text = body
        elif isinstance(body, list):
            body_text = '\n'.join(str(line) for line in body)
        else:
            body_text = str(body)

        # Check for logging.exception() call in the body
        has_logging_exception = bool(re.search(r'logging\.exception\s*\(', body_text))

        if has_logging_exception:
            print(f"PASS: Component 4 -- Body contains logging.exception() (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 -- No logging.exception() found in body")
            print(f"  Body text: {body_text[:200]}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
