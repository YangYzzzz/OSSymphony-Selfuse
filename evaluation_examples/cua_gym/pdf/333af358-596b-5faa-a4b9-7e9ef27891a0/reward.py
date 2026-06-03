"""
Reward Script: Add a table of authorities to an appellate brief PDF
Task ID: pdf_legal_084
Domain: pdf
Scoring:
  - Component 1 (0.20): Output file exists and has 26 pages
  - Component 2 (0.15): Page 1 contains "TABLE OF AUTHORITIES" heading
  - Component 3 (0.20): Smith v. Jones citation with page refs pp. 5, 8, 12
  - Component 4 (0.20): Brown v. Board citation with page refs pp. 7, 15
  - Component 5 (0.20): Miranda v. Arizona citation with page refs pp. 9, 11, 18
  - Component 6 (0.05): Original brief content preserved on page 2
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_084'

# Paths
OUTPUT_FILE = os.path.join(WORKDIR, 'legal', 'appellate', 'brief_with_toa.pdf')
ORIGINAL_FILE = os.path.join(WORKDIR, 'legal', 'appellate', 'brief.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: output file must exist
    if not os.path.exists(OUTPUT_FILE):
        print(f"CRITICAL: Output file not found: {OUTPUT_FILE}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("CRITICAL: PyMuPDF (fitz) not available")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = fitz.open(OUTPUT_FILE)
    except Exception as e:
        print(f"CRITICAL: Cannot open output PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File has 26 pages (0.20 points)
    # Initial brief has 25 pages; adding TOA page should make 26
    try:
        page_count = doc.page_count
        if page_count == 26:
            print(f"PASS: Component 1 — Page count is 26 (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Expected 26 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Get page 1 text (index 0) for citation checks
    try:
        page0_text = doc[0].get_text()
    except Exception as e:
        print(f"ERROR: Cannot read page 0 text: {e}")
        page0_text = ""

    # Component 2: Page 1 contains "TABLE OF AUTHORITIES" heading (0.15 points)
    try:
        if re.search(r'TABLE\s+OF\s+AUTHORITIES', page0_text, re.IGNORECASE):
            print(f"PASS: Component 2 — 'TABLE OF AUTHORITIES' heading found on page 1 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — 'TABLE OF AUTHORITIES' heading not found on page 1")
            print(f"  Page 1 text preview: {page0_text[:200]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Smith v. Jones citation with page refs (0.20 points)
    try:
        has_citation = bool(re.search(r'Smith\s+v\.\s+Jones', page0_text, re.IGNORECASE))
        has_reporter = bool(re.search(r'123\s+F\.3d\s+456', page0_text))
        has_pages = bool(re.search(r'pp?\.\s*5.*8.*12', page0_text))
        if has_citation and has_reporter and has_pages:
            print(f"PASS: Component 3 — Smith v. Jones citation complete with page refs (0.20 pts)")
            total_score += 0.20
        elif has_citation and has_reporter:
            print(f"PARTIAL: Component 3 — Smith v. Jones citation found but page refs incomplete (0.10 pts)")
            total_score += 0.10
        elif has_citation:
            print(f"PARTIAL: Component 3 — Smith v. Jones name found but citation details missing (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 3 — Smith v. Jones citation not found on page 1")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Brown v. Board citation with page refs (0.20 points)
    try:
        has_citation = bool(re.search(r'Brown\s+v\.\s+Board', page0_text, re.IGNORECASE))
        has_reporter = bool(re.search(r'347\s+U\.S\.\s+483', page0_text))
        has_pages = bool(re.search(r'pp?\.\s*7.*15', page0_text))
        if has_citation and has_reporter and has_pages:
            print(f"PASS: Component 4 — Brown v. Board citation complete with page refs (0.20 pts)")
            total_score += 0.20
        elif has_citation and has_reporter:
            print(f"PARTIAL: Component 4 — Brown v. Board citation found but page refs incomplete (0.10 pts)")
            total_score += 0.10
        elif has_citation:
            print(f"PARTIAL: Component 4 — Brown v. Board name found but citation details missing (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 4 — Brown v. Board citation not found on page 1")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Miranda v. Arizona citation with page refs (0.20 points)
    try:
        has_citation = bool(re.search(r'Miranda\s+v\.\s+Arizona', page0_text, re.IGNORECASE))
        has_reporter = bool(re.search(r'384\s+U\.S\.\s+436', page0_text))
        has_pages = bool(re.search(r'pp?\.\s*9.*11.*18', page0_text))
        if has_citation and has_reporter and has_pages:
            print(f"PASS: Component 5 — Miranda v. Arizona citation complete with page refs (0.20 pts)")
            total_score += 0.20
        elif has_citation and has_reporter:
            print(f"PARTIAL: Component 5 — Miranda v. Arizona citation found but page refs incomplete (0.10 pts)")
            total_score += 0.10
        elif has_citation:
            print(f"PARTIAL: Component 5 — Miranda v. Arizona name found but citation details missing (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 5 — Miranda v. Arizona citation not found on page 1")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Original brief content preserved on page 2 (0.05 points)
    # The original brief's first page should now be page 2 (index 1)
    try:
        page1_text = doc[1].get_text()
        # Check for distinctive text from the original brief's first page
        if 'UNITED STATES COURT OF APPEALS' in page1_text and 'NINTH CIRCUIT' in page1_text:
            print(f"PASS: Component 6 — Original brief content preserved on page 2 (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 6 — Original brief content not found on page 2")
            print(f"  Page 2 text preview: {page1_text[:200]}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_FILE):
    print(f"File not found: {OUTPUT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task()
