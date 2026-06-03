"""
Reward Script: Highlight annotations for contract review
Task ID: pdf_legal_031
Domain: pdf
Scoring:
  Component 1: Yellow highlights on 'Tenant' instances (0.35 pts)
  Component 2: Green highlights on 'Landlord' instances (0.35 pts)
  Component 3: Red highlights on 'Default' instances (0.30 pts)
"""

import os

try:
    import fitz  # PyMuPDF
except ImportError:
    import pymupdf as fitz

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_031'

# Expected colors (RGB floats)
YELLOW = (1.0, 1.0, 0.0)
GREEN = (0.0, 1.0, 0.0)
RED = (1.0, 0.0, 0.0)

COLOR_TOLERANCE = 0.1  # tolerance for color matching


def color_matches(actual, expected, tol=COLOR_TOLERANCE):
    """Check if an RGB color tuple matches expected within tolerance."""
    if actual is None or len(actual) < 3:
        return False
    return all(abs(a - e) < tol for a, e in zip(actual, expected))


def count_highlights_on_text(doc, search_term, expected_color):
    """
    Count how many highlight annotations with the expected color
    overlap with instances of search_term across all pages.
    Returns (matched_count, total_text_instances).
    """
    total_text_instances = 0
    matched_count = 0

    for page in doc:
        text_rects = page.search_for(search_term)
        total_text_instances += len(text_rects)

        # Track which text instances have been matched to avoid double counting
        matched_texts = set()

        annots = page.annots()
        if annots is None:
            continue

        for annot in annots:
            if annot.type[1] != "Highlight":
                continue
            stroke = annot.colors.get("stroke")
            if not color_matches(stroke, expected_color):
                continue
            # Check overlap with text instances
            arect = annot.rect
            for idx, trect in enumerate(text_rects):
                if idx not in matched_texts and arect.intersects(trect):
                    matched_count += 1
                    matched_texts.add(idx)
                    break  # one annot can match one text instance

    return matched_count, total_text_instances


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: file must exist and be loadable
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Yellow highlights on 'Tenant' (0.35 points)
    try:
        matched, total = count_highlights_on_text(doc, "Tenant", YELLOW)
        if total > 0 and matched > 0:
            # Progressive: partial credit based on coverage ratio
            ratio = matched / total
            points = 0.35 * ratio
            if ratio > 0:
                total_score += points
            print(f"PASS: Component 1 — Yellow highlights on 'Tenant': {matched}/{total} instances ({points:.3f} pts)")
        elif total == 0:
            print(f"FAIL: Component 1 — No 'Tenant' text found in PDF")
        else:
            print(f"FAIL: Component 1 — No yellow highlights on 'Tenant' (0/{total} instances)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Green highlights on 'Landlord' (0.35 points)
    try:
        matched, total = count_highlights_on_text(doc, "Landlord", GREEN)
        if total > 0 and matched > 0:
            ratio = matched / total
            points = 0.35 * ratio
            if ratio > 0:
                total_score += points
            print(f"PASS: Component 2 — Green highlights on 'Landlord': {matched}/{total} instances ({points:.3f} pts)")
        elif total == 0:
            print(f"FAIL: Component 2 — No 'Landlord' text found in PDF")
        else:
            print(f"FAIL: Component 2 — No green highlights on 'Landlord' (0/{total} instances)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Red highlights on 'Default' (0.30 points)
    try:
        matched, total = count_highlights_on_text(doc, "Default", RED)
        if total > 0 and matched > 0:
            ratio = matched / total
            points = 0.30 * ratio
            if ratio > 0:
                total_score += points
            print(f"PASS: Component 3 — Red highlights on 'Default': {matched}/{total} instances ({points:.3f} pts)")
        elif total == 0:
            print(f"FAIL: Component 3 — No 'Default' text found in PDF")
        else:
            print(f"FAIL: Component 3 — No red highlights on 'Default' (0/{total} instances)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.3f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/legal/lease_agreement_reviewed.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
