"""
Reward Script: Go Chi REST API setup in VSCode
Task ID: vscode_gf6_073
Domain: vscode
Scoring:
  Component 1: go.mod contains chi dependency (0.15)
  Component 2: router.go with chi.Router and 5 middleware (0.20)
  Component 3: routes.go with all required routes (0.20)
  Component 4: handler files with >= 5 handler functions (0.15)
  Component 5: router_test.go with >= 4 test cases using httptest (0.15)
  Component 6: .vscode/launch.json with Go debug config (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'go-chi-api')


def verify_task():
    total_score = 0.0

    # Component 1: go.mod contains go-chi/chi/v5 dependency (0.15 points)
    # Initial env has no chi dependency; golden env does.
    try:
        go_mod_path = os.path.join(PROJECT, 'go.mod')
        if not os.path.exists(go_mod_path):
            print("FAIL: Component 1 — go.mod not found")
        else:
            with open(go_mod_path, 'r') as f:
                go_mod_content = f.read()
            if 'go-chi/chi/v5' in go_mod_content:
                print(f"PASS: Component 1 — go.mod contains go-chi/chi/v5 dependency (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — go.mod missing go-chi/chi/v5 dependency")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: internal/router/router.go exists with chi.Router and 5 middleware (0.20 points)
    # Initial env has no such file; golden env has it with all middleware.
    try:
        router_path = os.path.join(PROJECT, 'internal', 'router', 'router.go')
        if not os.path.exists(router_path):
            print("FAIL: Component 2 — internal/router/router.go not found")
        else:
            with open(router_path, 'r') as f:
                router_content = f.read()

            # Check for chi.Router usage
            has_chi_router = 'chi.NewRouter()' in router_content or 'chi.Router' in router_content

            # Check for 5 required middleware
            required_middleware = [
                'Logger',
                'Recoverer',
                'RealIP',
                'RequestID',
            ]
            found_middleware = sum(1 for mw in required_middleware if mw in router_content)

            # Check for custom CORS middleware
            has_cors = 'CORS' in router_content or 'cors' in router_content.lower()

            if has_chi_router and found_middleware >= 4 and has_cors:
                print(f"PASS: Component 2 — router.go has chi.Router, {found_middleware}/4 standard middleware + CORS (0.20 pts)")
                total_score += 0.20
            elif has_chi_router and found_middleware >= 2:
                partial = 0.10
                print(f"PARTIAL: Component 2 — router.go has chi.Router but only {found_middleware}/4 middleware, CORS={has_cors} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — chi.Router={has_chi_router}, middleware={found_middleware}/4, CORS={has_cors}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: internal/router/routes.go with all required routes (0.20 points)
    # Initial env has no such file; golden env registers all routes.
    try:
        routes_path = os.path.join(PROJECT, 'internal', 'router', 'routes.go')
        if not os.path.exists(routes_path):
            print("FAIL: Component 3 — internal/router/routes.go not found")
        else:
            with open(routes_path, 'r') as f:
                routes_content = f.read()

            # Check for required route patterns
            required_routes = [
                '/health',
                '/users',
                'userID',  # {userID} parameter route
            ]
            found_routes = sum(1 for route in required_routes if route in routes_content)

            # Check for HTTP methods
            required_methods = ['Get', 'Post', 'Put', 'Delete']
            found_methods = sum(1 for method in required_methods if method in routes_content)

            if found_routes >= 3 and found_methods >= 4:
                print(f"PASS: Component 3 — routes.go has {found_routes}/3 route groups, {found_methods}/4 HTTP methods (0.20 pts)")
                total_score += 0.20
            elif found_routes >= 2 and found_methods >= 2:
                partial = 0.10
                print(f"PARTIAL: Component 3 — routes.go has {found_routes}/3 route groups, {found_methods}/4 HTTP methods ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — routes={found_routes}/3, methods={found_methods}/4")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: internal/handlers/ has handler files with >= 5 handler functions (0.15 points)
    # Initial env has no handlers dir; golden env has users.go and health.go with 5+ functions.
    try:
        handlers_dir = os.path.join(PROJECT, 'internal', 'handlers')
        if not os.path.isdir(handlers_dir):
            print("FAIL: Component 4 — internal/handlers/ directory not found")
        else:
            handler_files = [f for f in os.listdir(handlers_dir) if f.endswith('.go')]
            if len(handler_files) < 2:
                print(f"FAIL: Component 4 — only {len(handler_files)} handler file(s), need >= 2")
            else:
                # Count exported handler functions across all handler files
                handler_func_count = 0
                for hf in handler_files:
                    hf_path = os.path.join(handlers_dir, hf)
                    with open(hf_path, 'r') as f:
                        content = f.read()
                    # Count functions that take (http.ResponseWriter, *http.Request)
                    funcs = re.findall(r'func\s+\w+\s*\(\s*\w+\s+http\.ResponseWriter', content)
                    handler_func_count += len(funcs)

                if handler_func_count >= 5:
                    print(f"PASS: Component 4 — {len(handler_files)} handler files with {handler_func_count} handler functions (0.15 pts)")
                    total_score += 0.15
                elif handler_func_count >= 3:
                    partial = 0.08
                    print(f"PARTIAL: Component 4 — {handler_func_count}/5 handler functions ({partial} pts)")
                    total_score += partial
                else:
                    print(f"FAIL: Component 4 — only {handler_func_count} handler functions, need >= 5")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: tests/router_test.go with >= 4 test cases using httptest (0.15 points)
    # Initial env has no test file; golden env has 5 test cases.
    try:
        test_path = os.path.join(PROJECT, 'tests', 'router_test.go')
        if not os.path.exists(test_path):
            print("FAIL: Component 5 — tests/router_test.go not found")
        else:
            with open(test_path, 'r') as f:
                test_content = f.read()

            # Count test functions
            test_funcs = re.findall(r'func\s+(Test\w+)\s*\(', test_content)
            uses_httptest = 'httptest' in test_content

            if len(test_funcs) >= 4 and uses_httptest:
                print(f"PASS: Component 5 — {len(test_funcs)} test functions using httptest (0.15 pts)")
                total_score += 0.15
            elif len(test_funcs) >= 2 and uses_httptest:
                partial = 0.08
                print(f"PARTIAL: Component 5 — {len(test_funcs)}/4 test functions ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — test_funcs={len(test_funcs)}, httptest={uses_httptest}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: .vscode/launch.json with Go debug configuration (0.15 points)
    # Initial env has no launch.json; golden env has one with Go config.
    try:
        launch_path = os.path.join(PROJECT, '.vscode', 'launch.json')
        if not os.path.exists(launch_path):
            print("FAIL: Component 6 — .vscode/launch.json not found")
        else:
            with open(launch_path, 'r') as f:
                launch_content = f.read()

            # Strip JSONC comments before parsing
            stripped = re.sub(r'//.*$', '', launch_content, flags=re.MULTILINE)
            try:
                launch_json = json.loads(stripped)
            except json.JSONDecodeError:
                print("FAIL: Component 6 — launch.json is invalid JSON")
                launch_json = None

            if launch_json is not None:
                configs = launch_json.get('configurations', [])
                has_go_config = any(
                    c.get('type') == 'go' for c in configs
                )
                if has_go_config and len(configs) >= 1:
                    print(f"PASS: Component 6 — launch.json has {len(configs)} Go config(s) (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 6 — no Go-type configuration in launch.json")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
