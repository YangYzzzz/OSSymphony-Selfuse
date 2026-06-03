"""
Reward Script: Export quarterly_review.odt as PDF preserving base filename and directory
Task ID: osworld_writer_pdf_export_keepname_009
Domain: libreoffice_writer
Scoring:
  Component 1: PDF file exists at /home/user/Reports/quarterly_review.pdf          (0.5 pts)
  Component 2: PDF is a valid PDF with non-trivial content (>1000 bytes, %PDF hdr) (0.3 pts)
  Component 3: PDF base filename matches ODT base filename (quarterly_review)       (0.2 pts)
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_pdf_export_keepname_009'

# Expected paths derived from task description
ODT_PATH = '/home/user/Reports/quarterly_review.odt'
PDF_PATH = '/home/user/Reports/quarterly_review.pdf'
REPORTS_DIR = '/home/user/Reports'


def verify_task():
    """
    Verify that the ODT document was exported as a PDF, preserving the base
    filename and output directory.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: source ODT must exist (not a scoring component)
    if not os.path.exists(ODT_PATH):
        print(f"CRITICAL: Source ODT not found: {ODT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PDF exists at the correct path in the same directory as ODT (0.5 points)
    # This FAILS on initial_env (no PDF) and PASSES on golden_env (PDF created)
    try:
        pdf_exists = os.path.exists(PDF_PATH)
        if pdf_exists:
            print(f"PASS: Component 1 — PDF exists at {PDF_PATH} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — PDF not found at {PDF_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: PDF is a valid PDF format with non-trivial content (0.3 points)
    # Checks that the file starts with %PDF header and is larger than 1000 bytes
    # This FAILS on initial_env (file absent) and PASSES on golden_env (valid PDF)
    try:
        if os.path.exists(PDF_PATH):
            pdf_size = os.path.getsize(PDF_PATH)
            with open(PDF_PATH, 'rb') as f:
                pdf_header = f.read(4)
            is_valid_pdf = pdf_header == b'%PDF'
            is_nontrivial = pdf_size > 1000

            if is_valid_pdf and is_nontrivial:
                print(f"PASS: Component 2 — Valid PDF header found, size={pdf_size} bytes (0.3 pts)")
                total_score += 0.3
            elif not is_valid_pdf:
                print(f"FAIL: Component 2 — File does not start with %PDF header (got: {pdf_header})")
            else:
                print(f"FAIL: Component 2 — PDF size too small ({pdf_size} bytes, expected >1000)")
        else:
            print(f"FAIL: Component 2 — PDF does not exist, cannot verify content")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: PDF base filename matches ODT base filename, ensuring name was preserved (0.2 points)
    # Expected: quarterly_review.pdf (stem == quarterly_review, same as odt stem)
    # This FAILS on initial_env (no PDF) and PASSES on golden_env (correctly named PDF)
    try:
        if os.path.exists(PDF_PATH):
            odt_stem = os.path.splitext(os.path.basename(ODT_PATH))[0]
            pdf_stem = os.path.splitext(os.path.basename(PDF_PATH))[0]
            odt_dir = os.path.dirname(ODT_PATH)
            pdf_dir = os.path.dirname(PDF_PATH)

            name_matches = (odt_stem == pdf_stem)
            dir_matches = (os.path.abspath(odt_dir) == os.path.abspath(pdf_dir))

            if name_matches and dir_matches:
                print(f"PASS: Component 3 — Filename stem '{pdf_stem}' matches ODT stem, "
                      f"directory preserved: {pdf_dir} (0.2 pts)")
                total_score += 0.2
            elif not name_matches:
                print(f"FAIL: Component 3 — PDF stem '{pdf_stem}' != ODT stem '{odt_stem}'")
            else:
                print(f"FAIL: Component 3 — PDF directory '{pdf_dir}' != ODT directory '{odt_dir}'")
        else:
            print(f"FAIL: Component 3 — PDF does not exist, cannot verify filename/directory")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
