"""
Reward Script: Java Functional Utils Maven Project
Task ID: vscode_gf4_070
Domain: vscode
Scoring:
  C1: Either.java with right-biased Either monad methods (0.15)
  C2: Try.java with success/failure monad methods (0.15)
  C3: Validated.java with applicative error accumulation (0.15)
  C4: LazySupplier.java with memoized lazy evaluation (0.10)
  C5: Streams.java with stream utility methods (0.15)
  C6: At least 25 JUnit 5 test methods (0.15)
  C7: Maven test results show all tests pass with 0 failures (0.15)
"""

import os
import re
import glob as glob_mod

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'java-functional-utils')
SRC_MAIN = os.path.join(PROJECT, 'src', 'main', 'java', 'com', 'functional')
SRC_TEST = os.path.join(PROJECT, 'src', 'test', 'java', 'com', 'functional')
SUREFIRE = os.path.join(PROJECT, 'target', 'surefire-reports')


def read_file(path):
    """Read a file and return its content, or None if not found."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception:
        return None


def check_methods_in_java(content, method_names):
    """Check which method names appear in Java source content (as method declarations or references)."""
    found = []
    missing = []
    for m in method_names:
        # Match method declaration patterns like: methodName( or methodName (
        if re.search(rf'\b{re.escape(m)}\s*\(', content):
            found.append(m)
        else:
            missing.append(m)
    return found, missing


def verify_task():
    total_score = 0.0

    # Component 1: Either.java with map, flatMap, fold, left(), right() (0.15 pts)
    try:
        either_path = os.path.join(SRC_MAIN, 'Either.java')
        content = read_file(either_path)
        if content is None:
            print("FAIL: Component 1 — Either.java not found")
        else:
            required = ['map', 'flatMap', 'fold', 'left', 'right']
            found, missing = check_methods_in_java(content, required)
            if not missing:
                # Also verify it has Left and Right inner types
                has_left_type = 'Left' in content and ('class Left' in content or 'record Left' in content)
                has_right_type = 'Right' in content and ('class Right' in content or 'record Right' in content)
                if has_left_type and has_right_type:
                    print(f"PASS: Component 1 — Either.java has all methods ({', '.join(required)}) and Left/Right types (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 1 — Either.java missing Left/Right inner types")
            else:
                print(f"FAIL: Component 1 — Either.java missing methods: {missing}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Try.java with map, flatMap, recover, onSuccess, onFailure (0.15 pts)
    try:
        try_path = os.path.join(SRC_MAIN, 'Try.java')
        content = read_file(try_path)
        if content is None:
            print("FAIL: Component 2 — Try.java not found")
        else:
            required = ['map', 'flatMap', 'recover', 'onSuccess', 'onFailure']
            found, missing = check_methods_in_java(content, required)
            if not missing:
                # Verify Success/Failure types
                has_success = 'Success' in content and ('class Success' in content or 'record Success' in content)
                has_failure = 'Failure' in content and ('class Failure' in content or 'record Failure' in content)
                if has_success and has_failure:
                    print(f"PASS: Component 2 — Try.java has all methods ({', '.join(required)}) and Success/Failure types (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 2 — Try.java missing Success/Failure inner types")
            else:
                print(f"FAIL: Component 2 — Try.java missing methods: {missing}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Validated.java with combine() and error accumulation (0.15 pts)
    try:
        validated_path = os.path.join(SRC_MAIN, 'Validated.java')
        content = read_file(validated_path)
        if content is None:
            print("FAIL: Component 3 — Validated.java not found")
        else:
            has_combine = bool(re.search(r'\bcombine\s*\(', content))
            has_valid = 'Valid' in content and ('class Valid' in content or 'record Valid' in content)
            has_invalid = 'Invalid' in content and ('class Invalid' in content or 'record Invalid' in content)
            # Check for error accumulation: errors should be collected into a list
            has_accumulation = 'List' in content and ('addAll' in content or 'errors' in content.lower())
            if has_combine and has_valid and has_invalid and has_accumulation:
                print(f"PASS: Component 3 — Validated.java has combine(), Valid/Invalid types, and error accumulation (0.15 pts)")
                total_score += 0.15
            else:
                details = []
                if not has_combine:
                    details.append("missing combine()")
                if not has_valid or not has_invalid:
                    details.append("missing Valid/Invalid types")
                if not has_accumulation:
                    details.append("missing error accumulation")
                print(f"FAIL: Component 3 — Validated.java issues: {', '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: LazySupplier.java with memoized lazy evaluation (0.10 pts)
    try:
        lazy_path = os.path.join(SRC_MAIN, 'LazySupplier.java')
        content = read_file(lazy_path)
        if content is None:
            print("FAIL: Component 4 — LazySupplier.java not found")
        else:
            has_supplier = 'Supplier' in content
            has_get = bool(re.search(r'\bget\s*\(', content))
            # Memoization: check for caching pattern (evaluated flag or cached value)
            has_memoize = ('evaluated' in content or 'cached' in content or 'computed' in content
                          or 'volatile' in content or 'synchronized' in content)
            if has_supplier and has_get and has_memoize:
                print(f"PASS: Component 4 — LazySupplier.java implements memoized lazy Supplier (0.10 pts)")
                total_score += 0.10
            else:
                details = []
                if not has_supplier:
                    details.append("not a Supplier")
                if not has_get:
                    details.append("missing get()")
                if not has_memoize:
                    details.append("no memoization pattern detected")
                print(f"FAIL: Component 4 — LazySupplier.java issues: {', '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Streams.java with zip, unzip, chunk, sliding, takeWhile (0.15 pts)
    try:
        streams_path = os.path.join(SRC_MAIN, 'stream', 'Streams.java')
        content = read_file(streams_path)
        if content is None:
            print("FAIL: Component 5 — Streams.java not found at stream/Streams.java")
        else:
            required = ['zip', 'unzip', 'chunk', 'sliding', 'takeWhile']
            found, missing = check_methods_in_java(content, required)
            if not missing:
                print(f"PASS: Component 5 — Streams.java has all utility methods ({', '.join(required)}) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — Streams.java missing methods: {missing}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: At least 25 JUnit 5 test methods (0.15 pts)
    try:
        test_files = []
        for root, dirs, files in os.walk(SRC_TEST):
            for f in files:
                if f.endswith('Test.java'):
                    test_files.append(os.path.join(root, f))

        total_tests = 0
        test_details = []
        for tf in test_files:
            content = read_file(tf)
            if content:
                count = len(re.findall(r'@Test', content))
                total_tests += count
                test_details.append(f"{os.path.basename(tf)}: {count}")

        if total_tests >= 25:
            print(f"PASS: Component 6 — Found {total_tests} @Test methods across {len(test_files)} test files (0.15 pts)")
            print(f"  Details: {', '.join(test_details)}")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 — Found only {total_tests} @Test methods, need at least 25")
            if test_details:
                print(f"  Details: {', '.join(test_details)}")
            else:
                print("  No test files found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: Maven test results show all tests pass (0.15 pts)
    try:
        if not os.path.isdir(SUREFIRE):
            print("FAIL: Component 7 — No surefire-reports directory (mvn test not run)")
        else:
            report_files = glob_mod.glob(os.path.join(SUREFIRE, '*.txt'))
            if not report_files:
                print("FAIL: Component 7 — No surefire report files found")
            else:
                total_run = 0
                total_failures = 0
                total_errors = 0
                for rf in report_files:
                    content = read_file(rf)
                    if content:
                        match = re.search(
                            r'Tests run:\s*(\d+),\s*Failures:\s*(\d+),\s*Errors:\s*(\d+)',
                            content
                        )
                        if match:
                            total_run += int(match.group(1))
                            total_failures += int(match.group(2))
                            total_errors += int(match.group(3))

                if total_run >= 25 and total_failures == 0 and total_errors == 0:
                    print(f"PASS: Component 7 — Maven tests: {total_run} run, 0 failures, 0 errors (0.15 pts)")
                    total_score += 0.15
                elif total_run > 0 and total_failures == 0 and total_errors == 0:
                    # Tests pass but fewer than 25
                    print(f"FAIL: Component 7 — Maven tests pass but only {total_run} tests run (need 25+)")
                else:
                    print(f"FAIL: Component 7 — Maven tests: {total_run} run, {total_failures} failures, {total_errors} errors")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = min(total_score, 1.0)
    # Round to avoid float precision issues
    final_score = round(final_score, 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
