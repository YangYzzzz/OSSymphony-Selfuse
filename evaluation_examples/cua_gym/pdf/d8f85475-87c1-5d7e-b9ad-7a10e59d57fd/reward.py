"""
Reward Script: Verify check_encryption.py script and encryption_report.csv.
Task ID: pdf_cross_098
Domain: pdf

Task: Write ~/scripts/check_encryption.py that scans all PDF files in
~/Documents/ (recursively) and creates a report ~/Documents/encryption_report.csv
with columns: filepath, encrypted (yes/no), page_count, file_size_kb.
Sort by encrypted status (encrypted first), then by filename. Run it.

Ground truth:
  - ~/scripts/check_encryption.py exists and is a valid Python script
  - ~/Documents/encryption_report.csv exists with correct structure
  - CSV has columns: filepath, encrypted, page_count, file_size_kb
  - All ~25 PDFs are listed with correct encryption status
  - 4 PDFs are marked as encrypted (yes), ~21 as unencrypted (no)
  - Encrypted entries appear before unencrypted entries (sorted by encrypted first)
  - Within each group, entries are sorted by filename

Scoring rubric (total = 1.0):
  Component 1 (0.10): ~/scripts/check_encryption.py exists
  Component 2 (0.10): ~/Documents/encryption_report.csv exists
  Component 3 (0.15): CSV has correct column headers
  Component 4 (0.15): CSV lists >= 20 PDFs (all PDFs found recursively)
  Component 5 (0.15): Correct count of encrypted PDFs (exactly 4 marked yes)
  Component 6 (0.15): Correct encryption status for specific known files
  Component 7 (0.10): Encrypted entries appear first (sorted by encrypted status)
  Component 8 (0.10): Within each group, entries are sorted by filename
"""

import os
import csv
import glob

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

DOCUMENTS_DIR = '/home/user/Documents'
SCRIPTS_DIR = '/home/user/scripts'
SCRIPT_PATH = os.path.join(SCRIPTS_DIR, 'check_encryption.py')
REPORT_PATH = os.path.join(DOCUMENTS_DIR, 'encryption_report.csv')

# Known encrypted PDF basenames (created by initial_setup.py)
KNOWN_ENCRYPTED_BASENAMES = {
    'financial_projections_2024.pdf',
    'merger_proposal.pdf',
    'signed_partnership_agreement.pdf',
    'board_presentation_confidential.pdf',
}

# Known unencrypted PDF basenames (spot check)
KNOWN_UNENCRYPTED_BASENAMES = {
    'annual_report_2023.pdf',
    'service_agreement_2023.pdf',
    'invoice_2023_001.pdf',
    'company_overview.pdf',
    'product_launch_slides.pdf',
}

