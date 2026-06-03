"""
Reward Script: i18n workflow setup in VSCode
Task ID: vscode_wf_079
Domain: vscode
Scoring:
  Component 1: i18n-ally extension installed (0.15)
  Component 2: locales/en.json exists with >= 10 keys (0.20)
  Component 3: locales/es.json exists with matching keys (0.20)
  Component 4: settings.json has i18n-ally config (0.20)
  Component 5: tasks.json has check-translations task (0.15)
  Component 6: check_translations script exists and is functional (0.10)
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT = os.path.join(WORKDIR, 'project')
TASK_ID = 'vscode_wf_079'


def _is_subset(expected, actual):
    """Check that expected is a subset of actual (deep)."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and _is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        if not isinstance(actual, list):
            return False
        return expected == actual
    return expected == actual


def _load_json(path):
    """Load a JSON file, handling JSONC (comments)."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments for JSONC compatibility
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(cleaned)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  Could not load {path}: {e}")
        return None


def _get_flat_keys(data, prefix=''):
    """Recursively extract all leaf keys from a nested dict."""
    keys = set()
    if not isinstance(data, dict):
        return keys
    for key, value in data.items():
        full_key = f'{prefix}.{key}' if prefix else key
        if isinstance(value, dict):
            keys.update(_get_flat_keys(value, full_key))
        else:
            keys.add(full_key)
    return keys


def verify_task():
    """
    Verify i18n workflow setup with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Extension 'lokalise.i18n-ally' is installed (0.15 points)
    # Check by scanning the VSCode extensions directory on disk
    try:
        ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
        found_ext = False
        if os.path.isdir(ext_dir):
            for entry in os.listdir(ext_dir):
                if entry.lower().startswith('lokalise.i18n-ally'):
                    found_ext = True
                    break
        if found_ext:
            print(f"PASS: Component 1 -- i18n-ally extension installed (0.15 pts)")
            total_score += 0.15
        else:
            contents = os.listdir(ext_dir) if os.path.isdir(ext_dir) else []
            print(f"FAIL: Component 1 -- i18n-ally extension not found in {ext_dir}. Contents: {contents[:10]}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: locales/en.json exists with >= 10 key-value pairs (0.20 points)
    en_keys = set()
    try:
        en_path = os.path.join(PROJECT, 'locales', 'en.json')
        en_data = _load_json(en_path)
        if en_data is not None:
            en_keys = _get_flat_keys(en_data)
            key_count = len(en_keys)
            if key_count >= 10:
                print(f"PASS: Component 2 -- locales/en.json has {key_count} keys (>= 10) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 -- locales/en.json has only {key_count} keys (need >= 10)")
        else:
            print(f"FAIL: Component 2 -- locales/en.json not found or invalid JSON")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: locales/es.json exists with matching key structure to en.json (0.20 points)
    try:
        es_path = os.path.join(PROJECT, 'locales', 'es.json')
        es_data = _load_json(es_path)
        if es_data is not None and len(en_keys) >= 10:
            es_keys = _get_flat_keys(es_data)
            if len(es_keys) >= 10 and en_keys == es_keys:
                print(f"PASS: Component 3 -- locales/es.json has {len(es_keys)} keys matching en.json (0.20 pts)")
                total_score += 0.20
            elif len(es_keys) >= 10:
                # Partial: keys exist but don't fully match
                overlap = len(en_keys & es_keys)
                total_keys = len(en_keys | es_keys)
                ratio = overlap / total_keys if total_keys > 0 else 0
                partial = round(0.20 * ratio, 2)
                print(f"PARTIAL: Component 3 -- es.json has {len(es_keys)} keys, {overlap}/{total_keys} overlap ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 -- locales/es.json has only {len(es_keys)} keys (need >= 10)")
        elif es_data is not None:
            es_keys = _get_flat_keys(es_data)
            if len(es_keys) >= 10:
                print(f"PARTIAL: Component 3 -- es.json has {len(es_keys)} keys but en.json check failed (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 -- locales/es.json has only {len(es_keys)} keys")
        else:
            print(f"FAIL: Component 3 -- locales/es.json not found or invalid JSON")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: settings.json has i18n-ally configuration (0.20 points)
    try:
        settings_path = os.path.join(PROJECT, '.vscode', 'settings.json')
        settings = _load_json(settings_path)
        if settings is not None:
            has_locales_paths = 'i18n-ally.localesPaths' in settings
            has_source_lang = 'i18n-ally.sourceLanguage' in settings
            has_display_lang = 'i18n-ally.displayLanguage' in settings

            matched = sum([has_locales_paths, has_source_lang, has_display_lang])
            if matched == 3:
                print(f"PASS: Component 4 -- settings.json has all 3 i18n-ally keys (0.20 pts)")
                total_score += 0.20
            elif matched > 0:
                partial = round(0.20 * (matched / 3), 2)
                print(f"PARTIAL: Component 4 -- settings.json has {matched}/3 i18n-ally keys ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 -- settings.json has no i18n-ally configuration keys")
        else:
            print(f"FAIL: Component 4 -- .vscode/settings.json not found or invalid")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: tasks.json has 'check-translations' task (0.15 points)
    try:
        tasks_path = os.path.join(PROJECT, '.vscode', 'tasks.json')
        tasks_data = _load_json(tasks_path)
        if tasks_data is not None:
            tasks_list = tasks_data.get('tasks', [])
            found_task = any(
                t.get('label', '').lower() == 'check-translations'
                for t in tasks_list
                if isinstance(t, dict)
            )
            if found_task:
                print(f"PASS: Component 5 -- tasks.json has 'check-translations' task (0.15 pts)")
                total_score += 0.15
            else:
                labels = [t.get('label', '') for t in tasks_list if isinstance(t, dict)]
                print(f"FAIL: Component 5 -- 'check-translations' task not found. Labels: {labels}")
        else:
            print(f"FAIL: Component 5 -- .vscode/tasks.json not found or invalid")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: check_translations script exists in scripts/ (0.10 points)
    try:
        scripts_dir = os.path.join(PROJECT, 'scripts')
        found_script = False
        if os.path.isdir(scripts_dir):
            for fname in os.listdir(scripts_dir):
                if 'translation' in fname.lower() or 'i18n' in fname.lower() or 'missing' in fname.lower():
                    script_path = os.path.join(scripts_dir, fname)
                    if os.path.isfile(script_path) and os.path.getsize(script_path) > 50:
                        found_script = True
                        print(f"PASS: Component 6 -- found script '{fname}' ({os.path.getsize(script_path)} bytes) (0.10 pts)")
                        total_score += 0.10
                        break

        if not found_script:
            # Also check project root for script files
            for fname in os.listdir(PROJECT):
                fpath = os.path.join(PROJECT, fname)
                if os.path.isfile(fpath) and ('translation' in fname.lower() or 'i18n' in fname.lower() or 'missing' in fname.lower()):
                    if os.path.getsize(fpath) > 50:
                        found_script = True
                        print(f"PASS: Component 6 -- found script '{fname}' in project root ({os.path.getsize(fpath)} bytes) (0.10 pts)")
                        total_score += 0.10
                        break

        if not found_script:
            print(f"FAIL: Component 6 -- no translation check script found in scripts/ or project root")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isdir(PROJECT):
    print(f"Project directory not found: {PROJECT}")
    print("REWARD: 0.0")
else:
    verify_task()
