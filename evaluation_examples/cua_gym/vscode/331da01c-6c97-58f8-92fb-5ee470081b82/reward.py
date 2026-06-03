"""
Reward Script: Typed Microservice Framework with Fastify, Zod, DrizzleORM
Task ID: vscode_gf4_060
Domain: vscode
Scoring:
  Component 1 (0.15): package.json has all required dependencies
  Component 2 (0.20): router.ts has TypedRouter class with get/post/put/delete + Zod validation
  Component 3 (0.20): middleware.ts has compose() + auth, rate-limit, cors middlewares
  Component 4 (0.15): database.ts has DrizzleORM SQLite adapter with migration support
  Component 5 (0.15): productService.ts has CRUD service using the framework
  Component 6 (0.15): 15+ Vitest tests exist across test files
"""

import os
import re
import json

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'ts-microservice-framework')


def read_file(path):
    """Read a file and return its content, or None if not found."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception:
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: project directory exists
    if not os.path.isdir(PROJECT_DIR):
        print(f"CRITICAL: Project directory {PROJECT_DIR} does not exist")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: package.json has all required dependencies (0.15 points)
    try:
        pkg_content = read_file(os.path.join(PROJECT_DIR, 'package.json'))
        if pkg_content is None:
            print("FAIL: Component 1 — package.json not found")
        else:
            pkg = json.loads(pkg_content)
            deps = pkg.get('dependencies', {})
            dev_deps = pkg.get('devDependencies', {})
            all_deps = {**deps, **dev_deps}

            required_deps = ['fastify', 'pino', 'zod', 'drizzle-orm', 'better-sqlite3', 'vitest', 'supertest']
            found = [d for d in required_deps if d in all_deps]
            missing = [d for d in required_deps if d not in all_deps]

            if len(missing) == 0:
                print(f"PASS: Component 1 — All 7 required dependencies found in package.json (0.15 pts)")
                total_score += 0.15
            elif len(found) >= 5:
                partial = round(0.15 * len(found) / 7, 3)
                print(f"PARTIAL: Component 1 — {len(found)}/7 deps found (missing: {missing}). ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 1 — Only {len(found)}/7 deps found (missing: {missing})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: router.ts has TypedRouter with get/post/put/delete and Zod schema validation (0.20 points)
    try:
        router_content = read_file(os.path.join(PROJECT_DIR, 'src', 'framework', 'router.ts'))
        if router_content is None:
            print("FAIL: Component 2 — src/framework/router.ts not found")
        else:
            checks = {
                'TypedRouter_class': bool(re.search(r'class\s+TypedRouter', router_content)),
                'get_method': bool(re.search(r'\bget\s*[\(<]', router_content)),
                'post_method': bool(re.search(r'\bpost\s*[\(<]', router_content)),
                'put_method': bool(re.search(r'\bput\s*[\(<]', router_content)),
                'delete_method': bool(re.search(r'\bdelete\s*[\(<]', router_content)),
                'zod_schema_usage': bool(re.search(r'Zod|ZodType|ZodSchema|z\.object|\.parse\(', router_content)),
            }
            passed = sum(1 for v in checks.values() if v)
            if passed == len(checks):
                print(f"PASS: Component 2 — TypedRouter class with all 4 HTTP methods + Zod validation (0.20 pts)")
                total_score += 0.20
            elif passed >= 4:
                partial = round(0.20 * passed / len(checks), 3)
                failed = [k for k, v in checks.items() if not v]
                print(f"PARTIAL: Component 2 — {passed}/{len(checks)} checks passed (failed: {failed}). ({partial} pts)")
                total_score += partial
            else:
                failed = [k for k, v in checks.items() if not v]
                print(f"FAIL: Component 2 — Only {passed}/{len(checks)} checks passed (failed: {failed})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: middleware.ts has compose() + auth, rate-limit, cors middlewares (0.20 points)
    try:
        mw_content = read_file(os.path.join(PROJECT_DIR, 'src', 'framework', 'middleware.ts'))
        if mw_content is None:
            print("FAIL: Component 3 — src/framework/middleware.ts not found")
        else:
            checks = {
                'compose_function': bool(re.search(r'(function\s+compose|export\s+.*compose|const\s+compose\s*=)', mw_content)),
                'auth_middleware': bool(re.search(r'(auth[Mm]iddleware|authentication)', mw_content)),
                'ratelimit_middleware': bool(re.search(r'(rate[Ll]imit|rateLimitMiddleware|rateLimit)', mw_content)),
                'cors_middleware': bool(re.search(r'(cors[Mm]iddleware|corsMiddleware|CORS)', mw_content)),
            }
            passed = sum(1 for v in checks.values() if v)
            if passed == len(checks):
                print(f"PASS: Component 3 — compose() + auth, rate-limit, cors middlewares all found (0.20 pts)")
                total_score += 0.20
            elif passed >= 2:
                partial = round(0.20 * passed / len(checks), 3)
                failed = [k for k, v in checks.items() if not v]
                print(f"PARTIAL: Component 3 — {passed}/{len(checks)} checks passed (failed: {failed}). ({partial} pts)")
                total_score += partial
            else:
                failed = [k for k, v in checks.items() if not v]
                print(f"FAIL: Component 3 — Only {passed}/{len(checks)} checks passed (failed: {failed})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: database.ts has DrizzleORM SQLite adapter with migration support (0.15 points)
    try:
        db_content = read_file(os.path.join(PROJECT_DIR, 'src', 'framework', 'database.ts'))
        if db_content is None:
            print("FAIL: Component 4 — src/framework/database.ts not found")
        else:
            checks = {
                'drizzle_import': bool(re.search(r'drizzle[-_]orm|drizzle', db_content)),
                'sqlite_adapter': bool(re.search(r'better[-_]sqlite3|BetterSQLite3|sqlite', db_content, re.IGNORECASE)),
                'migration_support': bool(re.search(r'migrat', db_content, re.IGNORECASE)),
                'class_or_adapter': bool(re.search(r'(class\s+\w*[Dd]atabase|class\s+\w*[Aa]dapter|export\s+.*[Dd]atabase)', db_content)),
            }
            passed = sum(1 for v in checks.values() if v)
            if passed == len(checks):
                print(f"PASS: Component 4 — DrizzleORM SQLite adapter with migration support (0.15 pts)")
                total_score += 0.15
            elif passed >= 2:
                partial = round(0.15 * passed / len(checks), 3)
                failed = [k for k, v in checks.items() if not v]
                print(f"PARTIAL: Component 4 — {passed}/{len(checks)} checks passed (failed: {failed}). ({partial} pts)")
                total_score += partial
            else:
                failed = [k for k, v in checks.items() if not v]
                print(f"FAIL: Component 4 — Only {passed}/{len(checks)} checks passed (failed: {failed})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: productService.ts has CRUD service using the framework (0.15 points)
    try:
        svc_content = read_file(os.path.join(PROJECT_DIR, 'src', 'services', 'productService.ts'))
        if svc_content is None:
            print("FAIL: Component 5 — src/services/productService.ts not found")
        else:
            checks = {
                'product_service_or_class': bool(re.search(r'(class\s+\w*[Pp]roduct|[Pp]roduct[Ss]ervice|registerProduct)', svc_content)),
                'create_op': bool(re.search(r'(create[Pp]roduct|CREATE|INSERT|\.create\b)', svc_content, re.IGNORECASE)),
                'read_op': bool(re.search(r'(get[Pp]roduct|list[Pp]roduct|SELECT|\.get\b|\.find\b)', svc_content, re.IGNORECASE)),
                'update_op': bool(re.search(r'(update[Pp]roduct|UPDATE|\.update\b)', svc_content, re.IGNORECASE)),
                'delete_op': bool(re.search(r'(delete[Pp]roduct|DELETE|\.delete\b|\.remove\b)', svc_content, re.IGNORECASE)),
                'uses_framework': bool(re.search(r'(TypedRouter|DatabaseAdapter|import.*framework)', svc_content)),
            }
            passed = sum(1 for v in checks.values() if v)
            if passed == len(checks):
                print(f"PASS: Component 5 — Complete CRUD service using the framework (0.15 pts)")
                total_score += 0.15
            elif passed >= 3:
                partial = round(0.15 * passed / len(checks), 3)
                failed = [k for k, v in checks.items() if not v]
                print(f"PARTIAL: Component 5 — {passed}/{len(checks)} checks passed (failed: {failed}). ({partial} pts)")
                total_score += partial
            else:
                failed = [k for k, v in checks.items() if not v]
                print(f"FAIL: Component 5 — Only {passed}/{len(checks)} checks passed (failed: {failed})")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: 15+ Vitest tests exist across test files (0.15 points)
    try:
        tests_dir = os.path.join(PROJECT_DIR, 'tests')
        test_count = 0

        if not os.path.isdir(tests_dir):
            # Also check for __tests__ or test files in src
            alt_patterns = [
                os.path.join(PROJECT_DIR, '__tests__'),
                os.path.join(PROJECT_DIR, 'test'),
            ]
            for alt in alt_patterns:
                if os.path.isdir(alt):
                    tests_dir = alt
                    break

        if os.path.isdir(tests_dir):
            for root, dirs, files in os.walk(tests_dir):
                for fname in files:
                    if fname.endswith('.test.ts') or fname.endswith('.spec.ts') or fname.endswith('.test.js'):
                        fpath = os.path.join(root, fname)
                        content = read_file(fpath)
                        if content:
                            # Count it() and test() calls
                            it_matches = re.findall(r'\bit\s*\(', content)
                            test_matches = re.findall(r'\btest\s*\(', content)
                            test_count += len(it_matches) + len(test_matches)

        # Also search src directory for co-located test files
        src_dir = os.path.join(PROJECT_DIR, 'src')
        if os.path.isdir(src_dir):
            for root, dirs, files in os.walk(src_dir):
                for fname in files:
                    if fname.endswith('.test.ts') or fname.endswith('.spec.ts'):
                        fpath = os.path.join(root, fname)
                        content = read_file(fpath)
                        if content:
                            it_matches = re.findall(r'\bit\s*\(', content)
                            test_matches = re.findall(r'\btest\s*\(', content)
                            test_count += len(it_matches) + len(test_matches)

        if test_count >= 15:
            print(f"PASS: Component 6 — {test_count} Vitest tests found (>= 15 required) (0.15 pts)")
            total_score += 0.15
        elif test_count >= 10:
            partial = round(0.15 * test_count / 15, 3)
            print(f"PARTIAL: Component 6 — {test_count}/15 tests found. ({partial} pts)")
            total_score += partial
        elif test_count > 0:
            partial = round(0.15 * test_count / 15, 3)
            print(f"PARTIAL: Component 6 — Only {test_count}/15 tests found. ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 6 — No test files found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
