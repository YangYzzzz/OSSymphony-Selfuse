"""
Reward Script: Convert memo.docx to PDF, add page numbers and 'CONVERTED FROM DOCX' footer
Task ID: pdf_gf2_025
Domain: pdf (libreoffice_calc domain label but PDF task)
Scoring:
  Component 1: memo.pdf exists and is a valid 4-page PDF (0.2)
  Component 2: memo_final.pdf exists and is a valid 4-page PDF (0.2)
  Component 3: Page numbers 1-4 centered at bottom of each page in memo_final.pdf (0.3)
  Component 4: 'CONVERTED FROM DOCX' footer text on every page in memo_final.pdf (0.3)
"""

import os

try:
    import pymupdf
except ImportError:
    try:
        import fitz as pymupdf
    except ImportError:
        pymupdf = None

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_025'

MEMO_PDF = os.path.join(WORKDIR, 'Documents', 'memo.pdf')
MEMO_FINAL_PDF = os.path.join(WORKDIR, 'Documents', 'memo_final.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Early exit if pymupdf is not available and files don't exist
    if pymupdf is None:
        if not os.path.exists(MEMO_PDF) and not os.path.exists(MEMO_FINAL_PDF):
            print("FAIL: pymupdf not available and no PDF files found")
            print("REWARD: 0.0")
            return 0.0
        else:
            print("CRITICAL: pymupdf not available but PDF files exist — cannot verify")
            print("REWARD: 0.0")
            return 0.0

    # Component 1: memo.pdf exists and is a valid 4-page PDF (0.2 points)
    # This file should NOT exist on initial_env (only memo.docx exists initially)
    try:
        if not os.path.exists(MEMO_PDF):
            print(f"FAIL: Component 1 — memo.pdf does not exist at {MEMO_PDF}")
        else:
            doc = pymupdf.open(MEMO_PDF)
            page_count = doc.page_count
            doc.close()
            if page_count == 4:
                print(f"PASS: Component 1 — memo.pdf exists with {page_count} pages (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 — memo.pdf has {page_count} pages, expected 4")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: memo_final.pdf exists and is a valid 4-page PDF (0.2 points)
    # This file should NOT exist on initial_env
    try:
        if not os.path.exists(MEMO_FINAL_PDF):
            print(f"FAIL: Component 2 — memo_final.pdf does not exist at {MEMO_FINAL_PDF}")
        else:
            doc = pymupdf.open(MEMO_FINAL_PDF)
            page_count = doc.page_count
            doc.close()
            if page_count == 4:
                print(f"PASS: Component 2 — memo_final.pdf exists with {page_count} pages (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — memo_final.pdf has {page_count} pages, expected 4")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Components 3 and 4 require memo_final.pdf to exist
    if not os.path.exists(MEMO_FINAL_PDF):
        print("FAIL: Components 3-4 skipped — memo_final.pdf not found")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    try:
        doc = pymupdf.open(MEMO_FINAL_PDF)
    except Exception as e:
        print(f"CRITICAL: Cannot open memo_final.pdf: {e}")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 3: Page numbers 1-4 centered at bottom of each page (0.3 points)
    # Each page contributes 0.075 points (0.3 / 4)
    try:
        page_number_score = 0.0
        pages_with_numbers = 0
        for i in range(doc.page_count):
            page = doc[i]
            expected_num = str(i + 1)
            page_height = page.rect.height
            page_width = page.rect.width

            # Search bottom region (last 100 pts) for the page number
            bottom_rect = pymupdf.Rect(0, page_height - 100, page_width, page_height)
            bottom_text = page.get_textbox(bottom_rect)

            # Check that the expected page number appears in the bottom text
            if expected_num in bottom_text:
                # Verify it is roughly centered by checking text span positions
                data = page.get_text("dict")
                found_centered = False
                for block in data["blocks"]:
                    if block["type"] != 0:
                        continue
                    for line in block["lines"]:
                        for span in line["spans"]:
                            if span["text"].strip() == expected_num and span["bbox"][1] > page_height - 100:
                                # Check if x-center is roughly in the middle of the page
                                x_center = (span["bbox"][0] + span["bbox"][2]) / 2.0
                                if abs(x_center - page_width / 2.0) < 80:
                                    found_centered = True
                                    break
                        if found_centered:
                            break
                    if found_centered:
                        break

                if found_centered:
                    pages_with_numbers += 1
                    page_number_score += 0.075
                    print(f"  Page {i}: number '{expected_num}' found centered at bottom")
                else:
                    print(f"  Page {i}: number '{expected_num}' found at bottom but not centered")
            else:
                print(f"  Page {i}: number '{expected_num}' NOT found in bottom region")

        if pages_with_numbers == 4:
            print(f"PASS: Component 3 — All 4 pages have centered page numbers (0.3 pts)")
            total_score += 0.3
        elif pages_with_numbers > 0:
            print(f"PARTIAL: Component 3 — {pages_with_numbers}/4 pages have centered page numbers ({page_number_score:.3f} pts)")
            total_score += page_number_score
        else:
            print(f"FAIL: Component 3 — No pages have page numbers at bottom")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 'CONVERTED FROM DOCX' footer on every page (0.3 points)
    # Each page contributes 0.075 points (0.3 / 4)
    # The footer should be small gray text at the bottom
    try:
        footer_score = 0.0
        pages_with_footer = 0
        for i in range(doc.page_count):
            page = doc[i]
            page_height = page.rect.height
            page_width = page.rect.width

            # Search bottom region for the footer text
            bottom_rect = pymupdf.Rect(0, page_height - 100, page_width, page_height)
            bottom_text = page.get_textbox(bottom_rect)

            if "CONVERTED FROM DOCX" in bottom_text:
                # Verify it has gray color (not black) and small font
                data = page.get_text("dict")
                found_gray = False
                for block in data["blocks"]:
                    if block["type"] != 0:
                        continue
                    for line in block["lines"]:
                        for span in line["spans"]:
                            if "CONVERTED FROM DOCX" in span["text"] and span["bbox"][1] > page_height - 100:
                                color_int = span["color"]
                                r = (color_int >> 16) & 0xFF
                                g = (color_int >> 8) & 0xFF
                                b = color_int & 0xFF
                                font_size = span["size"]
                                # Gray means R==G==B and not black (all 0) and not white (all 255)
                                is_gray = (r == g == b and 50 < r < 220)
                                is_small = font_size <= 10.0
                                if is_gray and is_small:
                                    found_gray = True
                                    print(f"  Page {i}: footer found, color=({r},{g},{b}), size={font_size}")
                                elif is_gray:
                                    found_gray = True
                                    print(f"  Page {i}: footer found gray but size={font_size} (slightly large)")
                                elif is_small:
                                    # Accept if text is small even if color is not perfectly gray
                                    found_gray = True
                                    print(f"  Page {i}: footer found small but color=({r},{g},{b})")
                                else:
                                    print(f"  Page {i}: footer found but color=({r},{g},{b}), size={font_size}")
                                break
                        if found_gray:
                            break
                    if found_gray:
                        break

                if found_gray:
                    pages_with_footer += 1
                    footer_score += 0.075
                else:
                    # Still give partial credit if text is present but not styled
                    pages_with_footer += 1
                    footer_score += 0.05
                    print(f"  Page {i}: footer text present but style not verified")
            else:
                print(f"  Page {i}: 'CONVERTED FROM DOCX' NOT found in bottom region")

        if pages_with_footer == 4 and footer_score >= 0.28:
            print(f"PASS: Component 4 — All 4 pages have 'CONVERTED FROM DOCX' footer (0.3 pts)")
            total_score += 0.3
        elif pages_with_footer > 0:
            actual_pts = min(footer_score, 0.3)
            print(f"PARTIAL: Component 4 — {pages_with_footer}/4 pages have footer ({actual_pts:.3f} pts)")
            total_score += actual_pts
        else:
            print(f"FAIL: Component 4 — No pages have 'CONVERTED FROM DOCX' footer")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
