"""
Reward Script: Go integration tests with testcontainers-go setup
Task ID: vscode_gf6_070
Domain: vscode
Scoring:
  Component 1: go.mod has testcontainers-go dependencies (0.15)
  Component 2: tests/integration/db_test.go exists with build tag (0.20)
  Component 3: db_test.go has TestMain with container setup (0.15)
  Component 4: db_test.go has at least 2 integration test functions (0.15)
  Component 5: docker-compose.test.yml with postgres service (0.10)
  Component 6: Makefile has test-integration target (0.15)
  Component 7: .vscode/tasks.json has Integration Tests task (0.10)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_070'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'go-integration-tests')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: go.mod has testcontainers-go dependencies (0.15 points)
    try:
        go_mod_path = os.path.join(PROJECT_DIR, 'go.mod')
        with open(go_mod_path, 'r') as f:
            go_mod_content = f.read()

        has_tc = 'testcontainers/testcontainers-go' in go_mod_content
        has_tc_postgres = 'testcontainers-go/modules/postgres' in go_mod_content

        if has_tc and has_tc_postgres:
            print(f"PASS: Component 1 — go.mod has both testcontainers-go and modules/postgres (0.15 pts)")
            total_score += 0.15
        elif has_tc:
            print(f"PARTIAL: Component 1 — go.mod has testcontainers-go but missing modules/postgres (0.08 pts)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 1 — go.mod missing testcontainers-go dependencies")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: tests/integration/db_test.go exists with //go:build integration tag (0.20 points)
    try:
        test_file_path = os.path.join(PROJECT_DIR, 'tests', 'integration', 'db_test.go')
        if os.path.exists(test_file_path):
            with open(test_file_path, 'r') as f:
                test_content = f.read()

            # Check for build tag - either //go:build integration or // +build integration
            has_build_tag = bool(re.search(r'//go:build\s+integration', test_content)) or \
                            bool(re.search(r'//\s*\+build\s+integration', test_content))

            if has_build_tag:
                print(f"PASS: Component 2 — db_test.go exists with integration build tag (0.20 pts)")
                total_score += 0.20
            elif not has_build_tag:
                print(f"PARTIAL: Component 2 — db_test.go exists but missing integration build tag (0.10 pts)")
                total_score += 0.10
        else:
            print(f"FAIL: Component 2 — tests/integration/db_test.go not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: db_test.go has TestMain with container setup (0.15 points)
    try:
        test_file_path = os.path.join(PROJECT_DIR, 'tests', 'integration', 'db_test.go')
        if os.path.exists(test_file_path):
            with open(test_file_path, 'r') as f:
                test_content = f.read()

            has_test_main = 'func TestMain(' in test_content
            has_container_setup = ('testcontainers' in test_content.lower() or
                                   'RunContainer' in test_content or
                                   'postgres.Run' in test_content)
            has_terminate = ('Terminate' in test_content or 'defer' in test_content)

            if has_test_main and has_container_setup:
                print(f"PASS: Component 3 — TestMain found with container setup (0.15 pts)")
                total_score += 0.15
            elif has_test_main:
                print(f"PARTIAL: Component 3 — TestMain found but no container setup detected (0.07 pts)")
                total_score += 0.07
            else:
                print(f"FAIL: Component 3 — TestMain not found in db_test.go")
        else:
            print(f"FAIL: Component 3 — db_test.go not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: db_test.go has at least 2 integration test functions (0.15 points)
    try:
        test_file_path = os.path.join(PROJECT_DIR, 'tests', 'integration', 'db_test.go')
        if os.path.exists(test_file_path):
            with open(test_file_path, 'r') as f:
                test_content = f.read()

            # Find Test functions (not TestMain)
            test_funcs = re.findall(r'func\s+(Test[A-Z]\w*)\s*\(\s*t\s+\*testing\.T\s*\)', test_content)
            num_tests = len(test_funcs)

            if num_tests >= 2:
                print(f"PASS: Component 4 — Found {num_tests} test functions: {test_funcs} (0.15 pts)")
                total_score += 0.15
            elif num_tests == 1:
                print(f"PARTIAL: Component 4 — Found only 1 test function: {test_funcs} (0.07 pts)")
                total_score += 0.07
            else:
                print(f"FAIL: Component 4 — No test functions found in db_test.go")
        else:
            print(f"FAIL: Component 4 — db_test.go not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: docker-compose.test.yml with postgres service (0.10 points)
    try:
        compose_path = os.path.join(PROJECT_DIR, 'docker-compose.test.yml')
        if os.path.exists(compose_path):
            with open(compose_path, 'r') as f:
                compose_content = f.read()

            has_postgres = 'postgres' in compose_content.lower()
            has_services = 'services:' in compose_content or 'services :' in compose_content

            if has_postgres and has_services:
                print(f"PASS: Component 5 — docker-compose.test.yml has postgres service (0.10 pts)")
                total_score += 0.10
            else:
                print(f"PARTIAL: Component 5 — docker-compose.test.yml exists but missing postgres service definition")
        else:
            print(f"FAIL: Component 5 — docker-compose.test.yml not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Makefile has test-integration target (0.15 points)
    try:
        makefile_path = os.path.join(PROJECT_DIR, 'Makefile')
        with open(makefile_path, 'r') as f:
            makefile_content = f.read()

        # Check for test-integration target
        has_target = bool(re.search(r'^test-integration\s*:', makefile_content, re.MULTILINE))
        has_correct_cmd = bool(re.search(r'go\s+test\s+.*-tags=integration', makefile_content))

        if has_target and has_correct_cmd:
            print(f"PASS: Component 6 — Makefile has test-integration target with correct command (0.15 pts)")
            total_score += 0.15
        elif has_target:
            print(f"PARTIAL: Component 6 — Makefile has test-integration target but command may be incorrect (0.08 pts)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 6 — Makefile missing test-integration target")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: .vscode/tasks.json has Integration Tests task (0.10 points)
    try:
        tasks_path = os.path.join(PROJECT_DIR, '.vscode', 'tasks.json')
        if os.path.exists(tasks_path):
            with open(tasks_path, 'r') as f:
                # Handle JSONC (strip comments)
                content = f.read()
                content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
                tasks_json = json.loads(content_clean)

            tasks = tasks_json.get('tasks', [])
            matching = [t for t in tasks if 'integration' in t.get('label', '').lower() and 'test' in t.get('label', '').lower()]

            if len(matching) > 0:
                print(f"PASS: Component 7 — .vscode/tasks.json has Integration Tests task (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 7 — .vscode/tasks.json exists but no Integration Tests task found. Labels: {[t.get('label','') for t in tasks]}")
        else:
            print(f"FAIL: Component 7 — .vscode/tasks.json not found")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
