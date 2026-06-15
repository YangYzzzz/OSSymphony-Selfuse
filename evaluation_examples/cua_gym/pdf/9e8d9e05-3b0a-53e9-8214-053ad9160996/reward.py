"""
Reward Script: OCR batch processing of 8 scanned PDFs
Task ID: pdf_gf2_047
Domain: pdf
Scoring:
  Component 1: All 8 _searchable.pdf files exist (0.25)
  Component 2: Each searchable PDF has OCR text layer (0.30)
  Component 3: Page counts of searchable PDFs match originals (0.15)
  Component 4: ocr_log.txt exists with 8 lines (0.15)
  Component 5: ocr_log.txt lines contain filename, page count, word count (0.15)
"""

import os
import fitz  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_047'
BATCH_DIR = os.path.join(WORKDIR, 'scans', 'batch')

FILE_STEMS = ['scan_a', 'scan_b', 'scan_c', 'scan_d', 'scan_e', 'scan_f', 'scan_g', 'scan_h']


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: batch directory exists
    if not os.path.isdir(BATCH_DIR):
        print(f"CRITICAL: Batch directory not found: {BATCH_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All 8 _searchable.pdf files exist (0.25 points)
    # Each file contributes 0.25/8 = 0.03125 points
    try:
        searchable_exist_count = 0
        for stem in FILE_STEMS:
            searchable_path = os.path.join(BATCH_DIR, f'{stem}_searchable.pdf')
            if os.path.isfile(searchable_path):
                searchable_exist_count += 1
            else:
                print(f"FAIL: {stem}_searchable.pdf does not exist")

        comp1_score = (searchable_exist_count / 8.0) * 0.25
        total_score += comp1_score
        if searchable_exist_count == 8:
            print(f"PASS: Component 1 — All 8 searchable PDFs exist ({comp1_score:.4f} pts)")
        else:
            print(f"PARTIAL: Component 1 — {searchable_exist_count}/8 searchable PDFs exist ({comp1_score:.4f} pts)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Each searchable PDF has OCR text layer (0.30 points)
    # A searchable PDF must have extractable text (word count > 0)
    # Each file contributes 0.30/8 = 0.0375 points
    try:
        text_layer_count = 0
        for stem in FILE_STEMS:
            searchable_path = os.path.join(BATCH_DIR, f'{stem}_searchable.pdf')
            if not os.path.isfile(searchable_path):
                print(f"FAIL: Component 2 — {stem}_searchable.pdf missing, cannot check text layer")
                continue
            try:
                doc = fitz.open(searchable_path)
                full_text = ''.join(page.get_text() for page in doc)
                word_count = len(full_text.split())
                doc.close()
                if word_count > 0:
                    text_layer_count += 1
                else:
                    print(f"FAIL: Component 2 — {stem}_searchable.pdf has no extractable text (0 words)")
            except Exception as e:
                print(f"ERROR: Component 2 — Could not read {stem}_searchable.pdf: {e}")

        comp2_score = (text_layer_count / 8.0) * 0.30
        total_score += comp2_score
        if text_layer_count == 8:
            print(f"PASS: Component 2 — All 8 searchable PDFs have OCR text layer ({comp2_score:.4f} pts)")
        else:
            print(f"PARTIAL: Component 2 — {text_layer_count}/8 have text layer ({comp2_score:.4f} pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Page counts of searchable PDFs match originals (0.15 points)
    # Each matching file contributes 0.15/8 = 0.01875 points
    try:
        page_match_count = 0
        for stem in FILE_STEMS:
            orig_path = os.path.join(BATCH_DIR, f'{stem}.pdf')
            searchable_path = os.path.join(BATCH_DIR, f'{stem}_searchable.pdf')
            if not os.path.isfile(orig_path) or not os.path.isfile(searchable_path):
                continue
            try:
                orig_doc = fitz.open(orig_path)
                srch_doc = fitz.open(searchable_path)
                orig_pages = orig_doc.page_count
                srch_pages = srch_doc.page_count
                orig_doc.close()
                srch_doc.close()
                if orig_pages == srch_pages:
                    page_match_count += 1
                else:
                    print(f"FAIL: Component 3 — {stem}: orig has {orig_pages} pages, searchable has {srch_pages}")
            except Exception as e:
                print(f"ERROR: Component 3 — Could not compare {stem}: {e}")

        comp3_score = (page_match_count / 8.0) * 0.15
        total_score += comp3_score
        if page_match_count == 8:
            print(f"PASS: Component 3 — All 8 searchable PDFs have matching page counts ({comp3_score:.4f} pts)")
        else:
            print(f"PARTIAL: Component 3 — {page_match_count}/8 page counts match ({comp3_score:.4f} pts)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: ocr_log.txt exists with 8 lines (0.15 points)
    log_path = os.path.join(BATCH_DIR, 'ocr_log.txt')
    log_lines = []
    try:
        if os.path.isfile(log_path):
            with open(log_path, 'r') as f:
                log_lines = [line.strip() for line in f.readlines() if line.strip()]
            if len(log_lines) == 8:
                print(f"PASS: Component 4 — ocr_log.txt exists with 8 non-empty lines (0.1500 pts)")
                total_score += 0.15
            elif len(log_lines) > 0:
                # Partial credit: proportional to lines present (up to 8)
                ratio = min(len(log_lines), 8) / 8.0
                comp4_score = ratio * 0.15
                total_score += comp4_score
                print(f"PARTIAL: Component 4 — ocr_log.txt has {len(log_lines)} lines, expected 8 ({comp4_score:.4f} pts)")
            else:
                print(f"FAIL: Component 4 — ocr_log.txt is empty")
        else:
            print(f"FAIL: Component 4 — ocr_log.txt does not exist")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: ocr_log.txt content correctness (0.15 points)
    # Each line should reference a filename, page count, and word count
    # We check that each line mentions one of the scan files and contains at least 2 numbers
    try:
        if len(log_lines) > 0:
            valid_lines = 0
            for line in log_lines:
                # Check: line references one of the 8 scan files
                has_filename = False
                for stem in FILE_STEMS:
                    if stem in line or f'{stem}.pdf' in line:
                        has_filename = True
                        break
                # Check: line contains at least 2 numeric values (page count + word count)
                import re
                numbers = re.findall(r'\d+', line)
                has_numbers = len(numbers) >= 2  # at least page count and word count

                if has_filename and has_numbers:
                    valid_lines += 1
                else:
                    print(f"FAIL: Component 5 — log line invalid (filename={has_filename}, numbers={len(numbers)}): {line[:80]}")

            comp5_score = (valid_lines / max(len(log_lines), 8)) * 0.15
            total_score += comp5_score
            if valid_lines >= 8:
                print(f"PASS: Component 5 — All 8 log lines have filename + page/word counts ({comp5_score:.4f} pts)")
            else:
                print(f"PARTIAL: Component 5 — {valid_lines}/{len(log_lines)} valid log lines ({comp5_score:.4f} pts)")
        else:
            print(f"FAIL: Component 5 — No log lines to validate")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
