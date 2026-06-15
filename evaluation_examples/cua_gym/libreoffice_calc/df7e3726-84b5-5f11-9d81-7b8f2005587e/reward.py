"""
Reward Script: Highlight first sentence of Chapter 5 in dissertation.pdf
Task ID: pdf_fm_030
Domain: pdf (libreoffice_calc in config, but actual domain is PDF/Okular)
Scoring:
  Component 1 (0.4): Highlight annotation exists on page 52 (0-indexed 51)
  Component 2 (0.3): Highlight color is yellow (stroke ~ [1, 1, 0])
  Component 3 (0.3): Highlight overlaps the first sentence text
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_030'
TARGET_FILE = os.path.join(WORKDIR, 'Documents', 'dissertation.pdf')
# Page 52 in 1-indexed = page 51 in 0-indexed
TARGET_PAGE = 51
FIRST_SENTENCE = 'This chapter presents the experimental results obtained from our three-phase study.'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf
        except ImportError:
            print("CRITICAL: Neither pymupdf nor fitz available")
            print("REWARD: 0.0")
            return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: file has at least 52 pages
    if len(doc) < 52:
        print(f"PRECONDITION FAIL: PDF has only {len(doc)} pages, need at least 52")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    page = doc[TARGET_PAGE]

    # Collect highlight annotations on target page
    highlights = []
    try:
        for annot in page.annots():
            if annot.type[1] == "Highlight":
                highlights.append(annot)
    except Exception as e:
        print(f"ERROR: Could not iterate annotations: {e}")

    # Component 1: At least one Highlight annotation exists on page 52 (0.4 points)
    try:
        if len(highlights) >= 1:
            print(f"PASS: Component 1 - Found {len(highlights)} highlight annotation(s) on page 52 (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 - No highlight annotations found on page 52")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: The highlight is yellow (stroke color ~ [1, 1, 0]) (0.3 points)
    try:
        yellow_found = False
        for hl in highlights:
            stroke = hl.colors.get("stroke")
            if stroke and len(stroke) >= 3:
                # Check if color is approximately yellow: R~1, G~1, B~0
                if abs(stroke[0] - 1.0) < 0.1 and abs(stroke[1] - 1.0) < 0.1 and stroke[2] < 0.15:
                    yellow_found = True
                    print(f"PASS: Component 2 - Yellow highlight found (stroke: {list(stroke)}) (0.3 pts)")
                    break
        if not yellow_found:
            if highlights:
                colors_found = [list(hl.colors.get("stroke", [])) for hl in highlights]
                print(f"FAIL: Component 2 - No yellow highlight. Colors found: {colors_found}")
            else:
                print(f"FAIL: Component 2 - No highlights to check color")
        if yellow_found:
            total_score += 0.3
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: A highlight overlaps the first sentence text (0.3 points)
    try:
        text_instances = page.search_for(FIRST_SENTENCE)
        if not text_instances:
            # Try a shorter substring in case of minor differences
            shorter = FIRST_SENTENCE[:60]
            text_instances = page.search_for(shorter)

        overlap_found = False
        if text_instances:
            for hl in highlights:
                hl_rect = hl.rect
                for inst in text_instances:
                    if hl_rect.intersects(inst):
                        overlap_found = True
                        break
                if overlap_found:
                    break

        if overlap_found:
            print(f"PASS: Component 3 - Highlight overlaps first sentence text (0.3 pts)")
            total_score += 0.3
        else:
            if not text_instances:
                print(f"FAIL: Component 3 - Could not locate first sentence text on page 52")
            else:
                print(f"FAIL: Component 3 - No highlight overlaps the first sentence text")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(TARGET_FILE):
    print(f"File not found: {TARGET_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(TARGET_FILE)
