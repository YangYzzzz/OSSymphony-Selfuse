"""
Reward Script: Configure .env file associations in VSCode
Task ID: vscode_web_089
Domain: vscode
Scoring:
  Component 1 (0.4): files.associations key exists with at least one env-related pattern mapped to dotenv/properties
  Component 2 (0.3): A wildcard pattern covers .env.* variants (e.g., "*.env.*" or ".env.*")
  Component 3 (0.3): All three specific variants (.env.local, .env.development, .env.production) are matched
"""

import os
import json
import re
import fnmatch

HOME = '/home/user'
SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')
TASK_ID = 'vscode_web_089'

# Valid language IDs for env file associations
VALID_LANG_IDS = {'dotenv', 'properties', 'ini', 'shellscript'}


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip // comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def pattern_matches_file(pattern, filename):
    """Check if a glob pattern in files.associations would match a given filename."""
    # VSCode uses glob patterns: try fnmatch
    if fnmatch.fnmatch(filename, pattern):
        return True
    # Also check without leading dot context
    return False


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: Cannot load settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: files.associations exists with at least one env-related mapping (0.4 points)
    # This checks that the user added a files.associations entry related to .env files
    try:
        file_assoc = settings.get('files.associations', {})
        if not isinstance(file_assoc, dict):
            print(f"FAIL: Component 1 — files.associations is not a dict: {type(file_assoc)}")
        else:
            # Check if any key relates to .env patterns and maps to a valid language
            env_related = False
            for pattern, lang_id in file_assoc.items():
                lang_lower = str(lang_id).lower().strip()
                pattern_lower = pattern.lower()
                # Pattern should relate to .env files
                if '.env' in pattern_lower and lang_lower in VALID_LANG_IDS:
                    env_related = True
                    break
            if env_related:
                print(f"PASS: Component 1 — files.associations has env-related mapping (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — No env-related mapping found in files.associations: {file_assoc}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: A wildcard/glob pattern covers .env.* variants (0.3 points)
    # The task requires .env.local, .env.development, .env.production to all be treated as dotenv
    # A good solution uses a wildcard like "*.env.*", ".env.*", or "*.env*"
    try:
        file_assoc = settings.get('files.associations', {})
        has_wildcard = False
        target_files = ['.env.local', '.env.development', '.env.production']

        for pattern, lang_id in file_assoc.items():
            lang_lower = str(lang_id).lower().strip()
            if lang_lower not in VALID_LANG_IDS:
                continue
            # Check if this pattern matches all three target files
            matches_all = all(pattern_matches_file(pattern, tf) for tf in target_files)
            if matches_all:
                has_wildcard = True
                print(f"  Found wildcard pattern '{pattern}' -> '{lang_id}' matching all variants")
                break

        if not has_wildcard:
            # Also accept explicit entries for each variant
            matched_count = 0
            for tf in target_files:
                for pattern, lang_id in file_assoc.items():
                    lang_lower = str(lang_id).lower().strip()
                    if lang_lower in VALID_LANG_IDS and pattern_matches_file(pattern, tf):
                        matched_count += 1
                        break
            if matched_count == len(target_files):
                has_wildcard = True
                print(f"  All {matched_count} variants explicitly matched")

        if has_wildcard:
            print(f"PASS: Component 2 — Wildcard/explicit patterns cover .env.* variants (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Patterns do not cover all .env.* variants")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Each of .env.local, .env.development, .env.production individually verified (0.3 points)
    # Awards 0.1 per file matched
    try:
        file_assoc = settings.get('files.associations', {})
        target_files = ['.env.local', '.env.development', '.env.production']
        matched = []

        for tf in target_files:
            for pattern, lang_id in file_assoc.items():
                lang_lower = str(lang_id).lower().strip()
                if lang_lower in VALID_LANG_IDS and pattern_matches_file(pattern, tf):
                    matched.append(tf)
                    break

        comp3_score = len(matched) * 0.1
        if comp3_score > 0:
            print(f"PASS: Component 3 — {len(matched)}/3 variants matched: {matched} ({comp3_score:.1f} pts)")
            total_score += comp3_score
        else:
            print(f"FAIL: Component 3 — No individual variants matched")
            for tf in target_files:
                print(f"  {tf}: not matched by any pattern")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
