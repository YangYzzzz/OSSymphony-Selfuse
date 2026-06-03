"""
Reward Script: Extract PDF metadata and save as JSON
Task ID: pdf_mbc_030
Domain: pdf
Scoring:
  Component 1 (0.15): ebook_metadata.json file exists
  Component 2 (0.15): File contains valid JSON
  Component 3 (0.40): All 7 required metadata fields present (partial credit)
  Component 4 (0.30): Field values match expected values (partial credit)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_030'

# Expected metadata from task context
EXPECTED_METADATA = {
    "Title": "The Art of Programming",
    "Author": "Jane Developer",
    "Subject": "Computer Science",
    "Keywords": "programming, algorithms, data structures",
    "Creator": "LaTeX",
    "Producer": "pdfTeX-1.40.25",
    "CreationDate": "D:20240701",
}

# The task says "all metadata fields" — these are the required keys
REQUIRED_KEYS = list(EXPECTED_METADATA.keys())


def normalize_key(key):
    """Normalize key for case-insensitive comparison."""
    return key.strip().lower().replace("_", "").replace("-", "").replace(" ", "")


def find_value_for_key(data, expected_key):
    """Find a value in the JSON data matching the expected key (case-insensitive)."""
    norm_expected = normalize_key(expected_key)
    for k, v in data.items():
        if normalize_key(k) == norm_expected:
            return str(v).strip() if v is not None else ""
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    json_path = os.path.join(WORKDIR, 'Documents', 'ebook_metadata.json')

    # Component 1: ebook_metadata.json file exists (0.15 points)
    # This is the primary task-introduced change: the file must be created
    try:
        if os.path.isfile(json_path):
            print(f"PASS: Component 1 — ebook_metadata.json exists at {json_path} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — ebook_metadata.json not found at {json_path}")
            print(f"REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"REWARD: 0.0")
        return 0.0

    # Component 2: File contains valid JSON (0.15 points)
    data = None
    try:
        with open(json_path, 'r') as f:
            content = f.read().strip()
        data = json.loads(content)
        if isinstance(data, dict):
            print(f"PASS: Component 2 — Valid JSON object with {len(data)} keys (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — JSON is not an object (type: {type(data).__name__})")
            print(f"REWARD: {total_score}")
            return total_score
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 2 — Invalid JSON: {e}")
        print(f"REWARD: {total_score}")
        return total_score
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 3: All 7 required metadata fields are present (0.40 points)
    # Partial credit: ~0.057 per field found
    try:
        fields_found = 0
        for key in REQUIRED_KEYS:
            val = find_value_for_key(data, key)
            if val is not None:
                fields_found += 1
                print(f"  FOUND key matching '{key}': value='{val}'")
            else:
                print(f"  MISSING key matching '{key}'")

        per_field = 0.40 / len(REQUIRED_KEYS)
        key_score = round(fields_found * per_field, 4)
        if fields_found == len(REQUIRED_KEYS):
            print(f"PASS: Component 3 — All {len(REQUIRED_KEYS)} metadata fields present ({key_score:.2f} pts)")
        elif fields_found > 0:
            print(f"PARTIAL: Component 3 — {fields_found}/{len(REQUIRED_KEYS)} metadata fields present ({key_score:.2f} pts)")
        else:
            print(f"FAIL: Component 3 — No metadata fields found")
        total_score += key_score
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Field values match expected values (0.30 points)
    # Partial credit: ~0.043 per correct value
    try:
        values_correct = 0
        for key, expected_val in EXPECTED_METADATA.items():
            actual_val = find_value_for_key(data, key)
            if actual_val is None:
                print(f"  VALUE SKIP '{key}': key not found")
                continue
            # Normalize for comparison: strip whitespace, compare case-insensitively for text
            if actual_val.lower() == expected_val.lower():
                values_correct += 1
                print(f"  VALUE MATCH '{key}': '{actual_val}'")
            else:
                print(f"  VALUE MISMATCH '{key}': expected='{expected_val}', found='{actual_val}'")

        per_value = 0.30 / len(EXPECTED_METADATA)
        value_score = round(values_correct * per_value, 4)
        if values_correct == len(EXPECTED_METADATA):
            print(f"PASS: Component 4 — All {len(EXPECTED_METADATA)} values correct ({value_score:.2f} pts)")
        elif values_correct > 0:
            print(f"PARTIAL: Component 4 — {values_correct}/{len(EXPECTED_METADATA)} values correct ({value_score:.2f} pts)")
        else:
            print(f"FAIL: Component 4 — No values match")
        total_score += value_score
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
