#!/usr/bin/env python3
"""
reward.py for pdf_basic_137

Task: Open ~/Desktop/interview_questions.pdf in Evince, navigate to page 5,
highlight the text 'Tell me about a time' in green, and add a sticky note
saying 'Prepare STAR method response'. Save the document.

Scoring rubric (0.0 – 1.0):
  Component 1 (0.10): File ~/Desktop/interview_questions.pdf exists and is readable.
  Component 2 (0.10): File has been saved/modified (mtime newer than initial OR annotations present).
  Component 3 (0.10): PDF has exactly 8 pages (no pages added/removed).
  Component 4 (0.30): A green highlight annotation covers the text 'Tell me about a time' on page 5.
  Component 5 (0.25): A sticky-note (Text) annotation with content 'Prepare STAR method response'
                      exists on page 5 (or anywhere in the document as fallback).
  Component 6 (0.15): The original text content on page 5 is preserved (not corrupted).
"""

import os
import sys
import re

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _open_doc(path):
    """Open a PDF and return the doc object, or None on failure."""
    try:
        doc = pymupdf.open(path)
        return doc
    except Exception as e:
        print(f"  Error opening {path}: {e}")
        return None


def _get_annotations(doc, page_idx):
    """Return list of annotation property dicts for a given page index."""
    page = doc[page_idx]
    result = []
    for annot in page.annots():
        colors = annot.colors
        result.append({
            "type": annot.type[1],       # e.g. "Highlight", "Text", "FreeText"
            "type_code": annot.type[0],
            "content": annot.info.get("content", ""),
            "rect": tuple(annot.rect),
            "stroke": colors.get("stroke"),
            "fill": colors.get("fill"),
        })
    return result


def _color_is_green(color_tuple, tolerance=0.15):
    """
    Check whether a colour tuple (r, g, b) – values 0-1 – looks green.
    Green is defined as: g component is dominant and r/b are low.
    """
    if color_tuple is None or len(color_tuple) < 3:
        return False
    r, g, b = color_tuple[0], color_tuple[1], color_tuple[2]
    # Pure green: (0, 1, 0)
    # Allow significant tolerance for viewer-specific colour representations.
    # Must be noticeably greener than red and blue.
    return (
        g > 0.4
        and g > r + tolerance
        and g > b + tolerance
    )


def _highlight_covers_text(doc, page_idx, search_text):
    """
    Check whether any Highlight annotation on `page_idx` overlaps with the
    bounding box of `search_text`.  Returns (found_highlight, is_green).
    """
    page = doc[page_idx]
    text_instances = page.search_for(search_text)
    if not text_instances:
        return False, False

    for annot in page.annots():
        if annot.type[1] != "Highlight":
            continue
        a_rect = annot.rect
        for inst in text_instances:
            if a_rect.intersects(inst):
                # Found a highlight over the text — check colour
                colors = annot.colors
                stroke = colors.get("stroke")
                is_green = _color_is_green(stroke)
                return True, is_green

    return False, False


def _sticky_note_exists(doc, expected_content, page_idx=None):
    """
    Return True if a 'Text' (sticky-note) annotation with content containing
    `expected_content` exists.  If page_idx is given, check only that page;
    otherwise check all pages.
    """
    pages = [doc[page_idx]] if page_idx is not None else list(doc)
    for page in pages:
        for annot in page.annots():
            if annot.type[1] == "Text":
                content = annot.info.get("content", "")
                if expected_content in content:
                    return True
    return False


# ---------------------------------------------------------------------------
# Main scoring
# ---------------------------------------------------------------------------

