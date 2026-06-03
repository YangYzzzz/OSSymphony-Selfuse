"""
Reward Script: Booklet-ordered PDF from brochure.pdf
Task ID: pdf_gf2_050
Domain: pdf
Scoring:
  Component 1 (0.2): brochure_booklet.pdf exists with 8 pages
  Component 2 (0.5): Pages in correct booklet order [7,0,1,6,5,2,3,4]
  Component 3 (0.3): All original content preserved
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_050'

# Distinctive text fingerprints for each original page (0-indexed)
# These are unique identifiers that only appear on one page each
ORIGINAL_PAGE_FINGERPRINTS = {
    0: "Annual Product Catalog 2025",
    1: "Founded in 2008",
    2: "MeridianCloud Platform",
    3: "MeridianInsight 3.0",
    4: "MeridianShield Enterprise",
    5: "Apex Financial Group",
    6: "Starter Plan",
    7: "1200 Innovation Drive",
}

# Expected booklet order: booklet_page_index -> original_page_index
# doc.select([7, 0, 1, 6, 5, 2, 3, 4])
EXPECTED_ORDER = [7, 0, 1, 6, 5, 2, 3, 4]


def verify_task():
    """
    Verify booklet PDF creation with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    booklet_path = f'{WORKDIR}/Documents/brochure_booklet.pdf'
    source_path = f'{WORKDIR}/Documents/brochure.pdf'

    # Precondition: source brochure must exist
    if not os.path.exists(source_path):
        print("CRITICAL: Source brochure.pdf not found")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: booklet file must exist (gate, not scored)
    if not os.path.exists(booklet_path):
        print("FAIL: brochure_booklet.pdf does not exist")
        print("REWARD: 0.0")
        return 0.0

    try:
        booklet_doc = pymupdf.open(booklet_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open booklet PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Booklet has exactly 8 pages (0.2 points)
    try:
        page_count = booklet_doc.page_count
        if page_count == 8:
            print(f"PASS: Component 1 — Booklet has 8 pages (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected 8 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Pages in correct booklet order (0.5 points)
    # Each correctly placed page earns 0.5/8 = 0.0625 points
    try:
        correct_pages = 0
        for booklet_idx, orig_idx in enumerate(EXPECTED_ORDER):
            if booklet_idx >= booklet_doc.page_count:
                break
            page_text = booklet_doc[booklet_idx].get_text("text")
            fingerprint = ORIGINAL_PAGE_FINGERPRINTS[orig_idx]
            if fingerprint in page_text:
                correct_pages += 1
            else:
                print(f"  MISMATCH: Booklet page {booklet_idx} should contain "
                      f"original page {orig_idx} (fingerprint: '{fingerprint}') — not found")

        if correct_pages == 8:
            print(f"PASS: Component 2 — All 8 pages in correct booklet order (0.5 pts)")
            total_score += 0.5
        elif correct_pages > 0:
            partial = round(0.5 * correct_pages / 8, 4)
            print(f"PARTIAL: Component 2 — {correct_pages}/8 pages correctly ordered ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No pages in correct booklet order")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All content preserved (0.3 points)
    # Verify all 8 unique fingerprints appear somewhere in the booklet
    try:
        all_booklet_text = ""
        for i in range(booklet_doc.page_count):
            all_booklet_text += booklet_doc[i].get_text("text")

        found_count = 0
        for orig_idx, fingerprint in ORIGINAL_PAGE_FINGERPRINTS.items():
            if fingerprint in all_booklet_text:
                found_count += 1
            else:
                print(f"  MISSING: Original page {orig_idx} content ('{fingerprint}') not found in booklet")

        if found_count == 8:
            print(f"PASS: Component 3 — All 8 original pages' content preserved (0.3 pts)")
            total_score += 0.3
        elif found_count > 0:
            partial = round(0.3 * found_count / 8, 4)
            print(f"PARTIAL: Component 3 — {found_count}/8 pages' content preserved ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No original content found in booklet")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    booklet_doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
