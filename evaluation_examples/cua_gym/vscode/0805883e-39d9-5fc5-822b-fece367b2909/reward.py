"""
Reward Script: Create GitHub Actions CI workflow file
Task ID: vscode_ops_069
Domain: vscode
Scoring:
  Component 1 - ci.yml exists at correct path (0.15)
  Component 2 - Triggers on push to main branch (0.25)
  Component 3 - Checkout step present (0.15)
  Component 4 - Setup Node.js 18 step present (0.20)
  Component 5 - npm install step present (0.10)
  Component 6 - npm test step present (0.15)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_069'
CI_PATH = os.path.join(WORKDIR, 'my-service', '.github', 'workflows', 'ci.yml')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: ci.yml not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load and parse YAML
    try:
        import yaml
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            print(f"CRITICAL: ci.yml is not a valid YAML mapping, got {type(data)}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot parse ci.yml as YAML: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Also read raw content for step verification
    with open(file_path, 'r') as f:
        raw_content = f.read()

    # Component 1: ci.yml exists at the correct path and is valid YAML (0.15 points)
    # We already verified existence and YAML parsing above — the file being at the
    # correct path (.github/workflows/ci.yml) and being parseable YAML is the check.
    # This FAILS on initial_env because the file doesn't exist there.
    try:
        if data and isinstance(data, dict):
            print(f"PASS: Component 1 - ci.yml exists and is valid YAML (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - ci.yml exists but is empty or not a mapping")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Triggers on push to main branch (0.25 points)
    try:
        on_trigger = data.get('on') or data.get(True)  # YAML parses 'on' as True sometimes
        push_config = None
        if isinstance(on_trigger, dict):
            push_config = on_trigger.get('push')
        elif isinstance(on_trigger, str) and on_trigger == 'push':
            # Simple 'on: push' without branch filter — partial credit
            pass

        if isinstance(push_config, dict):
            branches = push_config.get('branches', [])
            if 'main' in branches:
                print(f"PASS: Component 2 - Triggers on push to main (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 - push branches does not include 'main', found: {branches}")
        else:
            # Check if raw content contains the trigger pattern
            if re.search(r'on:\s*\n\s+push:\s*\n\s+branches:\s*\n\s+-\s*main', raw_content):
                print(f"PASS: Component 2 - Triggers on push to main (raw match) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 - No push trigger to main found. on_trigger={on_trigger}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Extract all steps from all jobs
    steps = []
    try:
        jobs = data.get('jobs', {})
        if isinstance(jobs, dict):
            for job_name, job_config in jobs.items():
                if isinstance(job_config, dict):
                    job_steps = job_config.get('steps', [])
                    if isinstance(job_steps, list):
                        steps.extend(job_steps)
    except Exception as e:
        print(f"ERROR: Could not extract steps: {e}")

    # Component 3: Checkout step using actions/checkout (0.15 points)
    try:
        has_checkout = False
        for step in steps:
            if isinstance(step, dict):
                uses = step.get('uses', '')
                if isinstance(uses, str) and 'actions/checkout' in uses:
                    has_checkout = True
                    break
        if has_checkout:
            print(f"PASS: Component 3 - Checkout step found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 - No actions/checkout step found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Setup Node.js 18 step (0.20 points)
    try:
        has_node_setup = False
        for step in steps:
            if isinstance(step, dict):
                uses = step.get('uses', '')
                if isinstance(uses, str) and 'actions/setup-node' in uses:
                    with_config = step.get('with', {})
                    if isinstance(with_config, dict):
                        node_version = str(with_config.get('node-version', ''))
                        if '18' in node_version:
                            has_node_setup = True
                            break
        if has_node_setup:
            print(f"PASS: Component 4 - Setup Node.js 18 step found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 - No actions/setup-node with node-version 18 found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: npm install step (0.10 points)
    try:
        has_npm_install = False
        for step in steps:
            if isinstance(step, dict):
                run_cmd = step.get('run', '')
                if isinstance(run_cmd, str) and 'npm install' in run_cmd:
                    has_npm_install = True
                    break
                # Also check 'npm ci' as a valid alternative
                if isinstance(run_cmd, str) and 'npm ci' in run_cmd:
                    has_npm_install = True
                    break
        if has_npm_install:
            print(f"PASS: Component 5 - npm install step found (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 - No npm install step found")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: npm test step (0.15 points)
    try:
        has_npm_test = False
        for step in steps:
            if isinstance(step, dict):
                run_cmd = step.get('run', '')
                if isinstance(run_cmd, str) and 'npm test' in run_cmd:
                    has_npm_test = True
                    break
        if has_npm_test:
            print(f"PASS: Component 6 - npm test step found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 - No npm test step found")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(CI_PATH):
    print(f"File not found: {CI_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(CI_PATH)
