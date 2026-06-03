"""
Reward Script: Create a PDF cover page for court filing and prepend to brief
Task ID: pdf_legal_042
Domain: pdf
Scoring:
  Component 1: Output file exists with correct page count (41 pages) — 0.2 pts
  Component 2: Cover page contains all 5 required text elements — 0.3 pts
  Component 3: Cover page text elements are centered — 0.2 pts
  Component 4: Original brief pages preserved (pages 2-41 match original) — 0.3 pts
"""

import os
import sys

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_042'
OUTPUT_PATH = f'{WORKDIR}/legal/brief_with_cover.pdf'
ORIGINAL_PATH = f'{WORKDIR}/legal/brief.pdf'

# Required text elements on the cover page
REQUIRED_TEXTS = [
    'IN THE UNITED STATES DISTRICT COURT',
    'FOR THE NORTHERN DISTRICT OF CALIFORNIA',
    'SMITH v. JONES',
    'Case No. 3:24-cv-01234',
    'MEMORANDUM OF POINTS AND AUTHORITIES',
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("CRITICAL: PyMuPDF (fitz) not available")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: output file must exist
    if not os.path.exists(OUTPUT_PATH):
        print(f"CRITICAL: Output file not found: {OUTPUT_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: original brief must exist (needed for page comparison)
    if not os.path.exists(ORIGINAL_PATH):
        print(f"CRITICAL: Original brief not found: {ORIGINAL_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = fitz.open(OUTPUT_PATH)
        doc_original = fitz.open(ORIGINAL_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF files: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output has 41 pages (original 40 + 1 cover) — 0.2 pts
    try:
        page_count = doc.page_count
        original_count = doc_original.page_count
        expected_count = original_count + 1
        if page_count == expected_count:
            print(f"PASS: Component 1 — Page count is {page_count} (original {original_count} + 1 cover) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected {expected_count} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Cover page contains all 5 required text elements — 0.3 pts
    try:
        cover_page = doc[0]
        cover_text = cover_page.get_text()

        found_count = 0
        for req_text in REQUIRED_TEXTS:
            if req_text in cover_text:
                found_count += 1
                print(f"  FOUND: '{req_text}'")
            else:
                # Try case-insensitive match as fallback
                if req_text.lower() in cover_text.lower():
                    found_count += 1
                    print(f"  FOUND (case-insensitive): '{req_text}'")
                else:
                    print(f"  MISSING: '{req_text}'")

        if found_count == len(REQUIRED_TEXTS):
            print(f"PASS: Component 2 — All {found_count}/{len(REQUIRED_TEXTS)} text elements present on cover page (0.3 pts)")
            total_score += 0.3
        elif found_count > 0:
            # Partial credit proportional to found elements
            partial = 0.3 * (found_count / len(REQUIRED_TEXTS))
            print(f"PARTIAL: Component 2 — {found_count}/{len(REQUIRED_TEXTS)} text elements found ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No required text elements found on cover page")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Cover page text elements are centered — 0.2 pts
    try:
        cover_page = doc[0]
        page_width = cover_page.rect.width
        page_center = page_width / 2.0
        blocks = cover_page.get_text('blocks')

        # Filter to text blocks only (block_type == 0)
        text_blocks = [b for b in blocks if b[6] == 0]

        if len(text_blocks) == 0:
            print(f"FAIL: Component 3 — No text blocks found on cover page")
        else:
            centered_count = 0
            # Allow 30pt tolerance for centering
            tolerance = 30.0
            for b in text_blocks:
                x0, x1 = b[0], b[2]
                block_center = (x0 + x1) / 2.0
                offset = abs(block_center - page_center)
                if offset <= tolerance:
                    centered_count += 1

            if centered_count == len(text_blocks):
                print(f"PASS: Component 3 — All {centered_count} text blocks are centered (tolerance {tolerance}pt) (0.2 pts)")
                total_score += 0.2
            elif centered_count > 0:
                partial = 0.2 * (centered_count / len(text_blocks))
                print(f"PARTIAL: Component 3 — {centered_count}/{len(text_blocks)} text blocks centered ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — No text blocks are centered")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Original brief pages preserved — pages 2-41 match original — 0.3 pts
    try:
        if doc.page_count < 2 or doc_original.page_count < 1:
            print(f"FAIL: Component 4 — Not enough pages to compare")
        else:
            matching_pages = 0
            total_pages_to_check = doc_original.page_count
            # Compare each page of original with corresponding page in output (offset by 1)
            for i in range(total_pages_to_check):
                golden_page_text = doc[i + 1].get_text()[:300]
                original_page_text = doc_original[i].get_text()[:300]
                if golden_page_text == original_page_text:
                    matching_pages += 1

            if matching_pages == total_pages_to_check:
                print(f"PASS: Component 4 — All {total_pages_to_check} original pages preserved (0.3 pts)")
                total_score += 0.3
            elif matching_pages > 0:
                ratio = matching_pages / total_pages_to_check
                partial = 0.3 * ratio
                print(f"PARTIAL: Component 4 — {matching_pages}/{total_pages_to_check} pages match ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — No original pages match in output")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()
    doc_original.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
