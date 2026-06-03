"""
Reward Script: Install CMake Tools extension and configure Debug build type
Task ID: vscode_lang_080
Domain: vscode
Scoring:
  Component 1 (0.35): CMake Tools extension (ms-vscode.cmake-tools) is installed
  Component 2 (0.25): cmake.buildType set to "Debug" in settings (user or workspace)
  Component 3 (0.25): Build directory with CMakeCache.txt confirming Debug build type
  Component 4 (0.15): Workspace .vscode/settings.json contains cmake.buildType "Debug"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_080'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'cmake-app')
VSCODE_USER_SETTINGS = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')
WORKSPACE_SETTINGS = os.path.join(PROJECT_DIR, '.vscode', 'settings.json')
CMAKE_CACHE = os.path.join(PROJECT_DIR, 'build', 'CMakeCache.txt')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments) by stripping comments first."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  Could not load {path}: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: CMake Tools extension is installed (0.35 points)
    # This is the core requirement - installing ms-vscode.cmake-tools
    # NOTE: subprocess is required for `code --list-extensions` — this is the only
    # way to query installed VSCode extensions (per domain skill guidance).
    try:
        import subprocess
        result = subprocess.run(
            ['code', '--list-extensions'],
            capture_output=True, text=True, timeout=15
        )
        extensions = result.stdout.strip().lower().split('\n')
        cmake_tools_installed = any('ms-vscode.cmake-tools' in ext for ext in extensions)
        if cmake_tools_installed:
            print(f"PASS: Component 1 - CMake Tools extension is installed (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 - CMake Tools extension not found. Installed: {extensions}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: cmake.buildType set to "Debug" in any settings file (0.25 points)
    # Check both user-level and workspace-level settings for cmake.buildType = Debug
    try:
        user_settings = load_jsonc(VSCODE_USER_SETTINGS)
        ws_settings = load_jsonc(WORKSPACE_SETTINGS)
        user_has_debug = (user_settings or {}).get('cmake.buildType') == 'Debug'
        ws_has_debug = (ws_settings or {}).get('cmake.buildType') == 'Debug'

        if user_has_debug:
            print(f"  Found cmake.buildType=Debug in user settings")
        if ws_has_debug:
            print(f"  Found cmake.buildType=Debug in workspace settings")

        if user_has_debug or ws_has_debug:
            print(f"PASS: Component 2 - cmake.buildType is 'Debug' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 - cmake.buildType not set to 'Debug' in any settings")
            if user_settings:
                print(f"  User settings: {json.dumps(user_settings, indent=2)}")
            if ws_settings:
                print(f"  Workspace settings: {json.dumps(ws_settings, indent=2)}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Build directory exists with CMakeCache.txt confirming Debug build (0.25 points)
    # This verifies that CMake configure actually ran with Debug type
    try:
        if os.path.isfile(CMAKE_CACHE):
            with open(CMAKE_CACHE, 'r') as f:
                cache_content = f.read()
            # Look for CMAKE_BUILD_TYPE:STRING=Debug in the cache
            match = re.search(r'CMAKE_BUILD_TYPE:STRING=(\S+)', cache_content)
            if match and match.group(1) == 'Debug':
                print(f"PASS: Component 3 - CMakeCache.txt confirms Debug build type (0.25 pts)")
                total_score += 0.25
            else:
                found_type = match.group(1) if match else 'not found'
                print(f"FAIL: Component 3 - CMAKE_BUILD_TYPE is '{found_type}', expected 'Debug'")
        else:
            print(f"FAIL: Component 3 - Build directory or CMakeCache.txt not found at {CMAKE_CACHE}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Workspace .vscode/settings.json has cmake.buildType "Debug" (0.15 points)
    # Verifies workspace-level configuration specifically
    try:
        ws_settings = load_jsonc(WORKSPACE_SETTINGS)
        if ws_settings is not None and ws_settings.get('cmake.buildType') == 'Debug':
            print(f"PASS: Component 4 - Workspace settings contain cmake.buildType=Debug (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 - Workspace .vscode/settings.json missing or no cmake.buildType=Debug")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
