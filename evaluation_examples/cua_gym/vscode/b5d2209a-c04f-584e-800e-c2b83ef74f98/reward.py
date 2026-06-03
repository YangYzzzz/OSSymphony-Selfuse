"""
Reward Script: Create REST Client .http file with CRUD requests
Task ID: vscode_gf3_008
Domain: vscode
Scoring:
  - Component 1 (0.15): File exists at correct path
  - Component 2 (0.20): File-level variable @userId = 123
  - Component 3 (0.20): GET request to /api/users
  - Component 4 (0.25): POST request with JSON body
  - Component 5 (0.20): DELETE request using {{userId}} variable
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_008'

FILE_PATH = os.path.join(WORKDIR, 'projects', 'api-tests', 'users.http')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not content.strip():
        print("CRITICAL: File is empty")
        print("REWARD: 0.0")
        return 0.0

    # Split content into sections by '###' separator
    # The '###' separator is used to delimit requests in REST Client format
    sections = re.split(r'^\s*###\s*.*$', content, flags=re.MULTILINE)

    print(f"INFO: File has {len(content)} chars, {len(sections)} sections (split by ###)")

    # Component 1: File-level variable @userId = 123 (0.20 points)
    # This must be defined at the top of the file
    try:
        # Check for @userId = 123 pattern (allowing flexible spacing)
        userId_pattern = re.search(r'@userId\s*=\s*123', content)
        if userId_pattern:
            print(f"PASS: Component 1 — @userId = 123 variable found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — @userId = 123 variable not found in file")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: GET request to http://localhost:3000/api/users (0.20 points)
    try:
        get_pattern = re.search(r'GET\s+http://localhost:3000/api/users\b', content)
        if get_pattern:
            print(f"PASS: Component 2 — GET request to /api/users found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — GET request to http://localhost:3000/api/users not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: POST request with JSON body (0.25 points)
    # Must have POST to /api/users, Content-Type header, and a JSON body
    try:
        post_match = re.search(r'POST\s+http://localhost:3000/api/users\b', content)
        post_found = post_match is not None
        has_content_type = False
        has_json_body = False

        if post_found:
            # Extract the POST section (from POST line to next ### or end)
            rest_after_post = content[post_match.start():]
            next_sep = re.search(r'^\s*###', rest_after_post[1:], flags=re.MULTILINE)
            post_section = rest_after_post[:next_sep.start() + 1] if next_sep else rest_after_post

            has_content_type = bool(re.search(r'Content-Type\s*:\s*application/json', post_section, re.IGNORECASE))
            has_json_body = bool(re.search(r'\{[^}]*\}', post_section, re.DOTALL))

        partial = 0.0
        if post_found:
            partial += 0.10
        if has_content_type:
            partial += 0.075
        if has_json_body:
            partial += 0.075

        if post_found and has_content_type and has_json_body:
            print(f"PASS: Component 3 — POST request with Content-Type and JSON body (0.25 pts)")
            total_score += 0.25
        elif partial > 0:
            print(f"PARTIAL: Component 3 — POST: {post_found}, Content-Type: {has_content_type}, JSON body: {has_json_body} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — POST request to http://localhost:3000/api/users not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: DELETE request using {{userId}} variable (0.20 points)
    try:
        # Must have DELETE to /api/users/{{userId}} (or with the variable reference)
        delete_pattern = re.search(r'DELETE\s+http://localhost:3000/api/users/\{\{userId\}\}', content)
        if delete_pattern:
            print(f"PASS: Component 4 — DELETE request with {{userId}} variable reference (0.20 pts)")
            total_score += 0.20
        else:
            # Check if DELETE exists at all but with wrong variable usage
            delete_any = re.search(r'DELETE\s+http://localhost:3000/api/users/', content)
            if delete_any:
                print(f"PARTIAL: Component 4 — DELETE request found but not using {{userId}} variable (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — DELETE request to /api/users/{{userId}} not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Three requests separated by ### (0.15 points)
    # Verify there are at least 3 ### separators and 3 distinct HTTP methods
    try:
        separator_count = len(re.findall(r'^\s*###', content, flags=re.MULTILINE))
        methods_found = set()
        if re.search(r'\bGET\s+http', content):
            methods_found.add('GET')
        if re.search(r'\bPOST\s+http', content):
            methods_found.add('POST')
        if re.search(r'\bDELETE\s+http', content):
            methods_found.add('DELETE')

        if separator_count >= 3 and len(methods_found) >= 3:
            print(f"PASS: Component 5 — {separator_count} separators, {len(methods_found)} methods: {methods_found} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — separators: {separator_count} (need >=3), methods: {methods_found} (need 3)")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

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
