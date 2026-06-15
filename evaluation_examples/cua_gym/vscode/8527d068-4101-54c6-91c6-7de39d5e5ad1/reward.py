"""
Reward Script: Configure Jest test runner for api-tests project
Task ID: vscode_gf5_013
Domain: vscode
Scoring:
  Component 1 (0.25): jest and @types/jest in devDependencies
  Component 2 (0.25): jest.config.js exists with testMatch pointing to __tests__
  Component 3 (0.25): __tests__/utils.test.js exists with >=2 calculateTax test cases
  Component 4 (0.15): "test" script in package.json scripts section
  Component 5 (0.10): node_modules/jest exists (npm install was run)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'api-tests')
TASK_ID = 'vscode_gf5_013'


def verify_task():
    """
    Verify Jest test runner configuration with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: project directory exists
    if not os.path.isdir(PROJECT_DIR):
        print(f"CRITICAL: Project directory not found: {PROJECT_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: jest and @types/jest in devDependencies (0.25 points)
    try:
        pkg_path = os.path.join(PROJECT_DIR, 'package.json')
        with open(pkg_path, 'r') as f:
            pkg = json.load(f)
        dev_deps = pkg.get('devDependencies', {})
        has_jest = 'jest' in dev_deps
        has_types_jest = '@types/jest' in dev_deps
        if has_jest and has_types_jest:
            print(f"PASS: Component 1 — jest ({dev_deps['jest']}) and @types/jest ({dev_deps['@types/jest']}) in devDependencies (0.25 pts)")
            total_score += 0.25
        elif has_jest:
            print(f"PARTIAL: Component 1 — jest found but @types/jest missing (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — devDependencies missing jest and/or @types/jest. Found: {list(dev_deps.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: jest.config.js exists with testMatch pointing to __tests__ (0.25 points)
    try:
        config_path = os.path.join(PROJECT_DIR, 'jest.config.js')
        if os.path.isfile(config_path):
            with open(config_path, 'r') as f:
                config_content = f.read()
            # Check that testMatch references __tests__ directory
            has_test_match = 'testMatch' in config_content
            has_tests_dir = '__tests__' in config_content
            if has_test_match and has_tests_dir:
                print(f"PASS: Component 2 — jest.config.js exists with testMatch pointing to __tests__ (0.25 pts)")
                total_score += 0.25
            elif has_test_match:
                print(f"PARTIAL: Component 2 — jest.config.js has testMatch but does not reference __tests__ (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 2 — jest.config.js exists but missing testMatch. Content: {config_content[:200]}")
        else:
            print(f"FAIL: Component 2 — jest.config.js not found at {config_path}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: __tests__/utils.test.js exists with >=2 calculateTax test cases (0.25 points)
    try:
        test_file_path = os.path.join(PROJECT_DIR, '__tests__', 'utils.test.js')
        if os.path.isfile(test_file_path):
            with open(test_file_path, 'r') as f:
                test_content = f.read()
            # Count test cases that reference calculateTax
            # Match patterns like test('...', ...) or it('...', ...) that contain calculateTax in the body
            # A simpler heuristic: count occurrences of calculateTax( in test calls
            # Look for test/it blocks
            test_blocks = re.findall(r'(?:test|it)\s*\(', test_content)
            num_tests = len(test_blocks)
            has_calculate_tax = 'calculateTax' in test_content
            if has_calculate_tax and num_tests >= 2:
                print(f"PASS: Component 3 — utils.test.js found with {num_tests} test cases referencing calculateTax (0.25 pts)")
                total_score += 0.25
            elif has_calculate_tax and num_tests == 1:
                print(f"PARTIAL: Component 3 — utils.test.js has calculateTax but only {num_tests} test case (need >=2) (0.10 pts)")
                total_score += 0.10
            elif num_tests >= 2:
                print(f"PARTIAL: Component 3 — utils.test.js has {num_tests} tests but does not reference calculateTax (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — utils.test.js exists but insufficient tests or no calculateTax reference. Tests found: {num_tests}, calculateTax: {has_calculate_tax}")
        else:
            # Check if test file exists with different name in __tests__
            tests_dir = os.path.join(PROJECT_DIR, '__tests__')
            if os.path.isdir(tests_dir):
                files = os.listdir(tests_dir)
                test_files = [f for f in files if f.endswith('.test.js')]
                if test_files:
                    # Check any test file for calculateTax
                    for tf in test_files:
                        tf_path = os.path.join(tests_dir, tf)
                        with open(tf_path, 'r') as f:
                            content = f.read()
                        blocks = re.findall(r'(?:test|it)\s*\(', content)
                        if 'calculateTax' in content and len(blocks) >= 2:
                            print(f"PASS: Component 3 — {tf} found with {len(blocks)} test cases for calculateTax (0.25 pts)")
                            total_score += 0.25
                            break
                    else:
                        print(f"FAIL: Component 3 — __tests__ dir has files {test_files} but none with >=2 calculateTax tests")
                else:
                    print(f"FAIL: Component 3 — __tests__ directory exists but no .test.js files found")
            else:
                print(f"FAIL: Component 3 — __tests__ directory not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: "test" script in package.json (0.15 points)
    try:
        pkg_path = os.path.join(PROJECT_DIR, 'package.json')
        with open(pkg_path, 'r') as f:
            pkg = json.load(f)
        scripts = pkg.get('scripts', {})
        test_script = scripts.get('test', '')
        if 'jest' in test_script.lower():
            print(f"PASS: Component 4 — 'test' script found: '{test_script}' (0.15 pts)")
            total_score += 0.15
        elif 'test' in scripts:
            print(f"PARTIAL: Component 4 — 'test' script exists but doesn't reference jest: '{test_script}' (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 4 — No 'test' script in package.json scripts: {list(scripts.keys())}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: node_modules/jest exists (npm install was run) (0.10 points)
    try:
        jest_module_path = os.path.join(PROJECT_DIR, 'node_modules', 'jest')
        if os.path.isdir(jest_module_path):
            print(f"PASS: Component 5 — node_modules/jest exists (npm install completed) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — node_modules/jest not found (npm install not run)")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
