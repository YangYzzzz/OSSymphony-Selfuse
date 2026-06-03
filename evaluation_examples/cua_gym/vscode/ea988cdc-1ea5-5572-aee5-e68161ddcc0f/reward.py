"""
Reward Script: GitHub Actions coverage workflow configuration
Task ID: vscode_gf3_056
Domain: vscode
Scoring:
  Component 1 (0.15): Valid YAML workflow file with proper structure and PR trigger
  Component 2 (0.25): Jest test step runs with coverage flags
  Component 3 (0.30): codecov/codecov-action@v4 step with proper config
  Component 4 (0.30): actions/github-script step that posts coverage comment to PR
"""

import os
import yaml

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_056'
FILE_PATH = os.path.join(WORKDIR, 'projects', 'webapp', '.github', 'workflows', 'coverage.yml')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load and parse YAML
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        workflow = yaml.safe_load(content)
        if not isinstance(workflow, dict):
            print(f"CRITICAL: File is not a valid YAML mapping")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot parse YAML: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid workflow structure with PR trigger (0.15 points)
    # The workflow must have a 'name', 'on' trigger for pull_request, and 'jobs'
    try:
        has_name = isinstance(workflow.get('name'), str) and len(workflow.get('name', '')) > 0
        has_jobs = isinstance(workflow.get('jobs'), dict) and len(workflow.get('jobs', {})) > 0

        # Check for pull_request trigger
        on_trigger = workflow.get('on') or workflow.get(True)  # YAML parses 'on' as True sometimes
        has_pr_trigger = False
        if isinstance(on_trigger, dict):
            has_pr_trigger = 'pull_request' in on_trigger
        elif isinstance(on_trigger, list):
            has_pr_trigger = 'pull_request' in on_trigger
        elif isinstance(on_trigger, str):
            has_pr_trigger = on_trigger == 'pull_request'

        if has_name and has_jobs and has_pr_trigger:
            print(f"PASS: Component 1 — Valid workflow with name='{workflow.get('name')}', has jobs, PR trigger (0.15 pts)")
            total_score += 0.15
        else:
            missing = []
            if not has_name:
                missing.append('name')
            if not has_jobs:
                missing.append('jobs')
            if not has_pr_trigger:
                missing.append('pull_request trigger')
            print(f"FAIL: Component 1 — Missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Helper: collect all steps across all jobs
    all_steps = []
    jobs = workflow.get('jobs', {})
    if isinstance(jobs, dict):
        for job_name, job_config in jobs.items():
            if isinstance(job_config, dict) and isinstance(job_config.get('steps'), list):
                all_steps.extend(job_config['steps'])

    # Component 2: Jest coverage step (0.25 points)
    # Must have a step that runs jest with --coverage flag
    try:
        jest_coverage_found = False
        for step in all_steps:
            if not isinstance(step, dict):
                continue
            run_cmd = step.get('run', '')
            if isinstance(run_cmd, str) and 'jest' in run_cmd.lower() and '--coverage' in run_cmd.lower():
                jest_coverage_found = True
                print(f"PASS: Component 2 — Jest coverage step found: '{run_cmd.strip()}' (0.25 pts)")
                total_score += 0.25
                break
        if not jest_coverage_found:
            print(f"FAIL: Component 2 — No step found running jest with --coverage")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: codecov/codecov-action@v4 step (0.30 points)
    # Must use codecov/codecov-action@v4 (or v4.x)
    try:
        codecov_found = False
        for step in all_steps:
            if not isinstance(step, dict):
                continue
            uses_val = step.get('uses', '')
            if isinstance(uses_val, str) and 'codecov/codecov-action@v4' in uses_val:
                codecov_found = True
                # Partial: check for token configuration
                with_config = step.get('with', {})
                has_token = False
                if isinstance(with_config, dict):
                    token_val = str(with_config.get('token', ''))
                    if 'CODECOV_TOKEN' in token_val or 'codecov' in token_val.lower():
                        has_token = True

                if has_token:
                    print(f"PASS: Component 3 — codecov-action@v4 with CODECOV_TOKEN configured (0.30 pts)")
                    total_score += 0.30
                else:
                    # Still give most credit for having the action, just missing token config
                    print(f"PARTIAL: Component 3 — codecov-action@v4 found but CODECOV_TOKEN not configured (0.20 pts)")
                    total_score += 0.20
                break
        if not codecov_found:
            print(f"FAIL: Component 3 — No codecov/codecov-action@v4 step found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: actions/github-script step that posts PR comment (0.30 points)
    # Must use actions/github-script and include code that creates a PR comment
    try:
        github_script_found = False
        for step in all_steps:
            if not isinstance(step, dict):
                continue
            uses_val = step.get('uses', '')
            if isinstance(uses_val, str) and 'actions/github-script' in uses_val:
                github_script_found = True
                with_config = step.get('with', {})
                script_content = ''
                if isinstance(with_config, dict):
                    script_content = str(with_config.get('script', ''))

                # Check the script creates a comment (createComment or create_comment)
                has_comment_creation = (
                    'createComment' in script_content or
                    'create_comment' in script_content or
                    'createcomment' in script_content.lower()
                )
                # Check script references coverage
                has_coverage_ref = (
                    'coverage' in script_content.lower() or
                    'Coverage' in script_content
                )

                if has_comment_creation and has_coverage_ref:
                    print(f"PASS: Component 4 — github-script posts coverage comment to PR (0.30 pts)")
                    total_score += 0.30
                elif has_comment_creation:
                    print(f"PARTIAL: Component 4 — github-script creates comment but no coverage reference (0.20 pts)")
                    total_score += 0.20
                elif has_coverage_ref:
                    print(f"PARTIAL: Component 4 — github-script references coverage but no createComment call (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 4 — github-script found but no comment creation or coverage reference in script")
                break
        if not github_script_found:
            print(f"FAIL: Component 4 — No actions/github-script step found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
