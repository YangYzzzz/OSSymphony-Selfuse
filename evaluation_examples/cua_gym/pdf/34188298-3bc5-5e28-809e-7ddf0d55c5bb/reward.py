"""
Reward Script: Update PDF metadata
Task ID: pdf_gf2_014
Domain: pdf
Scoring:
  - Component 1: Title metadata (0.20)
  - Component 2: Author metadata (0.20)
  - Component 3: Subject metadata (0.15)
  - Component 4: Keywords metadata (0.15)
  - Component 5: Creator metadata (0.10)
  - Component 6: Creation date metadata (0.05)
  - Component 7: Page count preserved at 18 (0.15)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_014'

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    meta = doc.metadata
    page_count = doc.page_count
    doc.close()

    print(f"INFO: Loaded file with {page_count} pages")
    print(f"INFO: Metadata: {meta}")

    # Component 1: Title metadata (0.20 points)
    try:
        expected_title = "Quantum Computing Applications in Cryptography"
        actual_title = (meta.get("title") or "").strip()
        if actual_title == expected_title:
            print(f"PASS: Component 1 — Title matches: '{actual_title}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Expected title '{expected_title}', found '{actual_title}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Author metadata (0.20 points)
    try:
        expected_author = "Dr. James Wei"
        actual_author = (meta.get("author") or "").strip()
        if actual_author == expected_author:
            print(f"PASS: Component 2 — Author matches: '{actual_author}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Expected author '{expected_author}', found '{actual_author}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Subject metadata (0.15 points)
    try:
        expected_subject = "Quantum Cryptography"
        actual_subject = (meta.get("subject") or "").strip()
        if actual_subject == expected_subject:
            print(f"PASS: Component 3 — Subject matches: '{actual_subject}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Expected subject '{expected_subject}', found '{actual_subject}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Keywords metadata (0.15 points)
    try:
        expected_keywords = "quantum, cryptography, lattice-based, post-quantum"
        actual_keywords = (meta.get("keywords") or "").strip()
        # Normalize: compare sorted keyword sets for robustness
        expected_set = set(k.strip().lower() for k in expected_keywords.split(","))
        actual_set = set(k.strip().lower() for k in actual_keywords.split(",")) if actual_keywords else set()
        if expected_set == actual_set:
            print(f"PASS: Component 4 — Keywords match: '{actual_keywords}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Expected keywords '{expected_keywords}', found '{actual_keywords}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Creator metadata (0.10 points)
    try:
        expected_creator = "LibreOffice Writer"
        actual_creator = (meta.get("creator") or "").strip()
        if actual_creator == expected_creator:
            print(f"PASS: Component 5 — Creator matches: '{actual_creator}' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — Expected creator '{expected_creator}', found '{actual_creator}'")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Creation date contains 2026-03-15 (0.05 points)
    try:
        actual_date = (meta.get("creationDate") or "").strip()
        # PyMuPDF stores dates as 'D:YYYYMMDDHHmmSS...' format
        # We check that the date string contains 20260315
        if "20260315" in actual_date:
            print(f"PASS: Component 6 — Creation date contains 2026-03-15: '{actual_date}' (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 6 — Expected creation date with 20260315, found '{actual_date}'")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: Page count preserved at 18 (0.15 points)
    # This ensures the content was not corrupted during metadata update
    # This check is anchored to the output file existing (which it doesn't on initial_env)
    try:
        if page_count == 18:
            print(f"PASS: Component 7 — Page count is 18 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 7 — Expected 18 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/research_paper_meta.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
