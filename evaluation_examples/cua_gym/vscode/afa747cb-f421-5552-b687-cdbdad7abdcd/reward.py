"""
Reward Script: k6 load testing pipeline setup
Task ID: vscode_gf3_087
Domain: vscode
Scoring:
  Component 1 (0.35): k6/load-test.js exists with correct 3-stage VU ramp pattern
  Component 2 (0.25): k6/load-test.js has correct thresholds (p95<500ms, error rate<1%)
  Component 3 (0.20): VSCode task 'k6 Load Test' defined in .vscode/tasks.json
  Component 4 (0.20): GitHub Actions workflow runs k6 after staging deployment
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_087'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'api-service')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # =========================================================================
    # Component 1: k6/load-test.js exists with correct 3-stage VU ramp (0.35)
    # =========================================================================
    k6_path = os.path.join(PROJECT_DIR, 'k6', 'load-test.js')
    k6_content = None
    try:
        if not os.path.exists(k6_path):
            print(f"FAIL: Component 1 — k6/load-test.js does not exist at {k6_path}")
        else:
            with open(k6_path, 'r') as f:
                k6_content = f.read()

            # Check for 3-stage pattern:
            #   Stage 1: ramp up to 50 VUs over 1 minute
            #   Stage 2: hold at 50 VUs for 3 minutes
            #   Stage 3: ramp down over 30 seconds
            stage_checks = 0

            # Stage 1: ramp to 50 over 1m
            if re.search(r"duration.*['\"]1m['\"].*target.*50|target.*50.*duration.*['\"]1m['\"]", k6_content):
                stage_checks += 1
            elif re.search(r"duration.*['\"]60s['\"].*target.*50|target.*50.*duration.*['\"]60s['\"]", k6_content):
                stage_checks += 1

            # Stage 2: hold at 50 for 3m
            if re.search(r"duration.*['\"]3m['\"].*target.*50|target.*50.*duration.*['\"]3m['\"]", k6_content):
                stage_checks += 1
            elif re.search(r"duration.*['\"]180s['\"].*target.*50|target.*50.*duration.*['\"]180s['\"]", k6_content):
                stage_checks += 1

            # Stage 3: ramp down over 30s (target 0)
            if re.search(r"duration.*['\"]30s['\"].*target.*0|target.*0.*duration.*['\"]30s['\"]", k6_content):
                stage_checks += 1

            if stage_checks == 3:
                print(f"PASS: Component 1 — k6/load-test.js has all 3 stages correct (0.35 pts)")
                total_score += 0.35
            elif stage_checks >= 2:
                print(f"PARTIAL: Component 1 — {stage_checks}/3 stages correct (0.2 pts)")
                total_score += 0.2
            elif stage_checks >= 1:
                print(f"PARTIAL: Component 1 — {stage_checks}/3 stages correct (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 1 — No matching stages found in k6/load-test.js")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # =========================================================================
    # Component 2: Thresholds — p95 < 500ms and error rate < 1% (0.25)
    # =========================================================================
    try:
        if k6_content is None:
            print(f"FAIL: Component 2 — k6/load-test.js not available")
        else:
            threshold_checks = 0

            # Check p95 < 500ms threshold
            # Patterns: p(95)<500, p(95) < 500, ['p(95)<500']
            if re.search(r"http_req_duration.*p\(95\)\s*<\s*500", k6_content):
                threshold_checks += 1

            # Check error rate < 1%
            # Patterns: rate<0.01, rate < 0.01
            if re.search(r"http_req_failed.*rate\s*<\s*0\.01", k6_content):
                threshold_checks += 1

            if threshold_checks == 2:
                print(f"PASS: Component 2 — Both thresholds defined correctly (0.25 pts)")
                total_score += 0.25
            elif threshold_checks == 1:
                print(f"PARTIAL: Component 2 — Only {threshold_checks}/2 thresholds correct (0.12 pts)")
                total_score += 0.12
            else:
                print(f"FAIL: Component 2 — No valid thresholds found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # =========================================================================
    # Component 3: VSCode task 'k6 Load Test' in .vscode/tasks.json (0.20)
    # =========================================================================
    tasks_path = os.path.join(PROJECT_DIR, '.vscode', 'tasks.json')
    try:
        if not os.path.exists(tasks_path):
            print(f"FAIL: Component 3 — .vscode/tasks.json does not exist")
        else:
            with open(tasks_path, 'r') as f:
                content = f.read()
            # Strip JSONC comments before parsing
            clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            tasks_data = json.loads(clean)

            tasks_list = tasks_data.get('tasks', [])
            matching = [t for t in tasks_list
                        if 'k6' in t.get('label', '').lower()
                        and 'load' in t.get('label', '').lower()
                        and 'test' in t.get('label', '').lower()]

            if len(matching) > 0:
                print(f"PASS: Component 3 — 'k6 Load Test' task found in tasks.json (0.20 pts)")
                total_score += 0.20
            else:
                labels = [t.get('label', '') for t in tasks_list]
                print(f"FAIL: Component 3 — No 'k6 Load Test' task found. Labels: {labels}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # =========================================================================
    # Component 4: GitHub Actions workflow for k6 load testing (0.20)
    # =========================================================================
    try:
        workflows_dir = os.path.join(PROJECT_DIR, '.github', 'workflows')
        if not os.path.isdir(workflows_dir):
            print(f"FAIL: Component 4 — .github/workflows/ directory not found")
        else:
            # Search all yml/yaml files for a k6 workflow
            k6_workflow_file = None
            workflow_content = None

            for fname in os.listdir(workflows_dir):
                if fname.endswith(('.yml', '.yaml')):
                    fpath = os.path.join(workflows_dir, fname)
                    with open(fpath, 'r') as f:
                        wf_content = f.read()
                    # Check if this workflow runs k6
                    if re.search(r'k6\s+run', wf_content):
                        k6_workflow_file = fname
                        workflow_content = wf_content
                        break

            if k6_workflow_file is not None:
                # Verify it runs k6 load-test.js specifically
                if re.search(r'k6\s+run.*load-test', workflow_content):
                    print(f"PASS: Component 4 — Workflow '{k6_workflow_file}' runs k6 load-test (0.20 pts)")
                    total_score += 0.20
                elif re.search(r'k6\s+run', workflow_content):
                    print(f"PARTIAL: Component 4 — Workflow '{k6_workflow_file}' runs k6 but not load-test.js (0.10 pts)")
                    total_score += 0.10
            else:
                print(f"FAIL: Component 4 — No GitHub Actions workflow found that runs k6")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
