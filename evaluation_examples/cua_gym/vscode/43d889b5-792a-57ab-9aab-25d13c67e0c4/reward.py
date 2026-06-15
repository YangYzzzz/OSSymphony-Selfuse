"""
Reward Script: Verify Rust HTTP client library implementation
Task ID: vscode_gf4_069
Domain: vscode
Scoring:
  C1 (0.15): Cargo.toml has required dependencies
  C2 (0.15): Cargo.toml features correct (reqwest json+cookies, tokio full)
  C3 (0.15): src/client.rs with HttpClient builder pattern
  C4 (0.15): src/request.rs with RequestBuilder + HTTP methods + body builders
  C5 (0.10): src/response.rs with Response wrapper methods
  C6 (0.10): src/error.rs with thiserror error types
  C7 (0.10): src/middleware.rs with logging and retry
  C8 (0.10): Tests using mockito (10+)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf4_069'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'rust-http-client')


def read_file(path):
    """Read file content, return None if not found."""
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

    cargo_path = os.path.join(PROJECT_DIR, 'Cargo.toml')
    cargo_content = read_file(cargo_path)
    if cargo_content is None:
        print(f"CRITICAL: Cannot read {cargo_path}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Cargo.toml has required dependencies (0.15 points)
    # Required: reqwest, tokio, serde, serde_derive, url, thiserror
    try:
        required_deps = ['reqwest', 'tokio', 'serde', 'url', 'thiserror']
        # serde_derive can be a separate dep or serde with derive feature
        cargo_lower = cargo_content.lower()
        found_deps = []
        missing_deps = []
        for dep in required_deps:
            # Check for dep name in [dependencies] section
            if re.search(rf'^{dep}\s*=', cargo_content, re.MULTILINE):
                found_deps.append(dep)
            else:
                missing_deps.append(dep)

        # Check serde_derive: either as separate dep or serde has derive feature
        has_serde_derive = (
            re.search(r'^serde_derive\s*=', cargo_content, re.MULTILINE) is not None or
            re.search(r'serde\s*=.*features\s*=\s*\[.*"derive"', cargo_content) is not None
        )

        if len(found_deps) >= 5 and has_serde_derive:
            print(f"PASS: Component 1 — All required dependencies found: {found_deps}, serde_derive: yes (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Missing deps: {missing_deps}, serde_derive: {has_serde_derive}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Cargo.toml features correct (0.15 points)
    # reqwest needs json+cookies features, tokio needs full feature
    try:
        checks_passed = 0
        total_checks = 3

        # reqwest json feature
        if re.search(r'reqwest\s*=.*"json"', cargo_content):
            checks_passed += 1
            print("  PASS: reqwest has json feature")
        else:
            print("  FAIL: reqwest missing json feature")

        # reqwest cookies feature
        if re.search(r'reqwest\s*=.*"cookies"', cargo_content):
            checks_passed += 1
            print("  PASS: reqwest has cookies feature")
        else:
            print("  FAIL: reqwest missing cookies feature")

        # tokio full feature
        if re.search(r'tokio\s*=.*"full"', cargo_content):
            checks_passed += 1
            print("  PASS: tokio has full feature")
        else:
            print("  FAIL: tokio missing full feature")

        if checks_passed == total_checks:
            print(f"PASS: Component 2 — All dependency features correct (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — {checks_passed}/{total_checks} feature checks passed")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: src/client.rs with HttpClient builder pattern (0.15 points)
    try:
        client_path = os.path.join(PROJECT_DIR, 'src', 'client.rs')
        client_content = read_file(client_path)
        if client_content is None:
            print("FAIL: Component 3 — src/client.rs not found")
        else:
            checks = 0
            total_checks = 5

            # HttpClient struct
            if re.search(r'struct\s+HttpClient', client_content):
                checks += 1
            # Builder pattern (HttpClientBuilder or builder method)
            if re.search(r'fn\s+builder', client_content) or re.search(r'struct\s+HttpClientBuilder', client_content):
                checks += 1
            # base_url method
            if re.search(r'fn\s+base_url', client_content):
                checks += 1
            # header method
            if re.search(r'fn\s+header', client_content):
                checks += 1
            # bearer_token or timeout or retry method
            builder_methods = 0
            for method in ['bearer_token', 'timeout', 'retry']:
                if re.search(rf'fn\s+{method}', client_content):
                    builder_methods += 1
            if builder_methods >= 2:
                checks += 1

            if checks >= 4:
                print(f"PASS: Component 3 — client.rs has HttpClient with builder pattern ({checks}/{total_checks} checks) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — client.rs only passed {checks}/{total_checks} checks")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: src/request.rs with RequestBuilder + HTTP methods + body builders (0.15 points)
    try:
        request_path = os.path.join(PROJECT_DIR, 'src', 'request.rs')
        request_content = read_file(request_path)
        if request_content is None:
            print("FAIL: Component 4 — src/request.rs not found")
        else:
            checks = 0
            total_checks = 4

            # RequestBuilder struct
            if re.search(r'struct\s+RequestBuilder', request_content):
                checks += 1

            # HTTP method support (at least GET, POST referenced)
            http_methods_found = 0
            for method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                if method in request_content:
                    http_methods_found += 1
            if http_methods_found >= 3:
                checks += 1

            # query method
            if re.search(r'fn\s+query', request_content):
                checks += 1

            # json or form body builder
            body_builders = 0
            for builder in ['json', 'form']:
                if re.search(rf'fn\s+{builder}', request_content):
                    body_builders += 1
            if body_builders >= 1:
                checks += 1

            if checks >= 3:
                print(f"PASS: Component 4 — request.rs has RequestBuilder with methods ({checks}/{total_checks} checks) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — request.rs only passed {checks}/{total_checks} checks")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: src/response.rs with Response wrapper (0.10 points)
    try:
        response_path = os.path.join(PROJECT_DIR, 'src', 'response.rs')
        response_content = read_file(response_path)
        if response_content is None:
            print("FAIL: Component 5 — src/response.rs not found")
        else:
            checks = 0
            total_checks = 4

            # Response struct
            if re.search(r'struct\s+Response', response_content):
                checks += 1
            # status method
            if re.search(r'fn\s+status', response_content):
                checks += 1
            # json method
            if re.search(r'fn\s+json', response_content):
                checks += 1
            # text method
            if re.search(r'fn\s+text', response_content):
                checks += 1

            if checks >= 3:
                print(f"PASS: Component 5 — response.rs has Response with wrapper methods ({checks}/{total_checks} checks) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — response.rs only passed {checks}/{total_checks} checks")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: src/error.rs with thiserror error types (0.10 points)
    try:
        error_path = os.path.join(PROJECT_DIR, 'src', 'error.rs')
        error_content = read_file(error_path)
        if error_content is None:
            print("FAIL: Component 6 — src/error.rs not found")
        else:
            checks = 0
            total_checks = 3

            # Uses thiserror derive macro
            if 'thiserror' in error_content or '#[derive' in error_content and 'Error' in error_content:
                checks += 1
            # Has enum error type
            if re.search(r'enum\s+\w*[Ee]rror', error_content):
                checks += 1
            # Has multiple error variants (at least 2 #[error(...)] attributes)
            error_attrs = re.findall(r'#\[error\(', error_content)
            if len(error_attrs) >= 2:
                checks += 1

            if checks >= 2:
                print(f"PASS: Component 6 — error.rs has custom thiserror types ({checks}/{total_checks} checks) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 — error.rs only passed {checks}/{total_checks} checks")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: src/middleware.rs with logging and retry (0.10 points)
    try:
        middleware_path = os.path.join(PROJECT_DIR, 'src', 'middleware.rs')
        middleware_content = read_file(middleware_path)
        if middleware_content is None:
            print("FAIL: Component 7 — src/middleware.rs not found")
        else:
            checks = 0
            total_checks = 3

            # Has Middleware trait or similar abstraction
            if re.search(r'trait\s+Middleware', middleware_content) or 'middleware' in middleware_content.lower():
                checks += 1
            # Has logging middleware
            if re.search(r'[Ll]ogging', middleware_content):
                checks += 1
            # Has retry middleware
            if re.search(r'[Rr]etry', middleware_content):
                checks += 1

            if checks >= 2:
                print(f"PASS: Component 7 — middleware.rs has logging and retry ({checks}/{total_checks} checks) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 7 — middleware.rs only passed {checks}/{total_checks} checks")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    # Component 8: Tests using mockito (10+ tests) (0.10 points)
    try:
        # Check for test files in tests/ directory or inline tests
        tests_dir = os.path.join(PROJECT_DIR, 'tests')
        test_content = ""

        if os.path.isdir(tests_dir):
            for fname in os.listdir(tests_dir):
                if fname.endswith('.rs'):
                    content = read_file(os.path.join(tests_dir, fname))
                    if content:
                        test_content += content

        # Also check src/ files for #[test] or #[tokio::test]
        src_dir = os.path.join(PROJECT_DIR, 'src')
        if os.path.isdir(src_dir):
            for fname in os.listdir(src_dir):
                if fname.endswith('.rs'):
                    content = read_file(os.path.join(src_dir, fname))
                    if content:
                        test_content += content

        # Count test functions
        test_fns = re.findall(r'#\[(?:tokio::)?test\]', test_content)
        num_tests = len(test_fns)

        # Check mockito usage
        uses_mockito = 'mockito' in test_content

        if num_tests >= 10 and uses_mockito:
            print(f"PASS: Component 8 — Found {num_tests} tests using mockito (0.10 pts)")
            total_score += 0.10
        elif num_tests >= 5 and uses_mockito:
            partial = 0.05
            print(f"PARTIAL: Component 8 — Found {num_tests} tests with mockito ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 8 — Found {num_tests} tests, uses_mockito={uses_mockito}")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

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
