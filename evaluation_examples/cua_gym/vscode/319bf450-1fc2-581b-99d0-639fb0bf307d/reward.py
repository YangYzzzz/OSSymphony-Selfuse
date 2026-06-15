"""
Reward Script: Go Swagger/OpenAPI Documentation Generation
Task ID: vscode_gf6_084
Domain: vscode
Scoring:
  C1 (0.10) - swag CLI installed
  C2 (0.15) - go.mod has swaggo dependencies
  C3 (0.20) - main.go has swagger annotations (@title, @version, @host, @BasePath)
  C4 (0.20) - all 5 handler functions have swagger annotations
  C5 (0.10) - main.go registers swagger UI route at /swagger/
  C6 (0.10) - docs/ directory has swagger.json and swagger.yaml
  C7 (0.05) - Makefile has 'docs' target
  C8 (0.10) - .vscode/tasks.json has 'Swagger: Generate' task
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'projects', 'go-swagger')


def verify_task():
    total_score = 0.0

    # Component 1: swag CLI installed (0.10 points)
    try:
        swag_path = os.path.join(WORKDIR, 'go', 'bin', 'swag')
        if os.path.isfile(swag_path) and os.access(swag_path, os.X_OK):
            print(f"PASS: Component 1 - swag CLI found at {swag_path} (0.10 pts)")
            total_score += 0.10
        else:
            # Also check PATH
            import shutil
            swag_which = shutil.which('swag')
            if swag_which:
                print(f"PASS: Component 1 - swag CLI found in PATH at {swag_which} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 1 - swag CLI not found")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: go.mod has swaggo dependencies (0.15 points)
    try:
        gomod_path = os.path.join(PROJECT, 'go.mod')
        with open(gomod_path, 'r') as f:
            gomod_content = f.read()

        has_http_swagger = 'github.com/swaggo/http-swagger' in gomod_content
        has_swag = 'github.com/swaggo/swag' in gomod_content

        if has_http_swagger and has_swag:
            print(f"PASS: Component 2 - go.mod has both swaggo/http-swagger and swaggo/swag (0.15 pts)")
            total_score += 0.15
        elif has_http_swagger or has_swag:
            print(f"PARTIAL: Component 2 - go.mod has one of swaggo deps (http-swagger={has_http_swagger}, swag={has_swag}) (0.08 pts)")
            total_score += 0.08
        else:
            print(f"FAIL: Component 2 - go.mod missing swaggo dependencies")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: main.go has swagger annotations (0.20 points)
    try:
        main_path = os.path.join(PROJECT, 'cmd', 'server', 'main.go')
        with open(main_path, 'r') as f:
            main_content = f.read()

        annotations = {
            '@title': bool(re.search(r'//\s*@title\s+', main_content)),
            '@version': bool(re.search(r'//\s*@version\s+', main_content)),
            '@host': bool(re.search(r'//\s*@host\s+', main_content)),
            '@BasePath': bool(re.search(r'//\s*@BasePath\s+', main_content)),
        }
        found_count = sum(annotations.values())

        # Also check for @description (bonus but not required for full score)
        has_description = bool(re.search(r'//\s*@description\s+', main_content))

        if found_count == 4:
            print(f"PASS: Component 3 - main.go has all 4 required annotations: {annotations} (0.20 pts)")
            total_score += 0.20
        elif found_count >= 2:
            pts = round(0.20 * found_count / 4, 2)
            print(f"PARTIAL: Component 3 - main.go has {found_count}/4 annotations: {annotations} ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 3 - main.go missing swagger annotations: {annotations}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: All 5 handler functions have swagger annotations (0.20 points)
    try:
        handlers_path = os.path.join(PROJECT, 'internal', 'handlers', 'users.go')
        with open(handlers_path, 'r') as f:
            handlers_content = f.read()

        # The 5 handler functions to check
        handler_names = ['ListUsers', 'CreateUser', 'GetUser', 'UpdateUser', 'DeleteUser']
        annotated_count = 0

        for handler in handler_names:
            # Look for swagger godoc annotations before the function
            # Pattern: // <HandlerName> godoc  (or just @Summary/@Router before func <Handler>)
            # Find the function definition and look backwards for annotations
            func_pattern = rf'func\s+{handler}\s*\('
            func_match = re.search(func_pattern, handlers_content)
            if func_match:
                # Get the text before this function (up to 2000 chars back)
                start = max(0, func_match.start() - 2000)
                preceding = handlers_content[start:func_match.start()]

                # Check for swagger annotations in the block before the function
                has_summary = bool(re.search(r'//\s*@Summary\s+', preceding.split('\n\n')[-1] if '\n\n' in preceding else preceding))
                has_router = bool(re.search(r'//\s*@Router\s+', preceding.split('\n\n')[-1] if '\n\n' in preceding else preceding))

                if has_summary and has_router:
                    annotated_count += 1

        if annotated_count == 5:
            print(f"PASS: Component 4 - All 5 handlers have swagger annotations (0.20 pts)")
            total_score += 0.20
        elif annotated_count > 0:
            pts = round(0.20 * annotated_count / 5, 2)
            print(f"PARTIAL: Component 4 - {annotated_count}/5 handlers annotated ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 4 - No handler functions have swagger annotations")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Swagger UI route registered at /swagger/ (0.10 points)
    try:
        main_path = os.path.join(PROJECT, 'cmd', 'server', 'main.go')
        with open(main_path, 'r') as f:
            main_content = f.read()

        # Check for swagger route registration and httpSwagger import
        has_swagger_route = bool(re.search(r'/swagger/', main_content))
        has_http_swagger_import = bool(re.search(r'(httpSwagger|http-swagger|swaggo/http-swagger)', main_content))

        if has_swagger_route and has_http_swagger_import:
            print(f"PASS: Component 5 - Swagger UI route registered at /swagger/ (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 - swagger route={has_swagger_route}, import={has_http_swagger_import}")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: docs/ directory with swagger.json and swagger.yaml (0.10 points)
    try:
        docs_dir = os.path.join(PROJECT, 'docs')
        has_json = os.path.isfile(os.path.join(docs_dir, 'swagger.json'))
        has_yaml = os.path.isfile(os.path.join(docs_dir, 'swagger.yaml'))

        if has_json and has_yaml:
            # Validate swagger.json is valid JSON with expected structure
            with open(os.path.join(docs_dir, 'swagger.json'), 'r') as f:
                swagger_data = json.load(f)
            if 'swagger' in swagger_data or 'openapi' in swagger_data:
                print(f"PASS: Component 6 - docs/ has valid swagger.json and swagger.yaml (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 - swagger.json exists but missing swagger/openapi field")
        elif has_json or has_yaml:
            print(f"PARTIAL: Component 6 - docs/ has json={has_json}, yaml={has_yaml} (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 6 - docs/ directory missing or empty")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    # Component 7: Makefile has 'docs' target (0.05 points)
    try:
        makefile_path = os.path.join(PROJECT, 'Makefile')
        with open(makefile_path, 'r') as f:
            makefile_content = f.read()

        # Check for 'docs' target - look for "docs:" at the start of a line
        has_docs_target = bool(re.search(r'^docs\s*:', makefile_content, re.MULTILINE))
        # Also check it runs swag
        has_swag_cmd = 'swag' in makefile_content

        if has_docs_target and has_swag_cmd:
            print(f"PASS: Component 7 - Makefile has 'docs' target with swag command (0.05 pts)")
            total_score += 0.05
        elif has_docs_target:
            print(f"PARTIAL: Component 7 - Makefile has 'docs' target but no swag command (0.03 pts)")
            total_score += 0.03
        else:
            print(f"FAIL: Component 7 - Makefile missing 'docs' target")
    except Exception as e:
        print(f"ERROR: Component 7 - {e}")

    # Component 8: .vscode/tasks.json has 'Swagger: Generate' task (0.10 points)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        with open(tasks_path, 'r') as f:
            tasks_data = json.load(f)

        tasks = tasks_data.get('tasks', [])
        matching_tasks = [
            t for t in tasks
            if 'swagger' in t.get('label', '').lower()
            and 'generate' in t.get('label', '').lower()
        ]

        if len(matching_tasks) > 0:
            print(f"PASS: Component 8 - tasks.json has Swagger Generate task (0.10 pts)")
            total_score += 0.10
        else:
            labels = [t.get('label', '') for t in tasks]
            print(f"FAIL: Component 8 - No Swagger Generate task found. Labels: {labels}")
    except FileNotFoundError:
        print(f"FAIL: Component 8 - .vscode/tasks.json does not exist")
    except Exception as e:
        print(f"ERROR: Component 8 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
