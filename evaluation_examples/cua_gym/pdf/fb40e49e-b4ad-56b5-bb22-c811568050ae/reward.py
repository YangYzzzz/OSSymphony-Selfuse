"""
Reward Script: Repair corrupted PDF using pikepdf recovery mode
Task ID: pdf_fm_094
Domain: pdf
Scoring:
  Component 1 (0.25): repaired_report.pdf opens cleanly with pymupdf (no errors)
  Component 2 (0.25): repaired_report.pdf opens cleanly with pikepdf
  Component 3 (0.25): Correct page count (5 pages) and all pages have text content
  Component 4 (0.25): Key content preserved (title, section headers from original)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_094'
REPAIRED_PATH = os.path.join(WORKDIR, 'Documents', 'repaired_report.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist (gate, not scored)
    if not os.path.exists(file_path):
        print(f"CRITICAL: repaired_report.pdf not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: repaired_report.pdf opens cleanly with pymupdf (0.25 points)
    # This checks that the file is a valid, non-corrupted PDF that pymupdf can parse.
    # On initial_env, repaired_report.pdf does not exist so this is gated by the precondition.
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
        page_count = doc.page_count
        if page_count > 0:
            # Try reading text from first page to confirm it's a real PDF
            first_page_text = doc[0].get_text()
            if len(first_page_text) > 10:
                print(f"PASS: Component 1 - File opens with pymupdf, {page_count} pages, "
                      f"first page has {len(first_page_text)} chars (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 - File opens but first page has insufficient text: "
                      f"{len(first_page_text)} chars")
        else:
            print(f"FAIL: Component 1 - File opens but has 0 pages")
        doc.close()
    except Exception as e:
        print(f"ERROR: Component 1 - Cannot open with pymupdf: {e}")

    # Component 2: repaired_report.pdf opens cleanly with pikepdf (0.25 points)
    # The task specifically asks to use pikepdf for repair, so the output should be
    # pikepdf-compatible with no structural issues.
    try:
        import pikepdf
        pdf = pikepdf.open(file_path)
        num_pages = len(pdf.pages)
        if num_pages > 0:
            # Verify basic structure - each page should have a valid mediabox
            valid_pages = 0
            for page in pdf.pages:
                if hasattr(page, 'mediabox') or '/MediaBox' in page:
                    valid_pages += 1
            pdf.close()
            if valid_pages == num_pages:
                print(f"PASS: Component 2 - File opens with pikepdf, {num_pages} pages, "
                      f"all pages have valid MediaBox (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 - Only {valid_pages}/{num_pages} pages have valid MediaBox")
        else:
            print(f"FAIL: Component 2 - pikepdf reports 0 pages")
            pdf.close()
    except Exception as e:
        print(f"ERROR: Component 2 - Cannot open with pikepdf: {e}")

    # Component 3: Correct page count (5 pages) and all pages have text (0.25 points)
    # The original damaged_report.pdf had 5 pages. The repaired version must preserve all 5.
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
        pc = doc.page_count
        pages_with_text = 0
        for i in range(pc):
            text = doc[i].get_text().strip()
            if len(text) > 20:
                pages_with_text += 1
        doc.close()

        if pc == 5 and pages_with_text == 5:
            print(f"PASS: Component 3 - Correct page count (5) and all 5 pages have "
                  f"substantial text (0.25 pts)")
            total_score += 0.25
        elif pc == 5 and pages_with_text >= 3:
            partial = 0.15
            print(f"PARTIAL: Component 3 - Correct page count (5) but only {pages_with_text}/5 "
                  f"pages have text ({partial} pts)")
            total_score += partial
        elif pc == 5:
            partial = 0.10
            print(f"PARTIAL: Component 3 - Correct page count (5) but only {pages_with_text}/5 "
                  f"pages have text ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 - Expected 5 pages, found {pc}; "
                  f"{pages_with_text} pages with text")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Key content preserved from original document (0.25 points)
    # The repaired file should contain the original report content: title, author, sections.
    try:
        import pymupdf
        doc = pymupdf.open(file_path)
        all_text = ""
        for i in range(doc.page_count):
            all_text += doc[i].get_text()
        doc.close()

        # Check for key content markers from the original document
        key_markers = [
            "Q4 2025 Performance Report",
            "Elena Vasquez",
            "Revenue Overview",
            "Client Acquisition",
            "Project Delivery",
        ]

        found = 0
        for marker in key_markers:
            if marker in all_text:
                found += 1
            else:
                print(f"  MISS: Key marker not found: '{marker}'")

        if found == len(key_markers):
            print(f"PASS: Component 4 - All {len(key_markers)} key content markers preserved "
                  f"(0.25 pts)")
            total_score += 0.25
        elif found >= 3:
            partial = round(0.25 * found / len(key_markers), 2)
            print(f"PARTIAL: Component 4 - {found}/{len(key_markers)} key markers found "
                  f"({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 - Only {found}/{len(key_markers)} key markers found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(REPAIRED_PATH):
    print(f"File not found: {REPAIRED_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(REPAIRED_PATH)
