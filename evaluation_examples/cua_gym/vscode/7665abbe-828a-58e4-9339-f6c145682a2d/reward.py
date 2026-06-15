"""
Reward Script: Inline variable 'baseUrl' in api.js
Task ID: vscode_rrt_035
Domain: vscode
Scoring:
  - Component 1 (0.3): baseUrl declaration removed
  - Component 2 (0.4): All fetch calls use literal URL (no ${baseUrl} references)
  - Component 3 (0.3): Three functions preserved with correct inlined URLs
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_035'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'client', 'api.js')

BASE_URL = 'https://api.example.com/v2'
EXPECTED_ENDPOINTS = ['users', 'products', 'orders']


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load file content
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    lines = content.strip().split('\n')

    # Component 1: baseUrl declaration is removed (0.3 points)
    # Check that no line declares baseUrl as a const/let/var
    try:
        has_declaration = False
        for line in lines:
            stripped = line.strip()
            if re.match(r'^(const|let|var)\s+baseUrl\s*=', stripped):
                has_declaration = True
                break
        if not has_declaration:
            print(f"PASS: Component 1 — baseUrl declaration not found (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — baseUrl declaration still present")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: No ${baseUrl} template literal references remain (0.4 points)
    # This checks that all usages have been replaced
    try:
        baseurl_refs = re.findall(r'\$\{baseUrl\}', content)
        plain_refs = re.findall(r'\bbaseUrl\b', content)
        if len(plain_refs) == 0:
            print(f"PASS: Component 2 — No references to baseUrl found (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — Found {len(plain_refs)} reference(s) to baseUrl: template={len(baseurl_refs)}, total={len(plain_refs)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Three functions preserved with correct inlined URLs (0.3 points)
    # Each function should contain fetch('https://api.example.com/v2/<endpoint>')
    try:
        matches_found = 0
        for endpoint in EXPECTED_ENDPOINTS:
            expected_url = f"{BASE_URL}/{endpoint}"
            # Accept both single-quoted and double-quoted, and template literal forms
            # The key is the literal URL string is present
            patterns = [
                re.escape(f"fetch('{expected_url}')"),
                re.escape(f'fetch("{expected_url}")'),
                re.escape(f"fetch(`{expected_url}`)"),
            ]
            found = False
            for pat in patterns:
                if re.search(pat, content):
                    found = True
                    break
            if found:
                matches_found += 1
                print(f"  Found inlined URL for /{endpoint}")
            else:
                print(f"  Missing inlined URL for /{endpoint}")

        if matches_found == len(EXPECTED_ENDPOINTS):
            print(f"PASS: Component 3 — All {len(EXPECTED_ENDPOINTS)} functions have correct inlined URLs (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Only {matches_found}/{len(EXPECTED_ENDPOINTS)} functions have correct inlined URLs")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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
