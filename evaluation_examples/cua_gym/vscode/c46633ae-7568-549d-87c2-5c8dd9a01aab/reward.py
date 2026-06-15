"""
Reward Script: VSCode Playwright E2E Testing Workflow Setup
Task ID: vscode_wf_066
Domain: vscode
Scoring:
  Component 1: ms-playwright.playwright extension installed (0.15)
  Component 2: playwright.config.ts with chromium+firefox projects and baseURL (0.20)
  Component 3: tests/e2e/homepage.spec.ts with navigation tests (0.20)
  Component 4: tests/e2e/homepage.spec.ts with form submission tests + page object pattern (0.15)
  Component 5: launch.json with Playwright debug configuration (0.15)
  Component 6: tasks.json with e2e-test, e2e-headed, e2e-report tasks (0.15)
"""

import os
import json
import re
import subprocess

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
VSCODE_DIR = os.path.join(PROJECT, '.vscode')
TASK_ID = 'vscode_wf_066'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: ms-playwright.playwright extension installed (0.15 points)
    try:
        result = subprocess.run(
            ["code", "--list-extensions"],
            capture_output=True, text=True, timeout=15
        )
        extensions = result.stdout.strip().lower()
        if "ms-playwright.playwright" in extensions:
            print("PASS: Component 1 — ms-playwright.playwright extension installed (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — ms-playwright.playwright not found in extensions: {result.stdout.strip()}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: playwright.config.ts with chromium+firefox projects and baseURL (0.20 points)
    try:
        config_path = os.path.join(PROJECT, 'playwright.config.ts')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config_content = f.read()

            config_lower = config_content.lower()
            has_chromium = 'chromium' in config_lower
            has_firefox = 'firefox' in config_lower
            has_base_url = 'baseurl' in config_lower
            has_projects = 'projects' in config_lower

            sub_score = 0.0
            if has_projects and has_chromium and has_firefox:
                sub_score += 0.15
            if has_base_url:
                sub_score += 0.05

            if sub_score > 0:
                print(f"PASS: Component 2 — playwright.config.ts has projects(chromium={has_chromium}, firefox={has_firefox}), baseURL={has_base_url} ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 2 — playwright.config.ts missing required config: projects={has_projects}, chromium={has_chromium}, firefox={has_firefox}, baseURL={has_base_url}")
        else:
            print("FAIL: Component 2 — playwright.config.ts does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: tests/e2e/homepage.spec.ts with navigation tests (0.20 points)
    try:
        spec_path = os.path.join(PROJECT, 'tests', 'e2e', 'homepage.spec.ts')
        if os.path.exists(spec_path):
            with open(spec_path, 'r') as f:
                spec_content = f.read()

            spec_lower = spec_content.lower()
            # Check for navigation test patterns
            has_playwright_import = '@playwright/test' in spec_content
            has_navigate = 'navigate' in spec_lower or 'goto' in spec_lower
            has_url_check = 'tohaveurl' in spec_lower or 'haveurl' in spec_lower or 'url' in spec_lower

            if has_playwright_import and has_navigate and has_url_check:
                print("PASS: Component 3 — homepage.spec.ts has navigation tests with Playwright imports (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — homepage.spec.ts missing navigation tests: import={has_playwright_import}, navigate={has_navigate}, url_check={has_url_check}")
        else:
            print("FAIL: Component 3 — tests/e2e/homepage.spec.ts does not exist")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: tests/e2e/homepage.spec.ts with form submission tests + page object pattern (0.15 points)
    try:
        spec_path = os.path.join(PROJECT, 'tests', 'e2e', 'homepage.spec.ts')
        if os.path.exists(spec_path):
            with open(spec_path, 'r') as f:
                spec_content = f.read()

            spec_lower = spec_content.lower()
            # Check for form submission patterns
            has_form_submit = 'submit' in spec_lower
            has_fill = 'fill' in spec_lower or 'type' in spec_lower
            # Check for page object pattern (class definition with page property)
            has_page_object = bool(re.search(r'class\s+\w+.*\{', spec_content)) and 'page' in spec_lower

            sub_score = 0.0
            if has_form_submit and has_fill:
                sub_score += 0.08
            if has_page_object:
                sub_score += 0.07

            if sub_score > 0:
                print(f"PASS: Component 4 — form submission={has_form_submit and has_fill}, page object={has_page_object} ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 4 — form_submit={has_form_submit}, fill={has_fill}, page_object={has_page_object}")
        else:
            print("FAIL: Component 4 — tests/e2e/homepage.spec.ts does not exist")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: launch.json with Playwright debug configuration (0.15 points)
    try:
        launch_path = os.path.join(VSCODE_DIR, 'launch.json')
        if os.path.exists(launch_path):
            with open(launch_path, 'r') as f:
                content = f.read()
            # Strip JSONC comments
            clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            launch_data = json.loads(clean)

            configs = launch_data.get('configurations', [])
            playwright_debug_found = any(
                'playwright' in json.dumps(c).lower() and
                ('debug' in json.dumps(c).lower() or c.get('request') == 'launch')
                for c in configs
            )

            if playwright_debug_found:
                print("PASS: Component 5 — launch.json has Playwright debug configuration (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — launch.json exists but no Playwright debug config found. Configs: {[c.get('name', '') for c in configs]}")
        else:
            print("FAIL: Component 5 — .vscode/launch.json does not exist")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: tasks.json with e2e-test, e2e-headed, e2e-report tasks (0.15 points)
    try:
        tasks_path = os.path.join(VSCODE_DIR, 'tasks.json')
        if os.path.exists(tasks_path):
            with open(tasks_path, 'r') as f:
                content = f.read()
            # Strip JSONC comments
            clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            tasks_data = json.loads(clean)

            task_labels = [t.get('label', '') for t in tasks_data.get('tasks', [])]
            has_e2e_test = 'e2e-test' in task_labels
            has_e2e_headed = 'e2e-headed' in task_labels
            has_e2e_report = 'e2e-report' in task_labels

            found_count = sum([has_e2e_test, has_e2e_headed, has_e2e_report])
            sub_score = round(found_count * 0.05, 2)

            if sub_score > 0:
                print(f"PASS: Component 6 — tasks.json has {found_count}/3 required tasks: e2e-test={has_e2e_test}, e2e-headed={has_e2e_headed}, e2e-report={has_e2e_report} ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 6 — tasks.json missing all required tasks. Found labels: {task_labels}")
        else:
            print("FAIL: Component 6 — .vscode/tasks.json does not exist")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
