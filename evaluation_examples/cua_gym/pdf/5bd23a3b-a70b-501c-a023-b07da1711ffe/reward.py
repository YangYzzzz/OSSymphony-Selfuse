"""
Reward Script: Add freetext annotations to lease amendment PDF
Task ID: pdf_legal_085
Domain: pdf
Scoring:
  - Component 1 (0.10): Output file exists at expected path
  - Component 2 (0.30): FreeText annotation on page 1 with text 'APPROVED BY LANDLORD 03/20/2024'
  - Component 3 (0.30): FreeText annotation on page 3 with text 'TENANT INITIALS: ___'
  - Component 4 (0.15): Page 1 annotation positioned near (72, 700)
  - Component 5 (0.15): Page 3 annotation positioned near (400, 700)
"""

import os
import fitz  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_085'
OUTPUT_PATH = os.path.join(WORKDIR, 'legal', 'lease_amendment_annotated.pdf')

# Position tolerance in points (allow some deviation)
POS_TOLERANCE = 30.0


def get_freetext_annots(doc, page_num):
    """Get all FreeText annotations on a given page."""
    page = doc[page_num]
    annots = []
    if page.annots():
        for annot in page.annots():
            if annot.type[1] == 'FreeText':
                annots.append({
                    'content': annot.info.get('content', ''),
                    'rect': tuple(annot.rect),  # (x0, y0, x1, y1)
                    'colors': annot.colors,
                    'text_in_rect': page.get_text('text', clip=annot.rect).strip(),
                })
    return annots


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists (0.10 points)
    # This is a task-introduced change: the annotated file does NOT exist in initial_env
    try:
        if os.path.isfile(OUTPUT_PATH):
            print(f"PASS: Component 1 -- Output file exists at {OUTPUT_PATH} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 -- Output file not found at {OUTPUT_PATH}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print("REWARD: 0.0")
        return 0.0

    # Load the document
    try:
        doc = fitz.open(OUTPUT_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {OUTPUT_PATH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: FreeText annotation on page 0 (page 1 in 1-indexed) with correct text (0.30 points)
    try:
        page0_annots = get_freetext_annots(doc, 0)
        found_page0_text = False
        expected_text_p0 = 'APPROVED BY LANDLORD 03/20/2024'
        for annot in page0_annots:
            # Check both the info content and the rendered text
            annot_text = annot['content'] or annot['text_in_rect']
            if expected_text_p0 in annot_text:
                found_page0_text = True
                break
        if found_page0_text:
            print(f"PASS: Component 2 -- FreeText on page 1 contains '{expected_text_p0}' (0.30 pts)")
            total_score += 0.30
        else:
            texts_found = [a['content'] or a['text_in_rect'] for a in page0_annots]
            print(f"FAIL: Component 2 -- Expected FreeText with '{expected_text_p0}' on page 1, found: {texts_found}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: FreeText annotation on page 2 (page 3 in 1-indexed) with correct text (0.30 points)
    try:
        page2_annots = get_freetext_annots(doc, 2)
        found_page2_text = False
        expected_text_p2 = 'TENANT INITIALS: ___'
        for annot in page2_annots:
            annot_text = annot['content'] or annot['text_in_rect']
            if expected_text_p2 in annot_text:
                found_page2_text = True
                break
        if found_page2_text:
            print(f"PASS: Component 3 -- FreeText on page 3 contains '{expected_text_p2}' (0.30 pts)")
            total_score += 0.30
        else:
            texts_found = [a['content'] or a['text_in_rect'] for a in page2_annots]
            print(f"FAIL: Component 3 -- Expected FreeText with '{expected_text_p2}' on page 3, found: {texts_found}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Page 1 annotation positioned near (72, 700) (0.15 points)
    try:
        page0_annots = get_freetext_annots(doc, 0)
        found_pos_p0 = False
        for annot in page0_annots:
            annot_text = annot['content'] or annot['text_in_rect']
            if expected_text_p0 in annot_text:
                rect = annot['rect']  # (x0, y0, x1, y1)
                x0, y0 = rect[0], rect[1]
                if abs(x0 - 72.0) <= POS_TOLERANCE and abs(y0 - 700.0) <= POS_TOLERANCE:
                    found_pos_p0 = True
                    print(f"PASS: Component 4 -- Page 1 annotation at ({x0}, {y0}), expected near (72, 700) (0.15 pts)")
                else:
                    print(f"FAIL: Component 4 -- Page 1 annotation at ({x0}, {y0}), expected near (72, 700)")
                break
        if not found_pos_p0 and not any(expected_text_p0 in (a['content'] or a['text_in_rect']) for a in page0_annots):
            print(f"FAIL: Component 4 -- No matching FreeText annotation found on page 1")
        elif found_pos_p0:
            total_score += 0.15
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Page 3 annotation positioned near (400, 700) (0.15 points)
    try:
        page2_annots = get_freetext_annots(doc, 2)
        found_pos_p2 = False
        for annot in page2_annots:
            annot_text = annot['content'] or annot['text_in_rect']
            if expected_text_p2 in annot_text:
                rect = annot['rect']  # (x0, y0, x1, y1)
                x0, y0 = rect[0], rect[1]
                if abs(x0 - 400.0) <= POS_TOLERANCE and abs(y0 - 700.0) <= POS_TOLERANCE:
                    found_pos_p2 = True
                    print(f"PASS: Component 5 -- Page 3 annotation at ({x0}, {y0}), expected near (400, 700) (0.15 pts)")
                else:
                    print(f"FAIL: Component 5 -- Page 3 annotation at ({x0}, {y0}), expected near (400, 700)")
                break
        if not found_pos_p2 and not any(expected_text_p2 in (a['content'] or a['text_in_rect']) for a in page2_annots):
            print(f"FAIL: Component 5 -- No matching FreeText annotation found on page 3")
        elif found_pos_p2:
            total_score += 0.15
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
