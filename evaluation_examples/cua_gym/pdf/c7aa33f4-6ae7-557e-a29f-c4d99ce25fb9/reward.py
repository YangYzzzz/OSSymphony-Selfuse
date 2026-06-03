"""
Reward Script: PDF Newspaper Layout Generator
Task ID: pdf_gf3_031
Domain: pdf
Scoring:
  Component 1: Script exists (0.15)
  Component 2: PDF exists and is loadable (0.10)
  Component 3: PDF has exactly 4 pages (0.10)
  Component 4: Pages are A3 size (0.10)
  Component 5: Page 1 has masthead in large display type (0.15)
  Component 6: Images embedded across pages (0.10)
  Component 7: At least 2 pull quotes in styled boxes (0.15)
  Component 8: Page 4 classified ads in small text (0.15)
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
TASK_ID = 'pdf_gf3_031'

SCRIPT_PATH = f'{WORKDIR}/scripts/pdf_newspaper.py'
PDF_PATH = f'{WORKDIR}/output/newspaper.pdf'

# A3 size in points: 841.89 x 1190.55
A3_WIDTH = 841.89
A3_HEIGHT = 1190.55
SIZE_TOLERANCE = 5.0  # points


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Script exists at /home/user/scripts/pdf_newspaper.py (0.15 points)
    # The task asks to CREATE this script; it does not exist in initial_env.
    try:
        if os.path.exists(SCRIPT_PATH) and os.path.getsize(SCRIPT_PATH) > 100:
            print(f"PASS: Component 1 — Script exists at {SCRIPT_PATH} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Script not found or too small at {SCRIPT_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: PDF exists at /home/user/output/newspaper.pdf and is loadable (0.10 points)
    # The task asks the script to GENERATE this PDF; it does not exist in initial_env.
    try:
        if os.path.exists(PDF_PATH):
            doc = pymupdf.open(PDF_PATH)
            if doc.page_count > 0:
                print(f"PASS: Component 2 — PDF exists and is loadable with {doc.page_count} pages (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 2 — PDF exists but has 0 pages")
            doc.close()
        else:
            print(f"FAIL: Component 2 — PDF not found at {PDF_PATH}")
            # No PDF means nothing else can be verified
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load the PDF for remaining checks
    try:
        doc = pymupdf.open(PDF_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF: {e}")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 3: PDF has exactly 4 pages (0.10 points)
    try:
        if doc.page_count == 4:
            print(f"PASS: Component 3 — PDF has 4 pages (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — Expected 4 pages, found {doc.page_count}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Pages are A3 size (~842 x 1191 points) (0.10 points)
    try:
        a3_pages = 0
        for i in range(doc.page_count):
            page = doc[i]
            w, h = page.rect.width, page.rect.height
            if (abs(w - A3_WIDTH) <= SIZE_TOLERANCE and abs(h - A3_HEIGHT) <= SIZE_TOLERANCE):
                a3_pages += 1
        if a3_pages == doc.page_count and doc.page_count > 0:
            print(f"PASS: Component 4 — All {a3_pages} pages are A3 size (0.10 pts)")
            total_score += 0.10
        else:
            page0 = doc[0]
            print(f"FAIL: Component 4 — {a3_pages}/{doc.page_count} pages are A3. Page 0 size: {page0.rect.width:.1f}x{page0.rect.height:.1f}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Page 1 has masthead with newspaper title in large display type (0.15 points)
    # Masthead should be at the top of page 1 with large font (>=30pt)
    try:
        page0 = doc[0]
        data0 = page0.get_text("dict")
        masthead_spans = [
            span for block in data0["blocks"] if block["type"] == 0
            for line in block["lines"]
            for span in line["spans"]
            if span["size"] >= 30 and span["bbox"][1] < 100 and len(span["text"].strip()) > 3
        ]
        if len(masthead_spans) > 0:
            print(f"PASS: Component 5 — Masthead found with large display type on page 1 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — No large masthead text (>=30pt) found near top of page 1")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Images embedded across pages (at least 3 total) (0.10 points)
    try:
        total_images = 0
        pages_with_images = 0
        for i in range(doc.page_count):
            page_images = len(doc[i].get_images())
            total_images += page_images
            if page_images > 0:
                pages_with_images += 1
        if total_images >= 3:
            print(f"PASS: Component 6 — {total_images} images found across {pages_with_images} pages (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 — Only {total_images} images found, expected >= 3")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: At least 2 pull quotes in styled boxes (0.15 points)
    # Pull quotes are italic text >= 12pt with background drawings (boxes) nearby
    try:
        pull_quote_count = 0
        for pi in range(doc.page_count):
            page = doc[pi]
            data = page.get_text("dict")
            drawings = page.get_drawings()
            # Find italic text blocks >= 12pt that look like pull quotes
            italic_blocks = []
            for block in data["blocks"]:
                if block["type"] != 0:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        is_italic = bool(span["flags"] & 2)
                        if is_italic and span["size"] >= 12 and len(span["text"].strip()) > 15:
                            italic_blocks.append(span["bbox"])

            # Check if any italic block has a nearby filled drawing (styled box)
            matched_quotes = set()
            for ib in italic_blocks:
                ib_rect = pymupdf.Rect(ib)
                for d in drawings:
                    d_rect = d.get("rect")
                    if d_rect is None:
                        continue
                    fill = d.get("fill")
                    if fill is not None:
                        # Check if the drawing rect contains or overlaps the italic text
                        if d_rect.intersects(ib_rect):
                            # Use the drawing rect as key to avoid double counting
                            matched_quotes.add((round(d_rect.x0, 1), round(d_rect.y0, 1), pi))
                            break

            pull_quote_count += len(matched_quotes)

        if pull_quote_count >= 2:
            print(f"PASS: Component 7 — {pull_quote_count} styled pull quotes found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 7 — Only {pull_quote_count} styled pull quotes found, expected >= 2")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    # Component 8: Page 4 classified ads section in small text (~8pt) (0.15 points)
    # Classified ads should be at the bottom of page 4 (last page) with font size <= 9pt
    try:
        last_page_idx = doc.page_count - 1
        if last_page_idx >= 0:
            page_last = doc[last_page_idx]
            page_height = page_last.rect.height
            data_last = page_last.get_text("dict")
            small_text_bottom_count = 0
            classified_keywords_found = 0
            classified_keywords = ["FOR SALE", "WANTED", "HELP WANTED", "SERVICES",
                                   "YARD SALE", "ROOMMATE", "PET CARE", "TUTORING",
                                   "CLASSIFIED", "555-"]
            page_text = page_last.get_text("text")

            # Check for small text (<=9pt) in bottom half of page
            for block in data_last["blocks"]:
                if block["type"] != 0:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["size"] <= 9.0 and span["bbox"][1] > page_height * 0.5:
                            small_text_bottom_count += 1

            # Check for classified-style keywords
            for kw in classified_keywords:
                if kw in page_text:
                    classified_keywords_found += 1

            if small_text_bottom_count >= 5 and classified_keywords_found >= 3:
                print(f"PASS: Component 8 — Classified ads found on last page: {small_text_bottom_count} small text spans, {classified_keywords_found} classified keywords (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 8 — small text spans in bottom half: {small_text_bottom_count}, classified keywords: {classified_keywords_found}")
        else:
            print(f"FAIL: Component 8 — No pages in PDF")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(PDF_PATH) and not os.path.exists(SCRIPT_PATH):
    print(f"Neither script nor PDF found")
    print("REWARD: 0.0")
elif pymupdf is None:
    # pymupdf not available; can only check file existence
    # But since neither script nor PDF should exist on initial, this is fine
    print("pymupdf not available, cannot verify PDF contents")
    score = 0.0
    if os.path.exists(SCRIPT_PATH) and os.path.getsize(SCRIPT_PATH) > 100:
        score += 0.15
    if os.path.exists(PDF_PATH):
        score += 0.10
    print(f"REWARD: {score}")
else:
    verify_task()
