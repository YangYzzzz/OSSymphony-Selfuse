"""
Reward Script: Configure pre-commit hook using Husky and lint-staged
Task ID: vscode_web_084
Domain: vscode
Scoring:
  - Component 1 (0.25): husky and lint-staged in devDependencies
  - Component 2 (0.15): prepare script set to "husky"
  - Component 3 (0.25): .husky/pre-commit hook exists, is executable, and calls lint-staged
  - Component 4 (0.35): lint-staged config with correct ESLint and Prettier patterns
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_084'
WEBAPP_DIR = os.path.join(WORKDIR, 'projects', 'webapp')
PACKAGE_JSON = os.path.join(WEBAPP_DIR, 'package.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load package.json (precondition)
    try:
        with open(PACKAGE_JSON, 'r') as f:
            pkg = json.load(f)
    except Exception as e:
        print(f"CRITICAL: Cannot load {PACKAGE_JSON}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: husky and lint-staged are in devDependencies (0.25 points)
    try:
        dev_deps = pkg.get('devDependencies', {})
        has_husky = 'husky' in dev_deps
        has_lint_staged = 'lint-staged' in dev_deps
        if has_husky and has_lint_staged:
            print(f"PASS: Component 1 - husky and lint-staged in devDependencies (0.25 pts)")
            total_score += 0.25
        else:
            missing = []
            if not has_husky:
                missing.append('husky')
            if not has_lint_staged:
                missing.append('lint-staged')
            print(f"FAIL: Component 1 - missing devDependencies: {missing}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: prepare script is set to "husky" (0.15 points)
    try:
        scripts = pkg.get('scripts', {})
        prepare_val = scripts.get('prepare', '')
        if 'husky' in str(prepare_val).lower():
            print(f"PASS: Component 2 - prepare script is '{prepare_val}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 - expected prepare script containing 'husky', found: '{prepare_val}'")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: .husky/pre-commit hook exists, is executable, and calls lint-staged (0.25 points)
    try:
        pre_commit_path = os.path.join(WEBAPP_DIR, '.husky', 'pre-commit')
        if os.path.isfile(pre_commit_path):
            is_executable = os.access(pre_commit_path, os.X_OK)
            with open(pre_commit_path, 'r') as f:
                content = f.read()
            calls_lint_staged = 'lint-staged' in content
            if is_executable and calls_lint_staged:
                print(f"PASS: Component 3 - pre-commit hook is executable and calls lint-staged (0.25 pts)")
                total_score += 0.25
            elif calls_lint_staged:
                print(f"PARTIAL: Component 3 - pre-commit calls lint-staged but not executable (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 - pre-commit exists but does not call lint-staged. Content: {repr(content)}")
        else:
            print(f"FAIL: Component 3 - .husky/pre-commit not found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: lint-staged config with correct ESLint and Prettier patterns (0.35 points)
    try:
        # Check for lint-staged config in package.json, .lintstagedrc, or .lintstagedrc.json
        lint_staged_config = None

        # Check package.json first
        if 'lint-staged' in pkg and isinstance(pkg['lint-staged'], dict):
            lint_staged_config = pkg['lint-staged']
            print(f"  Found lint-staged config in package.json")

        # Check .lintstagedrc
        if lint_staged_config is None:
            for rc_name in ['.lintstagedrc', '.lintstagedrc.json', '.lintstagedrc.yaml', '.lintstagedrc.yml']:
                rc_path = os.path.join(WEBAPP_DIR, rc_name)
                if os.path.isfile(rc_path):
                    with open(rc_path, 'r') as f:
                        lint_staged_config = json.load(f)
                    print(f"  Found lint-staged config in {rc_name}")
                    break

        # Check lint-staged.config.js (just check existence)
        if lint_staged_config is None:
            config_js = os.path.join(WEBAPP_DIR, 'lint-staged.config.js')
            config_mjs = os.path.join(WEBAPP_DIR, 'lint-staged.config.mjs')
            if os.path.isfile(config_js) or os.path.isfile(config_mjs):
                # Cannot parse JS, but we can check for patterns in the text
                js_path = config_js if os.path.isfile(config_js) else config_mjs
                with open(js_path, 'r') as f:
                    js_content = f.read()
                has_eslint_pattern = 'eslint' in js_content.lower()
                has_prettier_pattern = 'prettier' in js_content.lower()
                if has_eslint_pattern and has_prettier_pattern:
                    print(f"PASS: Component 4 - JS config contains eslint and prettier (0.35 pts)")
                    total_score += 0.35
                else:
                    print(f"FAIL: Component 4 - JS config missing eslint/prettier patterns")
                lint_staged_config = "JS_HANDLED"

        if lint_staged_config is None:
            print(f"FAIL: Component 4 - no lint-staged config found anywhere")
        elif lint_staged_config != "JS_HANDLED":
            # Verify the config has correct patterns
            eslint_match_count = 0
            prettier_match_count = 0

            for pattern, commands in lint_staged_config.items():
                cmds_str = ' '.join(commands) if isinstance(commands, list) else str(commands)
                cmds_lower = cmds_str.lower()

                # Check for ESLint on JS/TS files
                if 'eslint' in cmds_lower:
                    pat_lower = pattern.lower()
                    if any(ext in pat_lower for ext in ['js', 'ts', 'jsx', 'tsx']):
                        eslint_match_count += 1

                # Check for Prettier on supported files
                if 'prettier' in cmds_lower:
                    pat_lower = pattern.lower()
                    if any(ext in pat_lower for ext in ['js', 'ts', 'jsx', 'tsx', 'css', 'json']):
                        prettier_match_count += 1

            sub_score = 0.0
            if eslint_match_count > 0:
                sub_score += 0.175
                print(f"  PASS: ESLint rule found for JS/TS files")
            else:
                print(f"  FAIL: No ESLint rule for JS/TS files in lint-staged config")

            if prettier_match_count > 0:
                sub_score += 0.175
                print(f"  PASS: Prettier rule found for supported files")
            else:
                print(f"  FAIL: No Prettier rule in lint-staged config")

            if sub_score > 0:
                print(f"PASS: Component 4 - lint-staged config verified ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 4 - lint-staged config missing required rules")

    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isfile(PACKAGE_JSON):
    print(f"File not found: {PACKAGE_JSON}")
    print("REWARD: 0.0")
else:
    verify_task()
