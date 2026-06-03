"""
Reward Script: Add yellow highlight and sticky note to PDF
Task ID: pdf_legal_075
Domain: pdf
Scoring:
  Component 1 (0.20): Output file exists at expected path
  Component 2 (0.30): Yellow highlight annotation on page 3 covering the specified region
  Component 3 (0.30): Sticky note (Text annotation) on page 3 with correct content
  Component 4 (0.20): Sticky note positioned near (545, 100) on page 3
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_075'
OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'insurance', 'policy_review_marked.pdf')

# Expected values from task description
EXPECTED_PAGE_INDEX = 2  # page 3 is 0-indexed as 2
EXPECTED_HIGHLIGHT_REGION = (72, 100, 540, 200)  # approximate region
EXPECTED_NOTE_TEXT = 'Key liability provision - discuss at team meeting'
EXPECTED_NOTE_POSITION = (545, 100)
REGION_TOLERANCE = 60  # tolerance in points for region matching


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists and is a valid PDF (0.20 points)
    # This is task-introduced: initial_env has no policy_review_marked.pdf
    try:
        if not os.path.exists(file_path):
            print(f"FAIL: Component 1 - Output file not found at {file_path}")
            print("REWARD: 0.0")
            return 0.0

        doc = pymupdf.open(file_path)
        if doc.page_count < 3:
            print(f"FAIL: Component 1 - PDF has only {doc.page_count} pages, need at least 3")
            doc.close()
            print("REWARD: 0.0")
            return 0.0

        print(f"PASS: Component 1 - Output file exists and is valid PDF with {doc.page_count} pages (0.20 pts)")
        total_score += 0.20
    except Exception as e:
        print(f"ERROR: Component 1 - Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get page 3 (0-indexed as 2)
    page = doc[EXPECTED_PAGE_INDEX]
    annots = []
    for annot in page.annots():
        annots.append({
            "type": annot.type[1],
            "type_code": annot.type[0],
            "content": annot.info.get("content", ""),
            "rect": tuple(annot.rect),
            "colors_stroke": annot.colors.get("stroke"),
            "colors_fill": annot.colors.get("fill"),
        })

    # Component 2: Yellow highlight annotation on page 3 (0.30 points)
    try:
        highlights = [a for a in annots if a["type"] == "Highlight"]
        if not highlights:
            print(f"FAIL: Component 2 - No highlight annotations found on page 3")
        else:
            # Check for yellow color and approximate region overlap
            found_yellow_highlight = False
            for h in highlights:
                stroke = h["colors_stroke"]
                is_yellow = False
                if stroke and len(stroke) >= 3:
                    # Yellow: R close to 1, G close to 1, B close to 0
                    if stroke[0] > 0.8 and stroke[1] > 0.8 and stroke[2] < 0.3:
                        is_yellow = True

                if is_yellow:
                    # Check region overlap: highlight should roughly cover the specified area
                    rect = h["rect"]
                    ex0, ey0, ex1, ey1 = EXPECTED_HIGHLIGHT_REGION
                    # Verify the highlight rect overlaps significantly with expected region
                    overlap_x = max(0, min(rect[2], ex1) - max(rect[0], ex0))
                    overlap_y = max(0, min(rect[3], ey1) - max(rect[1], ey0))
                    if overlap_x > 0 and overlap_y > 0:
                        found_yellow_highlight = True
                        print(f"PASS: Component 2 - Yellow highlight found on page 3 at rect {rect} (0.30 pts)")
                        total_score += 0.30
                        break

            if not found_yellow_highlight:
                # Check if there's any highlight at all (even wrong color)
                print(f"FAIL: Component 2 - No yellow highlight covering expected region on page 3")
                print(f"  Found highlights: {[(h['rect'], h['colors_stroke']) for h in highlights]}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Sticky note with correct content on page 3 (0.30 points)
    try:
        text_annots = [a for a in annots if a["type"] == "Text"]
        if not text_annots:
            print(f"FAIL: Component 3 - No sticky note (Text) annotations found on page 3")
        else:
            found_note = False
            for ta in text_annots:
                if EXPECTED_NOTE_TEXT in ta["content"]:
                    found_note = True
                    print(f"PASS: Component 3 - Sticky note with correct text found (0.30 pts)")
                    total_score += 0.30
                    break
            if not found_note:
                print(f"FAIL: Component 3 - No sticky note with expected text found")
                print(f"  Expected: '{EXPECTED_NOTE_TEXT}'")
                print(f"  Found notes: {[ta['content'] for ta in text_annots]}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Sticky note positioned near (545, 100) (0.20 points)
    try:
        text_annots = [a for a in annots if a["type"] == "Text"]
        if not text_annots:
            print(f"FAIL: Component 4 - No sticky note annotations to check position")
        else:
            found_positioned = False
            for ta in text_annots:
                if EXPECTED_NOTE_TEXT in ta["content"]:
                    rect = ta["rect"]
                    # Check if the annotation's top-left corner is near (545, 100)
                    dist_x = abs(rect[0] - EXPECTED_NOTE_POSITION[0])
                    dist_y = abs(rect[1] - EXPECTED_NOTE_POSITION[1])
                    if dist_x <= REGION_TOLERANCE and dist_y <= REGION_TOLERANCE:
                        found_positioned = True
                        print(f"PASS: Component 4 - Sticky note positioned at ({rect[0]:.1f}, {rect[1]:.1f}), near expected ({EXPECTED_NOTE_POSITION[0]}, {EXPECTED_NOTE_POSITION[1]}) (0.20 pts)")
                        total_score += 0.20
                        break
            if not found_positioned:
                positions = [(ta['rect'][0], ta['rect'][1]) for ta in text_annots if EXPECTED_NOTE_TEXT in ta['content']]
                print(f"FAIL: Component 4 - Sticky note not near expected position")
                print(f"  Expected near: {EXPECTED_NOTE_POSITION}")
                print(f"  Found at: {positions}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)
