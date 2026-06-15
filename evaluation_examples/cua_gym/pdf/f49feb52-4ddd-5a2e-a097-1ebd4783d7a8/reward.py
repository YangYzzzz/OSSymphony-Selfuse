"""
Reward Script: Create a PDF cover page with centered title, colored background, separator, and author info.
Task ID: pdf_cr_038
Domain: pdf
Scoring:
  Component 1: PDF exists, 1 page, A4 size (0.15)
  Component 2: Dark blue background rectangle (0.20)
  Component 3: Title text present with bold white styling (0.25)
  Component 4: Subtitle, author, date text present (0.20)
  Component 5: White horizontal line separator (0.10)
  Component 6: Title centered in page center region (0.10)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_038'

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PDF has 1 page with A4 dimensions (0.15 points)
    try:
        page_count = doc.page_count
        if page_count == 1:
            page = doc[0]
            w, h = page.rect.width, page.rect.height
            # A4 is 595x842 pts, allow some tolerance
            if abs(w - 595) <= 5 and abs(h - 842) <= 5:
                print(f"PASS: Component 1 — 1 page, A4 size ({w}x{h}) (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — Page size {w}x{h}, expected ~595x842")
        else:
            print(f"FAIL: Component 1 — Page count {page_count}, expected 1")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    page = doc[0]

    # Component 2: Dark blue background rectangle fill ~(0, 0.1, 0.3) (0.20 points)
    try:
        drawings = page.get_drawings()
        found_dark_blue_rect = False
        for d in drawings:
            fill = d.get("fill")
            if fill and len(fill) == 3:
                r, g, b = fill
                # Dark blue: R close to 0, G close to 0.1, B close to 0.3
                # Allow tolerance for different generation methods
                if r < 0.15 and g < 0.25 and b > 0.15 and b < 0.5:
                    # Check it covers a significant portion of the page (background rect)
                    rect = d.get("rect")
                    if rect:
                        rect_area = rect.width * rect.height
                        page_area = page.rect.width * page.rect.height
                        if rect_area > page_area * 0.8:
                            found_dark_blue_rect = True
                            print(f"PASS: Component 2 — Dark blue background rect found, fill={fill}, rect={rect} (0.20 pts)")
                            break
        if not found_dark_blue_rect:
            # Also check if any drawing has a dark blue fill even if not full-page
            for d in drawings:
                fill = d.get("fill")
                if fill and len(fill) == 3:
                    r, g, b = fill
                    if r < 0.15 and g < 0.25 and b > 0.15 and b < 0.5:
                        found_dark_blue_rect = True
                        print(f"PASS: Component 2 — Dark blue drawing found (not full-page), fill={fill} (0.20 pts)")
                        break
        if found_dark_blue_rect:
            total_score += 0.20
        else:
            fills = [d.get("fill") for d in drawings]
            print(f"FAIL: Component 2 — No dark blue background found. Drawing fills: {fills}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Title 'Strategic Technology Roadmap' in bold white ~30pt (0.25 points)
    try:
        data = page.get_text("dict")
        title_found = False
        title_bold_white = False
        for block in data["blocks"]:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    if "Strategic Technology Roadmap" in span["text"]:
                        title_found = True
                        c = span["color"]
                        rgb = (c >> 16 & 0xFF, c >> 8 & 0xFF, c & 0xFF)
                        is_bold = bool(span["flags"] & 16)
                        size = span["size"]
                        # Check: bold, white (RGB close to 255,255,255), size >= 24pt
                        white_enough = all(v > 200 for v in rgb)
                        size_ok = size >= 24
                        if is_bold and white_enough and size_ok:
                            title_bold_white = True
                            print(f"PASS: Component 3 — Title found: bold={is_bold}, rgb={rgb}, size={size} (0.25 pts)")
                        else:
                            print(f"FAIL: Component 3 — Title found but style wrong: bold={is_bold}, rgb={rgb}, size={size}")
                        break
                if title_found:
                    break
            if title_found:
                break
        if title_bold_white:
            total_score += 0.25
        elif not title_found:
            print(f"FAIL: Component 3 — Title 'Strategic Technology Roadmap' not found in text")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Subtitle, author, and date text present (0.20 points)
    # Check for: 'Board of Directors', 'Technology Strategy Division', 'March 2024'
    try:
        full_text = page.get_text("text")
        required_strings = [
            "Board of Directors",
            "Technology Strategy Division",
            "March 2024",
        ]
        found_count = 0
        for s in required_strings:
            if s in full_text:
                found_count += 1
                print(f"  Found: '{s}'")
            else:
                print(f"  Missing: '{s}'")

        if found_count == len(required_strings):
            print(f"PASS: Component 4 — All required text strings present ({found_count}/{len(required_strings)}) (0.20 pts)")
            total_score += 0.20
        elif found_count > 0:
            partial = round(0.20 * found_count / len(required_strings), 2)
            print(f"PARTIAL: Component 4 — {found_count}/{len(required_strings)} strings found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — None of the required text strings found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: White horizontal line separator (0.10 points)
    try:
        drawings = page.get_drawings()
        found_white_line = False
        for d in drawings:
            color = d.get("color")
            fill = d.get("fill")
            items = d.get("items", [])
            # Look for a line ('l' item) with white color
            has_line_item = any(item[0] == 'l' for item in items)
            if has_line_item:
                # Check if stroke color is white
                is_white_stroke = False
                if color and len(color) == 3:
                    if all(v > 0.8 for v in color):
                        is_white_stroke = True
                if is_white_stroke:
                    found_white_line = True
                    print(f"PASS: Component 5 — White line separator found, color={color} (0.10 pts)")
                    break
        if found_white_line:
            total_score += 0.10
        else:
            line_colors = []
            for d in drawings:
                items = d.get("items", [])
                if any(item[0] == 'l' for item in items):
                    line_colors.append(d.get("color"))
            print(f"FAIL: Component 5 — No white line separator found. Line colors: {line_colors}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Title text centered in page center region (0.10 points)
    try:
        instances = page.search_for("Strategic Technology Roadmap")
        if instances:
            rect = instances[0]
            cx = rect.x0 + rect.width / 2
            cy = rect.y0 + rect.height / 2
            pw, ph = page.rect.width, page.rect.height
            # Check horizontal centering: center x within middle 50% of page
            h_centered = pw * 0.25 < cx < pw * 0.75
            # Check vertical: title should be roughly in center region (25%-75% of page height)
            v_centered = ph * 0.2 < cy < ph * 0.7
            if h_centered and v_centered:
                print(f"PASS: Component 6 — Title centered at ({cx:.1f}, {cy:.1f}) on {pw}x{ph} page (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 — Title at ({cx:.1f}, {cy:.1f}), h_centered={h_centered}, v_centered={v_centered}")
        else:
            print(f"FAIL: Component 6 — Could not find title text for position check")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Desktop/cover_page.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
