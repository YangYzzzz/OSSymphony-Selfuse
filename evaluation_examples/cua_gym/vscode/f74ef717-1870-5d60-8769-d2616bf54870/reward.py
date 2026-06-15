"""
Reward Script: Add $schema property to config.json pointing to local schema file
Task ID: vscode_lp_019
Domain: vscode
Scoring:
  Component 1 (0.4): $schema key exists with correct value "./schemas/config-schema.json"
  Component 2 (0.3): $schema is the first property in the JSON object
  Component 3 (0.3): Original config data preserved (all original keys intact)
"""

import json
import os

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_019'

# Expected $schema value
EXPECTED_SCHEMA = "./schemas/config-schema.json"

# Original top-level keys that must still be present after the edit
ORIGINAL_KEYS = [
    "appName", "version", "environment", "server",
    "database", "logging", "features", "notifications"
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load file as raw text first (to check key ordering)
    try:
        with open(file_path, 'r') as f:
            raw_content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse JSON
    try:
        data = json.loads(raw_content)
    except json.JSONDecodeError:
        # Fallback: try stripping JSONC-style comments (// ...) outside strings
        try:
            # Remove single-line comments only outside of quoted strings
            # Simple approach: remove lines that are comment-only
            lines = raw_content.split('\n')
            cleaned_lines = []
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('//'):
                    continue
                cleaned_lines.append(line)
            data = json.loads('\n'.join(cleaned_lines))
        except json.JSONDecodeError as e:
            print(f"CRITICAL: Cannot parse JSON in {file_path}: {e}")
            print("REWARD: 0.0")
            return 0.0

    # Component 1: $schema key exists with correct value (0.4 points)
    try:
        if "$schema" in data:
            schema_val = data["$schema"]
            if schema_val == EXPECTED_SCHEMA:
                print(f"PASS: Component 1 — $schema = '{schema_val}' (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — $schema value is '{schema_val}', expected '{EXPECTED_SCHEMA}'")
        else:
            print(f"FAIL: Component 1 — $schema key not found in config.json")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: $schema is the first property in the JSON (0.3 points)
    # Use ordered key extraction from raw JSON to check position
    try:
        # json.loads preserves insertion order in Python 3.7+
        # data already parsed with order preserved
        keys_list = list(data.keys())
        if len(keys_list) > 0 and keys_list[0] == "$schema":
            print(f"PASS: Component 2 — $schema is the first key (position 0 of {len(keys_list)} keys) (0.3 pts)")
            total_score += 0.3
        elif "$schema" in keys_list:
            pos = keys_list.index("$schema")
            print(f"FAIL: Component 2 — $schema is at position {pos}, expected position 0. Keys: {keys_list[:3]}...")
        else:
            print(f"FAIL: Component 2 — $schema key not present, cannot check position")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: $schema added AND original config data preserved (0.3 points)
    # This is a compound check: $schema must exist AND original data must be intact.
    # On initial_env: $schema is missing, so this component FAILS (correct).
    try:
        if "$schema" not in data:
            print(f"FAIL: Component 3 — $schema not present, cannot verify data preservation alongside schema addition")
        else:
            missing_keys = [k for k in ORIGINAL_KEYS if k not in data]
            if len(missing_keys) == 0:
                # Spot-check a few specific values to ensure data wasn't corrupted
                checks_passed = 0
                total_checks = 3

                # Check appName
                if data.get("appName") == "DataPipeline Pro":
                    checks_passed += 1
                # Check server.port
                if isinstance(data.get("server"), dict) and data["server"].get("port") == 8080:
                    checks_passed += 1
                # Check database.driver
                if isinstance(data.get("database"), dict) and data["database"].get("driver") == "postgresql":
                    checks_passed += 1

                if checks_passed == total_checks:
                    print(f"PASS: Component 3 — $schema present AND all {len(ORIGINAL_KEYS)} original keys preserved, data integrity verified ({checks_passed}/{total_checks} spot checks) (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — Original keys present but data corrupted ({checks_passed}/{total_checks} spot checks passed)")
            else:
                print(f"FAIL: Component 3 — Missing original keys: {missing_keys}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}/config.json'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
