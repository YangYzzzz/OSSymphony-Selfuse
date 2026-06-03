"""
Reward Script: Save all open Chrome tabs as PDFs to /home/user/Documents/Job-Applications/Postings
Task ID: osworld_multi_apps_bulk_pdf_save_008
Domain: multi_apps (Chrome + OS)
Scoring:
  Component 1: Postings subfolder created (0.2 pts)
  Component 2: Exactly 5 PDF files present in Postings folder (0.3 pts)
  Component 3: All 5 expected job title file names are present (0.3 pts)
  Component 4: All PDF files have valid PDF headers (%PDF-) (0.2 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_bulk_pdf_save_008'
POSTINGS_DIR = '/home/user/Documents/Job-Applications/Postings'

# Expected PDF filenames derived from the 5 job postings in the task context
# (job titles as shown in the Chrome tab titles)
EXPECTED_PDF_FILES = [
    'Data Scientist at Spotify.pdf',
    'DevOps Engineer at Netflix.pdf',
    'Product Manager at Stripe.pdf',
    'Senior Software Engineer at Google.pdf',
    'UX Designer at Airbnb.pdf',
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Postings subfolder is created (0.2 points)
    # This FAILS on initial (no Postings folder) and PASSES on golden (folder exists).
    try:
        if os.path.isdir(POSTINGS_DIR):
            print(f"PASS: Component 1 — Postings folder exists at {POSTINGS_DIR} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Postings folder not found at {POSTINGS_DIR}")
            # Without the folder, all remaining checks are meaningless
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Enumerate PDF files in the Postings folder
    try:
        all_files = os.listdir(POSTINGS_DIR)
        pdf_files = [f for f in all_files if f.lower().endswith('.pdf')]
    except Exception as e:
        print(f"ERROR: Cannot list Postings directory: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Exactly 5 PDF files are saved in the Postings folder (0.3 points)
    # This FAILS on initial (no PDFs at all) and PASSES on golden (5 PDFs present).
    try:
        if len(pdf_files) == 5:
            print(f"PASS: Component 2 — Exactly 5 PDF files found in Postings folder (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected 5 PDF files, found {len(pdf_files)}: {pdf_files}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 5 expected job title filenames are present (0.3 points)
    # This FAILS on initial (no PDFs) and PASSES on golden (all 5 correctly named PDFs).
    try:
        actual_set = set(all_files)
        expected_set = set(EXPECTED_PDF_FILES)
        missing = expected_set - actual_set
        if not missing:
            print(f"PASS: Component 3 — All 5 expected job title PDF files are present (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Missing PDF files: {sorted(missing)}")
            print(f"  Found files: {sorted(actual_set)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All expected PDF files have valid PDF headers (%PDF-) (0.2 points)
    # This FAILS on initial (files don't exist) and PASSES on golden (all are valid PDFs).
    try:
        valid_pdf_count = 0
        invalid_files = []
        for fname in EXPECTED_PDF_FILES:
            fpath = os.path.join(POSTINGS_DIR, fname)
            if not os.path.isfile(fpath):
                invalid_files.append(f"{fname} (not found)")
                continue
            try:
                with open(fpath, 'rb') as fh:
                    header = fh.read(5)
                if header == b'%PDF-':
                    valid_pdf_count += 1
                else:
                    invalid_files.append(f"{fname} (invalid header: {header!r})")
            except Exception as fe:
                invalid_files.append(f"{fname} (read error: {fe})")

        if valid_pdf_count == 5 and not invalid_files:
            print(f"PASS: Component 4 — All 5 PDF files have valid %PDF- headers (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — {valid_pdf_count}/5 files have valid PDF headers")
            if invalid_files:
                for inv in invalid_files:
                    print(f"  Invalid: {inv}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
