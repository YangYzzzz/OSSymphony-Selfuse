"""
Reward Script for pdf_basic_133
Task: Open ~/Desktop/safety_data_sheet.pdf in Evince, navigate to page 3,
      add a red highlight over 'DANGER: Highly flammable', add an underline
      to 'Keep away from heat sources' on the same page. Save the document.

Scoring rubric (total = 1.0):
  Component 1 (0.50): Red highlight annotation over 'DANGER: Highly flammable' on page 3
                       - 0.50 for red highlight; 0.25 for non-red highlight
  Component 2 (0.50): Underline annotation over 'Keep away from heat sources' on page 3

The file existence and page count checks are prerequisites (early exit at 0.0).
The score is purely based on whether the required annotations are present and correct.
The initial state (no annotations) scores 0.0; the golden state (with annotations) scores 1.0.
"""

import os
import sys

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

DESKTOP = os.path.expanduser("~/Desktop")
PDF_PATH = os.path.join(DESKTOP, "safety_data_sheet.pdf")


def _open_pdf(path):
    """Open a PDF; return None on failure."""
    try:
        return pymupdf.open(path)
    except Exception as exc:
        print(f"  ERROR opening {path}: {exc}")
        return None


def verify_task():
    """Verify task completion with progressive scoring. Returns 0.0–1.0."""
    total_score = 0.0

    # ---- Prerequisite: File exists ----
    if not os.path.exists(PDF_PATH):
        print(f"FAIL prerequisite: safety_data_sheet.pdf not found at {PDF_PATH}")
        print(f"REWARD: {total_score}")
        return total_score

    # ---- Prerequisite: Valid PDF ----
    doc = _open_pdf(PDF_PATH)
    if doc is None:
        print("FAIL prerequisite: Could not open PDF (corrupted or invalid)")
        print(f"REWARD: {total_score}")
        return total_score

    page_count = doc.page_count
    if page_count < 3:
        print(f"FAIL prerequisite: PDF has only {page_count} pages, need at least 3")
        doc.close()
        print(f"REWARD: {total_score}")
        return total_score

    file_size = os.path.getsize(PDF_PATH)
    print(f"OK: safety_data_sheet.pdf exists ({file_size} bytes, {page_count} pages)")

    page3 = doc[2]  # 0-indexed; page 3 is index 2

    # ---- Verify target text exists on page 3 (diagnostic only, no score) ----
    page3_text = page3.get_text()
    has_danger = "DANGER: Highly flammable" in page3_text
    has_keep = "Keep away from heat sources" in page3_text
    print(f"Diagnostic: 'DANGER: Highly flammable' on page 3: {has_danger}")
    print(f"Diagnostic: 'Keep away from heat sources' on page 3: {has_keep}")

    # ------ Component 1: Red highlight over 'DANGER: Highly flammable' (0.50) ------
    highlight_score = 0.0

    danger_instances = page3.search_for("DANGER: Highly flammable")
    if not danger_instances:
        print(f"FAIL Component 1: 'DANGER: Highly flammable' not found in searchable text on page 3")
    else:
        highlight_found = False
        highlight_is_red = False

        for annot in page3.annots():
            if annot.type[1] != "Highlight":
                continue

            annot_rect = annot.rect
            for text_rect in danger_instances:
                if annot_rect.intersects(text_rect):
                    highlight_found = True
                    stroke = annot.colors.get("stroke")
                    if stroke and len(stroke) >= 3:
                        r, g, b = stroke[0], stroke[1], stroke[2]
                        # Red: high R (>0.7), low G (<0.3), low B (<0.3)
                        if r > 0.7 and g < 0.3 and b < 0.3:
                            highlight_is_red = True
                    break

        if highlight_found and highlight_is_red:
            print(f"PASS Component 1: Red highlight found over 'DANGER: Highly flammable' (+0.50)")
            highlight_score = 0.50
        elif highlight_found:
            # Highlight exists but wrong color — partial credit
            print(f"PARTIAL Component 1: Highlight found over 'DANGER: Highly flammable' but not red (+0.25)")
            for annot in page3.annots():
                if annot.type[1] == "Highlight":
                    for di in danger_instances:
                        if annot.rect.intersects(di):
                            print(f"  Actual highlight color: stroke={annot.colors.get('stroke')}")
            highlight_score = 0.25
        else:
            print(f"FAIL Component 1: No highlight annotation over 'DANGER: Highly flammable' on page 3")
            all_annots = list(page3.annots())
            print(f"  All annotations on page 3: {len(all_annots)}")
            for a in all_annots:
                print(f"    type={a.type[1]}, rect={tuple(a.rect)}, colors={a.colors}")

    total_score += highlight_score

    # ------ Component 2: Underline over 'Keep away from heat sources' (0.50) ------
    underline_score = 0.0

    keep_instances = page3.search_for("Keep away from heat sources")
    if not keep_instances:
        print(f"FAIL Component 2: 'Keep away from heat sources' not found in searchable text on page 3")
    else:
        underline_found = False

        for annot in page3.annots():
            if annot.type[1] != "Underline":
                continue

            annot_rect = annot.rect
            for text_rect in keep_instances:
                if annot_rect.intersects(text_rect):
                    underline_found = True
                    break

        if underline_found:
            print(f"PASS Component 2: Underline annotation found over 'Keep away from heat sources' (+0.50)")
            underline_score = 0.50
        else:
            print(f"FAIL Component 2: No underline annotation over 'Keep away from heat sources' on page 3")
            all_annots = list(page3.annots())
            print(f"  Annotations on page 3:")
            for a in all_annots:
                print(f"    type={a.type[1]}, rect={tuple(a.rect)}")

    total_score += underline_score

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nTotal score: {final_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
