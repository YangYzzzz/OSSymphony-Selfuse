"""
Reward Script: Advanced Go Testing Configuration in VSCode
Task ID: vscode_gf6_034
Domain: vscode
Scoring:
  C1: testdata/users.json - valid JSON array with 5 user objects (0.15)
  C2: testdata/products.json - valid JSON array with 10 product objects (0.15)
  C3: internal/testutil/helpers.go - LoadFixture with t.Helper() and t.Fatal() (0.20)
  C4: internal/handlers/users_test.go - httptest, fixtures, TestMain (0.20)
  C5: internal/handlers/users_integration_test.go - //go:build integration (0.15)
  C6: .vscode/tasks.json - go test -count=1 -race task (0.15)
"""

import os
import json

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'go-test-advanced')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: testdata/users.json exists with 5 user objects (0.15 points)
    try:
        users_path = os.path.join(PROJECT, 'testdata', 'users.json')
        if os.path.isfile(users_path):
            with open(users_path, 'r') as f:
                users_data = json.load(f)
            if isinstance(users_data, list) and len(users_data) == 5:
                # Verify they are objects (dicts) with some expected keys
                all_objects = all(isinstance(u, dict) for u in users_data)
                if all_objects:
                    print(f"PASS: Component 1 - testdata/users.json has 5 user objects (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 1 - users.json items are not objects")
            else:
                print(f"FAIL: Component 1 - users.json expected list of 5 items, got {type(users_data).__name__} with {len(users_data) if isinstance(users_data, list) else 'N/A'} items")
        else:
            print(f"FAIL: Component 1 - testdata/users.json not found")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: testdata/products.json exists with 10 product objects (0.15 points)
    try:
        products_path = os.path.join(PROJECT, 'testdata', 'products.json')
        if os.path.isfile(products_path):
            with open(products_path, 'r') as f:
                products_data = json.load(f)
            if isinstance(products_data, list) and len(products_data) == 10:
                all_objects = all(isinstance(p, dict) for p in products_data)
                if all_objects:
                    print(f"PASS: Component 2 - testdata/products.json has 10 product objects (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 2 - products.json items are not objects")
            else:
                print(f"FAIL: Component 2 - products.json expected list of 10 items, got {type(products_data).__name__} with {len(products_data) if isinstance(products_data, list) else 'N/A'} items")
        else:
            print(f"FAIL: Component 2 - testdata/products.json not found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: internal/testutil/helpers.go with LoadFixture, t.Helper(), t.Fatal() (0.20 points)
    try:
        helpers_path = os.path.join(PROJECT, 'internal', 'testutil', 'helpers.go')
        if os.path.isfile(helpers_path):
            with open(helpers_path, 'r') as f:
                helpers_content = f.read()

            c3_score = 0.0
            has_load_fixture = 'LoadFixture' in helpers_content and 'func ' in helpers_content
            has_t_helper = 't.Helper()' in helpers_content
            has_t_fatal = 't.Fatal(' in helpers_content or 't.Fatalf(' in helpers_content

            if has_load_fixture:
                c3_score += 0.08
            else:
                print(f"FAIL: Component 3a - LoadFixture function not found in helpers.go")

            if has_t_helper:
                c3_score += 0.06
            else:
                print(f"FAIL: Component 3b - t.Helper() not found in helpers.go")

            if has_t_fatal:
                c3_score += 0.06
            else:
                print(f"FAIL: Component 3c - t.Fatal()/t.Fatalf() not found in helpers.go")

            if c3_score > 0:
                print(f"PASS: Component 3 - helpers.go has LoadFixture={has_load_fixture}, t.Helper()={has_t_helper}, t.Fatal()={has_t_fatal} ({c3_score} pts)")
                total_score += c3_score
        else:
            print(f"FAIL: Component 3 - internal/testutil/helpers.go not found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: internal/handlers/users_test.go with httptest, fixtures, TestMain (0.20 points)
    try:
        test_path = os.path.join(PROJECT, 'internal', 'handlers', 'users_test.go')
        if os.path.isfile(test_path):
            with open(test_path, 'r') as f:
                test_content = f.read()

            c4_score = 0.0
            has_new_recorder = 'httptest.NewRecorder()' in test_content
            has_new_server = 'httptest.NewServer(' in test_content
            has_fixture_load = 'LoadFixture' in test_content or 'testutil.LoadFixture' in test_content
            has_test_main = 'func TestMain(' in test_content

            if has_new_recorder:
                c4_score += 0.05
            else:
                print(f"FAIL: Component 4a - httptest.NewRecorder() not found in users_test.go")

            if has_new_server:
                c4_score += 0.05
            else:
                print(f"FAIL: Component 4b - httptest.NewServer() not found in users_test.go")

            if has_fixture_load:
                c4_score += 0.05
            else:
                print(f"FAIL: Component 4c - LoadFixture not used in users_test.go")

            if has_test_main:
                c4_score += 0.05
            else:
                print(f"FAIL: Component 4d - TestMain function not found in users_test.go")

            if c4_score > 0:
                print(f"PASS: Component 4 - users_test.go: Recorder={has_new_recorder}, Server={has_new_server}, Fixture={has_fixture_load}, TestMain={has_test_main} ({c4_score} pts)")
                total_score += c4_score
        else:
            print(f"FAIL: Component 4 - internal/handlers/users_test.go not found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: internal/handlers/users_integration_test.go with //go:build integration (0.15 points)
    try:
        integration_path = os.path.join(PROJECT, 'internal', 'handlers', 'users_integration_test.go')
        if os.path.isfile(integration_path):
            with open(integration_path, 'r') as f:
                integration_content = f.read()

            # Must have the build tag as the first directive line
            has_build_tag = '//go:build integration' in integration_content
            if has_build_tag:
                print(f"PASS: Component 5 - users_integration_test.go has //go:build integration tag (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 - //go:build integration tag not found in users_integration_test.go")
        else:
            print(f"FAIL: Component 5 - internal/handlers/users_integration_test.go not found")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: .vscode/tasks.json with go test -count=1 -race task (0.15 points)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        if os.path.isfile(tasks_path):
            with open(tasks_path, 'r') as f:
                tasks_data = json.load(f)

            tasks_list = tasks_data.get('tasks', [])
            found_race_task = False
            for task in tasks_list:
                cmd = task.get('command', '') or ''
                # Also check args if command is just 'go'
                args = task.get('args', [])
                full_cmd = cmd + ' ' + ' '.join(str(a) for a in args) if args else cmd

                if '-count=1' in full_cmd and '-race' in full_cmd and 'go test' in full_cmd:
                    found_race_task = True
                    break

            if found_race_task:
                print(f"PASS: Component 6 - .vscode/tasks.json has go test -count=1 -race task (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 6 - No task with 'go test -count=1 -race' found in tasks.json")
        else:
            print(f"FAIL: Component 6 - .vscode/tasks.json not found")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
