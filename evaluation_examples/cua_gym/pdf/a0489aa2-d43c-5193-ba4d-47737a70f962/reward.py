"""
Reward Script: Add exhibit stamps and Bates numbering to financial evidence PDFs
Task ID: pdf_fin_094
Domain: pdf
Scoring:
  - Component 1 (0.15): All 3 stamped PDF files exist in stamped/ directory
  - Component 2 (0.35): Exhibit stamps (EXHIBIT A/B/C) on page 1 of each document
  - Component 3 (0.35): Continuous Bates numbering EX-00001 through EX-00015
  - Component 4 (0.15): Page counts preserved (doc_a=5, doc_b=3, doc_c=7)
"""

import os
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    import pymupdf as fitz

STAMPED_DIR = '/home/user/finance/evidence/stamped'
TASK_ID = 'pdf_fin_094'

# Expected document properties
DOCS = [
    ('doc_a.pdf', 5, 'EXHIBIT A'),
    ('doc_b.pdf', 3, 'EXHIBIT B'),
    ('doc_c.pdf', 7, 'EXHIBIT C'),
]

# Expected Bates numbers: EX-00001 through EX-00015 continuously across all docs
# doc_a: pages get EX-00001..EX-00005
# doc_b: pages get EX-00006..EX-00008
# doc_c: pages get EX-00009..EX-00015
EXPECTED_BATES = {}
bates_counter = 1
for fname, page_count, _ in DOCS:
    EXPECTED_BATES[fname] = []
    for _ in range(page_count):
        EXPECTED_BATES[fname].append(f'EX-{bates_counter:05d}')
        bates_counter += 1


def extract_text_from_page(doc, page_idx):
    """Extract all text from a PDF page."""
    page = doc[page_idx]
    return page.get_text()


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: All 3 stamped PDF files exist (0.15 points)
    # This checks that the stamped/ directory contains the expected output files.
    # Only awards points if ALL 3 files are present (not partial).
    try:
        files_found = 0
        for fname, _, _ in DOCS:
            fpath = os.path.join(STAMPED_DIR, fname)
            if os.path.isfile(fpath):
                files_found += 1
            else:
                print(f"FAIL: Component 1 — Missing file: {fpath}")

        if files_found == 3:
            print(f"PASS: Component 1 — All 3 stamped PDFs exist (0.15 pts)")
            total_score += 0.15
        elif files_found > 0:
            # Partial: proportional credit within this component
            partial = round(0.15 * (files_found / 3), 4)
            if partial > 0:
                print(f"PARTIAL: Component 1 — {files_found}/3 files found ({partial} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 1 — No stamped files found in {STAMPED_DIR}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Early exit if no files at all
    if not any(os.path.isfile(os.path.join(STAMPED_DIR, f)) for f, _, _ in DOCS):
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Exhibit stamps on page 1 of each document (0.35 points)
    # Each document's first page should contain the correct EXHIBIT label.
    # Points: ~0.1167 per correct exhibit stamp
    try:
        exhibit_pass = 0
        per_exhibit = round(0.35 / 3, 4)
        for fname, _, expected_exhibit in DOCS:
            fpath = os.path.join(STAMPED_DIR, fname)
            if not os.path.isfile(fpath):
                print(f"FAIL: Component 2 — {fname} not found, cannot check exhibit stamp")
                continue
            try:
                doc = fitz.open(fpath)
                if len(doc) < 1:
                    print(f"FAIL: Component 2 — {fname} has 0 pages")
                    doc.close()
                    continue
                page_text = extract_text_from_page(doc, 0)
                if expected_exhibit in page_text:
                    print(f"PASS: Component 2 — {fname} page 1 contains '{expected_exhibit}' ({per_exhibit} pts)")
                    total_score += per_exhibit
                    exhibit_pass += 1
                else:
                    print(f"FAIL: Component 2 — {fname} page 1 missing '{expected_exhibit}'")
                doc.close()
            except Exception as e:
                print(f"ERROR: Component 2 — {fname}: {e}")

        if exhibit_pass == 3:
            print(f"  All 3 exhibit stamps verified")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Continuous Bates numbering EX-00001 through EX-00015 (0.35 points)
    # Each page of each document should have the correct sequential Bates number.
    # Points distributed per correct Bates number: 0.35/15 per number
    try:
        bates_correct = 0
        bates_total = 15
        per_bates = round(0.35 / bates_total, 4)
        for fname, expected_pages, _ in DOCS:
            fpath = os.path.join(STAMPED_DIR, fname)
            if not os.path.isfile(fpath):
                print(f"FAIL: Component 3 — {fname} not found, cannot check Bates numbers")
                continue
            try:
                doc = fitz.open(fpath)
                expected_bates_list = EXPECTED_BATES[fname]
                for page_idx, expected_bates in enumerate(expected_bates_list):
                    if page_idx >= len(doc):
                        print(f"FAIL: Component 3 — {fname} page {page_idx} does not exist")
                        continue
                    page_text = extract_text_from_page(doc, page_idx)
                    if expected_bates in page_text:
                        bates_correct += 1
                    else:
                        print(f"FAIL: Component 3 — {fname} page {page_idx} missing '{expected_bates}'")
                doc.close()
            except Exception as e:
                print(f"ERROR: Component 3 — {fname}: {e}")

        bates_score = round(per_bates * bates_correct, 4)
        if bates_correct == bates_total:
            print(f"PASS: Component 3 — All {bates_total} Bates numbers correct ({bates_score} pts)")
            total_score += bates_score
        elif bates_correct > 0:
            print(f"PARTIAL: Component 3 — {bates_correct}/{bates_total} Bates numbers correct ({bates_score} pts)")
            total_score += bates_score
        else:
            print(f"FAIL: Component 3 — No correct Bates numbers found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Page counts preserved (0.15 points)
    # doc_a should have 5 pages, doc_b 3 pages, doc_c 7 pages
    # Points: 0.05 per correct page count
    try:
        page_count_pass = 0
        per_doc_pages = 0.05
        for fname, expected_pages, _ in DOCS:
            fpath = os.path.join(STAMPED_DIR, fname)
            if not os.path.isfile(fpath):
                print(f"FAIL: Component 4 — {fname} not found")
                continue
            try:
                doc = fitz.open(fpath)
                actual_pages = len(doc)
                doc.close()
                if actual_pages == expected_pages:
                    print(f"PASS: Component 4 — {fname} has {actual_pages} pages as expected ({per_doc_pages} pts)")
                    total_score += per_doc_pages
                    page_count_pass += 1
                else:
                    print(f"FAIL: Component 4 — {fname} has {actual_pages} pages, expected {expected_pages}")
            except Exception as e:
                print(f"ERROR: Component 4 — {fname}: {e}")

        if page_count_pass == 3:
            print(f"  All 3 page counts correct")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isdir(STAMPED_DIR):
    print(f"Stamped directory not found: {STAMPED_DIR}")
    print("REWARD: 0.0")
else:
    verify_task()
