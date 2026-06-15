"""
Reward Script: GitLab CI/CD pipeline for Docker build, scan, push, deploy, test, manual production
Task ID: os_adm_067
Domain: os (file-based verification)
Scoring:
  - Component 1: File exists and valid YAML with 6 correct stages (0.20)
  - Component 2: build stage with docker build + CI_COMMIT_SHA tag (0.15)
  - Component 3: scan stage with trivy + CRITICAL severity (0.15)
  - Component 4: push stage to registry.internal:5000 with auth (0.15)
  - Component 5: deploy-staging with docker service update (0.10)
  - Component 6: test stage with integration test execution (0.10)
  - Component 7: deploy-production with when:manual + only:main (0.15)
"""

import os
import yaml

WORKDIR = '/home/user'
TASK_ID = 'os_adm_067'
CI_FILE = os.path.join(WORKDIR, 'webapp-inventory', '.gitlab-ci.yml')

EXPECTED_STAGES = ['build', 'scan', 'push', 'deploy-staging', 'test', 'deploy-production']


def verify_task(file_path):
    """
    Verify GitLab CI/CD pipeline task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load and parse YAML
    try:
        with open(file_path, 'r') as f:
            ci_config = yaml.safe_load(f)
        if not isinstance(ci_config, dict):
            print(f"CRITICAL: .gitlab-ci.yml is not a valid YAML mapping")
            print("REWARD: 0.0")
            return 0.0
    except FileNotFoundError:
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot parse YAML {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: stages list has all 6 required stages (0.20 points)
    try:
        stages = ci_config.get('stages', [])
        if isinstance(stages, list) and set(EXPECTED_STAGES) == set(stages) and len(stages) == 6:
            print(f"PASS: Component 1 — stages list has all 6 required stages: {stages} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — expected stages {EXPECTED_STAGES}, found {stages}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: build stage with docker build + CI_COMMIT_SHA tag (0.15 points)
    try:
        build_job = ci_config.get('build', {})
        if not isinstance(build_job, dict):
            print(f"FAIL: Component 2 — 'build' job not found or not a dict")
        else:
            build_stage_ok = build_job.get('stage') == 'build'
            scripts = build_job.get('script', [])
            script_text = ' '.join(str(s) for s in scripts) if isinstance(scripts, list) else str(scripts)
            has_docker_build = 'docker build' in script_text
            # CI_COMMIT_SHA may be referenced directly or via a variable alias (e.g., DOCKER_TAG)
            variables = ci_config.get('variables', {})
            variables_text = ' '.join(str(v) for v in variables.values()) if isinstance(variables, dict) else ''
            has_commit_sha = ('CI_COMMIT_SHA' in script_text or
                              'CI_COMMIT_SHA' in variables_text)
            if build_stage_ok and has_docker_build and has_commit_sha:
                print(f"PASS: Component 2 — build stage has docker build with CI_COMMIT_SHA (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — build stage: stage_ok={build_stage_ok}, docker_build={has_docker_build}, commit_sha={has_commit_sha}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: scan stage with trivy image + CRITICAL severity (0.15 points)
    try:
        scan_job = ci_config.get('scan', {})
        if not isinstance(scan_job, dict):
            print(f"FAIL: Component 3 — 'scan' job not found or not a dict")
        else:
            scan_stage_ok = scan_job.get('stage') == 'scan'
            scripts = scan_job.get('script', [])
            script_text = ' '.join(str(s) for s in scripts) if isinstance(scripts, list) else str(scripts)
            has_trivy = 'trivy image' in script_text or 'trivy' in script_text
            has_critical = 'CRITICAL' in script_text
            if scan_stage_ok and has_trivy and has_critical:
                print(f"PASS: Component 3 — scan stage with trivy + CRITICAL severity (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — scan stage: stage_ok={scan_stage_ok}, trivy={has_trivy}, critical={has_critical}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: push stage to registry.internal:5000 with CI variable auth (0.15 points)
    try:
        push_job = ci_config.get('push', {})
        if not isinstance(push_job, dict):
            print(f"FAIL: Component 4 — 'push' job not found or not a dict")
        else:
            push_stage_ok = push_job.get('stage') == 'push'
            scripts = push_job.get('script', [])
            script_text = ' '.join(str(s) for s in scripts) if isinstance(scripts, list) else str(scripts)
            has_registry = 'registry.internal:5000' in script_text or 'registry.internal' in script_text
            has_docker_push = 'docker push' in script_text
            # Check for CI variable-based authentication (e.g., $CI_REGISTRY_USER, $CI_REGISTRY_PASSWORD)
            has_ci_auth = ('CI_REGISTRY' in script_text or 'CI_DEPLOY' in script_text or
                           'docker login' in script_text)
            if push_stage_ok and has_registry and has_docker_push and has_ci_auth:
                print(f"PASS: Component 4 — push stage to registry.internal:5000 with auth (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — push: stage_ok={push_stage_ok}, registry={has_registry}, push={has_docker_push}, auth={has_ci_auth}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: deploy-staging with docker service update (0.10 points)
    try:
        deploy_staging_job = ci_config.get('deploy-staging', {})
        if not isinstance(deploy_staging_job, dict):
            print(f"FAIL: Component 5 — 'deploy-staging' job not found or not a dict")
        else:
            stage_ok = deploy_staging_job.get('stage') == 'deploy-staging'
            scripts = deploy_staging_job.get('script', [])
            script_text = ' '.join(str(s) for s in scripts) if isinstance(scripts, list) else str(scripts)
            has_service_update = 'docker service update' in script_text or 'docker stack deploy' in script_text
            if stage_ok and has_service_update:
                print(f"PASS: Component 5 — deploy-staging with docker service update (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — deploy-staging: stage_ok={stage_ok}, service_update={has_service_update}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: test stage with integration test execution (0.10 points)
    try:
        test_job = ci_config.get('test', {})
        if not isinstance(test_job, dict):
            print(f"FAIL: Component 6 — 'test' job not found or not a dict")
        else:
            stage_ok = test_job.get('stage') == 'test'
            scripts = test_job.get('script', [])
            script_text = ' '.join(str(s) for s in scripts) if isinstance(scripts, list) else str(scripts)
            # Check for some form of integration test execution (curl, test script, etc.)
            has_test = ('curl' in script_text or 'test' in script_text.lower() or
                        'pytest' in script_text or 'bash' in script_text)
            if stage_ok and has_test:
                print(f"PASS: Component 6 — test stage with integration test (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 — test: stage_ok={stage_ok}, has_test={has_test}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: deploy-production with when:manual + only:main (0.15 points)
    try:
        deploy_prod_job = ci_config.get('deploy-production', {})
        if not isinstance(deploy_prod_job, dict):
            print(f"FAIL: Component 7 — 'deploy-production' job not found or not a dict")
        else:
            stage_ok = deploy_prod_job.get('stage') == 'deploy-production'
            has_manual = deploy_prod_job.get('when') == 'manual'
            only_config = deploy_prod_job.get('only', [])
            has_only_main = 'main' in only_config if isinstance(only_config, list) else only_config == 'main'
            if stage_ok and has_manual and has_only_main:
                print(f"PASS: Component 7 — deploy-production with when:manual + only:main (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 7 — deploy-prod: stage_ok={stage_ok}, manual={has_manual}, only_main={has_only_main}")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
if not os.path.exists(CI_FILE):
    print(f"File not found: {CI_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(CI_FILE)
