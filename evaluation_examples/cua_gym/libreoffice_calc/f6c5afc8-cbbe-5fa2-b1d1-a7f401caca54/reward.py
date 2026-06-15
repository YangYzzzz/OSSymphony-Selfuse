"""
Reward Script: Add Vim autowrite setting to ~/.vimrc
Task ID: osworld_multi_apps_web_search_config_003
Domain: os (file configuration)
Scoring:
  - Component 1 (0.6 pts): .vimrc contains an active (uncommented) 'set autowrite' or 'set autowriteall'
  - Component 2 (0.4 pts): The autowrite setting is specifically 'set autowriteall' (preferred per task context)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_search_config_003'
VIMRC_PATH = os.path.join(WORKDIR, '.vimrc')


def find_active_autowrite_setting(lines):
    """
    Search for active (uncommented) autowrite setting lines in .vimrc.
    Returns the matched setting string or None if not found.
    Vim comments start with '"', so we skip those lines.
    """
    for line in lines:
        stripped = line.strip()
        # Skip Vim comment lines (start with '"')
        if stripped.startswith('"'):
            continue
        # Match 'set autowrite' or 'set autowriteall' as a standalone setting
        m = re.match(r'^set\s+(autowrite(?:all)?)\s*$', stripped, re.IGNORECASE)
        if m:
            return stripped
        # Also catch inline set commands like 'set autowriteall noswapfile' etc.
        m2 = re.search(r'\bset\s+(autowrite(?:all)?)\b', stripped, re.IGNORECASE)
        if m2:
            return stripped
    return None


def verify_task(vimrc_path):
    """
    Verify that ~/.vimrc has been modified to include Vim autowrite settings.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: .vimrc file must exist
    if not os.path.isfile(vimrc_path):
        print(f"CRITICAL: .vimrc not found at {vimrc_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(vimrc_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read .vimrc: {e}")
        print("REWARD: 0.0")
        return 0.0

    lines = content.splitlines()

    # Precondition gate: verify original .vimrc structure is intact (not corrupted/replaced)
    # These are pre-existing settings — used as gate only, NOT scored
    required_existing = ['set nocompatible', 'set number', 'set tabstop=4', 'set hlsearch']
    file_is_intact = all(setting in content for setting in required_existing)
    if not file_is_intact:
        missing = [s for s in required_existing if s not in content]
        print(f"GATE FAIL: Original .vimrc settings missing (file may be corrupted): {missing}")
        print("REWARD: 0.0")
        return 0.0
    else:
        print("GATE PASS: Original .vimrc structure is intact")

    # Component 1: .vimrc contains an ACTIVE (uncommented) autowrite setting (0.6 points)
    # 'set autowrite' or 'set autowriteall' — not commented out with '"'
    # This FAILS on initial_env (no autowrite) and PASSES on golden_env (has autowriteall)
    try:
        matched_setting = find_active_autowrite_setting(lines)
        if matched_setting is not None:
            print(f"PASS: Component 1 — active autowrite setting found: '{matched_setting}' (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — no active 'set autowrite[all]' line found in .vimrc")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        matched_setting = None

    # Component 2: The autowrite setting is specifically 'set autowriteall' (the stronger/preferred form)
    # per task context which states "set autowriteall (or equivalent)" as the expected result (0.4 points)
    # This FAILS on initial_env (no autowriteall present) and PASSES on golden_env
    try:
        if matched_setting is not None:
            # Check that the matched setting contains 'autowriteall' (not just 'autowrite')
            is_autowriteall = bool(re.search(r'\bautowriteall\b', matched_setting, re.IGNORECASE))
            if is_autowriteall:
                print(f"PASS: Component 2 — preferred 'set autowriteall' form used (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — setting is '{matched_setting}' (valid but preferred form is 'set autowriteall')")
        else:
            print(f"FAIL: Component 2 — no active autowrite setting present")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(VIMRC_PATH):
    print(f"File not found: {VIMRC_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(VIMRC_PATH)
