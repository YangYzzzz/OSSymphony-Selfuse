"""
Reward Script: VSCode project scaffolding workflow verification
Task ID: vscode_wf_067
Domain: vscode
Scoring:
  Component 1 (0.25): Directory structure with .gitkeep files
  Component 2 (0.15): Git initialized with comprehensive .gitignore
  Component 3 (0.20): Config files (.editorconfig, .prettierrc, .eslintrc.json)
  Component 4 (0.15): .vscode/settings.json with TypeScript React settings
  Component 5 (0.10): .vscode/tasks.json with build, test, lint tasks
  Component 6 (0.10): .vscode/launch.json with Chrome debug config
  Component 7 (0.05): .vscode/extensions.json with recommended extensions
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
TASK_ID = 'vscode_wf_067'


def load_json_file(path):
    """Load a JSON file, stripping JSONC comments if needed."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip JSONC comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Fallback: try with strict=False to handle control characters
        return json.loads(content, strict=False)


def is_subset(expected, actual):
    """Check that expected is a subset of actual (recursive for dicts)."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        if not isinstance(actual, list):
            return False
        # Check all expected items are in actual
        return all(item in actual for item in expected)
    return expected == actual


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: ~/project must exist
    if not os.path.isdir(PROJECT):
        print(f"CRITICAL: Project directory {PROJECT} does not exist")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Directory structure with .gitkeep files (0.25 points)
    try:
        expected_dirs = [
            'src/components',
            'src/utils',
            'src/services',
            'src/hooks',
            'tests/unit',
            'tests/integration',
            'public',
            'docs',
        ]
        expected_gitkeeps = [
            'src/components/.gitkeep',
            'src/utils/.gitkeep',
            'src/services/.gitkeep',
            'src/hooks/.gitkeep',
            'tests/unit/.gitkeep',
            'tests/integration/.gitkeep',
            'public/.gitkeep',
            'docs/.gitkeep',
        ]

        dirs_found = 0
        for d in expected_dirs:
            full = os.path.join(PROJECT, d)
            if os.path.isdir(full):
                dirs_found += 1
            else:
                print(f"FAIL: Directory missing: {d}")

        gitkeeps_found = 0
        for gk in expected_gitkeeps:
            full = os.path.join(PROJECT, gk)
            if os.path.isfile(full):
                gitkeeps_found += 1
            else:
                print(f"FAIL: .gitkeep missing: {gk}")

        # Score: proportional to dirs + gitkeeps found
        dir_ratio = dirs_found / len(expected_dirs)
        gk_ratio = gitkeeps_found / len(expected_gitkeeps)
        comp1_score = 0.25 * (0.5 * dir_ratio + 0.5 * gk_ratio)
        if comp1_score > 0:
            print(f"PASS: Component 1 — {dirs_found}/{len(expected_dirs)} dirs, {gitkeeps_found}/{len(expected_gitkeeps)} .gitkeeps ({comp1_score:.3f} pts)")
            total_score += comp1_score
        else:
            print(f"FAIL: Component 1 — no expected directories or .gitkeep files found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Git initialized with comprehensive .gitignore (0.15 points)
    try:
        git_dir = os.path.join(PROJECT, '.git')
        gitignore_path = os.path.join(PROJECT, '.gitignore')

        git_init_ok = os.path.isdir(git_dir) and os.path.isfile(os.path.join(git_dir, 'HEAD'))
        gitignore_ok = False

        if os.path.isfile(gitignore_path):
            with open(gitignore_path, 'r') as f:
                gitignore_content = f.read()
            # Check for key patterns that should be in a comprehensive .gitignore
            required_patterns = ['node_modules', '.env', 'build', 'coverage']
            patterns_found = sum(1 for p in required_patterns if p in gitignore_content)
            if patterns_found >= 3:
                gitignore_ok = True

        comp2_score = 0.0
        if git_init_ok and gitignore_ok:
            comp2_score = 0.15
            print(f"PASS: Component 2 — Git initialized with comprehensive .gitignore ({comp2_score} pts)")
        elif git_init_ok:
            comp2_score = 0.07
            print(f"PARTIAL: Component 2 — Git initialized but .gitignore incomplete ({comp2_score} pts)")
        else:
            print(f"FAIL: Component 2 — Git not initialized or .gitignore missing")

        total_score += comp2_score
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Config files (.editorconfig, .prettierrc, .eslintrc.json) (0.20 points)
    try:
        comp3_score = 0.0

        # .editorconfig - must exist and contain meaningful config
        ec_path = os.path.join(PROJECT, '.editorconfig')
        if os.path.isfile(ec_path):
            with open(ec_path, 'r') as f:
                ec_content = f.read()
            if 'root' in ec_content or 'indent' in ec_content or 'charset' in ec_content or 'trim_trailing' in ec_content:
                comp3_score += 0.065
                print(f"PASS: .editorconfig exists with config content")
            else:
                print(f"FAIL: .editorconfig exists but has no meaningful config")
        else:
            print(f"FAIL: .editorconfig missing")

        # .prettierrc - must be valid JSON with config keys
        pr_path = os.path.join(PROJECT, '.prettierrc')
        if os.path.isfile(pr_path):
            try:
                pr_data = load_json_file(pr_path)
                if isinstance(pr_data, dict) and len(pr_data) >= 2:
                    comp3_score += 0.065
                    print(f"PASS: .prettierrc exists with {len(pr_data)} settings")
                else:
                    print(f"FAIL: .prettierrc exists but has insufficient config")
            except Exception as pe:
                print(f"FAIL: .prettierrc is not valid JSON: {pe}")
        else:
            print(f"FAIL: .prettierrc missing")

        # .eslintrc.json - must have extends, parser or plugins for React TS
        eslint_path = os.path.join(PROJECT, '.eslintrc.json')
        if os.path.isfile(eslint_path):
            try:
                eslint_data = load_json_file(eslint_path)
                has_react = False
                has_typescript = False

                # Check extends, plugins, or parser for React + TypeScript references
                eslint_str = json.dumps(eslint_data).lower()
                if 'react' in eslint_str:
                    has_react = True
                if 'typescript' in eslint_str:
                    has_typescript = True

                if has_react and has_typescript:
                    comp3_score += 0.07
                    print(f"PASS: .eslintrc.json configured for React + TypeScript")
                elif has_react or has_typescript:
                    comp3_score += 0.035
                    print(f"PARTIAL: .eslintrc.json has {'React' if has_react else 'TypeScript'} but missing {'TypeScript' if has_react else 'React'}")
                else:
                    print(f"FAIL: .eslintrc.json missing React/TypeScript configuration")
            except Exception as ee:
                print(f"FAIL: .eslintrc.json is not valid JSON: {ee}")
        else:
            print(f"FAIL: .eslintrc.json missing")

        if comp3_score > 0:
            print(f"PASS: Component 3 — config files ({comp3_score:.3f} pts)")
        total_score += comp3_score
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: .vscode/settings.json with TypeScript React settings (0.15 points)
    try:
        settings_path = os.path.join(PROJECT, '.vscode', 'settings.json')
        comp4_score = 0.0

        if os.path.isfile(settings_path):
            settings = load_json_file(settings_path)
            checks_passed = 0
            total_checks = 4

            # Check for TypeScript-related settings
            settings_str = json.dumps(settings).lower()
            if 'typescript' in settings_str:
                checks_passed += 1
                print(f"  PASS: settings.json has TypeScript settings")
            else:
                print(f"  FAIL: settings.json missing TypeScript settings")

            # Check for formatter settings
            if 'editor.formatonsave' in {k.lower() for k in settings.keys()} or 'editor.defaultformatter' in {k.lower() for k in settings.keys()}:
                checks_passed += 1
                print(f"  PASS: settings.json has formatter settings")
            else:
                # Check case-sensitive too
                if 'editor.formatOnSave' in settings or 'editor.defaultFormatter' in settings:
                    checks_passed += 1
                    print(f"  PASS: settings.json has formatter settings")
                else:
                    print(f"  FAIL: settings.json missing formatter settings")

            # Check for React-related (emmet, jsx, etc.)
            if 'emmet' in settings_str or 'react' in settings_str or 'jsx' in settings_str or 'typescriptreact' in settings_str:
                checks_passed += 1
                print(f"  PASS: settings.json has React-related settings")
            else:
                print(f"  FAIL: settings.json missing React-related settings")

            # Check for tab/indent settings
            if 'editor.tabsize' in settings_str or 'editor.tabSize' in settings:
                checks_passed += 1
                print(f"  PASS: settings.json has tab size settings")
            else:
                print(f"  FAIL: settings.json missing tab size settings")

            comp4_score = 0.15 * (checks_passed / total_checks)
            print(f"PASS: Component 4 — {checks_passed}/{total_checks} settings checks ({comp4_score:.3f} pts)")
        else:
            print(f"FAIL: Component 4 — .vscode/settings.json missing")

        total_score += comp4_score
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: .vscode/tasks.json with build, test, lint tasks (0.10 points)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        comp5_score = 0.0

        if os.path.isfile(tasks_path):
            tasks_data = load_json_file(tasks_path)
            task_labels = []
            if 'tasks' in tasks_data and isinstance(tasks_data['tasks'], list):
                task_labels = [t.get('label', '').lower() for t in tasks_data['tasks']]

            required_tasks = ['build', 'test', 'lint']
            tasks_found = sum(1 for rt in required_tasks if any(rt in label for label in task_labels))

            comp5_score = 0.10 * (tasks_found / len(required_tasks))
            if tasks_found == len(required_tasks):
                print(f"PASS: Component 5 — All 3 tasks (build, test, lint) found ({comp5_score:.3f} pts)")
            elif tasks_found > 0:
                print(f"PARTIAL: Component 5 — {tasks_found}/{len(required_tasks)} tasks found ({comp5_score:.3f} pts)")
            else:
                print(f"FAIL: Component 5 — No required tasks found in tasks.json")
        else:
            print(f"FAIL: Component 5 — .vscode/tasks.json missing")

        total_score += comp5_score
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: .vscode/launch.json with Chrome debug config (0.10 points)
    try:
        launch_path = os.path.join(PROJECT, '.vscode', 'launch.json')
        comp6_score = 0.0

        if os.path.isfile(launch_path):
            # launch.json may contain VSCode variables like ${workspaceFolder}
            # which can cause JSON parse errors, so read as text for verification
            with open(launch_path, 'r') as f:
                launch_content = f.read().lower()

            has_chrome = 'chrome' in launch_content
            has_configurations = '"configurations"' in launch_content
            has_localhost = 'localhost' in launch_content

            if has_chrome and has_configurations:
                comp6_score = 0.10
                print(f"PASS: Component 6 — Chrome debug configuration found ({comp6_score} pts)")
            elif has_configurations:
                comp6_score = 0.03
                print(f"PARTIAL: Component 6 — launch.json has configurations but no Chrome config ({comp6_score} pts)")
            else:
                print(f"FAIL: Component 6 — No Chrome debug configuration in launch.json")
        else:
            print(f"FAIL: Component 6 — .vscode/launch.json missing")

        total_score += comp6_score
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: .vscode/extensions.json with recommended extensions (0.05 points)
    try:
        ext_path = os.path.join(PROJECT, '.vscode', 'extensions.json')
        comp7_score = 0.0

        if os.path.isfile(ext_path):
            ext_data = load_json_file(ext_path)
            recommendations = ext_data.get('recommendations', [])

            if isinstance(recommendations, list) and len(recommendations) >= 3:
                comp7_score = 0.05
                print(f"PASS: Component 7 — {len(recommendations)} recommended extensions found ({comp7_score} pts)")
            elif isinstance(recommendations, list) and len(recommendations) > 0:
                comp7_score = 0.025
                print(f"PARTIAL: Component 7 — Only {len(recommendations)} extensions recommended ({comp7_score} pts)")
            else:
                print(f"FAIL: Component 7 — No extension recommendations found")
        else:
            print(f"FAIL: Component 7 — .vscode/extensions.json missing")

        total_score += comp7_score
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.3f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
