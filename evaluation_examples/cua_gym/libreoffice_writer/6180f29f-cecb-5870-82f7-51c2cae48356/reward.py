"""
Reward Script: Format As Code macro with toolbar button
Task ID: writer_tech_057
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): FormatAsCode macro exists in Standard.Module1
  Component 2 (0.20): Macro references Liberation Mono font
  Component 3 (0.20): Macro references 9pt font size
  Component 4 (0.10): Macro sets gray background/highlight color
  Component 5 (0.20): Custom toolbar button referencing the macro exists
"""

import os
import glob
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_057'

# Paths for LibreOffice Basic macros and toolbar config
LO_USER = os.path.join(WORKDIR, '.config', 'libreoffice', '4', 'user')
BASIC_DIR = os.path.join(LO_USER, 'basic', 'Standard')
TOOLBAR_DIR = os.path.join(LO_USER, 'config', 'soffice.cfg', 'modules', 'swriter', 'toolbar')


def read_macro_content():
    """Read all .xba files in Standard library, return combined content."""
    xba_pattern = os.path.join(BASIC_DIR, '*.xba')
    files = glob.glob(xba_pattern)
    content = ""
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8', errors='replace') as fh:
                content += fh.read() + "\n"
        except Exception as e:
            print(f"WARN: Could not read {f}: {e}")
    return content


def read_toolbar_files():
    """Read all toolbar XML files for swriter, return combined content."""
    xml_pattern = os.path.join(TOOLBAR_DIR, '*.xml')
    files = glob.glob(xml_pattern)
    content = ""
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8', errors='replace') as fh:
                content += fh.read() + "\n"
        except Exception as e:
            print(f"WARN: Could not read {f}: {e}")
    return content


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Read macro content from all .xba files
    macro_content = read_macro_content()
    if not macro_content.strip():
        print("CRITICAL: No .xba macro files found in Standard library")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: FormatAsCode macro sub exists (0.30 points)
    # Check for a Sub named FormatAsCode (case-insensitive match on sub name)
    try:
        # Look for "Sub FormatAsCode" in the macro content
        has_format_sub = bool(re.search(
            r'Sub\s+FormatAsCode\b', macro_content, re.IGNORECASE
        ))
        if has_format_sub:
            print(f"PASS: Component 1 — FormatAsCode sub found in macro (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — No 'Sub FormatAsCode' found in macro files")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Macro references Liberation Mono font (0.20 points)
    try:
        has_liberation_mono = bool(re.search(
            r'Liberation\s*Mono', macro_content, re.IGNORECASE
        ))
        if has_liberation_mono:
            print(f"PASS: Component 2 — Liberation Mono font reference found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — No 'Liberation Mono' reference in macro")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Macro references 9pt font size (0.20 points)
    try:
        # Look for CharHeight set to 9, or font size 9
        has_9pt = bool(re.search(
            r'(?:CharHeight["\s,]*(?:=|,)\s*9\b)|(?:\.CharHeight\s*=\s*9\b)|'
            r'(?:setPropertyValue\s*\(\s*["\']CharHeight["\']\s*,\s*9\s*\))|'
            r'(?:CharHeight.*?\b9\b)',
            macro_content, re.IGNORECASE
        ))
        if has_9pt:
            print(f"PASS: Component 3 — 9pt font size reference found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — No 9pt (CharHeight 9) reference in macro")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Macro sets background/highlight color to gray (0.10 points)
    try:
        # Look for CharHighlight or CharBackColor being set (any gray-ish value)
        has_bg_color = bool(re.search(
            r'(?:CharHighlight|CharBackColor|CharBackground)',
            macro_content, re.IGNORECASE
        ))
        if has_bg_color:
            print(f"PASS: Component 4 — Background/highlight color setting found (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — No CharHighlight/CharBackColor in macro")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Custom toolbar button referencing FormatAsCode macro (0.20 points)
    try:
        toolbar_content = read_toolbar_files()
        if not toolbar_content.strip():
            print(f"FAIL: Component 5 — No custom toolbar XML files found in swriter toolbar dir")
        else:
            # Check for a toolbar item referencing the macro
            has_toolbar_ref = bool(re.search(
                r'FormatAsCode', toolbar_content, re.IGNORECASE
            ))
            if has_toolbar_ref:
                print(f"PASS: Component 5 — Toolbar button referencing FormatAsCode found (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 5 — Toolbar files exist but no FormatAsCode reference")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
