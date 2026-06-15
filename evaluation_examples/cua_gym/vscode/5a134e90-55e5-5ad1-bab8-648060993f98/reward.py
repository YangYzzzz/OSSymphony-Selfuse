"""
Reward Script: Configure Tailwind CSS development setup in VSCode
Task ID: vscode_wf_053
Domain: vs_code
Scoring:
  Component 1: Extension installed (0.15)
  Component 2: tailwind.config.js exists with custom theme (0.25)
  Component 3: postcss.config.js with correct plugins (0.15)
  Component 4: VSCode settings for CSS validation + Tailwind (0.20)
  Component 5: Emmet configured for Tailwind in settings.json (0.10)
  Component 6: tasks.json with build and watch tasks (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
VSCODE_DIR = os.path.join(PROJECT, '.vscode')
TASK_ID = 'vscode_wf_053'


def load_json_file(path):
    """Load a JSON file, stripping JSONC comments if needed."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line // comments (JSONC)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def load_js_config(path):
    """Read a JS config file and return its raw text."""
    with open(path, 'r') as f:
        return f.read()


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Extension "bradlc.vscode-tailwindcss" is installed (0.15 points)
    try:
        ext_dir = os.path.expanduser('~/.vscode/extensions')
        ext_found = False
        if os.path.isdir(ext_dir):
            for entry in os.listdir(ext_dir):
                if entry.lower().startswith('bradlc.vscode-tailwindcss'):
                    ext_found = True
                    break
        if ext_found:
            print(f"PASS: Component 1 — Tailwind CSS IntelliSense extension installed (0.15 pts)")
            total_score += 0.15
        else:
            installed = os.listdir(ext_dir) if os.path.isdir(ext_dir) else []
            print(f"FAIL: Component 1 — Extension 'bradlc.vscode-tailwindcss' not found. Dir contents: {installed}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: tailwind.config.js with custom theme (colors, spacing, fontFamily) (0.25 points)
    tw_config_path = os.path.join(PROJECT, 'tailwind.config.js')
    try:
        if not os.path.exists(tw_config_path):
            print(f"FAIL: Component 2 — tailwind.config.js not found")
        else:
            tw_content = load_js_config(tw_config_path)
            sub_score = 0.0
            # Check for colors extension
            if 'colors' in tw_content and ('aurora' in tw_content or 'midnight' in tw_content or re.search(r'colors\s*:\s*\{', tw_content)):
                # Verify it has actual custom color definitions (not just the key)
                if re.search(r"'#[0-9a-fA-F]{3,6}'", tw_content) or re.search(r'"#[0-9a-fA-F]{3,6}"', tw_content):
                    sub_score += 0.08
                    print(f"PASS: Component 2a — custom colors found in tailwind.config.js")
                else:
                    print(f"FAIL: Component 2a — 'colors' key found but no hex color values")
            else:
                print(f"FAIL: Component 2a — no custom colors in tailwind.config.js")

            # Check for spacing extension
            if 'spacing' in tw_content and re.search(r"'[\d]+'\s*:", tw_content):
                sub_score += 0.08
                print(f"PASS: Component 2b — custom spacing found in tailwind.config.js")
            else:
                print(f"FAIL: Component 2b — no custom spacing in tailwind.config.js")

            # Check for fontFamily extension
            if 'fontFamily' in tw_content or 'font' in tw_content.lower():
                if re.search(r"(sans|display|mono|serif)\s*:", tw_content):
                    sub_score += 0.09
                    print(f"PASS: Component 2c — custom fontFamily found in tailwind.config.js")
                else:
                    print(f"FAIL: Component 2c — fontFamily key not properly defined")
            else:
                print(f"FAIL: Component 2c — no fontFamily in tailwind.config.js")

            total_score += sub_score
            print(f"  Component 2 subtotal: {sub_score}/0.25")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: postcss.config.js with tailwindcss and autoprefixer plugins (0.15 points)
    postcss_path = os.path.join(PROJECT, 'postcss.config.js')
    try:
        if not os.path.exists(postcss_path):
            print(f"FAIL: Component 3 — postcss.config.js not found")
        else:
            postcss_content = load_js_config(postcss_path)
            has_tailwind = 'tailwindcss' in postcss_content
            has_autoprefixer = 'autoprefixer' in postcss_content
            if has_tailwind and has_autoprefixer:
                print(f"PASS: Component 3 — postcss.config.js has tailwindcss and autoprefixer (0.15 pts)")
                total_score += 0.15
            else:
                missing = []
                if not has_tailwind:
                    missing.append('tailwindcss')
                if not has_autoprefixer:
                    missing.append('autoprefixer')
                print(f"FAIL: Component 3 — postcss.config.js missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: VSCode settings.json disables CSS validation, configures Tailwind (0.20 points)
    settings_path = os.path.join(VSCODE_DIR, 'settings.json')
    try:
        if not os.path.exists(settings_path):
            print(f"FAIL: Component 4 — .vscode/settings.json not found")
        else:
            settings = load_json_file(settings_path)
            sub_score = 0.0

            # Check css.validate is disabled
            if settings.get('css.validate') is False:
                sub_score += 0.07
                print(f"PASS: Component 4a — css.validate is false")
            else:
                print(f"FAIL: Component 4a — css.validate is not false, found: {settings.get('css.validate')}")

            # Check tailwindCSS settings exist
            has_tailwind_config = any(k.startswith('tailwindCSS') for k in settings)
            if has_tailwind_config:
                sub_score += 0.07
                print(f"PASS: Component 4b — tailwindCSS settings present")
            else:
                print(f"FAIL: Component 4b — no tailwindCSS settings found")

            # Check editor.quickSuggestions.strings is true (for Tailwind class completion)
            qs = settings.get('editor.quickSuggestions', {})
            if isinstance(qs, dict) and qs.get('strings') is True:
                sub_score += 0.06
                print(f"PASS: Component 4c — editor.quickSuggestions.strings is true")
            else:
                print(f"FAIL: Component 4c — editor.quickSuggestions.strings not set to true, found: {qs}")

            total_score += sub_score
            print(f"  Component 4 subtotal: {sub_score}/0.20")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Emmet configured for Tailwind completions in settings.json (0.10 points)
    try:
        if not os.path.exists(settings_path):
            print(f"FAIL: Component 5 — .vscode/settings.json not found")
        else:
            settings = load_json_file(settings_path)
            has_emmet = False
            # Check emmet.includeLanguages or tailwindCSS.emmetCompletions
            if settings.get('tailwindCSS.emmetCompletions') is True:
                has_emmet = True
            if 'emmet.includeLanguages' in settings:
                has_emmet = True
            if settings.get('emmet.triggerExpansionOnTab') is True:
                has_emmet = True

            if has_emmet:
                print(f"PASS: Component 5 — Emmet configured for Tailwind (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — No Emmet/Tailwind integration settings found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: tasks.json with CSS build and watch tasks (0.15 points)
    tasks_path = os.path.join(VSCODE_DIR, 'tasks.json')
    try:
        if not os.path.exists(tasks_path):
            print(f"FAIL: Component 6 — .vscode/tasks.json not found")
        else:
            tasks_data = load_json_file(tasks_path)
            tasks_list = tasks_data.get('tasks', [])
            has_build = False
            has_watch = False
            for task in tasks_list:
                label = (task.get('label', '') or '').lower()
                command = (task.get('command', '') or '').lower()
                detail = (task.get('detail', '') or '').lower()
                combined = label + ' ' + command + ' ' + detail
                if 'tailwind' in combined or 'tailwindcss' in combined:
                    if 'build' in combined and '--watch' not in command:
                        has_build = True
                    if 'watch' in combined or '--watch' in command:
                        has_watch = True

            sub_score = 0.0
            if has_build:
                sub_score += 0.075
                print(f"PASS: Component 6a — CSS build task found")
            else:
                print(f"FAIL: Component 6a — No CSS build task found in tasks.json")

            if has_watch:
                sub_score += 0.075
                print(f"PASS: Component 6b — CSS watch task found")
            else:
                print(f"FAIL: Component 6b — No CSS watch task found in tasks.json")

            total_score += sub_score
            print(f"  Component 6 subtotal: {sub_score}/0.15")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
