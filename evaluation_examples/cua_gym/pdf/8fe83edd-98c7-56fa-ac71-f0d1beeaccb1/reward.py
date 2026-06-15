"""
Reward Script: Certificate PDF creation verification
Task ID: pdf_gf3_009
Domain: pdf
Scoring:
  - Component 1: File exists and is valid PDF (0.1)
  - Component 2: Landscape orientation (0.1)
  - Component 3: Title 'Certificate of Completion' present (0.2)
  - Component 4: Recipient 'Jane Smith' present (0.15)
  - Component 5: Course 'Advanced Python Programming' and date '2024-03-15' present (0.15)
  - Component 6: Decorative border (drawings/rectangles) present (0.15)
  - Component 7: Two signature lines with 'Instructor' and 'Director' labels (0.15)
"""

import os

WORKDIR = '/home/user/documents'
TASK_ID = 'pdf_gf3_009'
FILE_PATH = os.path.join(WORKDIR, 'certificate.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(FILE_PATH):
        print(f"CRITICAL: File not found: {FILE_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must be loadable as PDF
    try:
        import pymupdf
        doc = pymupdf.open(FILE_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {FILE_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if doc.page_count < 1:
        print("CRITICAL: PDF has no pages")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    page = doc[0]
    text = page.get_text().lower()
    text_original = page.get_text()

    # Component 1: File is a valid PDF with content (0.1 points)
    # This checks that the PDF is not just an empty file but actually has text content
    try:
        if len(text.strip()) > 20:
            print(f"PASS: Component 1 — Valid PDF with text content ({len(text.strip())} chars) (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — PDF has insufficient text content ({len(text.strip())} chars)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Landscape orientation (width > height) (0.1 points)
    try:
        w = page.rect.width
        h = page.rect.height
        if w > h:
            print(f"PASS: Component 2 — Landscape orientation (width={w:.1f} > height={h:.1f}) (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 2 — Not landscape (width={w:.1f}, height={h:.1f})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Title 'Certificate of Completion' present (0.2 points)
    try:
        if 'certificate of completion' in text:
            print(f"PASS: Component 3 — Title 'Certificate of Completion' found (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Title 'Certificate of Completion' not found in text")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Recipient name 'Jane Smith' present (0.15 points)
    try:
        if 'jane smith' in text:
            print(f"PASS: Component 4 — Recipient 'Jane Smith' found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — Recipient 'Jane Smith' not found in text")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Course name and date present (0.15 points)
    try:
        course_found = 'advanced python programming' in text
        date_found = '2024-03-15' in text or 'march 15, 2024' in text or '03/15/2024' in text or '15 march 2024' in text or '2024-03-15' in text_original
        if course_found and date_found:
            print(f"PASS: Component 5 — Course name and date found (0.15 pts)")
            total_score += 0.15
        elif course_found:
            print(f"PARTIAL: Component 5 — Course found but date missing (0.075 pts)")
            total_score += 0.075
        elif date_found:
            print(f"PARTIAL: Component 5 — Date found but course name missing (0.075 pts)")
            total_score += 0.075
        else:
            print(f"FAIL: Component 5 — Neither course name nor date found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Decorative border (rectangles in drawings) (0.15 points)
    try:
        drawings = page.get_drawings()
        # Look for rectangle-like drawings that span a significant portion of the page
        border_rects = []
        page_w = page.rect.width
        page_h = page.rect.height
        for d in drawings:
            rect = d.get('rect')
            if rect is not None:
                rw = rect.width
                rh = rect.height
                # A border rectangle should be large relative to page size
                if rw > page_w * 0.7 and rh > page_h * 0.7:
                    border_rects.append(rect)
        if len(border_rects) >= 1:
            print(f"PASS: Component 6 — Decorative border found ({len(border_rects)} large rect(s)) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 — No decorative border rectangles found (found {len(drawings)} drawings total, but none large enough)")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: Two signature lines with 'Instructor' and 'Director' labels (0.15 points)
    try:
        instructor_found = 'instructor' in text
        director_found = 'director' in text

        # Also check for signature line drawings (horizontal lines near bottom of page)
        sig_lines = []
        for d in drawings:
            rect = d.get('rect')
            if rect is not None:
                # Signature lines are thin horizontal lines in the bottom third of the page
                if rect.height < 2 and rect.y0 > page_h * 0.6 and rect.width > 50:
                    sig_lines.append(rect)

        if instructor_found and director_found and len(sig_lines) >= 2:
            print(f"PASS: Component 7 — Both signature labels and lines found (0.15 pts)")
            total_score += 0.15
        elif instructor_found and director_found:
            print(f"PARTIAL: Component 7 — Labels found but signature lines missing (0.1 pts)")
            total_score += 0.1
        elif len(sig_lines) >= 2:
            print(f"PARTIAL: Component 7 — Signature lines found but labels missing (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 7 — Signature area incomplete (instructor={instructor_found}, director={director_found}, sig_lines={len(sig_lines)})")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
