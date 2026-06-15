"""
Reward Script: JavaScript linting and formatting pipeline in VSCode
Task ID: vscode_wf_042
Domain: vscode
Scoring:
  Component 1 - Extensions installed (0.15)
  Component 2 - .eslintrc.json with Airbnb-style rules (0.20)
  Component 3 - .prettierrc with correct config (0.15)
  Component 4 - .eslintignore and .prettierignore (0.10)
  Component 5 - .vscode/settings.json with formatOnSave + ESLint auto-fix (0.25)
  Component 6 - .vscode/tasks.json with pre-commit task (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'project')
TASK_ID = 'vscode_wf_042'


def _is_subset(expected, actual):
    """Check that expected is a subset of actual (for JSON dicts)."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and _is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        if not isinstance(actual, list):
            return False
        return expected == actual
    return expected == actual


def _load_json(path):
    """Load a JSON file, handling JSONC (comments)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments for JSONC compatibility
    cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(cleaned)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Extensions installed (0.15 points)
    # ESLint (dbaeumer.vscode-eslint) and Prettier (esbenp.prettier-vscode)
    # Check by scanning ~/.vscode/extensions/ directory for extension folders
    try:
        ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
        ext_entries = os.listdir(ext_dir) if os.path.isdir(ext_dir) else []

        eslint_installed = any(e.lower().startswith('dbaeumer.vscode-eslint') for e in ext_entries)
        prettier_installed = any(e.lower().startswith('esbenp.prettier-vscode') for e in ext_entries)

        if eslint_installed and prettier_installed:
            print(f"PASS: Component 1 - Both ESLint and Prettier extensions installed (0.15 pts)")
            total_score += 0.15
        elif eslint_installed or prettier_installed:
            installed = 'ESLint' if eslint_installed else 'Prettier'
            missing = 'Prettier' if eslint_installed else 'ESLint'
            print(f"PARTIAL: Component 1 - Only {installed} installed, {missing} missing (0.075 pts)")
            total_score += 0.075
        else:
            print(f"FAIL: Component 1 - Neither ESLint nor Prettier extensions installed")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: .eslintrc.json with correct rules (0.20 points)
    # Must have semi, quotes, no-unused-vars, no-console rules
    try:
        eslintrc_path = os.path.join(PROJECT_DIR, '.eslintrc.json')
        if not os.path.exists(eslintrc_path):
            print(f"FAIL: Component 2 - .eslintrc.json not found")
        else:
            eslintrc = _load_json(eslintrc_path)

            rules = eslintrc.get('rules', {})
            required_rules = ['semi', 'quotes', 'no-unused-vars', 'no-console']
            found_rules = [r for r in required_rules if r in rules]

            if len(found_rules) == 4:
                # Check semi requires "always" and quotes requires "single"
                semi_ok = isinstance(rules.get('semi'), list) and 'always' in rules['semi']
                quotes_ok = isinstance(rules.get('quotes'), list) and 'single' in rules['quotes']

                if semi_ok and quotes_ok:
                    print(f"PASS: Component 2 - .eslintrc.json has all 4 rules with correct values (0.20 pts)")
                    total_score += 0.20
                else:
                    details = []
                    if not semi_ok:
                        details.append(f"semi rule value: {rules.get('semi')}")
                    if not quotes_ok:
                        details.append(f"quotes rule value: {rules.get('quotes')}")
                    print(f"PARTIAL: Component 2 - Rules present but values wrong: {', '.join(details)} (0.10 pts)")
                    total_score += 0.10
            elif len(found_rules) > 0:
                print(f"PARTIAL: Component 2 - Only {len(found_rules)}/4 rules found: {found_rules} (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 2 - No required rules found in .eslintrc.json")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: .prettierrc with correct config (0.15 points)
    # Must have singleQuote: true, trailingComma: "all", printWidth: 80
    try:
        prettierrc_path = os.path.join(PROJECT_DIR, '.prettierrc')
        if not os.path.exists(prettierrc_path):
            print(f"FAIL: Component 3 - .prettierrc not found")
        else:
            prettierrc = _load_json(prettierrc_path)

            expected = {
                "singleQuote": True,
                "trailingComma": "all",
                "printWidth": 80
            }

            matches = 0
            for key, val in expected.items():
                if prettierrc.get(key) == val:
                    matches += 1

            if matches == 3:
                print(f"PASS: Component 3 - .prettierrc has all 3 correct settings (0.15 pts)")
                total_score += 0.15
            elif matches > 0:
                print(f"PARTIAL: Component 3 - {matches}/3 settings correct in .prettierrc (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 3 - No correct settings in .prettierrc, got: {prettierrc}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: .eslintignore and .prettierignore (0.10 points)
    # Both must exclude node_modules/ and dist/
    try:
        eslintignore_path = os.path.join(PROJECT_DIR, '.eslintignore')
        prettierignore_path = os.path.join(PROJECT_DIR, '.prettierignore')

        eslintignore_ok = False
        prettierignore_ok = False

        if os.path.exists(eslintignore_path):
            with open(eslintignore_path, 'r') as f:
                content = f.read()
            lines = [l.strip() for l in content.strip().split('\n') if l.strip()]
            # Check for node_modules and dist (with or without trailing /)
            has_node = any('node_modules' in l for l in lines)
            has_dist = any('dist' in l for l in lines)
            eslintignore_ok = has_node and has_dist

        if os.path.exists(prettierignore_path):
            with open(prettierignore_path, 'r') as f:
                content = f.read()
            lines = [l.strip() for l in content.strip().split('\n') if l.strip()]
            has_node = any('node_modules' in l for l in lines)
            has_dist = any('dist' in l for l in lines)
            prettierignore_ok = has_node and has_dist

        if eslintignore_ok and prettierignore_ok:
            print(f"PASS: Component 4 - Both ignore files exist with correct entries (0.10 pts)")
            total_score += 0.10
        elif eslintignore_ok or prettierignore_ok:
            which = '.eslintignore' if eslintignore_ok else '.prettierignore'
            print(f"PARTIAL: Component 4 - Only {which} is correct (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 4 - Ignore files missing or incomplete")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: .vscode/settings.json with formatOnSave + ESLint auto-fix (0.25 points)
    # Must have: editor.formatOnSave, editor.defaultFormatter = prettier,
    # editor.codeActionsOnSave.source.fixAll.eslint = true
    try:
        vscode_settings_path = os.path.join(PROJECT_DIR, '.vscode', 'settings.json')
        if not os.path.exists(vscode_settings_path):
            print(f"FAIL: Component 5 - .vscode/settings.json not found")
        else:
            settings = _load_json(vscode_settings_path)

            checks = {
                'formatOnSave': settings.get('editor.formatOnSave') is True,
                'defaultFormatter': 'prettier' in str(settings.get('editor.defaultFormatter', '')).lower(),
                'eslintAutoFix': False
            }

            # Check ESLint auto-fix on save - can be nested in different ways
            code_actions = settings.get('editor.codeActionsOnSave', {})
            if isinstance(code_actions, dict):
                # Could be "source.fixAll.eslint": true or "source.fixAll.eslint": "explicit"
                eslint_fix = code_actions.get('source.fixAll.eslint')
                if eslint_fix is True or eslint_fix == 'explicit' or eslint_fix == 'always':
                    checks['eslintAutoFix'] = True

            passed = sum(1 for v in checks.values() if v)

            if passed == 3:
                print(f"PASS: Component 5 - .vscode/settings.json fully configured (0.25 pts)")
                total_score += 0.25
            elif passed > 0:
                pts = round(0.25 * passed / 3, 3)
                failed = [k for k, v in checks.items() if not v]
                print(f"PARTIAL: Component 5 - {passed}/3 checks passed, failed: {failed} ({pts} pts)")
                total_score += pts
            else:
                print(f"FAIL: Component 5 - .vscode/settings.json has no required settings")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: .vscode/tasks.json with pre-commit task (0.15 points)
    # Must have a task labeled "pre-commit" that runs eslint and prettier --check
    try:
        tasks_path = os.path.join(PROJECT_DIR, '.vscode', 'tasks.json')
        if not os.path.exists(tasks_path):
            print(f"FAIL: Component 6 - .vscode/tasks.json not found")
        else:
            tasks_config = _load_json(tasks_path)
            tasks = tasks_config.get('tasks', [])

            # Find a pre-commit task
            precommit_task = None
            for task in tasks:
                label = str(task.get('label', '')).lower()
                if 'pre-commit' in label or 'precommit' in label:
                    precommit_task = task
                    break

            if precommit_task is None:
                print(f"FAIL: Component 6 - No pre-commit task found in tasks.json")
            else:
                command = str(precommit_task.get('command', ''))
                has_eslint = 'eslint' in command.lower()
                has_prettier_check = 'prettier' in command.lower() and 'check' in command.lower()

                if has_eslint and has_prettier_check:
                    print(f"PASS: Component 6 - pre-commit task runs eslint and prettier --check (0.15 pts)")
                    total_score += 0.15
                elif has_eslint or has_prettier_check:
                    present = 'eslint' if has_eslint else 'prettier --check'
                    print(f"PARTIAL: Component 6 - pre-commit task only has {present} (0.075 pts)")
                    total_score += 0.075
                else:
                    print(f"FAIL: Component 6 - pre-commit task command doesn't include eslint or prettier: {command}")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
