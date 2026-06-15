"""
Reward Script: Add semi-transparent blue rectangle overlay on page 3 of a PDF
Task ID: pdf_res_083
Domain: pdf
Scoring:
  - Component 1 (0.15): Output file exists at /home/user/papers/highlight_region_marked.pdf
  - Component 2 (0.15): PDF has 7 pages (same as original)
  - Component 3 (0.40): Page 3 (0-indexed page 2) has a blue-filled rectangle at region (50, 200, 550, 400)
  - Component 4 (0.30): The blue rectangle has semi-transparency (fill_opacity < 1.0)
"""

import os
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    import pymupdf as fitz

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_083'
OUTPUT_PATH = f'{WORKDIR}/papers/highlight_region_marked.pdf'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists at the correct path (0.15 points)
    # NOTE: We only score this if the file is the OUTPUT file (not the original).
    # The initial_env should NOT have this file.
    try:
        if os.path.exists(file_path):
            print(f"PASS: Component 1 — Output file exists at {file_path} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Output file not found at {file_path}")
            print(f"REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"REWARD: 0.0")
        return 0.0

    # Load the PDF
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: PDF has 7 pages (0.15 points)
    try:
        page_count = doc.page_count
        if page_count == 7:
            print(f"PASS: Component 2 — PDF has 7 pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — Expected 7 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Page 3 (0-indexed page 2) has a blue-filled rectangle at region (50, 200, 550, 400) (0.40 points)
    try:
        page = doc[2]  # 0-indexed page 2 = page 3 in human terms
        drawings = page.get_drawings()

        # Look for a drawing with blue fill covering the target region
        target_rect = fitz.Rect(50, 200, 550, 400)
        blue_rect_found = False

        for d in drawings:
            d_fill = d.get("fill")
            d_rect = d.get("rect")
            if d_fill is None or d_rect is None:
                continue

            # Check if fill is blue: R ~0, G ~0, B ~1
            r, g, b = d_fill[0], d_fill[1], d_fill[2]
            is_blue = (r < 0.2 and g < 0.2 and b > 0.7)

            if not is_blue:
                continue

            # Check if rect approximately matches target (50, 200, 550, 400)
            rect = fitz.Rect(d_rect)
            tolerance = 5.0  # points tolerance
            rect_matches = (
                abs(rect.x0 - target_rect.x0) <= tolerance and
                abs(rect.y0 - target_rect.y0) <= tolerance and
                abs(rect.x1 - target_rect.x1) <= tolerance and
                abs(rect.y1 - target_rect.y1) <= tolerance
            )

            if rect_matches:
                blue_rect_found = True
                print(f"PASS: Component 3 — Blue rectangle found at {tuple(rect)} with fill={d_fill} (0.40 pts)")
                total_score += 0.40
                break

        if not blue_rect_found:
            print(f"FAIL: Component 3 — No blue-filled rectangle found at region (50, 200, 550, 400) on page 3")
            # Print what we did find for debugging
            for i, d in enumerate(drawings):
                if d.get("fill"):
                    print(f"  Drawing {i}: rect={d.get('rect')}, fill={d.get('fill')}, fill_opacity={d.get('fill_opacity')}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: The blue rectangle has semi-transparency (fill_opacity < 1.0) (0.30 points)
    try:
        page = doc[2]
        drawings = page.get_drawings()
        semi_transparent_blue_found = False

        for d in drawings:
            d_fill = d.get("fill")
            d_rect = d.get("rect")
            d_fill_opacity = d.get("fill_opacity")
            if d_fill is None or d_rect is None:
                continue

            # Check blue fill
            r, g, b = d_fill[0], d_fill[1], d_fill[2]
            is_blue = (r < 0.2 and g < 0.2 and b > 0.7)
            if not is_blue:
                continue

            # Check rect matches target
            rect = fitz.Rect(d_rect)
            tolerance = 5.0
            rect_matches = (
                abs(rect.x0 - target_rect.x0) <= tolerance and
                abs(rect.y0 - target_rect.y0) <= tolerance and
                abs(rect.x1 - target_rect.x1) <= tolerance and
                abs(rect.y1 - target_rect.y1) <= tolerance
            )
            if not rect_matches:
                continue

            # Check semi-transparency: fill_opacity should be > 0 and < 1.0
            if d_fill_opacity is not None and 0.0 < d_fill_opacity < 1.0:
                semi_transparent_blue_found = True
                print(f"PASS: Component 4 — Blue rectangle has semi-transparency (fill_opacity={d_fill_opacity}) (0.30 pts)")
                total_score += 0.30
                break

        if not semi_transparent_blue_found:
            print(f"FAIL: Component 4 — Blue rectangle does not have semi-transparency (fill_opacity should be between 0 and 1 exclusive)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)
