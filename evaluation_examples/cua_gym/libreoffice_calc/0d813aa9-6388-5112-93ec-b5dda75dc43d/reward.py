"""
Reward Script: Build Docker image, tag, and push to local registry
Task ID: os_adm_028
Domain: os (Docker)
Scoring:
  - Component 1 (0.3): Docker image 'myapp:v1.0' exists locally
  - Component 2 (0.3): Docker image tagged as 'localhost:5050/myapp:v1.0' locally
  - Component 3 (0.4): Image pushed to registry at localhost:5050 with tag 'v1.0'
"""

import os
import json
import requests

WORKDIR = '/home/user'
TASK_ID = 'os_adm_028'

# The registry runs on port 5050 (host) -> 5000 (container) because
# the env_cli occupies port 5000 on the host.
REGISTRY_PORT = 5050


def get_docker_images():
    """Get list of local docker images via sudo docker images --format json."""
    try:
        raw = os.popen('echo password | sudo -S docker images --format json 2>/dev/null').read()
        images = []
        for line in raw.strip().split('\n'):
            line = line.strip()
            if line:
                try:
                    images.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return images
    except Exception as e:
        print(f"ERROR: Could not query docker images: {e}")
        return []


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Get local docker images
    images = get_docker_images()
    image_repo_tags = set()
    for img in images:
        repo = img.get('Repository', '')
        tag = img.get('Tag', '')
        if repo and tag:
            image_repo_tags.add(f"{repo}:{tag}")

    print(f"DEBUG: Found local images: {image_repo_tags}")

    # Component 1: Docker image 'myapp:v1.0' exists locally (0.3 points)
    # This checks that the build was successful
    try:
        if 'myapp:v1.0' in image_repo_tags:
            print(f"PASS: Component 1 — 'myapp:v1.0' found in local docker images (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — 'myapp:v1.0' not found in local docker images")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Docker image tagged for registry 'localhost:5050/myapp:v1.0' (0.3 points)
    # This checks that the image was tagged for the local registry
    try:
        if f'localhost:{REGISTRY_PORT}/myapp:v1.0' in image_repo_tags:
            print(f"PASS: Component 2 — 'localhost:{REGISTRY_PORT}/myapp:v1.0' found in local docker images (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — 'localhost:{REGISTRY_PORT}/myapp:v1.0' not found in local docker images")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Image pushed to registry and available with tag 'v1.0' (0.4 points)
    # This is the most important check - verifies the push succeeded
    try:
        # Check the registry catalog first
        catalog_resp = requests.get(f'http://localhost:{REGISTRY_PORT}/v2/_catalog', timeout=5)
        catalog = catalog_resp.json()
        repos = catalog.get('repositories', [])
        print(f"DEBUG: Registry catalog: {repos}")

        if 'myapp' not in repos:
            print(f"FAIL: Component 3 — 'myapp' not found in registry catalog (repos: {repos})")
        else:
            # Check tags for myapp
            tags_resp = requests.get(f'http://localhost:{REGISTRY_PORT}/v2/myapp/tags/list', timeout=5)
            tags_data = tags_resp.json()
            tags = tags_data.get('tags', [])
            print(f"DEBUG: Registry tags for myapp: {tags}")

            if 'v1.0' in tags:
                print(f"PASS: Component 3 — 'myapp' with tag 'v1.0' found in registry at localhost:{REGISTRY_PORT} (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 3 — 'v1.0' tag not found for myapp in registry (tags: {tags})")
    except requests.ConnectionError:
        print(f"FAIL: Component 3 — Cannot connect to registry at localhost:{REGISTRY_PORT}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
