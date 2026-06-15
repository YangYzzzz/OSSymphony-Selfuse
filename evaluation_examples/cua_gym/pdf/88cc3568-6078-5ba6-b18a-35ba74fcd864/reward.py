"""
Reward Script: Create a PDF portfolio with embedded file attachments
Task ID: pdf_gf1_048
Domain: pdf
Scoring:
  Component 1: portfolio.pdf exists and is a valid PDF (0.10)
  Component 2: PDF has at least 1 page (cover page) (0.10)
  Component 3: Exactly 3 embedded file attachments (0.30)
  Component 4: Attachment names match expected files (0.30)
  Component 5: Portfolio file size > sum of source files (0.20)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_048'

PORTFOLIO_PATH = os.path.join(WORKDIR, 'Documents', 'portfolio.pdf')
SOURCE_DIR = os.path.join(WORKDIR, 'Documents', 'files')
EXPECTED_FILES = {'report.pdf', 'data.xlsx', 'readme.txt'}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ---------------------------------------------------------------
    # Component 1: portfolio.pdf exists and is a valid PDF (0.10 pts)
    # ---------------------------------------------------------------
    try:
        if not os.path.isfile(PORTFOLIO_PATH):
            print(f"FAIL: Component 1 -- portfolio.pdf not found at {PORTFOLIO_PATH}")
            print("REWARD: 0.0")
            return 0.0

        # Try opening with pikepdf to validate it's a real PDF
        import pikepdf
        pdf = pikepdf.open(PORTFOLIO_PATH)
        valid_pdf = len(pdf.pages) >= 0  # opened successfully means it's valid
        pdf.close()
        if valid_pdf:
            print(f"PASS: Component 1 -- portfolio.pdf exists and is a valid PDF (0.10 pts)")
            total_score += 0.10
    except Exception as e:
        print(f"FAIL: Component 1 -- cannot open portfolio.pdf as PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ---------------------------------------------------------------
    # Component 2: PDF has at least 1 page (cover page) (0.10 pts)
    # ---------------------------------------------------------------
    try:
        import pikepdf
        pdf = pikepdf.open(PORTFOLIO_PATH)
        page_count = len(pdf.pages)
        pdf.close()
        if page_count >= 1:
            print(f"PASS: Component 2 -- PDF has {page_count} page(s) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 -- PDF has {page_count} pages, expected >= 1")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # ---------------------------------------------------------------
    # Component 3: Exactly 3 embedded file attachments (0.30 pts)
    # ---------------------------------------------------------------
    try:
        import pikepdf
        pdf = pikepdf.open(PORTFOLIO_PATH)
        attachment_names = list(pdf.attachments.keys())
        pdf.close()
        att_count = len(attachment_names)
        if att_count == 3:
            print(f"PASS: Component 3 -- Found exactly 3 attachments: {attachment_names} (0.30 pts)")
            total_score += 0.30
        elif att_count > 0:
            partial = 0.30 * (min(att_count, 3) / 3.0)  # partial credit
            print(f"PARTIAL: Component 3 -- Found {att_count} attachments (expected 3), awarding {partial:.2f} pts")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- No attachments found in portfolio.pdf")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # ---------------------------------------------------------------
    # Component 4: Attachment names match expected files (0.30 pts)
    # Each correct name: 0.10 pts
    # ---------------------------------------------------------------
    try:
        import pikepdf
        pdf = pikepdf.open(PORTFOLIO_PATH)
        attachment_names = set(pdf.attachments.keys())
        pdf.close()

        matched = EXPECTED_FILES & attachment_names
        match_count = len(matched)
        if match_count == 3:
            print(f"PASS: Component 4 -- All 3 expected file names found: {sorted(matched)} (0.30 pts)")
            total_score += 0.30
        elif match_count > 0:
            missing = EXPECTED_FILES - attachment_names
            print(f"PARTIAL: Component 4 -- {match_count}/3 names matched. Missing: {sorted(missing)} ({0.10 * match_count:.2f} pts)")
            total_score += 0.10 * match_count
        else:
            print(f"FAIL: Component 4 -- None of the expected names found. Got: {sorted(attachment_names)}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # ---------------------------------------------------------------
    # Component 5: Portfolio file size > sum of source files (0.20 pts)
    # A real portfolio embeds all source files, so its size should exceed
    # the sum of source file sizes due to PDF overhead.
    # ---------------------------------------------------------------
    try:
        portfolio_size = os.path.getsize(PORTFOLIO_PATH)
        source_sizes = []
        for fname in EXPECTED_FILES:
            fpath = os.path.join(SOURCE_DIR, fname)
            if os.path.isfile(fpath):
                source_sizes.append(os.path.getsize(fpath))

        if len(source_sizes) == 3:
            total_source = sum(source_sizes)
            if portfolio_size > total_source:
                print(f"PASS: Component 5 -- Portfolio size ({portfolio_size}) > sum of sources ({total_source}) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 5 -- Portfolio size ({portfolio_size}) <= sum of sources ({total_source})")
        else:
            # Source files missing -- can't compare; skip this check gracefully
            # Still check if portfolio is reasonably large (> 5000 bytes as a fallback)
            if portfolio_size > 5000:
                print(f"PARTIAL: Component 5 -- Source files missing for comparison, but portfolio is {portfolio_size} bytes (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 -- Source files missing and portfolio is only {portfolio_size} bytes")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
