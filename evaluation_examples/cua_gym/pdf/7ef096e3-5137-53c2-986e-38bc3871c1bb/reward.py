"""
Reward Script: Highlight every occurrence of 'liability' in insurance_policy.pdf with yellow highlight
Task ID: pdf_fm_023
Domain: pdf
Scoring:
  Component 1 (0.3): Highlight annotations exist on the PDF (> 0 highlights added)
  Component 2 (0.4): Every occurrence of 'liability' has a corresponding highlight annotation
  Component 3 (0.3): All highlight annotations use yellow color (stroke ~[1,1,0])
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_023'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'legal', 'insurance_policy.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import fitz
    except ImportError:
        try:
            import pymupdf as fitz
        except ImportError:
            print("CRITICAL: Neither fitz nor pymupdf importable")
            print("REWARD: 0.0")
            return 0.0

    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Count all 'liability' occurrences and highlight annotations across all pages
    total_liability_occurrences = 0
    total_highlight_annots = 0
    total_non_highlight_annots = 0
    yellow_highlights = 0
    non_yellow_highlights = 0
    highlighted_liability_count = 0

    for page_num in range(len(doc)):
        page = doc[page_num]

        # Count liability text occurrences on this page
        liability_instances = page.search_for('liability')
        total_liability_occurrences += len(liability_instances)

        # Count annotations on this page
        annots = list(page.annots()) if page.annots() else []
        highlights = [a for a in annots if a.type[1] == 'Highlight']
        total_highlight_annots += len(highlights)
        total_non_highlight_annots += len(annots) - len(highlights)

        # Check color of each highlight
        for annot in highlights:
            stroke = annot.colors.get('stroke', [])
            if stroke and len(stroke) >= 3:
                r, g, b = stroke[0], stroke[1], stroke[2]
                if abs(r - 1.0) < 0.1 and abs(g - 1.0) < 0.1 and abs(b - 0.0) < 0.1:
                    yellow_highlights += 1
                else:
                    non_yellow_highlights += 1
            else:
                non_yellow_highlights += 1

        # Check how many liability occurrences have overlapping highlight annotations
        for inst_rect in liability_instances:
            for annot in highlights:
                if annot.rect.intersects(inst_rect):
                    highlighted_liability_count += 1
                    break

    doc.close()

    print(f"INFO: Total 'liability' occurrences: {total_liability_occurrences}")
    print(f"INFO: Total highlight annotations: {total_highlight_annots}")
    print(f"INFO: Highlighted liability instances: {highlighted_liability_count}")
    print(f"INFO: Yellow highlights: {yellow_highlights}, Non-yellow: {non_yellow_highlights}")

    # Component 1: Highlight annotations exist (0.3 points)
    # This checks that the task added highlight annotations at all.
    # Initial PDF has 0 annotations, so this only passes on golden.
    try:
        if total_highlight_annots > 0:
            print(f"PASS: Component 1 — {total_highlight_annots} highlight annotations found (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No highlight annotations found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Every 'liability' occurrence is highlighted (0.4 points)
    # Award proportional partial credit based on coverage.
    # Initial PDF has 0 highlights so coverage = 0.
    try:
        if total_liability_occurrences > 0:
            coverage = highlighted_liability_count / total_liability_occurrences
            if coverage >= 0.99:
                print(f"PASS: Component 2 — All {highlighted_liability_count}/{total_liability_occurrences} occurrences highlighted (0.4 pts)")
                total_score += 0.4
            elif coverage > 0:
                partial = round(0.4 * coverage, 2)
                print(f"PARTIAL: Component 2 — {highlighted_liability_count}/{total_liability_occurrences} occurrences highlighted ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — 0/{total_liability_occurrences} occurrences highlighted")
        else:
            print(f"FAIL: Component 2 — No 'liability' text found in PDF")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All highlights are yellow (0.3 points)
    # Award proportional credit. Initial has 0 highlights so this scores 0.
    try:
        if total_highlight_annots > 0:
            yellow_ratio = yellow_highlights / total_highlight_annots
            if yellow_ratio >= 0.99:
                print(f"PASS: Component 3 — All {yellow_highlights}/{total_highlight_annots} highlights are yellow (0.3 pts)")
                total_score += 0.3
            elif yellow_ratio > 0:
                partial = round(0.3 * yellow_ratio, 2)
                print(f"PARTIAL: Component 3 — {yellow_highlights}/{total_highlight_annots} highlights are yellow ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — No yellow highlights (0/{total_highlight_annots})")
        else:
            print(f"FAIL: Component 3 — No highlights to check color on")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
