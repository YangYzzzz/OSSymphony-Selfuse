"""
Reward Script: Add 'ACCEPTED' green text stamp on page 1 top-right of camera_ready.pdf
Task ID: pdf_res_053
Domain: pdf
Scoring:
  Component 1: Output file exists and is valid PDF (0.15)
  Component 2: All 8 pages preserved (0.15)
  Component 3: Page 1 contains 'ACCEPTED' text (0.35)
  Component 4: 'ACCEPTED' positioned in top-right area (0.20)
  Component 5: 'ACCEPTED' text is green (0.15)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_053'

def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    output_path = os.path.join(WORKDIR, 'papers', 'camera_ready_stamped.pdf')

    # Component 1: Output file exists and is a valid PDF (0.15 points)
    try:
        import fitz
        if not os.path.exists(output_path):
            print(f"FAIL: Component 1 — output file {output_path} does not exist")
            print("REWARD: 0.0")
            return 0.0
        doc = fitz.open(output_path)
        if len(doc) == 0:
            print("FAIL: Component 1 — PDF has 0 pages (corrupt or empty)")
            print("REWARD: 0.0")
            return 0.0
        print(f"PASS: Component 1 — output file exists and is valid PDF ({len(doc)} pages) (0.15 pts)")
        total_score += 0.15
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: All 8 pages preserved (0.15 points)
    try:
        page_count = len(doc)
        if page_count == 8:
            print(f"PASS: Component 2 — all 8 pages preserved (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — expected 8 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Page 1 contains 'ACCEPTED' text (0.35 points)
    accepted_found = False
    try:
        page = doc[0]
        text = page.get_text()
        if 'ACCEPTED' in text:
            accepted_found = True
            print(f"PASS: Component 3 — 'ACCEPTED' found in page 1 text (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 3 — 'ACCEPTED' not found in page 1 text")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 'ACCEPTED' positioned in top-right area (0.20 points)
    # Top-right: x > page_width/2, y < page_height/4
    try:
        if accepted_found:
            page = doc[0]
            page_width = page.rect.width
            page_height = page.rect.height
            blocks = page.get_text('dict')['blocks']
            found_top_right = False
            for b in blocks:
                if b.get('type') != 0:
                    continue
                for line in b.get('lines', []):
                    for span in line.get('spans', []):
                        if 'ACCEPTED' in span.get('text', ''):
                            origin = span.get('origin', (0, 0))
                            bbox = span.get('bbox', (0, 0, 0, 0))
                            # Check: text is in right half (x > width/2) and top quarter (y < height/4)
                            x_pos = origin[0] if origin else bbox[0]
                            y_pos = origin[1] if origin else bbox[1]
                            if x_pos > page_width / 2 and y_pos < page_height / 4:
                                found_top_right = True
                                print(f"PASS: Component 4 — 'ACCEPTED' at ({x_pos:.0f}, {y_pos:.0f}), top-right of page (width={page_width:.0f}, height={page_height:.0f}) (0.20 pts)")
                                break
                    if found_top_right:
                        break
                if found_top_right:
                    break
            if found_top_right:
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — 'ACCEPTED' not positioned in top-right area")
        else:
            print(f"FAIL: Component 4 — skipped (ACCEPTED text not found)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: 'ACCEPTED' text is green (0.15 points)
    # Green color: 0x008000 = 32768, or RGB close to (0, 0.5, 0) or (0, 1, 0)
    try:
        if accepted_found:
            page = doc[0]
            blocks = page.get_text('dict')['blocks']
            found_green = False
            color_checked = False
            for b in blocks:
                if found_green or color_checked:
                    break
                if b.get('type') != 0:
                    continue
                for line in b.get('lines', []):
                    if found_green or color_checked:
                        break
                    for span in line.get('spans', []):
                        if 'ACCEPTED' in span.get('text', ''):
                            color_int = span.get('color', -1)
                            color_checked = True
                            # Extract RGB components from integer color
                            r = (color_int >> 16) & 0xFF
                            g = (color_int >> 8) & 0xFF
                            b_val = color_int & 0xFF
                            # Green means: g component is dominant, r and b are low
                            if g > 64 and g > r and g > b_val:
                                found_green = True
                                print(f"PASS: Component 5 — 'ACCEPTED' color is green (R={r}, G={g}, B={b_val}, int={color_int}) (0.15 pts)")
                            else:
                                print(f"FAIL: Component 5 — 'ACCEPTED' color not green (R={r}, G={g}, B={b_val}, int={color_int})")
                            break
            if found_green:
                total_score += 0.15
            elif not color_checked:
                print(f"FAIL: Component 5 — could not find ACCEPTED span to check color")
        else:
            print(f"FAIL: Component 5 — skipped (ACCEPTED text not found)")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
