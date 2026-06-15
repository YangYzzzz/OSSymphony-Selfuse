"""
Reward Script: Highlight all occurrences of 'machine learning' in yellow
Task ID: pdf_res_001
Domain: pdf
Scoring:
  Component 1 (0.2): Output file exists with correct page count (15 pages)
  Component 2 (0.4): Exactly 23 highlight annotations across all pages
  Component 3 (0.2): All highlights use yellow color (stroke ~[1,1,0])
  Component 4 (0.2): Highlights overlap with actual 'machine learning' text positions
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_001'

TARGET_FILE = f'{WORKDIR}/papers/survey_ml_highlighted.pdf'
EXPECTED_PAGES = 15
EXPECTED_HIGHLIGHTS = 23
YELLOW = (1.0, 1.0, 0.0)
COLOR_TOLERANCE = 0.05


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be loadable
    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf

    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file has correct page count (0.2 points)
    # This checks the output file exists AND has expected structure.
    # The initial_env does NOT have survey_ml_highlighted.pdf, so this fails on initial.
    try:
        page_count = len(doc)
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 1 -- Page count is {page_count} (expected {EXPECTED_PAGES}) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- Page count is {page_count}, expected {EXPECTED_PAGES}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Total highlight annotation count == 23 (0.4 points)
    # Awards partial credit: 0.4 * (actual_highlights / expected_highlights) capped at 0.4
    try:
        total_highlights = 0
        for i in range(len(doc)):
            page = doc[i]
            annot_iter = page.annots()
            if annot_iter:
                for annot in annot_iter:
                    if annot.type[1] == "Highlight":
                        total_highlights += 1

        if total_highlights == EXPECTED_HIGHLIGHTS:
            print(f"PASS: Component 2 -- Found {total_highlights} highlights (expected {EXPECTED_HIGHLIGHTS}) (0.4 pts)")
            total_score += 0.4
        elif total_highlights > 0:
            partial = 0.4 * min(total_highlights / EXPECTED_HIGHLIGHTS, 1.0)
            # Cap partial at 0.35 -- only exact match gets full 0.4
            partial = min(partial, 0.35)
            print(f"PARTIAL: Component 2 -- Found {total_highlights} highlights, expected {EXPECTED_HIGHLIGHTS} ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- Found 0 highlights, expected {EXPECTED_HIGHLIGHTS}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: All highlights are yellow (0.2 points)
    # Checks that every highlight annotation has stroke color close to (1.0, 1.0, 0.0)
    try:
        yellow_count = 0
        non_yellow_count = 0
        for i in range(len(doc)):
            page = doc[i]
            annot_iter = page.annots()
            if annot_iter:
                for annot in annot_iter:
                    if annot.type[1] == "Highlight":
                        stroke = annot.colors.get("stroke")
                        if stroke and len(stroke) >= 3:
                            if all(abs(stroke[c] - YELLOW[c]) < COLOR_TOLERANCE for c in range(3)):
                                yellow_count += 1
                            else:
                                non_yellow_count += 1
                                print(f"  Non-yellow highlight on page {i}: stroke={stroke}")
                        else:
                            non_yellow_count += 1

        if yellow_count > 0 and non_yellow_count == 0:
            print(f"PASS: Component 3 -- All {yellow_count} highlights are yellow (0.2 pts)")
            total_score += 0.2
        elif yellow_count > 0:
            print(f"PARTIAL: Component 3 -- {yellow_count} yellow, {non_yellow_count} non-yellow")
            partial = 0.2 * (yellow_count / (yellow_count + non_yellow_count))
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- No yellow highlights found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Highlights overlap with 'machine learning' text positions (0.2 points)
    # Verifies that highlights are actually placed over the correct text
    try:
        overlapping = 0
        total_text_instances = 0
        for i in range(len(doc)):
            page = doc[i]
            text_instances = page.search_for("machine learning")
            total_text_instances += len(text_instances)

            # Collect highlight rects on this page
            highlight_rects = []
            annot_iter = page.annots()
            if annot_iter:
                for annot in annot_iter:
                    if annot.type[1] == "Highlight":
                        highlight_rects.append(annot.rect)

            # Check each text instance overlaps with at least one highlight
            for inst in text_instances:
                for hr in highlight_rects:
                    if hr.intersects(inst):
                        overlapping += 1
                        break

        if total_text_instances > 0 and overlapping == total_text_instances:
            print(f"PASS: Component 4 -- All {overlapping}/{total_text_instances} text instances covered by highlights (0.2 pts)")
            total_score += 0.2
        elif overlapping > 0:
            partial = 0.2 * (overlapping / max(total_text_instances, 1))
            print(f"PARTIAL: Component 4 -- {overlapping}/{total_text_instances} text instances covered ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- No highlights overlap with 'machine learning' text")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

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
