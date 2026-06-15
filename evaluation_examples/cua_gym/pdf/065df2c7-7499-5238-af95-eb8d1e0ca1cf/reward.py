"""
Reward Script: Write PDF document properties to a text file
Task ID: pdf_mbc_011
Domain: pdf
Scoring:
  Component 1: properties.txt exists and is non-empty (0.1 pts)
  Component 2: Title, Author, Subject, Keywords present and correct (0.3 pts)
  Component 3: Creator and Producer present and correct (0.2 pts)
  Component 4: Creation Date and Modification Date present and correct (0.2 pts)
  Component 5: Page Count and Page Size present and correct (0.2 pts)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_011'
PROPS_FILE = os.path.join(WORKDIR, 'Documents', 'properties.txt')

# Ground truth values from task context
EXPECTED = {
    'title': 'Smart City Infrastructure Proposal',
    'author': 'Urban Planning Dept',
    'subject': 'Infrastructure',
    'keywords': 'smart city, IoT, sensors',
    'creator': 'LibreOffice Writer',
    'producer': 'LibreOffice 7.5',
}

def normalize(s):
    """Normalize string for flexible comparison."""
    if s is None:
        return ''
    return str(s).strip().lower()

def file_contains_value(content_lower, key_label, expected_value):
    """Check if the file content contains a line with key_label and expected_value (case-insensitive)."""
    expected_lower = normalize(expected_value)
    # Look for a line like "key_label: expected_value" or "key_label expected_value"
    for line in content_lower.split('\n'):
        line_stripped = line.strip()
        if normalize(key_label) in line_stripped and expected_lower in line_stripped:
            return True
    return False

def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: properties.txt exists and is non-empty (0.1 points)
    try:
        if os.path.exists(PROPS_FILE):
            content = open(PROPS_FILE, 'r').read()
            if len(content.strip()) > 20:
                print(f"PASS: Component 1 -- properties.txt exists with {len(content)} chars (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 1 -- properties.txt exists but too short ({len(content)} chars)")
        else:
            print(f"FAIL: Component 1 -- properties.txt not found at {PROPS_FILE}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    content_lower = content.lower()

    # Component 2: Title, Author, Subject, Keywords correct (0.3 points)
    # 0.075 each
    try:
        comp2_score = 0.0
        checks = [
            ('title', EXPECTED['title']),
            ('author', EXPECTED['author']),
            ('subject', EXPECTED['subject']),
            ('keywords', EXPECTED['keywords']),
        ]
        for key_label, expected_val in checks:
            if file_contains_value(content_lower, key_label, expected_val):
                print(f"  PASS: '{key_label}' found with correct value '{expected_val}'")
                comp2_score += 0.075
            else:
                print(f"  FAIL: '{key_label}' not found or incorrect (expected '{expected_val}')")

        if comp2_score > 0:
            print(f"PASS: Component 2 -- basic metadata ({comp2_score:.3f} pts)")
            total_score += comp2_score
        else:
            print(f"FAIL: Component 2 -- no basic metadata properties found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Creator and Producer correct (0.2 points)
    # 0.1 each
    try:
        comp3_score = 0.0
        checks = [
            ('creator', EXPECTED['creator']),
            ('producer', EXPECTED['producer']),
        ]
        for key_label, expected_val in checks:
            if file_contains_value(content_lower, key_label, expected_val):
                print(f"  PASS: '{key_label}' found with correct value '{expected_val}'")
                comp3_score += 0.1
            else:
                print(f"  FAIL: '{key_label}' not found or incorrect (expected '{expected_val}')")

        if comp3_score > 0:
            print(f"PASS: Component 3 -- creator/producer ({comp3_score:.3f} pts)")
            total_score += comp3_score
        else:
            print(f"FAIL: Component 3 -- no creator/producer properties found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Creation Date and Modification Date (0.2 points)
    # 0.1 each
    try:
        comp4_score = 0.0

        # Check for creation date - look for "2025-03-15" or "2025/03/15" or "March 15, 2025" etc.
        creation_date_patterns = ['2025-03-15', '2025/03/15', 'mar 15', '03/15/2025', '03-15-2025', '15/03/2025', '20250315']
        found_creation = False
        for pat in creation_date_patterns:
            if pat in content_lower:
                # Also verify it is associated with "creation" keyword
                for line in content_lower.split('\n'):
                    if 'creation' in line and pat in line:
                        found_creation = True
                        break
                if found_creation:
                    break

        if found_creation:
            print(f"  PASS: creation date found with correct date (2025-03-15)")
            comp4_score += 0.1
        else:
            print(f"  FAIL: creation date not found or incorrect")

        # Check for modification date
        mod_date_patterns = ['2025-03-15', '2025/03/15', 'mar 15', '03/15/2025', '03-15-2025', '15/03/2025', '20250315']
        found_mod = False
        for pat in mod_date_patterns:
            if pat in content_lower:
                for line in content_lower.split('\n'):
                    if ('modif' in line or 'mod date' in line or 'mod_date' in line) and pat in line:
                        found_mod = True
                        break
                if found_mod:
                    break

        if found_mod:
            print(f"  PASS: modification date found with correct date (2025-03-15)")
            comp4_score += 0.1
        else:
            print(f"  FAIL: modification date not found or incorrect")

        if comp4_score > 0:
            print(f"PASS: Component 4 -- dates ({comp4_score:.3f} pts)")
            total_score += comp4_score
        else:
            print(f"FAIL: Component 4 -- no date properties found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Page Count and Page Size (0.2 points)
    # 0.1 each
    try:
        comp5_score = 0.0

        # Page count: should mention "8"
        found_page_count = False
        for line in content_lower.split('\n'):
            if 'page' in line and 'count' in line and '8' in line:
                found_page_count = True
                break
            if 'pages' in line and '8' in line:
                found_page_count = True
                break

        if found_page_count:
            print(f"  PASS: page count found with value 8")
            comp5_score += 0.1
        else:
            print(f"  FAIL: page count not found or incorrect (expected 8)")

        # Page size: should mention "letter" or "8.5 x 11" or "8.5x11"
        found_page_size = False
        for line in content_lower.split('\n'):
            if 'page' in line and 'size' in line:
                if 'letter' in line or '8.5' in line:
                    found_page_size = True
                    break

        if found_page_size:
            print(f"  PASS: page size found (Letter / 8.5 x 11)")
            comp5_score += 0.1
        else:
            print(f"  FAIL: page size not found or incorrect (expected Letter)")

        if comp5_score > 0:
            print(f"PASS: Component 5 -- page info ({comp5_score:.3f} pts)")
            total_score += comp5_score
        else:
            print(f"FAIL: Component 5 -- no page info found")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
