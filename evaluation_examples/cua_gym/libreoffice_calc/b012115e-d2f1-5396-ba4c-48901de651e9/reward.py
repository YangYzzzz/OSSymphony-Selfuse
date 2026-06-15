"""
Reward Script: Write a JUnit 5 test class 'CalculatorTest' in the test directory
Task ID: vscode_lang_056
Domain: vscode (Java / JUnit 5)
Scoring:
  Component 1 (0.15): CalculatorTest.java exists at correct path with meaningful content
  Component 2 (0.15): JUnit 5 imports and class structure present
  Component 3 (0.25): @Test methods testing add()
  Component 4 (0.25): @Test methods testing subtract()
  Component 5 (0.20): @Test methods testing multiply()
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_056'
PROJECT_DIR = os.path.join(WORKDIR, 'calculator-project')
TEST_FILE = os.path.join(
    PROJECT_DIR, 'src', 'test', 'java', 'com', 'example', 'CalculatorTest.java'
)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: CalculatorTest.java exists at correct path (0.15 points)
    # This file does NOT exist in initial_env, so scoring its existence is valid.
    try:
        if os.path.isfile(TEST_FILE):
            with open(TEST_FILE, 'r') as f:
                content = f.read()
            if len(content.strip()) > 50:
                print(f"PASS: Component 1 — CalculatorTest.java exists at {TEST_FILE} ({len(content)} chars) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — File exists but is too short ({len(content)} chars)")
                content = ""
        else:
            print(f"FAIL: Component 1 — CalculatorTest.java not found at {TEST_FILE}")
            content = ""
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        content = ""

    if not content:
        # No test file, no further checks possible
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: JUnit 5 imports and class structure (0.15 points)
    try:
        has_junit5_import = bool(re.search(
            r'import\s+org\.junit\.jupiter\.api\.Test', content
        ))
        has_assertions_import = bool(re.search(
            r'import\s+.*org\.junit\.jupiter\.api\.Assertions', content
        ))
        has_class_decl = bool(re.search(
            r'class\s+CalculatorTest', content
        ))

        checks_passed = sum([has_junit5_import, has_assertions_import, has_class_decl])
        if checks_passed == 3:
            print(f"PASS: Component 2 — JUnit 5 imports + CalculatorTest class found (0.15 pts)")
            total_score += 0.15
        elif checks_passed >= 2:
            partial = 0.10
            print(f"PARTIAL: Component 2 — {checks_passed}/3 structure checks passed ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — JUnit5 import: {has_junit5_import}, Assertions: {has_assertions_import}, Class: {has_class_decl}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Helper: find @Test methods and their bodies
    # Match @Test annotation (possibly with other annotations between) followed by method
    test_methods = re.findall(
        r'@Test[^}]*?void\s+(\w+)\s*\([^)]*\)\s*\{([^}]*)\}',
        content, re.DOTALL
    )

    # Component 3: @Test methods testing add() with assertions (0.25 points)
    try:
        add_tests = [
            (name, body) for name, body in test_methods
            if re.search(r'\.add\s*\(', body)
        ]
        # Also check that assertions are used (assertEquals, assertTrue, etc.)
        add_with_assert = [
            (name, body) for name, body in add_tests
            if re.search(r'assert\w+\s*\(', body)
        ]
        if len(add_with_assert) >= 2:
            print(f"PASS: Component 3 — Found {len(add_with_assert)} test methods for add() with assertions (0.25 pts)")
            total_score += 0.25
        elif len(add_with_assert) == 1:
            print(f"PARTIAL: Component 3 — Found 1 test method for add() with assertion (0.15 pts)")
            total_score += 0.15
        elif len(add_tests) >= 1:
            print(f"PARTIAL: Component 3 — Found {len(add_tests)} test(s) for add() but missing assertions (0.10 pts)")
            total_score += 0.10
        else:
            # Fallback: check method name contains 'add'
            add_named = [name for name, body in test_methods if 'add' in name.lower()]
            if add_named:
                print(f"PARTIAL: Component 3 — Found method(s) named with 'add': {add_named} (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 3 — No test methods found testing add()")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: @Test methods testing subtract() with assertions (0.25 points)
    try:
        subtract_tests = [
            (name, body) for name, body in test_methods
            if re.search(r'\.subtract\s*\(', body)
        ]
        subtract_with_assert = [
            (name, body) for name, body in subtract_tests
            if re.search(r'assert\w+\s*\(', body)
        ]
        if len(subtract_with_assert) >= 2:
            print(f"PASS: Component 4 — Found {len(subtract_with_assert)} test methods for subtract() with assertions (0.25 pts)")
            total_score += 0.25
        elif len(subtract_with_assert) == 1:
            print(f"PARTIAL: Component 4 — Found 1 test method for subtract() with assertion (0.15 pts)")
            total_score += 0.15
        elif len(subtract_tests) >= 1:
            print(f"PARTIAL: Component 4 — Found {len(subtract_tests)} test(s) for subtract() but missing assertions (0.10 pts)")
            total_score += 0.10
        else:
            subtract_named = [name for name, body in test_methods if 'subtract' in name.lower()]
            if subtract_named:
                print(f"PARTIAL: Component 4 — Found method(s) named with 'subtract': {subtract_named} (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 4 — No test methods found testing subtract()")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: @Test methods testing multiply() with assertions (0.20 points)
    try:
        multiply_tests = [
            (name, body) for name, body in test_methods
            if re.search(r'\.multiply\s*\(', body)
        ]
        multiply_with_assert = [
            (name, body) for name, body in multiply_tests
            if re.search(r'assert\w+\s*\(', body)
        ]
        if len(multiply_with_assert) >= 2:
            print(f"PASS: Component 5 — Found {len(multiply_with_assert)} test methods for multiply() with assertions (0.20 pts)")
            total_score += 0.20
        elif len(multiply_with_assert) == 1:
            print(f"PARTIAL: Component 5 — Found 1 test method for multiply() with assertion (0.10 pts)")
            total_score += 0.10
        elif len(multiply_tests) >= 1:
            print(f"PARTIAL: Component 5 — Found {len(multiply_tests)} test(s) for multiply() but missing assertions (0.05 pts)")
            total_score += 0.05
        else:
            multiply_named = [name for name, body in test_methods if 'multiply' in name.lower()]
            if multiply_named:
                print(f"PARTIAL: Component 5 — Found method(s) named with 'multiply': {multiply_named} (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 5 — No test methods found testing multiply()")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
