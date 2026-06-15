"""
Reward Script: Create a composite PDF with figure from source and caption
Task ID: pdf_res_091
Domain: pdf
Scoring:
  Component 1 (0.3): figure_plate.pdf exists and has exactly 1 page
  Component 2 (0.4): Caption text is present in the page
  Component 3 (0.3): An image/figure is embedded in the page
"""

import os
import fitz  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_091'
TARGET_FILE = os.path.join(WORKDIR, 'papers', 'figure_plate.pdf')
EXPECTED_CAPTION = 'Figure 3.2: Architecture of the proposed model (reproduced from Smith et al., 2025)'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PDF has exactly 1 page (0.3 points)
    # This checks the structural requirement: a single new page was created.
    # Initial env has no figure_plate.pdf, so this fails on initial.
    try:
        page_count = len(doc)
        if page_count == 1:
            print(f"PASS: Component 1 — PDF has exactly 1 page (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Expected 1 page, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Caption text is present (0.4 points)
    # The task requires the specific caption string. We check via text extraction.
    # Initial env has no figure_plate.pdf, so this fails on initial.
    try:
        page = doc[0]
        text = page.get_text().strip()
        # Check for the full caption string
        if EXPECTED_CAPTION in text:
            print(f"PASS: Component 2 — Caption found in text extraction (0.4 pts)")
            total_score += 0.4
        else:
            # Check partial match for debugging
            if 'Figure 3.2' in text:
                print(f"FAIL: Component 2 — 'Figure 3.2' found but full caption missing")
                print(f"  Extracted text: {repr(text[:300])}")
            else:
                print(f"FAIL: Component 2 — Caption not found in text extraction")
                print(f"  Extracted text: {repr(text[:300])}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Image/figure content is embedded (0.3 points)
    # The task requires the figure from page 5 of source_figure.pdf to be placed on the page.
    # We verify by checking for embedded images or Form XObjects (show_pdf_page creates XObjects).
    # Initial env has no figure_plate.pdf, so this fails on initial.
    try:
        page = doc[0]
        images = page.get_images(full=True)
        xobjects = page.get_xobjects()

        # show_pdf_page() embeds content as a Form XObject, get_images() may also detect it
        has_visual_content = len(images) > 0 or len(xobjects) > 0

        if has_visual_content:
            print(f"PASS: Component 3 — Visual content found: {len(images)} image(s), {len(xobjects)} xobject(s) (0.3 pts)")
            total_score += 0.3
        else:
            # Also check if page has substantial drawing commands (pixmap-based content)
            # Some figure embedding methods create inline content streams
            page_dict = page.get_text("dict")
            image_blocks = [b for b in page_dict.get("blocks", []) if b.get("type") == 1]
            if len(image_blocks) > 0:
                print(f"PASS: Component 3 — Image blocks found in content stream (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — No visual content (images/xobjects) found on page")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(TARGET_FILE):
    print(f"File not found: {TARGET_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(TARGET_FILE)
