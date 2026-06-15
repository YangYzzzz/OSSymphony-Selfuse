"""
Reward Script: Clean up legal citation list by removing duplicates and sorting alphabetically
Task ID: osworld_writer_duplicate_line_removal_010
Domain: libreoffice_writer
Scoring:
  Component 1: All duplicate citations removed (32 unique citations remaining) — 0.5 points
  Component 2: Citations sorted alphabetically — 0.5 points
"""

import os

from docx import Document

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_duplicate_line_removal_010'

# Ground truth from task context:
# Initial doc: 48 citation lines, 16 are duplicates → 32 unique
# Golden doc: 32 unique citations, sorted alphabetically

EXPECTED_CITATION_COUNT = 32


def get_citation_lines(doc):
    """
    Extract citation lines from the document.
    The document has 3 header paragraphs (potentially with blank lines between them)
    then citation lines. We identify citation lines as non-empty paragraphs
    that appear after the 'CASES CITED' paragraph.
    """
    paras = [p.text for p in doc.paragraphs]
    # Find the index of "CASES CITED" section header
    cases_cited_idx = None
    for i, text in enumerate(paras):
        if text.strip() == 'CASES CITED':
            cases_cited_idx = i
            break

    if cases_cited_idx is None:
        return None

    # All non-empty paragraphs after "CASES CITED" are citation lines
    citations = [p for p in paras[cases_cited_idx + 1:] if p.strip()]
    return citations


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

    # Extract citation lines (everything after the 'CASES CITED' header)
    citations = get_citation_lines(doc)
    if citations is None:
        print("CRITICAL: Could not find 'CASES CITED' section in document")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(citations)} citation lines in document")

    # Component 1: Deduplication — exactly 32 unique citations with no duplicates (0.5 points)
    # This FAILS on initial_env (48 lines, 16 duplicates) and PASSES on golden_env (32 unique lines)
    try:
        num_citations = len(citations)
        unique_citations = list(dict.fromkeys(citations))  # preserve order while deduplicating
        num_unique = len(unique_citations)
        has_duplicates = num_citations != num_unique

        if not has_duplicates and num_citations == EXPECTED_CITATION_COUNT:
            print(f"PASS: Component 1 — Deduplication complete: {num_citations} unique citations (no duplicates) ({0.5} pts)")
            total_score += 0.5
        elif has_duplicates:
            duplicate_count = num_citations - num_unique
            print(f"FAIL: Component 1 — Found {duplicate_count} duplicate(s) among {num_citations} citations; expected 0 duplicates in {EXPECTED_CITATION_COUNT} lines")
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_CITATION_COUNT} unique citations, found {num_citations}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Alphabetical sorting — citations must be in case-insensitive alphabetical order (0.5 points)
    # This FAILS on initial_env (unsorted order) and PASSES on golden_env (sorted alphabetically)
    try:
        if len(citations) == 0:
            print("FAIL: Component 2 — No citations found to check sorting")
        else:
            sorted_citations = sorted(citations, key=lambda x: x.lower())
            is_sorted = (citations == sorted_citations)
            if is_sorted:
                print(f"PASS: Component 2 — Citations are sorted alphabetically ({0.5} pts)")
                total_score += 0.5
            else:
                # Find first out-of-order pair for diagnostics
                for i in range(1, len(citations)):
                    if citations[i].lower() < citations[i - 1].lower():
                        print(f"FAIL: Component 2 — Not alphabetically sorted; first violation at position {i}: '{citations[i-1]}' followed by '{citations[i]}'")
                        break
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in the given env
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
