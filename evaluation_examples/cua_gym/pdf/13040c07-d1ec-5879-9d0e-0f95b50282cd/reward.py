"""
Reward Script: Add sticky note and freetext annotations to a PDF
Task ID: pdf_gf2_006
Domain: pdf
Scoring:
  Component 1 (0.15): Output file exists with 8 pages preserved
  Component 2 (0.35): Page 3 (1-indexed) has a Text (sticky note) annotation
                       with content 'Verify figures with finance team before publishing'
  Component 3 (0.15): Sticky note is positioned near coordinates (300, 400)
  Component 4 (0.35): Page 5 (1-indexed) has a FreeText annotation with 'ACTION NEEDED'
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_006'


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

    # Component 1: Output file has 8 pages (0.15 points)
    # The task requires all 8 pages to be preserved.
    try:
        page_count = doc.page_count
        if page_count == 8:
            print(f"PASS: Component 1 — PDF has {page_count} pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected 8 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Page 3 (0-indexed: page 2) has a Text (sticky note) annotation
    # with content 'Verify figures with finance team before publishing' (0.35 points)
    try:
        page2 = doc[2]  # 0-indexed page 2 = page 3 in 1-indexed
        annots_page2 = list(page2.annots()) if page2.annots() else []
        text_annots = [a for a in annots_page2 if a.type[1] == "Text"]
        found_sticky = False
        expected_content = "Verify figures with finance team before publishing"
        for a in text_annots:
            content = a.info.get("content", "")
            if expected_content.lower() in content.lower():
                found_sticky = True
                print(f"PASS: Component 2 — Found sticky note on page 3 with content: {repr(content)} (0.35 pts)")
                break
        if not found_sticky:
            all_contents = [a.info.get("content", "") for a in text_annots]
            print(f"FAIL: Component 2 — No Text annotation with expected content on page 3. "
                  f"Found {len(text_annots)} Text annots with contents: {all_contents}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Sticky note is near coordinates (300, 400) (0.15 points)
    # We check that the annotation rect's top-left corner is within a reasonable
    # tolerance of (300, 400). Tolerance of 50 points (~0.7 inches).
    try:
        if found_sticky:
            page2 = doc[2]
            annots_page2 = list(page2.annots()) if page2.annots() else []
            text_annots = [a for a in annots_page2 if a.type[1] == "Text"]
            for a in text_annots:
                content = a.info.get("content", "")
                if expected_content.lower() in content.lower():
                    rect = a.rect
                    x0, y0 = rect.x0, rect.y0
                    dist = ((x0 - 300) ** 2 + (y0 - 400) ** 2) ** 0.5
                    if dist <= 50:
                        print(f"PASS: Component 3 — Sticky note at ({x0:.1f}, {y0:.1f}), "
                              f"distance from (300,400) = {dist:.1f} pts (0.15 pts)")
                        total_score += 0.15
                    else:
                        print(f"FAIL: Component 3 — Sticky note at ({x0:.1f}, {y0:.1f}), "
                              f"distance from (300,400) = {dist:.1f} pts (too far, tolerance=50)")
                    break
        else:
            print(f"FAIL: Component 3 — Skipped (no sticky note found in Component 2)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Award Component 2 points only after Component 3 check (to keep variable scope clean)
    if found_sticky:
        total_score += 0.35

    # Component 4: Page 5 (0-indexed: page 4) has a FreeText annotation
    # with content 'ACTION NEEDED' (0.35 points)
    try:
        page4 = doc[4]  # 0-indexed page 4 = page 5 in 1-indexed
        annots_page4 = list(page4.annots()) if page4.annots() else []
        freetext_annots = [a for a in annots_page4 if a.type[1] == "FreeText"]
        found_freetext = False
        for a in freetext_annots:
            content = a.info.get("content", "")
            if "ACTION NEEDED" in content.upper():
                found_freetext = True
                # Also verify it's in the top area of the page (y0 < 200)
                rect = a.rect
                if rect.y0 < 200:
                    print(f"PASS: Component 4 — Found FreeText 'ACTION NEEDED' at top of page 5, "
                          f"rect=({rect.x0:.0f},{rect.y0:.0f},{rect.x1:.0f},{rect.y1:.0f}) (0.35 pts)")
                    total_score += 0.35
                else:
                    # Still give partial credit if content matches but position is off
                    print(f"PARTIAL: Component 4 — FreeText 'ACTION NEEDED' found but y0={rect.y0:.0f} "
                          f"is not at the top (expected y0 < 200). Awarding 0.20 pts")
                    total_score += 0.20
                break
        if not found_freetext:
            all_contents = [a.info.get("content", "") for a in freetext_annots]
            print(f"FAIL: Component 4 — No FreeText annotation with 'ACTION NEEDED' on page 5. "
                  f"Found {len(freetext_annots)} FreeText annots with contents: {all_contents}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/Documents/{TASK_ID}_annotated.pdf'
# Task specifies output as draft_report_annotated.pdf
file_path = f'{WORKDIR}/Documents/draft_report_annotated.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
