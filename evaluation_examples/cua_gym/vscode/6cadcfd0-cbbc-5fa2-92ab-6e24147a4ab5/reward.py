"""
Reward Script: Docker development environment for Go web service
Task ID: vscode_gf6_044
Domain: vscode
Scoring:
  - Component 1: Dockerfile with two-stage build (0.25)
  - Component 2: docker-compose.yml with app/postgres/redis (0.25)
  - Component 3: docker-compose.dev.yml override (0.15)
  - Component 4: Makefile docker targets (0.20)
  - Component 5: .vscode/tasks.json with docker tasks (0.15)
"""

import os
import re
import json

WORKDIR = '/home/user/projects/go-docker-dev'
TASK_ID = 'vscode_gf6_044'


def verify_task():
    total_score = 0.0

    # =========================================================================
    # Component 1: Dockerfile with two-stage build (0.25 points)
    # =========================================================================
    try:
        dockerfile_path = os.path.join(WORKDIR, 'Dockerfile')
        if not os.path.exists(dockerfile_path):
            print("FAIL: Component 1 — Dockerfile does not exist")
        else:
            with open(dockerfile_path, 'r') as f:
                content = f.read()
            content_lower = content.lower()

            c1_score = 0.0

            # Check builder stage with golang:1.21-alpine
            if re.search(r'FROM\s+golang:1\.21-alpine\s+AS\s+builder', content, re.IGNORECASE):
                c1_score += 0.05
                print("PASS: Component 1a — Builder stage uses golang:1.21-alpine")
            else:
                print(f"FAIL: Component 1a — Expected 'FROM golang:1.21-alpine AS builder'")

            # Check go build command
            if 'go build' in content and '/app/server' in content and './cmd/server' in content:
                c1_score += 0.05
                print("PASS: Component 1b — go build -o /app/server ./cmd/server found")
            else:
                print("FAIL: Component 1b — Expected 'go build -o /app/server ./cmd/server'")

            # Check production stage with alpine:3.19
            if re.search(r'FROM\s+alpine:3\.19', content, re.IGNORECASE):
                c1_score += 0.05
                print("PASS: Component 1c — Production stage uses alpine:3.19")
            else:
                print("FAIL: Component 1c — Expected 'FROM alpine:3.19' for production stage")

            # Check COPY from builder
            if re.search(r'COPY\s+--from=builder', content):
                c1_score += 0.04
                print("PASS: Component 1d — COPY --from=builder found")
            else:
                print("FAIL: Component 1d — Expected COPY --from=builder")

            # Check EXPOSE 8080 and CMD
            if 'EXPOSE 8080' in content or 'expose 8080' in content_lower:
                c1_score += 0.03
                print("PASS: Component 1e — EXPOSE 8080 found")
            else:
                print("FAIL: Component 1e — Expected EXPOSE 8080")

            # Check CMD runs /app/server
            if '/app/server' in content and re.search(r'(CMD|ENTRYPOINT)', content):
                c1_score += 0.03
                print("PASS: Component 1f — CMD /app/server found")
            else:
                print("FAIL: Component 1f — Expected CMD to run /app/server")

            total_score += c1_score
            print(f"  Component 1 subtotal: {c1_score}/0.25")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # =========================================================================
    # Component 2: docker-compose.yml with app, postgres, redis (0.25 points)
    # =========================================================================
    try:
        compose_path = os.path.join(WORKDIR, 'docker-compose.yml')
        if not os.path.exists(compose_path):
            print("FAIL: Component 2 — docker-compose.yml does not exist")
        else:
            with open(compose_path, 'r') as f:
                content = f.read()

            c2_score = 0.0

            # Check app service with port 8080 mapping
            if re.search(r'app:', content) and '8080:8080' in content:
                c2_score += 0.05
                print("PASS: Component 2a — app service with port 8080:8080")
            else:
                print("FAIL: Component 2a — Expected app service with port 8080:8080")

            # Check app depends_on postgres and redis
            if 'depends_on' in content and 'postgres' in content and 'redis' in content:
                c2_score += 0.05
                print("PASS: Component 2b — app depends_on postgres and redis")
            else:
                print("FAIL: Component 2b — Expected depends_on postgres and redis")

            # Check postgres service with postgres:15-alpine
            if re.search(r'postgres:15-alpine', content):
                c2_score += 0.05
                print("PASS: Component 2c — postgres service uses postgres:15-alpine")
            else:
                print("FAIL: Component 2c — Expected postgres:15-alpine image")

            # Check postgres healthcheck
            if 'healthcheck' in content and 'pg_isready' in content:
                c2_score += 0.05
                print("PASS: Component 2d — postgres healthcheck with pg_isready")
            else:
                print("FAIL: Component 2d — Expected postgres healthcheck")

            # Check redis service with redis:7-alpine
            if re.search(r'redis:7-alpine', content):
                c2_score += 0.05
                print("PASS: Component 2e — redis service uses redis:7-alpine")
            else:
                print("FAIL: Component 2e — Expected redis:7-alpine image")

            total_score += c2_score
            print(f"  Component 2 subtotal: {c2_score}/0.25")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # =========================================================================
    # Component 3: docker-compose.dev.yml override (0.15 points)
    # =========================================================================
    try:
        dev_compose_path = os.path.join(WORKDIR, 'docker-compose.dev.yml')
        if not os.path.exists(dev_compose_path):
            print("FAIL: Component 3 — docker-compose.dev.yml does not exist")
        else:
            with open(dev_compose_path, 'r') as f:
                content = f.read()

            c3_score = 0.0

            # Check app service override exists
            if re.search(r'app:', content):
                c3_score += 0.03
                print("PASS: Component 3a — app service override present")
            else:
                print("FAIL: Component 3a — Expected app service in dev override")

            # Check volume mount for source code
            if 'volumes' in content and re.search(r'\.:/build|\.:/app|\.:/src', content):
                c3_score += 0.06
                print("PASS: Component 3b — Source volume mount found")
            else:
                print("FAIL: Component 3b — Expected source code volume mount")

            # Check air command for hot reload
            if 'air' in content:
                c3_score += 0.06
                print("PASS: Component 3c — air hot reload command found")
            else:
                print("FAIL: Component 3c — Expected 'air' for hot reload")

            total_score += c3_score
            print(f"  Component 3 subtotal: {c3_score}/0.15")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # =========================================================================
    # Component 4: Makefile has docker targets (0.20 points)
    # =========================================================================
    try:
        makefile_path = os.path.join(WORKDIR, 'Makefile')
        if not os.path.exists(makefile_path):
            print("FAIL: Component 4 — Makefile does not exist")
        else:
            with open(makefile_path, 'r') as f:
                content = f.read()

            c4_score = 0.0

            # Check for docker-build target
            if re.search(r'^docker-build:', content, re.MULTILINE):
                c4_score += 0.05
                print("PASS: Component 4a — docker-build target found")
            else:
                print("FAIL: Component 4a — Expected docker-build target in Makefile")

            # Check for docker-up target
            if re.search(r'^docker-up:', content, re.MULTILINE):
                c4_score += 0.05
                print("PASS: Component 4b — docker-up target found")
            else:
                print("FAIL: Component 4b — Expected docker-up target in Makefile")

            # Check for docker-dev target
            if re.search(r'^docker-dev:', content, re.MULTILINE):
                c4_score += 0.05
                print("PASS: Component 4c — docker-dev target found")
            else:
                print("FAIL: Component 4c — Expected docker-dev target in Makefile")

            # Check for docker-down target
            if re.search(r'^docker-down:', content, re.MULTILINE):
                c4_score += 0.05
                print("PASS: Component 4d — docker-down target found")
            else:
                print("FAIL: Component 4d — Expected docker-down target in Makefile")

            total_score += c4_score
            print(f"  Component 4 subtotal: {c4_score}/0.20")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # =========================================================================
    # Component 5: .vscode/tasks.json with 4 docker tasks (0.15 points)
    # =========================================================================
    try:
        tasks_path = os.path.join(WORKDIR, '.vscode', 'tasks.json')
        if not os.path.exists(tasks_path):
            print("FAIL: Component 5 — .vscode/tasks.json does not exist")
        else:
            with open(tasks_path, 'r') as f:
                # Handle potential JSONC (comments)
                raw = f.read()
                # Strip single-line comments for safety
                cleaned = re.sub(r'//.*$', '', raw, flags=re.MULTILINE)
                tasks_config = json.loads(cleaned)

            tasks = tasks_config.get('tasks', [])
            task_labels = [t.get('label', '') for t in tasks]

            c5_score = 0.0
            expected_labels = ['docker-build', 'docker-up', 'docker-dev', 'docker-down']

            for label in expected_labels:
                # Check label exists (case-insensitive match)
                if any(label.lower() == tl.lower() for tl in task_labels):
                    c5_score += 0.0375
                    print(f"PASS: Component 5 — task '{label}' found in tasks.json")
                else:
                    print(f"FAIL: Component 5 — task '{label}' not found in tasks.json (found: {task_labels})")

            total_score += c5_score
            print(f"  Component 5 subtotal: {c5_score}/0.15")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
