"""
Reward Script: Save all open Chrome tabs as PDFs into /home/user/Documents/News-Archive,
               using the article title as each filename.
Task ID: osworld_multi_apps_bulk_pdf_save_004
Domain: multi_apps (Chrome + OS)
Scoring:
  Component 1: News-Archive contains exactly 4 PDF files (0.4 pts)
  Component 2: All 4 PDFs are correctly named after article titles (0.4 pts)
  Component 3: All 4 files are valid PDF format (start with %PDF header) (0.2 pts)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_bulk_pdf_save_004'
NEWS_ARCHIVE_DIR = '/home/user/Documents/News-Archive'

# The expected PDF filenames, derived from the article titles
EXPECTED_PDF_NAMES = {
    'Breakthrough in Quantum Computing Promises Faster Drug Discovery.pdf',
    'Coastal Cities Adapt as Sea Level Rise Accelerates Along US East Seaboard.pdf',
    'Global Climate Summit Reaches Historic Carbon Agreement.pdf',
    'Remote Work Reshapes Urban Real Estate Markets Across North America.pdf',
}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: News-Archive directory must exist
    if not os.path.isdir(NEWS_ARCHIVE_DIR):
        print(f"CRITICAL: News-Archive directory not found: {NEWS_ARCHIVE_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: News-Archive contains exactly 4 PDF files (0.4 points)
    try:
        all_files = os.listdir(NEWS_ARCHIVE_DIR)
        pdf_files = [f for f in all_files if f.lower().endswith('.pdf')]
        pdf_count = len(pdf_files)
        if pdf_count == 4:
            print(f"PASS: Component 1 — News-Archive contains exactly 4 PDF files (0.4 pts)")
            total_score += 0.4
        elif pdf_count > 0:
            print(f"FAIL: Component 1 — Expected 4 PDF files, found {pdf_count}: {pdf_files}")
        else:
            print(f"FAIL: Component 1 — No PDF files found in News-Archive. Contents: {all_files}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 4 PDFs are correctly named after article titles (0.4 points)
    try:
        actual_pdf_names = set(f for f in os.listdir(NEWS_ARCHIVE_DIR) if f.lower().endswith('.pdf'))
        matched = actual_pdf_names & EXPECTED_PDF_NAMES
        missing = EXPECTED_PDF_NAMES - actual_pdf_names
        extra = actual_pdf_names - EXPECTED_PDF_NAMES

        if actual_pdf_names == EXPECTED_PDF_NAMES:
            print(f"PASS: Component 2 — All 4 PDFs correctly named after article titles (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — PDF filenames do not match expected article titles")
            if missing:
                print(f"  Missing: {missing}")
            if extra:
                print(f"  Extra/unexpected: {extra}")
            if matched:
                print(f"  Matched: {len(matched)}/4 titles correct")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 4 files are valid PDF format (start with %PDF header) (0.2 points)
    try:
        pdf_files_in_dir = [f for f in os.listdir(NEWS_ARCHIVE_DIR) if f.lower().endswith('.pdf')]
        if not pdf_files_in_dir:
            print(f"FAIL: Component 3 — No PDF files to validate")
        else:
            valid_pdfs = []
            invalid_pdfs = []
            for fname in pdf_files_in_dir:
                fpath = os.path.join(NEWS_ARCHIVE_DIR, fname)
                try:
                    with open(fpath, 'rb') as pf:
                        header = pf.read(4)
                    if header == b'%PDF':
                        valid_pdfs.append(fname)
                    else:
                        invalid_pdfs.append((fname, header))
                except Exception as fe:
                    invalid_pdfs.append((fname, str(fe)))

            if len(valid_pdfs) == 4 and not invalid_pdfs:
                print(f"PASS: Component 3 — All 4 files are valid PDF format (0.2 pts)")
                total_score += 0.2
            elif valid_pdfs and not invalid_pdfs:
                print(f"FAIL: Component 3 — Only {len(valid_pdfs)} of 4 PDFs are valid format")
            else:
                print(f"FAIL: Component 3 — {len(invalid_pdfs)} file(s) have invalid PDF headers: {invalid_pdfs}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
