"""
Reward Script: VSCode workspace configuration for Sphinx/reStructuredText docs project
Task ID: vscode_cm_092
Domain: vscode (libreoffice_calc listed but actually vscode config task)
Scoring:
  Component 1: Extensions installed (rst + cSpell)               — 0.20
  Component 2: Workspace .vscode/settings.json RST configuration — 0.20
  Component 3: Workspace .vscode/settings.json cSpell config     — 0.20
  Component 4: tasks.json sphinx-build task                      — 0.20
  Component 5: tasks.json build-and-open task                    — 0.20
  Total: 1.0
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = '/home/user/projects/docs_project'
VSCODE_SETTINGS = os.path.join(PROJECT_DIR, '.vscode', 'settings.json')
VSCODE_TASKS = os.path.join(PROJECT_DIR, '.vscode', 'tasks.json')
USER_SETTINGS = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_json_file(path):
    """Load a JSON file, handling JSONC (comments)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments for JSONC support
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def check_extensions_installed():
    """Check if rst and cSpell extensions are installed via code CLI."""
    try:
        import subprocess
        result = subprocess.run(['code', '--list-extensions'],
                                capture_output=True, text=True, timeout=15)
        extensions = result.stdout.strip().lower().split('\n')
        return extensions
    except Exception:
        return []


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Extensions installed — rst + code-spell-checker (0.20 points)
    try:
        extensions = check_extensions_installed()
        rst_installed = any('restructuredtext' in ext for ext in extensions)
        cspell_installed = any('code-spell-checker' in ext for ext in extensions)

        if rst_installed and cspell_installed:
            print(f"PASS: Component 1 — Both extensions installed: restructuredtext + code-spell-checker (0.20 pts)")
            total_score += 0.20
        elif rst_installed or cspell_installed:
            installed = []
            if rst_installed:
                installed.append('restructuredtext')
            if cspell_installed:
                installed.append('code-spell-checker')
            print(f"PARTIAL: Component 1 — Only {installed} installed (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — No required extensions installed. Found: {extensions}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Workspace .vscode/settings.json RST configuration (0.20 points)
    # Must have: restructuredtext.confPath pointing to source dir, and preview settings enabled
    try:
        if not os.path.exists(VSCODE_SETTINGS):
            print(f"FAIL: Component 2 — {VSCODE_SETTINGS} does not exist")
        else:
            settings = load_json_file(VSCODE_SETTINGS)

            conf_path = settings.get('restructuredtext.confPath', '')
            # confPath should point to the source directory containing conf.py
            conf_path_ok = 'source' in conf_path and 'docs_project' in conf_path

            preview_scroll_editor = settings.get('restructuredtext.preview.scrollEditorWithPreview', False)
            preview_scroll_preview = settings.get('restructuredtext.preview.scrollPreviewWithEditor', False)

            checks_passed = sum([conf_path_ok, preview_scroll_editor, preview_scroll_preview])

            if checks_passed == 3:
                print(f"PASS: Component 2 — RST confPath='{conf_path}', preview scroll settings enabled (0.20 pts)")
                total_score += 0.20
            elif checks_passed >= 1:
                partial = round(0.20 * checks_passed / 3, 2)
                print(f"PARTIAL: Component 2 — {checks_passed}/3 RST checks passed ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — No RST config found. confPath='{conf_path}', scrollEditor={preview_scroll_editor}, scrollPreview={preview_scroll_preview}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Workspace .vscode/settings.json cSpell configuration (0.20 points)
    # Must have: cSpell.enabled=true, cSpell.words with technical terms, cSpell.enableFiletypes includes rst
    try:
        if not os.path.exists(VSCODE_SETTINGS):
            print(f"FAIL: Component 3 — {VSCODE_SETTINGS} does not exist")
        else:
            settings = load_json_file(VSCODE_SETTINGS)

            cspell_enabled = settings.get('cSpell.enabled', False)
            cspell_words = settings.get('cSpell.words', [])
            cspell_filetypes = settings.get('cSpell.enableFiletypes', [])

            has_enabled = cspell_enabled is True
            has_custom_words = isinstance(cspell_words, list) and len(cspell_words) >= 5
            has_rst_filetype = 'restructuredtext' in cspell_filetypes

            checks_passed = sum([has_enabled, has_custom_words, has_rst_filetype])

            if checks_passed == 3:
                print(f"PASS: Component 3 — cSpell enabled, {len(cspell_words)} custom words, rst filetype enabled (0.20 pts)")
                total_score += 0.20
            elif checks_passed >= 1:
                partial = round(0.20 * checks_passed / 3, 2)
                print(f"PARTIAL: Component 3 — {checks_passed}/3 cSpell checks passed ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — cSpell not configured. enabled={cspell_enabled}, words={len(cspell_words)}, filetypes={cspell_filetypes}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: tasks.json — sphinx-build task (0.20 points)
    # Must have a task that runs sphinx-build with correct source/output dirs
    try:
        if not os.path.exists(VSCODE_TASKS):
            print(f"FAIL: Component 4 — {VSCODE_TASKS} does not exist")
        else:
            tasks_config = load_json_file(VSCODE_TASKS)
            tasks = tasks_config.get('tasks', [])

            sphinx_task_found = False
            for task in tasks:
                cmd = task.get('command', '')
                args = task.get('args', [])
                label = task.get('label', '')
                task_type = task.get('type', '')

                # Check for sphinx-build command
                if 'sphinx' in cmd.lower() or 'sphinx' in label.lower():
                    # Verify it has html build flag and correct paths
                    args_str = ' '.join(str(a) for a in args)
                    has_html_flag = '-b' in args and 'html' in args
                    has_source_path = any('source' in str(a) for a in args)

                    if has_html_flag and has_source_path:
                        sphinx_task_found = True
                        print(f"PASS: Component 4 — Sphinx build task found: '{label}', cmd='{cmd}', html output with source path (0.20 pts)")
                        total_score += 0.20
                        break
                    elif has_source_path or has_html_flag:
                        sphinx_task_found = True
                        print(f"PARTIAL: Component 4 — Sphinx task found but incomplete config: '{label}' (0.10 pts)")
                        total_score += 0.10
                        break

            if not sphinx_task_found:
                print(f"FAIL: Component 4 — No sphinx-build task found. Tasks: {[t.get('label','') for t in tasks]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: tasks.json — build-and-open task (0.20 points)
    # Must have a task that depends on the build task and opens the output in a browser
    try:
        if not os.path.exists(VSCODE_TASKS):
            print(f"FAIL: Component 5 — {VSCODE_TASKS} does not exist")
        else:
            tasks_config = load_json_file(VSCODE_TASKS)
            tasks = tasks_config.get('tasks', [])

            open_task_found = False
            for task in tasks:
                depends_on = task.get('dependsOn', '')
                cmd = task.get('command', '')
                args = task.get('args', [])
                label = task.get('label', '')

                # A task that depends on another task and opens HTML
                has_dependency = bool(depends_on)
                opens_html = any('html' in str(a).lower() for a in args) or 'html' in cmd.lower()
                opens_browser = 'xdg-open' in cmd or 'open' in cmd.lower() or 'browser' in label.lower()

                if has_dependency and (opens_html or opens_browser):
                    open_task_found = True
                    print(f"PASS: Component 5 — Build-and-open task found: '{label}', dependsOn='{depends_on}', opens output (0.20 pts)")
                    total_score += 0.20
                    break

            if not open_task_found:
                print(f"FAIL: Component 5 — No build-and-open task found. Tasks: {[t.get('label','') for t in tasks]}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
