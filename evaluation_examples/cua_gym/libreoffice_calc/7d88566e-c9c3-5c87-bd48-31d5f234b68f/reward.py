"""
Reward Script: Apply OCR to scanned PDF and create searchable PDF with embedded text layer
Task ID: pdf_gf1_027
Domain: pdf
Scoring:
  Component 1: Output file exists with correct page count (0.2)
  Component 2: Each page has extractable text >= 100 chars (0.4)
  Component 3: Extracted text contains legal terms (0.2)
  Component 4: Pages still contain original images (visual preservation) (0.2)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf1_027'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    output_path = os.path.join(WORKDIR, 'Documents', 'scanned_contract_searchable.pdf')

    # Precondition: output file must exist
    if not os.path.exists(output_path):
        print(f"CRITICAL: Output file not found: {output_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf

    try:
        doc = pymupdf.open(output_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {output_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file has exactly 3 pages (0.2 points)
    # This checks that the searchable PDF was created with all 3 pages from the original.
    # The initial_env does NOT have scanned_contract_searchable.pdf, so this fails on initial.
    try:
        page_count = doc.page_count
        if page_count == 3:
            print(f"PASS: Component 1 — Page count is 3 (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected 3 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Each page has extractable text with at least 100 characters (0.4 points)
    # The original scanned PDF has 0 text per page. The searchable version must have embedded OCR text.
    # Score 0.133... per page (total 0.4 for all 3 pages)
    try:
        pages_with_text = 0
        per_page_score = 0.4 / 3.0
        for i in range(min(doc.page_count, 3)):
            text = doc[i].get_text("text").strip()
            text_len = len(text)
            if text_len >= 100:
                print(f"PASS: Component 2.{i} — Page {i} has {text_len} chars of text (>= 100) ({per_page_score:.4f} pts)")
                total_score += per_page_score
                pages_with_text += 1
            else:
                print(f"FAIL: Component 2.{i} — Page {i} has only {text_len} chars (need >= 100)")
        print(f"INFO: Component 2 — {pages_with_text}/3 pages have sufficient text")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Extracted text contains legal terms (0.2 points)
    # The task states the PDF is a scanned legal contract. OCR text should contain legal terminology.
    # Check for at least 2 of: 'agreement', 'party', 'hereby'
    try:
        all_text = ""
        for i in range(doc.page_count):
            all_text += doc[i].get_text("text").strip().lower() + " "

        legal_terms = ['agreement', 'party', 'hereby']
        found_terms = [term for term in legal_terms if term in all_text]
        # Need at least 2 of 3 legal terms
        if len(found_terms) >= 2:
            print(f"PASS: Component 3 — Found legal terms: {found_terms} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Found only {len(found_terms)} legal terms: {found_terms}, need >= 2")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Pages still contain images (visual appearance preserved) (0.2 points)
    # The original scanned PDF has 1 image per page. The searchable version should retain these images
    # (OCR adds a text layer but should not remove the scanned images).
    try:
        pages_with_images = 0
        per_page_img_score = 0.2 / 3.0
        for i in range(min(doc.page_count, 3)):
            images = doc[i].get_images()
            if len(images) >= 1:
                print(f"PASS: Component 4.{i} — Page {i} has {len(images)} image(s) ({per_page_img_score:.4f} pts)")
                total_score += per_page_img_score
                pages_with_images += 1
            else:
                print(f"FAIL: Component 4.{i} — Page {i} has no images (original scanned images lost)")
        print(f"INFO: Component 4 — {pages_with_images}/3 pages retain images")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
