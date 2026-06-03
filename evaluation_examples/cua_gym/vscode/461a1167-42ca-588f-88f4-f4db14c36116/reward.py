"""
Reward Script: Next.js development workflow setup in VSCode
Task ID: vscode_wf_094
Domain: vscode
Scoring:
  1. tsconfig.json strict mode + Next.js paths (0.15)
  2. .eslintrc.json with next/core-web-vitals (0.15)
  3. .prettierrc configured (0.10)
  4. launch.json with debug configurations (0.15)
  5. tasks.json with all 6 tasks (0.20)
  6. .vscode/settings.json with Next.js settings (0.15)
  7. next.config.js bundle-analyzer + package.json updates (0.10)
"""

import os
import json
import re

PROJECT = '/home/user/project'
TASK_ID = 'vscode_wf_094'


def load_json_file(path):
    """Load a JSON file, handling JSONC comments and control characters."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip JSONC comments carefully: only strip // that are NOT inside strings
    # Strategy: strip lines where // appears outside of quoted strings
    lines = content.split('\n')
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # Skip full-line comments
        if stripped.startswith('//'):
            cleaned.append('')
            continue
        # For lines with inline comments, try to preserve string content
        # Simple heuristic: don't strip if // is likely inside a string value
        cleaned.append(line)
    content = '\n'.join(cleaned)
    # Strip trailing commas before } or ]
    content = re.sub(r',\s*([}\]])', r'\1', content)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Try with strict=False to handle control characters
        return json.loads(content, strict=False)


def _is_subset(expected, actual):
    """Check that expected is a subset of actual (recursive dict match)."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and _is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        if not isinstance(actual, list):
            return False
        # Check all expected items exist in actual
        return all(any(_is_subset(e, a) for a in actual) for e in expected)
    return expected == actual


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: tsconfig.json has strict:true and Next.js-specific paths (0.15 points)
    try:
        tsconfig = load_json_file(os.path.join(PROJECT, 'tsconfig.json'))
        comp_opts = tsconfig.get('compilerOptions', {})

        has_strict = comp_opts.get('strict') is True
        has_paths = isinstance(comp_opts.get('paths'), dict) and len(comp_opts.get('paths', {})) > 0
        has_base_url = 'baseUrl' in comp_opts

        if has_strict and has_paths and has_base_url:
            print(f"PASS: Component 1 — tsconfig strict:{has_strict}, paths:{len(comp_opts['paths'])} entries, baseUrl:{comp_opts['baseUrl']} (0.15 pts)")
            total_score += 0.15
        elif has_strict:
            print(f"PARTIAL: Component 1 — strict:true found but missing paths or baseUrl (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 1 — strict:{has_strict}, paths:{has_paths}, baseUrl:{has_base_url}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: .eslintrc.json extends next/core-web-vitals (0.15 points)
    try:
        eslint_path = os.path.join(PROJECT, '.eslintrc.json')
        if not os.path.exists(eslint_path):
            print(f"FAIL: Component 2 — .eslintrc.json does not exist")
        else:
            eslint = load_json_file(eslint_path)
            extends_list = eslint.get('extends', [])
            if isinstance(extends_list, str):
                extends_list = [extends_list]

            has_core_web_vitals = any('core-web-vitals' in ext for ext in extends_list)
            has_rules = isinstance(eslint.get('rules'), dict) and len(eslint.get('rules', {})) > 0

            if has_core_web_vitals and has_rules:
                print(f"PASS: Component 2 — ESLint extends core-web-vitals with {len(eslint['rules'])} custom rules (0.15 pts)")
                total_score += 0.15
            elif has_core_web_vitals:
                print(f"PARTIAL: Component 2 — ESLint extends core-web-vitals but no custom rules (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 2 — extends:{extends_list}, missing core-web-vitals")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: .prettierrc configured (0.10 points)
    try:
        prettierrc_path = None
        for name in ['.prettierrc', '.prettierrc.json', '.prettierrc.js']:
            p = os.path.join(PROJECT, name)
            if os.path.exists(p):
                prettierrc_path = p
                break

        if prettierrc_path is None:
            print(f"FAIL: Component 3 — No .prettierrc file found")
        else:
            prettier = load_json_file(prettierrc_path)
            # Check it has meaningful config (at least 3 settings)
            if isinstance(prettier, dict) and len(prettier) >= 3:
                print(f"PASS: Component 3 — .prettierrc has {len(prettier)} settings (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — .prettierrc has fewer than 3 settings: {prettier}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: launch.json with server-side and client-side debug configs (0.15 points)
    try:
        launch_path = os.path.join(PROJECT, '.vscode', 'launch.json')
        if not os.path.exists(launch_path):
            print(f"FAIL: Component 4 — .vscode/launch.json does not exist")
        else:
            launch = load_json_file(launch_path)
            configs = launch.get('configurations', [])

            has_server = False
            has_client = False
            for cfg in configs:
                cfg_name = cfg.get('name', '').lower()
                cfg_type = cfg.get('type', '').lower()
                cfg_request = cfg.get('request', '').lower()

                # Server-side: type=node with attach/launch
                if cfg_type == 'node' and ('server' in cfg_name or cfg_request == 'attach'):
                    has_server = True
                # Client-side: type=chrome
                if cfg_type == 'chrome' or ('client' in cfg_name and cfg_type in ['chrome', 'pwa-chrome']):
                    has_client = True

            if has_server and has_client:
                print(f"PASS: Component 4 — launch.json has server-side and client-side debug configs (0.15 pts)")
                total_score += 0.15
            elif has_server or has_client:
                print(f"PARTIAL: Component 4 — server:{has_server}, client:{has_client} (0.07 pts)")
                total_score += 0.07
            else:
                print(f"FAIL: Component 4 — No server or client debug configs found in {len(configs)} configurations")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: tasks.json with all 6 tasks (0.20 points)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        if not os.path.exists(tasks_path):
            print(f"FAIL: Component 5 — .vscode/tasks.json does not exist")
        else:
            tasks_config = load_json_file(tasks_path)
            tasks = tasks_config.get('tasks', [])
            task_labels = [t.get('label', '').lower() for t in tasks]

            required_tasks = ['dev', 'build', 'start', 'lint', 'type-check', 'analyze-bundle']
            found_tasks = []
            for req in required_tasks:
                # Match with flexible naming (e.g., "type-check" matches "type-check" or "typecheck")
                req_normalized = req.replace('-', '')
                if any(req == label or req_normalized == label.replace('-', '') for label in task_labels):
                    found_tasks.append(req)

            found_count = len(found_tasks)
            if found_count == 6:
                print(f"PASS: Component 5 — All 6 tasks found: {found_tasks} (0.20 pts)")
                total_score += 0.20
            elif found_count >= 4:
                pts = round(0.20 * found_count / 6, 2)
                print(f"PARTIAL: Component 5 — {found_count}/6 tasks found: {found_tasks} (missing: {set(required_tasks)-set(found_tasks)}) ({pts} pts)")
                total_score += pts
            elif found_count >= 1:
                pts = round(0.20 * found_count / 6, 2)
                print(f"PARTIAL: Component 5 — {found_count}/6 tasks found: {found_tasks} ({pts} pts)")
                total_score += pts
            else:
                print(f"FAIL: Component 5 — No required tasks found. Labels: {task_labels}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: .vscode/settings.json with Next.js settings (0.15 points)
    try:
        settings_path = os.path.join(PROJECT, '.vscode', 'settings.json')
        if not os.path.exists(settings_path):
            print(f"FAIL: Component 6 — .vscode/settings.json does not exist")
        else:
            settings = load_json_file(settings_path)

            # Check for key Next.js-related settings
            checks = 0
            total_checks = 4

            # CSS modules support
            if settings.get('css.modules.enabled') is True or any('css' in k.lower() and 'module' in k.lower() for k in settings):
                checks += 1

            # TypeScript workspace SDK
            if 'typescript.tsdk' in settings or 'typescript.enablePromptUseWorkspaceTsdk' in settings:
                checks += 1

            # Format on save / Prettier integration
            if settings.get('editor.formatOnSave') is True or settings.get('editor.defaultFormatter') == 'esbenp.prettier-vscode':
                checks += 1

            # ESLint validation or code actions on save
            if 'eslint.validate' in settings or 'editor.codeActionsOnSave' in settings:
                checks += 1

            if checks >= 3:
                print(f"PASS: Component 6 — settings.json has {checks}/{total_checks} Next.js settings (0.15 pts)")
                total_score += 0.15
            elif checks >= 1:
                pts = round(0.15 * checks / total_checks, 2)
                print(f"PARTIAL: Component 6 — {checks}/{total_checks} settings present ({pts} pts)")
                total_score += pts
            else:
                print(f"FAIL: Component 6 — No Next.js-related settings found in settings.json")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: next.config.js bundle-analyzer + package.json updates (0.10 points)
    try:
        # Check next.config.js for bundle-analyzer
        next_config_path = os.path.join(PROJECT, 'next.config.js')
        if not os.path.exists(next_config_path):
            next_config_path = os.path.join(PROJECT, 'next.config.mjs')

        has_bundle_analyzer_config = False
        if os.path.exists(next_config_path):
            with open(next_config_path, 'r') as f:
                config_content = f.read()
            if 'bundle-analyzer' in config_content or 'bundleAnalyzer' in config_content:
                has_bundle_analyzer_config = True

        # Check package.json for added devDependencies and scripts
        pkg_path = os.path.join(PROJECT, 'package.json')
        pkg = load_json_file(pkg_path)
        dev_deps = pkg.get('devDependencies', {})
        scripts = pkg.get('scripts', {})

        has_prettier_dep = 'prettier' in dev_deps
        has_bundle_analyzer_dep = '@next/bundle-analyzer' in dev_deps
        has_type_check_script = 'type-check' in scripts or 'typecheck' in scripts
        has_analyze_script = 'analyze' in scripts or 'analyze-bundle' in scripts

        score_items = [has_bundle_analyzer_config, has_prettier_dep or has_bundle_analyzer_dep, has_type_check_script or has_analyze_script]
        passed = sum(score_items)

        if passed >= 2:
            print(f"PASS: Component 7 — bundle-analyzer-config:{has_bundle_analyzer_config}, deps:{has_prettier_dep or has_bundle_analyzer_dep}, scripts:{has_type_check_script or has_analyze_script} (0.10 pts)")
            total_score += 0.10
        elif passed >= 1:
            print(f"PARTIAL: Component 7 — {passed}/3 checks passed (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 7 — bundle-analyzer:{has_bundle_analyzer_config}, deps updated:{has_prettier_dep or has_bundle_analyzer_dep}, scripts:{has_type_check_script or has_analyze_script}")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
