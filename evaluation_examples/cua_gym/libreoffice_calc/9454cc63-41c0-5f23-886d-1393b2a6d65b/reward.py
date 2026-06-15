"""
Reward Script: Install GIMP Script-Fu syntax extension in VSCode and write a Script-Fu crop script
Task ID: osworld_multi_apps_vscode_ext_script_008
Domain: vscode + os (multi-app)

Scoring rubric:
  Component 1: ~/Desktop/gimp_scripts/crop_center.scm file exists             — 0.3 pts
  Component 2: Script-Fu script has valid procedure with crop-256 logic        — 0.4 pts
  Component 3: VSCode Scheme/Script-Fu related extension is installed          — 0.3 pts
  Total: 1.0
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_vscode_ext_script_008'
SCRIPT_PATH = '/home/user/Desktop/gimp_scripts/crop_center.scm'
EXTENSIONS_JSON = '/home/user/.vscode/extensions/extensions.json'
EXTENSIONS_DIR = '/home/user/.vscode/extensions'

# Known Scheme/Script-Fu related extension IDs (case-insensitive match)
SCHEME_EXTENSION_IDS = [
    'evzen-wybitul.magic-racket',    # Racket/Scheme support
    'karyfoundation.racket',         # Racket
    'suketa.vscode-deno',            # Deno (sometimes used for Script-Fu)
    'leanprover.lean4',              # In case of fallback
    'zhm.scheme',                    # Scheme extension
    'sjurba.vscode-scheme',          # Another Scheme extension
    'release.scheme',                # Scheme
    'qualidafial.vscode-racket',     # Racket
    'choamilani.scheme',             # Scheme
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: ~/Desktop/gimp_scripts/crop_center.scm exists (0.3 points)
    # This FAILS on initial (directory doesn't exist) — PASSES on golden
    try:
        script_exists = os.path.isfile(SCRIPT_PATH)
        if script_exists:
            print(f"PASS: Component 1 — crop_center.scm exists at {SCRIPT_PATH} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — crop_center.scm not found at {SCRIPT_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Script-Fu script contains valid Script-Fu procedure with crop to 256x256 (0.4 points)
    # Checks: define, gimp-image-crop, 256, script-fu-register or equivalent
    # This FAILS on initial (file absent) — PASSES on golden
    try:
        if not os.path.isfile(SCRIPT_PATH):
            print("FAIL: Component 2 — script file absent, cannot verify content")
        else:
            with open(SCRIPT_PATH, 'r') as f:
                content = f.read()

            # Check for: (define ...) procedure
            has_define = bool(re.search(r'\(define\s+\(', content))
            # Check for: crop operation (gimp-image-crop or similar)
            has_crop = bool(re.search(r'gimp-image-crop|gimp-item-transform-scale|gimp-selection-bounds', content))
            # Check for: 256 (the crop size)
            has_256 = '256' in content
            # Check for: Script-Fu image size calculation (width/height retrieval)
            has_size_calc = bool(re.search(
                r'gimp-image-width|gimp-image-height|gimp-drawable-width|gimp-drawable-height',
                content
            ))
            # Check for: script-fu-register (proper Script-Fu plugin registration)
            has_register = bool(re.search(r'script-fu-register|script-fu-menu-register', content))
            # Check for: file save / export operation
            has_save = bool(re.search(r'file-png-save|gimp-file-overwrite|file-jpeg-save|gimp-xcf-save|gimp-image-delete', content))

            checks_passed = sum([has_define, has_crop, has_256, has_size_calc, has_register, has_save])
            print(f"  Script content checks:")
            print(f"    has_define={has_define}, has_crop={has_crop}, has_256={has_256}")
            print(f"    has_size_calc={has_size_calc}, has_register={has_register}, has_save={has_save}")
            print(f"    Checks passed: {checks_passed}/6")

            if checks_passed >= 5:
                print(f"PASS: Component 2 — Valid Script-Fu crop procedure found (0.4 pts)")
                total_score += 0.4
            elif checks_passed >= 3:
                print(f"PARTIAL: Component 2 — Script-Fu script partially valid ({checks_passed}/6 checks), awarding 0.2 pts")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — Script-Fu script does not contain valid crop procedure ({checks_passed}/6 checks)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: VSCode Scheme/Script-Fu extension installed (0.3 points)
    # Checks extensions.json and extension directory entries
    # This FAILS on initial (extensions.json is empty []) — PASSES on golden
    try:
        scheme_ext_found = False
        ext_id_found = None

        # Method 1: Check extensions.json for known Scheme/Script-Fu extensions
        if os.path.isfile(EXTENSIONS_JSON):
            try:
                with open(EXTENSIONS_JSON, 'r') as f:
                    ext_data = json.load(f)
                matches_json = [
                    ext.get('identifier', {}).get('id', '').lower()
                    for ext in ext_data
                    for known_id in SCHEME_EXTENSION_IDS
                    if known_id.lower() in ext.get('identifier', {}).get('id', '').lower()
                    or ext.get('identifier', {}).get('id', '').lower() in known_id.lower()
                ]
                if matches_json:
                    scheme_ext_found = len(matches_json) > 0
                    ext_id_found = matches_json[0]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"  extensions.json parse warning: {e}")

        # Method 2: Check extension directory names for Scheme/Script-Fu related names
        if not scheme_ext_found and os.path.isdir(EXTENSIONS_DIR):
            scheme_keywords = ['racket', 'scheme', 'script-fu', 'lisp', 'deno']
            matches_dir = [
                entry
                for entry in os.listdir(EXTENSIONS_DIR)
                for kw in scheme_keywords
                if kw in entry.lower()
            ]
            if matches_dir:
                scheme_ext_found = len(matches_dir) > 0
                ext_id_found = matches_dir[0]

        if scheme_ext_found:
            print(f"PASS: Component 3 — Scheme/Script-Fu extension installed: {ext_id_found} (0.3 pts)")
            total_score += 0.3
        else:
            # Report what IS installed for debugging
            if os.path.isfile(EXTENSIONS_JSON):
                try:
                    with open(EXTENSIONS_JSON, 'r') as f:
                        ext_data = json.load(f)
                    installed_ids = [e.get('identifier', {}).get('id', '?') for e in ext_data]
                    print(f"FAIL: Component 3 — No Scheme/Script-Fu extension found. Installed: {installed_ids}")
                except Exception:
                    print("FAIL: Component 3 — Could not parse extensions.json")
            else:
                print("FAIL: Component 3 — extensions.json not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
