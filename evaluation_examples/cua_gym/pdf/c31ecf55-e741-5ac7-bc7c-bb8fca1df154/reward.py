"""
Reward Script: Extract PDF metadata and write to text file
Task ID: pdf_mbc_001
Domain: pdf
Scoring:
  Component 1: Title line correct (0.35 pts)
  Component 2: Author line correct (0.35 pts)
  Component 3: CreationDate line correct (0.30 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_001'

# Expected values from task context
EXPECTED_TITLE = 'Q3 2024 Financial Report'
EXPECTED_AUTHOR = 'Sarah Chen'
EXPECTED_CREATION_DATE = 'D:20240915083000'


def verify_task(file_path):
    """
    Verify that report_metadata.txt contains the correct PDF metadata.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse lines into a dict for flexible matching
    lines = [line.strip() for line in content.strip().splitlines() if line.strip()]
    metadata = {}
    for line in lines:
        if ':' in line:
            # Split on first ': ' to handle values that may contain colons
            key_part, _, val_part = line.partition(':')
            metadata[key_part.strip()] = val_part.strip()

    print(f"INFO: Found {len(lines)} non-empty lines, parsed {len(metadata)} key-value pairs")
    print(f"INFO: Parsed metadata: {metadata}")

    # Component 1: Title line correct (0.35 points)
    try:
        title_val = metadata.get('Title', None)
        if title_val is not None and title_val == EXPECTED_TITLE:
            print(f"PASS: Component 1 — Title matches: '{title_val}' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — Expected Title: '{EXPECTED_TITLE}', found: '{title_val}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Author line correct (0.35 points)
    try:
        author_val = metadata.get('Author', None)
        if author_val is not None and author_val == EXPECTED_AUTHOR:
            print(f"PASS: Component 2 — Author matches: '{author_val}' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — Expected Author: '{EXPECTED_AUTHOR}', found: '{author_val}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: CreationDate line correct (0.30 points)
    try:
        date_val = metadata.get('CreationDate', None)
        if date_val is not None and date_val == EXPECTED_CREATION_DATE:
            print(f"PASS: Component 3 — CreationDate matches: '{date_val}' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — Expected CreationDate: '{EXPECTED_CREATION_DATE}', found: '{date_val}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/report_metadata.txt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
