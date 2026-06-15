"""
Reward Script: Reactive data management library with RxJS and TypeScript
Task ID: vscode_gf4_054
Domain: vscode
Scoring:
  C1 (0.15) - package.json has required dependencies
  C2 (0.10) - tsconfig.json is valid TypeScript config
  C3 (0.25) - src/store.ts has Store class with BehaviorSubject, dispatch, select, middleware
  C4 (0.15) - src/operators.ts has debounceAction, retryWithBackoff, cacheLatest
  C5 (0.10) - src/effects.ts has Effects class with ofType
  C6 (0.10) - src/demo/todoStore.ts demonstrates a TODO store
  C7 (0.15) - 20+ Jest tests across test files
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'ts-reactive-library')


def verify_task():
    total_score = 0.0

    # Precondition: project directory exists
    if not os.path.isdir(PROJECT):
        print(f"CRITICAL: Project directory {PROJECT} does not exist")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: package.json has required dependencies (0.15 points)
    try:
        pkg_path = os.path.join(PROJECT, 'package.json')
        if not os.path.exists(pkg_path):
            print("FAIL: Component 1 — package.json does not exist")
        else:
            with open(pkg_path, 'r') as f:
                pkg = json.load(f)

            all_deps = {}
            all_deps.update(pkg.get('dependencies', {}))
            all_deps.update(pkg.get('devDependencies', {}))

            required_deps = ['rxjs', 'typescript', 'jest', 'ts-jest', '@types/jest']
            found_deps = [d for d in required_deps if d in all_deps]
            missing_deps = [d for d in required_deps if d not in all_deps]

            if len(found_deps) == len(required_deps):
                print(f"PASS: Component 1 — All 5 required deps found: {found_deps} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — Missing deps: {missing_deps}, found: {found_deps}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: tsconfig.json is valid TypeScript config (0.10 points)
    try:
        tsconfig_path = os.path.join(PROJECT, 'tsconfig.json')
        if not os.path.exists(tsconfig_path):
            print("FAIL: Component 2 — tsconfig.json does not exist")
        else:
            with open(tsconfig_path, 'r') as f:
                tsconfig = json.load(f)

            has_compiler_options = 'compilerOptions' in tsconfig
            compiler_opts = tsconfig.get('compilerOptions', {})
            # Must have at least target and module
            has_target = 'target' in compiler_opts
            has_module = 'module' in compiler_opts
            has_strict = compiler_opts.get('strict', False)

            if has_compiler_options and has_target and has_module:
                print(f"PASS: Component 2 — Valid tsconfig with target={compiler_opts['target']}, module={compiler_opts['module']}, strict={has_strict} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 2 — tsconfig missing compilerOptions/target/module. Keys: {list(compiler_opts.keys())}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: src/store.ts has Store class with BehaviorSubject, dispatch, select, middleware (0.25 points)
    try:
        store_path = os.path.join(PROJECT, 'src', 'store.ts')
        if not os.path.exists(store_path):
            print("FAIL: Component 3 — src/store.ts does not exist")
        else:
            with open(store_path, 'r') as f:
                store_content = f.read()

            checks = {
                'Store class': bool(re.search(r'class\s+Store', store_content)),
                'BehaviorSubject': 'BehaviorSubject' in store_content,
                'dispatch method': bool(re.search(r'dispatch\s*\(', store_content)),
                'select method': bool(re.search(r'select\s*[<(]', store_content)),
                'middleware': bool(re.search(r'[Mm]iddleware', store_content)),
            }

            passed = sum(1 for v in checks.values() if v)
            total_checks = len(checks)

            if passed == total_checks:
                print(f"PASS: Component 3 — store.ts has all required elements: {list(checks.keys())} (0.25 pts)")
                total_score += 0.25
            else:
                failed = [k for k, v in checks.items() if not v]
                print(f"FAIL: Component 3 — Missing in store.ts: {failed} ({passed}/{total_checks})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: src/operators.ts has debounceAction, retryWithBackoff, cacheLatest (0.15 points)
    try:
        ops_path = os.path.join(PROJECT, 'src', 'operators.ts')
        if not os.path.exists(ops_path):
            print("FAIL: Component 4 — src/operators.ts does not exist")
        else:
            with open(ops_path, 'r') as f:
                ops_content = f.read()

            required_operators = ['debounceAction', 'retryWithBackoff', 'cacheLatest']
            found_ops = []
            missing_ops = []
            for op in required_operators:
                # Check it's defined as a function/const (not just mentioned in comments)
                if re.search(rf'(function|const|export\s+function)\s+{op}', ops_content):
                    found_ops.append(op)
                else:
                    missing_ops.append(op)

            if len(found_ops) == len(required_operators):
                print(f"PASS: Component 4 — All 3 custom operators found: {found_ops} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — Missing operators: {missing_ops}, found: {found_ops}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: src/effects.ts has Effects class with ofType (0.10 points)
    try:
        effects_path = os.path.join(PROJECT, 'src', 'effects.ts')
        if not os.path.exists(effects_path):
            print("FAIL: Component 5 — src/effects.ts does not exist")
        else:
            with open(effects_path, 'r') as f:
                effects_content = f.read()

            has_effects_class = bool(re.search(r'class\s+Effects', effects_content))
            has_oftype = bool(re.search(r'(function|const|export\s+function)\s+ofType', effects_content))

            if has_effects_class and has_oftype:
                print(f"PASS: Component 5 — Effects class and ofType found (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — Effects class: {has_effects_class}, ofType: {has_oftype}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: src/demo/todoStore.ts demonstrates a TODO store (0.10 points)
    try:
        todo_path = os.path.join(PROJECT, 'src', 'demo', 'todoStore.ts')
        if not os.path.exists(todo_path):
            print("FAIL: Component 6 — src/demo/todoStore.ts does not exist")
        else:
            with open(todo_path, 'r') as f:
                todo_content = f.read()

            # Should import from store, have a reducer, and define todo-related types
            has_store_import = bool(re.search(r"from\s+['\"]\.\.\/store['\"]", todo_content) or
                                    re.search(r"from\s+['\"].*store['\"]", todo_content))
            has_reducer = bool(re.search(r'[Rr]educer', todo_content))
            has_todo_type = bool(re.search(r'(Todo|todo)', todo_content))
            has_state = bool(re.search(r'(TodoState|State)', todo_content))

            if has_store_import and has_reducer and has_todo_type:
                print(f"PASS: Component 6 — todoStore.ts has Store import, reducer, and Todo types (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 — store import: {has_store_import}, reducer: {has_reducer}, todo type: {has_todo_type}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: 20+ Jest tests across test files (0.15 points)
    try:
        tests_dir = os.path.join(PROJECT, '__tests__')
        # Also check for tests in other common locations
        test_locations = [tests_dir]
        alt_tests = os.path.join(PROJECT, 'tests')
        src_tests = os.path.join(PROJECT, 'src')
        if os.path.isdir(alt_tests):
            test_locations.append(alt_tests)

        total_test_count = 0
        test_files_found = []

        for test_dir in test_locations:
            if not os.path.isdir(test_dir):
                continue
            for root, dirs, files in os.walk(test_dir):
                for fname in files:
                    if fname.endswith(('.test.ts', '.test.js', '.spec.ts', '.spec.js')):
                        fpath = os.path.join(root, fname)
                        test_files_found.append(fpath)
                        with open(fpath, 'r') as f:
                            content = f.read()
                        # Count test/it blocks
                        test_matches = re.findall(r'\b(test|it)\s*\(', content)
                        total_test_count += len(test_matches)

        # Also scan src/ for inline test files
        if os.path.isdir(src_tests):
            for root, dirs, files in os.walk(src_tests):
                for fname in files:
                    if fname.endswith(('.test.ts', '.test.js', '.spec.ts', '.spec.js')):
                        fpath = os.path.join(root, fname)
                        if fpath not in test_files_found:
                            test_files_found.append(fpath)
                            with open(fpath, 'r') as f:
                                content = f.read()
                            test_matches = re.findall(r'\b(test|it)\s*\(', content)
                            total_test_count += len(test_matches)

        if total_test_count >= 20:
            print(f"PASS: Component 7 — {total_test_count} tests found across {len(test_files_found)} test files (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 7 — Only {total_test_count} tests found (need >= 20) in {len(test_files_found)} files: {test_files_found}")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {round(final_score, 2)}")
    return final_score


# Entry point
verify_task()
