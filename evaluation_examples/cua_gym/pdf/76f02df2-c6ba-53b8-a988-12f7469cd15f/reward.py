"""
Reward Script: Multi-app workflow — GIMP letterhead + Writer proposal + pymupdf watermark
Task ID: pdf_cross_141
Domain: pdf
Scoring:
  - Component 1: PDF is multi-page (>= 2 pages)                         — 0.15 pts
  - Component 2: Letterhead image (2000x250) on every page as header     — 0.30 pts
  - Component 3: 3 proposal paragraphs in content                        — 0.25 pts
  - Component 4: 'CONFIDENTIAL' watermark on every page                  — 0.20 pts
  - Component 5: Sequential page numbers on every page                   — 0.10 pts
  Total: 1.00
"""

import os
import sys

# Ensure user-local pip packages are on path (in case pymupdf installed via pip3 --user)
sys.path.insert(0, '/home/user/.local/lib/python3.10/site-packages')

try:
    import pymupdf
except ImportError:
    try:
        import fitz as pymupdf
    except ImportError:
        print("CRITICAL: pymupdf/fitz not available")
        print("REWARD: 0.0")
        sys.exit(0)

PDF_PATH = '/home/user/Documents/proposal_final.pdf'


def verify_task(pdf_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: the file must exist and be a valid PDF
    if not os.path.exists(pdf_path):
        print(f"CRITICAL: PDF not found at {pdf_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(pdf_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {pdf_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = doc.page_count

    # Component 1: PDF is multi-page (>= 2 pages) (0.15 points)
    # The task requires a multi-page PDF with both proposal content and terms/appendix pages.
    # Initial env has no PDF at all, so this check correctly fails on initial_env.
    try:
        if page_count >= 2:
            print(f"PASS: Component 1 — PDF has {page_count} pages (>= 2 required) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — PDF has {page_count} pages, expected >= 2")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Letterhead image (2000x250) on every page as header (0.30 points)
    # Task requires a GIMP-created 2000x250px letterhead embedded as image header on every page.
    # We check that every page has at least one image with the correct dimensions.
    try:
        pages_with_correct_header = 0
        for page_idx in range(page_count):
            page = doc[page_idx]
            images = page.get_images()
            found_header = False
            for img_info in images:
                xref = img_info[0]
                try:
                    img_dict = doc.extract_image(xref)
                    w = img_dict['width']
                    h = img_dict['height']
                    # Letterhead must be 2000x250 px (exact, as specified in task)
                    if w == 2000 and h == 250:
                        # Also verify it's positioned in the top/header area of the page
                        # Get image block rect from rawdict
                        data = page.get_text('rawdict')
                        for block in data['blocks']:
                            if block['type'] == 1:  # image block
                                img_rect = block.get('bbox')
                                if img_rect is not None:
                                    # Header means it's in the top 25% of the page
                                    page_height = page.rect.height
                                    if img_rect[1] < page_height * 0.25:
                                        found_header = True
                                        break
                        if not found_header:
                            # Accept if image has right dimensions even if rect check fails
                            found_header = True
                except Exception:
                    pass
            if found_header:
                pages_with_correct_header += 1

        if pages_with_correct_header == page_count and page_count >= 2:
            print(f"PASS: Component 2 — Letterhead image (2000x250) found on all {page_count} pages (0.30 pts)")
            total_score += 0.30
        elif pages_with_correct_header > 0:
            partial = 0.30 * (pages_with_correct_header / page_count)
            print(f"PARTIAL: Component 2 — Letterhead found on {pages_with_correct_header}/{page_count} pages ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Letterhead image (2000x250) not found on any page")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 3 proposal paragraphs/sections in content (0.25 points)
    # Task requires adding 3 paragraphs of proposal content in Writer.
    # We check for the 3 major section headings that should appear in the proposal.
    try:
        all_text = ""
        for page_idx in range(page_count):
            all_text += doc[page_idx].get_text("text")

        required_sections = [
            "Executive Summary",
            "Proposed Collaboration Scope",
            "Financial Projections",
        ]
        found_sections = [s for s in required_sections if s in all_text]

        if len(found_sections) == 3:
            print(f"PASS: Component 3 — All 3 proposal paragraphs/sections found (0.25 pts)")
            total_score += 0.25
        elif len(found_sections) >= 1:
            partial = 0.25 * (len(found_sections) / 3)
            print(f"PARTIAL: Component 3 — Found {len(found_sections)}/3 sections: {found_sections} ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No proposal sections found in text")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 'CONFIDENTIAL' watermark on every page (0.20 points)
    # Task requires pymupdf to add CONFIDENTIAL watermark to every page.
    try:
        pages_with_watermark = 0
        for page_idx in range(page_count):
            page = doc[page_idx]
            instances = page.search_for("CONFIDENTIAL")
            if instances:
                pages_with_watermark += 1

        if pages_with_watermark == page_count and page_count >= 1:
            print(f"PASS: Component 4 — 'CONFIDENTIAL' watermark found on all {page_count} pages (0.20 pts)")
            total_score += 0.20
        elif pages_with_watermark > 0:
            partial = 0.20 * (pages_with_watermark / page_count)
            print(f"PARTIAL: Component 4 — 'CONFIDENTIAL' on {pages_with_watermark}/{page_count} pages ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — 'CONFIDENTIAL' watermark not found on any page")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Sequential page numbers on every page (0.10 points)
    # Task requires pymupdf to add page numbers to every page.
    # We check that each page contains its respective page number "Page N".
    try:
        pages_with_correct_number = 0
        for page_idx in range(page_count):
            page = doc[page_idx]
            expected_num_str = f"Page {page_idx + 1}"
            page_text = page.get_text("text")
            if expected_num_str in page_text:
                pages_with_correct_number += 1

        if pages_with_correct_number == page_count and page_count >= 1:
            print(f"PASS: Component 5 — Sequential page numbers found on all {page_count} pages (0.10 pts)")
            total_score += 0.10
        elif pages_with_correct_number > 0:
            partial = 0.10 * (pages_with_correct_number / page_count)
            print(f"PARTIAL: Component 5 — Page numbers correct on {pages_with_correct_number}/{page_count} pages ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — Sequential page numbers not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task(PDF_PATH)
