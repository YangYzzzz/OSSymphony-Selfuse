"""
Reward Script: Serverless AWS SAM development workflow setup in VSCode
Task ID: vscode_wf_073
Domain: vscode (file-based verification)
Scoring:
  Component 1: AWS Toolkit extension installed (0.15)
  Component 2: template.yaml with SAM Lambda + API Gateway (0.20)
  Component 3: src/handler.py with Lambda handler (0.20)
  Component 4: requirements.txt exists with dependencies (0.05)
  Component 5: launch.json with SAM debug config (0.15)
  Component 6: tasks.json with sam-build, sam-local-api, sam-deploy (0.15)
  Component 7: VSCode settings with AWS region/profile (0.10)
"""

import json
import os
import re
import subprocess

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
VSCODE_DIR = os.path.join(PROJECT, '.vscode')
VSCODE_USER = os.path.join(WORKDIR, '.config', 'Code', 'User')
TASK_ID = 'vscode_wf_073'


def load_json_file(path):
    """Load a JSON file, stripping JSONC comments if needed."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """Verify task completion with progressive scoring. Returns float 0.0-1.0."""
    total_score = 0.0

    # Component 1: AWS Toolkit extension installed (0.15 points)
    try:
        result = subprocess.run(
            ['code', '--list-extensions'],
            capture_output=True, text=True, timeout=15
        )
        extensions = result.stdout.strip().lower().split('\n')
        if any('aws-toolkit' in ext or 'amazonwebservices' in ext for ext in extensions):
            print(f"PASS: Component 1 — AWS Toolkit extension installed (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — AWS Toolkit extension not found. Extensions: {extensions}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: template.yaml with SAM Lambda + API Gateway (0.20 points)
    try:
        template_path = os.path.join(PROJECT, 'template.yaml')
        if not os.path.exists(template_path):
            print(f"FAIL: Component 2 — template.yaml not found at {template_path}")
        else:
            with open(template_path, 'r') as f:
                content = f.read()
            content_lower = content.lower()
            has_sam_transform = 'aws::serverless' in content_lower
            has_lambda_func = 'aws::serverless::function' in content_lower
            has_api_event = 'type: api' in content_lower

            sub_score = 0.0
            if has_sam_transform and has_lambda_func:
                sub_score += 0.12
            if has_api_event:
                sub_score += 0.08

            if sub_score > 0:
                print(f"PASS: Component 2 — template.yaml SAM template found "
                      f"(transform={has_sam_transform}, lambda={has_lambda_func}, "
                      f"api={has_api_event}) ({sub_score:.2f} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 2 — template.yaml missing SAM structure "
                      f"(transform={has_sam_transform}, lambda={has_lambda_func}, api={has_api_event})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: src/handler.py with Lambda handler (0.20 points)
    try:
        handler_path = os.path.join(PROJECT, 'src', 'handler.py')
        if not os.path.exists(handler_path):
            print(f"FAIL: Component 3 — src/handler.py not found")
        else:
            with open(handler_path, 'r') as f:
                content = f.read()

            has_lambda_handler = 'def lambda_handler' in content
            has_event_param = 'event' in content and 'context' in content
            has_json_import = 'import json' in content
            has_response_body = 'statusCode' in content or 'statuscode' in content.lower()

            sub_score = 0.0
            if has_lambda_handler and has_event_param:
                sub_score += 0.12
            if has_json_import and has_response_body:
                sub_score += 0.08

            if sub_score > 0:
                print(f"PASS: Component 3 — handler.py Lambda handler found "
                      f"(handler_func={has_lambda_handler}, params={has_event_param}, "
                      f"json={has_json_import}, response={has_response_body}) ({sub_score:.2f} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 3 — handler.py missing Lambda handler structure")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: requirements.txt with dependencies (0.05 points)
    try:
        req_path = os.path.join(PROJECT, 'requirements.txt')
        if not os.path.exists(req_path):
            print(f"FAIL: Component 4 — requirements.txt not found")
        else:
            with open(req_path, 'r') as f:
                content = f.read().strip()
            if len(content) > 0:
                print(f"PASS: Component 4 — requirements.txt exists with content (0.05 pts)")
                total_score += 0.05
            else:
                print(f"FAIL: Component 4 — requirements.txt is empty")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: launch.json with SAM debug configuration (0.15 points)
    try:
        launch_path = os.path.join(VSCODE_DIR, 'launch.json')
        if not os.path.exists(launch_path):
            print(f"FAIL: Component 5 — launch.json not found")
        else:
            data = load_json_file(launch_path)
            configs = data.get('configurations', [])

            has_sam_config = False
            for cfg in configs:
                cfg_type = str(cfg.get('type', '')).lower()
                cfg_name = str(cfg.get('name', '')).lower()
                invoke_target = cfg.get('invokeTarget', {})
                target_type = str(invoke_target.get('target', '')).lower()

                if ('sam' in cfg_type or 'sam' in cfg_name) and 'template' in target_type:
                    has_sam_config = True
                    break

            if has_sam_config:
                print(f"PASS: Component 5 — launch.json has SAM debug configuration (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — launch.json missing SAM debug configuration. "
                      f"Configs: {[c.get('name') for c in configs]}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: tasks.json with sam-build, sam-local-api, sam-deploy (0.15 points)
    try:
        tasks_path = os.path.join(VSCODE_DIR, 'tasks.json')
        if not os.path.exists(tasks_path):
            print(f"FAIL: Component 6 — tasks.json not found")
        else:
            data = load_json_file(tasks_path)
            tasks = data.get('tasks', [])
            task_labels = [str(t.get('label', '')).lower() for t in tasks]

            required_tasks = ['sam-build', 'sam-local-api', 'sam-deploy']
            found = []
            missing = []
            for req in required_tasks:
                if any(req in label for label in task_labels):
                    found.append(req)
                else:
                    missing.append(req)

            # Progressive scoring: each task worth 0.05
            sub_score = len(found) * 0.05
            if sub_score > 0:
                print(f"PASS: Component 6 — tasks.json has {len(found)}/3 required tasks "
                      f"(found={found}, missing={missing}) ({sub_score:.2f} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 6 — tasks.json missing all required tasks. "
                      f"Labels found: {task_labels}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: VSCode settings with AWS region and profile (0.10 points)
    try:
        settings_path = os.path.join(VSCODE_USER, 'settings.json')
        if not os.path.exists(settings_path):
            print(f"FAIL: Component 7 — VSCode settings.json not found")
        else:
            settings = load_json_file(settings_path)

            has_region = False
            has_profile = False
            for key, val in settings.items():
                key_lower = key.lower()
                if 'aws' in key_lower and 'region' in key_lower and val:
                    has_region = True
                if 'aws' in key_lower and 'profile' in key_lower and val:
                    has_profile = True

            sub_score = 0.0
            if has_region:
                sub_score += 0.05
            if has_profile:
                sub_score += 0.05

            if sub_score > 0:
                print(f"PASS: Component 7 — AWS settings found "
                      f"(region={has_region}, profile={has_profile}) ({sub_score:.2f} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 7 — No AWS region/profile in settings. "
                      f"Keys: {list(settings.keys())}")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
