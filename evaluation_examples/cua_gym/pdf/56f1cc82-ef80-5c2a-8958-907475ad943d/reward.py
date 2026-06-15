"""
Reward Script: Verify yellow highlight on abstract section and sticky note annotation on page 1
Task ID: pdf_fm_045
Domain: pdf
Scoring:
  Component 1 (0.35): Yellow highlight annotations exist on page 1
  Component 2 (0.25): Highlights are in the abstract region (y range ~270-550)
  Component 3 (0.25): Sticky note (Text annotation) with 'Strong methodology description' on page 1
  Component 4 (0.15): Sticky note color is yellow
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_045'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'research', 'neuroimaging_study.pdf')


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

    if len(doc) < 1:
        print("CRITICAL: PDF has no pages")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    page = doc[0]

    # Collect all annotations on page 1
    try:
        all_annots = list(page.annots())
    except Exception as e:
        print(f"CRITICAL: Cannot read annotations: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    highlights = [a for a in all_annots if a.type[1] == "Highlight"]
    text_annots = [a for a in all_annots if a.type[1] == "Text"]

    # Component 1: Yellow highlight annotations exist on page 1 (0.35 points)
    # Initial env has 0 highlights; golden env has 34 yellow highlights
    try:
        yellow_highlights = []
        for h in highlights:
            stroke = h.colors.get("stroke")
            if stroke and len(stroke) == 3:
                r, g, b = stroke
                # Yellow: R~1.0, G~1.0, B~0.0
                if r > 0.8 and g > 0.8 and b < 0.3:
                    yellow_highlights.append(h)

        if len(yellow_highlights) >= 3:
            print(f"PASS: Component 1 — Found {len(yellow_highlights)} yellow highlight annotations on page 1 (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — Expected multiple yellow highlights, found {len(yellow_highlights)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Highlights overlap with abstract region on page 1 (0.25 points)
    # The abstract section on page 1 is roughly between y=270 and y=550
    # We verify that highlights are actually in the abstract area, not elsewhere
    try:
        abstract_region_min_y = 260.0
        abstract_region_max_y = 560.0
        highlights_in_abstract = 0
        for h in yellow_highlights:
            rect = h.rect
            # Check if the highlight is within the abstract y-region
            if rect.y0 >= abstract_region_min_y and rect.y1 <= abstract_region_max_y:
                highlights_in_abstract += 1

        if highlights_in_abstract >= 3:
            print(f"PASS: Component 2 — {highlights_in_abstract} highlights are in the abstract region (y={abstract_region_min_y}-{abstract_region_max_y}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Only {highlights_in_abstract} highlights in abstract region, expected >= 3")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Sticky note (Text annotation) with 'Strong methodology description' on page 1 (0.25 points)
    # Initial env has 0 Text annotations; golden env has one with the expected content
    try:
        matching_notes = []
        for t in text_annots:
            content = t.info.get("content", "")
            if "Strong methodology description" in content:
                matching_notes.append(t)

        if len(matching_notes) >= 1:
            print(f"PASS: Component 3 — Found sticky note with 'Strong methodology description' (0.25 pts)")
            total_score += 0.25
        else:
            all_contents = [t.info.get("content", "") for t in text_annots]
            print(f"FAIL: Component 3 — No sticky note with expected text. Found {len(text_annots)} text annots: {all_contents}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Sticky note color is yellow (0.15 points)
    # This checks the note annotation has yellow color, matching the task requirement
    try:
        if len(matching_notes) >= 1:
            note = matching_notes[0]
            stroke = note.colors.get("stroke")
            if stroke and len(stroke) == 3:
                r, g, b = stroke
                if r > 0.8 and g > 0.8 and b < 0.3:
                    print(f"PASS: Component 4 — Sticky note has yellow color (stroke={stroke}) (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 4 — Sticky note color is not yellow: stroke={stroke}")
            else:
                print(f"FAIL: Component 4 — Cannot determine sticky note color: stroke={stroke}")
        else:
            print(f"FAIL: Component 4 — No matching sticky note found (depends on Component 3)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

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
