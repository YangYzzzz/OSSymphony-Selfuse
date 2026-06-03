"""
Reward Script: Configure VSCode large file optimizations
Task ID: vscode_fix_050
Domain: vscode
Scoring:
  - Component 1 (0.3): files.maxMemoryForLargeFilesMB >= 1024
  - Component 2 (0.2): editor.largeFileOptimizations is true
  - Component 3 (0.3): editor.maxTokenizationLineLength is set to a reduced value
  - Component 4 (0.2): editor.minimap.enabled is false
"""

import os
import json
import re

HOME = '/home/user'
SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')
TASK_ID = 'vscode_fix_050'


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify VSCode large file performance optimizations.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Component 1: files.maxMemoryForLargeFilesMB is set high enough (0.3 points)
    # Default is 4096 in some versions, but the initial env does NOT have this set.
    # The task requires increasing memory allocation for large files.
    try:
        max_mem = settings.get('files.maxMemoryForLargeFilesMB')
        if max_mem is not None and isinstance(max_mem, (int, float)) and max_mem >= 1024:
            print(f"PASS: Component 1 — files.maxMemoryForLargeFilesMB = {max_mem} (>= 1024) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — files.maxMemoryForLargeFilesMB = {max_mem}, expected >= 1024")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: editor.largeFileOptimizations is enabled (0.2 points)
    # This ensures VSCode applies optimizations for large files.
    try:
        large_file_opt = settings.get('editor.largeFileOptimizations')
        if large_file_opt is True:
            print(f"PASS: Component 2 — editor.largeFileOptimizations = true (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — editor.largeFileOptimizations = {large_file_opt}, expected true")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: editor.maxTokenizationLineLength is set (0.3 points)
    # Limiting tokenization length reduces CPU usage on large files with long lines.
    try:
        max_token_len = settings.get('editor.maxTokenizationLineLength')
        if max_token_len is not None and isinstance(max_token_len, (int, float)) and max_token_len > 0:
            print(f"PASS: Component 3 — editor.maxTokenizationLineLength = {max_token_len} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — editor.maxTokenizationLineLength = {max_token_len}, expected a positive number")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: editor.minimap.enabled is false (0.2 points)
    # Disabling minimap reduces rendering overhead for large files.
    try:
        minimap = settings.get('editor.minimap.enabled')
        if minimap is False:
            print(f"PASS: Component 4 — editor.minimap.enabled = false (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — editor.minimap.enabled = {minimap}, expected false")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
