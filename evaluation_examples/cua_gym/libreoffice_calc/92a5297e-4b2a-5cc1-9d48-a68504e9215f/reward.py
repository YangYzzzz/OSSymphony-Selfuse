"""
Reward Script: Save all open Chrome tabs as PDFs to /home/user/Documents/Legal-Docs
Task ID: osworld_multi_apps_bulk_pdf_save_006
Domain: multi_apps (Chrome + OS)

Task: Save each open Chrome tab (showing legal documents) to /home/user/Documents/Legal-Docs
      using the page title as the filename. 4 tabs expected, each must be saved as a PDF.

Expected PDF files in /home/user/Documents/Legal-Docs:
  - Employment Contract Template.pdf
  - Non-Disclosure Agreement Template.pdf
  - Privacy Policy Template.pdf
  - Service Level Agreement.pdf

Scoring Rubric:
  Component 1: Exactly 4 PDF files saved in Legal-Docs directory (0.4 pts)
  Component 2: All 4 expected filenames (matching page titles) are present (0.4 pts)
  Component 3: All 4 expected files have valid PDF content (0.2 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_bulk_pdf_save_006'
LEGAL_DOCS_DIR = '/home/user/Documents/Legal-Docs'

# Expected PDF filenames (based on Chrome tab page titles from task context)
EXPECTED_FILES = [
    'Employment Contract Template.pdf',
    'Non-Disclosure Agreement Template.pdf',
    'Privacy Policy Template.pdf',
    'Service Level Agreement.pdf',
]


def verify_task():
    """
    Verify that 4 PDF files matching the page titles have been saved to
    /home/user/Documents/Legal-Docs.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: directory must exist
    if not os.path.isdir(LEGAL_DOCS_DIR):
        print(f"CRITICAL: Directory not found: {LEGAL_DOCS_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # List actual files in Legal-Docs
    try:
        actual_files = os.listdir(LEGAL_DOCS_DIR)
        pdf_files = [f for f in actual_files if f.lower().endswith('.pdf')]
        print(f"INFO: Found {len(pdf_files)} PDF file(s) in {LEGAL_DOCS_DIR}: {sorted(pdf_files)}")
    except Exception as e:
        print(f"CRITICAL: Cannot list directory {LEGAL_DOCS_DIR}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Exactly 4 PDF files exist in Legal-Docs (0.4 points)
    # This FAILS on initial_env (0 PDFs) and PASSES on golden_env (4 PDFs)
    try:
        if len(pdf_files) == 4:
            print(f"PASS: Component 1 — Exactly 4 PDF files found in Legal-Docs (0.4 pts)")
            total_score += 0.4
        elif len(pdf_files) > 0:
            # Partial credit: some files saved but not all 4
            partial = round((len(pdf_files) / 4) * 0.4, 2)
            print(f"PARTIAL: Component 1 — Found {len(pdf_files)}/4 PDF files ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No PDF files found in Legal-Docs (expected 4)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 4 expected filenames present (matching page titles) (0.4 points)
    # This FAILS on initial_env (no files) and PASSES on golden_env (all 4 present)
    try:
        found_expected = []
        missing_expected = []
        for expected_name in EXPECTED_FILES:
            if expected_name in actual_files:
                found_expected.append(expected_name)
            else:
                missing_expected.append(expected_name)

        if len(found_expected) == len(EXPECTED_FILES):
            print(f"PASS: Component 2 — All 4 expected filenames present (0.4 pts)")
            total_score += 0.4
        elif len(found_expected) > 0:
            partial = round((len(found_expected) / len(EXPECTED_FILES)) * 0.4, 2)
            print(f"PARTIAL: Component 2 — {len(found_expected)}/{len(EXPECTED_FILES)} expected "
                  f"filenames found ({partial} pts): {found_expected}")
            print(f"  Missing: {missing_expected}")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No expected filenames found in Legal-Docs")
            print(f"  Expected: {EXPECTED_FILES}")
            print(f"  Actual:   {sorted(actual_files)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All expected files have valid PDF content (proper %PDF header) (0.2 points)
    # This FAILS on initial_env (no files) and PASSES on golden_env (valid PDFs)
    try:
        valid_pdf_count = 0
        invalid_pdfs = []
        for expected_name in EXPECTED_FILES:
            fpath = os.path.join(LEGAL_DOCS_DIR, expected_name)
            if os.path.isfile(fpath):
                with open(fpath, 'rb') as fp:
                    header = fp.read(4)
                if header == b'%PDF':
                    valid_pdf_count += 1
                else:
                    invalid_pdfs.append(f"{expected_name} (bad header: {header})")

        if valid_pdf_count == len(EXPECTED_FILES) and not invalid_pdfs:
            print(f"PASS: Component 3 — All 4 files have valid PDF headers (0.2 pts)")
            total_score += 0.2
        elif valid_pdf_count > 0:
            partial = round((valid_pdf_count / len(EXPECTED_FILES)) * 0.2, 2)
            print(f"PARTIAL: Component 3 — {valid_pdf_count}/{len(EXPECTED_FILES)} files have "
                  f"valid PDF headers ({partial} pts)")
            if invalid_pdfs:
                print(f"  Invalid: {invalid_pdfs}")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No valid PDF files found (0 with %PDF header)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: verify the task
if not os.path.isdir(LEGAL_DOCS_DIR):
    print(f"Directory not found: {LEGAL_DOCS_DIR}")
    print("REWARD: 0.0")
else:
    verify_task()
