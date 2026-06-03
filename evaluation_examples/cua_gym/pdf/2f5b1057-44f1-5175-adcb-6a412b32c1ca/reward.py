"""
Reward Script: Combine two landscape PDFs side by side on a single portrait page
Task ID: pdf_ro_044
Domain: pdf
Scoring:
  Component 1: combined.pdf is a single Letter portrait page (612x792) — 0.30 pts
  Component 2: Contains text from left.pdf (Revenue chart) — 0.25 pts
  Component 3: Contains text from right.pdf (Active Users chart) — 0.25 pts
  Component 4: Side-by-side layout (left content in left half, right in right half) — 0.20 pts
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_044'

COMBINED_PATH = os.path.join(WORKDIR, 'Documents', 'combined.pdf')
LEFT_PATH = os.path.join(WORKDIR, 'Documents', 'left.pdf')
RIGHT_PATH = os.path.join(WORKDIR, 'Documents', 'right.pdf')

# Distinctive strings from each source PDF
LEFT_MARKERS = ["Q4 2025 Revenue by Department", "Engineering", "Westbridge"]
RIGHT_MARKERS = ["Monthly Active Users by Region", "North America", "Meridian"]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: combined.pdf must exist
    if not os.path.exists(COMBINED_PATH):
        print(f"CRITICAL: combined.pdf not found at {COMBINED_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(COMBINED_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open combined.pdf: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Single page, Letter portrait (612x792) — 0.30 points
    try:
        page_count = doc.page_count
        if page_count != 1:
            print(f"FAIL: Component 1 — expected 1 page, found {page_count}")
        else:
            page = doc[0]
            w, h = page.rect.width, page.rect.height
            # Letter size: 612x792, tolerance of 2 points
            is_letter_width = abs(w - 612.0) <= 2.0
            is_letter_height = abs(h - 792.0) <= 2.0
            is_portrait = h > w

            if is_letter_width and is_letter_height and is_portrait:
                print(f"PASS: Component 1 — single page, Letter portrait ({w}x{h}) (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 1 — page size {w}x{h}, expected ~612x792 portrait")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Extract text from combined.pdf for content checks
    try:
        page = doc[0]
        full_text = page.get_text("text")
    except Exception as e:
        print(f"ERROR: Cannot extract text from combined.pdf: {e}")
        doc.close()
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Contains text from left.pdf (Revenue chart) — 0.25 points
    try:
        left_found = 0
        for marker in LEFT_MARKERS:
            if marker in full_text:
                left_found += 1
                print(f"  LEFT marker found: {marker}")
            else:
                print(f"  LEFT marker missing: {marker}")

        if left_found == len(LEFT_MARKERS):
            print(f"PASS: Component 2 — all {left_found}/{len(LEFT_MARKERS)} left.pdf markers present (0.25 pts)")
            total_score += 0.25
        elif left_found > 0:
            partial = 0.25 * (left_found / len(LEFT_MARKERS))
            print(f"PARTIAL: Component 2 — {left_found}/{len(LEFT_MARKERS)} left.pdf markers ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — no left.pdf content found in combined.pdf")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Contains text from right.pdf (Active Users chart) — 0.25 points
    try:
        right_found = 0
        for marker in RIGHT_MARKERS:
            if marker in full_text:
                right_found += 1
                print(f"  RIGHT marker found: {marker}")
            else:
                print(f"  RIGHT marker missing: {marker}")

        if right_found == len(RIGHT_MARKERS):
            print(f"PASS: Component 3 — all {right_found}/{len(RIGHT_MARKERS)} right.pdf markers present (0.25 pts)")
            total_score += 0.25
        elif right_found > 0:
            partial = 0.25 * (right_found / len(RIGHT_MARKERS))
            print(f"PARTIAL: Component 3 — {right_found}/{len(RIGHT_MARKERS)} right.pdf markers ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — no right.pdf content found in combined.pdf")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Side-by-side layout — left content in left half, right in right half — 0.20 points
    try:
        page = doc[0]
        page_width = page.rect.width
        midpoint = page_width / 2.0  # ~306 for Letter

        blocks = page.get_text("blocks")

        # Classify blocks by their distinctive markers
        left_block_xs = []
        right_block_xs = []

        for b in blocks:
            x0, y0, x1, y1 = b[0], b[1], b[2], b[3]
            text = b[4] if len(b) > 4 else ""
            center_x = (x0 + x1) / 2.0

            # Check if block contains left.pdf markers
            for marker in LEFT_MARKERS:
                if marker in text:
                    left_block_xs.append(center_x)
                    break

            # Check if block contains right.pdf markers
            for marker in RIGHT_MARKERS:
                if marker in text:
                    right_block_xs.append(center_x)
                    break

        left_in_left_half = all(x < midpoint for x in left_block_xs) if left_block_xs else False
        right_in_right_half = all(x >= midpoint for x in right_block_xs) if right_block_xs else False

        if left_block_xs and right_block_xs and left_in_left_half and right_in_right_half:
            print(f"PASS: Component 4 — left content centered at x={sum(left_block_xs)/len(left_block_xs):.1f} (< {midpoint:.1f}), "
                  f"right content centered at x={sum(right_block_xs)/len(right_block_xs):.1f} (>= {midpoint:.1f}) (0.20 pts)")
            total_score += 0.20
        elif left_block_xs and right_block_xs:
            # Partial: at least both sources detected, but positioning wrong
            left_avg = sum(left_block_xs) / len(left_block_xs)
            right_avg = sum(right_block_xs) / len(right_block_xs)
            if left_avg < right_avg:
                # At least the relative order is correct
                print(f"PARTIAL: Component 4 — correct left-right order (left avg x={left_avg:.1f}, right avg x={right_avg:.1f}) but not cleanly split at midpoint (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — left avg x={left_avg:.1f}, right avg x={right_avg:.1f} — wrong order or overlapping")
        else:
            print(f"FAIL: Component 4 — could not detect distinctive markers in text blocks "
                  f"(left blocks: {len(left_block_xs)}, right blocks: {len(right_block_xs)})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(COMBINED_PATH):
    print(f"File not found: {COMBINED_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
