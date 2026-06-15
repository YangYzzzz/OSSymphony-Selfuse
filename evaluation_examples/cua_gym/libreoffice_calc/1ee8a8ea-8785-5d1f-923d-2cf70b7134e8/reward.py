"""
Reward Script: VSCode CSV to JSON conversion with Rainbow CSV extension
Task ID: vscode_wf_019
Domain: vscode
Scoring:
  Component 1 (0.3): Rainbow CSV extension installed
  Component 2 (0.3): data.json exists and is a valid JSON array with 5 entries
  Component 3 (0.4): data.json entries match CSV data exactly
"""

import os
import json
import subprocess

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_019'

# Expected CSV data (from data.csv ground truth)
EXPECTED_ROWS = [
    {"name": "Alice Morgan", "age": 29, "city": "Seattle"},
    {"name": "Carlos Rivera", "age": 34, "city": "Austin"},
    {"name": "Priya Patel", "age": 27, "city": "Chicago"},
    {"name": "James O'Brien", "age": 41, "city": "Boston"},
    {"name": "Mei-Ling Zhang", "age": 33, "city": "San Francisco"},
]

EXPECTED_KEYS = {"name", "age", "city"}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Rainbow CSV extension is installed (0.3 points)
    # This checks that mechatroner.rainbow-csv extension is present
    try:
        result = subprocess.run(
            ["code", "--list-extensions"],
            capture_output=True, text=True, timeout=15
        )
        extensions = result.stdout.strip().lower().split('\n')
        if "mechatroner.rainbow-csv" in extensions:
            print(f"PASS: Component 1 — Rainbow CSV extension installed (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — mechatroner.rainbow-csv not found in extensions: {extensions}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: data.json exists and is a valid JSON array with 5 entries (0.3 points)
    json_path = os.path.join(WORKDIR, 'project', 'data.json')
    data = None
    try:
        if not os.path.isfile(json_path):
            print(f"FAIL: Component 2 — {json_path} does not exist")
        else:
            with open(json_path, 'r') as f:
                data = json.load(f)
            if not isinstance(data, list):
                print(f"FAIL: Component 2 — data.json is not a JSON array, type={type(data).__name__}")
            elif len(data) != 5:
                print(f"FAIL: Component 2 — data.json has {len(data)} entries, expected 5")
            else:
                print(f"PASS: Component 2 — data.json is a valid JSON array with 5 entries (0.3 pts)")
                total_score += 0.3
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 2 — data.json is not valid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: data.json entries match CSV data exactly (0.4 points)
    # Each entry must have keys name/age/city with correct values
    if data is not None and isinstance(data, list) and len(data) == 5:
        try:
            matches = 0
            for i, (actual, expected) in enumerate(zip(data, EXPECTED_ROWS)):
                # Check keys
                if not isinstance(actual, dict):
                    print(f"  FAIL: Row {i} is not a dict")
                    continue
                actual_keys = set(actual.keys())
                if not EXPECTED_KEYS.issubset(actual_keys):
                    print(f"  FAIL: Row {i} missing keys: {EXPECTED_KEYS - actual_keys}")
                    continue
                # Check values - age can be int or string representation
                name_ok = str(actual.get("name", "")).strip() == expected["name"]
                city_ok = str(actual.get("city", "")).strip() == expected["city"]
                # Age might be string or int depending on conversion method
                try:
                    age_ok = int(actual.get("age", -1)) == expected["age"]
                except (ValueError, TypeError):
                    age_ok = False
                if name_ok and age_ok and city_ok:
                    matches += 1
                else:
                    print(f"  FAIL: Row {i} mismatch — name_ok={name_ok}, age_ok={age_ok}, city_ok={city_ok}")
                    print(f"    actual: {actual}")
                    print(f"    expected: {expected}")

            if matches == 5:
                print(f"PASS: Component 3 — all 5 entries match CSV data exactly (0.4 pts)")
                total_score += 0.4
            elif matches > 0:
                partial = round(0.4 * matches / 5, 2)
                print(f"PARTIAL: Component 3 — {matches}/5 entries match ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — no entries match CSV data")
        except Exception as e:
            print(f"ERROR: Component 3 — {e}")
    else:
        print(f"SKIP: Component 3 — data.json not valid (depends on Component 2)")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
