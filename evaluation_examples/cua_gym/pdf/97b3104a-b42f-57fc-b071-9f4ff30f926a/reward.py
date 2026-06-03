"""
Reward Script: Verify stamp removal from over_stamped.pdf
Task ID: pdf_adv_195
Domain: pdf

Task: Remove annotations of type 'Stamp' from all pages of ~/Documents/over_stamped.pdf
      while preserving all other annotation types (highlights, notes, links).
      Save as ~/Documents/no_stamps.pdf.

Scoring rubric (total = 1.0):
  Component 1 (0.10): Output file ~/Documents/no_stamps.pdf exists
  Component 2 (0.10): Output file has exactly 8 pages
  Component 3 (0.35): Zero Stamp annotations remain across all pages (progressive per page)
  Component 4 (0.20): All 5 Highlight annotations are preserved
  Component 5 (0.15): All 3 Text (sticky note) annotations are preserved
  Component 6 (0.10): Both link annotations are preserved
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = "/home/user/Documents"
SOURCE_FILE = f"{WORKDIR}/over_stamped.pdf"
OUTPUT_FILE = f"{WORKDIR}/no_stamps.pdf"

EXPECTED_PAGES = 8
EXPECTED_STAMPS = 0
EXPECTED_HIGHLIGHTS = 5
EXPECTED_NOTES = 3
EXPECTED_LINKS = 2


def count_annots_by_type(doc, annot_type):
    """Count annotations of a given type across all pages."""
    return sum(
        sum(1 for a in doc[i].annots() if a.type[1] == annot_type)
        for i in range(doc.page_count)
    )


def count_links(doc):
    """Count all link annotations across all pages."""
    return sum(len(doc[i].get_links()) for i in range(doc.page_count))


def count_stamps_per_page(doc):
    """Return list of stamp counts per page."""
    return [
        sum(1 for a in doc[i].annots() if a.type[1] == "Stamp")
        for i in range(doc.page_count)
    ]


def verify_task():
    """Verify task completion with progressive scoring."""
    total_score = 0.0

    # ── Component 1: Output file exists (0.10 pts) ──────────────────────────
    if not os.path.exists(OUTPUT_FILE):
        print(f"FAIL: Component 1 — no_stamps.pdf not found at {OUTPUT_FILE}")
        print(f"REWARD: 0.0")
        return 0.0

    print(f"PASS: Component 1 — no_stamps.pdf exists (+0.10)")
    total_score += 0.10

    # Open the output PDF
    try:
        doc = pymupdf.open(OUTPUT_FILE)
    except Exception as e:
        print(f"CRITICAL: Cannot open {OUTPUT_FILE}: {e}")
        print(f"REWARD: {total_score:.2f}")
        return total_score

    # ── Component 2: Correct page count (0.10 pts) ──────────────────────────
    actual_pages = doc.page_count
    if actual_pages == EXPECTED_PAGES:
        print(f"PASS: Component 2 — Output has {actual_pages} pages (+0.10)")
        total_score += 0.10
    else:
        print(f"FAIL: Component 2 — Expected {EXPECTED_PAGES} pages, found {actual_pages}")

    # ── Component 3: Zero Stamp annotations (0.35 pts, progressive) ─────────
    # Award partial credit per page that has 0 stamps
    # Check source to ensure it originally had stamps (sanity check)
    source_has_stamps = False
    if os.path.exists(SOURCE_FILE):
        try:
            src_doc = pymupdf.open(SOURCE_FILE)
            src_stamps = count_annots_by_type(src_doc, "Stamp")
            src_doc.close()
            source_has_stamps = src_stamps > 0
        except Exception:
            source_has_stamps = True  # assume yes if we can't check

    stamps_per_page = count_stamps_per_page(doc)
    total_stamps = sum(stamps_per_page)
    pages_with_zero_stamps = sum(1 for s in stamps_per_page if s == 0)

    if total_stamps == 0:
        print(f"PASS: Component 3 — All Stamp annotations removed (0 stamps across all pages) (+0.35)")
        total_score += 0.35
    elif total_stamps > 0:
        # Progressive: award per page clean (max 8 pages)
        per_page_score = 0.35 * (pages_with_zero_stamps / EXPECTED_PAGES)
        per_page_score = round(per_page_score, 4)
        print(
            f"PARTIAL: Component 3 — {total_stamps} stamps remain on some pages. "
            f"{pages_with_zero_stamps}/{EXPECTED_PAGES} pages clean (+{per_page_score:.4f})"
        )
        # Detail which pages still have stamps
        for pi, sc in enumerate(stamps_per_page):
            if sc > 0:
                print(f"  Page {pi + 1}: {sc} stamp(s) remain")
        total_score += per_page_score

    # ── Component 4: Highlights preserved (0.20 pts) ────────────────────────
    actual_highlights = count_annots_by_type(doc, "Highlight")
    if actual_highlights >= EXPECTED_HIGHLIGHTS:
        print(f"PASS: Component 4 — {actual_highlights} Highlight annotations preserved "
              f"(expected {EXPECTED_HIGHLIGHTS}) (+0.20)")
        total_score += 0.20
    elif actual_highlights > 0:
        partial = 0.20 * (actual_highlights / EXPECTED_HIGHLIGHTS)
        partial = round(partial, 4)
        print(
            f"PARTIAL: Component 4 — Only {actual_highlights}/{EXPECTED_HIGHLIGHTS} "
            f"Highlight annotations preserved (+{partial:.4f})"
        )
        total_score += partial
    else:
        print(f"FAIL: Component 4 — No Highlight annotations found (expected {EXPECTED_HIGHLIGHTS})")

    # ── Component 5: Text (note) annotations preserved (0.15 pts) ───────────
    actual_notes = count_annots_by_type(doc, "Text")
    if actual_notes >= EXPECTED_NOTES:
        print(f"PASS: Component 5 — {actual_notes} Text (note) annotations preserved "
              f"(expected {EXPECTED_NOTES}) (+0.15)")
        total_score += 0.15
    elif actual_notes > 0:
        partial = 0.15 * (actual_notes / EXPECTED_NOTES)
        partial = round(partial, 4)
        print(
            f"PARTIAL: Component 5 — Only {actual_notes}/{EXPECTED_NOTES} "
            f"Text annotations preserved (+{partial:.4f})"
        )
        total_score += partial
    else:
        print(f"FAIL: Component 5 — No Text annotations found (expected {EXPECTED_NOTES})")

    # ── Component 6: Links preserved (0.10 pts) ─────────────────────────────
    actual_links = count_links(doc)
    if actual_links >= EXPECTED_LINKS:
        print(f"PASS: Component 6 — {actual_links} link(s) preserved "
              f"(expected {EXPECTED_LINKS}) (+0.10)")
        total_score += 0.10
    elif actual_links > 0:
        partial = 0.10 * (actual_links / EXPECTED_LINKS)
        partial = round(partial, 4)
        print(
            f"PARTIAL: Component 6 — Only {actual_links}/{EXPECTED_LINKS} "
            f"links preserved (+{partial:.4f})"
        )
        total_score += partial
    else:
        print(f"FAIL: Component 6 — No links found (expected {EXPECTED_LINKS})")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
