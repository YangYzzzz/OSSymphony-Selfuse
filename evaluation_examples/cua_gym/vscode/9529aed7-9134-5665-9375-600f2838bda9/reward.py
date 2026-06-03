"""
Reward Script: Configure rust-analyzer to add custom feature flag 'test-utils'
Task ID: vscode_lang_044
Domain: vscode
Scoring:
  Component 1 (0.3): rust-analyzer.cargo.features key exists in workspace settings
  Component 2 (0.5): The features list contains "test-utils"
  Component 3 (0.2): Existing workspace settings are preserved (not overwritten)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_044'

# Workspace settings path (the task asks for "current workspace" config)
WORKSPACE_SETTINGS = os.path.join(WORKDIR, TASK_ID, '.vscode', 'settings.json')
# Global user settings path (alternative location an agent might use)
GLOBAL_SETTINGS = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_jsonc(path):
    """Load a JSON file, stripping JSONC-style comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip // comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip trailing commas before } or ]
    content = re.sub(r',\s*([}\]])', r'\1', content)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Determine which settings file has the rust-analyzer config
    # The task says "current workspace", so check workspace settings first, then global
    settings = None
    settings_source = None

    for candidate_path, label in [
        (WORKSPACE_SETTINGS, 'workspace'),
        (GLOBAL_SETTINGS, 'global'),
    ]:
        if os.path.exists(candidate_path):
            try:
                data = load_jsonc(candidate_path)
                if 'rust-analyzer.cargo.features' in data:
                    settings = data
                    settings_source = label
                    break
            except Exception as e:
                print(f"WARN: Could not parse {candidate_path}: {e}")

    if settings is None:
        # Try loading workspace settings anyway to check other components
        if os.path.exists(WORKSPACE_SETTINGS):
            try:
                settings = load_jsonc(WORKSPACE_SETTINGS)
                settings_source = 'workspace (no target key)'
            except Exception as e:
                print(f"CRITICAL: Cannot load workspace settings: {e}")
                print("REWARD: 0.0")
                return 0.0
        else:
            print(f"CRITICAL: Workspace settings not found at {WORKSPACE_SETTINGS}")
            print("REWARD: 0.0")
            return 0.0

    print(f"INFO: Checking settings from {settings_source} source")

    # Component 1: rust-analyzer.cargo.features key exists (0.3 points)
    try:
        if 'rust-analyzer.cargo.features' in settings:
            print(f"PASS: Component 1 — 'rust-analyzer.cargo.features' key found in {settings_source} settings (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — 'rust-analyzer.cargo.features' key not found in settings")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The features list contains "test-utils" (0.5 points)
    try:
        features = settings.get('rust-analyzer.cargo.features', None)
        if features is not None and isinstance(features, list) and 'test-utils' in features:
            print(f"PASS: Component 2 — 'test-utils' found in features list: {features} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — Expected 'test-utils' in features list, found: {features}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Existing workspace settings preserved AND target setting present (0.2 points)
    # This is a compound check: the target key must exist (anchoring to the task change)
    # AND the pre-existing settings must not have been overwritten
    try:
        ws_settings = load_jsonc(WORKSPACE_SETTINGS)
        features = ws_settings.get('rust-analyzer.cargo.features', None)
        has_target = features is not None and isinstance(features, list) and 'test-utils' in features
        if not has_target:
            print(f"FAIL: Component 3 — Target setting not present, skipping preservation check")
        else:
            preserved_keys = [
                'editor.formatOnSave',
                'editor.tabSize',
                'rust-analyzer.checkOnSave.command',
            ]
            preserved_count = sum(1 for k in preserved_keys if k in ws_settings)
            if preserved_count == len(preserved_keys):
                print(f"PASS: Component 3 — Target key present AND all {len(preserved_keys)} existing settings preserved (0.2 pts)")
                total_score += 0.2
            else:
                missing = [k for k in preserved_keys if k not in ws_settings]
                print(f"FAIL: Component 3 — {preserved_count}/{len(preserved_keys)} settings preserved, missing: {missing}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
