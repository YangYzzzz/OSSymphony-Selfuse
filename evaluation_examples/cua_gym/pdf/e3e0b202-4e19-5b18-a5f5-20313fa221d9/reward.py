"""
Reward Script: Redact all addresses from complaint.pdf
Task ID: pdf_legal_012
Domain: pdf
Scoring:
  - Component 1 (0.15): Page count preserved (9 pages)
  - Component 2 (0.50): All 5 street addresses removed from extracted text
  - Component 3 (0.35): Black redaction rectangles present on relevant pages
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_012'

# The 5 addresses that must be redacted (from the original complaint.pdf)
ADDRESSES = [
    "4721 Riverside Drive",          # Page 0 - Elena Vasquez
    "1388 Magnolia Boulevard",       # Page 0 - Summit Ridge
    "903 West Elm Street",           # Page 1 - Derek Thornton
    "2650 Peachtree Road NW",        # Page 5 - Margaret Chen
    "517 Harbor View Lane",          # Page 6 - Robert Hayes
]

# Additional address fragments to check (city, state, ZIP combos)
ADDRESS_FRAGMENTS = [
    "Sacramento, CA 95820",
    "Burbank, CA 91502",
    "Denver, CO 80204",
    "Atlanta, GA 30305",
    "Annapolis, MD 21401",
]

# Pages that should have black redaction rectangles
REDACTION_PAGES = [0, 1, 5, 6]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    import pymupdf

    total_score = 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Page count preserved at 9 pages (0.15 points)
    try:
        page_count = doc.page_count
        if page_count == 9:
            print(f"PASS: Component 1 — Page count is 9 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected 9 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 5 street addresses removed from text (0.50 points)
    # Each address removal is worth 0.10 points
    try:
        all_text = ""
        for page in doc:
            all_text += page.get_text("text")

        addresses_redacted = 0
        for i, addr in enumerate(ADDRESSES):
            if addr not in all_text:
                addresses_redacted += 1
                print(f"PASS: Component 2.{i+1} — Address '{addr}' not found in text (redacted)")
            else:
                print(f"FAIL: Component 2.{i+1} — Address '{addr}' still present in text")

        # Also check fragments for additional confidence
        fragments_redacted = 0
        for i, frag in enumerate(ADDRESS_FRAGMENTS):
            if frag not in all_text:
                fragments_redacted += 1

        # Score: primarily based on street address removal
        if addresses_redacted == 5:
            print(f"PASS: Component 2 — All 5 addresses redacted from text (0.50 pts)")
            total_score += 0.50
        elif addresses_redacted > 0:
            partial = round(addresses_redacted * 0.10, 2)
            print(f"PARTIAL: Component 2 — {addresses_redacted}/5 addresses redacted ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No addresses redacted from text")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Black redaction rectangles on relevant pages (0.35 points)
    try:
        pages_with_redaction = 0
        for pg_num in REDACTION_PAGES:
            page = doc[pg_num]
            drawings = page.get_drawings()
            # Look for black filled rectangles (fill color = (0,0,0) i.e. black)
            black_filled = [
                d for d in drawings
                if d.get("fill") is not None
                and len(d.get("fill", ())) == 3
                and all(c < 0.05 for c in d["fill"])
            ]
            if black_filled:
                pages_with_redaction += 1
                print(f"PASS: Component 3 — Page {pg_num} has {len(black_filled)} black redaction rectangle(s)")
            else:
                print(f"FAIL: Component 3 — Page {pg_num} has no black redaction rectangles")

        if pages_with_redaction == len(REDACTION_PAGES):
            print(f"PASS: Component 3 — All {len(REDACTION_PAGES)} pages have redaction marks (0.35 pts)")
            total_score += 0.35
        elif pages_with_redaction > 0:
            partial = round(pages_with_redaction * (0.35 / len(REDACTION_PAGES)), 2)
            print(f"PARTIAL: Component 3 — {pages_with_redaction}/{len(REDACTION_PAGES)} pages have redaction marks ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No pages have black redaction rectangles")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/legal/complaint_redacted.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
