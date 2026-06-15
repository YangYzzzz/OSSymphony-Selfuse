"""
Reward Script: Remove double paragraph marks (empty lines) from document
Task ID: writer_frd_009
Domain: libreoffice_writer
Scoring:
  Component 1: No empty paragraphs remain (0.5 pts)
  Component 2: Paragraph count reduced to expected range (0.2 pts)
  Component 3: All original text content preserved (0.3 pts)
"""

import os

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'writer_frd_009'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    paras = doc.paragraphs

    # Extract paragraph texts
    all_texts = [p.text for p in paras]
    empty_count = sum(1 for t in all_texts if t.strip() == '')
    non_empty_texts = [t for t in all_texts if t.strip() != '']

    # Expected non-empty paragraphs (from initial document content)
    # The initial doc has 19 non-empty paragraphs with 18 empty ones between them
    EXPECTED_NON_EMPTY_COUNT = 19

    print(f"INFO: Total paragraphs: {len(paras)}")
    print(f"INFO: Empty paragraphs: {empty_count}")
    print(f"INFO: Non-empty paragraphs: {len(non_empty_texts)}")

    # Component 1: No empty paragraphs remain (0.5 points)
    # In initial_env there are 18 empty paragraphs; in golden there should be 0
    try:
        if empty_count == 0:
            print(f"PASS: Component 1 -- All empty paragraphs removed (0.5 pts)")
            total_score += 0.5
        else:
            # Partial credit: proportional to how many were removed
            # Initial had 18 empty paragraphs
            initial_empty = 18
            removed = max(0, initial_empty - empty_count)
            partial = 0.5 * (removed / initial_empty) if initial_empty > 0 else 0.0
            # Only award partial if at least some were removed
            if removed > 0:
                print(f"PARTIAL: Component 1 -- {removed}/{initial_empty} empty paragraphs removed ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 1 -- Still {empty_count} empty paragraphs remain (expected 0)")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Paragraph count is in expected range (0.2 points)
    # Golden should have exactly 19 paragraphs (all non-empty)
    # Initial has 37 paragraphs
    try:
        total_para_count = len(paras)
        if total_para_count == EXPECTED_NON_EMPTY_COUNT:
            print(f"PASS: Component 2 -- Paragraph count is {total_para_count} (expected {EXPECTED_NON_EMPTY_COUNT}) (0.2 pts)")
            total_score += 0.2
        elif total_para_count < 37 and total_para_count > EXPECTED_NON_EMPTY_COUNT:
            # Some empty paras removed but not all - partial credit
            removed_paras = 37 - total_para_count
            expected_removed = 37 - EXPECTED_NON_EMPTY_COUNT  # 18
            partial = 0.2 * (removed_paras / expected_removed)
            if partial > 0:
                print(f"PARTIAL: Component 2 -- Paragraph count is {total_para_count} (some removed, partial credit {partial:.2f} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 2 -- Paragraph count is {total_para_count}, expected {EXPECTED_NON_EMPTY_COUNT}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Empty paragraphs removed AND text content preserved (0.3 points)
    # This is a compound check: it requires that empty lines were removed (the task change)
    # AND that original text was not lost. This ensures it only passes when the task is done.
    try:
        # Gate: empty paragraphs must actually be removed (task change required)
        if empty_count > 0:
            print(f"FAIL: Component 3 -- Empty paragraphs still present ({empty_count}), text preservation check skipped")
        else:
            # Now verify content is intact
            expected_first = "Quarterly Performance Review - Q1 2025"
            expected_last_start = "Risk factors to monitor include potential currency fluctuations affecting Europe"
            expected_headings = [
                "Executive Summary",
                "Revenue Analysis",
                "Team Performance",
                "Product Development",
                "Financial Outlook",
            ]

            content_issues = []

            if len(non_empty_texts) != EXPECTED_NON_EMPTY_COUNT:
                content_issues.append(f"Expected {EXPECTED_NON_EMPTY_COUNT} non-empty paragraphs, found {len(non_empty_texts)}")

            if len(non_empty_texts) > 0 and non_empty_texts[0].strip() != expected_first:
                content_issues.append(f"First paragraph mismatch")

            if len(non_empty_texts) > 0 and not non_empty_texts[-1].strip().startswith(expected_last_start):
                content_issues.append(f"Last paragraph mismatch")

            for heading in expected_headings:
                if heading not in non_empty_texts:
                    content_issues.append(f"Missing heading: '{heading}'")

            if len(content_issues) == 0:
                print(f"PASS: Component 3 -- Empty lines removed AND all text preserved (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 -- Empty lines removed but content issues: {'; '.join(content_issues)}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

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
