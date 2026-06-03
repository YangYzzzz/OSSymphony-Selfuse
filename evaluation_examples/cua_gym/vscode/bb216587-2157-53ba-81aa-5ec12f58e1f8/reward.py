"""
Reward Script: Testing pyramid workflow in ~/project
Task ID: vscode_wf_089
Domain: vscode
Scoring:
  C1 (0.15): Test directories with sample test files
  C2 (0.15): Jest unit config targeting tests/unit/
  C3 (0.15): Jest integration config with setup/teardown
  C4 (0.10): Playwright config targeting tests/e2e
  C5 (0.20): tasks.json has test-unit, test-integration, test-e2e, test-all
  C6 (0.10): test-all uses dependsOrder sequence with correct order
  C7 (0.15): launch.json has debug configs for all 3 test levels
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
VSCODE_DIR = os.path.join(PROJECT, '.vscode')
TASK_ID = 'vscode_wf_089'


def load_json_file(path):
    """Load a JSON file, stripping JSONC comments if present."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def read_file(path):
    """Read a text file and return its contents."""
    with open(path, 'r') as f:
        return f.read()


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Test directories with sample test files (0.15 points)
    # Initial state: tests/ is empty. Golden: has unit/, integration/, e2e/ with test files.
    try:
        unit_dir = os.path.join(PROJECT, 'tests', 'unit')
        integration_dir = os.path.join(PROJECT, 'tests', 'integration')
        e2e_dir = os.path.join(PROJECT, 'tests', 'e2e')

        has_unit_test = False
        has_integration_test = False
        has_e2e_test = False

        if os.path.isdir(unit_dir):
            unit_files = os.listdir(unit_dir)
            has_unit_test = any(f.endswith(('.test.js', '.test.ts', '.spec.js', '.spec.ts')) for f in unit_files)

        if os.path.isdir(integration_dir):
            integ_files = os.listdir(integration_dir)
            has_integration_test = any(f.endswith(('.test.js', '.test.ts', '.spec.js', '.spec.ts')) for f in integ_files)

        if os.path.isdir(e2e_dir):
            e2e_files = os.listdir(e2e_dir)
            has_e2e_test = any(f.endswith(('.test.js', '.test.ts', '.spec.js', '.spec.ts')) for f in e2e_files)

        if has_unit_test and has_integration_test and has_e2e_test:
            print(f"PASS: Component 1 -- All 3 test directories have test files (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- unit={has_unit_test}, integration={has_integration_test}, e2e={has_e2e_test}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Jest unit config exists and targets tests/unit/ (0.15 points)
    # Initial state: no jest.unit.config.js. Golden: exists with testMatch for tests/unit/.
    try:
        unit_config_path = os.path.join(PROJECT, 'jest.unit.config.js')
        if os.path.isfile(unit_config_path):
            content = read_file(unit_config_path)
            # Check it references tests/unit
            if 'tests/unit' in content or 'unit' in content.lower():
                print(f"PASS: Component 2 -- jest.unit.config.js exists and targets unit tests (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 -- jest.unit.config.js exists but doesn't reference unit tests")
        else:
            print(f"FAIL: Component 2 -- jest.unit.config.js not found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Jest integration config with setup/teardown (0.15 points)
    # Initial state: no jest.integration.config.js. Golden: exists with globalSetup/globalTeardown.
    try:
        integ_config_path = os.path.join(PROJECT, 'jest.integration.config.js')
        if os.path.isfile(integ_config_path):
            content = read_file(integ_config_path)
            has_integration_ref = 'tests/integration' in content or 'integration' in content.lower()
            has_setup_teardown = ('globalSetup' in content or 'setup' in content.lower()) and \
                                ('globalTeardown' in content or 'teardown' in content.lower())
            if has_integration_ref and has_setup_teardown:
                print(f"PASS: Component 3 -- jest.integration.config.js with setup/teardown (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 -- integ_ref={has_integration_ref}, setup_teardown={has_setup_teardown}")
        else:
            print(f"FAIL: Component 3 -- jest.integration.config.js not found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Playwright config exists and targets e2e (0.10 points)
    # Initial state: no playwright config. Golden: playwright.config.ts with testDir for e2e.
    try:
        pw_config_content = None
        for fname in ['playwright.config.ts', 'playwright.config.js']:
            pw_path = os.path.join(PROJECT, fname)
            if os.path.isfile(pw_path):
                pw_config_content = read_file(pw_path)
                if 'e2e' in pw_config_content or 'playwright' in pw_config_content.lower():
                    break
                else:
                    pw_config_content = None
        if pw_config_content is not None:
            print(f"PASS: Component 4 -- Playwright config found and references e2e (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 -- No playwright config found or doesn't reference e2e")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: tasks.json has all 4 required tasks (0.20 points)
    # Initial state: no tasks.json. Golden: has test-unit, test-integration, test-e2e, test-all.
    try:
        tasks_path = os.path.join(VSCODE_DIR, 'tasks.json')
        if os.path.isfile(tasks_path):
            tasks_config = load_json_file(tasks_path)
            tasks_list = tasks_config.get('tasks', [])
            task_labels = [t.get('label', '') for t in tasks_list]

            required_labels = ['test-unit', 'test-integration', 'test-e2e', 'test-all']
            found_labels = [lbl for lbl in required_labels if lbl in task_labels]

            if len(found_labels) == 4:
                print(f"PASS: Component 5 -- tasks.json has all 4 required tasks (0.20 pts)")
                total_score += 0.20
            else:
                missing = set(required_labels) - set(found_labels)
                print(f"FAIL: Component 5 -- Missing tasks: {missing}. Found: {found_labels}")
        else:
            print(f"FAIL: Component 5 -- tasks.json not found")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: test-all uses dependsOrder sequence with correct order (0.10 points)
    # Initial state: no tasks.json. Golden: test-all depends on the 3 test tasks in sequence.
    try:
        tasks_path = os.path.join(VSCODE_DIR, 'tasks.json')
        if os.path.isfile(tasks_path):
            tasks_config = load_json_file(tasks_path)
            tasks_list = tasks_config.get('tasks', [])

            test_all_task = None
            for t in tasks_list:
                if t.get('label') == 'test-all':
                    test_all_task = t
                    break

            if test_all_task:
                depends_on = test_all_task.get('dependsOn', [])
                depends_order = test_all_task.get('dependsOrder', '')

                # Must have sequence order and depend on all 3 test tasks
                has_sequence = depends_order == 'sequence'
                has_all_deps = all(dep in depends_on for dep in ['test-unit', 'test-integration', 'test-e2e'])

                # Verify unit comes before integration, integration before e2e
                correct_order = False
                if has_all_deps and len(depends_on) >= 3:
                    unit_idx = depends_on.index('test-unit')
                    integ_idx = depends_on.index('test-integration')
                    e2e_idx = depends_on.index('test-e2e')
                    correct_order = unit_idx < integ_idx < e2e_idx

                if has_sequence and correct_order:
                    print(f"PASS: Component 6 -- test-all has dependsOrder:sequence with correct order (0.10 pts)")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 6 -- sequence={has_sequence}, deps={depends_on}, order_ok={correct_order}")
            else:
                print(f"FAIL: Component 6 -- test-all task not found in tasks.json")
        else:
            print(f"FAIL: Component 6 -- tasks.json not found")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    # Component 7: launch.json has debug configs for all 3 test levels (0.15 points)
    # Initial state: no launch.json. Golden: 3 debug configurations.
    try:
        launch_path = os.path.join(VSCODE_DIR, 'launch.json')
        if os.path.isfile(launch_path):
            launch_config = load_json_file(launch_path)
            configurations = launch_config.get('configurations', [])

            # Check for debug configs covering unit, integration, and e2e
            config_names = [c.get('name', '').lower() for c in configurations]
            config_args = []
            for c in configurations:
                args_str = ' '.join(c.get('runtimeArgs', []) + [c.get('program', '')])
                config_args.append(args_str.lower())

            # Check each level is represented
            has_unit_debug = any(
                ('unit' in name) or ('unit' in args)
                for name, args in zip(config_names, config_args)
            )
            has_integ_debug = any(
                ('integration' in name) or ('integration' in args)
                for name, args in zip(config_names, config_args)
            )
            has_e2e_debug = any(
                ('e2e' in name) or ('playwright' in args)
                for name, args in zip(config_names, config_args)
            )

            if has_unit_debug and has_integ_debug and has_e2e_debug:
                print(f"PASS: Component 7 -- launch.json has debug configs for all 3 levels (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 7 -- unit={has_unit_debug}, integration={has_integ_debug}, e2e={has_e2e_debug}")
        else:
            print(f"FAIL: Component 7 -- launch.json not found")
    except Exception as e:
        print(f"ERROR: Component 7 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
