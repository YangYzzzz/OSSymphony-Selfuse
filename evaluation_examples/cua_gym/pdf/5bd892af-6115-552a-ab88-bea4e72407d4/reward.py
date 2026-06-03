"""
Reward Script: Add underline annotations to section headings on pages 1-5
Task ID: pdf_fm_032
Domain: pdf
Scoring:
  Component 1 (0.5): Each of 6 headings has an Underline annotation (proportional)
  Component 2 (0.3): Underline annotations are positioned over the heading text
  Component 3 (0.2): No extra underline annotations beyond the 6 headings
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_032'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'project_plan.pdf')

# Expected headings from context: 6 section headings on pages 0-4 (0-indexed)
EXPECTED_HEADINGS = {
    0: ['Project Overview'],
    1: ['Objectives'],
    2: ['Timeline'],
    3: ['Resources'],
    4: ['Risk Assessment', 'Budget Summary'],
}


def find_heading_locations(doc):
    """Find the bounding rects of 14pt bold headings on pages 0-4."""
    heading_locs = {}  # {page_idx: [(heading_text, rect), ...]}
    for pg_idx in range(min(5, doc.page_count)):
        page = doc[pg_idx]
        blocks = page.get_text('dict')['blocks']
        locs = []
        for b in blocks:
            if 'lines' not in b:
                continue
            for line in b['lines']:
                for span in line['spans']:
                    if abs(span['size'] - 14.0) < 0.5 and 'bold' in span['font'].lower():
                        bbox = pymupdf.Rect(span['bbox'])
                        locs.append((span['text'], bbox))
        heading_locs[pg_idx] = locs
    return heading_locs


def get_underline_annots(page):
    """Get all Underline annotations on a page."""
    underlines = []
    for annot in page.annots():
        if annot.type[0] == 9:  # Underline type code
            underlines.append(annot.rect)
    return underlines


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if doc.page_count < 5:
        print(f"FAIL: PDF has only {doc.page_count} pages, expected at least 5")
        print("REWARD: 0.0")
        doc.close()
        return 0.0

    # Find heading locations in the document
    heading_locs = find_heading_locations(doc)
    all_headings = []
    for pg_idx in sorted(heading_locs.keys()):
        for text, rect in heading_locs[pg_idx]:
            all_headings.append((pg_idx, text, rect))

    if len(all_headings) == 0:
        print("FAIL: No 14pt bold headings found in pages 0-4")
        print("REWARD: 0.0")
        doc.close()
        return 0.0

    print(f"INFO: Found {len(all_headings)} headings across pages 0-4")

    # Component 1: Each heading has at least one Underline annotation on its page (0.5 points)
    # Proportional: each heading is worth 0.5/num_headings
    try:
        headings_with_underline = 0
        per_heading_score = 0.5 / len(all_headings)

        for pg_idx, heading_text, heading_rect in all_headings:
            page = doc[pg_idx]
            underlines = get_underline_annots(page)
            if len(underlines) > 0:
                headings_with_underline += 1
                print(f"PASS: Page {pg_idx} has underline annotation(s) — heading '{heading_text}' covered")
            else:
                print(f"FAIL: Page {pg_idx} has no underline annotations — heading '{heading_text}' not underlined")

        comp1_score = headings_with_underline * per_heading_score
        if comp1_score > 0:
            total_score += comp1_score
        print(f"Component 1 score: {comp1_score:.3f}/0.500 ({headings_with_underline}/{len(all_headings)} headings on pages with underlines)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Underline annotations are positioned over heading text (0.3 points)
    # Each heading's underline must overlap with the heading's bounding rect
    try:
        headings_correctly_positioned = 0
        per_heading_pos_score = 0.3 / len(all_headings)

        for pg_idx, heading_text, heading_rect in all_headings:
            page = doc[pg_idx]
            underlines = get_underline_annots(page)
            # Check if any underline overlaps with this heading
            has_overlap = any(ul_rect.intersects(heading_rect) for ul_rect in underlines)
            if has_overlap:
                headings_correctly_positioned += 1
                print(f"PASS: Underline on page {pg_idx} overlaps with '{heading_text}'")
            else:
                print(f"FAIL: No underline on page {pg_idx} overlaps with '{heading_text}' at {tuple(heading_rect)}")

        comp2_score = headings_correctly_positioned * per_heading_pos_score
        if comp2_score > 0:
            total_score += comp2_score
        print(f"Component 2 score: {comp2_score:.3f}/0.300 ({headings_correctly_positioned}/{len(all_headings)} correctly positioned)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct total underline count and no stray annotations (0.2 points)
    # Must have exactly N underlines on pages 0-4 (matching heading count) AND none on pages 5+
    # This is a compound check: only awards points if underlines exist (task-introduced change)
    try:
        total_underlines_0_4 = 0
        for pg_idx in range(5):
            page = doc[pg_idx]
            total_underlines_0_4 += len(get_underline_annots(page))

        extra_underlines_5_plus = 0
        for pg_idx in range(5, doc.page_count):
            page = doc[pg_idx]
            extra_underlines_5_plus += len(get_underline_annots(page))

        comp3_score = 0.0
        # Compound condition: exact count on pages 0-4 AND no strays on pages 5+
        # This ensures initial_env (0 underlines) does NOT earn points
        if total_underlines_0_4 == len(all_headings) and extra_underlines_5_plus == 0:
            print(f"PASS: Exact underline count {total_underlines_0_4} on pages 0-4, none on pages 5+")
            comp3_score = 0.2
        else:
            if total_underlines_0_4 != len(all_headings):
                print(f"FAIL: Underline count on pages 0-4: {total_underlines_0_4}, expected {len(all_headings)}")
            if extra_underlines_5_plus > 0:
                print(f"FAIL: Found {extra_underlines_5_plus} underline annotation(s) on pages 5+")

        total_score += comp3_score
        print(f"Component 3 score: {comp3_score:.3f}/0.200")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.3f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
