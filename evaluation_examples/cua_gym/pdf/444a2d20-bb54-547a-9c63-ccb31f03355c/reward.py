"""
Reward Script: Interleave pages from english.pdf and spanish.pdf into bilingual.pdf
Task ID: pdf_ro_026
Domain: pdf
Scoring:
  Component 1 (0.2): bilingual.pdf exists with exactly 20 pages
  Component 2 (0.4): Even-indexed pages (0,2,4,...) contain English content
  Component 3 (0.4): Odd-indexed pages (1,3,5,...) contain Spanish content
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_026'

def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    bilingual_path = os.path.join(WORKDIR, 'Documents', 'bilingual.pdf')
    english_path = os.path.join(WORKDIR, 'Documents', 'english.pdf')
    spanish_path = os.path.join(WORKDIR, 'Documents', 'spanish.pdf')

    # Precondition: source files must exist
    if not os.path.exists(english_path) or not os.path.exists(spanish_path):
        print("CRITICAL: Source PDFs missing")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: bilingual.pdf must exist (not scored - just a gate)
    if not os.path.exists(bilingual_path):
        print("FAIL: bilingual.pdf does not exist")
        print("REWARD: 0.0")
        return 0.0

    try:
        bil_doc = pymupdf.open(bilingual_path)
        eng_doc = pymupdf.open(english_path)
        spa_doc = pymupdf.open(spanish_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDFs: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: bilingual.pdf has exactly 20 pages (0.2 points)
    # This FAILS on initial (no bilingual.pdf) and PASSES on golden
    try:
        page_count = bil_doc.page_count
        if page_count == 20:
            print(f"PASS: Component 1 — bilingual.pdf has {page_count} pages (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — expected 20 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Even-indexed pages (0,2,4,...,18) match English source pages (0.4 points)
    # Check that bilingual page 2*i contains text from english page i
    try:
        eng_matches = 0
        total_eng_checks = 10
        for i in range(10):
            bil_page_idx = 2 * i  # pages 0, 2, 4, ..., 18
            if bil_page_idx >= bil_doc.page_count:
                print(f"  FAIL: bilingual page {bil_page_idx} does not exist")
                continue
            bil_text = bil_doc[bil_page_idx].get_text("text").strip()[:200]
            eng_text = eng_doc[i].get_text("text").strip()[:200]
            if "English Edition" in bil_text and eng_text[:80] in bil_text:
                eng_matches += 1
            else:
                print(f"  FAIL: bilingual page {bil_page_idx} does not match english page {i}")
                print(f"    bilingual text start: {repr(bil_text[:80])}")
                print(f"    english text start:   {repr(eng_text[:80])}")

        if eng_matches == total_eng_checks:
            print(f"PASS: Component 2 — all 10 even-indexed pages match English source (0.4 pts)")
            total_score += 0.4
        elif eng_matches > 0:
            partial = round(0.4 * eng_matches / total_eng_checks, 2)
            print(f"PARTIAL: Component 2 — {eng_matches}/10 English pages match ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — no even-indexed pages match English source")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Odd-indexed pages (1,3,5,...,19) match Spanish source pages (0.4 points)
    # Check that bilingual page 2*i+1 contains text from spanish page i
    try:
        spa_matches = 0
        total_spa_checks = 10
        for i in range(10):
            bil_page_idx = 2 * i + 1  # pages 1, 3, 5, ..., 19
            if bil_page_idx >= bil_doc.page_count:
                print(f"  FAIL: bilingual page {bil_page_idx} does not exist")
                continue
            bil_text = bil_doc[bil_page_idx].get_text("text").strip()[:200]
            spa_text = spa_doc[i].get_text("text").strip()[:200]
            if "Spanish Edition" in bil_text and spa_text[:80] in bil_text:
                spa_matches += 1
            else:
                print(f"  FAIL: bilingual page {bil_page_idx} does not match spanish page {i}")
                print(f"    bilingual text start: {repr(bil_text[:80])}")
                print(f"    spanish text start:   {repr(spa_text[:80])}")

        if spa_matches == total_spa_checks:
            print(f"PASS: Component 3 — all 10 odd-indexed pages match Spanish source (0.4 pts)")
            total_score += 0.4
        elif spa_matches > 0:
            partial = round(0.4 * spa_matches / total_spa_checks, 2)
            print(f"PARTIAL: Component 3 — {spa_matches}/10 Spanish pages match ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — no odd-indexed pages match Spanish source")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    bil_doc.close()
    eng_doc.close()
    spa_doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
