"""
Reward Script: Crop all pages in scanned_book.pdf to remove 30-point margins, save as scanned_book_cropped.pdf
Task ID: pdf_gf1_014
Domain: pdf
Scoring:
  - Component 1 (0.15): Cropped file exists with correct page count (8)
  - Component 2 (0.50): All pages have correct dimensions 552x732 (30pt margin removed)
  - Component 3 (0.15): Cropbox values are correctly set to (30, 30, 582, 762) on all pages
  - Component 4 (0.20): Text content is preserved in the cropped PDF
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_014'

# Expected values from task context
EXPECTED_PAGES = 8
EXPECTED_WIDTH = 552.0   # 612 - 2*30
EXPECTED_HEIGHT = 732.0  # 792 - 2*30
MARGIN = 30.0
TOLERANCE = 2.0  # points tolerance for dimension checks

# Cropbox expected: (30, 30, 582, 762)
EXPECTED_CROPBOX = (30.0, 30.0, 582.0, 762.0)

def verify_task(file_path, source_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: source file must exist
    if not os.path.exists(source_path):
        print(f"PRECONDITION FAIL: Source file not found: {source_path}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Cropped file exists with correct page count (0.15 points)
    try:
        if not os.path.exists(file_path):
            print(f"FAIL: Component 1 — Cropped file not found: {file_path}")
            print("REWARD: 0.0")
            return 0.0

        doc = pymupdf.open(file_path)
        page_count = doc.page_count

        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 1 — Cropped file exists with {page_count} pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_PAGES} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: All pages have correct effective dimensions 552x732 (0.50 points)
    try:
        pages_correct_dims = 0
        for i in range(doc.page_count):
            page = doc[i]
            w = page.rect.width
            h = page.rect.height
            if abs(w - EXPECTED_WIDTH) <= TOLERANCE and abs(h - EXPECTED_HEIGHT) <= TOLERANCE:
                pages_correct_dims += 1
            else:
                print(f"  Page {i}: width={w}, height={h} — WRONG (expected ~{EXPECTED_WIDTH}x{EXPECTED_HEIGHT})")

        if pages_correct_dims == doc.page_count:
            print(f"PASS: Component 2 — All {doc.page_count} pages have correct dimensions {EXPECTED_WIDTH}x{EXPECTED_HEIGHT} (0.50 pts)")
            total_score += 0.50
        elif pages_correct_dims > 0:
            partial = 0.50 * (pages_correct_dims / doc.page_count)
            print(f"PARTIAL: Component 2 — {pages_correct_dims}/{doc.page_count} pages have correct dimensions ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No pages have correct dimensions")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Cropbox is correctly set on all pages (0.15 points)
    try:
        pages_correct_cropbox = 0
        for i in range(doc.page_count):
            page = doc[i]
            cb = page.cropbox
            if (abs(cb.x0 - EXPECTED_CROPBOX[0]) <= TOLERANCE and
                abs(cb.y0 - EXPECTED_CROPBOX[1]) <= TOLERANCE and
                abs(cb.x1 - EXPECTED_CROPBOX[2]) <= TOLERANCE and
                abs(cb.y1 - EXPECTED_CROPBOX[3]) <= TOLERANCE):
                pages_correct_cropbox += 1
            else:
                print(f"  Page {i}: cropbox=({cb.x0}, {cb.y0}, {cb.x1}, {cb.y1}) — WRONG")

        if pages_correct_cropbox == doc.page_count:
            print(f"PASS: Component 3 — All pages have correct cropbox {EXPECTED_CROPBOX} (0.15 pts)")
            total_score += 0.15
        elif pages_correct_cropbox > 0:
            partial = 0.15 * (pages_correct_cropbox / doc.page_count)
            print(f"PARTIAL: Component 3 — {pages_correct_cropbox}/{doc.page_count} pages have correct cropbox ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No pages have correct cropbox")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Text content is preserved (0.20 points)
    try:
        source_doc = pymupdf.open(source_path)
        text_preserved_count = 0
        for i in range(min(doc.page_count, source_doc.page_count)):
            source_text = source_doc[i].get_text("text").strip()
            cropped_text = doc[i].get_text("text").strip()
            # The cropped text should contain most of the source text
            # (some marginal text might be clipped, but core content should remain)
            if len(source_text) > 0:
                # Check that at least 80% of source text lines are in cropped text
                source_lines = [l.strip() for l in source_text.split('\n') if l.strip()]
                cropped_full = cropped_text
                matches = sum(1 for line in source_lines if line in cropped_full)
                ratio = matches / len(source_lines) if source_lines else 1.0
                if ratio >= 0.7:
                    text_preserved_count += 1
                else:
                    print(f"  Page {i}: text match ratio={ratio:.2f} — too low")
            else:
                text_preserved_count += 1  # empty page is OK
        source_doc.close()

        if text_preserved_count == doc.page_count:
            print(f"PASS: Component 4 — Text content preserved on all pages (0.20 pts)")
            total_score += 0.20
        elif text_preserved_count > 0:
            partial = 0.20 * (text_preserved_count / doc.page_count)
            print(f"PARTIAL: Component 4 — Text preserved on {text_preserved_count}/{doc.page_count} pages ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Text content not preserved")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/scanned_book_cropped.pdf'
source_path = f'{WORKDIR}/Documents/scanned_book.pdf'

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path, source_path)
