"""
Reward Script: Split newsletter.pdf into individual articles based on bookmarks
Task ID: pdf_gf2_044
Domain: pdf
Scoring:
  Component 1 (0.20) - All 4 expected PDF files exist in output directory
  Component 2 (0.30) - Each file has exactly 3 pages
  Component 3 (0.40) - Text content of each section matches corresponding pages from original
  Component 4 (0.10) - No unexpected extra files in output directory
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_044'

SECTION_DIR = os.path.join(WORKDIR, 'Documents', 'newsletter_sections')
ORIGINAL_PDF = os.path.join(WORKDIR, 'Documents', 'newsletter.pdf')

# Expected files and their page ranges (0-indexed) from the original PDF
EXPECTED_SECTIONS = {
    'Cover Story.pdf':     (0, 3),   # pages 1-3 -> indices 0,1,2
    'Tech Review.pdf':     (3, 6),   # pages 4-6 -> indices 3,4,5
    'Community News.pdf':  (6, 9),   # pages 7-9 -> indices 6,7,8
    'Classifieds.pdf':     (9, 12),  # pages 10-12 -> indices 9,10,11
}


def normalize_text(text):
    """Normalize text for comparison: collapse whitespace, strip, lowercase."""
    import re
    return re.sub(r'\s+', ' ', text).strip().lower()


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: section directory must exist
    if not os.path.isdir(SECTION_DIR):
        print(f"CRITICAL: Output directory not found: {SECTION_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Load original PDF text for content comparison later
    try:
        orig_doc = pymupdf.open(ORIGINAL_PDF)
        orig_page_texts = []
        for i in range(orig_doc.page_count):
            orig_page_texts.append(orig_doc[i].get_text('text'))
        orig_doc.close()
    except Exception as e:
        print(f"CRITICAL: Cannot load original PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All 4 expected PDF files exist (0.20 points)
    try:
        existing_files = []
        for fname in EXPECTED_SECTIONS:
            fpath = os.path.join(SECTION_DIR, fname)
            if os.path.isfile(fpath):
                existing_files.append(fname)
            else:
                print(f"FAIL: Component 1 — Missing file: {fname}")

        files_found = len(existing_files)
        if files_found == 4:
            print(f"PASS: Component 1 — All 4 expected files exist (0.20 pts)")
            total_score += 0.20
        elif files_found > 0:
            partial = round(0.20 * files_found / 4, 2)
            print(f"PARTIAL: Component 1 — {files_found}/4 files found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No expected files found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Each file has exactly 3 pages (0.30 points)
    try:
        correct_page_counts = 0
        for fname in EXPECTED_SECTIONS:
            fpath = os.path.join(SECTION_DIR, fname)
            if not os.path.isfile(fpath):
                print(f"FAIL: Component 2 — {fname} missing, cannot check page count")
                continue
            try:
                doc = pymupdf.open(fpath)
                pc = doc.page_count
                doc.close()
                if pc == 3:
                    correct_page_counts += 1
                    print(f"PASS: Component 2 — {fname} has 3 pages")
                else:
                    print(f"FAIL: Component 2 — {fname} has {pc} pages, expected 3")
            except Exception as e:
                print(f"ERROR: Component 2 — Cannot open {fname}: {e}")

        if correct_page_counts == 4:
            print(f"PASS: Component 2 — All 4 files have correct page count (0.30 pts)")
            total_score += 0.30
        elif correct_page_counts > 0:
            partial = round(0.30 * correct_page_counts / 4, 2)
            print(f"PARTIAL: Component 2 — {correct_page_counts}/4 correct page counts ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No files have correct page count")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Text content matches corresponding original pages (0.40 points)
    try:
        content_matches = 0
        for fname, (start_idx, end_idx) in EXPECTED_SECTIONS.items():
            fpath = os.path.join(SECTION_DIR, fname)
            if not os.path.isfile(fpath):
                print(f"FAIL: Component 3 — {fname} missing, cannot check content")
                continue
            try:
                doc = pymupdf.open(fpath)
                pages_matched = 0
                pages_checked = min(doc.page_count, end_idx - start_idx)
                # Check each page's text matches the corresponding original page
                for page_i in range(pages_checked):
                    orig_idx = start_idx + page_i
                    if orig_idx >= len(orig_page_texts):
                        break
                    section_text = normalize_text(doc[page_i].get_text('text'))
                    original_text = normalize_text(orig_page_texts[orig_idx])

                    # Check substantial overlap: the section page should contain
                    # a significant portion of the original page text
                    if len(original_text) == 0 and len(section_text) == 0:
                        pages_matched += 1
                        continue
                    if len(original_text) == 0:
                        break

                    # Word overlap check: at least 70% of original words in section
                    orig_words = set(original_text.split())
                    sect_words = set(section_text.split())
                    if len(orig_words) == 0:
                        pages_matched += 1
                        continue
                    overlap = len(orig_words & sect_words) / len(orig_words)
                    if overlap >= 0.7:
                        pages_matched += 1
                    else:
                        print(f"FAIL: Component 3 — {fname} page {page_i+1} content mismatch (overlap: {overlap:.2f})")
                doc.close()

                if pages_matched == pages_checked and pages_checked > 0:
                    content_matches += 1
                    print(f"PASS: Component 3 — {fname} content matches original pages {start_idx+1}-{end_idx}")
            except Exception as e:
                print(f"ERROR: Component 3 — Cannot verify {fname}: {e}")

        if content_matches == 4:
            print(f"PASS: Component 3 — All 4 sections have correct content (0.40 pts)")
            total_score += 0.40
        elif content_matches > 0:
            partial = round(0.40 * content_matches / 4, 2)
            print(f"PARTIAL: Component 3 — {content_matches}/4 sections match ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No sections have matching content")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Exactly 4 files in output directory and no extras (0.10 points)
    # This component only scores if at least one expected file exists (task-introduced change)
    try:
        all_files = [f for f in os.listdir(SECTION_DIR) if os.path.isfile(os.path.join(SECTION_DIR, f))]
        expected_names = set(EXPECTED_SECTIONS.keys())
        extra_files = [f for f in all_files if f not in expected_names]

        if files_found == 4 and len(extra_files) == 0 and len(all_files) == 4:
            print(f"PASS: Component 4 — Exactly 4 expected files, no extras (0.10 pts)")
            total_score += 0.10
        elif files_found == 0:
            print(f"FAIL: Component 4 — No expected files exist yet")
        elif len(extra_files) > 0:
            print(f"FAIL: Component 4 — Unexpected files found: {extra_files}")
        else:
            print(f"FAIL: Component 4 — Not all 4 expected files present ({files_found}/4)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.isdir(SECTION_DIR):
    print(f"Output directory not found: {SECTION_DIR}")
    print("REWARD: 0.0")
else:
    verify_task()
