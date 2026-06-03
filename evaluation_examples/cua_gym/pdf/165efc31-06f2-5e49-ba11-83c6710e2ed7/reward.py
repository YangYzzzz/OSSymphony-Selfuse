"""
Reward Script: Convert scanned receipt PDFs to searchable PDFs using OCR
Task ID: pdf_fin_035
Domain: pdf
Scoring:
  Component 1 (0.4): All 5 output files exist in searchable_receipts/
  Component 2 (0.4): Each output PDF has extractable text (text layer added by OCR)
  Component 3 (0.2): Extracted text contains recognizable receipt content (store names, amounts, dates)
"""

import os
import pymupdf
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_035'

EXPECTED_FILES = [
    'receipt_001.pdf',
    'receipt_002.pdf',
    'receipt_003.pdf',
    'receipt_004.pdf',
    'receipt_005.pdf',
]

OUTPUT_DIR = os.path.join(WORKDIR, 'finance', 'searchable_receipts')

# Minimum text length to consider a PDF as having a meaningful text layer
MIN_TEXT_LENGTH = 50


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: All 5 output files exist in searchable_receipts/ (0.4 points)
    # This checks that the agent created all 5 output files.
    # On initial_env, searchable_receipts/ is empty, so this will FAIL.
    try:
        existing_files = []
        for fname in EXPECTED_FILES:
            fpath = os.path.join(OUTPUT_DIR, fname)
            if os.path.isfile(fpath):
                existing_files.append(fname)

        files_found = len(existing_files)
        if files_found == len(EXPECTED_FILES):
            print(f"PASS: Component 1 — All {files_found}/{len(EXPECTED_FILES)} output files exist (0.4 pts)")
            total_score += 0.4
        elif files_found > 0:
            partial = round(0.4 * files_found / len(EXPECTED_FILES), 2)
            print(f"PARTIAL: Component 1 — {files_found}/{len(EXPECTED_FILES)} files exist ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No output files found in {OUTPUT_DIR}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Each output PDF has extractable text (0.4 points)
    # The task is to add a text layer via OCR. Initial PDFs are image-only (0 text).
    # Golden PDFs should have substantial extractable text.
    # On initial_env, searchable_receipts/ is empty, so this will FAIL (no files to check).
    try:
        pdfs_with_text = 0
        for fname in EXPECTED_FILES:
            fpath = os.path.join(OUTPUT_DIR, fname)
            if not os.path.isfile(fpath):
                print(f"  SKIP: {fname} not found")
                continue
            try:
                doc = pymupdf.open(fpath)
                if doc.page_count < 1:
                    print(f"  FAIL: {fname} has no pages")
                    doc.close()
                    continue
                page = doc[0]
                text = page.get_text("text").strip()
                doc.close()
                if len(text) >= MIN_TEXT_LENGTH:
                    pdfs_with_text += 1
                    print(f"  OK: {fname} has text layer ({len(text)} chars)")
                else:
                    print(f"  FAIL: {fname} has insufficient text ({len(text)} chars, need >= {MIN_TEXT_LENGTH})")
            except Exception as e:
                print(f"  ERROR: {fname} — {e}")

        if pdfs_with_text == len(EXPECTED_FILES):
            print(f"PASS: Component 2 — All {pdfs_with_text}/{len(EXPECTED_FILES)} PDFs have text layers (0.4 pts)")
            total_score += 0.4
        elif pdfs_with_text > 0:
            partial = round(0.4 * pdfs_with_text / len(EXPECTED_FILES), 2)
            print(f"PARTIAL: Component 2 — {pdfs_with_text}/{len(EXPECTED_FILES)} PDFs have text layers ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No PDFs have meaningful text layers")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Extracted text contains recognizable receipt content (0.2 points)
    # Verify that OCR produced meaningful text, not garbage.
    # We check for receipt-like patterns: dollar amounts, dates, store-like words.
    # On initial_env, no files exist so this will FAIL.
    try:
        pdfs_with_receipt_content = 0
        # Patterns common to receipts
        dollar_pattern = re.compile(r'\$?\d+\.\d{2}')
        date_pattern = re.compile(r'\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[-/]\d{2}[-/]\d{4}')

        for fname in EXPECTED_FILES:
            fpath = os.path.join(OUTPUT_DIR, fname)
            if not os.path.isfile(fpath):
                continue
            try:
                doc = pymupdf.open(fpath)
                if doc.page_count < 1:
                    doc.close()
                    continue
                text = doc[0].get_text("text")
                doc.close()

                has_amount = bool(dollar_pattern.search(text))
                has_date = bool(date_pattern.search(text))

                if has_amount and has_date:
                    pdfs_with_receipt_content += 1
                    print(f"  OK: {fname} contains receipt data (amounts + dates)")
                elif has_amount or has_date:
                    # Partial: at least some recognizable content
                    pdfs_with_receipt_content += 0.5
                    print(f"  PARTIAL: {fname} has some receipt data (amount={has_amount}, date={has_date})")
                else:
                    print(f"  FAIL: {fname} text does not contain recognizable receipt data")
            except Exception as e:
                print(f"  ERROR: {fname} — {e}")

        if pdfs_with_receipt_content >= len(EXPECTED_FILES):
            print(f"PASS: Component 3 — All PDFs contain recognizable receipt content (0.2 pts)")
            total_score += 0.2
        elif pdfs_with_receipt_content > 0:
            partial = round(0.2 * pdfs_with_receipt_content / len(EXPECTED_FILES), 2)
            print(f"PARTIAL: Component 3 — {pdfs_with_receipt_content}/{len(EXPECTED_FILES)} PDFs have receipt content ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No PDFs contain recognizable receipt data")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isdir(OUTPUT_DIR):
    print(f"Output directory not found: {OUTPUT_DIR}")
    print("REWARD: 0.0")
else:
    verify_task()
