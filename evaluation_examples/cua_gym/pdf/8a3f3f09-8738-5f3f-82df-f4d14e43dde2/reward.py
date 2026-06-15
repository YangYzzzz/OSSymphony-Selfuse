"""
Reward Script: Add footer to every page of a 100-page thesis PDF
Task ID: pdf_res_034
Domain: pdf
Scoring:
  Component 1 (0.2): Output file exists, is valid PDF with 100 pages
  Component 2 (0.4): Footer text 'PhD Thesis - University of Oxford - 2026' on ALL 100 pages
  Component 3 (0.2): Footer font size is ~8pt
  Component 4 (0.2): Footer text is gray and positioned at the bottom of the page
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_034'
FOOTER_TEXT = 'PhD Thesis - University of Oxford - 2026'
EXPECTED_PAGES = 100

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid PDF with 100 pages (0.2 points)
    try:
        page_count = len(doc)
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 1 — PDF has {page_count} pages (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_PAGES} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Footer text present on ALL 100 pages (0.4 points)
    try:
        pages_with_footer = 0
        for i in range(len(doc)):
            page_text = doc[i].get_text('text')
            if FOOTER_TEXT in page_text:
                pages_with_footer += 1

        if pages_with_footer == EXPECTED_PAGES:
            print(f"PASS: Component 2 — Footer found on all {pages_with_footer}/{EXPECTED_PAGES} pages (0.4 pts)")
            total_score += 0.4
        elif pages_with_footer > 0:
            # Partial credit: proportional to pages with footer
            partial = 0.4 * (pages_with_footer / EXPECTED_PAGES)
            print(f"PARTIAL: Component 2 — Footer found on {pages_with_footer}/{EXPECTED_PAGES} pages ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Footer not found on any page")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Footer font size is approximately 8pt (0.2 points)
    try:
        footer_size_ok = False
        page = doc[0]
        blocks = page.get_text('dict')['blocks']
        for block in blocks:
            if block.get('type', 0) != 0:
                continue
            for line in block.get('lines', []):
                for span in line.get('spans', []):
                    if FOOTER_TEXT in span.get('text', ''):
                        size = span['size']
                        # Allow small tolerance for font size (7-9pt)
                        if 7.0 <= size <= 9.0:
                            footer_size_ok = True
                            print(f"PASS: Component 3 — Footer font size is {size}pt (0.2 pts)")
                            total_score += 0.2
                        else:
                            print(f"FAIL: Component 3 — Footer font size is {size}pt, expected ~8pt")
                        break
                if footer_size_ok:
                    break
            if footer_size_ok:
                break
        if not footer_size_ok and total_score < 0.4:
            print(f"FAIL: Component 3 — Could not find footer span to check font size")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Footer is gray-colored and positioned at bottom of page (0.2 points)
    try:
        color_ok = False
        position_ok = False
        page = doc[0]
        page_height = page.rect.height
        blocks = page.get_text('dict')['blocks']
        for block in blocks:
            if block.get('type', 0) != 0:
                continue
            for line in block.get('lines', []):
                for span in line.get('spans', []):
                    if FOOTER_TEXT in span.get('text', ''):
                        # Check color: gray means R=G=B, not black (0) and not white
                        color_int = span['color']
                        r = (color_int >> 16) & 0xFF
                        g = (color_int >> 8) & 0xFF
                        b = color_int & 0xFF
                        # Gray: R, G, B are roughly equal and not black (0,0,0)
                        if r == g == b and r > 50:
                            color_ok = True
                        elif abs(r - g) < 20 and abs(g - b) < 20 and abs(r - b) < 20 and r > 50:
                            color_ok = True

                        # Check position: footer should be in bottom 15% of page
                        bbox = span['bbox']
                        y_center = (bbox[1] + bbox[3]) / 2
                        if y_center > page_height * 0.85:
                            position_ok = True

                        break

        sub_score = 0.0
        if color_ok and position_ok:
            sub_score = 0.2
            print(f"PASS: Component 4 — Footer is gray (r={r},g={g},b={b}) and at bottom (y={y_center:.0f}/{page_height:.0f}) (0.2 pts)")
        elif color_ok:
            sub_score = 0.1
            print(f"PARTIAL: Component 4 — Footer is gray but not at bottom")
        elif position_ok:
            sub_score = 0.1
            print(f"PARTIAL: Component 4 — Footer at bottom but not gray-colored")
        else:
            print(f"FAIL: Component 4 — Footer is not gray or not at bottom")

        total_score += sub_score
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/thesis/thesis_final_footer.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
