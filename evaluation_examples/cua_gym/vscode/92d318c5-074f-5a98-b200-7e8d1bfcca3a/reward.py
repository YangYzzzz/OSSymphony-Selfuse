"""
Reward Script: Set up file associations in VSCode workspace settings
Task ID: vscode_code_072
Domain: vs_code
Scoring:
  - Component 1: *.njk → html association (0.25 pts)
  - Component 2: *.graphql → graphql association (0.25 pts)
  - Component 3: *.gql → graphql association (0.25 pts)
  - Component 4: Dockerfile.* → dockerfile association (0.25 pts)
  Total: 1.0
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_072'

# Workspace-local settings file (the target of the task)
WORKSPACE_SETTINGS_PATH = os.path.join(WORKDIR, TASK_ID, '.vscode', 'settings.json')


def _is_subset(expected, actual) -> bool:
    """Check that all expected key-value pairs exist in actual (subset match)."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and _is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        return expected == actual
    return expected == actual


def load_json_with_comments(path: str) -> dict:
    """Load a JSON file, stripping JSONC-style // comments before parsing."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content_no_comments = re.sub(r'//[^\n]*', '', content)
    return json.loads(content_no_comments)


def verify_task(settings_path: str) -> float:
    """
    Verify task completion with progressive scoring.
    Checks that the workspace .vscode/settings.json contains the required
    files.associations entries added by the task.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings file must exist
    if not os.path.exists(settings_path):
        print(f"CRITICAL: Workspace settings file not found: {settings_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load settings
    try:
        settings = load_json_with_comments(settings_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse settings file {settings_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Extract files.associations — the entire task is about adding these entries
    associations = settings.get('files.associations', {})
    if not isinstance(associations, dict):
        associations = {}

    print(f"Found files.associations: {associations}")

    # Component 1: *.njk → html (0.25 points)
    # Task requires .njk files (Nunjucks templates) to get HTML syntax highlighting
    try:
        njk_value = associations.get('*.njk', None)
        if njk_value is not None and njk_value.lower() == 'html':
            print(f"PASS: Component 1 — '*.njk' mapped to '{njk_value}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — expected '*.njk' → 'html', found: {njk_value!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: *.graphql → graphql (0.25 points)
    # Task requires .graphql files to get GraphQL syntax highlighting
    try:
        graphql_value = associations.get('*.graphql', None)
        if graphql_value is not None and graphql_value.lower() == 'graphql':
            print(f"PASS: Component 2 — '*.graphql' mapped to '{graphql_value}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — expected '*.graphql' → 'graphql', found: {graphql_value!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: *.gql → graphql (0.25 points)
    # Task requires .gql files to also get GraphQL syntax highlighting
    try:
        gql_value = associations.get('*.gql', None)
        if gql_value is not None and gql_value.lower() == 'graphql':
            print(f"PASS: Component 3 — '*.gql' mapped to '{gql_value}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — expected '*.gql' → 'graphql', found: {gql_value!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Dockerfile.* → dockerfile (0.25 points)
    # Task requires Dockerfile.dev, Dockerfile.prod etc. to be recognized as Dockerfiles
    try:
        dockerfile_value = associations.get('Dockerfile.*', None)
        if dockerfile_value is not None and dockerfile_value.lower() == 'dockerfile':
            print(f"PASS: Component 4 — 'Dockerfile.*' mapped to '{dockerfile_value}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — expected 'Dockerfile.*' → 'dockerfile', found: {dockerfile_value!r}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(WORKSPACE_SETTINGS_PATH):
    print(f"File not found: {WORKSPACE_SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(WORKSPACE_SETTINGS_PATH)
