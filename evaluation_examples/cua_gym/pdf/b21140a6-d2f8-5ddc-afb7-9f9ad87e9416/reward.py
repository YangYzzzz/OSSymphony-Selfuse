"""
Reward Script: Verify annotated PDF with highlight, sticky note, and rectangle annotations
Task ID: pdf_cr_026
Domain: pdf
Scoring:
  - Component 1 (0.15): File exists and has exactly 1 page
  - Component 2 (0.20): Page text contains 'critical path analysis'
  - Component 3 (0.15): At least 3 annotations on page 1
  - Component 4 (0.20): Has a Highlight annotation (type 8)
  - Component 5 (0.15): Has a Text (sticky note) annotation with 'Review this section'
  - Component 6 (0.15): Has a Square/Rect annotation (type 4)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_026'
FILE_PATH = os.path.join(WORKDIR, 'Desktop', 'annotated.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PDF has exactly 1 page (0.15 points)
    try:
        page_count = len(doc)
        if page_count == 1:
            print(f"PASS: Component 1 — PDF has 1 page (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — expected 1 page, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Text contains 'critical path analysis' (0.20 points)
    try:
        page = doc[0]
        text = page.get_text().lower()
        if 'critical path analysis' in text:
            print(f"PASS: Component 2 — text contains 'critical path analysis' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — 'critical path analysis' not found in page text")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Get annotations for components 3-6
    try:
        page = doc[0]
        annots = list(page.annots()) if page.annots() else []
    except Exception as e:
        print(f"ERROR: Could not read annotations: {e}")
        annots = []

    # Component 3: At least 3 annotations (0.15 points)
    try:
        annot_count = len(annots)
        if annot_count >= 3:
            print(f"PASS: Component 3 — {annot_count} annotations found (>= 3) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — expected >= 3 annotations, found {annot_count}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Has Highlight annotation (type 8) (0.20 points)
    try:
        has_highlight = any(a.type[0] == 8 for a in annots)
        if has_highlight:
            print(f"PASS: Component 4 — Highlight annotation found (0.20 pts)")
            total_score += 0.20
        else:
            annot_types = [a.type for a in annots]
            print(f"FAIL: Component 4 — no Highlight annotation found. Types present: {annot_types}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Has Text (sticky note) with 'Review this section' (0.15 points)
    try:
        has_sticky = False
        for a in annots:
            if a.type[0] == 0:  # Text annotation (sticky note)
                content = a.info.get('content', '')
                if 'review this section' in content.lower():
                    has_sticky = True
                    break
        if has_sticky:
            print(f"PASS: Component 5 — Text annotation with 'Review this section' found (0.15 pts)")
            total_score += 0.15
        else:
            # Show what we did find
            text_annots = [(a.type, a.info.get('content', '')) for a in annots if a.type[0] == 0]
            print(f"FAIL: Component 5 — no Text annotation with 'Review this section'. Text annots: {text_annots}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Has Square/Rect annotation (type 4) (0.15 points)
    try:
        has_square = any(a.type[0] == 4 for a in annots)
        if has_square:
            print(f"PASS: Component 6 — Square/Rect annotation found (0.15 pts)")
            total_score += 0.15
        else:
            annot_types = [a.type for a in annots]
            print(f"FAIL: Component 6 — no Square annotation found. Types present: {annot_types}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
