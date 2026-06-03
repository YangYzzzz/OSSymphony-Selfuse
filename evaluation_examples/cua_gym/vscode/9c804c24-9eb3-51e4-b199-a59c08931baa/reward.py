"""
Reward Script: Configure Playwright test runner in VSCode project
Task ID: vscode_gf5_030
Domain: vscode
Scoring:
  Component 1: @playwright/test in devDependencies (0.20)
  Component 2: playwright.config.ts with 3 browser projects (0.35)
  Component 3: tests/app.spec.ts with title check (0.25)
  Component 4: Headless mode configured (0.10)
  Component 5: Test script in package.json (0.10)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'e2e-tests')


def verify_task():
    """
    Verify Playwright test runner configuration.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: @playwright/test in devDependencies (0.20 points)
    try:
        pkg_path = os.path.join(PROJECT_DIR, 'package.json')
        with open(pkg_path, 'r') as f:
            pkg = json.load(f)
        dev_deps = pkg.get('devDependencies', {})
        if '@playwright/test' in dev_deps:
            print(f"PASS: Component 1 — @playwright/test found in devDependencies: {dev_deps['@playwright/test']} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — @playwright/test not in devDependencies. Found keys: {list(dev_deps.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: playwright.config.ts exists with 3 browser projects (0.35 points)
    try:
        config_path = os.path.join(PROJECT_DIR, 'playwright.config.ts')
        if not os.path.exists(config_path):
            print(f"FAIL: Component 2 — playwright.config.ts not found at {config_path}")
        else:
            with open(config_path, 'r') as f:
                config_content = f.read()

            # Check for all three browser projects
            required_browsers = ['chromium', 'firefox', 'webkit']
            found_browsers = []
            for browser in required_browsers:
                if re.search(r"name\s*:\s*['\"]" + browser + r"['\"]", config_content):
                    found_browsers.append(browser)

            if len(found_browsers) == 3:
                print(f"PASS: Component 2 — playwright.config.ts has all 3 browser projects: {found_browsers} (0.35 pts)")
                total_score += 0.35
            else:
                missing = set(required_browsers) - set(found_browsers)
                print(f"FAIL: Component 2 — Missing browser projects: {missing}. Found: {found_browsers}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: tests/app.spec.ts with title check (0.25 points)
    try:
        test_path = os.path.join(PROJECT_DIR, 'tests', 'app.spec.ts')
        if not os.path.exists(test_path):
            print(f"FAIL: Component 3 — tests/app.spec.ts not found")
        else:
            with open(test_path, 'r') as f:
                test_content = f.read()

            # Check for essential test elements:
            # 1. imports from @playwright/test
            has_import = bool(re.search(r"from\s+['\"]@playwright/test['\"]", test_content))
            # 2. visits localhost:3000
            has_goto = bool(re.search(r"goto\s*\(\s*['\"]http://localhost:3000", test_content) or
                           re.search(r"goto\s*\(\s*['\"/]", test_content))
            # 3. checks page title containing 'My App'
            has_title_check = bool(re.search(r"(toHaveTitle|title)", test_content, re.IGNORECASE) and
                                   re.search(r"My\s*App", test_content))

            checks_passed = sum([has_import, has_goto, has_title_check])
            if checks_passed == 3:
                print(f"PASS: Component 3 — tests/app.spec.ts has import, goto, and title check (0.25 pts)")
                total_score += 0.25
            elif checks_passed >= 2:
                partial = 0.15
                print(f"PARTIAL: Component 3 — {checks_passed}/3 checks passed (import={has_import}, goto={has_goto}, title={has_title_check}) ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — import={has_import}, goto={has_goto}, title_check={has_title_check}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Headless mode configured in playwright.config.ts (0.10 points)
    try:
        config_path = os.path.join(PROJECT_DIR, 'playwright.config.ts')
        if not os.path.exists(config_path):
            print(f"FAIL: Component 4 — playwright.config.ts not found")
        else:
            with open(config_path, 'r') as f:
                config_content = f.read()

            # Check for headless: true in the config
            if re.search(r"headless\s*:\s*true", config_content):
                print(f"PASS: Component 4 — headless: true configured (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — headless: true not found in playwright.config.ts")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Test script in package.json (0.10 points)
    try:
        pkg_path = os.path.join(PROJECT_DIR, 'package.json')
        with open(pkg_path, 'r') as f:
            pkg = json.load(f)
        scripts = pkg.get('scripts', {})
        test_script = scripts.get('test', '')
        if 'playwright' in test_script:
            print(f"PASS: Component 5 — test script references playwright: '{test_script}' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — test script does not reference playwright. scripts: {scripts}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
