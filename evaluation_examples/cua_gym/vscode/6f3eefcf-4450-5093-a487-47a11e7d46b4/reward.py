"""
Reward Script: Migrate Jest test suite to Vitest in a TypeScript project
Task ID: vscode_gf6_079
Domain: vscode
Scoring:
  Component 1 (0.25): package.json devDependencies — vitest present, jest absent
  Component 2 (0.20): package.json scripts — all 4 vitest-based scripts
  Component 3 (0.20): vitest.config.ts — exists with correct configuration
  Component 4 (0.20): Test file migrated — vi.* calls, no jest.* calls
  Component 5 (0.15): .vscode/settings.json — vitest settings present
"""

import os
import json
import re

WORKDIR = '/home/user/projects/ts-vitest'
TASK_ID = 'vscode_gf6_079'


def verify_task():
    """Verify Jest-to-Vitest migration with progressive scoring. Returns 0.0-1.0."""
    total_score = 0.0

    # ── Component 1: package.json devDependencies (0.25 pts) ──
    # vitest, @vitest/coverage-v8, @vitest/ui must be present; jest, ts-jest must be absent
    try:
        pkg_path = os.path.join(WORKDIR, 'package.json')
        with open(pkg_path, 'r') as f:
            pkg = json.load(f)

        dev_deps = pkg.get('devDependencies', {})
        has_vitest = 'vitest' in dev_deps
        has_coverage_v8 = '@vitest/coverage-v8' in dev_deps
        has_vitest_ui = '@vitest/ui' in dev_deps
        no_jest = 'jest' not in dev_deps
        no_ts_jest = 'ts-jest' not in dev_deps

        passed = sum([has_vitest, has_coverage_v8, has_vitest_ui, no_jest, no_ts_jest])
        if passed == 5:
            print(f"PASS: Component 1 — devDependencies correct: vitest pkgs present, jest pkgs absent (0.25 pts)")
            total_score += 0.25
        else:
            details = []
            if not has_vitest: details.append("missing vitest")
            if not has_coverage_v8: details.append("missing @vitest/coverage-v8")
            if not has_vitest_ui: details.append("missing @vitest/ui")
            if not no_jest: details.append("jest still present")
            if not no_ts_jest: details.append("ts-jest still present")
            # Partial: award proportionally
            partial = 0.25 * (passed / 5)
            total_score += partial
            print(f"PARTIAL: Component 1 — {passed}/5 checks: {', '.join(details)} ({partial:.3f} pts)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ── Component 2: package.json scripts (0.20 pts) ──
    # test: 'vitest run', test:watch: 'vitest', test:ui: 'vitest --ui', test:coverage: 'vitest run --coverage'
    try:
        scripts = pkg.get('scripts', {})
        expected_scripts = {
            'test': 'vitest run',
            'test:watch': 'vitest',
            'test:ui': 'vitest --ui',
            'test:coverage': 'vitest run --coverage',
        }
        matched = 0
        for key, expected_val in expected_scripts.items():
            actual_val = scripts.get(key, '')
            if actual_val.strip() == expected_val:
                matched += 1
            else:
                print(f"  DETAIL: script '{key}' expected '{expected_val}', found '{actual_val}'")

        if matched == 4:
            print(f"PASS: Component 2 — All 4 vitest scripts correct (0.20 pts)")
            total_score += 0.20
        elif matched > 0:
            partial = 0.20 * (matched / 4)
            total_score += partial
            print(f"PARTIAL: Component 2 — {matched}/4 scripts correct ({partial:.3f} pts)")
        else:
            print(f"FAIL: Component 2 — No vitest scripts found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ── Component 3: vitest.config.ts exists with correct config (0.20 pts) ──
    # Must have: test.environment='node', test.coverage.provider='v8',
    # test.coverage.thresholds with lines:80, branches:80
    try:
        config_path = os.path.join(WORKDIR, 'vitest.config.ts')
        if not os.path.exists(config_path):
            print(f"FAIL: Component 3 — vitest.config.ts does not exist")
        else:
            with open(config_path, 'r') as f:
                config_content = f.read()

            checks_passed = 0
            total_checks = 4

            # Check environment: 'node'
            if re.search(r"""environment\s*:\s*['"]node['"]""", config_content):
                checks_passed += 1
            else:
                print(f"  DETAIL: environment:'node' not found in vitest.config.ts")

            # Check coverage.provider: 'v8'
            if re.search(r"""provider\s*:\s*['"]v8['"]""", config_content):
                checks_passed += 1
            else:
                print(f"  DETAIL: coverage.provider:'v8' not found in vitest.config.ts")

            # Check thresholds lines: 80
            if re.search(r'lines\s*:\s*80', config_content):
                checks_passed += 1
            else:
                print(f"  DETAIL: thresholds.lines:80 not found in vitest.config.ts")

            # Check thresholds branches: 80
            if re.search(r'branches\s*:\s*80', config_content):
                checks_passed += 1
            else:
                print(f"  DETAIL: thresholds.branches:80 not found in vitest.config.ts")

            if checks_passed == total_checks:
                print(f"PASS: Component 3 — vitest.config.ts has all required config (0.20 pts)")
                total_score += 0.20
            elif checks_passed > 0:
                partial = 0.20 * (checks_passed / total_checks)
                total_score += partial
                print(f"PARTIAL: Component 3 — {checks_passed}/{total_checks} config checks ({partial:.3f} pts)")
            else:
                print(f"FAIL: Component 3 — vitest.config.ts missing all required config")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ── Component 4: Test file migrated (0.20 pts) ──
    # vi.fn(), vi.mock(), vi.spyOn() present; no jest.fn(), jest.mock(), jest.spyOn()
    try:
        test_path = os.path.join(WORKDIR, 'tests', '__tests__', 'userService.test.ts')
        if not os.path.exists(test_path):
            print(f"FAIL: Component 4 — test file not found at {test_path}")
        else:
            with open(test_path, 'r') as f:
                test_content = f.read()

            checks_passed = 0
            total_checks = 4

            # vi.fn() should be present
            if 'vi.fn()' in test_content:
                checks_passed += 1
            else:
                print(f"  DETAIL: vi.fn() not found in test file")

            # vi.restoreAllMocks() should be present
            if 'vi.restoreAllMocks()' in test_content:
                checks_passed += 1
            else:
                print(f"  DETAIL: vi.restoreAllMocks() not found in test file")

            # jest.fn() should NOT be present
            if 'jest.fn()' not in test_content and 'jest.mock(' not in test_content and 'jest.spyOn(' not in test_content:
                checks_passed += 1
            else:
                print(f"  DETAIL: jest.fn()/jest.mock()/jest.spyOn() still present in test file")

            # jest.restoreAllMocks() should NOT be present
            if 'jest.restoreAllMocks()' not in test_content:
                checks_passed += 1
            else:
                print(f"  DETAIL: jest.restoreAllMocks() still present in test file")

            if checks_passed == total_checks:
                print(f"PASS: Component 4 — Test file fully migrated to vitest (0.20 pts)")
                total_score += 0.20
            elif checks_passed > 0:
                partial = 0.20 * (checks_passed / total_checks)
                total_score += partial
                print(f"PARTIAL: Component 4 — {checks_passed}/{total_checks} migration checks ({partial:.3f} pts)")
            else:
                print(f"FAIL: Component 4 — Test file not migrated")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ── Component 5: .vscode/settings.json vitest settings (0.15 pts) ──
    # Must contain vitest-specific settings (e.g., vitest.enable, vitest.commandLine)
    try:
        settings_path = os.path.join(WORKDIR, '.vscode', 'settings.json')
        if not os.path.exists(settings_path):
            print(f"FAIL: Component 5 — .vscode/settings.json not found")
        else:
            with open(settings_path, 'r') as f:
                content = f.read()
            # Strip JSONC comments
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            settings = json.loads(content_clean)

            # Check for any vitest-related setting key
            vitest_keys = [k for k in settings.keys() if 'vitest' in k.lower()]
            if len(vitest_keys) >= 1:
                print(f"PASS: Component 5 — .vscode/settings.json has vitest settings: {vitest_keys} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — No vitest-related settings found. Keys: {list(settings.keys())}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(WORKDIR):
    print(f"Project directory not found: {WORKDIR}")
    print("REWARD: 0.0")
else:
    verify_task()
