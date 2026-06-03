"""
Reward Script: Configure c_cpp_properties.json with include paths and C17 standard
Task ID: vscode_lang_079
Domain: vscode
Scoring:
  Component 1 (0.20): c_cpp_properties.json exists and is valid JSON with configurations array
  Component 2 (0.25): includePath contains "${workspaceFolder}/include"
  Component 3 (0.25): includePath contains "${workspaceFolder}/**"
  Component 4 (0.20): cStandard is "c17"
  Component 5 (0.10): compilerPath contains "gcc"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_079'
PROJECT_DIR = os.path.join(WORKDIR, TASK_ID)
CONFIG_PATH = os.path.join(PROJECT_DIR, '.vscode', 'c_cpp_properties.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(CONFIG_PATH):
        print(f"CRITICAL: c_cpp_properties.json not found at {CONFIG_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: file must be valid JSON
    try:
        with open(CONFIG_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments if present
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        data = json.loads(cleaned)
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse c_cpp_properties.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid structure with configurations array (0.20 points)
    # This checks that the file has the correct top-level structure.
    # This FAILS on initial_env (file doesn't exist, early return above).
    try:
        configs = data.get('configurations', None)
        if isinstance(configs, list) and len(configs) > 0:
            config = configs[0]  # Use first configuration
            if isinstance(config, dict):
                print(f"PASS: Component 1 -- Valid configurations array with {len(configs)} config(s) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 -- First configuration is not a dict: {type(config)}")
                config = {}
        else:
            print(f"FAIL: Component 1 -- 'configurations' is missing or empty: {configs}")
            config = {}
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        config = {}

    # Component 2: includePath contains "${workspaceFolder}/include" (0.25 points)
    try:
        include_path = config.get('includePath', [])
        if isinstance(include_path, list):
            found_include = any('${workspaceFolder}/include' == p or '${workspaceFolder}/include' in p
                               for p in include_path
                               if isinstance(p, str) and p.strip() != '${workspaceFolder}/**')
            if found_include:
                print(f"PASS: Component 2 -- includePath contains '${{workspaceFolder}}/include' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 -- includePath missing '${{workspaceFolder}}/include'. Found: {include_path}")
        else:
            print(f"FAIL: Component 2 -- includePath is not a list: {include_path}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: includePath contains "${workspaceFolder}/**" (0.25 points)
    try:
        include_path = config.get('includePath', [])
        if isinstance(include_path, list):
            found_wildcard = any('${workspaceFolder}/**' == p for p in include_path if isinstance(p, str))
            if found_wildcard:
                print(f"PASS: Component 3 -- includePath contains '${{workspaceFolder}}/**' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- includePath missing '${{workspaceFolder}}/**'. Found: {include_path}")
        else:
            print(f"FAIL: Component 3 -- includePath is not a list: {include_path}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: cStandard is "c17" (0.20 points)
    try:
        c_standard = config.get('cStandard', None)
        if isinstance(c_standard, str) and c_standard.lower() == 'c17':
            print(f"PASS: Component 4 -- cStandard is '{c_standard}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 -- cStandard expected 'c17', found: {c_standard}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: compilerPath contains "gcc" (0.10 points)
    try:
        compiler_path = config.get('compilerPath', None)
        if isinstance(compiler_path, str) and 'gcc' in compiler_path.lower():
            print(f"PASS: Component 5 -- compilerPath contains 'gcc': '{compiler_path}' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 -- compilerPath expected to contain 'gcc', found: {compiler_path}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
