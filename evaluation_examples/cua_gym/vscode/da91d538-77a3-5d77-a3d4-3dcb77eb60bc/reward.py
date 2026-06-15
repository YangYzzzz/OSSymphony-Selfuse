"""
Reward Script: Replace all Docker image ':latest' tags with ':v1.5.2' in docker-compose*.yml files
Task ID: vscode_ops_059
Domain: vscode
Scoring:
  - Component 1 (0.35): docker-compose.yml — all ':latest' replaced with ':v1.5.2'
  - Component 2 (0.35): docker-compose.staging.yml — all ':latest' replaced with ':v1.5.2'
  - Component 3 (0.30): docker-compose.prod.yml — all ':latest' replaced with ':v1.5.2'
"""

import os
import re

WORKDIR = '/home/user'
WORKSPACE = os.path.join(WORKDIR, 'workspace')

# Expected image tags after replacement for each file
# These are the image lines that should have :v1.5.2 instead of :latest
EXPECTED_TAGS = {
    'docker-compose.yml': [
        'myregistry/web-frontend:v1.5.2',
        'myregistry/api-server:v1.5.2',
        'postgres:v1.5.2',
        'redis:v1.5.2',
        'myregistry/nginx-proxy:v1.5.2',
    ],
    'docker-compose.staging.yml': [
        'myregistry/web-frontend:v1.5.2',
        'myregistry/api-server:v1.5.2',
        'postgres:v1.5.2',
        'redis:v1.5.2',
        'myregistry/task-worker:v1.5.2',
    ],
    'docker-compose.prod.yml': [
        'myregistry/web-frontend:v1.5.2',
        'myregistry/api-server:v1.5.2',
        'postgres:v1.5.2',
        'redis:v1.5.2',
        'myregistry/nginx-proxy:v1.5.2',
        'myregistry/metrics-collector:v1.5.2',
    ],
}

WEIGHTS = {
    'docker-compose.yml': 0.35,
    'docker-compose.staging.yml': 0.35,
    'docker-compose.prod.yml': 0.30,
}


def extract_image_tags(content):
    """Extract all image tag values from a docker-compose YAML file."""
    # Match lines like: image: something:tag
    pattern = r'^\s*image:\s*(.+)$'
    tags = []
    for line in content.split('\n'):
        m = re.match(pattern, line)
        if m:
            tags.append(m.group(1).strip())
    return tags


def verify_file(filename, expected_tags):
    """
    Verify that a docker-compose file has all ':latest' replaced with ':v1.5.2'.
    Returns (score_fraction, details_str) where score_fraction is 0.0 to 1.0
    for this file's portion.
    """
    filepath = os.path.join(WORKSPACE, filename)

    if not os.path.exists(filepath):
        return 0.0, f"File not found: {filepath}"

    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except Exception as e:
        return 0.0, f"Cannot read {filepath}: {e}"

    # Check 1: No ':latest' tags remain in image lines
    actual_tags = extract_image_tags(content)
    if not actual_tags:
        return 0.0, f"No image tags found in {filename}"

    latest_count = sum(1 for tag in actual_tags if tag.endswith(':latest'))
    v152_count = sum(1 for tag in actual_tags if tag.endswith(':v1.5.2'))
    total_tags = len(actual_tags)

    if latest_count > 0:
        # Some tags still have :latest — partial credit based on how many were replaced
        replaced_fraction = v152_count / total_tags if total_tags > 0 else 0.0
        return replaced_fraction, f"{filename}: {latest_count}/{total_tags} tags still ':latest', {v152_count} replaced to ':v1.5.2'"

    # Check 2: All expected tags are present with :v1.5.2
    missing = []
    for expected in expected_tags:
        if expected not in actual_tags:
            missing.append(expected)

    if missing:
        # Most tags correct but some don't match expected
        match_fraction = (len(expected_tags) - len(missing)) / len(expected_tags)
        return match_fraction, f"{filename}: missing expected tags: {missing}"

    return 1.0, f"{filename}: all {total_tags} image tags correctly set to ':v1.5.2'"


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    for filename, expected_tags in EXPECTED_TAGS.items():
        weight = WEIGHTS[filename]

        # Component: Verify this docker-compose file
        try:
            fraction, details = verify_file(filename, expected_tags)
            component_score = weight * fraction
            if fraction > 0.0:
                total_score += component_score

            if fraction >= 1.0:
                print(f"PASS: {details} ({weight} pts)")
            else:
                print(f"FAIL: {details} (earned {component_score:.2f}/{weight} pts)")
        except Exception as e:
            print(f"ERROR: {filename} — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
