"""
Reward Script: Overlay grid pattern on PDF to create graph paper
Task ID: pdf_ro_041
Domain: pdf
Scoring:
  Component 1 (0.15): graph_paper.pdf exists with 5 Letter-size pages
  Component 2 (0.20): All pages have grid drawings (lines present)
  Component 3 (0.20): Line color is #CCCCCC (0.8, 0.8, 0.8) with ~0.5pt width
  Component 4 (0.25): Sufficient horizontal lines per page (>=20)
  Component 5 (0.20): Sufficient vertical lines per page (>=20)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_041'


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

    # Component 1: File has 5 Letter-size pages (0.15 points)
    try:
        page_count = doc.page_count
        if page_count == 5:
            # Check all pages are Letter size (612x792)
            non_letter_pages = [
                i for i in range(page_count)
                if abs(round(doc[i].rect.width) - 612) > 5
                or abs(round(doc[i].rect.height) - 792) > 5
            ]
            if len(non_letter_pages) == 0:
                print(f"PASS: Component 1 — 5 Letter-size pages found (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — Not all pages are Letter size")
        else:
            print(f"FAIL: Component 1 — Expected 5 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 5 pages have grid drawings (0.20 points)
    try:
        pages_with_drawings = 0
        for i in range(min(doc.page_count, 5)):
            drawings = doc[i].get_drawings()
            if len(drawings) >= 10:  # need substantial drawings for a grid
                pages_with_drawings += 1
        if pages_with_drawings == 5:
            print(f"PASS: Component 2 — All 5 pages have grid drawings (0.20 pts)")
            total_score += 0.20
        elif pages_with_drawings > 0:
            partial = round(0.20 * pages_with_drawings / 5, 2)
            print(f"PARTIAL: Component 2 — {pages_with_drawings}/5 pages have drawings ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No pages have grid drawings")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Line color is #CCCCCC (0.8, 0.8, 0.8) and width ~0.5pt (0.20 points)
    try:
        expected_color = (0.8, 0.8, 0.8)
        pages_correct_color = 0
        pages_correct_width = 0

        for i in range(min(doc.page_count, 5)):
            drawings = doc[i].get_drawings()
            if not drawings:
                continue

            # Check if majority of drawings have the correct color
            color_match_count = 0
            width_match_count = 0
            for d in drawings:
                c = d.get('color')
                if c and all(abs(a - e) < 0.05 for a, e in zip(c, expected_color)):
                    color_match_count += 1
                w = d.get('width')
                if w is not None and abs(w - 0.5) < 0.2:
                    width_match_count += 1

            if color_match_count >= len(drawings) * 0.8:
                pages_correct_color += 1
            if width_match_count >= len(drawings) * 0.8:
                pages_correct_width += 1

        color_ok = pages_correct_color == 5
        width_ok = pages_correct_width == 5

        if color_ok and width_ok:
            print(f"PASS: Component 3 — Color #CCCCCC and width 0.5pt correct on all pages (0.20 pts)")
            total_score += 0.20
        elif color_ok:
            print(f"PARTIAL: Component 3 — Color correct but width wrong (0.10 pts)")
            total_score += 0.10
        elif width_ok:
            print(f"PARTIAL: Component 3 — Width correct but color wrong (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — Color and width incorrect (color_pages={pages_correct_color}, width_pages={pages_correct_width})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Sufficient horizontal lines per page (0.25 points)
    # Task says ~44 horizontal lines per page (every 18pts across 792pt height)
    # Golden has ~90 per page (some drawings bundle multiple segments)
    # Accept >= 20 as minimum threshold for a real grid
    try:
        pages_with_enough_horiz = 0
        for i in range(min(doc.page_count, 5)):
            drawings = doc[i].get_drawings()
            horiz_count = 0
            for d in drawings:
                for item in d.get('items', []):
                    if item[0] == 'l':
                        p1, p2 = item[1], item[2]
                        if abs(p1.y - p2.y) < 1.0:  # horizontal line
                            horiz_count += 1
            if horiz_count >= 20:
                pages_with_enough_horiz += 1

        if pages_with_enough_horiz == 5:
            print(f"PASS: Component 4 — All pages have sufficient horizontal lines (0.25 pts)")
            total_score += 0.25
        elif pages_with_enough_horiz > 0:
            partial = round(0.25 * pages_with_enough_horiz / 5, 2)
            print(f"PARTIAL: Component 4 — {pages_with_enough_horiz}/5 pages have enough horiz lines ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No pages have sufficient horizontal lines")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Sufficient vertical lines per page (0.20 points)
    # Task says ~34 vertical lines per page (every 18pts across 612pt width)
    # Golden has ~70 per page. Accept >= 20 as minimum threshold.
    try:
        pages_with_enough_vert = 0
        for i in range(min(doc.page_count, 5)):
            drawings = doc[i].get_drawings()
            vert_count = 0
            for d in drawings:
                for item in d.get('items', []):
                    if item[0] == 'l':
                        p1, p2 = item[1], item[2]
                        if abs(p1.x - p2.x) < 1.0:  # vertical line
                            vert_count += 1
            if vert_count >= 20:
                pages_with_enough_vert += 1

        if pages_with_enough_vert == 5:
            print(f"PASS: Component 5 — All pages have sufficient vertical lines (0.20 pts)")
            total_score += 0.20
        elif pages_with_enough_vert > 0:
            partial = round(0.20 * pages_with_enough_vert / 5, 2)
            print(f"PARTIAL: Component 5 — {pages_with_enough_vert}/5 pages have enough vert lines ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — No pages have sufficient vertical lines")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/graph_paper.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
