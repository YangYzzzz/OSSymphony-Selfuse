"""
Reward Script: Convert JavaScript project to TypeScript
Task ID: vscode_wf_074
Domain: vscode
Scoring:
  Component 1: .js files renamed to .ts (0.20 pts)
  Component 2: tsconfig.json with strict configuration (0.20 pts)
  Component 3: devDependencies (typescript, @types/node) (0.20 pts)
  Component 4: Type annotations present in .ts files (0.20 pts)
  Component 5: tasks.json with build and watch tasks (0.20 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'project')
SRC_DIR = os.path.join(PROJECT_DIR, 'src')
TASK_ID = 'vscode_wf_074'


def load_json_file(path):
    """Load a JSON file, stripping JSONC comments if needed."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(cleaned)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: .js files renamed to .ts (0.20 points)
    # In initial_env: index.js, utils.js, api.js exist. In golden_env: index.ts, utils.ts, api.ts exist.
    try:
        expected_ts = ['index.ts', 'utils.ts', 'api.ts']
        forbidden_js = ['index.js', 'utils.js', 'api.js']

        ts_exist = all(os.path.isfile(os.path.join(SRC_DIR, f)) for f in expected_ts)
        js_absent = all(not os.path.isfile(os.path.join(SRC_DIR, f)) for f in forbidden_js)

        if ts_exist and js_absent:
            print(f"PASS: Component 1 — All .ts files exist, no .js files remain (0.20 pts)")
            total_score += 0.20
        else:
            existing_ts = [f for f in expected_ts if os.path.isfile(os.path.join(SRC_DIR, f))]
            remaining_js = [f for f in forbidden_js if os.path.isfile(os.path.join(SRC_DIR, f))]
            print(f"FAIL: Component 1 — .ts present: {existing_ts}, .js remaining: {remaining_js}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: tsconfig.json with strict configuration (0.20 points)
    # Must have strict: true, target: ES2020, module: commonjs
    try:
        tsconfig_path = os.path.join(PROJECT_DIR, 'tsconfig.json')
        if os.path.isfile(tsconfig_path):
            tsconfig = load_json_file(tsconfig_path)
            opts = tsconfig.get('compilerOptions', {})

            strict_ok = opts.get('strict') is True
            target_ok = str(opts.get('target', '')).upper() == 'ES2020'
            module_ok = str(opts.get('module', '')).lower() == 'commonjs'

            if strict_ok and target_ok and module_ok:
                print(f"PASS: Component 2 — tsconfig.json has strict:true, target:ES2020, module:commonjs (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — strict={opts.get('strict')}, target={opts.get('target')}, module={opts.get('module')}")
        else:
            print(f"FAIL: Component 2 — tsconfig.json not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: devDependencies contain typescript and @types/node (0.20 points)
    # In initial_env: no devDependencies. In golden_env: typescript and @types/node present.
    try:
        pkg_path = os.path.join(PROJECT_DIR, 'package.json')
        if os.path.isfile(pkg_path):
            pkg = load_json_file(pkg_path)
            dev_deps = pkg.get('devDependencies', {})

            has_typescript = 'typescript' in dev_deps
            has_types_node = '@types/node' in dev_deps

            if has_typescript and has_types_node:
                print(f"PASS: Component 3 — devDependencies has typescript and @types/node (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — typescript={has_typescript}, @types/node={has_types_node}, devDeps={list(dev_deps.keys())}")
        else:
            print(f"FAIL: Component 3 — package.json not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Type annotations present in .ts files (0.20 points)
    # Golden .ts files have TypeScript-specific syntax (interfaces, type annotations, generics)
    # Initial .js files have none of these. We check for TypeScript patterns in all three files.
    try:
        ts_files = ['index.ts', 'utils.ts', 'api.ts']
        # Patterns that indicate TypeScript type annotations (not present in plain JS)
        ts_patterns = [
            r':\s*(string|number|boolean|void|any|unknown|never)\b',  # type annotations
            r'\binterface\s+\w+',  # interface declarations
            r'<\w+(?:\[\])?(?:,\s*\w+)*>',  # generics
            r':\s*\w+\[\]',  # array type annotations
            r':\s*Promise<',  # Promise type
            r'\bexport\s+interface\b',  # exported interfaces
            r'as\s+\w+',  # type assertions
        ]

        files_with_types = 0
        for ts_file in ts_files:
            ts_path = os.path.join(SRC_DIR, ts_file)
            if os.path.isfile(ts_path):
                with open(ts_path, 'r') as f:
                    content = f.read()
                for pattern in ts_patterns:
                    if re.search(pattern, content):
                        files_with_types += 1
                        break

        if files_with_types == 3:
            print(f"PASS: Component 4 — All 3 .ts files contain TypeScript type annotations (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Only {files_with_types}/3 files have type annotations")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: tasks.json with build (tsc) and watch (tsc -w) tasks (0.20 points)
    # In initial_env: no .vscode/tasks.json. In golden_env: tasks.json with build and watch tasks.
    try:
        tasks_path = os.path.join(PROJECT_DIR, '.vscode', 'tasks.json')
        if os.path.isfile(tasks_path):
            tasks_config = load_json_file(tasks_path)
            tasks_list = tasks_config.get('tasks', [])

            # Check for build task: label contains 'build' and command is 'tsc'
            has_build = any(
                'build' in str(t.get('label', '')).lower() and 'tsc' in str(t.get('command', '')).lower()
                for t in tasks_list
            )

            # Check for watch task: label contains 'watch', command is 'tsc', args include '-w'
            has_watch = any(
                'watch' in str(t.get('label', '')).lower()
                and 'tsc' in str(t.get('command', '')).lower()
                and '-w' in [str(a).lower() for a in t.get('args', [])]
                for t in tasks_list
            )

            if has_build and has_watch:
                print(f"PASS: Component 5 — tasks.json has build (tsc) and watch (tsc -w) tasks (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 5 — build={has_build}, watch={has_watch}")
        else:
            print(f"FAIL: Component 5 — .vscode/tasks.json not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

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
