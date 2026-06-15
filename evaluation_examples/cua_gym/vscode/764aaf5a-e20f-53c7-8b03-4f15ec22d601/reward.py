"""
Reward Script: Database testing workflow with testcontainers
Task ID: vscode_gf3_079
Domain: vscode
Scoring:
  C1: Integration test file exists and is substantial (0.10)
  C2: Uses testcontainers import (0.15)
  C3: PostgreSQL container setup in beforeAll (0.20)
  C4: Migration/schema execution against test container (0.15)
  C5: UserRepository tested with real DB queries (0.15)
  C6: Container teardown in afterAll (0.10)
  C7: Jest config has testTimeout 30000 for integration tests (0.15)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_079'

TEST_FILE = os.path.join(WORKDIR, 'projects', 'backend', 'src', '__tests__', 'integration', 'userRepository.test.ts')
JEST_CONFIG = os.path.join(WORKDIR, 'projects', 'backend', 'jest.config.ts')


def verify_task():
    total_score = 0.0

    # ── Component 1: Integration test file exists and is substantial (0.10) ──
    try:
        if not os.path.isfile(TEST_FILE):
            print(f"FAIL: Component 1 — file does not exist: {TEST_FILE}")
            # No file means nothing else can pass
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        with open(TEST_FILE, 'r') as f:
            content = f.read()

        # Must be non-trivial (at least 50 lines)
        line_count = len(content.strip().split('\n'))
        if line_count >= 50:
            print(f"PASS: Component 1 — integration test file exists with {line_count} lines (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — file exists but only {line_count} lines (need >=50 for substantial test)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ── Component 2: Uses testcontainers import (0.15) ──
    try:
        # Check for testcontainers import
        if re.search(r"from\s+['\"]testcontainers['\"]", content) or \
           re.search(r"require\s*\(\s*['\"]testcontainers['\"]", content) or \
           re.search(r"import\s+.*testcontainers", content):
            print(f"PASS: Component 2 — testcontainers package imported (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — no testcontainers import found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ── Component 3: PostgreSQL container setup in beforeAll (0.20) ──
    try:
        has_beforeAll = 'beforeAll' in content
        has_postgres_container = bool(re.search(r"GenericContainer\s*\(\s*['\"]postgres", content, re.IGNORECASE)) or \
                                 bool(re.search(r"PostgreSqlContainer", content, re.IGNORECASE))
        has_exposed_port = bool(re.search(r"withExposedPorts\s*\(\s*5432\s*\)", content))

        if has_beforeAll and has_postgres_container and has_exposed_port:
            print(f"PASS: Component 3 — PostgreSQL container setup in beforeAll with port 5432 (0.20 pts)")
            total_score += 0.20
        else:
            missing = []
            if not has_beforeAll:
                missing.append("beforeAll")
            if not has_postgres_container:
                missing.append("PostgreSQL GenericContainer")
            if not has_exposed_port:
                missing.append("withExposedPorts(5432)")
            print(f"FAIL: Component 3 — missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ── Component 4: Migration/schema execution against test container (0.15) ──
    try:
        # Check for CREATE TABLE or migration execution
        has_migration = bool(re.search(r"CREATE\s+TABLE", content, re.IGNORECASE)) or \
                        bool(re.search(r"migration", content, re.IGNORECASE) and re.search(r"(run|execute|query)", content, re.IGNORECASE))
        # Should reference users table
        has_users_table = bool(re.search(r"users", content, re.IGNORECASE))

        if has_migration and has_users_table:
            print(f"PASS: Component 4 — migration/schema creates users table (0.15 pts)")
            total_score += 0.15
        else:
            missing = []
            if not has_migration:
                missing.append("CREATE TABLE or migration execution")
            if not has_users_table:
                missing.append("users table reference")
            print(f"FAIL: Component 4 — missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ── Component 5: UserRepository tested with real DB queries (0.15) ──
    try:
        has_user_repo = bool(re.search(r"UserRepository", content))
        # Check for actual test cases with describe/it blocks that do CRUD
        has_describe = bool(re.search(r"describe\s*\(", content))
        has_it_blocks = len(re.findall(r"\bit\s*\(", content))
        # Must have actual assertions with expect()
        has_expects = len(re.findall(r"expect\s*\(", content))
        # Must interact with repo methods (create, find, update, delete, etc.)
        repo_method_calls = len(re.findall(r"userRepo\.\w+\s*\(", content, re.IGNORECASE))

        if has_user_repo and has_describe and has_it_blocks >= 3 and has_expects >= 3 and repo_method_calls >= 3:
            print(f"PASS: Component 5 — UserRepository tested with {has_it_blocks} test cases, "
                  f"{has_expects} assertions, {repo_method_calls} repo calls (0.15 pts)")
            total_score += 0.15
        else:
            details = f"UserRepo={has_user_repo}, describe={has_describe}, it_blocks={has_it_blocks}, " \
                      f"expects={has_expects}, repo_calls={repo_method_calls}"
            print(f"FAIL: Component 5 — insufficient test coverage: {details}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # ── Component 6: Container teardown in afterAll (0.10) ──
    try:
        has_afterAll = 'afterAll' in content
        has_container_stop = bool(re.search(r"container\s*\.\s*stop\s*\(", content, re.IGNORECASE)) or \
                             bool(re.search(r"container\s*&&.*stop", content, re.IGNORECASE))
        has_pool_end = bool(re.search(r"pool\s*\.\s*end\s*\(", content, re.IGNORECASE)) or \
                       bool(re.search(r"(close|disconnect|end)\s*\(", content, re.IGNORECASE))

        if has_afterAll and has_container_stop:
            print(f"PASS: Component 6 — container teardown in afterAll (0.10 pts)")
            total_score += 0.10
        else:
            missing = []
            if not has_afterAll:
                missing.append("afterAll block")
            if not has_container_stop:
                missing.append("container.stop() call")
            print(f"FAIL: Component 6 — missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # ── Component 7: Jest config has testTimeout 30000 for integration tests (0.15) ──
    try:
        if not os.path.isfile(JEST_CONFIG):
            print(f"FAIL: Component 7 — jest config not found: {JEST_CONFIG}")
        else:
            with open(JEST_CONFIG, 'r') as f:
                jest_content = f.read()

            has_timeout_30000 = bool(re.search(r"testTimeout\s*:\s*30000", jest_content))
            has_integration_project = bool(re.search(r"integration", jest_content, re.IGNORECASE))

            if has_timeout_30000 and has_integration_project:
                print(f"PASS: Component 7 — jest config has testTimeout: 30000 for integration tests (0.15 pts)")
                total_score += 0.15
            else:
                missing = []
                if not has_timeout_30000:
                    missing.append("testTimeout: 30000")
                if not has_integration_project:
                    missing.append("integration test project/config")
                print(f"FAIL: Component 7 — missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
