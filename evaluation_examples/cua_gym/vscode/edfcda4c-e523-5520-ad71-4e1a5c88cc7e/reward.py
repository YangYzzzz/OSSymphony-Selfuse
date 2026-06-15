"""
Reward Script: Configure JSON schema mapping for package.json in VSCode
Task ID: vscode_lp_030
Domain: vscode
Scoring:
  Component 1 (0.3): json.schemas key exists and is a non-empty list
  Component 2 (0.4): An entry has url matching schemastore.org/package.json
  Component 3 (0.3): That entry has fileMatch containing "package.json"
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")


def load_settings():
    """Load VSCode settings.json, handling JSONC comments safely."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # First try direct parse
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass
        # Try with strict=False to handle control chars
        try:
            return json.loads(content, strict=False)
        except json.JSONDecodeError:
            pass
        # Strip JSONC comments carefully: only // outside of strings
        # Simple heuristic: remove lines that are purely comments
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('//'):
                continue
            cleaned_lines.append(line)
        cleaned = '\n'.join(cleaned_lines)
        return json.loads(cleaned)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify that VSCode settings.json contains a json.schemas entry
    mapping package.json to the npm schema from schemastore.org.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Component 1: json.schemas key exists and is a non-empty list (0.3 points)
    try:
        schemas = settings.get("json.schemas")
        if isinstance(schemas, list) and len(schemas) > 0:
            print(f"PASS: Component 1 — json.schemas exists with {len(schemas)} entries (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — json.schemas missing or empty, found: {type(schemas).__name__} = {schemas}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: An entry has url matching the npm package.json schema (0.4 points)
    try:
        schemas = settings.get("json.schemas", [])
        if not isinstance(schemas, list):
            schemas = []
        target_url = "https://json.schemastore.org/package.json"
        url_match = any(
            isinstance(entry, dict) and entry.get("url", "").rstrip("/") == target_url
            for entry in schemas
        )
        if url_match:
            print(f"PASS: Component 2 — Found entry with url '{target_url}' (0.4 pts)")
            total_score += 0.4
        else:
            urls_found = [entry.get("url") for entry in schemas if isinstance(entry, dict)]
            print(f"FAIL: Component 2 — No entry with url '{target_url}'. URLs found: {urls_found}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: That entry has fileMatch containing "package.json" (0.3 points)
    try:
        schemas = settings.get("json.schemas", [])
        if not isinstance(schemas, list):
            schemas = []
        target_url = "https://json.schemastore.org/package.json"
        filematch_ok = False
        for entry in schemas:
            if not isinstance(entry, dict):
                continue
            if entry.get("url", "").rstrip("/") == target_url:
                file_match = entry.get("fileMatch", [])
                if isinstance(file_match, list):
                    # Check if any fileMatch pattern matches package.json
                    for pattern in file_match:
                        if isinstance(pattern, str) and "package.json" in pattern:
                            filematch_ok = True
                            break
                elif isinstance(file_match, str) and "package.json" in file_match:
                    filematch_ok = True
                break  # Only check the first entry with matching url
        if filematch_ok:
            print(f"PASS: Component 3 — fileMatch includes 'package.json' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — fileMatch does not include 'package.json' for the schema entry")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
