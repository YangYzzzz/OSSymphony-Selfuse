"""
Reward Script: TypeScript project setup in VSCode
Task ID: vscode_wf_040
Domain: vscode
Scoring:
  1. package.json with typescript + ts-node devDependencies (0.15)
  2. tsconfig.json with strict, ES2020, outDir, rootDir (0.20)
  3. src/index.ts exists with typed function (0.15)
  4. .vscode/tasks.json with build and watch tasks (0.20)
  5. .vscode/launch.json with ts-node debug config (0.15)
  6. .vscode/extensions.json recommending TypeScript extension (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
TASK_ID = 'vscode_wf_040'


def load_json_file(path):
    """Load a JSON file, handling JSONC (comments)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments for JSONC support
    stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(stripped)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: package.json with typescript + ts-node in devDependencies (0.15 points)
    try:
        pkg_path = os.path.join(PROJECT, 'package.json')
        pkg = load_json_file(pkg_path)
        dev_deps = pkg.get('devDependencies', {})
        has_ts = 'typescript' in dev_deps
        has_tsnode = 'ts-node' in dev_deps
        if has_ts and has_tsnode:
            print(f"PASS: Component 1 - package.json has typescript and ts-node in devDependencies (0.15 pts)")
            total_score += 0.15
        else:
            missing = []
            if not has_ts:
                missing.append('typescript')
            if not has_tsnode:
                missing.append('ts-node')
            print(f"FAIL: Component 1 - Missing devDependencies: {missing}")
    except FileNotFoundError:
        print(f"FAIL: Component 1 - package.json not found at {pkg_path}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: tsconfig.json with strict:true, target:ES2020, outDir:./dist, rootDir:./src (0.20 points)
    try:
        tsconfig_path = os.path.join(PROJECT, 'tsconfig.json')
        tsconfig = load_json_file(tsconfig_path)
        compiler = tsconfig.get('compilerOptions', {})

        checks = {
            'strict': compiler.get('strict') is True,
            'target_ES2020': str(compiler.get('target', '')).upper() == 'ES2020',
            'outDir': compiler.get('outDir', '').rstrip('/') == './dist',
            'rootDir': compiler.get('rootDir', '').rstrip('/') == './src',
        }
        passed = sum(1 for v in checks.values() if v)

        if passed == 4:
            print(f"PASS: Component 2 - tsconfig.json has all required compilerOptions (0.20 pts)")
            total_score += 0.20
        elif passed >= 2:
            partial = 0.10
            print(f"PARTIAL: Component 2 - tsconfig.json has {passed}/4 required options ({partial} pts). Failed: {[k for k,v in checks.items() if not v]}")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - tsconfig.json missing required options. Status: {checks}")
    except FileNotFoundError:
        print(f"FAIL: Component 2 - tsconfig.json not found at {tsconfig_path}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: src/index.ts exists with a typed function (0.15 points)
    try:
        index_path = os.path.join(PROJECT, 'src', 'index.ts')
        with open(index_path, 'r') as f:
            ts_content = f.read()

        # Check for TypeScript type annotations (: type patterns in function params/returns)
        has_type_annotation = bool(re.search(r':\s*(string|number|boolean|void|any|object|User|\w+\[\])', ts_content))
        has_function = bool(re.search(r'function\s+\w+', ts_content))

        if has_type_annotation and has_function:
            print(f"PASS: Component 3 - src/index.ts exists with typed function (0.15 pts)")
            total_score += 0.15
        elif has_function:
            print(f"PARTIAL: Component 3 - src/index.ts has function but no type annotations (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 3 - src/index.ts missing typed function. has_function={has_function}, has_type_annotation={has_type_annotation}")
    except FileNotFoundError:
        print(f"FAIL: Component 3 - src/index.ts not found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: .vscode/tasks.json with 'build' (tsc) and 'watch' (tsc -w) tasks (0.20 points)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        tasks_config = load_json_file(tasks_path)
        tasks_list = tasks_config.get('tasks', [])

        has_build = False
        has_watch = False

        for task in tasks_list:
            label = str(task.get('label', '')).lower()
            command = str(task.get('command', '')).lower()
            args = [str(a).lower() for a in task.get('args', [])]

            # Build task: label contains 'build', command is tsc
            if 'build' in label and 'tsc' in command:
                has_build = True

            # Watch task: label contains 'watch', uses tsc with -w flag
            if 'watch' in label:
                if 'tsc' in command and '-w' in args:
                    has_watch = True
                elif 'tsc -w' in command or 'tsc --watch' in command:
                    has_watch = True

        if has_build and has_watch:
            print(f"PASS: Component 4 - tasks.json has build and watch tasks (0.20 pts)")
            total_score += 0.20
        elif has_build or has_watch:
            print(f"PARTIAL: Component 4 - tasks.json has build={has_build}, watch={has_watch} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 - tasks.json missing build and watch tasks. Found labels: {[t.get('label') for t in tasks_list]}")
    except FileNotFoundError:
        print(f"FAIL: Component 4 - tasks.json not found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: .vscode/launch.json with ts-node debug config (0.15 points)
    try:
        launch_path = os.path.join(PROJECT, '.vscode', 'launch.json')
        launch_config = load_json_file(launch_path)
        configs = launch_config.get('configurations', [])

        has_tsnode_debug = False
        for cfg in configs:
            runtime_args = cfg.get('runtimeArgs', [])
            # Check for ts-node/register in runtimeArgs
            if 'ts-node/register' in runtime_args:
                has_tsnode_debug = True
                break
            # Also check as joined string
            if any('ts-node' in str(a) for a in runtime_args):
                has_tsnode_debug = True
                break

        if has_tsnode_debug:
            print(f"PASS: Component 5 - launch.json has ts-node debug configuration (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 - launch.json missing ts-node debug config. Configs: {[c.get('name') for c in configs]}")
    except FileNotFoundError:
        print(f"FAIL: Component 5 - launch.json not found")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: .vscode/extensions.json recommending TypeScript extension (0.15 points)
    try:
        ext_path = os.path.join(PROJECT, '.vscode', 'extensions.json')
        ext_config = load_json_file(ext_path)
        recommendations = ext_config.get('recommendations', [])

        has_ts_ext = any('typescript' in str(r).lower() for r in recommendations)

        if has_ts_ext:
            print(f"PASS: Component 6 - extensions.json recommends TypeScript extension (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 - extensions.json missing TypeScript recommendation. Found: {recommendations}")
    except FileNotFoundError:
        print(f"FAIL: Component 6 - extensions.json not found")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
