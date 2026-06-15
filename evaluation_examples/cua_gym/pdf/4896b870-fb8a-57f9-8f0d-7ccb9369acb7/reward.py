"""
Reward Script: Add strikethrough and sticky note annotations on PDF page 4
Task ID: pdf_basic_159
Domain: pdf
Scoring:
  Component 1 (0.5): Strikethrough (StrikeOut) annotation over 'Budget allocation is insufficient' on page 4
  Component 2 (0.5): Sticky note (Text annotation) with content containing
                     'Budget has been increased to $500K - see updated proposal' on page 4
Total: 1.0
"""

import os

# Try both import styles for compatibility
try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user/Desktop'
TARGET_SENTENCE = 'Budget allocation is insufficient'
STICKY_NOTE_CONTENT = 'Budget has been increased to $500K - see updated proposal'
PDF_PATH = f'{WORKDIR}/proposal_feedback.pdf'
PAGE_INDEX = 3  # Page 4 (0-indexed)


def get_page_annotations(page):
    """Collect all annotation data from a PDF page."""
    annots_data = []
    for annot in page.annots():
        annots_data.append({
            "type": annot.type[1],           # "StrikeOut", "Text", "Highlight", etc.
            "type_code": annot.type[0],
            "content": annot.info.get("content", ""),
            "rect": pymupdf.Rect(annot.rect),
            "colors": {
                "stroke": annot.colors.get("stroke"),
                "fill": annot.colors.get("fill"),
            },
        })
    return annots_data


def check_strikeout_on_target(page, target_sentence):
    """
    Check if a StrikeOut annotation exists on the page that overlaps with the target sentence.
    Returns True if found, False otherwise.
    """
    text_instances = page.search_for(target_sentence)
    annots_data = get_page_annotations(page)
    strikeout_annots = [a for a in annots_data if a["type"] == "StrikeOut"]

    if not strikeout_annots:
        return False

    if not text_instances:
        # Text not found by search (unusual), but StrikeOut exists on page
        # Accept if at least a StrikeOut is on this page
        return len(strikeout_annots) > 0

    # Check if any StrikeOut overlaps with the target text location
    target_rect = text_instances[0]
    for sa in strikeout_annots:
        sa_rect = sa["rect"]
        # Check intersection OR vertical proximity (some viewers store slightly offset rects)
        if sa_rect.intersects(target_rect):
            return True
        # Secondary: check vertical overlap (y-range overlap)
        if sa_rect.y0 <= target_rect.y1 and sa_rect.y1 >= target_rect.y0:
            return True
    return False


def check_sticky_note_content(page, expected_content):
    """
    Check if a Text (sticky note) annotation exists on the page with the expected content.
    Returns True if found, False otherwise.
    """
    annots_data = get_page_annotations(page)
    text_annots = [a for a in annots_data if a["type"] == "Text"]

    for ta in text_annots:
        content = ta.get("content", "")
        # Check for key phrases (flexible matching)
        if ("Budget has been increased" in content or
                "$500K" in content or
                "500K" in content.lower() or
                "updated proposal" in content.lower()):
            return True, content
    return False, ""


def verify_task(pdf_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: Open the PDF
    try:
        doc = pymupdf.open(pdf_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {pdf_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        # Precondition: Verify the document has at least 4 pages
        if doc.page_count < 4:
            print(f"CRITICAL: PDF has {doc.page_count} pages, expected at least 4")
            print("REWARD: 0.0")
            return 0.0

        page = doc[PAGE_INDEX]

        # Component 1: StrikeOut annotation over 'Budget allocation is insufficient' on page 4 (0.5 points)
        # This FAILS on initial_env (no annotations) and PASSES on golden_env (has StrikeOut annotation)
        try:
            strikeout_present = check_strikeout_on_target(page, TARGET_SENTENCE)
            if strikeout_present:
                print(f"PASS: Component 1 — StrikeOut annotation found over '{TARGET_SENTENCE}' on page 4 (0.5 pts)")
                total_score += 0.5
            else:
                annots_data = get_page_annotations(page)
                strikeout_annots = [a for a in annots_data if a["type"] == "StrikeOut"]
                if strikeout_annots:
                    print(f"FAIL: Component 1 — StrikeOut annotation exists but does not overlap with '{TARGET_SENTENCE}' (rects: {[str(a['rect']) for a in strikeout_annots]})")
                else:
                    print(f"FAIL: Component 1 — No StrikeOut annotation found on page 4 (expected strikethrough over '{TARGET_SENTENCE}')")
        except Exception as e:
            print(f"ERROR: Component 1 — {e}")

        # Component 2: Sticky note (Text annotation) with budget update message on page 4 (0.5 points)
        # This FAILS on initial_env (no annotations) and PASSES on golden_env (has Text annotation with correct content)
        try:
            found, found_content = check_sticky_note_content(page, STICKY_NOTE_CONTENT)
            if found:
                print(f"PASS: Component 2 — Sticky note with budget update found on page 4 (content: '{found_content[:80]}') (0.5 pts)")
                total_score += 0.5
            else:
                annots_data = get_page_annotations(page)
                text_annots = [a for a in annots_data if a["type"] == "Text"]
                if text_annots:
                    contents = [ta.get("content", "") for ta in text_annots]
                    print(f"FAIL: Component 2 — Text annotation found but content mismatch. Found: {contents}")
                else:
                    print(f"FAIL: Component 2 — No sticky note (Text annotation) found on page 4. Expected: '{STICKY_NOTE_CONTENT}'")
        except Exception as e:
            print(f"ERROR: Component 2 — {e}")

    except Exception as e:
        print(f"ERROR: Unexpected error during verification: {e}")
    finally:
        doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against the canonical PDF path on the VM
if not os.path.exists(PDF_PATH):
    print(f"File not found: {PDF_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(PDF_PATH)
