"""
Reward Script: Merge PDFs into portfolio with bookmarks and embedded attachments
Task ID: pdf_gf2_036
Domain: pdf
Scoring:
  Component 1 (0.3): File exists with correct page count (11 pages)
  Component 2 (0.3): TOC/bookmarks match expected entries
  Component 3 (0.4): 3 embedded file attachments present with correct names
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_036'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be loadable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Page count is 11 (resume 2 + cover_letter 1 + work_samples 8) (0.3 points)
    try:
        page_count = doc.page_count
        if page_count == 11:
            print(f"PASS: Component 1 — Page count is 11 (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Expected 11 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Bookmarks (TOC) match expected entries (0.3 points)
    # Expected: [[1, "Resume", 1], [1, "Cover Letter", 3], [1, "Work Samples", 4]]
    try:
        toc = doc.get_toc()
        expected_toc = [
            [1, "Resume", 1],
            [1, "Cover Letter", 3],
            [1, "Work Samples", 4],
        ]

        if len(toc) >= 3:
            # Check each expected bookmark exists (order and page numbers)
            matches = 0
            for exp in expected_toc:
                for entry in toc:
                    if (entry[0] == exp[0] and
                        entry[1].strip().lower() == exp[1].strip().lower() and
                        entry[2] == exp[2]):
                        matches += 1
                        break

            if matches == 3:
                print(f"PASS: Component 2 — All 3 bookmarks found: Resume@1, Cover Letter@3, Work Samples@4 (0.3 pts)")
                total_score += 0.3
            elif matches >= 2:
                partial = round(0.3 * matches / 3, 2)
                print(f"PARTIAL: Component 2 — {matches}/3 bookmarks matched ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — Only {matches}/3 bookmarks matched. TOC found: {toc}")
        else:
            print(f"FAIL: Component 2 — Expected at least 3 bookmarks, found {len(toc)}. TOC: {toc}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Embedded file attachments (0.4 points)
    # Expected: 3 attachments named resume.pdf, cover_letter.pdf, work_samples.pdf
    try:
        emb_count = doc.embfile_count()
        expected_names = {"resume.pdf", "cover_letter.pdf", "work_samples.pdf"}

        if emb_count >= 3:
            found_names = set()
            for i in range(emb_count):
                info = doc.embfile_info(i)
                name = info.get("name", "")
                found_names.add(name)

            matched_names = expected_names.intersection(found_names)
            if len(matched_names) == 3:
                print(f"PASS: Component 3 — All 3 file attachments found: {sorted(matched_names)} (0.4 pts)")
                total_score += 0.4
            elif len(matched_names) >= 2:
                partial = round(0.4 * len(matched_names) / 3, 2)
                print(f"PARTIAL: Component 3 — {len(matched_names)}/3 attachments matched ({partial} pts). Found: {found_names}")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — Expected attachments {expected_names}, found names: {found_names}")
        else:
            print(f"FAIL: Component 3 — Expected at least 3 embedded files, found {emb_count}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/portfolio/complete_portfolio.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
