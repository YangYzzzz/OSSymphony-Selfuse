"""
Reward Script: Remove highlight annotations from PDF while preserving sticky notes and underlines
Task ID: pdf_fm_041
Domain: pdf
Scoring:
  Component 1 (0.50): All highlight annotations removed (0 highlights)
  Component 2 (0.25): Highlights removed AND all 8 sticky notes (Text) preserved
  Component 3 (0.25): Highlights removed AND all 5 underline annotations preserved
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_041'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'group_project.pdf')


def count_annotations_by_type(pdf_path):
    """Count annotations grouped by type across all pages."""
    counts = {}
    try:
        doc = pymupdf.open(pdf_path)
        for i in range(doc.page_count):
            page = doc[i]
            for annot in page.annots():
                atype = annot.type[1]  # e.g. "Highlight", "Text", "Underline"
                counts[atype] = counts.get(atype, 0) + 1
        doc.close()
    except Exception as e:
        print(f"ERROR: Failed to read annotations: {e}")
    return counts


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid PDF
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
        doc.close()
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Count all annotations by type
    annot_counts = count_annotations_by_type(file_path)
    highlight_count = annot_counts.get("Highlight", 0)
    text_count = annot_counts.get("Text", 0)
    underline_count = annot_counts.get("Underline", 0)

    print(f"INFO: Annotation counts: {annot_counts}")
    print(f"INFO: Highlights={highlight_count}, Text(sticky)={text_count}, Underline={underline_count}")

    # Component 1: All highlight annotations removed (0.5 points)
    # This FAILS on initial (15 highlights) and PASSES on golden (0 highlights)
    try:
        if highlight_count == 0:
            print(f"PASS: Component 1 — All highlights removed (0 found) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Expected 0 highlights, found {highlight_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Highlights removed AND all 8 sticky notes preserved (0.25 points)
    # Anchored to highlight removal so it FAILS on initial_env
    try:
        if highlight_count == 0 and text_count == 8:
            print(f"PASS: Component 2 — Highlights removed AND all 8 sticky notes preserved (0.25 pts)")
            total_score += 0.25
        elif highlight_count > 0:
            print(f"FAIL: Component 2 — Highlights not removed ({highlight_count} remain), sticky notes check skipped")
        else:
            print(f"FAIL: Component 2 — Expected 8 sticky notes (Text), found {text_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Highlights removed AND all 5 underline annotations preserved (0.25 points)
    # Anchored to highlight removal so it FAILS on initial_env
    try:
        if highlight_count == 0 and underline_count == 5:
            print(f"PASS: Component 3 — Highlights removed AND all 5 underlines preserved (0.25 pts)")
            total_score += 0.25
        elif highlight_count > 0:
            print(f"FAIL: Component 3 — Highlights not removed ({highlight_count} remain), underline check skipped")
        else:
            print(f"FAIL: Component 3 — Expected 5 underlines, found {underline_count}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
