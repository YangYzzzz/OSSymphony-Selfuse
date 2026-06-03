"""
Reward Script: Find corresponding author on Google Scholar and summarize in Writer
Task ID: osworld_multi_apps_paper_scholar_browse_009
Domain: libreoffice_writer (multi-app: PDF + Chrome + Writer)
Scoring:
  Component 1: Document has at least one non-empty paragraph (0.2 pts)
  Component 2: Paragraph matches the required format pattern (0.3 pts)
  Component 3: Correct author name 'Yuki Tanaka' is present (0.2 pts)
  Component 4: h-index value matches expected value of 23 (0.15 pts)
  Component 5: Citations value matches expected value of 1547 (0.15 pts)
Total: 1.0
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_paper_scholar_browse_009'

# Expected ground truth values (from golden_env)
EXPECTED_AUTHOR = 'Yuki Tanaka'
EXPECTED_H_INDEX = 23
EXPECTED_CITATIONS = 1547

# Format pattern: 'Name: [name], h-index: [h], Citations: [n]'
FORMAT_PATTERN = re.compile(
    r'Name:\s*.+,\s*h-index:\s*\d+,\s*Citations:\s*\d+',
    re.IGNORECASE
)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Checks that the Writer document contains a one-line summary of the
    corresponding author's Google Scholar profile.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document
    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all non-empty paragraph texts
    all_paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

    # Component 1: Document has at least one non-empty paragraph (0.2 points)
    try:
        if len(all_paragraphs) >= 1:
            print(f"PASS: Component 1 — document has {len(all_paragraphs)} non-empty paragraph(s) (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 1 — document is empty, no non-empty paragraphs found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Get all text combined for subsequent checks
    doc_text = '\n'.join(all_paragraphs)

    # Component 2: Paragraph matches the required format 'Name: ..., h-index: ..., Citations: ...' (0.3 points)
    try:
        format_match = FORMAT_PATTERN.search(doc_text)
        if format_match:
            print(f"PASS: Component 2 — format pattern matched: '{format_match.group()}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — expected format 'Name: [name], h-index: [number], Citations: [number]', got: '{doc_text[:200]}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct author name 'Yuki Tanaka' is present in the document (0.2 points)
    try:
        if EXPECTED_AUTHOR.lower() in doc_text.lower():
            print(f"PASS: Component 3 — author name '{EXPECTED_AUTHOR}' found in document (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — expected author name '{EXPECTED_AUTHOR}', not found in: '{doc_text[:200]}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: h-index value matches expected value of 23 (0.15 points)
    try:
        h_index_match = re.search(r'h-index:\s*(\d+)', doc_text, re.IGNORECASE)
        if h_index_match:
            found_h_index = int(h_index_match.group(1))
            if found_h_index == EXPECTED_H_INDEX:
                print(f"PASS: Component 4 — h-index is {found_h_index} (expected {EXPECTED_H_INDEX}) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — h-index is {found_h_index}, expected {EXPECTED_H_INDEX}")
        else:
            print("FAIL: Component 4 — h-index value not found in document")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Citations value matches expected value of 1547 (0.15 points)
    try:
        citations_match = re.search(r'Citations:\s*(\d+)', doc_text, re.IGNORECASE)
        if citations_match:
            found_citations = int(citations_match.group(1))
            if found_citations == EXPECTED_CITATIONS:
                print(f"PASS: Component 5 — Citations is {found_citations} (expected {EXPECTED_CITATIONS}) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — Citations is {found_citations}, expected {EXPECTED_CITATIONS}")
        else:
            print("FAIL: Component 5 — Citations value not found in document")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

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
