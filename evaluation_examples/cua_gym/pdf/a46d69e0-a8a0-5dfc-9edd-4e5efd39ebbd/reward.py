"""
Reward Script: Add highlight and underline annotations to a legal PDF
Task ID: pdf_gf2_007
Domain: pdf
Scoring:
  Component 1 (0.20): Output file exists with correct page count
  Component 2 (0.30): Yellow highlight annotations on all 'liability' occurrences
  Component 3 (0.15): Highlight annotations overlap with 'liability' text
  Component 4 (0.20): Red underline annotations on all 'without limitation' occurrences
  Component 5 (0.15): Underline annotations overlap with 'without limitation' text
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_007'

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file exists and has correct page count (0.20 points)
    # The task requires saving to terms_reviewed.pdf. Page count must remain 10.
    try:
        page_count = len(doc)
        if page_count == 10:
            print(f"PASS: Component 1 — File exists with correct page count ({page_count}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Expected 10 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Yellow highlight annotations covering 'liability' (0.30 points)
    # Task requires yellow highlights on ALL occurrences of 'liability'.
    # We count highlight annotations with yellow stroke color across all pages.
    try:
        total_liability_text = 0
        total_yellow_highlights = 0
        for page in doc:
            liability_rects = page.search_for('liability')
            total_liability_text += len(liability_rects)
            for annot in page.annots():
                if annot.type[1] == 'Highlight':
                    stroke = annot.colors.get('stroke')
                    # Yellow = (1.0, 1.0, 0.0) with tolerance
                    if stroke and len(stroke) >= 3:
                        if abs(stroke[0] - 1.0) < 0.1 and abs(stroke[1] - 1.0) < 0.1 and abs(stroke[2] - 0.0) < 0.1:
                            total_yellow_highlights += 1

        if total_liability_text == 0:
            print(f"FAIL: Component 2 — No 'liability' text found in document")
        elif total_yellow_highlights >= total_liability_text:
            print(f"PASS: Component 2 — Found {total_yellow_highlights} yellow highlights for {total_liability_text} 'liability' occurrences (0.30 pts)")
            total_score += 0.30
        elif total_yellow_highlights > 0:
            # Partial credit: proportion of highlights found
            ratio = total_yellow_highlights / total_liability_text
            partial = round(0.30 * ratio, 2)
            print(f"PARTIAL: Component 2 — Found {total_yellow_highlights}/{total_liability_text} yellow highlights ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No yellow highlight annotations found (expected {total_liability_text})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Highlight annotations spatially overlap with 'liability' text (0.15 points)
    # Verify that highlights are actually positioned over the correct text, not just existing.
    try:
        covered_count = 0
        total_liability = 0
        for page in doc:
            text_rects = page.search_for('liability')
            total_liability += len(text_rects)
            for tr in text_rects:
                covered = False
                for annot in page.annots():
                    if annot.type[1] == 'Highlight' and annot.rect.intersects(tr):
                        covered = True
                        break
                if covered:
                    covered_count += 1

        if total_liability == 0:
            print(f"FAIL: Component 3 — No 'liability' text found")
        elif covered_count >= total_liability:
            print(f"PASS: Component 3 — All {total_liability} 'liability' instances covered by highlights (0.15 pts)")
            total_score += 0.15
        elif covered_count > 0:
            ratio = covered_count / total_liability
            partial = round(0.15 * ratio, 2)
            print(f"PARTIAL: Component 3 — {covered_count}/{total_liability} 'liability' instances covered ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No 'liability' instances covered by highlights")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Red underline annotations for 'without limitation' (0.20 points)
    # Task requires red underline annotations on ALL occurrences of 'without limitation'.
    try:
        total_wl_text = 0
        total_red_underlines = 0
        for page in doc:
            wl_rects = page.search_for('without limitation')
            total_wl_text += len(wl_rects)
            for annot in page.annots():
                if annot.type[1] == 'Underline':
                    stroke = annot.colors.get('stroke')
                    # Red = (1.0, 0.0, 0.0) with tolerance
                    if stroke and len(stroke) >= 3:
                        if abs(stroke[0] - 1.0) < 0.1 and abs(stroke[1] - 0.0) < 0.1 and abs(stroke[2] - 0.0) < 0.1:
                            total_red_underlines += 1

        if total_wl_text == 0:
            print(f"FAIL: Component 4 — No 'without limitation' text found in document")
        elif total_red_underlines >= total_wl_text:
            print(f"PASS: Component 4 — Found {total_red_underlines} red underlines for {total_wl_text} 'without limitation' occurrences (0.20 pts)")
            total_score += 0.20
        elif total_red_underlines > 0:
            ratio = total_red_underlines / total_wl_text
            partial = round(0.20 * ratio, 2)
            print(f"PARTIAL: Component 4 — Found {total_red_underlines}/{total_wl_text} red underlines ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No red underline annotations found (expected {total_wl_text})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Underline annotations spatially overlap with 'without limitation' text (0.15 points)
    try:
        covered_count = 0
        total_wl = 0
        for page in doc:
            text_rects = page.search_for('without limitation')
            total_wl += len(text_rects)
            for tr in text_rects:
                covered = False
                for annot in page.annots():
                    if annot.type[1] == 'Underline' and annot.rect.intersects(tr):
                        covered = True
                        break
                if covered:
                    covered_count += 1

        if total_wl == 0:
            print(f"FAIL: Component 5 — No 'without limitation' text found")
        elif covered_count >= total_wl:
            print(f"PASS: Component 5 — All {total_wl} 'without limitation' instances covered by underlines (0.15 pts)")
            total_score += 0.15
        elif covered_count > 0:
            ratio = covered_count / total_wl
            partial = round(0.15 * ratio, 2)
            print(f"PARTIAL: Component 5 — {covered_count}/{total_wl} 'without limitation' instances covered ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — No 'without limitation' instances covered by underlines")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/legal/terms_reviewed.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
