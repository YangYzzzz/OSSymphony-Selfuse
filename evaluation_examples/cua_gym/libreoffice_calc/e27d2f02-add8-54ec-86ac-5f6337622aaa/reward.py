"""
Reward Script: Check PDF document properties and write to text file
Task ID: pdf_mbc_033
Domain: pdf (libreoffice_calc in config, but actual task is PDF property inspection)
Scoring:
  Component 1 (0.3): okular_props.txt exists and contains correct page count (24)
  Component 2 (0.3): okular_props.txt contains correct embedded fonts count (3)
  Component 3 (0.4): okular_props.txt contains correct PDF version (1.6)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_033'
OUTPUT_FILE = os.path.join(WORKDIR, 'Documents', 'okular_props.txt')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(OUTPUT_FILE):
        print(f"CRITICAL: Output file not found: {OUTPUT_FILE}")
        print("REWARD: 0.0")
        return 0.0

    try:
        content = open(OUTPUT_FILE, 'r').read()
        content_lower = content.lower()
        print(f"File content:\n{content}")
    except Exception as e:
        print(f"CRITICAL: Cannot read file {OUTPUT_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Page count is 24 (0.3 points)
    # The file should mention that the PDF has 24 pages
    try:
        # Look for patterns like "pages = 24", "pages: 24", "24 pages", "number of pages: 24"
        page_patterns = [
            r'pages?\s*[=:]\s*24\b',
            r'24\s+pages?\b',
            r'number\s+of\s+pages\s*[=:]\s*24\b',
            r'page\s+count\s*[=:]\s*24\b',
        ]
        page_found = any(re.search(p, content_lower) for p in page_patterns)
        if page_found:
            print(f"PASS: Component 1 — Page count 24 found (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Could not find page count = 24 in file")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Embedded fonts count is 3 (0.3 points)
    # The file should mention 3 embedded fonts (could list them or just state the count)
    try:
        font_patterns = [
            r'embedded\s+fonts?\s*[=:]\s*3\b',
            r'3\s+embedded\s+fonts?\b',
            r'fonts?\s*[=:]\s*3\b',
        ]
        font_found = any(re.search(p, content_lower) for p in font_patterns)

        # Also accept if three font names are listed (e.g., Arial, Times New Roman, Courier)
        # or Liberation equivalents
        if not font_found:
            known_fonts = [
                'arial', 'times new roman', 'courier',
                'liberation sans', 'liberation serif', 'liberation mono',
            ]
            fonts_mentioned = sum(1 for f in known_fonts if f in content_lower)
            font_found = (fonts_mentioned >= 3)  # derived from actual count check

        if font_found:
            print(f"PASS: Component 2 — Embedded fonts = 3 found (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Could not find embedded fonts = 3 in file")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: PDF version is 1.6 (0.4 points)
    # The file should mention PDF version 1.6
    try:
        version_patterns = [
            r'pdf\s+version\s*[=:]\s*1\.6\b',
            r'version\s*[=:]\s*1\.6\b',
            r'pdf\s+1\.6\b',
            r'1\.6\s+pdf\b',
        ]
        version_found = any(re.search(p, content_lower) for p in version_patterns)
        if version_found:
            print(f"PASS: Component 3 — PDF version 1.6 found (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 3 — Could not find PDF version = 1.6 in file")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
