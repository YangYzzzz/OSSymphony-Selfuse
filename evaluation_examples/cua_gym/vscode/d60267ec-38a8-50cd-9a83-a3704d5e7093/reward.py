"""
Reward Script: Create GitHub Actions CI workflow for VSCode extension project
Task ID: vscode_gf3_017
Domain: vscode
Scoring:
  - Component 1 (0.20): Valid YAML with push+pull_request triggers on main branch
  - Component 2 (0.25): Job named 'test' running on 'ubuntu-latest'
  - Component 3 (0.20): Checkout step present (actions/checkout)
  - Component 4 (0.15): Node.js 18 setup step present (actions/setup-node with node-version 18)
  - Component 5 (0.20): npm ci and npm test run steps present
"""

import os
import sys

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_017'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'extension-project', '.github', 'workflows', 'vscode-ci.yml')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: file must exist — if not, nothing to verify
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Gate: file must be valid YAML
    try:
        import yaml
    except ImportError:
        # Fallback: try to install pyyaml or parse manually
        print("WARN: pyyaml not available, attempting manual parse")
        yaml = None

    content = None
    data = None
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        if yaml:
            data = yaml.safe_load(content)
        else:
            # Minimal fallback: use a simple approach
            # Try json first (won't work for YAML), then basic string checks
            data = None
    except Exception as e:
        print(f"CRITICAL: Cannot read/parse file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if data is None and content is not None:
        # Fallback: string-based verification if YAML parser unavailable
        print("WARN: Using string-based verification (no YAML parser)")
        data = _string_based_parse(content)

    if not isinstance(data, dict):
        print(f"CRITICAL: YAML file does not parse to a dict, got: {type(data)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid YAML with push + pull_request triggers on 'main' branch (0.20 points)
    try:
        on_config = data.get('on') or data.get(True)  # YAML parses 'on' as True sometimes
        has_push_main = False
        has_pr_main = False

        if isinstance(on_config, dict):
            # Check push trigger
            push_cfg = on_config.get('push', {})
            if isinstance(push_cfg, dict):
                branches = push_cfg.get('branches', [])
                if isinstance(branches, list):
                    has_push_main = 'main' in branches
                elif isinstance(branches, str):
                    has_push_main = branches == 'main'

            # Check pull_request trigger
            pr_cfg = on_config.get('pull_request', {})
            if isinstance(pr_cfg, dict):
                branches = pr_cfg.get('branches', [])
                if isinstance(branches, list):
                    has_pr_main = 'main' in branches
                elif isinstance(branches, str):
                    has_pr_main = branches == 'main'

        if has_push_main and has_pr_main:
            print(f"PASS: Component 1 — push and pull_request triggers on 'main' (0.20 pts)")
            total_score += 0.20
        elif has_push_main or has_pr_main:
            print(f"PARTIAL: Component 1 — only one trigger found (push_main={has_push_main}, pr_main={has_pr_main}) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — triggers not configured for main branch. on_config={on_config}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Job named 'test' running on 'ubuntu-latest' (0.25 points)
    try:
        jobs = data.get('jobs', {})
        if isinstance(jobs, dict) and 'test' in jobs:
            test_job = jobs['test']
            runs_on = test_job.get('runs-on', '') if isinstance(test_job, dict) else ''
            if runs_on == 'ubuntu-latest':
                print(f"PASS: Component 2 — job 'test' runs on 'ubuntu-latest' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"PARTIAL: Component 2 — job 'test' exists but runs-on='{runs_on}' not 'ubuntu-latest' (0.10 pts)")
                total_score += 0.10
        else:
            print(f"FAIL: Component 2 — no job named 'test' found. Jobs: {list(jobs.keys()) if isinstance(jobs, dict) else jobs}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Get steps for remaining components
    steps = []
    try:
        jobs = data.get('jobs', {})
        if isinstance(jobs, dict) and 'test' in jobs:
            test_job = jobs['test']
            if isinstance(test_job, dict):
                steps = test_job.get('steps', [])
                if not isinstance(steps, list):
                    steps = []
    except Exception:
        steps = []

    # Component 3: Checkout step present (0.20 points)
    try:
        has_checkout = False
        for step in steps:
            if isinstance(step, dict):
                uses = step.get('uses', '')
                if isinstance(uses, str) and 'actions/checkout' in uses:
                    has_checkout = True
                    break
        if has_checkout:
            print(f"PASS: Component 3 — checkout step found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — no actions/checkout step found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Node.js 18 setup step (0.15 points)
    try:
        has_node_setup = False
        for step in steps:
            if isinstance(step, dict):
                uses = step.get('uses', '')
                if isinstance(uses, str) and 'actions/setup-node' in uses:
                    with_cfg = step.get('with', {})
                    if isinstance(with_cfg, dict):
                        node_ver = str(with_cfg.get('node-version', ''))
                        if node_ver.strip().strip("'\"") == '18' or node_ver.startswith('18'):
                            has_node_setup = True
                            break
        if has_node_setup:
            print(f"PASS: Component 4 — Node.js 18 setup step found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — no actions/setup-node with node-version 18 found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: npm ci and npm test run steps (0.20 points)
    try:
        has_npm_ci = False
        has_npm_test = False
        for step in steps:
            if isinstance(step, dict):
                run_cmd = step.get('run', '')
                if isinstance(run_cmd, str):
                    # Check for npm ci (could be part of a multi-line run or standalone)
                    if 'npm ci' in run_cmd:
                        has_npm_ci = True
                    if 'npm test' in run_cmd:
                        has_npm_test = True
        if has_npm_ci and has_npm_test:
            print(f"PASS: Component 5 — npm ci and npm test steps found (0.20 pts)")
            total_score += 0.20
        elif has_npm_ci or has_npm_test:
            print(f"PARTIAL: Component 5 — npm_ci={has_npm_ci}, npm_test={has_npm_test} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — neither npm ci nor npm test found in steps")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


def _string_based_parse(content):
    """Minimal string-based YAML-like parsing fallback."""
    # This is a last resort — prefer pyyaml
    import re
    result = {}
    # Just return None to signal we need yaml
    return None


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
