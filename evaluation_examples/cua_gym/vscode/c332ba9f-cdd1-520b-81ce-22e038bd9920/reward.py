"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m creating a set of Web Components (e.g., <my-button>, <my-card>) and VS Code keeps showing red squiggles saying these tags aren’t valid HTML—how can I stop those validation warnings from popping up?
Generated: 2025-09-11 21:48:57
Status: success
Model: azure-o3
Total Steps: 9
"""

import json
import pathlib
import re
import os

"""
Reward Script for verifying suppression of HTML validation warnings for custom Web Components in VS Code.

Scoring Logic (progressive):
1. Detect at least one VS Code settings.json that defines the `html.customData` property (0.4 points).
2. Each referenced custom-data JSON file must exist and be valid JSON containing a `tags` array (0.4 points total once any valid file is found).
3. Verify that the custom-data file(s) actually define the expected custom element names ( `my-button`, `my-card` ):
   • 0.1 points per required tag found (up to 0.2).

Maximum score = 1.0.  Returns exactly 1.0 only when all three conditions are fully satisfied.
"""

def _load_json_allowing_comments(file_path: pathlib.Path):
    """Load JSON while stripping // line comments and /* */ block comments, and removing dangling commas."""
    text = file_path.read_text(encoding="utf-8")

    # Remove block comments
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    # Remove line comments
    text = re.sub(r"//.*", "", text)
    # Remove trailing commas before }} or ]]
    text = re.sub(r",\s*([}\]])", r"\1", text)

    return json.loads(text or "{}")


def _find_settings_files() -> list:
    """Return list of plausible VS Code settings.json paths (user + workspace)."""
    home = pathlib.Path.home()
    candidates = []

    # User-level settings
    user_settings = home / ".config" / "Code" / "User" / "settings.json"
    if user_settings.exists():
        candidates.append(user_settings)

    # Workspace-level .vscode/**/settings.json files under the home directory
    for path in home.rglob("settings.json"):
        if ".vscode" in path.parts:
            candidates.append(path)

    # De-duplicate while preserving order
    return list(dict.fromkeys(candidates))


def verify_task():
    max_score = 1.0
    score = 0.0

    settings_files = _find_settings_files()
    if not settings_files:
        print("✗ No VS Code settings.json files found.")
        return score

    print(f"Found {len(settings_files)} settings.json file(s) to inspect.")

    # STEP 1 ─ Check for html.customData property
    custom_data_refs = []
    for settings_path in settings_files:
        try:
            data = _load_json_allowing_comments(settings_path)
        except Exception as e:
            print(f"✗ Failed to parse {settings_path}: {e}")
            continue

        refs = data.get("html.customData", []) if isinstance(data, dict) else []
        if refs:
            print(f"✓ 'html.customData' found in {settings_path}")
            base = settings_path.parent
            for ref in refs:
                ref_path = pathlib.Path(ref)
                if not ref_path.is_absolute():
                    ref_path = (base / ref).resolve()
                custom_data_refs.append(ref_path)

    if custom_data_refs:
        score += 0.4
    else:
        print("✗ No 'html.customData' property with entries found in any settings.json.")
        return score  # Early exit because subsequent checks depend on this

    # STEP 2 ─ Validate referenced custom-data JSON files
    valid_custom_data = []
    for ref_path in custom_data_refs:
        if not ref_path.exists():
            print(f"✗ Referenced custom data file missing: {ref_path}")
            continue
        try:
            data = _load_json_allowing_comments(ref_path)
            if isinstance(data, dict) and "tags" in data:
                valid_custom_data.append((ref_path, data))
                print(f"✓ Valid custom data JSON: {ref_path}")
            else:
                print(f"✗ JSON file does not contain 'tags' array: {ref_path}")
        except Exception as e:
            print(f"✗ Failed to parse JSON {ref_path}: {e}")

    if valid_custom_data:
        score += 0.4
    else:
        print("✗ No valid custom data JSON files could be parsed.")
        return score

    # STEP 3 ─ Check for specific custom tag declarations
    required_tags = {"my-button", "my-card"}
    found_tags = set()
    for _path, data in valid_custom_data:
        for tag in data.get("tags", []):
            if isinstance(tag, dict):
                name = tag.get("name")
                if name in required_tags:
                    found_tags.add(name)

    if found_tags:
        print(f"✓ Found custom tag definitions: {found_tags}")
        # 0.1 per required tag (up to 0.2)
        tag_score = 0.1 * len(found_tags)
        score += tag_score
    else:
        print("✗ None of the required custom tag definitions ('my-button', 'my-card') were found.")

    final_score = min(score, max_score)
    print(f"Total score: {final_score}")
    return final_score


if __name__ == "__main__":
    reward = verify_task()
    print(f"REWARD: {reward}")

