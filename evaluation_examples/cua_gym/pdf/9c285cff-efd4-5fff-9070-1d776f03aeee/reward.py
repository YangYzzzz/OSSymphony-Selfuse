"""
Reward Script: Add squiggly underline annotations under all 'shall' and 'must' instances
Task ID: pdf_legal_053
Domain: pdf
Scoring:
  Component 1 (0.1): Output file exists at expected path
  Component 2 (0.2): All annotations are Squiggly type (no other annotation types)
  Component 3 (0.4): Total squiggly annotation count is 67 (45 'shall' + 22 'must')
  Component 4 (0.3): Annotations overlap with actual 'shall'/'must' text positions
"""

import os
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    import pymupdf as fitz

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_053'
OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'compliance', 'regulatory_filing_flagged.pdf')
SOURCE_PATH = os.path.join(WORKDIR, 'legal', 'compliance', 'regulatory_filing.pdf')

EXPECTED_SQUIGGLY_COUNT = 67  # 45 'shall' + 22 'must'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists at correct path (0.1 points)
    # This is a task-introduced change: the flagged PDF must be created by the agent.
    try:
        if os.path.exists(OUTPUT_PATH) and os.path.getsize(OUTPUT_PATH) > 0:
            print(f"PASS: Component 1 — Output file exists at {OUTPUT_PATH} (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — Output file not found or empty at {OUTPUT_PATH}")
            print(f"REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"REWARD: 0.0")
        return 0.0

    # Load the output PDF
    try:
        doc = fitz.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open output PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all annotations across all pages
    all_annots = []
    annot_type_counts = {}
    try:
        for i in range(len(doc)):
            page = doc[i]
            if page.annots():
                for annot in page.annots():
                    atype = annot.type[1]
                    annot_type_counts[atype] = annot_type_counts.get(atype, 0) + 1
                    all_annots.append({
                        'page': i,
                        'type': atype,
                        'rect': annot.rect,
                    })
    except Exception as e:
        print(f"ERROR: Failed to enumerate annotations: {e}")

    squiggly_count = annot_type_counts.get('Squiggly', 0)
    total_annot_count = sum(annot_type_counts.values())
    print(f"INFO: Found {total_annot_count} total annotations, {squiggly_count} Squiggly")
    print(f"INFO: Annotation type breakdown: {annot_type_counts}")

    # Component 2: All annotations are Squiggly type (0.2 points)
    # The task only asks for squiggly underlines; any other annotation type is wrong.
    try:
        non_squiggly = total_annot_count - squiggly_count
        if squiggly_count > 0 and non_squiggly == 0:
            print(f"PASS: Component 2 — All {squiggly_count} annotations are Squiggly type (0.2 pts)")
            total_score += 0.2
        elif squiggly_count > 0 and non_squiggly > 0:
            # Partial: some squiggly exist but also other types
            ratio = squiggly_count / total_annot_count
            partial = round(0.2 * ratio, 2)
            print(f"PARTIAL: Component 2 — {squiggly_count}/{total_annot_count} are Squiggly ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No Squiggly annotations found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Total squiggly annotation count matches expected (0.4 points)
    # Expected: 67 (45 'shall' + 22 'must'). Award partial credit for being close.
    try:
        if squiggly_count == EXPECTED_SQUIGGLY_COUNT:
            print(f"PASS: Component 3 — Squiggly count is exactly {EXPECTED_SQUIGGLY_COUNT} (0.4 pts)")
            total_score += 0.4
        elif squiggly_count > 0:
            # Partial credit: proportional to how close to expected
            ratio = min(squiggly_count, EXPECTED_SQUIGGLY_COUNT) / EXPECTED_SQUIGGLY_COUNT
            # Penalize over-counting too
            if squiggly_count > EXPECTED_SQUIGGLY_COUNT:
                over_ratio = EXPECTED_SQUIGGLY_COUNT / squiggly_count
                ratio = ratio * over_ratio
            partial = round(0.4 * ratio, 2)
            print(f"PARTIAL: Component 3 — Found {squiggly_count} Squiggly (expected {EXPECTED_SQUIGGLY_COUNT}), ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No Squiggly annotations found (expected {EXPECTED_SQUIGGLY_COUNT})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Annotations overlap with actual 'shall'/'must' text (0.3 points)
    # Sample annotations and verify they are placed over 'shall' or 'must' text.
    try:
        squiggly_annots = [a for a in all_annots if a['type'] == 'Squiggly']
        if len(squiggly_annots) == 0:
            print(f"FAIL: Component 4 — No Squiggly annotations to verify text overlap")
        else:
            overlap_count = 0
            checked = 0
            for annot_info in squiggly_annots:
                page = doc[annot_info['page']]
                rect = annot_info['rect']
                # Extract text under the annotation rectangle
                text = page.get_text('text', clip=rect).strip().lower()
                if 'shall' in text or 'must' in text:
                    overlap_count += 1
                checked += 1

            if checked > 0:
                overlap_ratio = overlap_count / checked
                if overlap_ratio >= 0.9:
                    print(f"PASS: Component 4 — {overlap_count}/{checked} annotations overlap with 'shall'/'must' text (0.3 pts)")
                    total_score += 0.3
                elif overlap_ratio > 0.0:
                    partial = round(0.3 * overlap_ratio, 2)
                    print(f"PARTIAL: Component 4 — {overlap_count}/{checked} annotations overlap ({partial} pts)")
                    total_score += partial
                else:
                    print(f"FAIL: Component 4 — 0/{checked} annotations overlap with 'shall'/'must' text")
            else:
                print(f"FAIL: Component 4 — No annotations checked")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
