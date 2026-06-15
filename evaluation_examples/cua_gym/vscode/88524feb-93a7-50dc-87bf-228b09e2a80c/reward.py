"""
Reward Script: Configure C/C++ IntelliSense to use compile_commands.json from CMake
Task ID: vscode_lang_088
Domain: vs_code
Scoring:
  Component 1 (0.5): .vscode/settings.json contains C_Cpp.default.compileCommands pointing to build/compile_commands.json
  Component 2 (0.5): CMakeLists.txt contains set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_088'
WORKSPACE_DIR = os.path.join(WORKDIR, 'workspace')
VSCODE_SETTINGS_PATH = os.path.join(WORKSPACE_DIR, '.vscode', 'settings.json')
CMAKE_PATH = os.path.join(WORKSPACE_DIR, 'CMakeLists.txt')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: .vscode/settings.json contains C_Cpp.default.compileCommands (0.5 points)
    # The setting must point to ${workspaceFolder}/build/compile_commands.json
    try:
        if not os.path.exists(VSCODE_SETTINGS_PATH):
            print(f"FAIL: Component 1 -- .vscode/settings.json not found at {VSCODE_SETTINGS_PATH}")
        else:
            with open(VSCODE_SETTINGS_PATH, 'r') as f:
                content = f.read()
            # Strip JSONC comments before parsing
            stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            stripped = re.sub(r'/\*.*?\*/', '', stripped, flags=re.DOTALL)
            settings = json.loads(stripped)

            compile_commands_val = settings.get('C_Cpp.default.compileCommands', None)
            if compile_commands_val is not None:
                # Accept the standard VSCode variable form
                expected = '${workspaceFolder}/build/compile_commands.json'
                if compile_commands_val == expected:
                    print(f"PASS: Component 1 -- C_Cpp.default.compileCommands = '{compile_commands_val}' (0.5 pts)")
                    total_score += 0.5
                else:
                    # Also accept absolute path form
                    alt_expected = os.path.join(WORKSPACE_DIR, 'build', 'compile_commands.json')
                    if compile_commands_val == alt_expected:
                        print(f"PASS: Component 1 -- C_Cpp.default.compileCommands = '{compile_commands_val}' (absolute path accepted) (0.5 pts)")
                        total_score += 0.5
                    else:
                        print(f"FAIL: Component 1 -- C_Cpp.default.compileCommands = '{compile_commands_val}', expected '{expected}'")
            else:
                print(f"FAIL: Component 1 -- C_Cpp.default.compileCommands not found in settings.json")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: CMakeLists.txt contains set(CMAKE_EXPORT_COMPILE_COMMANDS ON) (0.5 points)
    try:
        if not os.path.exists(CMAKE_PATH):
            print(f"FAIL: Component 2 -- CMakeLists.txt not found at {CMAKE_PATH}")
        else:
            with open(CMAKE_PATH, 'r') as f:
                cmake_content = f.read()

            # Match set(CMAKE_EXPORT_COMPILE_COMMANDS ON) with flexible whitespace
            pattern = r'set\s*\(\s*CMAKE_EXPORT_COMPILE_COMMANDS\s+ON\s*\)'
            if re.search(pattern, cmake_content, re.IGNORECASE):
                print(f"PASS: Component 2 -- CMakeLists.txt contains CMAKE_EXPORT_COMPILE_COMMANDS ON (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 2 -- CMAKE_EXPORT_COMPILE_COMMANDS ON not found in CMakeLists.txt")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
