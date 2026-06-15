"""
Reward Script: Change bullet character from U+2022 to U+25B6 in feature_list.docx
Task ID: writer_list_002
Domain: libreoffice_writer
Scoring:
  - Component 1 (0.6): The ListBullet abstractNum's lvlText value is U+25B6 (right-pointing triangle)
  - Component 2 (0.4): The old round bullet U+2022 no longer appears as any bullet lvlText character
                       (confirms the default bullet was replaced, not just a new entry added)
"""

import os
import zipfile
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_list_002'

TARGET_BULLET_CHAR = '\u25b6'   # U+25B6 BLACK RIGHT-POINTING TRIANGLE
INITIAL_BULLET_CHAR = '\u2022'  # U+2022 BULLET (round, default)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must be accessible and contain numbering.xml
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            if 'word/numbering.xml' not in z.namelist():
                print(f"CRITICAL: word/numbering.xml not found in {file_path}")
                print("REWARD: 0.0")
                return 0.0
            numbering_xml = z.read('word/numbering.xml').decode('utf-8')
    except Exception as e:
        print(f"CRITICAL: Cannot read {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse all lvlText values from abstractNum blocks
    try:
        abstract_num_pattern = re.compile(
            r'<w:abstractNum\s[^>]*>(.*?)</w:abstractNum>',
            re.DOTALL
        )
        lvl_text_in_list_bullet = None   # lvlText from the ListBullet style's abstractNum
        all_bullet_chars = []            # all non-empty lvlText from bullet-type abstractNums

        for match in abstract_num_pattern.finditer(numbering_xml):
            block = match.group(0)
            if 'numFmt w:val="bullet"' not in block:
                continue
            lvl_text_match = re.search(r'<w:lvlText\s+w:val="([^"]*)"', block)
            if not lvl_text_match:
                continue
            char_val = lvl_text_match.group(1)
            if char_val:
                all_bullet_chars.append(char_val)
                # Check if this is the ListBullet style abstractNum
                if 'pStyle w:val="ListBullet"' in block:
                    lvl_text_in_list_bullet = char_val
    except Exception as e:
        print(f"ERROR: Parsing numbering.xml: {e}")
        lvl_text_in_list_bullet = None
        all_bullet_chars = []

    # Component 1: ListBullet abstractNum's lvlText is U+25B6 (0.6 points)
    # This FAILS on initial (lvlText = U+2022) and PASSES on golden (lvlText = U+25B6)
    try:
        if lvl_text_in_list_bullet == TARGET_BULLET_CHAR:
            print(f"PASS: Component 1 — ListBullet lvlText is U+25B6 (right-pointing triangle) (0.6 pts)")
            total_score += 0.6
        elif lvl_text_in_list_bullet == INITIAL_BULLET_CHAR:
            print(f"FAIL: Component 1 — ListBullet lvlText is still U+2022 (round bullet), not changed to U+25B6")
        elif lvl_text_in_list_bullet is None:
            print(f"FAIL: Component 1 — Could not find ListBullet abstractNum lvlText in numbering.xml")
        else:
            actual_hex = hex(ord(lvl_text_in_list_bullet[0])) if lvl_text_in_list_bullet else 'empty'
            print(f"FAIL: Component 1 — lvlText is {repr(lvl_text_in_list_bullet)} ({actual_hex}), expected U+25B6")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The old U+2022 round bullet no longer appears as any bullet lvlText (0.4 points)
    # This verifies the default bullet was replaced rather than a new entry added alongside.
    # FAILS on initial (U+2022 is present as bullet lvlText) and PASSES on golden (U+2022 absent).
    try:
        has_old_bullet = INITIAL_BULLET_CHAR in all_bullet_chars
        if not has_old_bullet and all_bullet_chars:
            print(f"PASS: Component 2 — U+2022 (round bullet) no longer present as a bullet lvlText; "
                  f"bullet chars found: {[repr(c) for c in all_bullet_chars]} (0.4 pts)")
            total_score += 0.4
        elif has_old_bullet:
            print(f"FAIL: Component 2 — U+2022 (round bullet) still present in bullet lvlText definitions")
        else:
            print(f"FAIL: Component 2 — No bullet lvlText entries found in numbering.xml")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in given env
file_path = f'{WORKDIR}/feature_list.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
