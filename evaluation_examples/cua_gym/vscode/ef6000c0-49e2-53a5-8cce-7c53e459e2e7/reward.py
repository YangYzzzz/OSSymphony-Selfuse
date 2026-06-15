"""
Reward Script: Monorepo workspace configuration verification
Task ID: vscode_wf_047
Domain: vscode
Scoring:
  Component 1 (0.25): Workspace file exists with 3 folder entries (shared, api, web)
  Component 2 (0.20): Workspace has per-folder settings (formatters/linters)
  Component 3 (0.25): tasks.json has build:shared, build:api, build:web, build:all
  Component 4 (0.15): build:all uses dependsOn with correct dependency ordering
  Component 5 (0.15): extensions.json recommends TypeScript, ESLint, Prettier
"""

import os
import json
import re
import glob

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
TASK_ID = 'vscode_wf_047'


def load_json_file(path):
    """Load a JSON file, stripping JSONC comments if needed."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_workspace_file():
    """Find a .code-workspace file in the project directory."""
    pattern = os.path.join(PROJECT, '*.code-workspace')
    matches = glob.glob(pattern)
    if matches:
        return matches[0]
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # =========================================================================
    # Component 1: Workspace file with 3 folder entries (0.25 points)
    # =========================================================================
    ws_data = None
    try:
        ws_path = find_workspace_file()
        if ws_path is None:
            print("FAIL: Component 1 -- No .code-workspace file found in ~/project/")
        else:
            ws_data = load_json_file(ws_path)
            folders = ws_data.get('folders', [])
            folder_paths = [f.get('path', '') for f in folders]

            # Normalize paths - check that all three package folders are referenced
            has_shared = any('shared' in p for p in folder_paths)
            has_api = any('api' in p for p in folder_paths)
            has_web = any('web' in p for p in folder_paths)

            if len(folders) >= 3 and has_shared and has_api and has_web:
                print(f"PASS: Component 1 -- Workspace has {len(folders)} folders: {folder_paths} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 -- Expected 3 folders (shared, api, web), found: {folder_paths}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # =========================================================================
    # Component 2: Workspace has per-folder settings (0.20 points)
    # Checks that workspace-level settings include formatter/linter config
    # =========================================================================
    try:
        if ws_data is None:
            print("FAIL: Component 2 -- No workspace data to check settings")
        else:
            settings = ws_data.get('settings', {})
            checks_passed = 0
            total_checks = 3

            # Check 1: Has some formatter setting
            has_formatter = (
                'editor.defaultFormatter' in settings
                or any('defaultFormatter' in str(v) for k, v in settings.items() if isinstance(v, dict))
            )
            if has_formatter:
                checks_passed += 1
                print("  PASS: Workspace has formatter settings")
            else:
                print("  FAIL: No formatter settings found in workspace")

            # Check 2: Has TypeScript-related settings
            has_ts_settings = (
                'typescript.tsdk' in settings
                or any('typescript' in k.lower() for k in settings)
                or '[typescript]' in settings
                or '[typescriptreact]' in settings
            )
            if has_ts_settings:
                checks_passed += 1
                print("  PASS: Workspace has TypeScript settings")
            else:
                print("  FAIL: No TypeScript settings found")

            # Check 3: Has ESLint or linting config
            has_linting = (
                'eslint.validate' in settings
                or any('eslint' in k.lower() for k in settings)
                or any('codeActionsOnSave' in str(v) for v in settings.values() if isinstance(v, dict))
            )
            if has_linting:
                checks_passed += 1
                print("  PASS: Workspace has linting settings")
            else:
                print("  FAIL: No linting settings found")

            if checks_passed >= 2:
                score = 0.20
                print(f"PASS: Component 2 -- Workspace settings ({checks_passed}/{total_checks} checks) ({score} pts)")
                total_score += score
            else:
                print(f"FAIL: Component 2 -- Only {checks_passed}/{total_checks} setting checks passed")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # =========================================================================
    # Component 3: tasks.json has the 4 required build tasks (0.25 points)
    # =========================================================================
    tasks_data = None
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        if not os.path.exists(tasks_path):
            print("FAIL: Component 3 -- .vscode/tasks.json not found")
        else:
            tasks_data = load_json_file(tasks_path)
            tasks = tasks_data.get('tasks', [])
            task_labels = [t.get('label', '') for t in tasks]

            required_tasks = ['build:shared', 'build:api', 'build:web', 'build:all']
            found_tasks = [rt for rt in required_tasks if any(rt in label for label in task_labels)]
            missing_tasks = [rt for rt in required_tasks if rt not in found_tasks]

            if len(found_tasks) == 4:
                print(f"PASS: Component 3 -- All 4 build tasks found: {found_tasks} (0.25 pts)")
                total_score += 0.25
            elif len(found_tasks) >= 2:
                partial = round(0.25 * len(found_tasks) / 4, 2)
                print(f"PARTIAL: Component 3 -- Found {len(found_tasks)}/4 tasks: {found_tasks}, missing: {missing_tasks} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 -- Found {len(found_tasks)}/4 required tasks. Labels: {task_labels}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # =========================================================================
    # Component 4: build:all uses dependsOn with correct ordering (0.15 points)
    # shared must build before api and web; api and web can be parallel
    # =========================================================================
    try:
        if tasks_data is None:
            print("FAIL: Component 4 -- No tasks.json data")
        else:
            tasks = tasks_data.get('tasks', [])
            build_all = None
            build_api = None
            build_web = None
            for t in tasks:
                label = t.get('label', '')
                if label == 'build:all':
                    build_all = t
                elif label == 'build:api':
                    build_api = t
                elif label == 'build:web':
                    build_web = t

            if build_all is None:
                print("FAIL: Component 4 -- build:all task not found")
            else:
                depends_on = build_all.get('dependsOn', [])
                has_depends = len(depends_on) > 0

                # Check dependency ordering: shared must be built before api/web
                # This can be achieved in two ways:
                # 1) build:all depends on build:api + build:web, which each depend on build:shared
                # 2) build:all depends on build:shared, build:api, build:web with explicit ordering

                # Check if api and web depend on shared (indirect ordering)
                api_depends_shared = False
                web_depends_shared = False
                if build_api:
                    api_deps = build_api.get('dependsOn', [])
                    api_depends_shared = any('shared' in str(d) for d in api_deps)
                if build_web:
                    web_deps = build_web.get('dependsOn', [])
                    web_depends_shared = any('shared' in str(d) for d in web_deps)

                # build:all has dependsOn AND proper ordering exists
                if has_depends and (api_depends_shared or web_depends_shared):
                    print(f"PASS: Component 4 -- build:all has dependsOn={depends_on}, api depends_shared={api_depends_shared}, web depends_shared={web_depends_shared} (0.15 pts)")
                    total_score += 0.15
                elif has_depends:
                    # Has dependsOn but ordering might not be explicit
                    print(f"PARTIAL: Component 4 -- build:all has dependsOn={depends_on} but dependency ordering unclear (0.08 pts)")
                    total_score += 0.08
                else:
                    print(f"FAIL: Component 4 -- build:all has no dependsOn")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # =========================================================================
    # Component 5: extensions.json recommends TS, ESLint, Prettier (0.15 points)
    # =========================================================================
    try:
        # Check .vscode/extensions.json
        ext_path = os.path.join(PROJECT, '.vscode', 'extensions.json')
        # Also check workspace file for embedded extensions recommendations
        ext_recs = []

        if os.path.exists(ext_path):
            ext_data = load_json_file(ext_path)
            ext_recs = ext_data.get('recommendations', [])
        elif ws_data and 'extensions' in ws_data:
            ext_recs = ws_data['extensions'].get('recommendations', [])

        if not ext_recs:
            print("FAIL: Component 5 -- No extension recommendations found")
        else:
            ext_recs_lower = [e.lower() for e in ext_recs]

            # Check for TypeScript extension
            has_ts = any('typescript' in e for e in ext_recs_lower)
            # Check for ESLint extension
            has_eslint = any('eslint' in e for e in ext_recs_lower)
            # Check for Prettier extension
            has_prettier = any('prettier' in e for e in ext_recs_lower)

            found_count = sum([has_ts, has_eslint, has_prettier])

            if found_count == 3:
                print(f"PASS: Component 5 -- All 3 recommended extensions found: {ext_recs} (0.15 pts)")
                total_score += 0.15
            elif found_count >= 1:
                partial = round(0.15 * found_count / 3, 2)
                print(f"PARTIAL: Component 5 -- {found_count}/3 extensions found (ts={has_ts}, eslint={has_eslint}, prettier={has_prettier}): {ext_recs} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 -- None of TypeScript/ESLint/Prettier found in {ext_recs}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
