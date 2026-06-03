"""
Reward Script: Create Dockerfile for Node.js user-service and build Docker image
Task ID: vscode_gf5_015
Domain: vscode
Scoring:
  - Component 1 (0.25): Dockerfile exists in user-service directory
  - Component 2 (0.35): Dockerfile has valid Node.js content (FROM node, COPY, CMD)
  - Component 3 (0.40): Docker image 'user-service:v1' exists in local registry
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_015'
DOCKERFILE_PATH = os.path.join(WORKDIR, 'projects', 'microservices', 'user-service', 'Dockerfile')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Dockerfile exists (0.25 points)
    # This FAILS on initial (no Dockerfile) and PASSES on golden (Dockerfile created)
    try:
        if os.path.isfile(DOCKERFILE_PATH):
            with open(DOCKERFILE_PATH, 'r') as f:
                dockerfile_content = f.read().strip()
            if len(dockerfile_content) > 10:
                print(f"PASS: Component 1 -- Dockerfile exists at {DOCKERFILE_PATH} ({len(dockerfile_content)} chars) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 -- Dockerfile exists but is too short ({len(dockerfile_content)} chars)")
                dockerfile_content = ""
        else:
            print(f"FAIL: Component 1 -- Dockerfile not found at {DOCKERFILE_PATH}")
            dockerfile_content = ""
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        dockerfile_content = ""

    # Component 2: Dockerfile contains valid Node.js configuration (0.35 points)
    # Checks: FROM node-based image, has COPY or ADD, has CMD or ENTRYPOINT
    # This FAILS on initial (no Dockerfile) and PASSES on golden (valid Dockerfile)
    if dockerfile_content:
        try:
            sub_score = 0.0
            content_upper = dockerfile_content.upper()

            # Check FROM instruction with node base image
            from_match = re.search(r'FROM\s+node[:\w.\-]*', dockerfile_content, re.IGNORECASE)
            if from_match:
                print(f"  Component 2a: FROM node image found: {from_match.group()}")
                sub_score += 0.15
            else:
                print(f"  Component 2a: FAIL -- No FROM node image found")

            # Check COPY or ADD instruction (copies source code)
            if re.search(r'(COPY|ADD)\s+', dockerfile_content, re.IGNORECASE):
                print(f"  Component 2b: COPY/ADD instruction found")
                sub_score += 0.10
            else:
                print(f"  Component 2b: FAIL -- No COPY or ADD instruction found")

            # Check CMD or ENTRYPOINT (starts the application)
            if re.search(r'(CMD|ENTRYPOINT)\s+', dockerfile_content, re.IGNORECASE):
                print(f"  Component 2c: CMD/ENTRYPOINT instruction found")
                sub_score += 0.10
            else:
                print(f"  Component 2c: FAIL -- No CMD or ENTRYPOINT instruction found")

            if sub_score > 0:
                print(f"PASS: Component 2 -- Dockerfile has valid Node.js config ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 2 -- Dockerfile missing critical instructions")
        except Exception as e:
            print(f"ERROR: Component 2 -- {e}")
    else:
        print(f"FAIL: Component 2 -- No Dockerfile content to verify")

    # Component 3: Docker image 'user-service:v1' exists (0.40 points)
    # This FAILS on initial (no image) and PASSES on golden (image built)
    # We use os.popen with 'sg docker' to activate the docker group membership
    # (the user is in the docker group but it's not in the active group set)
    try:
        output = os.popen('sg docker -c "docker images --format {{.Repository}}:{{.Tag}}" 2>/dev/null').read().strip()
        image_list = [line.strip() for line in output.split('\n') if line.strip()]
        print(f"  Docker images found: {image_list}")

        if 'user-service:v1' in image_list:
            print(f"PASS: Component 3 -- Docker image 'user-service:v1' found in local registry (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 3 -- Docker image 'user-service:v1' not found. Available: {image_list}")
    except Exception as e:
        print(f"ERROR: Component 3 -- Could not query Docker: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
