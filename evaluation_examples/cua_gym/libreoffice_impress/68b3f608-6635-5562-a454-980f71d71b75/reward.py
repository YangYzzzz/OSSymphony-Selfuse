"""
Reward Script: Export presentation as PDF
Task ID: impress_sales_040
Domain: libreoffice_impress
Scoring:
  Component 1 (0.3): PDF file exists at /home/user/Desktop/CloudSync_Proposal.pdf
  Component 2 (0.3): PDF is a valid PDF file (correct header and structure)
  Component 3 (0.4): PDF contains exactly 10 pages (matching the 10 slides)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'impress_sales_040'
PDF_PATH = os.path.join(WORKDIR, 'Desktop', 'CloudSync_Proposal.pdf')
EXPECTED_PAGES = 10


def count_pdf_pages(file_path):
    """Count pages in a PDF using regex on raw bytes.
    Counts /Type /Page entries (excluding /Type /Pages).
    """
    with open(file_path, 'rb') as f:
        content = f.read()
    # Match /Type followed by optional whitespace then /Page but NOT /Pages
    pages = re.findall(rb'/Type\s*/Page(?!s)', content)
    return len(pages)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: PDF file exists at correct path (0.3 points)
    # This checks that a file named CloudSync_Proposal.pdf is on the Desktop
    try:
        if os.path.isfile(PDF_PATH):
            file_size = os.path.getsize(PDF_PATH)
            if file_size > 0:
                print(f"PASS: Component 1 - PDF exists at {PDF_PATH} (size: {file_size} bytes) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 - PDF exists but is empty (0 bytes)")
        else:
            print(f"FAIL: Component 1 - PDF not found at {PDF_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Gate: if file does not exist, no point checking further
    if total_score == 0.0:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: PDF is a valid PDF file (0.3 points)
    # Check PDF magic header bytes (%PDF-) and EOF marker
    try:
        with open(PDF_PATH, 'rb') as f:
            header = f.read(5)
            f.seek(-32, 2)  # read last 32 bytes for EOF marker
            tail = f.read()

        if header == b'%PDF-':
            if b'%%EOF' in tail:
                print(f"PASS: Component 2 - Valid PDF header and EOF marker (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 - PDF header OK but missing %%EOF marker")
        else:
            print(f"FAIL: Component 2 - Invalid PDF header: {header!r}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: PDF contains exactly 10 pages (0.4 points)
    # The source presentation has 10 slides, so the PDF should have 10 pages
    try:
        page_count = count_pdf_pages(PDF_PATH)
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 3 - PDF has {page_count} pages (expected {EXPECTED_PAGES}) (0.4 pts)")
            total_score += 0.4
        else:
            # Partial credit: if page count > 0 but wrong, give some credit
            if page_count > 0:
                ratio = min(page_count, EXPECTED_PAGES) / max(page_count, EXPECTED_PAGES)
                partial = round(0.4 * ratio, 2)
                print(f"PARTIAL: Component 3 - PDF has {page_count} pages (expected {EXPECTED_PAGES}), partial credit: {partial} pts")
                total_score += partial
            else:
                print(f"FAIL: Component 3 - Could not detect any pages in PDF")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
