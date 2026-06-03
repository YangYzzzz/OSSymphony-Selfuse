"""
Reward Script: Merge PDFs using Python script with pymupdf
Task ID: pdf_cross_126
Domain: pdf (cross-domain: VSCode + terminal + PDF)
Scoring:
  Component 1: ~/scripts/merge_pdfs.py exists with try/except error handling (0.35 pts)
  Component 2: ~/Documents/merged_output.pdf exists with correct total page count (16) (0.40 pts)
  Component 3: Pages are in correct order matching merge_list.txt (0.25 pts)
  Total: 1.0
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_cross_126'

SCRIPT_PATH = f'{WORKDIR}/scripts/merge_pdfs.py'
MERGED_PDF_PATH = f'{WORKDIR}/Documents/merged_output.pdf'
MERGE_LIST_PATH = f'{WORKDIR}/Documents/merge_list.txt'

# Expected per-file page counts (from context ground truth)
EXPECTED_FILES = [
    ('/home/user/Documents/intro.pdf', 3),
    ('/home/user/Documents/chapter1.pdf', 4),
    ('/home/user/Documents/chapter2.pdf', 4),
    ('/home/user/Documents/chapter3.pdf', 3),
    ('/home/user/Documents/appendix.pdf', 2),
]
EXPECTED_TOTAL_PAGES = sum(p for _, p in EXPECTED_FILES)  # 16


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Precondition gate: script must exist ---
    if not os.path.exists(SCRIPT_PATH):
        print(f"CRITICAL: merge_pdfs.py not found at {SCRIPT_PATH}")
        print(f"REWARD: 0.0")
        return 0.0

    # --- Component 1: Script has proper error handling for missing files (0.35 pts) ---
    # The task requires try/except for FileNotFoundError (or similar)
    try:
        with open(SCRIPT_PATH, 'r') as f:
            script_content = f.read()

        has_try_except = 'try:' in script_content and 'except' in script_content
        handles_file_error = (
            'FileNotFoundError' in script_content
            or 'not os.path' in script_content
            or 'os.path.isfile' in script_content
            or 'os.path.exists' in script_content
        )
        uses_pymupdf = 'pymupdf' in script_content or 'import fitz' in script_content
        reads_merge_list = 'merge_list' in script_content or 'merge_list.txt' in script_content

        if has_try_except and handles_file_error and uses_pymupdf and reads_merge_list:
            print(f"PASS: Component 1 — merge_pdfs.py has try/except error handling, uses pymupdf, reads merge_list.txt (0.35 pts)")
            total_score += 0.35
        elif has_try_except and uses_pymupdf:
            print(f"PASS (partial): Component 1 — merge_pdfs.py has try/except and uses pymupdf but may be missing some requirements (0.20 pts)")
            total_score += 0.20
        elif uses_pymupdf and reads_merge_list:
            print(f"FAIL: Component 1 — merge_pdfs.py uses pymupdf and reads merge_list.txt but lacks try/except error handling")
        else:
            print(f"FAIL: Component 1 — merge_pdfs.py missing required elements: try/except={has_try_except}, pymupdf={uses_pymupdf}, reads_merge_list={reads_merge_list}")

    except Exception as e:
        print(f"ERROR: Component 1 — Could not read script file: {e}")

    # --- Precondition gate: merged output must exist ---
    if not os.path.exists(MERGED_PDF_PATH):
        print(f"CRITICAL: merged_output.pdf not found at {MERGED_PDF_PATH}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # --- Component 2: merged_output.pdf has the correct total page count (0.40 pts) ---
    try:
        doc = pymupdf.open(MERGED_PDF_PATH)
        actual_pages = doc.page_count
        doc.close()

        if actual_pages == EXPECTED_TOTAL_PAGES:
            print(f"PASS: Component 2 — merged_output.pdf has correct page count: {actual_pages} (expected {EXPECTED_TOTAL_PAGES}) (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 2 — merged_output.pdf has {actual_pages} pages, expected {EXPECTED_TOTAL_PAGES}")

    except Exception as e:
        print(f"ERROR: Component 2 — Could not open merged_output.pdf: {e}")

    # --- Component 3: Pages are in the correct order from merge_list.txt (0.25 pts) ---
    # Verify by checking that text content from each source file appears at the expected
    # cumulative offset in the merged document.
    try:
        import re as _re
        merged = pymupdf.open(MERGED_PDF_PATH)
        if merged.page_count != EXPECTED_TOTAL_PAGES:
            print(f"SKIP: Component 3 — page count mismatch prevents order verification")
            merged.close()
        else:
            mismatches = []
            cumulative_page = 0
            for pdf_path, page_count in EXPECTED_FILES:
                # Get sample text from first page of source file
                try:
                    src = pymupdf.open(pdf_path)
                    src_text = src[0].get_text("text").strip()[:80]
                    src.close()
                except Exception:
                    src_text = None

                # Get text from corresponding page in merged output
                merged_text = merged[cumulative_page].get_text("text").strip()[:80]

                if src_text and merged_text:
                    # Compare first ~80 chars of first page (tolerant comparison)
                    if src_text[:50] not in merged_text and merged_text[:50] not in src_text:
                        # Allow for minor whitespace differences
                        src_norm = _re.sub(r'\s+', ' ', src_text[:50])
                        merged_norm = _re.sub(r'\s+', ' ', merged_text[:50])
                        if src_norm != merged_norm:
                            mismatches.append(os.path.basename(pdf_path))
                            print(f"FAIL: Component 3 — Page {cumulative_page+1}: expected text from {os.path.basename(pdf_path)}, got mismatch")
                            print(f"  Expected start: {repr(src_text[:50])}")
                            print(f"  Merged page: {repr(merged_text[:50])}")

                cumulative_page += page_count

            merged.close()

            if len(mismatches) == 0:
                print(f"PASS: Component 3 — All 5 PDF files appear in correct order in merged output (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — {len(mismatches)} file(s) out of order: {mismatches}")

    except Exception as e:
        print(f"ERROR: Component 3 — Could not verify page order: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
