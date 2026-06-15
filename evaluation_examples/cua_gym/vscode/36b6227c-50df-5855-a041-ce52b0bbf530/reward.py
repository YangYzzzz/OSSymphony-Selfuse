"""
Reward Script: Create a C/C++ snippet for header guard pattern
Task ID: vscode_lang_094
Domain: vscode
Scoring:
  - Component 1: c.json snippet file exists and is valid JSON (0.15)
  - Component 2: Snippet named "Header Guard" with prefix "hguard" (0.25)
  - Component 3: Body contains #ifndef and #define with uppercase TM_FILENAME_BASE (0.35)
  - Component 4: Body contains #endif closing guard (0.10)
  - Component 5: Body uses proper variable transform for uppercase (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_094'

# Possible snippet file locations
SNIPPET_PATHS = [
    os.path.join(WORKDIR, '.config', 'Code', 'User', 'snippets', 'c.json'),
    os.path.join(WORKDIR, '.config', 'Code', 'User', 'snippets', 'cpp.json'),
]


def find_snippet_file():
    """Find the C/C++ snippet file in known locations."""
    for path in SNIPPET_PATHS:
        if os.path.exists(path):
            return path
    # Also check for .code-snippets files in user snippets dir
    snippets_dir = os.path.join(WORKDIR, '.config', 'Code', 'User', 'snippets')
    if os.path.isdir(snippets_dir):
        for fname in os.listdir(snippets_dir):
            if fname.endswith('.code-snippets'):
                return os.path.join(snippets_dir, fname)
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: c.json (or equivalent) snippet file exists and is valid JSON (0.15 points)
    snippet_path = find_snippet_file()
    snippets = None
    try:
        if snippet_path is None:
            print("FAIL: Component 1 -- No C/C++ snippet file found in user snippets directory")
        else:
            with open(snippet_path, 'r') as f:
                content = f.read()
            # Handle JSONC (strip comments)
            cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            snippets = json.loads(cleaned)
            if isinstance(snippets, dict) and len(snippets) > 0:
                print(f"PASS: Component 1 -- Snippet file found at {snippet_path} with {len(snippets)} snippet(s) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 -- Snippet file found but empty or not a dict")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 1 -- Snippet file found but invalid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    if snippets is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Snippet named "Header Guard" (or similar) with prefix "hguard" (0.25 points)
    try:
        # Find a snippet with header-guard-like name
        hguard_snippet = None
        for name, snippet in snippets.items():
            name_lower = name.lower()
            if 'header' in name_lower and 'guard' in name_lower:
                hguard_snippet = snippet
                break

        if hguard_snippet is None:
            # Fallback: check for any snippet with prefix "hguard"
            for name, snippet in snippets.items():
                if isinstance(snippet, dict) and snippet.get('prefix', '') == 'hguard':
                    hguard_snippet = snippet
                    break

        if hguard_snippet is not None:
            prefix = hguard_snippet.get('prefix', '')
            if prefix == 'hguard':
                print(f"PASS: Component 2 -- Found 'Header Guard' snippet with prefix 'hguard' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 -- Found header guard snippet but prefix is '{prefix}', expected 'hguard'")
        else:
            print(f"FAIL: Component 2 -- No header guard snippet found. Available: {list(snippets.keys())}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    if hguard_snippet is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Get body for remaining checks
    body = hguard_snippet.get('body', [])
    if isinstance(body, list):
        body_text = '\n'.join(str(line) for line in body)
    else:
        body_text = str(body)

    # Component 3: Body contains #ifndef and #define with TM_FILENAME_BASE uppercase (0.35 points)
    try:
        has_ifndef = '#ifndef' in body_text
        has_define = '#define' in body_text
        has_filename_base = 'TM_FILENAME_BASE' in body_text
        # Check for uppercase transform - various valid patterns
        has_upcase = ('upcase' in body_text.lower() or 'UPCASE' in body_text or
                      '/upcase/' in body_text or ':upcase' in body_text)

        if has_ifndef and has_define and has_filename_base and has_upcase:
            print(f"PASS: Component 3 -- Body has #ifndef, #define with TM_FILENAME_BASE uppercase transform (0.35 pts)")
            total_score += 0.35
        else:
            missing = []
            if not has_ifndef:
                missing.append('#ifndef')
            if not has_define:
                missing.append('#define')
            if not has_filename_base:
                missing.append('TM_FILENAME_BASE')
            if not has_upcase:
                missing.append('upcase transform')
            print(f"FAIL: Component 3 -- Body missing: {', '.join(missing)}")
            print(f"  Body text: {body_text[:300]}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Body contains #endif closing guard (0.10 points)
    try:
        if '#endif' in body_text:
            print(f"PASS: Component 4 -- Body contains #endif closing guard (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 -- Body missing #endif")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Body uses proper variable transform for uppercase (0.15 points)
    # The standard VSCode snippet transform: ${TM_FILENAME_BASE/(.*)/${1:/upcase}/}
    try:
        # Check for the proper transform pattern
        # Valid patterns: ${TM_FILENAME_BASE/(.*)/${1:/upcase}/} or similar regex transforms
        transform_pattern = re.search(
            r'\$\{TM_FILENAME_BASE/.*upcase.*\}',
            body_text,
            re.IGNORECASE
        )
        if transform_pattern:
            print(f"PASS: Component 5 -- Proper TM_FILENAME_BASE transform pattern found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 -- No proper transform pattern like ${{TM_FILENAME_BASE/(.*)/${{1:/upcase}}/}} found")
            print(f"  Body text: {body_text[:300]}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
