"""
Reward Script: VSCode diff editor - merge specific CSS styles from old to new file
Task ID: vscode_web_075
Domain: vs_code
Scoring:
  Component 1 (0.30): .hidden and .sr-only utility classes merged into styles-new.css
  Component 2 (0.35): .tooltip styles merged into styles-new.css
  Component 3 (0.35): .badge styles merged into styles-new.css
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_075'
TARGET_FILE = os.path.join(WORKDIR, 'projects', 'website', 'styles-new.css')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    The task requires merging specific styles from styles-old.css into styles-new.css.
    In the initial state, styles-new.css is missing: .hidden, .sr-only, .tooltip, and .badge styles.
    In the golden state, these have been selectively merged from styles-old.css.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be readable
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: .hidden and .sr-only utility classes (0.30 points)
    # These exist in styles-old.css but are absent from the initial styles-new.css.
    # The golden styles-new.css should have them merged in.
    try:
        has_hidden = bool(re.search(r'\.hidden\s*\{[^}]*display\s*:\s*none', content))
        has_sr_only = bool(re.search(r'\.sr-only\s*\{', content))

        if has_hidden and has_sr_only:
            print(f"PASS: Component 1 - .hidden and .sr-only utility classes found (0.30 pts)")
            total_score += 0.30
        elif has_hidden or has_sr_only:
            found = []
            if has_hidden:
                found.append('.hidden')
            if has_sr_only:
                found.append('.sr-only')
            print(f"PARTIAL: Component 1 - Only {', '.join(found)} found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - Neither .hidden nor .sr-only found in styles-new.css")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: .tooltip styles (0.35 points)
    # The tooltip section with .tooltip and .tooltip::after should be merged from old to new.
    try:
        has_tooltip_base = bool(re.search(r'\.tooltip\s*\{[^}]*cursor\s*:\s*help', content))
        has_tooltip_after = bool(re.search(r'\.tooltip\s*::after\s*\{', content))
        has_tooltip_hover = bool(re.search(r'\.tooltip\s*:hover\s*::after\s*\{', content))

        tooltip_parts = sum([has_tooltip_base, has_tooltip_after, has_tooltip_hover])
        if tooltip_parts == 3:
            print(f"PASS: Component 2 - Complete .tooltip styles found (0.35 pts)")
            total_score += 0.35
        elif tooltip_parts > 0:
            partial = round(0.35 * tooltip_parts / 3, 2)
            print(f"PARTIAL: Component 2 - {tooltip_parts}/3 tooltip sub-rules found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - No .tooltip styles found in styles-new.css")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: .badge styles (0.35 points)
    # The badge section with .badge base, .badge-success, .badge-warning, .badge-danger
    try:
        has_badge_base = bool(re.search(r'\.badge\s*\{[^}]*border-radius\s*:\s*9999px', content))
        has_badge_success = bool(re.search(r'\.badge-success\s*\{', content))
        has_badge_warning = bool(re.search(r'\.badge-warning\s*\{', content))
        has_badge_danger = bool(re.search(r'\.badge-danger\s*\{', content))

        badge_parts = sum([has_badge_base, has_badge_success, has_badge_warning, has_badge_danger])
        if badge_parts == 4:
            print(f"PASS: Component 3 - Complete .badge styles found (0.35 pts)")
            total_score += 0.35
        elif badge_parts > 0:
            partial = round(0.35 * badge_parts / 4, 2)
            print(f"PARTIAL: Component 3 - {badge_parts}/4 badge sub-rules found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 - No .badge styles found in styles-new.css")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(TARGET_FILE):
    print(f"File not found: {TARGET_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(TARGET_FILE)
