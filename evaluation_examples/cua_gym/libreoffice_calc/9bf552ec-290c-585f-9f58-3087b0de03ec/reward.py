"""
Reward Script: Code formatting standardization workflow for ~/project
Task ID: vscode_wf_086
Domain: libreoffice_calc (VSCode workflow)
Scoring:
  - Component 1: Extensions installed (0.15)
  - Component 2: .prettierrc config (0.15)
  - Component 3: .eslintrc.json config (0.15)
  - Component 4: .editorconfig config (0.10)
  - Component 5: tasks.json with all 4 tasks (0.25)
  - Component 6: .prettierignore (0.05)
  - Component 7: VSCode settings (formatOnSave + ESLint auto-fix) (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')
TASK_ID = 'vscode_wf_086'


def load_json_file(path):
    """Load a JSON file, stripping JSONC comments if needed."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def _is_subset(expected, actual):
    """Check expected is a subset of actual (recursive for dicts)."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and _is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        return expected == actual
    return expected == actual


def check_extensions():
    """Check if Prettier, ESLint, and EditorConfig extensions are installed by scanning disk."""
    ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
    required = [
        'esbenp.prettier-vscode',
        'dbaeumer.vscode-eslint',
        'editorconfig.editorconfig',
    ]
    found = 0
    try:
        entries = os.listdir(ext_dir) if os.path.isdir(ext_dir) else []
    except OSError:
        entries = []
    entries_lower = [e.lower() for e in entries]
    for ext_id in required:
        # Extension dirs are like "esbenp.prettier-vscode-11.0.3"
        if any(e.startswith(ext_id.lower()) for e in entries_lower):
            found += 1
            print(f"  FOUND: {ext_id}")
        else:
            print(f"  MISSING: {ext_id}")
    return found / len(required)


def verify_task():
    """Verify task completion with progressive scoring. Returns float 0.0-1.0."""
    total_score = 0.0

    # Component 1: Extensions installed (0.15 points)
    try:
        ext_ratio = check_extensions()
        if ext_ratio > 0:
            pts = round(0.15 * ext_ratio, 4)
            print(f"PASS: Component 1 — {int(ext_ratio*3)}/3 extensions installed ({pts} pts)")
            total_score += pts
        else:
            print("FAIL: Component 1 — No required extensions installed")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: .prettierrc with singleQuote, trailingComma, printWidth: 100 (0.15 points)
    prettierrc_path = os.path.join(PROJECT, '.prettierrc')
    try:
        if not os.path.exists(prettierrc_path):
            print("FAIL: Component 2 — .prettierrc not found")
        else:
            prettier_cfg = load_json_file(prettierrc_path)
            checks = 0
            if prettier_cfg.get('singleQuote') is True:
                checks += 1
            else:
                print(f"  FAIL: singleQuote expected True, got {prettier_cfg.get('singleQuote')}")
            if prettier_cfg.get('trailingComma') == 'all':
                checks += 1
            else:
                print(f"  FAIL: trailingComma expected 'all', got {prettier_cfg.get('trailingComma')}")
            if prettier_cfg.get('printWidth') == 100:
                checks += 1
            else:
                print(f"  FAIL: printWidth expected 100, got {prettier_cfg.get('printWidth')}")
            if checks == 3:
                print(f"PASS: Component 2 — .prettierrc correct (0.15 pts)")
                total_score += 0.15
            elif checks > 0:
                pts = round(0.15 * checks / 3, 4)
                print(f"PARTIAL: Component 2 — {checks}/3 checks passed ({pts} pts)")
                total_score += pts
            else:
                print("FAIL: Component 2 — .prettierrc has no correct values")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: .eslintrc.json consistent with Prettier (extends includes "prettier") (0.15 points)
    eslintrc_path = os.path.join(PROJECT, '.eslintrc.json')
    try:
        if not os.path.exists(eslintrc_path):
            print("FAIL: Component 3 — .eslintrc.json not found")
        else:
            eslint_cfg = load_json_file(eslintrc_path)
            extends = eslint_cfg.get('extends', [])
            if isinstance(extends, str):
                extends = [extends]
            has_prettier = 'prettier' in extends
            has_recommended = 'eslint:recommended' in extends
            if has_prettier and has_recommended:
                print(f"PASS: Component 3 — .eslintrc.json extends prettier + recommended (0.15 pts)")
                total_score += 0.15
            elif has_prettier:
                print(f"PARTIAL: Component 3 — extends prettier but not recommended (0.10 pts)")
                total_score += 0.10
            elif has_recommended:
                print(f"PARTIAL: Component 3 — extends recommended but not prettier (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 3 — extends={extends}, missing prettier and recommended")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: .editorconfig with matching indent settings (0.10 points)
    editorconfig_path = os.path.join(PROJECT, '.editorconfig')
    try:
        if not os.path.exists(editorconfig_path):
            print("FAIL: Component 4 — .editorconfig not found")
        else:
            with open(editorconfig_path, 'r') as f:
                ec_content = f.read()
            # Check for key settings: indent_style = space, indent_size = 2, end_of_line = lf
            checks = 0
            if re.search(r'indent_style\s*=\s*space', ec_content):
                checks += 1
            else:
                print("  FAIL: indent_style should be 'space'")
            if re.search(r'indent_size\s*=\s*2', ec_content):
                checks += 1
            else:
                print("  FAIL: indent_size should be '2'")
            if re.search(r'end_of_line\s*=\s*lf', ec_content):
                checks += 1
            else:
                print("  FAIL: end_of_line should be 'lf'")
            if checks == 3:
                print(f"PASS: Component 4 — .editorconfig correct (0.10 pts)")
                total_score += 0.10
            elif checks > 0:
                pts = round(0.10 * checks / 3, 4)
                print(f"PARTIAL: Component 4 — {checks}/3 checks passed ({pts} pts)")
                total_score += pts
            else:
                print("FAIL: Component 4 — .editorconfig has no correct values")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: tasks.json with format-all, lint-fix, standardize (compound), check-format (0.25 points)
    tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
    try:
        if not os.path.exists(tasks_path):
            print("FAIL: Component 5 — .vscode/tasks.json not found")
        else:
            tasks_cfg = load_json_file(tasks_path)
            tasks_list = tasks_cfg.get('tasks', [])
            labels = {t.get('label'): t for t in tasks_list}

            sub_score = 0.0

            # 5a: format-all task runs prettier --write (0.05)
            if 'format-all' in labels:
                cmd = labels['format-all'].get('command', '')
                if 'prettier' in cmd and '--write' in cmd:
                    print("  PASS: 5a — format-all runs prettier --write")
                    sub_score += 0.05
                else:
                    print(f"  FAIL: 5a — format-all command wrong: {cmd}")
            else:
                print("  FAIL: 5a — format-all task not found")

            # 5b: lint-fix task runs eslint --fix (0.05)
            if 'lint-fix' in labels:
                cmd = labels['lint-fix'].get('command', '')
                if 'eslint' in cmd and '--fix' in cmd:
                    print("  PASS: 5b — lint-fix runs eslint --fix")
                    sub_score += 0.05
                else:
                    print(f"  FAIL: 5b — lint-fix command wrong: {cmd}")
            else:
                print("  FAIL: 5b — lint-fix task not found")

            # 5c: standardize is compound task depending on format-all and lint-fix (0.10)
            if 'standardize' in labels:
                deps = labels['standardize'].get('dependsOn', [])
                if 'format-all' in deps and 'lint-fix' in deps:
                    print("  PASS: 5c — standardize is compound (depends on format-all + lint-fix)")
                    sub_score += 0.10
                else:
                    print(f"  FAIL: 5c — standardize dependsOn wrong: {deps}")
            else:
                print("  FAIL: 5c — standardize task not found")

            # 5d: check-format task runs prettier --check (0.05)
            if 'check-format' in labels:
                cmd = labels['check-format'].get('command', '')
                if 'prettier' in cmd and '--check' in cmd:
                    print("  PASS: 5d — check-format runs prettier --check")
                    sub_score += 0.05
                else:
                    print(f"  FAIL: 5d — check-format command wrong: {cmd}")
            else:
                print("  FAIL: 5d — check-format task not found")

            if sub_score > 0:
                total_score += sub_score
                print(f"PASS: Component 5 — tasks.json ({sub_score} pts)")
            else:
                print("FAIL: Component 5 — no valid tasks found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: .prettierignore excluding node_modules, dist, coverage (0.05 points)
    prettierignore_path = os.path.join(PROJECT, '.prettierignore')
    try:
        if not os.path.exists(prettierignore_path):
            print("FAIL: Component 6 — .prettierignore not found")
        else:
            with open(prettierignore_path, 'r') as f:
                ignore_content = f.read()
            lines = [l.strip() for l in ignore_content.strip().splitlines() if l.strip()]
            required_entries = ['node_modules', 'dist', 'coverage']
            found = sum(1 for entry in required_entries if entry in lines)
            if found == 3:
                print(f"PASS: Component 6 — .prettierignore correct (0.05 pts)")
                total_score += 0.05
            elif found > 0:
                pts = round(0.05 * found / 3, 4)
                print(f"PARTIAL: Component 6 — {found}/3 entries found ({pts} pts)")
                total_score += pts
            else:
                print("FAIL: Component 6 — .prettierignore missing all required entries")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: VSCode settings: formatOnSave enabled and ESLint auto-fix (0.15 points)
    try:
        if not os.path.exists(SETTINGS_PATH):
            print("FAIL: Component 7 — settings.json not found")
        else:
            settings = load_json_file(SETTINGS_PATH)
            sub_score = 0.0

            # 7a: editor.formatOnSave = true (0.075)
            if settings.get('editor.formatOnSave') is True:
                print("  PASS: 7a — editor.formatOnSave is true")
                sub_score += 0.075
            else:
                print(f"  FAIL: 7a — editor.formatOnSave = {settings.get('editor.formatOnSave')}")

            # 7b: ESLint auto-fix on save (0.075)
            code_actions = settings.get('editor.codeActionsOnSave', {})
            eslint_fix = code_actions.get('source.fixAll.eslint')
            if eslint_fix in (True, 'explicit', 'always'):
                print("  PASS: 7b — ESLint auto-fix on save enabled")
                sub_score += 0.075
            else:
                print(f"  FAIL: 7b — source.fixAll.eslint = {eslint_fix}")

            if sub_score > 0:
                total_score += sub_score
                print(f"PASS: Component 7 — settings ({sub_score} pts)")
            else:
                print("FAIL: Component 7 — no correct settings found")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
