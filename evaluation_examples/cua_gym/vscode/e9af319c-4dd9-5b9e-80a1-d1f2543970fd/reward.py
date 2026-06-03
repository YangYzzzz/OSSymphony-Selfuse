"""
Reward Script: Extract selected code into a new method called 'buildQueryString'
Task ID: vscode_rrt_051
Domain: vscode
Scoring:
  Component 1 (0.3): buildQueryString method exists in the class
  Component 2 (0.3): buildQueryString has correct signature and contains extraction logic
  Component 3 (0.2): search method calls this.buildQueryString(params)
  Component 4 (0.2): Inline query string building removed from search method
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_051'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'api', 'ApiClient.ts')


def verify_task(file_path):
    """
    Verify that the query string building code was extracted into a
    new method called 'buildQueryString' in the TypeScript class.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: buildQueryString method exists in the class (0.3 points)
    # Check that a method named buildQueryString is defined within the class
    try:
        # Match method definition: buildQueryString with any access modifier
        method_pattern = r'(?:private\s+|public\s+|protected\s+)?buildQueryString\s*\('
        method_match = re.search(method_pattern, content)
        if method_match:
            print(f"PASS: Component 1 — buildQueryString method found (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — buildQueryString method not found in class")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: buildQueryString has correct signature and contains the extracted logic (0.3 points)
    # Should accept params: Record<string, string>, return string, and contain the query building logic
    try:
        # Check for proper signature with params parameter and string return type
        sig_pattern = r'buildQueryString\s*\(\s*params\s*:\s*Record\s*<\s*string\s*,\s*string\s*>\s*\)\s*:\s*string'
        sig_match = re.search(sig_pattern, content)

        # Extract the buildQueryString method body to check it contains the logic
        # Find the method and its body
        method_body_pattern = r'buildQueryString\s*\([^)]*\)[^{]*\{([\s\S]*?)^\s{4}\}'
        method_body_match = re.search(method_body_pattern, content, re.MULTILINE)

        has_sig = sig_match is not None
        has_logic = False
        if method_body_match:
            body = method_body_match.group(1)
            # The extracted method should contain the query string building logic:
            # - parts array, for loop with encodeURIComponent, join('&')
            has_parts = 'parts' in body
            has_encode = 'encodeURIComponent' in body
            has_join = "join('&')" in body or 'join("&")' in body or "join(`&`)" in body
            has_logic = has_parts and has_encode and has_join

        if has_sig and has_logic:
            print(f"PASS: Component 2 — correct signature and contains extraction logic (0.3 pts)")
            total_score += 0.3
        elif has_sig:
            print(f"PARTIAL: Component 2 — signature correct but logic incomplete (0.15 pts)")
            total_score += 0.15
        elif has_logic:
            print(f"PARTIAL: Component 2 — logic present but signature wrong (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — signature: {has_sig}, logic: {has_logic}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: search method calls this.buildQueryString(params) (0.2 points)
    # The search method should delegate to the new method
    try:
        # Find the search method body
        search_pattern = r'async\s+search\s*\([^)]*\)\s*\{([\s\S]*?)^\s{4}\}'
        search_match = re.search(search_pattern, content, re.MULTILINE)

        if search_match:
            search_body = search_match.group(1)
            # Check for this.buildQueryString call
            call_pattern = r'this\.buildQueryString\s*\(\s*params\s*\)'
            if re.search(call_pattern, search_body):
                print(f"PASS: Component 3 — search calls this.buildQueryString(params) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — search does not call this.buildQueryString(params)")
                print(f"  search body: {search_body.strip()}")
        else:
            print(f"FAIL: Component 3 — search method not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Inline query string building removed from search method (0.2 points)
    # The search method should no longer contain the for loop, parts array, etc.
    try:
        if search_match:
            search_body = search_match.group(1)
            # These patterns should NOT be in search anymore (they were extracted)
            has_inline_parts = 'parts' in search_body
            has_inline_loop = 'for' in search_body and 'Object.entries' in search_body
            has_inline_encode = 'encodeURIComponent' in search_body

            if not has_inline_parts and not has_inline_loop and not has_inline_encode:
                print(f"PASS: Component 4 — inline query string code removed from search (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 — search still contains inline query building code")
                print(f"  has_parts={has_inline_parts}, has_loop={has_inline_loop}, has_encode={has_inline_encode}")
        else:
            print(f"FAIL: Component 4 — search method not found (cannot check removal)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
