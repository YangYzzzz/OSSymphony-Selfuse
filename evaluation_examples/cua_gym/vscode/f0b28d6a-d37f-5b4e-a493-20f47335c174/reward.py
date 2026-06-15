"""
Reward Script: CI pipeline for monorepo with job dependencies
Task ID: vscode_gf3_083
Domain: vscode
Scoring:
  Component 1 (0.10): YAML file exists and is valid YAML with jobs
  Component 2 (0.25): lint job with ESLint, Prettier, flake8, black
  Component 3 (0.20): test-frontend job needs lint, runs Jest
  Component 4 (0.25): test-backend job needs lint, postgres service, runs pytest
  Component 5 (0.20): e2e job needs both test jobs, runs Playwright
"""

import os
import yaml  # PyYAML is available on the VM

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_083'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'fullstack-app', '.github', 'workflows', 'pr-checks.yml')


def normalize(s):
    """Lowercase and strip a string for flexible matching."""
    if isinstance(s, str):
        return s.strip().lower()
    return str(s).strip().lower()


def yaml_contains(text, keyword):
    """Check if a keyword appears in a YAML text dump (case-insensitive)."""
    return keyword.lower() in text.lower()


def get_needs(job):
    """Extract needs as a list from a job dict."""
    needs = job.get('needs', [])
    if isinstance(needs, str):
        needs = [needs]
    return [normalize(n) for n in needs]


