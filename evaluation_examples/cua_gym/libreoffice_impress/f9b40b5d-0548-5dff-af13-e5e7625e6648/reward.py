"""
Reward Script: Export presentation as PDF handout (3 slides/page with note lines)
Task ID: impress_el_018
Domain: libreoffice_impress
Scoring:
  Component 1: PDF file exists at expected path (0.15)
  Component 2: PDF has exactly 3 pages (0.25)
  Component 3: Each page has 3 slide thumbnail images (0.25)
  Component 4: Horizontal note-taking lines present on each page (0.25)
  Component 5: PDF page size is portrait/standard handout (0.10)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'impress_el_018'


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice state before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: PDF file exists (0.15 points)
    # This is a task-introduced change: no PDF exists initially.
    try:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 1000:
            print(f"PASS: Component 1 — PDF file exists at {file_path} "
                  f"(size: {os.path.getsize(file_path)} bytes) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — PDF file not found or too small at {file_path}")
            print(f"REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"REWARD: 0.0")
        return 0.0

    # Load PDF with PyMuPDF (fitz)
    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: PDF has exactly 3 pages (9 slides / 3 per page) (0.25 points)
    try:
        page_count = doc.page_count
        if page_count == 3:
            print(f"PASS: Component 2 — PDF has 3 pages (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Expected 3 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Each page has exactly 3 images (slide thumbnails) (0.25 points)
    # Handout layout with 3 slides per page means 3 embedded images per page
    try:
        pages_with_3_images = 0
        actual_page_count = min(doc.page_count, 10)  # safety cap
        for i in range(actual_page_count):
            page = doc[i]
            images = page.get_images()
            img_count = len(images)
            if img_count == 3:
                pages_with_3_images += 1
            else:
                print(f"  Page {i+1}: expected 3 images, found {img_count}")

        if actual_page_count > 0 and pages_with_3_images == actual_page_count:
            print(f"PASS: Component 3 — All {actual_page_count} pages have 3 slide "
                  f"thumbnails each (0.25 pts)")
            total_score += 0.25
        elif actual_page_count > 0 and pages_with_3_images > 0:
            partial = 0.25 * (pages_with_3_images / actual_page_count)
            print(f"PARTIAL: Component 3 — {pages_with_3_images}/{actual_page_count} "
                  f"pages have 3 images ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No pages have 3 slide thumbnails")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Horizontal note-taking lines present on each page (0.25 points)
    # The handout format with lines should have ruled horizontal lines next to each slide.
    # We expect multiple horizontal lines (>= 10 per page) on the right side.
    try:
        pages_with_lines = 0
        for i in range(min(doc.page_count, 10)):
            page = doc[i]
            paths = page.get_drawings()
            horizontal_lines = 0
            for path in paths:
                for item in path.get('items', []):
                    if item[0] == 'l':  # line segment
                        p1, p2 = item[1], item[2]
                        # Horizontal line: y-coordinates nearly equal
                        if abs(p1.y - p2.y) < 2:
                            # Line has meaningful length (> 50 pts)
                            if abs(p2.x - p1.x) > 50:
                                horizontal_lines += 1

            if horizontal_lines >= 10:
                pages_with_lines += 1
                print(f"  Page {i+1}: {horizontal_lines} note-taking lines found")
            else:
                print(f"  Page {i+1}: only {horizontal_lines} horizontal lines "
                      f"(expected >= 10)")

        actual_page_count = min(doc.page_count, 10)
        if actual_page_count > 0 and pages_with_lines == actual_page_count:
            print(f"PASS: Component 4 — All {actual_page_count} pages have note-taking "
                  f"lines (0.25 pts)")
            total_score += 0.25
        elif actual_page_count > 0 and pages_with_lines > 0:
            partial = 0.25 * (pages_with_lines / actual_page_count)
            print(f"PARTIAL: Component 4 — {pages_with_lines}/{actual_page_count} "
                  f"pages have lines ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No pages have note-taking lines")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: PDF page size is portrait (height > width) (0.10 points)
    # Handout PDFs should be in portrait orientation (e.g., A4 or Letter)
    try:
        if doc.page_count > 0:
            page = doc[0]
            rect = page.rect
            if rect.height > rect.width:
                print(f"PASS: Component 5 — PDF is portrait orientation "
                      f"({rect.width:.1f}x{rect.height:.1f}) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — PDF is landscape "
                      f"({rect.width:.1f}x{rect.height:.1f}), expected portrait")
        else:
            print(f"FAIL: Component 5 — No pages in PDF")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification
persist_app_state("libreoffice_impress")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
