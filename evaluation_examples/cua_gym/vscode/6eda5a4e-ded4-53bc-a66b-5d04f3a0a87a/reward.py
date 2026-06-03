"""
Reward Script: JSDoc-driven type system for JavaScript project
Task ID: vscode_gf3_077
Domain: vscode
Scoring:
  - Component 1: @ts-check directive at top of client.js (0.10)
  - Component 2: @typedef ApiResponse with properties (0.20)
  - Component 3: @typedef User with properties (0.20)
  - Component 4: @typedef PaginatedResult with properties (0.15)
  - Component 5: @template generic on fetchPaginated (0.10)
  - Component 6: Return types reference custom typedefs (0.10)
  - Component 7: jsconfig.json exists with checkJs + strict (0.15)
"""

import os
import re
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_077'

CLIENT_JS = os.path.join(WORKDIR, 'projects', 'js-app', 'src', 'api', 'client.js')
JSCONFIG = os.path.join(WORKDIR, 'projects', 'js-app', 'jsconfig.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load client.js content
    try:
        with open(CLIENT_JS, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot load file {CLIENT_JS}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: @ts-check directive at the top of the file (0.10 points)
    # The very first non-empty line should be // @ts-check
    try:
        lines = content.split('\n')
        first_non_empty = ''
        for line in lines:
            if line.strip():
                first_non_empty = line.strip()
                break
        if first_non_empty == '// @ts-check':
            print(f"PASS: Component 1 — @ts-check found at top of file (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — Expected '// @ts-check' at top, found: '{first_non_empty}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: @typedef ApiResponse with required properties (0.20 points)
    try:
        # Check for @typedef {Object} ApiResponse
        has_typedef = bool(re.search(r'@typedef\s+\{Object\}\s+ApiResponse', content))
        if not has_typedef:
            # Also accept @typedef {object} ApiResponse (lowercase)
            has_typedef = bool(re.search(r'@typedef\s+\{object\}\s+ApiResponse', content, re.IGNORECASE))

        # Check for required properties in ApiResponse typedef block
        # Extract the JSDoc block containing ApiResponse typedef
        api_response_block = ''
        blocks = re.findall(r'/\*\*[\s\S]*?\*/', content)
        for block in blocks:
            if '@typedef' in block and 'ApiResponse' in block:
                api_response_block = block
                break

        required_props = ['success', 'data', 'statusCode']
        found_props = []
        for prop in required_props:
            if re.search(r'@property\s+\{[^}]+\}\s+(\[?' + prop + r'\b)', api_response_block):
                found_props.append(prop)

        if has_typedef and len(found_props) == len(required_props):
            print(f"PASS: Component 2 — @typedef ApiResponse with properties {found_props} (0.20 pts)")
            total_score += 0.20
        elif has_typedef and len(found_props) > 0:
            partial = 0.10
            print(f"PARTIAL: Component 2 — ApiResponse typedef found but only {found_props}/{required_props} props ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — @typedef ApiResponse not found or no properties (typedef={has_typedef}, props={found_props})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: @typedef User with required properties (0.20 points)
    try:
        has_typedef = bool(re.search(r'@typedef\s+\{[Oo]bject\}\s+User\b', content))

        user_block = ''
        for block in blocks:
            if '@typedef' in block and re.search(r'\bUser\b', block) and 'fetchUser' not in block:
                user_block = block
                break

        required_props = ['id', 'name', 'email', 'role']
        found_props = []
        for prop in required_props:
            if re.search(r'@property\s+\{[^}]+\}\s+(\[?' + prop + r'\b)', user_block):
                found_props.append(prop)

        if has_typedef and len(found_props) == len(required_props):
            print(f"PASS: Component 3 — @typedef User with properties {found_props} (0.20 pts)")
            total_score += 0.20
        elif has_typedef and len(found_props) > 0:
            partial = 0.10
            print(f"PARTIAL: Component 3 — User typedef found but only {found_props}/{required_props} props ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — @typedef User not found or no properties (typedef={has_typedef}, props={found_props})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: @typedef PaginatedResult with required properties (0.15 points)
    try:
        has_typedef = bool(re.search(r'@typedef\s+\{[Oo]bject\}\s+PaginatedResult', content))

        paginated_block = ''
        for block in blocks:
            if '@typedef' in block and 'PaginatedResult' in block:
                paginated_block = block
                break

        required_props = ['items', 'totalCount', 'currentPage', 'totalPages', 'hasNextPage']
        found_props = []
        for prop in required_props:
            if re.search(r'@property\s+\{[^}]+\}\s+(\[?' + prop + r'\b)', paginated_block):
                found_props.append(prop)

        if has_typedef and len(found_props) >= 4:
            print(f"PASS: Component 4 — @typedef PaginatedResult with properties {found_props} (0.15 pts)")
            total_score += 0.15
        elif has_typedef and len(found_props) > 0:
            partial = 0.07
            print(f"PARTIAL: Component 4 — PaginatedResult typedef found but only {found_props}/{required_props} props ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — @typedef PaginatedResult not found or no properties (typedef={has_typedef}, props={found_props})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: @template generic on fetchPaginated function (0.10 points)
    try:
        # Find the JSDoc block that precedes fetchPaginated
        fetch_pag_pattern = re.search(r'(/\*\*[\s\S]*?\*/)\s*\n\s*async\s+function\s+fetchPaginated', content)
        if fetch_pag_pattern:
            fp_block = fetch_pag_pattern.group(1)
            if '@template' in fp_block:
                print(f"PASS: Component 5 — @template found on fetchPaginated (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — fetchPaginated JSDoc block lacks @template")
        else:
            print(f"FAIL: Component 5 — Could not find JSDoc block for fetchPaginated")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Return types reference custom typedefs (ApiResponse, User, PaginatedResult) (0.10 points)
    # Check that at least some functions use the new types in @returns
    try:
        custom_returns = 0
        # Check for @returns with ApiResponse
        if re.search(r'@returns\s+\{[^}]*ApiResponse[^}]*\}', content):
            custom_returns += 1
        # Check for @returns with User
        if re.search(r'@returns\s+\{[^}]*User[^}]*\}', content):
            custom_returns += 1
        # Check for @returns with PaginatedResult
        if re.search(r'@returns\s+\{[^}]*PaginatedResult[^}]*\}', content):
            custom_returns += 1

        if custom_returns >= 2:
            print(f"PASS: Component 6 — {custom_returns} functions use custom return types (0.10 pts)")
            total_score += 0.10
        elif custom_returns >= 1:
            partial = 0.05
            print(f"PARTIAL: Component 6 — Only {custom_returns} functions use custom return types ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 6 — No functions reference custom types in @returns")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: jsconfig.json exists with checkJs and strict enabled (0.15 points)
    try:
        if not os.path.exists(JSCONFIG):
            print(f"FAIL: Component 7 — jsconfig.json not found at {JSCONFIG}")
        else:
            with open(JSCONFIG, 'r') as f:
                jsconfig = json.load(f)

            compiler_opts = jsconfig.get('compilerOptions', {})
            has_check_js = compiler_opts.get('checkJs') is True
            has_strict = compiler_opts.get('strict') is True

            if has_check_js and has_strict:
                print(f"PASS: Component 7 — jsconfig.json has checkJs=true and strict=true (0.15 pts)")
                total_score += 0.15
            elif has_check_js or has_strict:
                partial = 0.07
                print(f"PARTIAL: Component 7 — jsconfig.json: checkJs={has_check_js}, strict={has_strict} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 7 — jsconfig.json missing checkJs and strict (checkJs={has_check_js}, strict={has_strict})")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
