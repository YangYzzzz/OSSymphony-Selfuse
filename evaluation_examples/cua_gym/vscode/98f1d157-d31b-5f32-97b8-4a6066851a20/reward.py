"""
Reward Script: Install Error Lens extension and configure its settings in VSCode
Task ID: vscode_gf2_037
Domain: vscode
Scoring:
  Component 1: Error Lens extension installed (0.3 points)
  Component 2: errorLens.enabledDiagnosticLevels == ['error', 'warning'] (0.3 points)
  Component 3: errorLens.messageEnabled == true (0.2 points)
  Component 4: errorLens.delay == 500 (0.2 points)
"""

import os
import json
import re
import subprocess

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_037'
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        # Strip trailing commas before } or ]
        content = re.sub(r',\s*([}\]])', r'\1', content)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Error Lens extension is installed (0.3 points)
    try:
        result = subprocess.run(
            ['code', '--list-extensions'],
            capture_output=True, text=True, timeout=15
        )
        extensions = [ext.strip().lower() for ext in result.stdout.strip().split('\n') if ext.strip()]
        if 'usernamehw.errorlens' in extensions:
            print(f"PASS: Component 1 — Error Lens extension installed (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Error Lens extension not found. Installed: {extensions}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Load settings for remaining components
    settings = load_settings()
    if settings is None:
        print("CRITICAL: Cannot load settings.json — skipping settings checks")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: errorLens.enabledDiagnosticLevels == ['error', 'warning'] (0.3 points)
    try:
        levels = settings.get('errorLens.enabledDiagnosticLevels')
        if isinstance(levels, list) and sorted(levels) == sorted(['error', 'warning']):
            print(f"PASS: Component 2 — enabledDiagnosticLevels is {levels} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected ['error', 'warning'], found: {levels}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: errorLens.messageEnabled == true (0.2 points)
    try:
        msg_enabled = settings.get('errorLens.messageEnabled')
        if msg_enabled is True:
            print(f"PASS: Component 3 — messageEnabled is true (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Expected true, found: {msg_enabled}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: errorLens.delay == 500 (0.2 points)
    try:
        delay = settings.get('errorLens.delay')
        if delay == 500:
            print(f"PASS: Component 4 — delay is 500 (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — Expected 500, found: {delay}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
