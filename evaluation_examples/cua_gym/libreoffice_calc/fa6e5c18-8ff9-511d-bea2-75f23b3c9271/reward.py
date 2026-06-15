"""
Reward Script: Find recent papers by PDF authors and list them in Writer document
Task ID: osworld_multi_apps_paper_scholar_browse_013
Domain: libreoffice_writer (multi-app task involving Chrome + PDF + Writer)
Scoring:
  Component 1: Document has at least 1 non-empty entry (0.3 points)
  Component 2: Entries follow '[Year] Title' format with valid years 2023-2025 (0.4 points)
  Component 3: Document has at least 3 entries (up to 5) (0.3 points)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_paper_scholar_browse_013'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The task requires:
    - Open a PDF, identify 3 authors (Jiasen Lu, Dhruv Batra, Devi Parikh)
    - Search Google Scholar for recent papers (2023-2025) by those authors
    - List up to 5 papers in Writer document in format '[Year] Title'
    - Save the document

    Initial state: blank Writer document
    Golden state: 5 entries in '[Year] Title' format
    """
    total_score = 0.0

    try:
        from docx import Document
    except ImportError:
        print("CRITICAL: python-docx not available")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all non-empty paragraph texts
    entries = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    print(f"INFO: Found {len(entries)} non-empty paragraphs in document")
    for i, entry in enumerate(entries):
        print(f"  [{i+1}]: {entry}")

    # Component 1: Document has at least 1 non-empty entry (0.3 points)
    # Initial state: blank document (0 entries) — this will FAIL on initial
    # Golden state: 5 entries — this will PASS on golden
    try:
        if len(entries) >= 1:
            print(f"PASS: Component 1 — Document contains {len(entries)} entries (at least 1 required) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Document is empty (0 non-empty paragraphs found)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Entries follow '[Year] Title' format with valid years (0.4 points)
    # Format pattern: [YYYY] followed by a title string
    # Valid years for "last 2 years" from 2025: 2023, 2024, 2025
    # Initial state: blank — no entries to match format — FAIL
    # Golden state: 5 entries all in correct format — PASS
    try:
        # Pattern: starts with [YYYY] where YYYY is 2023-2025
        year_title_pattern = re.compile(r'^\[20(2[3-5])\]\s+.{5,}')
        formatted_entries = [e for e in entries if year_title_pattern.match(e)]
        print(f"INFO: {len(formatted_entries)} entries match '[Year] Title' format with valid years 2023-2025")

        if len(formatted_entries) >= 1:
            print(f"PASS: Component 2 — {len(formatted_entries)} entries correctly formatted as '[Year] Title' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — No entries match '[Year] Title' format with years 2023-2025")
            if entries:
                print(f"  Sample entry: {entries[0]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Document contains at least 3 properly formatted entries (0.3 points)
    # Task asks for "up to 5" papers — a good completion should have at least 3
    # Initial state: blank — FAIL
    # Golden state: 5 formatted entries — PASS (5 >= 3)
    try:
        # Re-use formatted_entries from Component 2 or recompute safely
        year_title_pattern2 = re.compile(r'^\[20(2[3-5])\]\s+.{5,}')
        formatted_entries2 = [e for e in entries if year_title_pattern2.match(e)]

        if len(formatted_entries2) >= 3:
            print(f"PASS: Component 3 — Document has {len(formatted_entries2)} properly formatted entries (at least 3 required) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Only {len(formatted_entries2)} properly formatted entries found (need at least 3)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
