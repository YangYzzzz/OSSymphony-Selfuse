"""
Reward Script: Virtual DOM Library Implementation in TypeScript
Task ID: vscode_gf4_084
Domain: vscode
Scoring:
  - Component 1: package.json with required deps (0.10)
  - Component 2: src/vdom.ts with VNode type and createElement (0.15)
  - Component 3: src/diff.ts with Patch types and diff function (0.15)
  - Component 4: src/patch.ts with applyPatch (0.10)
  - Component 5: src/component.ts with Component class + lifecycle (0.15)
  - Component 6: jest.config.js / tsconfig.json configured (0.05)
  - Component 7: Test file with >= 25 tests (0.10)
  - Component 8: npm test passes all tests (0.20)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'ts-virtual-dom')


def verify_task():
    total_score = 0.0

    # Component 1: package.json has required devDependencies (0.10 points)
    try:
        pkg_path = os.path.join(PROJECT, 'package.json')
        with open(pkg_path, 'r') as f:
            pkg = json.load(f)

        required_deps = ['typescript', 'jest', '@types/jest', 'ts-jest']
        dev_deps = pkg.get('devDependencies', {})
        all_deps = {**pkg.get('dependencies', {}), **dev_deps}

        found = [d for d in required_deps if d in all_deps]
        if len(found) == len(required_deps):
            # Also verify test script exists
            scripts = pkg.get('scripts', {})
            if 'test' in scripts and 'jest' in scripts['test']:
                print(f"PASS: Component 1 — package.json has all required deps and test script (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 1 — package.json missing 'test' script with jest")
        else:
            missing = [d for d in required_deps if d not in all_deps]
            print(f"FAIL: Component 1 — package.json missing deps: {missing}")
    except FileNotFoundError:
        print(f"FAIL: Component 1 — package.json not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: src/vdom.ts with VNode type and createElement (0.15 points)
    try:
        vdom_path = os.path.join(PROJECT, 'src', 'vdom.ts')
        with open(vdom_path, 'r') as f:
            content = f.read()

        checks = {
            'VNode type with tag': bool(re.search(r'(interface|type)\s+VNode', content) and 'tag' in content and 'props' in content and 'children' in content),
            'key optional field': bool(re.search(r'key\s*\?\s*:', content)),
            'createElement function': bool(re.search(r'(function|const)\s+createElement', content) or 'createElement' in content),
        }
        passed = sum(1 for v in checks.values() if v)
        if passed == len(checks):
            print(f"PASS: Component 2 — src/vdom.ts has VNode type and createElement (0.15 pts)")
            total_score += 0.15
        else:
            failed = [k for k, v in checks.items() if not v]
            print(f"FAIL: Component 2 — src/vdom.ts missing: {failed}")
    except FileNotFoundError:
        print(f"FAIL: Component 2 — src/vdom.ts not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: src/diff.ts with Patch types and diff function (0.15 points)
    try:
        diff_path = os.path.join(PROJECT, 'src', 'diff.ts')
        with open(diff_path, 'r') as f:
            content = f.read()

        patch_types = ['CREATE', 'REMOVE', 'REPLACE', 'UPDATE_PROPS', 'REORDER']
        found_types = [pt for pt in patch_types if pt in content]
        has_diff_func = bool(re.search(r'(function|const|export\s+function)\s+diff', content))

        if len(found_types) == len(patch_types) and has_diff_func:
            print(f"PASS: Component 3 — src/diff.ts has all Patch types and diff function (0.15 pts)")
            total_score += 0.15
        else:
            missing_types = [pt for pt in patch_types if pt not in content]
            issues = []
            if missing_types:
                issues.append(f"missing patch types: {missing_types}")
            if not has_diff_func:
                issues.append("missing diff function")
            print(f"FAIL: Component 3 — src/diff.ts issues: {', '.join(issues)}")
    except FileNotFoundError:
        print(f"FAIL: Component 3 — src/diff.ts not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: src/patch.ts with applyPatch function (0.10 points)
    try:
        patch_path = os.path.join(PROJECT, 'src', 'patch.ts')
        with open(patch_path, 'r') as f:
            content = f.read()

        has_apply = bool(re.search(r'(function|const|export\s+function)\s+applyPatch', content))
        # Should also manipulate DOM
        has_dom_ops = any(kw in content for kw in ['createElement', 'appendChild', 'removeChild', 'replaceChild', 'setAttribute'])

        if has_apply and has_dom_ops:
            print(f"PASS: Component 4 — src/patch.ts has applyPatch with DOM operations (0.10 pts)")
            total_score += 0.10
        else:
            issues = []
            if not has_apply:
                issues.append("missing applyPatch function")
            if not has_dom_ops:
                issues.append("no DOM manipulation detected")
            print(f"FAIL: Component 4 — src/patch.ts issues: {', '.join(issues)}")
    except FileNotFoundError:
        print(f"FAIL: Component 4 — src/patch.ts not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: src/component.ts with Component class + lifecycle (0.15 points)
    try:
        comp_path = os.path.join(PROJECT, 'src', 'component.ts')
        with open(comp_path, 'r') as f:
            content = f.read()

        has_class = bool(re.search(r'class\s+Component', content))
        has_state = 'setState' in content
        lifecycle_methods = ['mount', 'update', 'unmount']
        found_lifecycle = [m for m in lifecycle_methods if m.lower() in content.lower()]

        if has_class and has_state and len(found_lifecycle) == len(lifecycle_methods):
            print(f"PASS: Component 5 — src/component.ts has Component class with state and lifecycle (0.15 pts)")
            total_score += 0.15
        else:
            issues = []
            if not has_class:
                issues.append("missing Component class")
            if not has_state:
                issues.append("missing setState")
            missing = [m for m in lifecycle_methods if m.lower() not in content.lower()]
            if missing:
                issues.append(f"missing lifecycle methods: {missing}")
            print(f"FAIL: Component 5 — src/component.ts issues: {', '.join(issues)}")
    except FileNotFoundError:
        print(f"FAIL: Component 5 — src/component.ts not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: jest.config and tsconfig configured properly (0.05 points)
    try:
        jest_path = os.path.join(PROJECT, 'jest.config.js')
        ts_path = os.path.join(PROJECT, 'tsconfig.json')

        jest_exists = os.path.exists(jest_path)
        ts_exists = os.path.exists(ts_path)

        if jest_exists and ts_exists:
            with open(jest_path, 'r') as f:
                jest_content = f.read()
            with open(ts_path, 'r') as f:
                ts_content = f.read()

            has_jsdom = 'jsdom' in jest_content
            has_ts_jest = 'ts-jest' in jest_content
            has_ts_config = 'compilerOptions' in ts_content

            if has_jsdom and has_ts_jest and has_ts_config:
                print(f"PASS: Component 6 — jest.config.js and tsconfig.json properly configured (0.05 pts)")
                total_score += 0.05
            else:
                issues = []
                if not has_jsdom:
                    issues.append("jest.config missing jsdom")
                if not has_ts_jest:
                    issues.append("jest.config missing ts-jest")
                if not has_ts_config:
                    issues.append("tsconfig missing compilerOptions")
                print(f"FAIL: Component 6 — config issues: {', '.join(issues)}")
        else:
            missing = []
            if not jest_exists:
                missing.append("jest.config.js")
            if not ts_exists:
                missing.append("tsconfig.json")
            print(f"FAIL: Component 6 — missing config files: {missing}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: Test file with >= 25 tests (0.10 points)
    try:
        # Look for test files
        tests_dir = os.path.join(PROJECT, '__tests__')
        test_files = []
        if os.path.isdir(tests_dir):
            for fn in os.listdir(tests_dir):
                if fn.endswith('.test.ts') or fn.endswith('.spec.ts'):
                    test_files.append(os.path.join(tests_dir, fn))

        # Also check src directory for co-located tests
        src_dir = os.path.join(PROJECT, 'src')
        if os.path.isdir(src_dir):
            for fn in os.listdir(src_dir):
                if fn.endswith('.test.ts') or fn.endswith('.spec.ts'):
                    test_files.append(os.path.join(src_dir, fn))

        # Also check project root
        for fn in os.listdir(PROJECT):
            fp = os.path.join(PROJECT, fn)
            if os.path.isfile(fp) and (fn.endswith('.test.ts') or fn.endswith('.spec.ts')):
                test_files.append(fp)

        if not test_files:
            print(f"FAIL: Component 7 — no test files found")
        else:
            total_tests = 0
            for tf in test_files:
                with open(tf, 'r') as f:
                    tc = f.read()
                # Count test() and it() calls
                test_count = len(re.findall(r'\b(?:test|it)\s*\(', tc))
                total_tests += test_count

            if total_tests >= 25:
                print(f"PASS: Component 7 — found {total_tests} tests (>= 25 required) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 7 — found only {total_tests} tests, need >= 25")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    # Component 8: npm test passes (0.20 points)
    try:
        # Run npm test using os.popen (no subprocess import needed)
        node_bin = '/home/user/.nvm/versions/node/v18.20.8/bin'
        if os.path.isdir(node_bin):
            env_path = f"{node_bin}:{os.environ.get('PATH', '/usr/bin:/bin')}"
            result = os.popen(
                f'cd {PROJECT} && PATH={env_path} npm test 2>&1'
            ).read()

            # Parse test results
            if 'Tests:' in result:
                match = re.search(r'Tests:\s+(\d+)\s+passed', result)
                fail_match = re.search(r'(\d+)\s+failed', result)
                if match:
                    passed_count = int(match.group(1))
                    failed_count = int(fail_match.group(1)) if fail_match else 0
                    if failed_count == 0 and passed_count >= 25:
                        print(f"PASS: Component 8 — npm test: {passed_count} tests passed, 0 failed (0.20 pts)")
                        total_score += 0.20
                    elif failed_count == 0 and passed_count > 0:
                        # Partial credit: some tests pass but < 25
                        partial = 0.20 * (passed_count / 25.0)
                        partial = min(partial, 0.15)  # Cap at 0.15 for incomplete
                        print(f"PARTIAL: Component 8 — npm test: {passed_count}/{25} tests passed ({partial:.2f} pts)")
                        total_score += partial
                    else:
                        print(f"FAIL: Component 8 — npm test: {passed_count} passed, {failed_count} failed")
                else:
                    print(f"FAIL: Component 8 — could not parse test results")
                    # Check if there was an error
                    if 'FAIL' in result or 'Error' in result:
                        print(f"  Test output snippet: {result[-500:]}")
            else:
                print(f"FAIL: Component 8 — npm test did not produce results")
                print(f"  Output snippet: {result[-300:]}")
        else:
            # Try alternative node paths
            jest_bin = os.path.join(PROJECT, 'node_modules', '.bin', 'jest')
            if os.path.exists(jest_bin):
                print(f"FAIL: Component 8 — node binary not found at expected path, cannot run tests")
            else:
                print(f"FAIL: Component 8 — node_modules/.bin/jest not found, dependencies not installed")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isdir(PROJECT):
    print(f"Project directory not found: {PROJECT}")
    print("REWARD: 0.0")
else:
    verify_task()
