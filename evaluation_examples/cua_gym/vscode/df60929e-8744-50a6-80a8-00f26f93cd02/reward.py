"""
Reward Script: Storybook development workflow setup in ~/project
Task ID: vscode_wf_075
Domain: vscode
Scoring:
  Component 1: .storybook/main.js with stories glob and addons (0.15)
  Component 2: .storybook/preview.js with decorators (0.15)
  Component 3: Button.stories.jsx with 4 story variants (0.30)
  Component 4: tasks.json with 3 storybook tasks (0.20)
  Component 5: launch.json with storybook debug config on port 6006 (0.20)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')


def verify_task():
    """
    Verify Storybook workflow setup with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: .storybook/main.js exists with stories glob and addons (0.15 points)
    try:
        main_js_path = os.path.join(PROJECT, '.storybook', 'main.js')
        if os.path.isfile(main_js_path):
            with open(main_js_path, 'r') as f:
                content = f.read()
            # Check for stories glob pattern (e.g., '../src/**/*.stories.@(js|jsx|ts|tsx)')
            has_stories_glob = bool(re.search(r'stories\s*:', content) and re.search(r'\*\*.*stories', content))
            # Check for addons array
            has_addons = bool(re.search(r'addons\s*:', content))
            if has_stories_glob and has_addons:
                print(f"PASS: Component 1 -- .storybook/main.js has stories glob and addons (0.15 pts)")
                total_score += 0.15
            elif has_stories_glob or has_addons:
                print(f"PARTIAL: Component 1 -- main.js has {'stories glob' if has_stories_glob else 'addons'} but missing {'addons' if has_stories_glob else 'stories glob'} (0.07 pts)")
                total_score += 0.07
            else:
                print(f"FAIL: Component 1 -- main.js missing both stories glob and addons")
        else:
            print(f"FAIL: Component 1 -- .storybook/main.js does not exist")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: .storybook/preview.js exists with decorators (0.15 points)
    try:
        preview_js_path = os.path.join(PROJECT, '.storybook', 'preview.js')
        if os.path.isfile(preview_js_path):
            with open(preview_js_path, 'r') as f:
                content = f.read()
            # Check for decorators definition
            has_decorators = bool(re.search(r'decorators\s*:', content))
            if has_decorators:
                print(f"PASS: Component 2 -- .storybook/preview.js has decorators (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 -- preview.js exists but missing decorators")
        else:
            print(f"FAIL: Component 2 -- .storybook/preview.js does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Button.stories.jsx with 4 story variants (0.30 points)
    # Variants required: Default, Primary, Disabled, Loading
    try:
        stories_path = os.path.join(PROJECT, 'src', 'components', 'Button.stories.jsx')
        if os.path.isfile(stories_path):
            with open(stories_path, 'r') as f:
                content = f.read()
            # Check for each required story variant export
            required_variants = ['Default', 'Primary', 'Disabled', 'Loading']
            found_variants = []
            for variant in required_variants:
                # Match export const Default = ... or export const Default
                if re.search(rf'export\s+(const|var|let|function)\s+{variant}\b', content):
                    found_variants.append(variant)
            variant_count = len(found_variants)
            missing = [v for v in required_variants if v not in found_variants]
            if variant_count == 4:
                print(f"PASS: Component 3 -- Button.stories.jsx has all 4 variants: {found_variants} (0.30 pts)")
                total_score += 0.30
            elif variant_count > 0:
                partial = round(0.30 * (variant_count / 4), 2)
                print(f"PARTIAL: Component 3 -- Found {variant_count}/4 variants: {found_variants}, missing: {missing} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 -- No required story variants found in Button.stories.jsx")
        else:
            print(f"FAIL: Component 3 -- Button.stories.jsx does not exist")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: tasks.json with storybook, build-storybook, test-storybook tasks (0.20 points)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        if os.path.isfile(tasks_path):
            with open(tasks_path, 'r') as f:
                # Handle JSONC (strip comments)
                raw = f.read()
                cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
                tasks_config = json.loads(cleaned)
            tasks = tasks_config.get('tasks', [])
            task_labels = [t.get('label', '') for t in tasks]
            required_tasks = ['storybook', 'build-storybook', 'test-storybook']
            found_tasks = []
            for req in required_tasks:
                # Case-insensitive label match
                if any(req.lower() == lbl.lower() for lbl in task_labels):
                    found_tasks.append(req)
            missing_tasks = [t for t in required_tasks if t not in found_tasks]
            if len(found_tasks) == 3:
                print(f"PASS: Component 4 -- tasks.json has all 3 required tasks: {found_tasks} (0.20 pts)")
                total_score += 0.20
            elif len(found_tasks) > 0:
                partial = round(0.20 * (len(found_tasks) / 3), 2)
                print(f"PARTIAL: Component 4 -- Found {len(found_tasks)}/3 tasks: {found_tasks}, missing: {missing_tasks} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 -- No required tasks found. Labels present: {task_labels}")
        else:
            print(f"FAIL: Component 4 -- .vscode/tasks.json does not exist")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: launch.json with storybook debug config on port 6006 (0.20 points)
    try:
        launch_path = os.path.join(PROJECT, '.vscode', 'launch.json')
        if os.path.isfile(launch_path):
            with open(launch_path, 'r') as f:
                raw = f.read()
            # Strip comments and handle VSCode variables like ${workspaceFolder}
            cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
            # Try JSON parse; fall back to raw text search if it fails
            try:
                launch_config = json.loads(cleaned)
                configs = launch_config.get('configurations', [])
                has_storybook_debug = any('6006' in cfg.get('url', '') for cfg in configs)
            except json.JSONDecodeError:
                # JSON parse failed (e.g., ${workspaceFolder} not valid JSON)
                # Fall back to raw content check
                has_storybook_debug = '6006' in raw
            if has_storybook_debug:
                print(f"PASS: Component 5 -- launch.json has storybook debug config on port 6006 (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 5 -- launch.json exists but no config targeting port 6006")
        else:
            print(f"FAIL: Component 5 -- .vscode/launch.json does not exist")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
