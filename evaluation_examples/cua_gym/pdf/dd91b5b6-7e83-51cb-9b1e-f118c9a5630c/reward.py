"""
Reward Script: Batch stamp PDFs with 'REVIEWED 2026-04-01' at top-right of page 1
Task ID: pdf_gf2_026
Domain: pdf
Scoring:
  Component 1 (0.30): All 6 _reviewed.pdf files exist
  Component 2 (0.20): Each reviewed file has same page count as its source
  Component 3 (0.30): Each reviewed file contains 'REVIEWED 2026-04-01' on page 1
  Component 4 (0.20): Stamp text is positioned in top-right area of page 1
"""

import os
import pymupdf

WORKDIR = '/home/user'
REPORTS_DIR = os.path.join(WORKDIR, 'Documents', 'reports')

# The 6 source files and their expected reviewed counterparts
SOURCE_FILES = [
    'report_q1.pdf',
    'report_q2.pdf',
    'report_q3.pdf',
    'report_q4.pdf',
    'report_annual.pdf',
    'report_summary.pdf',
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: reports directory exists
    if not os.path.isdir(REPORTS_DIR):
        print(f"CRITICAL: Reports directory not found: {REPORTS_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All 6 _reviewed.pdf files exist (0.30 points)
    try:
        existing_reviewed = []
        for sf in SOURCE_FILES:
            reviewed_name = sf.replace('.pdf', '_reviewed.pdf')
            reviewed_path = os.path.join(REPORTS_DIR, reviewed_name)
            if os.path.isfile(reviewed_path):
                existing_reviewed.append(reviewed_name)
            else:
                print(f"FAIL: Component 1 — Missing reviewed file: {reviewed_name}")

        if len(existing_reviewed) == 6:
            print(f"PASS: Component 1 — All 6 reviewed files exist (0.30 pts)")
            total_score += 0.30
        elif len(existing_reviewed) > 0:
            partial = 0.30 * (len(existing_reviewed) / 6.0)
            print(f"PARTIAL: Component 1 — {len(existing_reviewed)}/6 reviewed files exist ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No reviewed files found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # If no reviewed files exist, no point checking further
    if not existing_reviewed:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Each reviewed file has same page count as source (0.20 points)
    try:
        page_count_matches = 0
        for sf in SOURCE_FILES:
            reviewed_name = sf.replace('.pdf', '_reviewed.pdf')
            src_path = os.path.join(REPORTS_DIR, sf)
            rev_path = os.path.join(REPORTS_DIR, reviewed_name)

            if not os.path.isfile(rev_path) or not os.path.isfile(src_path):
                continue

            src_doc = pymupdf.open(src_path)
            rev_doc = pymupdf.open(rev_path)
            src_pages = src_doc.page_count
            rev_pages = rev_doc.page_count
            src_doc.close()
            rev_doc.close()

            if src_pages == rev_pages:
                page_count_matches += 1
            else:
                print(f"FAIL: Component 2 — {reviewed_name}: expected {src_pages} pages, found {rev_pages}")

        if page_count_matches == len(existing_reviewed):
            print(f"PASS: Component 2 — All {page_count_matches} reviewed files have correct page counts (0.20 pts)")
            total_score += 0.20
        elif page_count_matches > 0:
            partial = 0.20 * (page_count_matches / len(existing_reviewed))
            print(f"PARTIAL: Component 2 — {page_count_matches}/{len(existing_reviewed)} files have correct page counts ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No reviewed files have correct page count")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Each reviewed file has 'REVIEWED 2026-04-01' text on page 1 (0.30 points)
    try:
        stamp_found_count = 0
        for sf in SOURCE_FILES:
            reviewed_name = sf.replace('.pdf', '_reviewed.pdf')
            rev_path = os.path.join(REPORTS_DIR, reviewed_name)

            if not os.path.isfile(rev_path):
                continue

            doc = pymupdf.open(rev_path)
            page = doc[0]
            text = page.get_text('text')
            doc.close()

            if 'REVIEWED 2026-04-01' in text:
                stamp_found_count += 1
            else:
                print(f"FAIL: Component 3 — {reviewed_name}: 'REVIEWED 2026-04-01' not found on page 1")

        if stamp_found_count == len(existing_reviewed):
            print(f"PASS: Component 3 — All {stamp_found_count} reviewed files have stamp text on page 1 (0.30 pts)")
            total_score += 0.30
        elif stamp_found_count > 0:
            partial = 0.30 * (stamp_found_count / len(existing_reviewed))
            print(f"PARTIAL: Component 3 — {stamp_found_count}/{len(existing_reviewed)} files have stamp text ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No reviewed files have stamp text")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Stamp is in top-right area of page 1 (0.20 points)
    # Top-right means: x position > 50% of page width, y position < 25% of page height
    try:
        position_correct_count = 0
        for sf in SOURCE_FILES:
            reviewed_name = sf.replace('.pdf', '_reviewed.pdf')
            rev_path = os.path.join(REPORTS_DIR, reviewed_name)

            if not os.path.isfile(rev_path):
                continue

            doc = pymupdf.open(rev_path)
            page = doc[0]
            pw = page.rect.width
            ph = page.rect.height

            instances = page.search_for('REVIEWED 2026-04-01')
            doc.close()

            if not instances:
                print(f"FAIL: Component 4 — {reviewed_name}: stamp text not found for position check")
                continue

            # Check position of the first instance
            rect = instances[0]
            # x center should be in right half, y center should be in top quarter
            cx = (rect.x0 + rect.x1) / 2.0
            cy = (rect.y0 + rect.y1) / 2.0

            if cx > pw * 0.5 and cy < ph * 0.25:
                position_correct_count += 1
            else:
                print(f"FAIL: Component 4 — {reviewed_name}: stamp at cx={cx:.1f}, cy={cy:.1f} "
                      f"(page {pw:.0f}x{ph:.0f}), expected top-right")

        checked_count = max(stamp_found_count, 1) if 'stamp_found_count' in dir() else len(existing_reviewed)
        # Only count against files that have the stamp (those checked in component 3)
        files_with_stamp = stamp_found_count if 'stamp_found_count' in dir() else len(existing_reviewed)
        if files_with_stamp > 0 and position_correct_count == files_with_stamp:
            print(f"PASS: Component 4 — All {position_correct_count} stamps in top-right position (0.20 pts)")
            total_score += 0.20
        elif position_correct_count > 0 and files_with_stamp > 0:
            partial = 0.20 * (position_correct_count / files_with_stamp)
            print(f"PARTIAL: Component 4 — {position_correct_count}/{files_with_stamp} stamps correctly positioned ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No stamps in correct top-right position")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
