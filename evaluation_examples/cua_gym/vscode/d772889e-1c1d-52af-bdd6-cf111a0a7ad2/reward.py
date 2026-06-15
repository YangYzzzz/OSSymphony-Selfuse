"""
Reward Script: Create REST Client .http file with named auth request and token variable extraction
Task ID: vscode_gf3_014
Domain: vscode
Scoring:
  - Component 1 (0.20): File exists and contains @name authRequest directive
  - Component 2 (0.20): POST request to http://localhost:4000/auth/token
  - Component 3 (0.10): Content-Type: application/json header in POST request
  - Component 4 (0.15): Request body with JSON credentials
  - Component 5 (0.15): GET request with Authorization header
  - Component 6 (0.20): Bearer token uses correct variable syntax {{authRequest.response.body.$.token}}
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_014'

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist (task creates this file; no points awarded for existence alone)
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

    content_lower = content.lower()

    # Component 1: @name authRequest directive (0.20 points)
    # The REST Client naming syntax uses "# @name <requestName>" or "@name <requestName>"
    try:
        # Match @name authRequest (case-sensitive for the variable name)
        has_name_directive = bool(re.search(r'@\s*name\s+authRequest', content))
        if has_name_directive:
            print(f"PASS: Component 1 — Found @name authRequest directive (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — @name authRequest directive not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: POST request to http://localhost:4000/auth/token (0.20 points)
    try:
        has_post = bool(re.search(r'POST\s+http://localhost:4000/auth/token', content, re.IGNORECASE))
        if has_post:
            print(f"PASS: Component 2 — Found POST http://localhost:4000/auth/token (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — POST to http://localhost:4000/auth/token not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Content-Type: application/json header (0.10 points)
    try:
        has_content_type = bool(re.search(r'content-type\s*:\s*application/json', content_lower))
        if has_content_type:
            print(f"PASS: Component 3 — Found Content-Type: application/json (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — Content-Type: application/json header not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: JSON request body with credentials (0.15 points)
    # Check that there's a JSON body block with username/password or similar credentials
    try:
        has_json_body = bool(re.search(r'\{[^}]*"(username|user|email)"', content))
        if has_json_body:
            print(f"PASS: Component 4 — Found JSON request body with credentials (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — JSON request body with credentials not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: GET request with Authorization header (0.15 points)
    try:
        has_get = bool(re.search(r'GET\s+http', content, re.IGNORECASE))
        has_auth_header = bool(re.search(r'authorization\s*:', content_lower))
        if has_get and has_auth_header:
            print(f"PASS: Component 5 — Found GET request with Authorization header (0.15 pts)")
            total_score += 0.15
        else:
            if not has_get:
                print(f"FAIL: Component 5 — GET request not found")
            if not has_auth_header:
                print(f"FAIL: Component 5 — Authorization header not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Bearer token with correct variable syntax (0.20 points)
    # Must use {{authRequest.response.body.$.token}} in the Authorization header
    try:
        # Look for the exact variable reference pattern
        has_bearer_token = bool(re.search(
            r'authorization\s*:\s*bearer\s+\{\{authRequest\.response\.body\.\$\.token\}\}',
            content,
            re.IGNORECASE
        ))
        if has_bearer_token:
            print(f"PASS: Component 6 — Found Bearer {{{{authRequest.response.body.$.token}}}} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 6 — Bearer token with correct variable syntax not found")
            # Check for partial match (variable reference without Bearer)
            if re.search(r'authRequest\.response\.body\.\$\.token', content):
                print(f"  NOTE: Found authRequest.response.body.$.token reference but not in correct Bearer format")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/projects/docs/api-reference.http'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
