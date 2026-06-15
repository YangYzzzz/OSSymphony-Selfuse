"""
Reward Script: Download each open Chrome tab as PDF and save to Finance/Research directory
Task ID: osworld_multi_apps_bulk_pdf_save_003
Domain: multi_apps (Chrome + OS filesystem)

Scoring Rubric:
  Component 1: At least one valid PDF file exists in the Research directory (0.3 pts)
  Component 2: Exactly 3 PDF files are present in the Research directory (0.4 pts)
  Component 3: All 3 PDFs have filenames matching the expected page titles (0.3 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_bulk_pdf_save_003'

# Expected PDF filenames (based on task context: page titles of the 3 financial articles)
EXPECTED_PDF_NAMES = [
    "Understanding Bond Yields and Market Volatility.pdf",
    "Warren Buffett's Top Investment Principles for 2025.pdf",
    "Diversification Strategies for Long-Term Wealth Building.pdf",
]

TARGET_DIR = '/home/user/Documents/Finance/Research'


def is_valid_pdf(file_path: str) -> bool:
    """Check if file has a valid PDF header (%PDF)."""
    try:
        with open(file_path, 'rb') as f:
            header = f.read(4)
        return header == b'%PDF'
    except Exception:
        return False


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: target directory must exist
    if not os.path.isdir(TARGET_DIR):
        print(f"FAIL: Target directory does not exist: {TARGET_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Get list of PDF files in the target directory
    try:
        all_files = os.listdir(TARGET_DIR)
        pdf_files = [f for f in all_files if f.endswith('.pdf')]
    except Exception as e:
        print(f"CRITICAL: Cannot list directory {TARGET_DIR}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: At least one valid PDF file exists in Research directory (0.3 points)
    # This FAILS on initial_env (empty dir) and PASSES on golden_env (3 PDFs present)
    try:
        valid_pdfs = [f for f in pdf_files if is_valid_pdf(os.path.join(TARGET_DIR, f))]
        if len(valid_pdfs) >= 1:
            print(f"PASS: Component 1 — At least one valid PDF found: {valid_pdfs[0]} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No valid PDF files found in {TARGET_DIR} (found {len(all_files)} total files)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Exactly 3 PDF files present in Research directory (0.4 points)
    # This FAILS on initial_env (0 files) and PASSES on golden_env (3 PDFs)
    try:
        if len(pdf_files) == 3:
            print(f"PASS: Component 2 — Exactly 3 PDF files found in {TARGET_DIR} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — Expected 3 PDF files, found {len(pdf_files)}: {pdf_files}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 3 PDFs have filenames matching the expected page titles (0.3 points)
    # This FAILS on initial_env (no files) and PASSES on golden_env (correctly named files)
    try:
        pdf_file_set = set(pdf_files)
        expected_set = set(EXPECTED_PDF_NAMES)
        matching = pdf_file_set & expected_set
        if len(matching) == len(expected_set):
            print(f"PASS: Component 3 — All 3 PDF filenames match expected page titles (0.3 pts)")
            total_score += 0.3
        else:
            missing = expected_set - pdf_file_set
            unexpected = pdf_file_set - expected_set
            print(f"FAIL: Component 3 — PDF filename mismatch.")
            if missing:
                print(f"  Missing expected: {missing}")
            if unexpected:
                print(f"  Unexpected extra: {unexpected}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
