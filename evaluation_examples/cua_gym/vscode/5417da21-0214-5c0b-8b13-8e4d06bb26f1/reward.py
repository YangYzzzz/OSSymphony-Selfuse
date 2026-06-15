"""
Reward Script: GitHub Actions CI workflow with path-based filtering for monorepo
Task ID: vscode_gf3_065
Domain: vscode
Scoring:
  - Component 1 (0.15): ci.yml file exists at correct path
  - Component 2 (0.20): dorny/paths-filter@v3 used with backend/frontend filters
  - Component 3 (0.20): Backend test job conditional on backend path changes
  - Component 4 (0.20): Frontend test job conditional on frontend path changes
  - Component 5 (0.10): Shared tests always run (no path condition)
  - Component 6 (0.15): workflow_dispatch trigger with override input
"""

import os
import sys

# PyYAML may not be available; fall back to manual parsing
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_065'
CI_PATH = os.path.join(WORKDIR, 'projects', 'monorepo', '.github', 'workflows', 'ci.yml')


def parse_yaml_content(content):
    """Parse YAML content. Use PyYAML if available, else return raw text."""
    if HAS_YAML:
        return yaml.safe_load(content)
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: ci.yml file exists at correct path (0.15 points)
    # This checks the task-introduced change: the file must be CREATED
    try:
        if not os.path.exists(CI_PATH):
            print(f"FAIL: Component 1 — ci.yml not found at {CI_PATH}")
            print("REWARD: 0.0")
            return 0.0

        with open(CI_PATH, 'r') as f:
            content = f.read()

        if len(content.strip()) < 50:
            print(f"FAIL: Component 1 — ci.yml exists but is too short ({len(content.strip())} chars)")
            print("REWARD: 0.0")
            return 0.0

        print(f"PASS: Component 1 — ci.yml exists at correct path ({len(content)} bytes) (0.15 pts)")
        total_score += 0.15
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Try to parse as YAML for structured checks
    data = parse_yaml_content(content)
    content_lower = content.lower()

    # Component 2: dorny/paths-filter@v3 used with backend and frontend filters (0.20 points)
    try:
        has_paths_filter = False
        has_backend_filter = False
        has_frontend_filter = False

        if data and isinstance(data, dict):
            # Search in all jobs for uses: dorny/paths-filter
            jobs = data.get('jobs', {})
            if isinstance(jobs, dict):
                for job_name, job_def in jobs.items():
                    if not isinstance(job_def, dict):
                        continue
                    steps = job_def.get('steps', [])
                    if not isinstance(steps, list):
                        continue
                    for step in steps:
                        if not isinstance(step, dict):
                            continue
                        uses_val = str(step.get('uses', ''))
                        if 'dorny/paths-filter' in uses_val:
                            has_paths_filter = True
                            # Check the filters config
                            with_block = step.get('with', {})
                            if isinstance(with_block, dict):
                                filters_str = str(with_block.get('filters', ''))
                                if 'packages/backend' in filters_str:
                                    has_backend_filter = True
                                if 'packages/frontend' in filters_str:
                                    has_frontend_filter = True
        else:
            # Fallback: text-based check
            if 'dorny/paths-filter' in content:
                has_paths_filter = True
            if 'packages/backend' in content:
                has_backend_filter = True
            if 'packages/frontend' in content:
                has_frontend_filter = True

        if has_paths_filter and has_backend_filter and has_frontend_filter:
            print(f"PASS: Component 2 — dorny/paths-filter with backend+frontend filters (0.20 pts)")
            total_score += 0.20
        elif has_paths_filter:
            partial = 0.10
            missing = []
            if not has_backend_filter:
                missing.append('backend')
            if not has_frontend_filter:
                missing.append('frontend')
            print(f"PARTIAL: Component 2 — paths-filter found but missing filters: {missing} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — dorny/paths-filter not found in workflow")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Backend test job conditional on backend path changes (0.20 points)
    try:
        has_backend_job = False
        backend_conditional = False
        backend_runs_tests = False

        if data and isinstance(data, dict):
            jobs = data.get('jobs', {})
            if isinstance(jobs, dict):
                for job_name, job_def in jobs.items():
                    if not isinstance(job_def, dict):
                        continue
                    job_name_lower = job_name.lower()
                    # Look for a backend test job
                    steps = job_def.get('steps', [])
                    steps_text = str(steps).lower() if steps else ''
                    if_cond = str(job_def.get('if', '')).lower()

                    is_backend_job = (
                        'backend' in job_name_lower or
                        ('backend' in steps_text and 'test' in steps_text)
                    )

                    if is_backend_job and 'backend' in if_cond:
                        has_backend_job = True
                        backend_conditional = True
                        # Check it has needs pointing to detect-changes or similar
                        needs = job_def.get('needs', [])
                        if needs:
                            backend_conditional = True
                        # Check it runs tests
                        for step in (steps if isinstance(steps, list) else []):
                            if isinstance(step, dict):
                                run_cmd = str(step.get('run', ''))
                                if 'test' in run_cmd and 'backend' in run_cmd:
                                    backend_runs_tests = True
        else:
            # Text fallback
            if 'backend' in content_lower and 'test' in content_lower:
                has_backend_job = True
                # Check for if condition referencing backend
                import re
                if re.search(r"if:.*backend.*==.*'true'", content, re.IGNORECASE):
                    backend_conditional = True
                if re.search(r'test.*backend|backend.*test', content_lower):
                    backend_runs_tests = True

        if has_backend_job and backend_conditional:
            print(f"PASS: Component 3 — Backend test job with path-based condition (0.20 pts)")
            total_score += 0.20
        elif has_backend_job:
            print(f"PARTIAL: Component 3 — Backend test job found but no path condition (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — No backend test job found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Frontend test job conditional on frontend path changes (0.20 points)
    try:
        has_frontend_job = False
        frontend_conditional = False

        if data and isinstance(data, dict):
            jobs = data.get('jobs', {})
            if isinstance(jobs, dict):
                for job_name, job_def in jobs.items():
                    if not isinstance(job_def, dict):
                        continue
                    job_name_lower = job_name.lower()
                    steps = job_def.get('steps', [])
                    steps_text = str(steps).lower() if steps else ''
                    if_cond = str(job_def.get('if', '')).lower()

                    is_frontend_job = (
                        'frontend' in job_name_lower or
                        ('frontend' in steps_text and 'test' in steps_text)
                    )

                    if is_frontend_job and 'frontend' in if_cond:
                        has_frontend_job = True
                        frontend_conditional = True

        else:
            import re
            if 'frontend' in content_lower and 'test' in content_lower:
                has_frontend_job = True
                if re.search(r"if:.*frontend.*==.*'true'", content, re.IGNORECASE):
                    frontend_conditional = True

        if has_frontend_job and frontend_conditional:
            print(f"PASS: Component 4 — Frontend test job with path-based condition (0.20 pts)")
            total_score += 0.20
        elif has_frontend_job:
            print(f"PARTIAL: Component 4 — Frontend test job found but no path condition (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — No frontend test job found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Shared tests always run — no path-based condition (0.10 points)
    try:
        has_shared_job = False
        shared_unconditional = False

        if data and isinstance(data, dict):
            jobs = data.get('jobs', {})
            if isinstance(jobs, dict):
                for job_name, job_def in jobs.items():
                    if not isinstance(job_def, dict):
                        continue
                    job_name_lower = job_name.lower()
                    steps = job_def.get('steps', [])
                    steps_text = str(steps).lower() if steps else ''

                    is_shared_job = (
                        'shared' in job_name_lower or
                        ('shared' in steps_text and 'test' in steps_text)
                    )

                    if is_shared_job:
                        has_shared_job = True
                        # Shared should NOT have an 'if' condition that references path filter outputs
                        if_cond = str(job_def.get('if', '')).lower()
                        # It's unconditional if there's no 'if' at all, or the 'if' doesn't
                        # reference path filter outputs
                        if not if_cond or ('backend' not in if_cond and 'frontend' not in if_cond and 'shared' not in if_cond):
                            shared_unconditional = True
        else:
            if 'shared' in content_lower and 'test' in content_lower:
                has_shared_job = True
                shared_unconditional = True  # text fallback: assume unconditional

        if has_shared_job and shared_unconditional:
            print(f"PASS: Component 5 — Shared tests run unconditionally (0.10 pts)")
            total_score += 0.10
        elif has_shared_job:
            print(f"PARTIAL: Component 5 — Shared test job found but has path condition (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 5 — No shared test job found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: workflow_dispatch trigger with override input (0.15 points)
    try:
        has_workflow_dispatch = False
        has_override_input = False

        if data and isinstance(data, dict):
            on_block = data.get('on', data.get(True, {}))  # YAML parses 'on' as True sometimes
            if isinstance(on_block, dict):
                wd = on_block.get('workflow_dispatch', {})
                if wd is not None:
                    has_workflow_dispatch = True
                    if isinstance(wd, dict):
                        inputs = wd.get('inputs', {})
                        if isinstance(inputs, dict) and len(inputs) > 0:
                            # Check for any override-related input
                            for inp_name, inp_def in inputs.items():
                                inp_name_lower = inp_name.lower()
                                if 'override' in inp_name_lower or 'filter' in inp_name_lower or 'all' in inp_name_lower:
                                    has_override_input = True
                                    break
                            # Also check if the override input is referenced in job if conditions
                            if not has_override_input:
                                # Check if any input is of type boolean
                                for inp_name, inp_def in inputs.items():
                                    if isinstance(inp_def, dict) and inp_def.get('type') == 'boolean':
                                        has_override_input = True
                                        break
            elif isinstance(on_block, list):
                if 'workflow_dispatch' in on_block:
                    has_workflow_dispatch = True
        else:
            if 'workflow_dispatch' in content:
                has_workflow_dispatch = True
            if 'override' in content_lower:
                has_override_input = True

        # Also check if override input is referenced in job conditions (text check)
        if has_workflow_dispatch and not has_override_input:
            if 'override' in content_lower or 'github.event.inputs' in content:
                has_override_input = True

        if has_workflow_dispatch and has_override_input:
            print(f"PASS: Component 6 — workflow_dispatch with override input (0.15 pts)")
            total_score += 0.15
        elif has_workflow_dispatch:
            print(f"PARTIAL: Component 6 — workflow_dispatch found but no override input (0.08 pts)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 6 — No workflow_dispatch trigger found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(CI_PATH):
    print(f"File not found: {CI_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
