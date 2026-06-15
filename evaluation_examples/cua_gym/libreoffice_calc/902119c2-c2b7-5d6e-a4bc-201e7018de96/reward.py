"""
Reward Script: GitHub Actions CI workflow setup in VSCode
Task ID: vscode_web_087
Domain: vscode (file-based verification)
Scoring:
  Component 1: .github/workflows/ci.yml exists (0.1 pts)
  Component 2: Workflow triggers on push and pull_request to main (0.25 pts)
  Component 3: Workflow has a job with Node.js setup and dependency install (0.15 pts)
  Component 4: ESLint step present (0.2 pts)
  Component 5: TypeScript type-checking step present (0.2 pts)
  Component 6: Jest/npm test step present (0.1 pts)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_087'
CI_PATH = os.path.join(WORKDIR, 'projects', 'webapp', '.github', 'workflows', 'ci.yml')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: ci.yml must exist — if not, nothing to verify
    if not os.path.exists(CI_PATH):
        print(f"CRITICAL: ci.yml not found at {CI_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(CI_PATH, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read ci.yml: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse YAML content (use regex-based checks to avoid yaml dependency)
    content_lower = content.lower()

    # Component 1: File exists and is non-empty YAML with a workflow name or 'on:' trigger (0.1 pts)
    # This ONLY awards points if the file exists in .github/workflows/ — which it does NOT in initial_env
    try:
        has_on_trigger = bool(re.search(r'^on:', content, re.MULTILINE))
        has_jobs = bool(re.search(r'^jobs:', content, re.MULTILINE))
        if has_on_trigger and has_jobs:
            print(f"PASS: Component 1 — ci.yml has 'on:' trigger and 'jobs:' section (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — ci.yml missing 'on:' or 'jobs:' section")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Triggers on push AND pull_request to main branch (0.25 pts)
    try:
        has_push = bool(re.search(r'push:', content))
        has_pull_request = bool(re.search(r'pull_request:', content))
        # Check that 'main' branch is referenced in trigger context
        has_main_branch = bool(re.search(r'branches:.*main', content, re.DOTALL))
        # More specific: main in a branches list
        main_in_branches = bool(re.search(r'branches:\s*\[?\s*["\']?main', content))

        if has_push and has_pull_request and main_in_branches:
            print(f"PASS: Component 2 — push and pull_request triggers on main branch (0.25 pts)")
            total_score += 0.25
        else:
            missing = []
            if not has_push:
                missing.append("push trigger")
            if not has_pull_request:
                missing.append("pull_request trigger")
            if not main_in_branches:
                missing.append("main branch specification")
            print(f"FAIL: Component 2 — missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Job with Node.js setup and dependency installation (0.15 pts)
    try:
        has_node_setup = bool(re.search(r'setup-node', content))
        has_install = bool(re.search(r'npm\s+(ci|install)', content))
        if has_node_setup and has_install:
            print(f"PASS: Component 3 — Node.js setup and dependency install steps found (0.15 pts)")
            total_score += 0.15
        else:
            missing = []
            if not has_node_setup:
                missing.append("Node.js setup (actions/setup-node)")
            if not has_install:
                missing.append("npm install/ci step")
            print(f"FAIL: Component 3 — missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: ESLint step (0.2 pts)
    try:
        # Accept: npx eslint ., npm run lint, eslint
        has_eslint = bool(re.search(r'(npx\s+eslint|npm\s+run\s+lint|eslint\s+\.)', content))
        if has_eslint:
            print(f"PASS: Component 4 — ESLint step found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — No ESLint step found (expected 'npx eslint .' or 'npm run lint')")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: TypeScript type-checking step (0.2 pts)
    try:
        has_tsc = bool(re.search(r'(npx\s+tsc\s+--noEmit|tsc\s+--noEmit|npm\s+run\s+type[_-]?check)', content))
        if has_tsc:
            print(f"PASS: Component 5 — TypeScript type-checking step found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 — No TypeScript type-checking step (expected 'npx tsc --noEmit')")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Jest/npm test step (0.1 pts)
    try:
        has_test = bool(re.search(r'npm\s+test', content))
        if has_test:
            print(f"PASS: Component 6 — Jest test step found (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 6 — No test step found (expected 'npm test')")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
