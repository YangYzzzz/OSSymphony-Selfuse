"""
Reward Script: Configure rust-analyzer to use nightly Rust toolchain
Task ID: vscode_lang_035
Domain: vscode
Scoring:
  Component 1 (0.4): rust-toolchain.toml exists with channel = "nightly"
  Component 2 (0.3): settings.json contains rust-analyzer nightly env config
  Component 3 (0.3): settings.json contains rust-analyzer.rustc.source key
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_035'
PROJECT_DIR = os.path.join(WORKDIR, TASK_ID)


def load_jsonc(path):
    """Load a JSON file, stripping // comments if present (JSONC support)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: rust-toolchain.toml exists with channel = "nightly" (0.4 points)
    # This file does NOT exist in initial_env, only in golden_env
    try:
        toolchain_path = os.path.join(PROJECT_DIR, 'rust-toolchain.toml')
        if os.path.exists(toolchain_path):
            with open(toolchain_path, 'r') as f:
                content = f.read()
            # Check for channel = "nightly" in the file content
            # Support both [toolchain]\nchannel = "nightly" and bare channel = "nightly"
            if re.search(r'channel\s*=\s*["\']nightly["\']', content):
                print(f"PASS: Component 1 -- rust-toolchain.toml has channel = nightly (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 -- rust-toolchain.toml exists but channel != nightly. Content: {content.strip()}")
        else:
            print(f"FAIL: Component 1 -- rust-toolchain.toml does not exist at {toolchain_path}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: settings.json has rust-analyzer nightly env config (0.3 points)
    # In golden_env, settings.json has "rust-analyzer.server.extraEnv": {"RUSTUP_TOOLCHAIN": "nightly"}
    # This key does NOT exist in initial_env settings.json
    try:
        settings_path = os.path.join(PROJECT_DIR, '.vscode', 'settings.json')
        if os.path.exists(settings_path):
            settings = load_jsonc(settings_path)
            extra_env = settings.get('rust-analyzer.server.extraEnv', {})
            if isinstance(extra_env, dict) and extra_env.get('RUSTUP_TOOLCHAIN') == 'nightly':
                print(f"PASS: Component 2 -- rust-analyzer.server.extraEnv has RUSTUP_TOOLCHAIN=nightly (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 -- Expected RUSTUP_TOOLCHAIN=nightly in extraEnv, found: {extra_env}")
        else:
            print(f"FAIL: Component 2 -- settings.json not found at {settings_path}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: settings.json has rust-analyzer.rustc.source key set (0.3 points)
    # In golden_env this is set to null. In initial_env it does not exist at all.
    # The key existing (regardless of value) indicates the user configured rust-analyzer.
    try:
        settings_path = os.path.join(PROJECT_DIR, '.vscode', 'settings.json')
        if os.path.exists(settings_path):
            settings = load_jsonc(settings_path)
            if 'rust-analyzer.rustc.source' in settings:
                print(f"PASS: Component 3 -- rust-analyzer.rustc.source present in settings (value: {settings['rust-analyzer.rustc.source']}) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 -- rust-analyzer.rustc.source not found in settings. Keys: {list(settings.keys())}")
        else:
            print(f"FAIL: Component 3 -- settings.json not found at {settings_path}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
