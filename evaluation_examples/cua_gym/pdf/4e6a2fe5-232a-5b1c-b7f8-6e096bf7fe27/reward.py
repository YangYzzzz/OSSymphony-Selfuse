"""
Reward Script: Split 100-page batch invoice PDF into 50 individual invoice PDFs
Task ID: pdf_gf3_013
Domain: pdf
Scoring:
  Component 1: Split directory created with exactly 50 PDF files (0.2 pts)
  Component 2: All files follow INV-2024-XXX.pdf naming pattern (0.2 pts)
  Component 3: Each split PDF has exactly 2 pages (0.2 pts)
  Component 4: Invoice number on first page matches filename (0.2 pts)
  Component 5: Total pages across all splits equals 100 (0.2 pts)
"""

import os
import re

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
SPLIT_DIR = os.path.join(WORKDIR, 'invoices', 'split')
BATCH_PDF = os.path.join(WORKDIR, 'invoices', 'batch_invoices.pdf')
EXPECTED_FILES = 50
EXPECTED_PAGES_PER_FILE = 2
EXPECTED_TOTAL_PAGES = 100

INV_PATTERN = re.compile(r'^INV-2024-\d{3}\.pdf$')
INV_TEXT_PATTERN = re.compile(r'Invoice\s*#\s*(INV-2024-\d{3})')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: batch PDF must exist
    if not os.path.exists(BATCH_PDF):
        print(f"CRITICAL: Batch PDF not found at {BATCH_PDF}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: split directory must exist
    if not os.path.isdir(SPLIT_DIR):
        print(f"FAIL: Split directory does not exist at {SPLIT_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Get list of PDF files in split directory
    try:
        all_files = sorted(os.listdir(SPLIT_DIR))
        pdf_files = [f for f in all_files if f.lower().endswith('.pdf')]
    except Exception as e:
        print(f"CRITICAL: Cannot list split directory: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Exactly 50 PDF files in split directory (0.2 points)
    try:
        if len(pdf_files) == EXPECTED_FILES:
            print(f"PASS: Component 1 — Found exactly {EXPECTED_FILES} PDF files (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_FILES} PDFs, found {len(pdf_files)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All files follow INV-2024-XXX.pdf naming pattern (0.2 points)
    try:
        matching = [f for f in pdf_files if INV_PATTERN.match(f)]
        if len(matching) == len(pdf_files) and len(pdf_files) > 0:
            print(f"PASS: Component 2 — All {len(pdf_files)} files match INV-2024-XXX.pdf pattern (0.2 pts)")
            total_score += 0.2
        else:
            non_matching = [f for f in pdf_files if not INV_PATTERN.match(f)]
            print(f"FAIL: Component 2 — {len(non_matching)} files don't match pattern: {non_matching[:5]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Each split PDF has exactly 2 pages (0.2 points)
    try:
        correct_page_count = 0
        wrong_page_files = []
        for f in pdf_files:
            fpath = os.path.join(SPLIT_DIR, f)
            doc = pymupdf.open(fpath)
            pages = len(doc)
            doc.close()
            if pages == EXPECTED_PAGES_PER_FILE:
                correct_page_count += 1
            else:
                wrong_page_files.append((f, pages))

        if correct_page_count == len(pdf_files) and len(pdf_files) > 0:
            print(f"PASS: Component 3 — All {len(pdf_files)} PDFs have exactly 2 pages (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — {len(wrong_page_files)} files have wrong page count: {wrong_page_files[:5]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Invoice number on first page matches filename (0.2 points)
    try:
        matched_count = 0
        mismatch_files = []
        for f in pdf_files:
            fpath = os.path.join(SPLIT_DIR, f)
            doc = pymupdf.open(fpath)
            if len(doc) > 0:
                text = doc[0].get_text()[:500]
                m = INV_TEXT_PATTERN.search(text)
                if m:
                    expected_name = m.group(1) + '.pdf'
                    if expected_name == f:
                        matched_count += 1
                    else:
                        mismatch_files.append((f, expected_name))
                else:
                    mismatch_files.append((f, 'NO_INVOICE_NUMBER_FOUND'))
            doc.close()

        if matched_count == len(pdf_files) and len(pdf_files) > 0:
            print(f"PASS: Component 4 — All {len(pdf_files)} filenames match invoice numbers (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — {len(mismatch_files)} mismatches: {mismatch_files[:5]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Total pages across all splits equals 100 (0.2 points)
    try:
        total_pages = 0
        for f in pdf_files:
            fpath = os.path.join(SPLIT_DIR, f)
            doc = pymupdf.open(fpath)
            total_pages += len(doc)
            doc.close()

        if total_pages == EXPECTED_TOTAL_PAGES:
            print(f"PASS: Component 5 — Total pages across splits: {total_pages} == {EXPECTED_TOTAL_PAGES} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 — Total pages: {total_pages}, expected {EXPECTED_TOTAL_PAGES}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
