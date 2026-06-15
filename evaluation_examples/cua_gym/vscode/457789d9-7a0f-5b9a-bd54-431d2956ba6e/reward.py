"""
Reward Script: Playwright accessibility testing suite creation
Task ID: vscode_gf3_071
Domain: vscode
Scoring:
  Component 1 (0.20): homepage.spec.ts file exists at correct path
  Component 2 (0.30): homepage.spec.ts imports and uses @axe-core/playwright correctly
  Component 3 (0.15): homepage.spec.ts writes violations to a11y-report.json
  Component 4 (0.15): homepage.spec.ts asserts violations array is empty
  Component 5 (0.10): @axe-core/playwright added to package.json devDependencies
  Component 6 (0.10): Playwright config has 'accessibility' project matching tests/accessibility/**
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_071'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'webapp')
SPEC_PATH = os.path.join(PROJECT_DIR, 'tests', 'accessibility', 'homepage.spec.ts')
PACKAGE_JSON_PATH = os.path.join(PROJECT_DIR, 'package.json')
PLAYWRIGHT_CONFIG_TS = os.path.join(PROJECT_DIR, 'playwright.config.ts')
PLAYWRIGHT_CONFIG_JS = os.path.join(PROJECT_DIR, 'playwright.config.js')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: homepage.spec.ts exists at the correct path (0.20 points)
    # This file does NOT exist in initial_env, only in golden_env
    try:
        if os.path.isfile(SPEC_PATH):
            with open(SPEC_PATH, 'r') as f:
                spec_content = f.read()
            if len(spec_content.strip()) > 50:
                print(f"PASS: Component 1 — homepage.spec.ts exists at {SPEC_PATH} ({len(spec_content)} bytes) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 — homepage.spec.ts exists but is too small ({len(spec_content)} bytes)")
                spec_content = ""
        else:
            print(f"FAIL: Component 1 — homepage.spec.ts not found at {SPEC_PATH}")
            spec_content = ""
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        spec_content = ""

    # Component 2: Imports and uses @axe-core/playwright (0.30 points)
    # The test must import AxeBuilder from @axe-core/playwright and call .analyze()
    try:
        if spec_content:
            has_axe_import = bool(re.search(r"(import|require).*['\"]@axe-core/playwright['\"]", spec_content))
            has_analyze_call = bool(re.search(r'\.analyze\(\)', spec_content))
            has_axe_builder = bool(re.search(r'AxeBuilder|axeBuilder|new\s+\w+\(\s*\{\s*page', spec_content))

            sub_score = 0.0
            if has_axe_import:
                sub_score += 0.15
                print(f"  PASS: Component 2a — imports @axe-core/playwright")
            else:
                print(f"  FAIL: Component 2a — missing import of @axe-core/playwright")

            if has_analyze_call and has_axe_builder:
                sub_score += 0.15
                print(f"  PASS: Component 2b — uses AxeBuilder and calls .analyze()")
            elif has_analyze_call or has_axe_builder:
                sub_score += 0.075
                print(f"  PARTIAL: Component 2b — has AxeBuilder={has_axe_builder}, analyze={has_analyze_call}")
            else:
                print(f"  FAIL: Component 2b — no AxeBuilder usage or .analyze() call found")

            if sub_score > 0:
                print(f"PASS: Component 2 — axe-core integration verified ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 2 — no axe-core integration found")
        else:
            print(f"FAIL: Component 2 — spec file not available")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Custom reporter writes violations to a11y-report.json (0.15 points)
    # The spec must reference 'a11y-report.json' and write to it
    try:
        if spec_content:
            has_report_path = bool(re.search(r'a11y-report\.json', spec_content))
            has_write_operation = bool(re.search(r'(writeFile|writeFileSync|fs\.write)', spec_content))
            has_json_stringify = bool(re.search(r'JSON\.stringify', spec_content))

            if has_report_path and has_write_operation and has_json_stringify:
                print(f"PASS: Component 3 — writes violations to a11y-report.json with JSON.stringify (0.15 pts)")
                total_score += 0.15
            elif has_report_path and (has_write_operation or has_json_stringify):
                print(f"PARTIAL: Component 3 — a11y-report.json referenced but incomplete write logic (0.075 pts)")
                total_score += 0.075
            else:
                print(f"FAIL: Component 3 — no custom reporter writing to a11y-report.json (path={has_report_path}, write={has_write_operation}, stringify={has_json_stringify})")
        else:
            print(f"FAIL: Component 3 — spec file not available")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Asserts violations array is empty (0.15 points)
    # The test must assert that violations is empty (expect(...violations...).toEqual([]) or similar)
    try:
        if spec_content:
            # Check for assertion on violations being empty
            has_violations_check = bool(re.search(
                r'(expect.*violations.*\.(toEqual|toHaveLength|toBe|toStrictEqual)\s*\(\s*(\[\s*\]|0)\s*\)|'
                r'assert.*violations.*(\.|length|===)\s*(0|\[\s*\])|'
                r'violations\s*\.\s*length\s*===?\s*0)',
                spec_content
            ))

            if has_violations_check:
                print(f"PASS: Component 4 — asserts violations array is empty (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — no assertion found checking violations is empty")
        else:
            print(f"FAIL: Component 4 — spec file not available")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: @axe-core/playwright in package.json devDependencies (0.10 points)
    # This dependency is NOT in initial_env's package.json
    try:
        if os.path.isfile(PACKAGE_JSON_PATH):
            with open(PACKAGE_JSON_PATH, 'r') as f:
                pkg = json.load(f)
            dev_deps = pkg.get('devDependencies', {})
            if '@axe-core/playwright' in dev_deps:
                print(f"PASS: Component 5 — @axe-core/playwright in devDependencies: {dev_deps['@axe-core/playwright']} (0.10 pts)")
                total_score += 0.10
            else:
                # Also check regular dependencies
                deps = pkg.get('dependencies', {})
                if '@axe-core/playwright' in deps:
                    print(f"PASS: Component 5 — @axe-core/playwright in dependencies: {deps['@axe-core/playwright']} (0.10 pts)")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 5 — @axe-core/playwright not found in package.json")
        else:
            print(f"FAIL: Component 5 — package.json not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Playwright config has 'accessibility' project matching tests/accessibility/** (0.10 points)
    # Initial config has only chromium and firefox projects
    try:
        config_path = None
        config_content = ""
        for p in [PLAYWRIGHT_CONFIG_TS, PLAYWRIGHT_CONFIG_JS]:
            if os.path.isfile(p):
                config_path = p
                with open(p, 'r') as f:
                    config_content = f.read()
                break

        if config_content:
            # Check for project named 'accessibility'
            has_accessibility_project = bool(re.search(r"name:\s*['\"]accessibility['\"]", config_content))
            # Check for testMatch referencing tests/accessibility/**
            has_test_match = bool(re.search(r"testMatch.*accessibility", config_content))

            if has_accessibility_project and has_test_match:
                print(f"PASS: Component 6 — playwright config has 'accessibility' project with correct testMatch (0.10 pts)")
                total_score += 0.10
            elif has_accessibility_project:
                print(f"PARTIAL: Component 6 — 'accessibility' project exists but testMatch may be wrong (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 6 — no 'accessibility' project found in playwright config")
        else:
            print(f"FAIL: Component 6 — playwright config not found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