def verify_task():
    total_score = 0.0

    # Precondition: File must exist
    if not os.path.exists(FILE_PATH):
        print(f"CRITICAL: File not found: {FILE_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: Must be valid YAML with a 'jobs' key
    try:
        with open(FILE_PATH, 'r') as f:
            content = f.read()
        data = yaml.safe_load(content)
        if not isinstance(data, dict) or 'jobs' not in data:
            print("CRITICAL: YAML does not contain 'jobs' key")
            print("REWARD: 0.0")
            return 0.0
        jobs = data['jobs']
    except Exception as e:
        print(f"CRITICAL: Cannot parse YAML: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1 (0.10 pts): File is valid YAML with jobs and uses pull_request trigger
    try:
        has_jobs = isinstance(jobs, dict) and len(jobs) >= 4
        # Check that it triggers on pull_request
        on_trigger = data.get('on', data.get(True, {}))
        has_pr_trigger = False
        if isinstance(on_trigger, dict):
            has_pr_trigger = 'pull_request' in on_trigger
        elif isinstance(on_trigger, list):
            has_pr_trigger = 'pull_request' in on_trigger
        elif isinstance(on_trigger, str):
            has_pr_trigger = on_trigger == 'pull_request'

        if has_jobs and has_pr_trigger:
            print(f"PASS: Component 1 — Valid YAML with {len(jobs)} jobs and PR trigger (0.10 pts)")
            total_score += 0.10
        elif has_jobs:
            print(f"PARTIAL: Component 1 — Has {len(jobs)} jobs but no PR trigger (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 1 — Expected >=4 jobs, found {len(jobs) if isinstance(jobs, dict) else 0}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Helper: find a job by name (case-insensitive key match)
    def find_job(name):
        for k, v in jobs.items():
            if normalize(k) == normalize(name):
                return v
        return None

    # Helper: dump job steps to string for keyword searching
    def steps_text(job):
        steps = job.get('steps', [])
        parts = []
        for step in steps:
            if isinstance(step, dict):
                for key in ('run', 'name', 'uses'):
                    val = step.get(key, '')
                    if val:
                        parts.append(str(val))
                # Also check nested 'with' values
                w = step.get('with', {})
                if isinstance(w, dict):
                    for wv in w.values():
                        parts.append(str(wv))
        return ' '.join(parts)

    # Component 2 (0.25 pts): lint job with ESLint, Prettier, flake8, black
    try:
        lint_job = find_job('lint')
        if lint_job is None:
            print("FAIL: Component 2 — No 'lint' job found")
        else:
            st = steps_text(lint_job)
            checks = {
                'eslint': 'eslint' in st.lower(),
                'prettier': 'prettier' in st.lower(),
                'flake8': 'flake8' in st.lower(),
                'black': 'black' in st.lower(),
            }
            passed = sum(checks.values())
            if passed == 4:
                print(f"PASS: Component 2 — lint job has all 4 linters (0.25 pts)")
                total_score += 0.25
            elif passed >= 2:
                partial = round(0.25 * passed / 4, 2)
                missing = [k for k, v in checks.items() if not v]
                print(f"PARTIAL: Component 2 — lint job has {passed}/4 linters, missing: {missing} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — lint job missing linters: {[k for k, v in checks.items() if not v]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3 (0.20 pts): test-frontend job needs lint, runs Jest
    try:
        tf_job = find_job('test-frontend')
        if tf_job is None:
            print("FAIL: Component 3 — No 'test-frontend' job found")
        else:
            needs = get_needs(tf_job)
            needs_lint = 'lint' in needs
            st = steps_text(tf_job)
            has_jest = 'jest' in st.lower()

            if needs_lint and has_jest:
                print(f"PASS: Component 3 — test-frontend needs lint and runs Jest (0.20 pts)")
                total_score += 0.20
            elif needs_lint or has_jest:
                partial = 0.10
                print(f"PARTIAL: Component 3 — needs_lint={needs_lint}, has_jest={has_jest} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — needs_lint={needs_lint}, has_jest={has_jest}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4 (0.25 pts): test-backend job needs lint, postgres service, pytest
    try:
        tb_job = find_job('test-backend')
        if tb_job is None:
            print("FAIL: Component 4 — No 'test-backend' job found")
        else:
            needs = get_needs(tb_job)
            needs_lint = 'lint' in needs

            # Check postgres service container
            services = tb_job.get('services', {})
            has_postgres = any(
                'postgres' in normalize(svc_name) or
                (isinstance(svc_conf, dict) and 'postgres' in normalize(str(svc_conf.get('image', ''))))
                for svc_name, svc_conf in (services.items() if isinstance(services, dict) else [])
            )

            st = steps_text(tb_job)
            has_pytest = 'pytest' in st.lower()

            sub_checks = {
                'needs_lint': needs_lint,
                'has_postgres': has_postgres,
                'has_pytest': has_pytest,
            }
            passed = sum(sub_checks.values())
            if passed == 3:
                print(f"PASS: Component 4 — test-backend needs lint, has postgres service, runs pytest (0.25 pts)")
                total_score += 0.25
            elif passed >= 1:
                partial = round(0.25 * passed / 3, 2)
                missing = [k for k, v in sub_checks.items() if not v]
                print(f"PARTIAL: Component 4 — {passed}/3 checks, missing: {missing} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — all sub-checks failed: {sub_checks}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5 (0.20 pts): e2e job needs both test jobs, runs Playwright
    try:
        e2e_job = find_job('e2e')
        if e2e_job is None:
            print("FAIL: Component 5 — No 'e2e' job found")
        else:
            needs = get_needs(e2e_job)
            needs_tf = 'test-frontend' in needs
            needs_tb = 'test-backend' in needs
            needs_both = needs_tf and needs_tb

            st = steps_text(e2e_job)
            has_playwright = 'playwright' in st.lower()

            if needs_both and has_playwright:
                print(f"PASS: Component 5 — e2e needs both test jobs and runs Playwright (0.20 pts)")
                total_score += 0.20
            elif (needs_tf or needs_tb) and has_playwright:
                partial = 0.10
                print(f"PARTIAL: Component 5 — needs_tf={needs_tf}, needs_tb={needs_tb}, playwright={has_playwright} ({partial} pts)")
                total_score += partial
            elif has_playwright:
                partial = 0.05
                print(f"PARTIAL: Component 5 — has Playwright but wrong needs ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — needs_both={needs_both}, playwright={has_playwright}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
