"""
Reward Script: Verify PDF annotation task on lease_agreement.pdf
Task ID: pdf_fm_049
Domain: pdf

Task: Open ~/Documents/legal/lease_agreement.pdf, go to page 8,
  - highlight 'security deposit of $2,500' in yellow
  - add strikethrough to 'no pets allowed'
  - add a sticky note saying 'Negotiate pet clause' near the struck text

Scoring:
  Component 1: Yellow highlight annotation overlapping 'security deposit of' text on page 8 (0.35)
  Component 2: StrikeOut annotation overlapping 'no pets allowed' text on page 8 (0.35)
  Component 3: Text (sticky note) annotation with 'Negotiate pet clause' content on page 8 (0.30)
"""

import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_049'

PDF_PATH = f'{WORKDIR}/Documents/legal/lease_agreement.pdf'
PAGE_NUM = 7  # 0-indexed, so page 8 = index 7


def verify_task(pdf_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = pymupdf.open(pdf_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {pdf_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(doc) < 8:
        print(f"FAIL: PDF has only {len(doc)} pages, need at least 8")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    page = doc[PAGE_NUM]

    # Collect all annotations on page 8
    try:
        annots_list = []
        for annot in page.annots():
            annots_list.append({
                "type": annot.type[1],
                "type_code": annot.type[0],
                "content": annot.info.get("content", ""),
                "rect": annot.rect,
                "stroke": annot.colors.get("stroke"),
                "fill": annot.colors.get("fill"),
            })
        print(f"INFO: Found {len(annots_list)} annotations on page 8")
    except Exception as e:
        print(f"ERROR: Could not read annotations: {e}")
        annots_list = []

    # Component 1: Yellow highlight on 'security deposit of' text (0.35 points)
    try:
        text_instances = page.search_for("security deposit of")
        highlight_found = False
        yellow_match = False

        if not text_instances:
            print("FAIL: Component 1 -- text 'security deposit of' not found on page 8")
        else:
            for a in annots_list:
                if a["type"] != "Highlight":
                    continue
                for inst in text_instances:
                    if a["rect"].intersects(inst):
                        highlight_found = True
                        # Check if color is yellow (1,1,0) with tolerance
                        stroke = a["stroke"]
                        if stroke and len(stroke) >= 3:
                            r_val, g_val, b_val = float(stroke[0]), float(stroke[1]), float(stroke[2])
                            if r_val > 0.8 and g_val > 0.8 and b_val < 0.3:
                                yellow_match = True
                        break
                if highlight_found:
                    break

            if highlight_found and yellow_match:
                print(f"PASS: Component 1 -- Yellow highlight found on 'security deposit of' (0.35 pts)")
                total_score += 0.35
            elif highlight_found:
                # Highlight exists but not yellow -- partial credit
                print(f"PARTIAL: Component 1 -- Highlight found but color is not yellow (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 -- No highlight annotation overlapping 'security deposit of' text")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Strikethrough on 'no pets allowed' text (0.35 points)
    try:
        text_instances = page.search_for("no pets allowed")
        strikeout_found = False

        if not text_instances:
            print("FAIL: Component 2 -- text 'no pets allowed' not found on page 8")
        else:
            for a in annots_list:
                if a["type"] != "StrikeOut":
                    continue
                for inst in text_instances:
                    if a["rect"].intersects(inst):
                        strikeout_found = True
                        break
                if strikeout_found:
                    break

            if strikeout_found:
                print(f"PASS: Component 2 -- Strikethrough found on 'no pets allowed' (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 -- No StrikeOut annotation overlapping 'no pets allowed' text")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Sticky note with 'Negotiate pet clause' (0.30 points)
    try:
        note_found = False
        for a in annots_list:
            if a["type"] == "Text":
                content = a["content"]
                if "Negotiate pet clause" in content:
                    note_found = True
                    break

        if note_found:
            print(f"PASS: Component 3 -- Sticky note with 'Negotiate pet clause' found (0.30 pts)")
            total_score += 0.30
        else:
            # Check if any Text annotation exists with partial match
            text_annots = [a for a in annots_list if a["type"] == "Text"]
            if text_annots:
                # Check for case-insensitive partial match
                for a in text_annots:
                    if "negotiate" in a["content"].lower() and "pet" in a["content"].lower():
                        note_found = True
                        print(f"PARTIAL: Component 3 -- Sticky note with similar content found: '{a['content']}' (0.20 pts)")
                        total_score += 0.20
                        break
                if not note_found:
                    print(f"FAIL: Component 3 -- Text annotations found but none contain 'Negotiate pet clause'. Contents: {[a['content'] for a in text_annots]}")
            else:
                print(f"FAIL: Component 3 -- No sticky note (Text annotation) found on page 8")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
import os

if not os.path.exists(PDF_PATH):
    print(f"File not found: {PDF_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(PDF_PATH)
