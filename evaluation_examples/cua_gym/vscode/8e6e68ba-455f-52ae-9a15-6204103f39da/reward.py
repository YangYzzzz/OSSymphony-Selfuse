"""
Reward Script: Advanced async patterns implementation in VSCode project
Task ID: vscode_gf6_076
Domain: vscode
Scoring:
  C1 (0.15) - throttle.py has AsyncRateLimiter with asyncio.Semaphore + acquire()
  C2 (0.15) - retry.py has async_retry decorator with exponential backoff
  C3 (0.15) - circuit_breaker.py has AsyncCircuitBreaker with 3 states
  C4 (0.15) - test_patterns.py has >= 6 async test functions
  C5 (0.10) - .vscode/settings.json has pytestArgs with asyncio-mode
  C6 (0.30) - pytest tests/test_patterns.py passes all tests
"""

import os
import re
import json

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'python-async-patterns')


def verify_task():
    total_score = 0.0

    # Component 1: throttle.py has AsyncRateLimiter with asyncio.Semaphore and acquire() (0.15)
    try:
        throttle_path = os.path.join(PROJECT, 'src', 'patterns', 'throttle.py')
        with open(throttle_path, 'r') as f:
            content = f.read()
        has_class = 'class AsyncRateLimiter' in content
        has_semaphore = 'asyncio.Semaphore' in content or 'Semaphore' in content
        has_acquire = re.search(r'async\s+def\s+acquire', content) is not None
        has_max_calls = 'max_calls' in content
        has_period = 'period' in content
        if has_class and has_semaphore and has_acquire and has_max_calls and has_period:
            print(f"PASS: Component 1 — AsyncRateLimiter with Semaphore, acquire(), max_calls, period (0.15 pts)")
            total_score += 0.15
        else:
            missing = []
            if not has_class: missing.append('class AsyncRateLimiter')
            if not has_semaphore: missing.append('asyncio.Semaphore')
            if not has_acquire: missing.append('async def acquire')
            if not has_max_calls: missing.append('max_calls param')
            if not has_period: missing.append('period param')
            print(f"FAIL: Component 1 — missing: {', '.join(missing)}")
    except FileNotFoundError:
        print(f"FAIL: Component 1 — throttle.py not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: retry.py has async_retry decorator with exponential backoff (0.15)
    try:
        retry_path = os.path.join(PROJECT, 'src', 'patterns', 'retry.py')
        with open(retry_path, 'r') as f:
            content = f.read()
        has_decorator = 'def async_retry' in content
        has_max_attempts = 'max_attempts' in content
        has_backoff = 'backoff_factor' in content
        has_exceptions = 'exceptions' in content
        has_sleep = 'asyncio.sleep' in content
        # Check for exponential backoff pattern (2 ** attempt or similar)
        has_exponential = re.search(r'2\s*\*\*', content) is not None
        if has_decorator and has_max_attempts and has_backoff and has_exceptions and has_sleep and has_exponential:
            print(f"PASS: Component 2 — async_retry with max_attempts, backoff_factor, exceptions, exponential backoff (0.15 pts)")
            total_score += 0.15
        else:
            missing = []
            if not has_decorator: missing.append('def async_retry')
            if not has_max_attempts: missing.append('max_attempts')
            if not has_backoff: missing.append('backoff_factor')
            if not has_exceptions: missing.append('exceptions')
            if not has_sleep: missing.append('asyncio.sleep')
            if not has_exponential: missing.append('exponential backoff (2**)')
            print(f"FAIL: Component 2 — missing: {', '.join(missing)}")
    except FileNotFoundError:
        print(f"FAIL: Component 2 — retry.py not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: circuit_breaker.py has AsyncCircuitBreaker with 3 states (0.15)
    try:
        cb_path = os.path.join(PROJECT, 'src', 'patterns', 'circuit_breaker.py')
        with open(cb_path, 'r') as f:
            content = f.read()
        has_class = 'class AsyncCircuitBreaker' in content
        has_closed = 'CLOSED' in content
        has_open = 'OPEN' in content
        has_half_open = 'HALF_OPEN' in content
        has_trip = 'trip_threshold' in content
        has_reset = 'reset_timeout' in content
        if has_class and has_closed and has_open and has_half_open and has_trip and has_reset:
            print(f"PASS: Component 3 — AsyncCircuitBreaker with CLOSED/OPEN/HALF_OPEN, trip_threshold, reset_timeout (0.15 pts)")
            total_score += 0.15
        else:
            missing = []
            if not has_class: missing.append('class AsyncCircuitBreaker')
            if not has_closed: missing.append('CLOSED state')
            if not has_open: missing.append('OPEN state')
            if not has_half_open: missing.append('HALF_OPEN state')
            if not has_trip: missing.append('trip_threshold')
            if not has_reset: missing.append('reset_timeout')
            print(f"FAIL: Component 3 — missing: {', '.join(missing)}")
    except FileNotFoundError:
        print(f"FAIL: Component 3 — circuit_breaker.py not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: test_patterns.py has >= 6 async test functions (0.15)
    try:
        test_path = os.path.join(PROJECT, 'tests', 'test_patterns.py')
        with open(test_path, 'r') as f:
            content = f.read()
        # Count async test functions (async def test_...)
        async_tests = re.findall(r'async\s+def\s+test_\w+', content)
        count = len(async_tests)
        # Verify tests cover all three patterns
        tests_rate_limiter = any('rate_limiter' in t or 'throttle' in t or 'limiter' in t for t in async_tests)
        tests_retry = any('retry' in t for t in async_tests)
        tests_circuit = any('circuit' in t or 'breaker' in t for t in async_tests)
        if count >= 6 and tests_rate_limiter and tests_retry and tests_circuit:
            print(f"PASS: Component 4 — {count} async test functions covering all 3 patterns (0.15 pts)")
            total_score += 0.15
        else:
            reasons = []
            if count < 6: reasons.append(f'only {count} async tests (need >= 6)')
            if not tests_rate_limiter: reasons.append('no rate limiter tests')
            if not tests_retry: reasons.append('no retry tests')
            if not tests_circuit: reasons.append('no circuit breaker tests')
            print(f"FAIL: Component 4 — {'; '.join(reasons)}")
    except FileNotFoundError:
        print(f"FAIL: Component 4 — test_patterns.py not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: .vscode/settings.json has pytestArgs with asyncio-mode (0.10)
    try:
        settings_path = os.path.join(PROJECT, '.vscode', 'settings.json')
        with open(settings_path, 'r') as f:
            # Handle JSONC (strip comments)
            raw = f.read()
            cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
            settings = json.loads(cleaned)
        pytest_enabled = settings.get('python.testing.pytestEnabled', False)
        pytest_args = settings.get('python.testing.pytestArgs', [])
        has_asyncio_mode = any('asyncio-mode' in str(arg) or 'asyncio_mode' in str(arg) for arg in pytest_args)
        if pytest_enabled and has_asyncio_mode:
            print(f"PASS: Component 5 — pytestEnabled=true, pytestArgs has asyncio-mode (0.10 pts)")
            total_score += 0.10
        else:
            reasons = []
            if not pytest_enabled: reasons.append('pytestEnabled not true')
            if not has_asyncio_mode: reasons.append('pytestArgs missing asyncio-mode')
            print(f"FAIL: Component 5 — {'; '.join(reasons)}")
    except FileNotFoundError:
        print(f"FAIL: Component 5 — .vscode/settings.json not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: pytest tests actually pass (0.30)
    try:
        import subprocess
        venv_python = os.path.join(PROJECT, 'venv', 'bin', 'python')
        if not os.path.exists(venv_python):
            venv_python = 'python3'
        result = subprocess.run(
            [venv_python, '-m', 'pytest', 'tests/test_patterns.py', '-v', '--tb=short'],
            capture_output=True, text=True, cwd=PROJECT, timeout=60
        )
        output = result.stdout + result.stderr
        # Parse test results
        passed_match = re.search(r'(\d+)\s+passed', output)
        failed_match = re.search(r'(\d+)\s+failed', output)
        passed_count = int(passed_match.group(1)) if passed_match else 0
        failed_count = int(failed_match.group(1)) if failed_match else 0
        total_tests = passed_count + failed_count

        if result.returncode == 0 and passed_count >= 6:
            print(f"PASS: Component 6 — all {passed_count} tests passed (0.30 pts)")
            total_score += 0.30
        elif passed_count > 0:
            # Partial credit proportional to pass rate
            ratio = passed_count / max(total_tests, 6)
            partial = round(0.30 * ratio, 2)
            print(f"PARTIAL: Component 6 — {passed_count}/{total_tests} tests passed ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 6 — tests failed or could not run. Return code: {result.returncode}")
            if output.strip():
                # Print last 10 lines for debugging
                for line in output.strip().split('\n')[-10:]:
                    print(f"  pytest: {line}")
    except FileNotFoundError:
        print(f"FAIL: Component 6 — test_patterns.py not found or pytest not available")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
