"""
Reward Script: Rust async runtime project with executor, timer, and channel modules
Task ID: vscode_gf4_035
Domain: vscode
Scoring:
  - Component 1: Cargo.toml has required dependencies (0.20)
  - Component 2: executor.rs with key async executor structures (0.20)
  - Component 3: timer.rs with async sleep future (0.15)
  - Component 4: channel.rs with bounded async channel (0.20)
  - Component 5: Module structure (mod.rs, lib.rs) wired correctly (0.10)
  - Component 6: Test files exist with tokio::test annotations (0.15)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_035'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'rust-async-runtime')
SRC_DIR = os.path.join(PROJECT_DIR, 'src')
RUNTIME_DIR = os.path.join(SRC_DIR, 'runtime')
TESTS_DIR = os.path.join(PROJECT_DIR, 'tests')


def read_file(path):
    """Read a file and return its contents, or None if it doesn't exist."""
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
        print(f"CRITICAL: Project directory not found: {PROJECT_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Cargo.toml has required dependencies (0.20 points)
    try:
        cargo_content = read_file(os.path.join(PROJECT_DIR, 'Cargo.toml'))
        if cargo_content is None:
            print("FAIL: Component 1 — Cargo.toml not found")
        else:
            deps_found = 0
            total_deps = 4

            # Check for tokio with full features
            if re.search(r'tokio\s*=\s*\{[^}]*features\s*=\s*\[.*"full".*\]', cargo_content):
                deps_found += 1
                print("PASS: Component 1a — tokio with full features found")
            else:
                print("FAIL: Component 1a — tokio with full features not found")

            # Check for futures
            if re.search(r'futures\s*=', cargo_content):
                deps_found += 1
                print("PASS: Component 1b — futures dependency found")
            else:
                print("FAIL: Component 1b — futures dependency not found")

            # Check for pin-project
            if re.search(r'pin-project\s*=', cargo_content):
                deps_found += 1
                print("PASS: Component 1c — pin-project dependency found")
            else:
                print("FAIL: Component 1c — pin-project dependency not found")

            # Check for thiserror
            if re.search(r'thiserror\s*=', cargo_content):
                deps_found += 1
                print("PASS: Component 1d — thiserror dependency found")
            else:
                print("FAIL: Component 1d — thiserror dependency not found")

            if deps_found == total_deps:
                print(f"PASS: Component 1 — All {total_deps} dependencies present (0.20 pts)")
                total_score += 0.20
            elif deps_found > 0:
                partial = round(0.20 * deps_found / total_deps, 2)
                print(f"PARTIAL: Component 1 — {deps_found}/{total_deps} dependencies found ({partial} pts)")
                total_score += partial
            else:
                print("FAIL: Component 1 — No required dependencies found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: executor.rs with key async executor structures (0.20 points)
    try:
        executor_content = read_file(os.path.join(RUNTIME_DIR, 'executor.rs'))
        if executor_content is None:
            print("FAIL: Component 2 — src/runtime/executor.rs not found")
        else:
            checks_passed = 0
            total_checks = 5

            # Check VecDeque usage for task queuing
            if 'VecDeque' in executor_content:
                checks_passed += 1
                print("PASS: Component 2a — VecDeque for task queuing")
            else:
                print("FAIL: Component 2a — VecDeque not found")

            # Check Pin<Box<dyn Future<Output=()> + Send>>> pattern
            if 'Pin' in executor_content and 'Box' in executor_content and 'Future' in executor_content:
                checks_passed += 1
                print("PASS: Component 2b — Pin<Box<dyn Future>> pattern")
            else:
                print("FAIL: Component 2b — Pin<Box<dyn Future>> pattern not found")

            # Check Waker implementation
            if 'Waker' in executor_content:
                checks_passed += 1
                print("PASS: Component 2c — Waker usage")
            else:
                print("FAIL: Component 2c — Waker not found")

            # Check run() method
            if re.search(r'(pub\s+)?fn\s+run\s*\(', executor_content):
                checks_passed += 1
                print("PASS: Component 2d — run() method defined")
            else:
                print("FAIL: Component 2d — run() method not found")

            # Check poll() call in run method (actually polls futures)
            if re.search(r'\.poll\s*\(', executor_content):
                checks_passed += 1
                print("PASS: Component 2e — poll() call for driving futures")
            else:
                print("FAIL: Component 2e — poll() call not found")

            if checks_passed == total_checks:
                print(f"PASS: Component 2 — executor.rs fully implemented (0.20 pts)")
                total_score += 0.20
            elif checks_passed > 0:
                partial = round(0.20 * checks_passed / total_checks, 2)
                print(f"PARTIAL: Component 2 — {checks_passed}/{total_checks} checks ({partial} pts)")
                total_score += partial
            else:
                print("FAIL: Component 2 — executor.rs missing required structures")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: timer.rs with async sleep future (0.15 points)
    try:
        timer_content = read_file(os.path.join(RUNTIME_DIR, 'timer.rs'))
        if timer_content is None:
            print("FAIL: Component 3 — src/runtime/timer.rs not found")
        else:
            checks_passed = 0
            total_checks = 4

            # Check Duration usage
            if 'Duration' in timer_content:
                checks_passed += 1
                print("PASS: Component 3a — Duration type used")
            else:
                print("FAIL: Component 3a — Duration not found")

            # Check sleep function
            if re.search(r'(pub\s+)?fn\s+sleep\s*\(', timer_content):
                checks_passed += 1
                print("PASS: Component 3b — sleep() function defined")
            else:
                print("FAIL: Component 3b — sleep() function not found")

            # Check Future implementation
            if 'impl Future' in timer_content:
                checks_passed += 1
                print("PASS: Component 3c — Future trait implemented")
            else:
                print("FAIL: Component 3c — Future trait impl not found")

            # Check Poll usage (Ready/Pending)
            if 'Poll::Ready' in timer_content and 'Poll::Pending' in timer_content:
                checks_passed += 1
                print("PASS: Component 3d — Poll::Ready/Pending states handled")
            else:
                print("FAIL: Component 3d — Poll states not found")

            if checks_passed == total_checks:
                print(f"PASS: Component 3 — timer.rs fully implemented (0.15 pts)")
                total_score += 0.15
            elif checks_passed > 0:
                partial = round(0.15 * checks_passed / total_checks, 2)
                print(f"PARTIAL: Component 3 — {checks_passed}/{total_checks} checks ({partial} pts)")
                total_score += partial
            else:
                print("FAIL: Component 3 — timer.rs missing required elements")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: channel.rs with bounded async channel (0.20 points)
    try:
        channel_content = read_file(os.path.join(RUNTIME_DIR, 'channel.rs'))
        if channel_content is None:
            print("FAIL: Component 4 — src/runtime/channel.rs not found")
        else:
            checks_passed = 0
            total_checks = 5

            # Check Sender struct
            if re.search(r'(pub\s+)?struct\s+Sender', channel_content):
                checks_passed += 1
                print("PASS: Component 4a — Sender struct defined")
            else:
                print("FAIL: Component 4a — Sender struct not found")

            # Check Receiver struct
            if re.search(r'(pub\s+)?struct\s+Receiver', channel_content):
                checks_passed += 1
                print("PASS: Component 4b — Receiver struct defined")
            else:
                print("FAIL: Component 4b — Receiver struct not found")

            # Check Mutex usage (for internal state)
            if 'Mutex' in channel_content:
                checks_passed += 1
                print("PASS: Component 4c — Mutex for synchronization")
            else:
                print("FAIL: Component 4c — Mutex not found")

            # Check VecDeque for buffer
            if 'VecDeque' in channel_content:
                checks_passed += 1
                print("PASS: Component 4d — VecDeque for message buffer")
            else:
                print("FAIL: Component 4d — VecDeque not found")

            # Check Waker notification
            if 'Waker' in channel_content:
                checks_passed += 1
                print("PASS: Component 4e — Waker for notifications")
            else:
                print("FAIL: Component 4e — Waker not found")

            if checks_passed == total_checks:
                print(f"PASS: Component 4 — channel.rs fully implemented (0.20 pts)")
                total_score += 0.20
            elif checks_passed > 0:
                partial = round(0.20 * checks_passed / total_checks, 2)
                print(f"PARTIAL: Component 4 — {checks_passed}/{total_checks} checks ({partial} pts)")
                total_score += partial
            else:
                print("FAIL: Component 4 — channel.rs missing required elements")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Module structure wired correctly (0.10 points)
    try:
        mod_content = read_file(os.path.join(RUNTIME_DIR, 'mod.rs'))
        lib_content = read_file(os.path.join(SRC_DIR, 'lib.rs'))

        checks_passed = 0
        total_checks = 2

        # Check mod.rs exports all three modules
        if mod_content is not None:
            modules_exported = 0
            for mod_name in ['executor', 'timer', 'channel']:
                if re.search(rf'(pub\s+)?mod\s+{mod_name}\s*;', mod_content):
                    modules_exported += 1
            if modules_exported == 3:
                checks_passed += 1
                print("PASS: Component 5a — mod.rs exports all three modules")
            else:
                print(f"FAIL: Component 5a — mod.rs exports {modules_exported}/3 modules")
        else:
            print("FAIL: Component 5a — src/runtime/mod.rs not found")

        # Check lib.rs declares the runtime module
        if lib_content is not None:
            if re.search(r'(pub\s+)?mod\s+runtime\s*;', lib_content):
                checks_passed += 1
                print("PASS: Component 5b — lib.rs declares runtime module")
            else:
                print("FAIL: Component 5b — lib.rs does not declare runtime module")
        else:
            print("FAIL: Component 5b — src/lib.rs not found")

        if checks_passed == total_checks:
            print(f"PASS: Component 5 — Module structure correct (0.10 pts)")
            total_score += 0.10
        elif checks_passed > 0:
            partial = round(0.10 * checks_passed / total_checks, 2)
            print(f"PARTIAL: Component 5 — {checks_passed}/{total_checks} checks ({partial} pts)")
            total_score += partial
        else:
            print("FAIL: Component 5 — Module structure not set up")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Test files with tokio::test for all three components (0.15 points)
    try:
        test_files_scored = 0
        total_test_files = 3

        for component in ['executor', 'timer', 'channel']:
            matched_file = None
            if os.path.isdir(TESTS_DIR):
                for fname in os.listdir(TESTS_DIR):
                    if fname.endswith('.rs') and component in fname.lower():
                        test_content = read_file(os.path.join(TESTS_DIR, fname))
                        if test_content and ('#[tokio::test]' in test_content or '#[test]' in test_content):
                            matched_file = fname
                            break

            if matched_file is not None:
                test_files_scored += 1
                print(f"PASS: Component 6 — test for {component} found ({matched_file})")
            else:
                print(f"FAIL: Component 6 — no test file with tests for {component}")

        if test_files_scored == total_test_files:
            print(f"PASS: Component 6 — All {total_test_files} test files present (0.15 pts)")
            total_score += 0.15
        elif test_files_scored > 0:
            partial = round(0.15 * test_files_scored / total_test_files, 2)
            print(f"PARTIAL: Component 6 — {test_files_scored}/{total_test_files} test files ({partial} pts)")
            total_score += partial
        else:
            print("FAIL: Component 6 — No test files found in tests/")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
