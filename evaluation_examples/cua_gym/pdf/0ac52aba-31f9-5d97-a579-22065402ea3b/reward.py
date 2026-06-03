"""
Reward Script: Add text annotations for senior partner review comments
Task ID: pdf_legal_067
Domain: pdf
Scoring:
  Component 1 (0.20): Output file exists and is a valid PDF
  Component 2 (0.50): All 5 text annotations present with correct content on correct pages
  Component 3 (0.15): All annotations have author 'Partner Williams'
  Component 4 (0.15): Annotations are positioned at specified coordinates
"""

import os
import sys

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_067'

# Expected annotations: (0-indexed page, x, y, content)
EXPECTED_ANNOTATIONS = [
    (1,  400, 100, 'Representations need strengthening'),
    (4,  400, 300, 'Add material adverse change definition'),
    (7,  400, 150, 'Indemnification cap too low'),
    (11, 400, 400, 'Closing conditions incomplete'),
    (14, 400, 200, 'Escrow terms acceptable'),
]

EXPECTED_AUTHOR = 'Partner Williams'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists and is a valid PDF with annotations (0.20 points)
    # The initial env does NOT have this file, so this scores a task-introduced change.
    try:
        if not os.path.exists(file_path):
            print(f"FAIL: Component 1 — Output file not found: {file_path}")
            print("REWARD: 0.0")
            return 0.0
        doc = pymupdf.open(file_path)
        page_count = len(doc)
        # Collect all annotations across the document
        all_annots = []
        for i in range(page_count):
            page = doc[i]
            if page.annots():
                for a in page.annots():
                    all_annots.append((i, a))
        if len(all_annots) > 0:
            print(f"PASS: Component 1 — Valid PDF with {len(all_annots)} annotations ({page_count} pages) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — PDF has no annotations")
            doc.close()
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
        doc.close()
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Reopen for detailed checks
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot reopen file: {e}")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: All 5 text annotations with correct content on correct pages (0.50 points)
    # Each annotation is worth 0.10 points
    try:
        content_score = 0.0
        for page_idx, x, y, expected_content in EXPECTED_ANNOTATIONS:
            page = doc[page_idx]
            found = False
            if page.annots():
                for annot in page.annots():
                    # Check it's a Text annotation (sticky note) type code 0
                    if annot.type[0] == 0:
                        actual_content = annot.info.get("content", "")
                        if expected_content in actual_content or actual_content in expected_content:
                            found = True
                            break
            if found:
                print(f"PASS: Component 2 — Page {page_idx + 1}: annotation '{expected_content}' found (0.10 pts)")
                content_score += 0.10
            else:
                print(f"FAIL: Component 2 — Page {page_idx + 1}: annotation '{expected_content}' NOT found")
        total_score += content_score
        print(f"  Component 2 subtotal: {content_score:.2f}/0.50")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All annotations have author 'Partner Williams' (0.15 points)
    # Each correct author is worth 0.03 points
    try:
        author_score = 0.0
        for page_idx, x, y, expected_content in EXPECTED_ANNOTATIONS:
            page = doc[page_idx]
            if page.annots():
                for annot in page.annots():
                    if annot.type[0] == 0:
                        actual_content = annot.info.get("content", "")
                        if expected_content in actual_content or actual_content in expected_content:
                            title = annot.info.get("title", "")
                            if title == EXPECTED_AUTHOR:
                                author_score += 0.03
                                print(f"PASS: Component 3 — Page {page_idx + 1}: author is '{title}' (0.03 pts)")
                            else:
                                print(f"FAIL: Component 3 — Page {page_idx + 1}: expected author '{EXPECTED_AUTHOR}', found '{title}'")
                            break
        total_score += author_score
        print(f"  Component 3 subtotal: {author_score:.2f}/0.15")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Annotations positioned at specified coordinates (0.15 points)
    # Each correct position is worth 0.03 points (tolerance of 20 points)
    try:
        pos_score = 0.0
        for page_idx, exp_x, exp_y, expected_content in EXPECTED_ANNOTATIONS:
            page = doc[page_idx]
            if page.annots():
                for annot in page.annots():
                    if annot.type[0] == 0:
                        actual_content = annot.info.get("content", "")
                        if expected_content in actual_content or actual_content in expected_content:
                            rect = annot.rect
                            # Text annotations are placed at a point; rect x0,y0 is the anchor
                            ax, ay = rect.x0, rect.y0
                            dist = ((ax - exp_x) ** 2 + (ay - exp_y) ** 2) ** 0.5
                            if dist < 20:
                                pos_score += 0.03
                                print(f"PASS: Component 4 — Page {page_idx + 1}: position ({ax:.0f},{ay:.0f}) matches expected ({exp_x},{exp_y}) (0.03 pts)")
                            else:
                                print(f"FAIL: Component 4 — Page {page_idx + 1}: position ({ax:.0f},{ay:.0f}) far from expected ({exp_x},{exp_y}), dist={dist:.1f}")
                            break
        total_score += pos_score
        print(f"  Component 4 subtotal: {pos_score:.2f}/0.15")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/legal/ma/acquisition_agreement_reviewed.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
