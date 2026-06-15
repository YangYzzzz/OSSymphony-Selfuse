"""
Reward Script: VSCode TypeScript Express API project setup
Task ID: vscode_gf4_018
Domain: vscode
Scoring:
  Component 1: package.json with correct dependencies (0.25)
  Component 2: tsconfig.json with correct compiler options (0.20)
  Component 3: src/routes/users.ts with GET and POST handlers (0.20)
  Component 4: src/app.ts mounting the users router (0.15)
  Component 5: tests/__tests__/users.test.ts with supertest tests (0.20)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'ts-express-api')
TASK_ID = 'vscode_gf4_018'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: package.json with correct dependencies (0.25 points)
    try:
        pkg_path = os.path.join(PROJECT_DIR, 'package.json')
        with open(pkg_path, 'r') as f:
            pkg = json.load(f)

        deps = pkg.get('dependencies', {})
        dev_deps = pkg.get('devDependencies', {})

        # express must be in production dependencies
        has_express = 'express' in deps

        # These must be in devDependencies
        required_dev = ['@types/express', 'typescript', 'ts-node', 'nodemon',
                        'jest', '@types/jest', 'ts-jest', 'supertest']
        dev_found = [d for d in required_dev if d in dev_deps]
        dev_ratio = len(dev_found) / len(required_dev)

        comp1_score = 0.0
        if has_express:
            comp1_score += 0.05
        # Scale remaining 0.20 by how many dev deps are present
        comp1_score += 0.20 * dev_ratio

        if has_express and dev_ratio == 1.0:
            print(f"PASS: Component 1 — package.json has all dependencies ({comp1_score:.2f} pts)")
        else:
            missing_dev = [d for d in required_dev if d not in dev_deps]
            print(f"PARTIAL: Component 1 — express={'yes' if has_express else 'no'}, "
                  f"dev deps {len(dev_found)}/{len(required_dev)}, missing: {missing_dev}")

        if comp1_score > 0:
            total_score += comp1_score
    except FileNotFoundError:
        print("FAIL: Component 1 — package.json not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: tsconfig.json with correct compiler options (0.20 points)
    try:
        ts_path = os.path.join(PROJECT_DIR, 'tsconfig.json')
        with open(ts_path, 'r') as f:
            content = f.read()
        # Strip single-line comments for JSONC compatibility
        content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        tsconfig = json.loads(content_clean)

        compiler_opts = tsconfig.get('compilerOptions', {})
        checks = {
            'strict': compiler_opts.get('strict') is True,
            'outDir': compiler_opts.get('outDir', '').rstrip('/') == './dist',
            'rootDir': compiler_opts.get('rootDir', '').rstrip('/') == './src',
            'target': str(compiler_opts.get('target', '')).upper() == 'ES2020',
        }
        passed = sum(1 for v in checks.values() if v)
        comp2_score = 0.20 * (passed / 4)

        if passed == 4:
            print(f"PASS: Component 2 — tsconfig.json has all required options ({comp2_score:.2f} pts)")
        else:
            failed = [k for k, v in checks.items() if not v]
            print(f"PARTIAL: Component 2 — {passed}/4 checks passed, failed: {failed} "
                  f"(actual: strict={compiler_opts.get('strict')}, outDir={compiler_opts.get('outDir')}, "
                  f"rootDir={compiler_opts.get('rootDir')}, target={compiler_opts.get('target')})")

        if comp2_score > 0:
            total_score += comp2_score
    except FileNotFoundError:
        print("FAIL: Component 2 — tsconfig.json not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: src/routes/users.ts with GET and POST /users handlers (0.20 points)
    try:
        users_path = os.path.join(PROJECT_DIR, 'src', 'routes', 'users.ts')
        with open(users_path, 'r') as f:
            users_content = f.read()

        comp3_score = 0.0
        # Check for Router import/usage
        has_router = bool(re.search(r'Router', users_content))
        # Check for GET /users handler
        has_get = bool(re.search(r'router\.(get|GET)\s*\(\s*[\'"]/?users[\'"]', users_content, re.IGNORECASE))
        # Check for POST /users handler
        has_post = bool(re.search(r'router\.(post|POST)\s*\(\s*[\'"]/?users[\'"]', users_content, re.IGNORECASE))
        # Check for export
        has_export = bool(re.search(r'export\s+(default\s+)?router', users_content))

        if has_router:
            comp3_score += 0.04
        if has_get:
            comp3_score += 0.06
        if has_post:
            comp3_score += 0.06
        if has_export:
            comp3_score += 0.04

        if comp3_score == 0.20:
            print(f"PASS: Component 3 — users.ts has Router, GET, POST, and export ({comp3_score:.2f} pts)")
        else:
            print(f"PARTIAL: Component 3 — Router={has_router}, GET={has_get}, POST={has_post}, "
                  f"export={has_export} ({comp3_score:.2f} pts)")

        if comp3_score > 0:
            total_score += comp3_score
    except FileNotFoundError:
        print("FAIL: Component 3 — src/routes/users.ts not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: src/app.ts mounts the users router (0.15 points)
    try:
        app_path = os.path.join(PROJECT_DIR, 'src', 'app.ts')
        with open(app_path, 'r') as f:
            app_content = f.read()

        comp4_score = 0.0
        # Check for express import
        has_express_import = bool(re.search(r'import\s+.*express', app_content))
        # Check for users router import
        has_router_import = bool(re.search(r'import\s+.*from\s+[\'"]\.?\.?/?routes/users[\'"]', app_content))
        # Check for app.use mounting the router
        has_mount = bool(re.search(r'app\.use\s*\(', app_content))

        if has_express_import:
            comp4_score += 0.03
        if has_router_import:
            comp4_score += 0.06
        if has_mount:
            comp4_score += 0.06

        if comp4_score == 0.15:
            print(f"PASS: Component 4 — app.ts imports express, imports users router, and mounts it ({comp4_score:.2f} pts)")
        else:
            print(f"PARTIAL: Component 4 — express_import={has_express_import}, "
                  f"router_import={has_router_import}, mount={has_mount} ({comp4_score:.2f} pts)")

        if comp4_score > 0:
            total_score += comp4_score
    except FileNotFoundError:
        print("FAIL: Component 4 — src/app.ts not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: tests/__tests__/users.test.ts with supertest tests (0.20 points)
    try:
        test_path = os.path.join(PROJECT_DIR, 'tests', '__tests__', 'users.test.ts')
        with open(test_path, 'r') as f:
            test_content = f.read()

        comp5_score = 0.0
        # Check for supertest import
        has_supertest = bool(re.search(r'import\s+.*supertest', test_content))
        # Check for app import
        has_app_import = bool(re.search(r'import\s+.*app', test_content))
        # Check for GET test
        has_get_test = bool(re.search(r'\.(get|GET)\s*\(\s*[\'"][^\'"]*users[\'"]', test_content))
        # Check for POST test
        has_post_test = bool(re.search(r'\.(post|POST)\s*\(\s*[\'"][^\'"]*users[\'"]', test_content))
        # Check for at least 2 test cases (it/test blocks)
        test_cases = len(re.findall(r'\b(it|test)\s*\(', test_content))
        has_multiple_tests = test_cases >= 2

        if has_supertest:
            comp5_score += 0.04
        if has_app_import:
            comp5_score += 0.04
        if has_get_test:
            comp5_score += 0.04
        if has_post_test:
            comp5_score += 0.04
        if has_multiple_tests:
            comp5_score += 0.04

        if comp5_score == 0.20:
            print(f"PASS: Component 5 — users.test.ts has supertest, app import, GET test, POST test, "
                  f"{test_cases} test cases ({comp5_score:.2f} pts)")
        else:
            print(f"PARTIAL: Component 5 — supertest={has_supertest}, app_import={has_app_import}, "
                  f"GET_test={has_get_test}, POST_test={has_post_test}, "
                  f"test_cases={test_cases} ({comp5_score:.2f} pts)")

        if comp5_score > 0:
            total_score += comp5_score
    except FileNotFoundError:
        print("FAIL: Component 5 — tests/__tests__/users.test.ts not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
verify_task()
