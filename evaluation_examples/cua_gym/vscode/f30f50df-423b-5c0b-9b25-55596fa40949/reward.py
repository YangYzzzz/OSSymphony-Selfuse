"""
Reward Script: Create a user snippet for JavaScript that generates a console.log statement.
Task ID: vscode_code_014
Domain: vs_code
Scoring:
  Component 1: A snippet with prefix 'clog' exists in javascript.json  (0.5 pts)
  Component 2: Snippet body contains 'console.log($1);'                 (0.3 pts)
  Component 3: Snippet has a non-empty description field                (0.2 pts)
  Total: 1.0

Note: The javascript.json file itself is a precondition gate, not a scoring component.
      If it does not exist, score is 0.0 (no partial credit for file existence alone).
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_014'
SNIPPET_PATH = '/home/user/.config/Code/User/snippets/javascript.json'


def verify_task(snippet_path):
    """
    Verify task completion with progressive scoring.

    The task requires:
    1. A javascript.json file exists at ~/.config/Code/User/snippets/javascript.json
    2. The file contains a snippet entry with prefix 'clog'
    3. That snippet body includes 'console.log($1);' (cursor inside parentheses)
    4. That snippet has a non-empty description

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: javascript.json must exist and be parseable
    # File existence itself is not scored -- it is a gate for the real checks below
    if not os.path.exists(snippet_path):
        print(f"FAIL: javascript.json not found at {snippet_path}")
        print(f"\nScore: 0.0/1.0")
        print(f"REWARD: 0.0")
        return 0.0

    try:
        with open(snippet_path, 'r') as f:
            content = f.read()
        # Strip JSONC comments (VSCode supports // comments in JSON files)
        content_stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        snippets = json.loads(content_stripped)
    except (json.JSONDecodeError, IOError) as e:
        print(f"CRITICAL: Cannot parse {snippet_path}: {e}")
        print(f"\nScore: 0.0/1.0")
        print(f"REWARD: 0.0")
        return 0.0

    # Component 1: File contains a snippet entry with prefix 'clog' (0.5 points)
    # This FAILS on initial_env (file is absent, gate returns 0.0) and PASSES on golden_env
    clog_snippet = None
    try:
        for snippet_name, snippet_data in snippets.items():
            if isinstance(snippet_data, dict):
                prefix = snippet_data.get('prefix', '')
                # prefix can be a string or a list of strings
                if isinstance(prefix, list):
                    if 'clog' in prefix:
                        clog_snippet = snippet_data
                        break
                elif isinstance(prefix, str):
                    if prefix == 'clog':
                        clog_snippet = snippet_data
                        break

        if clog_snippet is not None:
            print(f"PASS: Component 1 -- Found snippet with prefix 'clog' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 -- No snippet with prefix 'clog' found in {snippet_path}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Snippet body contains 'console.log($1);' (0.3 points)
    # This FAILS on initial_env (file absent, 0.0 already returned) and PASSES on golden_env
    try:
        if clog_snippet is not None:
            body = clog_snippet.get('body', [])
            # body can be a list of strings or a single string
            if isinstance(body, str):
                body_text = body
            elif isinstance(body, list):
                body_text = '\n'.join(body)
            else:
                body_text = ''

            # The task requires the body to produce a console.log statement with cursor inside
            # Expected: "console.log($1);" -- with $1 as the cursor/tabstop position
            if 'console.log(' in body_text and '$1' in body_text:
                print(f"PASS: Component 2 -- Body contains 'console.log($1);' (0.3 pts) -- body: {body}")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 -- Expected body with 'console.log($1);', found: {body}")
        else:
            print(f"FAIL: Component 2 -- Skipped (no 'clog' snippet found)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Snippet has a non-empty 'description' field (0.2 points)
    # This FAILS on initial_env (file absent, 0.0 already returned) and PASSES on golden_env
    try:
        if clog_snippet is not None:
            description = clog_snippet.get('description', '')
            if description and str(description).strip():
                print(f"PASS: Component 3 -- Snippet has description: '{description}' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 -- Snippet 'description' field is missing or empty")
        else:
            print(f"FAIL: Component 3 -- Skipped (no 'clog' snippet found)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification against the canonical snippets path on the VM
verify_task(SNIPPET_PATH)
