"""
Reward Script: VSCode tasks.json with parallel Build All and sequential Test All
Task ID: vscode_gf2_043
Domain: vscode
Scoring:
  Component 1 (0.15): tasks.json exists and is valid JSON with correct version
  Component 2 (0.35): Three individual build tasks with npm run build and correct cwd per package
  Component 3 (0.30): Build All compound task with dependsOrder parallel and correct dependsOn
  Component 4 (0.20): Test All task that depends on Build All
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_043'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'monorepo', '.vscode', 'tasks.json')

REQUIRED_PACKAGES = {'auth', 'api', 'ui'}


def load_tasks_json(file_path):
    """Load tasks.json, handling JSONC (comments)."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments for JSONC compatibility
    cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(cleaned)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: tasks.json exists, is valid JSON, has version 2.0.0 (0.15 points)
    try:
        data = load_tasks_json(file_path)
        if isinstance(data, dict) and data.get('version') == '2.0.0':
            print(f"PASS: Component 1 -- tasks.json is valid JSON with version 2.0.0 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Expected version '2.0.0', found: {data.get('version') if isinstance(data, dict) else 'not a dict'}")
            # Cannot continue without valid structure
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 -- Cannot parse tasks.json: {e}")
        print(f"REWARD: 0.0")
        return 0.0

    tasks = data.get('tasks', [])
    if not isinstance(tasks, list):
        print(f"FAIL: 'tasks' field is not a list")
        print(f"REWARD: {total_score}")
        return total_score

    # Build a lookup by label for convenience
    tasks_by_label = {}
    for t in tasks:
        label = t.get('label', '')
        if label:
            tasks_by_label[label.lower().strip()] = t

    # Component 2: Three individual build tasks with npm run build and correct cwd (0.35 points)
    # Each package contributes ~0.117 points. We need all three for full marks but give partial.
    try:
        packages_found = set()
        for t in tasks:
            label = (t.get('label') or '').lower()
            command = (t.get('command') or '').strip()
            cwd = ''
            if isinstance(t.get('options'), dict):
                cwd = (t['options'].get('cwd') or '').strip()

            # Check if this task runs npm run build
            if 'npm' in command and 'build' in command:
                # Check which package cwd points to
                for pkg in REQUIRED_PACKAGES:
                    # Accept various cwd patterns:
                    # ${workspaceFolder}/packages/auth, ./packages/auth, packages/auth, etc.
                    if f'packages/{pkg}' in cwd or f'packages\\{pkg}' in cwd:
                        packages_found.add(pkg)

        per_pkg_score = 0.35 / 3.0
        pkg_score = len(packages_found) * per_pkg_score
        if packages_found == REQUIRED_PACKAGES:
            print(f"PASS: Component 2 -- All 3 build tasks found with correct cwd (auth, api, ui) (0.35 pts)")
            total_score += 0.35
        elif len(packages_found) > 0:
            print(f"PARTIAL: Component 2 -- Found build tasks for {packages_found}, missing {REQUIRED_PACKAGES - packages_found} ({pkg_score:.3f} pts)")
            total_score += pkg_score
        else:
            print(f"FAIL: Component 2 -- No individual build tasks with correct cwd found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Build All compound task with dependsOrder parallel (0.30 points)
    try:
        build_all = None
        for t in tasks:
            label = (t.get('label') or '').strip()
            if label.lower() == 'build all':
                build_all = t
                break

        if build_all is None:
            print(f"FAIL: Component 3 -- No task with label 'Build All' found")
        else:
            depends_on = build_all.get('dependsOn', [])
            depends_order = (build_all.get('dependsOrder') or '').lower().strip()

            # Check dependsOrder is parallel
            has_parallel = depends_order == 'parallel'
            # Check it depends on 3 tasks (the individual build tasks)
            has_three_deps = isinstance(depends_on, list) and len(depends_on) >= 3

            if has_parallel and has_three_deps:
                print(f"PASS: Component 3 -- Build All has dependsOrder=parallel with {len(depends_on)} dependencies (0.30 pts)")
                total_score += 0.30
            elif has_parallel and not has_three_deps:
                print(f"PARTIAL: Component 3 -- Build All has dependsOrder=parallel but only {len(depends_on) if isinstance(depends_on, list) else 0} dependencies (0.15 pts)")
                total_score += 0.15
            elif not has_parallel and has_three_deps:
                print(f"PARTIAL: Component 3 -- Build All has {len(depends_on)} dependencies but dependsOrder is '{depends_order}' not 'parallel' (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 -- Build All missing both parallel order and proper dependencies")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Test All task depends on Build All (0.20 points)
    try:
        test_all = None
        for t in tasks:
            label = (t.get('label') or '').strip()
            if label.lower() == 'test all':
                test_all = t
                break

        if test_all is None:
            print(f"FAIL: Component 4 -- No task with label 'Test All' found")
        else:
            depends_on = test_all.get('dependsOn', [])
            # Check if it depends on Build All
            depends_on_lower = [d.lower().strip() if isinstance(d, str) else '' for d in depends_on] if isinstance(depends_on, list) else []
            if 'build all' in depends_on_lower:
                print(f"PASS: Component 4 -- Test All depends on Build All (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 -- Test All dependsOn={depends_on}, expected to include 'Build All'")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(TASKS_JSON_PATH):
    print(f"File not found: {TASKS_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(TASKS_JSON_PATH)
