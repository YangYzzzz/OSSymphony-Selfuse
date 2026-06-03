"""
Reward Script: Create Cypress custom login command with TypeScript types
Task ID: vscode_gf3_050
Domain: vscode (file-based)
Scoring:
  Component 1 (0.10): commands.ts file exists at correct path
  Component 2 (0.20): TypeScript type declaration for login command
  Component 3 (0.30): Cypress.Commands.add with cy.request POST to /api/auth/login
  Component 4 (0.20): Token stored in localStorage AND cookie set
  Component 5 (0.20): e2e.ts imports ./commands
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_050'

COMMANDS_PATH = os.path.join(WORKDIR, 'projects', 'webapp', 'cypress', 'support', 'commands.ts')
E2E_PATH = os.path.join(WORKDIR, 'projects', 'webapp', 'cypress', 'support', 'e2e.ts')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: commands.ts file exists at the correct path (0.1 points)
    try:
        if os.path.isfile(COMMANDS_PATH):
            with open(COMMANDS_PATH, 'r') as f:
                commands_content = f.read()
            if len(commands_content.strip()) > 0:
                print(f"PASS: Component 1 — commands.ts exists at {COMMANDS_PATH} ({len(commands_content)} chars) (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 1 — commands.ts exists but is empty")
                commands_content = ""
        else:
            print(f"FAIL: Component 1 — commands.ts not found at {COMMANDS_PATH}")
            commands_content = ""
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        commands_content = ""

    # If commands.ts doesn't exist or is empty, remaining file-based checks will fail
    # but we still check e2e.ts (Component 5) independently

    # Component 2: TypeScript type declaration for the login custom command (0.2 points)
    # Must have: declare namespace Cypress, interface Chainable, login method with email+password params
    try:
        if commands_content:
            has_namespace = bool(re.search(r'declare\s+namespace\s+Cypress', commands_content))
            has_chainable = bool(re.search(r'interface\s+Chainable', commands_content))
            has_login_sig = bool(re.search(r'login\s*\(', commands_content))
            has_email_param = bool(re.search(r'email\s*:\s*string', commands_content))
            has_password_param = bool(re.search(r'password\s*:\s*string', commands_content))

            type_checks_passed = sum([has_namespace, has_chainable, has_login_sig, has_email_param, has_password_param])

            if type_checks_passed >= 4:
                print(f"PASS: Component 2 — TypeScript type declaration found (namespace={has_namespace}, chainable={has_chainable}, login_sig={has_login_sig}, email={has_email_param}, password={has_password_param}) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — Incomplete type declaration ({type_checks_passed}/5 checks: namespace={has_namespace}, chainable={has_chainable}, login_sig={has_login_sig}, email={has_email_param}, password={has_password_param})")
        else:
            print(f"FAIL: Component 2 — commands.ts not available")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Cypress.Commands.add('login', ...) with cy.request POST to /api/auth/login (0.3 points)
    try:
        if commands_content:
            has_commands_add = bool(re.search(r"Cypress\.Commands\.add\s*\(\s*['\"]login['\"]", commands_content))
            has_cy_request = bool(re.search(r"cy\.request\s*\(", commands_content))
            has_post_method = bool(re.search(r"['\"]POST['\"]", commands_content, re.IGNORECASE))
            has_login_url = bool(re.search(r"/api/auth/login", commands_content))

            req_checks = sum([has_commands_add, has_cy_request, has_post_method, has_login_url])

            if req_checks >= 3:
                print(f"PASS: Component 3 — Login command implementation found (add={has_commands_add}, request={has_cy_request}, POST={has_post_method}, url={has_login_url}) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Incomplete command implementation ({req_checks}/4: add={has_commands_add}, request={has_cy_request}, POST={has_post_method}, url={has_login_url})")
        else:
            print(f"FAIL: Component 3 — commands.ts not available")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Token stored in localStorage AND cookie set (0.2 points)
    try:
        if commands_content:
            has_localstorage = bool(re.search(r"localStorage\.setItem\s*\(", commands_content))
            has_cookie = bool(re.search(r"cy\.setCookie\s*\(", commands_content) or
                            re.search(r"setCookie\s*\(", commands_content) or
                            re.search(r"document\.cookie", commands_content))

            if has_localstorage and has_cookie:
                print(f"PASS: Component 4 — Token stored in localStorage and cookie set (0.2 pts)")
                total_score += 0.2
            elif has_localstorage:
                print(f"FAIL: Component 4 — localStorage set but no cookie found")
                total_score += 0.1  # partial: localStorage only
            elif has_cookie:
                print(f"FAIL: Component 4 — Cookie set but no localStorage found")
                total_score += 0.1  # partial: cookie only
            else:
                print(f"FAIL: Component 4 — Neither localStorage nor cookie handling found")
        else:
            print(f"FAIL: Component 4 — commands.ts not available")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: e2e.ts imports ./commands (0.2 points)
    try:
        if os.path.isfile(E2E_PATH):
            with open(E2E_PATH, 'r') as f:
                e2e_content = f.read()

            # Check for import of commands file
            has_import = bool(re.search(r"import\s+['\"]\.\/commands['\"]", e2e_content) or
                            re.search(r"import\s+['\"]\.\/commands\.ts['\"]", e2e_content) or
                            re.search(r"require\s*\(\s*['\"]\.\/commands", e2e_content) or
                            re.search(r"import\s+.*from\s+['\"]\.\/commands", e2e_content))

            if has_import:
                print(f"PASS: Component 5 — e2e.ts imports ./commands (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 5 — e2e.ts does not import ./commands. Content:\n{e2e_content[:200]}")
        else:
            print(f"FAIL: Component 5 — e2e.ts not found at {E2E_PATH}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
