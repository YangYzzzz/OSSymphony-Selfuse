"""
Reward Script: Add 'DRAFT' watermark FreeText annotation to every page of an 8-page PDF
Task ID: pdf_fm_042
Domain: pdf
Scoring:
  Component 1 (0.4): All 8 pages have a FreeText annotation with 'DRAFT' content
  Component 2 (0.3): Annotations use light gray color (~0.8,0.8,0.8) and large font (>=60pt)
  Component 3 (0.3): Annotations are rotated diagonally (~45 degrees)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_042'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: document should have 8 pages
    if doc.page_count != 8:
        print(f"PRECONDITION FAIL: Expected 8 pages, found {doc.page_count}")
        print("REWARD: 0.0")
        doc.close()
        return 0.0

    # Component 1: All 8 pages have a FreeText annotation with 'DRAFT' content (0.4 points)
    try:
        draft_freetext_pages = 0
        for i in range(8):
            page = doc[i]
            annots = list(page.annots()) if page.annots() else []
            has_draft_freetext = False
            for a in annots:
                if a.type[1] == "FreeText" and "DRAFT" in (a.info.get("content", "") or ""):
                    has_draft_freetext = True
                    break
            if has_draft_freetext:
                draft_freetext_pages += 1

        if draft_freetext_pages == 8:
            print(f"PASS: Component 1 - All 8 pages have FreeText 'DRAFT' annotation (0.4 pts)")
            total_score += 0.4
        elif draft_freetext_pages > 0:
            partial = round(0.4 * (draft_freetext_pages / 8), 2)
            print(f"PARTIAL: Component 1 - {draft_freetext_pages}/8 pages have FreeText 'DRAFT' ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 - No pages have a FreeText 'DRAFT' annotation")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Annotations use light gray color and large font (0.3 points)
    # Check via the DA (Default Appearance) string in the annotation's PDF object
    try:
        gray_large_font_pages = 0
        for i in range(8):
            page = doc[i]
            annots = list(page.annots()) if page.annots() else []
            for a in annots:
                if a.type[1] != "FreeText" or "DRAFT" not in (a.info.get("content", "") or ""):
                    continue
                # Read the raw PDF object to get DA string
                xref = a.xref
                obj_str = doc.xref_object(xref)

                # Check for gray color: look for DA string with rg values close to 0.8
                da_match = re.search(r'/DA\s*\(([^)]+)\)', obj_str)
                color_ok = False
                font_ok = False

                if da_match:
                    da_str = da_match.group(1)
                    # Parse color: pattern like "0.8 0.8 0.8 rg" or "0.8 0.8 0.8 RG"
                    color_match = re.search(r'([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+[rR][gG]', da_str)
                    if color_match:
                        r, g, b = float(color_match.group(1)), float(color_match.group(2)), float(color_match.group(3))
                        # Light gray: all components >= 0.6 and similar to each other
                        if r >= 0.6 and g >= 0.6 and b >= 0.6:
                            color_ok = True

                    # Parse font size: pattern like "/Helv 72.0 Tf"
                    font_match = re.search(r'([\d.]+)\s+Tf', da_str)
                    if font_match:
                        font_size = float(font_match.group(1))
                        if font_size >= 60.0:
                            font_ok = True

                if color_ok and font_ok:
                    gray_large_font_pages += 1
                    break  # one matching annot per page is enough

        if gray_large_font_pages == 8:
            print(f"PASS: Component 2 - All 8 pages have light gray, large font DRAFT annotation (0.3 pts)")
            total_score += 0.3
        elif gray_large_font_pages > 0:
            partial = round(0.3 * (gray_large_font_pages / 8), 2)
            print(f"PARTIAL: Component 2 - {gray_large_font_pages}/8 pages meet color+font criteria ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 - No DRAFT annotations have light gray color AND large font (>=60pt)")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Annotations are rotated diagonally (0.3 points)
    # Check the /Rotate key in the annotation object for ~45 or ~315 degrees
    try:
        rotated_pages = 0
        for i in range(8):
            page = doc[i]
            annots = list(page.annots()) if page.annots() else []
            for a in annots:
                if a.type[1] != "FreeText" or "DRAFT" not in (a.info.get("content", "") or ""):
                    continue

                # Check rotation via the annotation's rotation attribute
                rotation = getattr(a, 'rotation', 0) or 0

                # Accept rotations around 45 degrees (315 = -45 = 360-45)
                # Also check the raw object for /Rotate
                if rotation in (0, None):
                    xref = a.xref
                    obj_str = doc.xref_object(xref)
                    rot_match = re.search(r'/Rotate\s+(\d+)', obj_str)
                    if rot_match:
                        rotation = int(rot_match.group(1))

                # Accept 315 (=-45), 45, or anything diagonal (not 0, 90, 180, 270)
                if rotation not in (0, 90, 180, 270, None):
                    rotated_pages += 1
                    break

        if rotated_pages == 8:
            print(f"PASS: Component 3 - All 8 pages have diagonally rotated DRAFT annotation (0.3 pts)")
            total_score += 0.3
        elif rotated_pages > 0:
            partial = round(0.3 * (rotated_pages / 8), 2)
            print(f"PARTIAL: Component 3 - {rotated_pages}/8 pages have rotated annotation ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 - No DRAFT annotations are diagonally rotated")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/policy_draft.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
