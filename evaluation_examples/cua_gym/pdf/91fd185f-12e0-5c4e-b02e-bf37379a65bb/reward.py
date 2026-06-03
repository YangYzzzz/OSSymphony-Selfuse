"""
Reward Script: Resize all pages of mixed_sizes.pdf to uniform A4 (595x842 points)
Task ID: pdf_ro_037
Domain: pdf
Scoring:
  Component 1 (0.15): Output file exists and is a valid PDF
  Component 2 (0.20): Page count is exactly 15
  Component 3 (0.30): All pages have A4 width (~595 pts)
  Component 4 (0.25): All pages have A4 height (~842 pts)
  Component 5 (0.10): Content preserved — text extractable from representative pages
"""

import os
import fitz  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_037'

# A4 dimensions in points
A4_WIDTH = 595.0
A4_HEIGHT = 842.0
# Tolerance for page size comparison (1 point tolerance)
SIZE_TOLERANCE = 2.0


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists and is a valid PDF (0.15 points)
    # This is task-introduced: uniform_a4.pdf does not exist in initial_env
    try:
        doc = fitz.open(file_path)
        if doc.page_count > 0:
            print(f"PASS: Component 1 — File exists and is valid PDF ({len(doc)} pages) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — PDF has 0 pages")
    except Exception as e:
        print(f"FAIL: Component 1 — Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Page count is exactly 15 (0.20 points)
    try:
        page_count = len(doc)
        if page_count == 15:
            print(f"PASS: Component 2 — Page count is 15 (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Expected 15 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All pages have A4 width ~595 points (0.30 points)
    try:
        pages_with_correct_width = 0
        width_issues = []
        for i in range(len(doc)):
            page = doc[i]
            w = page.rect.width
            if abs(w - A4_WIDTH) <= SIZE_TOLERANCE:
                pages_with_correct_width += 1
            else:
                width_issues.append(f"Page {i}: width={w:.1f}")

        if pages_with_correct_width == len(doc) and len(doc) > 0:
            print(f"PASS: Component 3 — All {len(doc)} pages have A4 width (~595 pts) (0.30 pts)")
            total_score += 0.30
        elif pages_with_correct_width > 0:
            # Partial credit: proportion of pages with correct width
            partial = 0.30 * (pages_with_correct_width / len(doc))
            print(f"PARTIAL: Component 3 — {pages_with_correct_width}/{len(doc)} pages have A4 width ({partial:.2f} pts)")
            if width_issues:
                print(f"  Issues: {width_issues[:5]}")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No pages have A4 width. Issues: {width_issues[:5]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All pages have A4 height ~842 points (0.25 points)
    try:
        pages_with_correct_height = 0
        height_issues = []
        for i in range(len(doc)):
            page = doc[i]
            h = page.rect.height
            if abs(h - A4_HEIGHT) <= SIZE_TOLERANCE:
                pages_with_correct_height += 1
            else:
                height_issues.append(f"Page {i}: height={h:.1f}")

        if pages_with_correct_height == len(doc) and len(doc) > 0:
            print(f"PASS: Component 4 — All {len(doc)} pages have A4 height (~842 pts) (0.25 pts)")
            total_score += 0.25
        elif pages_with_correct_height > 0:
            partial = 0.25 * (pages_with_correct_height / len(doc))
            print(f"PARTIAL: Component 4 — {pages_with_correct_height}/{len(doc)} pages have A4 height ({partial:.2f} pts)")
            if height_issues:
                print(f"  Issues: {height_issues[:5]}")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — No pages have A4 height. Issues: {height_issues[:5]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Content preserved — text extractable from representative pages (0.10 points)
    # Check pages from each original size group (Letter, Legal, A3) to ensure content survived
    try:
        sample_pages = [0, 5, 10]  # One from each original size group
        pages_with_text = 0
        for idx in sample_pages:
            if idx < len(doc):
                text = doc[idx].get_text().strip()
                if len(text) > 50:  # Meaningful text content
                    pages_with_text += 1
                else:
                    print(f"  Page {idx}: text length only {len(text)} chars")

        if pages_with_text == len(sample_pages):
            print(f"PASS: Component 5 — Content preserved on sample pages {sample_pages} (0.10 pts)")
            total_score += 0.10
        elif pages_with_text > 0:
            partial = 0.10 * (pages_with_text / len(sample_pages))
            print(f"PARTIAL: Component 5 — {pages_with_text}/{len(sample_pages)} sample pages have text ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — No text found on sample pages {sample_pages}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/uniform_a4.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
