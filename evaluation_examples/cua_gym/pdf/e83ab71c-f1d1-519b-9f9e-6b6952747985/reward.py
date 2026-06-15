"""
Reward Script: Add underline annotations (red) under WARNING/CAUTION and yellow highlights over DANGER
Task ID: pdf_ro_024
Domain: pdf
Scoring:
  - Component 1: Underline annotations over WARNING occurrences (0.30)
  - Component 2: Underline annotations over CAUTION occurrences (0.20)
  - Component 3: Underline annotations are red (0.15)
  - Component 4: Highlight annotations over DANGER occurrences (0.20)
  - Component 5: Highlights are yellow (0.10)
  - Component 6: No spurious annotations -- total ~35 (0.05)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_024'
FILE_PATH = os.path.join(WORKDIR, 'safety', 'manual_marked.pdf')

EXPECTED_WARNING = 18
EXPECTED_CAUTION = 12
EXPECTED_DANGER = 5
EXPECTED_TOTAL_ANNOTS = EXPECTED_WARNING + EXPECTED_CAUTION + EXPECTED_DANGER  # 35


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: load the file
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Gather all annotation data across all pages
    underline_over_warning = 0
    underline_over_caution = 0
    highlight_over_danger = 0
    total_underlines = 0
    total_highlights = 0
    total_annotations = 0
    red_underlines = 0
    yellow_highlights = 0

    try:
        for i in range(doc.page_count):
            page = doc[i]
            warning_rects = page.search_for('WARNING')
            caution_rects = page.search_for('CAUTION')
            danger_rects = page.search_for('DANGER')

            for annot in page.annots():
                total_annotations += 1
                atype = annot.type[1]
                arect = annot.rect
                stroke = annot.colors.get('stroke', [])

                if atype == 'Underline':
                    total_underlines += 1

                    # Check if red (stroke ~= (1, 0, 0))
                    if stroke and len(stroke) >= 3:
                        if (abs(stroke[0] - 1.0) < 0.1 and
                                abs(stroke[1] - 0.0) < 0.1 and
                                abs(stroke[2] - 0.0) < 0.1):
                            red_underlines += 1

                    # Check overlap with WARNING
                    matched_warning = False
                    for wr in warning_rects:
                        if arect.intersects(wr):
                            underline_over_warning += 1
                            matched_warning = True
                            break

                    # Check overlap with CAUTION (only if not matched WARNING)
                    if not matched_warning:
                        for cr in caution_rects:
                            if arect.intersects(cr):
                                underline_over_caution += 1
                                break

                elif atype == 'Highlight':
                    total_highlights += 1

                    # Check if yellow (stroke ~= (1, 1, 0))
                    if stroke and len(stroke) >= 3:
                        if (abs(stroke[0] - 1.0) < 0.1 and
                                abs(stroke[1] - 1.0) < 0.1 and
                                abs(stroke[2] - 0.0) < 0.1):
                            yellow_highlights += 1

                    # Check overlap with DANGER
                    for dr in danger_rects:
                        if arect.intersects(dr):
                            highlight_over_danger += 1
                            break

    except Exception as e:
        print(f"ERROR: Failed during annotation scan: {e}")
        print("REWARD: 0.0")
        doc.close()
        return 0.0

    doc.close()

    # Component 1: Underline annotations over WARNING occurrences (0.30 points)
    # Proportional scoring based on how many of 18 are covered
    try:
        if EXPECTED_WARNING > 0 and underline_over_warning > 0:
            ratio = min(underline_over_warning / EXPECTED_WARNING, 1.0)
            pts = round(0.30 * ratio, 4)
            print(f"PASS: Component 1 -- Underlines over WARNING: {underline_over_warning}/{EXPECTED_WARNING} ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 1 -- Underlines over WARNING: {underline_over_warning}/{EXPECTED_WARNING}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Underline annotations over CAUTION occurrences (0.20 points)
    try:
        if EXPECTED_CAUTION > 0 and underline_over_caution > 0:
            ratio = min(underline_over_caution / EXPECTED_CAUTION, 1.0)
            pts = round(0.20 * ratio, 4)
            print(f"PASS: Component 2 -- Underlines over CAUTION: {underline_over_caution}/{EXPECTED_CAUTION} ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 2 -- Underlines over CAUTION: {underline_over_caution}/{EXPECTED_CAUTION}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Underline annotations are red (0.15 points)
    # All underlines should be red
    try:
        expected_total_underlines = EXPECTED_WARNING + EXPECTED_CAUTION  # 30
        if total_underlines > 0 and red_underlines > 0:
            ratio = min(red_underlines / expected_total_underlines, 1.0)
            pts = round(0.15 * ratio, 4)
            print(f"PASS: Component 3 -- Red underlines: {red_underlines}/{expected_total_underlines} ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 3 -- Red underlines: {red_underlines}/{total_underlines}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Highlight annotations over DANGER occurrences (0.20 points)
    try:
        if EXPECTED_DANGER > 0 and highlight_over_danger > 0:
            ratio = min(highlight_over_danger / EXPECTED_DANGER, 1.0)
            pts = round(0.20 * ratio, 4)
            print(f"PASS: Component 4 -- Highlights over DANGER: {highlight_over_danger}/{EXPECTED_DANGER} ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 4 -- Highlights over DANGER: {highlight_over_danger}/{EXPECTED_DANGER}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Highlights are yellow (0.10 points)
    try:
        if total_highlights > 0 and yellow_highlights > 0:
            ratio = min(yellow_highlights / EXPECTED_DANGER, 1.0)
            pts = round(0.10 * ratio, 4)
            print(f"PASS: Component 5 -- Yellow highlights: {yellow_highlights}/{EXPECTED_DANGER} ({pts} pts)")
            total_score += pts
        else:
            print(f"FAIL: Component 5 -- Yellow highlights: {yellow_highlights}/{total_highlights}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: No spurious annotations (0.05 points)
    # Total should be ~35 (18 WARNING + 12 CAUTION underlines + 5 DANGER highlights)
    try:
        if total_annotations >= EXPECTED_TOTAL_ANNOTS and total_annotations <= EXPECTED_TOTAL_ANNOTS + 5:
            print(f"PASS: Component 6 -- Total annotations: {total_annotations} (expected ~{EXPECTED_TOTAL_ANNOTS}) (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 6 -- Total annotations: {total_annotations} (expected ~{EXPECTED_TOTAL_ANNOTS})")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
