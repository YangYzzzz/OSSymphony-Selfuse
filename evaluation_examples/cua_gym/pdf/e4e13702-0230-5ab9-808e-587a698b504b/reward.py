"""
Reward Script: Read PDF metadata and write summary to metadata_report.txt
Task ID: pdf_gf1_028
Domain: pdf
Scoring:
  Component 1 (0.25): All required field labels present (Title:, Author:, Creator:, Producer:, CreationDate:, ModDate:)
  Component 2 (0.25): Title line contains 'Q3 Financial Summary'
  Component 3 (0.20): Author line contains 'Finance Team'
  Component 4 (0.15): Page count present — 'Pages: 8' or '8 pages'
  Component 5 (0.15): CreationDate and ModDate lines contain actual date values
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_028'

REPORT_PATH = os.path.join(WORKDIR, 'Documents', 'metadata_report.txt')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist
    if not os.path.exists(REPORT_PATH):
        print(f"CRITICAL: metadata_report.txt not found at {REPORT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(REPORT_PATH, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read {REPORT_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    content_lower = content.lower()
    lines = content.strip().split('\n')

    # Component 1: All required field labels present (0.25 points)
    try:
        required_labels = ['title:', 'author:', 'creator:', 'producer:', 'creationdate:', 'moddate:']
        found_labels = [label for label in required_labels if label in content_lower]
        missing_labels = [label for label in required_labels if label not in content_lower]

        if len(found_labels) == len(required_labels):
            print(f"PASS: Component 1 — All 6 required field labels present (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Missing labels: {missing_labels}. Found: {found_labels}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Title line contains 'Q3 Financial Summary' (0.25 points)
    try:
        matching_lines = [
            line for line in lines
            if 'title' in line.lower() and 'q3 financial summary' in line.lower()
        ]
        if len(matching_lines) > 0:
            print(f"PASS: Component 2 — Title line contains 'Q3 Financial Summary' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — No line with both 'Title' and 'Q3 Financial Summary' found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Author line contains 'Finance Team' (0.20 points)
    try:
        matching_lines = [
            line for line in lines
            if 'author' in line.lower() and 'finance team' in line.lower()
        ]
        if len(matching_lines) > 0:
            print(f"PASS: Component 3 — Author line contains 'Finance Team' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — No line with both 'Author' and 'Finance Team' found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Page count is 8 (0.15 points)
    # Accept variations: 'Pages: 8', '8 pages', 'Page Count: 8', 'Number of Pages: 8', etc.
    try:
        page_pattern = r'(pages?\s*:\s*8\b|\b8\s+pages?\b|(page\s*count|number\s+of\s+pages?)\s*:\s*8\b)'
        if re.search(page_pattern, content_lower):
            print(f"PASS: Component 4 — Page count of 8 found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Could not find page count of 8 in the report")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: CreationDate and ModDate lines have actual date values (0.15 points)
    # The lines should contain actual date strings, not just the label
    try:
        creation_value_len = 0
        mod_value_len = 0
        for line in lines:
            line_lower = line.lower().strip()
            if 'creationdate' in line_lower:
                idx = line_lower.index('creationdate')
                after_label = line[idx + len('creationdate'):].lstrip(':').strip()
                creation_value_len = len(after_label)
            if 'moddate' in line_lower:
                idx = line_lower.index('moddate')
                after_label = line[idx + len('moddate'):].lstrip(':').strip()
                mod_value_len = len(after_label)

        if creation_value_len >= 4 and mod_value_len >= 4:
            print(f"PASS: Component 5 — CreationDate and ModDate both have date values (0.15 pts)")
            total_score += 0.15
        else:
            missing = []
            if creation_value_len < 4:
                missing.append(f'CreationDate (value length: {creation_value_len})')
            if mod_value_len < 4:
                missing.append(f'ModDate (value length: {mod_value_len})')
            print(f"FAIL: Component 5 — Insufficient date values for: {missing}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
