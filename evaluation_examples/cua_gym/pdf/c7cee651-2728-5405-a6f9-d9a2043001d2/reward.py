"""
Reward Script: Verify pdftk combination of chapters with blank pages
Task ID: pdf_basic_146
Domain: pdf

Scoring Rubric:
  Component 1: volume1.pdf exists and has correct total page count (65 pages)  — 0.40 pts
  Component 2: Blank page after chapter1 (page 21, 0-indexed: 20)              — 0.25 pts
  Component 3: Blank page after chapter2 (page 47, 0-indexed: 46)              — 0.25 pts
  Component 4: Chapter content ordering preserved (ch1 first, ch3 last)         — 0.10 pts
  Total: 1.00

Expected structure of volume1.pdf:
  Pages 1-20:  chapter1.pdf content  (20 pages)
  Page  21:    blank page
  Pages 22-46: chapter2.pdf content  (25 pages)
  Page  47:    blank page
  Pages 48-65: chapter3.pdf content  (18 pages)
  TOTAL: 65 pages
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'pdf_basic_146'


def verify_task(file_path: str) -> float:
    """
    Verify that volume1.pdf was created correctly by pdftk with blank pages between chapters.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid PDF
    if not os.path.exists(file_path):
        print(f"FAIL: volume1.pdf not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf
        except ImportError:
            print("CRITICAL: PyMuPDF not available")
            print("REWARD: 0.0")
            return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    actual_pages = doc.page_count
    print(f"INFO: volume1.pdf has {actual_pages} pages")

    # Component 1: Total page count == 65
    # chapter1(20) + blank(1) + chapter2(25) + blank(1) + chapter3(18) = 65
    try:
        EXPECTED_PAGES = 65
        if actual_pages == EXPECTED_PAGES:
            print(f"PASS: Component 1 — Page count is {actual_pages} (expected {EXPECTED_PAGES}) (+0.40)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_PAGES} pages, found {actual_pages}")
            # Partial credit: close to correct count suggests partial work
            # (e.g., combining without blank pages = 63 pages)
            if actual_pages == 63:
                print("  NOTE: 63 pages suggests chapters combined without blank pages")
            elif actual_pages > 0:
                print(f"  NOTE: {actual_pages} pages — unexpected count")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Blank page after chapter1 (0-indexed page 20 = 1-indexed page 21)
    # This page should have no text content
    try:
        if actual_pages >= 21:
            blank_page_20 = doc[20]  # 0-indexed: page at index 20 = 21st page
            text_content = blank_page_20.get_text().strip()
            image_list = blank_page_20.get_images()
            drawing_list = blank_page_20.get_drawings()
            # A blank page has: no text, no images, no drawings
            # We allow for very minor whitespace text (encoding artifacts)
            is_blank = (len(text_content) == 0 and
                        len(image_list) == 0 and
                        len(drawing_list) == 0)
            if is_blank:
                print(f"PASS: Component 2 — Page 21 (0-indexed:20) is blank (no text/images/drawings) (+0.25)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — Page 21 (0-indexed:20) is NOT blank")
                print(f"  text='{text_content[:80]}', images={len(image_list)}, drawings={len(drawing_list)}")
        else:
            print(f"FAIL: Component 2 — PDF has fewer than 21 pages ({actual_pages}), cannot check blank page position")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Blank page after chapter2 (0-indexed page 46 = 1-indexed page 47)
    try:
        if actual_pages >= 47:
            blank_page_46 = doc[46]  # 0-indexed: page at index 46 = 47th page
            text_content = blank_page_46.get_text().strip()
            image_list = blank_page_46.get_images()
            drawing_list = blank_page_46.get_drawings()
            is_blank = (len(text_content) == 0 and
                        len(image_list) == 0 and
                        len(drawing_list) == 0)
            if is_blank:
                print(f"PASS: Component 3 — Page 47 (0-indexed:46) is blank (no text/images/drawings) (+0.25)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Page 47 (0-indexed:46) is NOT blank")
                print(f"  text='{text_content[:80]}', images={len(image_list)}, drawings={len(drawing_list)}")
        else:
            print(f"FAIL: Component 3 — PDF has fewer than 47 pages ({actual_pages}), cannot check blank page position")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Content ordering — verify chapter ordering by checking
    # that chapter titles appear in correct order in the document
    # Chapter 1 title text should appear before Chapter 2, which appears before Chapter 3
    try:
        # Search for distinctive chapter markers on expected pages
        # Chapter 1 title should be on page 1 (index 0)
        # Chapter 2 title should be on page 22 (index 21) — after ch1(20) + blank(1)
        # Chapter 3 title should be on page 48 (index 47) — after ch1+blank+ch2+blank
        ordering_correct = False
        if actual_pages >= 65:
            page_0_text = doc[0].get_text()
            # Check chapter 1 title on first page
            ch1_first = "Chapter 1" in page_0_text or "Introduction" in page_0_text
            # Check chapter 2 is after blank page (at index 21)
            page_21_text = doc[21].get_text()
            ch2_second = "Chapter 2" in page_21_text or "Empirical" in page_21_text or "Analysis" in page_21_text
            # Check chapter 3 is after second blank page (at index 47)
            page_47_text = doc[47].get_text()
            ch3_third = "Chapter 3" in page_47_text or "Conclusion" in page_47_text

            ordering_correct = ch1_first and ch2_second and ch3_third
            if ordering_correct:
                print(f"PASS: Component 4 — Chapter ordering correct: Ch1(p1), Ch2(p22), Ch3(p48) (+0.10)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — Chapter ordering not as expected")
                print(f"  ch1_first={ch1_first}, ch2_second={ch2_second}, ch3_third={ch3_third}")
                print(f"  page 0 text snippet: '{page_0_text[:60]}'")
                if actual_pages >= 22:
                    print(f"  page 21 text snippet: '{page_21_text[:60]}'")
                if actual_pages >= 48:
                    print(f"  page 47 text snippet: '{page_47_text[:60]}'")
        else:
            # Even if page count is wrong, try to verify ordering from what's there
            print(f"FAIL: Component 4 — Not enough pages ({actual_pages}) to verify ordering at expected positions")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore breakdown: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: test against canonical artifact path
file_path = f'{WORKDIR}/volume1.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