def main():
    pdf_path = os.path.expanduser("~/Desktop/interview_questions.pdf")
    target_page_idx = 4      # page 5 is index 4 (0-based)
    target_text = "Tell me about a time"
    sticky_text = "Prepare STAR method response"

    score = 0.0

    # -------------------------------------------------------------------
    # Component 1: File exists and is readable (0.10)
    # -------------------------------------------------------------------
    if not os.path.exists(pdf_path):
        print(f"FAIL Component 1: {pdf_path} does not exist")
        print(f"REWARD: 0.0")
        return

    doc = _open_doc(pdf_path)
    if doc is None:
        print("FAIL Component 1: Cannot open interview_questions.pdf")
        print(f"REWARD: 0.0")
        return

    score += 0.10
    print("PASS Component 1: interview_questions.pdf exists and is readable")

    # -------------------------------------------------------------------
    # Component 2: File has been modified / annotations present (0.10)
    # -------------------------------------------------------------------
    all_annots = []
    for i in range(doc.page_count):
        all_annots.extend(_get_annotations(doc, i))

    if len(all_annots) > 0:
        score += 0.10
        print(f"PASS Component 2: Document has {len(all_annots)} annotation(s) — file was modified")
    else:
        print("FAIL Component 2: No annotations found — document may not have been modified")

    # -------------------------------------------------------------------
    # Component 3: Page count is exactly 8 (0.10)
    # -------------------------------------------------------------------
    page_count = doc.page_count
    if page_count == 8:
        score += 0.10
        print("PASS Component 3: Page count is 8")
    else:
        print(f"FAIL Component 3: Expected 8 pages, got {page_count}")

    # -------------------------------------------------------------------
    # Component 4: Green highlight over 'Tell me about a time' on page 5 (0.30)
    # -------------------------------------------------------------------
    if page_count > target_page_idx:
        found_hl, is_green = _highlight_covers_text(doc, target_page_idx, target_text)
        if found_hl and is_green:
            score += 0.30
            print(f"PASS Component 4: Green highlight found over '{target_text}' on page 5")
        elif found_hl and not is_green:
            # Partial credit: highlight exists but wrong colour
            score += 0.15
            print(f"PARTIAL Component 4: Highlight found over '{target_text}' on page 5, "
                  f"but colour is not green (partial credit 0.15)")
        else:
            # Try a partial match — maybe only part of the phrase is highlighted
            partial_phrase = "Tell me about"
            found_partial, is_green_partial = _highlight_covers_text(
                doc, target_page_idx, partial_phrase
            )
            if found_partial and is_green_partial:
                score += 0.15
                print(f"PARTIAL Component 4: Green highlight found over partial text '{partial_phrase}' "
                      f"on page 5 (partial credit 0.15)")
            else:
                print(f"FAIL Component 4: No highlight annotation found over '{target_text}' on page 5")
    else:
        print(f"FAIL Component 4: Document has fewer than 5 pages — cannot check page 5")

    # -------------------------------------------------------------------
    # Component 5: Sticky note 'Prepare STAR method response' on page 5 (0.25)
    # -------------------------------------------------------------------
    # First try page 5 specifically, then fall back to any page
    sticky_on_p5 = _sticky_note_exists(doc, sticky_text, page_idx=target_page_idx)
    sticky_anywhere = _sticky_note_exists(doc, sticky_text)

    if sticky_on_p5:
        score += 0.25
        print(f"PASS Component 5: Sticky note '{sticky_text}' found on page 5")
    elif sticky_anywhere:
        score += 0.15
        print(f"PARTIAL Component 5: Sticky note '{sticky_text}' found on a different page "
              f"(expected page 5) — partial credit 0.15")
    else:
        # Try case-insensitive / partial match
        pages_to_check = list(range(doc.page_count))
        partial_found = False
        for pi in pages_to_check:
            page = doc[pi]
            for annot in page.annots():
                if annot.type[1] == "Text":
                    content = annot.info.get("content", "").lower()
                    if "star" in content or "prepare" in content:
                        partial_found = True
                        break
            if partial_found:
                break
        if partial_found:
            score += 0.10
            print(f"PARTIAL Component 5: Found a sticky note with related content "
                  f"(but not exact match '{sticky_text}') — partial credit 0.10")
        else:
            print(f"FAIL Component 5: No sticky note containing '{sticky_text}' found")

    # -------------------------------------------------------------------
    # Component 6: Original text content on page 5 preserved (0.15)
    # -------------------------------------------------------------------
    if page_count > target_page_idx:
        p5_text = doc[target_page_idx].get_text("text")
        # The target phrase itself must still be present
        if target_text in p5_text and "Behavioral Interview" in p5_text:
            score += 0.15
            print("PASS Component 6: Original text content on page 5 is preserved")
        elif target_text in p5_text:
            score += 0.10
            print("PARTIAL Component 6: Target text present but page content may be altered (0.10)")
        else:
            print("FAIL Component 6: Original text content on page 5 appears to be corrupted/missing")
    else:
        print("FAIL Component 6: Cannot check page 5 content — not enough pages")

    doc.close()

    # -------------------------------------------------------------------
    # Final score
    # -------------------------------------------------------------------
    final_reward = round(min(score, 1.0), 2)
    print(f"\nTotal score: {final_reward}")
    print(f"REWARD: {final_reward}")


if __name__ == "__main__":
    main()
