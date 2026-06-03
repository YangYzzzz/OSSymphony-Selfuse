"""
Reward Script: Highlight all instances of 'transformer' in blue in a PDF
Task ID: pdf_fm_022
Domain: pdf (libreoffice_calc label but actually PDF task)
Scoring:
  Component 1 (0.3): At least 20 highlight annotations exist in the PDF
  Component 2 (0.3): All highlight annotations use blue color
  Component 3 (0.4): Highlights overlap with 'transformer' text instances (>=25 of 28)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_022'
PDF_PATH = os.path.join(WORKDIR, 'Documents', 'research', 'paper_ml_2025.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("CRITICAL: PyMuPDF (fitz) not available")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all highlight annotations across all pages
    all_highlights = []  # list of (page_idx, annot_rect, stroke_color)
    try:
        for page_idx in range(len(doc)):
            page = doc[page_idx]
            if page.annots():
                for annot in page.annots():
                    if annot.type[1] == "Highlight":
                        stroke = annot.colors.get("stroke")
                        all_highlights.append((page_idx, annot.rect, stroke))
    except Exception as e:
        print(f"ERROR: Failed to enumerate annotations: {e}")

    highlight_count = len(all_highlights)
    print(f"INFO: Found {highlight_count} highlight annotations total")

    # Component 1: At least 20 highlight annotations exist (0.3 points)
    # The task requires 28 highlights for all 'transformer' instances.
    # We use 20 as threshold for this component to allow minor misses.
    try:
        if highlight_count >= 20:
            print(f"PASS: Component 1 — {highlight_count} highlight annotations found (>=20) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Only {highlight_count} highlights found, expected >=20")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All highlight annotations use blue color (0.3 points)
    # Blue = stroke color close to (0, 0, 1) with tolerance
    try:
        if highlight_count == 0:
            print("FAIL: Component 2 — No highlights to check color")
        else:
            blue_count = 0
            for page_idx, rect, stroke in all_highlights:
                if stroke is not None and len(stroke) >= 3:
                    r, g, b = stroke[0], stroke[1], stroke[2]
                    # Blue: high blue channel, low red and green
                    if b > 0.6 and r < 0.4 and g < 0.4:
                        blue_count += 1
            blue_ratio = blue_count / highlight_count
            if blue_ratio >= 0.9:
                print(f"PASS: Component 2 — {blue_count}/{highlight_count} highlights are blue ({blue_ratio:.1%}) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Only {blue_count}/{highlight_count} highlights are blue ({blue_ratio:.1%}), need >=90%")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Highlights overlap with 'transformer' text instances (0.4 points)
    # Find all case-insensitive 'transformer' instances across all pages
    # and check how many have an overlapping highlight annotation.
    try:
        total_text_instances = 0
        covered_instances = 0

        for page_idx in range(len(doc)):
            page = doc[page_idx]
            # search_for is case-insensitive by default in PyMuPDF
            text_rects = page.search_for("transformer")
            total_text_instances += len(text_rects)

            # Get highlights on this page
            page_highlights = [(rect, stroke) for (pidx, rect, stroke) in all_highlights if pidx == page_idx]

            for text_rect in text_rects:
                # Check if any highlight overlaps this text instance
                for h_rect, _ in page_highlights:
                    if h_rect.intersects(text_rect):
                        covered_instances += 1
                        break

        print(f"INFO: {covered_instances}/{total_text_instances} 'transformer' instances have overlapping highlights")

        if total_text_instances == 0:
            print("FAIL: Component 3 — No 'transformer' text found in PDF")
        else:
            coverage_ratio = covered_instances / total_text_instances
            # Award full points if >= 25/28 (~89%) instances are covered
            if coverage_ratio >= 0.89:
                print(f"PASS: Component 3 — {covered_instances}/{total_text_instances} instances covered ({coverage_ratio:.1%}) (0.4 pts)")
                total_score += 0.4
            elif coverage_ratio >= 0.5:
                # Partial credit: proportional between 0.5 and 0.89 coverage
                partial = 0.4 * (coverage_ratio - 0.5) / (0.89 - 0.5)
                print(f"PARTIAL: Component 3 — {covered_instances}/{total_text_instances} instances covered ({coverage_ratio:.1%}) ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — Only {covered_instances}/{total_text_instances} instances covered ({coverage_ratio:.1%})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(PDF_PATH):
    print(f"File not found: {PDF_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(PDF_PATH)
