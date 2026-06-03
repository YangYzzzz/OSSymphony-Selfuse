"""
Reward Script: Configure c_cpp_properties.json for C17 and C++20 standards
Task ID: vscode_lang_085
Domain: vscode
Scoring:
  - Component 1 (0.4): cStandard is set to "c17"
  - Component 2 (0.4): cppStandard is set to "c++20"
  - Component 3 (0.2): Both standards changed together AND config structure intact
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_085'
CONFIG_PATH = os.path.join(WORKDIR, TASK_ID, '.vscode', 'c_cpp_properties.json')


def load_jsonc(file_path):
    """Load a JSONC file (JSON with comments), stripping // comments."""
    with open(file_path, 'r') as f:
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

    # Precondition: file must exist and be valid JSON
    if not os.path.exists(CONFIG_PATH):
        print(f"CRITICAL: Config file not found: {CONFIG_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        config = load_jsonc(CONFIG_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse {CONFIG_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must have configurations array with at least one entry
    configurations = config.get("configurations", [])
    if not configurations:
        print("CRITICAL: No configurations found in c_cpp_properties.json")
        print("REWARD: 0.0")
        return 0.0

    # Collect actual standard values from all configurations
    c_standards = [cfg.get("cStandard", "<missing>") for cfg in configurations]
    cpp_standards = [cfg.get("cppStandard", "<missing>") for cfg in configurations]

    # Component 1: cStandard is "c17" (0.4 points)
    # Initial has "c11", golden has "c17" — this checks the change
    try:
        if "c17" in c_standards:
            print(f"PASS: Component 1 — cStandard is 'c17' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Expected cStandard 'c17', found: {c_standards}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: cppStandard is "c++20" (0.4 points)
    # Initial has "c++14", golden has "c++20" — this checks the change
    try:
        if "c++20" in cpp_standards:
            print(f"PASS: Component 2 — cppStandard is 'c++20' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — Expected cppStandard 'c++20', found: {cpp_standards}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Both standards in same configuration AND structure intact (0.2 points)
    # This verifies the task was done correctly — both standards should be in
    # the same configuration entry, and other key fields should be preserved
    try:
        # Find a config entry where both standards are set correctly
        matching_cfg = next(
            (cfg for cfg in configurations
             if cfg.get("cStandard") == "c17" and cfg.get("cppStandard") == "c++20"),
            None
        )
        if matching_cfg is not None:
            has_name = "name" in matching_cfg
            has_include = "includePath" in matching_cfg
            has_compiler = "compilerPath" in matching_cfg

            if has_name and has_include and has_compiler:
                print(f"PASS: Component 3 — Both standards in same config, structure intact (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Standards in same config but structure incomplete: "
                      f"name={has_name}, includePath={has_include}, compilerPath={has_compiler}")
        else:
            print(f"FAIL: Component 3 — Standards not in same configuration entry")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
