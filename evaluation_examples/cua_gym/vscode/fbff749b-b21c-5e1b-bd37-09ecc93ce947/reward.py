"""
Reward Script: Set up a global user snippet with prefix 'header' for comment header block
Task ID: vscode_code_017
Domain: vs_code
Scoring:
  - Component 1: snippet file contains a snippet named 'File Header' with prefix 'header'
                 and a non-empty description (0.3 pts)
  - Component 2: Snippet body uses VSCode date variables:
                 CURRENT_YEAR, CURRENT_MONTH, CURRENT_DATE (0.4 pts)
  - Component 3: Snippet body uses TM_FILENAME variable for the filename (0.3 pts)
Total: 1.0

Note: File existence is used as a precondition gate only (not scored).
All scoring components check content that changes between initial_env and golden_env.
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_017'
SNIPPETS_FILE = os.path.join(WORKDIR, '.config', 'Code', 'User', 'snippets', 'my-global.code-snippets')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Precondition gate: file must exist and be parseable ---
    if not os.path.exists(SNIPPETS_FILE):
        print(f"PRECONDITION FAIL: Snippet file not found at {SNIPPETS_FILE}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    try:
        with open(SNIPPETS_FILE, 'r') as f:
            content = f.read()
        # Strip JSONC comments if present (VSCode snippet files may use // comments)
        content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        snippets = json.loads(content_clean)
    except Exception as e:
        print(f"PRECONDITION FAIL: Cannot parse snippet file {SNIPPETS_FILE}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Helper: find snippet with prefix 'header'
    def find_header_snippet(snippets_dict):
        """Return (name, data) for the first snippet with prefix 'header', or (None, None)."""
        match = next(
            ((name, data) for name, data in snippets_dict.items()
             if isinstance(data, dict) and data.get('prefix') == 'header'),
            None
        )
        if match is not None:
            return match
        return (None, None)

    # Component 1: Snippet has prefix 'header', a non-empty body, and a non-empty description (0.3 points)
    # FAILS on initial_env (file doesn't exist => precondition fails => 0.0 total)
    # PASSES on golden_env (file exists with correct structure)
    snippet_name = None
    snippet_data = None
    try:
        snippet_name, snippet_data = find_header_snippet(snippets)

        if snippet_name is not None:
            has_description = bool(snippet_data.get('description', '').strip())
            has_body = isinstance(snippet_data.get('body'), list) and len(snippet_data['body']) > 0

            if has_body and has_description:
                print(f"PASS: Component 1 — Snippet '{snippet_name}' has prefix 'header', "
                      f"description='{snippet_data.get('description')}', "
                      f"body with {len(snippet_data['body'])} lines (0.3 pts)")
                total_score += 0.3
            elif has_body:
                # Partial credit: has prefix+body but no description
                print(f"PARTIAL: Component 1 — Snippet '{snippet_name}' has prefix 'header' and body, "
                      f"but missing description (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — Snippet with prefix 'header' found but has invalid or empty body")
        else:
            print(f"FAIL: Component 1 — No snippet with prefix 'header' found. "
                  f"Found keys: {list(snippets.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Snippet body uses all three VSCode date variables (0.4 points)
    # CURRENT_YEAR, CURRENT_MONTH, CURRENT_DATE must all appear in the body
    # FAILS on initial_env (file doesn't exist => gate fails)
    # PASSES on golden_env (body contains all three date variables)
    try:
        if snippet_data is None:
            print(f"FAIL: Component 2 — Cannot check date variables; no 'header' snippet found")
        else:
            body = snippet_data.get('body', [])
            body_str = '\n'.join(body) if isinstance(body, list) else str(body)

            has_year = '${CURRENT_YEAR}' in body_str
            has_month = '${CURRENT_MONTH}' in body_str
            has_date = '${CURRENT_DATE}' in body_str

            date_vars = [
                ('${CURRENT_YEAR}', has_year),
                ('${CURRENT_MONTH}', has_month),
                ('${CURRENT_DATE}', has_date),
            ]
            present_count = sum(1 for _, v in date_vars if v)
            missing_vars = [name for name, v in date_vars if not v]

            if present_count == 3:
                print(f"PASS: Component 2 — Body contains all date variables "
                      f"(CURRENT_YEAR, CURRENT_MONTH, CURRENT_DATE) (0.4 pts)")
                total_score += 0.4
            elif present_count >= 1:
                partial = round(0.4 * present_count / 3, 2)
                print(f"PARTIAL: Component 2 — Body has {present_count}/3 date variables, "
                      f"missing: {missing_vars} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — Body missing all date variables: {missing_vars}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Snippet body uses TM_FILENAME variable for the filename (0.3 points)
    # FAILS on initial_env (file doesn't exist => gate fails)
    # PASSES on golden_env (body contains ${TM_FILENAME})
    try:
        if snippet_data is None:
            print(f"FAIL: Component 3 — Cannot check TM_FILENAME variable; no 'header' snippet found")
        else:
            body = snippet_data.get('body', [])
            body_str = '\n'.join(body) if isinstance(body, list) else str(body)

            if '${TM_FILENAME}' in body_str:
                print(f"PASS: Component 3 — Body contains ${{TM_FILENAME}} variable (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Body does not contain ${{TM_FILENAME}}. Body content: {body_str!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
