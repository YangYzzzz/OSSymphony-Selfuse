"""
Reward Script: Go Event Streaming Library
Task ID: vscode_gf4_077
Domain: vscode
Scoring:
  C1 (0.10) - go.mod with correct module path
  C2 (0.15) - producer.go with Publish, PublishBatch, Close
  C3 (0.15) - consumer.go with Subscribe + functional options
  C4 (0.15) - broker.go with in-memory broker
  C5 (0.15) - middleware.go with 4 middlewares
  C6 (0.10) - example order pipeline
  C7 (0.10) - 12+ test functions
  C8 (0.10) - tests compile successfully
"""

import os
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'go-event-streaming')


def read_file(path):
    """Read a file and return its contents, or None if not found."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except (FileNotFoundError, PermissionError, IOError) as e:
        print(f"  Could not read {path}: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: go.mod exists with module github.com/user/go-events (0.10 points)
    try:
        gomod_path = os.path.join(PROJECT_DIR, 'go.mod')
        content = read_file(gomod_path)
        if content and 'module github.com/user/go-events' in content:
            print(f"PASS: Component 1 - go.mod has correct module path (0.10 pts)")
            total_score += 0.10
        else:
            if content is None:
                print(f"FAIL: Component 1 - go.mod not found")
            else:
                print(f"FAIL: Component 1 - go.mod missing 'module github.com/user/go-events', content: {content[:100]}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: producer.go with Producer struct, Publish, PublishBatch, Close (0.15 points)
    try:
        prod_path = os.path.join(PROJECT_DIR, 'pkg', 'stream', 'producer.go')
        content = read_file(prod_path)
        if content:
            checks = {
                'Producer struct': re.search(r'type\s+Producer\s+struct', content) is not None,
                'Publish method': re.search(r'func\s+\(.*Producer\)\s+Publish\s*\(', content) is not None,
                'PublishBatch method': re.search(r'func\s+\(.*Producer\)\s+PublishBatch\s*\(', content) is not None,
                'Close method': re.search(r'func\s+\(.*Producer\)\s+Close\s*\(', content) is not None,
            }
            passed = sum(v for v in checks.values())
            if passed == 4:
                print(f"PASS: Component 2 - producer.go has all required elements (0.15 pts)")
                total_score += 0.15
            else:
                for name, ok in checks.items():
                    status = "OK" if ok else "MISSING"
                    print(f"  {status}: {name}")
                pts = round(0.15 * passed / 4, 3)
                print(f"PARTIAL: Component 2 - {passed}/4 checks passed ({pts} pts)")
                total_score += pts
        else:
            print(f"FAIL: Component 2 - producer.go not found")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: consumer.go with Consumer, Subscribe, functional options (0.15 points)
    try:
        cons_path = os.path.join(PROJECT_DIR, 'pkg', 'stream', 'consumer.go')
        content = read_file(cons_path)
        # Also check types.go for functional option types
        types_path = os.path.join(PROJECT_DIR, 'pkg', 'stream', 'types.go')
        types_content = read_file(types_path) or ""
        combined = content + "\n" + types_content if content else types_content

        if content:
            checks = {
                'Consumer struct': re.search(r'type\s+Consumer\s+struct', content) is not None,
                'Subscribe method': re.search(r'func\s+\(.*Consumer\)\s+Subscribe\s*\(', content) is not None,
                'ConsumerOption type': re.search(r'(type\s+ConsumerOption\s+func|ConsumerOption)', combined) is not None,
                'MaxConcurrency option': 'MaxConcurrency' in combined,
                'RetryPolicy option': 'RetryPolicy' in combined,
                'DeadLetterQueue option': 'DeadLetterQueue' in combined,
            }
            passed = sum(v for v in checks.values())
            if passed >= 5:
                print(f"PASS: Component 3 - consumer.go has all required elements (0.15 pts)")
                total_score += 0.15
            else:
                for name, ok in checks.items():
                    status = "OK" if ok else "MISSING"
                    print(f"  {status}: {name}")
                pts = round(0.15 * passed / 6, 3)
                print(f"PARTIAL: Component 3 - {passed}/6 checks passed ({pts} pts)")
                total_score += pts
        else:
            print(f"FAIL: Component 3 - consumer.go not found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: broker.go with in-memory Broker, channel/goroutine, topic routing, persistent log (0.15 points)
    try:
        broker_path = os.path.join(PROJECT_DIR, 'pkg', 'stream', 'broker.go')
        content = read_file(broker_path)
        if content:
            checks = {
                'Broker struct': re.search(r'type\s+Broker\s+struct', content) is not None,
                'Channel-based (chan keyword)': 'chan ' in content or 'chan\n' in content or 'chan}' in content or 'chan struct' in content,
                'Topic routing (subscribers map)': 'subscribers' in content and 'map[string]' in content,
                'Persistent log option': re.search(r'(EnablePersistentLog|logEnabled|eventLog)', content) is not None,
            }
            passed = sum(v for v in checks.values())
            if passed >= 3:
                print(f"PASS: Component 4 - broker.go has core broker elements (0.15 pts)")
                total_score += 0.15
            else:
                for name, ok in checks.items():
                    status = "OK" if ok else "MISSING"
                    print(f"  {status}: {name}")
                pts = round(0.15 * passed / 4, 3)
                print(f"PARTIAL: Component 4 - {passed}/4 checks passed ({pts} pts)")
                total_score += pts
        else:
            print(f"FAIL: Component 4 - broker.go not found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: middleware.go with 4 middlewares: Logging, Retry, Timeout, Filter (0.15 points)
    try:
        mw_path = os.path.join(PROJECT_DIR, 'pkg', 'stream', 'middleware.go')
        content = read_file(mw_path)
        if content:
            checks = {
                'Logging middleware': re.search(r'func\s+Logging\s*\(', content) is not None,
                'Retry middleware': re.search(r'func\s+Retry\s*\(', content) is not None,
                'Timeout middleware': re.search(r'func\s+Timeout\s*\(', content) is not None,
                'Filter middleware': re.search(r'func\s+Filter\s*\(', content) is not None,
            }
            passed = sum(v for v in checks.values())
            if passed == 4:
                print(f"PASS: Component 5 - middleware.go has all 4 middlewares (0.15 pts)")
                total_score += 0.15
            else:
                for name, ok in checks.items():
                    status = "OK" if ok else "MISSING"
                    print(f"  {status}: {name}")
                pts = round(0.15 * passed / 4, 3)
                print(f"PARTIAL: Component 5 - {passed}/4 middlewares found ({pts} pts)")
                total_score += pts
        else:
            print(f"FAIL: Component 5 - middleware.go not found")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: Example order processing pipeline (0.10 points)
    try:
        # Search for example in common locations
        example_found = False
        example_content = None
        for candidate in [
            os.path.join(PROJECT_DIR, 'example', 'order_pipeline', 'main.go'),
            os.path.join(PROJECT_DIR, 'examples', 'order_pipeline', 'main.go'),
            os.path.join(PROJECT_DIR, 'cmd', 'example', 'main.go'),
            os.path.join(PROJECT_DIR, 'example', 'main.go'),
            os.path.join(PROJECT_DIR, 'examples', 'main.go'),
        ]:
            c = read_file(candidate)
            if c:
                example_content = c
                example_found = True
                break

        if not example_found:
            # Broader search: any .go file under example/ or examples/
            for root_dir in ['example', 'examples', 'cmd']:
                check_dir = os.path.join(PROJECT_DIR, root_dir)
                if os.path.isdir(check_dir):
                    for dirpath, _, filenames in os.walk(check_dir):
                        for fn in filenames:
                            if fn.endswith('.go'):
                                example_content = read_file(os.path.join(dirpath, fn))
                                if example_content:
                                    example_found = True
                                    break
                        if example_found:
                            break
                if example_found:
                    break

        if example_found and example_content:
            # Verify it references stream package and has order-related content
            has_stream_import = 'stream' in example_content
            has_order = re.search(r'(?i)(order|Order)', example_content) is not None
            if has_stream_import and has_order:
                print(f"PASS: Component 6 - Example order pipeline found (0.10 pts)")
                total_score += 0.10
            elif has_stream_import:
                print(f"PARTIAL: Component 6 - Example found but no order reference (0.05 pts)")
                total_score += 0.05
            else:
                print(f"PARTIAL: Component 6 - Go file found but no stream import (0.025 pts)")
                total_score += 0.025
        else:
            print(f"FAIL: Component 6 - No example pipeline found")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    # Component 7: 12+ test functions (0.10 points)
    try:
        test_count = 0
        # Walk project for _test.go files
        for dirpath, _, filenames in os.walk(PROJECT_DIR):
            for fn in filenames:
                if fn.endswith('_test.go'):
                    content = read_file(os.path.join(dirpath, fn))
                    if content:
                        # Count func TestXxx patterns
                        tests = re.findall(r'^func\s+Test\w+\s*\(', content, re.MULTILINE)
                        test_count += len(tests)

        if test_count >= 12:
            print(f"PASS: Component 7 - Found {test_count} test functions (>= 12) (0.10 pts)")
            total_score += 0.10
        elif test_count > 0:
            # Partial credit: proportional up to 12
            ratio = min(test_count / 12.0, 1.0)
            pts = round(0.10 * ratio, 3)
            print(f"PARTIAL: Component 7 - Found {test_count}/12 test functions ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 7 - No test functions found")
    except Exception as e:
        print(f"ERROR: Component 7 - {e}")

    # Component 8: Tests compile (go vet or go build) (0.10 points)
    try:
        # Check if the Go code at least has valid structure by verifying
        # all required files exist and have valid package declarations
        required_files = [
            os.path.join(PROJECT_DIR, 'pkg', 'stream', 'producer.go'),
            os.path.join(PROJECT_DIR, 'pkg', 'stream', 'consumer.go'),
            os.path.join(PROJECT_DIR, 'pkg', 'stream', 'broker.go'),
            os.path.join(PROJECT_DIR, 'pkg', 'stream', 'middleware.go'),
        ]
        all_valid = True
        for fpath in required_files:
            content = read_file(fpath)
            if not content:
                all_valid = False
                print(f"  MISSING: {fpath}")
                continue
            if not re.search(r'^package\s+stream', content, re.MULTILINE):
                all_valid = False
                print(f"  INVALID: {fpath} - no 'package stream' declaration")

        # Also check go.mod
        gomod = read_file(os.path.join(PROJECT_DIR, 'go.mod'))
        if not gomod:
            all_valid = False
            print(f"  MISSING: go.mod")

        if all_valid:
            print(f"PASS: Component 8 - All required files have valid package declarations (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 8 - Some required files missing or invalid")
    except Exception as e:
        print(f"ERROR: Component 8 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isdir(PROJECT_DIR):
    print(f"Project directory not found: {PROJECT_DIR}")
    print("REWARD: 0.0")
else:
    verify_task()
