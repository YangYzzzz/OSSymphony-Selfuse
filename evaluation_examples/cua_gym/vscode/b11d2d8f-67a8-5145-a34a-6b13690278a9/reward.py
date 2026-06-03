"""
Reward Script: Playwright testing infrastructure for a React app
Task ID: vscode_gf3_062
Domain: vscode
Scoring:
  Component 1 (0.15): playwright.config.ts exists
  Component 2 (0.10): config has chromium project
  Component 3 (0.10): config has mobile Chrome project with iPhone 13
  Component 4 (0.10): config has globalSetup pointing to global-setup
  Component 5 (0.05): config has baseURL set
  Component 6 (0.15): global-setup.ts exists with API auth
  Component 7 (0.10): global-setup.ts saves storageState to .auth/user.json
  Component 8 (0.15): dashboard.spec.ts exists
  Component 9 (0.10): dashboard.spec.ts uses storageState
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_062'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'react-app')

def verify_task():
    """
    Verify Playwright testing infrastructure setup.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- File 1: playwright.config.ts ---
    config_path = os.path.join(PROJECT_DIR, 'playwright.config.ts')
    config_content = None

    # Component 1: playwright.config.ts exists and is non-empty (0.15 points)
    try:
        if os.path.isfile(config_path):
            with open(config_path, 'r') as f:
                config_content = f.read()
            if len(config_content.strip()) > 50:
                print(f"PASS: Component 1 — playwright.config.ts exists ({len(config_content)} chars) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — playwright.config.ts is too small ({len(config_content)} chars)")
        else:
            print(f"FAIL: Component 1 — playwright.config.ts not found at {config_path}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if config_content:
        # Component 2: config has chromium project (0.10 points)
        try:
            # Look for a project named 'chromium' or using Desktop Chrome device
            has_chromium = bool(
                re.search(r"""name\s*:\s*['"]chromium['"]""", config_content) or
                re.search(r"""devices\s*\[\s*['"]Desktop Chrome['"]\s*\]""", config_content)
            )
            if has_chromium:
                print(f"PASS: Component 2 — chromium project found in config (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 2 — no chromium project found in config")
        except Exception as e:
            print(f"ERROR: Component 2 — {e}")

        # Component 3: config has mobile Chrome project with iPhone 13 (0.10 points)
        try:
            has_mobile = bool(
                re.search(r"""['"]Mobile Chrome['"]""", config_content, re.IGNORECASE) or
                re.search(r"""['"]mobile\s*chrome['"]""", config_content, re.IGNORECASE)
            )
            has_iphone13 = bool(
                re.search(r"""iPhone\s*13""", config_content)
            )
            if has_mobile and has_iphone13:
                print(f"PASS: Component 3 — Mobile Chrome project with iPhone 13 found (0.10 pts)")
                total_score += 0.10
            elif has_iphone13:
                # iPhone 13 device implies mobile testing even without explicit name
                print(f"PASS: Component 3 — iPhone 13 device config found (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — no mobile Chrome/iPhone 13 project (mobile={has_mobile}, iphone13={has_iphone13})")
        except Exception as e:
            print(f"ERROR: Component 3 — {e}")

        # Component 4: config has globalSetup pointing to global-setup (0.10 points)
        try:
            has_global_setup = bool(
                re.search(r"""globalSetup\s*:\s*['"].*global-setup""", config_content)
            )
            if has_global_setup:
                print(f"PASS: Component 4 — globalSetup configured (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — globalSetup not found in config")
        except Exception as e:
            print(f"ERROR: Component 4 — {e}")

        # Component 5: config has baseURL (0.05 points)
        try:
            has_base_url = bool(
                re.search(r"""baseURL\s*:\s*['"]""", config_content)
            )
            if has_base_url:
                print(f"PASS: Component 5 — baseURL configured (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 5 — baseURL not found in config")
        except Exception as e:
            print(f"ERROR: Component 5 — {e}")

    # --- File 2: playwright/global-setup.ts ---
    global_setup_path = os.path.join(PROJECT_DIR, 'playwright', 'global-setup.ts')
    gs_content = None

    # Component 6: global-setup.ts exists with API authentication (0.15 points)
    try:
        if os.path.isfile(global_setup_path):
            with open(global_setup_path, 'r') as f:
                gs_content = f.read()
            # Must contain API-based auth (post/login/auth keywords)
            has_api_auth = bool(
                re.search(r"""(\.post\s*\(|fetch\s*\(|request\.)""", gs_content) and
                re.search(r"""(login|auth|authenticate)""", gs_content, re.IGNORECASE)
            )
            if has_api_auth and len(gs_content.strip()) > 50:
                print(f"PASS: Component 6 — global-setup.ts with API auth found (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 6 — global-setup.ts exists but missing API auth (api_auth={has_api_auth})")
        else:
            print(f"FAIL: Component 6 — global-setup.ts not found at {global_setup_path}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: global-setup.ts saves storageState to .auth/user.json (0.10 points)
    try:
        if gs_content:
            has_storage_state_save = bool(
                re.search(r"""storageState""", gs_content)
            )
            has_auth_user_json = bool(
                re.search(r"""\.auth/user\.json""", gs_content) or
                re.search(r"""auth.*user\.json""", gs_content)
            )
            if has_storage_state_save and has_auth_user_json:
                print(f"PASS: Component 7 — storageState saved to .auth/user.json (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 7 — storageState save missing (storageState={has_storage_state_save}, auth_user_json={has_auth_user_json})")
        else:
            print(f"FAIL: Component 7 — global-setup.ts not available")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    # --- File 3: playwright/tests/dashboard.spec.ts ---
    spec_path = os.path.join(PROJECT_DIR, 'playwright', 'tests', 'dashboard.spec.ts')
    spec_content = None

    # Component 8: dashboard.spec.ts exists and is a valid test file (0.15 points)
    try:
        if os.path.isfile(spec_path):
            with open(spec_path, 'r') as f:
                spec_content = f.read()
            has_test = bool(
                re.search(r"""(test\s*\(|test\.describe|it\s*\()""", spec_content)
            )
            if has_test and len(spec_content.strip()) > 50:
                print(f"PASS: Component 8 — dashboard.spec.ts with tests found (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 8 — dashboard.spec.ts exists but no tests found (has_test={has_test})")
        else:
            print(f"FAIL: Component 8 — dashboard.spec.ts not found at {spec_path}")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

    # Component 9: dashboard.spec.ts uses storageState for auth (0.10 points)
    try:
        if spec_content:
            has_storage_state_use = bool(
                re.search(r"""storageState""", spec_content)
            )
            if has_storage_state_use:
                print(f"PASS: Component 9 — storageState used in test file (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 9 — storageState not referenced in dashboard.spec.ts")
        else:
            print(f"FAIL: Component 9 — dashboard.spec.ts not available")
    except Exception as e:
        print(f"ERROR: Component 9 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
