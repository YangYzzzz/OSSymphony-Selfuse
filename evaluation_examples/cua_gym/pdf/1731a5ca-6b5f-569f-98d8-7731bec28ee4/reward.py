"""
Reward Script: Extract chart from PDF, annotate with text box and red arrow,
               save as PNG, then insert into new 1-page PDF.
Task ID: pdf_cross_079
Domain: pdf
Scoring:
  Component 1: annotated_chart.png exists                          (0.20 pts)
  Component 2: annotated_chart.png contains red annotation (arrow) (0.30 pts)
  Component 3: annotated_chart.png has white text box in top-left  (0.20 pts)
  Component 4: chart_standalone.pdf is a valid 1-page PDF          (0.15 pts)
  Component 5: chart_standalone.pdf embeds the annotated image     (0.15 pts)
  Total: 1.00
"""

import os
import sys

WORKDIR = '/home/user/Documents'
TASK_ID = 'pdf_cross_079'

PNG_PATH = os.path.join(WORKDIR, 'annotated_chart.png')
PDF_PATH = os.path.join(WORKDIR, 'chart_standalone.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: annotated_chart.png exists (0.20 points)
    # This file should NOT exist on initial_env (only market_analysis.pdf is present initially)
    try:
        if os.path.exists(PNG_PATH):
            # Verify it's a valid PNG of meaningful size (> 10KB)
            size = os.path.getsize(PNG_PATH)
            if size > 10000:
                print(f"PASS: Component 1 — annotated_chart.png exists, size={size} bytes (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 — annotated_chart.png too small ({size} bytes), likely empty/corrupt")
        else:
            print(f"FAIL: Component 1 — annotated_chart.png not found at {PNG_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: annotated_chart.png contains a red arrow (0.30 points)
    # The task requires a red arrow pointing to the highest bar (TechCorp at 32%).
    # A red arrow = significant number of strongly-red pixels (R high, G/B low)
    try:
        from PIL import Image
        import numpy as np

        if os.path.exists(PNG_PATH):
            img = Image.open(PNG_PATH)
            img_arr = np.array(img.convert('RGB'))
            h, w = img_arr.shape[:2]

            # Strong red pixels: R > 180, G < 80, B < 80
            red_mask = (img_arr[:, :, 0] > 180) & (img_arr[:, :, 1] < 80) & (img_arr[:, :, 2] < 80)
            red_count = int(np.sum(red_mask))

            # A meaningful arrow should have at least 500 red pixels
            # The golden artifact has ~2304 red pixels in the arrow
            if red_count >= 500:
                print(f"PASS: Component 2 — Red arrow found ({red_count} red pixels) in annotated_chart.png (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 — Insufficient red pixels ({red_count}) in annotated_chart.png; "
                      f"expected >= 500 for a red arrow")
        else:
            print(f"FAIL: Component 2 — annotated_chart.png not found, cannot check for red arrow")
    except ImportError:
        print("ERROR: Component 2 — PIL/numpy not available")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: annotated_chart.png has a white-background text box in top-left (0.20 points)
    # The task requires: 'text annotation box in the top-left with white background'
    # containing 'Source: Market Analysis Report 2025\nPage 4, Figure 3'
    # Verification: the top-left region should have a distinctly white rectangular area
    # with dark text pixels (the text inside the box).
    try:
        from PIL import Image
        import numpy as np

        if os.path.exists(PNG_PATH):
            img = Image.open(PNG_PATH)
            img_arr = np.array(img.convert('RGB'))
            h, w = img_arr.shape[:2]

            # Check top-left quadrant (top 25% height, left 40% width)
            tl_h = h // 4
            tl_w = int(w * 0.4)
            tl_region = img_arr[:tl_h, :tl_w]

            # Look for dark text pixels (R<100, G<100, B<100) indicating text
            dark_mask = (tl_region[:, :, 0] < 100) & (tl_region[:, :, 1] < 100) & (tl_region[:, :, 2] < 100)
            dark_count = int(np.sum(dark_mask))

            # Also check that the region contains white (background of text box)
            white_mask = (tl_region[:, :, 0] > 240) & (tl_region[:, :, 1] > 240) & (tl_region[:, :, 2] > 240)
            white_count = int(np.sum(white_mask))
            total_tl_pixels = tl_h * tl_w

            # A text box should have at least some dark text and substantial white background
            # Dark text >= 500 pixels AND white ratio >= 20%
            white_ratio = white_count / total_tl_pixels
            has_text_pixels = dark_count >= 500
            has_white_bg = white_ratio >= 0.20

            if has_text_pixels and has_white_bg:
                print(f"PASS: Component 3 — Top-left text box found: {dark_count} dark (text) pixels, "
                      f"{white_ratio:.1%} white background in top-left quadrant (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — Top-left text box not detected; "
                      f"dark_pixels={dark_count} (need>=500), white_ratio={white_ratio:.1%} (need>=20%)")
        else:
            print(f"FAIL: Component 3 — annotated_chart.png not found, cannot check text box")
    except ImportError:
        print("ERROR: Component 3 — PIL/numpy not available")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: chart_standalone.pdf is a valid 1-page PDF (0.15 points)
    # The task requires creating a new 1-page PDF containing the annotated chart image.
    # This file should NOT exist on initial_env.
    try:
        try:
            import pymupdf
            _fitz = pymupdf
        except ImportError:
            import fitz as _fitz

        if os.path.exists(PDF_PATH):
            doc = _fitz.open(PDF_PATH)
            page_count = doc.page_count
            doc.close()
            if page_count == 1:
                print(f"PASS: Component 4 — chart_standalone.pdf is a valid 1-page PDF (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — chart_standalone.pdf has {page_count} pages; expected exactly 1")
        else:
            print(f"FAIL: Component 4 — chart_standalone.pdf not found at {PDF_PATH}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: chart_standalone.pdf contains an embedded image (the annotated chart) (0.15 points)
    # The PDF should embed the annotated_chart.png as an image resource.
    # We verify that page 0 contains at least 1 image object.
    try:
        try:
            import pymupdf
            _fitz = pymupdf
        except ImportError:
            import fitz as _fitz

        if os.path.exists(PDF_PATH):
            doc = _fitz.open(PDF_PATH)
            if doc.page_count >= 1:
                page = doc[0]
                images = page.get_images()
                image_count = len(images)
                if image_count >= 1:
                    # Verify the embedded image has substantial dimensions
                    xref = images[0][0]
                    img_data = doc.extract_image(xref)
                    img_w = img_data.get('width', 0)
                    img_h = img_data.get('height', 0)
                    doc.close()
                    if img_w > 100 and img_h > 100:
                        print(f"PASS: Component 5 — chart_standalone.pdf embeds {image_count} image(s), "
                              f"first image={img_w}x{img_h}px (0.15 pts)")
                        total_score += 0.15
                    else:
                        print(f"FAIL: Component 5 — Embedded image too small: {img_w}x{img_h}px; "
                              f"expected substantial annotated chart image")
                else:
                    doc.close()
                    print(f"FAIL: Component 5 — chart_standalone.pdf has 0 images on page 0; "
                          f"annotated chart image not found")
            else:
                doc.close()
                print(f"FAIL: Component 5 — chart_standalone.pdf has no pages")
        else:
            print(f"FAIL: Component 5 — chart_standalone.pdf not found, cannot verify embedded image")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score:.1f}")
    return final_score


if __name__ == "__main__":
    verify_task()
