"""
Reward Script: Install REST Client extension and configure environment variables
Task ID: vscode_we_067
Domain: vscode
Scoring:
  - Component 1 (0.30): humao.rest-client extension is installed
  - Component 2 (0.20): $shared env variable with version=v1
  - Component 3 (0.25): development env with correct host and token
  - Component 4 (0.25): production env with correct host and token
"""

import json
import os
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip JSONC line comments (only those NOT inside strings)
        # Simple approach: try parsing directly first, fall back to comment stripping
        try:
            return json.loads(content, strict=False)
        except json.JSONDecodeError:
            # Only strip comments if direct parse fails
            content = re.sub(r'^\s*//.*$', '', content, flags=re.MULTILINE)
            return json.loads(content, strict=False)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARN: Could not load settings.json: {e}")
        return {}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: humao.rest-client extension is installed (0.30 points)
    try:
        ext_dir = os.path.join(HOME, ".vscode", "extensions")
        matching_exts = [
            e for e in (os.listdir(ext_dir) if os.path.isdir(ext_dir) else [])
            if e.lower().startswith("humao.rest-client-")
        ]
        if len(matching_exts) > 0:
            print(f"PASS: Component 1 -- humao.rest-client extension found: {matching_exts[0]} (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 -- humao.rest-client extension not found in ~/.vscode/extensions/")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Load settings for remaining components
    settings = load_settings()
    env_vars = settings.get("rest-client.environmentVariables", None)

    if env_vars is None:
        print("FAIL: Components 2-4 -- 'rest-client.environmentVariables' key not found in settings.json")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: $shared env variable with version=v1 (0.20 points)
    try:
        shared = env_vars.get("$shared", None)
        if isinstance(shared, dict) and shared.get("version") == "v1":
            print(f"PASS: Component 2 -- $shared.version == 'v1' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 -- Expected $shared.version='v1', found: {shared}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: development env with correct host and token (0.25 points)
    try:
        dev = env_vars.get("development", None)
        if isinstance(dev, dict):
            host_ok = dev.get("host") == "http://localhost:3000"
            token_ok = dev.get("token") == "dev-token-123"
            if host_ok and token_ok:
                print(f"PASS: Component 3 -- development env correct: host={dev.get('host')}, token={dev.get('token')} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- development env mismatch: host_ok={host_ok}, token_ok={token_ok}, actual={dev}")
        else:
            print(f"FAIL: Component 3 -- 'development' key missing or not a dict, found: {dev}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: production env with correct host and token (0.25 points)
    try:
        prod = env_vars.get("production", None)
        if isinstance(prod, dict):
            host_ok = prod.get("host") == "https://api.example.com"
            token_ok = prod.get("token") == "prod-token-456"
            if host_ok and token_ok:
                print(f"PASS: Component 4 -- production env correct: host={prod.get('host')}, token={prod.get('token')} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 -- production env mismatch: host_ok={host_ok}, token_ok={token_ok}, actual={prod}")
        else:
            print(f"FAIL: Component 4 -- 'production' key missing or not a dict, found: {prod}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
