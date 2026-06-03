"""
Reward Script: Set up Code Spell Checker for ~/project
Task ID: vscode_wf_032
Domain: vscode
Scoring:
  - Component 1 (0.40): Extension streetsidesoftware.code-spell-checker is installed
  - Component 2 (0.35): .vscode/settings.json contains cSpell.words with all 4 custom words
  - Component 3 (0.25): .vscode/settings.json contains cSpell.enabledLanguageIds with python and markdown
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_032'
PROJECT_DIR = os.path.join(WORKDIR, 'project')
SETTINGS_PATH = os.path.join(PROJECT_DIR, '.vscode', 'settings.json')

REQUIRED_WORDS = {'fastapi', 'pydantic', 'sqlalchemy', 'uvicorn'}
REQUIRED_LANGUAGE_IDS = {'python', 'markdown'}
EXTENSION_ID = 'streetsidesoftware.code-spell-checker'


def load_jsonc(path):
    """Load a JSONC file (JSON with comments) by stripping comments first."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip block comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Extension installed (0.40 points)
    # Check that streetsidesoftware.code-spell-checker exists in ~/.vscode/extensions/
    try:
        ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
        if os.path.isdir(ext_dir):
            ext_folders = os.listdir(ext_dir)
            # Extension folders are named like "streetsidesoftware.code-spell-checker-3.0.1"
            ext_found = any(
                folder.lower().startswith(EXTENSION_ID.lower())
                for folder in ext_folders
                if os.path.isdir(os.path.join(ext_dir, folder))
            )
            if ext_found:
                print(f"PASS: Component 1 -- Extension '{EXTENSION_ID}' is installed (0.40 pts)")
                total_score += 0.40
            else:
                print(f"FAIL: Component 1 -- Extension '{EXTENSION_ID}' not found in {ext_dir}. Contents: {ext_folders}")
        else:
            print(f"FAIL: Component 1 -- Extensions directory not found: {ext_dir}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: cSpell.words contains all 4 custom words (0.35 points)
    try:
        if not os.path.exists(SETTINGS_PATH):
            print(f"FAIL: Component 2 -- Settings file not found at {SETTINGS_PATH}")
        else:
            settings = load_jsonc(SETTINGS_PATH)
            cspell_words_raw = settings.get('cSpell.words', [])
            if not isinstance(cspell_words_raw, list):
                print(f"FAIL: Component 2 -- cSpell.words is not a list: {type(cspell_words_raw)}")
            else:
                cspell_words = {w.lower() for w in cspell_words_raw if isinstance(w, str)}
                missing = REQUIRED_WORDS - cspell_words
                if not missing:
                    print(f"PASS: Component 2 -- All 4 custom words found in cSpell.words (0.35 pts)")
                    total_score += 0.35
                else:
                    print(f"FAIL: Component 2 -- Missing words: {missing}. Found: {cspell_words}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: cSpell.enabledLanguageIds contains python and markdown (0.25 points)
    try:
        if not os.path.exists(SETTINGS_PATH):
            print(f"FAIL: Component 3 -- Settings file not found at {SETTINGS_PATH}")
        else:
            settings = load_jsonc(SETTINGS_PATH)
            lang_ids_raw = settings.get('cSpell.enabledLanguageIds', [])
            if not isinstance(lang_ids_raw, list):
                print(f"FAIL: Component 3 -- cSpell.enabledLanguageIds is not a list: {type(lang_ids_raw)}")
            else:
                lang_ids = {lid.lower() for lid in lang_ids_raw if isinstance(lid, str)}
                missing = REQUIRED_LANGUAGE_IDS - lang_ids
                if not missing:
                    print(f"PASS: Component 3 -- python and markdown found in cSpell.enabledLanguageIds (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 3 -- Missing language IDs: {missing}. Found: {lang_ids}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
