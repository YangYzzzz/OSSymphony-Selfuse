"""
Reward Script: GitHub Actions release pipeline with semantic versioning
Task ID: vscode_gf3_090
Domain: vscode
Scoring:
  Component 1 (0.15): release.yml exists at correct path
  Component 2 (0.20): Workflow triggers on push to main
  Component 3 (0.15): Proper CI steps (checkout + node setup)
  Component 4 (0.15): NODE_AUTH_TOKEN secret is used
  Component 5 (0.15): Runs semantic-release
  Component 6 (0.20): @semantic-release/git plugin configured
"""

import os
import re
import json

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'npm-package')
RELEASE_YML = os.path.join(PROJECT_DIR, '.github', 'workflows', 'release.yml')


def find_releaserc_config():
    """Search for semantic-release config in .releaserc.json, .releaserc, .releaserc.yml, or package.json."""
    # Check .releaserc.json
    rc_json = os.path.join(PROJECT_DIR, '.releaserc.json')
    if os.path.exists(rc_json):
        try:
            with open(rc_json) as f:
                return json.load(f)
        except Exception:
            pass

    # Check .releaserc (may be JSON or YAML)
    rc_file = os.path.join(PROJECT_DIR, '.releaserc')
    if os.path.exists(rc_file):
        try:
            with open(rc_file) as f:
                return json.load(f)
        except Exception:
            pass

    # Check package.json for "release" key
    pkg_json = os.path.join(PROJECT_DIR, 'package.json')
    if os.path.exists(pkg_json):
        try:
            with open(pkg_json) as f:
                pkg = json.load(f)
            if 'release' in pkg:
                return pkg['release']
        except Exception:
            pass

    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ---- Precondition: load the release.yml file ----
    if not os.path.exists(RELEASE_YML):
        print(f"CRITICAL: release.yml not found at {RELEASE_YML}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(RELEASE_YML) as f:
            yml_content = f.read()
        yml_lower = yml_content.lower()
    except Exception as e:
        print(f"CRITICAL: Cannot read {RELEASE_YML}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: release.yml exists and is non-trivial (0.15 points)
    # This component checks that the file has meaningful content (not just empty/minimal)
    try:
        if len(yml_content.strip()) > 50:
            print(f"PASS: Component 1 — release.yml exists with {len(yml_content)} chars (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — release.yml too short ({len(yml_content)} chars)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Workflow triggers on push to main (0.20 points)
    try:
        # Check for push trigger on main branch
        has_push = bool(re.search(r'on\s*:', yml_content)) and 'push' in yml_lower
        has_main = bool(re.search(r'branches\s*:', yml_content)) and 'main' in yml_content
        if has_push and has_main:
            print(f"PASS: Component 2 — triggers on push to main (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — push trigger: {has_push}, main branch: {has_main}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Proper CI steps - checkout and node setup (0.15 points)
    try:
        has_checkout = bool(re.search(r'actions/checkout', yml_content))
        has_node_setup = bool(re.search(r'actions/setup-node', yml_content))
        if has_checkout and has_node_setup:
            print(f"PASS: Component 3 — checkout and setup-node actions present (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — checkout: {has_checkout}, setup-node: {has_node_setup}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: NODE_AUTH_TOKEN secret is used (0.15 points)
    try:
        has_node_auth = bool(re.search(r'NODE_AUTH_TOKEN', yml_content))
        if has_node_auth:
            print(f"PASS: Component 4 — NODE_AUTH_TOKEN secret referenced (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — NODE_AUTH_TOKEN not found in release.yml")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Runs semantic-release (0.15 points)
    try:
        has_semantic_release = bool(re.search(r'semantic.release', yml_lower))
        if has_semantic_release:
            print(f"PASS: Component 5 — semantic-release execution found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — semantic-release not referenced in workflow")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: @semantic-release/git plugin configured (0.20 points)
    # This checks for the plugin in any semantic-release config location
    try:
        sr_config = find_releaserc_config()
        git_plugin_in_config = False
        git_plugin_in_yml = '@semantic-release/git' in yml_content

        if sr_config and 'plugins' in sr_config:
            plugins = sr_config['plugins']
            plugin_names = [
                p if isinstance(p, str) else (p[0] if isinstance(p, list) and len(p) > 0 else '')
                for p in plugins
            ]
            git_plugin_in_config = any('@semantic-release/git' in str(n) for n in plugin_names)

        if git_plugin_in_config or git_plugin_in_yml:
            print(f"PASS: Component 6 — @semantic-release/git plugin configured (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 6 — @semantic-release/git plugin not found in config")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
