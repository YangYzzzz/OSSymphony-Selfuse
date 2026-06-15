"""
Reward Script: Playwright test with comprehensive network mocking
Task ID: vscode_gf3_085
Domain: vscode
Scoring: 6 components checking file content for required Playwright patterns
  - Component 1 (0.20): page.route() intercepts /api/** with abort/fail for offline sim
  - Component 2 (0.15): Verifies offline banner visibility
  - Component 3 (0.15): Uses page.unroute() to restore connectivity
  - Component 4 (0.15): Clicks retry button
  - Component 5 (0.20): Mocks successful API response with route.fulfill()
  - Component 6 (0.15): Verifies data loads correctly after reconnection
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_085'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'webapp', 'tests', 'offline-behavior.spec.ts')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist (gate, no points)
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must be a non-trivial TypeScript/Playwright test file
    if len(content.strip()) < 100:
        print(f"CRITICAL: File is too short ({len(content)} chars), not a real test")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must import from @playwright/test
    if '@playwright/test' not in content:
        print("CRITICAL: Not a Playwright test file (missing @playwright/test import)")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Uses page.route() to intercept /api/** with abort/fail for offline simulation (0.20 pts)
    try:
        # Must have page.route with an api pattern AND an abort('failed') or abort('connectionrefused')
        has_route_api = bool(re.search(r'page\.route\s*\(\s*[\'"`].*api.*[\'"`]', content))
        has_abort = bool(re.search(r'route\.abort\s*\(\s*[\'"`](failed|connectionrefused)[\'"`]\s*\)', content))
        if has_route_api and has_abort:
            print(f"PASS: Component 1 — page.route() intercepts API calls with abort (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — route API interception: has_route_api={has_route_api}, has_abort={has_abort}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Verifies offline banner visibility (0.15 pts)
    try:
        has_offline_banner_locator = bool(re.search(r'(offline[-_]?banner|offline)', content, re.IGNORECASE))
        has_visibility_check = bool(re.search(r'toBeVisible\s*\(\s*\)', content))
        # Must check that something related to "offline" is visible
        has_offline_visible = bool(re.search(
            r'offline.*toBeVisible|toBeVisible.*offline|offline.*banner',
            content, re.IGNORECASE | re.DOTALL
        ))
        if has_offline_banner_locator and has_visibility_check and has_offline_visible:
            print(f"PASS: Component 2 — Verifies offline banner visibility (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — offline banner check: locator={has_offline_banner_locator}, visible={has_visibility_check}, combined={has_offline_visible}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Uses page.unroute() to restore connectivity (0.15 pts)
    try:
        has_unroute = bool(re.search(r'page\.unroute\s*\(', content))
        if has_unroute:
            print(f"PASS: Component 3 — Uses page.unroute() to restore connectivity (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — page.unroute() not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Clicks retry button (0.15 pts)
    try:
        has_retry_locator = bool(re.search(r'retry', content, re.IGNORECASE))
        has_click = bool(re.search(r'\.click\s*\(\s*\)', content))
        # Must have a retry-related element that gets clicked
        has_retry_click = bool(re.search(r'retry.*\.click|click.*retry', content, re.IGNORECASE | re.DOTALL))
        if has_retry_locator and has_click and has_retry_click:
            print(f"PASS: Component 4 — Clicks retry button (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — retry button click: locator={has_retry_locator}, click={has_click}, combined={has_retry_click}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Mocks successful API response with route.fulfill() (0.20 pts)
    try:
        has_fulfill = bool(re.search(r'route\.fulfill\s*\(', content))
        has_status_200 = bool(re.search(r'status\s*:\s*200', content))
        has_json_body = bool(re.search(r'(body|json)\s*:', content))
        if has_fulfill and has_status_200 and has_json_body:
            print(f"PASS: Component 5 — Mocks successful API response with route.fulfill() (0.20 pts)")
            total_score += 0.20
        elif has_fulfill and has_json_body:
            # Partial: has fulfill with body but no explicit 200 (default is 200)
            print(f"PARTIAL: Component 5 — route.fulfill() found with body but no explicit status:200 (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — mock response: fulfill={has_fulfill}, status200={has_status_200}, json_body={has_json_body}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Verifies data loads correctly after reconnection (0.15 pts)
    try:
        # After reconnection, must verify some data/dashboard element is visible or has content
        # AND verify the offline banner is gone (not visible)
        has_not_visible = bool(re.search(r'not\.toBeVisible\s*\(\s*\)', content))
        # Check for data verification: dashboard, table, stat, orders, etc.
        has_data_verify = bool(re.search(
            r'(dashboard|table|stat|orders|data|content).*toBeVisible|toHaveCount|toContainText',
            content, re.IGNORECASE | re.DOTALL
        ))
        if has_not_visible and has_data_verify:
            print(f"PASS: Component 6 — Verifies data loads after reconnection (0.15 pts)")
            total_score += 0.15
        elif has_not_visible or has_data_verify:
            print(f"PARTIAL: Component 6 — partial reconnection verification: not_visible={has_not_visible}, data_verify={has_data_verify} (0.07 pts)")
            total_score += 0.07
        else:
            print(f"FAIL: Component 6 — reconnection verification: not_visible={has_not_visible}, data_verify={has_data_verify}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

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
