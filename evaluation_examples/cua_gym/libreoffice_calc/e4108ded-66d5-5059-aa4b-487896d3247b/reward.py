"""
Reward Script: PDF OCR — make scanned invoice searchable and extract text
Task ID: pdf_gf2_012
Domain: pdf
Scoring:
  Component 1: OCR PDF exists with 3 pages (0.15)
  Component 2: OCR PDF has text layer on all pages (0.25)
  Component 3: OCR PDF searchable for "INV-2026-0042" (0.20)
  Component 4: Text file exists and is non-empty (0.10)
  Component 5: Text file has page separators for 3 pages (0.15)
  Component 6: Text file contains invoice number (0.15)
"""

import os

try:
    import fitz  # PyMuPDF
except ImportError:
    import pymupdf as fitz

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_012'

OCR_PDF_PATH = os.path.join(WORKDIR, 'scans', 'invoice_scan_ocr.pdf')
TEXT_FILE_PATH = os.path.join(WORKDIR, 'scans', 'invoice_text.txt')


def verify_task():
    """
    Verify PDF OCR task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: OCR PDF exists and has 3 pages (0.15 points)
    try:
        if not os.path.exists(OCR_PDF_PATH):
            print(f"FAIL: Component 1 — OCR PDF not found at {OCR_PDF_PATH}")
            # If the main output file doesn't exist, nothing else can pass
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        doc = fitz.open(OCR_PDF_PATH)
        page_count = len(doc)
        if page_count == 3:
            print(f"PASS: Component 1 — OCR PDF exists with {page_count} pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected 3 pages, found {page_count}")
        doc.close()
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: OCR PDF has text layer on all 3 pages (0.25 points)
    try:
        doc = fitz.open(OCR_PDF_PATH)
        pages_with_text = 0
        for i in range(len(doc)):
            page_text = doc[i].get_text("text").strip()
            if len(page_text) > 20:  # meaningful text, not just whitespace artifacts
                pages_with_text += 1
            else:
                print(f"  INFO: Page {i} text length={len(page_text)} (too short)")
        doc.close()

        if pages_with_text == 3:
            print(f"PASS: Component 2 — All 3 pages have text layer (0.25 pts)")
            total_score += 0.25
        elif pages_with_text > 0:
            partial = round(0.25 * pages_with_text / 3, 2)
            print(f"PARTIAL: Component 2 — {pages_with_text}/3 pages have text ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No pages have extractable text")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: OCR PDF is searchable for "INV-2026-0042" (0.20 points)
    try:
        doc = fitz.open(OCR_PDF_PATH)
        search_hits = sum(len(doc[i].search_for("INV-2026-0042")) for i in range(len(doc)))
        doc.close()

        if search_hits > 0:
            print(f"PASS: Component 3 — 'INV-2026-0042' found via search ({search_hits} hits) (0.20 pts)")
            total_score += 0.20
        else:
            # Fallback: check via text extraction
            doc = fitz.open(OCR_PDF_PATH)
            all_text = "".join(page.get_text("text") for page in doc)
            doc.close()
            if "INV-2026-0042" in all_text:
                print(f"PASS: Component 3 — 'INV-2026-0042' found in extracted text (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — 'INV-2026-0042' not found in OCR PDF")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Text file exists and is non-empty (0.10 points)
    try:
        if not os.path.exists(TEXT_FILE_PATH):
            print(f"FAIL: Component 4 — Text file not found at {TEXT_FILE_PATH}")
        else:
            with open(TEXT_FILE_PATH, 'r', errors='replace') as f:
                text_content = f.read()
            if len(text_content.strip()) > 50:
                print(f"PASS: Component 4 — Text file exists with {len(text_content)} chars (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — Text file too short ({len(text_content.strip())} chars)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Text file has page separators "--- Page N ---" for all 3 pages (0.15 points)
    try:
        if os.path.exists(TEXT_FILE_PATH):
            with open(TEXT_FILE_PATH, 'r', errors='replace') as f:
                text_content = f.read()

            separators_found = 0
            for n in range(1, 4):
                sep = f"--- Page {n} ---"
                if sep in text_content:
                    separators_found += 1
                else:
                    print(f"  INFO: Missing separator '{sep}'")

            if separators_found == 3:
                print(f"PASS: Component 5 — All 3 page separators found (0.15 pts)")
                total_score += 0.15
            elif separators_found > 0:
                partial = round(0.15 * separators_found / 3, 2)
                print(f"PARTIAL: Component 5 — {separators_found}/3 separators ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — No page separators found")
        else:
            print(f"FAIL: Component 5 — Text file not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Text file contains "INV-2026-0042" (0.15 points)
    try:
        if os.path.exists(TEXT_FILE_PATH):
            with open(TEXT_FILE_PATH, 'r', errors='replace') as f:
                text_content = f.read()

            if "INV-2026-0042" in text_content:
                print(f"PASS: Component 6 — Invoice number found in text file (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 6 — 'INV-2026-0042' not found in text file")
        else:
            print(f"FAIL: Component 6 — Text file not found")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
