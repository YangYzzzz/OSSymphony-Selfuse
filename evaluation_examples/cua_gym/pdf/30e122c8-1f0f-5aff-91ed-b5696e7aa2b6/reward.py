"""
Reward Script: Set PDF metadata dates using pdftk
Task ID: pdf_mbc_021
Domain: pdf
Scoring:
  Component 1 (0.35): ModDate is 'D:20250101120000+00'
  Component 2 (0.35): CreationDate is 'D:20241215090000+00'
  Component 3 (0.30): Content preserved (page count and text match source)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_021'

# Paths
OUTPUT_PATH = os.path.join(WORKDIR, 'Documents', 'policy_doc_dated.pdf')
SOURCE_PATH = os.path.join(WORKDIR, 'Documents', 'policy_doc.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: output file must exist
    if not os.path.exists(OUTPUT_PATH):
        print(f"CRITICAL: Output file not found: {OUTPUT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Load output PDF metadata using pikepdf (best for docinfo inspection)
    try:
        import pikepdf
        pdf = pikepdf.open(OUTPUT_PATH)
        docinfo = pdf.docinfo
    except Exception as e:
        print(f"CRITICAL: Cannot open output PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: ModDate is 'D:20250101120000+00' (0.35 points)
    try:
        mod_date_raw = str(docinfo.get('/ModDate', ''))
        # Normalize: strip any surrounding whitespace
        mod_date = mod_date_raw.strip()
        expected_mod = 'D:20250101120000+00'
        if expected_mod in mod_date:
            print(f"PASS: Component 1 -- ModDate is correct: {mod_date} (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 -- Expected ModDate containing '{expected_mod}', found: '{mod_date}'")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: CreationDate is 'D:20241215090000+00' (0.35 points)
    try:
        creation_date_raw = str(docinfo.get('/CreationDate', ''))
        creation_date = creation_date_raw.strip()
        expected_creation = 'D:20241215090000+00'
        if expected_creation in creation_date:
            print(f"PASS: Component 2 -- CreationDate is correct: {creation_date} (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 -- Expected CreationDate containing '{expected_creation}', found: '{creation_date}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    pdf.close()

    # Component 3: Content preserved - page count and text match source (0.30 points)
    try:
        import pymupdf
        src_doc = pymupdf.open(SOURCE_PATH)
        out_doc = pymupdf.open(OUTPUT_PATH)

        src_pages = len(src_doc)
        out_pages = len(out_doc)

        # Check page count matches
        pages_match = (src_pages == out_pages)

        # Check text content on all pages matches
        mismatched_page = -1
        for i in range(src_pages):
            src_text = src_doc[i].get_text().strip()
            out_text = out_doc[i].get_text().strip()
            if src_text != out_text:
                mismatched_page = i
                print(f"  Page {i+1} text mismatch: src len={len(src_text)}, out len={len(out_text)}")
                break
        text_match = (mismatched_page == -1)

        src_doc.close()
        out_doc.close()

        if pages_match and text_match:
            print(f"PASS: Component 3 -- Content preserved ({out_pages} pages, text matches) (0.30 pts)")
            total_score += 0.30
        elif pages_match:
            print(f"FAIL: Component 3 -- Page count OK ({out_pages}) but text content differs")
        else:
            print(f"FAIL: Component 3 -- Page count mismatch: source={src_pages}, output={out_pages}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
