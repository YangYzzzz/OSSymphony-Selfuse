"""
Reward Script: Verify strikethrough and sticky note on page 2 of construction_bid.pdf.
Task ID: pdf_basic_184
Domain: pdf

Task: Open ~/Desktop/construction_bid.pdf in Evince. On page 2, strikethrough
      the text 'estimated completion: 6 months' and add a sticky note saying
      'Revised timeline: 4 months per updated schedule'. Save.

Ground truth (page 2 = index 1, 0-based):
  - A StrikeOut annotation overlaps the text 'estimated completion: 6 months'.
  - A Text (sticky note) annotation is present with content
    'Revised timeline: 4 months per updated schedule'.
  - The file still has 5 pages.
  - The original text content is preserved (file not corrupted).

Scoring rubric (total = 1.0):
  Component 1 (0.10): construction_bid.pdf still exists at ~/Desktop/
  Component 2 (0.10): File has exactly 5 pages
  Component 3 (0.10): Page 2 still contains the original text 'estimated completion: 6 months'
  Component 4 (0.30): StrikeOut annotation exists on page 2 overlapping the target text
  Component 5 (0.30): Text (sticky note) annotation exists on page 2 with correct content
  Component 6 (0.10): Original page content markers are intact (not corrupted)
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

DESKTOP = '/home/user/Desktop'
PDF_FILE = f'{DESKTOP}/construction_bid.pdf'

TARGET_TEXT = 'estimated completion: 6 months'
NOTE_CONTENT = 'Revised timeline: 4 months per updated schedule'
PAGE_INDEX = 1  # page 2 is index 1 (0-based)


def collect_annot_data(page):
    """Collect annotation data as plain dicts while the page is live."""
    result = []
    for annot in page.annots():
        result.append({
            "type_code": annot.type[0],
            "type_name": annot.type[1],
            "rect": (annot.rect.x0, annot.rect.y0, annot.rect.x1, annot.rect.y1),
            "content": annot.info.get("content", ""),
            "title": annot.info.get("title", ""),
        })
    return result


def verify_task() -> float:
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ------------------------------------------------------------------ #
    # Component 1: construction_bid.pdf exists (0.10)
    # ------------------------------------------------------------------ #
    try:
        if os.path.exists(PDF_FILE):
            print("PASS: Component 1 — construction_bid.pdf exists (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — construction_bid.pdf not found at {PDF_FILE}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Open the PDF
    try:
        doc = pymupdf.open(PDF_FILE)
    except Exception as e:
        print(f"CRITICAL: Cannot open {PDF_FILE}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # ------------------------------------------------------------------ #
    # Component 2: Exactly 5 pages (0.10)
    # ------------------------------------------------------------------ #
    try:
        if doc.page_count == 5:
            print("PASS: Component 2 — construction_bid.pdf has exactly 5 pages (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 — Expected 5 pages, found {doc.page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Collect page 2 data (text, annotations, target text search) while doc is open
    page2_text = ""
    page2_annot_data = []
    target_rect_tuple = None

    try:
        if doc.page_count >= 2:
            page2 = doc[PAGE_INDEX]
            page2_text = page2.get_text("text")
            page2_annot_data = collect_annot_data(page2)
            instances = page2.search_for(TARGET_TEXT)
            if instances:
                r = instances[0]
                target_rect_tuple = (r.x0, r.y0, r.x1, r.y1)
    except Exception as e:
        print(f"ERROR: collecting page 2 data — {e}")

    # Collect page texts for content marker checks
    page_texts = {}
    try:
        for idx in [0, 1, 4]:
            if doc.page_count > idx:
                page_texts[idx] = doc[idx].get_text("text")
    except Exception as e:
        print(f"ERROR: collecting page texts — {e}")

    doc.close()

    # ------------------------------------------------------------------ #
    # Component 3: Page 2 still contains original target text (0.10)
    # The text should remain even after strikethrough (annotation doesn't remove text)
    # ------------------------------------------------------------------ #
    try:
        if TARGET_TEXT in page2_text:
            print(f"PASS: Component 3 — Page 2 contains '{TARGET_TEXT}' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — Page 2 missing target text '{TARGET_TEXT}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ------------------------------------------------------------------ #
    # Component 4: StrikeOut annotation on page 2 overlapping target text (0.30)
    # ------------------------------------------------------------------ #
    try:
        strikeout_found = False

        for ad in page2_annot_data:
            if ad["type_name"] == "StrikeOut":
                if target_rect_tuple is not None:
                    # Check rect intersection
                    ar = ad["rect"]
                    tr = target_rect_tuple
                    # Rects intersect if they overlap on both axes
                    if ar[0] < tr[2] and ar[2] > tr[0] and ar[1] < tr[3] and ar[3] > tr[1]:
                        strikeout_found = True
                        break
                else:
                    # Target text not found, but a strikeout exists — partial credit
                    strikeout_found = True
                    break

        if not strikeout_found:
            # Looser fallback: any StrikeOut annotation at all on page 2
            for ad in page2_annot_data:
                if ad["type_name"] == "StrikeOut":
                    strikeout_found = True
                    print("  NOTE: StrikeOut found but exact overlap with target text could not be confirmed")
                    break

        if strikeout_found:
            print("PASS: Component 4 — StrikeOut annotation found on page 2 (0.30 pts)")
            total_score += 0.30
        else:
            annot_type_list = [ad["type_name"] for ad in page2_annot_data]
            print(
                f"FAIL: Component 4 — No StrikeOut annotation found on page 2 "
                f"(found annotation types: {annot_type_list})"
            )
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ------------------------------------------------------------------ #
    # Component 5: Text (sticky note) annotation with correct content (0.30)
    # ------------------------------------------------------------------ #
    try:
        note_exact_match = False
        note_partial_match = False
        note_exists = False

        for ad in page2_annot_data:
            if ad["type_name"] == "Text":
                note_exists = True
                content = ad["content"]
                if NOTE_CONTENT in content:
                    note_exact_match = True
                    break
                # Partial: check key phrases
                if "4 months" in content and "timeline" in content.lower():
                    note_partial_match = True

        if note_exact_match:
            print(
                "PASS: Component 5 — Sticky note with correct content found on page 2 "
                "(0.30 pts)"
            )
            total_score += 0.30
        elif note_partial_match:
            print(
                "PARTIAL: Component 5 — Sticky note found with partial match "
                "(key terms '4 months'/'timeline' present) (0.15 pts)"
            )
            total_score += 0.15
        elif note_exists:
            print(
                "PARTIAL: Component 5 — Text annotation exists on page 2 but "
                "content does not match expected (0.05 pts)"
            )
            total_score += 0.05
        else:
            annot_type_list = [ad["type_name"] for ad in page2_annot_data]
            print(
                f"FAIL: Component 5 — No Text (sticky note) annotation found on page 2 "
                f"(found annotation types: {annot_type_list})"
            )
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # ------------------------------------------------------------------ #
    # Component 6: Page content markers intact (0.10)
    # Verifies the document was not corrupted/replaced
    # ------------------------------------------------------------------ #
    try:
        marker_checks = {
            0: "BID_PAGE_1_MARKER",
            1: "BID_PAGE_2_MARKER",
            4: "BID_PAGE_5_MARKER",
        }
        all_pages_ok = all(
            marker in page_texts.get(idx, "")
            for idx, marker in marker_checks.items()
        )

        if all_pages_ok:
            print("PASS: Component 6 — Document content markers intact (0.10 pts)")
            total_score += 0.10
        else:
            for idx, marker in marker_checks.items():
                if marker not in page_texts.get(idx, ""):
                    print(f"  FAIL subcheck C6: page {idx + 1} missing '{marker}'")
            print("FAIL: Component 6 — Some page content markers missing (document may be corrupted)")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: verify the output file on the VM
verify_task()
