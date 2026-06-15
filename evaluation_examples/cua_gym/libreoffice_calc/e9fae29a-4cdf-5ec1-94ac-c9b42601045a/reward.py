"""
Reward Script: Configure a Docker-based development environment for the project at /home/user/projects/webapp/
Task ID: osworld_multi_apps_sys_config_010
Domain: os (system configuration / Docker)
Scoring:
  Component 1 (0.25): Dockerfile exists with required content (node:18-alpine, WORKDIR /app, npm install, EXPOSE 3000)
  Component 2 (0.25): docker-compose.yml exists with required content (service 'web', port mapping 8080:3000)
  Component 3 (0.25): Docker image for webapp was built (docker images shows relevant image)
  Component 4 (0.25): Container is running and app is accessible at localhost:8080 (HTTP 200)
"""

import os
import subprocess
import re

WORKDIR = '/home/user/projects/webapp'
TASK_ID = 'osworld_multi_apps_sys_config_010'

DOCKERFILE_PATH = os.path.join(WORKDIR, 'Dockerfile')
COMPOSE_PATH = os.path.join(WORKDIR, 'docker-compose.yml')


def verify_task():
    """
    Verify Docker environment setup with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # -----------------------------------------------------------------------
    # Component 1: Dockerfile exists with required content (0.25 points)
    # Checks: file present, uses node:18-alpine base, sets WORKDIR /app,
    #         copies package.json, runs npm install, exposes port 3000
    # -----------------------------------------------------------------------
    try:
        if not os.path.isfile(DOCKERFILE_PATH):
            print(f"FAIL: Component 1 — Dockerfile not found at {DOCKERFILE_PATH}")
        else:
            content = open(DOCKERFILE_PATH).read()
            checks = {
                'FROM node:18-alpine': 'node:18-alpine' in content or 'FROM node:18-alpine' in content,
                'WORKDIR /app': 'WORKDIR /app' in content,
                'COPY package.json': 'COPY package.json' in content,
                'RUN npm install': 'RUN npm install' in content,
                'EXPOSE 3000': 'EXPOSE 3000' in content,
            }
            failed = [k for k, v in checks.items() if not v]
            if not failed:
                print(f"PASS: Component 1 — Dockerfile found with all required directives (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 — Dockerfile missing required directives: {failed}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: docker-compose.yml exists with required content (0.25 points)
    # Checks: file present, service named 'web', port mapping 8080:3000,
    #         volume mounting source directory
    # -----------------------------------------------------------------------
    try:
        if not os.path.isfile(COMPOSE_PATH):
            print(f"FAIL: Component 2 — docker-compose.yml not found at {COMPOSE_PATH}")
        else:
            content = open(COMPOSE_PATH).read()
            checks = {
                'service web': 'web:' in content,
                'port 8080:3000': '8080:3000' in content,
                'volume mount': ('volumes:' in content and ('.:/app' in content or '/app' in content)),
            }
            failed = [k for k, v in checks.items() if not v]
            if not failed:
                print(f"PASS: Component 2 — docker-compose.yml found with service 'web', port 8080:3000, and volumes (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — docker-compose.yml missing required config: {failed}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Docker image for webapp was built (0.25 points)
    # Checks: 'docker images' lists an image built from /home/user/projects/webapp
    # We look for any image whose name contains 'webapp' or was built recently
    # using the project directory as context
    # -----------------------------------------------------------------------
    try:
        result = subprocess.run(
            ['docker', 'images', '--format', '{{.Repository}}:{{.Tag}} {{.CreatedSince}}'],
            capture_output=True, text=True
        )
        images_output = result.stdout.strip()
        # Check if there's any image named webapp (docker-compose names images <dir>_<service>)
        webapp_images = [
            line for line in images_output.split('\n')
            if 'webapp' in line.lower() and '<none>' not in line
        ]
        if webapp_images:
            print(f"PASS: Component 3 — Docker image built for webapp: {webapp_images[0]} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — No webapp Docker image found. Images available: {images_output[:200]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: Container is running and app responds at localhost:8080 (0.25 points)
    # Checks: curl http://localhost:8080 returns HTTP 200
    # -----------------------------------------------------------------------
    try:
        result = subprocess.run(
            ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', 'http://localhost:8080'],
            capture_output=True, text=True, timeout=15
        )
        http_code = result.stdout.strip()
        if http_code == '200':
            print(f"PASS: Component 4 — App accessible at localhost:8080 (HTTP {http_code}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — Expected HTTP 200 at localhost:8080, got: {http_code}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
