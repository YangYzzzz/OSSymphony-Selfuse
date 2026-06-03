"""
Reward Script: Save all Chrome tabs as PDFs to /home/user/Documents/Papers/
Task ID: osworld_multi_apps_bulk_pdf_save_007
Domain: multi_apps (Chrome + OS)
Scoring:
  Component 1: /home/user/Documents/Papers/ directory exists (0.2 pts)
  Component 2: Exactly 3 PDF files exist in the Papers directory (0.3 pts)
  Component 3: All 3 PDF filenames match the expected paper titles (0.3 pts)
  Component 4: All 3 files are valid PDFs (start with %PDF- header) (0.2 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_bulk_pdf_save_007'

PAPERS_DIR = '/home/user/Documents/Papers'

# Expected PDF filenames based on paper titles shown on Chrome tabs
EXPECTED_PDF_NAMES = [
    'Attention Is All You Need.pdf',
    'BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.pdf',
    'An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale.pdf',
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The task requires:
    1. Creating /home/user/Documents/Papers/ directory
    2. Saving 3 Chrome tab pages as PDFs there
    3. Naming each PDF after the paper title
    """
    total_score = 0.0

    # Component 1: Papers directory exists (0.2 points)
    # This directory does NOT exist in initial_env, so it's a task-introduced change
    try:
        if os.path.isdir(PAPERS_DIR):
            print(f"PASS: Component 1 — Papers directory exists at {PAPERS_DIR} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Papers directory does not exist at {PAPERS_DIR}")
            # If directory doesn't exist, no point checking files
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Exactly 3 PDF files exist in the Papers directory (0.3 points)
    # The directory is empty on initial_env, so finding 3 PDFs is a task-introduced change
    try:
        all_files = os.listdir(PAPERS_DIR)
        pdf_files = [f for f in all_files if f.lower().endswith('.pdf')]
        if len(pdf_files) == 3:
            print(f"PASS: Component 2 — Exactly 3 PDF files found in {PAPERS_DIR} (0.3 pts)")
            print(f"  Found: {sorted(pdf_files)}")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected 3 PDF files, found {len(pdf_files)}")
            print(f"  All files: {all_files}")
            print(f"  PDF files: {pdf_files}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: PDF filenames match expected paper titles (0.3 points)
    # Each correct filename earns 0.1 points (3 x 0.1 = 0.3)
    # This verifies the agent used the paper title as the filename
    try:
        actual_files = set(os.listdir(PAPERS_DIR)) if os.path.isdir(PAPERS_DIR) else set()
        matched_count = 0
        for expected_name in EXPECTED_PDF_NAMES:
            if expected_name in actual_files:
                print(f"PASS: Component 3a — Found expected file: '{expected_name}'")
                matched_count += 1
            else:
                print(f"FAIL: Component 3a — Missing expected file: '{expected_name}'")
                # Check for partial match (case-insensitive or without colons)
                normalized_expected = expected_name.lower().replace(':', '').replace('  ', ' ')
                for actual in actual_files:
                    normalized_actual = actual.lower().replace(':', '').replace('  ', ' ')
                    if normalized_expected == normalized_actual:
                        print(f"  NOTE: Found case/punctuation variant: '{actual}'")
                        matched_count += 0.5  # partial credit for near-match
                        break

        if matched_count == len(EXPECTED_PDF_NAMES):
            print(f"PASS: Component 3 — All 3 PDF filenames match expected titles (0.3 pts)")
            total_score += 0.3
        elif matched_count > 0:
            points_earned = round(matched_count / len(EXPECTED_PDF_NAMES) * 0.3, 4)
            print(f"PARTIAL: Component 3 — {matched_count}/{len(EXPECTED_PDF_NAMES)} filenames matched ({points_earned} pts)")
            total_score += points_earned
        else:
            print(f"FAIL: Component 3 — No PDF filenames matched expected titles")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All PDF files are valid PDFs (have %PDF- header) (0.2 points)
    # Verifies the files are real PDFs, not empty files or HTML renamed to .pdf
    try:
        if os.path.isdir(PAPERS_DIR):
            pdf_files_in_dir = [f for f in os.listdir(PAPERS_DIR) if f.lower().endswith('.pdf')]
            if not pdf_files_in_dir:
                print("FAIL: Component 4 — No PDF files to validate")
            else:
                valid_pdfs = 0
                for pdf_file in pdf_files_in_dir:
                    pdf_path = os.path.join(PAPERS_DIR, pdf_file)
                    try:
                        with open(pdf_path, 'rb') as f:
                            header = f.read(5)
                        if header == b'%PDF-':
                            valid_pdfs += 1
                        else:
                            print(f"FAIL: Component 4 — '{pdf_file}' is not a valid PDF (header: {header})")
                    except Exception as e:
                        print(f"ERROR: Component 4 — Cannot read '{pdf_file}': {e}")

                if valid_pdfs == len(pdf_files_in_dir) and valid_pdfs == 3:
                    print(f"PASS: Component 4 — All {valid_pdfs} PDF files have valid %PDF- header (0.2 pts)")
                    total_score += 0.2
                elif valid_pdfs > 0:
                    partial = round(valid_pdfs / 3 * 0.2, 4)
                    print(f"PARTIAL: Component 4 — {valid_pdfs}/3 PDF files are valid ({partial} pts)")
                    total_score += partial
                else:
                    print(f"FAIL: Component 4 — No valid PDF files found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
