"""
Reward Script: Highlight 'Termination for Convenience' and add sticky note on page 14
Task ID: pdf_fm_017
Domain: pdf (libreoffice_calc listed but actual domain is PDF annotation)
Scoring:
  Component 1: Yellow highlight annotation exists on page 14 (0.4 points)
  Component 2: Highlight covers the 'Termination for Convenience' heading text (0.3 points)
  Component 3: Sticky note annotation with correct text on page 14 (0.3 points)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_017'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'legal', 'contract_draft.pdf')
TARGET_PAGE = 13  # page 14 is 0-indexed as 13
TARGET_TEXT = 'Termination for Convenience'
EXPECTED_NOTE = 'Legal team needs to review this section before signing'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be loadable
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must have at least 14 pages
    if len(doc) < 14:
        print(f"CRITICAL: PDF has only {len(doc)} pages, need at least 14")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    page = doc[TARGET_PAGE]

    # Collect annotations on page 14
    highlights = []
    text_annots = []
    try:
        for annot in page.annots():
            if annot.type[1] == "Highlight":
                highlights.append(annot)
            elif annot.type[1] == "Text":
                text_annots.append(annot)
    except Exception as e:
        print(f"ERROR: Could not enumerate annotations: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Yellow highlight annotation exists on page 14 (0.4 points)
    # This checks that at least one highlight exists AND it is yellow
    try:
        yellow_highlight_found = False
        for h in highlights:
            stroke = h.colors.get("stroke")
            if stroke is not None:
                # Yellow = (1.0, 1.0, 0.0) with tolerance
                if (len(stroke) >= 3 and
                        abs(stroke[0] - 1.0) < 0.1 and
                        abs(stroke[1] - 1.0) < 0.1 and
                        abs(stroke[2] - 0.0) < 0.1):
                    yellow_highlight_found = True
                    break
        if yellow_highlight_found:
            print(f"PASS: Component 1 -- Yellow highlight found on page 14 (0.4 pts)")
            total_score += 0.4
        else:
            if len(highlights) > 0:
                colors = [h.colors.get("stroke") for h in highlights]
                print(f"FAIL: Component 1 -- Highlight exists but not yellow. Colors: {colors}")
            else:
                print(f"FAIL: Component 1 -- No highlight annotations on page 14")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Highlight covers the 'Termination for Convenience' heading text (0.3 points)
    # Verify that the highlight annotation rectangle overlaps with where the target text is
    try:
        text_instances = page.search_for(TARGET_TEXT)
        if not text_instances:
            print(f"FAIL: Component 2 -- Target text '{TARGET_TEXT}' not found on page 14")
        else:
            highlight_covers_text = False
            for h in highlights:
                h_rect = h.rect
                for inst in text_instances:
                    if h_rect.intersects(inst):
                        highlight_covers_text = True
                        break
                if highlight_covers_text:
                    break
            if highlight_covers_text:
                print(f"PASS: Component 2 -- Highlight covers '{TARGET_TEXT}' text (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 -- Highlight does not overlap with '{TARGET_TEXT}' text")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Sticky note with correct content on page 14 (0.3 points)
    # Check for a Text annotation (sticky note) with the expected content
    try:
        note_found = False
        for ta in text_annots:
            content = ta.info.get("content", "")
            if EXPECTED_NOTE.lower() in content.lower():
                note_found = True
                print(f"PASS: Component 3 -- Sticky note found with text: '{content}' (0.3 pts)")
                total_score += 0.3
                break
        if not note_found:
            if len(text_annots) > 0:
                contents = [ta.info.get("content", "") for ta in text_annots]
                print(f"FAIL: Component 3 -- Text annotations found but none contain expected text. Found: {contents}")
            else:
                print(f"FAIL: Component 3 -- No sticky note (Text) annotations on page 14")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

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
