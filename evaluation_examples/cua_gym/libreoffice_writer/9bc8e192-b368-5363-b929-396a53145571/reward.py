"""
Reward Script: Find every line starting with a number followed by a period and add a tab after the period.
Task ID: writer_edit_061
Domain: libreoffice_writer
Scoring:
  Component 1: At least one numbered line has tab after period (0.2 pts)
  Component 2: All 8 numbered items have tab character after period (0.5 pts)
  Component 3: Item text content is intact (no items missing/corrupted) (0.3 pts)
"""

import os
import re

# python-docx for .docx verification
from docx import Document

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_edit_061'
FILE_NAME = 'numbered_list.docx'

# Expected content: 8 numbered items
EXPECTED_ITEMS = [
    "First item",
    "Second item",
    "Third item",
    "Fourth item",
    "Fifth item",
    "Sixth item",
    "Seventh item",
    "Eighth item",
]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Replace '. ' (period-space) with '.\t' (period-tab) in all lines
          starting with a number followed by a period (e.g. '1.', '2.', ...).
    Expected: Each of the 8 numbered paragraphs has the format 'N.\tItem name'
              (tab character after period, instead of a space).
    """
    total_score = 0.0

    # Precondition: Load the document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all paragraphs text
    paragraphs = [para.text for para in doc.paragraphs]

    # Identify numbered paragraphs (lines matching /^\d+\. /) — these are the ones to change
    # Pattern for lines that STILL have the old format (number. space)
    old_pattern = re.compile(r'^\d+\. ')
    # Pattern for lines that correctly have the new format (number.\t)
    new_pattern = re.compile(r'^\d+\.\t')

    numbered_paras = [p for p in paragraphs if old_pattern.match(p) or new_pattern.match(p)]

    # Component 1: At least one numbered line has been converted to use tab (0.2 points)
    # This FAILS on initial_env (all lines use space), PASSES on golden_env (all use tab)
    try:
        converted_lines = [p for p in paragraphs if new_pattern.match(p)]
        if len(converted_lines) >= 1:
            print(f"PASS: Component 1 — {len(converted_lines)} line(s) have tab after period (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — no lines with tab after period found. "
                  f"Found {len(numbered_paras)} numbered lines, all still use space.")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: ALL 8 numbered items have tab character after period (0.5 points)
    # This FAILS on initial_env (0 tabs), PASSES on golden_env (all 8 have tabs)
    try:
        # Lines that still use old format (space after period)
        unconverted_lines = [p for p in paragraphs if old_pattern.match(p)]

        if len(converted_lines) == 8 and len(unconverted_lines) == 0:
            print(f"PASS: Component 2 — all 8 numbered items have tab after period (0.5 pts)")
            total_score += 0.5
        else:
            if len(converted_lines) < 8:
                print(f"FAIL: Component 2 — only {len(converted_lines)}/8 items converted to tab. "
                      f"{len(unconverted_lines)} item(s) still use space: {unconverted_lines[:3]}")
            else:
                print(f"FAIL: Component 2 — unexpected state: {len(converted_lines)} converted, "
                      f"{len(unconverted_lines)} unconverted")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Item text content is fully intact (0.3 points)
    # Both checks (has tab AND has correct item text) must pass — anchored to the change
    # This FAILS on initial_env because the tab format is not present, PASSES on golden_env
    try:
        missing_items = [
            f"{i}.\t{expected_item}"
            for i, expected_item in enumerate(EXPECTED_ITEMS, start=1)
            if f"{i}.\t{expected_item}" not in paragraphs
        ]

        if len(missing_items) == 0 and len(converted_lines) == 8:
            print(f"PASS: Component 3 — all 8 items have correct tab format and intact text (0.3 pts)")
            total_score += 0.3
        else:
            if len(missing_items) > 0:
                print(f"FAIL: Component 3 — item text corrupted or missing. "
                      f"Missing lines: {missing_items}")
            else:
                print(f"FAIL: Component 3 — content check failed (not all 8 items converted)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification against canonical artifact path
file_path = os.path.join(WORKDIR, FILE_NAME)
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