REQUIRED_COLUMNS = {'filepath', 'encrypted', 'page_count', 'file_size_kb'}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ------------------------------------------------------------------ #
    # Component 1: ~/scripts/check_encryption.py exists (0.10)
    # ------------------------------------------------------------------ #
    try:
        if os.path.exists(SCRIPT_PATH):
            print(f"PASS: Component 1 — {SCRIPT_PATH} exists (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — {SCRIPT_PATH} not found")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # ------------------------------------------------------------------ #
    # Component 2: ~/Documents/encryption_report.csv exists (0.10)
    # ------------------------------------------------------------------ #
    try:
        if os.path.exists(REPORT_PATH):
            print(f"PASS: Component 2 — {REPORT_PATH} exists (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 — {REPORT_PATH} not found")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Read the CSV
    try:
        with open(REPORT_PATH, 'r', newline='') as f:
            reader = csv.DictReader(f)
            report_rows = list(reader)
            actual_columns = set(reader.fieldnames) if reader.fieldnames else set()
    except Exception as e:
        print(f"CRITICAL: Cannot read {REPORT_PATH}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Also check columns from first row keys if fieldnames not captured properly
    if not actual_columns and report_rows:
        actual_columns = set(report_rows[0].keys())

    # ------------------------------------------------------------------ #
    # Component 3: CSV has correct column headers (0.15)
    # ------------------------------------------------------------------ #
    try:
        missing_cols = REQUIRED_COLUMNS - actual_columns
        if not missing_cols:
            print(f"PASS: Component 3 — CSV has all required columns: {sorted(REQUIRED_COLUMNS)} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Missing columns: {sorted(missing_cols)}")
            print(f"  Found columns: {sorted(actual_columns)}")
            # Partial credit if some columns are present
            found_cols = REQUIRED_COLUMNS & actual_columns
            partial = 0.15 * (len(found_cols) / len(REQUIRED_COLUMNS))
            if partial > 0:
                print(f"  PARTIAL: {len(found_cols)}/{len(REQUIRED_COLUMNS)} columns found ({partial:.2f} pts)")
                total_score += partial
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ------------------------------------------------------------------ #
    # Component 4: CSV lists >= 20 PDFs (all PDFs found recursively) (0.15)
    # ------------------------------------------------------------------ #
    try:
        total_pdfs = len(report_rows)
        if total_pdfs >= 20:
            print(f"PASS: Component 4 — CSV lists {total_pdfs} PDFs (>= 20 required) (0.15 pts)")
            total_score += 0.15
        elif total_pdfs >= 15:
            partial = 0.15 * (total_pdfs / 25)
            print(f"PARTIAL: Component 4 — CSV lists {total_pdfs} PDFs (expected >= 20) ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — CSV lists only {total_pdfs} PDFs (expected >= 20)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ------------------------------------------------------------------ #
    # Component 5: Correct count of encrypted PDFs (exactly 4) (0.15)
    # ------------------------------------------------------------------ #
    try:
        enc_rows = [r for r in report_rows if r.get('encrypted', '').strip().lower() == 'yes']
        unenc_rows = [r for r in report_rows if r.get('encrypted', '').strip().lower() == 'no']

        if len(enc_rows) == 4:
            print(f"PASS: Component 5 — Exactly 4 PDFs marked as encrypted (0.15 pts)")
            total_score += 0.15
        else:
            # Partial credit for close answers
            diff = abs(len(enc_rows) - 4)
            if diff <= 1:
                partial = 0.075
                print(f"PARTIAL: Component 5 — Found {len(enc_rows)} encrypted PDFs (expected 4) ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — Found {len(enc_rows)} encrypted PDFs (expected 4)")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # ------------------------------------------------------------------ #
    # Component 6: Correct encryption status for known files (0.15)
    # ------------------------------------------------------------------ #
    try:
        # Build lookup: basename -> encrypted status from report
        basename_to_enc = {}
        for row in report_rows:
            fp = row.get('filepath', '')
            bn = os.path.basename(fp)
            basename_to_enc[bn] = row.get('encrypted', '').strip().lower()

        # Check known encrypted files are marked 'yes'
        enc_hits = 0
        for basename in KNOWN_ENCRYPTED_BASENAMES:
            if basename in basename_to_enc:
                if basename_to_enc[basename] == 'yes':
                    enc_hits += 1
                else:
                    print(f"  FAIL subcheck C6: {basename} should be 'yes', got '{basename_to_enc[basename]}'")
            else:
                print(f"  FAIL subcheck C6: {basename} not found in report")

        # Check known unencrypted files are marked 'no'
        unenc_hits = 0
        for basename in KNOWN_UNENCRYPTED_BASENAMES:
            if basename in basename_to_enc:
                if basename_to_enc[basename] == 'no':
                    unenc_hits += 1
                else:
                    print(f"  FAIL subcheck C6: {basename} should be 'no', got '{basename_to_enc[basename]}'")
            else:
                print(f"  FAIL subcheck C6: {basename} not found in report")

        total_checks = len(KNOWN_ENCRYPTED_BASENAMES) + len(KNOWN_UNENCRYPTED_BASENAMES)
        correct = enc_hits + unenc_hits
        comp6_score = 0.15 * (correct / total_checks)

        if correct == total_checks:
            print(f"PASS: Component 6 — All {total_checks} known files have correct encryption status (0.15 pts)")
        elif correct > 0:
            print(f"PARTIAL: Component 6 — {correct}/{total_checks} known files correct ({comp6_score:.2f} pts)")
        else:
            print(f"FAIL: Component 6 — No known files have correct encryption status (0.00 pts)")
        total_score += comp6_score
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # ------------------------------------------------------------------ #
    # Component 7: Encrypted entries appear first (0.10)
    # ------------------------------------------------------------------ #
    try:
        if not report_rows:
            print("FAIL: Component 7 — Report is empty")
        else:
            # Find the last 'yes' row and the first 'no' row
            last_yes_idx = -1
            first_no_idx = len(report_rows)

            for i, row in enumerate(report_rows):
                enc_val = row.get('encrypted', '').strip().lower()
                if enc_val == 'yes':
                    last_yes_idx = i
                elif enc_val == 'no' and first_no_idx == len(report_rows):
                    first_no_idx = i

            # All 'yes' rows must come before all 'no' rows
            if last_yes_idx < first_no_idx:
                print(f"PASS: Component 7 — Encrypted entries appear before unencrypted entries (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 7 — Encrypted entries not sorted before unencrypted entries")
                print(f"  Last 'yes' at row {last_yes_idx + 1}, first 'no' at row {first_no_idx + 1}")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    # ------------------------------------------------------------------ #
    # Component 8: Within each group, sorted by filename (0.10)
    # ------------------------------------------------------------------ #
    try:
        enc_rows_data = [r for r in report_rows if r.get('encrypted', '').strip().lower() == 'yes']
        unenc_rows_data = [r for r in report_rows if r.get('encrypted', '').strip().lower() == 'no']

        def is_sorted_by_filename(rows):
            """Check if rows are sorted by basename of filepath."""
            filenames = [os.path.basename(r.get('filepath', '')) for r in rows]
            return filenames == sorted(filenames)

        enc_sorted = is_sorted_by_filename(enc_rows_data) if enc_rows_data else True
        unenc_sorted = is_sorted_by_filename(unenc_rows_data) if unenc_rows_data else True

        if enc_sorted and unenc_sorted:
            print(f"PASS: Component 8 — Both groups are sorted by filename (0.10 pts)")
            total_score += 0.10
        elif enc_sorted or unenc_sorted:
            partial = 0.05
            which = "encrypted" if enc_sorted else "unencrypted"
            print(f"PARTIAL: Component 8 — Only {which} group is sorted by filename ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 8 — Neither group is sorted by filename")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint
if __name__ == "__main__":
    verify_task()
